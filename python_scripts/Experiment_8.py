from pso_lib import *
from math import *

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

standard_pso_with_non_linear_adjustment()