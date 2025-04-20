from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.server.llm_chain import build_chain
import logging
import time


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for your use case
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chain = build_chain()


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    logging.info("request: %s", body)
    messages = body.get("messages", [])

    user_input = messages[-1]["content"] if messages else "Hello?"

    response = chain.invoke({"query": user_input})

    json_response = JSONResponse({
        "id": "chatcmpl-langchain-001",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "my-apprentice-model",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response["result"],
                },
                "finish_reason": "stop"
            }
        ]
    })

    logging.info("response: %s", response["result"])

    return json_response


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
                "id": "my-apprentice-model",
                "object": "model",
                "owned_by": "me",
                "permissions": []}]
    })