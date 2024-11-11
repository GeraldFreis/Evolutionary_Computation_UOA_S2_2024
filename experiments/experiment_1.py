import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FileReader import filereader
from Individual import *
from Population import *
from statistics import stdev, mean, median
import pandas as pd
from tqdm import tqdm
import time
from concurrent.futures import ProcessPoolExecutor
from OptTourReader import read_optimal_tour, calculate_tour_length


def run_experiment(file, opt_file, k, run_number, output_folder):
    start_time = time.time()
    node_matrix = filereader(file)

    # Read the optimal tour if provided
    if opt_file:
        optimal_tour = read_optimal_tour(opt_file)
        optimal_tour_length = calculate_tour_length(optimal_tour, node_matrix)
    else:
        optimal_tour_length = None

    print(f"File: {file} | Population Size: {k} | Run: {run_number}")

    population = Population(
        node_matrix,
        num_paths=k,
        crossover=Crossover.order_crossover,
        matepool_selection="tournament",
        survivor_selection="elitism",
        selection_params={"tournament_size": k // 5 * 4},
        mutation=Swap,
        mutation_rate=0.9
    )

    result_data = []

    for generation in tqdm(range(20000), desc=f"File {file} - Population Size {k} - Run {run_number}"):
        population.evolve()

        if generation in [100, 1000, 2000, 4999, 9999, 19999]:
            pop_fitnesses = population.get_population_statistics()
            max_f = max(pop_fitnesses)
            min_f = min(pop_fitnesses)
            mean_fitness = mean(pop_fitnesses)
            stdev_fitness = stdev(pop_fitnesses)
            median_fitness = median(pop_fitnesses)
            avg_fitness = population.average_fitness()

            # Calculate the tour length of the best individual and compare with the optimal
            best_individual_tour_length = calculate_tour_length(population.best_individual.path, node_matrix)
            if optimal_tour_length:
                distance_from_optimal = abs(best_individual_tour_length - optimal_tour_length)
            else:
                distance_from_optimal = None

            print(f"\nGeneration {generation}")
            print(f"Max fitness: {max_f}")
            print(f"Min fitness: {min_f}")
            print(f"Mean fitness: {mean_fitness}")
            print(f"Stdev fitness: {stdev_fitness}")
            print(f"Median fitness: {median_fitness}")
            print(f"Best tour length: {best_individual_tour_length}")
            if distance_from_optimal is not None:
                print(f"Distance from optimal: {distance_from_optimal}\n")
                result_data.append({
                     "Distance from Optimal": distance_from_optimal,
                })

            result_data.append({
                "File": file, "Population Size": k, "Generation": generation,
                "Best Individual Fitness": population.best_individual.total_cost,
                "Best Tour Length": best_individual_tour_length,
                "Max Fitness": max_f, "Min Fitness": min_f, "Mean Fitness": avg_fitness,
                "STDEV Fitness": stdev_fitness, "Median Fitness": median_fitness
            })

    # Save results for this run to a CSV file
    output_file = os.path.join(output_folder, f"experiment_{run_number}_{os.path.basename(file)}_pop_{k}.csv")
    pd.DataFrame(result_data).to_csv(output_file, index=False)

    print(f"Execution time for {file} | Population {k} | Run {run_number}: {time.time() - start_time:.2f} seconds")
    print(f"Results saved to {output_file}")


def experiment_1(output_folder, num_runs=1):
    population_sizes = [50]
    test_files = [
        ("./tours/eil51.tsp", "./tours/eil51.opt.tour"),
        ("./tours/eil76.tsp", "./tours/eil76.opt.tour"),
        ("./tours/eil101.tsp", "./tours/eil101.opt.tour"),
        ("./tours/st70.tsp", "./tours/st70.opt.tour"),
        ("./tours/kroA100.tsp", "./tours/kroA100.opt.tour"),
        ("./tours/kroC100.tsp", "./tours/kroC100.opt.tour"),
        ("./tours/lin105.tsp", "./tours/lin105.opt.tour"),
        ("./tours/pcb442.tsp", "./tours/pcb442.opt.tour"),
        ("./tours/pr2392.tsp", "./tours/pr2392.opt.tour"),
        ("./tours/usa13509.tsp", "")
    ]

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Run multiple times as specified by `num_runs`
    for run_number in range(1, num_runs + 1):
        with ProcessPoolExecutor() as executor:
            futures = []
            for file, opt_file in test_files:
                for k in population_sizes:
                    futures.append(executor.submit(run_experiment, file, opt_file, k, run_number, output_folder))

            for future in futures:
                future.result()


if __name__ == '__main__':
    # Set the output folder for the experiment results
    output_folder = "results/experiment_1_results"
    # Specify the number of times the experiment should run
    num_runs = 30
    experiment_1(output_folder, num_runs)