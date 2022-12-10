days = 80
fish = []

with open('./input.txt') as f:
    tokens = f.readlines()[0].strip().split(',')
    for token in tokens:
        fish.append(int(token))

for day in range(1, days+1):
    # print(day)
    new_fish = []
    for f in fish:
        if f == 0:
            new_fish.append(6) # Original fish
            new_fish.append(8) # Baby fish
        else:
            new_fish.append(f-1)
    fish = new_fish

print(len(fish))