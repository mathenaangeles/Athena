from flask import Flask
from flask_cors import CORS 
from flask_session import Session

import config

app = Flask(__name__)

app.config.from_object(config)
Session(app)

CORS(app, resources={r"/*":{"origins":"*"}})

@app.route("/login")
def login():
    return None

if __name__ == "__main__":
    app.run(debug=True)