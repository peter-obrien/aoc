import sys
import time

class Probe:

    def __init__(self, velocity_x: int, velocity_y: int) -> None:
        self.positions = set()
        self.positions.add((0,0))
        self.current_position = [0,0]
        self.original_velocity = (velocity_x, velocity_y)
        self.velocity = [velocity_x,  velocity_y]

    def __str__(self) -> str:
        return str(self.original_velocity)

    def move(self):
        self.current_position[0] = self.current_position[0] + self.velocity[0]
        self.current_position[1] = self.current_position[1] + self.velocity[1]
        self.positions.add(tuple(self.current_position))
        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        self.velocity[1] -= 1

    # Return -1 if before target, 0 if in target and 1 if past target
    def compare_to_target(self, x: tuple, y: tuple):
        if self.current_position[0] > x[1] or self.current_position[1] < y[0]:
            return 1
        else:
            return 0 if (self.current_position[0] >= x[0] and self.current_position[0] <= x[1]) and (self.current_position[1] >= y[0] and self.current_position[1] <= y[1]) else -1

    def max_height(self):
        return max(pos[1] for pos in self.positions)

    def print_path(self, target_x: tuple, target_y: tuple):
        if self.compare_to_target(target_x, target_y) > 0:
            print('Currently unable to print probes that miss the target.')
            return
        lower_grid = []
        for _ in range(abs(target_y[0])+1):
            lower_grid.append(['.' for _ in range(target_x[1]+1)])
        lower_grid[0][0] = 'S'
        for y in range(abs(target_y[1]), abs(target_y[0])+1):
            for x in range(target_x[0], target_x[1]+1):
                lower_grid[y][x] = 'T'
        # Plot points where y <= 0
        for point in self.positions:
            if point[1] <= 0 and point[0] != 0:
                lower_grid[abs(point[1])][point[0]] = '#'
        # Add water above y=0
        grid = []
        for _ in range(max([pos[1] for pos in self.positions])):
            grid.append(['.' for _ in range(target_x[1]+1)])
        # Plot points where y > 0
        for point in self.positions:
            if point[1] > 0:
                grid[point[1]-1][point[0]] = '#'
        grid.reverse()
        grid.extend(lower_grid)
        for row in grid:
            print(''.join(row))

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    with open(filename) as f:
        tokens = f.readline()[13:].split(', ')
        target_x = tuple(map(int, tokens[0].split('=')[1].split('..')))
        target_y = tuple(map(int, tokens[1].split('=')[1].split('..')))

    best = Probe(0,0)
    candidates = set()
    for x in range(target_x[1], -1, -1):
        for y in range(abs(target_y[0])):
            P = Probe(x, y)
            while P.compare_to_target(target_x, target_y) < 0:
                P.move()
            if P.compare_to_target(target_x, target_y) == 0 and P.max_height() > best.max_height():
                best = P
                candidates.add(P.original_velocity)
    print(f"Part 1: {best.max_height()} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    candidates = set()
    for x in range(target_x[1], -1, -1):
        # We can use the y value from Part 1 since we know any larger Y values will not reach the target zone
        for y in range(target_y[0], best.original_velocity[1]+1):
            P = Probe(x, y)
            while P.compare_to_target(target_x, target_y) < 0:
                P.move()
            if P.compare_to_target(target_x, target_y) == 0:
                candidates.add(P.original_velocity)
    print(f"Part 2: {len(candidates)} (took {(time.time() - start_time)}s)")