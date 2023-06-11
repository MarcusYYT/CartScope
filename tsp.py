import math
import sys
import copy
from queue import PriorityQueue
import route_generator

INF = sys.maxsize
rows = 40
columns = 21


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == INF:
                print('%5s' % '@', end='')
            else:
                print('%5s' % matrix[i][j], end='')
        print()


# Calculate the distance between two nodes
def distance(nodes, node1, node2):
    dis = route_generator.dijkstra(nodes, node1, node2)
    return dis[0]


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


# Multiple access points of greedy
def greedy_tsp(worker, nodes, items):
    dist_matrix, access_points, new_items = getAdjacency(worker, items, nodes)
    route = [0]
    length = 0
    pre_shelf = 0
    while len(route) <= len(new_items):
        cur_min = INF
        cur_node = -1
        for i in range(len(access_points)):
            id = math.floor(i/4+1)
            skip = False
            for num in route:
                if num > 0:
                    tmp_id = math.floor((num-1)/4)+1
                    if tmp_id == id:
                        skip = True
                        break
            if skip:
                continue
            dis = dist_matrix[pre_shelf][i+1]
            if dis < cur_min:
                cur_min = dis
                cur_node = i+1
        route.append(cur_node)
        length += cur_min
    length += distance(nodes, access_points[route[len(route) - 1]-1], worker)
    # print(route, length)
    res = []
    for i in range(1, len(route)):
        res.append(access_points[route[i]-1])
    return res, length


def move_multi(matrix, x, y):
    points_x = []
    points_y = []
    if x > 1:
        id = math.floor((x - 1) / 4)
        for i in range(1 + id * 4, 5 + id * 4):
            points_x.append(i)
    else:
        points_x.append(x)
    if y > 1:
        id = math.floor((y - 1) / 4)
        for i in range(1 + id * 4, 5 + id * 4):
            points_y.append(i)
    else:
        points_y.append(y)
    moveMatrix = copy.deepcopy(matrix)
    for i in range(len(points_x)):
        point = points_x[i]
        for j in range(len(matrix)):
            moveMatrix[point][j] = INF
    for i in range(len(points_y)):
        point = points_y[i]
        for j in range(len(matrix)):
            moveMatrix[j][point] = INF
    res = reduce_matrix(moveMatrix)
    return res, moveMatrix


def get_block_min(x, y, matrix):
    res = INF
    for i in range(x, x + 4):
        tmp_min = min(matrix[i][y:y + 4])
        res = min(res, tmp_min)
    return res


def reduce_matrix(matrix):
    res = 0
    n = math.floor((len(matrix) - 1) / 4)
    # Row reduction
    min_val = min(matrix[0])
    if min_val != INF:
        for i in range(len(matrix)):
            if matrix[0][i] != INF:
                matrix[0][i] -= min_val
        res += min_val
    for i in range(n):
        min_val = INF
        # The first column
        tmp_min = INF
        for k in range(4):
            tmp_min = min(tmp_min, matrix[4 * i + k + 1][0])
        min_val = min(tmp_min, min_val)
        # The rest block
        for j in range(n):
            tmp_min = get_block_min(4 * i + 1, 4 * j + 1, matrix)
            min_val = min(tmp_min, min_val)
        if min_val == INF or min_val == 0:
            continue
        for j in range(4):
            for k in range(4 * n + 1):
                if matrix[4 * i + j + 1][k] != INF:
                    matrix[4 * i + j + 1][k] -= min_val
        res += min_val

    min_val = INF
    for i in range(len(matrix)):
        min_val = min(min_val, matrix[i][0])
    if min_val != INF:
        for i in range(len(matrix)):
            if matrix[i][0] != INF:
                matrix[i][0] -= min_val
        res += min_val
    # Column reduction
    for i in range(n):
        min_val = INF
        # The first column
        tmp_min = min(matrix[0][4 * i + 1:4 * i + 5])
        min_val = min(tmp_min, min_val)
        # The rest block
        for j in range(n):
            tmp_min = get_block_min(4 * j + 1, 4 * i + 1, matrix)
            min_val = min(tmp_min, min_val)
        if min_val == INF or min_val == 0:
            continue
        for j in range(4):
            for k in range(4 * n + 1):
                if matrix[k][4 * i + j + 1] != INF:
                    matrix[k][4 * i + j + 1] -= min_val
        res += min_val
    # print(res)
    # print_matrix(matrix)
    return res



dist_arr = [1, 0, -1, 0, 1]
def getAdjacency(start, items, nodes):
    new_items = []
    for i in range(len(items)):
        x = math.floor(items[i][0])
        y = math.floor(items[i][1])
        if (x, y) not in new_items:
            new_items.append((x, y))
    global dist_arr
    n = len(new_items)
    dist_matrix = [[INF] * (4*n + 1) for _ in range(4*n + 1)]
    access_points = []
    for item in new_items:
        x, y = item
        for i in range(4):
            new_x = x + dist_arr[i]
            new_y = y + dist_arr[i + 1]
            if isValid((new_x, new_y), nodes):
                access_points.append((new_x, new_y))
            else:
                access_points.append(None)

    for i in range(len(access_points)):
        if access_points[i] != None:
            dist_start = distance(nodes, start, access_points[i])
            dist_matrix[0][i+1] = dist_start
            dist_matrix[i+1][0] = dist_start

    for i in range(1, 4 * n + 1):
        point1 = access_points[i - 1]
        if point1 == None:
            continue
        for j in range(i + 1, 4 * n + 1):
            point2 = access_points[j - 1]
            if point2 == None:
                continue
            dist = distance(nodes, point1, point2)
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
    # print_matrix(dist_matrix)
    # print(access_points)
    return dist_matrix, access_points, new_items


def branch_tsp(start, nodes, items):
    dist_matrix, access_points, new_items = getAdjacency(start, items, nodes)
    pq = PriorityQueue()
    matrix = copy.deepcopy(dist_matrix)
    # print_matrix(dist_matrix)
    val = reduce_matrix(matrix)
    # print(val)
    # print_matrix(matrix)
    root = Node(val, {
        'matrix': matrix,
        'path': [0],
        'num': 0
    })
    pq.put(root)
    curBound = INF
    curNode  = None
    n = len(new_items)
    while not pq.empty():
        node = pq.get()
        # End condition
        if node.bound > curBound:
            res = []
            for id in curNode.data['path']:
                if id >= 1:
                    res.append(access_points[id-1])
            return res, curBound
        if len(node.data['path']) == n+1:
            if node.bound < curBound:
                curBound = node.bound
                curNode = node
                continue
        for j in range(len(access_points)):
            id = math.floor(j/4)
            skip = False
            for num in node.data['path']:
                if num >= 1:
                    compare_id = math.floor((num-1)/4)
                    if compare_id == id:
                        skip = True
                        break
            if not skip and node.data['matrix'][node.data['num']][j+1] != INF and access_points[j] is not None:
                # Compute new bounds
                newBound, newMatrix = move_multi(node.data['matrix'], node.data['num'], j+1)
                # if node.data['num'] > 0:
                    # print('from', access_points[node.data['num']-1], 'to', access_points[j], node.data['matrix'][node.data['num']][j+1])
                newVal = node.bound + node.data['matrix'][node.data['num']][j+1] + newBound
                newPath = copy.deepcopy(node.data['path'])
                newPath.append(j+1)
                pq.put(Node(newVal, {
                    'matrix': newMatrix,
                    'path': newPath,
                    'num': j+1
                }))
    return None, -1

#
# matrix = [
#     [INF, 2, 3, 4, 5],
#     [2, INF, 3, 4, 5],
#     [3, 3, INF, 4, 5],
#     [4, 4, 4, INF, 5],
#     [5, 5, 5, 5, INF],
# ]
#
# print(reduce_matrix(matrix))
# print_matrix(matrix)

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
    return 0 <= x < len(nodes) and 0 <= y < len(nodes[0]) and nodes[x][y] != 2


class Node(object):
    def __init__(self, bound, data):
        self.bound = bound
        self.data = data

    def __lt__(self, other):
        if self.bound == other.bound:
            return len(self.data['path']) < len(other.data['path'])
        else:
            return self.bound < other.bound
