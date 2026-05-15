from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os

# -----------------------------------
# CONFIG
# -----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------------
# CARGA PDF
# -----------------------------------

loader = PyPDFLoader("data/reglamento.pdf")

docs = loader.load()

print(f"Documentos cargados: {len(docs)}")

# -----------------------------------
# SPLIT
# -----------------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = splitter.split_documents(docs)

print(f"Chunks generados: {len(chunks)}")

# -----------------------------------
# EMBEDDINGS
# -----------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="embedding-001",
    google_api_key=API_KEY
)

# -----------------------------------
# VECTOR STORE
# -----------------------------------

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("✅ Base vectorial creada")