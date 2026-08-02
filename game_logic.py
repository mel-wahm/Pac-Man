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


def center_coordinates(x, y, width, height, total_w, total_h, cell_size):
	nx = width / 2 + (x - total_w) * cell_size
	ny = height / 2 - (y - total_h) * cell_size
	return (nx, ny)

