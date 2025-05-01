from crewai import Agent, LLM

llm = LLM(
    model="openai/local-qwen14b",
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
    )


ProductManager = Agent(
    role='Product Manager',
    goal='Turn user intent into a clear project specification and roadmap',
    backstory=(
        "You are a detail-oriented product manager with experience in agile software teams. "
        "You excel at turning vague ideas into well-defined, achievable plans with clear deliverables."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=True,
    tools=[],  # we can add tools like file writing later
)
