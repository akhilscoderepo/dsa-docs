<!-- solutions-for: 19-recursion-and-backtracking -->
### Call State

#### Solution: [Build] Sum A Prefix (Author exercise)
<!-- id: bt-sum-prefix -->

**Approach.** The call for `k` returns the total of the first `k` figures, which is the total of the first `k - 1` plus the figure at index `k - 1`, and the call for zero returns zero before touching the array. The shrinking measure is `k` itself. The oracle is a plain loop. The harness compares the two on random arrays and every prefix length, and it also shows that a deep enough prefix overflows the stack, which is why the applicability stage prefers a loop for long inputs.

**Complexity.** Linear time, with one frame per figure, so a linear stack as well.

```java run
import java.util.Random;

public final class SumPrefix {
    static long total(int[] a, int k) {
        if (k == 0) return 0;
        return total(a, k - 1) + a[k - 1];
    }

    static long oracle(int[] a, int k) {
        long s = 0;
        for (int i = 0; i < k; i++) s += a[i];
        return s;
    }

    public static void main(String[] args) {
        if (total(new int[] {3, 1, 4, 1, 5}, 3) != 8) throw new AssertionError("example 1");
        if (total(new int[] {7, 2}, 0) != 0) throw new AssertionError("example 2");
        if (total(new int[0], 0) != 0) throw new AssertionError("empty array");
        Random rnd = new Random(19101);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2_000_001) - 1_000_000;
            for (int k = 0; k <= n; k++) {
                if (total(a, k) != oracle(a, k)) throw new AssertionError("differs at k=" + k);
            }
        }
        boolean overflowed = false;
        try {
            total(new int[3_000_000], 3_000_000);
        } catch (StackOverflowError e) {
            overflowed = true;
        }
        if (!overflowed) throw new AssertionError("a three-million-deep prefix recursion should overflow the default stack");
    }
}
```

#### Solution: [Vary] Power By Halving (LeetCode 50)
<!-- id: bt-power-halving -->

**Approach.** Each call asks once for the power at `n / 2`, squares it, and multiplies by `x` when `n` is odd, and a call count is carried in a one-slot array. Making the half-sized call a second time instead of reusing it would turn the logarithmic count into a linear one, and the harness shows that by counting the calls of such a variant on exponents of the form 2^j. The oracle multiplies one step at a time. Random exponents are kept small so the oracle finishes, and the largest exponent is checked for its call count and against bases whose power is known.

**Complexity.** O(log n) calls, at most 32 for any `int` exponent, and a stack of the same depth.

```java run
import java.util.Random;

public final class PowerHalving {
    static int calls;

    static double power(double x, int n) {
        calls++;
        if (n == 0) return 1.0;
        double half = power(x, n / 2);
        return (n % 2 == 0) ? half * half : half * half * x;
    }

    static int twiceCalls;

    static double twice(double x, int n) {
        twiceCalls++;
        if (n == 0) return 1.0;
        return twice(x, n / 2) * twice(x, n / 2) * ((n % 2 == 0) ? 1.0 : x);
    }

    static double oracle(double x, int n) {
        double r = 1.0;
        for (int i = 0; i < n; i++) r *= x;
        return r;
    }

    static boolean close(double a, double b) {
        return Math.abs(a - b) <= 1e-9 * Math.max(1.0, Math.abs(b));
    }

    public static void main(String[] args) {
        calls = 0;
        if (power(2.0, 10) != 1024.0 || calls != 5) throw new AssertionError("example 1");
        calls = 0;
        if (power(3.0, 0) != 1.0 || calls != 1) throw new AssertionError("example 2");
        Random rnd = new Random(19102);
        for (int t = 0; t < 4000; t++) {
            double x = rnd.nextInt(601) / 100.0 - 3.0;
            int n = rnd.nextInt(60);
            calls = 0;
            double got = power(x, n);
            if (!close(got, oracle(x, n))) throw new AssertionError("value differs for " + x + "^" + n);
        }
        calls = 0;
        power(1.0, Integer.MAX_VALUE);
        if (calls > 32) throw new AssertionError("too many calls: " + calls);
        calls = 0;
        if (power(-1.0, Integer.MAX_VALUE) != -1.0) throw new AssertionError("odd power of -1");
        if (power(0.0, Integer.MAX_VALUE) != 0.0) throw new AssertionError("power of 0");
        for (int j = 1; j <= 10; j++) {
            twiceCalls = 0;
            twice(1.0, 1 << j);
            if (twiceCalls < (1 << j)) throw new AssertionError("a doubled call should cost at least n calls");
        }
    }
}
```

#### Solution: [Boundary] Zero And Negative Exponents (Author exercise)
<!-- id: bt-negative-exponent -->

**Approach.** The exponent is converted to a `long` first, and only then made positive, because negating the most negative `int` returns the same negative number and would leave the shrinking measure below the base case. The positive power is found by halving, and a negative exponent returns its reciprocal, which turns an overflowing power into zero. The harness asserts the negation fact directly and compares random cases with an oracle that multiplies, or divides, one step at a time over a small range. It also checks the two examples and the extreme exponents with bases of one in absolute value and with base 2.

**Complexity.** O(log |n|) time, at most 33 calls, and a stack of the same depth.

```java run
import java.util.Random;

public final class NegativeExponent {
    static double pos(double x, long n) {
        if (n == 0) return 1.0;
        double half = pos(x, n / 2);
        return (n % 2 == 0) ? half * half : half * half * x;
    }

    static double power(double x, int n) {
        long e = n;
        return e >= 0 ? pos(x, e) : 1.0 / pos(x, -e);
    }

    static double oracle(double x, int n) {
        double r = 1.0;
        for (int i = 0; i < Math.abs(n); i++) r *= x;
        return n >= 0 ? r : 1.0 / r;
    }

    public static void main(String[] args) {
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("negating the most negative int should not change it");
        if (-(long) Integer.MIN_VALUE != 2147483648L) throw new AssertionError("widening first gives the positive value");
        if (power(2.0, -2) != 0.25) throw new AssertionError("example 1");
        if (power(-1.0, Integer.MIN_VALUE) != 1.0) throw new AssertionError("example 2");
        if (power(2.0, Integer.MIN_VALUE) != 0.0) throw new AssertionError("underflow should read as zero");
        if (power(-1.0, Integer.MIN_VALUE + 1) != -1.0) throw new AssertionError("odd negative exponent of -1");
        if (power(0.5, 0) != 1.0 || power(-2.0, 0) != 1.0) throw new AssertionError("zero exponent");
        Random rnd = new Random(19103);
        for (int t = 0; t < 4000; t++) {
            double x = (rnd.nextInt(400) + 1) / 200.0 * (rnd.nextBoolean() ? 1 : -1);
            int n = rnd.nextInt(41) - 20;
            double a = power(x, n), b = oracle(x, n);
            if (Math.abs(a - b) > 1e-9 * Math.max(1.0, Math.abs(b))) throw new AssertionError("differs for " + x + "^" + n);
        }
    }
}
```

#### Solution: [Recognize] Recursive String Reversal By Range (Author exercise)
<!-- id: bt-reverse-range -->

**Approach.** The call state is the pair of indexes, the shrinking measure is `hi - lo`, which drops by two on every call, and the base case is any interval where `lo >= hi`, which covers both an empty interval and a single character. An even-length interval ends on `lo > hi` and an odd one on `lo == hi`, and both must return without swapping. All work is done on one `char[]`, so there are no slices. The oracle builds the answer from substrings with `StringBuilder.reverse`. The harness compares the two on random strings and all ranges, including inverted ones.

**Complexity.** About half the length of the range in calls, so linear time, and a stack of the same depth.

```java run
import java.util.Random;

public final class ReverseRange {
    static void flip(char[] c, int lo, int hi) {
        if (lo >= hi) return;
        char t = c[lo];
        c[lo] = c[hi];
        c[hi] = t;
        flip(c, lo + 1, hi - 1);
    }

    static String reverseRange(String s, int lo, int hi) {
        char[] c = s.toCharArray();
        flip(c, lo, hi);
        return new String(c);
    }

    static String oracle(String s, int lo, int hi) {
        if (lo >= hi) return s;
        return s.substring(0, lo) + new StringBuilder(s.substring(lo, hi + 1)).reverse() + s.substring(hi + 1);
    }

    public static void main(String[] args) {
        if (!reverseRange("abcde", 0, 4).equals("edcba")) throw new AssertionError("example 1");
        if (!reverseRange("river", 3, 1).equals("river")) throw new AssertionError("example 2");
        if (!reverseRange("a", 0, 0).equals("a")) throw new AssertionError("single character");
        Random rnd = new Random(19104);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < n; i++) sb.append((char) ('a' + rnd.nextInt(26)));
            String s = sb.toString();
            for (int lo = 0; lo < n; lo++) {
                for (int hi = 0; hi < n; hi++) {
                    if (!reverseRange(s, lo, hi).equals(oracle(s, lo, hi))) throw new AssertionError(s + " " + lo + " " + hi);
                }
            }
        }
    }
}
```
