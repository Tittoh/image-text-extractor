# Flask Image Text Extractor

Flask Image Text Extractor is a RESTful API that extracts text from online images. Given a list of image URLs, it processes each image, applies optical character recognition (OCR) using Tesseract, and returns the extracted text for each image.

## Features

- Extracts text from online images using Tesseract OCR.
- Supports processing multiple image URLs in a single request.
- Limits the maximum number of URLs to 8 per request.
- Provides error handling for invalid image URLs or processing failures.

## Requirements

- Python 3.6 or higher
- Flask
- requests
- Pillow
- pytesseract
- Tesseract OCR

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/tittoh/image-text-extractor.git
    ```

2. Install the dependencies using pip:

    ```shell
    pip install -r requirements.txt
    ```
3. Install Tesseract OCR. You can follow the installation instructions specific to your operating system:

    - **[Tesseract OCR Installation](https://github.com/tesseract-ocr/tessdoc/blob/main/Installation.md)**

## Usage

1. Start the Flask development server:
    ```shell
    python main.py
    ```
2. Make POST requests to the `/process_images` endpoint with the list of image URLs. For example:
    ```http
    POST /process_images HTTP/1.1
    Content-Type: application/json

    {
      "image_urls": [
        "http://example.com/image1.jpg",
        "http://example.com/image2.jpg",
        "http://example.com/image3.jpg"
      ]
    }
    ```
3. The API will process the images, extract the text using OCR, and return a response with the extracted text for each image.

## API Endpoints
### `POST /process_images`

Extracts text from online images.

Request Body
```json
{
  "image_urls": [
    "http://example.com/image1.jpg",
    "http://example.com/image2.jpg",
    "http://example.com/image3.jpg"
  ]
}
```
- `image_urls` (required): A list of image URLs to process. Maximum of 8 URLs allowed.

Response
```json
[
  {
    "id": "image1",
    "text": "Text extracted from image1.jpg"
  },
  {
    "id": "image2",
    "text": "Text extracted from image2.jpg"
  },
  {
    "id": "image3",
    "error": "Error message for image3.jpg"
  }
]
```
- `id`: The ID of the image (derived from the image URL's filename without the extension).
- `text`: The extracted text from the image.
- `error`: If an error occurs during image processing, an error message will be present instead of the `text` field.

## Testing
Run tests
```shell
python -m unittest test_main.py
```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the `MIT License`

*Feel free to customize and expand the README file to fit the specific details and requirements of your Flask Image Text Extractor app.*

