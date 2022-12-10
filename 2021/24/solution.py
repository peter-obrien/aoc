from __future__ import annotations
from functools import lru_cache
import sys
import time

class ALU:
    def __init__(self, instructions: list[tuple]) -> None:
        self.vars = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        self.instruction_sets = []
        counter = -1
        for i in instructions:
            if 'inp' in i:
                counter += 1
                self.instruction_sets.append([])
            self.instruction_sets[counter].append(i)
        self.next_input: int = None
    
    def __str__(self) -> str:
        return f"w={self.vars['w']} | x={self.vars['x']} | y={self.vars['y']} | z={self.vars['z']}"
    
    @lru_cache(maxsize=None)
    def execute_dfs(self, depth: int = 0, z: int = 0, find_max: bool = True):
        search_range = range(9, 0, -1) if find_max else range(1, 10)
        for i in search_range:
            if depth == 0:
                # Clear the cache after each top level number to keep memory consumption semi bounded
                print(f'Searching Depth {depth} - Value {i}. Clearing caches! {time.ctime()}')
                self.execute_dfs.cache_clear()
                self.process_instruction_set.cache_clear()
            z_for_i = self.process_instruction_set(i, z, depth)
            if depth == 13:
                if z_for_i == 0:
                    return str(i)
            else:
                depth_result = self.execute_dfs(depth + 1, z_for_i, find_max)
                if depth_result:
                    return str(i) + depth_result
        return None

    # All instruction sets start with an input into 'w' and 'x' and 'y' are cleared to 0 via mul operations so 'z' is the only carry over
    @lru_cache(maxsize=None)
    def process_instruction_set(self, input: int, z: int, depth: int) -> int:
        self.next_input = input
        self.vars['z'] = z # Unnecessary, but wanted to use the variable
        for i in self.instruction_sets[depth]:
            self.process_instruction(i)
        return int(self.vars['z'])

    def process_instruction(self, ins: tuple):
        if ins[0] == 'inp':
            self.vars[ins[1]] = self.next_input
        elif ins[0] == 'add':
            self.vars[ins[1]] += int(ins[2]) if ins[2].lstrip('-').isdigit() else self.vars[ins[2]]
        elif ins[0] == 'mul':
            self.vars[ins[1]] *= int(ins[2]) if ins[2].lstrip('-').isdigit() else self.vars[ins[2]]
        elif ins[0] == 'div':
            self.vars[ins[1]] //= int(ins[2]) if ins[2].lstrip('-').isdigit() else self.vars[ins[2]]
        elif ins[0] == 'mod':
            self.vars[ins[1]] %= int(ins[2]) if ins[2].lstrip('-').isdigit() else self.vars[ins[2]]
        elif ins[0] == 'eql':
            self.vars[ins[1]] = int(self.vars[ins[1]] == (int(ins[2]) if ins[2].lstrip('-').isdigit() else self.vars[ins[2]]))
        else:
            raise Exception(f"'Unknown instruction: {ins[0]}")

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    instructions: list[tuple] = []

    with open(filename) as f:
        instructions = list(map(tuple, [line.split() for line in f.read().splitlines()]))

    P = ALU(instructions)

    print(f"Part 1: {P.execute_dfs()} (took {(time.time() - start_time)}s)")
    start_time = time.time()

    print(f"Part 2: {P.execute_dfs(find_max=False)} (took {(time.time() - start_time)}s)")