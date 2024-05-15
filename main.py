from Downloader import poiDownloader
from Processor import assistant
from Processor import algorithms

# city = "Kraków"
# file = open("api_key.txt", "r")
# apiKey = file.read()
# file.close()

# pois = poiDownloader.getPoisCityRadius(city, 20000, apiKey)
# print(pois)

# words = "museum church"
# print(assistant.getPoisForGivenWords(pois, words))

doc_contents = []
file_names = ["doc1.txt", "doc2.txt", "doc3.txt"]

for file_name in file_names:
    with open("Data/" + file_name, "r") as file:
        doc_contents.append(file.read())

result = algorithms.all_algorithms(doc_list=doc_contents, display=True)
