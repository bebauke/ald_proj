from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm

class DummyAlgorithm(ISearchAlgorithm):
    def __init__(self, name = "Dummy"):
        super().__init__(name)

    def search(self, graph, start, end):
        nodes = graph.get_nodes()
        # Dummy shortest route
        shortest_route = nodes[::14]
        # Dummy visited nodes
        search_stats = nodes[::7]

        return shortest_route, search_stats