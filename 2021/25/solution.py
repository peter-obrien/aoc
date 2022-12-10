import sys
import time

def copy_cucumbers(cucumbers: list):
    result = []
    for row in cucumbers:
        new_row = []
        for c in row:
            new_row.append(c)
        result.append(new_row)
    return result

def move_right(cucumbers: list):
    new_cucumbers = copy_cucumbers(cucumbers)
    for i in range(len(cucumbers)):
        for j in range(len(cucumbers[i])):
            if cucumbers[i][j] == '>' and cucumbers[i][(j+1)%len(cucumbers[i])] == '.':
                new_cucumbers[i][j] = '.'
                new_cucumbers[i][(j+1)%len(cucumbers[i])] = '>'
    return new_cucumbers

def move_down(cucumbers: list):
    new_cucumbers = copy_cucumbers(cucumbers)
    for i in range(len(cucumbers)):
        for j in range(len(cucumbers[i])):
            if cucumbers[i][j] == 'v' and cucumbers[(i+1)%len(cucumbers)][j] == '.':
                new_cucumbers[i][j] = '.'
                new_cucumbers[(i+1)%len(cucumbers)][j] = 'v'
    return new_cucumbers

def print_cucumbers(cucumbers: list):
    for row in cucumbers:
        print(row)

if __name__ == '__main__':
    filename = './sample.txt' if '-s' in sys.argv else './input.txt'
    start_time = time.time()

    cucumbers = []

    with open(filename) as f:
        lines = f.read().splitlines()
        for line in lines:
            cucumbers.append([c for c in line])

    moves = 0
    while True:
        new_cucumbers = move_down(move_right(cucumbers))
        moves += 1

        if cucumbers == new_cucumbers:
            break
        else:
            cucumbers = new_cucumbers

    result = moves
    print(f"Part 1: {result} (took {(time.time() - start_time)}s)")