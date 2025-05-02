import logging
from fastapi import FastAPI, Request, APIRouter, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from src.server.llm import BACKENDS, default_backend_name, build_response
from src.server.proxy import ProxyBackend

# FastAPI application setup
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metadata router
meta_router = APIRouter()


@meta_router.get("/api/v1/chats/")
async def get_chats(page: int = 1, page_size: int = 10):
    all_chats = [
        {"id": 1, "title": "Chat 1", "created_at": "2025-04-19T10:00:00Z"},
        {"id": 2, "title": "Chat 2", "created_at": "2025-04-19T11:00:00Z"},
        {"id": 3, "title": "Chat 3", "created_at": "2025-04-19T12:00:00Z"},
    ]
    start, end = (page - 1) * page_size, page * page_size
    return JSONResponse({"object": "list", "data": all_chats[start:end], "page": page, "page_size": page_size, "total": len(all_chats)})


@meta_router.get("/api/tags")
@meta_router.get("/v1/tags")
async def get_tags():
    return JSONResponse({"object": "list", "data": []})


@meta_router.get("/api/version")
@meta_router.get("/v1/version")
async def get_version():
    return JSONResponse({"version": "0.5.8"})


@meta_router.get("/v1/models")
async def get_models():
    return JSONResponse({
        "object": "list",
        "data": [{"id": "my-apprentice-model", "object": "model", "owned_by": "me", "permissions": []}]
    })

# Chat router
chat_router = APIRouter()


@chat_router.post("/v1/chat/completions")
async def chat_completions(
    request: Request,
    stream: bool = Query(False, description="Stream mode or single response")
):
    body = await request.json()
    logging.info("request: %s", body)
    messages = body.get("messages", [])
    user_input = messages[-1]["content"] if messages else "Hello?"

    selected = 'proxy'
    backend_impl = ProxyBackend('http://localhost:9222')
    if not backend_impl:
        raise HTTPException(status_code=400,
                            detail=f"Unknown backend '{selected}'")

    if not stream:
        logging.info("request %s", user_input)
        content = await backend_impl.invoke(user_input)
        logging.info("response from %s: %s", selected, content)
        return JSONResponse(build_response(content))

    return StreamingResponse(backend_impl.stream(user_input), media_type="text/event-stream")

# Register routers
app.include_router(meta_router)
app.include_router(chat_router)
