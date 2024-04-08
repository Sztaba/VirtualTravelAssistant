import requests


# with open('outputfile.json', 'wb') as outf:
#     outf.write(response.content)

def getPoisCityRadius(cityName, radius, apikey="5ae2e3f221c38a28845f05b6975076af4d407c5597b65a8c85c662b7"):
    request = "http://api.opentripmap.com/0.1/en/places/geoname?name=" + cityName + "&apikey=" + apikey
    response = requests.get(request)
    dict = response.json()
    request = "http://api.opentripmap.com/0.1/en/places/radius?format=json&radius=" + str(radius) + "&lon=" + str(
        dict["lon"]) + "&lat=" + str(dict["lat"]) + "&apikey=" + apikey
    response = requests.get(request)
    return response.json()


# result = getPoisCityRadius("Kraków", 20000)
# print(result[0]["kinds"])