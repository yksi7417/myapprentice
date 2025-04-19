from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from llm_chain import build_chain
from config import PORT
import uvicorn

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
    messages = body.get("messages", [])

    user_input = messages[-1]["content"] if messages else "Hello?"

    response = chain.run({"question": user_input})

    return JSONResponse({
        "id": "chatcmpl-langchain-001",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "llama.cpp-langchain",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response,
                },
                "finish_reason": "stop"
            }
        ]
    })


@app.get("/api/tags")
@app.get("/v1/tags")
async def get_tags():
    return JSONResponse(content={[]})


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
