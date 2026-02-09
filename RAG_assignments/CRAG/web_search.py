"""
Web search / external document fetch for CRAG retry.
When a retry is triggered, fetches the reference PDF from India Code (IPC Act)
and adds relevant chunks to the context.
"""

import tempfile
from pathlib import Path
from typing import List, Optional

import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Default reference PDF (Indian Penal Code) used when retry is involved
DEFAULT_WEB_PDF_URL = "https://www.indiacode.nic.in/bitstream/123456789/15289/1/ipc_act.pdf"

# Request timeout and headers (some servers expect a browser-like User-Agent)
FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}
FETCH_TIMEOUT = 60


def fetch_pdf_from_url(
    url: str = DEFAULT_WEB_PDF_URL,
    timeout: int = FETCH_TIMEOUT,
    headers: Optional[dict] = None,
) -> List[Document]:
    """
    Download a PDF from the given URL and load it as LangChain documents.
    Returns a list of Document (one per page) or empty list on failure.
    """
    try:
        resp = requests.get(
            url,
            headers=headers or FETCH_HEADERS,
            timeout=timeout,
            stream=True,
        )
        resp.raise_for_status()
    except Exception:
        return []

    suffix = Path(url).suffix or ".pdf"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(resp.content)
        path = f.name

    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        return docs
    except Exception:
        return []
    finally:
        Path(path).unlink(missing_ok=True)


def get_text_splitter(chunk_size: int = 800, chunk_overlap: int = 150) -> RecursiveCharacterTextSplitter:
    """Splitter for web PDF chunks (slightly larger chunks for legal text)."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )


def get_web_context_for_query(
    query: str,
    embeddings,
    url: str = DEFAULT_WEB_PDF_URL,
    top_k: int = 3,
) -> str:
    """
    Fetch the PDF from URL, split into chunks, run similarity search with `query`,
    and return the concatenated relevant chunks as a single context string.
    Used when CRAG triggers a retry to augment context with the reference document.
    """
    docs = fetch_pdf_from_url(url)
    if not docs:
        return ""

    splitter = get_text_splitter()
    splits = splitter.split_documents(docs)
    if not splits:
        return ""

    try:
        vector_store = FAISS.from_documents(splits, embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})
        retrieved = retriever.invoke(query)
        if not retrieved:
            return ""
        return "\n\n---\n\n".join(doc.page_content for doc in retrieved)
    except Exception:
        # Fallback: return first few chunks to stay within context limits
        total = min(3, len(splits))
        return "\n\n---\n\n".join(splits[i].page_content for i in range(total))
