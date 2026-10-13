<!-- lesson-kind: standard -->
<!-- lesson-id: modular-arithmetic -->
## Modular Arithmetic

<!-- stage: context -->
### Why Large Counts Need A Modulus

A counting problem asks for the number of valid arrangements of 100,000 items. The true count has hundreds of thousands of digits, and no `long` can hold it. The statement therefore asks for the answer modulo 1,000,000,007. A hashing routine has a similar need, since it folds a long input into a number of fixed width.

A program that multiplies first and reduces last gets a wrong answer without any warning. Java does not throw when a `long` product passes its range. The question for this lesson is how a program keeps every intermediate value small while the final answer stays exact.

The **remainder** of `a` divided by `m` is the value `a % m` in Java for positive operands. Two integers `a` and `b` are **congruent** modulo `m` when `m` divides `a - b`. Reduction keeps the answer in the residue class that the statement asks for.

<!-- stage: naive -->
### Multiplying Everything Before Reducing

The direct approach computes the full sum and the full product in one `long` each and takes the remainder at the end. The method below returns the sum and the product of an array modulo `m`.

```java
static long[] sumAndProductLate(int[] a, int m) {
    long sum = 0;
    long product = 1;
    for (int v : a) {
        sum += v;                  // grows without any reduction
        product *= v;              // grows much faster than the sum
    }
    return new long[]{sum % m, product % m};   // reduces only once, at the very end
}
```

For a short array of small numbers this method works, because the totals fit in a `long`. The reduction at the end is the only place where `m` appears.

<!-- stage: bottleneck -->
### The Product Outgrows Sixty-Four Bits

```predict
An array holds 20 copies of the number 1,000,000,000. The method above multiplies them in a long. The true product is 10^180, and a long holds at most about 9.2 * 10^18. What does the method return?

It returns a number that looks valid but is wrong. Java wraps the product around the range of long without a warning, and the final remainder is taken from the wrapped value. The result is not the product modulo m.
```

#### Count The Digits

The true product of `n` numbers near 10^9 has about 9n digits, so the exact value needs O(n) digits and each multiplication on such a number costs O(n). Computing the exact product with `BigInteger` therefore costs O(n^2) time for the whole array. A `long` has only 19 digits. Two numbers of size 10^9 multiply to 10^18, which still fits, and the third factor makes the product overflow.

#### Locate The Silent Failure

The failure is silent. Addition also overflows, but later, after about 9 billion terms of size 10^9. Java wraps the value in two's complement arithmetic, which is a remainder modulo 2^64 and not modulo `m`. The wrapped number has no relation to the answer. A correct method must reduce while the numbers are still small, so that no intermediate value passes the range of `long`.

<!-- stage: insight -->
### Reduce After Every Step

#### Keep The Congruence After Each Operation

Reduction is allowed after every addition and multiplication, because it preserves congruence. If `a` and `a'` are congruent modulo `m`, and `b` and `b'` are congruent modulo `m`, then `a + b` is congruent to `a' + b'`, and `a * b` is congruent to `a' * b'`. A program may replace each partial result by its remainder at any moment, and the final remainder is the same as the remainder of the exact value. The invariant is that the running value is always congruent to the exact value and lies in the range 0 to `m - 1`.

<!-- names: congruence, wide product, normalized remainder, power table -->

#### Widen Before Multiplying

A **wide product** is a product computed in `long` from two operands that are already below `m`. With `m` up to 1,000,000,007, each operand is below 2^30, and the product is below 2^60, which fits in a `long` with room to spare. The cast must come before the multiplication. The expression `(long) a * b % m` widens `a` first. The expression `(long) (a * b) % m` multiplies two `int` values first, wraps, and then widens the wrong number.

#### Normalize Negative Remainders

Java's `%` operator returns a result with the sign of its left operand. The expression `-7 % 5` is -2 and not 3. A **normalized remainder** is the value in the range 0 to `m - 1` that is congruent to the input. `Math.floorMod(x, m)` returns it, and so does `((x % m) + m) % m`. A subtraction such as `a - b` can be negative, so its result needs this step before it is stored or compared.

#### Combine Reduction With Binary Exponentiation

Computing `base` raised to `exp` by `exp` multiplications is far too slow for an exponent near 10^18. Binary exponentiation squares the base once per bit of the exponent and multiplies it into the result when the bit is set. Every multiplication is followed by a reduction, so the work is O(log exp) wide products. The method keeps `result` and `base` below `m` throughout.

#### Precompute A Power Table

Some counts need the same power many times, for example `2^k` for many values of `k`. A **power table** holds `pow[i]` for `i` from 0 up to the largest needed index. Each entry is the previous one times 2, reduced. Building it costs O(n) time, and each later lookup costs O(1). When `m` is 1, every entry must be 0, so the first entry is `1 % m` and not the constant 1.

<!-- stage: variables -->
### Quantities The Reductions Track

These five quantities appear across the helpers of lesson 10.

- **m** is the modulus, an `int` with `1 <= m <= 1,000,000,007` in this lesson.
- **sum** and **product** are `long` running values, always reduced into 0 to `m - 1`.
- **base** and **exp** are the operands of a power, where `exp` is a `long` that halves each round.
- **result** is the partial power, and it holds the product of the bases for the set bits so far.
- **pow** is the power table, an `int[]` where `pow[i]` is `2^i` modulo `m`.

A value is called reduced when it lies in the range 0 to `m - 1`. In the second trace, `raw` is the running sum reduced with Java `%` alone, and `norm` is the same sum after normalization.

<!-- stage: trace -->
### Follow One Power And One Running Sum

#### Raise Three To The Thirteenth Power

Take `3^13` modulo 1000. The exponent 13 is `1101` in binary, and the trace reads its bits from the lowest. The bits in that order are 1, 0, 1 and 1. The result starts at 1 and the base starts at 3.

The lowest bit is 1, so the result becomes 3. The base squares to 9. The next bit is 0, so the result stays 3, and the base squares to 81. The third bit is 1, so the result becomes 3 times 81, which is 243. The base squares to 6561, which reduces to 561. The last bit is 1, so the result becomes 243 times 561, which is 136,323 and reduces to 323. The exact value of `3^13` is 1,594,323, whose last three digits are 323.

```trace
{"cells":[1,0,1,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"result":1,"base":3},"note":"The result starts at 1 and the base starts at 3. No bit has been read."},{"at":{"i":0},"vars":{"bit":1,"result":3,"base":9},"note":"Bit 1 is set, so the result becomes 3. The base squares to 9 for the next bit."},{"at":{"i":1},"vars":{"bit":0,"result":3,"base":81},"note":"Bit 0 is clear, so the result stays 3. The base squares to 81 for the next bit."},{"at":{"i":2},"vars":{"bit":1,"result":243,"base":561},"note":"Bit 1 is set, so the result becomes 243. The base squares to 561 for the next bit."},{"at":{"i":3},"vars":{"bit":1,"result":323,"base":721},"note":"Bit 1 is set, so the result becomes 323. The base squares to 721 for the next bit."}]}
```

#### Add Signed Changes Modulo Seven

Take the changes 5, -9, 4, -13 and 8 and the modulus 7. The exact total is -5, and its normalized remainder is 2. The trace keeps two running sums. The first, `raw`, uses `(raw + x) % 7`. The second, `norm`, uses `Math.floorMod(norm + x, 7)`.

After the second change the raw sum is -4, and the normalized sum is 3. Both are congruent, since they differ by 7. The raw sum returns to 0 after the third change. It is negative again at the fourth change, with -6, while the normalized sum is 1. The last change moves both sums to 2. The raw sum is right only when it lands in 0 to 6, and here that happens at the end by luck of the values.

```trace
{"cells":[5,-9,4,-13,8],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"raw":0,"norm":0},"note":"Both sums start at 0. No change has been added."},{"at":{"i":0},"vars":{"raw":5,"norm":5},"note":"The change 5 gives raw 5 and normalized 5."},{"at":{"i":1},"vars":{"raw":-4,"norm":3},"note":"The change -9 gives raw -4 and normalized 3. The raw sum is negative, which is not a valid remainder."},{"at":{"i":2},"vars":{"raw":0,"norm":0},"note":"The change 4 gives raw 0 and normalized 0."},{"at":{"i":3},"vars":{"raw":-6,"norm":1},"note":"The change -13 gives raw -6 and normalized 1. The raw sum is negative, which is not a valid remainder."},{"at":{"i":4},"vars":{"raw":2,"norm":2},"note":"The change 8 gives raw 2 and normalized 2."}]}
```

The hardest step is the third bit of the power. The base then holds 81, which is `3^4`, and the set bit means the result must absorb `3^4`. The result 3 is `3^1`, and the product `3^1 * 3^4` is `3^5`, which matches the low bits 101 read so far.

<!-- stage: code -->
### Implement Modular Helpers

```java
static int addMod(int a, int b, int m) {
    return (int) (((long) a + b) % m);        // a and b are reduced, so the sum is below 2 * m
}

static int mulMod(int a, int b, int m) {
    return (int) ((long) a * b % m);          // widen before multiplying, so no wrap occurs
}

static int subMod(int a, int b, int m) {
    return Math.floorMod((long) a - b, m);    // long difference, normalized into 0..m-1
}

static int powMod(long base, long exp, int m) {
    long result = 1 % m;                      // equals 0 when m is 1
    long b = Math.floorMod(base, (long) m);   // reduce the base before any squaring
    while (exp > 0) {
        if ((exp & 1) == 1) result = result * b % m;   // a set bit multiplies the current power in
        b = b * b % m;                                  // squares for the next bit
        exp >>= 1;                                      // one bit of the exponent is consumed
    }
    return (int) result;
}

static int[] powersOfTwo(int count, int m) {
    int[] pow = new int[count];
    if (count > 0) pow[0] = 1 % m;            // the first entry also respects m = 1
    for (int i = 1; i < count; i++) {
        pow[i] = addMod(pow[i - 1], pow[i - 1], m);   // doubling is one modular addition
    }
    return pow;
}
```

The helpers assume reduced operands, except `powMod`, which reduces its own base. A product of two values below 1,000,000,007 stays below about 1.0 * 10^18, while `Long.MAX_VALUE` is about 9.2 * 10^18. The loop in `powMod` runs once per bit of `exp`, which is at most 63 times. A modulus above 3 * 10^9 would break the product bound, and it also does not fit in `int`.

<!-- stage: applicability -->
### When To Reduce Modulo A Constant

#### Recognize The Pattern

Reach for modular arithmetic when a statement says "return the answer modulo `m`" or when counts and products grow without bound. The invariant to hold in code is that every stored value is reduced into the range 0 to `m - 1` after each addition, subtraction or multiplication. Counting problems with dynamic programming, hashing and combinatorial formulas all follow this cue.

#### Watch For The Nearest False Friend

Comparison is a false friend. A reduced value says nothing about the size of the exact value, so a program cannot test "is the exact total larger than the limit" from a remainder. Division is another false friend, because `a / b` modulo `m` is not the remainder of `a` divided by `b` as integers. Division needs a modular inverse, which is beyond this chapter. For problems that need both size and exactness, keep the size check in `long` or `BigInteger`.

#### Avoid The Java Hazards

Java `%` returns negative results for negative left operands, so subtraction needs `Math.floorMod` or an added `m`. The cast must precede the multiplication, as in `(long) a * b`. When `m` is 1, every answer is 0, so initial values such as 1 become `1 % m`. The result type of `Math.floorMod(long, int)` is `int`, while `Math.floorMod(long, long)` is `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Modular Sum And Product (Author exercise)
<!-- id: bt10-sum-and-product -->

**Prerequisites.** The wide product and the running reduction from this lesson.

**Problem.** Given an array `a` of nonnegative integers and a modulus `m`, return an `int[]` of length 2. The first value is the sum of all elements modulo `m`. The second value is the product of all elements modulo `m`, and the product of an empty array is 1 modulo `m`.

**Constraints.** The limits are:
- **Length** of `a` is an `int` with `0 <= n <= 100,000`.
- **Values** are `int` values with `0 <= a[i] <= 2,147,483,647`.
- **`m`** is an `int` with `1 <= m <= 1,000,000,007`.
- **Return** is `{sum mod m, product mod m}`, and both lie in `0` to `m - 1`.

**Example 1.** Input `a = [1000000000, 999999999, 123456789]` and `m = 1000000007`, output `[123456774, 913580142]`, where the exact product is far above the range of `long`.

**Example 2.** Input `a = []` and `m = 10`, output `[0, 1]`, since the empty sum is 0 and the empty product is 1. With `m = 1` the same input gives `[0, 0]`.

**Hint.** Each element can exceed `m`. Reduce it first, and then decide which operand to cast to `long` before the product.

**Changed decision.** Baseline case: casts to `long` before the product and reduces after every step.

#### [Vary] Modular Fast Power (Author exercise)
<!-- id: bt10-modular-power -->

**Prerequisites.** The exercise above.

**Problem.** Given a base, an exponent and a modulus `m`, return `base` raised to `exp`, modulo `m`. The value `base` raised to 0 is 1 for every base, including 0, and the returned value is reduced modulo `m`.

**Constraints.** The limits are:
- **`base`** is a `long` with `0 <= base <= 10^18`.
- **`exp`** is a `long` with `0 <= exp <= 10^18`.
- **`m`** is an `int` with `1 <= m <= 1,000,000,007`.
- **Return** is an `int` in `0` to `m - 1`.

**Example 1.** Input `base = 2`, `exp = 10` and `m = 1000`, output 24, since 2^10 is 1024.

**Example 2.** Input `base = 10^18`, `exp = 10^18` and `m = 1000000007`, output 504853526. Input `base = 0`, `exp = 0` and `m = 7` gives 1.

**Hint.** The exponent is too large for a loop of `exp` steps. Which operation halves the exponent, and when must the result absorb the current base?

**Changed decision.** The operation changes from one product to a power, so reduction combines with binary exponentiation.

#### [Boundary] Negative Remainder (Author exercise)
<!-- id: bt10-negative-remainder -->

**Prerequisites.** The two exercises above.

**Problem.** Given two integer arrays `a` and `b` of equal length and a modulus `m`, return an `int[]` whose entry `i` is the normalized remainder of `a[i] - b[i]` modulo `m`. A normalized remainder lies in `0` to `m - 1`.

**Constraints.** The limits are:
- **Length** of both arrays is an `int` with `0 <= n <= 100,000`.
- **Values** are any `int`, so each difference can pass the range of `int`.
- **`m`** is an `int` with `1 <= m <= 2,147,483,647`.
- **Return** is an `int[]` of length `n`.

**Example 1.** Input `a = [3, -4, 10]`, `b = [10, 6, 10]` and `m = 5`, output `[3, 0, 0]`, since -7 is congruent to 3 and -10 is congruent to 0.

**Example 2.** Input `a = [-2147483648, 2147483647]`, `b = [2147483647, -2147483648]` and `m = 1000`, output `[705, 295]`, where the first difference is below the range of `int`.

**Hint.** Which type holds `a[i] - b[i]` when the two values are `Integer.MIN_VALUE` and `Integer.MAX_VALUE`, and what sign does `%` give a negative left operand?

**Changed decision.** The difference can be negative or wider than `int`, so the remainder needs widening and normalization.

#### [Recognize] Number of Subsequences That Satisfy the Given Sum Condition (LeetCode 1498)
<!-- id: bt10-subsequence-sum-condition -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums`, an integer `target` and a modulus `m`, count the nonempty subsequences whose minimum plus maximum is at most `target`. A subsequence keeps the original order and may skip elements. Return the count modulo `m`. This version differs from the original statement, because `m` is an input and not the fixed value 1,000,000,007.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `1 <= n <= 100,000`.
- **Values** are `int` values with `1 <= nums[i] <= 1,000,000`.
- **`target`** is an `int` with `1 <= target <= 2,000,000`.
- **`m`** is an `int` with `1 <= m <= 1,000,000,007`.
- **Mutation** of `nums` is allowed, and the order of elements does not change the count.

**Example 1.** Input `nums = [4, 1, 6, 2, 3]`, `target = 7` and `m = 1000`, output 22.

**Example 2.** Input `nums = [3, 3, 6, 8]`, `target = 9` and `m = 1000000007`, output 6. The same input with `m = 1` returns 0.

**Hint.** Plan in three parts. First, build the table `pow[i]` of `2^i` modulo `m` for `i` up to `n`. Second, sort `nums` and set a left pointer `l` at the start and a right pointer `r` at the end. Third, while `l <= r`, test `nums[l] + nums[r] <= target`. If it holds, `nums[l]` is the minimum of `2^(r - l)` subsequences, because each element between the pointers is in or out. Add `pow[r - l]` and move `l` right. Otherwise move `r` left.

**Changed decision.** Powers of two modulo `m` come from a precomputed table, and a modulus of 1 turns every count into 0.
