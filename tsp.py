import math
import sys
import copy
from queue import PriorityQueue
import route_generator

INF = sys.maxsize
rows = 40
columns = 21


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
#     for i in range(len(items) - 1):
#         dis += distance(nodes, items[i], items[i + 1])
#     dis += distance(nodes, worker, items[len(items) - 1])
#     return route, dis

# Map the item location to a accessible lane position
def getMappedLoc(location):
    x = math.floor(location[0])
    y = math.floor(location[1])
    if x == 0:
        return (1, y)
    if y == 0:
        return (x, 1)
    if x == rows:
        return (x - 1, y)
    if y == columns:
        return (x, y - 1)
    return (x, y - 1)

# Single access point of branch and bound
def branch_tsp(worker, nodes, items):
    for i in range(len(items)):
        items[i] = getMappedLoc(items[i])
    n = len(items)
    dist_matrix = [[INF] * (n + 1) for _ in range(n + 1)]
    # Construct the distance matrix
    for i in range(n):
        item = items[i]
        dist = distance(nodes, worker, item)
        dist_matrix[0][i + 1] = dist
        dist_matrix[i + 1][0] = dist
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            item1 = items[i - 1]
            item2 = items[j - 1]
            dist = distance(nodes, item1, item2)
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
    route, dis = tsp_branch_bound(dist_matrix)
    # Remove worker location for the generality of the API
    route.remove(0)
    list = []
    # Convert the id of items into specific locations
    for item in route:
        list.append(items[item - 1])
    print(list, dis)
    return list, dis

# Single access point of greedy
def greedy_tsp(worker, nodes, items):
    for i in range(len(items)):
        items[i] = getMappedLoc(items[i])
    route = []
    dis = 0
    cur_node = worker
    item_set = {}
    start_size = sys.getsizeof(item_set)
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
            if items[j] in item_set:
                new_dis = distance(nodes, cur_node, items[j])
                if new_dis < cur_dis:
                    cur_item = items[j]
                    cur_dis = new_dis
        route.append(cur_item)
        dis += cur_dis
        del item_set[cur_item]
    end_size = sys.getsizeof(item_set)
    print(f"Memory usage of current run using Greedy Algorithm: {end_size - start_size}")
    return route, dis


def reduce_matrix(matrix):
    # The value of this reduction
    res = 0
    reduced_matrix = []
    for row in matrix:
        min_val = min(row)
        reduced_row = [INF] * len(row)
        if min_val == INF:
            reduced_matrix.append(reduced_row)
            continue
        for i in range(len(row)):
            if row[i] == INF:
                continue
            reduced_row[i] = row[i] - min_val
        reduced_matrix.append(reduced_row)
        res += min_val
    # Perform column reduction
    num_cols = len(matrix[0])
    col_mins = [INF] * num_cols
    for row in reduced_matrix:
        for j, val in enumerate(row):
            if val < col_mins[j]:
                col_mins[j] = val
    for i in range(len(col_mins)):
        if col_mins[i] == INF:
            continue
        res += col_mins[i]
        for j in range(len(col_mins)):
            reduced_matrix[j][i] -= col_mins[i]
    return res, reduced_matrix


def tsp_branch_bound(dist_matrix):
    n = len(dist_matrix)
    matrix = []
    start_size_matrix = sys.getsizeof(matrix)
    bound, matrix = reduce_matrix(dist_matrix)
    pq = PriorityQueue()
    start_size_queue = sys.getsizeof(pq)
    root = {
        'bound': bound,
        'matrix': matrix,
        'path': [0],
        'num': 0
    }
    pq.put(root)
    while not pq.empty():
        # Do a BFS traverse, this is to get the size of a layer
        size = pq.qsize()
        curBound = INF
        arr = []
        for i in range(size):
            node = pq.get()
            # End condition
            if len(node['path']) == n:
                end_size_matrix = sys.getsizeof(matrix)
                end_size_queue = sys.getsizeof(pq)
                print(
                    f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
                return node['path'], node['bound']
            for j in range(n):
                if j != node['num'] and j not in node['path']:
                    newBound, newMatrix = move(node['matrix'], node['num'], j)
                    # Compute new bounds
                    newVal = node['bound'] + dist_matrix[node['num']][j] + newBound
                    if newVal < curBound:
                        curBound = newVal
                        arr.clear()
                        newPath = copy.deepcopy(node['path'])
                        newPath.append(j)
                        arr.append([j, newMatrix, newPath])
                    elif newBound == curBound:
                        newPath = copy.deepcopy(node['path'])
                        newPath.append(j)
                        arr.append([j, newMatrix, newPath])
        # Add potential nodes into the queue for future traverse
        for i in range(len(arr)):
            pq.put({
                'bound': curBound,
                'matrix': arr[i][1],
                'path': arr[i][2],
                'num': arr[i][0]
            })
    end_size_matrix = sys.getsizeof(matrix)
    end_size_queue = sys.getsizeof(pq)
    print(f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
    return None, -1


# This function is to move from one point to another and do some pre settings
def move(matrix, x, y):
    moveMatrix = list(matrix)
    for i in range(len(matrix)):
        moveMatrix[x][i] = INF
        moveMatrix[i][y] = INF
    moveMatrix[y][x] = INF
    # print(moveMatrix)
    return reduce_matrix(moveMatrix)

# shelf -> access points
shelf_access = {}
# access points -> shelf and id
access_shelf = {}
# list of access points
access_points = []
def multi_branch_tsp(worker, nodes, items):
    id = 1
    for item in items:
        locs = getLoc(item, nodes)
        shelf_access[item] = locs
        for loc in loc:
            access_shelf[loc] = {"shelf": item, "id": id}
            access_points.append(loc)
            id += 1
    n = len(access_points)
    dist_matrix = [[INF] * (n + 1) for _ in range(n + 1)]
    # Construct the distance matrix
    for i in range(n):
        point = access_points[i]
        dist = distance(nodes, worker, point)
        dist_matrix[0][i + 1] = dist
        dist_matrix[i + 1][0] = dist
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            p1 = access_points[i - 1]
            p2 = access_points[j - 1]
            dist = distance(nodes, p1, p2)
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
    route, dis = branch_and_bound_multi(dist_matrix)
    # Remove worker location for the generality of the API
    route.remove(0)
    list = []
    # Convert the id of items into specific locations
    for item in route:
        list.append(access_points[item-1])
    print(list, dis)
    return list, dis

def branch_and_bound_multi(dist_matrix):
    n = len(dist_matrix)
    matrix = []
    start_size_matrix = sys.getsizeof(matrix)
    bound, matrix = reduce_matrix(dist_matrix)
    pq = PriorityQueue()
    start_size_queue = sys.getsizeof(pq)
    root = {
        'bound': bound,
        'matrix': matrix,
        'path': [0],
        'num': 0
    }
    pq.put(root)
    while not pq.empty():
        # Do a BFS traverse, this is to get the size of a layer
        size = pq.qsize()
        curBound = INF
        arr = []
        for i in range(size):
            node = pq.get()
            # End condition
            if len(node['path']) == n:
                end_size_matrix = sys.getsizeof(matrix)
                end_size_queue = sys.getsizeof(pq)
                print(
                    f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
                return node['path'], node['bound']
            for j in range(n):
                if j != node['num'] and j not in node['path']:
                    newBound, newMatrix = move(node['matrix'], node['num'], j)
                    # Compute new bounds
                    newVal = node['bound'] + dist_matrix[node['num']][j] + newBound
                    if newVal < curBound:
                        curBound = newVal
                        arr.clear()
                        newPath = copy.deepcopy(node['path'])
                        newPath.append(j)
                        arr.append([j, newMatrix, newPath])
                    elif newBound == curBound:
                        newPath = copy.deepcopy(node['path'])
                        newPath.append(j)
                        arr.append([j, newMatrix, newPath])
        # Add potential nodes into the queue for future traverse
        for i in range(len(arr)):
            pq.put({
                'bound': curBound,
                'matrix': arr[i][1],
                'path': arr[i][2],
                'num': arr[i][0]
            })
    end_size_matrix = sys.getsizeof(matrix)
    end_size_queue = sys.getsizeof(pq)
    print(f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
    return None, -1

def move_multi(matrix, x, y):
    moveMatrix = list(matrix)
    for i in range(len(matrix)):
        moveMatrix[x][i] = INF
        moveMatrix[i][y] = INF
    moveMatrix[y][x] = INF
    # print(moveMatrix)
    return reduce_matrix(moveMatrix)

dir_matrix = [1, 0, -1, 0, 1]
def getLoc(location, nodes):
    locs = []
    x, y = location
    for i in range(4):
        new_x = x + dir_matrix[i]
        new_y = y + dir_matrix[i + 1]
        if isValid([new_x, new_y], nodes) and nodes[new_x][new_y] != 2:
            locs.append([new_x, new_y])
    return locs

def isValid(point, nodes):
    x, y = point
    return 0 <= x < len(nodes)  and 0 <= y < len(nodes[0])
