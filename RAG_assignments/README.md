# CRAG – Corrective RAG App (Indian Penal Code – IPC)

Streamlit app that uses **Corrective RAG (CRAG)** to answer questions over the **Indian Penal Code (IPC)** using the official **India Code IPC Act PDF**. The system evaluates retrieved context quality and refines the query and re-retrieves when quality is Poor or Fair.

## Architecture (Pipeline)

```
User enters IPC-related question
         ↓
Fetch India Code IPC PDF (web)
         ↓
Document Loader + Text Splitter
         ↓
Vector Store (FAISS, in-memory)
         ↓
Retriever
         ↓
CRAG Evaluator (LLM)
    ├─ Poor/Fair  → refine query → re-retrieve over IPC
    └─ Good/Excellent → generate answer
         ↓
Final Answer  OR  "no answer found for the question, it's beyond our limit"
```

## CRAG Prompt (Summary)

1. **Step 1 – Context evaluation**  
   Rate retrieved context for the query: Relevance, Completeness, Accuracy, Specificity (0–1) and **Overall quality** [Excellent/Good/Fair/Poor].

2. **Step 2 – Correction decision**  
   - If **Poor** or **Fair**: Action = **Retrieve_again**, provide **New Query** and **REASONING**.  
   - If **Excellent** or **Good**: Action = **PROCEED_WITH_ANSWER**, **Confidence** [High/Medium/Low].

3. **Step 3 – Response**  
   Output **Context Quality**, **Confidence Level**, and **Answer**.

---

## India Code IPC web reference

- All context comes from the **India Code IPC Act PDF**  
  (`https://www.indiacode.nic.in/bitstream/123456789/15289/1/ipc_act.pdf` by default).
- For each round (initial and any retry):
  - The app fetches and chunks the IPC PDF (or reuses it, depending on caching).
  - Uses embeddings + similarity search to select the most relevant sections.
  - Feeds those sections into the CRAG evaluator prompt.
- You can override the default IPC URL with the `CRAG_WEB_PDF_URL` environment variable.

---

## Step-by-step instructions

### 1. Clone / open the project

Ensure you are in the project directory:

```bash
cd c:\Users\vigne\Codebase\B5-GenAI\RAG_assignments\CRAG
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

Optional: set the model used for CRAG evaluation and answer generation:

```env
OPENAI_MODEL=gpt-4o-mini
```

Optional: override the India Code IPC PDF URL used on retry:

```env
# Default (if not set) is the official IPC PDF on India Code
CRAG_WEB_PDF_URL=https://www.indiacode.nic.in/bitstream/123456789/15289/1/ipc_act.pdf
```

### 5. Run the Streamlit app

```bash
streamlit run app.py
```

The app will open in your browser (e.g. `http://localhost:8501`).

### 6. Use the app

1. **Ask a question**  
   In the main area, type your IPC-related question (e.g. “What is the punishment for theft under the IPC?”) and click **“Get answer”**.

2. **View results**  
   - **Pipeline steps**: retrieval round(s), CRAG evaluation (e.g. Poor/Fair → refine and re-retrieve, or Good/Excellent → answer).  
   - **Answer**: final answer or “no answer found for the question; it’s beyond our limit” when the system cannot answer from the documents.  
   - **CRAG evaluation details** (expandable): context quality, confidence, reasoning, and raw CRAG response.

---

## Project structure

```
CRAG/
├── app.py           # Streamlit UI and CRAG pipeline (IPC-only)
├── crag_prompt.py   # CRAG system and evaluation prompts
├── crag_logic.py    # Parse CRAG response, corrective decision
├── doc_store.py     # (Optional/unused) legacy local document loaders
├── web_search.py    # Fetch & search India Code IPC web PDF
├── requirements.txt
├── .env.example     # Example env vars (OPENAI_API_KEY, CRAG_WEB_PDF_URL, etc.)
├── .env             # Your local secrets (not committed)
└── README.md
```

## Requirements

- Python 3.10+
- OpenAI API key
- Internet access (to fetch the India Code IPC PDF, unless `CRAG_WEB_PDF_URL` is disabled/changed)

## Troubleshooting

- **“Set OPENAI_API_KEY”**  
  Add `OPENAI_API_KEY` to `.env` or your environment and restart the app.

- **“Please upload HR policy files and click Build index”**  
  Upload at least one PDF or TXT file and click **“Build index”** before asking a question.

- **Encoding errors with TXT**  
  Save TXT files as UTF-8. If needed, the app can be updated to try other encodings.

- **Chroma on Windows**  
  If Chroma fails, use **FAISS** in the sidebar when building the index.
