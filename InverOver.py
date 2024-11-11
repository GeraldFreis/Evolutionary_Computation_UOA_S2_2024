import random
import numpy as np
from Individual import Individual

class InverOver:
    def __init__(self, population, p=0.02):
        """
        Initialize the InverOver operator.
        
        Args:
        - population: List of individuals (tours) that the operator will work on.
        - p: Probability of performing random inversion.
        """
        self.population = population
        self.p = p

    def apply_operator(self, individual):
        """
        Apply the inver-over operator to an individual.
        
        Args:
        - individual: The individual (tour) to apply the operator to.
        
        Returns:
        - A new individual after the inver-over operator has been applied.
        """
        current_solution = np.array(individual.path)  # Copy of the individual's tour as a NumPy array
        city = random.choice(current_solution)  # Select a random city

        while True:
            if random.random() <= self.p:  # With probability p, select the next city randomly
                next_city = random.choice([c for c in current_solution if c != city])
            else:  # Otherwise, use a "clue" from another individual in the population
                other_individual = random.choice(self.population)
                
                # Find the index of the city in the other_individual's path
                city_indices = np.where(other_individual.path == city)[0]
                if city_indices.size == 0:
                    continue  # Skip this iteration if the city is not found
                city_index = city_indices[0]  # Get the first occurrence of the city
                
                # Get the next city based on the index
                next_city = other_individual.path[(city_index + 1) % len(other_individual.path)]

            # Find positions of the current and next city in the current solution
            city_index = np.where(current_solution == city)[0][0]  # Get index of city
            next_city_index = np.where(current_solution == next_city)[0][0]  # Get index of next_city

            # Perform the inversion
            if city_index != next_city_index:
                if city_index < next_city_index:
                    current_solution[city_index + 1: next_city_index + 1] = np.flip(
                        current_solution[city_index + 1: next_city_index + 1]
                    )
                else:
                    current_solution[next_city_index + 1: city_index + 1] = np.flip(
                        current_solution[next_city_index + 1: city_index + 1]
                    )

            # Stop if the next city is already the neighbor of the current city
            if current_solution[(city_index + 1) % len(current_solution)] == next_city:
                break

            # Move to the next city for further inversions
            city = next_city

        # Return the new solution after applying the inver-over operator
        return current_solution.tolist()  # Convert back to a list if needed

    def evolve_population(self):
        """
        Apply the inver-over operator to each individual in the population.
        """
        new_population = []
        for individual in self.population:
            new_solution = self.apply_operator(individual)
            individual.path = new_solution 
            individual.calculate_fitness()  # Update the fitness of the individual
            new_population.append(individual)
        
        self.population = new_population  # Update population with new individuals