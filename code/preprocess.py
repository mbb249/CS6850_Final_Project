import json
import pandas as pd
import networkx as nx
import numpy as np

# File paths
original_features_path = "../git_web_ml/musae_git_features.json"
original_edges_path = "../git_web_ml/musae_git_edges.csv"
modified_features_path = "../modified_data/modified_git_features.json"
modified_edges_path = "../modified_data/modified_git_edges.csv"


# Step 1: Load the data
def load_data():
    with open(original_features_path, "r") as f:
        features = json.load(f)
    edges = pd.read_csv(
        original_edges_path, names=["source", "target"], skiprows=1
    )  # Skip header row
    return features, edges


# Step 2: Convert to graph and keep only the largest connected component
def create_graph(features, edges):
    # Convert node IDs in edges to strings
    edges["source"] = edges["source"].astype(str)
    edges["target"] = edges["target"].astype(str)

    # Create a graph from the string-converted edges
    G = nx.from_pandas_edgelist(edges, source="source", target="target")

    # Extract the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    G_lcc = G.subgraph(largest_cc).copy()

    # Add features to the graph
    for node, feats in features.items():
        if node in G_lcc.nodes:
            G_lcc.nodes[node]["features"] = feats
    return G_lcc


# Step 3: Create feature vectors for ML
def create_feature_vectors(G, edges):
    X = []  # Feature vectors
    y = []  # Labels

    # Positive samples (edges that exist)
    for _, row in edges.iterrows():
        node1, node2 = str(row["source"]), str(row["target"])
        if node1 in G.nodes and node2 in G.nodes:
            # Subtract features of the two nodes
            feature_vector = np.array(G.nodes[node1]["features"]) - np.array(
                G.nodes[node2]["features"]
            )
            X.append(feature_vector)
            y.append(1)

    # Negative samples (random pairs of nodes with no edge)
    all_nodes = list(G.nodes)
    for _ in range(len(edges)):  # Generate as many negatives as positives
        node1, node2 = np.random.choice(all_nodes, 2, replace=False)
        if not G.has_edge(node1, node2):  # Ensure no edge exists
            feature_vector = np.array(G.nodes[node1]["features"]) - np.array(
                G.nodes[node2]["features"]
            )
            X.append(feature_vector)
            y.append(0)

    return np.array(X), np.array(y)


# Main function
if __name__ == "__main__":
    print("Loading data...")
    features, edges = load_data()

    print("Creating graph...")
    G = create_graph(features, edges)

    print("Creating feature vectors for ML...")
    X, y = create_feature_vectors(G, edges)

    print("Feature vectors and labels created!")
    print(f"Feature matrix shape: {X.shape}")
    print(f"Labels shape: {y.shape}")
