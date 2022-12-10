heightmap = []
risk_level = 0

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        heightmap.append(list(map(int, list(line.strip()))))
    for n in range(0, len(heightmap)):
        for m in range(0, len(heightmap[n])):
            candidate = heightmap[n][m]
            above = 10
            below = 10
            left = 10
            right = 10
            if n-1 >= 0:
                above = heightmap[n-1][m]
            if n+1 < len(heightmap):
                below = heightmap[n+1][m]
            if m-1 >= 0:
                left = heightmap[n][m-1]
            if m+1 < len(heightmap[n]):
                right = heightmap[n][m+1]
            if candidate < above and candidate < below and candidate < left and candidate < right:
                risk_level += (candidate + 1)
print(risk_level)