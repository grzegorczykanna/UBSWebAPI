import csv
from flask import Flask, jsonify, request, Response
import io
import json
import requests

app = Flask(__name__)

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
    return Response(output, mimetype="text/plain")


# Route to get the 10 biggest countries by area in a region
@app.route("/api/region/<region>/biggest_countries_in_region", methods=["GET"])
def get_10_biggest_countries_by_area_for_region(region):

    # Fetch the data from the API
    data = fetch_data("region", region)

    if data:
        # Sort countries by area in descending order
        sorted_data = sorted(
            data, key=lambda country: country.get("area"), reverse=True
        )

        # Get 10 biggest countries
        biggest_countries = sorted_data[:10]

        # Build the result
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
            for country in biggest_countries
            if country.get("area")
        ]

        # Check if the user requested CSV format
        if request.args.get("format") == "csv":
            # Return a CSV response
            return format_csv_output(result)

        # Return a JSON response
        return Response(json.dumps(result, indent=4), mimetype="application/json")

    else:
        return jsonify({"error": "Failed to fetch data"}), 500


# Route to get the countries with over 3 borders in a subregion
@app.route("/api/subregion/<subregion>/countries_borders", methods=["GET"])
def get_all_countries_with_over_3_borders_for_subregion(subregion):

    data = fetch_data("subregion", subregion)

    if data:
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
            for country in data
            if len(country.get("borders")) > 3
        ]

        if request.args.get("format") == "csv":
            return format_csv_output(result)

        return Response(json.dumps(result, indent=4), mimetype="application/json")

    else:
        return jsonify({"error": "Failed to fetch data"}), 500


# Route to get the population in a subregion
@app.route("/api/subregion/<subregion>/subregion_population", methods=["GET"])
def get_the_population_for_subregion(subregion):

    data = fetch_data("subregion", subregion)

    if data:

        # Calculate the total population for the subregion
        total_population = sum(country.get("population") for country in data)

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
            for country in data
            if country.get("population")
        ]

        # Wrap the country data response and the total population
        result.append({f"Total population of {subregion.title()}": total_population})

        if request.args.get("format") == "csv":
            total_population_entry = result[-1]

            return format_csv_output(
                result, total_population_entry=total_population_entry
            )

        return Response(json.dumps(result, indent=4), mimetype="application/json")

    else:
        return jsonify({"error": "Failed to fetch data"}), 500


if __name__ == "__main__":
    app.run(debug=True)
