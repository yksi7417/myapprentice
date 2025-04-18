import os
import streamlit as st

from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import LlamaCpp

# ========== SETUP ==========
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
MODEL_PATH = "./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

st.set_page_config(page_title="🦙 Offline LLM QA")
st.title("🔍 Ask Your Offline LLM")

question = st.text_input("Question", value="What does LangChain do?")

# ========== LOAD LLM ==========
llm = LlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.0,
    max_tokens=512,
    n_ctx=2048,
    n_threads=8,
    verbose=False,
    use_mlock=True  # prevent model from being swapped out
)

# ========== LOAD VECTOR STORE ==========
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
vectorstore = Chroma(embedding_function=embeddings)

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
