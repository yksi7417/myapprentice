from config import HF_MODEL_PATH, CONTEXT_SIZE, EMBED_PATH
import torch
import logging

from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import LlamaCpp

# to turn off telemetry for chromadb
from chromadb import Client
from chromadb.config import Settings
chromadb_settings = Settings(
    anonymized_telemetry=False,
)

logger = logging.getLogger(__name__)


def build_chain():
    llm = LlamaCpp(
        model_path=HF_MODEL_PATH,
        temperature=0.0,
        max_tokens=512,
        n_ctx=CONTEXT_SIZE,
        n_threads=8,
        verbose=False,
        n_gpu_layers=32,
        n_batch=64,
        use_mlock=True
    )

    logging.info(f"CUDA? {torch.cuda.is_available()},version:{torch.version.cuda}")

    # ========== LOAD VECTOR STORE ==========
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_PATH,
                                       model_kwargs={"device": "cuda"},
                                       encode_kwargs={"device": "cuda"})

    client = Client(settings=chromadb_settings)
    vectorstore = Chroma(client=client, embedding_function=embeddings)

    # Example documents
    docs = [
        "LangChain makes it easy to integrate LLMs with data sources.",
        "Hugging Face hosts hundreds of models you can pull in via API.",
        "Llama.cpp allows running LLM locally in quantized formats."
    ]
    vectorstore.add_texts(docs)

    # ========== BUILD QA CHAIN ==========
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    return chain
