import requests
from flask import Flask, jsonify, request
import pytesseract
from PIL import Image

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

            result = {
                'url': image_url,
                'text': text
            }
            results.append(result)
        except Exception as e:
            error_message = {
                'url': image_url,
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
