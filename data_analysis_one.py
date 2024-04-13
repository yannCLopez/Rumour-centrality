import networkx as nx
import numpy as np
import pandas as pd
import random
import scipy.stats as stats
import pickle  # Import pickle for serialization
import gzip
import shutil
import time

file_path = "simulation_results_raw.csv.gz"
output_path_both = "results/both_centralities_one.csv"

"""
This code picks one c and delta and compute hearing and sending centralities for all nodes using all the available data (sample sizes will, therefore, be unbalanced).
"""
start_time = time.time()

def calculate_sending_centrality_one(df, c_value, delta_value):

    # Filter the data for the specific pair of c_value and delta_value
    filtered_data = df[(df["c_value"] == c_value) & (df["delta_value"] == delta_value)]

    # Dictionary to store sending centrality values, indexed by initial_infected_node
    sending_centrality_by_node = {}

    # Adjust the loop to cover the initial infected nodes you're interested in (0 through 4)
    for infected_node in range(1):
        if infected_node % 20 == 0:
            print(f"Node[{infected_node}]")

        # Filter out rows where initial_infected_node is the current number
        specific_infected_node_data = filtered_data[
            filtered_data["initial_infected_node"] == infected_node
        ].copy()

        # For each row, calculate A_y as the sum of ever_infected divided by 500
        Ay_values = specific_infected_node_data["ever_infected"].apply(sum) / 500

        # Calculate the average of all A_y values for this infected_node
        sending_centrality = Ay_values.mean() if not Ay_values.empty else 0

        # Store the calculated sending centrality in the dictionary
        sending_centrality_by_node[infected_node] = sending_centrality

    return sending_centrality_by_node



def calculate_hearing_centrality_one(df, c_value, delta_value):
    # Filter the data for the specific pair of c_value and delta_value
    filtered_data = df[(df["c_value"] == c_value) & (df["delta_value"] == delta_value)]

    # Dictionary to store hearing centrality values, indexed by initial_infected_node
    hearing_centrality_by_node = {}

    # Adjust the loop to cover the infected nodes you're interested in (0 through 499)
    for infected_node in range(1):

        # Calculate the status sum for the current node
        status_sum = df['ever_infected'].apply(lambda x: x[infected_node]).sum()

        # Calculate B as the sum of the statuses divided by length of the filtered data
        B = status_sum / len(filtered_data)
        
        # Store the calculated hearing centrality in the dictionary
        hearing_centrality_by_node[infected_node] = B

    return hearing_centrality_by_node


#BOTH

header_row = 1

# Open the gzip file for writing text. 'wt' mode is for writing text.
with open(output_path_both, "w", encoding="utf-8") as f:  # Changed to open()
    # Write the header
    f.write("c_value,delta_value,initial_infected_node,sending_centrality, hearing_centrality\n")

    rows_to_skip = (
                    39000000
                )  # Calculate how many rows to skip

    raw_data_df = pd.read_csv(
                    file_path,
                    compression="gzip",
                    skiprows=range(1, rows_to_skip),
                    nrows=500000,
                )
    
    raw_data_df["ever_infected"] = raw_data_df[
            "ever_infected"
        ].apply(lambda x: [pd.to_numeric(num) for num in x.split()])
            
                # Calculate sending centralities
    sending_centralities = calculate_sending_centrality_one(
                    raw_data_df, 0.06, 0.9600000000000004 
                )
        # Calculate hearing centralities
    hearing_centralities = calculate_hearing_centrality_one(
        raw_data_df, 0.06, 0.9600000000000004
    )

    # Write each result incrementally. Ensure nodes in both dictionaries match.
    for node in sending_centralities:
        sending_centrality = sending_centralities[node]
        hearing_centrality = hearing_centralities.get(node, 0)  # Default to 0 if not found
        line = f"{0.06},{0.9600000000000004},{node},{sending_centrality:.15f},{hearing_centrality:.15f}\n"
        f.write(line)

print(f"File saved to {output_path_both}")

end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")