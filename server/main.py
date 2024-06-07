from flask import Flask, request
from flask_cors import CORS 
from flask_session import Session

from azure.storage.blob import BlobServiceClient

import os   
import config

app = Flask(__name__)

app.config.from_object(config)
Session(app)

CORS(app, resources={r"/*":{"origins":"*"}})

@app.route("/documents", methods=["POST"])  
def upload_documents():  
    file_names = ""  
    for file in request.files.getlist("photos"):  
        filenames += file.filename + " "  
    return file_names

if __name__ == "__main__":
    app.run(debug=True)