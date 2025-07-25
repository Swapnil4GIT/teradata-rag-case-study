import logging
import os
from time import time

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from llm_request import LLMRequest
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Import OpenTelemetry and Dynatrace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from schema import PredictRequest
from SecretManager import SecretManager

logger = logging.getLogger(__name__)

app = FastAPI()

# Global variables for embeddings and vectorstore
embeddings = None
vectorstore = None

# Initialize OpenTelemetry tracing
# TBD - Due to dynatrace account not available for me. I need a dynatrace host
# def init_tracing():
#     provider = TracerProvider()
#     exporter = OTLPSpanExporter(
#         endpoint=os.getenv("DYNATRACE_OTLP_ENDPOINT", "https://<YOUR_ENVIRONMENT_ID>.live.dynatrace.com/api/v2/otlp/v1/traces"),
#         headers={"Authorization": f"Api-Token {os.getenv('DYNATRACE_API_TOKEN')}"}
#     )
#     provider.add_span_processor(BatchSpanProcessor(exporter))
#     FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)

# TBD - Due to dynatrace host not available
# @app.on_event("startup")
# def startup_event():
#     init_tracing()
#     logger.info("Tracing initialized successfully.")


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
        os.environ["OPENAI_API_KEY"] = os.getenv("llm_key", "dummy")
        PERSISTENCE_DIR = os.getenv("persistence_dir", "vector_db")
        # project_number = os.getenv("project_number", "270035285032")
        # secret_manager = SecretManager(project_number)
        # os.environ["OPENAI_API_KEY"] = secret_manager.get_secret("llm_key")

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
        llm_start_time = time()
        response = llm.invoke(request.query)
        logger.info(f"LLM call latency in seconds: {time()-llm_start_time:.2f}")
        return {"response": response}
    except Exception as e:
        logger.info(f"Error during prediction: {e}")
        return {"error": "An error occurred during prediction."}
