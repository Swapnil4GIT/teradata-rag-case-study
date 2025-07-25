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

# Screenshots from my system

* Sample Query1
  <img width="1673" height="587" alt="test1" src="https://github.com/user-attachments/assets/6ce33f9e-5246-4ab8-ad07-a517c48c6eb3" />

* Sample Query2
  <img width="1611" height="621" alt="test2" src="https://github.com/user-attachments/assets/7bfedc47-0517-46b6-a715-ea6fcfc8c2f2" />

* Terminal Http api status
  <img width="1668" height="945" alt="Terminal" src="https://github.com/user-attachments/assets/78bd6630-d66a-4602-a3ec-d83d968a4fc6" />

# Sample Queries for users to try

* Tell me about your insurance products
* Which employee got the prestigious award
* What is insurellm?
* What is Samantha Green's career history?
* What is compensation history of Emily?

  



  

