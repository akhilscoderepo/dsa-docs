from common import *
import itertools
CH = '29-dynamic-programming-intervals-and-advanced-states'
INF = 10**9

def bits(mask, n):
    return format(mask, '0%db' % n)

def brute(c):
    n = len(c)
    return min(sum(c[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n)))

def run(c, ph, expect):
    n = len(c)
    full = (1 << n) - 1
    dp = [INF] * (1 << n)
    dp[0] = 0
    st = [{"at": {"mask": -1}, "vars": {"mask": bits(0, n), "worker": -1, "dp": 0},
           "note": "Only mask 0 is known. The empty set of jobs costs 0, and the other entries wait."}]
    for mask in range(1, full + 1):
        w = bin(mask).count('1') - 1
        opts = []
        for j in range(n):
            if mask >> j & 1:
                opts.append((dp[mask ^ (1 << j)] + c[w][j], j))
        best = min(o[0] for o in opts)
        dp[mask] = best
        parts = "; ".join("job %d leaves mask %s at %d plus %d, which is %d" % (j, bits(mask ^ (1 << j), n), dp[mask ^ (1 << j)], c[w][j], v) for v, j in opts)
        st.append({"at": {"mask": mask},
                   "vars": {"mask": bits(mask, n), "worker": w, "dp": best},
                   "note": "Mask %s holds %d job%s, so worker %d takes the last one. Options: %s. The entry keeps the smallest, %d." % (bits(mask, n), w + 1, "" if w == 0 else "s", w, parts, best)})
    assert dp[full] == expect == brute(c), (dp[full], expect, brute(c))
    fill(CH, '04-bitmask-assignment.md', block(list(range(1 << n)), ["mask"], st), ph)

run([[3, 3, 9], [2, 8, 9], [7, 6, 5]], "@@TRACE1@@", 10)
run([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]], "@@TRACE2@@", 
    brute([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]]))
