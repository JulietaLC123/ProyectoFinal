from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

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
# EMBEDDINGS LOCALES
# -----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------
# VECTOR DB
# -----------------------------------

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

print("✅ Base vectorial creada")