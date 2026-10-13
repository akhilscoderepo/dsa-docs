import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '07-binary-arithmetic.md'
M = 0xFFFFFFFF

def s32(x):
    x &= M
    return x - (1 << 32) if x >> 31 else x

# ---------- algorithms and brute force oracles ----------
def add_rounds(a, b):
    a &= M; b &= M
    rounds = 0
    while b:
        a, b = (a ^ b) & M, ((a & b) << 1) & M
        rounds += 1
    return s32(a), rounds

def half(a, b):
    return [a ^ b, (a & b)]

def add_str(x, y):
    return bin(int(x, 2) + int(y, 2))[2:]

def add_str_cols(x, y):
    out = []; i = len(x) - 1; j = len(y) - 1; c = 0
    while i >= 0 or j >= 0 or c:
        t = c
        if i >= 0: t += int(x[i]); i -= 1
        if j >= 0: t += int(y[j]); j -= 1
        out.append(str(t & 1)); c = t >> 1
    return ''.join(reversed(out))

rng = random.Random(3007)
for a in (0, 1):
    for b in (0, 1):
        assert half(a, b)[0] + 2 * half(a, b)[1] == a + b
for _ in range(2000):
    a = rng.randint(-2**31, 2**31 - 1); b = rng.randint(-2**31, 2**31 - 1)
    s, r = add_rounds(a, b)
    assert s == s32(a + b) and r <= 32
    n = rng.randint(1, 12); m = rng.randint(1, 12)
    x = ''.join(rng.choice('01') for _ in range(n)); y = ''.join(rng.choice('01') for _ in range(m))
    assert int(add_str_cols(x, y), 2) == int(x, 2) + int(y, 2)

# ---------- traces ----------
def trace_words():
    a, b = 13, 11
    cells = [a]; steps = [{"at": {"round": 0}, "vars": {"a": a, "b": b},
        "note": "The loop starts with a = 13 (1101) and the second operand b = 11 (1011)."}]
    r = 0
    while b:
        sw = a ^ b; cw = (a & b) << 1
        r += 1
        a, b = sw, cw
        cells.append(a)
        note = f"Round {r} gives the sum word {a:b} and the carry word {b:b}."
        note += " The carry word is 0, so the loop stops." if b == 0 else " The carry word is not 0, so another round follows."
        steps.append({"at": {"round": r}, "vars": {"a": a, "b": b}, "note": note})
    assert a == 24 and r == 4 and cells == [13, 6, 20, 16, 24]
    assert add_rounds(13, 11) == (24, 4)
    return block(cells, ["round"], steps)

def trace_string():
    x, y = "1011", "110"
    cells = [int(ch) for ch in x]
    steps = [{"at": {"i": len(x)}, "vars": {"carry": 0}, "note": "No column is read yet, so the carry is 0 and the pointer sits past the last digit."}]
    carry = 0; out = []
    for i in range(len(x) - 1, -1, -1):
        j = i - (len(x) - len(y))
        xd = int(x[i]); yd = int(y[j]) if j >= 0 else 0
        t = carry + xd + yd
        d = t & 1
        out.append(d)
        note = f"Column {len(x) - i} adds the digits {xd} and {yd} to the incoming carry {carry}, which gives {t}. The output digit is {d} and the new carry is {t >> 1}."
        carry = t >> 1
        steps.append({"at": {"i": i}, "vars": {"xDigit": xd, "yDigit": yd, "total": t, "carry": carry}, "note": note})
    assert carry == 1
    out.append(carry)
    steps.append({"at": {"i": -1}, "vars": {"carry": 1}, "note": "Every column is read and the carry is still 1, so it becomes the leading digit. The result reads 10001."})
    assert ''.join(map(str, reversed(out))) == "10001" == add_str(x, y)
    return block(cells, ["i"], steps)

ex = {}
ex["@@EX_B1@@"] = "Input `a = 1` and `b = 1`, output `[0, 1]`, because 1 + 1 is binary `10`, which has sum bit 0 and carry bit 1."
assert half(1, 1) == [0, 1]
assert half(1, 0) == [1, 0]
ex["@@EX_B2@@"] = "Input `a = 1` and `b = 0`, output `[1, 0]`, because only one input bit is set and no carry forms."

assert add_rounds(13, 11) == (24, 4)
assert add_rounds(999999999, 1) == (1000000000, 10)
ex["@@EX_V1@@"] = "Input `a = 13` and `b = 11`, output `[24, 4]`, because the carry word lasts four rounds, as the trace shows."
ex["@@EX_V2@@"] = "Input `a = 999999999` and `b = 1`, output `[1000000000, 10]`, because the carry travels up a run of nine set bits and needs ten rounds."
assert add_rounds(7, 0) == (7, 0)

assert add_rounds(-5, 3) == (-2, 2)
assert add_rounds(-2**31, -1) == (2**31 - 1, 1)
assert add_rounds(-1, 1) == (0, 32)
ex["@@EX_O1@@"] = "Input `a = -5` and `b = 3`, output -2, because the carry word becomes 0 after two rounds."
ex["@@EX_O2@@"] = "Input `a = -2147483648` and `b = -1`, output 2147483647, because the sum wraps modulo 2^32 and the carry out of column 31 is discarded."

assert add_str("111", "1") == "1000" and add_str_cols("111", "1") == "1000"
ex["@@EX_R1@@"] = "Input `x = \"111\"` and `y = \"1\"`, output `\"1000\"`, because the carry runs through all three columns and adds a leading digit."
assert add_str_cols("0", "000").lstrip('0') == '' and add_str("0", "000") == "0"
ex["@@EX_R2@@"] = "Input `x = \"0\"` and `y = \"000\"`, output `\"0\"`, because leading zeros in the inputs are dropped and the zero sum keeps one digit."

fill(CH, NAME, trace_words(), "@@TRACE1@@")
fill(CH, NAME, trace_string(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
