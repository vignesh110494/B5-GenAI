import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    PyPDFLoader
)
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ----------------------------------
# Load environment variables
# ----------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ----------------------------------
# Load documents (MULTI SOURCE)
# ----------------------------------
docs = []

docs += PyPDFLoader("data/genai_future.pdf").load()
docs += TextLoader("data/genai_overview.txt ").load()
docs += CSVLoader("data/genai_usecases.csv").load()

# ----------------------------------
# Split documents
# ----------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# ----------------------------------
# Embeddings + Vector Store
# ----------------------------------
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# ----------------------------------
# LLM
# ----------------------------------
llm = ChatOpenAI(temperature=0)

# ----------------------------------
# FUSION QUERY EXPANSION
# ----------------------------------
def generate_fusion_queries(question):
    return [
        question,
        f"Explain the concept related to: {question}",
        f"Common misconceptions about {question}",
        f"Historical clarification of {question}",
    ]

# ----------------------------------
# FUSION RETRIEVAL
# ----------------------------------
def fusion_retrieve(question):
    queries = generate_fusion_queries(question)
    fused_docs = {}

    for q in queries:
        retrieved = retriever.get_relevant_documents(q)
        for doc in retrieved:
            fused_docs[doc.page_content] = doc

    return list(fused_docs.values())

# ----------------------------------
# FINAL ANSWER GENERATION
# ----------------------------------
def fusion_rag_answer(question):
    fused_docs = fusion_retrieve(question)

    context = "\n\n".join(doc.page_content for doc in fused_docs)

    prompt = f"""
You are a factual assistant.
Do not hallucinate.
If the answer does not exist, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
"""

    return llm.invoke(prompt).content

# ----------------------------------
# RUN QUERY
# ----------------------------------
if __name__ == "__main__":
    question = "write en essay on AI jobs ?"
    answer = fusion_rag_answer(question)
    print("\nFinal Answer:\n", answer)

