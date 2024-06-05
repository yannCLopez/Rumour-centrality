# Rumour-centrality

**sending centrality**: Simulate infection of a node x times, and see what percentage of nodes he infects, on average.

**hearing centrality**: Sample a percentage of all simulations for all the nodes. See in what percentage of them the node in question was infected. 

  - **SIR_raw_data**: Generates the raw data for subsequent analysis. Ran 1000 SIR simulations for each node.
  - **data_analysis_hear_centr.py**: Computes the hearing centrality for all nodes and all pairs of c and delta. Took around 5h40 to run. Output is in Data/hear_send_merged.csv 
  - **data_analysis_sending_centr_parallel.py**:  Computes the hearing centrality for all nodes and all pairs of c and delta. Takes over 8 hours to run. The code uses parallel processing to reduce running time. Output is in **Data/hear_send_merged.csv**
  - **data_analysis_one.py**: picks one c and delta and computes hearing and sending centralities for all nodes using all the available data (sample sizes will, therefore, be unbalanced).
  - **pearson_correlation.py**: Calculates the pearson correlation between hearing and sending centralities.
  - **append_sending_centralities.py**: Appended all the separate csv documents created by data_analysis_sending_centr_parallel.py.

**analysis/:**
   - Contains scatterplots for hearing and sending centralities, and a csv file with all the pearson correlations. 
