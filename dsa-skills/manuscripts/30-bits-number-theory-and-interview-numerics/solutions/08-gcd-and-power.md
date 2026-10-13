<!-- solutions-for: 08-gcd-and-power -->
### Solutions For GCD And Power

#### Solution: [Build] Euclidean GCD (Author exercise)
<!-- id: bt08-euclid-gcd -->

**Approach.** The loop replaces the pair `(a, b)` by `(b, a % b)` until `b` is 0, and then returns `a`.

The replacement keeps the set of common divisors unchanged. A common divisor of `a` and `b` divides `a - q * b`, which is the remainder, and a common divisor of `b` and the remainder divides `q * b + remainder`, which is `a`. The remainder is smaller than `b`, so `b` strictly decreases and the loop must end. When `b` is 0, every integer divides it, so the answer is `a`. The case `gcd(0, 0)` returns 0 through the same loop without a branch. Three Java facts apply here: `Math.abs(Integer.MIN_VALUE)` stays negative, `%` keeps the sign of the left side, and 31-bit inputs need at most 44 replacements in the slowest case, which consecutive Fibonacci numbers produce.

**Complexity.**

- **Time** is O(log min(a, b)), because the larger value at least halves every two replacements.
- **Space** is O(1), because the loop keeps two values and one temporary.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class EuclidGcd {
    /**
     * Returns the greatest common divisor of two non-negative ints.
     * Time: O(log min(a, b)), the larger value halves every two replacements.
     * Space: O(1), two values and one temporary.
     * Invariant: gcd(a, b) is the same before and after every replacement.
     */
    static int gcd(int a, int b) {
        // The loop continues while the second value is nonzero.
        while (b != 0) {
            // The remainder is smaller than b, so the pair shrinks every pass.
            int r = a % b;
            // The old b becomes the larger value of the new pair.
            a = b;
            // The remainder becomes the smaller value of the new pair.
            b = r;
        }
        // When b is zero, a divides both original inputs and no larger value does.
        return a;
    }

    /** Counts the replacements, used to check the logarithmic bound. */
    static int steps(int a, int b) {
        int count = 0;
        // Each pass is one replacement of the pair.
        while (b != 0) {
            int r = a % b;
            a = b;
            b = r;
            count++;
        }
        return count;
    }

    /** Signed version: widens to long first, because Math.abs on Integer.MIN_VALUE stays negative. */
    static long signedGcd(int a, int b) {
        // After widening, the absolute value of any int fits in a long.
        long x = Math.abs((long) a);
        long y = Math.abs((long) b);
        // The same loop runs on non-negative values.
        while (y != 0) {
            long r = x % y;
            x = y;
            y = r;
        }
        return x;
    }

    /** Trial search from the larger candidate downward, used as an independent oracle on small inputs. */
    static int trial(int a, int b) {
        // Zero inputs return the other value.
        if (a == 0 || b == 0) return a + b;
        // The first divisor found from above is the greatest common divisor.
        for (int d = Math.min(a, b); d >= 1; d--) {
            if (a % d == 0 && b % d == 0) return d;
        }
        return 1;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (gcd(1071, 462) != 21) throw new AssertionError("example 1");
        if (gcd(0, 9) != 9) throw new AssertionError("example 2");
        // Checks the zero convention.
        if (gcd(0, 0) != 0) throw new AssertionError("gcd of zeros");
        // Checks the Java facts behind the sign handling.
        if (Math.abs(Integer.MIN_VALUE) >= 0) throw new AssertionError("abs of MIN");
        if (-7 % 3 != -1) throw new AssertionError("remainder sign");
        if (signedGcd(Integer.MIN_VALUE, 6) != 2) throw new AssertionError("signed gcd of MIN");
        if (signedGcd(-12, 18) != 6) throw new AssertionError("signed gcd of negatives");
        // Checks the slowest case for 31-bit inputs: consecutive Fibonacci numbers.
        if (steps(1836311903, 1134903170) > 45) throw new AssertionError("step bound");
        // Checks small random pairs against the trial search, which is the oracle.
        Random rnd = new Random(3081);
        for (int round = 0; round < 3000; round++) {
            int a = rnd.nextInt(400);
            int b = rnd.nextInt(400);
            if (gcd(a, b) != trial(a, b)) throw new AssertionError("small " + a + " " + b);
        }
        // Checks large random pairs against BigInteger.
        for (int round = 0; round < 3000; round++) {
            int a = rnd.nextInt(Integer.MAX_VALUE);
            int b = rnd.nextInt(Integer.MAX_VALUE);
            int expected = BigInteger.valueOf(a).gcd(BigInteger.valueOf(b)).intValue();
            if (gcd(a, b) != expected) throw new AssertionError("large " + a + " " + b);
        }
    }
}
```

#### Solution: [Vary] Integer Power (LeetCode 50)
<!-- id: bt08-integer-power -->

**Approach.** The loop reads the exponent from its lowest bit upward and squares the base after each bit.

The invariant is that `result * base^e` equals `x^n`. When the lowest bit of `e` is 1, one factor of `base` moves into `result`, which keeps the product. After that, `base` squares and `e` halves, which also keeps the product. When `e` reaches 0, the power `base^e` is 1, so `result` is the answer. The last pass squares the base once more than needed. For `x = -2` and `n = 63`, that extra square is 2^64 and wraps to 0 in a `long`, but the loop never multiplies it into `result`, so the exact answer `-2^63` survives. The loop condition `e > 0` is the reason that the unused square is harmless.

**Complexity.**

- **Time** is O(log n), because the loop runs once per bit of `n`, which is at most 30 passes for `n <= 10^9`.
- **Space** is O(1), because the loop keeps only `result`, `base` and `e`.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class IntegerPower {
    /**
     * Returns x raised to n for n >= 0, using repeated squaring.
     * Time: O(log n), one pass per bit of n.
     * Space: O(1), three values.
     * Invariant: result * base^e equals x^n at the start of every pass.
     */
    static long power(long x, int n) {
        // The result collects the factors that set bits of the exponent select.
        long result = 1;
        // The base holds x^(2^k) at pass k.
        long base = x;
        // The exponent shrinks by one bit per pass.
        int e = n;
        // The loop ends when no bit remains.
        while (e > 0) {
            // A set lowest bit moves one factor of base into the result.
            if ((e & 1) == 1) result *= base;
            // The next bit has twice the weight, so the base squares.
            base *= base;
            // The shift removes the bit that was just handled; e is positive, so >> is safe.
            e >>= 1;
        }
        // At e = 0 the remaining power is 1, so the result is x^n.
        return result;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (power(3, 13) != 1594323L) throw new AssertionError("example 1");
        if (power(-2, 63) != Long.MIN_VALUE) throw new AssertionError("example 2");
        // Checks the exponent zero, which returns 1 for every base including zero.
        if (power(0, 0) != 1 || power(-1000, 0) != 1) throw new AssertionError("exponent zero");
        // Checks the Java fact that the unused last square wraps without an exception.
        long wrap = 1L << 32;
        if (wrap * wrap != 0) throw new AssertionError("square wraps");
        // Checks random inputs against BigInteger.pow, keeping only results that fit in a long.
        Random rnd = new Random(3082);
        int checked = 0;
        for (int round = 0; round < 20000; round++) {
            int x = rnd.nextInt(2001) - 1000;
            int n = rnd.nextInt(40);
            BigInteger expected = BigInteger.valueOf(x).pow(n);
            if (expected.bitLength() >= 64) continue;
            checked++;
            if (power(x, n) != expected.longValue()) throw new AssertionError(x + "^" + n);
        }
        if (checked < 1000) throw new AssertionError("too few cases checked");
        // Checks a large exponent with base 1 and base -1.
        if (power(1, 1_000_000_000) != 1 || power(-1, 1_000_000_000) != 1 || power(-1, 999_999_999) != -1) {
            throw new AssertionError("unit bases");
        }
    }
}
```

#### Solution: [Boundary] Zero And MIN Exponent (Author exercise)
<!-- id: bt08-zero-min-exponent -->

**Approach.** The method widens the exponent to `long` before it changes the sign.

For an `int` exponent, `-Integer.MIN_VALUE` equals `Integer.MIN_VALUE`, so a loop that negates an `int` would keep a negative exponent and never run. Widening first gives the positive value 2^31 exactly. A negative exponent inverts the base once, and the loop then raises the inverse to the positive exponent. The exponent 0 skips the loop and returns 1.0 for every base, including 0.0. A zero base with a negative exponent inverts to infinity, and the loop keeps infinity, which matches Java division by zero. The invariant is the same as in the integer version: `result * base^e` equals the target power. The checks also confirm the `>>` and `>>>` facts from the lesson.

**Complexity.**

- **Time** is O(log |n|), because the loop runs once per bit of the widened exponent, at most 32 passes.
- **Space** is O(1), because the loop keeps three values.

```java run
import java.util.Random;

public final class ZeroMinExponent {
    /**
     * Returns x raised to any int exponent as a double.
     * Time: O(log |n|), at most 32 passes.
     * Space: O(1), three values.
     * Invariant: result * base^e equals x^n, with e held as a non-negative long.
     */
    static double power(double x, int n) {
        // Widen before any sign change, so Integer.MIN_VALUE becomes 2^31 and stays correct.
        long e = n;
        // A negative exponent inverts the base once and continues with a positive exponent.
        if (e < 0) {
            x = 1.0 / x;
            e = -e;
        }
        // The result starts at 1.0, which is the answer when the exponent is zero.
        double result = 1.0;
        // The loop runs once per remaining bit.
        while (e > 0) {
            // A set lowest bit multiplies the current base into the result.
            if ((e & 1) == 1) result *= x;
            // The next bit has twice the weight.
            x *= x;
            // The exponent is positive here, so the arithmetic shift drops one bit.
            e >>= 1;
        }
        return result;
    }

    /** Compares two doubles, allowing a tiny relative error and exact matches of infinities and zero. */
    static boolean close(double a, double b) {
        // Equal values, including both infinities and both zeros, match exactly.
        if (a == b) return true;
        // Otherwise the relative error must be tiny.
        return Math.abs(a - b) <= 1e-9 * Math.max(Math.abs(a), Math.abs(b));
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (power(2.0, -3) != 0.125) throw new AssertionError("example 1");
        if (power(-1.0, Integer.MIN_VALUE) != 1.0) throw new AssertionError("example 2");
        // Checks the Java fact that negating an int minimum leaves it negative.
        int min = Integer.MIN_VALUE;
        if (-min != min) throw new AssertionError("negation of MIN");
        long widened = min;
        if (-widened != 2147483648L) throw new AssertionError("widened negation");
        // Checks the shift facts from the applicability section.
        if ((min >> 31) != -1 || (min >>> 31) != 1) throw new AssertionError("shift kinds");
        // Checks zero base cases: exponent 0 gives 1.0, a negative exponent gives infinity.
        if (power(0.0, 0) != 1.0) throw new AssertionError("zero to zero");
        if (power(0.0, -1) != Double.POSITIVE_INFINITY) throw new AssertionError("zero to negative");
        if (power(0.0, 5) != 0.0) throw new AssertionError("zero to positive");
        // Checks the minimum exponent on bases that overflow, underflow or stay fixed.
        if (power(2.0, Integer.MIN_VALUE) != 0.0) throw new AssertionError("two to MIN");
        if (power(0.5, Integer.MIN_VALUE) != Double.POSITIVE_INFINITY) throw new AssertionError("half to MIN");
        if (power(1.0, Integer.MIN_VALUE) != 1.0) throw new AssertionError("one to MIN");
        // Checks random bases and exponents against Math.pow, which is the oracle.
        Random rnd = new Random(3083);
        double[] bases = {-3.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.25, 2.0, 3.0, 10.0};
        for (int round = 0; round < 5000; round++) {
            double x = bases[rnd.nextInt(bases.length)];
            int n = rnd.nextInt(81) - 40;
            if (!close(power(x, n), Math.pow(x, n))) throw new AssertionError(x + "^" + n);
        }
    }
}
```

#### Solution: [Recognize] LCM Safely (Author exercise)
<!-- id: bt08-safe-lcm -->

**Approach.** The method folds the array into a running least common multiple and tests the limit before each multiplication.

For two positive numbers, `lcm(l, v)` equals `l / gcd(l, v) * v`. Dividing first keeps the intermediate value at the size of the final answer, since the division is exact. The product is at most 10^18 exactly when `l / g <= 10^18 / v` in integer division, so the method tests that comparison and never forms a product that could overflow. Once the running value passes the limit, the least common multiple of the whole array is at least that large, because adding elements never shrinks it. The method therefore returns -1 at that point. The checks also show why the naive product fails: `46341 * 46341` overflows an `int`, and a product of two `10^9` values overflows nothing in `long` but a later product does.

**Complexity.**

- **Time** is O(n log M), where M is the largest element, because each of the `n` elements costs one gcd of at most about 45 replacements.
- **Space** is O(1), because the method keeps the running value and one gcd.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class SafeLcm {
    static final long LIMIT = 1_000_000_000_000_000_000L;

    /** Greatest common divisor of two positive longs. */
    static long gcd(long a, long b) {
        // The pair shrinks until the second value is zero.
        while (b != 0) {
            long r = a % b;
            a = b;
            b = r;
        }
        return a;
    }

    /**
     * Returns the least common multiple of all elements, or -1 when it exceeds 10^18.
     * Time: O(n log M), one gcd per element.
     * Space: O(1), one running value.
     * Invariant: lcm holds the least common multiple of the elements read so far and is at most 10^18.
     */
    static long safeLcm(int[] nums) {
        // The empty product is 1, and every element divides the final value.
        long lcm = 1;
        // One step per element, in order.
        for (int v : nums) {
            // The gcd lets the division happen before the multiplication.
            long g = gcd(lcm, v);
            // lcm / g * v exceeds the limit exactly when lcm / g exceeds LIMIT / v.
            if (lcm / g > LIMIT / v) return -1;
            // The division is exact, so this product is the new least common multiple.
            lcm = lcm / g * v;
        }
        // Every element has been folded in without passing the limit.
        return lcm;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (safeLcm(new int[]{4, 6, 10}) != 60) throw new AssertionError("example 1");
        if (safeLcm(new int[]{1_000_000_000, 999_999_999, 999_999_998}) != -1) throw new AssertionError("example 2");
        // Checks a pair that stays below the limit and one that sits exactly on it.
        if (safeLcm(new int[]{1_000_000_000, 999_999_999}) != 999_999_999_000_000_000L) throw new AssertionError("large pair");
        if (safeLcm(new int[]{1_000_000_000, 1_000_000_000}) != 1_000_000_000L) throw new AssertionError("equal pair");
        // Checks the Java fact behind the lesson: the int product overflows even for a small least common multiple.
        int a = 50_000;
        if (a * a > 0) throw new AssertionError("int product should overflow");
        if (safeLcm(new int[]{a, a}) != 50_000L) throw new AssertionError("small lcm");
        // Checks random arrays against BigInteger, which is the oracle.
        Random rnd = new Random(3084);
        int minus = 0;
        for (int round = 0; round < 5000; round++) {
            int n = 1 + rnd.nextInt(6);
            int[] nums = new int[n];
            BigInteger l = BigInteger.ONE;
            for (int i = 0; i < n; i++) {
                int[] scale = {10, 100, 100_000, 1_000_000_000};
                nums[i] = 1 + rnd.nextInt(scale[rnd.nextInt(4)]);
                BigInteger v = BigInteger.valueOf(nums[i]);
                l = l.divide(l.gcd(v)).multiply(v);
            }
            long expected = l.compareTo(BigInteger.valueOf(LIMIT)) > 0 ? -1 : l.longValue();
            if (expected == -1) minus++;
            if (safeLcm(nums) != expected) throw new AssertionError("round " + round);
        }
        // Confirms the random test exercised both outcomes.
        if (minus == 0 || minus == 5000) throw new AssertionError("one-sided test");
    }
}
```
