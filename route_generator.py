import heapq


def dijkstra(map, start, end):
    rows, cols = len(map), len(map[0])
    dist = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    pq = [(0, start)]
    dist[start[0]][start[1]] = 0

    while pq:
        d, (r, c) = heapq.heappop(pq)
        if visited[r][c]:
            continue
        visited[r][c] = True
        if (r, c) == end:
            route = []
            while (r, c) != start:
                route.append((r, c))
                r, c = parent[r][c]
            route.append(start)
            route.reverse()
            return d, route
        # Try to move in 4 directions
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if is_valid_point((nr, nc), rows, cols) and not visited[nr][nc] and not is_obstacle(map, (nr, nc)):
                new_dist = d + 1
                if new_dist < dist[nr][nc]:
                    dist[nr][nc] = new_dist
                    parent[nr][nc] = (r, c)
                    heapq.heappush(pq, (new_dist, (nr, nc)))

    return -1, []  # no path found


def is_valid_point(point, rows, cols):
    """
    Returns True if the point is within the boundaries of the grid
    """
    row, col = point
    return 0 <= row < rows and 0 <= col < cols

def is_obstacle(grid, point):
    """
    Returns True if the point is an obstacle in the grid
    """
    row, col = point
    return grid[row][col] == 2

def getDir(node1, node2):
    if node1[0]<node2[0]:
        return 'right'
    elif node1[0]>node2[0]:
        return 'left'
    elif node1[1]<node2[1]:
        return 'up'
    else:
        return 'down'

def print_path(path):
    pre_node = path[0]
    for i in range(1, len(path)):
        # Ignore the nodes with the same direction
        if path[i-1][0]==path[i][0] and pre_node[0]==path[i][0]:
            continue
        if path[i-1][1]==path[i][1] and pre_node[1]==path[i][1]:
            continue
        print('Move', getDir(pre_node, path[i-1]), 'from ', pre_node, 'to', path[i-1])
        pre_node = path[i-1]
    print('Move', getDir(pre_node, path[len(path)-1]), 'from ', pre_node, 'to', path[len(path)-1])
