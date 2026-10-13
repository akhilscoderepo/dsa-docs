import sys, pathlib, random, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '10-modular-arithmetic.md'
MOD = 1_000_000_007

def sum_prod(a, m):
    s = 0; p = 1 % m
    for v in a:
        s = (s + v % m) % m
        p = p * (v % m) % m
    return [s, p]

def sum_prod_brute(a, m):
    p = 1
    for v in a: p *= v
    return [sum(a) % m, p % m]

def powmod(b, e, m):
    r = 1 % m; b %= m
    while e > 0:
        if e & 1: r = r * b % m
        b = b * b % m; e >>= 1
    return r

def count_subseq(nums, target, m):
    a = sorted(nums); n = len(a)
    pw = [0] * n
    if n: pw[0] = 1 % m
    for i in range(1, n): pw[i] = pw[i - 1] * 2 % m
    l, r, res = 0, n - 1, 0
    while l <= r:
        if a[l] + a[r] <= target:
            res = (res + pw[r - l]) % m; l += 1
        else:
            r -= 1
    return res

def count_brute(nums, target, m):
    n = len(nums); c = 0
    for mask in range(1, 1 << n):
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if min(sub) + max(sub) <= target: c += 1
    return c % m

rng = random.Random(3010)
for _ in range(300):
    a = [rng.randint(0, 2**31 - 1) for _ in range(rng.randint(0, 8))]
    m = rng.choice([1, 2, 7, 1000, MOD])
    assert sum_prod(a, m) == sum_prod_brute(a, m)
    b, e = rng.randint(0, 10**6), rng.randint(0, 60)
    assert powmod(b, e, m) == pow(b, e, m)
    nums = [rng.randint(1, 12) for _ in range(rng.randint(1, 9))]
    t = rng.randint(1, 24)
    assert count_subseq(nums, t, m) == count_brute(nums, t, m), (nums, t, m)

def trace_pow():
    base, exp, m = 3, 13, 1000
    bits = [(exp >> i) & 1 for i in range(exp.bit_length())]
    r, b = 1, base
    steps = [{"at": {"i": -1}, "vars": {"result": 1, "base": 3}, "note": "The result starts at 1 and the base starts at 3. No bit has been read."}]
    for i, bit in enumerate(bits):
        if bit: r = r * b % m
        nb = b * b % m
        steps.append({"at": {"i": i}, "vars": {"bit": bit, "result": r, "base": nb},
                      "note": (f"Bit {bit} is set, so the result becomes {r}. " if bit else f"Bit {bit} is clear, so the result stays {r}. ") + f"The base squares to {nb} for the next bit."})
        b = nb
    assert r == pow(base, exp, m) == powmod(base, exp, m) == 323 and bits == [1, 0, 1, 1]
    return block(bits, ["i"], steps)

def trace_sum():
    xs, m = [5, -9, 4, -13, 8], 7
    raw = norm = 0
    steps = [{"at": {"i": -1}, "vars": {"raw": 0, "norm": 0}, "note": "Both sums start at 0. No change has been added."}]
    for i, x in enumerate(xs):
        raw = (lambda v: int(v - 7 * int(v / 7)))(raw + x)   # Java % truncates toward zero
        norm = (norm + x) % m
        note = f"The change {x} gives raw {raw} and normalized {norm}."
        if raw < 0: note += " The raw sum is negative, which is not a valid remainder."
        steps.append({"at": {"i": i}, "vars": {"raw": raw, "norm": norm}, "note": note})
    assert norm == sum(xs) % m == 2 and raw == 2
    return block(xs, ["i"], steps)

def arr(v): return "[" + ", ".join(map(str, v)) + "]"
ex = {}
a1 = [1000000000, 999999999, 123456789]; assert sum_prod(a1, MOD) == sum_prod_brute(a1, MOD)
ex["@@EX_B1@@"] = f"Input `a = {arr(a1)}` and `m = 1000000007`, output `{arr(sum_prod(a1, MOD))}`, where the exact product is far above the range of `long`."
a2 = []; assert sum_prod(a2, 1) == [0, 0] and sum_prod(a2, 10) == [0, 1]
ex["@@EX_B2@@"] = "Input `a = []` and `m = 10`, output `[0, 1]`, since the empty sum is 0 and the empty product is 1. With `m = 1` the same input gives `[0, 0]`."
assert powmod(2, 10, 1000) == 24
ex["@@EX_V1@@"] = "Input `base = 2`, `exp = 10` and `m = 1000`, output 24, since 2^10 is 1024."
big = powmod(10**18, 10**18, MOD); assert powmod(0, 0, 7) == 1 and powmod(0, 0, 1) == 0
ex["@@EX_V2@@"] = f"Input `base = 10^18`, `exp = 10^18` and `m = 1000000007`, output {big}. Input `base = 0`, `exp = 0` and `m = 7` gives 1."
import itertools
a, b, m = [3, -4, 10], [10, 6, 10], 5
r = [(x - y) % m for x, y in zip(a, b)]; assert r == [3, 0, 0]
ex["@@EX_X1@@"] = f"Input `a = {arr(a)}`, `b = {arr(b)}` and `m = 5`, output `{arr(r)}`, since -7 is congruent to 3 and -10 is congruent to 0."
mn, mx = -2**31, 2**31 - 1
v = (mn - mx) % 1000; w = (mx - mn) % 2147483647
ex["@@EX_X2@@"] = f"Input `a = [-2147483648, 2147483647]`, `b = [2147483647, -2147483648]` and `m = 1000`, output `{arr([v, (mx - mn) % 1000])}`, where the first difference is below the range of `int`."
nums, t, m = [4, 1, 6, 2, 3], 7, 1000
c = count_subseq(nums, t, m); assert c == count_brute(nums, t, m)
ex["@@EX_R1@@"] = f"Input `nums = {arr(nums)}`, `target = 7` and `m = 1000`, output {c}."
nums2, t2 = [3, 3, 6, 8], 9
assert count_subseq(nums2, t2, 1) == 0
c2 = count_subseq(nums2, t2, MOD); assert c2 == count_brute(nums2, t2, MOD)
ex["@@EX_R2@@"] = f"Input `nums = {arr(nums2)}`, `target = 9` and `m = 1000000007`, output {c2}. The same input with `m = 1` returns 0."

fill(CH, NAME, trace_pow(), "@@TRACE1@@")
fill(CH, NAME, trace_sum(), "@@TRACE2@@")
for k, v in ex.items(): fill(CH, NAME, v, k)
print("ok", ex["@@EX_V2@@"], ex["@@EX_X2@@"], ex["@@EX_R1@@"], ex["@@EX_R2@@"])
