import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from llm_request import LLMRequest
from schema import PredictRequest

app = FastAPI()

# Global variables for embeddings and vectorstore
embeddings = None
vectorstore = None


@app.on_event("startup")
def load_resources():
    """
    Method executed when the app starts.
    Initializes embeddings and vectorstore.
    """
    global embeddings, vectorstore
    print("Initializing resources during app startup...")

    try:
        load_dotenv()
        PERSISTENCE_DIR = os.getenv("persistence_dir", "vector_db")
        os.environ["OPENAI_API_KEY"] = os.getenv("llm_key", "dummy")

        # Initialize embeddings
        embeddings = OpenAIEmbeddings()
        print("Embeddings initialized successfully.")

        # Initialize vectorstore
        vectorstore = Chroma(
            persist_directory=PERSISTENCE_DIR, embedding_function=embeddings
        )
        print("Vectorstore loaded successfully.")

        collection = vectorstore._collection
        sample_embedding = collection.get(limit=1, include=["embeddings"])[
            "embeddings"
        ][0]
        dimensions = len(sample_embedding)
        print(f"The vectors have {dimensions:,} dimensions")

    except Exception as e:
        print(f"Error during startup initialization: {e}")
        raise


@app.post("/predict")
def predict(payload: dict[str, str]):
    """
    Predict method that accepts a JSON payload.
    """
    try:
        request = PredictRequest.from_dict(payload)
        print(request.query)
        print(request.query_id)
        print(request.session_id)
        llm = LLMRequest(
            vectorstore=vectorstore,
            query=request.query,
            prompt_name="system_prompt",
        )
        response = llm.invoke(request.query)
        return {"response": response}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"error": "An error occurred during prediction."}
