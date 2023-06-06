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
    shelves = []
    # get_shelves(items, nodes, shelves)
    pre = worker
    route = []
    length = 0
    cur_shelf = None
    while len(shelves) != 0:
        min_dis = INF
        access_point = None
        for shelf in shelves:
            locs = getLoc(shelf, nodes)
            for loc in locs:
                tmp_dis = distance(nodes, loc, pre)
                if tmp_dis < min_dis:
                    min_dis = tmp_dis
                    access_point = loc
                    cur_shelf = shelf
        length += min_dis
        route.append(access_point)
        shelves.remove(cur_shelf)
    length += distance(nodes, route[len(route)-1], worker)
    return route, length

def move_multi(matrix, x, y):
    points_x = []
    points_y = []
    if x>1:
        id = (x-2)/4
        for i in range(2+id*4, 6+id*4):
            points_x.append(i)
    else:
        points_x.append(x)
    if y>1:
        id = (x - 2) / 4
        for i in range(2 + id * 4, 6 + id * 4):
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
    return reduce_matrix(moveMatrix)


def get_block_min(x, y, matrix):
    res = INF
    for i in range(x, x+4):
        tmp_min = min(matrix[i][y:y+4])
        res = min(res, tmp_min)
    return res


def reduce_matrix(matrix):
    res = 0
    n = int((len(matrix) - 2)/4)
    # Row reduction
    for i in range(n):
        min_val = INF
        # The first two column
        for j in range(2):
            tmp_min = INF
            for k in range(4):
                tmp_min = min(tmp_min, matrix[4*i+k+2][j])
            min_val = min(tmp_min, min_val)
        # The rest block
        for j in range(n):
            tmp_min = get_block_min(4*i+2, 4*j+2, matrix)
            min_val = min(tmp_min, min_val)
        if min_val == INF or min_val == 0:
            continue
        for j in range(4):
            for k in range(4*n+2):
                if matrix[4*i+j+2][k] != INF:
                    matrix[4*i+j+2][k] -= min_val
        res += min_val

    # Column reduction
    for i in range(n):
        min_val = INF
        # The first two column
        for j in range(2):
            tmp_min = min(matrix[j][4*i+2:4*i+6])
            min_val = min(tmp_min, min_val)
        # The rest block
        for j in range(n):
            tmp_min = get_block_min(4*j+2, 4*i+2, matrix)
            min_val = min(tmp_min, min_val)
        if min_val == INF or min_val == 0:
            continue
        for j in range(4):
            for k in range(4*n+2):
                if matrix[k][4*i+j+2] != INF:
                    matrix[k][4*i+j+2] -= min_val
        res += min_val
    return res


def getAdjacency(start, end, items, nodes):
    n = len(items)
    dist_matrix = [[INF] * (n + 2) for _ in range(n + 2)]
    dist_matrix[0][1] = 0
    dist_matrix[1][0] = 0
    for i in range(n):
        item = items[i]
        dist_start = distance(nodes, start, item)
        dist_end = distance(nodes, end, item)
        dist_matrix[0][i+2] = dist_start
        dist_matrix[i+2][0] = dist_start
        dist_matrix[1][i + 2] = dist_end
        dist_matrix[i + 2][1] = dist_end
    for i in range(2, n + 2):
        for j in range(i + 1, n + 2):
            item1 = items[i - 2]
            item2 = items[j - 2]
            dist = distance(nodes, item1, item2)
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
    return dist_matrix


def branch_tsp(start, nodes, items, end):
    dist_matrix = getAdjacency(start, end, items, nodes)
    pq = PriorityQueue()
    matrix = copy.deepcopy(dist_matrix)
    val = reduce_matrix(matrix)
    root = Node(val, {
        'matrix': matrix,
        'path': [0],
        'num': 0
    })
    pq.put(root)

    curBound = INF
    curNode = None
    n = len(dist_matrix)
    while not pq.empty():
        size = pq.qsize()
        for i in range(size):
            node = pq.get()
            # End condition
            if node.bound>=curBound:
                return curNode['path'], curBound
            if len(node['path']) == n:
                if node.bound < curBound:
                    curBound = node.bound
                    curNode = node
                    continue
            for j in range(n):
                if j != node['num'] and j not in node['path']:
                    newBound, newMatrix = move_multi(node['matrix'], node['num'], j)
                    # Compute new bounds
                    newVal = node['bound'] + node['matrix'][node['num']][j] + newBound
                    newPath = copy.deepcopy(node['path'])
                    newPath.append(j)
                    pq.put(Node(newVal, {
                        'matrix': newMatrix,
                        'path': newPath,
                        'num': j
                    }))
    return None, -1
# matrix = [
#     [INF, 0, 2, 3, 4, 5],
#     [0, INF, 2, 3, 4, 5],
#     [2, 2, INF, 3, 4, 5],
#     [3, 3, 3, INF, 4, 5],
#     [4, 4, 4, 4, INF, 5],
#     [5, 5, 5, 5, 5, INF],
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
    return 0 <= x < len(nodes)  and 0 <= y < len(nodes[0])

class Node(object):
    def __init__(self, bound, data):
        self.bound = bound
        self.data = data

    def __lt__(self, other):
        if self.bound == other.bound:
            return len(self.data['path']) > len(other.data['path'])
