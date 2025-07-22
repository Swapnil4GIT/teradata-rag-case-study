from google.cloud import secretmanager

class SecretManager:
    def __init__(self, project_number):
        """
        Initialize the SecretManager with the Google Cloud project ID.
        """
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_number = project_number

    def get_secret(self, secret_name):
        """
        Retrieve the secret value from Google Secret Manager.
        
        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The secret payload as a string.
        """
        # Build the resource name of the secret
        secret_resource_name = f"projects/{self.project_number}/secrets/{secret_name}/versions/1"

        # Access the secret
        response = self.client.access_secret_version(name=secret_resource_name)

        # Extract the secret payload
        secret_payload = response.payload.data.decode("UTF-8")

        return secret_payload

# Example usage
if __name__ == "__main__":
    project_number = "your_project_number"  # Replace with your actual project ID
    secret_manager = SecretManager(project_number)
    openai_api_key = secret_manager.get_secret("openai-api-key")