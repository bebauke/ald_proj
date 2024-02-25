import numpy as np

class Graph:
    '''
    Class for creating and manipulating a graph.

    Attributes:
    - nodes_dict: dictionary of nodes and their indices
    - adjacency_matrix: 2D array of distances between nodes
    - coords: dictionary of nodes and their coordinates
    '''
    def __init__(self, node_list, coords_list=None):
        ## TODO: Add coordinates to nodes
        self.nodes_dict = {}
        if coords_list is not None:
            if isinstance(coords_list, dict):
                if not isinstance(coords_list[node_list[0]], tuple):
                    raise Exception("Invalid coordinates format:" + str(coords_list[node_list[0]]))
                coords = coords_list
            elif isinstance(coords_list, list):
                if not isinstance(coords_list[0], tuple):
                    raise Exception("Invalid coordinates format:" + str(coords_list[0]))
                if len(node_list) != len(coords_list):
                    raise Exception("Number of nodes and coordinates do not match.")
                coords = {node: coords_list[i] for i, node in enumerate(node_list)}
            else:
                raise Exception("Invalid coordinates format.")
        else:
            coords = {node: (None, None) for node in node_list}

        for node in node_list:
            self.nodes_dict[node] = node_list.index(node)

        # 2D array of distances between nodes
        self.adjacency_matrix = np.full((len(node_list), len(node_list)), np.inf)
        self.coords = coords

        # self.adjacency_matrix = {}
        # for node in node_list:
        #     self.adjacency_matrix[node_list.index(node)] = {}
        #     for node2 in node_list:
        #         self.adjacency_matrix[node_list.index(node)][node_list.index(node2)] = np.inf

    def _to_index(self, node):
        ret = None
        if type(node) == list:
            ret = []
            for n in node:
                if type(n) == int:
                    ret.append(n)
                elif n in self.nodes_dict.keys():
                    ret.append(self.nodes_dict[n])
                else:
                    raise Exception("Node not in graph: " + str(n) + ".")       
        elif type(node) == int:
            ret = node
        elif node in self.nodes_dict.keys():
            ret = self.nodes_dict[node]
        else:
            raise Exception("Node not in graph: " + str(node) + ".")
        return ret


    def update_edge(self, node1, node2, weight, weight2=None):
        '''
        Updates the weight of an edge between two nodes if the new weight is smaller than the old one.
        '''
        node1, node2 = self._to_index([node1, node2])

        if weight < self.adjacency_matrix[node1][node2]:
            self.adjacency_matrix[node1][node2] = weight

        if weight2 is not None:
            if weight2 < self.adjacency_matrix[node2][node1]:
                self.adjacency_matrix[node2][node1] = weight2
        else:
            if weight < self.adjacency_matrix[node2][node1]:
                self.adjacency_matrix[node2][node1] = weight

    def reset_edge(self, node1, node2):
        '''
        Resets the weight of an edge between two nodes to infinity.
        '''
        node1, node2 = self._to_index([node1, node2])

        self.adjacency_matrix[node1][node2] = np.inf
        self.adjacency_matrix[node2][node1] = np.inf

    def get_edge(self, node1, node2):
        '''
        Returns the weight of an edge between two nodes.
        '''
        node1, node2 = self._to_index([node1, node2])
        
        return self.adjacency_matrix[node1][node2]
    

    def get_neighbors(self, node):
        '''
        Returns a dictionary of all neighbors of a node and their weights.
        '''
        node = self._to_index(node)
        neighbors = np.where(self.adjacency_matrix[node] != np.inf)[0]
        stat = [list(self.nodes_dict.keys())[i] for i in neighbors]
        weights = self.adjacency_matrix[node][neighbors]
        ret = {}
        for i in range(len(stat)):
            ret[stat[i]] = weights[i]
        return ret
    
    def to_csv(self, path):
        '''
        Writes the adjacency matrix to a csv file.
        '''
        import pandas as pd
        df = pd.DataFrame(self.adjacency_matrix)
        df.to_csv(path, index=False)

        # coords 
        df = pd.DataFrame(self.coords)
        path_csv = path.split(".")[0] + "_coords.csv"
        df.to_csv(path_csv, index=False)

    def from_csv(path, path_coords=None):
        '''
        Reads the adjacency matrix from a csv file.
        '''
        
        try:
            import pandas as pd
            df = pd.read_csv(path)
            adjacency_matrix = df.to_numpy()
        
            # coords 
            if path_coords is None:
                path_coords = path.split(".")[0] + "_coords.csv"
            df = pd.read_csv(path_coords)
            coords = df.to_dict()
            nodes = list(coords.keys())

        except Exception as e:
            raise Exception("Could not read csv file: ", e)
        
        coords_d = {}
        for node in nodes:
            coords_d[node] = (coords[node][0], coords[node][1])

        g = Graph(nodes, coords_d)
        g.adjacency_matrix = adjacency_matrix

        return g
        

    def get_nodes(self):
        '''
        Returns a list of all nodes in the graph.
        '''
        return list(self.nodes_dict.keys())
    
    def get_coords(self, node):
        '''
        Returns the coordinates of a node.
        '''
        if node is None:
            return self.coords
        return self.coords[node]

    def get_cost(self, route):
        '''
        Returns the total cost of a route.
        '''
        cost = 0
        for i in range(len(route)-1):
            _cost = self.adjacency_matrix[self.nodes_dict[route[i]]][self.nodes_dict[route[i+1]]]
            if _cost == np.inf:
                raise Exception("Route not possible.")
                # continue
            cost += _cost
        return cost
    
    def get_distance(self, route):
        '''
        Returns the total distance of a route in km.
        '''
        distance = 0
        for i in range(len(route)-1):
            c1 = self.coords[route[i]]
            c2 = self.coords[route[i+1]]
            distance += np.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)
        return distance
        