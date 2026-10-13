import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '29-dynamic-programming-intervals-and-advanced-states'

def brute(n):
    return sum(1 for x in range(1, n + 1) if '0' not in str(x))

def run(n):
    digits = [int(c) for c in str(n)]
    ways = [[0, 0], [0, 0]]
    ways[1][0] = 1
    def vars_(p):
        return {"t1s0": ways[1][0], "t1s1": ways[1][1], "t0s0": ways[0][0], "t0s1": ways[0][1]}
    steps = [{"at": {"pos": -1}, "vars": vars_(-1),
              "note": "One empty prefix exists. It is tight, because it equals the empty start of n, and it is not started."}]
    for p, d in enumerate(digits):
        nxt = [[0, 0], [0, 0]]
        for t in range(2):
            for s in range(2):
                c = ways[t][s]
                if c == 0:
                    continue
                lim = d if t == 1 else 9
                for dig in range(lim + 1):
                    if s == 1 and dig == 0:
                        continue
                    nt = 1 if (t == 1 and dig == lim) else 0
                    ns = 1 if (s == 1 or dig != 0) else 0
                    nxt[nt][ns] += c
        ways = nxt
        total = ways[0][1] + ways[1][1]
        steps.append({"at": {"pos": p}, "vars": vars_(p),
                      "note": f"Position {p} has limit digit {d}. The started counts now sum to {total}, of which {ways[1][1]} stay tight."})
    ans = ways[0][1] + ways[1][1]
    assert ans == brute(n), (n, ans)
    return digits, steps, ans

t = pathlib.Path(__file__).resolve().parents[2] / 'dsa-skills' / 'manuscripts' / CH / '06-digit-dp.md'
res = {}
for ph, n in (("@@TRACE1@@", 3047), ("@@TRACE2@@", 130)):
    digits, steps, ans = run(n)
    res[n] = ans
    fill(CH, '06-digit-dp.md', block(digits, ["pos"], steps), ph)
assert res == {3047: 2277, 130: 108}
print(res)
