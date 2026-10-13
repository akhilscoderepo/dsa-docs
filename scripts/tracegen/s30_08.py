import sys, pathlib, random, math
from functools import reduce
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import block, fill

CH = '30-bits-number-theory-and-interview-numerics'
NAME = '08-gcd-and-power.md'
LIMIT = 10**18

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def power(x, n):
    res, e = 1, n
    while e:
        if e & 1: res *= x
        x *= x; e >>= 1
    return res

def safe_lcm(nums):
    l = 1
    for v in nums:
        g = gcd(l, v)
        if l // g > LIMIT // v:
            return -1
        l = l // g * v
    return l

def lcm_brute(nums):
    l = reduce(lambda a, b: a * b // math.gcd(a, b), nums)
    return -1 if l > LIMIT else l

rng = random.Random(3008)
for _ in range(3000):
    a = rng.randint(0, 10**rng.randint(1, 9)); b = rng.randint(0, 10**rng.randint(1, 9))
    assert gcd(a, b) == math.gcd(a, b)
    x = rng.randint(-6, 6); n = rng.randint(0, 20)
    assert power(x, n) == x ** n
    nums = [rng.randint(1, 10**rng.choice([1, 2, 5, 9])) for _ in range(rng.randint(1, 5))]
    assert safe_lcm(nums) == lcm_brute(nums), nums

def trace_gcd():
    a, b = 1071, 462
    seq = [a, b]
    steps = [{"at": {"a": 0, "b": 1}, "vars": {"a": a, "b": b}, "note": "The pair starts as 1071 and 462. The second value is not 0, so another replacement follows."}]
    i = 0
    while b:
        r = a % b
        seq.append(r)
        i += 1
        a, b = b, r
        if b:
            note = f"The remainder is {r}. The pair becomes {a} and {b}, which has the same common divisors."
        else:
            note = f"The remainder is 0. The pair becomes {a} and 0, so the loop stops and the answer is {a}."
        steps.append({"at": {"a": i, "b": i + 1}, "vars": {"a": a, "b": b}, "note": note})
    assert a == 21 == math.gcd(1071, 462) and seq == [1071, 462, 147, 21, 0]
    return block(seq, ["a", "b"], steps)

def trace_pow():
    x, n = 3, 13
    bits = [(n >> k) & 1 for k in range(4)]
    assert bits == [1, 0, 1, 1]
    base, res, e = x, 1, n
    steps = [{"at": {"bit": -1}, "vars": {"base": base, "result": res, "e": e}, "note": "Nothing is read yet. The result is 1, the base is 3 and the exponent is 13."}]
    for k in range(4):
        assert res * base ** e == x ** n
        bit = e & 1
        if bit: res *= base
        base *= base; e >>= 1
        note = (f"Bit {k} of 13 is {bit}, so the result " + (f"multiplies by the old base and becomes {res}." if bit else f"stays {res}.")
                + f" The base squares to {base} and the exponent drops to {e}.")
        steps.append({"at": {"bit": k}, "vars": {"base": base, "result": res, "e": e}, "note": note})
    assert res == 3 ** 13 == 1594323 and e == 0
    return block(bits, ["bit"], steps)

ex = {}
assert gcd(1071, 462) == 21 and gcd(0, 9) == 9 and gcd(0, 0) == 0
ex["@@EX_B1@@"] = "Input `a = 1071` and `b = 462`, output 21, after the pairs (462, 147), (147, 21) and (21, 0)."
ex["@@EX_B2@@"] = "Input `a = 0` and `b = 9`, output 9, because every integer divides 0 and the first replacement already gives `(9, 0)`."

assert power(3, 13) == 1594323 and power(-2, 63) == -2**63 and power(7, 0) == 1
ex["@@EX_V1@@"] = "Input `x = 3` and `n = 13`, output 1594323, from the factors 3, 81, 6561 and 43046721 selected by the bits of 13... "
ex["@@EX_V1@@"] = "Input `x = 3` and `n = 13`, output 1594323, which multiplies the bases 3, 81 and 6561 selected by the set bits of 13."
assert 3 * 81 * 6561 == 3 ** 13
ex["@@EX_V2@@"] = "Input `x = -2` and `n = 63`, output -9223372036854775808, because the base squares past the `long` range after the last needed bit and that value is never used."

ex["@@EX_O1@@"] = "Input `x = 2.0` and `n = -3`, output 0.125, because the method inverts the base and raises it to the power 3."
assert 0.5 ** 3 == 0.125
ex["@@EX_O2@@"] = "Input `x = -1.0` and `n = -2147483648`, output 1.0, because the exponent is even, and the widened value 2147483648 stays positive."

assert safe_lcm([4, 6, 10]) == 60
l = safe_lcm([10**9, 999999999, 999999998]); assert l == -1 and lcm_brute([10**9, 999999999, 999999998]) == -1
assert safe_lcm([10**9, 999999999]) == 999999999 * 10**9
ex["@@EX_R1@@"] = "Input `nums = [4, 6, 10]`, output 60, from the running values 4, 12 and 60."
ex["@@EX_R2@@"] = "Input `nums = [1000000000, 999999999, 999999998]`, output -1, because the first two elements give 999999999000000000 and the third element pushes the value past 10^18."

fill(CH, NAME, trace_gcd(), "@@TRACE1@@")
fill(CH, NAME, trace_pow(), "@@TRACE2@@")
for k, v in ex.items():
    fill(CH, NAME, v, k)
print("ok")
