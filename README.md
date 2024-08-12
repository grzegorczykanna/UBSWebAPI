Code task:

Create a web API that consumes data from a public API and exposes endpoints with the following data:

List the 10 biggest countries of a determined region of the world (Europe, Asia, Oceania, America, etc.).
List all the countries of a determined subregion (South America, West Europe, Eastern Asia, etc.) that has borders with more than 3 countries.
List the population of a subregion, including the countries that are part of it.

Requirements (must do):

All endpoints must support JSON and CSV as output format.
The code must be covered by tests, unit or/and integration.
The country data response object (used in points 1 and 2), must contain (at least) the following data:

Country Name
Capital
Region
Sub Region
Population
Area
Borders -> Each of the countries in the borders list should be the same object, containing the same data above (Optional)

Response object for point 3 is just a wrapper of the country data response, plus the total population of the subregion.

Nice to have (good to do):

Make the application available as a service in a container image.
You can use some caching mechanism to avoid repeated requests to the upstream and have faster responses.
Have documentation with instructions on how to run the application, what are the parameters used in the endpoints and anything else you consider necessary.

Data source:

There are many different websites that provide the required data for this task. You might choose any public service, if it is free, even if it requires authentication, you can choose whatever service you prefer. Here are a few examples:


https://restcountries.com/
https://countrylayer.com/
https://countryapi.io/

Task delivery:
You can publish your code directly to your GitHub account (or similar), no issues with it being publicly available. Or you can send us the solution via e-mail.
