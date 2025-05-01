import os
from src.agents.product_manager import ProductManager
from src.agents.architect import Architect
from src.agents.engineer import Engineer
from crewai import Crew, Task
from datetime import datetime

OUTPUT_DIR = "output"
LOG_FILE = "logs/log.txt"


def log(message: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")
    print(message)


def checkpoint_exists(name: str):
    return os.path.exists(f"{OUTPUT_DIR}/{name}.md")


def write_output(name: str, content: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = f"{OUTPUT_DIR}/{name}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"✅ Saved {name} output to {path}")


def run_task(agent, task_desc, output_name, force=False):
    if checkpoint_exists(output_name) and not force:
        log(f"⏩ Skipping {output_name}, already exists.")
        return open(f"{OUTPUT_DIR}/{output_name}.md", "r", encoding="utf-8").read()

    log(f"🚀 Running {output_name}...")

    task = Task(
        description=task_desc,
        expected_output=f"Please output your result in markdown format for {output_name}.",
        agent=agent
    )

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    joined_output = "\n\n".join(result.tasks_output)

    write_output(output_name, joined_output)
    return joined_output


def run_test_feedback_loop(spec_output, engineer_agent, pm_agent, force=False):
    # Phase 1: Engineer generates initial BDD-style test cases
    initial_test_desc = (
        f"Use the following product specification to write Python unit tests in a BDD style "
        f"(Given/When/Then) using `pytest-bdd` or `behave` syntax.\n\n"
        f"{spec_output}\n\n"
        f"Output tests in `.feature` files or `test_*.py` files with enough coverage for all listed milestones and features."
    )
    test_output = run_task(
        agent=engineer_agent,
        task_desc=initial_test_desc,
        output_name="tests_initial",
        force=force
    )

    # Phase 2: Product Manager reviews the test cases
    review_desc = (
        f"Review the following BDD-style test cases and check if they align with this product specification.\n\n"
        f"Specification:\n{spec_output}\n\n"
        f"Test Cases:\n{test_output}\n\n"
        f"Provide detailed feedback on any missing behavior, misaligned logic, or additional tests required."
    )
    review_output = run_task(
        agent=pm_agent,
        task_desc=review_desc,
        output_name="tests_feedback",
        force=force
    )

    # Phase 3: Engineer updates the test cases based on feedback
    refinement_desc = (
        f"Improve the BDD test cases below based on the feedback from the Product Manager.\n\n"
        f"Original Test Cases:\n{test_output}\n\n"
        f"PM Feedback:\n{review_output}\n\n"
        f"Ensure all expected behaviors and edge cases are now covered. Use clear Given/When/Then format."
    )
    refined_output = run_task(
        agent=engineer_agent,
        task_desc=refinement_desc,
        output_name="tests_final",
        force=force
    )

    return test_output, review_output, refined_output


def main(user_command: str, force_all=False):
    log(f"\n=== Starting Crew Pipeline ===")
    log(f"🎯 User Command: {user_command}")

    # Step 1: Product Manager
    pm_output = run_task(
        agent=ProductManager,
        task_desc=f"Analyze this command: '{user_command}'. Turn it into a clear specification.",
        output_name="specification",
        force=force_all
    )

    # Step 2: Architect
    arch_output = run_task(
        agent=Architect,
        task_desc=f"Use the following specification to design architecture:\n\n{pm_output}",
        output_name="architecture",
        force=force_all
    )

    # Step 2: Test Cases Generation and Feedback Loop
    (test_output, review_output, refined_output) = run_test_feedback_loop(
        spec_output=pm_output,
        engineer_agent=Engineer,
        pm_agent=ProductManager)

    log("🎉 Pipeline completed successfully.")
    return pm_output, arch_output


if __name__ == "__main__":
    command = "Build a single-player mahjong game with Cantonese rules"
    main(command, force_all=False)
