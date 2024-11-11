"""
Define Selection class for sorting a population
"""

import random
import numpy as np

"""class Individual:
    def __init__(self, chromosome, fitness):
        self.chromosome = chromosome
        self.fitness = fitness
"""
class Selection:
    """ Defines Selection defanitions.

    Methods:
        fitness_proportional_selection(population, num_select) - Random selection of factors.
        tournament_selection(population, tournament_size, num_select) - Selected individual winners.
        elitism_selection(population, num_elites) - Sort population by fitness, descending."""
    
    @staticmethod
    def fitness_proportional_selection(population, num_select):
        total_fitness = sum(ind.fitness for ind in population)
        selection_probs = [ind.fitness / total_fitness for ind in population]
        
        selected_individuals = random.choices(
            population, 
            weights=selection_probs, 
            k=num_select
        )
        return selected_individuals
    
    @staticmethod
    def tournament_selection(population, tournament_size, num_select):
        selected_individuals = []
        for _ in range(num_select):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda ind: ind.fitness)
            selected_individuals.append(winner)
        return selected_individuals
    
    @staticmethod
    def elitism_selection(population, num_elites):
        # Sort the population by fitness in descending order.
        sorted_population = sorted(population, key=lambda ind: ind.fitness, reverse=True)
        return sorted_population[:num_elites]
    

"""if __name__ == "__main__":
    population = [Individual(chromosome=[random.randint(0, 10) for _ in range(5)], fitness=random.uniform(0, 1)) for _ in range(20)]
    
    selected_by_fitness = Selection.fitness_proportional_selection(population, 5)
    selected_by_tournament = Selection.tournament_selection(population, tournament_size=3, num_select=5)
    selected_by_elitism = Selection.elitism_selection(population, num_elites=5)
    
    print("Selected by Fitness-Proportional:")
    for ind in selected_by_fitness:
        print(f"Chromosome: {ind.chromosome}, Fitness: {ind.fitness}")

    print("\nSelected by Tournament:")
    for ind in selected_by_tournament:
        print(f"Chromosome: {ind.chromosome}, Fitness: {ind.fitness}")

    print("\nSelected by Elitism:")
    for ind in selected_by_elitism:
        print(f"Chromosome: {ind.chromosome}, Fitness: {ind.fitness}")"""