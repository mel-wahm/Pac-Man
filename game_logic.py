def neighbor_coordinates(x, y, maze):
    neighbors = []
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
