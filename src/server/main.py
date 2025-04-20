from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_chain import build_chain
from config import PORT
import uvicorn
import logging
import pprint
import time

# 1. Set the global log level (DEBUG shows everything)
logging.basicConfig(
    level=logging.INFO,  # or logging.INFO if you want less verbosity
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


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
    logging.info("request: %s", request.body())
    body = await request.json()
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=PORT, reload=True)
