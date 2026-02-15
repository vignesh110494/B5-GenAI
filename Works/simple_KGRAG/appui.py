import os
import json
import streamlit as st
from openai import OpenAI
from neo4j import GraphDatabase
from dotenv import load_dotenv

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
load_dotenv()

st.set_page_config(
    page_title="Knowledge Graph RAG",
    page_icon="🧠",
    layout="wide"
)

# Initialize clients
ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

# Session state
if "kg_built" not in st.session_state:
    st.session_state.kg_built = False
if "entities" not in st.session_state:
    st.session_state.entities = []
if "relations" not in st.session_state:
    st.session_state.relations = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────

def extract(chunk):
    prompt = f"""Extract entities and relations from this text.
Return ONLY valid JSON like:
{{"entities": [{{"name": "AI", "type": "CONCEPT"}}],
"relations": [{{"source": "ML", "relation": "SUBSET_OF", "target": "AI"}}]}}

Text: {chunk}"""

    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    text = res.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1].removeprefix("json").strip()

    try:
        return json.loads(text)
    except:
        return {"entities": [], "relations": []}


def store(entities, relations):
    with db.session() as s:
        s.run("MATCH (n) DETACH DELETE n")

        for e in entities:
            s.run(
                "MERGE (n:Entity {name: $name}) SET n.type = $type",
                name=e["name"],
                type=e["type"]
            )

        for r in relations:
            s.run("""
                MATCH (a:Entity {name: $src}),
                      (b:Entity {name: $tgt})
                MERGE (a)-[:RELATES {type: $rel}]->(b)
            """, src=r["source"], rel=r["relation"], tgt=r["target"])


def search_graph(question):
    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f'Extract keywords from this question as a JSON array: "{question}"'
        }],
        temperature=0
    )

    text = res.choices[0].message.content.strip()
    if "```" in text:
        text = text.split("```")[1].removeprefix("json").strip()

    try:
        keywords = json.loads(text)
    except:
        keywords = []

    results = []
    with db.session() as s:
        for kw in keywords:
            records = s.run("""
                MATCH (n:Entity)
                WHERE toLower(n.name) CONTAINS toLower($kw)
                OPTIONAL MATCH (n)-[r:RELATES]->(m)
                OPTIONAL MATCH (p)-[r2:RELATES]->(n)
                RETURN n.name AS entity,
                       n.type AS type,
                       collect(DISTINCT {rel: r.type, target: m.name}) AS out,
                       collect(DISTINCT {rel: r2.type, source: p.name}) AS inc
            """, kw=kw)

            for rec in records:
                d = rec.data()
                info = f"{d['entity']} ({d['type']})"

                for o in d['out']:
                    if o['target']:
                        info += f"\n  → {d['entity']} --{o['rel']}--> {o['target']}"

                for i in d['inc']:
                    if i['source']:
                        info += f"\n  ← {i['source']} --{i['rel']}--> {d['entity']}"

                results.append(info)

    return "\n\n".join(results) if results else "No relevant knowledge found."


def ask(question):
    context = search_graph(question)

    res = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Answer ONLY using provided Knowledge Graph context. Be concise and factual."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        temperature=0.3
    )

    return res.choices[0].message.content


# ─────────────────────────────────────────────
# UI LAYOUT
# ─────────────────────────────────────────────

st.title("🧠 Knowledge Graph RAG System")
st.markdown("Build a Knowledge Graph from FAQ text and query it with AI.")

# ─────────────────────────────────────────────
# BUILD SECTION
# ─────────────────────────────────────────────

st.header("📄 1. Build Knowledge Graph")

uploaded_file = st.file_uploader("Upload FAQ Text File", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    chunks = [c.strip() for c in text.split("\n\n") if c.strip()]
    st.info(f"Detected {len(chunks)} text chunks.")

    if st.button("🚀 Build Knowledge Graph"):

        with st.spinner("Extracting entities and relations..."):
            all_entities, all_relations = [], []
            seen_e, seen_r = set(), set()

            progress = st.progress(0)

            for i, chunk in enumerate(chunks):
                data = extract(chunk)

                for e in data["entities"]:
                    if e["name"] not in seen_e:
                        seen_e.add(e["name"])
                        all_entities.append(e)

                for r in data["relations"]:
                    key = (r["source"], r["relation"], r["target"])
                    if key not in seen_r:
                        seen_r.add(key)
                        all_relations.append(r)

                progress.progress((i + 1) / len(chunks))

        store(all_entities, all_relations)

        st.session_state.entities = all_entities
        st.session_state.relations = all_relations
        st.session_state.kg_built = True

        st.success("✅ Knowledge Graph successfully built!")

        col1, col2 = st.columns(2)
        col1.metric("Entities", len(all_entities))
        col2.metric("Relations", len(all_relations))


# ─────────────────────────────────────────────
# PREVIEW SECTION
# ─────────────────────────────────────────────

if st.session_state.kg_built:
    st.header("🔍 Knowledge Graph Preview")

    if st.checkbox("Show Entities"):
        st.table(st.session_state.entities)

    if st.checkbox("Show Relations"):
        st.table(st.session_state.relations)


# ─────────────────────────────────────────────
# QUERY SECTION
# ─────────────────────────────────────────────

if st.session_state.kg_built:
    st.header("💬 2. Ask Questions")

    user_input = st.text_input("Ask something about your Knowledge Graph")

    if user_input:
        with st.spinner("Thinking..."):
            answer = ask(user_input)

        st.session_state.chat_history.append(
            {"question": user_input, "answer": answer}
        )

    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**❓ {chat['question']}**")
        st.markdown(f"💡 {chat['answer']}")
        st.markdown("---")


# ─────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────
# Note: In production, handle graceful shutdown
