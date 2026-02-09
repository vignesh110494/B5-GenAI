
#vector using huggingface model using chroma vector database

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Sample documents
texts = [
    "LangChain is a framework for building LLM-powered applications.",
    "ChromaDB is a vector database for storing embeddings.",
    "Embeddings convert text into numerical vectors."
]

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create Chroma vector store (in-memory)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)