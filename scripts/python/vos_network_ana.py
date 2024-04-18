import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import sys


period = sys.argv[1]

# Define paths to data files
droot = '../../data/wos'
country_fn = f'map_wos_fMRI_{period}_n1000.txt'
network_fn = f'network_wos_fMRI_{period}_n1000.txt'

# Load country information
country_info = pd.read_table(f'{droot}/{country_fn}')
# Load network links information
network_links = pd.read_table(f'{droot}/{network_fn}')

# Select top 10 countries by 'weight<Citations>'
top_countries = country_info.nlargest(10, 'weight<Citations>')

# Create a full matrix initialized with zeros for all countries
full_n = len(country_info)
full_matrix = np.zeros((full_n, full_n), dtype=int)

# Map of all country IDs to their indices in the full matrix
id_to_full_index = {id_: idx for idx, id_ in enumerate(country_info['id'])}

# Populate the full matrix with link strengths
for _, row in network_links.iterrows():
    source_idx = id_to_full_index.get(row['source'])
    target_idx = id_to_full_index.get(row['target'])
    if source_idx is not None and target_idx is not None:
        full_matrix[source_idx, target_idx] = row['strength']
        full_matrix[target_idx, source_idx] = row['strength']  # Assuming the relationship is bidirectional

# Create a list of indices for the top countries
top_indices = [id_to_full_index[id_] for id_ in top_countries['id']]

# Select rows and columns corresponding to top countries
final_matrix = full_matrix[np.ix_(top_indices, top_indices)]

# Convert the numpy matrix to a pandas DataFrame for better readability
link_matrix = pd.DataFrame(final_matrix, index=top_countries['label'], columns=top_countries['label'])

# Generate a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(link_matrix, annot=True, fmt="d", cmap="YlGnBu", linewidths=.5)
plt.title(f'{period}')
plt.show()

# Create a network graph
G = nx.from_pandas_adjacency(link_matrix)

# Node size proportional to 'weight<Citations>' scaled by a factor (for visibility)
node_size = [5000 * (weight / max(top_countries['weight<Citations>'])) for weight in top_countries['weight<Citations>']]
# Edge width proportional to 'strength'
edge_width = [2 * (G[u][v]['weight'] / max([G[x][y]['weight'] for x, y in G.edges()])) for u, v in G.edges()]

# Draw the network
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color="lightblue", alpha=0.6)
nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.5, edge_color="gray")
nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

plt.title(f'{period}')
plt.axis('off')  # Turn off the axis
plt.show()
