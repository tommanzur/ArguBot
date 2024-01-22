"""## **Argubot**: Un Cchatbot sobre la tesis doctoral de Tomás Manzur
"CONSTRUCCIÓN DE ARGUMENTOS Y CONTROVERSIAS SOCIO-TÉCNICAS:
Análisis de la conflictividad surgida en la discusión del Plan
Provincial de Ordenamiento Territorial de la Provincia de Mendoza"

# Descripción del Chatbot "ArguBot": Herramienta Interactiva y Segura
para Consultas sobre la Tesis Doctoral de Tomás Manzur

## Introducción
El **ArguBot** es un chatbot revolucionario, diseñado para ofrecer
asistencia especializada en consultas sobre la tesis doctoral de Tomás Manzur,
"Construcción de Argumentos y Controversias Socio-Técnicas".

Este bot se destaca por su análisis avanzado y su enfoque en la
**privacidad del usuario** y el uso de **fuentes de código abierto**.

## Funcionalidades Clave

### Uso Exclusivo de Fuentes Open Source
ArguBot está construido con fuentes de código abierto, incluyendo:
- Modelo Gemini de Google
- 'llamaindex' para gestión de datos
- 'chromadb' para búsquedas eficientes
Esto asegura **transparencia** y **adaptabilidad**.

### Privacidad del Usuario
La interacción con el bot requiere una **API_KEY**, ingresada de manera segura
mediante `getpass`. Esto garantiza la **confidencialidad** y la
**protección de los datos del usuario**.

### Implementación en Jupyter Notebook
ArguBot aprovecha la flexibilidad del entorno Jupyter Notebook,
permitiendo una implementación sencilla y personalizable,
con altos estándares de seguridad.

### Funciones Integradas
- **Consulta de Contenidos Específicos:** Respuestas detalladas sobre la tesis.
- **Análisis de Argumentos:** Explica argumentos manteniendo la confidencialidad.
- **Contextualización del Conflicto:** Información segura sobre el Plan de Ordenamiento Territorial.
- **Recursos Adicionales:** Enlaces a publicaciones y materiales relacionados que respetan la privacidad.

## Aplicación Práctica
ArguBot es una herramienta interactiva y educativa avanzada para académicos
y estudiantes en sociología y planificación territorial.
Su énfasis en la seguridad y privacidad, junto con su construcción basada
en fuentes de código abierto, lo convierte en un recurso valioso y confiable
para la investigación y el aprendizaje.
"""

import os
import chromadb
import requests
from getpass import getpass
from llama_index.llms import OpenAI, Gemini
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.response.notebook_utils import display_response
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.storage.storage_context import StorageContext
from llama_index.service_context import ServiceContext
from llama_index.prompts import PromptTemplate

GOOGLE_API_KEY = getpass("""Ingreso de Google API Key
                         Para comenzar a interactuar con el **ArguBot**, es
                         necesario que ingreses tu **Google API Key**. 
                         Por favor, introduce tu clave en el campo de entrada a continuación.
                         Recuerda que utilizamos `getpass` para asegurar que tu clave 
                         se mantendra **totalmente secreta** y **segura**.
                         Con `getpass`, tu clave **no se almacena** y se mantiene
                         confidencial dentro de la sesión actual del usuario.
                         Tu privacidad y seguridad son nuestra máxima prioridad.
                         Por favor, ingresa tu Google API Key aquí:""")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

with requests.get('https://drive.google.com/file/d/1iFHzW_QO_f6LJzBiOB5ZM7taxAvf7Jgr/view?usp=drive_link', stream=True) as r:
    r.raise_for_status()
    with open('/content/src/data.txt', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

### Cargando documentos
documents = SimpleDirectoryReader('src').load_data()

llm = Gemini(temperature=0.2, model="gemini-pro")

db = chromadb.PersistentClient(path="./chroma_db_HF")

# create collection
chroma_collection = db.get_or_create_collection("Tesis_Tomas_Manzur")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

### Seteando el service context y el storage context cambiando los valores default
svc = ServiceContext.from_defaults(embed_model=embed_model,llm=llm)
stc = StorageContext.from_defaults(vector_store=vector_store)

## Creando un nuevo index
index = VectorStoreIndex.from_documents(
    documents, storage_context=stc, service_context=svc
)

query_engine = index.as_query_engine()

template = (
    "Dado el contexto que te proporcionare responde las preguntas \n"
    "Contexto:\n"
    "################################\n"
    "{context_str}"
    "################################\n"
    "Responde en español como si fueras sociologo experto en controversias sociotécnicas y en análisis de conflictos sociales, políticos, ambientales y territoriales: {query_str}\n"
)
qa_template = PromptTemplate(template)
query_engine.update_prompts(
    {"response_synthesizer:text_qa_template": qa_template}
)

response = query_engine.query('Qué dice Tomás Manzur en su tesis doctoral?')
display_response(response)

i = 0
while i < 10:
  inp = input("User: ")
  response = query_engine.query(inp)
  display_response(response)
  i + 1