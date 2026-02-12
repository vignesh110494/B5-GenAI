# RAG App -- Ask Your PDF Anything

## 🚀 Overview

This is a Retrieval-Augmented Generation (RAG) application built using:

-   **Streamlit** (UI)
-   **LangChain (LCEL architecture)**
-   **FAISS** (Vector database)
-   **OpenAI GPT-4.1 Mini**
-   **OpenAI Embeddings (text-embedding-3-small)**

The application allows users to:

-   Upload a PDF file\
-   Ask questions about the document\
-   Receive AI-generated answers based only on the uploaded document

------------------------------------------------------------------------

## 🏗️ Architecture

    User Uploads PDF
            ↓
    Extract Text (PyPDF2)
            ↓
    Text Splitting (RecursiveCharacterTextSplitter)
            ↓
    Embeddings (text-embedding-3-small)
            ↓
    FAISS Vector Store
            ↓
    Retriever
            ↓
    GPT-4.1-mini
            ↓
    Answer Displayed in Streamlit

------------------------------------------------------------------------

## 📦 Tech Stack

  Component      Technology
  -------------- ------------------------
  UI             Streamlit
  LLM            GPT-4.1-mini
  Embeddings     text-embedding-3-small
  Vector Store   FAISS
  Framework      LangChain (LCEL)
  PDF Reader     PyPDF2

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone the Repository

``` bash
git clone <your-repo-url>
cd <project-folder>
```

### 2️⃣ Create Virtual Environment

**Windows:**

``` bash
python -m venv ragenv
ragenv\Scripts\activate
```

**Mac/Linux:**

``` bash
python3 -m venv ragenv
source ragenv/bin/activate
```

### 3️⃣ Install Dependencies

``` bash
pip install streamlit
pip install langchain langchain-core langchain-community
pip install langchain-openai
pip install langchain-text-splitters
pip install faiss-cpu
pip install PyPDF2
pip install python-dotenv
```

------------------------------------------------------------------------

## 🔐 Environment Variables

Create a `.env` file in your project root:

    OPENAI_API_KEY=your_openai_api_key_here

------------------------------------------------------------------------

## ▶️ Run the Application

``` bash
streamlit run demo.py
```

Then open the URL shown in your browser (usually http://localhost:8501).

------------------------------------------------------------------------

## 🧠 How It Works

### 1️⃣ PDF Upload

User uploads a text-based PDF.

> ⚠️ Note: Scanned PDFs (image-based) will not work unless OCR is
> applied.

### 2️⃣ Text Extraction

``` python
PdfReader(uploaded_file)
```

### 3️⃣ Text Splitting

    chunk_size=1000
    chunk_overlap=200

This improves retrieval accuracy.

### 4️⃣ Embeddings

Each chunk is converted into vectors using:

    text-embedding-3-small

### 5️⃣ Vector Store (FAISS)

The embeddings are stored in FAISS for fast similarity search.

### 6️⃣ Retrieval + LLM (RAG)

When a user asks a question:

-   Relevant chunks are retrieved\
-   Context is injected into the prompt\
-   GPT-4.1-mini generates the answer

#### LCEL Chain:

``` python
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)
```

------------------------------------------------------------------------

## 📌 Features

✔ Upload any text-based PDF\
✔ Automatic text chunking\
✔ Semantic search with FAISS\
✔ GPT-4.1-mini powered answers\
✔ Clean Streamlit UI\
✔ Error handling for scanned PDFs

------------------------------------------------------------------------

## 📄 License

This project is for educational and demonstration purposes.
