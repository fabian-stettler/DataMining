import networkx as nx
import plotly.graph_objects as go

from DataVisualization.LeafletGraph.countKeywords import countKeywords
from DataVisualization.LeafletGraph.createEdges import createEdges


def visualize_large_graph_plotly(edges_dict):
    print(edges_dict)
    multiplicatorNodesSize = 0.05

    # Create a graph
    G = nx.Graph()

    # Add edges to the graph
    for keyword, connections in edges_dict.items():
        for connected_keyword, weight in connections.items():
            G.add_edge(keyword, connected_keyword, weight=weight)

    # Position nodes using a layout algorithm suitable for large graphs
    pos = nx.spring_layout(G, k=4, iterations=100)

    # Calculate the sum of weights for each node
    node_weights = {}
    for node in G.nodes():
        total_weight = sum(d['weight'] for u, v, d in G.edges(node, data=True))
        node_weights[node] = total_weight

    # Set node sizes based on the sum of weights, with a smaller overall scale
    node_sizes = [node_weights[node] * multiplicatorNodesSize for node in G.nodes()]  # Adjusted scale for node size
    node_color_values = list(node_weights.values())  # Use the weight sums for color


    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),  # Thinner edges
        hoverinfo='none',
        mode='lines')

    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f'{node} ({node_weights[node]})')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        textposition='top center',
        marker=dict(
            size=node_sizes,  # Apply the degree-based node sizes
            color=node_color_values,  # Use the degree values for color
            colorscale='YlGnBu',
            showscale=True,  # Show the color scale bar
            line_width=2
        ),
        textfont=dict(
            size=10  # Font size for labels
        )
    )

    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Keyword Connections',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        annotations=[dict(
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False))
                    )

    # Adjust hover effect
    fig.update_traces(
        hoverlabel=dict(bgcolor="white"),
        hovertemplate='<b>%{text}</b><extra></extra>'
    )

    # Show the figure in the browser or save it as an HTML file
    fig.show()
    # Save to an HTML file
    fig.write_html("network_graph.html")

# Example usage with createEdges and countKeywords functions
visualize_large_graph_plotly(createEdges(countKeywords()))