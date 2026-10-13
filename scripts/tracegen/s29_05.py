from common import *
CH = '29-dynamic-programming-intervals-and-advanced-states'
FILE = '05-submask-aggregation.md'


def b(x, n):
    return format(x, '0%db' % n)


def run1(mask, n, ph):
    # Enumerate submasks with the descending step and record each move.
    subs = []
    sub = mask
    steps = []
    while sub > 0:
        subs.append(sub)
        nxt = (sub - 1) & mask
        k = len(subs) - 1
        steps.append({"at": {"i": k}, "vars": {"sub": b(sub, n), "sub-1": b(sub - 1, n), "next": b(nxt, n)},
                      "note": f"The submask {b(sub, n)} is reported. Subtracting 1 gives {b(sub - 1, n)}, and the AND with the mask leaves {b(nxt, n)}."
                      + (" This is 0, so the loop stops." if nxt == 0 else "")})
        sub = nxt
    assert len(subs) == 2 ** bin(mask).count('1') - 1
    assert subs == sorted(subs, reverse=True) and all(s & mask == s for s in subs)
    assert sorted(subs) == [s for s in range(1, mask + 1) if s & mask == s]
    steps.append({"at": {"i": len(subs)}, "vars": {"sub": b(0, n), "count": len(subs)},
                  "note": f"The loop ends with {len(subs)} nonempty submasks, which equals 2^{bin(mask).count('1')} - 1."})
    fill(CH, FILE, block(subs, ["i"], steps), ph)


def run2(w, cap, ph, expect):
    n = len(w)
    N = 1 << n
    sums = [sum(w[i] for i in range(n) if m >> i & 1) for m in range(N)]
    dp = [0] * N
    steps = [{"at": {"mask": 0}, "vars": {"mask": b(0, n), "sum": 0, "dp": 0},
              "note": "The empty mask needs 0 groups, so it is the base value."}]
    for m in range(1, N):
        if sums[m] <= cap:
            dp[m] = 1
            note = f"The items of {b(m, n)} weigh {sums[m]}, which fits the capacity {cap}. One group holds them."
            v = {"mask": b(m, n), "sum": sums[m], "dp": 1}
        else:
            best = 10 ** 9
            arg = 0
            sub = (m - 1) & m
            while sub > 0:
                c = dp[sub] + dp[m ^ sub]
                if c < best:
                    best, arg = c, sub
                sub = (sub - 1) & m
            dp[m] = best
            note = (f"The items of {b(m, n)} weigh {sums[m]}, which exceeds {cap}. The best split is {b(arg, n)} with {b(m ^ arg, n)}, "
                    f"which costs {dp[arg]} plus {dp[m ^ arg]}.")
            v = {"mask": b(m, n), "sum": sums[m], "split": b(arg, n), "dp": best}
        steps.append({"at": {"mask": m}, "vars": v, "note": note})
    assert dp[N - 1] == expect, dp[N - 1]
    # Oracle: assign each item to a group index, smallest group count wins.
    def brute(i, loads):
        if i == n:
            return len(loads)
        r = 10 ** 9
        for g in range(len(loads)):
            if loads[g] + w[i] <= cap:
                loads[g] += w[i]
                r = min(r, brute(i + 1, loads))
                loads[g] -= w[i]
        loads.append(w[i])
        r = min(r, brute(i + 1, loads))
        loads.pop()
        return r
    assert brute(0, []) == expect
    fill(CH, FILE, block(sums, ["mask"], steps), ph)


if __name__ == '__main__':
    run1(0b1101, 4, "@@TRACE1@@")
    run2([4, 3, 3, 2], 6, "@@TRACE2@@", 2)
