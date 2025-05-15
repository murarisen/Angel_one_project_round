from pathlib import Path
import streamlit as st
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# -------- CONFIGURATION --------
VDB_DIR      = Path("vectordb")          # created by build_index.py
EMBED_MODEL  = "all-minilm"    
LLM_MODEL    = "llama3"               

# -------- LOAD QA CHAIN --------
@st.cache_resource(show_spinner=False)
def load_qa_chain() -> RetrievalQA | None:
    if not (VDB_DIR / "index.faiss").exists():
        return None
    db = FAISS.load_local(
        VDB_DIR.as_posix(),
        OllamaEmbeddings(model=EMBED_MODEL),
        allow_dangerous_deserialization=True,
    )
    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = Ollama(model=LLM_MODEL, temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=False,   # no source docs returned
    )

qa_chain = load_qa_chain()

# -------- STREAMLIT CHAT UI --------
st.set_page_config(page_title="HR-Policy Chatbot")
st.title("HR-Policy Chatbot")
st.caption("Ask anything about Leave • Remote Work • Dress Code • Harassment • Disciplinary Action • Appraisals • IT and Data Security policies...")

if qa_chain is None:
    st.error("Index not found. Run build_index.py once, then refresh.")
    st.stop()

# Keep conversation in session_state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "...", "content": "..."}

# Display previous messages
for msg in st.session_state.chat_history:
    avatar = "" if msg["role"] == "assistant" else ""
    st.markdown(f"**{avatar} {msg['role'].capitalize()}:** {msg['content']}")

# Chat input
user_question = st.chat_input("Ask your question…")

if user_question:
    # 1) Show user message
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    st.markdown(f"** You:** {user_question}")

    # 2) Generate answer
    with st.spinner("Thinking…"):
        res = qa_chain({"query": user_question})
        answer = res["result"].strip()

    # 3) Show assistant answer
    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.markdown(f"** Bot:** {answer}")

st.markdown("---")
st.caption("Powered by FAISS · LangChain · Ollama")
