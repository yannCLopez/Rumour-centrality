import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


import os
print(os.getcwd())


# Placeholder for loading your data
df_sending = pd.read_csv(
    "results/hearing_and_sending_centralities/sending_centrality_all.csv"
)
df_hearing = pd.read_csv(
    "results/hearing_and_sending_centralities/hearing_centrality_all.csv"
)


# Merge the two DataFrames on 'c_value', 'delta_value', and 'initial_infected_node'
combined_df = pd.merge(
    df_sending, df_hearing, on=["c_value", "delta_value", "initial_infected_node"]
)
print('combined', combined_df[:7])
# Placeholder for your c_value and delta_value ranges
all_c_values = [0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16]
all_delta_values = [
            0.6,
            0.62,
            0.64,
            0.66,
            0.68,
            0.7,
            0.72,
            0.74,
            0.76,
            0.78,
            0.8,
            0.82,
            0.84,
            0.86,
            0.88,
            0.9,
            0.92,
            0.94,
            0.96,
            0.98,
]


# Prepare a list to hold our rows before converting to a DataFrame
results = []

# Calculate Pearson correlation coefficient and p-value for each unique pair of c_value and delta_value
for c_value in all_c_values:
    for delta_value in all_delta_values:
        # Filter for current c_value and delta_value
        subset_df = combined_df[
            (combined_df["c_value"] == c_value)
            & (combined_df["delta_value"] == delta_value)
        ]


        if (
            len(subset_df) > 1
        ):  # Ensure there are enough data points for correlation calculation
            correlation, p_value = pearsonr(
                subset_df["sending_centrality"], subset_df["hearing_centrality"]
            )
        else:
            correlation, p_value = None, None  # Not enough data points

        # Append the results
        results.append(
            {
                "c_value": c_value,
                "delta_value": delta_value,
                "pearson_correlation": correlation,
                "p-value": p_value,
            }
        )

print(results[:5])
# Convert the list of results into a DataFrame
results_df = pd.DataFrame(results)

# Save to CSV
results_df.to_csv("results/analysis/pearson_correlations.csv", index=False)

combined_df.to_csv("results/hearing_and_sending_centralities/hear_send_merged.csv", index=False)

# Letting you know the file is ready and its path
print(
    "CSV file with Pearson correlations and p-values has been saved to: /results/analysis/pearson_correlations.csv"
)

# Specified pairs for scatterplot
pairs_to_plot = [(0.16, 0.78), (0.1, 0.78), (0.08, 0.92), (0.16, 0.98), (0.16, 0.76), (0.08, 0.88)]

# Drawing scatterplots for specified pairs
for c_value, delta_value in pairs_to_plot:
    # Filter for current c_value and delta_value
    subset_df = combined_df[
        (combined_df["c_value"] == c_value) & 
        (combined_df["delta_value"] == delta_value)
    ]
    
    # Plotting
    plt.figure(figsize=(8, 6))
    plt.scatter(subset_df["sending_centrality"], subset_df["hearing_centrality"], alpha=0.6)
    plt.title(f"Sending vs. Hearing Centrality for c={c_value}, delta={delta_value}")
    plt.xlabel("Sending Centrality")
    plt.ylabel("Hearing Centrality")
    plt.grid(True)
    plt.show()
