import sys
import time

def grid_to_str(grid: list):
    return '\n'.join([''.join(row) for row in grid])

def fold(grid: list, axis: str, val: int):
    new_grid = []
    if axis == 'y':
        for r in range(0, val):
            new_grid.append(grid[r])
        for y in range(val+1, len(grid)):
            for x in range(0, len(grid[y])):
                if grid[y][x] == '@':
                    new_grid[val - (y - val)][x] = '@'
    else:
        values_in_fold = []
        for row in grid:
            values_in_fold.append(row[val])
            new_row = []
            for x in range(0, val):
                new_row.append(row[x])
            for x in range(val+1, len(row)):
                if row[x] == '@':
                    new_row[val - (x - val)] = '@'
            new_grid.append(new_row)
    return new_grid

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    folds = []
    dots = []
    max_x = 0
    max_y = 0

    with open(filename) as f:
        for line in f.read().splitlines():
            if 'fold' in line:
                tokens = line[11:].split('=')
                folds.append((tokens[0], int(tokens[1])))
            elif ',' in line:
                dots.append(list(map(int, line.split(','))))

    for dot in dots:
        max_x = max(max_x, dot[0])
        max_y = max(max_y, dot[1])

    grid = [[' ' for _ in range(max_x+1)] for _ in range(max_y+1)]

    for dot in dots:
        grid[dot[1]][dot[0]] = '@'

    dot_count_after_one_fold = sum([sum([1 if d == '@' else 0 for d in row]) for row in fold(grid, folds[0][0], folds[0][1])])
    print(f"Part 1: {dot_count_after_one_fold} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    for f in folds:
        grid = fold(grid, f[0], f[1])

    print(f"Part 2: (took {(time.time() - start_time)}s)\n{grid_to_str(grid)}")