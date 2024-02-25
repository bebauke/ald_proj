from lib.algorythms.ISearchAlgorithm import ISearchAlgorithm
import heapq  # Für Priority Queue

class NewAStarAlgorithmHeap(ISearchAlgorithm):
    def __init__(self, name):
        super().__init__(name)
    
    def _heuristic(self, graph, node1, node2):
        # Berechnet die euklidische Distanz als Heuristik
        b = graph.get_coords(node1)
        c = graph.get_coords(node2)
        return ((b[0] - c[0])**2 + (b[1] - c[1])**2)**0.5

    def search(self, graph, start, end):
        if start not in graph.get_nodes() or end not in graph.get_nodes():
            raise ValueError("Start oder Endknoten nicht im Graphen")
        if start == end:
            return [start], [start]

        open_set = []  # Priority Queue
        heapq.heappush(open_set, (0 + self._heuristic(graph, start, end), start))  # (Kosten-Schätzung, Knoten)
        
        came_from = {}  # Speichert den optimalen Vorgänger eines Knotens
        
        g_score = {node: float('inf') for node in graph.get_nodes()}
        g_score[start] = 0
        
        f_score = {node: float('inf') for node in graph.get_nodes()}
        f_score[start] = self._heuristic(graph, start, end)
        
        closed_set = set()
        
        while open_set:
            current = heapq.heappop(open_set)[1]  # Knoten mit der niedrigsten f_score entfernen
            
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path, list(closed_set)
            
            closed_set.add(current)
            
            for neighbor, weight in graph.get_neighbors(current).items():
                if neighbor in closed_set:
                    continue  # Überspringe bereits besuchte Knoten
                
                tentative_g_score = g_score[current] + weight
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(graph, neighbor, end)
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return [], []  # Kein Pfad gefunden