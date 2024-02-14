
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.data.networks import Graph
import numpy as np
from lib.algorythms.DijkstraAlgorithm import DijkstraAlgorithm
from lib.algorythms.AStarAlgorithm import AStarAlgorithm

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

    path, graph = algo1.search(g, "A", "L")

    solution_path = ["A", "B", "D", "H", "L"]

    assert path == solution_path

    # test if graph is only inf, 1 and 0
    for i in range(len(graph.adjacency_matrix)):
        for j in range(len(graph.adjacency_matrix[i])):
            if graph.adjacency_matrix[i][j] not in [0, 1, np.inf]:
                assert False

def test_AStarAlgorithm():
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

    algo = AStarAlgorithm("A*")

    path, graph = algo.search(g, "A", "L")

    solution_path = ["A", "B", "D", "H", "L"]

    assert path == solution_path
    
    # test if graph is only inf, 1 and 0
    for i in range(len(graph.adjacency_matrix)):
        for j in range(len(graph.adjacency_matrix[i])):
            if graph.adjacency_matrix[i][j] not in [0, 1, np.inf]:
                assert False
