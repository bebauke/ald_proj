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

    def search(self, graph: Graph, start: str, end: str) -> tuple[list, list]:
        '''
        Searches for the shortest path between two nodes in a graph.
        Returns the a list of nodes in the shortest path and a list of all visited nodes.
        '''
        pass

    def __str__(self) -> str:
        '''
        Returns the name of the algorithm and the parameters/settings (opt. the current state).
        '''
        return self.name