from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm
import numpy as np

class AStarAlgorithm(ISearchAlgorithm):
    def __init__(self, name):
        # magic ???
        super().__init__(name)
    
    def _heuristic(self, graph, node1, node2):
        b = graph.get_coords(node1)
        c = graph.get_coords(node2)
        if None in [b,c]:
            raise ValueError("Keine Kordinaten")
        if None in b or None in c:
            raise ValueError("Kordinaten sind leer")
        return ((b[0] - c[0])**2 + (b[1] - c[1])**2)**0.5

    def search(self, graph, start, end, max_iter = 200):

        # A* initialisieren
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
            u = graph.get_neighbors(start)
            helper={}
            for node, gewicht in u.items():
                exist=False
                for node_l, gewicht_l in l.items():
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

                h[node]=self._heuristic(graph,node, end) 
            
            for key, value in helper.items():
                value += h[key]
            if len(helper)==0:
                raise NotImplementedError("Was isn hier")
            
            w=min(helper, key=helper.get)
            R.append(w)       





