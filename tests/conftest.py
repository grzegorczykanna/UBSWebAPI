from app.app import app
import time
import pytest

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