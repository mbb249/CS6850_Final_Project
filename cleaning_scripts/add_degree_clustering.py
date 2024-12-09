import pandas as pd
from itertools import combinations
from collections import defaultdict

# Step 1: Read and Merge Venue and Check-in Data
# ----------------------------------------------

# Read venue coordinates
venues = pd.read_csv("venue_coordinates.csv")

# Read check-in locations
checkin_locations = pd.read_csv("first_checkin_locations.csv")

# Merge on 'Venue ID' using inner join and select relevant columns
df = pd.merge(venues, checkin_locations, how='inner', on='Venue ID')[['User ID', 'Latitude', 'Longitude']]

# Display the first 20 rows
print("First 20 rows of merged user locations:")
print(df.head(20))

# Save to 'user_locations.csv'
df.to_csv("user_locations.csv", index=False)

# Step 2: Read Friendship Data and Combine Edges
# ----------------------------------------------

def read_friendship_file(filepath):
    """Reads a friendship file and returns a list of tuples representing edges."""
    edges = []
    with open(filepath, 'r') as file:
        for line in file:
            # Split the line by whitespace and convert to integers
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    user1 = int(parts[0])
                    user2 = int(parts[1])
                    # Avoid self-friendship
                    if user1 != user2:
                        edges.append((user1, user2))
                except ValueError:
                    # Skip lines that don't have exactly two integers
                    continue
    return edges

# Paths to friendship datasets
friendship_old_path = "dataset_WWW_friendship_old.txt"
friendship_new_path = "dataset_WWW_friendship_new.txt"

# Read and combine edges from both datasets
edges_old = read_friendship_file(friendship_old_path)
edges_new = read_friendship_file(friendship_new_path)

# Combine edges ensuring no duplicates
all_edges_set = set(edges_old) | set(edges_new)
all_edges = list(all_edges_set)

print(f"Total number of edges from old dataset: {len(edges_old)}")
print(f"Total number of edges from new dataset: {len(edges_new)}")
print(f"Total unique combined edges: {len(all_edges)}")

# Save combined edges to a new file
combined_edges_path = "edges.txt"
with open(combined_edges_path, 'w') as file:
    for u, v in all_edges:
        file.write(f"{u}\t{v}\n")  # Using tab as a delimiter

print(f"Combined edges saved to '{combined_edges_path}'.")

# Step 3: Build the Adjacency List
# --------------------------------

# Initialize a default dictionary to store adjacency sets
adjacency = defaultdict(set)

# Populate the adjacency list ensuring bidirectional friendships
for u, v in all_edges:
    adjacency[u].add(v)
    adjacency[v].add(u)

print(f"Total number of unique users: {len(adjacency)}")

# Step 4: Compute Degree for Each User
# ------------------------------------

# Compute degree for each user
degree_dict = {user: len(friends) for user, friends in adjacency.items()}

# Convert to pandas Series for easy merging
degree_series = pd.Series(degree_dict, name='Degree')

# Step 5: Compute Clustering Coefficient for Each User
# -----------------------------------------------------

def compute_clustering_coefficient(user, friends, adjacency):
    """Computes the clustering coefficient for a given user."""
    k = len(friends)
    if k < 2:
        return 0.0  # Defined as 0 when there are fewer than two friends

    # Count the number of actual connections between friends
    actual_connections = 0
    # Iterate over all unique pairs of friends
    for friend1, friend2 in combinations(friends, 2):
        if friend2 in adjacency[friend1]:
            actual_connections += 1

    # Total possible connections between friends
    possible_connections = k * (k - 1) / 2

    # Clustering coefficient
    return actual_connections / possible_connections

# Compute clustering coefficient for each user
clustering_dict = {}
for user, friends in adjacency.items():
    clustering = compute_clustering_coefficient(user, friends, adjacency)
    clustering_dict[user] = clustering

# Convert to pandas Series for easy merging
clustering_series = pd.Series(clustering_dict, name='ClusteringCoefficient')

# Step 6: Merge Metrics with User Locations
# ------------------------------------------

# Read the user locations
user_locations = pd.read_csv("user_locations.csv")  # Assumes columns: 'User ID', 'Latitude', 'Longitude'

# Set 'User ID' as the index for merging
user_locations.set_index('User ID', inplace=True)

# Add Degree
user_locations = user_locations.join(degree_series, how='left')

# Add Clustering Coefficient
user_locations = user_locations.join(clustering_series, how='left')

# Reset index to have 'User ID' as a column again
user_locations.reset_index(inplace=True)

# Fill NaN values with 0 (users with no connections in friendship datasets)
user_locations['Degree'] = user_locations['Degree'].fillna(0).astype(int)
user_locations['ClusteringCoefficient'] = user_locations['ClusteringCoefficient'].fillna(0.0)

# Display the first few rows to verify
print("First 20 rows of user locations with metrics:")
print(user_locations.head(20))

# Step 7: Save the Enhanced Data
# -------------------------------

# Save to a new CSV file
enhanced_csv_path = "user_locations_with_metrics.csv"
user_locations.to_csv(enhanced_csv_path, index=False)

print(f"Enhanced user locations saved to '{enhanced_csv_path}'.")
