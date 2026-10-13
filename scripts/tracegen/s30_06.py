import sys, pathlib, random, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '06-overflow.md'
MAXI, MINI = 2 ** 31 - 1, -2 ** 31

def wrap(v):
    v &= 0xFFFFFFFF
    return v - 2 ** 32 if v >= 2 ** 31 else v

def jdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

def jmod(a, b):
    return a - b * jdiv(a, b)

def reverse_checked(x):
    rev = 0
    while x != 0:
        d = jmod(x, 10); x = jdiv(x, 10)
        if rev > MAXI // 10 or (rev == MAXI // 10 and d > 7) or rev < jdiv(MINI, 10) or (rev == jdiv(MINI, 10) and d < -8):
            return 0
        rev = rev * 10 + d
    return rev

def reverse_brute(x):
    s = int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)
    return s if MINI <= s <= MAXI else 0

rng = random.Random(3006)
for _ in range(2000):
    x = rng.choice([rng.randint(MINI, MAXI), rng.randint(-10 ** 6, 10 ** 6), rng.randint(10 ** 9, MAXI), rng.randint(MINI, -10 ** 9)])
    assert reverse_checked(x) == reverse_brute(x), x
for x in (MAXI, MINI, 0, 1463847412, 1463847413, -1463847412, -1463847413, 1534236469, 1463847419):
    assert reverse_checked(x) == reverse_brute(x), x

def trace_sum():
    vals = [1500000000, 1500000000, 100]
    steps = [{"at": {"i": -1}, "vars": {"intSum": 0, "longSum": 0}, "note": "Both accumulators start at 0."}]
    si, sl = 0, 0
    for i, v in enumerate(vals):
        si = wrap(si + v); sl += v
        txt = f"The value {v} is added. The long accumulator holds the true total {sl}."
        if si != sl:
            txt += f" The int accumulator kept only the low 32 bits, so it holds {si}, which is wrong."
        else:
            txt += f" The int accumulator still agrees at {si}."
        steps.append({"at": {"i": i}, "vars": {"intSum": si, "longSum": sl}, "note": txt})
    assert sl == 3000000100 and si == wrap(3000000100) and si < 0
    return block(vals, ["i"], steps)

def trace_rev():
    x = 1463847413
    digs = []; t = x
    while t:
        digs.append(t % 10); t //= 10
    steps = [{"at": {"i": -1}, "vars": {"rev": 0, "limit": MAXI // 10}, "note": "No digit is taken yet. The check compares rev with 214748364 before every multiplication."}]
    rev = 0; result = None
    for i, d in enumerate(digs):
        if rev > MAXI // 10 or (rev == MAXI // 10 and d > 7):
            steps.append({"at": {"i": i}, "vars": {"rev": rev, "digit": d}, "note": f"The value rev is {rev}, which is above 214748364. Multiplying by 10 would leave the int range, so the method returns 0."})
            result = 0
            break
        rev = rev * 10 + d
        steps.append({"at": {"i": i}, "vars": {"rev": rev, "digit": d}, "note": f"The check passes. The update gives rev = {rev}." + (" This is the ninth digit, so the next step is the decisive one." if i == 8 else "")})
    assert result == 0 == reverse_checked(x) == reverse_brute(x) and len(digs) == 10 and i == 9
    return block(digs, ["i"], steps)

def fmt(v): return json.dumps(v, separators=(",", ":"))
def cmp_key(p): return (p[0], -p[1])

ex = {}
a1 = [MAXI, MAXI, 5]; a2 = [MINI, MINI]
assert sum(a1) == 4294967299 and sum(a2) == -4294967296
ex["@@EX_B1@@"] = f"Input `a = {fmt(a1)}`, output 4294967299, while an `int` accumulator would end at 3."
ex["@@EX_B2@@"] = f"Input `a = {fmt(a2)}`, output -4294967296, which is far below the `int` range."
assert wrap(sum(a1)) == 3

p1 = [[MAXI, 1], [MINI, 5], [MAXI, 9], [0, 3]]
p2 = [[5, 2], [5, 7], [-1, 0]]
s1 = sorted(p1, key=cmp_key); s2 = sorted(p2, key=cmp_key)
assert s1 == [[MINI, 5], [0, 3], [MAXI, 9], [MAXI, 1]] and s2 == [[-1, 0], [5, 7], [5, 2]]
ex["@@EX_V1@@"] = f"Input `{fmt(p1)}`, output `{fmt(s1)}`. A subtraction comparator mis-orders `2147483647` and `-2147483648`."
ex["@@EX_V2@@"] = f"Input `{fmt(p2)}`, output `{fmt(s2)}`, because the two pairs with first number 5 go by second number 7 and then 2."
assert wrap(MAXI - MINI) == -1

ex["@@EX_O1@@"] = "Input `x = -2147483648`, output 2147483648, since negating in `int` would return the same negative value."
ex["@@EX_O2@@"] = "Input `x = -7`, output 7."

assert reverse_checked(1463847412) == 2147483641 == reverse_brute(1463847412)
assert reverse_checked(-4210) == -124 == reverse_brute(-4210)
ex["@@EX_R1@@"] = "Input `x = 1463847412`, output 2147483641, which sits just below the limit because the last digit 1 is at most 7."
ex["@@EX_R2@@"] = "Input `x = 2046384125`, output 0, because the reversed number 5214836402 is above 2147483647."
assert reverse_checked(2046384125) == 0 == reverse_brute(2046384125)

fill(CH, NAME, trace_sum(), "@@TRACE1@@")
fill(CH, NAME, trace_rev(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
