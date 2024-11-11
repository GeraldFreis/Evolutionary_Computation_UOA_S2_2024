import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from FileReader import filereader
from Individual import *
from Population import *
from InverOver import *
from statistics import stdev, mean, median
import pandas as pd
from tqdm import tqdm
from OptTourReader import read_optimal_tour, calculate_tour_length
import time
from concurrent.futures import ProcessPoolExecutor


def calculate_tour_length(tour, distance_matrix):
    length = 0
    num_cities = len(tour)
    for i in range(num_cities - 1):
        length += distance_matrix[tour[i]][tour[i + 1]]
    length += distance_matrix[tour[-1]][tour[0]]  # Return to start
    return length


def run_experiment(file, opt_file, k, run_number, output_folder):
    start_time = time.time()
    node_matrix = filereader(file)
    
    # Read the optimal tour if provided
    if opt_file != "":
        optimal_tour = read_optimal_tour(opt_file)
        optimal_tour_length = calculate_tour_length(optimal_tour, node_matrix)
    else:
        optimal_tour_length = None

    print(f"File: {file} | Population Size: {k} | Run: {run_number}")

    population = Population(
        node_matrix,
        num_paths=k,
        matepool_selection="tournament",
        survivor_selection="elitism",
        crossover=Crossover.order_crossover,
        mutation=Scramble,
        selection_params={"tournament_size": k // 4 * 5}
    )

    p = 0.02 if k < 50 else 0.07
    inver_over_operator = InverOver(population.population, p=p)

    best_tour_length = float('inf')
    early_stopping_threshold = 0.01

    result_data = []

    for generation in tqdm(range(20000), desc=f"File {file} - Population Size {k} - Run {run_number}"):
        inver_over_operator.evolve_population()

        if generation % 1000 == 0:
            best_individual = population.best_individual
            current_tour_length = calculate_tour_length(best_individual.path, node_matrix)

            print(f"\nGeneration {generation}")
            print(f"Best tour length: {current_tour_length}")
            print(f"Optimal tour length: {optimal_tour_length}")

            if opt_file != "":
                fitness_difference = abs(current_tour_length - optimal_tour_length)
                print(f"Distance from optimal: {fitness_difference}\n")
                result_data.append({
                     "Distance from Optimal": fitness_difference,
                })
                if fitness_difference / optimal_tour_length < early_stopping_threshold:
                    print(f"Early stopping at generation {generation}, best tour length: {current_tour_length}")
                    break
                        
            

            pop_fitnesses = population.get_population_statistics()
            max_f = max(pop_fitnesses)
            min_f = min(pop_fitnesses)
            mean_f = mean(pop_fitnesses)
            stdev_f = stdev(pop_fitnesses)
            median_f = median(pop_fitnesses)

            result_data.append({
                "File": file, "Population Size": k, "Generation": generation,
                "Best Individual Fitness": population.best_individual.total_cost,
                "Best Tour Length": current_tour_length,
                "Max Fitness": max_f, "Min Fitness": min_f, "Mean Fitness": mean_f,
                "STDEV Fitness": stdev_f, "Median Fitness": median_f, "Best Tour Length": current_tour_length
            })

        if current_tour_length < best_tour_length:
            best_tour_length = current_tour_length

    # Save results for this run to a CSV file
    output_file = os.path.join(output_folder, f"experiment_{run_number}_{os.path.basename(file)}_pop_{k}.csv")
    pd.DataFrame(result_data).to_csv(output_file, index=False)

    print(f"Execution time for {file} | Population {k} | Run {run_number}: {time.time() - start_time:.2f} seconds")
    print(f"Results saved to {output_file}")


def experiment_4(output_folder, num_runs=1):
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

    # Run the experiment multiple times as specified by `num_runs`
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
    output_folder = "results/experiment_4_results"
    # Specify the number of times the experiment should run
    num_runs = 30
    experiment_4(output_folder, num_runs)
