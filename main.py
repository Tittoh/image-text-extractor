import requests
from flask import Flask, jsonify, request
import pytesseract
from PIL import Image

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()
    image_link = data.get('image_link')
    unique_id = data.get('unique_id')

    try:
        response = requests.get(image_link, stream=True)
        response.raise_for_status()
        image = Image.open(response.raw)
        text = pytesseract.image_to_string(image)

        # Remove line breaks and replace with spaces
        text = text.replace('\n', ' ')


        result = {
            'id': unique_id,
            'text': text
        }
        return jsonify(result)
    except Exception as e:
        error_message = {
            'error': str(e)
        }
        return jsonify(error_message), 400

if __name__ == '__main__':
    app.run(debug=True)
