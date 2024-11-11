API Documentation

PSO Class

Parameters 
- fitness_function: The function to be optimized. Should take a single argument (the position) and return a scalar fitness value.
- dimensions (int): The number of dimensions for the optimization problem.
- bounds (tuple): A tuple of (lower_bound, upper_bound) specifying the bounds of the search space.
- num_particles (int, optional): Number of particles in the swarm. Default is 50.
- w (float, optional): Inertia weight, used to control the exploration and exploitation balance. Default is 0.729.
- c1 (float, optional): Cognitive coefficient, influences how much each particle is pulled towards its personal best. Default is 2.05.
- c2 (float, optional): Social coefficient, influences how much each particle is pulled towards the global best. Default is 2.05.
- max_iter (int, optional): Maximum number of iterations for the optimization process. Default is 1000.
- topology_type (str, optional): Type of swarm topology, can be "fully_connected", "ring", "star", or "random". Default is "fully_connected".

Methods
optimize()
    Optimize the fitness function using Particle Swarm Optimization.
    Returns the best position found by the swarm and the fitness value at that position.

    Returns:
        - best_position (ndarray): The best position found by the swarm during the optimization process
        - best_score (float): The fitness value corresponding to the best_position
        