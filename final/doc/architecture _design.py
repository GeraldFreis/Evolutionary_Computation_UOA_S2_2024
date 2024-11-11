This architecture contains four main classes: PSO, SwarmWithTopology, Particle, Topology.

PSO class:
This class controls the overall optimization process.
It takes a fitness function, search space dimensions, bounds, and various hyperparameters and topology type.
The method handles the particle updates over a set number of iterations.

SwarmWithTopology class:
It manages the swarm of particles and their interactions based on the chosen topology.
This class initializes particle positions and velocities and sets the topology for particle interactions using the class.

Particle class:
Each particle has attributes for position, velocity, and personal best values.
Position and velocity are updated based on the PSO formula, based on both personal and local best positions.

Topology class:
This class defines the structure of the swarm’s neighbourhood.
It supports different topologies including fully connected, ring, star, and random, allowing flexibility in how particles communicate and influence each other during optimization.