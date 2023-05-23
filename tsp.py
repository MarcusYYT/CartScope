
import itertools
import sys

import route_generator

# Calculate the distance between two nodes
def distance(nodes, node1, node2):
    dis = route_generator.dijkstra(nodes, node1, node2)
    return dis[0]

# # Brute force implementation of tsp
# def tsp_permutation(worker, nodes, items):
#     # Generate all possible permutations of the nodes
#     permutations = itertools.permutations(items)
#
#     # Initialize variables for the shortest distance and route
#     shortest_distance = float('inf')
#     shortest_route = None
#
#     # Iterate over each permutation and calculate its distance
#     for route in permutations:
#         route_distance = 0
#         for i in range(len(route) - 1):
#             route_distance += distance(nodes, route[i], route[i + 1])
#         # Add the distance from the last node back to the first node
#         route_distance += distance(nodes, worker, route[0])
#         route_distance += distance(nodes, worker, route[len(route)-1])
#
#         # Update the shortest distance and route if necessary
#         if route_distance < shortest_distance:
#             shortest_distance = route_distance
#             shortest_route = route
#
#     return shortest_route, shortest_distance
#
# # Simple implementation which only follows the initial order to pick up items
# def tsp_order(worker, nodes, items):
#     route = []
#     dis = 0
#     route += items
#     dis += distance(nodes, worker, items[0])
#     for i in range(len(items)-1):
#         dis += distance(nodes, items[i], items[i+1])
#     dis += distance(nodes, worker, items[len(items)-1])
#     return route, dis

def branch_tsp(worker, nodes, items):
    return None, 0

def greedy_tsp(worker, nodes, items):
    route = []
    dis = 0
    cur_node  = worker
    item_set = {}
    # Add all items into a hashmap
    for i in range(len(items)):
        item_set[items[i]] = True
    # Traverse all items
    for i in range(len(items)):
        cur_dis = sys.maxsize
        cur_item = -1
        # Go through items to find the nearest neighbor
        for j in range(len(items)):
            # Only traverse the items that has not been picked up
            if(item_set[items[j]]):
                new_dis = distance(nodes, cur_node, items[j])
                if(new_dis<cur_dis):
                    cur_item = items[j]
                    cur_dis = new_dis
        route.append(cur_item)
        dis += cur_dis
        del item_set[cur_item]
    return route, dis
