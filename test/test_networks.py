import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.data.networks import Graph

def get_test_graph(coords= False):
    if coords == False:
        coords = None
    else:
        coords = {
            "A": (0, 0),
            "B": (1, 0),
            "C": (2, 0),
            "D": (1, 1),
            "E": (1, -1),
            "F": (2, 1),
            "G": (2, -1),
            "H": (3, 1),
            "I": (3, -1),
            "J": (4, 1),
            "K": (4, -1),
            "L": (5, 0)
        }

    g = Graph(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], coords)
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

    return g

def test_Graph():
    g = get_test_graph()

    assert g.get_edge("A", "B") == 1
    assert g.get_edge("A", "C") == 2
    assert g.get_edge("B", "D") == 3
    assert g.get_edge("B", "E") == 4
    assert g.get_edge("C", "F") == 5
    assert g.get_edge("C", "G") == 6
    assert g.get_edge("D", "H") == 7
    assert g.get_edge("D", "I") == 8
    assert g.get_edge("E", "J") == 9
    assert g.get_edge("E", "K") == 10
    assert g.get_edge("F", "L") == 11
    assert g.get_edge("G", "L") == 12
    assert g.get_edge("H", "L") == 13
    assert g.get_edge("I", "L") == 14
    assert g.get_edge("J", "L") == 15
    assert g.get_edge("K", "L") == 16

    assert g.get_neighbors("A") == {"B": 1, "C": 2}
    assert g.get_neighbors("B") == {"A": 1, "D": 3, "E": 4}
    assert g.get_neighbors("C") == {"A": 2, "F": 5, "G": 6}

    g.reset_edge("A", "B")
    g.reset_edge("A", "C")
    g.reset_edge("B", "D")

    assert g.get_edge("A", "B") == float("inf")
    assert g.get_edge("A", "C") == float("inf")
    assert g.get_edge("B", "D") == float("inf")

    g.update_edge("A", "B", 1)
    g.update_edge("A", "C", 2)
    g.update_edge("B", "D", 3)

    assert g.get_edge("A", "B") == 1
    assert g.get_edge("A", "C") == 2
    assert g.get_edge("B", "D") == 3
    
def test_Graph_csv():
    g = get_test_graph()

    if not os.path.exists("test.csv") and not os.path.exists("test_coords.csv"):
        g.to_csv("test.csv")
        assert os.path.exists("test.csv")
        assert os.path.exists("test_coords.csv")
        os.remove("test.csv")
        os.remove("test_coords.csv")
    else:
        assert False; "File already exists"


def test_Graph_coords():
    g = get_test_graph(False)
    assert g.get_coords("A") == (None, None)

    g = get_test_graph(True)
    assert g.get_coords("A") == (0, 0)
    assert g.get_coords("B") == (1, 0)
    assert g.get_coords("C") == (2, 0)
    assert g.get_coords("D") == (1, 1)
    assert g.get_coords("E") == (1, -1)
    assert g.get_coords("F") == (2, 1)

