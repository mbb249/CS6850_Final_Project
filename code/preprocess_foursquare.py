import pandas as pd
import json

# File paths
input_csv = "../foursquare_data/data_with_twitter.csv"
output_json = "../foursquare_data/features.json"
input_edges = "../foursquare_data/edges.txt"
output_edges_csv = "../foursquare_data/edges.csv"

# Part 1: Convert CSV to JSON
print("Converting data_with_twitter.csv to features.json...")
df = pd.read_csv(input_csv)

# Convert DataFrame to the desired JSON format
output_data = {str(index): row.tolist() for index, row in df.iterrows()}

# Save to JSON
with open(output_json, "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print(f"Data successfully converted and saved to {output_json}")

# Part 2: Convert edges.txt to edges.csv
print("Converting edges.txt to edges.csv...")
# Read the edges.txt file
edges_df = pd.read_csv(input_edges, sep="\t", header=None, names=["Source", "Target"])

# Save to CSV
edges_df.to_csv(output_edges_csv, index=False)

print(f"Edges successfully converted and saved to {output_edges_csv}")
