import streamlit as st
from rag import preguntar

st.set_page_config(
    page_title="Asistente Reglamento",
    layout="wide"
)

st.title("📚 Asistente Inteligente de Reglamento")

pregunta = st.text_input(
    "Haz una pregunta sobre el reglamento"
)

if st.button("Consultar"):

    if pregunta.strip() != "":

        respuesta, docs = preguntar(pregunta)

        st.subheader("🤖 Respuesta")

        st.write(respuesta)

        st.subheader("📄 Fragmentos Recuperados")

        for i, doc in enumerate(docs, 1):

            with st.expander(f"Fragmento {i}"):

                st.write(doc.page_content)