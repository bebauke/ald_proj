from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm
import numpy as np

class DijkstraAlgorithm(ISearchAlgorithm):
    def __init__(self, name="Dijkstra"):
        super().__init__(name)

    def search(self, graph, start, end):
        # Pfadlängen
        l = {node: float('inf') for node in graph.get_nodes()}
        l[start] = 1
        
        # Vorgänger
        p = {}
        
        # Kürzester Pfad
        R = [start]  # Startknoten hinzufügen
        
        while R and R[-1] != end:
            w = min((node for node in graph.get_nodes() if node not in R), key=lambda x: l[x])
            R.append(w)
            
            for node, weight in graph.get_neighbors(w).items():
                if l[w] + weight < l[node]:
                    l[node] = l[w] + weight
                    p[node] = w

        # Pfad von start bis end rekonstruieren
        if end in p:
            path = [end]
            while path[-1] != start:
                path.append(p[path[-1]])
            path.reverse()
        else:
            path = []
        
        return path, list(l.keys())
