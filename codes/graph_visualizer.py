"""
This module provides functionality to visualize a graph structure using NetworkX and Plotly. The graph consists
of nodes representing cities and edges representing the connections between these cities with their respective
weights.

Functions:
    - visualize_graph: Visualizes the graph using a spring layout, displaying city names and weighted connections
     interactively.

Usage:
    The module can be used to create an interactive visual representation of a graph, where nodes are cities
    and edges are weighted connections between them. The visualization includes interactive elements such as
    hover information for both nodes and edges, displayed using Plotly for a scalable and interactive
    visualization environment.

Author: Peyman Kh
Date: 24/May/2024
"""

# Import libraries
import plotly.graph_objects as go
import networkx as nx


def visualize_graph(graph):
    """
    Visualizes a graph structure using NetworkX and Plotly. Nodes represent cities and edges represent
    connections between these cities with their respective weights.
    The visualization includes interactive elements such as hover information for both nodes and edges.
    The graph is displayed using Plotly, providing a scalable and interactive visualization environment.

    Parameters:
        - graph (Graph): A Graph object that contains the cities and their connections.
    """

    # Create a networkx graph from your the object
    G = nx.Graph()

    # Adding nodes
    for node in graph.get_cities():
        G.add_node(node)

    # Adding edges with weights
    for city in graph.get_cities():
        for neighbor, weight in graph.get_neighbors(city).items():
            if (neighbor, city) not in G.edges():
                G.add_edge(city, neighbor, weight=weight)

    # Use a NetworkX layout to position nodes
    pos = nx.spring_layout(G)


    # Extract the positions
    positions = {city: (pos[city][0], pos[city][1]) for city in pos}

    # Create edge traces
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = positions[edge[0]]
        x1, y1 = positions[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    # Create node traces
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        textposition="top center",
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='skyblue',
            size=20,
            line_width=2))

    for node in G.nodes():
        x, y = positions[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([node])

    # Annotations for edges
    edge_annotations = [
        dict(
            x=(positions[edge[0]][0] + positions[edge[1]][0]) / 2,
            y=(positions[edge[0]][1] + positions[edge[1]][1]) / 2,
            xref="x",
            yref="y",
            text=str(G[edge[0]][edge[1]]['weight']),  # edge weight
            showarrow=False,
            font=dict(size=10)
        ) for edge in G.edges()
    ]

    # Layout configuration
    layout = go.Layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=5, l=5, r=5, t=5),
        annotations=edge_annotations,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1100,  # Set the width of the figure
        height=700   # Set the height of the figure
    )

    # Combine traces and layout into a figure
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

    # Show the figure
    fig.show()