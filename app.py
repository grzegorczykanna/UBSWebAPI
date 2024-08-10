from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Replace 'your_api_key' with your actual API key
API_KEY = 'pPosOzAUOydzP83b3QYQPDPlmIdLGw5ngjlxknV8'
API_URL = 'https://countryapi.io/api'

@app.route('/api/all', methods=['GET'])
def get_country_info():

    # Set up the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Send a GET request to the API
    response = requests.get(f'{API_URL}/all', headers=headers)
    
    # Parse the JSON response
    data = response.json()

    # Return the data as a JSON response
    return jsonify(data)

# Route to get countries by region
@app.route('/api/region/<region>', methods=['GET'])
def get_countries_by_region(region):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(f'{API_URL}/region/{region}', headers=headers)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)