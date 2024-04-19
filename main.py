import os
import random
import argparse
import psutil
import time
import pandas as pd

from tabu_search import tabu_search, route_plot

# Define command-line arguments
parser = argparse.ArgumentParser(description='Run Tabu Search for TSP')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--random', action='store_true', help='Use random cities')
group.add_argument('--known', action='store_true', help='Use known cities')
parser.add_argument('--num_cities', type=int, required=True, help='Number of cities')
args = parser.parse_args()
# Define known cities
known_cities = [(60, 87), (13, 53), (66, 5), (38, 39), (79, 33), (38, 95), (73, 40), (39, 18), (51, 39), (90, 57),
                (42, 88), (76, 24), (55, 72), (19, 65), (81, 10), (64, 51), (33, 73), (94, 3), (27, 82), (59, 60),
                (31, 24), (90, 89), (15, 17), (71, 43), (8, 77), (46, 23), (20, 53), (61, 98), (2, 47), (16, 79),
                (74, 21), (85, 67), (33, 11), (40, 14), (56, 30), (67, 26), (98, 37), (9, 49), (28, 97), (49, 54),
                (70, 11), (24, 40), (87, 72), (63, 15), (45, 88), (33, 49), (13, 84), (98, 67), (52, 35), (80, 81)]

# Use command-line arguments to determine cities
if args.random:
    num_cities = args.num_cities
    cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_cities)]
elif args.known:
    num_cities = args.num_cities
    cities = known_cities[:num_cities]
else:
    raise ValueError('Either --random or --known must be specified')
#num_cities_list = [10, 20, 50]  # Number of cities to test [5, 10, 15, 20, 30, 50]
max_iterations_list = [5, 10, 50, 100, 200, 500, 1000, 5000]  # Number of iterations to test [5, 10, 50, 100, 200, 500, 1000, 5000]
tabu_size_list = [10, 20, 40, 50, 80, 100, 200]  # Tabu size to test [10, 20, 40, 50, 80, 100, 200]

# Check if the data file exists
if os.path.exists('TSPdata.csv'):
    # If it exists, load it into a dataframe
    df = pd.read_csv('TSPdata.csv')
else:
    # If it doesn't exist, create a new dataframe
    df = pd.DataFrame(columns=['Random/Known', 'max_iterations', 'tabu_size', 'num_cities', 'coordinates',
                               'execution_time', 'memory_used', 'best_route', 'best_distance'])

# Loop through the parameters
for tabu_size in tabu_size_list:
    for max_iterations in max_iterations_list:
        start_time = time.time()
        best_route, best_distance = tabu_search(cities, max_iterations, tabu_size)
        end_time = time.time()
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # Memory usage in MB

        # Create a DataFrame from the new row
        new_row = pd.DataFrame([{
            'Random/Known': 'Random' if args.random else 'Known',
            'max_iterations': max_iterations,
            'tabu_size': tabu_size,
            'num_cities': len(cities),
            'coordinates': str(cities),
            'execution_time': end_time - start_time,
            'memory_used': memory_usage,
            'best_route': str(best_route),
            'best_distance': best_distance
        }])
        # Concatenate the new row DataFrame with the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)
        # Plot the best route
        route_plot(cities, best_route, max_iterations, tabu_size)

# Save the dataframe to a CSV file
df.to_csv('TSPdata.csv', index=False)
