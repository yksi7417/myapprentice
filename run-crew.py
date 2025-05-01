import os
from src.agents.product_manager import ProductManager
from src.agents.architect import Architect
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
    write_output(output_name, result.tasks_output)
    return result.tasks_output


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

    log("🎉 Pipeline completed successfully.")
    return pm_output, arch_output


if __name__ == "__main__":
    command = "Build a single-player mahjong game with Cantonese rules"
    main(command, force_all=False)
