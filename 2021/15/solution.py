from collections import defaultdict, deque
import sys
import time
import heapq

class MyGraph:
    def __init__(self, matrix):
        self.matrix = matrix
    
    def __str__(self):
        str_row = []
        for row in self.matrix:
            str_r = ''
            for v in row:
                str_r += str(v)
            str_row.append(str_r)
        return '\n'.join(str_row)

    def get_tuple(self, x, y):
        return (self.matrix[y][x], x, y)

    def get_neighbors(self, x, y):
        if y - 1 >= 0:
            yield self.get_tuple(x, y-1)
        if y + 1 < len(self.matrix):
            yield self.get_tuple(x, y+1)
        if x - 1 >= 0:
            yield self.get_tuple(x-1, y)
        if x + 1 < len(self.matrix[0]):
            yield self.get_tuple(x+1, y)

def reconstruct_path(cameFrom: dict, current: tuple):
    total_path = deque()
    total_path.append(current)
    while current in cameFrom:
        current = cameFrom[current]
        total_path.appendleft(current)
    return total_path

def distance(a:tuple, b:tuple):
    # return abs(a[1] - b[1]) + abs(a[2] - b[2])
    return 1

# https://en.wikipedia.org/wiki/A*_search_algorithm
def astar(G: MyGraph, start: tuple, goal: tuple, h):
    # The set of discovered nodes that may need to be (re-)expanded.
    openSetList = []
    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start to n currently known.
    cameFrom = dict()
    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = defaultdict(lambda: sys.maxsize)
    gScore[start] = 0
    # For node n, fScore[n] := gScore[n] + h(n). fScore[n] represents our current best guess as to how short a path from start to finish can be if it goes through n.
    fScore = defaultdict(lambda: sys.maxsize)
    fScore[start] = h(start, goal)
    heapq.heappush(openSetList, (fScore[start], start))

    while len(openSetList) > 0:
        # current := the node in openSet having the lowest fScore[] value
        current = heapq.heappop(openSetList)[1]
        if current == goal:
            return reconstruct_path(cameFrom, current)
        for neighbor in G.get_neighbors(current[1], current[2]):
            tentative_gScore = gScore[current] + neighbor[0]
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = tentative_gScore + h(neighbor, goal)
                if neighbor not in openSetList:
                    heapq.heappush(openSetList, (fScore[neighbor], neighbor))
    raise Exception('End not reached')

def expand(val, inc):
    return val + inc if val + inc < 10 else (val + inc) % 9

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    grid = []
    with open(filename) as f:
        grid = [list(map(int, line.strip())) for line in f.readlines()]

    G = MyGraph(grid)
    path = astar(G, G.get_tuple(0,0), G.get_tuple(len(G.matrix[0])-1, len(G.matrix)-1), distance)
    total_risk = sum([n[0] for n in list(path)[1:]])
    print(f"Part 1: {total_risk} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    expanded_grid = []
    for row in grid:
        expanded_row = []
        for n in range(5):
            expanded_row.extend([expand(i, n) for i in row])
        expanded_grid.append(expanded_row)
    extra_rows = []
    for n in range(1,5):
        for row in expanded_grid:
            extra_rows.append([expand(i, n) for i in row])
    for row in extra_rows:
        expanded_grid.append(row)

    G = MyGraph(expanded_grid)
    path = astar(G, G.get_tuple(0,0), G.get_tuple(len(G.matrix[0])-1, len(G.matrix)-1), distance)
    # Don't count the starting position
    total_risk = sum([n[0] for n in list(path)[1:]])
    print(f"Part 2: {total_risk} (took {(time.time() - start_time)}s)")