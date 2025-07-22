import glob
import logging
import os

import functions_framework
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from SecretManager import SecretManager

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Ensure logs are sent to stdout
)
logger = logging.getLogger(__name__)


class VectorDBGenerator:
    def __init__(self):
        """
        Initialize the VectorDBGenerator by loading environment variables and
        setting up the SecretManager.
        """
        # Load environment variables
        load_dotenv()
        self.llm_key = os.getenv("llm_key")
        self.knowledge_base = os.getenv("knowledge_base")
        self.vector_db = os.getenv("vector_db")
        self.project_id = os.getenv("project_id")
        self.project_number = os.getenv("project_number")

        # Log the loaded environment variables
        print(f"llm_key: {self.llm_key}")
        print(f"knowledge_base: {self.knowledge_base}")
        print(f"vector_db: {self.vector_db}")

        # Initialize the SecretManager
        self.secret_manager = SecretManager(self.project_number)
        os.environ["OPENAI_API_KEY"] = self.secret_manager.get_secret("llm_key")

    def generate(self, request):
        """
        Generate the vector database using the provided request data.
        """
        print("Received request for vector generation.")

        try:
            folders = glob.glob("knowledge-base/*")
            if not folders:
                raise FileNotFoundError(
                    "No folders found in the 'knowledge-base' directory."
                )
        except FileNotFoundError as fnf_error:
            print(f"File not found error: {fnf_error}")
            raise
        except Exception as e:
            print(f"Unexpected error while accessing folders: {e}")
            raise

        text_loader_kwargs = {"encoding": "utf-8"}
        documents = []
        try:
            for folder in folders:
                doc_type = os.path.basename(folder)
                loader = DirectoryLoader(
                    folder,
                    glob="**/*.md",
                    loader_cls=TextLoader,
                    loader_kwargs=text_loader_kwargs,
                )
                folder_docs = loader.load()
                for doc in folder_docs:
                    doc.metadata["doc_type"] = doc_type
                    documents.append(doc)
        except Exception as e:
            print(f"Error while processing documents in folder '{folder}': {e}")
            raise

        try:
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            print(f"Loaded {len(chunks)} chunks from the documents.")
        except Exception as e:
            print(f"Error while splitting documents into chunks: {e}")
            raise

        embeddings = OpenAIEmbeddings()

        if os.path.exists(self.vector_db):
            Chroma(
                persist_directory=self.vector_db, embedding_function=embeddings
            ).delete_collection()

        try:
            vectorstore = Chroma.from_documents(
                documents=chunks, embedding=embeddings, persist_directory=self.vector_db
            )
            print(
                f"Vectorstore created with {vectorstore._collection.count()} documents."
            )
        except Exception as e:
            print(f"Error while creating the vectorstore: {e}")
            raise

        print(f"Vectorstore created with {vectorstore._collection.count()} documents")

        return {"status": "Vector database generation initiated."}


# Example usage in a Cloud Function
@functions_framework.http
def generate_vector_db(request):
    generator = VectorDBGenerator()
    response = generator.generate(request)
    return response  # Ensure a valid response is returned
