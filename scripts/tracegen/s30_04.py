import sys, pathlib, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill
from collections import Counter

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '04-xor-cancellation.md'

def single(nums):
    a = 0
    for v in nums: a ^= v
    return a

def single_brute(nums):
    return [v for v, c in Counter(nums).items() if c == 1][0]

def missing(a, lo):
    acc = lo + len(a)
    for i, v in enumerate(a): acc ^= (lo + i) ^ v
    return acc

def missing_brute(a, lo):
    return [v for v in range(lo, lo + len(a) + 1) if v not in set(a)][0]

def odd(nums):
    return single(nums)

def odd_brute(nums):
    return [v for v, c in Counter(nums).items() if c % 2][0]

def two(nums):
    d = single(nums)
    s = d & -d
    p = 0
    for v in nums:
        if v & s: p ^= v
    return sorted([p, d ^ p])

def two_brute(nums):
    return sorted(v for v, c in Counter(nums).items() if c == 1)

rnd = random.Random(40)
for _ in range(2000):
    n = rnd.randint(0, 12); lo = rnd.randint(-30, 30); gap = rnd.randint(0, n)
    a = [v for v in range(lo, lo + n + 1) if v != lo + gap]; rnd.shuffle(a)
    assert missing(a, lo) == missing_brute(a, lo) == lo + gap
    vals = rnd.sample(range(-20, 20), 8)
    arr = [vals[0]] * (1 + 2 * rnd.randint(0, 2)) + [v for v in vals[1:4] for _ in (0, 1)]
    assert odd(arr) == odd_brute(arr) == vals[0]
    arr2 = [vals[0], vals[1]] + [v for v in vals[2:6] for _ in (0, 1)]
    assert two(arr2) == two_brute(arr2)

def trace1():
    nums = [4, 1, 2, 1, 2]
    acc = 0
    steps = [{"at": {"i": -1}, "vars": {"acc": 0}, "note": "The accumulator starts at 0, the identity for the exclusive or."}]
    seen = set()
    for i, v in enumerate(nums):
        acc ^= v
        again = v in seen; seen.add(v)
        steps.append({"at": {"i": i}, "vars": {"acc": acc, "binary": format(acc, "03b")},
                      "note": f"The id {v} is read " + ("a second time, so it cancels its first copy." if again else "for the first time, so it enters the accumulator.") + f" The accumulator is {acc}."})
    assert acc == single(nums) == single_brute(nums) == 4
    return block(nums, ["i"], steps)

def trace2():
    a = [3, 0, 4, 1]; n = len(a)
    acc = n
    steps = [{"at": {"i": -1}, "vars": {"acc": acc}, "note": f"The accumulator starts at n = {n}, the number that has no index."}]
    for i, v in enumerate(a):
        acc ^= i ^ v
        steps.append({"at": {"i": i}, "vars": {"acc": acc},
                      "note": f"The step combines the index {i} and the element {v}. The accumulator is {acc}."})
    assert acc == missing(a, 0) == missing_brute(a, 0) == 2
    steps[-1]["note"] += " The loop ends with the missing number 2."
    return block(a, ["i"], steps)

def fmt(v):
    import json
    return json.dumps(v, separators=(",", ":"))

ex = {}
b1 = [9, -3, 7, 9, 7]; assert single(b1) == single_brute(b1) == -3
b2 = [42]; assert single(b2) == 42
ex["@@EX_B1@@"] = f"Input `nums = {fmt(b1)}`, output -3, because the pairs of 9 and of 7 cancel."
ex["@@EX_B2@@"] = f"Input `nums = {fmt(b2)}`, output 42, since a single element has no pair to cancel."
v1 = ([7, 5, 8, 6], 5); v2 = ([-2, 0, 2, 1], -2)
assert missing(*v1) == missing_brute(*v1) == 9 and missing(*v2) == missing_brute(*v2) == -1
ex["@@EX_V1@@"] = f"Input `lo = 5` and `a = {fmt(v1[0])}`, output 9, because the range 5 to 9 lacks its top value."
ex["@@EX_V2@@"] = f"Input `lo = -2` and `a = {fmt(v2[0])}`, output -1, because the range -2 to 2 lacks a negative value in the middle."
x1 = [0, 0, 0]; x2 = [-5, 3, -5, 3, -5]
assert odd(x1) == odd_brute(x1) == 0 and odd(x2) == odd_brute(x2) == -5
ex["@@EX_X1@@"] = f"Input `nums = {fmt(x1)}`, output 0, because 0 has an odd count of 3 and is a valid answer."
ex["@@EX_X2@@"] = f"Input `nums = {fmt(x2)}`, output -5, because -5 appears three times and 3 appears twice."
r1 = [6, 2, 9, 6, 4, 2]; r2 = [-1, 5, -1, 0]
assert two(r1) == two_brute(r1) == [4, 9] and two(r2) == two_brute(r2) == [0, 5]
ex["@@EX_R1@@"] = f"Input `nums = {fmt(r1)}`, output {fmt(two(r1))}, because 4 and 9 appear once and the pairs 6 and 2 cancel."
ex["@@EX_R2@@"] = f"Input `nums = {fmt(r2)}`, output {fmt(two(r2))}, because the single values are 0 and 5 and the pair -1 cancels."

fill(CH, NAME, trace1(), "@@TRACE1@@")
fill(CH, NAME, trace2(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
