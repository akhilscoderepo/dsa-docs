import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '03-low-bit.md'
M32 = 0xFFFFFFFF

def clear_k(x, k):
    r = 0
    while r < k and x != 0:
        x &= (x - 1); r += 1
    return x

def clear_k_brute(x, k):
    bits = [i for i in range(32) if (x >> i) & 1][:k]
    for i in bits: x &= ~(1 << i)
    return x

def count_loop(n):
    c = 0
    while n:
        n &= n - 1; c += 1
    return c

def lowest_bit(x):
    u = x & M32
    return (u & (-u & M32))

def lowest_brute(x):
    u = x & M32
    for i in range(32):
        if (u >> i) & 1: return 1 << i
    return 0

def table(n):
    a = [0] * (n + 1)
    for i in range(1, n + 1): a[i] = a[i & (i - 1)] + 1
    return a

rnd = random.Random(30)
for _ in range(3000):
    x = rnd.getrandbits(31); k = rnd.randint(0, 40)
    assert clear_k(x, k) == clear_k_brute(x, k)
    assert count_loop(x) == bin(x).count("1")
    y = rnd.randint(-2**31, 2**31 - 1)
    assert lowest_bit(y) == lowest_brute(y)
assert table(300) == [bin(i).count("1") for i in range(301)]

def trace1():
    x = 180
    cells = [(x >> (7 - i)) & 1 for i in range(8)]
    assert cells == [1, 0, 1, 1, 0, 1, 0, 0]
    steps = [{"at": {"bit": -1}, "vars": {"x": x, "rounds": 0},
              "note": "The loop starts with x = 180, which is 10110100. No round has run yet."}]
    rounds = 0
    while x:
        low = (x & -x).bit_length() - 1
        nx = x & (x - 1)
        rounds += 1
        steps.append({"at": {"bit": 7 - low}, "vars": {"x": nx, "rounds": rounds},
                      "note": f"Round {rounds} removes the set bit at position {low}. The value x - 1 is {x - 1}, and the AND leaves {nx}."})
        x = nx
    assert x == 0 and rounds == 4 == bin(180).count("1")
    steps[-1]["note"] += " The value is 0, so the loop stops."
    return block(cells, ["bit"], steps)

def trace2():
    n = 8
    ans = table(n)
    steps = [{"at": {"i": 0}, "vars": {"cleared": 0, "before": 0, "ans": 0}, "note": "The entry for 0 is 0 and serves as the base case."}]
    for i in range(1, n + 1):
        p = i & (i - 1)
        steps.append({"at": {"i": i}, "vars": {"cleared": p, "before": ans[p], "ans": ans[i]},
                      "note": f"The number {i} is {i:b} in binary. Clearing its lowest set bit gives {p}, whose entry is {ans[p]}, so the entry for {i} is {ans[i]}."})
    assert ans == [0, 1, 1, 2, 1, 2, 2, 3, 1]
    return block(ans, ["i"], steps)

def fmt(v):
    import json
    return json.dumps(v, separators=(",", ":"))

ex = {}
assert clear_k(180, 2) == 160
ex["@@EX_B1@@"] = "Input `x = 180` and `k = 2`, output 160. The value 10110100 loses its two lowest ones and becomes 10100000."
assert clear_k(7, 5) == 0
ex["@@EX_B2@@"] = "Input `x = 7` and `k = 5`, output 0. The value has three set bits, so the loop stops at 0 after three rounds."
assert count_loop(2**31 - 1) == 31 and count_loop(180) == 4
ex["@@EX_V1@@"] = "Input `n = 180`, output 4, because 10110100 contains four ones."
ex["@@EX_V2@@"] = "Input `n = 2147483647`, output 31, because every value bit is set and the loop runs 31 rounds."
assert lowest_bit(-8) == 8 and lowest_bit(-2**31) == 2**31
ex["@@EX_X1@@"] = "Input `x = -8`, output 8, because the pattern ends in three zeros and the lowest one is at position 3."
ex["@@EX_X2@@"] = "Input `x = -2147483648`, output 2147483648, because only bit 31 is set and the `int` result of `x & -x` is negative."
assert table(8) == [0, 1, 1, 2, 1, 2, 2, 3, 1] and table(0) == [0]
ex["@@EX_R1@@"] = "Input `n = 8`, output `[0,1,1,2,1,2,2,3,1]`, where the last entry restarts at 1 because 8 is a single set bit."
ex["@@EX_R2@@"] = "Input `n = 0`, output `[0]`, a single entry for the number 0."

fill(CH, NAME, trace1(), "@@TRACE1@@")
fill(CH, NAME, trace2(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
