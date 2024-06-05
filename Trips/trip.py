import pandas as pd
import networkx as nx
import osmnx as ox
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
from Processor.algorithms import all_algorithms, create_weighted_lsa, sortFinalPoi
from Processor.assistant import getPoisForWeightedLsaAllTopics, getListOfPoisShort, getPoisForTfidfAndLsa
from Downloader.poiDownloader import getPoisCityRadius
from .graphing import stage_one, stage_two, stage_three, stage_four
from typing import List, Any

class Trip(ABC):
    @abstractmethod
    def __init__(self, name: str, email: str, city:str, documents_path:str, api_key:str) -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def email(self) -> str:
        pass

    @property
    @abstractmethod
    def city(self) -> str:
        pass

    @property
    @abstractmethod
    def documents(self) -> List[str]:
        pass

    @property
    @abstractmethod
    def city_points_of_interest(self)-> Any:
        pass

    @abstractmethod
    def get_final_topics(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_points_of_interest(self) -> List[str]:
        pass


class HumanTraveller(Trip):
    def __init__(self, name: str, email: str, city:str, documents_path: list[str], api_key) -> None:
        self._name = name
        self._email = email
        self._city = city
        self._documents = []
        self._documents_path = documents_path
        self.api_key = api_key
        self._load_documents()
        self._analyse_documents()
        self._load_city_points_of_interest()
        self._select_pois()

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email
    @property
    def city(self) -> str:
        return self._city

    @property
    def city_points_of_interest(self) -> Any:
        pass

    @property
    def documents(self) -> List[str]:
        return self._documents

    def _load_documents(self) -> None:
        for file_name in self._documents_path:
            with open(file_name, "r") as file:
                self._documents.append(file.read())

    def _load_city_points_of_interest(self) -> None:
        self._city_points_of_interest = getPoisCityRadius(self._city, 20000, self.api_key)

    def _analyse_documents(self) -> None:
        self._result = all_algorithms(self._documents, display=False, save_csv=False)
        self._weighted_lsa = create_weighted_lsa(self._result['LSA'], self._result['TF-IDF'])

    def _select_pois(self) -> None:
        pois_with_info = getPoisForTfidfAndLsa(self._city_points_of_interest, self._result['TF-IDF'], self._weighted_lsa)
        self._selected_pois = sorted(pois_with_info, key=sortFinalPoi, reverse=True)[:10]
    def get_final_topics(self) -> pd.DataFrame:
        return self._weighted_lsa

    def get_points_of_interest(self) -> List[str]:
        pois_short = getListOfPoisShort(self._selected_pois)
        return set([poi['name'] for poi in pois_short])
    
    def simple_graph(self):
        Graph = ox.graph_from_place(self._city, network_type="walk")
        # add travel_time
        Graph = ox.add_edge_speeds(Graph)
        Graph = ox.add_edge_travel_times(Graph)
        pois = getListOfPoisShort(self._selected_pois)

        for poi in pois:
            poi_location = (poi['point']['lat'], poi['point']['lon'])
            nearest_node = ox.get_nearest_node(Graph, poi_location)
            Graph.add_node(nearest_node, pos=poi_location)
            Graph.add_edge(nearest_node, poi_location)

        fig, ax = ox.plot_graph(Graph, node_color='r', node_size=30, node_zorder=3, edge_linewidth=0.5, edge_color='b', close=False)
        plt.show()

    def trip_planner(self):
        pois = getListOfPoisShort(self._selected_pois)
        T, pos = stage_one(pois)
        # eulerian_path = stage_two(T, pos)
        # shortest_path = stage_three(eulerian_path, pos)
        # optimized_path = stage_four(eulerian_path, pos)
        # return optimized_path
