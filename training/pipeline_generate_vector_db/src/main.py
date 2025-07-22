import functions_framework
import os
import glob
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

@functions_framework.http
def generate_vector_db(request):
    # Load environment variables
    load_dotenv()

    # Get the directory path from the request
    request_json = request.get_json(silent=True)
    if not request_json or 'directory_path' not in request_json:
        return 'Directory path not provided', 400

    directory_path = request_json['directory_path']

    # Load text files from the specified directory
    loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(documents)

    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(split_docs, embeddings)

    return 'Vector database generated successfully', 200
