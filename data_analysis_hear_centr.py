import networkx as nx
import numpy as np
import pandas as pd
import random
import scipy.stats as stats
import pickle  # Import pickle for serialization
import gzip
import shutil

file_path = "results/simulation_results_raw.csv.gz"
output_path = "results/hearing_centrality_results.csv"

all_c_values = [0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16]
all_delta_values = [
    0.6000000000000001,
    0.6200000000000001,
    0.6400000000000001,
    0.6600000000000001,
    0.6800000000000002,
    0.7000000000000002,
    0.7200000000000002,
    0.7400000000000002,
    0.7600000000000002,
    0.7800000000000002,
    0.8000000000000003,
    0.8200000000000003,
    0.8400000000000003,
    0.8600000000000003,
    0.8800000000000003,
    0.9000000000000004,
    0.9200000000000004,
    0.9400000000000004,
    0.9600000000000004,
    0.9800000000000004,
]

def calculate_hearing_centrality_all(df, c_value, delta_value):
    # Filter the data for the specific pair of c_value and delta_value
    filtered_data = df[(df["c_value"] == c_value) & (df["delta_value"] == delta_value)]

    # Dictionary to store hearing centrality values, indexed by initial_infected_node
    hearing_centrality_by_node = {}

    # Adjust the loop to cover the infected nodes you're interested in (0 through 499)
    for infected_node in range(500):
        # Select 1000 random rows for the current node
        random_indices = random.sample(range(len(filtered_data)), k=1000)
        #c
        selected_rows = filtered_data.iloc[random_indices].copy()
        #c
        # Convert ever_infected from string to numerical lists only for the selected rows
        selected_rows['ever_infected'] = selected_rows['ever_infected'].apply(lambda x: [int(num) for num in x.split()])
        
        # Calculate the status sum for the current node
        status_sum = selected_rows['ever_infected'].apply(lambda x: x[infected_node]).sum()

        # Calculate B as the sum of the statuses divided by 1000
        B = status_sum / 1000
        
        # Store the calculated hearing centrality in the dictionary
        hearing_centrality_by_node[infected_node] = B

    return hearing_centrality_by_node


# Assuming the DataFrame's header is on the first row, and data starts from the second row.
header_row = 1

# Open the gzip file for writing text. 'wt' mode is for writing text.
with open(output_path, "w", encoding="utf-8") as f:  # Changed to open()
    # Write the header
    f.write("c_value,delta_value,node,hearing_centrality\n")

    for c_index, c_value in enumerate(all_c_values):
        for delta_index, delta_value in enumerate(all_delta_values):
            pair_index = c_index * len(all_delta_values) + delta_index
            rows_to_skip = (
                header_row + pair_index * 500000
            )  # Calculate how many rows to skip

            raw_data_df = pd.read_csv(
                file_path,
                compression="gzip",
                skiprows=range(1, rows_to_skip),
                nrows=500000,
            )
       
            # Calculate hearing centralities
            hearing_centralities = calculate_hearing_centrality_all(
                raw_data_df, c_value, delta_value
            )

            # Write each result incrementally
            for node, centrality in hearing_centralities.items():
                line = f"{c_value},{delta_value},{node},{centrality:.10f}\n"
                f.write(line)
              # Print progress every 10th pair processed
            if (c_index * len(all_delta_values) + delta_index + 1) % 5 == 0:
                print(f"Processed {c_index * len(all_delta_values) + delta_index + 1} pairs.")

print(f"File saved to {output_path}")
