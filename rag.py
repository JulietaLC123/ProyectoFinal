import os
from dotenv import load_dotenv
from google import genai

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# -----------------------------------
# CONFIG
# -----------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# -----------------------------------
# EMBEDDINGS
# -----------------------------------

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=API_KEY
)

# -----------------------------------
# VECTOR DB
# -----------------------------------

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 4}
)

# -----------------------------------
# PROMPT
# -----------------------------------

SYSTEM_PROMPT = """
Eres un asistente académico especializado en reglamentos universitarios.

REGLAS IMPORTANTES:

1. Responde SOLO usando el CONTEXTO.
2. No inventes información.
3. Si el contexto no contiene la respuesta responde EXACTAMENTE:
   "No encuentro esa información en el reglamento".
4. Explica de manera clara y breve.
5. Cita los artículos relevantes si aparecen.

FORMATO:

### Respuesta
### Artículos Relacionados
"""

# -----------------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------------

def preguntar(query):

    docs = retriever.invoke(query)

    contexto = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
{SYSTEM_PROMPT}

<CONTEXTO>
{contexto}
</CONTEXTO>

<PREGUNTA>
{query}
</PREGUNTA>
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text, docs