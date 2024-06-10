from flask import Flask, request
import requests
from flask_cors import CORS 

from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
indexer_url = os.getenv('AZURE_INDEXER_ENDPOINT')
container_name = os.getenv('AZURE_CONTAINER_NAME')
index_name = os.getenv('AZURE_INDEX_NAME')
credential = AzureKeyCredential(os.getenv('AZURE_AI_SEARCH_ADMIN_KEY'))

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)
try:
    container_client = blob_service_client.get_container_client(container=container_name) 
    container_client.get_container_properties()
except Exception as e:
    container_client = blob_service_client.create_container(container_name)

@app.route("/documents/", methods=["GET", "POST","DELETE"])  
def handle_documents():  
    if request.method == 'POST':
        for file in request.files.getlist('files'):
            try:
                container_client.upload_blob(file.filename, file)
                print(file.filename)
            except Exception as e:
                print(e)
    blob_items = container_client.list_blobs()
    documents = []
    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob=blob.name)
        document = {'url': blob_client.url, 'name': blob.name, 'created_on': blob.creation_time, 'size': round(blob.size/1024/1024, 2)}
        documents.append(document) 
    return documents

@app.route("/documents/<filename>", methods=["DELETE"])
def delete_document(filename):
    blob_client = container_client.get_blob_client(blob=filename)
    blob_client.delete_blob(delete_snapshots="include")
    return filename


@app.route("/indexer/", methods=["POST"])  
def run_indexer():
    headers = {
        'Content-Type': 'application/json',
        'api-key': os.getenv('AZURE_AI_SEARCH_ADMIN_KEY'),
    }
    requests.post(indexer_url, headers=headers)
    return "Indexer has ran successfully."

@app.route("/search/<full_text>", methods=["POST"])
def search(full_text):
    search_client = SearchClient(endpoint=os.getenv('AZURE_AI_SEARCH_ENDPOINT'), index_name=index_name, credential=credential, api_version="2024-05-01-preview")
    results = search_client.search(
        search_text=full_text,
        select='metadata_title,metadata_storage_path',
        highlight_pre_tag='<b>',
        highlight_post_tag='</b>',
        query_type='semantic',
        query_answer='extractive',
        query_caption='extractive',
        query_answer_threshold=0.1,
        semantic_configuration_name=os.getenv('AZURE_SEMANTIC_CONFIGURATION'),
        top=3) 
    res = []
    answers = []
    search_answers = results.get_answers()
    n = min(len(search_answers), 3)
    for i in range(n):
        answer = search_answers[i]
        answers.append({
            'text': answer.text,
            'highlights': answer.highlights
        })
    for result in results:
        print(result)
        captions = []
        search_captions = result.get('@search.captions', [])
        n = min(len(search_captions), 3)
        for i in range(n):
            caption = search_captions[i]
            captions.append({
                'text': caption.text,
                'highlights': caption.highlights
            })
        res.append({
            'title': result.get('metadata_title', ''),
            'url': result.get('metadata_storage_path', ''),
            'score': result.get('@search.score', ''),
            'reranker': result.get('@search.reranker_score', ''),
            'caption': captions,
            'answer': answers,
        })
    return res
if __name__ == "__main__":
    app.run(debug=True)