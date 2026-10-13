from common import *
CH = '29-dynamic-programming-intervals-and-advanced-states'
P = lambda p: "(%d, %d)" % (p[0], p[1])

def run(heap, ph):
    """Heap layout: children of cell k are 2k+1 and 2k+2; -1 marks a missing node."""
    n = len(heap)
    def present(k): return k < n and heap[k] != -1
    steps = [{"at": {"node": -1}, "vars": {}, "note": "Start: no subtree is finished yet."}]
    def go(k):
        if not present(k): return (0, 0)
        l = go(2 * k + 1); r = go(2 * k + 2)
        take = heap[k] + l[1] + r[1]
        skip = max(l) + max(r)
        steps.append({"at": {"node": k}, "vars": {"left": P(l), "right": P(r), "take": take, "skip": skip},
                      "note": f"Node {heap[k]} finishes. Take is {heap[k]} + {l[1]} + {r[1]} = {take}. Skip is {max(l)} + {max(r)} = {skip}."})
        return (take, skip)
    root = go(0)
    ans = max(root)
    steps.append({"at": {"node": 0}, "vars": {"take": root[0], "skip": root[1], "answer": ans},
                  "note": f"The answer is the larger of take {root[0]} and skip {root[1]}, which is {ans}."})
    fill(CH, '03-tree-dp.md', block(heap, ["node"], steps), ph)
    return ans

# oracle on the same heap layout
def brute(heap):
    ids = [k for k in range(len(heap)) if heap[k] != -1]
    best = 0
    for m in range(1 << len(ids)):
        s = {ids[i] for i in range(len(ids)) if m >> i & 1}
        if any(k in s and (k - 1) // 2 in s for k in s if k > 0): continue
        best = max(best, sum(heap[k] for k in s))
    return best

t1 = [6, 2, 5, 4, 1, -1, 3]; t2 = [2, 1, 3, -1, 4]
assert brute(t1) == 14 and brute(t2) == 7
assert run(t1, "@@TRACE1@@") == 14
assert run(t2, "@@TRACE2@@") == 7
