import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('TSPdata.csv')
print(df)
# Group the data by parameters and calculate the mean
df = df.drop(columns=['coordinates', 'best_route', 'Random/Known'])
grouped = df.groupby(['max_iterations', 'tabu_size', 'num_cities']).mean().reset_index()

# Plot the execution time for 10 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 10], x='max_iterations', y='execution_time', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Execution Time (s)')
plt.legend(title='Tabu Size')
plt.title('Execution Time for 10 Cities')
plt.savefig('analyze_plots/execution_time_10.png')
plt.show()

# Plot the execution time for 20 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 20], x='max_iterations', y='execution_time', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Execution Time (s)')
plt.legend(title='Tabu Size')
plt.title('Execution Time for 20 Cities')
plt.savefig('analyze_plots/execution_time_20.png')
plt.show()

# Plot the execution time for 50 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 50], x='max_iterations', y='execution_time', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Execution Time (s)')
plt.legend(title='Tabu Size')
plt.title('Execution Time for 50 Cities')
plt.savefig('analyze_plots/execution_time_50.png')
plt.show()

# Plot the memory used for 10 cities, parameterized by max_iterations and tabu_size

plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 10], x='max_iterations', y='memory_used', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Memory Used (MB)')
plt.legend(title='Tabu Size')
plt.title('Memory Used for 10 Cities')
plt.savefig('analyze_plots/memory_used_10.png')
plt.show()

# Plot the memory used for 20 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 20], x='max_iterations', y='memory_used', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Memory Used (MB)')
plt.legend(title='Tabu Size')
plt.title('Memory Used for 20 Cities')
plt.savefig('analyze_plots/memory_used_20.png')
plt.show()

# Plot the memory used for 50 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 50], x='max_iterations', y='memory_used', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Memory Used (MB)')
plt.legend(title='Tabu Size')
plt.title('Memory Used for 50 Cities')
plt.savefig('analyze_plots/memory_used_50.png')
plt.show()

# Plot the best distance for 10 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 10], x='max_iterations', y='best_distance', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Best Distance')
plt.legend(title='Tabu Size')
plt.title('Best Distance for 10 Cities')
plt.savefig('analyze_plots/best_distance_10.png')
plt.show()

# Plot the best distance for 20 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 20], x='max_iterations', y='best_distance', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Best Distance')
plt.legend(title='Tabu Size')
plt.title('Best Distance for 20 Cities')
plt.savefig('analyze_plots/best_distance_20.png')
plt.show()

# Plot the best distance for 50 cities, parameterized by max_iterations and tabu_size
plt.figure(figsize=(10, 6))
sns.lineplot(data=grouped[grouped['num_cities'] == 50], x='max_iterations', y='best_distance', hue='tabu_size')
plt.xscale('log')
plt.xlabel('Max Iterations')
plt.ylabel('Best Distance')
plt.legend(title='Tabu Size')
plt.title('Best Distance for 50 Cities')
plt.savefig('analyze_plots/best_distance_50.png')
plt.show()

