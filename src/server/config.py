import os
from dotenv import load_dotenv

load_dotenv()

HF_MODEL_PATH = os.getenv("HF_MODEL_PATH")
CONTEXT_SIZE = int(os.getenv("CONTEXT_SIZE", 2048))
PORT = int(os.getenv("PORT", 11434))
CHATGPT_PROXY_PORT = int(os.getenv("CHATGPT_PROXY_PORT", 19394))
EMBED_PATH = os.getenv("EMBED_MODEL_PATH", "./models/all-mpnet-base-v2")