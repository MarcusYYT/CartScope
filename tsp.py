# Brute force implementation of tsp
import itertools
import route_generator

# Calculate the distance between two cities
def distance(nodes, node1, node2):
    dis = route_generator.dfs_shortest_path(nodes, node1, node2)
    return dis[0]

def tsp_permutation(worker, nodes, cities):
    # Generate all possible permutations of the cities
    permutations = itertools.permutations(cities)

    # Initialize variables for the shortest distance and route
    shortest_distance = float('inf')
    shortest_route = None

    # Iterate over each permutation and calculate its distance
    for route in permutations:
        route_distance = 0
        for i in range(len(route) - 1):
            route_distance += distance(nodes, route[i], route[i + 1])
        # Add the distance from the last city back to the first city
        route_distance += distance(nodes, worker, route[0])
        route_distance += distance(nodes, worker, route[len(route)-1])

        # Update the shortest distance and route if necessary
        if route_distance < shortest_distance:
            shortest_distance = route_distance
            shortest_route = route

    return shortest_route, shortest_distance