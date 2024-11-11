We observe that an increased swarm size leads to faster convergence to best fitnesses, as visible in subfigure 1.
With 20 particles, no tests converge to a near zero fitness; yet all converge to respective optimal fitnesses by 250 iterations.
Comparably, 100-particle swarms allow 7 tests to converge to a near zero fitness, before 200 iterations. 
With 200 particle swarms, 8 tests converge to a near zero fitness with the last around 600 iterations. 
This highlights that increasing swarm size accelerates convergence. However, the marginal benefit of increasing from 100 to 200 particles 
suggests a logarithmic relationship between swarm size and optimal fitness.

Subplot 2, depicting the average distance to global optimum demonstrates that larger swarms converge to their global optimum more quickly.
With 20 particles, significant scatter is observed with tests converging only around 500 iterations.
In contrast, 100-particle swarms reduce scatter, and this trend continues with 200 particles.
This indicates that larger swarms maintain proximity to the global optimum, and have a tendency to 
converge to the global optimum at a higher rate.

Subplot 3 of the standard deviation of particles around the centre mass, highlights that an increased swarm size reduces particle scatter.
With 20 particles, the standard deviation remains high, demonstrating volatility. With 100 particles all tests converge
to the mean before 81% of the iterations, while with 200 particles 8 tests converge by 650 iterations.
The aforementioned suggests that 200 particles retains more variability, avoiding premature convergence unlike the 100-particle swarm.

In subplot 4, the trend of subplot 3 is conserved, where a large swarm converges faster, but 100-particles tends to
converge to the optimum and cease learning, unlike 200 particles.

Following this analysis, 200 particles would be chosen, as this offers the most variability and fastest convergence toward the global optimum across multiple tests.
