For the modulation index we use 0.9, as it is the lowest in the bounds of [0.9, 1.3] as specified in the paper.
This modulation index led to convergence before 800 epochs, which is beneath 81% of the iterations, in line with the paper. 

We find that half of all tests (5) converge with an optimal fitness towards zero, and that all tests except 1 converge to their global optimum before 1000 iterations. 
This indicates that non linear weight adjustment leads to slow convergence.

When compared to a constant weight adjustment (Experiment 6), the only significant difference is that with constant weight adjustment more tests converge to zero.
This highlights that non linear weight adjustment may not be a better choice than constant weight adjustment in this case. 
However, with non linear weight adjustment the swarm tends to be a greater distance from the centre of the swarm, as demonstrated by the consistently higher standard deviation over time; when compared to constant weight adjustment.

Likewise, the average magnitude of velocity vectors for the swarm is higher with non linear weight adjustment than constant weight adjustment. 
This may be beneficial as the swarm can continue to converge and learn over time, rather than plateau when a local optimum is found. 
Such suggests that a nonlinear weight adjustment can be useful for escaping local optima, where constant weight adjustment may be prone to falling into local optima. 

Although the final fitness for non-linear weight adjustment is similar if not slightly worse than constant weight adjustment, the ability for non-linear weight adjustment to continue to evolve may be beneficial in optimising certain functions.
