# teradata-rag-case-study

## Training Pipeline Architecture

<img width="1451" height="764" alt="Training" src="https://github.com/user-attachments/assets/c603c8cb-4da3-46f7-8399-3ddfed650153" />


## Serving Pipeline Architecture

<img width="1443" height="790" alt="Serving" src="https://github.com/user-attachments/assets/629c5ec3-9e19-48ab-bbda-2471c91e4228" />

# Set up instructions for cloud platform
* Need GCP cloud access
* Need GCP project with admin access
* Create llm_key in secrete manager for OpenAI LLM
* Create cluster by the name support-agent-cluster
* Create gke service account and assign secret manager accessor role to the SA
* Create kubectl service account with name employee-support-agent
* Bind gke service account to kubectl service account
* Perform gcloud auth login
* Fetch credentials from support-agent-cluster:  gcloud container clusters get-credentials support-agent-cluster --zone <region> --project <project_id>
* Create artifact registry repo custom-image-registry manually from gcp console
* Create cloud build trigger pointing to training/generate-vector-db/build-deploy/cloudbuild.yaml
* Create cloud build trigger pointing to serving/endpoint_support_agent/cloudbuild.yaml
* Create cloud build trigger pointing to base_image/cloudbuild.yaml
* Run all the 3 trigger pointing to main branch
* Run command helm upgrade --install employee ./helm-charts/support-agent
* GKE pod should come up with 1 replica/ 500m CPU/ 1 Gi Memory
 
# Set up instructions for local
* Clone the repository
* Create .env in project root directory
* Add below 3 env variables to .env file -
  - llm_key = "Your open ai API key"
  - persistence_dir = "vector_db"
  - llm_model = "gpt-4o-mini"
* Look at the serving/endpoint_support_agent/support_agen.py and load the env variables from local .env file instead of GCP secret manager
* cd to serving/endpoint_support_agent and execute command -
  - uvicorn support_agent:app --reload
* Open new terminal window and execute below command -
  - curl -X POST http://127.0.0.1:8000/predict   -H "Content-Type: application/json"   -d '{"query": "Can you describe Insurellm in a few sentences?", "query_id": "1", "session_id": "1"}'
* Open new terminal again and execute below command -
  - cd UI
  - python gradio_chatbot.py
  - Open the gradio local app url in browser and chat with the chatbot
* Execute below command to turn it off -
  - In each terminal ctrl+c
  
  

