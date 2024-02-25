from lib.data.networks import Graph
from lib.algorythms.DijkstraAlgorithm import DijkstraAlgorithm
from lib.algorythms.AStarAlgorithm import AStarAlgorithm
from lib.algorythms.NewAStarAlgorithm import NewAStarAlgorithm
from lib.algorythms.NewAStarAlgorithm_heap import NewAStarAlgorithmHeap
from lib.data.map_helper import MapHelper
from timeit import default_timer as timer


graph = Graph.from_csv("data/graph.csv")
map = MapHelper(graph)

def calculate_shortest_route_and_stats(start, end, algorithm="dijkstra"):
    '''
    Calculates the shortest route between two nodes in the graph.
    '''
    # Calculate the shortest route and the search statistics
    timer_start = timer()
    if algorithm == "dijkstra":
        shortest_route, visited = DijkstraAlgorithm("Dijkstra").search(graph, start, end)
    elif algorithm == "astar":
        shortest_route, visited = AStarAlgorithm("A*").search(graph, start, end)
    elif algorithm == "nastar":
        shortest_route, visited = NewAStarAlgorithm("A*").search(graph, start, end)
    elif algorithm == "nastar_heap":
        shortest_route, visited = NewAStarAlgorithmHeap("A*").search(graph, start, end)
    timer_end = timer()

    search_stats = {
        "visited_nodes": visited,
        "visited_nodes_count": len(visited),
        "distance" : round(graph.get_distance(shortest_route),2),
        "duration" : graph.get_cost(shortest_route),
        "execution_time": round(timer_end*1000 - timer_start*1000,2),
        "algorithm": algorithm
    }

    map.draw_map(start, end, shortest_route, visited)

    return shortest_route, search_stats

def get_nodes():
    '''
    Returns all nodes in the graph.
    '''
    return list(graph.get_nodes())