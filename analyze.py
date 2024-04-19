import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# Load the data
df = pd.read_csv('TSPdata.csv')

# Group the data by parameters and calculate the mean
df = df.drop(columns=['coordinates', 'best_route', 'Random/Known'])
grouped = df.groupby(['max_iterations', 'tabu_size', 'num_cities']).mean().reset_index()
# Show data
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df)
print("Sumed execution time of the program in seconds: ", df['execution_time'].sum())
# Define a function to plot data for different numbers of cities
def plot_data(data_type, num_cities):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=grouped[grouped['num_cities'] == num_cities], x='max_iterations', y=data_type, hue='tabu_size')
    plt.xscale('log')
    plt.xlabel('Max Iterations')
    plt.ylabel(f'{data_type.replace("_", " ").title()} ({unit[data_type]})')
    plt.legend(title='Tabu Size')
    plt.title(f'{data_type.replace("_", " ").title()} for {num_cities} Cities')
    plt.savefig(f'analyze_plots/{data_type}_{num_cities}.png')
    plt.show()

# Define units for each data type
unit = {
    'execution_time': 'Seconds',
    'memory_used': 'MB',
    'best_distance': 'Units'
}

# Plot data for different types and numbers of cities
for data_type in ['execution_time', 'memory_used', 'best_distance']:
    for num_cities in [10, 20, 50]:
        plot_data(data_type, num_cities)

