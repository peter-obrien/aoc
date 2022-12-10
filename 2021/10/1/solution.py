import queue
scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
syntax_error_score = 0

def parse_chunk(chunk):
    q = queue.LifoQueue()
    for n in range(0, len(chunk)):
        qtop = None
        if q.qsize() > 0:
            qtop = q.get()

        if chunk[n] in scores:
            if (chunk[n] == ')' and qtop == '(') or (chunk[n] == ']' and qtop == '[') or (chunk[n] == '}' and qtop == '{') or (chunk[n] == '>' and qtop == '<'):
                continue
            else:
                return scores[chunk[n]]
        else:
            if qtop:
                q.put(qtop)
            q.put(chunk[n])
    return 0

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        syntax_error_score += parse_chunk(line.strip())

print(syntax_error_score)