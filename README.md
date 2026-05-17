# Proyecto Final - Sistema RAG Reglamento Académico

## Descripción General

Este proyecto implementa un sistema RAG (Retrieval-Augmented Generation) para consultar un reglamento académico mediante lenguaje natural. El sistema permite que un estudiante haga preguntas sobre becas, cancelaciones, asistencia, sanciones, promedio académico y otros temas del reglamento, obteniendo respuestas contextualizadas a partir de documentos reales.

La solución combina búsqueda semántica con modelos de lenguaje ejecutados localmente usando Ollama y el modelo llama3.

---

# Objetivo del Proyecto

Construir un asistente académico capaz de:

* Leer documentos del reglamento.
* Dividir el contenido en fragmentos.
* Convertir esos fragmentos en vectores.
* Guardarlos en una base vectorial.
* Recuperar los fragmentos más relevantes.
* Generar respuestas precisas usando un LLM.
* Reducir al máximo las alucinaciones del modelo.

---

# Tecnologías Utilizadas

| Tecnología       | Uso                            |
| ---------------- | ------------------------------ |
| Python           | Desarrollo principal           |
| Streamlit        | Interfaz web                   |
| Ollama           | Ejecución local del modelo LLM |
| llama3           | Modelo de lenguaje             |
| LangChain        | Flujo RAG                      |
| ChromaDB / FAISS | Base vectorial                 |
| Embeddings       | Vectorización semántica        |

---

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

---

# Arquitectura de la Solución

El sistema sigue una arquitectura RAG clásica dividida en dos fases principales:

1. Fase de ingesta.
2. Fase de consulta.

## Flujo General

```text
Documentos PDF/TXT
        ↓
Carga de documentos
        ↓
Separación en chunks
        ↓
Generación de embeddings
        ↓
Base vectorial
        ↓
Pregunta del usuario
        ↓
Búsqueda semántica
        ↓
Construcción del prompt aumentado
        ↓
LLM (llama3)
        ↓
Respuesta final
```

---


# Proceso de Ingesta

La ingesta corresponde al proceso donde los documentos son preparados para la búsqueda semántica.

## 1. Carga de documentos

El sistema lee los archivos del reglamento académico desde la carpeta correspondiente.

Los formatos pueden incluir:

* PDF
* TXT
* DOCX

## 2. División en fragmentos

El contenido se divide en pequeños bloques llamados chunks.

Esto es necesario porque los modelos de embeddings trabajan mejor con fragmentos cortos y permite recuperar únicamente la información relevante.

Ejemplo:

```text
Chunk 1 → Becas y requisitos
Chunk 2 → Cancelación de materias
Chunk 3 → Faltas disciplinarias
```

## 3. Vectorización

Cada chunk se transforma en un embedding.

Un embedding es una representación numérica del significado semántico del texto.

Fragmentos con temas similares tendrán vectores cercanos entre sí.

## 4. Construcción de la base vectorial

Los embeddings se almacenan en una base vectorial.

Esta base permite encontrar rápidamente los fragmentos más relacionados con una pregunta del usuario.

## Reconstrucción de la base

Si se modifica el reglamento o se agregan documentos nuevos, ejecutar:

```bash
python ingestar.py
```

---

# Flujo de Consulta RAG

Cuando el usuario realiza una pregunta, el sistema sigue el siguiente proceso:

## Paso 1: Pregunta del usuario

Ejemplo:

```text
¿Qué ocurre si un estudiante pierde el promedio mínimo?
```

## Paso 2: Embedding de la pregunta

La pregunta también se convierte en un vector.

## Paso 3: Búsqueda semántica

La base vectorial compara el vector de la pregunta con los vectores almacenados.

Luego recupera los chunks más relevantes.

## Paso 4: Construcción del Prompt Aumentado

El sistema construye un prompt que contiene:

* Instrucciones del sistema.
* Contexto recuperado.
* Pregunta del usuario.

Ejemplo simplificado:

```text
[SISTEMA]
Responde únicamente usando el contexto.

[CONTEXTO]
Artículo 12: El estudiante pierde el cupo si el promedio es inferior a 3.0.

[PREGUNTA]
¿Qué ocurre si un estudiante pierde el promedio mínimo?
```

## Paso 5: Generación de respuesta

El modelo llama3 genera la respuesta utilizando el contexto recuperado.

---

# Estrategia Anti-Alucinación

Para reducir respuestas incorrectas o inventadas, el sistema implementa varias estrategias:

* Uso exclusivo del contexto recuperado.
* Restricción del prompt.
* Recuperación semántica previa.
* Fragmentación controlada.
* Separación entre conocimiento del modelo y documentos reales.

Ejemplo de instrucción:

```text
Si la respuesta no está en el contexto, indica que no se encontró información suficiente.
```

---

# Interfaz de Usuario

La interfaz fue desarrollada con Streamlit.

Características:

* Campo para preguntas.
* Respuesta generada por el sistema.
* Flujo sencillo y local.
* Interacción en tiempo real.

---

# Resultados Obtenidos

## Casos Correctos

El sistema respondió correctamente preguntas relacionadas con:

* Becas.
* Promedio mínimo.
* Cancelación de materias.
* Asistencia.
* Sanciones disciplinarias.

Ejemplos:

| Pregunta                                    | Resultado |
| ------------------------------------------- | --------- |
| ¿Cuál es el promedio mínimo?                | Correcto  |
| ¿Cuántas faltas permiten perder la materia? | Correcto  |
| ¿Cómo funcionan las becas?                  | Correcto  |

---

# Pruebas Anti-Alucinación

También se realizaron preguntas cuya respuesta no existía en el reglamento.

Ejemplo:

```text
¿La universidad entrega computadores gratis?
```

Resultado:

```text
No se encontró información suficiente en el contexto.
```

Esto demuestra que el sistema evita inventar información cuando no existe evidencia documental.

---

# Ventajas del Sistema

* Consultas rápidas.
* Menor riesgo de alucinaciones.
* Ejecución local.
* Fácil actualización del reglamento.
* Arquitectura escalable.
* Mejor experiencia de búsqueda académica.

---

# Limitaciones

* Depende de la calidad de los documentos.
* La precisión puede disminuir si los chunks son muy grandes.
* El modelo puede fallar si el contexto recuperado no es suficiente.
* Requiere recursos locales para ejecutar el LLM.

---

# Posibles Mejoras

* Agregar historial de conversaciones.
* Incorporar memoria contextual.
* Mejorar ranking de recuperación.
* Permitir múltiples documentos.
* Implementar citas automáticas.
* Agregar autenticación de usuarios.

---

# Estructura del Proyecto

```text
Proyecto/
│
├── app.py
├── ingestar.py
├── requirements.txt
├── README.md
├── documentos/
├── vectordb/
└── env/
```

---

# Conclusión

El proyecto demuestra cómo un sistema RAG puede utilizar recuperación semántica y modelos de lenguaje para responder preguntas académicas de manera más precisa y confiable.

La integración entre embeddings, búsqueda vectorial y generación de lenguaje permite crear asistentes inteligentes capaces de trabajar sobre documentación institucional real.

Además, el uso de Ollama y llama3 permite ejecutar toda la solución localmente sin depender de servicios externos.


## Construcción de la Base Vectorial

Si se modifica el reglamento o los documentos, ejecutar:

bash
python ingestar.py
