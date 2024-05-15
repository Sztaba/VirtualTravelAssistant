import json
from Downloader import poiDownloader
from Processor import assistant
from Processor import algorithms

city = "Kraków"
file = open("api_key.txt", "r")
apiKey = file.read()
file.close()

pois = poiDownloader.getPoisCityRadius(city, 20000, apiKey)

doc_contents = []
file_names = ["doc1.txt", "doc2.txt", "doc3.txt"]
for file_name in file_names:
    with open("Data/" + file_name, "r") as file:
        doc_contents.append(file.read())

result = algorithms.all_algorithms(doc_list=doc_contents, display=False, save_csv=False)
weighted_lsa = algorithms.create_weighted_lsa(result['LSA'], result['TF-IDF'])
print(weighted_lsa, '\n')

weighted_lsa_pois_per_topic = assistant.getPoisForWeightedLsaPerTopic(pois, weighted_lsa)
print('\n')
with open("Data/poisPerTopic.json", 'w') as f:
    json.dump(weighted_lsa_pois_per_topic, f)

weighted_lsa_pois_all_topics = assistant.getPoisForWeightedLsaAllTopics(pois, weighted_lsa)
with open("Data/poisAllTopics.json", 'w') as f:
    json.dump(weighted_lsa_pois_all_topics, f)

tfidf_pois = assistant.getPoisForTfidf(pois, result['TF-IDF'])
with open("Data/poisTfidf.json", 'w') as f:
    json.dump(tfidf_pois, f)