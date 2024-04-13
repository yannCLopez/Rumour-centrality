#Skips every first line, except that of the first file. 

import os

# Directory containing the files
directory = "sending_centrality"
# Output file where all files will be appended
output_file_path = "sending_centrality_all.csv"

# All possible c and delta values from your script
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

# Open the output file in write mode
with open(output_file_path, 'w') as outfile:
    first_file = True  # Flag to indicate if we're processing the first file
    # Iterate through each c_value
    for c_value in all_c_values:
        # Then iterate through each delta_value
        for delta_value in all_delta_values:
            # Construct the file name based on the current c_value and delta_value
            file_name = f"sending_centrality_results_{c_value}_{delta_value}.csv"
            file_path = os.path.join(directory, file_name)
            
            # Check if the file exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as infile:
                    if first_file:
                        # For the first file, read and write the contents as is
                        outfile.write(infile.read())
                        first_file = False  # Update the flag
                    else:
                        # For subsequent files, skip the first line
                        next(infile)  # Skip the first line
                        outfile.write(infile.read())
                print(f"Appended {file_name}")
            else:
                print(f"File {file_name} does not exist and was skipped.")

print(f"All files have been successfully appended to {output_file_path}.")
