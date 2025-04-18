import os
from dotenv import load_dotenv
import streamlit as st

# LangChain imports
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
# load environment
load_dotenv()
default_emb_model = "sentence-transformers/all-MiniLM-L6-v2"
default_hf_model = "google/flan-t5-small"
hf_token = os.environ["HF_API_TOKEN"]
hf_model = os.environ.get("HF_MODEL_NAME", default=default_hf_model)
emb_model = os.environ.get("EMBED_MODEL_NAME", default=default_emb_model)

tokenizer = AutoTokenizer.from_pretrained(hf_model)
model = AutoModelForSeq2SeqLM.from_pretrained(hf_model)
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
)
llm = HuggingFacePipeline(pipeline=pipe)

st.markdown("# Test LLM")
st.text_input("Model Name", value=hf_model, key="model_name")
st.text_input("Embedding Model Name", value=emb_model, key="emb_model_name")
st.text_input("Hugging Face API Token", value=hf_token, key="hf_token")
question = st.text_input("Question",
                         value="What does LangChain do?", key="question")

# initialize LLM
# initialize embeddings + a simple vector store
embeddings = HuggingFaceEmbeddings(model_name=emb_model)
vectorstore = Chroma(embedding_function=embeddings)

# build a simple RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# demo: add some docs, then ask a question
docs = [
    "LangChain makes it easy to integrate LLMs with data sources.",
    "Hugging Face hosts hundreds of models you can pull in via API."
]
vectorstore.add_texts(docs)

question = "What does LangChain do?"
answer = qa.invoke(question)

st.markdown("### Answer:")
st.text_area("Answer", value=answer, key="answer", height=200)
