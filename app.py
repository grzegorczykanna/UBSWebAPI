from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# datasource
API_URL = 'https://countryapi.io/api'
# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

@app.route('/api/all', methods=['GET'])
def get_country_info():
    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        # Send a GET request to the API
        response = requests.get(f'{API_URL}/all', headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Return the data as a JSON response
            return jsonify(data)
        else:
            # Handle different types of errors
            return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({"error": str(e)}), 500

@app.route('/api/region/<region>/10_biggest_countries', methods=['GET'])
def get_10_biggest_countries_by_region(region):
    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        # Send a GET request to the API
        response = requests.get(f'{API_URL}/region/{region}', headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

               # Extract relevant information: country name and area
            countries = [
                {
                    'name': country.get('name'),
                    'capital': country.get('capital'),
                    'region': country.get('region'),
                    'subregion': country.get('subregion'),
                    'population': country.get('population'),
                    'area': country.get('area'),
                    'borders': country.get('borders')
                } 
                for country in data.values() if country.get('area')
            ]
            
            # Sort countries by area in descending order
            countries_sorted = sorted(countries, key=lambda x: x['area'], reverse=True)
            
            # Get the top 10 countries
            top_10_countries = countries_sorted[:10]
            
            # Return the data as a JSON response
            return jsonify(top_10_countries)
        
        else:
            # Handle different types of errors
            return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)