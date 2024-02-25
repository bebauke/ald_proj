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

    def search(self, graph, start, end):
        # Pfadlängen
        l = {node: float('inf') for node in graph.get_nodes()}  # Initialisiere alle Pfadlängen als unendlich
        l[start] = 0  # Die Länge des Startknotens zum Startknoten ist 0, da es sich um den Startknoten handelt
        
        # Vorgänger
        p = {}  # Hier werden die Vorgänger der Knoten auf dem kürzesten Pfad gespeichert
        
        # Kürzester Pfad
        R = [start]  # Startknoten hinzufügen
        w= start
        
        # Der Algorithmus läuft, solange es noch Knoten zu durchsuchen gibt und das Ziel noch nicht erreicht ist
        while R and R[-1] != end:
            
            # Aktualisiere die Pfadlängen der Nachbarn von w
            for node, weight in graph.get_neighbors(w).items():
                if l[w] + weight < l[node]:
                    l[node] = l[w] + weight  # Aktualisiere die Pfadlänge
                    p[node] = w  # Setze w als Vorgänger von node
            
            # Wähle den Knoten mit der minimalen Pfadlänge, der noch nicht in R enthalten ist
            w = min((node for node in graph.get_nodes() if node not in R), key=lambda x: l[x]+self._heuristic(graph,x,end))
            R.append(w)  # Füge den ausgewählten Knoten zu R hinzu
            
                    
        # Pfad von start bis end rekonstruieren
        if end in p:  # Überprüfe, ob ein Pfad von start zu end existiert
            path = [end]  # Der Pfad beginnt mit dem Endknoten
            while path[-1] != start:
                path.append(p[path[-1]])  # Füge den Vorgänger des aktuellen Knotens zum Pfad hinzu
            path.reverse()  # Da der Pfad rückwärts aufgebaut wurde, kehre ihn um, um den korrekten Pfad zu erhalten
        else:
            path = []  # Wenn kein Pfad gefunden wurde, ist der Pfad leer
            raise Exception("kein end")
        
        return path, list(l.keys())  # Gebe den gefundenen Pfad und eine Liste aller Knoten im Graphen zurück
