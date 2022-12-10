import queue
closing = [')', ']', '}', '>']
scores_map = {"(": 1, "[": 2, "{": 3, "<": 4}
scores_list = []

def parse_chunk(chunk):
    autocomplete_score = 0
    q = queue.LifoQueue()
    for n in range(0, len(chunk)):
        qtop = None
        if q.qsize() > 0:
            qtop = q.get()

        if chunk[n] in closing:
            if (chunk[n] == ')' and qtop == '(') or (chunk[n] == ']' and qtop == '[') or (chunk[n] == '}' and qtop == '{') or (chunk[n] == '>' and qtop == '<'):
                continue
            else:
                # Invalid
                return None
        else:
            if qtop:
                q.put(qtop)
            q.put(chunk[n])
    while q.qsize() > 0:
        top = q.get()
        autocomplete_score = autocomplete_score * 5 + scores_map[top]
    return autocomplete_score

with open('./input.txt') as f:
    lines = f.readlines()
    for line in lines:
        score = parse_chunk(line.strip())
        if score:
            scores_list.append(score)

scores_list.sort()
print(scores_list[int(len(scores_list)/2)])