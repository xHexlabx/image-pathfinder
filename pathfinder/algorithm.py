# pathfinder/algorithm.py

from collections import deque

def find_path_bfs(grid, start, end):
    """Finds a path from start to end using Breadth-First Search (BFS)."""
    rows, cols = grid.shape
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        y, x = path[-1]

        if (y, x) == end:
            return path  # Path found

        # Explore neighbors (Up, Down, Left, Right)
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < rows and 0 <= nx < cols and grid[ny, nx] == 0 and (ny, nx) not in visited:
                visited.add((ny, nx))
                new_path = list(path)
                new_path.append((ny, nx))
                queue.append(new_path)
    return None  # No path found