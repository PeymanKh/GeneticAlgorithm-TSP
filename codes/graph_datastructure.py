"""
This module provides a graph data structure where each city is represented as a vertex (node) and the distances
between cities are represented as weighted edges. The main components are:

1. **Vertex Class**: Represents a vertex in the graph. Each vertex has a name and can have multiple edges to
                     other vertices, each with an optional weight.
2. **Graph Class**: Represents the entire graph. Supports adding cities (vertices) and establishing weighted
                    edges between them, which represent connections in the network.

Classes:
    - Vertex: A class to represent a single vertex in the graph.
    - Graph: A class to represent the entire graph, consisting of multiple vertices and edges.

Usage:
    The module can be used to create a graph, add cities, establish connections (edges) between cities, and
    retrieve information about the graph such as the list of cities and the neighbors of a specific city.

Author: Peyman Kh
Date: 24/May/2024
"""

# Import Libraries
from typing import Dict


class Vertex:
    """
    Represents a vertex in a graph. Each vertex has a name and can have multiple edges to other vertices.
    Each edge is stored with an optional weight.
    """

    def __init__(self, name: str):
        """
        Initialize a vertex with a given name.

        Parameters:
            - name (str): The name of the vertex.

        Returns:
            - None
        """
        self.name = name
        self.edges: Dict[str, int] = {}

    def add_edge(self, new_vertex: str, weight=0):
        """
        Add an edge from this vertex to another vertex with an optional weight (default is 0).

        Parameters:
            - new_vertex (str): The name of the vertex to connect to.
            - weight (int, optional): The weight of the edge. Defaults to 0.

        Returns:
            - None
        """
        self.edges[new_vertex] = weight

    def get_edges(self):
        """
        Return all edges from this vertex.

        Returns:
            - Dict[str, int]: A dictionary of connected vertices and their edge weights.
        """
        return self.edges

    def __str__(self):
        """Return a string representation of the vertex."""
        return f"Vertex({self.name})"

    def __repr__(self):
        """Return a string representation of the vertex (for debugging)."""
        return self.__str__()


class Graph:
    """
    Represents a graph data structure with cities as vertices. Supports adding cities and
    establishing weighted edges between them to represent connections in a network.
    """

    def __init__(self):
        """
        Initialize an empty graph.

        Returns:
            - None
        """
        self.cities: Dict[str, Vertex] = {}

    def add_city(self, name: str):
        """
        Add a city to the graph by creating a new Vertex instance.

        Parameters:
            - name (str): The name of the city to add.

        Returns:
            - None
        """
        self.cities[name] = Vertex(name)

    def add_neighbor(self, from_city: str, to_city: str, weight=0):
        """
        Add a weighted edge between two cities.

        Parameters:
            - from_city (str): The name of the starting city.
            - to_city (str): The name of the destination city.
            - weight (int, optional): The weight of the edge. Defaults to 0.

        Returns:
            - None
        """
        if from_city not in self.cities:
            self.add_city(from_city)
        if to_city not in self.cities:
            self.add_city(to_city)
        self.cities[from_city].add_edge(to_city, weight)

    def get_cities(self):
        """
        Return a list of all cities in the graph.

        Parameters:
            - None

        Returns:
            - List[str]: A list of city names.
        """
        return list(self.cities.keys())

    def get_neighbors(self, city_name: str):
        """
        Return all neighbors for a given city.

        Parameters:
            - city_name (str): The name of the city whose neighbors are to be retrieved.

        Returns:
            - Dict[str, int]: A dictionary of neighboring cities and their edge weights.

        Raises:
            - ValueError: If the city is not found in the graph.
        """
        if city_name not in self.cities:
            raise ValueError(f"City '{city_name}' not found in the graph.")
        return self.cities[city_name].get_edges()

    def __str__(self):
        """Return a string representation of the graph."""
        return f"Graph with cities: {list(self.cities.keys())}"