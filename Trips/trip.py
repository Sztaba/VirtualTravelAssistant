import pandas as pd
import networkx as nx
import osmnx as ox
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
from Processor.algorithms import all_algorithms, create_weighted_lsa, sortFinalPoi
from Processor.assistant import (
    getPoisForWeightedLsaAllTopics,
    getListOfPoisShort,
    getPoisForTfidfAndLsa,
)
from Downloader.poiDownloader import getPoisCityRadius
from .graphing import stage_one, stage_two, stage_three, stage_four
from typing import List, Any


class Trip(ABC):
    @abstractmethod
    def __init__(
        self, name: str, email: str, city: str, documents_path: str, api_key: str
    ) -> None:
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
    def city_points_of_interest(self) -> Any:
        pass

    @abstractmethod
    def get_final_topics(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_points_of_interest(self) -> List[str]:
        pass


class HumanTraveller(Trip):
    def __init__(
        self, name: str, email: str, city: str, documents_path: list[str], api_key
    ) -> None:
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
        self._preload_graph()
        self._load_nodes()

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
        self._city_points_of_interest = getPoisCityRadius(
            self._city, 20000, self.api_key
        )

    def _analyse_documents(self) -> None:
        self._result = all_algorithms(self._documents, display=False, save_csv=False)
        self._weighted_lsa = create_weighted_lsa(
            self._result["LSA"], self._result["TF-IDF"]
        )

    def _select_pois(self) -> None:
        pois_with_info = getPoisForTfidfAndLsa(
            self._city_points_of_interest, self._result["TF-IDF"], self._weighted_lsa
        )
        self._selected_pois = sorted(pois_with_info, key=sortFinalPoi, reverse=True)[
            :10
        ]

    def get_final_topics(self) -> pd.DataFrame:
        return self._weighted_lsa

    def get_points_of_interest(self) -> List[str]:
        pois_short = getListOfPoisShort(self._selected_pois)
        return set([poi["name"] for poi in pois_short])

    def _preload_graph(self) -> None:
        self.Graph = ox.graph_from_place(self._city, network_type="drive")
        self.Graph = ox.add_edge_speeds(self.Graph)
        self.Graph = ox.add_edge_travel_times(self.Graph)
        self._preload_map()

    def _preload_map(self) -> None:
        self.gdf_nodes, self.gdf_edges = ox.graph_to_gdfs(self.Graph)

    def _load_nodes(self):
        pois = getListOfPoisShort(self._selected_pois)
        nodes = []
        for poi in pois:
            # x - longitude, y - latitude
            x = poi["point"]["lon"]
            y = poi["point"]["lat"]
            node = ox.nearest_nodes(self.Graph, x, y)
            nodes.append(node)
        # plot nodes
        self.nodes = nodes
        x = pois[0]["point"]["lon"]
        y = pois[0]["point"]["lat"]
        return x, y


    def simple_graph(self):
        x,y = self._load_nodes()
        nc = ["r" if node in self.nodes else "w" for node in self.Graph.nodes()]
        ns = [12 if node in self.nodes else 0 for node in self.Graph.nodes()]
        bbox = ox.utils_geo.bbox_from_point((y, x), dist=2000)
        fig, ax = ox.plot_graph(
            self.Graph, node_color=nc, node_size=ns, node_zorder=2, bbox=bbox
        )

    def simple_map(self):
        return self.gdf_nodes.loc[self.nodes]

    def trip_planner(self):
        pois = getListOfPoisShort(self._selected_pois)
        T, pos = stage_one(pois)
        # eulerian_path = stage_two(T, pos)
        # shortest_path = stage_three(eulerian_path, pos)
        # optimized_path = stage_four(eulerian_path, pos)
        # return optimized_path
