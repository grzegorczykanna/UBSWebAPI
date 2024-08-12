from .app import app
import json
import pytest
import time


@pytest.fixture
def client():
    # Set up a test client for the Flask application
    with app.test_client() as client:
        app.testing = True
        yield client


@pytest.fixture
def expected_countries_europe():
    # Define the expected 10 biggest countries by area in Europe
    return [
        "Russia",
        "Ukraine",
        "France",
        "Spain",
        "Sweden",
        "Germany",
        "Finland",
        "Norway",
        "Poland",
        "Italy",
    ]


@pytest.fixture(scope="session", autouse=True)
def measure_total_time():
    start_time = time.time()
    yield
    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\nTotal time taken for all tests: {total_duration:.4f} seconds")


def test_get_10_biggest_countries_by_area_for_region_json(
    client, expected_countries_europe
):

    # Send a GET request to the endpoint
    response = client.get("/api/region/europe/biggest_countries_in_region")
    # Check that the status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response is valid JSON
    data = json.loads(response.data)
    assert isinstance(data, list)

    # Check that there are exactly 10 countries in the response
    assert len(data) == 10

    # Check the names of the countries returned by the API
    # are the same as expected
    countries_europe = [country["Country name"] for country in data]
    assert countries_europe == expected_countries_europe

    # Check that each country has the expected keys
    for country in data:
        assert "Country name" in country
        assert "Capital" in country
        assert "Region" in country
        assert "Sub Region" in country
        assert "Population" in country
        assert "Borders" in country


def test_get_10_biggest_countries_by_area_for_region_csv(client):

    # Send a GET request to the endpoint with the CSV format
    response = client.get("/api/region/europe/biggest_countries_in_region?format=csv")
    # Check that the status code is 200 (OK)
    assert response.status_code == 200

    # Check that the response is of desired type
    assert response.mimetype == "text/plain"

    # Check that the CSV contains the expected headers
    countries_csv = response.data.decode("utf-8")
    assert "Country name" in countries_csv
    assert "Capital" in countries_csv
    assert "Region" in countries_csv
    assert "Sub Region" in countries_csv
    assert "Population" in countries_csv
    assert "Borders" in countries_csv


def test_region_not_found(client):

    # Send a GET request to a non-existent region
    response = client.get("/api/region/nonexistentregion/biggest_countries_in_region")

    # Check that the status code is not 200
    assert response.status_code != 200

    # Check that the response contains an error message
    data = json.loads(response.data)
    assert "error" in data


def test_get_all_countries_with_over_3_borders_for_subregion_json(client):

    response = client.get("/api/subregion/central%20europe/countries_borders")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)

    for country in data:
        assert "Country name" in country
        assert "Capital" in country
        assert "Region" in country
        assert "Sub Region" in country
        assert "Population" in country
        assert "Borders" in country


def test_get_all_countries_with_over_3_borders_for_subregion_csv(client):

    response = client.get(
        "/api/subregion/central%20europe/countries_borders?format=csv"
    )
    assert response.status_code == 200
    assert response.mimetype == "text/plain"

    countries_csv = response.data.decode("utf-8")
    assert "Country name" in countries_csv
    assert "Capital" in countries_csv
    assert "Region" in countries_csv
    assert "Sub Region" in countries_csv
    assert "Population" in countries_csv
    assert "Borders" in countries_csv


def test_subregion_not_found_borders(client):

    response = client.get("/api/subregion/nonexistentsubregion/countries_borders")
    assert response.status_code != 200

    data = json.loads(response.data)
    assert "error" in data


def test_get_the_population_for_subregion_json(client):

    response = client.get("/api/subregion/central%20europe/subregion_population")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)

    for country in data[:-1]:
        assert "Country name" in country
        assert "Capital" in country
        assert "Region" in country
        assert "Sub Region" in country
        assert "Population" in country
        assert "Borders" in country

    assert isinstance(data[-1], dict)
    assert any(f"Total population of Central Europe" in key for key in data[-1].keys())


def test_get_the_population_for_subregion_csv(client):

    response = client.get(
        "/api/subregion/central%20europe/subregion_population?format=csv"
    )
    assert response.status_code == 200
    assert response.mimetype == "text/plain"

    countries_csv = response.data.decode("utf-8")
    assert "Country name" in countries_csv
    assert "Capital" in countries_csv
    assert "Region" in countries_csv
    assert "Sub Region" in countries_csv
    assert "Population" in countries_csv
    assert "Borders" in countries_csv
    assert f"Total population of Central Europe" in countries_csv


def test_subregion_not_found_total_population(client):

    response = client.get("/api/subregion/nonexistentsubregion/subregion_population")
    assert response.status_code != 200

    data = json.loads(response.data)
    assert "error" in data
