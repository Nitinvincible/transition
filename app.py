from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import http.client
import json

app = Flask(__name__)
CORS(app)

@app.route("/app/video", methods=["GET"])
def get_video():
    try:
        # Get query parameters
        query = request.args.get("query", "nature")  # Default search query is 'nature'
        per_page = request.args.get("per_page", 1)  # Default per page is 1

        # Create connection to Pexels API via HTTPS
        conn = http.client.HTTPSConnection("api.pexels.com")
        # Construct the URL with query and per_page
        url = f"/videos/search?query={query}&per_page={per_page}"
        
        # Set headers
        headers = {
            "Authorization": "N82L58IngLOXoFT5MF1UiQu2U61HsxFUAj5TGUAS2hSGdBXqGp5k9cVl"  # Replace with your Pexels API key
        }
        
        # Make the request
        conn.request("GET", url, headers=headers)
        # Get the response
        response = conn.getresponse()
        
        # If the request was successful, parse and return the data
        if response.status == 200:
            data = response.read().decode("utf-8")
            return jsonify(json.loads(data))
        else:
            return jsonify({"error": "Failed to fetch data from Pexels API"}), response.status
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()  # Ensure the connection is closed

if __name__ == "__main__":
    app.run(ssl_context=('d:/transition/pexels-video-app/backend/cert.pem', 'd:/transition/pexels-video-app/backend/key.pem'),
             host='0.0.0.0', port=443, debug=True)