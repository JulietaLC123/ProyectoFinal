# Proyecto Final - Sistema RAG Reglamento Académico

## Instalación

bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt


## Ejecutar Ollama

Descargar e instalar Ollama desde:

https://ollama.com/download

Luego descargar el modelo:

bash
ollama pull llama3


## Ejecutar el proyecto

Terminal 1:

bash
ollama run llama3


Terminal 2:

bash
.\env\Scripts\activate
streamlit run app.py


## Acceso

Abrir en el navegador:

txt
http://localhost:8501


## Construcción de la Base Vectorial

Si se modifica el reglamento o los documentos, ejecutar:

bash
python ingestar.py
