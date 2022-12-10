import sys
import time

def calculate_frequencies(lines: list):
    frequencies = dict()
    for line in lines:
        for c, counter in zip(line, range(len(line))):
            freqVal = frequencies.get(counter, (0,0))
            frequencies[counter] = (freqVal[0] + 1, freqVal[1]) if c == '1' else (freqVal[0], freqVal[1] + 1)
    return frequencies

def part1(lines: list):
    freq = calculate_frequencies(lines)
    gamma = ''
    epsilon = ''
    for f in freq:
        gamma += '0' if freq[f][0] > freq[f][1] else '1'
        epsilon += '1' if freq[f][0] > freq[f][1] else '0'
    return int(gamma, 2) * int(epsilon, 2)

def part2(oxygen: list, scrubber: list):
    i = 0
    while len(oxygen) > 1:
        freq = calculate_frequencies(oxygen)
        freqVal = freq[i]
        oxygen = list(filter(lambda val: val[i] == '0' if freqVal[1] > freqVal[0] else val[i] == '1', oxygen))
        i += 1
    i = 0
    while len(scrubber) > 1:
        freq = calculate_frequencies(scrubber)
        freqVal = freq[i]
        scrubber = list(filter(lambda val: val[i] == '0' if freqVal[1] <= freqVal[0] else val[i] == '1', scrubber))
        i += 1
    return int(oxygen[0], 2) * int(scrubber[0], 2)

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    with open(filename) as f:
        lines = f.read().splitlines()

    result = None
    print(f"Part 1: {part1(lines)} (took {(time.time() - start_time)}s)")
    start_time = time.time()
    print(f"Part 2: {part2(lines, lines)} (took {(time.time() - start_time)}s)")