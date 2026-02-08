import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# ----------------------------------
# CONFIG (use environment variable)
# ----------------------------------
load_dotenv()  # loads .env file

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
# ----------------------------------
# Load text file
# ----------------------------------
loader = TextLoader("selfRAG.txt")
docs = loader.load()

# ----------------------------------
# Split documents
# ----------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# ----------------------------------
# Embeddings
# ----------------------------------
embeddings = OpenAIEmbeddings()


# ----------------------------------
# Vector store
# ----------------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

# ----------------------------------
# NEGATIVE PROMPT (System instruction)
# ----------------------------------
NEGATIVE_INSTRUCTIONS = """
You must follow these rules strictly:
- Do NOT guess or hallucinate facts
- Do NOT provide incorrect historical information
- If you are unsure, say "I don't know"
- Do NOT invent names, dates, or titles
- Be concise and factual
"""

# ----------------------------------
# Custom prompt with negative prompt
# ----------------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=f"""
{NEGATIVE_INSTRUCTIONS}

Context:
{{context}}

Question:
{{question}}

Answer:
"""
)

# ----------------------------------
# LLM
# ----------------------------------

llm = ChatOpenAI(temperature=0)
verifier_llm = ChatOpenAI(temperature=0)

# ----------------------------------
# RetrievalQA with negative prompt
# ----------------------------------
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt}
)

# ----------------------------------
# Self-RAG style query
# ----------------------------------
def self_rag_query(question):
    print("First attempt (LLM only):")

    first_answer = llm.invoke(
        f"{NEGATIVE_INSTRUCTIONS}\n\nQuestion: {question}\nAnswer:"
    ).content

    if "i don't know" in first_answer.lower() or len(first_answer) < 30:
        print("Low confidence. Retrieving context and retrying...")
        improved_answer = qa.invoke({"query": question})["result"]
        return improved_answer
    else:
        return first_answer
    
# ----------------------------------
# Answer Verifier
# ----------------------------------
def is_answer_correct(question, answer):
    verification_prompt = f"""
Question: {question}
Answer: {answer}

Is this answer factually correct?
Reply with only YES or NO.
"""
    verdict = verifier_llm.invoke(verification_prompt).content.strip()
    return verdict.upper() == "YES"

# ----------------------------------
# Corrective RAG Pipeline
# ----------------------------------
def corrective_rag(question):
    print("\n🔹 Initial LLM answer (no retrieval):")
    initial_answer = llm.invoke(question).content
    print(initial_answer)

    print("\n🔍 Verifying answer...")
    if is_answer_correct(question, initial_answer):
        print("✅ Answer is correct.")
        return initial_answer

    print("❌ Answer is incorrect. Running RAG correction...")
    corrected_answer = qa.invoke({"query": question})["result"]
    return corrected_answer

# ----------------------------------
# Run Example
# ----------------------------------
response = corrective_rag(
    "Who is CM of tamil nadu?"
)

print("\n✅ Final Answer:")
print(response)
