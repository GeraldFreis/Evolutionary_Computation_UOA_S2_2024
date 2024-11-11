"""
Define a series of individuals into a population group
"""

from Individual import *
from Mutation import *
from Crossover import *
from Selection import *


class Population():
    """ A group of individuals to be used.

    Attributes:
        matrix - Individuals matrix
        num_paths - Population size
        population - Initial population
        best_individual - Stores best individual
        mutation - Mutation selection
        crossover - Crossover selection
        selection - What selection type 
        selection_params - Selection paramaters

    Methods:
        find_best_individual(self) - Return individual with lowest total cost.
        evolve(self) - Execute 1 iteration of the genetic algorithm.
        get_mating_pool(self) - Generate mating pool based on selection method
        do_crossover(self, mating_pool) - Crossover on mating pool to generate offspring
        do_mutation(self, offspring) - Apply mutation to the offspring with mutation rate
        average_fitness(self) - Calculate average fitness of population
        select_survivor(self, offspring) - Select from current population and offspring for new population
        get_population_statistics(self) - Return Stats of population"""

    def __init__(
            self,
            matrix,
            num_paths,
            matepool_selection,
            crossover,
            mutation,
            survivor_selection,
            num_child=None,
            mutation_rate=0.9,
            selection_params={}):
        # Initialize the Population with a matrix, number of paths (population size),
        # crossover function, selection method, and any selection parameters.
        self.matrix = matrix
        self.num_paths = num_paths
        # Create the initial population by generating Individuals.
        self.population = [Individual(matrix) for i in range(num_paths)]
        # Identify the best individual in the initial population.
        self.best_individual = self.find_best_individual()
        self.mutation = mutation
        self.crossover = crossover
        self.matepool_selection = matepool_selection
        self.survivor_selection = survivor_selection
        self.selection_params = selection_params
        self.mutation_rate = mutation_rate
        if num_child is None:
            self.num_child = num_paths
        else:
            self.num_child = num_child

    def find_best_individual(self):
        # Find and return the individual with the lowest total cost in the population.
        best = self.population[0]
        for ind in self.population:
            if ind.total_cost < best.total_cost:
                best = ind
        return best

    def evolve(self):
        # Execute one iteration of the genetic algorithm: selection, crossover, mutation, and survivor selection.
        mating_pool = self.get_mating_pool()
        offspring = self.do_crossover(mating_pool)
        self.do_mutation(offspring)
        self.select_survivor(offspring)

    def get_mating_pool(self):
        # Generate a mating pool based on the selection method.
        match self.matepool_selection:
            case "fitness_proportional":
                return Selection.fitness_proportional_selection(self.population, self.num_child)
            case "tournament":
                tournament_size = self.selection_params.get(
                    "tournament_size", self.num_paths // 4)
                return Selection.tournament_selection(self.population, tournament_size, self.num_paths)
            case "elitism":
                num_elites = self.selection_params.get("num_elites", 5)
                return Selection.elitism_selection(self.population, num_elites)
            case _:
                # Raise an error if the selection method is not recognized.
                raise ValueError("Unknown selection method")

    def do_crossover(self, mating_pool):
        # Perform crossover on the mating pool to generate offspring.
        new_population = []
        shuffle(mating_pool)
        for i in range(0, len(mating_pool), 2):
            parent1 = mating_pool[i]
            # Pair each individual with the next.
            parent2 = mating_pool[i + 1] if i + \
                1 < len(mating_pool) else mating_pool[0]

            # Apply the crossover function to produce two children paths.
            children = self.crossover(
                parent1.path, parent2.path)

            for child_path in children:
                child = Individual(self.matrix)
                child.path = child_path
                child.total_cost = child.find_total_cost()

                # Add the children to the new population.
                new_population.append(child)

        return new_population

    def do_mutation(self, offspring):
        for individual in offspring:
            # Randomly decide whether to mutate each individual.
            sample = np.random.random(1)
            if sample >= self.mutation_rate:
                continue

            # Apply one of four mutation operators.
            individual.path = self.mutation(individual.path)

            # Recalculate the total cost of the mutated individual.
            individual.total_cost = individual.find_total_cost()
            individual.fitness = individual.calculate_fitness()

        return offspring

    def average_fitness(self):
        # Calculate the average fitness of the population.
        total_fitness = sum(ind.fitness for ind in self.population)
        return total_fitness / self.num_paths

    def select_survivor(self, offspring):
        # Select survivors from the current population and offspring to form the new population.
        combined_population = self.population + offspring

        # Use elitism selection to keep the best individuals, so some elites are preserved.
        match self.survivor_selection:
            case "fitness_proportional":
                self.population = Selection.fitness_proportional_selection(combined_population, self.num_paths)
            case "tournament":
                tournament_size = self.selection_params.get(
                    "tournament_size", self.num_paths // 5 * 4)
                self.population = Selection.tournament_selection(combined_population, tournament_size, self.num_paths)
            case "elitism":
                self.population = Selection.elitism_selection(combined_population, self.num_paths)
            case _:
                # Raise an error if the selection method is not recognized.
                raise ValueError("Unknown selection method")

        # Update the best individual after the selection process.
        self.best_individual = self.find_best_individual()

    def get_population_statistics(self):
        return [self.population[i].total_cost for i in range(self.num_paths)]
