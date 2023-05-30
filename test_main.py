import unittest
from unittest.mock import patch, Mock
from main import app
import requests


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_process_images_success(self):
        payload = {
            'image_urls': [
                'http://example.com/image1.jpg',
                'http://example.com/image2.jpg'
            ]
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        self.assertIn('id', data[0])
        result = data[0]
        if 'error' not in result:
            self.assertIn('text', result)

        self.assertIn('id', data[1])
        result = data[1]
        if 'error' not in result:
            self.assertIn('text', result)

    def test_process_images_missing_field(self):
        payload = {}  # Missing 'image_urls' field
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "400 Bad Request: Missing 'image_urls' field in the request.")

    def test_process_images_invalid_data_type(self):
        payload = {
            'image_urls': 'invalid'
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], "400 Bad Request: 'image_urls' must be a list of strings.")

    def test_catch_all_endpoint(self):
        response = self.app.get('/invalid_endpoint')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'Endpoint not found')

    def test_process_images_empty_urls(self):
        payload = {
            'image_urls': []
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    @patch('main.requests.get')
    def test_process_images_invalid_url(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException()
        mock_get.return_value = mock_response

        payload = {
            'image_urls': ['http://example.com/image.jpg']
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('id', data[0])
        self.assertIn('error', data[0])

    @patch('main.requests.get')
    def test_process_images_network_error(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException()
        mock_get.return_value = mock_response

        payload = {
            'image_urls': ['http://example.com/image.jpg']
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('id', data[0])
        self.assertIn('error', data[0])

    @patch('main.requests.get')
    def test_process_images_timeout(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()
        mock_get.return_value = mock_response

        payload = {
            'image_urls': ['http://example.com/image.jpg']
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('id', data[0])
        self.assertIn('error', data[0])

    def test_process_images_security(self):
        payload = {
            'image_urls': ['http://example.com/image.jpg?param=<script>alert("XSS")</script>']
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn('id', data[0])
        self.assertIn('error', data[0])
        self.assertNotIn('text', data[0])
  
    def test_process_images_max_urls(self):
        payload = {
            'image_urls': [
                'http://example.com/image1.jpg',
                'http://example.com/image2.jpg',
                'http://example.com/image3.jpg',
                'http://example.com/image4.jpg',
                'http://example.com/image5.jpg',
                'http://example.com/image6.jpg',
                'http://example.com/image7.jpg',
                'http://example.com/image8.jpg',
                'http://example.com/image9.jpg'  # Exceeds the maximum limit
            ]
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(data, dict)
        self.assertIn('error', data)
        self.assertEqual(data['error'], '400 Bad Request: Maximum number of URLs allowed is 8.')

    def test_process_images_boundary_cases(self):
        payload = {
            'image_urls': [
                'http://example.com/image.jpg',
                'http://example.com/short_url',
                'http://example.com/very_long_url/with_long_path/and_file_name_1234567890.jpg',
                'http://example.com/image.jpg?param=special&extension=.png',
            ]
        }
        response = self.app.post('/process_images', json=payload)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        for result in data:
            self.assertIn('id', result)
            if 'error' not in result:
                self.assertNotIn('error', result)
                self.assertIn('text', result)
            else:
                self.assertIn('error', result)
                self.assertNotIn('text', result)


if __name__ == '__main__':
    unittest.main()
