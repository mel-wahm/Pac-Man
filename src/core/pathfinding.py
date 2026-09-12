from collections import deque


def neighbor_coordinates(
    x: int, y: int, maze: list[list[int]]
) -> list[tuple[int, int]]:
    """Get valid accessible adjacent cells in the maze grid.

    Args:
        x: Current horizontal cell coordinate.
        y: Current vertical cell coordinate.
        maze: 2D grid matrix containing bitmask wall information.

    Returns:
        List of accessible (x, y) neighbor coordinates.
    """
    neighbors: list[tuple[int, int]] = []
    c = len(maze[0]) - 1
    r = len(maze) - 1
    if x and not maze[y][x] & 8:
        neighbors.append((x - 1, y))
    if y and not maze[y][x] & 1:
        neighbors.append((x, y - 1))
    if x < c and not maze[y][x] & 2:
        neighbors.append((x + 1, y))
    if y < r and not maze[y][x] & 4:
        neighbors.append((x, y + 1))
    return neighbors


def shortest_path(
    start: tuple[int, int], end: tuple[int, int], maze: list[list[int]]
) -> dict[tuple[int, int], tuple[int, int]]:
    """Compute shortest path tree between two points using BFS.

    Args:
        start: Starting (x, y) coordinates.
        end: Target (x, y) coordinates.
        maze: 2D grid matrix containing bitmask wall information.

    Returns:
        Mapping of reached nodes to their predecessor in the path.
    """
    if start == end:
        return {}
    px, py = start
    ex, ey = end
    final_path: dict[tuple[int, int], tuple[int, int]] = {}
    queue: deque[tuple[int, int]] = deque()
    queue.append((px, py))
    visited: set[tuple[int, int]] = set()
    visited.add((px, py))
    while queue:
        cx, cy = queue.popleft()
        for nx, ny in neighbor_coordinates(cx, cy, maze):
            if (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            queue.append((nx, ny))
            final_path[(nx, ny)] = (cx, cy)
            if (nx, ny) == (ex, ey):
                return final_path
    return {}


def construct_path(
    end: tuple[int, int],
    start: tuple[int, int],
    final: dict[tuple[int, int], tuple[int, int]],
) -> list[tuple[int, int]]:
    """Reconstruct coordinate sequence from predecessor map.

    Args:
        end: Destination (x, y) coordinates.
        start: Origin (x, y) coordinates.
        final: Predecessor mapping produced by shortest_path.

    Returns:
        Ordered list of coordinates representing the path from start to end.
    """
    ex, ey = end
    if not final:
        return [start]
    final_path: list[tuple[int, int]] = []
    final_path.append(end)
    while (ex, ey) != start:
        ex, ey = final[(ex, ey)]
        final_path.append((ex, ey))
    return final_path[::-1]
