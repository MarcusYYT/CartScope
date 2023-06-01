import math
import sys
import copy
from queue import PriorityQueue, Queue
import route_generator
INF = sys.maxsize
rows = 40
columns = 21


# Calculate the distance between two nodes
def distance(nodes, node1, node2):
    dis = route_generator.dijkstra(nodes, node1, node2)
    return dis[0]


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
    return list, dis

# Single access point of greedy
def greedy_tsp(worker, nodes, items):
    for i in range(len(items)):
        items[i] = getMappedLoc(items[i])
    route = []
    dis = 0
    cur_node = worker
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
            if items[j] in item_set:
                new_dis = distance(nodes, cur_node, items[j])
                if new_dis < cur_dis:
                    cur_item = items[j]
                    cur_dis = new_dis
        route.append(cur_item)
        dis += cur_dis
        del item_set[cur_item]
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
            if reduced_matrix[j][i] == INF:
                continue
            reduced_matrix[j][i] -= col_mins[i]
    return res, reduced_matrix


def tsp_branch_bound(dist_matrix):
    n = len(dist_matrix)
    matrix = []
    bound, matrix = reduce_matrix(dist_matrix)
    pq = PriorityQueue()
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
    return None, -1


# This function is to move from one point to another and do some pre settings
def move(matrix, x, y):
    moveMatrix = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        moveMatrix[x][i] = INF
        moveMatrix[i][y] = INF
    moveMatrix[y][x] = INF
    return reduce_matrix(moveMatrix)

# shelf -> access points
shelf_access = {}
# access points -> shelf and id
access_shelf = {}
# list of access points
access_points = []

start = ()


def get_shelves(items, nodes, shelves):
    for item in items:
        x = math.floor(item[0])
        y = math.floor(item[1])
        shelf = (x, y)
        if shelf not in shelves:
            shelves.append(shelf)


def multi_branch_tsp(worker, nodes, items):
    global start
    id = 1
    start = worker
    shelves = []
    get_shelves(items, nodes, shelves)
    for shelf in shelves:
        locs = getLoc(shelf, nodes)
        shelf_access[shelf] = locs
        for loc in locs:
            access_shelf[loc] = {"shelf": shelf, "id": id}
            access_points.append(loc)
            id += 1
    access_shelf[worker] = {'shelf': worker, "id": 0}
    shelf_access[worker] = [worker]
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
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in dist_matrix]))
    route, dis = branch_and_bound_multi(dist_matrix, worker, len(shelves)+1)
    # Remove worker location for the generality of the API
    route.remove(worker)
    return route, dis


def get_dis(dist_matrix, path):
    dis = 0
    for i in range(1, len(path)):
        pre = access_shelf[path[i-1]]['id']
        cur = access_shelf[path[i]]['id']
        dis += dist_matrix[pre][cur]
    start = access_shelf[path[0]]['id']
    end = access_shelf[path[len(path)-1]]['id']
    dis += dist_matrix[start][end]
    return dis


def branch_and_bound_multi(dist_matrix, worker, n):
    matrix = []
    start_size_matrix = sys.getsizeof(matrix)
    bound, matrix = reduce_matrix(dist_matrix)
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    pq = Queue()
    start_size_queue = sys.getsizeof(pq)
    root = {
        'bound': bound,
        'matrix': matrix,
        'path': [worker],
        'num': 0,
        'visited': {worker}
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
                # end_size_matrix = sys.getsizeof(matrix)
                # end_size_queue = sys.getsizeof(pq)
                # print(
                #     f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
                final_distance = get_dis(dist_matrix, node['path'])
                while not pq.empty():
                    tmp_node = pq.get()
                    tmp_dis = get_dis(dist_matrix, tmp_node['path'])
                    if tmp_dis < final_distance:
                        node = tmp_node
                        final_distance = tmp_dis
                # print(size)
                return node['path'], final_distance
            tmp_bound = INF
            tmp_offset = 0
            tmp_list = []
            pre_shelf = None
            pre_base = 0
            for j in range(1, len(dist_matrix)):
                if j == node['num']:
                    continue
                shelf = get_shelf(j)
                # print(shelf)
                if shelf in node['visited']:
                    continue
                newBound, newMatrix = move_multi(node['matrix'], node['num'], j)
                # Compute new bounds
                newVal = node['bound'] + dist_matrix[node['num']][j] + newBound
                print(newBound, access_points[j-1], dist_matrix[node['num']][j])
                newPath = copy.deepcopy(node['path'])
                newPath.append(access_points[j - 1])
                newVisit = copy.deepcopy(node['visited'])
                newVisit.add(shelf)
                if shelf == pre_shelf:
                    dis = calculate_dis(dist_matrix, j, node['visited'])
                    # print(dis, pre_base)
                    offset = dis - pre_base
                    if newVal+offset < tmp_bound:
                        tmp_bound = newVal+offset
                        tmp_offset = offset
                        tmp_list.clear()
                        tmp_list.append([j, newMatrix, newPath, newVisit])
                    elif newVal+offset == tmp_bound:
                        if offset >= tmp_offset:
                            if offset > tmp_offset:
                                tmp_list.clear()
                                tmp_offset = offset
                            tmp_list.append([j, newMatrix, newPath, newVisit])
                else:
                    # print(shelf)
                    pre_shelf = shelf
                    pre_base = calculate_dis(dist_matrix, j, node['visited'])
                    if tmp_bound != INF:
                        pre_bound = tmp_bound-tmp_offset
                        if pre_bound < curBound:
                            curBound = pre_bound
                            arr.clear()
                            for item in tmp_list:
                                arr.append(item)
                        elif newBound == curBound:
                            for item in tmp_list:
                                arr.append(item)
                    tmp_bound = newVal
                    tmp_offset = 0
                    tmp_list.clear()
                    tmp_list.append([j, newMatrix, newPath, newVisit])
            pre_bound = tmp_bound - tmp_offset
            if pre_bound < curBound:
                curBound = pre_bound
                arr.clear()
                for item in tmp_list:
                    arr.append(item)
            elif newBound == curBound:
                for item in tmp_list:
                    arr.append(item)
        # Add potential nodes into the queue for future traverse
        # print(len(arr))
        for i in range(len(arr)):
            pq.put({
                'bound': curBound,
                'matrix': arr[i][1],
                'path': arr[i][2],
                'num': arr[i][0],
                'visited': arr[i][3]
            })
    end_size_matrix = sys.getsizeof(matrix)
    end_size_queue = sys.getsizeof(pq)
    print(f"Memory usage of current run using Batch&Bound Algorithm: {end_size_queue + end_size_matrix - start_size_matrix - start_size_queue}")
    return None, -1

def get_shelf(num):
    if num == 0:
        return start
    access_point = access_points[num-1]
    return access_shelf[access_point]['shelf']

def move_multi(matrix, x, y):
    shelf_x = get_shelf(x)
    shelf_y = get_shelf(y)

    points_x = shelf_access[shelf_x]
    points_y = shelf_access[shelf_y]
    moveMatrix = copy.deepcopy(matrix)
    for i in range(len(points_x)):
        point = points_x[i]
        x_id = access_shelf[point]['id']
        # print(x_id)
        for j in range(len(matrix)):
            moveMatrix[x_id][j] = INF
    for i in range(len(points_y)):
        point = points_y[i]
        y_id = access_shelf[point]['id']
        for j in range(len(matrix)):
            moveMatrix[j][y_id] = INF
    # print(moveMatrix)
    if shelf_y == (20, 10):
        print(x, y)
        print(points_x)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in moveMatrix]))
    return reduce_matrix(moveMatrix)

dir_matrix = [1, 0, -1, 0, 1]
def getLoc(location, nodes):
    locs = []
    x, y = location
    x = math.floor(x)
    y = math.floor(y)
    for i in range(4):
        new_x = x + dir_matrix[i]
        new_y = y + dir_matrix[i + 1]
        if isValid([new_x, new_y], nodes) and nodes[new_x][new_y] != 2:
            locs.append((new_x, new_y))
    return locs

def isValid(point, nodes):
    x, y = point
    return 0 <= x < len(nodes)  and 0 <= y < len(nodes[0])

def calculate_dis(dist_matrix, num, visited):
    shelf = get_shelf(num)
    pre = None
    res = 0
    cnt = 0
    sum = 0
    for i in range(1, len(dist_matrix)):
        tmp = get_shelf(i)
        if tmp == shelf or tmp in visited:
            continue
        if tmp == pre:
           sum += dist_matrix[num][i]
           cnt += 1
        else:
            if cnt != 0:
                res += sum/cnt
            sum = dist_matrix[num][i]
            cnt = 1
    if cnt!= 0:
        res += sum/cnt
    # print(res, num)
    return res