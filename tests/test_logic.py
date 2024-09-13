import unittest
from unittest.mock import patch, MagicMock
from app.logic import location_to_dict
from datetime import datetime

class TestLogicFunctions(unittest.TestCase):

    @patch('app.logic.requests.get')
    @patch('os.getenv', return_value='dummy_key')  # Mock so we wont raise eror for missing env var API_KEY
    @patch('app.logic.datetime')
    def test_location_to_dict(self, mock_datetime, mock_getenv, mock_get):
        # Mocks logic to think its Saturday for dictionary order to stay consistent
        mock_datetime.today.return_value = datetime(2024, 9, 14)
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "resolvedAddress": "Holon, Israel",
            "currentConditions": {
                "temp": 38,
                "humidity": 50,
                "uvindex": 5,
                "sunrise": "06:00 AM",
                "sunset": "07:00 PM",
                "conditions": "Clear"
            },
            "days": [{"hours": [{"temp": temp} for _ in range(24)]} for temp in range(20, 27)]

        }
        mock_get.return_value = mock_response

        result = location_to_dict("New York")
        
        self.assertEqual(result["c_location"], "Holon, Israel")
        self.assertEqual(result["Saturday"], (20, 20))
        self.assertEqual(result["c_temp"], 38)
        self.assertEqual(result["c_humidity"], 50)
        self.assertEqual(result["c_uv"], 5)
        self.assertEqual(result["c_sunrise"], "06:00 AM")
        self.assertEqual(result["c_sunset"], "07:00 PM")
        self.assertEqual(result["c_description"], "Clear")

if __name__ == '__main__':
    unittest.main()
