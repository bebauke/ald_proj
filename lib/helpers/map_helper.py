import folium 
from lib.data.networks import Graph

class MapHelper():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.stations = graph.get_nodes()
        self.coords = graph.get_coords()
