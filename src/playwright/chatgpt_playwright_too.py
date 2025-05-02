from crewai_tools import BaseTool
from playwright.async_api import async_playwright
import asyncio


class ChatGPTWebTool(BaseTool):
    name = "ChatGPT Web UI Tool"
    description = "Use this tool to input a prompt into chat.openai.com and return the response."

    async def _ask_chatgpt(self, prompt: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")

            # Get first page in the first context
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()

            await page.goto("https://chat.openai.com")
            await page.fill("textarea", "Summarize black holes in simple terms")
            await page.keyboard.press("Enter")

            await page.wait_for_selector("div.markdown")
            response = await page.inner_text("div.markdown")
            print("Response:", response)
            return response[-1].strip() if response else "No response found."

    def _run(self, prompt: str) -> dict:
        output = asyncio.run(self._ask_chatgpt(prompt))
        return {
            "id": "chatcmpl-ui-001",
            "object": "chat.completion",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output,
                },
                "finish_reason": "stop"
            }],
            "model": "gpt-4-ui",
        }
