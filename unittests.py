import unittest
import json
from app import app 

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask application
        self.app = app.test_client()
        self.app.testing = True

    def test_get_10_biggest_countries_by_area_for_region_json(self):
        # Send a GET request to the endpoint
        response = self.app.get('/api/region/europe/biggest_countries_in_region')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is valid JSON
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

        # Check that there are exactly 10 countries in the response
        self.assertEqual(len(data), 10)

        # Check that each country has the expected keys
        for country in data:
            self.assertIn('Country name', country)
            self.assertIn('Capital', country)
            self.assertIn('Region', country)
            self.assertIn('Sub Region', country)
            self.assertIn('Population', country)
            self.assertIn('Area', country)
            self.assertIn('Borders', country)

    def test_get_10_biggest_countries_by_area_for_region_csv(self):
        # Send a GET request to the endpoint with the CSV format
        response = self.app.get('/api/region/europe/biggest_countries_in_region?format=csv')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is of type CSV
        self.assertEqual(response.mimetype, 'text/csv')

        # Check that the CSV contains the expected headers
        csv_content = response.data.decode('utf-8')
        self.assertIn('Country name', csv_content)
        self.assertIn('Capital', csv_content)
        self.assertIn('Region', csv_content)
        self.assertIn('Sub Region', csv_content)
        self.assertIn('Population', csv_content)
        self.assertIn('Area', csv_content)
        self.assertIn('Borders', csv_content)

    def test_region_not_found(self):
        # Send a GET request to a non-existent region
        # response = self.app.get('/api/region/Northern%20Europe/biggest_countries_in_region')
        response = self.app.get('/api/region/nonexistentregion/biggest_countries_in_region')

        # Check that the status code is not 200 (should be 404 or similar)
        self.assertNotEqual(response.status_code, 200)

        # Check that the response contains an error message
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_all_countries_with_over_3_borders_for_subregion_json(self):
            # Send a GET request to the endpoint
            response = self.app.get('/api/subregion/central%20europe/countries_borders')

            # Check that the status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Check that the response is valid JSON
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

            # Check that each country has the expected keys
            for country in data:
                self.assertIn('Country name', country)
                self.assertIn('Capital', country)
                self.assertIn('Region', country)
                self.assertIn('Sub Region', country)
                self.assertIn('Population', country)
                self.assertIn('Area', country)
                self.assertIn('Borders', country)

    def test_get_all_countries_with_over_3_borders_for_subregion_csv(self):
        # Send a GET request to the endpoint with the CSV format
        response = self.app.get('/api/subregion/central%20europe/countries_borders?format=csv')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is of type CSV
        self.assertEqual(response.mimetype, 'text/csv')

        # Check that the CSV contains the expected headers
        csv_content = response.data.decode('utf-8')
        self.assertIn('Country name', csv_content)
        self.assertIn('Capital', csv_content)
        self.assertIn('Region', csv_content)
        self.assertIn('Sub Region', csv_content)
        self.assertIn('Population', csv_content)
        self.assertIn('Area', csv_content)
        self.assertIn('Borders', csv_content)

    def test_subregion_not_found(self):
        # Send a GET request to a non-existent region
        # response = self.app.get('/api/region/Northern%20Europe/biggest_countries_in_region')
        response = self.app.get('/api/region/nonexistentregion/biggest_countries_in_region')

        # Check that the status code is not 200 (should be 404 or similar)
        self.assertNotEqual(response.status_code, 200)

        # Check that the response contains an error message
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_get_the_population_for_subregion_json(self):
            # Send a GET request to the endpoint
            response = self.app.get('/api/subregion/central%20europe/region_population')

            # Check that the status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Check that the response is valid JSON
            data = json.loads(response.data)
            self.assertIsInstance(data, list)

            # Check that each country has the expected keys
            for country in data:
                self.assertIn('Country name', country)
                self.assertIn('Capital', country)
                self.assertIn('Region', country)
                self.assertIn('Sub Region', country)
                self.assertIn('Population', country)
                self.assertIn('Area', country)
                self.assertIn('Borders', country)
                self.assertIn(f'Total population of Central Europe', country)

    def test_get_the_population_for_subregion_csv(self):
        # Send a GET request to the endpoint with the CSV format
        response = self.app.get('/api/subregion/central%20europe/region_population?format=csv')

        # Check that the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response is of type CSV
        self.assertEqual(response.mimetype, 'text/csv')

        # Check that the CSV contains the expected headers
        csv_content = response.data.decode('utf-8')
        self.assertIn('Country name', csv_content)
        self.assertIn('Capital', csv_content)
        self.assertIn('Region', csv_content)
        self.assertIn('Sub Region', csv_content)
        self.assertIn('Population', csv_content)
        self.assertIn('Area', csv_content)
        self.assertIn('Borders', csv_content)
        self.assertIn('Total population of Central Europe', csv_content)
        
    def test_subregion_not_found(self):
        # Send a GET request to a non-existent region
        # response = self.app.get('/api/region/Northern%20Europe/biggest_countries_in_region')
        response = self.app.get('/api/region/nonexistentregion/biggest_countries_in_region')

        # Check that the status code is not 200 (should be 404 or similar)
        self.assertNotEqual(response.status_code, 200)

        # Check that the response contains an error message
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
