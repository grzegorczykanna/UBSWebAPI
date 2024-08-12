import csv
from flask import Flask, jsonify, request, Response
import io
import json
import requests
from utils.utils import fetch_data, format_csv_output, build_result

app = Flask(__name__)

API_URL = "https://restcountries.com/v3.1"


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

        # Select 10 biggest countries
        biggest_countries = sorted_data[:10]

        # Build the result output
        result = build_result(biggest_countries)

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
        # Select the countries with over 3 borders
        countries_borders = [
            country for country in data if len(country.get("borders")) > 3
        ]

        result = build_result(countries_borders)

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
        result = build_result(data, total_population=True)

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
