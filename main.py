from Downloader import poiDownloader
from Processor import assistant

city = "Kraków"

pois = poiDownloader.getPoisCityRadius(city, 20000)
# print(pois)

words = "museum church"
print(assistant.getPoisForGivenWords(pois, words))
