import sys
import time

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    position = 0
    depth_part1 = 0
    depth_part2 = 0
    aim = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.strip().split()
            if tokens[0] == 'forward':
                x = int(tokens[1])
                position += x
                depth_part2 += (aim * x)
            elif tokens[0] == 'up':
                depth_part1 -= int(tokens[1])
                aim -= int(tokens[1])
            elif tokens[0] == 'down':
                depth_part1 += int(tokens[1])
                aim += int(tokens[1])
            else:
                print('Unknown command')

    print(f"Part 1: {position * depth_part1}\nPart 2: {position * depth_part2}\n(took {(time.time() - start_time)}s)")