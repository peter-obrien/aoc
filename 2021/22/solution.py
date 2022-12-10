from __future__ import annotations
import sys
import time

class Cuboid:
    def __init__(self, x_range: tuple, y_range: tuple, z_range: tuple) -> None:
        self.x = x_range
        self.y = y_range
        self.z = z_range

    def __str__(self) -> str:
        return f"x:{self.x} y:{self.y} z:{self.z}"

    def cubes(self) -> int:
        return (self.x[1]-self.x[0]+1) * (self.y[1]-self.y[0]+1) * (self.z[1]-self.z[0]+1)

    def list_cubes(self) -> list[tuple]:
        result = []
        for x in range(self.x[0], self.x[1]+1):
            for y in range(self.y[0], self.y[1]+1):
                for z in range(self.z[0], self.z[1]+1):
                    result.append((x,y,z))
        return result

    def intersects(self, __o: Cuboid) -> bool:
        return not (
            __o.x[0] > self.x[1]
            or __o.x[1] < self.x[0]
            or __o.y[0] > self.y[1]
            or __o.y[1] < self.y[0]
            or __o.z[0] > self.z[1]
            or __o.z[1] < self.z[0]
        )

    # Return up to 6 Cuboids based on the intersection
    # Splits self around other
    def split(self, __o: Cuboid) -> list[Cuboid]:
        split_cuboids: list[Cuboid] = []
        # Top
        split_cuboids.append(Cuboid((self.x[0], self.x[1]),
                                    (__o.y[1]+1, self.y[1]),
                                    (self.z[0], self.z[1])))
        # Bottom
        split_cuboids.append(Cuboid((self.x[0], self.x[1]),
                                    (self.y[0], __o.y[0]-1),
                                    (self.z[0], self.z[1])))
        # Left
        split_cuboids.append(Cuboid((self.x[0], __o.x[0]-1),
                                    (max(self.y[0], __o.y[0]), min(self.y[1],__o.y[1])),
                                    (self.z[0], self.z[1])))
        # Right
        split_cuboids.append(Cuboid((__o.x[1]+1, self.x[1]),
                                    (max(self.y[0],__o.y[0]), min(self.y[1],__o.y[1])),
                                    (self.z[0], self.z[1])))
        # Front
        split_cuboids.append(Cuboid((max(self.x[0], __o.x[0]), min(self.x[1], __o.x[1])),
                                    (max(self.y[0],__o.y[0]), min(self.y[1],__o.y[1])),
                                    (self.z[0], __o.z[0]-1)))
        # Back
        split_cuboids.append(Cuboid((max(self.x[0], __o.x[0]), min(self.x[1], __o.x[1])),
                                    (max(self.y[0],__o.y[0]), min(self.y[1],__o.y[1])),
                                    (__o.z[1]+1, self.z[1])))
        # Remove Invalid cubes
        result: list[Cuboid] = []
        for c in split_cuboids:
            if c.cubes() > 0:
                result.append(c)
        return result

def solve(instructions: list[tuple], part1: bool = False):
    cuboids: list[Cuboid] = []
    for i in instructions:
        # Part 1 restricts to -50..50 in x, y & z
        if part1 and max(max(abs(dim[0]) for dim in i[1:]), max(abs(dim[1]) for dim in i[1:])) > 50:
            continue
        new_cuboids = []
        c = Cuboid(i[1], i[2], i[3])
        if i[0]:
            new_cuboids.append(c)
            for k in cuboids:
                if c.intersects(k):
                    new_cuboids.extend(k.split(c))
                else:
                    new_cuboids.append(k)
        else:
            for k in cuboids:
                if c.intersects(k):
                    new_cuboids.extend(k.split(c))
                else:
                    new_cuboids.append(k)
        cuboids = new_cuboids
    return sum([c.cubes() for c in cuboids])

if __name__ == '__main__':

    assert 26 == sum(c.cubes() for c in Cuboid((1,3), (1,3), (1,3)).split(Cuboid((2,2), (2,2), (2,2)))) # Removes middle
    assert 26 == sum(c.cubes() for c in Cuboid((1,3), (1,3), (1,3)).split(Cuboid((3,3), (3,3), (3,3)))) # Removes corner
    assert 18 == sum(c.cubes() for c in Cuboid((1,3), (1,3), (1,3)).split(Cuboid((3,3), (1,3), (1,3)))) # Removes right face
    assert 18 == sum(c.cubes() for c in Cuboid((1,3), (1,3), (1,3)).split(Cuboid((1,3), (1,3), (3,3)))) # Removes front face
    assert 18 == sum(c.cubes() for c in Cuboid((1,3), (1,3), (1,3)).split(Cuboid((1,3), (3,3), (1,3)))) # Removes top face
    assert 19 == sum(c.cubes() for c in Cuboid((11,13), (11,13), (11,13)).split(Cuboid((10,12), (10,12), (10,12)))) # From sample
    assert 19 == sum(c.cubes() for c in Cuboid((10,12), (10,12), (10,12)).split(Cuboid((11,13), (11,13), (11,13)))) # From sample reversed

    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    instructions = []

    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            tokens = line.split(',')
            tokens[0].split('=')[1]
            tuple(map(int, tokens[0].split('=')[1].split('..')))
            instructions.append(('on' in line,
                    tuple(map(int, tokens[0].split('=')[1].split('..'))),
                    tuple(map(int, tokens[1].split('=')[1].split('..'))),
                    tuple(map(int, tokens[2].split('=')[1].split('..')))))

    # Naive solution
    cuboids = dict()
    for i in instructions:
        if max(max(abs(dim[0]) for dim in i[1:]), max(abs(dim[1]) for dim in i[1:])) > 50:
            continue
        c = Cuboid(i[1], i[2], i[3])
        for cube in c.list_cubes():
            if i[0]:
                cuboids[cube] = 1
            else:
                cuboids.pop(cube, None)
    result = len(cuboids)
    print(f"Part 1 (naive): {result} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    result = solve(instructions, True)
    print(f"Part 1: {result} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    result = solve(instructions)
    print(f"Part 2: {result} (took {(time.time() - start_time)}s)")