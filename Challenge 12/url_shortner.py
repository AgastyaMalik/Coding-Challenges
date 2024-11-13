from flask import Flask, request, jsonify, redirect, render_template
import hashlib
import os

app = Flask(__name__)

# In-memory dictionary to store URLs for simplicity
url_store = {}

# Define the base URL for shortened links
BASE_URL = "http://localhost:5000/"

# Endpoint to render HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")
    
    if not long_url:
        return jsonify({"error": "Missing field: url"}), 400
    
    hash_object = hashlib.md5(long_url.encode())
    short_key = hash_object.hexdigest()[:6]
    
    while short_key in url_store and url_store[short_key] != long_url:
        short_key = hashlib.md5((long_url + os.urandom(4).hex()).encode()).hexdigest()[:6]
    
    if short_key not in url_store:
        url_store[short_key] = long_url
    
    response = {
        "key": short_key,
        "long_url": long_url,
        "short_url": BASE_URL + short_key
    }
    return jsonify(response), 201

# Redirect to long URL
@app.route('/<short_key>', methods=['GET'])
def redirect_to_url(short_key):
    long_url = url_store.get(short_key)
    if long_url:
        return redirect(long_url, code=302)
    else:
        return jsonify({"error": "URL not found"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
