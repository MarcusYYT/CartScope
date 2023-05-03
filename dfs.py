from collections import deque

def dfs_shortest_path(grid, start, goal):
    """
    Returns the shortest path from start to goal in a 2D grid
    with obstacles, using DFS algorithm.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Check if start and goal are valid points
    if not is_valid_point(start, rows, cols) or not is_valid_point(goal, rows, cols):
        return None, []

    # Define movement directions (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Initialize a visited set to keep track of visited points
    visited = set()

    # Create a deque to keep track of the path and push the start point
    path = deque([(start, 0, [])])

    # Loop until the deque is empty
    while path:
        # Get the current point, its distance from start and its path
        point, distance, path_taken = path.popleft()

        # Check if the current point is the goal
        if point == goal:
            return distance, path_taken + [point]

        # Mark the current point as visited
        visited.add(point)

        # Explore the neighboring points
        for direction in directions:
            next_point = (point[0] + direction[0], point[1] + direction[1])

            # Check if the neighboring point is valid and not visited
            if is_valid_point(next_point, rows, cols) and next_point not in visited and not is_obstacle(grid, next_point):
                # Add the neighboring point to the path with its distance from start and path taken
                path.append((next_point, distance + 1, path_taken + [point]))

    # If the goal is not found, return None and an empty path
    return None, []

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
    return grid[row][col] == '#'