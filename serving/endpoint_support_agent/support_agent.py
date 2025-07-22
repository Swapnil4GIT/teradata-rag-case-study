from fastapi import FastAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import os
from SecretManager import SecretManager
from GcsManager import GcsManager
from dotenv import load_dotenv

load_dotenv()
PERSISTENCE_DIR = os.getenv("persistence_dir", "vector_db")
os.environ["OPENAI_API_KEY"] = os.getenv("llm_key", "dummy")

embeddings = OpenAIEmbeddings()
vectorstore = Chroma(persist_directory=PERSISTENCE_DIR, embedding_function=embeddings)
app = FastAPI()


@app.get("/predict")
def predict():
    collection = vectorstore._collection
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"The vectors have {dimensions:,} dimensions")
    return {"message": "Hello, World!"}
