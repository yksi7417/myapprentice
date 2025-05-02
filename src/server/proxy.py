from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from playwright.async_api import async_playwright
import logging
import time
import json
import asyncio

CHROME_CDP_URL = "http://localhost:9222"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


async def invoke_chatgpt(prompt: str):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(CHROME_CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        await asyncio.sleep(0.5)
        await page.fill('div#prompt-textarea.ProseMirror[contenteditable="true"]', prompt)
        await asyncio.sleep(0.5)
        await page.keyboard.press("Enter")

        result = await wait_for_full_response(page)
        return result


@app.get("/api/v1/chats/")
async def get_chats(page: int = 1, page_size: int = 10):
    # Example chat data (replace with your database or storage logic)
    all_chats = [
        {"id": 1, "title": "Chat 1", "created_at": "2025-04-19T10:00:00Z"},
        {"id": 2, "title": "Chat 2", "created_at": "2025-04-19T11:00:00Z"},
        {"id": 3, "title": "Chat 3", "created_at": "2025-04-19T12:00:00Z"},
    ]

    # Paginate the chats
    start = (page - 1) * page_size
    end = start + page_size
    paginated_chats = all_chats[start:end]

    return JSONResponse(content={
        "object": "list",
        "data": paginated_chats,
        "page": page,
        "page_size": page_size,
        "total": len(all_chats),
    })


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    logging.info("request: %s", body)
    stream = body.get("stream", False)
    messages = body.get("messages", [])

    user_input = messages[-1]["content"] if messages else "Hello?"

    if not stream:
        result = await invoke_chatgpt(user_input)

        json_response = {
            "id": "chatcmpl-langchain-001",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "my-apprentice-model",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result,
                    },
                    "logprobs": None,
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
        logging.info("response: %s", result["result"])
        return JSONResponse(content=json_response)

    # STREAMING RESPONSE
    async def event_stream():
        result = await invoke_chatgpt(user_input)
        content = result

        # Role chunk
        yield f"data: {json.dumps({'id': 'chatcmpl-001','object': 'chat.completion.chunk','choices': [{'delta': {'role': 'assistant'}, 'index': 0}]})}\n\n"
        await asyncio.sleep(0.05)

        # Token-by-token stream
        for word in content.split():
            chunk = {
                "id": "chatcmpl-001",
                "object": "chat.completion.chunk",
                "choices": [{
                    "delta": {"content": word + " "},
                    "index": 0
                }]
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.05)

        # Final stop chunk
        stop_chunk = {
            "id": "chatcmpl-001",
            "object": "chat.completion.chunk",
            "choices": [{
                "delta": {},
                "index": 0,
                "finish_reason": "stop"
            }]
        }
        yield f"data: {json.dumps(stop_chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/tags")
@app.get("/v1/tags")
async def get_tags():
    return JSONResponse(content={
            "object": "list",
            "data": []})


@app.get("/api/version")
@app.get("/v1/version")
async def get_version():
    return JSONResponse(content={"version": "0.5.8"})


@app.get("/v1/models")
async def get_models():
    return JSONResponse(content={
        "object": "list",
        "data": [
            {
                "id": "my-proxy-model",
                "object": "model",
                "owned_by": "me",
                "permissions": []}]
    })
