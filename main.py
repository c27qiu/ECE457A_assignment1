import yaml
import math
from typing import Dict
from utils import search_algorithms, cost_functions, plot_utils
import itertools
import sys

    
def generate_neighborhoods(array_range, dimensions, num_neighborhoods_per_dimension):
    # Size of every grid cell in each dimension
    cell_size = [(array_range[1] - array_range[0]) / num_neighborhoods_per_dimension] * dimensions

    # Grid cell boundaries in every dimension
    grid_boundaries = [list(range(int(array_range[0]), int(array_range[1] + 1), int(size))) for size in cell_size]
    
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

def generate_layers(dimension, num_layers, x_range):
    # Calculate layer size for each dimension
    layer_size = [r[1] / num_layers for r in x_range]
        
    layers = []

    # Calculate the boundaries of each layer
    for i in range(num_layers):
        layer = []
        for d in range(dimension):
            lower_bound = -1* layer_size[d] * (i + 1)
            upper_bound = layer_size[d] * (i + 1)
            layer.append([lower_bound, upper_bound])
        layers.append(layer)

    return layers

def VNS(cost_function, neighborhoods, all_x_history, all_cost_history):
    best_cost = math.inf
    best_x = []
    
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
        
    return [best_cost, best_x]
    
def main(config: Dict) -> None:
    all_x_history = []
    all_cost_history = []
    
    # Getting user input:
    dimension = int(input("Enter a value for the dimension: "))
    # The actual number of neighborhoods will be num_neighborhoods_per_dimension^dimensions
    num_neighborhoods_per_dimension = int(input("Enter a value for the number of neighborhoods per dimension: "))
    num_layers = int(input("Enter a value for the number of layers to perform GNS: "))

    # Get the cost function
    if config['cost_function'] == 'schwefel':
        cost_function = cost_functions.schwefel
        x_range = [[-500, 500] for i in range(dimension)]  # The range for each dimension
    
    # Generate layers
    # NOTE: If num_layers = 1, then we are just performing VNS.
    # If num_layers != 1, then we are performing GNS.
    layers = generate_layers(dimension, num_layers, x_range)
    
    vns_solutions = []
    global_best = math.inf
    global_x = []

    for layer in layers:
        best_cost = math.inf
        best_x = []
        neighborhoods = generate_neighborhoods(layer[0], dimension, num_neighborhoods_per_dimension)
        best_solution = VNS(cost_function, neighborhoods, all_x_history, all_cost_history)
        vns_solutions.append(best_solution)
    
    for solutions in vns_solutions:
        cur_cost, cur_x = solutions[0], solutions[1]
        if cur_cost < global_best:
            global_best = cur_cost
            global_x = cur_x
    
    if len(global_x) == 2: 
        # If the dimensionality is 2, visualize the results.
        plot_utils.plot_results(best_x=global_x, best_cost=global_best,
                                x_history=all_x_history, cost_history=all_cost_history,
                                cost_function=cost_function, x_range=x_range)
        
    print('Global best x: ', global_x)
    print('Global best cost: ', global_best)

if __name__ == '__main__':
    with open('./config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    main(config=config)