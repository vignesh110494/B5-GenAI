"""
CRAG (Corrective RAG) Streamlit App.

Primary source: local `Laws.pdf` (or `Laws.txt`) in this project.
If retrieval from `Laws` has low quality, the system refines the query and
retries using the India Code IPC web PDF as an additional source.
"""

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage

from doc_store import load_documents_from_files, build_vector_store, get_retriever
from crag_prompt import CRAG_SYSTEM_PROMPT
from crag_logic import (
    build_evaluation_prompt,
    parse_crag_response,
    is_good_quality,
    should_retrieve_again,
    CRAGResult,
)
from web_search import get_web_context_for_query, DEFAULT_WEB_PDF_URL

load_dotenv()

# Page config
st.set_page_config(
    page_title="CRAG – Laws / IPC Q&A",
    page_icon="📋",
    layout="wide",
)

# Session state
if "laws_retriever" not in st.session_state:
    st.session_state.laws_retriever = None


def get_embeddings():
    """OpenAI embeddings; requires OPENAI_API_KEY."""
    return OpenAIEmbeddings(model="text-embedding-3-small")


def get_llm():
    """Chat LLM for CRAG evaluator and answer generation."""
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )


def get_laws_retriever(embeddings):
    """
    Build (or reuse) a retriever over the local Laws document.

    Looks for `Laws.pdf` or `Laws.txt` in the project root.
    """
    if st.session_state.laws_retriever is not None:
        return st.session_state.laws_retriever

    root = Path(__file__).resolve().parent
    candidate_paths = [root / "Laws.pdf", root / "Laws.txt"]
    existing = [str(p) for p in candidate_paths if p.exists()]
    if not existing:
        raise FileNotFoundError(
            "Could not find `Laws.pdf` or `Laws.txt` in the project root. "
            "Please add one of these files."
        )

    docs = load_documents_from_files(existing)
    vector_store = build_vector_store(docs, embeddings, store_type="faiss")
    retriever = get_retriever(vector_store, k=3)
    st.session_state.laws_retriever = retriever
    return retriever


def run_crag_evaluator(llm, user_query: str, retrieved_context: str) -> CRAGResult:
    """Run CRAG evaluation prompt and parse response."""
    prompt = build_evaluation_prompt(user_query, retrieved_context)
    messages = [
        SystemMessage(content=CRAG_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    text = response.content if hasattr(response, "content") else str(response)
    return parse_crag_response(text)


def get_context_from_retriever(retriever, query: str, k: int = 3) -> str:
    """Retrieve docs from Laws retriever and return concatenated context string."""
    docs = retriever.invoke(query)
    if not docs:
        return ""
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def run_crag_pipeline(
    laws_retriever,
    llm,
    user_query: str,
    embeddings,
    max_correction_rounds: int = 1,
    web_pdf_url: str | None = None,
) -> tuple[str, CRAGResult | None, list[str]]:
    """
    Run full CRAG pipeline:
    - Round 1: retrieve from local `Laws` document only.
    - Retry round: retrieve from `Laws` again using refined query AND
      augment context with relevant sections from the India Code IPC web PDF.

    Returns (final_answer, last_crag_result, steps_log).
    """
    steps = []
    current_query = user_query
    last_result = None
    url = web_pdf_url or DEFAULT_WEB_PDF_URL

    for round_idx in range(max_correction_rounds + 1):
        steps.append(
            f"**Round {round_idx + 1}** – Query: \"{current_query[:60]}...\""
            if len(current_query) > 60
            else f"**Round {round_idx + 1}** – Query: \"{current_query}\""
        )

        # Base context: always from local Laws document
        context = get_context_from_retriever(laws_retriever, current_query)

        # On retry (round_idx >= 1), augment context with IPC web PDF via web search
        if round_idx >= 1 and embeddings is not None:
            web_context = get_web_context_for_query(
                current_query, embeddings, url=url, top_k=3
            )
            if web_context.strip():
                context = (
                    context.strip()
                    + "\n\n---\n\n**[Additional context from India Code – IPC Act]**\n\n"
                    + web_context.strip()
                )
                steps.append(
                    "Augmented Laws context with additional IPC sections from web search."
                )

        if not context.strip():
            steps.append("No context retrieved from local Laws document.")
            return (
                "No answer found for the question; it's beyond our limit (no relevant content retrieved from Laws).",
                None,
                steps,
            )

        steps.append(f"Retrieved {len(context)} chars of context.")

        last_result = run_crag_evaluator(llm, user_query, context)
        steps.append(f"CRAG evaluation: **{last_result.overall_quality}** → Action: **{last_result.action}**")

        if is_good_quality(last_result.overall_quality):
            answer = last_result.answer or last_result.raw_response
            if not answer or "Answer:" in answer and answer.strip().endswith("Answer:"):
                answer = "The model did not produce a clear answer from the context."
            steps.append("Proceeding with answer.")
            return (answer, last_result, steps)

        if should_retrieve_again(last_result) and round_idx < max_correction_rounds:
            current_query = last_result.refined_query
            steps.append(
                f"Refining query to: \"{current_query[:60]}...\""
                if len(current_query) > 60
                else f"Refining query to: \"{current_query}\""
            )
            continue

        # Poor/Fair but no refined query or last round – still try to return something
        answer = last_result.answer or "No answer found for the question; it's beyond our limit (context quality was insufficient)."
        return (answer, last_result, steps)

    # Fallback
    final_answer = last_result.answer if last_result else "No answer found for the question; it's beyond our limit."
    return (final_answer, last_result, steps)


# ---- UI ----

st.title("📋 CRAG – Laws / IPC Q&A")
st.caption(
    "Corrective RAG over local `Laws` content, with a fallback retry that augments context "
    "from the Indian Penal Code (IPC) via the official India Code PDF."
)

with st.sidebar:
    st.header("Source & implementation")
    st.markdown(
        "- **Primary source:** `Laws.pdf` (or `Laws.txt`) in this project\n"
        "- **Fallback source (on low-quality retrieval):** India Code official IPC PDF\n"
        f"- **IPC default URL:** `{DEFAULT_WEB_PDF_URL}` (override with `CRAG_WEB_PDF_URL`)\n\n"
        "- **How it works:**\n"
        "  - First, the app builds a vector index from the local `Laws` document.\n"
        "  - For each question, it retrieves relevant sections from `Laws` and runs a CRAG evaluator\n"
        "    (Excellent/Good/Fair/Poor) over that context.\n"
        "  - If the context is Poor/Fair, CRAG refines the query and a retry round runs that still\n"
        "    uses `Laws` but also augments the context with relevant IPC sections fetched via web search.\n"
        "  - Answers are generated strictly from the combined retrieved context; if insufficient,\n"
        "    you’ll see a 'no answer found / beyond our limit' message."
    )

st.divider()
st.header("Ask your legal question")

question = st.text_area(
    "Question",
    placeholder="e.g. What is the punishment for theft?",
    height=100,
)
submit = st.button("Get answer")

if submit:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("Set `OPENAI_API_KEY` in your environment or `.env` file.")
        else:
            try:
                with st.spinner("Building Laws index and running CRAG pipeline..."):
                    llm = get_llm()
                    embeddings = get_embeddings()
                    laws_retriever = get_laws_retriever(embeddings)
                    web_pdf_url = os.getenv("CRAG_WEB_PDF_URL", DEFAULT_WEB_PDF_URL)
                    final_answer, crag_result, steps_log = run_crag_pipeline(
                        laws_retriever,
                        llm,
                        question.strip(),
                        embeddings=embeddings,
                        max_correction_rounds=1,
                        web_pdf_url=web_pdf_url,
                    )
            except FileNotFoundError as e:
                st.error(str(e))
            else:
                st.subheader("Pipeline steps")
                for step in steps_log:
                    st.markdown(step)

                st.subheader("Answer")
                st.markdown(final_answer)

                if crag_result:
                    with st.expander("CRAG evaluation details"):
                        st.markdown(f"**Context quality:** {crag_result.overall_quality}")
                        st.markdown(f"**Confidence:** {crag_result.confidence or '—'}")
                        if crag_result.reasoning:
                            st.markdown(f"**Reasoning:** {crag_result.reasoning}")
                        st.markdown("**Raw response:**")
                        st.text(crag_result.raw_response)
