from crewai import Agent, LLM

llm = LLM(
    model="openai/local-qwen14b",
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    )

Engineer = Agent(
    role='Software Engineer',
    goal='Write clean and modular code that follows the software architecture plan.',
    backstory=(
        "You are a disciplined and efficient senior software engineer that follows BDD best practices. "
        "You follow system design specs and write well-organized, documented code, using test driven approach "
        "that is easy to extend and test."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)
