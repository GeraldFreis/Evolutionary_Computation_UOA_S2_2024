from pso_lib import *
from math import *

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

standard_pso_with_top_tolopology("gbest")
standard_pso_with_top_tolopology("lbest")
standard_pso_with_top_tolopology("star")
standard_pso_with_top_tolopology("random")