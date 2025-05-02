from crewai_tools import BaseTool
from playwright.async_api import async_playwright
import asyncio


class ChatGPTWebTool(BaseTool):
    name = "ChatGPT Web UI Tool"
    description = "Use this tool to input a prompt into chat.openai.com and return the response."

    async def _ask_chatgpt(self, prompt: str) -> str:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)  # Change to True when stable
            context = await browser.new_context(storage_state="playwright_auth.json")  # use saved login
            page = await context.new_page()
            await page.goto("https://chat.openai.com")

            await page.wait_for_selector("textarea", timeout=15000)
            await page.fill("textarea", prompt)
            await page.keyboard.press("Enter")

            # Wait for response to appear
            await page.wait_for_selector("div.markdown", timeout=30000)

            # Get all response blocks
            responses = await page.locator("div.markdown").all_text_contents()
            await browser.close()
            return responses[-1].strip() if responses else "No response found."

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
