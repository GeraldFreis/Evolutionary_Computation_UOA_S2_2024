"""Provides the filereader function """

import numpy as np
from math import sqrt
import time
import datetime
from tqdm import tqdm

def euclidean_distance(x_1:int,
                        y_1: int,
                        x_2: int,
                        y_2: int)->float:
    """
        Euclidean distance from node_1 and node_2
    """
    return round(sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2), 2) 


def filereader(file: str)->np.array:
    """
        Read from file into a numpy array
    """
    # TODO: Check to see if first few lines are ok with this.
    # TODO: Can we remove last 3 lines? - Mitch
    with open(file, 'r') as raw_file:
        counter = 0
        nodes_and_coords = list()
        for line in raw_file:
            if(line != 'EOF\n'):
                if(counter < 6 ): counter += 1
                else:
                    values = [float(val) for val in line.split(" ") if val != '' and val != '\n']
                    if len(values) > 0:
                        nodes_and_coords.append(values)
    
    # creating an edge cost array: for all possible other nodes a cost is associated with the travel distance (useful for permutation eval.)
    edge_costs = np.zeros((len(nodes_and_coords), len(nodes_and_coords))) # n x n dimensional matrix

    for i, a, b in tqdm(nodes_and_coords, desc=f"Calculating distance matrix {file}"):
        for j, c, d in nodes_and_coords:
            if(i != j ):
                i = int(i)
                j = int(j)
                dist = euclidean_distance(a, b, c, d)
                edge_costs[i-1][j-1] = dist
                edge_costs[j-1][i-1] = dist
                
    return edge_costs
    