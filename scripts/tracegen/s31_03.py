import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '31-range-query-structures-and-sweep-processing'
A = [3, 1, 4, 1, 5, 9, 2, 6]

class Tree:
    def __init__(self, a):
        self.n = len(a)
        self.sum = [0] * (4 * self.n)
        self.add = [0] * (4 * self.n)
        self.steps = []
        self.pushes = 0
        self._build(1, 0, self.n, a)

    def _build(self, k, lo, hi, a):
        if hi - lo == 1:
            self.sum[k] = a[lo]
            return
        m = (lo + hi) // 2
        self._build(2 * k, lo, m, a)
        self._build(2 * k + 1, m, hi, a)
        self.sum[k] = self.sum[2 * k] + self.sum[2 * k + 1]

    def rec(self, k, lo, hi, note, extra=None):
        v = {"node": k, "sum": self.sum[k], "add": self.add[k], "pushes": self.pushes}
        if extra is not None:
            v["result"] = extra
        self.steps.append({"at": {"lo": lo, "hi": hi}, "vars": v, "note": note})

    def apply(self, k, lo, hi, d):
        self.sum[k] += d * (hi - lo)
        self.add[k] += d

    def push(self, k, lo, hi):
        if self.add[k]:
            m = (lo + hi) // 2
            self.apply(2 * k, lo, m, self.add[k])
            self.apply(2 * k + 1, m, hi, self.add[k])
            self.add[k] = 0
            self.pushes += 1
            return True
        return False

    def update(self, k, lo, hi, l, r, d):
        if r <= lo or hi <= l:
            self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and lies outside [{l}, {r}), so the update skips it.")
            return
        if l <= lo and hi <= r:
            self.apply(k, lo, hi, d)
            self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and lies inside [{l}, {r}). Its sum grows by {d} times {hi - lo}, and its tag becomes {self.add[k]}. The children stay unchanged.")
            return
        pushed = self.push(k, lo, hi)
        m = (lo + hi) // 2
        self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and overlaps [{l}, {r}) only in part, so the update descends. " + ("It pushes its tag first." if pushed else "Its tag is 0, so nothing needs pushing."))
        self.update(2 * k, lo, m, l, r, d)
        self.update(2 * k + 1, m, hi, l, r, d)
        self.sum[k] = self.sum[2 * k] + self.sum[2 * k + 1]
        self.rec(k, lo, hi, f"Node {k} recomputes its sum from its children as {self.sum[k]}.")

    def query(self, k, lo, hi, l, r):
        if r <= lo or hi <= l:
            self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and lies outside [{l}, {r}), so it contributes 0.", 0)
            return 0
        if l <= lo and hi <= r:
            self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and lies inside [{l}, {r}), so it contributes its sum {self.sum[k]}. Its own tag has been applied to that sum already.", self.sum[k])
            return self.sum[k]
        pushed = self.push(k, lo, hi)
        m = (lo + hi) // 2
        self.rec(k, lo, hi, f"Node {k} covers [{lo}, {hi}) and overlaps [{l}, {r}) only in part, so the query descends. " + ("It pushes its tag first, so both children hold correct sums." if pushed else "Its tag is 0, so nothing needs pushing."))
        res = self.query(2 * k, lo, m, l, r) + self.query(2 * k + 1, m, hi, l, r)
        return res

def brute_add(a, l, r, d):
    return [x + d if l <= i < r else x for i, x in enumerate(a)]

t = Tree(A)
t.update(1, 0, 8, 2, 7, 5)
ref = brute_add(A, 2, 7, 5)
assert t.sum[1] == sum(ref)
steps1 = t.steps
# leaves hold true values only after pushes; check the root sum and the tags set so far
assert t.add[5] == 5 and t.add[6] == 5 and t.add[14] == 5
t.steps = []
res = t.query(1, 0, 8, 3, 6)
assert res == sum(ref[3:6]) == 30
steps2 = t.steps
t.steps.append({"at": {"lo": 3, "hi": 6}, "vars": {"result": res, "pushes": t.pushes}, "note": f"The two partial branches and the covered node add up to {res}, which equals the sum of positions 3, 4 and 5 of the updated array."})
assert steps1 and len(steps1) >= 3 and len(steps2) >= 3

p = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / '03-lazy-propagation.md'
fill(CH, '03-lazy-propagation.md', block(A, ["lo", "hi"], steps1), "@@TRACE1@@")
fill(CH, '03-lazy-propagation.md', block(A, ["lo", "hi"], steps2), "@@TRACE2@@")
print(len(steps1), len(steps2), t.pushes, res)
