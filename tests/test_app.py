import unittest
import requests

class TestFlaskApp(unittest.TestCase):
    BASE_URL = "http://localhost:9090"

    def test_homepage(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Enter your location:", response.text)

    def test_login_page(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<form', response.text)

    def test_valid_location_search(self):
        data = {
            'submit_button': 'check',
            'input_location': 'New York'
        }
        response = requests.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("New York, NY, United States", response.text)

    def test_invalid_location_search(self):
        data = {
            'submit_button': 'check',
            'input_location': 'InvalidLocation'
        }
        response = requests.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("THE LOCATION YOU ENTERED IS NOT VALID", response.text)

    def test_history_page(self):
        data = {
            'submit_button': 'history'
        }
        response = requests.post(self.BASE_URL, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Download weather history", response.text)

if __name__ == "__main__":
    unittest.main()
