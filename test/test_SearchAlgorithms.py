import sys, os

import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.data.networks import Graph
import numpy as np
from lib.algorythms.DijkstraAlgorithm import DijkstraAlgorithm
from lib.algorythms.AStarAlgorithm import AStarAlgorithm
from lib.algorythms.DummyAlgorithm import DummyAlgorithm

# needs conda install pytest-timeout
@pytest.mark.timeout(5)
def test_DijkstraAlgorithm():
    g = Graph(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
    g.update_edge("A", "B", 1)
    g.update_edge("A", "C", 2)
    g.update_edge("B", "D", 3)
    g.update_edge("B", "E", 4)
    g.update_edge("C", "F", 5)
    g.update_edge("C", "G", 6)
    g.update_edge("D", "H", 7)
    g.update_edge("D", "I", 8)
    g.update_edge("E", "J", 9)
    g.update_edge("E", "K", 10)
    g.update_edge("F", "L", 11)
    g.update_edge("G", "L", 12)
    g.update_edge("H", "L", 13)
    g.update_edge("I", "L", 14)
    g.update_edge("J", "L", 15)
    g.update_edge("K", "L", 16)

    algo1 = DijkstraAlgorithm("Dijkstra")

    path, visited = algo1.search(g, "A", "L")

    solution_path = ['A', 'C', 'F', 'L']

    assert path == solution_path

    # test if graph is only inf, 1 and 0
    if len(visited)== 0:
        assert False

@pytest.mark.timeout(5)
def test_AStarAlgorithm():

    with pytest.raises(ValueError): 
        g = Graph(["A", "B", "C"])
        g.update_edge("A", "B", 1)
        g.update_edge("A", "C", 2)
        g.update_edge("B", "C", 1)

        algo = AStarAlgorithm("A*")
        algo.search(g,'A', 'C')



    g = Graph(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], {"A": (1, 1), "B": (2, 2), "C": (3, 3), "D": (4, 4), "E": (5, 5), "F": (6, 6), "G": (7, 7), "H": (8, 8), "I": (9, 9), "J": (10, 10), "K": (11, 11), "L": (12, 12)})

    g.update_edge("A", "B", 1)
    g.update_edge("A", "C", 2)
    g.update_edge("B", "D", 3)
    g.update_edge("B", "E", 4)
    g.update_edge("C", "F", 5)
    g.update_edge("C", "G", 6)
    g.update_edge("D", "H", 7)
    g.update_edge("D", "I", 8)
    g.update_edge("E", "J", 9)
    g.update_edge("E", "K", 10)
    g.update_edge("F", "L", 11)
    g.update_edge("G", "L", 12)
    g.update_edge("H", "L", 13)
    g.update_edge("I", "L", 14)
    g.update_edge("J", "L", 15)
    g.update_edge("K", "L", 16)

    path, visited = algo.search(g, "A", "L")

    solution_path = ['A', 'C', 'F', 'L']

    assert path == solution_path
    
    # test if graph is only inf, 1 and 0
    if len(visited)== 0:
        assert False


def test_DummyAlgorithm():
    g = Graph(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"])
    g.update_edge("A", "B", 1)
    g.update_edge("A", "C", 2)
    g.update_edge("B", "D", 3)
    g.update_edge("B", "E", 4)
    g.update_edge("C", "F", 5)
    g.update_edge("C", "G", 6)
    g.update_edge("D", "H", 7)
    g.update_edge("D", "I", 8)
    g.update_edge("E", "J", 9)
    g.update_edge("E", "K", 10)
    g.update_edge("F", "L", 11)
    g.update_edge("G", "L", 12)
    g.update_edge("H", "L", 13)
    g.update_edge("I", "L", 14)
    g.update_edge("J", "L", 15)
    g.update_edge("K", "L", 16)

    algo = DummyAlgorithm()

    path, visited = algo.search(g, "A", "L")

    assert isinstance(path, list)
    
    # test if graph is only inf, 1 and 0
    if len(visited) == 0:
        assert False
