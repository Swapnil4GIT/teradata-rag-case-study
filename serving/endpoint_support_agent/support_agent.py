import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from llm_request import LLMRequest
from schema import PredictRequest

logger = logging.getLogger(__name__)

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
    logger.info("Starting up the support agent application...")

    try:
        load_dotenv()
        PERSISTENCE_DIR = os.getenv("persistence_dir", "vector_db")
        os.environ["OPENAI_API_KEY"] = os.getenv("llm_key", "dummy")

        # Initialize embeddings
        embeddings = OpenAIEmbeddings()
        logger.info("Embeddings initialized successfully.")

        # Initialize vectorstore
        vectorstore = Chroma(
            persist_directory=PERSISTENCE_DIR, embedding_function=embeddings
        )
        logger.info("Vectorstore loaded successfully.")

        collection = vectorstore._collection
        sample_embedding = collection.get(limit=1, include=["embeddings"])[
            "embeddings"
        ][0]
        dimensions = len(sample_embedding)
        logger.info(f"The vectors have {dimensions:,} dimensions")

    except Exception as e:
        logger.error(f"Error during startup initialization: {e}")
        raise


@app.post("/predict")
def predict(payload: dict[str, str]):
    """
    Predict method that accepts a JSON payload.
    """
    try:
        request = PredictRequest.from_dict(payload)
        logger.info(request.query)
        logger.info(request.query_id)
        logger.info(request.session_id)
        llm = LLMRequest(
            vectorstore=vectorstore,
            query=request.query,
            prompt_name="system_prompt",
        )
        response = llm.invoke(request.query)
        return {"response": response}
    except Exception as e:
        logger.info(f"Error during prediction: {e}")
        return {"error": "An error occurred during prediction."}
