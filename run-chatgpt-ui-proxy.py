from crewai import Crew
from src.agents.chatgpt_ui_agent import ChatGPTUIAgent

crew = Crew(
    agents=[ChatGPTUIAgent],
    tasks=[{
        "description": "Use ChatGPT UI to answer: 'Summarize quantum entanglement in simple terms'",
        "agent": ChatGPTUIAgent
    }],
    verbose=True
)

if __name__ == "__main__":
    result = crew.run()
    print("OpenAI format result:\n", result)
