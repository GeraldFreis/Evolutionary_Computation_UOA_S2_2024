import numpy as np
from statistics import stdev
import seaborn as sns
import matplotlib.pyplot as plt

# Inheritance class for AckleyFuction.
class RealValueOptimProblem:
    def __init__(self, dim):
        self.dim = dim
        self.population = []

    def calculate_fitness(self):
        raise NotImplementedError

    def get_neighborhood(self):
        raise NotImplementedError

# Ackley function as described at https://www.sfu.ca/~ssurjano/ackley.html
class AckleyFunction(RealValueOptimProblem):
    def __init__(self, dim, bounds):
        super().__init__(dim)

        self.lower_bounds, self.upper_bounds = bounds

    def bound_representation(self, v):
        return np.clip(v, min=-self.lower_bounds, max=self.upper_bounds)

    def calculate_fitness(self, x):
        n = self.dim
        sum_squared = (x ** 2).sum()
        sum_cosine = (np.cos(2 * np.pi * x)).sum()

        first_exp = np.exp(-0.2 * np.sqrt(1 / n * sum_squared))
        second_exp = np.exp(sum_cosine / n)

        fitness = -20 * first_exp - second_exp + 20 + np.e

        return fitness

class Topology:
    def __init__(self, num_particles):
        self.num_particles = num_particles

    def fully_connected(self):
        # Each particle is connected to every other particle.
        neighbourhoods = {}
        for i in range(self.num_particles):
            neighbours = []

            for j in range(self.num_particles):
                if j != i:
                    neighbours.append(j)
            neighbourhoods[i] = neighbours
        
        return neighbourhoods
    
    def ring_topology(self):
        # Each particle is connected to its two nearest neighbours.
        neighbourhoods = {}
        for i in range(self.num_particles):
            neighbours = [(i - 1) % self.num_particles, (i + 1) % self.num_particles]
            neighbourhoods[i] = neighbours
        
        return neighbourhoods

    def star_topology(self):
        # Central particle 0 is connected to all others.
        neighbourhoods = {}
        neighbourhoods[0] = list(range(1, self.num_particles))

        for i in range(1, self.num_particles):
            neighbourhoods[i] = [0]
        
        return neighbourhoods

    def random_neighbourhood(self, connection_prob):
        # Particles are connected based on chance.
        neighbourhoods = {}
        for i in range(self.num_particles):
            neighbourhoods[i] = []

        for i in range(self.num_particles):
            for j in range(i + 1, self.num_particles):
                if np.random.rand() < connection_prob:
                    neighbourhoods[i].append(j)
                    neighbourhoods[j].append(i)

        return neighbourhoods

class Swarm:
    def __init__(self, num_particles, num_dim, lower_bound, upper_bound):
        self.num_particles = num_particles
        self.num_dim = num_dim
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound 

        # Initial positions + velocities
        self.positions = self.init_positions()
        self.velocities = self.init_velocities()

        # Best positions and scores
        self.personal_best_positions = self.positions.copy()
        self.personal_best_scores = np.full(num_particles, np.inf)

    def init_positions(self):
        # Randomly generated Positions
        return np.random.uniform(self.lower_bound, self.upper_bound, (self.num_particles, self.num_dim))
    
    def init_velocities(self):
        # Randomly generated velocities
        velocity_range = (self.upper_bound - self.lower_bound) * 0.1
        return np.random.uniform(-velocity_range, velocity_range, (self.num_particles, self.num_dim))
    
class SwarmWithTopology(Swarm):
    def __init__(self, num_particles, num_dim, lower_bound, upper_bound, topology_type="fully_connected", connection_prob=0.5):
        super().__init__(num_particles, num_dim, lower_bound, upper_bound)

        self.topology = Topology(num_particles)
        self.connection_prob = connection_prob
        self.neighbourhood = self.set_topology(topology_type)
    
    def set_topology(self, topology_type):
        match topology_type:
            case "fully_connected":
                return self.topology.fully_connected()
            case "ring":
                return self.topology.ring_topology()
            case "star":
                return self.topology.star_topology()
            case "random":
                return self.topology.random_neighbourhood(self.connection_prob)
            case _:
                raise ValueError("Invalid topology type")

# Generates swarm of particals to find local and possible global optimisation
class PSO:
    def __init__(self, fitness_function, dimensions, bounds, num_particles=50, w_min=0.729, w_max=0.729, c1=2.05, c2=2.05, max_iter=1000, topology_type="fully_connected"):

        # Input values
        self.fitness_function = fitness_function
        self.dimensions = dimensions
        self.bounds = bounds
        self.num_particles = num_particles
        self.w_min = w_min
        self.w_max = w_max
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter
        self.topology_type = topology_type
        # Topology
        self.swarm = SwarmWithTopology(num_particles, dimensions, bounds[0], bounds[1], topology_type)
        # Global bests
        self.global_best_position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.global_best_score = float('inf')

        print(f"PSO initialized with {num_particles} particles in {dimensions} dimensions")
        print(f"Search space bounds: {bounds}")
        print(f"Topology: {topology_type}")
        print(f"Max iterations: {max_iter}")
        print(f"Min inertia weight (w): {w_min}")
        print(f"Max inertia weight (w): {w_max}")
        print(f"Cognitive weight (c1): {c1}")
        print(f"Social weight (c2): {c2}")
        print(f"Global Best Position: {self.global_best_position} and Gllbal Best Score: {self.global_best_score}")

    # Finds the best fitness, mean distant to global optimum, standard deviation form center and average velocity
    def optimize(self, adjustment_type: str):

        min_fitness_list = list()
        mean_dist_to_opt_list = list()
        standard_deviation_to_centre_list = list()
        mean_magnitude_of_vector_list = list()

        # Run simulation, aquire fitness, distance to GO and position
        for i in range(self.max_iter):

            print(f"Iteration {i+1}/{self.max_iter}")
            self.cur_iter = i
            fitnesses = list()
            distances_to_global_optimum = list()
            particle_positions = list()

            for j in range(self.num_particles):
                # Fitness
                particle = self.swarm.positions[j]
                fitness = self.fitness_function(particle)
                fitnesses.append(fitness)

                # Distance to GO
                distances_to_global_optimum.append(np.linalg.norm(
                    np.array(particle) - np.array(self.global_best_position)))

                # Position
                particle_positions.append(particle)

                # Update personal best
                if fitness < self.swarm.personal_best_scores[j]:
                    self.swarm.personal_best_scores[j] = fitness
                    self.swarm.personal_best_positions[j] = np.copy(particle)
                    
                # Update global best
                if fitness < self.global_best_score:
                    self.global_best_score = fitness
                    self.global_best_position = np.copy(particle)

            velocities_list = list()

            # Update particle velocity + positions
            for x in range(self.swarm.num_particles):

                # Local best position in the neighbourhood
                neighbours = self.swarm.neighbourhood[x]
                local_best_position = self.get_local_best(neighbours)

                # Calculate new velocity
                w = self.get_inertia_weight(type=adjustment_type)
                inertia = w * self.swarm.velocities[x]
                cognitive = self.c1 * np.random.rand() * \
                    (self.swarm.personal_best_positions[x] -
                     self.swarm.positions[x]),
                social = self.c2 * np.random.rand() * (local_best_position -
                                                       self.swarm.positions[x])
                self.swarm.velocities[x] = inertia + cognitive + social
                velocities_list.append(self.swarm.velocities[x])
                # Calculate new positio
                self.swarm.positions[x] += self.swarm.velocities[x]
                # Out of bounds check
                self.swarm.positions[x] = np.clip(self.swarm.positions[x], self.bounds[0], self.bounds[1])
                # print(f"Updated position for particle {i}: {self.swarm.positions[i]}")

            # Print progress
            print(f"Iternation {i+1}/{self.max_iter} completed. Current global best score: {self.global_best_score}")

            # Get min_fitness_list
            min_fitness_list.append(min(fitnesses))
            # Get mean_dist_to_opt_list
            mean_dist_to_opt_list.append(sum(distances_to_global_optimum) / len(distances_to_global_optimum))
            # Get standard_deviation_to_centre_list
            average_position = np.mean(particle_positions)
            distances_to_average_particle = np.array([np.linalg.norm(np.array(i) - np.array(average_position)) for i in particle_positions])
            standard_deviation_of_distances = stdev( distances_to_average_particle)
            standard_deviation_to_centre_list.append(standard_deviation_of_distances)
            # Get mean_magnitude_of_vector_listr
            mean_magnitude_of_vector_list.append(np.mean(np.linalg.norm(velocities_list)))

        return min_fitness_list, mean_dist_to_opt_list, standard_deviation_to_centre_list, mean_magnitude_of_vector_list

    def get_local_best(self, neighbours):

        # Find the best position in the neighbourhood
        best_score = float('inf')
        best_position = None
        for neighbour in neighbours:
            if self.swarm.personal_best_scores[neighbour] < best_score:
                best_score = self.swarm.personal_best_scores[neighbour]
                best_position = self.swarm.personal_best_positions[neighbour]

        # Return local best or global best position
        return best_position if best_position is not None else self.global_best_position

    def get_inertia_weight(self, type="constant"):
        if type == "constant":
            return self.w_min
        if type == "non-linear":
            modulation_index = 0.9
            w = ((self.max_iter - self.cur_iter) / self.max_iter) ** modulation_index * \
                (self.w_min - self.w_max) + self.w_max
            return w

        raise ValueError(f"{type} inertia weight adjustment is not supported")



def creating_graphs(mean_fitness, difference_to_global_opt, standard_deviation_to_centre, magnitude_of_velocities, filepath_to_save_fig):
    # Graph style
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    plt.rcParams['figure.figsize'] = [10,10]
    fig, axis = plt.subplots(2,2)
    # Titles
    axis[0][0].set_title("Best Fitness vs Iteration")
    axis[0][1].set_title("Average distance to Global optimum vs Iteration")
    axis[1][0].set_title("Standard Deviation of Particles to Centre Mass vs Iteration")
    axis[1][1].set_title("Average Magnitude of Velocity Vector vs Iteration")
    # Y axis lable
    axis[0][0].set_ylabel("Best Fitness")
    axis[0][1].set_ylabel("Average Distance to G.O.")
    axis[1][0].set_ylabel("Standard Deviation to Centre Mass")
    axis[1][1].set_ylabel("Average Magnitude of Velocity Vector")
    # X axis lable
    axis[0][0].set_xlabel("Iteration")
    axis[0][1].set_xlabel("Iteration")
    axis[1][0].set_xlabel("Iteration")
    axis[1][1].set_xlabel("Iteration")
    # Plot mean fitness lines
    axis[0][0].plot(mean_fitness[0], linewidth=1); axis[0][0].plot(mean_fitness[1]); axis[0][0].plot(mean_fitness[2]); axis[0][0].plot(mean_fitness[3]); axis[0][0].plot(mean_fitness[4]); axis[0][0].plot(mean_fitness[5])
    axis[0][0].plot(mean_fitness[6]); axis[0][0].plot(mean_fitness[7]); axis[0][0].plot(mean_fitness[8]); axis[0][0].plot(mean_fitness[9]); 
     # Plot avg distance to G.O.
    axis[0][1].plot(difference_to_global_opt[0], label="Test 1"); axis[0][1].plot(difference_to_global_opt[1], label="Test 2"); axis[0][1].plot(difference_to_global_opt[2], label="Test 3"); axis[0][1].plot(difference_to_global_opt[3], label="Test 4"); axis[0][1].plot(difference_to_global_opt[4], label="Test 5"); axis[0][1].plot(difference_to_global_opt[5], label="Test 6")
    axis[0][1].plot(difference_to_global_opt[6], label="Test 7"); axis[0][1].plot(difference_to_global_opt[7], label="Test 8"); axis[0][1].plot(difference_to_global_opt[8], label="Test 9"); axis[0][1].plot(difference_to_global_opt[9], label="Test 10"); 
    # Plot SD of particals to centre
    axis[1][0].plot(standard_deviation_to_centre[0]); axis[1][0].plot(standard_deviation_to_centre[1]); axis[1][0].plot(standard_deviation_to_centre[2]); axis[1][0].plot(standard_deviation_to_centre[3]); axis[1][0].plot(standard_deviation_to_centre[4]); axis[1][0].plot(standard_deviation_to_centre[5])
    axis[1][0].plot(standard_deviation_to_centre[6]); axis[1][0].plot(standard_deviation_to_centre[7]); axis[1][0].plot(standard_deviation_to_centre[8]); axis[1][0].plot(standard_deviation_to_centre[9]); 
    # Plot avg velocity
    axis[1][1].plot(magnitude_of_velocities[0]); axis[1][1].plot(magnitude_of_velocities[1]); axis[1][1].plot(magnitude_of_velocities[2]); axis[1][1].plot(magnitude_of_velocities[3]); axis[1][1].plot(magnitude_of_velocities[4]); axis[1][1].plot(magnitude_of_velocities[5])
    axis[1][1].plot(magnitude_of_velocities[6]); axis[1][1].plot(magnitude_of_velocities[7]); axis[1][1].plot(magnitude_of_velocities[8]); axis[1][1].plot(magnitude_of_velocities[9]); 
    # Legend
    fig.legend(bbox_to_anchor=(1.0, 0.95))
    fig.tight_layout()
    plt.savefig(filepath_to_save_fig)