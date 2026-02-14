import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API Key
load_dotenv()

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Simple RAG App")
st.title("📄 Ask Your Document")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
query = st.text_input("Ask a question about the document")

if uploaded_file:

    print("✅ File uploaded successfully")

    # Save file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.info("📂 Loading document...")
    print("📂 Loading document...")

    # -------------------------------
    # Load Document
    # -------------------------------
    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()
    print(f"✅ Document loaded. Pages: {len(documents)}")

    st.info("✂ Splitting document into chunks...")
    print("✂ Splitting document...")

    # -------------------------------
    # Split into Chunks
    # -------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = splitter.split_documents(documents)
    print(f"✅ Total chunks created: {len(docs)}")

    st.info("🧠 Creating embeddings and vector store...")
    print("🧠 Creating embeddings...")

    # -------------------------------
    # Create Embeddings
    # -------------------------------
    embeddings = OpenAIEmbeddings()

    # -------------------------------
    # Create Vector Store
    # -------------------------------
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    print("✅ Vector store created successfully")

    # -------------------------------
    # Create LLM
    # -------------------------------
    print("🤖 Initializing LLM...")
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0.2
    )
    print("✅ LLM initialized")

    # -------------------------------
    # Create Prompt
    # -------------------------------
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {question}
    """)

    # -------------------------------
    # Create LCEL RAG Chain
    # -------------------------------
    print("🔗 Creating RAG chain...")
    rag_chain = (
        {
            "context": retriever,
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    print("✅ RAG chain ready")

    # -------------------------------
    # Answer Question
    # -------------------------------
    if query:

        print("🚀 Running RAG pipeline...")

        # Spinner while processing
        with st.spinner("🔄 Generating answer... Please wait"):
            response = rag_chain.invoke(query)

        print("✅ Response generated successfully")

        st.success("✅ Answer generated")
        st.subheader("Answer:")
        st.write(response)
