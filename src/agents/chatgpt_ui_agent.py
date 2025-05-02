from crewai import Agent
from src.playwright.chatgpt_playwright_tool import ChatGPTWebTool

chatgpt_tool = ChatGPTWebTool()

ChatGPTUIAgent = Agent(
    role="Web ChatGPT Interface",
    goal="Extract answers from ChatGPT UI",
    backstory="Specializes in navigating ChatGPT's web interface.",
    tools=[chatgpt_tool],
    verbose=True
)
