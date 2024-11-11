"""In this file we generaet a set  of experiments:
In these experiments we investigate the effects of different combinations of topology, swarm size and weight adjustment"""

from pso_lib import *
from math import *
from Experiment_6_and_7 import creating_graphs

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
        