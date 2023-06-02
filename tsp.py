import math
import sys
import copy
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
    get_shelves(items, nodes, shelves)
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

matrix = [
    [INF, 0, 2, 3, 4, 5],
    [0, INF, 2, 3, 4, 5],
    [2, 2, INF, 3, 4, 5],
    [3, 3, 3, INF, 4, 5],
    [4, 4, 4, 4, INF, 5],
    [5, 5, 5, 5, 5, INF],
]

print(reduce_matrix(matrix))
print_matrix(matrix)

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
