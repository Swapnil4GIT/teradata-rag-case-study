from uuid import uuid4

import gradio as gr
import requests

# Define the FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/predict"


# Function to send a JSON payload to the FastAPI server
def chatbot_interface(user_input):
    try:
        # Prepare the JSON payload
        payload = {
            "query": user_input,
            "query_id": uuid4().hex,
            "session_id": uuid4().hex,
        }

        # Send the POST request to the FastAPI server
        response = requests.post(FASTAPI_URL, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json().get("response", "No response received.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


# Create the Gradio interface
interface = gr.Interface(
    fn=chatbot_interface,
    inputs="text",
    outputs="text",
    title="Employee Support Agent",
    description="Enter a message to interact with the Support Agent chatbot.",
)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch()
