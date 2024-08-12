# API Documentation for Country Web API

## Overview

This Flask web API provides endpoints to retrieve information about countries, regions and subregions, utilizing data from the [Rest Countries API](https://restcountries.com/). It supports responses in both JSON and CSV formats and included caching for better performance.

## Table of Contents

- [API Documentation for Country Web API](#api-documentation-for-country-web-api)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Endpoints](#endpoints)
    - [Get the 10 biggest countries of a determined region of the world](#get-the-10-biggest-countries-of-a-determined-region-of-the-world)
      - [Endpoint](#endpoint)
      - [Method](#method)
      - [Parameters](#parameters)
      - [Response](#response)
      - [Example Request](#example-request)
      - [Example Response (CSV)](#example-response-csv)
    - [Get all countries of a determined subregion that has borders with more than 3 countries](#get-all-countries-of-a-determined-subregion-that-has-borders-with-more-than-3-countries)
      - [Endpoint](#endpoint-1)
      - [Method](#method-1)
      - [Parameters](#parameters-1)
      - [Response](#response-1)
      - [Example Request](#example-request-1)
      - [Example Response (JSON)](#example-response-json)
    - [Get the total population of a determined subregion](#get-the-total-population-of-a-determined-subregion)
      - [Endpoint](#endpoint-2)
      - [Method](#method-2)
      - [Parameters](#parameters-2)
      - [Response](#response-2)
      - [Example Request](#example-request-2)
      - [Example Response (JSON)](#example-response-json-1)
  - [Response Formats](#response-formats)
  - [Caching](#caching)
  - [Testing](#testing)

## Installation

To run the Flask web API locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/grzegorczykanna/UBSWebAPI.git
   cd UBSWebAPI/
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses Flask-Caching to cache responses. You can configure the cache settings in the app.py file:

   ```python
   config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}
```

## Endpoints

###  Get the 10 biggest countries of a determined region of the world

#### Endpoint
`/api/region/<region>/biggest_countries_in_region`

#### Method
`GET`

#### Parameters
- `region` The region to fetch data for (e.g. `europe`, `asia`).
- `format` Optional. Set to `csv` to receive the response in CSV format.

#### Response
- **Success**: Returns a JSON or CSV list of the 10 biggest countries of the determined region.
- **Error**: Returns an error message if the data could not be fetched.

#### Example Request

   ```bash
   GET /api/region/europe/biggest_countries_in_region?format=csv
   ```

#### Example Response (CSV)

   ```csv
   Country name,Capital,Region,Sub Region,Population,Area,Borders
   Russia,Moscow,Europe,Eastern Europe,144104080,17098242.0,"['AZE', 'BLR', 'CHN', 'EST', 'FIN', 'GEO', 'KAZ', 'PRK', 'LVA', 'LTU', 'MNG', 'NOR', 'POL', 'UKR']"
   Ukraine,Kyiv,Europe,Eastern Europe,44134693,603500.0,"['BLR', 'HUN', 'MDA', 'POL', 'ROU', 'RUS', 'SVK']"
   France,Paris,Europe,Western Europe,67391582,551695.0,"['AND', 'BEL', 'DEU', 'ITA', 'LUX', 'MCO', 'ESP', 'CHE']"
   Spain,Madrid,Europe,Southern Europe,47351567,505992.0,"['AND', 'FRA', 'GIB', 'PRT', 'MAR']"
   Sweden,Stockholm,Europe,Northern Europe,10353442,450295.0,"['FIN', 'NOR']"
   Germany,Berlin,Europe,Western Europe,83240525,357114.0,"['AUT', 'BEL', 'CZE', 'DNK', 'FRA', 'LUX', 'NLD', 'POL', 'CHE']"
   Finland,Helsinki,Europe,Northern Europe,5530719,338424.0,"['NOR', 'SWE', 'RUS']"
   Norway,Oslo,Europe,Northern Europe,5379475,323802.0,"['FIN', 'SWE', 'RUS']"
   Poland,Warsaw,Europe,Central Europe,37950802,312679.0,"['BLR', 'CZE', 'DEU', 'LTU', 'RUS', 'SVK', 'UKR']"
   Italy,Rome,Europe,Southern Europe,59554023,301336.0,"['AUT', 'FRA', 'SMR', 'SVN', 'CHE', 'VAT']"
```
### Get all countries of a determined subregion that has borders with more than 3 countries

#### Endpoint
`/api/subregion/<subregion>/countries_with_borders`

#### Method
`GET`

#### Parameters
- `subregion` The subregion to fetch data for (e.g. central europe).

#### Response
- **Success**: Returns a JSON list of countries that have more than 3 bordering countries.
- **Error**: Returns an error message if the data could not be fetched.

#### Example Request

   ```bash
   GET /api/subregion/central%20europe/countries_with_borders
   ```
#### Example Response (JSON)
   ```json
   [
    {
        "Country name": "Hungary",
        "Capital": "Budapest",
        "Region": "Europe",
        "Sub Region": "Central Europe",
        "Population": 9749763,
        "Area": 93028.0,
        "Borders": [
            "AUT",
            "HRV",
            "ROU",
            "SRB",
            "SVK",
            "SVN",
            "UKR"
        ]
    },
    ...
   ]
   ```


### Get the total population of a determined subregion

#### Endpoint
`/api/subregion/<subregion>/subregion_population`

#### Method
`GET`

#### Parameters
- `subregion` The subregion to fetch data for (e.g. central europe).

#### Response
- **Success**: Returns a JSON list of countries in the subregion with the total population of determined subregion.
- **Error**: Returns an error message if the data could not be fetched.

#### Example Request

   ```bash
   GET /api/subregion/central%20europe/subregion_population
   ```

#### Example Response (JSON)

 ```json
    [
     {
        "Country name": "Hungary",
        "Capital": "Budapest",
        "Region": "Europe",
        "Sub Region": "Central Europe",
        "Population": 9749763,
        "Area": 93028.0,
        "Borders": [
            "AUT",
            "HRV",
            "ROU",
            "SRB",
            "SVK",
            "SVN",
            "UKR"
        ]
     },

      ...

     {
        "Country name": "Slovakia",
        "Capital": "Bratislava",
        "Region": "Europe",
        "Sub Region": "Central Europe",
        "Population": 5458827,
        "Area": 49037.0,
        "Borders": [
            "AUT",
            "CZE",
            "HUN",
            "POL",
            "UKR"
        ]
     },
     {
        "Total population of subregion": 74875619
     }

```

## Response Formats

Responses can be returned in `JSON` or `CSV` format based on the format query parameter:

- **JSON**: The default response format.
- **CSV**: Use `?format=csv` to receive the response in CSV format.

## Caching

The API utilizes caching to improve performance. Responses are cached for a specified duration (default: 60 sec) using Flask-Caching. This helps avoid repeated requests to the upstream API.

## Testing

To run the tests for the application:

1. **Install pytest**:

   ```bash
   pip install pytest

2. **Run Tests**:

   ```bash
   pytest