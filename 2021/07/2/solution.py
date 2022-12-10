import statistics

starting_positions = []

def move_to_position(positions, destination):
    result: int = 0
    for pos in positions:
        num_moves = abs(pos - destination)
        for n in range(1, num_moves+1):
            result += n
    return result


with open('./input.txt') as f:
    data = f.readlines()[0]
    starting_positions = list(map(int, data.strip().split(',')))

mean = statistics.mean(starting_positions)
rounded_mean = round(mean)
rounded_mean_result = move_to_position(starting_positions, rounded_mean)
floored_mean = int(mean)
floored_mean_result = move_to_position(starting_positions, floored_mean)
if floored_mean_result < rounded_mean_result:
    print(f"Move to {floored_mean}")
    print(floored_mean_result)
else:
    print(f"Move to {rounded_mean}")
    print(rounded_mean_result)