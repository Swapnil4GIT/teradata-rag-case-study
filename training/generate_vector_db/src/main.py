import functions_framework
import os
import logging
from dotenv import load_dotenv
from SecretManager import SecretManager

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Ensure logs are sent to stdout
)
logger = logging.getLogger(__name__)

class VectorDBGenerator:
    def __init__(self):
        """
        Initialize the VectorDBGenerator by loading environment variables and setting up the SecretManager.
        """
        # Load environment variables
        load_dotenv()
        self.llm_key = os.getenv("llm_key")
        self.knowledge_base = os.getenv("knowledge_base")
        self.vector_db = os.getenv("vector_db")
        self.project_id = os.getenv("project_id")
        self.project_number = os.getenv("project_number")

        # Log the loaded environment variables
        logger.info(f"llm_key: {self.llm_key}")
        logger.info(f"knowledge_base: {self.knowledge_base}")
        logger.info(f"vector_db: {self.vector_db}")

        # Initialize the SecretManager
        self.secret_manager = SecretManager(self.project_number)

    def get_llm_key(self):
        """
        Retrieve the OpenAI API key from Google Secret Manager.
        
        Returns:
            str: The OpenAI API key.
        """
        return self.secret_manager.get_secret("llm_key")

    def generate(self, request):
        """
        Main method to handle the vector database generation logic.
        
        Args:
            request: The HTTP request object.

        Returns:
            dict: A response dictionary indicating success or failure.
        """
        try:
            llm_key = self.get_llm_key()
            logger.info(f"Retrieved OpenAI API Key:")
            # Add your vector database generation logic here
            return {"status": "success", "message": "Vector database generated successfully"}
        except Exception as e:
            logger.error(f"Error generating vector database: {e}")
            return {"status": "error", "message": str(e)}

# Example usage in a Cloud Function
@functions_framework.http
def generate_vector_db(request):
    generator = VectorDBGenerator()
    response = generator.generate(request)
    return response  # Ensure a valid response is returned