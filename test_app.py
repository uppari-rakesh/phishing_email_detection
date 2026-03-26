import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_load(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_empty_input(self):
        response = self.app.post('/', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No input provided', response.data)

    def test_valid_input(self):
        # Assuming the model is loaded and works, this should return a prediction
        response = self.app.post('/', data={'email': 'Congratulations! You won a lottery.'})
        self.assertEqual(response.status_code, 200)
        # Check for the UI elements that appear on result
        self.assertTrue(b'Phishing' in response.data or b'Legitimate' in response.data)

if __name__ == '__main__':
    unittest.main()
