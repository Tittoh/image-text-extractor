import requests
from flask import Flask, jsonify, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_images():
    data = request.get_json()
    image_urls = data.get('image_urls')

    results = []
    for image_url in image_urls:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            image = Image.open(response.raw)
            text = pytesseract.image_to_string(image)

            # Remove line breaks and replace with spaces
            text = text.replace('\n', ' ')

            # Extract the image ID from the URL
            image_id = os.path.splitext(os.path.basename(image_url))[0]

            result = {
                'id': image_id,
                'text': text
            }
            results.append(result)
        except Exception as e:
            error_message = {
                'id': image_id,
                'error': str(e)
            }
            results.append(error_message)

    return jsonify(results)

@app.route('/<path:path>')
def catch_all(path):
    error_message = {
        'error': 'Endpoint not found'
    }
    return jsonify(error_message), 404

if __name__ == '__main__':
    app.run(debug=True)
