"""
This module provides functions to solve the Traveling Salesman Problem (TSP) using a Genetic Algorithm (GA).
The GA is an evolutionary optimization technique that mimics the process of natural selection.

Functions:
    - initialize_population: Initializes the population with random routes.
    - calculate_fitness: Calculates the fitness scores for each route based on travel distance.
    - selection: Selects parent routes using tournament selection.
    - crossover: Performs ordered crossover to produce new offspring routes.
    - mutate: Applies mutation to the offspring routes.
    - calculate_total_distance: Calculates the total distance of a given route.
    - genetic_algorithm: Executes the genetic algorithm to find an approximate solution to the TSP.

Usage:
    The module can be used to solve the TSP by representing cities and distances in a graph and applying the
    genetic algorithm to find a near-optimal route. The genetic algorithm involves steps such as population
    initialization, fitness calculation, selection, crossover, mutation, and convergence over multiple generations.

Author: Peyman Kh
Date: 25/May/2024
"""

# Import libraries
import random


def initialize_population(pop_size, graph):
    """
    Initializes the population for the Genetic Algorithm.

    Each individual in the population is a random chromosome consisting of a route a salesman can take.

    Parameters:
        - pop_size (int): The size of the population.
        - graph (Graph): An instance of the Graph class containing city connections and distances.

    Returns:
        - list: A list of chromosomes representing individuals in the population.
    """

    city_list = graph.get_cities()
    populations = []

    for _ in range(pop_size):
        chromosome = city_list[:]
        random.shuffle(chromosome)
        populations.append(chromosome)

    return populations


def calculate_fitness(population, graph):
    """
    Calculates the fitness scores for each individual in the population based on the travel distance.
    Lower travel distances should result in higher fitness scores (using the inverse of the distance).

    Parameters:
        - population (list): A list of permutations of city lists representing individuals in the population.
        - graph (Graph): An instance of the Graph class containing city connections and distances.

    Returns:
        - list: A list of fitness scores for each individual, inversely related to their travel distances.
    """

    fitness_scores = []

    for chromosome in population:
        score = 0
        chromosome_length = len(chromosome)
        for j in range(chromosome_length):
            from_city = chromosome[j]
            to_city = chromosome[(j + 1) % chromosome_length]  # wrap around to the start
            score += graph.get_neighbors(from_city)[to_city]
        fitness_scores.append(1 / score if score > 0 else float('inf'))  # Inverse of distance as fitness

    return fitness_scores


def selection(population, fitness_scores, tournament_size=3):
    """
    Selects parents using tournament selection. Tournament selection works by selecting a few individuals randomly from the
    population and then choosing the best out of these to become a parent. This process is repeated until you have selected
    enough parents to produce the next generation.

    Parameters:
        - population (list): The current population of routes.
        - fitness_scores (list): Corresponding fitness scores for the population.
        - tournament_size (int): Number of individuals competing in each tournament.

    Returns:
        - list: The selected individuals who will become parents for the next generation.
    """

    parents = []
    population_size = len(population)

    for _ in range(population_size):
        # Randomly select tournament_size individuals and their fitness scores
        competitors = random.sample(list(zip(population, fitness_scores)), tournament_size)
        # Choose the competitor with the best fitness score (highest, since lower distance means higher fitness)
        winner = max(competitors, key=lambda x: x[1])
        parents.append(winner[0])

    return parents


def crossover(parents):
    """
    Performs ordered(OX) crossover on pairs of parent chromosomes to produce a new population of offspring.
    OX crossover randomly choose a subsequence of cities from one parent. This subsequence will be copied directly to the
    child to preserve a chunk of the route. then it start filling in the rest of the cities from the second parent, skipping
    those already included in the subsequence, and preserving the order in which they appear.

    Parameters:
        - parents (list): The selected parent chromosomes from the population.

    Returns:
        - list: A new population consisting of offspring generated from ordered crossovers.
    """

    offspring = []
    random.shuffle(parents)  # Shuffle to randomize pairing
    num_parents = len(parents)

    for i in range(0, num_parents, 2):
        parent1 = parents[i]
        parent2 = parents[(i + 1) % num_parents]  # Ensure wrap-around for pairing

        # Perform the ordered crossover for parent1 and parent2
        start, end = sorted(random.sample(range(len(parent1)), 2))
        child1 = [None] * len(parent1)
        child2 = [None] * len(parent2)

        # Copy the slice from parent1 to child1 and from parent2 to child2
        child1[start:end] = parent1[start:end]
        child2[start:end] = parent2[start:end]

        # Fill the remaining positions in child1 from parent2
        p2_index = end
        c1_index = end
        while None in child1:
            if parent2[p2_index % len(parent2)] not in child1:
                child1[c1_index % len(child1)] = parent2[p2_index % len(parent2)]
                c1_index += 1
            p2_index += 1

        # Fill the remaining positions in child2 from parent1
        p1_index = end
        c2_index = end
        while None in child2:
            if parent1[p1_index % len(parent1)] not in child2:
                child2[c2_index % len(child2)] = parent1[p1_index % len(parent1)]
                c2_index += 1
            p1_index += 1

        # Add the children to the new population
        offspring.append(child1)
        offspring.append(child2)

    return offspring


def mutate(offspring, mutation_rate=0.01):
    """
    Applies swap mutation to each chromosome in the offspring population. In this method, two cities in the route are randomly
    selected and their positions are swapped.

    Parameters:
        - offspring (list): The population of offspring routes.
        - mutation_rate (float): The probability of mutating a given gene (city in the route).

    Returns:
        - list: The mutated offspring population.
    """

    mutated_offspring = []

    for child in offspring:
        if random.random() < mutation_rate:  # Determine if mutation should occur
            idx1, idx2 = random.sample(range(len(child)), 2)  # Select two indices to swap
            child[idx1], child[idx2] = child[idx2], child[idx1]  # Perform the swap
        mutated_offspring.append(child)

    return mutated_offspring


def calculate_total_distance(route, graph):
    """
    Calculate the total distance of a given route.

    Parameters:
        - route (list): A list of city names representing the route taken.
        - graph (Graph): The graph data structure containing city distances.

    Returns:
        - int: The total distance traveled for the given route.
    """
    total_distance = 0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % len(route)]  # wrap around to the start
        total_distance += graph.get_neighbors(from_city)[to_city]
    return total_distance


def genetic_algorithm(graph, pop_size, generations, mutation_rate=0.01):
    """
    Executes a genetic algorithm to find an approximate solution to the Traveling Salesman Problem.

    Parameters:
        - graph (Graph): An instance of the Graph class containing city connections and distances.
        - pop_size (int): The number of routes (chromosomes) in the population.
        - generations (int): The number of generations to simulate.
        - mutation_rate (float): The probability of mutating a given gene (city in the route).

    Returns:
        - tuple: Best route found and its associated fitness score.
    """

    # Initialize population
    population = initialize_population(pop_size, graph)

    # Calculate initial fitness of the population
    fitness_scores = calculate_fitness(population, graph)

    for _ in range(generations):
        # Selection of parents
        parents = selection(population, fitness_scores)

        # Crossover to create a new generation of offspring
        offspring = crossover(parents)

        # Mutation of the new offspring
        mutated_offspring = mutate(offspring, mutation_rate)

        # Recalculate fitness for the new generation
        fitness_scores = calculate_fitness(mutated_offspring, graph)

        # The new offspring becomes the current population
        population = mutated_offspring

    # Find the best solution at the end of the evolution
    best_index = fitness_scores.index(max(fitness_scores))
    best_route = population[best_index]
    best_fitness = fitness_scores[best_index]

    return best_route, best_fitness