from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


from dotenv import load_dotenv
import streamlit as st
import os
from PyPDF2 import PdfReader

load_dotenv()

llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4.1-mini",
    temperature=0.2
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

st.title("RAG App: Ask Your PDF Anything")

uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

if uploaded_file is not None:

    raw_text = ""

    try:
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                raw_text += text

    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")

    if not raw_text.strip():
        st.error(
            "Could not extract any text from this PDF.\n\n"
            "It may be a scanned image PDF with no selectable text.\n\n"
            "Please use a text-based PDF or run OCR (Optional Character Recognition) first."
        )

    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = text_splitter.split_text(raw_text)

        if not chunks:
            st.error("No text chunks found. Nothing to embed.")
        else:
            st.success(f"Loaded! Split into {len(chunks)} chunks.")

            vector_store = FAISS.from_texts(chunks, embedding=embeddings)

            retriever = vector_store.as_retriever()

            # Prompt
            prompt = ChatPromptTemplate.from_template("""
            Answer the question based only on the context below:

            Context:
            {context}

            Question:
            {question}
            """)
            
            #lcel rag chain
            rag_chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm
            | StrOutputParser()
        )

           

            query = st.text_input("Ask a question about your PDF:")
            

            if query:
                with st.spinner("Thinking..."):
                    answer = rag_chain.invoke(query)

                st.subheader("Answer")
                st.write(answer)
