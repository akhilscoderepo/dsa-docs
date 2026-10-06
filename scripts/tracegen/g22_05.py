from common import *
from collections import deque
CH = '22-bfs-variations'; F = '05-resource-dominance.md'

def ch(c):
    return f"{c} charge" if c == 1 else f"{c} charges"

def simulate(n, edges, k, target):
    """Runs the dominance search of the lesson and records one step per dequeued entry."""
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    best = [-1] * n
    best[0] = k
    queue = deque([(0, k, 0)])
    steps, ans = [], -1
    while queue:
        node, rem, dist = queue.popleft()
        if node == target:
            ans = dist
            steps.append({"at": {"cur": node}, "vars": {"best": ",".join(map(str, best)), "queue": "empty" if not queue else " ".join(f"{a}:{b}" for a, b, _ in queue)},
                           "note": f"The search takes room {node} with {ch(rem)} after {dist} move{'' if dist == 1 else 's'}. This is the target, so it returns {dist}."})
            break
        added, dropped = [], []
        for nx, w in adj[node]:
            left = rem - w
            if left < 0:
                dropped.append(f"room {nx}, which costs more than the {ch(rem)} left")
            elif left <= best[nx]:
                dropped.append(f"room {nx} with {ch(left)}, which does not beat best {best[nx]}")
            else:
                best[nx] = left
                queue.append((nx, left, dist + 1))
                added.append(f"room {nx} with {ch(left)}")
        parts = []
        if added: parts.append("It enqueues " + " and ".join(added) + ".")
        if dropped: parts.append("It discards " + " and ".join(dropped) + ".")
        if not parts: parts.append("It has no outgoing edge to try.")
        steps.append({"at": {"cur": node}, "vars": {"best": ",".join(map(str, best)), "queue": "empty" if not queue else " ".join(f"{a}:{b}" for a, b, _ in queue)},
                      "note": f"The search takes room {node} with {ch(rem)} after {dist} move{'' if dist == 1 else 's'}. " + " ".join(parts)})
    return steps, ans

e1 = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,1]]
s, a = simulate(5, e1, 1, 4); assert a == 4
fill(CH, F, block(list(range(5)), ["cur"], s), "@@TRACE1@@")
e2 = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[3,0,0],[1,4,0],[4,5,1]]
s, a = simulate(6, e2, 1, 5); assert a == 5
assert any("does not beat best 1" in x["note"] for x in s)
fill(CH, F, block(list(range(6)), ["cur"], s), "@@TRACE2@@")
