from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv
import json
from urllib.parse import quote

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# datasource
API_URL = 'https://countryapi.io/api'
# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

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

@app.route('/api/region/<region>/borders', methods=['GET'])
def get_countries_with_over_3_borders_by_region(region):
    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    # Construct the final URL
    request_url = f'{API_URL}/region/{region}'
    
    # Debugging: Print the URL to the console
    print(f"Requesting data from: {request_url}")

    try:
        # Send a GET request to the API
        response = requests.get(request_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Filter countries with more than 3 borders
            countries_with_borders = [
                {
                    'name': country.get('name'),
                    'capital': country.get('capital'),
                    'region': country.get('region'),
                    'subregion': country.get('subregion'),
                    'population': country.get('population'),
                    'area': country.get('area'),
                    'borders': country.get('borders'),
                    'num_of_borders': len(country.get('borders', []))
                } 
                for country in data.values() if len(country.get('borders', [])) > 3
            ]
        
            return jsonify(countries_with_borders)
        # elif response.status_code == 404:
        #     return jsonify({"error": f"Subregion '{subregion}' not found in the external API"}), 404
   
        else:
            # Handle different types of errors
            return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({"error": str(e)}), 500

@app.route('/api/region/<region>/region_population', methods=['GET'])
def get_the_popultaion_of_region(region):
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

            total_population = 0
            countries_population = []

            # Calculate total population and list each country's population
            for country in data.values():
                name = country.get('name')
                capital = country.get('capital')
                region = country.get('region')
                subregion = country.get('subregion')
                area = country.get('area')
                borders = country.get('borders')
                population = country.get('population', 0)
                total_population += population
                countries_population.append({
                    'name': name,
                    'population': population,
                    'capital': capital,
                    'region': region,
                    'subregion': subregion,
                    'area': area,
                    'borders': borders
                })
            
            result = {
                'region': region,
                'total_population': total_population,
                'countries': countries_population
            }
            return jsonify(result)

        else:
            # Handle different types of errors
            return jsonify({"error": f"Failed to fetch data: {response.status_code}"}), response.status_code

    except Exception as e:
        # Handle any exceptions that occur
        return jsonify({"error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True)