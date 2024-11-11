"""
Traveling salesperson problem (TSP) for group assignment 1
of Evolutionary Comutation 2024 S2 at the University of Adelaide. 
Written by group 9 (group-assignment-1-groupniners)...
    Mitchell Pastro (a1716006)
    TODO: EVERYONE PUT YOUR NAME AND NUMBER HERE

Preamble:
    The input for TSP is given by n cities and distances dij between
    cities i and j where 1 <= i and j <= n. Tour starts at one city,
    visits each city once and returns to origin. The goal is to compute
    tour of minimal cost.
"""


from FileReader import *
from Individual import *
from Population import *
from Mutation import *
import time
import datetime

# TODO: Implement a TSPPRoblem class


def main():
    test_file = "./tours/pr2392.tsp"
    node_matrix = filereader(test_file)
    population = Population(
        node_matrix,
        num_paths=100,
        crossover=Crossover.cycle_crossover,
        mutation=Swap,
        matepool_selection="fitness_proportional",
        survivor_selection="elitism",
        # selection_params={"tournament_size": 25},
        mutation_rate=0.9
    )

    total_gen = 20000
    start = time.time()
    remaining_gen = total_gen
    for generation in range(total_gen):
        population.evolve()
        pop_avg = population.average_fitness()
        print("=====================================")
        print(f"Average fitness in generation {generation}: {pop_avg}")
        print(
            f"Best cost in generation {generation}: {population.best_individual.total_cost}")
        # Check how far off the best solution is from the optimal solution.
        # optimal_cost = population.best_individual.total_cost
        # print(f"Optimal cost: {optimal_cost}")
        # print(f"Optimal solution: {optimal_solution}")
        # print(f"Best solution: {population.best_individual.path}")
        end = time.time()
        remaining_gen -= 1
        elapsed = datetime.timedelta(seconds=end-start)
        remaining_seconds = (end-start) * remaining_gen / (total_gen - remaining_gen) if remaining_gen > 0 else 0
        eta = datetime.timedelta(seconds=remaining_seconds)
        print(f"Elapsed: {elapsed} - ETA: {eta}")
        print("=====================================")
        
        


if __name__ == "__main__":
    main()
