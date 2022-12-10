import collections
from typing import Counter

def solve(data: str, days: int):
	counts = collections.Counter(map(int, data.strip().split(',')))

	for day in range(days):
		new_counts: Counter[int] = collections.Counter()

		for age, count in counts.items():
			if age:
				new_counts[age - 1] += count
				continue
			new_counts[6] += count
			new_counts[8] += count

		counts = new_counts

	return sum(counts.values())

data = ''
with open('./input.txt') as f:
    data = f.readlines()[0]
print(solve(data, 256))