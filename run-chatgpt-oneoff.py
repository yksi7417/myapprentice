import asyncio
from playwright.async_api import async_playwright
import time


async def wait_for_full_response(page, selector="div.markdown", timeout=30, settle_time=2):
    start = time.time()
    last_content = ""
    last_change = time.time()

    while time.time() - start < timeout:
        elements = await page.locator(selector).all_text_contents()
        if not elements:
            await asyncio.sleep(0.5)
            continue

        content = elements[-1].strip()
        if content != last_content:
            last_content = content
            last_change = time.time()
        elif time.time() - last_change > settle_time:
            return content

        await asyncio.sleep(0.5)

    raise TimeoutError("Timeout waiting for full response.")


async def main(prompt: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        await asyncio.sleep(0.5)
        await page.fill('div#prompt-textarea.ProseMirror[contenteditable="true"]', prompt)
        await asyncio.sleep(0.5)
        await page.keyboard.press("Enter")

        result = await wait_for_full_response(page)
        return result


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = asyncio.run(main(user_input))
        print(f"Assistant: {result}")
