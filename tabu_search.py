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


def generate_initial_solution(cities):
    num_cities = len(cities)
    current_city = 0  # Start from the first city
    solution = [current_city]

    unvisited_cities = set(range(1, num_cities))  # All cities except the first one are unvisited

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: distance(cities[current_city], cities[city]))
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city

    return solution


def get_neighbors(solution):  # 2-opt neighborhood
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 2, len(solution) + (i > 0)):
            neighbor = solution.copy()
            neighbor[i:(j % len(solution))] = reversed(solution[i:(j % len(solution))])
            neighbors.append(neighbor)
    return neighbors


def tabu_search(cities, max_iterations, min_tabu_size, max_tabu_size):
    current_solution = generate_initial_solution(cities)
    best_solution = current_solution.copy()
    best_distance = total_distance(best_solution, cities)
    tabu_list = []
    tabu_size = min_tabu_size

    for iteration in range(max_iterations):
        neighbors = get_neighbors(current_solution)
        best_neighbor = None
        best_neighbor_distance = float('inf')

        for neighbor in neighbors:
            neighbor_distance = total_distance(neighbor, cities)
            if tuple(neighbor) in tabu_list and neighbor_distance >= best_distance:
                continue

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
            # aspiration criteria decrease tabu size when we find a better solution
            # and increase tabu size when we don't find a better solution
            tabu_size = max(min_tabu_size, tabu_size - 1)
        else:
            tabu_size = min(max_tabu_size, tabu_size + 1)

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

    # title
    plt.title(f'Tabu Search: {len(cities)} cities, {max_iterations} iterations, {tabu_size} tabu size')
    # Save the plot in the route_plots directory
    plt.savefig(f'route_plots6/tsp_plt_cit{len(cities)}_iter{max_iterations}_ts{tabu_size}.png')
