import networkx as nx
import numpy as np
import pandas as pd
import random
import scipy.stats as stats
import pickle  # Import pickle for serialization
import gzip
import shutil

# Load the adjacency matrix and convert it to a NetworkX graph


file_path = 'adj_allVillageRelationships_vilno_37_copy.xlsx'


adjacency_matrix_df = pd.read_excel(file_path, index_col=0)
graph = nx.from_pandas_adjacency(adjacency_matrix_df)
largest_eigenvalue = max(nx.adjacency_spectrum(graph)).real
eigenvector_centrality = np.array(list(nx.eigenvector_centrality(graph).values()))

def simulate_SIR(graph, c, delta, initial_infecteds):
    # Initialize all nodes as susceptible
    status = {node: 'S' for node in graph.nodes()}
    # Keep track of who gets infected during the simulation
    ever_infected = {node: 0 for node in graph.nodes()}
    # Infect the initial nodes
    for node in initial_infecteds:
        status[node] = 'I'
        ever_infected[node] = 1  # Mark the node as having been infected

    # Record the number of S, I, R nodes in each step
    SIR_counts = []

    while 'I' in status.values():
        new_status = status.copy()
        for node in graph.nodes():
            if status[node] == 'I':
                # Try to infect neighbors
                for neighbor in graph.neighbors(node):
                    if status[neighbor] == 'S' and np.random.rand() < c:
                        new_status[neighbor] = 'I'
                        ever_infected[neighbor] = 1  # Mark the node as having been infected
                # Attempt recovery
                if np.random.rand() < delta:
                    new_status[node] = 'R'
        status = new_status
        SIR_counts.append((list(status.values()).count('S'), list(status.values()).count('I'), list(status.values()).count('R')))

    return ever_infected

# Parameters
num_simulations = 1000
mesh = 0.02
delta_range = np.arange(0.8 - 0.2, 0.99, mesh)
c_base = 0.7 / largest_eigenvalue
c_range = np.arange(max(0, c_base - 0.1), c_base + 0.1 + mesh, mesh)
node_count = len(graph.nodes())

# Initialize dictionary to store the final results for each node
#c

simulation_results_list = []

for i, c in enumerate(c_range):
    print(f"Running simulations for c value: {i + 1} / {len(c_range)}")
    for j, delta in enumerate(delta_range):
        for node in graph.nodes():
            for _ in range(num_simulations):
                ever_infected = simulate_SIR(graph, c, delta, [node])
                # Store the result as a dictionary
                simulation_results_list.append({
                    'c_value': c,
                    'delta_value': delta,
                    'initial_infected_node': node,
                    'ever_infected': str(list(ever_infected.values()))  # Convert the ever_infected dict to a list and then to a string
                })

# Convert the list of dictionaries to a DataFrame
results_df = pd.DataFrame(simulation_results_list)

# Specify your desired CSV file path
csv_file_path = 'results/simulation_results_raw.csv'


# Specify the path for the compressed file
compressed_file_path = csv_file_path + '.gz'

# Save the DataFrame to a compressed CSV file
with gzip.open(compressed_file_path, 'wt', encoding='utf-8') as f:
    results_df.to_csv(f, index=False)


print(f"Compressed file saved to {compressed_file_path}")