import os
import math
import psutil
import time
import pandas as pd
import matplotlib.pyplot as plt

class Tabu:
    def __init__(self, cities):
        self.cities = cities

    @staticmethod
    def distance(city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    def total_distance(self, route):
        total = 0
        for i in range(len(route)):
            city1 = self.cities[route[i]]
            city2 = self.cities[route[(i + 1) % len(route)]]
            total += self.distance(city1, city2)
        return total

    def generate_initial_solution(self):
        num_cities = len(self.cities)
        current_city = 0  # Start from the first city
        solution = [current_city]

        unvisited_cities = set(range(1, num_cities))  # All cities except the first one are unvisited

        while unvisited_cities:
            next_city = min(unvisited_cities,
                            key=lambda city: self.distance(self.cities[current_city], self.cities[city]))
            unvisited_cities.remove(next_city)
            solution.append(next_city)
            current_city = next_city

        return solution

    @staticmethod
    def get_neighbors(solution):  # 2-opt neighborhood
        neighbors = []
        for i in range(len(solution)):
            for j in range(i + 2, len(solution) + (i > 0)):
                neighbor = solution.copy()
                neighbor[i:(j % len(solution))] = reversed(solution[i:(j % len(solution))])
                neighbors.append(neighbor)
        return neighbors

    def tabu_search(self, max_iterations, min_tabu_size, max_tabu_size):
        current_solution = self.generate_initial_solution()
        best_solution = current_solution.copy()
        best_distance = self.total_distance(best_solution)
        tabu_list = []
        tabu_size = min_tabu_size

        for iteration in range(max_iterations):
            if (iteration + 1) % 100 == 0:
                print(f"Running tabu_search iteration {iteration + 1} of {max_iterations}")
            neighbors = self.get_neighbors(current_solution)
            best_neighbor = None
            best_neighbor_distance = float('inf')

            for neighbor in neighbors:
                neighbor_distance = self.total_distance(neighbor)
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
                tabu_size = max(min_tabu_size, tabu_size - 1)
            else:
                tabu_size = min(max_tabu_size, tabu_size + 1)

        return best_solution, best_distance


cities = [(60, 87), (13, 53), (66, 5), (38, 39), (79, 33), (38, 95), (73, 40), (39, 18), (51, 39), (90, 57),
                (42, 88), (76, 24), (55, 72), (19, 65), (81, 10), (64, 51), (33, 73), (94, 3), (27, 82), (59, 60),
                (31, 24), (90, 89), (15, 17), (71, 43), (8, 77), (46, 23), (20, 53), (61, 98), (2, 47), (16, 79),
                (74, 21), (85, 67), (33, 11), (40, 14), (56, 30), (67, 26), (98, 37), (9, 49), (28, 97), (49, 54),
                (70, 11), (24, 40), (87, 72), (63, 15), (45, 88), (33, 49), (13, 84), (98, 67), (52, 35), (80, 81)]

file = 'pursuit.csv'

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(
        columns=['max_iterations', 'min_tabu_size', 'max_tabu_size', 'num_cities', 'coordinates',
                 'execution_time', 'memory_used', 'best_route', 'best_distance'])
# number of cities is how many tuples are in known_cities
num_cities = 50
print(num_cities)


# min_tabu_size_list = [10]  # Minimum tabu size to test
# max_tabu_size_list = [2000]  # Maximum tabu size to test
# max_iterations_list = [50000]
# # Loop through the parameters
#
# # Loop through the parameters
# for min_tabu_size in min_tabu_size_list:
#     for max_tabu_size in max_tabu_size_list:
#         for max_iterations in max_iterations_list:
#
#             start_time = time.time()
#             tabu = Tabu(cities)
#             best_route, best_distance = tabu.tabu_search(max_iterations, min_tabu_size, max_tabu_size)
#             end_time = time.time()
#             memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # Memory usage in MB
#
#             # Create a DataFrame from the new row
#             new_row = pd.DataFrame([{
#                 'max_iterations': max_iterations,
#                 'min_tabu_size': min_tabu_size,
#                 'max_tabu_size': max_tabu_size,
#                 'num_cities': len(cities),
#                 'coordinates': str(cities),
#                 'execution_time': end_time - start_time,
#                 'memory_used': memory_usage,
#                 'best_route': str(best_route),
#                 'best_distance': best_distance
#             }])
#             # Concatenate the new row DataFrame with the existing DataFrame
#             df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(file, index=False)
df = pd.read_csv(file)
# round the execution time, memory_used and best_distance to 2 decimal places
df['execution_time'] = df['execution_time'].round(2)
df['memory_used'] = df['memory_used'].round(2)
df['best_distance'] = df['best_distance'].round(2)
# Group the data by parameters and calculate the mean
best_route = [36, 9, 47, 31, 42, 49, 21, 27, 0, 44, 10, 5, 38, 18, 16, 29, 46, 24, 13, 26, 1, 37, 28, 41, 45, 39, 12, 19, 15, 23, 6, 4, 11, 30, 35, 34, 48, 8, 3, 20, 22, 32, 33, 7, 25, 43, 2, 40, 14, 17]

df = df.drop(columns=['coordinates', 'best_route'])

grouped = df.groupby(['max_iterations', 'max_tabu_size', 'num_cities']).mean().reset_index()
# Show data
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)
print(df)

# display the best route and lines between cities
plt.figure()
for city in cities:
    plt.plot(city[0], city[1], 'bo')
    plt.text(city[0], city[1], str(city), fontsize=8, ha='right')
for i in range(len(best_route)):
    city1 = cities[best_route[i]]
    city2 = cities[best_route[(i + 1) % len(best_route)]]
    plt.plot([city1[0], city2[0]], [city1[1], city2[1]], 'r')
plt.title(f'Tabu Search: {len(cities)} cities, 50000 iterations, 2000 tabu size')
plt.show()
