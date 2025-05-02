from typing import AsyncGenerator, Dict
from abc import ABC, abstractmethod
import os
import json
import asyncio
import time


# Default backend selection
default_backend_name = os.getenv("LLM_BACKEND", "chain")


class LLMBackend(ABC):
    @abstractmethod
    async def invoke(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        pass


# Helper to generate SSE token stream
async def generate_sse(content: str) -> AsyncGenerator[str, None]:
    header = {
        "id": "chatcmpl-001",
        "object": "chat.completion.chunk",
        "choices": [{"delta": {"role": "assistant"}, "index": 0}]
    }
    yield f"data: {json.dumps(header)}\n\n"
    await asyncio.sleep(0.05)
    for token in content.split():
        chunk = {
            "id": "chatcmpl-001",
            "object": "chat.completion.chunk",
            "choices": [{"delta": {"content": token + " "}, "index": 0}]
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        await asyncio.sleep(0.05)
    stop = {"id": "chatcmpl-001","object": "chat.completion.chunk","choices": [{"delta": {},"index": 0,"finish_reason": "stop"}]}
    yield f"data: {json.dumps(stop)}\n\n"
    yield "data: [DONE]\n\n"


def build_response(content: str) -> Dict:
    return {
        "id": "chatcmpl-langchain-001",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "my-apprentice-model",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "logprobs": None,
                "finish_reason": "stop"
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }


# Plugin registry
BACKENDS: Dict[str, LLMBackend] = {}
