# Octopus = [energy: int, flashed: bool]
octopuses = []

def step():
    flashes = 0
    # Increment all octopuses
    for row in octopuses:
        for octopus in row:
            octopus[0] += 1
    # Register flashes
    for n in range(0,10):
        for m in range(0,10):
            flash(n, m)
    # Reset flashed octopuses
    for row in octopuses:
        for octopus in row:
            if octopus[1]:
                flashes += 1
                octopus[0] = 0
                octopus[1] = False
    return flashes

def increment_neighbors(n,m):
    # Top
    if n - 1 >= 0:
        octopuses[n-1][m][0] += 1
        flash(n-1, m)
        # Top left
        if m - 1 >= 0:
            octopuses[n-1][m-1][0] += 1
            flash(n-1, m-1)
        # Top right
        if m + 1 < 10:
            octopuses[n-1][m+1][0] += 1
            flash(n-1, m+1)
    # Left
    if m - 1 >= 0:
        octopuses[n][m-1][0] += 1
        flash(n, m-1)
    # Right
    if m + 1 < 10:
        octopuses[n][m+1][0] += 1
        flash(n, m+1)
    # Bottom
    if n + 1 < 10:
        octopuses[n+1][m][0] += 1
        flash(n+1, m)
        # Bottom left
        if m - 1 >= 0:
            octopuses[n+1][m-1][0] += 1
            flash(n+1, m-1)
        # Bottom right
        if m + 1 < 10:
            octopuses[n+1][m+1][0] += 1
            flash(n+1, m+1)

def flash(n,m):
    if octopuses[n][m][0] > 9 and not octopuses[n][m][1]:
        octopuses[n][m][1] = True
        increment_neighbors(n,m)


with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        row = []
        for octopus in line.strip():
            row.append([int(octopus), False])
        octopuses.append(row)

step_num = 0
while True:
    step_num += 1
    flashes = step()
    if flashes == 100:
        break
print(step_num)