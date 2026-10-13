import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
A = [5, 2, 7, 1, 4, 3, 6, 8]

def build_trace(a):
    n = len(a)
    tree = [0] * (4 * n)
    steps = []
    def go(k, lo, hi):
        if lo == hi:
            tree[k] = a[lo]
            steps.append({"at": {"node": k}, "vars": {"lo": lo, "hi": hi, "stored": tree[k]},
                          "note": f"Leaf {k} owns position {lo} and stores {tree[k]}."})
            return
        m = (lo + hi) // 2
        go(2 * k, lo, m)
        go(2 * k + 1, m + 1, hi)
        tree[k] = tree[2 * k] + tree[2 * k + 1]
        steps.append({"at": {"node": k}, "vars": {"lo": lo, "hi": hi, "stored": tree[k]},
                      "note": f"Node {k} owns positions {lo} to {hi}. It adds {tree[2*k]} and {tree[2*k+1]} from its children and stores {tree[k]}."})
    go(1, 0, n - 1)
    assert tree[1] == sum(a)
    return tree[:2 * n], steps

def query_trace(tree, n, l, r):
    steps = []
    total = [0]
    def go(k, lo, hi):
        if r < lo or hi < l:
            steps.append({"at": {"node": k}, "vars": {"lo": lo, "hi": hi, "added": 0, "total": total[0]},
                          "note": f"Node {k} owns positions {lo} to {hi}, outside the query, so it returns the identity 0."})
            return
        if l <= lo and hi <= r:
            total[0] += tree[k]
            steps.append({"at": {"node": k}, "vars": {"lo": lo, "hi": hi, "added": tree[k], "total": total[0]},
                          "note": f"Node {k} owns positions {lo} to {hi}, fully inside the query, so it returns its stored {tree[k]}. The running total is {total[0]}."})
            return
        steps.append({"at": {"node": k}, "vars": {"lo": lo, "hi": hi, "added": 0, "total": total[0]},
                      "note": f"Node {k} owns positions {lo} to {hi} and overlaps the query in part, so it visits both children."})
        m = (lo + hi) // 2
        go(2 * k, lo, m)
        go(2 * k + 1, m + 1, hi)
    go(1, 0, n - 1)
    return total[0], steps

tree, bsteps = build_trace(A)
l, r = 2, 6
ans, qsteps = query_trace(tree, len(A), l, r)
assert ans == sum(A[l:r + 1]) == 21
assert min(A[4:7]) == 3 and min(A[:7]) == 1 and min(A[:4]) == 1
p = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / '02-segment-trees.md'
fill(CH, '02-segment-trees.md', block(tree, ["node"], bsteps), "@@TRACE1@@")
fill(CH, '02-segment-trees.md', block(tree, ["node"], qsteps), "@@TRACE2@@")
print(tree, ans)
