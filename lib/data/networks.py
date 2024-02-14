import numpy as np

class Graph:
    def __init__(self, node_list, coords_list=None):
        ## TODO: Add coordinates to nodes
        self.nodes_dict = {}
        if coords_list is not None:
            if isinstance(coords_list, dict):
                coords = coords_list
            elif isinstance(coords_list, list):
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
        

    def get_nodes(self):
        '''
        Returns a list of all nodes in the graph.
        '''
        return list(self.nodes_dict.keys())
    
    def get_coords(self, node):
        '''
        Returns the coordinates of a node.
        '''
        return self.coords[node]