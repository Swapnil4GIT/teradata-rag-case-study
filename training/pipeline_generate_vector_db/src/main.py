import functions_framework
import os
import glob
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import logging

from shared.SecretManager import SecretManager

logger = logging.getLogger(__name__)

@functions_framework.http
def generate_vector_db(request):
    # Load environment variables
    load_dotenv()
    llm_key = os.getenv("llm_key")
    knowledge_base = os.getenv("knowledge_base")
    vector_db = os.getenv("vector_db")
    # Get the directory path from the request
    logger.info(f"llm_key: {llm_key}")
    logger.info(f"knowledge_base: {knowledge_base}")
    logger.info(f"vector_db: {vector_db}")