from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM

# -----------------------------------
# EMBEDDINGS LOCALES
# -----------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------
# VECTOR DB
# -----------------------------------

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# -----------------------------------
# LLM LOCAL
# -----------------------------------

llm = OllamaLLM(
    model="llama3"
)

# -----------------------------------
# SYSTEM PROMPT
# -----------------------------------

SYSTEM_PROMPT = """
Eres un asistente académico especializado en reglamentos universitarios.

REGLAS OBLIGATORIAS:

1. Responde ÚNICAMENTE usando el CONTEXTO proporcionado.
2. NO deduzcas.
3. NO infieras.
4. NO completes información faltante.
5. Si la respuesta no aparece explícitamente en el contexto responde EXACTAMENTE:
"No encuentro esa información en el reglamento".
6. NO uses conocimiento externo.
7. Si el contexto no habla directamente del tema, responde que no existe información.

FORMATO:

### Respuesta
### Artículos Relacionados
"""
# -----------------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------------

def preguntar(query):

    # Recuperación semántica
    docs = retriever.invoke(query)

    # Construcción contexto
    contexto = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Prompt aumentado
    prompt = f"""
{SYSTEM_PROMPT}

<CONTEXTO>
{contexto}
</CONTEXTO>

<PREGUNTA>
{query}
</PREGUNTA>

Recuerda:
- Si la respuesta no está explícitamente en el contexto,
responde:
"No encuentro esa información en el reglamento"
"""

    # Generación respuesta
    respuesta = llm.invoke(prompt)

    return respuesta, docs