from crewai import Agent, LLM

ProductManager = Agent(
    role='Product Manager',
    goal='Turn user intent into a clear project specification and roadmap',
    backstory=(
        "You are a detail-oriented product manager with experience in agile software teams. "
        "You excel at turning vague ideas into well-defined, achievable plans with clear deliverables."
    ),
    llm=LLM(model="./models/DeepSeek-R1-Distill-Qwen-14B-Q8_0.gguf", base_url="http://localhost:11434/"),
    verbose=True,
    allow_delegation=True,
    tools=[],  # we can add tools like file writing later
)
