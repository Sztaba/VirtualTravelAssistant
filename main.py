from Downloader import poiDownloader
from Processor import assistant

city = "Kraków"
file = open("api_key.txt", "r")
apiKey = file.read()
file.close()

pois = poiDownloader.getPoisCityRadius(city, 20000, apiKey)
# print(pois)

words = "museum church"
print(assistant.getPoisForGivenWords(pois, words))
