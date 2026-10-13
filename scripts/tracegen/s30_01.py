import sys, pathlib, random, json
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '01-bit-masks.md'

# ---------- algorithms and brute force oracles ----------
def flag_ops(flags, ops):
    cnt = 0
    for code, p in ops:
        b = 1 << p
        if code == 0:
            cnt += 1 if (flags & b) != 0 else 0
        elif code == 1:
            flags |= b
        elif code == 2:
            flags &= ~b
        else:
            flags ^= b
    return [flags, cnt]

def flag_brute(flags, ops):
    bits = [(flags >> i) & 1 for i in range(31)]
    cnt = 0
    for code, p in ops:
        if code == 0: cnt += bits[p]
        elif code == 1: bits[p] = 1
        elif code == 2: bits[p] = 0
        else: bits[p] ^= 1
    return [sum(v << i for i, v in enumerate(bits)), cnt]

BIT = {"READ": 0, "WRITE": 1, "EXECUTE": 2, "DELETE": 3, "ADMIN": 4}
def perm_mask(g, r, need):
    m = 0
    for s in g: m |= 1 << BIT[s]
    for s in r: m &= ~(1 << BIT[s])
    q = 0
    for s in need: q |= 1 << BIT[s]
    return (m & q) == q

def perm_brute(g, r, need):
    have = set(g) - set(r)
    return all(s in have for s in need)

def to_signed64(v):
    v &= (1 << 64) - 1
    return v - (1 << 64) if v >> 63 else v

def width_mask(ps):
    m = 0
    for p in ps: m |= 1 << p
    return to_signed64(m)

def width_brute(ps):
    return to_signed64(sum(1 << p for p in set(ps)))

def pairs_mask(words):
    ms = []
    for w in words:
        m = 0
        for c in w: m |= 1 << (ord(c) - 97)
        ms.append(m)
    return sum(1 for i in range(len(ms)) for j in range(i + 1, len(ms)) if ms[i] & ms[j] == 0)

def pairs_brute(words):
    return sum(1 for i in range(len(words)) for j in range(i + 1, len(words)) if not (set(words[i]) & set(words[j])))

rng = random.Random(3001)
names = list(BIT)
for _ in range(500):
    f = rng.randint(0, 2 ** 31 - 1)
    ops = [(rng.randint(0, 3), rng.randint(0, 30)) for _ in range(rng.randint(0, 12))]
    assert flag_ops(f, ops) == flag_brute(f, ops)
    g = [rng.choice(names) for _ in range(rng.randint(0, 6))]
    r = [rng.choice(names) for _ in range(rng.randint(0, 4))]
    nd = [rng.choice(names) for _ in range(rng.randint(0, 3))]
    assert perm_mask(g, r, nd) == perm_brute(g, r, nd)
    ps = [rng.randint(0, 63) for _ in range(rng.randint(0, 8))]
    assert width_mask(ps) == width_brute(ps)
    ws = ["".join(rng.choice("abcdefgh") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(0, 7))]
    assert pairs_mask(ws) == pairs_brute(ws)

# ---------- traces ----------
def trace_flags():
    flags = 5
    cells = [(flags >> i) & 1 for i in range(8)]
    steps = [{"at": {"b": -1}, "vars": {"flags": flags}, "note": "The starting value is 5, so bits 0 and 2 are set and no operation has run."}]
    plan = [(1, 3, "Setting bit 3 ORs the value with 8"), (2, 0, "Clearing bit 0 ANDs the value with the complement of 1"),
            (3, 2, "Toggling bit 2 XORs the value with 4"), (0, 3, "Testing bit 3 ANDs the value with 8")]
    for code, p, txt in plan:
        b = 1 << p
        if code == 1: flags |= b
        elif code == 2: flags &= ~b
        elif code == 3: flags ^= b
        if code == 0:
            res = flags & b
            assert res != 0
            note = f"{txt}. The result is {res}, which is not 0, so the answer is yes."
            v = {"flags": flags, "test": res}
        else:
            note = f"{txt}. The value is now {flags}."
            v = {"flags": flags}
        steps.append({"at": {"b": p}, "vars": v, "note": note})
    assert flags == 8
    return block(cells, ["b"], steps)

def trace_word():
    word = "abca"
    cells = [ord(c) - 97 for c in word]
    mask = 0
    steps = [{"at": {"i": -1}, "vars": {"mask": 0}, "note": "The mask starts at 0, so no letter has been seen."}]
    seen = set()
    for i, c in enumerate(word):
        mask |= 1 << cells[i]
        again = cells[i] in seen
        seen.add(cells[i])
        note = f"The letter at position {cells[i]} " + ("is already set, so the OR leaves the mask unchanged" if again else f"sets bit {cells[i]}") + f". The mask is {mask}."
        steps.append({"at": {"i": i}, "vars": {"mask": mask}, "note": note})
    assert mask == 7 and (7 & 8) == 0
    return block(cells, ["i"], steps)

def fmt(v):
    return json.dumps(v, separators=(",", ":"))

def b(v): return "`true`" if v else "`false`"

ex = {}
o1 = [(1, 3), (2, 0), (3, 2), (0, 3)]; r1 = flag_ops(5, o1); assert r1 == flag_brute(5, o1) == [8, 1]
o2 = [(2, 5), (0, 5), (3, 30), (3, 30), (0, 30)]; r2 = flag_ops(0, o2); assert r2 == flag_brute(0, o2) == [0, 0]
ex["@@EX_A1@@"] = f"Input `flags = 5` and operations {fmt([list(o) for o in o1])}, output {fmt(r1)}, because the value goes 13, 12, 8 and the final test finds bit 3 set."
ex["@@EX_A2@@"] = f"Input `flags = 0` and operations {fmt([list(o) for o in o2])}, output {fmt(r2)}, because clearing a clear bit changes nothing and toggling bit 30 twice restores it."

g1, rv1 = ["READ", "WRITE", "DELETE"], ["DELETE"]
n1, n1b = ["READ", "WRITE"], ["READ", "DELETE"]
assert perm_mask(g1, rv1, n1) is True and perm_brute(g1, rv1, n1) is True
assert perm_mask(g1, rv1, n1b) is False and perm_brute(g1, rv1, n1b) is False
ex["@@EX_P1@@"] = f"Input `grants = {fmt(g1)}`, `revokes = {fmt(rv1)}` and `required = {fmt(n1)}`, output {b(True)}. With `required = {fmt(n1b)}` the output is {b(False)}, because `DELETE` was revoked."
g2, n2 = ["READ"], ["READ", "WRITE"]
assert perm_mask(g2, [], n2) is False and perm_brute(g2, [], n2) is False
ex["@@EX_P2@@"] = f"Input `grants = {fmt(g2)}`, `revokes = []` and `required = {fmt(n2)}`, output {b(False)}, because the user owns `READ` but not `WRITE`, so a test for any shared bit would wrongly say yes."

w1 = [0, 40, 63]; assert width_mask(w1) == width_brute(w1)
w2 = [32, 32]; assert width_mask(w2) == 4294967296 == width_brute(w2)
ex["@@EX_W1@@"] = f"Input `{fmt(w1)}`, output `{width_mask(w1)}`, because position 63 is the sign digit of a `long`, so the result is negative."
ex["@@EX_W2@@"] = f"Input `{fmt(w2)}`, output `{width_mask(w2)}`, because the duplicate sets position 32 once, and the form `1 << 32` would give 1 instead."

d1 = ["abc", "de", "cf", "ghi"]; assert pairs_mask(d1) == pairs_brute(d1) == 5
d2 = ["aa", "aa", "b"]; assert pairs_mask(d2) == pairs_brute(d2) == 2
ex["@@EX_D1@@"] = f"Input `{fmt(d1)}`, output {pairs_mask(d1)}, because only the pair `abc` and `cf` shares a letter among the six pairs."
ex["@@EX_D2@@"] = f"Input `{fmt(d2)}`, output {pairs_mask(d2)}, because each `aa` is disjoint from `b`, and the two equal words share the letter `a`."

fill(CH, NAME, trace_flags(), "@@TRACE1@@")
fill(CH, NAME, trace_word(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
