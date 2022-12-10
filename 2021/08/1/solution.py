result = 0
with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        signal_pattern = line.strip()
        output = signal_pattern.split(' | ')[1]
        signals = output.split()
        for signal in signals:
            if len(signal) in [2, 3, 4, 7]:
                result += 1
print(result)