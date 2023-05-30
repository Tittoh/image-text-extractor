import requests
from flask import Flask, jsonify, request
import pytesseract
from PIL import Image
import os
from werkzeug.exceptions import BadRequest
import logging

app = Flask(__name__)

def validate_request(data):
    if 'image_urls' not in data:
        raise BadRequest("Missing 'image_urls' field in the request.")
    image_urls = data['image_urls']

    if not isinstance(image_urls, list) or not all(isinstance(url, str) for url in image_urls):
        raise BadRequest("'image_urls' must be a list of strings.")

    if len(image_urls) > 8:
        raise BadRequest("Maximum number of URLs allowed is 8.")

@app.route('/process_images', methods=['POST'])
def process_images():
    try:
        data = request.get_json()
        validate_request(data)
        image_urls = data['image_urls']

        results = []
        for image_url in image_urls:
            # Extract the image ID from the URL
            image_id = os.path.splitext(os.path.basename(image_url))[0]
            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                image = Image.open(response.raw)
                text = pytesseract.image_to_string(image)

                # Remove line breaks and replace with spaces
                text = text.replace('\n', ' ')


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
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.exception("Exception occurred during image processing")
        return jsonify({'error': 'An internal server error occurred.'}), 500

@app.route('/<path:path>')
def catch_all(path):
    error_message = {
        'error': 'Endpoint not found'
    }
    return jsonify(error_message), 404

if __name__ == '__main__':
    app.run(debug=True)
