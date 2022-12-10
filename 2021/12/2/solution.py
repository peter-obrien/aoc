all_caves  = dict()

class Cave:

    def __init__(self, name: str):
        self.name = name
        self.isbig = name.isupper()
        self.issmall = not self.isbig
        self.isstart = name == 'start'
        self.isend = name == 'end'
        self.neighbors = set()
    
    def __str__(self):
        return self.name
    
    def add_neighbor(self, other_cave):
        self.neighbors.add(other_cave)

class Path:

    def __init__(self):
        self.visited = []

    def __str__(self):
        return '->'.join(list(map(str, self.visited)))
    
    def copy(self):
        my_copy = Path()
        for n in self.visited:
            my_copy.visited.append(n)
        return my_copy
    
    def can_visit(self, c: Cave):
        if c.issmall:
            smalls_visited = dict()
            for n in self.visited:
                if n.issmall:
                    if n in smalls_visited:
                        smalls_visited[n] = 1 + smalls_visited[n]
                    else:
                        smalls_visited[n] = 1
            return c not in smalls_visited or (not c.isstart and 2 not in smalls_visited.values())
        return True

    def visit(self, c: Cave):
        if self.can_visit(c):
            self.visited.append(c)
    
    def is_complete(self):
        return len(self.visited) > 1 and self.visited[len(self.visited)-1].isend

def search_cave(c: Cave, p: Path, all_paths: list):
    p.visit(c)
    if c.isend:
        all_paths.append(p)
    for n in c.neighbors:
        p_copy = p.copy()
        if p_copy.can_visit(n) and not p_copy.is_complete():
            search_cave(n, p_copy, all_paths)


with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        tokens = line.strip().split('-')
        for token in tokens:
            if token not in all_caves:
                new_cave = Cave(token)
                all_caves[token] = new_cave
        all_caves[tokens[0]].add_neighbor(all_caves[tokens[1]])
        all_caves[tokens[1]].add_neighbor(all_caves[tokens[0]])

all_paths = []
search_cave(all_caves['start'], Path(), all_paths)
print('Found ' + str(len(all_paths)) + ' paths')