# 🧠 Knowledge Graph RAG System

A Streamlit-based **Knowledge Graph + RAG (Retrieval-Augmented Generation)** system that:

- 📄 Builds a Knowledge Graph from FAQ text
- 🕸 Stores entities & relations in Neo4j
- 🤖 Uses OpenAI to extract structured knowledge
- 💬 Answers questions using graph-based retrieval
- 🔎 Provides explainable graph-based context

---

# 🚀 Features

- Automatic entity & relation extraction using OpenAI
- Structured graph storage using Neo4j
- Context retrieval from graph instead of vector similarity
- Controlled, low-hallucination responses
- Streamlit UI for easy interaction
- Session-based knowledge preview

---

# 🏗 Architecture

```
FAQ Text File
      ↓
Chunking
      ↓
OpenAI Extraction (Entities + Relations)
      ↓
Neo4j Knowledge Graph
      ↓
Keyword-based Graph Search
      ↓
LLM Answer Using Graph Context
```

---

# 🛠 Tech Stack

- **Python**
- **Streamlit**
- **OpenAI GPT-4o-mini**
- **Neo4j Graph Database**
- **dotenv**

---

# 📦 Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/your-repo/kg-rag-app.git
cd kg-rag-app
```

## 2️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have requirements.txt, install manually:

```bash
pip install streamlit openai neo4j python-dotenv
```

---

# 🔐 Environment Variables

Create a `.env` file in your root directory:

```env
OPENAI_API_KEY=your_openai_api_key

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

⚠️ **Never commit `.env` to GitHub.**  
Add it to `.gitignore`.

---

# 🧪 Running the App

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

# 📄 How It Works

## 1️⃣ Build Knowledge Graph

- Upload a `.txt` FAQ file
- Text is split into chunks
- OpenAI extracts:
  - Entities
  - Relationships
- Data is stored in Neo4j

Example extraction format:

```json
{
  "entities": [
    {"name": "AI", "type": "CONCEPT"}
  ],
  "relations": [
    {"source": "ML", "relation": "SUBSET_OF", "target": "AI"}
  ]
}
```

---

## 2️⃣ Graph Storage

Each entity is stored as:

```
(:Entity {name, type})
```

Each relationship is stored as:

```
(:Entity)-[:RELATES {type}]->(:Entity)
```

Before rebuilding, the graph is cleared:

```cypher
MATCH (n) DETACH DELETE n
```

---

## 3️⃣ Graph-Based Retrieval

When a user asks a question:

1. OpenAI extracts keywords
2. Neo4j searches matching entities
3. Retrieves:
   - Outgoing relationships
   - Incoming relationships
4. Builds structured graph context

---

## 4️⃣ Controlled Answer Generation

The model receives:

```
Context: (Graph data)
Question: (User query)
```

System instruction:

> "Answer ONLY using provided Knowledge Graph context. Be concise and factual."

This reduces hallucination significantly.

---

# 🧠 Example Use Case

Upload FAQ:

```
Machine Learning is a subset of Artificial Intelligence.

Deep Learning is a subset of Machine Learning.
```

Ask:

```
How is Deep Learning related to AI?
```

System retrieves:

```
Deep Learning → SUBSET_OF → Machine Learning
Machine Learning → SUBSET_OF → AI
```

Answer:

```
Deep Learning is a subset of Machine Learning, which is a subset of AI.
```

---

# 📊 Why Knowledge Graph RAG?

| Vector RAG | Knowledge Graph RAG |
|------------|--------------------|
| Similarity-based retrieval | Relationship-based retrieval |
| Unstructured context | Structured reasoning |
| Hard to explain | Fully explainable |
| May hallucinate | Constrained by graph |

---

# 🔎 Project Structure

```
kg-rag-app/
│
├── app.py
├── .env
├── requirements.txt
└── README.md
```

---

# ⚠️ Production Improvements (Recommended)

- Add incremental graph updates instead of delete-all
- Add proper Cypher injection safety
- Add entity normalization
- Add relation type validation
- Add graph visualization (pyvis)
- Add vector fallback retrieval (Hybrid RAG)
- Add user authentication
- Deploy with Docker

---

# 🏆 Advanced Enhancements

You can extend this to:

- Hybrid Vector + Graph RAG
- Multi-hop reasoning
- Graph embeddings
- Graph constraint enforcement
- Schema-based validation
- Domain-specific ontology integration

---

# 👨‍💻 Author

Knowledge Graph RAG System  
Built with ❤️ using Streamlit + Neo4j + OpenAI


