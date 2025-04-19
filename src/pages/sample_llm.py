import os
import streamlit as st
import torch

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

# ========== SETUP ==========
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


MODEL_PATH = os.environ.get("HF_MODEL_PATH",
                            "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf")
EMBED_PATH = os.environ.get("EMBED_MODEL_PATH", "./models/all-mpnet-base-v2")

st.title("🔍 Ask Your Offline LLM")

st.markdown(f"CUDA? {torch.cuda.is_available()}, version:{torch.version.cuda}")

question = st.text_input("Question", value="What does LangChain do?")

# ========== LOAD LLM ==========
llm = LlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.0,
    max_tokens=512,
    n_ctx=32768,
    n_threads=8,
    verbose=False,
    n_gpu_layers=32,
    use_mlock=True  # prevent model from being swapped out
)

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
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# ========== ANSWER ==========
if question:
    answer = qa.invoke(question)
    st.markdown("### 🧠 Answer")
    st.text_area("Answer", value=answer, height=200)
