from src.server.config import HF_MODEL_PATH, CONTEXT_SIZE
import torch
import logging

from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate

logger = logging.getLogger(__name__)


def build_chain():
    llm = LlamaCpp(
        model_path=HF_MODEL_PATH,
        n_ctx=CONTEXT_SIZE,
        verbose=True,
        n_gpu_layers=-1,
        use_mlock=True
    )

    logging.info(f"CUDA? {torch.cuda.is_available()}, version: {torch.version.cuda}")

    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser: {query}")
    chain = prompt | llm
    return chain
