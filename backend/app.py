from flask import Flask, request, jsonify
import requests
from endpoint_dc import EndpointDC
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["GET"])
def search_item():
    pass
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)