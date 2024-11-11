from pso_lib import *
from math import *

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

standard_pso()
standard_pso_with_k_particles(20)
standard_pso_with_k_particles(100)
standard_pso_with_k_particles(200)