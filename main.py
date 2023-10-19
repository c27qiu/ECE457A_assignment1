import yaml
import math
from typing import Dict
from utils import search_algorithms, cost_functions, plot_utils
import itertools
import sys

best_cost = math.inf
best_x = []
all_x_history = []
all_cost_history = []
    
def generate_neighborhoods(array_range, dimensions, num_neighborhoods_per_dimension):
    # Calculate the size of each grid cell for each dimension
    cell_size = [(array_range[1] - array_range[0]) / num_neighborhoods_per_dimension] * dimensions

    # Generate grid cell boundaries for each dimension
    grid_boundaries = [list(range(array_range[0], array_range[1] + 1, int(size))) for size in cell_size]

    # Generate neighborhoods by iterating through grid cell combinations
    neighborhoods = []
    for combination in itertools.product(*grid_boundaries):        
        neighborhood = []
        for i in range(dimensions):
            
            if combination[i] < grid_boundaries[0][-1] or combination[i] + int(cell_size[i]) <= grid_boundaries[0][-1]:
                neighborhood.append([combination[i], combination[i] + int(cell_size[i])])
                
        # Adding neighborhood to our list
        if len(neighborhood) == dimensions:
            neighborhoods.append(neighborhood)        

    return neighborhoods

def VNS(cost_function, neighborhoods):
    global best_cost
    global best_x
    global all_x_history
    global all_cost_history
    
    # Get the search algorithm
    if config['search_algorithm'] == 'local_search':
        k = 0
        
        while k < len(neighborhoods):
            best_cur_x, best_cur_cost, cur_x_history, cur_cost_history = search_algorithms.local_search(cost_function=cost_function, max_itr=config['local_search']['max_itr'],
                                                                                        convergence_threshold=config['local_search']['convergence_threshold'],
                                                                                        x_initial=config['x_initial'], cur_neighborhood=neighborhoods[k])
            all_x_history.extend(cur_x_history)
            all_cost_history.extend(cur_cost_history)
            
            if best_cur_cost < best_cost:
                best_cost = best_cur_cost
                best_x = best_cur_x
                k = 0
            else:
                k += 1
    
def main(config: Dict) -> None:
    dimension = int(input("Enter a value for the dimension: "))
    
    # The actual number of neighborhoods will be num_neighborhoods_per_dimension^dimensions
    num_neighborhoods_per_dimension = int(input("Enter a value for the number of neighborhoods per dimension: "))

    # Get the cost function
    if config['cost_function'] == 'schwefel':
        cost_function = cost_functions.schwefel
        x_range = [[-500, 500] for i in range(dimension)]  # The range for each dimension
    
    # Create neighborhoods
    neighborhoods = generate_neighborhoods([-500, 500], dimension, num_neighborhoods_per_dimension)

    VNS(cost_function, neighborhoods)
    
    if len(best_x) == 2: 
        # If the dimensionality is 2, visualize the results.
        plot_utils.plot_results(best_x=best_x, best_cost=best_cost,
                                x_history=all_x_history, cost_history=all_cost_history,
                                cost_function=cost_function, x_range=x_range)
        
    print('Global best x: ', best_x)
    print('Global best cost: ', best_cost)

if __name__ == '__main__':
    with open('./config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    main(config=config)