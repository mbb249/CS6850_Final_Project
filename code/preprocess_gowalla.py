import pandas as pd
import json
import os

# Define file paths
edges_file = "../gowalla_data/loc-gowalla_edges.txt"
checkins_file = "../gowalla_data/loc-gowalla_totalCheckins.txt"
output_dir = "../gowalla_data"

# Define output file paths
edges_csv_output = os.path.join(output_dir, "gowalla_edges.csv")
checkins_csv_output = os.path.join(output_dir, "gowalla_checkins.csv")
checkins_json_file = os.path.join(output_dir, "gowalla_checkins.json")


# Process the edges file
def process_edges(edges_file, edges_csv_output):
    edges_df = pd.read_csv(edges_file, sep="\t", header=None, names=["User1", "User2"])
    edges_df.to_csv(edges_csv_output, index=False, header=False)  # No headers
    print(f"Edges CSV saved to {edges_csv_output}")


# Process the checkins file
# Process the checkins file
# Process the checkins file
def process_checkins(checkins_file, checkins_csv_output, checkins_json_file):
    checkins_df = pd.read_csv(
        checkins_file,
        sep="\t",
        header=None,
        names=["User", "CheckinTime", "Latitude", "Longitude", "LocationID"],
    )
    # Calculate average latitude, longitude, and location ID
    checkins_agg = (
        checkins_df.groupby("User")
        .agg(
            AvgLatitude=("Latitude", "mean"),
            AvgLongitude=("Longitude", "mean"),
            AvgLocationID=("LocationID", "mean"),
        )
        .reset_index()
    )

    # Round to integers
    checkins_agg["AvgLatitude"] = checkins_agg["AvgLatitude"].round().astype(int)
    checkins_agg["AvgLongitude"] = checkins_agg["AvgLongitude"].round().astype(int)
    checkins_agg["AvgLocationID"] = checkins_agg["AvgLocationID"].round().astype(int)

    # Convert to JSON format, ensuring all values are Python int
    checkins_json_output = {
        int(row["User"]): [
            int(row["AvgLatitude"]),
            int(row["AvgLongitude"]),
            int(row["AvgLocationID"]),
        ]
        for _, row in checkins_agg.iterrows()
    }

    # Save outputs
    checkins_agg.to_csv(checkins_csv_output, index=False, header=False)  # No headers
    with open(checkins_json_file, "w") as f:
        json.dump(checkins_json_output, f, indent=4)

    print(f"Checkins CSV saved to {checkins_csv_output}")
    print(f"Checkins JSON saved to {checkins_json_file}")


# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Run processing
process_edges(edges_file, edges_csv_output)
process_checkins(checkins_file, checkins_csv_output, checkins_json_file)
