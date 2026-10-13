<!-- solutions-for: 10-modular-arithmetic -->
### Solutions For Modular Arithmetic

#### Solution: [Build] Modular Sum And Product (Author exercise)
<!-- id: bt10-sum-and-product -->

**Approach.** The solution reduces each element first and then reduces after every addition and multiplication.

An element can be larger than `m`, so the loop takes `v % m` before using it. The sum of two reduced values is below `2 * m`, which fits in a `long` and needs one reduction. The product of two reduced values is below `m * m`, and for `m` up to 1,000,000,007 that is below 1.0 * 10^18, so it fits in a `long`. The cast to `long` comes before the multiplication, because an `int` product would wrap. The invariant is that `sum` and `product` stay congruent to the exact sum and product of the prefix and stay inside 0 to `m - 1`. The product starts at `1 % m`, so an empty array with `m = 1` gives 0.

**Complexity.**

- **Time** is O(n), because each element costs one remainder, one addition and one multiplication.
- **Space** is O(1), because the loop keeps two running values and the two-slot result.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class ModularSumProduct {
    /**
     * Returns {sum mod m, product mod m} of a nonnegative int array.
     * Time: O(n), one pass with constant work per element.
     * Space: O(1), two running longs.
     * Invariant: sum and product are congruent to the exact prefix values and lie in 0..m-1.
     */
    static int[] sumAndProduct(int[] a, int m) {
        // The empty product is 1 modulo m, which is 0 when m is 1.
        long sum = 0, product = 1 % m;
        // One pass keeps every stored value reduced.
        for (int v : a) {
            // Reduce the element first, because it can exceed m.
            long r = v % m;
            // The sum of two reduced values is below 2m, so one remainder restores the range.
            sum = (sum + r) % m;
            // Both operands are below m and are held in long, so the product cannot wrap.
            product = product * r % m;
        }
        // Both values are below m, so the narrowing casts are exact.
        return new int[]{(int) sum, (int) product};
    }

    /** Oracle that builds the exact sum and product with BigInteger. */
    static int[] oracle(int[] a, int m) {
        BigInteger s = BigInteger.ZERO, p = BigInteger.ONE;
        for (int v : a) { s = s.add(BigInteger.valueOf(v)); p = p.multiply(BigInteger.valueOf(v)); }
        BigInteger bm = BigInteger.valueOf(m);
        return new int[]{s.mod(bm).intValue(), p.mod(bm).intValue()};
    }

    public static void main(String[] args) {
        // Example 1: large elements whose exact product exceeds a long.
        int[] a1 = {1_000_000_000, 999_999_999, 123_456_789};
        if (!java.util.Arrays.equals(sumAndProduct(a1, 1_000_000_007), oracle(a1, 1_000_000_007))) throw new AssertionError("example 1");
        // Example 2: the empty array, for m = 10 and for m = 1.
        if (!java.util.Arrays.equals(sumAndProduct(new int[0], 10), new int[]{0, 1})) throw new AssertionError("example 2a");
        if (!java.util.Arrays.equals(sumAndProduct(new int[0], 1), new int[]{0, 0})) throw new AssertionError("example 2b");
        // The late-reduction method from the lesson wraps on twenty copies of 10^9, so it must differ.
        long wrapped = 1;
        for (int i = 0; i < 20; i++) wrapped *= 1_000_000_000;
        int exact = sumAndProduct(filled(20, 1_000_000_000), 1_000_000_007)[1];
        if (wrapped % 1_000_000_007 == exact) throw new AssertionError("late reduction should differ");
        // Random arrays, including zeros and the maximum int, against BigInteger.
        Random rnd = new Random(3013);
        int[] mods = {1, 2, 7, 1000, 1_000_000_007};
        for (int round = 0; round < 500; round++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4) == 0 ? Integer.MAX_VALUE : rnd.nextInt(Integer.MAX_VALUE);
            int m = mods[rnd.nextInt(mods.length)];
            if (!java.util.Arrays.equals(sumAndProduct(a, m), oracle(a, m))) throw new AssertionError("round " + round);
        }
    }

    static int[] filled(int n, int v) {
        int[] a = new int[n];
        java.util.Arrays.fill(a, v);
        return a;
    }
}
```

#### Solution: [Vary] Modular Fast Power (Author exercise)
<!-- id: bt10-modular-power -->

**Approach.** The solution squares the base once per exponent bit and multiplies it into the result for each set bit.

The base is reduced first, because it can reach 10^18 and its square would wrap. The loop reads the lowest bit of `exp`. A set bit means the current `b`, which equals the original base to a power of two, belongs to the product, so `result` absorbs it. The base then squares and the exponent shifts right by one. Every product has two operands below `m`, so it fits in a `long`. The invariant is that `result * b^exp` stays congruent to the original power. An exponent of 0 skips the loop and returns `1 % m`, so the case 0 to the power 0 gives 1, and the modulus 1 gives 0.

**Complexity.**

- **Time** is O(log exp), because the loop runs once per bit and a `long` exponent has at most 63 bits.
- **Space** is O(1), because the loop keeps three longs.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class ModularPower {
    /**
     * Returns base^exp modulo m for m up to 1,000,000,007.
     * Time: O(log exp), one iteration per exponent bit.
     * Space: O(1), three long variables.
     * Invariant: result * b^exp is congruent to the original base^exp, with result and b in 0..m-1.
     */
    static int powMod(long base, long exp, int m) {
        // The start value 1 % m handles m = 1.
        long result = 1 % m;
        // Reduce the base so that the first square cannot wrap.
        long b = base % m;
        // Each round consumes one bit of the exponent.
        while (exp > 0) {
            // A set bit multiplies the current power of the base into the result.
            if ((exp & 1) == 1) result = result * b % m;
            // Squaring prepares the base for the next higher bit.
            b = b * b % m;
            // The shift halves the exponent, so the loop ends after log2(exp) rounds.
            exp >>= 1;
        }
        return (int) result;
    }

    /** Oracle using BigInteger.modPow. */
    static int oracle(long base, long exp, int m) {
        return BigInteger.valueOf(base).modPow(BigInteger.valueOf(exp), BigInteger.valueOf(m)).intValue();
    }

    public static void main(String[] args) {
        // Example 1: a small power.
        if (powMod(2, 10, 1000) != 24) throw new AssertionError("example 1");
        // Example 2: the largest operands and the zero-to-the-zero case.
        if (powMod(1_000_000_000_000_000_000L, 1_000_000_000_000_000_000L, 1_000_000_007) != 504853526) throw new AssertionError("example 2a");
        if (powMod(0, 0, 7) != 1) throw new AssertionError("example 2b");
        if (powMod(0, 0, 1) != 0 || powMod(5, 3, 1) != 0) throw new AssertionError("modulus one");
        // The lesson trace: 3^13 modulo 1000.
        if (powMod(3, 13, 1000) != 323) throw new AssertionError("trace");
        // Random operands with a fixed seed, against BigInteger.modPow.
        Random rnd = new Random(3014);
        int[] mods = {1, 2, 7, 1000, 1_000_000_007};
        for (int round = 0; round < 500; round++) {
            long base = (rnd.nextLong() >>> 1) % 1_000_000_000_000_000_001L;
            long exp = (rnd.nextLong() >>> 1) % 1_000_000_000_000_000_001L;
            if (round % 5 == 0) exp = rnd.nextInt(20);
            int m = mods[rnd.nextInt(mods.length)];
            if (powMod(base, exp, m) != oracle(base, exp, m)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Negative Remainder (Author exercise)
<!-- id: bt10-negative-remainder -->

**Approach.** The solution widens each difference to `long` and normalizes the remainder into 0 to `m - 1`.

The difference of two `int` values can lie below `Integer.MIN_VALUE`, so the subtraction runs in `long` after casting the left operand. Java `%` returns a result with the sign of its left operand, so a negative difference gives a negative remainder. `Math.floorMod` returns the value in 0 to `m - 1` that is congruent to the input. With `m` up to `Integer.MAX_VALUE` the result still fits in an `int`, since it is below `m`. The invariant is that every stored value is congruent to its difference and lies in the required range.

**Complexity.**

- **Time** is O(n), because each pair costs one subtraction and one floor remainder.
- **Space** is O(n) for the output array, with O(1) extra work.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class NegativeRemainder {
    /**
     * Returns the normalized remainder of a[i] - b[i] modulo m for every index.
     * Time: O(n), constant work per pair.
     * Space: O(n) for the output.
     * Invariant: out[i] is congruent to a[i] - b[i] and lies in 0..m-1.
     */
    static int[] differences(int[] a, int[] b, int m) {
        int[] out = new int[a.length];
        // One floor remainder per pair.
        for (int i = 0; i < a.length; i++) {
            // The cast on the left operand makes the whole subtraction a long subtraction.
            long diff = (long) a[i] - b[i];
            // floorMod keeps the result in 0..m-1, unlike the % operator for negative input.
            out[i] = Math.floorMod(diff, m);
        }
        return out;
    }

    /** Oracle using BigInteger.mod, which is always nonnegative. */
    static int[] oracle(int[] a, int[] b, int m) {
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            out[i] = BigInteger.valueOf(a[i]).subtract(BigInteger.valueOf(b[i])).mod(BigInteger.valueOf(m)).intValue();
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: small negatives with m = 5.
        if (!java.util.Arrays.equals(differences(new int[]{3, -4, 10}, new int[]{10, 6, 10}, 5), new int[]{3, 0, 0})) throw new AssertionError("example 1");
        // Example 2: the extreme int pair with m = 1000.
        int[] got = differences(new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE}, new int[]{Integer.MAX_VALUE, Integer.MIN_VALUE}, 1000);
        if (!java.util.Arrays.equals(got, new int[]{705, 295})) throw new AssertionError("example 2");
        // The raw operator gives a negative result, which is the hazard of this exercise.
        if (-7 % 5 != -2 || Math.floorMod(-7, 5) != 3) throw new AssertionError("operator behaviour");
        // An int subtraction wraps, so the widened version must differ from it.
        if ((Integer.MIN_VALUE - Integer.MAX_VALUE) == (long) Integer.MIN_VALUE - Integer.MAX_VALUE) throw new AssertionError("wrap expected");
        // Empty arrays and the largest modulus.
        if (differences(new int[0], new int[0], 7).length != 0) throw new AssertionError("empty");
        if (differences(new int[]{Integer.MIN_VALUE}, new int[]{Integer.MAX_VALUE}, Integer.MAX_VALUE)[0] != oracle(new int[]{Integer.MIN_VALUE}, new int[]{Integer.MAX_VALUE}, Integer.MAX_VALUE)[0]) throw new AssertionError("max modulus");
        // Random full-range values against BigInteger.
        Random rnd = new Random(3015);
        for (int round = 0; round < 500; round++) {
            int n = rnd.nextInt(10);
            int[] a = new int[n], b = new int[n];
            for (int i = 0; i < n; i++) { a[i] = rnd.nextInt(); b[i] = rnd.nextInt(); }
            int m = 1 + rnd.nextInt(Integer.MAX_VALUE);
            if (round % 3 == 0) m = 1 + rnd.nextInt(10);
            if (!java.util.Arrays.equals(differences(a, b, m), oracle(a, b, m))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Number of Subsequences That Satisfy the Given Sum Condition (LeetCode 1498)
<!-- id: bt10-subsequence-sum-condition -->

**Approach.** The solution sorts the array and counts, for each valid pair of ends, the subsequences that keep both ends.

After sorting, a subsequence is fixed by its smallest and largest chosen positions plus any subset of the positions between them. For `left` as the smallest position, the largest position `right` must satisfy `nums[left] + nums[right] <= target`. Two pointers find it. If the pair fits, then every subset of the `right - left` elements after `left` and up to `right` works, which gives `2^(right - left)` subsequences, and `left` moves up. Otherwise `right` moves down. The powers of two come from a table reduced modulo `m`, so each lookup is O(1) and no exponent overflows. The count is added with a reduction each time. The invariant is that all subsequences whose smallest position is below `left` are already counted. The first table entry is `1 % m`, so `m = 1` gives 0.

**Complexity.**

- **Time** is O(n log n), because the sort dominates and the two pointers together move at most `n` steps.
- **Space** is O(n), for the power table, plus the sort's own working space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SubsequenceSumCondition {
    /**
     * Counts nonempty subsequences with min + max <= target, modulo m.
     * Time: O(n log n), the sort plus a linear two-pointer pass.
     * Space: O(n), the power table.
     * Invariant: every subsequence whose smallest sorted position is below left is already counted.
     */
    static int countSubsequences(int[] nums, int target, int m) {
        int n = nums.length;
        // Sorting makes the smallest and largest chosen elements the two end positions.
        int[] a = nums.clone();
        Arrays.sort(a);
        // pow[i] is 2^i modulo m, and the first entry respects m = 1.
        int[] pow = new int[n];
        pow[0] = 1 % m;
        // Doubling modulo m keeps the table within range.
        for (int i = 1; i < n; i++) pow[i] = (int) (((long) pow[i - 1] * 2) % m);
        long total = 0;
        int left = 0, right = n - 1;
        // The pointers cross after at most n moves in total.
        while (left <= right) {
            if ((long) a[left] + a[right] <= target) {
                // Elements between the ends are free, which gives 2^(right-left) subsets.
                total = (total + pow[right - left]) % m;
                left++;
            } else {
                // The largest end is too large for this smallest end and for every later one.
                right--;
            }
        }
        return (int) total;
    }

    /** Oracle that enumerates every nonempty subset of at most 16 elements. */
    static int oracle(int[] nums, int target, int m) {
        int n = nums.length;
        long count = 0;
        for (int mask = 1; mask < (1 << n); mask++) {
            int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;
            for (int i = 0; i < n; i++) {
                if (((mask >> i) & 1) != 0) { lo = Math.min(lo, nums[i]); hi = Math.max(hi, nums[i]); }
            }
            if ((long) lo + hi <= target) count++;
        }
        return (int) (count % m);
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (countSubsequences(new int[]{4, 1, 6, 2, 3}, 7, 1000) != 22) throw new AssertionError("example 1");
        if (countSubsequences(new int[]{3, 3, 6, 8}, 9, 1_000_000_007) != 6) throw new AssertionError("example 2a");
        if (countSubsequences(new int[]{3, 3, 6, 8}, 9, 1) != 0) throw new AssertionError("example 2b");
        // A single element that fits alone counts once, and one that does not fit counts zero.
        if (countSubsequences(new int[]{5}, 10, 1000) != 1 || countSubsequences(new int[]{5}, 9, 1000) != 0) throw new AssertionError("single");
        // A large all-valid input reduces the count by the modulus, matching a direct power: 2^n - 1.
        int[] big = new int[100_000];
        Arrays.fill(big, 1);
        long expected = (modPow2(100_000, 1_000_000_007) - 1 + 1_000_000_007) % 1_000_000_007;
        if (countSubsequences(big, 2, 1_000_000_007) != expected) throw new AssertionError("large");
        // Random small arrays, targets and moduli against full enumeration.
        Random rnd = new Random(3016);
        int[] mods = {1, 2, 7, 1000, 1_000_000_007};
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(10);
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = 1 + rnd.nextInt(12);
            int target = 1 + rnd.nextInt(25);
            int m = mods[rnd.nextInt(mods.length)];
            if (countSubsequences(nums, target, m) != oracle(nums, target, m)) throw new AssertionError("round " + round);
        }
    }

    static long modPow2(int e, int m) {
        long r = 1 % m;
        for (int i = 0; i < e; i++) r = r * 2 % m;
        return r;
    }
}
```
