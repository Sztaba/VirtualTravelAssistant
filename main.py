import tkinter as tk
from View import View


file = open("api_key.txt", "r")
apiKey = file.read()
file.close()
root = tk.Tk()
ui = View.UserInterface(root, apiKey)
root.mainloop()


# import json
# from Downloader import poiDownloader
# from Processor import assistant
# from Processor import algorithms
# from Trips import trip

# city = "Paris"
# file = open("api_key.txt", "r")
# apiKey = file.read()
# file.close()
# pois = poiDownloader.getPoisCityRadius(city, 20000, apiKey)
#
# with open("Data/UserPreferences/info.txt", "r") as file:
#     users = [line.strip() for line in file.readlines()]
#
# for i, u in enumerate(users):
#     doc_contents = []
#     prefix = str(i + 1) + '_' + u + '_'
#     file_names = ["Data/UserPreferences/" + prefix + j for j in ["doc1.txt", "doc2.txt", "doc3.txt"]]
#     human = trip.HumanTraveller(u, "marek.kowalski@gmail.com", city, file_names, apiKey)
#     human.trip_planner()
    # human.simple_graph()

    # for file_name in file_names:
    #     with open(file_name, "r") as file:
    #         doc_contents.append(file.read())
    # result = algorithms.all_algorithms(doc_list=doc_contents, display=True, save_csv=False)
    # weighted_lsa = algorithms.create_weighted_lsa(result['LSA'], result['TF-IDF'])
    # print(weighted_lsa, '\n')
    # pois_with_info = assistant.getPoisForTfidfAndLsa(pois, result['TF-IDF'], weighted_lsa)
    # sorted_pois = sorted(pois_with_info, key=algorithms.sortFinalPoi, reverse=True)
    # print('\n')
    # with open("Data/UserPreferences/" + prefix + city + '_' + 'pois.json', 'w') as f:
    #     json.dump(sorted_pois, f)
