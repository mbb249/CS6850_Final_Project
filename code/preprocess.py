import json
import pandas as pd
import networkx as nx
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
import os

# File paths
original_features_path = "../git_web_ml/musae_git_features.json"
original_edges_path = "../git_web_ml/musae_git_edges.csv"
modified_features_path = "../modified_data/modified_git_features.csv"
modified_edges_path = "../modified_data/modified_git_edges.csv"
feature_vectors_path = "../modified_data/feature_vectors.csv"


# Step 1: Load the data
def load_data():
    print("Loading original features and edges...")
    with open(original_features_path, "r") as f:
        features = json.load(f)
    edges = pd.read_csv(
        original_edges_path, names=["source", "target"], skiprows=1
    )  # Skip header row
    print(f"Loaded {len(features)} features and {len(edges)} edges.")
    return features, edges


# Step 2: Convert to graph and keep only the largest connected component
def create_graph(features, edges):
    print("Converting edges to graph...")
    edges["source"] = edges["source"].astype(str)
    edges["target"] = edges["target"].astype(str)

    G = nx.from_pandas_edgelist(edges, source="source", target="target")

    # Extract the largest connected component
    print("Identifying the largest connected component...")
    largest_cc = max(nx.connected_components(G), key=len)
    G_lcc = G.subgraph(largest_cc).copy()

    print(
        f"Largest connected component has {len(G_lcc.nodes)} nodes and {len(G_lcc.edges)} edges."
    )

    # Add features to the graph
    print("Assigning features to nodes...")
    for node, feats in features.items():
        if node in G_lcc.nodes:
            G_lcc.nodes[node]["features"] = feats

    return G_lcc


# Step 3: Standardize feature dimensions using MultiLabelBinarizer and PCA
def standardize_features(G, output_dim=128):
    print("Standardizing features to fixed dimensions...")
    feature_list = [
        set(feats) for feats in nx.get_node_attributes(G, "features").values()
    ]
    mlb = MultiLabelBinarizer()
    binary_features = mlb.fit_transform(feature_list)

    print(f"Initial feature matrix shape: {binary_features.shape}")

    if binary_features.shape[1] > output_dim:
        pca = PCA(n_components=output_dim)
        reduced_features = pca.fit_transform(binary_features)
        print(f"Reduced feature matrix shape after PCA: {reduced_features.shape}")
    else:
        reduced_features = binary_features
        print(f"Feature matrix shape retained as {binary_features.shape}")

    # Assign standardized features back to nodes
    for idx, node in enumerate(G.nodes):
        G.nodes[node]["features"] = reduced_features[idx]

    print("Feature standardization complete.")


# Step 4: Write standardized features and edges to CSV
def write_to_csv(G, features_path, edges_path):
    print(f"Writing standardized features to {features_path}...")
    features = {
        node: {
            "node_id": node,
            **{"dim_" + str(i): val for i, val in enumerate(G.nodes[node]["features"])},
        }
        for node in G.nodes
    }
    features_df = pd.DataFrame(features.values())
    os.makedirs(os.path.dirname(features_path), exist_ok=True)
    features_df.to_csv(features_path, index=False)
    print(f"Features written. Total nodes: {len(features_df)}.")

    print(f"Writing edges to {edges_path}...")
    edges = nx.to_pandas_edgelist(G)
    edges.to_csv(edges_path, index=False)
    print(f"Edges written. Total edges: {len(edges)}.")


# Step 5: Create feature vectors for ML
def create_feature_vectors(G, edges, output_path):
    print("Creating feature vectors for ML tasks...")
    X = []  # Feature vectors
    y = []  # Labels

    # Positive samples (edges that exist)
    total_edges = len(edges)
    print(f"Processing {total_edges} edges for positive samples...")
    for i, (_, row) in enumerate(edges.iterrows()):
        node1, node2 = str(row["source"]), str(row["target"])
        if node1 in G.nodes and node2 in G.nodes:
            # Subtract features of the two nodes
            feature_vector = np.array(G.nodes[node1]["features"]) - np.array(
                G.nodes[node2]["features"]
            )
            X.append(feature_vector)
            y.append(1)

        if i % 1000 == 0:
            print(f"Processed {i}/{total_edges} edges.")

    # Negative samples (random pairs of nodes with no edge)
    all_nodes = list(G.nodes)
    print(f"Generating {total_edges} negative samples...")
    for i in range(total_edges):  # Generate as many negatives as positives
        node1, node2 = np.random.choice(all_nodes, 2, replace=False)
        if not G.has_edge(node1, node2):  # Ensure no edge exists
            feature_vector = np.array(G.nodes[node1]["features"]) - np.array(
                G.nodes[node2]["features"]
            )
            X.append(feature_vector)
            y.append(0)

        if i % 1000 == 0:
            print(f"Generated {i}/{total_edges} negative samples.")

    # Write to CSV
    print(f"Writing feature vectors and labels to {output_path}...")
    feature_vectors_df = pd.DataFrame(X)
    feature_vectors_df["label"] = y
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    feature_vectors_df.to_csv(output_path, index=False)
    print(
        f"Feature vectors and labels written. Total samples: {len(feature_vectors_df)}."
    )


# Main function
if __name__ == "__main__":
    print("Starting the process...")
    features, edges = load_data()

    print("Creating graph...")
    G = create_graph(features, edges)

    print("Standardizing feature dimensions...")
    standardize_features(G, output_dim=128)

    print("Saving standardized features and edges...")
    write_to_csv(G, modified_features_path, modified_edges_path)

    print("Creating feature vectors...")
    create_feature_vectors(G, edges, feature_vectors_path)

    print("Process complete.")
