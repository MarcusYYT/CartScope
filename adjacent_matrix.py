import numpy as np
from collections import deque

def bfs(matrix, start):
    m, n = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    dist = [[0] * n for _ in range(m)]
    queue = deque([start])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited[start[0]][start[1]] = True

    while queue:
        x, y = queue.popleft()

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n and not visited[nx][ny] and matrix[nx][ny] != 2:
                visited[nx][ny] = True
                dist[nx][ny] = dist[x][y] + 1
                queue.append((nx, ny))

    return dist

def adjacency_matrix(matrix):
    m, n = len(matrix), len(matrix[0])
    adj_matrix = np.zeros((m * n, m * n))

    for i in range(m):
        for j in range(n):
            if matrix[i][j] != 2:
                distances = bfs(matrix, (i, j))

                for x in range(m):
                    for y in range(n):
                        if matrix[x][y] != 2:
                            adj_matrix[i * n + j][x * n + y] = distances[x][y]

    return adj_matrix

if __name__ == "__main__":
    matrix = [
        [0, 0, 0],
        [0, 2, 0],
        [0, 0, 0]
    ]

    adj_matrix = adjacency_matrix(matrix)
    print(adj_matrix)
