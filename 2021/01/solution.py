import sys
import time

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'

    measure1 = [None, None]
    measure2 = [None]
    measure3 = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            val = int(line.strip())
            measure1.append(val)
            measure2.append(val)
            measure3.append(val)

    start_time = time.time()
    priorDepth = None
    increases = 0
    decreases = 0
    for currentDepth in measure3:
        if priorDepth is None:
            pass
        elif priorDepth < currentDepth:
            increases += 1
        elif currentDepth < priorDepth:
            decreases += 1
        else:
            # Same depth
            continue
        priorDepth = currentDepth
    print(f"Part 1: {increases} increases and {decreases} decreases were encountered (took {(time.time() - start_time)}s)")    

    start_time = time.time()
    increases = 0
    decreases = 0
    priorDepth = None
    for n in range(2, len(measure1)-3+1):
        currentDepth = measure1[n] + measure2[n] + measure3[n]
        if priorDepth is None:
            pass
        elif priorDepth < currentDepth:
            increases += 1
        elif currentDepth < priorDepth:
            decreases += 1
        else:
            # Same depth
            continue
        priorDepth = currentDepth
    print(f"Part 2: {increases} increases and {decreases} decreases were encountered (took {(time.time() - start_time)}s)")