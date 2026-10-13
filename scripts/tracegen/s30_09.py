import sys, pathlib, random, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '09-sieve.md'

def sieve(n):
    comp = [False] * (max(n + 1, 2))
    p = 2
    while p * p <= n:
        if not comp[p]:
            for m in range(p * p, n + 1, p):
                comp[m] = True
        p += 1
    return [x for x in range(2, n + 1) if not comp[x]]

def brute_primes(n):
    return [x for x in range(2, n + 1) if all(x % d for d in range(2, x))]

def spf_table(n):
    spf = [0] * max(n + 1, 2)
    for p in range(2, n + 1):
        if spf[p]: continue
        spf[p] = p
        for m in range(p * p, n + 1, p):
            if spf[m] == 0: spf[m] = p
    return spf

def factor(spf, x):
    out = []
    while x > 1:
        out.append(spf[x]); x //= spf[x]
    return out

def brute_factor(x):
    out = []; d = 2
    while x > 1:
        while x % d == 0:
            out.append(d); x //= d
        d += 1
    return out

def count_below(n):
    ps = sieve(n - 1) if n > 2 else []
    return [len(ps), ps[-1] if ps else -1]

def window_count(lo, hi):
    size = hi - lo + 1
    flag = [False] * size
    base = sieve(int(hi ** 0.5) + 1)
    for p in base:
        if p * p > hi: break
        start = max(p * p, ((lo + p - 1) // p) * p)
        for m in range(start, hi + 1, p):
            flag[m - lo] = True
    return sum(1 for x in range(max(lo, 2), hi + 1) if not flag[x - lo])

def window_brute(lo, hi):
    c = 0
    for x in range(max(lo, 2), hi + 1):
        d = 2; ok = True
        while d * d <= x:
            if x % d == 0: ok = False; break
            d += 1
        c += ok
    return c

rng = random.Random(3009)
for n in list(range(0, 80)) + [rng.randint(80, 600) for _ in range(30)]:
    assert sieve(n) == brute_primes(n), n
    s = spf_table(n)
    for x in range(2, n + 1):
        assert factor(s, x) == brute_factor(x)
    if n > 0:
        assert count_below(n) == [len(brute_primes(n - 1)), (brute_primes(n - 1) or [-1])[-1]]
for _ in range(200):
    lo = rng.randint(0, 300); hi = rng.randint(lo, 320)
    assert window_count(lo, hi) == window_brute(lo, hi), (lo, hi)
assert window_count(2147483600, 2147483647) == window_brute(2147483600, 2147483647)

def trace_sieve():
    n = 30
    cells = list(range(2, n + 1))
    idx = lambda v: v - 2
    marked = set()
    steps = [{"at": {"p": -1, "m": -1}, "vars": {"marks": 0}, "note": "No number is marked yet. The scan has not reached any candidate."}]
    total = 0
    p = 2
    while p * p <= n:
        if p not in marked:
            new = [m for m in range(p * p, n + 1, p) if m not in marked]
            for m in range(p * p, n + 1, p): marked.add(m)
            total += len(new)
            steps.append({"at": {"p": idx(p), "m": idx(p * p)}, "vars": {"p": p, "firstMultiple": p * p, "newMarks": len(new), "marks": total},
                          "note": f"The flag of {p} is false, so {p} is prime. The loop starts at {p * p} and writes {len(new)} new marks: {', '.join(map(str, new))}."})
        p += 1
    steps.append({"at": {"p": idx(7), "m": -1}, "vars": {"p": 7, "square": 49, "marks": total}, "note": "For p = 7 the square is 49, which is above 30. The loop ends, and every composite up to 30 is marked."})
    primes = [x for x in range(2, n + 1) if x not in marked]
    assert primes == sieve(n) and len(primes) == 10 and total == 19
    steps.append({"at": {"p": -1, "m": -1}, "vars": {"primes": len(primes), "marks": total}, "note": f"The unmarked numbers are the {len(primes)} primes: {', '.join(map(str, primes))}."})
    return block(cells, ["p", "m"], steps)

def trace_factor():
    s = spf_table(100)
    x = 84
    seq = [x]; fs = []
    while x > 1:
        fs.append(s[x]); x //= s[x]; seq.append(x)
    assert fs == [2, 2, 3, 7] and seq == [84, 42, 21, 7, 1]
    steps = []
    got = []
    for i, v in enumerate(seq):
        if i < len(fs):
            got.append(fs[i])
            steps.append({"at": {"i": i}, "vars": {"x": v, "spf": fs[i], "factors": str(got)},
                          "note": f"The value x is {v} and spf[{v}] is {fs[i]}. The factor {fs[i]} joins the list, and x becomes {v // fs[i]}."})
        else:
            steps.append({"at": {"i": i}, "vars": {"x": v, "factors": str(got)}, "note": "The value x is 1, so the loop stops. The product of the factors is 84."})
    return block(seq, ["i"], steps)

def fmt(v): return json.dumps(v, separators=(", ", ":")).replace(":", ":") 
def arr(v): return "[" + ", ".join(map(str, v)) + "]"

ex = {}
ex["@@EX_B1@@"] = f"Input `n = 30`, output `{arr(sieve(30))}`, the 10 primes up to 30."
assert sieve(2) == [2] and sieve(1) == []
ex["@@EX_B2@@"] = "Input `n = 2`, output `[2]`, because the bound itself is prime. Input `n = 1` returns an empty array."
assert count_below(10) == [4, 7] and count_below(2) == [0, -1]
ex["@@EX_V1@@"] = "Input `n = 10`, output `{4, 7}`, from the primes 2, 3, 5 and 7."
ex["@@EX_V2@@"] = "Input `n = 2`, output `{0, -1}`, because the prime 2 is not strictly smaller than 2."
a = window_count(0, 1); b = window_count(2147483600, 2147483647)
assert a == 0 and b == window_brute(2147483600, 2147483647)
ex["@@EX_X1@@"] = "Input `lo = 0` and `hi = 1`, output 0, because neither 0 nor 1 is prime."
ex["@@EX_X2@@"] = f"Input `lo = 2147483600` and `hi = 2147483647`, output {b}, and the largest value `2147483647` is among the primes."
assert window_brute(2147483647, 2147483647) == 1
s = spf_table(100)
q1 = [12, 97, 84]; q2 = [64, 2]
r1 = [factor(s, x) for x in q1]; r2 = [factor(s, x) for x in q2]
assert r1 == [[2, 2, 3], [97], [2, 2, 3, 7]] and r2 == [[2] * 6, [2]]
ex["@@EX_R1@@"] = f"Input `n = 100` and queries `{arr(q1)}`, output `[[2, 2, 3], [97], [2, 2, 3, 7]]`."
ex["@@EX_R2@@"] = "Input `n = 100` and queries `[64, 2]`, output `[[2, 2, 2, 2, 2, 2], [2]]`, a power of two and a prime."

fill(CH, NAME, trace_sieve(), "@@TRACE1@@")
fill(CH, NAME, trace_factor(), "@@TRACE2@@")
for k, v in ex.items(): fill(CH, NAME, v, k)
print("ok", b)
