import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.data.networks import Graph

class ISearchAlgorithm():
    '''
    Universal interface for search algorithms. Different parameter settings deserve a multitude of implementations.
    '''

    def __init__(self, name: str):
        '''
        Initializes the algorithm with a name.
        '''
        self.name = name

    def search(self, graph: Graph, start: str, end: str) -> (list, Graph):
        '''
        Searches for the shortest path between two nodes in a graph.
        Returns the shortest path and a Graph, where all visited edges are 1 and the shortest path is 0.
        The rest of the edges are np.inf.
        '''
        pass

    def __str__(self) -> str:
        '''
        Returns the name of the algorithm and the parameters/settings (opt. the current state).
        '''
        pass