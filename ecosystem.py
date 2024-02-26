import networkx as nx
from itertools import combinations
from pyvis.network import Network
import random

# Step 1: Parse the edges file
edges_file = "eco-everglades.edges"

edges = []
with open(edges_file, "r") as file:
    for line in file:
        source, target, weight = line.split()
        edges.append((source, target, float(weight)))

# Step 2: Create a networkx graph
G = nx.Graph()
G.add_weighted_edges_from(edges)

# Step 3: Find 3-node network motifs
def find_network_motifs(graph):
    motifs = []
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        if len(neighbors) >= 2:
            for pair in combinations(neighbors, 2):
                if graph.has_edge(pair[0], pair[1]):
                    motifs.append([node, pair[0], pair[1]])
    return motifs

motifs = find_network_motifs(G)

# Step 4: Use pyvis to visualize the network motifs
net_motifs = Network(height='800px', width='100%', notebook=True)

# Step 5: Add nodes and edges to the Pyvis network for motifs
color_map = {}
for idx, motif in enumerate(motifs):
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))  # Generate a random hex color for each motif
    label = f"Motif {idx+1}"  # Label for the motif
    for node in motif:
        net_motifs.add_node(node, color=color, label=label)  # Add label to each node
        color_map[node] = color
    for i in range(len(motif)):
        for j in range(i+1, len(motif)):
            if G.has_edge(motif[i], motif[j]):
                net_motifs.add_edge(motif[i], motif[j], color=color)

# Step 6: Set Pyvis physics layout for better visualization
net_motifs.force_atlas_2based()

# Step 7: Add legend and title
options_motifs = {
    "nodes": {
        "borderWidth": 2
    },
    "edges": {
        "smooth": {
            "type": "continuous"
        }
    },
    "interaction": {
        "hover": True,
        "navigationButtons": True,
        "keyboard": {
            "enabled": True
        },
        "zoomView": True  # Enable zoom
    },
    "manipulation": {
        "enabled": True
    },
    "physics": {
        "enabled": True,
        "stabilization": {
            "iterations": 1000,
            "updateInterval": 100
        }
    }
}

try:
    net_motifs.set_options(options_motifs)
except Exception as e:
    print(f"An error occurred while setting options: {e}")

# Step 8: Save or display the interactive plot
net_motifs.show('everglades_ecosystem_network_motifs.html')
