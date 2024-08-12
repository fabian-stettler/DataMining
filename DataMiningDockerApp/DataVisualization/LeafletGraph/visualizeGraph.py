import networkx as nx
import matplotlib.pyplot as plt

from DataVisualization.LeafletGraph.countKeywords import countKeywords
from DataVisualization.LeafletGraph.createEdges import createEdges


def visualize_large_graph(edges_dict):
    # Create a graph
    G = nx.Graph()

    # Add edges to the graph
    for keyword, connections in edges_dict.items():
        for connected_keyword, weight in connections.items():
            G.add_edge(keyword, connected_keyword, weight=weight)

    # Position nodes using a layout algorithm suitable for large graphs
    pos = nx.spring_layout(G, k=3, iterations=100)
    # Set node and edge sizes
    degrees = dict(G.degree())
    node_size = [degrees[node] * 25 for node in G.nodes()]  # Scale the size based on degree


    # Draw the nodes and edges
    plt.figure(figsize=(20, 20))  # Increase the figure size for better visibility
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='lightblue')

    edges = G.edges(data=True)
    edge_widths = 0.7
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=edge_widths, edge_color='gray')

    # Optionally, draw a subset of node labels (e.g., high-degree nodes only)
    high_degree_nodes = [node for node, degree in dict(G.degree()).items() if degree >= 1]
    labels = {node: node for node in high_degree_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_family='sans-serif')

    # Display the graph
    plt.title("Keyword Connections")
    plt.axis('off')
    plt.show()

visualize_large_graph(createEdges(countKeywords()))
