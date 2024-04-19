import math
import numpy as np
import matplotlib.pyplot as plt
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def total_distance(route, cities):
    total = 0
    for i in range(len(route)):
        city1 = cities[route[i]]
        city2 = cities[route[(i + 1) % len(route)]]
        total += distance(city1, city2)
    return total


def generate_initial_solution(num_cities):
    return np.random.permutation(num_cities)


def get_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors


def tabu_search(cities, max_iterations, tabu_size):
    num_cities = len(cities)
    current_solution = generate_initial_solution(num_cities)
    best_solution = current_solution.copy()
    best_distance = total_distance(best_solution, cities)
    tabu_list = []

    for _ in range(max_iterations):
        neighbors = get_neighbors(current_solution)
        best_neighbor = None
        best_neighbor_distance = float('inf')

        for neighbor in neighbors:
            if tuple(neighbor) in tabu_list:
                continue

            neighbor_distance = total_distance(neighbor, cities)
            if neighbor_distance < best_neighbor_distance:
                best_neighbor = neighbor
                best_neighbor_distance = neighbor_distance

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        tabu_list.append(tuple(current_solution))
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        if best_neighbor_distance < best_distance:
            best_solution = best_neighbor
            best_distance = best_neighbor_distance

    return best_solution, best_distance

def route_plot(cities, best_route, max_iterations, tabu_size):
    # Create a new figure
    plt.figure()

    # Plot each city as a point
    for city in cities:
        plt.plot(city[0], city[1], 'bo')
        plt.text(city[0], city[1], str(city), fontsize=8, ha='right')

    # Draw a line between each city in the order of the best route
    for i in range(-1, len(best_route) - 1):
        city1 = cities[best_route[i]]
        city2 = cities[best_route[i + 1]]
        plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r')

    #title
    plt.title(f'Tabu Search: {len(cities)} cities, {max_iterations} iterations, {tabu_size} tabu size')
    # Save the plot in the route_plots directory
    plt.savefig(f'route_plots2/tsp_plt_cit{len(cities)}_iter{max_iterations}_ts{tabu_size}.png')
    # Display the plot
    plt.show()
