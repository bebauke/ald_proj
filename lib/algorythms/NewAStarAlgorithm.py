from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def is_empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        self.elements.append((priority, item))
        self.elements.sort(reverse=True)  # Sortiere absteigend nach Priorität
    
    def get(self):
        return self.elements.pop()[1]  # Entferne und retourniere das Element mit der höchsten Priorität

class NewAStarAlgorithm(ISearchAlgorithm):
    def __init__(self, name):
        super().__init__(name)
    
    def _heuristic(self, graph, node1, node2):
        b = graph.get_coords(node1)
        c = graph.get_coords(node2)
        return ((b[0] - c[0])**2 + (b[1] - c[1])**2)**0.5

    def search(self, graph, start, end):
       # Überprüfe, ob Start- und Endknoten im Graphen vorhanden sind
        if start not in graph.get_nodes() or end not in graph.get_nodes():
            raise ValueError("Start oder Endknoten nicht im Graphen")
        # Fall, wenn Startknoten gleich Endknoten ist: Rückgabe des Startknotens als Pfad
        if start == end:
            return [start], [start]

        # Initialisiere die Priority Queue für die offenen Knoten
        queue = PriorityQueue()
        queue.put(start, 0)  # Füge den Startknoten mit Priorität 0 hinzu

        # Wörterbuch zum Speichern des Vorgängers eines jeden Knotens auf dem kürzesten Pfad
        prev = {}

        # Initialisiere die l-Werte aller Knoten als unendlich, außer für den Startknoten
        l = {node: float('inf') for node in graph.get_nodes()}
        l[start] = 0 

        # Initialisiere die lh-Werte aller Knoten als unendlich, setze für den Startknoten den Heuristikwert
        lh = {node: float('inf') for node in graph.get_nodes()}
        lh[start] = self._heuristic(graph, start, end)

        # Ein Set zum Speichern aller bereits besuchten Knoten
        visited = set() # R

        # Die Hauptschleife des Algorithmus läuft, bis die Priority Queue leer ist
        while not queue.is_empty():
            # Entferne den Knoten mit der niedrigsten lh aus der Priority Queue
            cur = queue.get()
            
            # Wenn der aktuelle Knoten das Ziel ist, rekonstruiere den Pfad und gib ihn zurück
            if cur == end:
                path = []
                while cur in prev:
                    path.append(cur)
                    cur = prev[cur]
                path.append(start)
                path.reverse()  # Umkehrung des Pfades, da dieser rückwärts aufgebaut wurde
                return path, list(visited)  # Rückgabe des Pfades und der besuchten Knoten
            
            visited.add(cur)  # Markiere den aktuellen Knoten als besucht
            
            # Durchlaufe alle Nachbarn des aktuellen Knotens
            for neighbor, weight in graph.get_neighbors(cur).items():
                l_inter = l[cur] + weight  # Berechne den l-Score des Nachbarn
                if l_inter < l[neighbor]:  # Prüfe, ob ein besserer Weg gefunden wurde
                    # Aktualisiere den besten Weg zum Nachbarn
                    prev[neighbor] = cur
                    l[neighbor] = l_inter
                    lh[neighbor] = l_inter + self._heuristic(graph, neighbor, end)  # Aktualisiere den f-Score des Nachbarn
                    # Füge den Nachbarn zur Priority Queue hinzu, falls er nicht schon enthalten ist
                    if neighbor not in [item[1] for item in queue.elements]:
                        queue.put(neighbor, lh[neighbor])

        return [], []  # Kein Pfad gefunden
