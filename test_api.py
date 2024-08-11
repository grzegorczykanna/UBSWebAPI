import pytest
import json
from . import app #Make sure this matches the location of your Flask app

@pytest.fixture
def client():
    # Set up a test client for the Flask application
    with app.test_client() as client:
        app.testing = True
        yield client

def test_get_top_10_countries_by_population_json(client):
    # Send a GET request to the endpoint
    response = client.get('/api/region/europe/top10')

    # Check that the status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response is valid JSON
    data = json.loads(response.data)
    assert isinstance(data, list)

    # Check that there are exactly 10 countries in the response
    assert len(data) == 10

    # Check that each country has the expected keys
    for country in data:
        assert 'population' in country
        assert 'name' in country

def test_get_top_10_countries_by_population_csv(client):
    # Send a GET request to the endpoint with the CSV format
    response = client.get('/api/region/europe/top10?format=csv')

    # Check that the status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response is of type CSV
    assert response.mimetype == 'text/csv'

    # Check that the CSV contains the expected headers
    csv_content = response.data.decode('utf-8')
    assert 'population' in csv_content
    assert 'name' in csv_content

def test_region_not_found(client):
    # Send a GET request to a non-existent region
    response = client.get('/api/region/nonexistentregion/top10')

    # Check that the status code is not 200 (should be 404 or similar)
    assert response.status_code != 200

    # Check that the response contains an error message
    data = json.loads(response.data)
    assert 'error' in data
