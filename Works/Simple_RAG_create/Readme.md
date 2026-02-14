# 📄 Simple RAG App – Ask Your Document

A simple Retrieval-Augmented Generation (RAG) application built using:

- **Streamlit** (User Interface)
- **LangChain (LCEL Architecture)**
- **FAISS** (Vector Database)
- **OpenAI Embeddings**
- **ChatOpenAI (gpt-4.1-mini)**

This app allows users to upload a PDF and ask questions grounded strictly in the document content.

---

# 🚀 Features

- 📂 Upload PDF document  
- ✂ Automatic document chunking  
- 🧠 Generate OpenAI embeddings  
- 📊 Store vectors in FAISS  
- 🔎 Retrieve Top-K relevant chunks (k=4)  
- 🤖 Generate answers using GPT-4.1-mini  
- 🔄 Spinner while generating responses  
- 🖥 Debug print statements for each stage  

---

# 🏗 Architecture Flow

```
User Upload PDF
        ↓
PyPDFLoader (Extract Text)
        ↓
RecursiveCharacterTextSplitter
        ↓
OpenAI Embeddings
        ↓
FAISS Vector Store
        ↓
Top-K Retrieval (k=4)
        ↓
Prompt + LLM
        ↓
Display Answer in Streamlit
```

---

# 🧰 Tech Stack

| Component | Technology |
|------------|------------|
| UI | Streamlit |
| LLM | gpt-4.1-mini |
| Embeddings | OpenAIEmbeddings |
| Vector DB | FAISS |
| Framework | LangChain (LCEL) |
| Document Loader | PyPDFLoader |

---

# 📦 Installation

## 1️⃣ Create Project Folder

```bash
mkdir simple_rag_app
cd simple_rag_app
```

---

## 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Activate environment:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

## 3️⃣ Install Required Packages

```bash
pip install streamlit langchain langchain-core langchain-community langchain-openai faiss-cpu pypdf python-dotenv
```

---

# 🔐 Environment Configuration

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key_here
```

⚠ Do not include quotes.

---

# ▶️ Running the Application

If your file name is:

### app.py
```bash
streamlit run app.py
```

### demo.py
```bash
streamlit run demo.py
```

After running, open your browser at:

```
http://localhost:8501
```

---

# ⚙ Configuration Details

## Chunking Settings

```python
chunk_size = 1000
chunk_overlap = 200
```

## Retrieval Settings

```python
search_kwargs = {"k": 4}
```

## LLM Settings

```python
model="gpt-4.1-mini"
temperature=0.2
```

---

# 🔍 How It Works

1. User uploads a PDF.
2. The document is loaded using `PyPDFLoader`.
3. Text is split into overlapping chunks.
4. Each chunk is converted into embeddings.
5. FAISS stores embeddings in memory.
6. When a user asks a question:
   - Top 4 similar chunks are retrieved.
   - Context + question are sent to the LLM.
   - LLM generates a grounded answer.
7. The answer is displayed in the Streamlit UI.

---

# 🖥 User Interface Flow

- Upload a PDF file.
- Enter a question.
- Spinner appears while processing.
- Answer is displayed below.

---

# 🔎 Debug Logging

The app prints the following stages in the terminal:

- File upload success
- Document loading
- Number of pages loaded
- Chunk splitting
- Total chunks created
- Embedding creation
- Vector store initialization
- LLM initialization
- RAG chain creation
- Response generation

---

# 📁 Project Structure

```
simple_rag_app/
│
├── app.py (or demo.py)
├── .env
├── README.md
```

---

# 🚀 Future Improvements

- Persistent FAISS index  
- Embedding caching  
- Streaming token output  
- Chat-style UI  
- Source document highlighting  
- Token usage tracking  
- Deployment to Streamlit Cloud  
- Docker containerization  

---

# 📜 License

This project is for educational purposes.

---

# 👨‍💻 Author

Built to understand and implement modern Retrieval-Augmented Generation (RAG) using LangChain LCEL architecture.

---

If you'd like, I can also generate:

- ✅ `requirements.txt`
- ✅ Dockerfile
- ✅ Production-ready folder structure
- ✅ Streamlit Cloud deployment guide
- ✅ Optimized version with caching

Just let me know 🚀
