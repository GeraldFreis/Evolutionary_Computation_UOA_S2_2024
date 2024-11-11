def read_optimal_tour(optimal_file):
    """
    Read the optimal tour from a file.

    Args:
    - optimal_file: Path to the file containing the optimal tour.

    Returns:
    - List of city indices representing the optimal tour.
    """
    with open(optimal_file, 'r') as file:
        lines = file.readlines()

    # Extract the tour from the file, ignoring any headers, comments, or EOF markers
    tour = []
    for line in lines:
        if line.strip().isdigit():
            city = int(line.strip()) - 1  # Convert city index to 0-based
            tour.append(city)
        elif line.strip() == '-1':  # End of tour section
            break
    return tour

def calculate_tour_length(tour, distance_matrix):
    """
    Calculate the length of a tour based on the distance matrix.
    
    Args:
    - tour: List of city indices representing the tour.
    - distance_matrix: 2D matrix containing distances between cities.
    
    Returns:
    - Total length of the tour.
    """
    length = 0
    num_cities = len(tour)
    for i in range(num_cities - 1):
        length += distance_matrix[tour[i]][tour[i+1]]
    length += distance_matrix[tour[-1]][tour[0]]  # Return to start