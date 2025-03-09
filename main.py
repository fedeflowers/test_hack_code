import heapq
from collections import deque

def read_input(file_path):
    with open(file_path, 'r') as file:
        C, R, S = map(int, file.readline().split())
        snake_lengths = list(map(int, file.readline().split()))
        grid = []
        for _ in range(R):
            grid.append(file.readline().split())
    return C, R, S, snake_lengths, grid

def wrap_around(x, y, C, R):
    return (x % C, y % R)

def get_neighbors(x, y, grid, C, R):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = wrap_around(x + dx, y + dy, C, R)
        if grid[ny][nx] not in ('*', 'S'):  # Exclude wormholes and occupied cells
            neighbors.append((nx, ny))
    return neighbors

def get_wormhole_pairs(grid):
    wormholes = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == '*':
                if '*' not in wormholes:
                    wormholes['*'] = []
                wormholes['*'].append((x, y))
    return wormholes

def deploy_snake(grid, start_x, start_y, length, C, R, wormholes):
    score = int(grid[start_y][start_x])
    x, y = start_x, start_y
    path = [(x, y)]
    grid[y][x] = 'S'  # Mark as occupied by a snake

    for _ in range(length - 1):
        neighbors = get_neighbors(x, y, grid, C, R)
        if neighbors:
            nx, ny = max(neighbors, key=lambda pos: int(grid[pos[1]][pos[0]]) if grid[pos[1]][pos[0]] not in ('*', 'S') else -float('inf'))
            if grid[ny][nx] == '*':
                if wormholes:
                    nx, ny = wormholes['*'].pop(0)
                    if not wormholes['*']:
                        del wormholes['*']
            if grid[ny][nx] != 'S':  # Ensure no overlap
                x, y = nx, ny
                path.append((x, y))
                score += int(grid[ny][nx])
                grid[ny][nx] = 'S'
            else:
                break
        else:
            break
    return score, path

def greedy_snake_deployment(C, R, S, snake_lengths, grid):
    wormholes = get_wormhole_pairs(grid)
    snake_scores = []
    for snake_length in snake_lengths:
        max_score = -float('inf')
        best_path = []
        for y in range(R):
            for x in range(C):
                if grid[y][x] != 'S' and grid[y][x] != '*':  # Ensure starting point is valid
                    temp_grid = [row.copy() for row in grid]
                    score, path = deploy_snake(temp_grid, x, y, snake_length, C, R, wormholes)
                    if score > max_score:
                        max_score = score
                        best_path = path
        if max_score > 0:
            for px, py in best_path:
                grid[py][px] = 'S'  # Mark the final path on the grid
            snake_scores.append((max_score, best_path))
    return snake_scores

def write_output(output_path, snake_scores):
    with open(output_path, 'w') as file:
        for score, path in snake_scores:
            if path:
                start_x, start_y = path[0]
                file.write(f"{start_x} {start_y} ")
                for i in range(1, len(path)):
                    dx = path[i][0] - path[i-1][0]
                    dy = path[i][1] - path[i-1][1]
                    if dx == 1 or dx == -C + 1:
                        dir = 'R'
                    elif dx == -1 or dx == C - 1:
                        dir = 'L'
                    elif dy == 1 or dy == -R + 1:
                        dir = 'D'
                    elif dy == -1 or dy == R - 1:
                        dir = 'U'
                    file.write(f"{dir} ")
                file.write(f"Score: {score}\n")
            else:
                file.write("\n")

if __name__ == "__main__":
    input_path = "02-swarming-ant.txt"
    output_path = "output.txt"
    C, R, S, snake_lengths, grid = read_input(input_path)
    snake_scores = greedy_snake_deployment(C, R, S, snake_lengths, grid)
    write_output(output_path, snake_scores)