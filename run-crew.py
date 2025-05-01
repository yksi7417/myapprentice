from crewai import Crew
from crewai import Task
from src.agents.product_manager import ProductManager

# import os
# os.environ['LITELLM_API_KEY'] = 'sk-local'
# os.environ['LITELLM_API_BASE'] = 'http://localhost:8000/v1'
# os.environ['LITELLM_MODEL'] = '.\\models\\DeepSeek-R1-Distill-Qwen-14B-Q8_0.gguf'

# os.environ["OPENAI_ORGANIZATION"] = "your-org-id"       # OPTIONAL
# os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"     # OPTIONAL
# os.environ['OPENAI_MODEL'] = '.\\models\\DeepSeek-R1-Distill-Qwen-14B-Q8_0.gguf'
# os.environ['OPENAI_API_KEY'] = 'sk-local'


def main():
    # Replace this with user input
    user_command = "Build a single-player mahjong game with Cantonese rules"
    print("working on:", user_command)

    DefineSpecs = Task(
        description=(
            f"Analyze the user's request: '{user_command}'. "
            "Turn it into a product spec with goal, scope, features, and milestones."
        ),
        expected_output=(
            "A bullet-point software spec with:\n"
            "- Objective\n- Key features\n- Milestones\n- Assumptions\n- Final product description"
        ),
        agent=ProductManager,
    )

    crew = Crew(
        agents=[ProductManager],
        tasks=[DefineSpecs],
        verbose=True
    )

    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
