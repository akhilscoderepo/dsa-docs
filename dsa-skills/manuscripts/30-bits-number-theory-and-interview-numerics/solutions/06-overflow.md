<!-- solutions-for: 06-overflow -->
### Solutions For Overflow

#### Solution: [Build] Int Sum Into Long (Author exercise)
<!-- id: bt06-sum-into-long -->

**Approach.** A `long` accumulator makes each addition a `long` addition.

The expression `total += v` with a `long` total and an `int` value converts `v` to `long` first, so the addition uses 64 bits. The true sum of 10^5 values is below 10^5 * 2^31, which is about 2.1 * 10^14 and far under 2^63. An `int` accumulator would keep only the low 32 bits of each partial result, and the final conversion to `long` could not restore the lost bits. The invariant is that `total` equals the exact sum of the elements read so far. The empty array returns 0.

**Complexity.**

- **Time** is O(n), because the loop reads each element once.
- **Space** is O(1), as one accumulator is kept.

```java run
import java.util.Random;

public final class SumIntoLong {
    /**
     * Returns the exact sum of the elements of a.
     * Time: O(n).
     * Space: O(1).
     * Invariant: total equals the true sum of the elements already read.
     */
    static long sum(int[] a) {
        // A long accumulator widens each int before the addition happens.
        long total = 0;
        for (int v : a) {
            // long plus int is computed in 64 bits, so no partial sum wraps.
            total += v;
        }
        return total;
    }

    /** The late form: the sum is complete in int before it becomes long. */
    static long lateSum(int[] a) {
        int total = 0;
        for (int v : a) total += v;
        return total;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (sum(new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE, 5}) != 4294967299L) throw new AssertionError("example 1");
        if (sum(new int[]{Integer.MIN_VALUE, Integer.MIN_VALUE}) != -4294967296L) throw new AssertionError("example 2");
        // Checks that the late form returns the wrong value, and the empty array returns 0.
        if (lateSum(new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE, 5}) != 3L) throw new AssertionError("late form");
        if (sum(new int[]{}) != 0) throw new AssertionError("empty");
        // Checks that a late cast of a finished int sum stays wrong.
        int x = Integer.MAX_VALUE;
        if ((long) (x + 1) != -2147483648L) throw new AssertionError("late cast");
        if ((long) x + 1 != 2147483648L) throw new AssertionError("early cast");
        // Checks random arrays against BigInteger sums.
        Random rnd = new Random(3045);
        for (int round = 0; round < 300; round++) {
            int[] a = new int[rnd.nextInt(30)];
            java.math.BigInteger expected = java.math.BigInteger.ZERO;
            for (int i = 0; i < a.length; i++) {
                a[i] = rnd.nextInt();
                expected = expected.add(java.math.BigInteger.valueOf(a[i]));
            }
            if (sum(a) != expected.longValueExact()) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Safe Comparator (Author exercise)
<!-- id: bt06-safe-comparator -->

**Approach.** The comparator returns the sign from `Integer.compare` and never a difference.

A comparator must be consistent, so it needs the true order of two numbers. The difference `a - b` of two `int` values can leave the `int` range and flip its sign. For `a = 2147483647` and `b = -2147483648` the subtraction gives -1, which says `a` is smaller. The call `Integer.compare(a, b)` compares the values directly. The first key ascends, so the comparator compares first numbers as `(a, b)`. The second key descends, so it compares second numbers with the arguments swapped, as `(b, a)`.

**Complexity.**

- **Time** is O(m log m) for `m` pairs, because the sort makes O(m log m) comparisons of O(1) each.
- **Space** is O(log m) for the sort, beyond the array that sorts in place.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SafeComparator {
    /**
     * Sorts pairs by first ascending, then second descending.
     * Time: O(m log m).
     * Space: O(log m) for the sort.
     * Invariant: the comparator returns the sign of the true comparison for every pair of inputs.
     */
    static int[][] sortPairs(int[][] pairs) {
        // Integer.compare returns the sign without subtracting, so it cannot wrap.
        Arrays.sort(pairs, (p, q) -> {
            int c = Integer.compare(p[0], q[0]);
            // Equal first numbers fall through to the second number in descending order.
            return c != 0 ? c : Integer.compare(q[1], p[1]);
        });
        return pairs;
    }

    /** Oracle: the same order, decided with long subtraction that cannot wrap. */
    static int[][] oracle(int[][] pairs) {
        int[][] copy = new int[pairs.length][];
        for (int i = 0; i < copy.length; i++) copy[i] = pairs[i].clone();
        Arrays.sort(copy, (p, q) -> {
            long c = (long) p[0] - q[0];
            if (c != 0) return c < 0 ? -1 : 1;
            long d = (long) q[1] - p[1];
            return d < 0 ? -1 : d > 0 ? 1 : 0;
        });
        return copy;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[][] e1 = sortPairs(new int[][]{{Integer.MAX_VALUE, 1}, {Integer.MIN_VALUE, 5}, {Integer.MAX_VALUE, 9}, {0, 3}});
        if (!Arrays.deepEquals(e1, new int[][]{{Integer.MIN_VALUE, 5}, {0, 3}, {Integer.MAX_VALUE, 9}, {Integer.MAX_VALUE, 1}})) throw new AssertionError("example 1");
        int[][] e2 = sortPairs(new int[][]{{5, 2}, {5, 7}, {-1, 0}});
        if (!Arrays.deepEquals(e2, new int[][]{{-1, 0}, {5, 7}, {5, 2}})) throw new AssertionError("example 2");
        // Checks the Java fact that subtraction flips the sign at the extremes.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("subtraction wraps");
        if (Integer.compare(Integer.MAX_VALUE, Integer.MIN_VALUE) <= 0) throw new AssertionError("compare");
        // Checks random pairs drawn from extreme and small values against the oracle.
        Random rnd = new Random(3055);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, -1, 0, 1, 7, -7, 1 << 30, -(1 << 30)};
        for (int round = 0; round < 300; round++) {
            int[][] pairs = new int[rnd.nextInt(12)][2];
            for (int[] p : pairs) {
                p[0] = pool[rnd.nextInt(pool.length)];
                p[1] = rnd.nextBoolean() ? pool[rnd.nextInt(pool.length)] : rnd.nextInt();
            }
            int[][] expected = oracle(pairs);
            if (!Arrays.deepEquals(sortPairs(pairs), expected)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] MIN_VALUE Negation (Author exercise)
<!-- id: bt06-min-value-negation -->

**Approach.** The conversion to `long` comes first, and the absolute value comes second.

The value 2,147,483,648 has no `int` form, so `-Integer.MIN_VALUE` equals `Integer.MIN_VALUE` and `Math.abs(Integer.MIN_VALUE)` stays negative. After the cast `(long) x`, the value is the same number in 64 bits, and `Math.abs` on a `long` can produce 2,147,483,648 without trouble. Every other `int` also works, since its absolute value is at most 2,147,483,647 and the widened form holds it exactly. The invariant is that no arithmetic runs on the narrow type.

**Complexity.**

- **Time** is O(1), because the method does one cast and one comparison.
- **Space** is O(1), as no storage grows.

```java run
import java.util.Random;

public final class MinValueNegation {
    /**
     * Returns |x| as a long.
     * Time: O(1).
     * Space: O(1).
     * Invariant: the operand is already a long when the sign changes.
     */
    static long absolute(int x) {
        // Widen first, so negation works on a type that can hold 2,147,483,648.
        long wide = x;
        // The sign change now happens in 64 bits.
        return wide < 0 ? -wide : wide;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (absolute(Integer.MIN_VALUE) != 2147483648L) throw new AssertionError("example 1");
        if (absolute(-7) != 7) throw new AssertionError("example 2");
        // Checks the Java facts that make the boundary special.
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("negation wraps");
        if (Math.abs(Integer.MIN_VALUE) >= 0) throw new AssertionError("Math.abs on int stays negative");
        if (Math.abs((long) Integer.MIN_VALUE) != 2147483648L) throw new AssertionError("long abs");
        // Checks random values and the extremes against BigInteger.
        Random rnd = new Random(3065);
        int[] extremes = {0, 1, -1, Integer.MAX_VALUE, Integer.MIN_VALUE, Integer.MIN_VALUE + 1};
        for (int x : extremes) {
            if (absolute(x) != java.math.BigInteger.valueOf(x).abs().longValueExact()) throw new AssertionError("extreme " + x);
        }
        for (int round = 0; round < 500; round++) {
            int x = rnd.nextInt();
            if (absolute(x) != java.math.BigInteger.valueOf(x).abs().longValueExact()) throw new AssertionError("x " + x);
        }
    }
}
```

#### Solution: [Recognize] Reverse Digits Of An Integer (LeetCode 7)
<!-- id: bt06-reverse-digits -->

**Approach.** The loop tests the range before each multiplication, so no operation overflows.

The loop takes the last digit with `x % 10` and removes it with `x / 10`. Java truncates toward zero, so a negative `x` gives negative digits and the sign carries through without a branch. Before the update `rev * 10 + digit`, the program compares `rev` with `Integer.MAX_VALUE / 10`, which is 214,748,364. If `rev` is above it, the product is out of range. If `rev` equals it, the last digit must be at most 7, the final digit of 2,147,483,647. The negative side mirrors this with `Integer.MIN_VALUE / 10`, which is -214,748,364, and the digit limit -8. The invariant is that `rev` always holds a value in the `int` range, so the test itself never overflows.

**Complexity.**

- **Time** is O(d) for `d` decimal digits, which is at most 10 digits here, so O(1).
- **Space** is O(1), since only `rev`, `digit` and `x` are kept.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class ReverseDigits {
    /**
     * Reverses the decimal digits of x, or returns 0 when the result leaves the int range.
     * Time: O(d) for d digits, at most 10.
     * Space: O(1).
     * Invariant: rev is the reversal of the digits already removed, and it fits in an int.
     */
    static int reverse(int x) {
        int rev = 0;
        // Each pass removes the last digit of x.
        while (x != 0) {
            // The remainder keeps the sign of x because Java division truncates toward zero.
            int digit = x % 10;
            x /= 10;
            // Test before multiplying, using only int values.
            if (rev > Integer.MAX_VALUE / 10 || (rev == Integer.MAX_VALUE / 10 && digit > 7)
                    || rev < Integer.MIN_VALUE / 10 || (rev == Integer.MIN_VALUE / 10 && digit < -8)) {
                return 0;
            }
            // The update is now safe.
            rev = rev * 10 + digit;
        }
        return rev;
    }

    /** Oracle: reverse the decimal string with BigInteger and range-check the result. */
    static int oracle(int x) {
        BigInteger v = BigInteger.valueOf(x);
        String s = new StringBuilder(v.abs().toString()).reverse().toString();
        BigInteger r = new BigInteger(s);
        if (x < 0) r = r.negate();
        if (r.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) > 0 || r.compareTo(BigInteger.valueOf(Integer.MIN_VALUE)) < 0) return 0;
        return r.intValueExact();
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (reverse(1463847412) != 2147483641) throw new AssertionError("example 1");
        if (reverse(2046384125) != 0) throw new AssertionError("example 2");
        // Checks signs, trailing zeros and the extreme inputs.
        if (reverse(-4210) != -124) throw new AssertionError("negative");
        if (reverse(0) != 0 || reverse(Integer.MIN_VALUE) != 0 || reverse(Integer.MAX_VALUE) != 0) throw new AssertionError("extremes");
        if (Integer.MAX_VALUE / 10 != 214748364 || Integer.MIN_VALUE / 10 != -214748364) throw new AssertionError("limits");
        // Checks random values of every length against the BigInteger oracle.
        Random rnd = new Random(3075);
        for (int round = 0; round < 5000; round++) {
            int x = switch (rnd.nextInt(4)) {
                case 0 -> rnd.nextInt();
                case 1 -> rnd.nextInt(2_000_001) - 1_000_000;
                case 2 -> 1_000_000_000 + rnd.nextInt(1_147_483_648);
                default -> -(1_000_000_000 + rnd.nextInt(1_147_483_648));
            };
            if (reverse(x) != oracle(x)) throw new AssertionError("x " + x);
        }
    }
}
```
