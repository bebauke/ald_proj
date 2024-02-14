from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm

class DijkstraAlgorithm(ISearchAlgorithm):
    def __init__(self, name = "Dijkstra"):
        super().__init__(name)

    def search(self, graph, start, end):
        pass