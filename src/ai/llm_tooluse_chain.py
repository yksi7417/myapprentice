from src.server.config import HF_MODEL_PATH, CONTEXT_SIZE
import torch
import logging

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import LlamaCpp

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

    # Prompt accepts a system_prompt and user query for tool use
    prompt = PromptTemplate.from_template("{system_prompt}\n\nUser: {query}")
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )
    return chain
