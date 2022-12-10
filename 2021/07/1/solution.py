import statistics

starting_positions = []

def move_to_position(positions, destination):
    result: int = 0
    for pos in positions:
        result += abs(pos - destination)
    return result


with open('./input.txt') as f:
    data = f.readlines()[0]
    starting_positions = list(map(int, data.strip().split(',')))
print(move_to_position(starting_positions, statistics.median(starting_positions)))