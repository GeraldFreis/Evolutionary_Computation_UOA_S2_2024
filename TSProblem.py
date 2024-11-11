""" Defines the Classes used in solving the TSP problem """
import numpy as np
import pandas as pd
from FileReader import filereader
import networkx as nx
import matplotlib.pyplot as plt

def _nodes_and_coords(file_path)->dict:
        """This function returns each node (city) and its respective coordinates as a tuple in a dict
            Args: file_path: file to read in and get node positions
            Return: a dictionary of node positions: {node: (x,y)}
        """
        position_dictionary = dict()

        with open(file_path, 'r') as raw_file:
            counter = 0
            nodes_and_coords = list()
            for line in raw_file:
                if(line != 'EOF\n'):
                    if(counter < 6 ): counter += 1
                    else:
                        nodes_and_coords = [int(val) for val in line.split(" ") if val != '']
                        position_dictionary[nodes_and_coords[0]] = (nodes_and_coords[1], nodes_and_coords[2])
        return position_dictionary

class TSPProblem():
    """ Class to hold our TSP problem

        Atributes:
            file_path: File to load
            edge_costs: From file to load
            position_dictionary: {node: (x,y)}
             
        Methods:
            random_walk(): Construct and show random walk on the graph"""
    
    def __init__(self, file_path_to_load):
        self.file_path = file_path_to_load
        self.edge_costs = filereader(file_path_to_load)
        self.position_dictionary = _nodes_and_coords(self.file_path)
    

    def random_walk(self):
        """
        Construct and show random walk on the graph 
            Args: None
            Return: None
        """
        
        path = np.random.permutation([i for i in range(1, len(self.position_dictionary)-1)])
        adjacency_matrix = np.zeros((len(self.position_dictionary), len(self.position_dictionary)))
        edge_list = list()
        for i in range(0, len(path)-1):
            adjacency_matrix[path[i]][path[i+1]] = 1
            edge_list.append((path[i], path[i+1]))
        # print(position_dictionary)
        G = nx.Graph(edge_list)
        # print(G.edges())
        # nx.draw(G, pos=self.position_dictionary)
        nx.draw(G)
        plt.show()

    def get_edge_costs(self):
        return self.edge_costs
    
    def get_nodes_and_coords(self)->dict:
        return self.position_dictionary

#TODO: What kind of data does matrix hold?
class Individual():
    """ Class to hold Individula TSP solution

        Attributes:
            matrix       Data matrix
            path         Random permutation of the path taken
            total_cost   Cost of entire path taken
                
        Methods:
            find_total_cost(self)   Calculate total cost current permutation"""
    # Using Random Numbers
    def __init__(self, num_nodes, matrix):
        # returns a random permutation of the nodes
        self.matrix = matrix
        self.path  = np.random.permutation(num_nodes)
        self.total_cost = 0
    
    def find_total_cost(self):
        """
        Evaluates cost of pathway 
            Args:
            Return:
        """
        # Calculates the total cost of a generate permutation
        for node in self.path:
            # check if the node is the first node
            if node == self.path[0]:
                continue
            else:
                self.total_cost += self.matrix[self.path[node-1]][self.path[node]]
            
#TODO: It looks like we can get rid of this

if __name__ == "__main__":
    file = "./tours/st70.tsp"
    problem = TSPProblem(file)
    # drawing a random walk on the graph
    problem.random_walk()