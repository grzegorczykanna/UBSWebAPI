import csv
from flask import Response
import io
import requests

API_URL = "https://restcountries.com/v3.1"


def fetch_data(type, name):
    """
    Fetch data from the API.

    Args:
        type (str): 'region' or 'subregion'
        name (str): The name of region/subregion to fetch data for.

    Returns:
        list: A list of country data for the region/subregion if successful, otherwise None.
    """
    # Construct the URL for fetching region data
    request_url = f"{API_URL}/{type}/{name}"

    # Send the request
    response = requests.get(request_url)

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()
    else:
        return None


def format_csv_output(result, total_population_entry=None):
    """
    Formats a list of dictionaries into a CSV output.

    Args:
        result (list): List of dictionaries containing the country data.
        total_population_entry (dict, optional): A dictionary containing the total population entry.
                                                 If provided, it will be added as the last row in the CSV.

    Returns:
        Response: A Flask Response object containing the CSV data.
    """
    # Create a CSV file
    output = io.StringIO()
    fieldnames = result[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(result[:-1] if total_population_entry else result)

    # Add a row for the total population entry
    if total_population_entry:
        total_population_key = list(total_population_entry.keys())[0]
        total_population_row = {field: "" for field in fieldnames}
        total_population_row["Country name"] = total_population_key
        total_population_row["Population"] = total_population_entry[
            total_population_key
        ]

        writer.writerow(total_population_row)

    output.seek(0)

    # Return the CSV data as a response
    return Response(output, mimetype="text/csv")


def build_result(countries, total_population=False):
    """
    Build a list of dictionaries for country data with optional total population.

    Args:
        countries (list): A list of country data dictionaries.
        total_population (bool): If True, includes total population entry at the end.

    Returns:
        list: A list of dictionaries containing country information.
    """
    result = [
        {
            "Country name": country.get("name").get("common"),
            "Capital": country.get("capital")[0],
            "Region": country.get("region"),
            "Sub Region": country.get("subregion"),
            "Population": country.get("population"),
            "Area": country.get("area"),
            "Borders": country.get("borders"),
        }
        for country in countries
    ]

    if total_population:
        # Calculate total population
        total_population_value = sum(country.get("population") for country in countries)
        # Wrap the country data response and the total population
        result.append({f"Total population of subregion": total_population_value})

    return result
