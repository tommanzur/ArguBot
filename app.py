import chromadb
from llama_index.llms import Gemini
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.vector_stores import ChromaVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.storage.storage_context import StorageContext
from llama_index.service_context import ServiceContext
from llama_index.prompts import PromptTemplate
from flask import Flask, request

app = Flask(__name__, static_folder='src', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

documents = SimpleDirectoryReader('./documents').load_data()

llm = Gemini(temperature=0.2, model="gemini-pro")

db = chromadb.PersistentClient(path="./chroma_db_HF")
chroma_collection = db.get_or_create_collection("Tesis_Tomas_Manzur")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

svc = ServiceContext.from_defaults(embed_model=embed_model,llm=llm)
stc = StorageContext.from_defaults(vector_store=vector_store)

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

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = query_engine.query(user_input)
    print(response)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)