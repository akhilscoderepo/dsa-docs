import sys, pathlib, random, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '02-shifts.md'
M = 0xFFFFFFFF

def s32(v):
    v &= M
    return v - (1 << 32) if v >> 31 else v

def sar(x, k): return x >> k              # python >> on negative ints is arithmetic
def shr(x, k): return (x & M) >> k        # zero fill on the 32-bit pattern

# ---------- algorithms and brute force oracles ----------
def bit_at(x, i): return sar(x, i) & 1
def bit_brute(x, i): return format(x & M, '032b')[31 - i] == '1' and 1 or 0

def reverse_loop(n):
    res = 0
    for _ in range(32):
        res = ((res << 1) | (n & 1)) & M
        n = shr(n, 1)
    return s32(res)
def reverse_brute(n): return s32(int(format(n & M, '032b')[::-1], 2))

def count_loop(x):
    x &= M; c = 0
    for _ in range(32):
        if x == 0: break
        c += x & 1; x >>= 1
    assert x == 0
    return c
def count_brute(x): return bin(x & M).count('1')

def pack(x, y): return s32((x << 20) | y)
def unpack(p, f): return shr(p, 20) if f == 0 else p & 0xFFFFF
def pack_answers(recs, qs):
    st = [pack(x, y) for x, y in recs]
    return [unpack(st[r], f) for r, f in qs]
def pack_brute(recs, qs): return [recs[r][f] for r, f in qs]

rng = random.Random(3002)
for _ in range(600):
    x = rng.randint(-2 ** 31, 2 ** 31 - 1); i = rng.randint(0, 31)
    assert bit_at(x, i) == bit_brute(x, i)
    assert reverse_loop(x) == reverse_brute(x)
    assert count_loop(x) == count_brute(x)
    recs = [(rng.randint(0, 4095), rng.randint(0, 1048575)) for _ in range(rng.randint(1, 5))]
    qs = [(rng.randrange(len(recs)), rng.randint(0, 1)) for _ in range(6)]
    assert pack_answers(recs, qs) == pack_brute(recs, qs)

# ---------- traces ----------
def trace_digits():
    x = 180
    cells = [(x >> i) & 1 for i in range(8)]
    steps = [{"at": {"i": -1}, "vars": {"x": x}, "note": "The cells show positions 0 to 7 of 180, and no read has run."}]
    for i in (2, 3, 7):
        sh = x >> i
        assert sh & 1 == cells[i] == bit_brute(x, i)
        steps.append({"at": {"i": i}, "vars": {"shifted": sh, "bit": sh & 1},
                      "note": f"The shift 180 >> {i} gives {sh}. The AND with 1 keeps only the lowest bit, which is {sh & 1}."})
    return block(cells, ["i"], steps)

def trace_shifts():
    x = -16
    dist = [0, 4, 8, 12, 16, 20, 24, 28, 31]
    steps = []
    for k, s in enumerate(dist):
        a, z = sar(x, s), s32(shr(x, s))   # zero fill on the pattern, shown as a Java int
        assert a == x >> s and z == s32((x & M) >> s)
        if s == 0: note = "With distance 0 both shifts return -16."
        elif s == 4: note = f"The signed shift copies the sign into the top positions and gives {a}. The zero-fill shift puts zeros there and gives {z}."
        elif s == 31: note = f"The signed shift stays at {a}. The zero-fill shift reaches {z}, the sign bit alone."
        else: note = f"The signed shift stays at {a}. The zero-fill shift gives {z}."
        steps.append({"at": {"s": k}, "vars": {"signed": a, "zeroFill": z}, "note": note})
    assert sar(x, 4) == -1 and shr(x, 4) == 268435455 and shr(x, 31) == 1 and s32(shr(x, 0)) == -16
    return block(dist, ["s"], steps)

def fmt(v): return json.dumps(v, separators=(",", ":"))
ex = {}
x1, i1 = 180, 2; x2, i2 = -2 ** 31 + 5, 31
assert bit_at(x1, i1) == 1; assert bit_at(x2, i2) == 1 == bit_brute(x2, i2)
ex["@@EX_E1@@"] = f"Input `x = {x1}` and `i = {i1}`, output {bit_at(x1, i1)}, because `180 >> 2` is 45 and the lowest bit of 45 is 1."
ex["@@EX_E2@@"] = f"Input `x = {x2}` and `i = {i2}`, output {bit_at(x2, i2)}, because position 31 is the sign bit of a negative `int`."

r1 = 43261596; r2 = -3; e1 = reverse_loop(r1); e2 = reverse_loop(r2)
assert e1 == reverse_brute(r1) == 964176192 and e2 == reverse_brute(r2) == -1073741825
ex["@@EX_R1@@"] = f"Input `n = {r1}`, output {e1}, because the 32-bit pattern `{format(r1 & M, '032b')}` reverses to `{format(e1 & M, '032b')}`."
ex["@@EX_R2@@"] = f"Input `n = {r2}`, output {e2}, because the pattern `{format(r2 & M, '032b')}` reverses to `{format(e2 & M, '032b')}` and has a 0 only at position 30."

n1, n2 = -8, -2 ** 31
assert count_loop(n1) == count_brute(n1) == 29 and count_loop(n2) == 1
ex["@@EX_N1@@"] = f"Input `x = {n1}`, output {count_loop(n1)}, because the pattern `{format(n1 & M, '032b')}` has 29 ones."
ex["@@EX_N2@@"] = f"Input `x = Integer.MIN_VALUE`, output {count_loop(n2)}, because only the sign bit is 1, and a loop with `>>` would stay at -1 forever."

recs1 = [(4095, 7), (1, 1048575), (0, 0)]; q1 = [(0, 0), (0, 1), (1, 1)]
recs2 = [(2, 5)]; q2 = [(0, 0), (0, 1)]
a1 = pack_answers(recs1, q1); a2 = pack_answers(recs2, q2)
assert a1 == pack_brute(recs1, q1) == [4095, 7, 1048575] and a2 == [2, 5]
assert pack(4095, 7) < 0
ex["@@EX_K1@@"] = f"Input records {fmt([list(r) for r in recs1])} and queries {fmt([list(q) for q in q1])}, output {fmt(a1)}. The first record stores as {pack(4095, 7)}, which is negative, and the zero-fill shift still recovers 4095."
ex["@@EX_K2@@"] = f"Input records {fmt([list(r) for r in recs2])} and queries {fmt([list(q) for q in q2])}, output {fmt(a2)}, because the record stores as {pack(2, 5)} and the two reads split it again."

fill(CH, NAME, trace_digits(), "@@TRACE1@@")
fill(CH, NAME, trace_shifts(), "@@TRACE2@@")
for k, v in ex.items(): fill(CH, NAME, v, k)
print("ok")
