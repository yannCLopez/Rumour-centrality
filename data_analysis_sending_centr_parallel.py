import pandas as pd
from multiprocessing import Pool
import os

file_path = "simulation_results_raw.csv.gz"


def calculate_sending_centrality_all(df, c_value, delta_value):

    # Filter the data for the specific pair of c_value and delta_value
    filtered_data = df[(df["c_value"] == c_value) & (df["delta_value"] == delta_value)]

    # Dictionary to store sending centrality values, indexed by initial_infected_node
    sending_centrality_by_node = {}

    # Adjust the loop to cover the initial infected nodes you're interested in 
    for infected_node in range(500):
        if infected_node % 50 == 0:
            print(f"Node[{infected_node}]")
        # Filter out rows where initial_infected_node is the current number
        specific_infected_node_data = filtered_data[
            filtered_data["initial_infected_node"] == infected_node
        ].copy()

        # Change ever_infected from string to numerical lists
        specific_infected_node_data["ever_infected"] = specific_infected_node_data[
            "ever_infected"
        ].apply(lambda x: [pd.to_numeric(num) for num in x.split()])

        # For each row, calculate A_y as the sum of ever_infected divided by 500
        Ay_values = specific_infected_node_data["ever_infected"].apply(sum) / 500

        # Calculate the average of all A_y values for this infected_node
        sending_centrality = Ay_values.mean() if not Ay_values.empty else 0

        # Store the calculated sending centrality in the dictionary
        sending_centrality_by_node[infected_node] = sending_centrality

    return sending_centrality_by_node



def process_pair(args):
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
     
    c_value, delta_value = args
    print(f"Starting processing for c={c_value}, delta={delta_value}")  # Log the start of processing
    
    output_path = f"results/run_4/sending_centrality_results_{c_value}_{delta_value}.csv"
    
    # Load the data specific to c_value and delta_value
    # Assuming the DataFrame's header is on the first row, and data starts from the second row.
    header_row = 1
    with open(output_path, "w", encoding="utf-8") as f:  # Changed to open()
        # Write the header
        f.write("c_value,delta_value,initial_infected_node,sending_centrality\n")

        pair_index = all_c_values.index(c_value) * len(all_delta_values) + all_delta_values.index(delta_value)
        rows_to_skip = header_row + pair_index * 500000  # Adjust based on your data structure
        
        raw_data_df = pd.read_csv(
            file_path,
            compression="gzip",
            skiprows=range(1, rows_to_skip),
            nrows=500000,
        )
        
        # Place your data processing logic here, similar to calculate_sending_centrality_all()
        sending_centralities = calculate_sending_centrality_all(raw_data_df, c_value, delta_value)
        
        # Write results to file, consider using CSV or other efficient data formats
       
        for node, centrality in sending_centralities.items():
            line = f"{c_value},{delta_value},{node},{centrality:.10f}\n"
            f.write(line)
    
    print(f"Process ID: {os.getpid()} - Results for c={c_value}, delta={delta_value} saved to {output_path}")


if __name__ == "__main__":
    # Define your sets of c_values and delta_values
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
    # Prepare a list of all combinations of c_value and delta_value
    args_list = [(c, d) for c in all_c_values for d in all_delta_values]
    
    # Determine the number of processes based on your machine's capability
    num_processes = os.cpu_count()  # or a fixed number less than or equal to the number of CPU cores
    
    with Pool(processes=num_processes) as pool:
        # Map process_pair function to each combination of c_value and delta_value
        pool.map(process_pair, args_list)
    
    print("Parallel processing complete.")
