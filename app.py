from flask import Flask, jsonify
import requests

app = Flask(__name__)

API_URL = 'https://restcountries.com/v3.1'

# Route to get the 10 biggest countries by area in a region
@app.route('/api/region/<region>/biggest_countries_in_region', methods=['GET'])
def get_10_biggest_countries_by_area_for_region(region):
    # Construct the URL for fetching region data
    request_url = f'{API_URL}/region/{region}'
    
    # Send the request
    response = requests.get(request_url)
    
    if response.status_code == 200:
        data = response.json()

        # Sort countries by area in descending order
        sorted_countries = sorted(
            data,
            key=lambda country: country.get('area', 0),
            reverse=True
        )

        # Get the top 10 largest countries
        biggest_countries = sorted_countries[:10]
        
        # Build the result
        result = {
            f'10 biggest countries in {region.capitalize()}': [
                {
                    'Capital': country.get('capital'),
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders'),
                    'Country name': country.get('name', {}).get('common')
                }
                for country in biggest_countries if country.get('area')
            ]
        }

        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    
# Route to get the countries with over 3 borders in a subregion
@app.route('/api/subregion/<subregion>/countries_borders', methods=['GET'])
def get_all_countries_with_over_3_borders_for_subregion(subregion):
    # Construct the URL for fetching region data
    request_url = f'{API_URL}/subregion/{subregion}'
    
    # Send the request
    response = requests.get(request_url)
    
    if response.status_code == 200:
        data = response.json()
        
        result = {
            f'Countries in {subregion.title()} with more than 3 borders': [
                {
                    'Capital': country.get('capital'),
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders'),
                    'Country name': country.get('name', {}).get('common')
                }
                for country in data if len(country.get('borders')) > 3
            ]
        }

        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code
    
# Route to get the population in a subregion
@app.route('/api/subregion/<subregion>/region_population', methods=['GET'])
def get_the_population_for_subregion(subregion):
    # Construct the URL for fetching region data
    request_url = f'{API_URL}/subregion/{subregion}'
    
    # Send the request
    response = requests.get(request_url)
    
    if response.status_code == 200:
        data = response.json()

        total_population = 0

        # Calculate total population and list each country's population
        for country in data:
            population = country.get('population')
            total_population += population
        
        result = {
            'subregion': country.get('subregion'),
            'total_population': total_population,
        }

        
        result = {
            f'Total population in {subregion.title()}': total_population,
            f'Countries included in {subregion.title()}': [
                {
                    'Capital': country.get('capital'),
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders'),
                    'Country name': country.get('name', {}).get('common')
                }
                for country in data if country.get('population')
            ]
        }

        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)