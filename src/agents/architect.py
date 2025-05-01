from crewai import Agent, LLM

llm = LLM(
    model="openai/local-qwen14b",
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    )


Architect = Agent(
    role='Software Architect',
    goal='Design a clean, modular, and extensible architecture based on the given product specification',
    backstory=(
        "You are a veteran software architect known for designing robust, scalable systems. "
        "You specialize in converting product specs into clear blueprints, breaking down responsibilities into logical modules."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False,
)
