"""Document loading, splitting, and vector store (FAISS/Chroma)."""

import tempfile
from pathlib import Path
from typing import List, Literal

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma


def load_documents_from_files(file_paths: List[str]) -> List[Document]:
    """Load PDF and TXT files into LangChain documents."""
    docs = []
    for path in file_paths:
        p = Path(path)
        suffix = p.suffix.lower()
        if suffix == ".pdf":
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif suffix in (".txt", ".text"):
            loader = TextLoader(path, encoding="utf-8")
            docs.extend(loader.load())
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
    return docs


def get_text_splitter(
    chunk_size: int = 300,
    chunk_overlap: int = 20,
) -> RecursiveCharacterTextSplitter:
    """Return a text splitter for chunking documents."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def build_vector_store(
    documents: List[Document],
    embeddings: OpenAIEmbeddings,
    store_type: Literal["faiss", "chroma"] = "chroma",
    persist_directory: str | None = None,
):
    """Build FAISS or Chroma vector store from documents."""
    if not documents:
        raise ValueError("No documents to index.")

    splitter = get_text_splitter()
    splits = splitter.split_documents(documents)

    if store_type == "faiss":
        return FAISS.from_documents(splits, embeddings)
    else:
        persist = persist_directory or tempfile.mkdtemp(prefix="crag_chroma_")
        return Chroma.from_documents(
            splits,
            embeddings,
            persist_directory=persist,
        )


def get_retriever(vector_store, k: int = 3):
    """Return a retriever from the vector store."""
    return vector_store.as_retriever(search_kwargs={"k": k})
