square_length = 1000
grid = []

def print_grid():
    for row in grid:
        print(row)

def is_horizontal(start, end):
    return start[1] == end[1]

def is_vertical(start, end):
    return start[0] == end[0]

def mark_point(current_val):
    return current_val + 1

def mark_line_on_grid(start, end):
    if is_horizontal(start, end):
        if start[0] > end[0]:
            x = start[0]
            while x >= end[0]:
                grid[start[1]][x] = mark_point(grid[start[1]][x])
                x -= 1
        else:
            x = start[0]
            while x <= end[0]:
                grid[start[1]][x] = mark_point(grid[start[1]][x])
                x += 1
    elif is_vertical(start, end):
        if start[1] > end[1]:
            y = start[1]
            while y >= end[1]:
                grid[y][start[0]] = mark_point(grid[y][start[0]])
                y -= 1
        else:
            y = start[1]
            while y <= end[1]:
                grid[y][start[0]] = mark_point(grid[y][start[0]])
                y += 1
    else:
        x = start[0]
        y = start[1]
        while True:
            grid[y][x] = mark_point(grid[y][x])
            if [x,y] == end:
                break
            if start[0] > end[0]:
                x -= 1
            else:
                x +=1
            if start[1] > end[1]:
                y -= 1
            else:
                y += 1


for n in range(0,square_length):
    new_row = []
    for m in range(0, square_length):
        new_row.append(0)
    grid.append(new_row)

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        tokens = line.strip().split(' -> ')
        start = tokens[0].split(',')
        end = tokens[1].split(',')
        mark_line_on_grid([int(start[0]), int(start[1])], [int(end[0]), int(end[1])])

points_of_overlap = 0
for row in grid:
    for val in row:
        if val > 1:
            points_of_overlap += 1
print(points_of_overlap)