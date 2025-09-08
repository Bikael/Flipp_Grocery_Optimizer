from flask import Flask, request, jsonify
import requests
from Sale_finder.endpoint_dc import EndpointDC
from deal_selector import DealSelector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["GET"])
def search_item():
    postal_code = "K1A0B1"
    dc = EndpointDC(postal_code, ["eggs"])
    items = dc.get_flyer_items(["walmart"])

    return items
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)