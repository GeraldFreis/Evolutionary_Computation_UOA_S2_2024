Analysis of the standard particle swarm optimization shows that although there are notable deviations between each test, a generalised trend can be found. 
Each observation follows the same negative exponential curve shape where values start off large before rapidly reaching an asymptote, as is to be expected 
for this kind of optimization. Each observation however contains slightly different shapes and trends that set each apart.

Best fitness has the most extreme exponential curve, reaching the asymptote the fastest, at around 200 iterations for the majority (9 out of 10 in the 
provided diagram) before flatlining at different optimum. 

Average distance to global optimum follows a similar trend as best fitness, but with a tighter spread after 100 iterations and a smaller exponential curve.

Standard deviation to centre mass is by far the most varied of the observations, having the greatest spread, smallest curve and most deviations away 
from the asymptote (possibly as a result of some particles finding stable orbits). However, most tests start to flatline around 450 to 500 iterations.

FInally, the average magnitude of velocity is similar to the previous observation but less extreme. There appears to be decent correlation, starting to 
flatline around 450 iterations with similar spikes away from the asymptote.

Some notable conclusions to draw from these tests are…
    Different swarms converge to different local optimums
    The difference between swarms optimums can vary by a not insignificant amount.
    Despite all the runs following a similar shape and pattern, some runs generate observations that deviate from the asymptote greatly.

In conclusion, while PSO can be used to find local optimums, several swarms should be used to determine the global optimum. Furthermore, most tests can 
be halted after between 200 to 400 iterations.