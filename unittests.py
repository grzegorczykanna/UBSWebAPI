import unittest
import json
from app import app  # Import your Flask app from the file where it's defined

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask application
        self.app = app.test_client()
        self.app.testing = True

    def test_get_top_10_countries_by_population_json(self):
        # Send a GET request to the endpoint
        response = self.app.get('/api/region/europe/top10')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is valid JSON
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # Check that there are exactly 10 countries in the response
        self.assertEqual(len(data), 10)

        # Check that each country has the expected keys
        for country in data:
            self.assertIn('population', country)
            self.assertIn('name', country)

    def test_get_top_10_countries_by_population_csv(self):
        # Send a GET request to the endpoint with the CSV format
        response = self.app.get('/api/region/europe/top10?format=csv')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is of type CSV
        self.assertEqual(response.mimetype, 'text/csv')

        # Check that the CSV contains the expected headers
        csv_content = response.data.decode('utf-8')
        self.assertIn('population', csv_content)
        self.assertIn('name', csv_content)

    def test_region_not_found(self):
        # Send a GET request to a non-existent region
        response = self.app.get('/api/region/nonexistentregion/top10')

        # Check that the status code is not 200 (should be 404 or similar)
        self.assertNotEqual(response.status_code, 200)

        # Check that the response contains an error message
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
