from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm
import numpy as np

class DijkstraAlgorithm(ISearchAlgorithm):
    def __init__(self, name = "Dijkstra"):
        super().__init__(name)

    def search(self, graph, start, end):
         # Anzahl der Elemente berechnen
        l = {}   # Pfadlängen
        v = []   # Besuchte Punkte
        p = {}   # Vorgänger
        R = []   # kuerzester Pfad gefunden
        h = {}   # Heuristik
    

        l[start]=0
        w=start
        R.append(start)
        while w != end: 
            u=graph.get_neighbors(start)
            helper={}
            for node, gewicht in u.items():
                exist=False
                for node_l,gewicht_l in l.items():
                    if node==node_l:
                        exist=True
                if exist:
                    if l[node] > l[w]+gewicht:
                        l[node] = l[w]+gewicht
                        helper[node] = l[w]+gewicht
                        p[node]=w
                else:
                    l[node] = l[w]+gewicht
                    helper[node] = l[w]+gewicht
                    p[node]=w
            w=min(helper, key=helper.get)
            R.append(w)
        
        value=end
        while helper_v != start:
            
            helper_v=p[value]
            v.append(helper_v)
            value=helper_v
        