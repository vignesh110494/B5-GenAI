# from langchain_community .document_loaders import TextLoader

# # to load notes file
# test = TextLoader("notes.txt")
# documents = test.load()
# print(documents)  

# to load pdf File

# from langchain_community.document_loaders import PyPDFLoader
# test2 = PyPDFLoader("LLM_Basics_Guide.pdf")
# documents2 = test2.load()
# print(documents2)  

# # to load the webpage
# from langchain_community.document_loaders import WebBaseLoader
# test3 = WebBaseLoader(web_path= "https://www.geeksforgeeks.org/artificial-intelligence/large-language-model-llm/")
# documents3 = test3.load()
# print(documents3)


# to load the arxiv loader research paper IEEE journals ArxivLoader
# from langchain_community.document_loaders import ArxivLoader
# test4 = ArxivLoader(query="1706.03762")
# print(test4.load())

# to test ssl is ok or not 
# import ssl, urllib.request
# urllib.request.urlopen("https://arxiv.org")
# print("SSL OK")


# # to load data from wikipedia
# from langchain_community.document_loaders import WikipediaLoader
# test5 = WikipediaLoader(query="AI agents", load_max_docs=2)
# print(test5.load())

# # character text splitter
# from langchain_community.document_loaders import PyPDFLoader
# spliittext = PyPDFLoader("LLM_Basics_Guide.pdf")
# spliittext_print = spliittext.load()
# fulltext = "\n".join([doc.page_content for doc in spliittext_print])
# print(fulltext)

# #CharacterTextSplitter
# from langchain_text_splitters import CharacterTextSplitter
# text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
#    chunk_size=100, chunk_overlap=0
# )
# text_CharacterTextSplitter = text_splitter.split_text(fulltext)
# print(text_CharacterTextSplitter)

# #RecursiveCharacterTextSplitter
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# text_splitter1 = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# text_RecursiveCharacterTextSplitter = text_splitter1.split_text(fulltext)
# print(text_RecursiveCharacterTextSplitter)

# # embedding using open ai key starts
# from langchain_openai import OpenAIEmbeddings

# openai_embeddings = OpenAIEmbeddings(keyhere)

# textembed = "Langchain is a framework for developing applications powered by language models."

# embeded = openai_embeddings.embed_query(textembed)
# print(embeded[:5])
# embedding using open ai key ends

# # embeddings using huggin face model if key is not available
# from langchain_huggingface import HuggingFaceEmbeddings
# embedded2 = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 
# textembed2 = "Langchain is a framework for developing applications powered by language models."
# embeded2 = embedded2.embed_query(textembed2)
# print(embeded2[:5]) 

#embed using grok model


# from groq import Groq
# import os

# client = Groq(api_key=keyhere)

# text = "LangChain is a framework for developing applications powered by language models."

# response = client.embeddings.create(
#     model="llama-3.1-8b-instant",
#     input=text
# )

# embedding = response.data[0].embedding

# print(embedding[:5])
# print("Embedding length:", len(embedding))


# # vector  using huggingface model using faiss vector database

# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# text = ["Prompt Engineering Basics", "Real-World Use Cases", "Popular Large Language Models"]

# embeded_new = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# vector_store = FAISS.from_texts(texts=text, embedding=embeded_new)

# print(vector_store)

# vector_store.save_local("faiss_myfirstvectorDB")  

# retriever = vector_store.as_retriever()
# query = "Real?"
# answer = retriever.invoke(query)
# # print(answer)

# for doc in answer:
#     print(doc.page_content)


#vector using huggingface model using chroma vector database

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Sample documents
texts = [
    "LangChain is a framework for building LLM-powered applications.",
    "ChromaDB is a vector database for storing embeddings.",
    "Embeddings convert text into numerical vectors."
]

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Create Chroma vector store (in-memory)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


