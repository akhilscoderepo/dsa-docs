from common import *
from collections import deque
CH = '22-bfs-variations'
F = '06-bfs-state-modeling.md'

# trace 1: walled spread on a 3x3 hall, cells flattened in row order
g = [[2, 1, 1], [1, 3, 1], [0, 1, 1]]
h, w = 3, 3
sym = {0: ".", 1: "F", 2: "R", 3: "#"}
cells = [sym[g[i // w][i % w]] for i in range(h * w)]
left = sum(row.count(1) for row in g)
dist = {}
q = deque()
for i in range(h * w):
    if g[i // w][i % w] == 2:
        dist[i] = 0; q.append(i)
steps = []
minute_end = 0
while q:
    cur = q.popleft()
    r, c = divmod(cur, w)
    found = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        a, b = r + dr, c + dc
        n = a * w + b
        if 0 <= a < h and 0 <= b < w and g[a][b] == 1 and n not in dist:
            dist[n] = dist[cur] + 1; q.append(n); left -= 1; found.append(n)
    minute_end = max(minute_end, dist[cur] + (1 if found else 0))
    if found:
        note = f"Cell {cur} was rotten at minute {dist[cur]}. It rots cell(s) {', '.join(map(str, found))} at minute {dist[cur] + 1}, so left is now {left}."
    else:
        note = f"Cell {cur} was rotten at minute {dist[cur]}, and every side neighbour is a wall, an empty bench, outside the hall or already rotten, so nothing new is found."
    steps.append({"at": {"cell": cur}, "vars": {"minute": dist[cur], "left": left}, "note": note})
assert left == 0 and max(dist.values()) == 5 and len(steps) == 7
fill(CH, F, block(cells, ["cell"], steps), "@@TRACE1@@")

# trace 2: count shortest ladders rat -> pen
reg = ["pat", "pet", "pot", "rot", "ret", "ren", "pen", "ten"]
begin, end = "rat", "pen"
words = [begin] + reg
known = set(reg)
ways = {begin: 1}; final = {begin}; layer = [begin]; lay = 0; steps = []
while layer and end not in ways:
    fresh = {}
    for s in layer:
        added = []
        for i in range(3):
            for x in "abcdefghijklmnopqrstuvwxyz":
                n = s[:i] + x + s[i + 1:]
                if n in known and n not in final:
                    fresh[n] = fresh.get(n, 0) + ways[s]; added.append(n)
        if added:
            note = f"{s} holds {ways[s]} way(s) and passes them to " + ", ".join(f"{n} (now {fresh[n]})" for n in added) + "."
        else:
            note = f"{s} holds {ways[s]} way(s), and none of its one-letter neighbours is new."
        steps.append({"at": {"w": words.index(s)}, "vars": {"layer": lay, "ways": ways[s]}, "note": note})
    final |= set(fresh); ways.update(fresh); layer = list(fresh); lay += 1
assert ways[end] == 3 and len(steps) == 7, (ways, len(steps))
fill(CH, F, block(words, ["w"], steps), "@@TRACE2@@")
