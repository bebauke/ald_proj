from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm

class AStarAlgorithm(ISearchAlgorithm):
    def __init__(self, name):
        # magic ???
        super().__init__(name)
    
    def _heuristic(self, graph, node1, node2):
        b = graph.get_coords(node1)
        c = graph.get_coords(node2)
        return ((b[0] - c[0])**2 + (b[1] - c[1])**2)**0.5

    def search(self, graph, start, end):
        pass
