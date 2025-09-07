from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["GET"])
def search_item():
    item = request.args.get("item", "")
    postal_code = "K1A0B1"  # <-- Replace with env var later!
    url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code={postal_code}&q={item}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    items = [
        {
            "name": i.get("name"),
            "price": i.get("current_price"),
            "merchant": i.get("merchant_name")
        }
        for i in data.get("items", [])
    ]
    return jsonify(items)

if __name__ == "__main__":
    app.run(port=5000, debug=True)