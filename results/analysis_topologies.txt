In the fully connected swarm (gbest) topology, particles quickly converge to the best-known solution, as seen in the sharp fitness drop in early iterations. 
Most tests reach an optimal value by 200 iterations, but this rapid convergence leads to early clustering and reduced exploration. 
While gbest converges fastest, it often gets stuck in local optimum, as shown by the flat lines in the fitness plot.

The ring topology (lbest) limits communication to nearby neighbors, which preserves diversity for longer. In the figure, you can see that fitness improves more steadily over time, with more variation across tests compared to gbest. 
This allows the swarm to explore the solution space more thoroughly. 
While it takes longer to converge, around 1000+ iterations in most cases, lbest avoids the premature convergence seen in gbest, leading to more accurate solutions.

The star topology strikes a balance between the two. 
In the figure, the convergence is faster than lbest but not as fast as gbest. 
This topology still shows some spread among particles, as reflected in the velocity and standard deviation plots, suggesting a good balance of exploration and convergence.

The random neighborhood topology shows a quick fitness drop, similar to gbest, but maintains more diversity, as reflected by larger variations in standard deviation and velocity. 
This prevents premature convergence while still achieving similar fitness values, improving global search capability in the long term.

In conclusion, gbest converges the fastest due to all particles being influenced by the global best, though it risks premature convergence. 
The random neighborhood maintains a wider swarm, allowing for better exploration. 
While gbest is the fastest to run, lbest produces the closest result to the global optimum by balancing exploration and convergence.
