import folium 
from lib.data.networks import Graph

class MapHelper():
    def __init__(self, graph: Graph):
        self.graph = graph
        self.nodes = graph.get_nodes()
        self.map = folium.Map(location=[48.2082, 16.3738], zoom_start=12)
        self.elements = [] # tupples (id, type, coords(start, end), color, size)
        
    def _add_line(self, start, end, color="black", size=2, tag = None):
        element = (tag, "line", (start, end), color, size)
        self.elements.append(element)

    def _add_marker(self, coords, color="blue", size=2, id = None):
        element = (id, "marker", coords, color, size)
        self.elements.append(element)

    def _reset_map(self):
        self.map = folium.Map(location=[48.2082, 16.3738], zoom_start=12)
        self.elements = []

    def _create_map(self):
        for e in self.elements:
            if e[1] == "line":
                folium.PolyLine([e[2][0], e[2][1]], popup=e[0], color=e[3], weight=e[4]).add_to(self.map)
            elif e[1] == "marker":
                folium.Circle(e[2], radius=20*e[4], popup=e[0], color=e[3], fill=True, fill_color=e[3]).add_to(self.map)
                #folium.Marker(e[2], icon=folium.Icon(color=e[3], icon_color='white', icon='train', angle=0, prefix='fa'), popup=e[0]).add_to(self.map)
        # save map
        self.map.save("app/static/map.html")

    def draw_map(self, start, end, shortest_route, visited):
        self._reset_map()
        lines_drawn = []
        for node in self.nodes:
            if type(node) != str:
                raise ValueError("Node must be a string")
            neighbours = self.graph.get_neighbors(node)
            for n in neighbours:
                if n not in lines_drawn:
                    popup = str(self.graph.get_cost([node, n])) + " min, " + str(round(self.graph.get_distance([node, n]), 2)) + " km"
                    if node in shortest_route and n in shortest_route:
                        self._add_line(self.graph.get_coords(node), self.graph.get_coords(n), "blue", 4, popup)
                    else:
                        self._add_line(self.graph.get_coords(node), self.graph.get_coords(n), "gray", 2, popup)
            lines_drawn.append(node)
            

            if node == start or node == end:
                tag=None
                if node == start:
                    tag = "Start: "+ node
                else:
                    tag = "End: "+ node
                self._add_marker(self.graph.get_coords(node), "red", 10, tag)
            elif node in shortest_route:
                self._add_marker(self.graph.get_coords(node), "green", 6, node)
            elif node in visited:
                self._add_marker(self.graph.get_coords(node), "blue", 3, node)
            else:
                self._add_marker(self.graph.get_coords(node), "gray", 3, node)
        self._create_map()

