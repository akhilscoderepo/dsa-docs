<!-- lesson-kind: standard -->
<!-- lesson-id: gcd-and-power -->
## GCD And Power

<!-- stage: context -->
### Why Big Divisors And Big Exponents Stall

A job scheduler runs one task every 1,071 seconds and another every 462 seconds. Both start together, and the operator asks when they next start together again. The answer needs the greatest common divisor of the two periods, which is the largest integer that divides both. A fraction library has the same need, because it reduces 1,071 over 462 by dividing both numbers by that divisor.

A growth model has a different need. It multiplies a value by a constant factor once per step, and the step count can reach two billion. The program must produce a power of the factor, and it must finish in a fraction of a second. This lesson asks how a program finds a common divisor and a large power in steps that follow the number of digits and not the size of the values.

<!-- stage: naive -->
### Trying Every Divisor And Every Multiplication

The direct method for the divisor tries every candidate from the smaller input down to 1. The first candidate that divides both numbers is the answer. The direct method for the power multiplies the base into a result once for each unit of the exponent.

```java
static int gcdByTrial(int a, int b) {
    for (int d = Math.min(a, b); d >= 1; d--) {
        if (a % d == 0 && b % d == 0) {
            return d;                      // the first hit from above is the largest
        }
    }
    return Math.max(a, b);                 // one input is zero, so the other one is the divisor
}

static double powByLoop(double x, int n) {
    double result = 1.0;
    for (int i = 0; i < n; i++) {
        result *= x;                       // one multiplication per unit of the exponent
    }
    return result;
}
```

Both methods are easy to check by hand, and both give correct answers on small inputs.

<!-- stage: bottleneck -->
### Both Loops Cost O(n) In The Value

```predict
The numbers 2,000,000,000 and 1,999,999,999 have the greatest common divisor 1. About how many candidates does gcdByTrial test? How many multiplications does powByLoop run for n = 2,000,000,000?

About two billion for each. The trial search starts at 1,999,999,999 and finds a divisor only at 1, so it tests almost every candidate. The power loop runs once per unit of n. The cost follows the size of the value, not the length of its binary form.
```

#### Count The Candidates

The trial search costs O(min(a, b)) divisions, and each division is a slow instruction. For inputs near 2 * 10^9 the search runs billions of iterations, which takes many seconds. A program that reduces a million fractions cannot afford it.

#### Count The Multiplications

The power loop costs O(n) multiplications. For n near 2 * 10^9 it again runs billions of iterations. Both loops treat a 31-bit input as if it were a count of items. A faster method must make progress proportional to the number of bits, which is about 31 steps, and must throw away a large share of the problem at every step.

<!-- stage: insight -->
### Shrink The Problem By Half Each Step

#### Replace The Pair By A Remainder

The **remainder** of `a` divided by `b` is the value `r` in `a = q * b + r` with `0 <= r < b`, and Java writes it as `a % b`. Every common divisor of `a` and `b` divides `r = a - q * b`. Every common divisor of `b` and `r` divides `a = q * b + r`. The two pairs share exactly the same common divisors, so `gcd(a, b)` equals `gcd(b, a % b)`. The **Euclidean algorithm** applies that replacement until the second value is 0. Then `gcd(a, 0)` equals `a`, because every integer divides 0.

<!-- names: Euclidean algorithm, binary exponentiation, accumulated result -->

#### Why The Replacement Is Fast

The remainder is always smaller than `b`, so the second value strictly decreases and the loop ends. A stronger fact holds. After two replacements the larger value is at most half of the old larger value. So the loop runs O(log min(a, b)) times, and for 31-bit inputs it runs at most about 45 times.

#### Square The Base While Halving The Exponent

**Binary exponentiation** computes `x^n` from the binary digits of `n`. An even exponent gives `x^n = (x * x)^(n / 2)`. An odd exponent gives `x^n = x * x^(n - 1)`. The method keeps three values. The `base` starts as `x` and is squared in every round. The exponent `e` starts as `n` and loses its lowest bit in every round. The **accumulated result** starts as 1 and multiplies by `base` whenever the lowest bit of `e` is 1.

The invariant is that `result * base^e` always equals `x^n`. At the start it holds because `result` is 1, `base` is `x` and `e` is `n`. When `e` is odd, moving one factor of `base` into `result` keeps the product. When `e` is halved, squaring `base` keeps the product. The loop ends at `e = 0`, where `base^e` is 1 and `result` equals `x^n`. It runs once per bit of `n`, which is O(log n) multiplications.

<!-- stage: variables -->
### Quantities Each Loop Holds

The Euclidean loop holds these values.

- **a** is the larger value in the pair, and it receives the old `b` each round.
- **b** is the smaller value in the pair, and it receives `a % b` each round.
- **r** is the temporary remainder, saved before the pair changes.

The power loop holds these values.

- **base** is the current repeated square of the input, and it is squared in every round.
- **e** is the exponent that remains, held as a `long` so that negating an `int` exponent cannot overflow.
- **result** is the accumulated result, which collects the factors of `base` that the bits of `e` select.

The test `(e & 1) == 1` reads the lowest bit and `e >>= 1` removes it. Both are safe here because `e` is never negative. The Euclidean loop works with non-negative values, so its `%` never returns a negative remainder. A signed input first becomes non-negative with `Math.abs` after widening to `long`, because `Math.abs(Integer.MIN_VALUE)` stays negative.

<!-- stage: trace -->
### Follow One Divisor And One Power

#### Reduce 1071 And 462

The cells hold the sequence of values that the pair visits. The pointer `a` marks the larger value and the pointer `b` marks the smaller value. The first step takes 1071 divided by 462, which leaves 147. The pair becomes 462 and 147. The next remainder is 21, and then 147 divided by 21 leaves 0. The pair is now 21 and 0, so the loop stops with 21.

```trace
{"cells":[1071,462,147,21,0],"pointers":["a","b"],"steps":[{"at":{"a":0,"b":1},"vars":{"a":1071,"b":462},"note":"The pair starts as 1071 and 462. The second value is not 0, so another replacement follows."},{"at":{"a":1,"b":2},"vars":{"a":462,"b":147},"note":"The remainder is 147. The pair becomes 462 and 147, which has the same common divisors."},{"at":{"a":2,"b":3},"vars":{"a":147,"b":21},"note":"The remainder is 21. The pair becomes 147 and 21, which has the same common divisors."},{"at":{"a":3,"b":4},"vars":{"a":21,"b":0},"note":"The remainder is 0. The pair becomes 21 and 0, so the loop stops and the answer is 21."}]}
```

#### Raise 3 To The Thirteenth Power

The exponent 13 is `1101` in binary. The cells below hold its bits from lowest to highest. A bit of 1 means the result multiplies by the current `base`, and a bit of 0 skips that multiplication. The base is squared after every bit.

```trace
{"cells":[1,0,1,1],"pointers":["bit"],"steps":[{"at":{"bit":-1},"vars":{"base":3,"result":1,"e":13},"note":"Nothing is read yet. The result is 1, the base is 3 and the exponent is 13."},{"at":{"bit":0},"vars":{"base":9,"result":3,"e":6},"note":"Bit 0 of 13 is 1, so the result multiplies by the old base and becomes 3. The base squares to 9 and the exponent drops to 6."},{"at":{"bit":1},"vars":{"base":81,"result":3,"e":3},"note":"Bit 1 of 13 is 0, so the result stays 3. The base squares to 81 and the exponent drops to 3."},{"at":{"bit":2},"vars":{"base":6561,"result":243,"e":1},"note":"Bit 2 of 13 is 1, so the result multiplies by the old base and becomes 243. The base squares to 6561 and the exponent drops to 1."},{"at":{"bit":3},"vars":{"base":43046721,"result":1594323,"e":0},"note":"Bit 3 of 13 is 1, so the result multiplies by the old base and becomes 1594323. The base squares to 43046721 and the exponent drops to 0."}]}
```

The hardest step is the second one. The bit is 0, so the result stays 3, but the base still squares from 9 to 81. The later bits need that square, because the third bit selects 81 and the fourth bit selects 6561.

<!-- stage: code -->
### Implement Divisor, Power And Common Multiple

```java
final class NumberTools {
    static long gcd(long a, long b) {
        a = Math.abs(a);                         // the divisor ignores signs
        b = Math.abs(b);
        while (b != 0) {
            long r = a % b;                      // r < b, so the pair strictly shrinks
            a = b;
            b = r;
        }
        return a;                                // gcd(a, 0) is a, and gcd(0, 0) is 0
    }

    static double power(double x, int n) {
        long e = n;                              // widen first, so -Integer.MIN_VALUE is safe
        if (e < 0) {
            x = 1.0 / x;                         // a negative exponent inverts the base
            e = -e;
        }
        double result = 1.0;
        while (e > 0) {
            if ((e & 1) == 1) result *= x;       // this bit of the exponent selects the current base
            x *= x;                              // the next bit has twice the weight
            e >>= 1;                             // e is non-negative, so the shift is safe
        }
        return result;
    }

    static long lcm(long a, long b) {
        if (a == 0 || b == 0) return 0;
        return Math.abs(a / gcd(a, b) * b);      // divide first, so the product stays near its final size
    }
}
```

The method `gcd` returns a non-negative value for any inputs, with 0 only for two zeros. The method `power` reads the lowest bit with `&` and drops it with `>>=`. Both operations are cheap, and the loop runs once per bit of `n`. The method `lcm` divides before multiplying. The product `a * b` can be as large as the square of the inputs, while `a / gcd * b` is exactly the least common multiple, which is the smallest positive integer that both inputs divide. The least common multiple can need twice as many bits as one input, so `int` inputs need a `long` result.

<!-- stage: applicability -->
### When Remainders And Squares Apply

#### Recognize The Pattern

Look for divisibility questions such as reducing a ratio, finding a shared period or testing whether two numbers share a factor. Look also for a power with a large exponent, or an operation that composes with itself many times. The invariant for the first family is that each step keeps the set of common divisors unchanged. The invariant for the second family is that the product of the accumulated result and the remaining power stays equal to the target.

#### Watch For The Nearest False Friend

`Math.pow` is a false friend when an exact integer answer is required. It returns a `double`, which holds only 53 bits of precision, so results above 2^53 lose low digits. Multiplying `a * b` before dividing by the gcd is the second false friend for the least common multiple. The product overflows `int` for inputs above 46,340, even when the true least common multiple is small.

#### Avoid The Java Number Traps

Negating an `int` exponent fails for `Integer.MIN_VALUE`, because its negation is itself. Widen to `long` before negating. The remainder operator `%` returns a negative value when the left side is negative, so reduce signs before the loop. Zero needs a defined answer, which is `gcd(a, 0) = a`, `gcd(0, 0) = 0` and `x^0 = 1` for every `x`. Use `>>` only on values already known to be non-negative, or use `>>>` for unsigned shifts of `int` values.

<!-- stage: exercises -->
### Exercises

#### [Build] Euclidean GCD (Author exercise)
<!-- id: bt08-euclid-gcd -->

**Prerequisites.** The remainder step from this lesson.

**Problem.** Given two non-negative integers `a` and `b`, return their greatest common divisor, which is the largest integer that divides both. Repeatedly replace the pair `(a, b)` with `(b, a % b)` until the second value is 0.

**Constraints.** Limits:
- **`a` and `b`** are `int` values with `0 <= a, b <= 2^31 - 1`.
- **Zero** is allowed, with `gcd(a, 0) = a` and `gcd(0, 0) = 0`.
- **Return** is an `int`.

**Example 1.** Input `a = 1071` and `b = 462`, output 21, after the pairs (462, 147), (147, 21) and (21, 0).

**Example 2.** Input `a = 0` and `b = 9`, output 9, because every integer divides 0 and the first replacement already gives `(9, 0)`.

**Hint.** What does the loop return when the second value reaches 0?

**Changed decision.** Baseline case: replaces the pair by the second value and the remainder.

#### [Vary] Integer Power (LeetCode 50)
<!-- id: bt08-integer-power -->

**Prerequisites.** The Euclidean exercise above and the power loop from this lesson.

**Problem.** Given an integer `x` and a non-negative integer `n`, return `x` raised to the power `n` as a `long`. Square the base while halving the exponent. This version differs from LeetCode 50, which takes a `double` base and a signed exponent. Here the base and the result are exact integers, and `x^0` equals 1.

**Constraints.** Limits:
- **`x`** is an `int` with `-1000 <= x <= 1000`.
- **`n`** is an `int` with `0 <= n <= 10^9`.
- **Result** fits in a `long`, and the inputs guarantee it.
- **Return** is a `long`.

**Example 1.** Input `x = 3` and `n = 13`, output 1594323, which multiplies the bases 3, 81 and 6561 selected by the set bits of 13.

**Example 2.** Input `x = -2` and `n = 63`, output -9223372036854775808, because the base squares past the `long` range after the last needed bit and that value is never used.

**Hint.** Which value does the loop keep when a bit of the exponent is 0?

**Changed decision.** The base becomes an exact integer, so the result must be tracked in `long` arithmetic with no rounding.

#### [Boundary] Zero And MIN Exponent (Author exercise)
<!-- id: bt08-zero-min-exponent -->

**Prerequisites.** The two exercises above.

**Problem.** Given a finite `double` base `x` and any `int` exponent `n`, return `x` raised to the power `n` as a `double`. A negative exponent means the reciprocal of the positive power. The exponent may be `Integer.MIN_VALUE`. Follow Java `double` arithmetic for overflow, underflow and division by zero.

**Constraints.** Limits:
- **`x`** is a finite `double`, which may be 0.0.
- **`n`** is an `int` over the full range, including 0 and `Integer.MIN_VALUE`.
- **Zero exponent** returns 1.0 for every `x`, including 0.0.
- **Return** is a `double`, and a value beyond the double range becomes infinity or 0.0.

**Example 1.** Input `x = 2.0` and `n = -3`, output 0.125, because the method inverts the base and raises it to the power 3.

**Example 2.** Input `x = -1.0` and `n = -2147483648`, output 1.0, because the exponent is even, and the widened value 2147483648 stays positive.

**Hint.** What is the value of `-n` when `n` is `Integer.MIN_VALUE`, and which type avoids that?

**Changed decision.** The exponent now includes 0 and the one `int` whose negation overflows.

#### [Recognize] LCM Safely (Author exercise)
<!-- id: bt08-safe-lcm -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `nums` of positive integers, return the least common multiple of all elements, which is the smallest positive integer divisible by every element. If that value is greater than 10^18, return -1. Divide by the gcd before multiplying at every step.

**Constraints.** Limits:
- **Length** of `nums` is an `int` with `1 <= length <= 10^5`.
- **Elements** are `int` values with `1 <= nums[i] <= 10^9`.
- **Return** is a `long`, either the least common multiple or -1.
- **Mutation** of `nums` is not allowed.

**Example 1.** Input `nums = [4, 6, 10]`, output 60, from the running values 4, 12 and 60.

**Example 2.** Input `nums = [1000000000, 999999999, 999999998]`, output -1, because the first two elements give 999999999000000000 and the third element pushes the value past 10^18.

**Hint.** Before multiplying the running value by the next element, which comparison shows the product would pass 10^18?

**Changed decision.** The running value can grow past `long`, so each step checks the limit before it multiplies.
