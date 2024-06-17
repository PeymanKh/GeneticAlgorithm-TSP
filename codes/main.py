"""
This module initializes the graph with cities and their mutual distances, collects user input for genetic
algorithm parameters, runs the genetic algorithm to find the optimal route, visualizes the graph, and
outputs the results.

Functions:
    - main: Executes the TSP solution process by performing the following steps:
            - Initializes a graph with cities and their mutual distances.
            - Requests user input for genetic algorithm parameters: population size, number of generations, and
              mutation rate.
            - Executes the genetic algorithm to find the most efficient route minimizing travel distance.
            - Visualizes the graph with cities and routes using NetworkX and Plotly.
            - Outputs the best route found, its total travel distance, and fitness score.

Usage:
    This module serves as the entry point for solving the TSP using a genetic algorithm. It requires user input
    for the genetic algorithm parameters and provides a visual and textual representation of the results.

"""

# Import libraries
from graph_datastructure import Graph
from graph_visualizer import visualize_graph
from genetic_algorithm import genetic_algorithm, calculate_total_distance


def main():
    """
    Main function to run the Traveling Salesman Problem (TSP) solution using a genetic algorithm.

    This function performs the following steps:
        - Initializes a graph with cities and their mutual distances.
        - Requests user input for genetic algorithm parameters: population size, number of generations,
          and mutation rate.
        - Executes the genetic algorithm to find the most efficient route minimizing travel distance.
        - Visualizes the graph with cities and routes using NetworkX and Plotly.
        - Outputs the best route found, its total travel distance, and fitness score.

    The user is prompted to input the population size, generations, and mutation rate, with guidance
    on expected values. In case of invalid inputs, the function will terminate with an error message.
    """

    # Create Graph object
    graph = Graph()

    # Adding cities and their mutual distances
    city_distances = {
        'Brighton': {'Brighton': 0, 'Bristol': 172, 'Cambridge': 145, 'Glasgow': 607, 'Liverpool': 329, 'London': 72,
                     'Manchester': 312, 'Oxford': 120},
        'Bristol': {'Brighton': 172, 'Bristol': 0, 'Cambridge': 192, 'Glasgow': 494, 'Liverpool': 209, 'London': 158,
                    'Manchester': 216, 'Oxford': 92},
        'Cambridge': {'Brighton': 145, 'Bristol': 192, 'Cambridge': 0, 'Glasgow': 490, 'Liverpool': 237, 'London': 75,
                      'Manchester': 205, 'Oxford': 100},
        'Glasgow': {'Brighton': 607, 'Bristol': 494, 'Cambridge': 490, 'Glasgow': 0, 'Liverpool': 286, 'London': 545,
                    'Manchester': 296, 'Oxford': 489},
        'Liverpool': {'Brighton': 329, 'Bristol': 209, 'Cambridge': 237, 'Glasgow': 286, 'Liverpool': 0, 'London': 421,
                      'Manchester': 49, 'Oxford': 208},
        'London': {'Brighton': 72, 'Bristol': 158, 'Cambridge': 75, 'Glasgow': 545, 'Liverpool': 421, 'London': 0,
                   'Manchester': 249, 'Oxford': 75},
        'Manchester': {'Brighton': 312, 'Bristol': 216, 'Cambridge': 205, 'Glasgow': 296, 'Liverpool': 49,
                       'London': 249, 'Manchester': 9, 'Oxford': 194},
        'Oxford': {'Brighton': 120, 'Bristol': 92, 'Cambridge': 100, 'Glasgow': 489, 'Liverpool': 208, 'London': 75,
                   'Manchester': 194, 'Oxford': 0}
    }

    # Add cities and their neighbors to the graph
    for city, neighbors in city_distances.items():
        for neighbor, distance in neighbors.items():
            graph.add_neighbor(city, neighbor, distance)

    # Get user inputs for the genetic algorithm parameters
    try:
        pop_size = int(input("Enter the population size(numbers above 500 take more time to execute): "))
        generations = int(input("Enter the number of generations: "))
        mutation_rate = float(input("Enter the mutation rate (e.g., 0.01 for 1%): "))
    except ValueError:
        print("Invalid input. Please enter numerical values.")
        return

    # Execute the genetic algorithm
    best_route, best_fitness = genetic_algorithm(graph, pop_size, generations, mutation_rate)
    best_route_distance = calculate_total_distance(best_route, graph)

    # Visualize the graph data structure
    visualize_graph(graph)

    # Print the best route and its fitness score
    print("Best Route Found:")
    print(" -> ".join(best_route))
    print(f"Total Distance Traveled: {best_route_distance} km")
    print(f"Fitness Score: {best_fitness}")


if __name__ == "__main__":
    main()