import sys
import time

def solve(polymer: str, instructions: dict, iterations: int):
    frequencies = dict()
    least = sys.maxsize
    most = 0

    for i in range(len(polymer)):
        pair = polymer[i:i+2]
        # Track the frequency of each individual letter
        frequencies[polymer[i]] = frequencies.get(polymer[i], 0) + 1
        if len(pair) == 2: # Account for final character
            # Track the frequency of each pair
            frequencies[pair] = frequencies.get(pair, 0) + 1

    for i in range(iterations):
        new_frequencies = dict()
        for k in frequencies:
            if len(k) == 1:
                new_frequencies[k] = new_frequencies.get(k, 0) + frequencies[k]
            else:
                freq = frequencies[k]
                left = k[0] + instructions[k]
                right = instructions[k] + k[1]
                new_frequencies[left] = new_frequencies.get(left, 0) + freq
                new_frequencies[right] = new_frequencies.get(right, 0) + freq
                new_frequencies[instructions[k]] = new_frequencies.get(instructions[k], 0) + freq
        frequencies = new_frequencies

    for k in frequencies:
        if len(k) == 1:
            v = frequencies[k]
            most = max(most, v)
            least = min(least, v)

    return most-least

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    polymer = None
    instructions = dict()

    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            if len(line) == 0:
                continue
            if '->' in line:
                tokens = line.strip().split(' -> ')
                instructions[tokens[0]] = tokens[1]
            else:
                polymer = line.strip()

    print(f"Part 1: {solve(polymer, instructions, 10)} (took {(time.time() - start_time)}s)")
    start_time = time.time()
    print(f"Part 2: {solve(polymer, instructions, 40)} (took {(time.time() - start_time)}s)")