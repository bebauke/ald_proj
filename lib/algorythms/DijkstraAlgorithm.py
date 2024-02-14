from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm

class DijkstraAlgorithm(ISearchAlgorithm):
    def __init__(self, name):
        super().__init__(name)

    def search(self, graph, start, end):
        pass