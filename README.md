# Athena

## Getting Started

### Server - Flask
1. Navigate to the `server` directory.
2. Create a `.env` file and set the following variables.
```
FLASK_APP=main.py
FLASK_DEBUG=1
AZURE_STORAGE_CONNECTION_STRING=""
AZURE_CONTAINER_NAME=""
AZURE_AI_SEARCH_ADMIN_KEY=""
AZURE_AI_SEARCH_ENDPOINT=""
AZURE_BLOB_ENDPOINT=""
AZURE_INDEXER_ENDPOINT=""
AZURE_INDEX_NAME=""
AZURE_SEMANTIC_CONFIGURATION=""
OPENAI_API_KEY=""
```
3. Start a virtual environment then run `pip install -r requirements.txt`. 
4. Run `flask run` to start the server.

### Client - VueJS
1. Navigate to the `client` directory.
2. Run `npm install`.
3. Run `npm run server`.
