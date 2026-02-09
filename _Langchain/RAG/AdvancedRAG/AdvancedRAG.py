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
from langchain.prompts import PromptTemplate

# ----------------------------------
# Load environment variables
# ----------------------------------
load_dotenv()

# ----------------------------------
# Load documents (MULTI SOURCE)
# ----------------------------------
docs = []
docs += TextLoader("data/genai_overview.txt").load()
docs += CSVLoader("data/genai_usecases.csv").load()
docs += PyPDFLoader("data/genai_future.pdf").load()

# ----------------------------------
# Split documents
# ----------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# ----------------------------------
# Embeddings & Vector Store
# ----------------------------------
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 10}
)

# ----------------------------------
# LLM
# ----------------------------------
llm = ChatOpenAI(temperature=0)

# ----------------------------------
# NEGATIVE PROMPT (Guardrails)
# ----------------------------------
NEGATIVE_RULES = """
You must follow these rules:
- Do NOT hallucinate facts
- Do NOT guess if context is missing
- Say "I don't know" if unsure
- Be concise and factual
"""

# ----------------------------------
# RAG Prompt
# ----------------------------------
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=f"""
{NEGATIVE_RULES}

Context:
{{context}}

Question:
{{question}}

Answer:
"""
)

# ----------------------------------
# FUSION QUERY GENERATION
# ----------------------------------
def expand_queries(question):
    return [
        question,
        f"Explain the concept of {question}",
        f"Common misconceptions about {question}",
        f"Historical or technical clarification of {question}",
    ]

# ----------------------------------
# FUSION RETRIEVAL
# ----------------------------------
def fusion_retrieve(question):
    queries = expand_queries(question)
    fused_docs = {}

    for q in queries:
        retrieved_docs = retriever.get_relevant_documents(q)
        for doc in retrieved_docs:
            fused_docs[doc.page_content] = doc

    return list(fused_docs.values())

# ----------------------------------
# CORRECTIVE RAG LOGIC
# ----------------------------------
def advanced_rag(question):
    # Step 1: LLM-only attempt
    first_answer = llm.invoke(
        f"{NEGATIVE_RULES}\n\nQuestion: {question}\nAnswer:"
    ).content

    # Confidence check
    if "i don't know" not in first_answer.lower() and len(first_answer) > 40:
        return first_answer

    # Step 2: Fusion Retrieval
    fused_docs = fusion_retrieve(question)
    context = "\n\n".join(doc.page_content for doc in fused_docs)

    # Step 3: Final grounded answer
    final_prompt = rag_prompt.format(
        context=context,
        question=question
    )

    return llm.invoke(final_prompt).content

# ----------------------------------
# RUN
# ----------------------------------
if __name__ == "__main__":
    query = "about poondi dam in tiruvallur?"
    answer = advanced_rag(query)
    print("\nFinal Answer:\n", answer)




