heightmap = []
working_basin = []
basins = []

def get_neighbors(n,m):
    result = [9, 9, 9, 9] # top, bottom, left, right
    if n-1 >= 0:
        result[0] = (heightmap[n-1][m], (n-1, m))
    else:
        result[0] = (9, None)

    if n+1 < len(heightmap):
        result[1] = (heightmap[n+1][m], (n+1, m))
    else:
        result[1] = (9, None)

    if m-1 >= 0:
        result[2] = (heightmap[n][m-1], (n, m-1))
    else:
        result[2] = (9, None)

    if m+1 < len(heightmap[n]):
        result[3] = (heightmap[n][m+1], (n, m+1))
    else:
        result[3] = (9, None)

    return result

def search_basin(n,m):
    neighbors = get_neighbors(n,m)
    for neighbor in neighbors:
        if neighbor[0] < 9 and neighbor not in working_basin:
            working_basin.append(neighbor)
            search_basin(neighbor[1][0], neighbor[1][1])

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        heightmap.append(list(map(int, list(line.strip()))))
    for n in range(0, len(heightmap)):
        for m in range(0, len(heightmap[n])):
            candidate = heightmap[n][m]
            neighbors = get_neighbors(n, m)
            if candidate < neighbors[0][0] and candidate < neighbors[1][0] and candidate < neighbors[2][0] and candidate < neighbors[3][0]:
                low_point = candidate
                working_basin = [(low_point, (n,m))]
                search_basin(n,m)
                basins.append(len(working_basin))

basins.sort(reverse=True)
result = 1
for n in range(0,3):
    result *= basins[n]
print(result)