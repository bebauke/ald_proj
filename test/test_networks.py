import os,sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.data.networks import Graph

def test_Graph():
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

    if not os.path.exists("test.csv"):
        g.to_csv("test.csv")

        assert os.path.exists("test.csv")
        os.remove("test.csv")
    else:
        assert False; "File already exists"


