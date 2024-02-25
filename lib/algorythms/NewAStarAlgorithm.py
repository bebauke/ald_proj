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
        if start not in graph.get_nodes() or end not in graph.get_nodes():
            raise ValueError("Start oder Endknoten nicht im Graphen")
        if start == end:
            return [start], [start]

        open_set = PriorityQueue()
        open_set.put(start, 0)
        
        came_from = {}
        
        g_score = {node: float('inf') for node in graph.get_nodes()}
        g_score[start] = 0
        
        f_score = {node: float('inf') for node in graph.get_nodes()}
        f_score[start] = self._heuristic(graph, start, end)

        closed_set = set()
        
        while not open_set.is_empty():
            current = open_set.get()
            
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
                tentative_g_score = g_score[current] + weight
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(graph, neighbor, end)
                    if neighbor not in [item[1] for item in open_set.elements]:
                        open_set.put(neighbor, f_score[neighbor])
        
        return [], []  # Kein Pfad gefunden

