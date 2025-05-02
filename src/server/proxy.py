import os
import time
import asyncio
from playwright.async_api import async_playwright
from src.server.llm import LLMBackend, BACKENDS, generate_sse


class ProxyBackend(LLMBackend):
    def __init__(self, cdp_url: str = None):
        self.cdp_url = cdp_url or os.getenv("CHROME_CDP_URL", "http://localhost:9222")

    async def invoke(self, prompt: str) -> str:
        prompt_selector = 'div#prompt-textarea.ProseMirror[contenteditable]'

        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(self.cdp_url)
            ctx = browser.contexts[0]
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()
            await asyncio.sleep(0.5)
            await page.fill(prompt_selector, prompt)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Enter")
            return await self._wait(page)

    async def _wait(self, page,
                    selector: str = "div.markdown",
                    timeout: int = 30,
                    settle_time: int = 2) -> str:

        start = time.time()
        last, last_change = "", time.time()

        while time.time() - start < timeout:
            elems = await page.locator(selector).all_text_contents()
            if not elems:
                await asyncio.sleep(0.5)
                continue
            txt = elems[-1].strip()
            if txt != last:
                last, last_change = txt, time.time()
            elif time.time() - last_change > settle_time:
                return txt
            await asyncio.sleep(0.5)
        raise TimeoutError("Timeout waiting for LLM response.")

    async def stream(self, prompt: str):
        content = await self.invoke(prompt)
        async for chunk in generate_sse(content):
            yield chunk


BACKENDS["proxy"] = ProxyBackend()
