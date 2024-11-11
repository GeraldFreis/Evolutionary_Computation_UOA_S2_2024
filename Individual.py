"""
The Individual class contains a single permutation (and
possible solution) of given cities
"""

import numpy as np


class Individual():
    """ An individual in a population, using a random permutation for the path.

    Attributes:
        matrix      Number of nodes in the path (based on the matrix size).
        num_nodes   Generate a random permutation of the nodes to create the path.
        path        The path taken
        total_cost  Total cost of the entire path taken
        fitness     Fitness based on total_cost

    Methods:
        find_total_cost(self)  Calculates the total cost of a generate permutation
        perm(self)             Generates a new permutation """

    def __init__(self, matrix):
        self.matrix = matrix
        self.num_nodes = matrix.shape[0]
        self.path = np.random.permutation(self.num_nodes)
        # TODO:Shouldnt this be on one line? Or does python not do that? - Mitchell
        self.total_cost = 0
        self.total_cost = self.find_total_cost()
        self.fitness = self.calculate_fitness()

    def find_total_cost(self):
        # Calculates the total cost of a generated permutation.
        total_cost = 0
        for i in range(self.num_nodes - 1):
            # Calculate the cost of traveling from one node to the next.
            total_cost += self.matrix[self.path[i]][self.path[i + 1]]
        # Add the cost of returning to the starting node.
        total_cost += self.matrix[self.path[-1]][self.path[0]]
        return total_cost

    def calculate_fitness(self):
        # Calculate fitness as the inverse of total cost.
        # Higher fitness corresponds to lower total cost.
        return 3e7 - self.total_cost
    
    def print_random_tour(self):
        print([i for i in self.path])
