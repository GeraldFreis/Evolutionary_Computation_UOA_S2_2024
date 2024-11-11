""" 
This file allows all experiments (6, 7, 8, 9, 10) to be run and generate images of results
"""

from pso_lib import *
"""Define functions"""

# for experiment 6
def standard_pso(): ...

# for experiment 7
def standard_pso_with_k_particles(k): ...

# for experiment 8
def standard_pso_with_non_linear_adjustment(): ...

# for experiment 9:
def standard_pso_with_top_tolopology(top): ...

# for experiment 10:
def combination_pso(swarm_size: int, topology: str, weight_adj: str): ...


"""Function implementation"""

# Experiment 6: Standard PSO using Ackley function with 10 dim, range of +/-30, 1000 iterations
def standard_pso():

    dimensions = 10
    bounds = (-30, 30)
    ackley = AckleyFunction(dimensions, bounds)
    m_f =list(); c_m = list(); s_d = list() ;v = list()

    # 10 instances of the PSO with the Ackley fitness function
    for _ in range(0, 10):
        pso = PSO(fitness_function=ackley.calculate_fitness, dimensions=dimensions, bounds=bounds, topology_type="random")
        # optimisation
        mean_fitness, centre_of_mass,  standard_deviations , velocities = pso.optimize(adjustment_type="constant"); 
        m_f.append(mean_fitness); c_m.append(centre_of_mass); s_d.append(standard_deviations); v.append(velocities)
    
    # plotting
    creating_graphs(m_f, c_m, s_d, v, "results/metrics_std_pso.png")

# Experiment 7: Same as experiment 6 with swarm sizes 20, 100 and 200
def standard_pso_with_k_particles(k):

    dimensions = 10
    bounds = (-30, 30)
    ackley = AckleyFunction(dimensions, bounds)
    m_f =list(); c_m = list(); s_d = list() ;v = list()

    # 10 instances of the PSO with the Ackley fitness function
    for _ in range(0, 10):
        pso = PSO(fitness_function=ackley.calculate_fitness, dimensions=dimensions, bounds=bounds, topology_type="random", num_particles=k)
        # optimisation
        mean_fitness, centre_of_mass,  standard_deviations , velocities = pso.optimize(adjustment_type="constant"); 
        m_f.append(mean_fitness); c_m.append(centre_of_mass); s_d.append(standard_deviations); v.append(velocities)
    
    # plotting
    creating_graphs(m_f, c_m, s_d, v, "results/metrics_std_pso_swarm{}.png".format(k))

# Experiment 8: Derive PSO  with non-linear inertia weight
def standard_pso_with_non_linear_adjustment():

    dimensions = 10
    bounds = (-30, 30)
    ackley = AckleyFunction(dimensions, bounds)
    m_f =list(); c_m = list(); s_d = list() ;v = list()

    # 10 instances of the PSO
    for _ in range(0, 10):
        pso = PSO(fitness_function=ackley.calculate_fitness, dimensions=dimensions, bounds=bounds, topology_type="random")
        # optimisation
        mean_fitness, centre_of_mass,  standard_deviations , velocities = pso.optimize(adjustment_type="non-linear"); 
        m_f.append(mean_fitness); c_m.append(centre_of_mass); s_d.append(standard_deviations); v.append(velocities)
    
    # plotting
    creating_graphs(m_f, c_m, s_d, v, "results/metrics_std_pso_weight_adjust.png")

# Experiment 9: Derive PSO with different neighbourhood topologies
def standard_pso_with_top_tolopology(top):

    dimensions = 10
    bounds = (-30, 30)
    ackley = AckleyFunction(dimensions, bounds)
    m_f =list(); c_m = list(); s_d = list() ;v = list()
    # 10 instances of the PSO
    for _ in range(0, 10):
        pso = PSO(fitness_function=ackley.calculate_fitness, dimensions=dimensions, bounds=bounds, topology_type=top)
        # optimisation
        mean_fitness, centre_of_mass,  standard_deviations , velocities = pso.optimize(adjustment_type="constant"); 
        m_f.append(mean_fitness); c_m.append(centre_of_mass); s_d.append(standard_deviations); v.append(velocities)
    
    # plotting
    creating_graphs(m_f, c_m, s_d, v, "results/metrics_std_pso_topo_{}.png".format(top))

# experiment 10: Best combination of swarm size, wight and topology
def combination_pso(swarm_size: int, topology: str, weight_adj: str):
    
    dimensions = 10
    bounds = (-30, 30)
    ackley = AckleyFunction(dimensions, bounds)
    m_f =list(); c_m = list(); s_d = list() ;v = list()
    # 10 instances of the PSO
    for _ in range(0, 10):
        pso = PSO(fitness_function=ackley.calculate_fitness, dimensions=dimensions, bounds=bounds, topology_type=topology, num_particles=swarm_size)
        # optimisation
        mean_fitness, centre_of_mass,  standard_deviations , velocities = pso.optimize(adjustment_type=weight_adj); 
        m_f.append(mean_fitness); c_m.append(centre_of_mass); s_d.append(standard_deviations); v.append(velocities)
    
    # plotting
    creating_graphs(m_f, c_m, s_d, v, "results/metrics_std_pso_swarm{}_topology_{}_weightadjustment_{}.png".format(swarm_size, topology, weight_adj))

"""Running the functions"""
# experiment 6
standard_pso() 

# experiment 7
standard_pso_with_k_particles(20)
standard_pso_with_k_particles(100)
standard_pso_with_k_particles(200)

# experiment 8
standard_pso_with_non_linear_adjustment()

# experiment 9
standard_pso_with_top_tolopology("fully_connected")
standard_pso_with_top_tolopology("ring")
standard_pso_with_top_tolopology("star")
standard_pso_with_top_tolopology("random")

# experiment 10
combination_pso(20, "fully_connected", "constant")
combination_pso(20, "ring", "constant")
combination_pso(20, "star", "constant")

combination_pso(100, "fully_connected", "constant")
combination_pso(100, "ring", "constant")
combination_pso(100, "star", "constant")

combination_pso(200, "fully_connected", "constant")
combination_pso(200, "ring", "constant")
combination_pso(200, "star", "constant")

combination_pso(20, "fully_connected", "non-linear")
combination_pso(20, "ring", "non-linear")
combination_pso(20, "star", "non-linear")

combination_pso(100, "fully_connected", "non-linear")
combination_pso(100, "ring", "non-linear")
combination_pso(100, "star", "non-linear")

combination_pso(200, "fully_connected", "non-linear")
combination_pso(200, "ring", "non-linear")
combination_pso(200, "star", "non-linear")