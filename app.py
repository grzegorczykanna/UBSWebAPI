from flask import Flask, jsonify, request, Response
import requests
import csv
import io
import json

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
        result = [
                {
                    'Country name': country.get('name', {}).get('common'),
                    'Capital': country.get('capital')[0],
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders')
                }
                for country in biggest_countries if country.get('area')
            ]
        
        # Check if the user requested CSV format
        if request.args.get('format') == 'csv':
            # Create a CSV file in memory
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["Country name", "Capital", "Region", "Sub Region", "Population", "Area", "Borders"])
            writer.writeheader()
            writer.writerows(result)
            output.seek(0)
            
            # Return the CSV data as a response
            return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=biggest_countries_in_region.csv"})
        else:
            return Response(json.dumps(result, indent=4), mimetype='application/json')
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
        
        result = [
                {
                    'Country name': country.get('name', {}).get('common'),
                    'Capital': country.get('capital')[0],
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders')
                }
                for country in data if len(country.get('borders')) > 3
        ]

        # Check if the user requested CSV format
        if request.args.get('format') == 'csv':
            # Create a CSV file in memory
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["Country name", "Capital", "Region", "Sub Region", "Population", "Area", "Borders"])
            writer.writeheader()
            writer.writerows(result)
            output.seek(0)
            
            # Return the CSV data as a response
            return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=biggest_countries_in_region.csv"})
        else:
            return Response(json.dumps(result, indent=4), mimetype='application/json')
        
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

        
        result = [
            
                {
                    'Country name': country.get('name', {}).get('common'),
                    'Capital': country.get('capital')[0],
                    'Region': country.get('region'),
                    'Sub Region': country.get('subregion'),
                    'Population': country.get('population'),
                    'Area': country.get('area'),
                    'Borders': country.get('borders'),
                    f'Total population of {subregion.title()}': total_population
                }
                for country in data if country.get('population')
        ]

        # Check if the user requested CSV format
        if request.args.get('format') == 'csv':
            # Create a CSV file in memory
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=["Country name", "Capital", "Region", "Sub Region", "Population", "Area", "Borders", f"Total population of {subregion.title()}"])
            writer.writeheader()
            writer.writerows(result)
            output.seek(0)
            
            # Return the CSV data as a response
            return Response(output, mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=biggest_countries_in_region.csv"})
        else:
            return Response(json.dumps(result, indent=4), mimetype='application/json')
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)