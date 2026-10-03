<!-- solutions-for: 07-exclusion-state -->
### Exclusion State

#### Solution: [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Approach.** Addition has an inverse, so the sum of every value except one is the grand total minus that value. One pass computes the grand total in a `long`, since a hundred thousand values of a billion add to a hundred trillion, and a second pass writes the total minus each value. The same answer can be built from a left pass and a right pass, and the program checks that the two shapes agree, which prepares the product exercise where only the two-pass shape is available.

**Complexity.** Two passes, linear time, and the output array as the only extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SumExceptSelf {
    static long[] sumExceptSelf(int[] a) {
        long total = 0;
        for (int x : a) total += x;
        long[] out = new long[a.length];
        for (int i = 0; i < a.length; i++) out[i] = total - a[i];
        return out;
    }
    static long[] twoPass(int[] a) {
        int n = a.length;
        long[] out = new long[n];
        long left = 0;
        for (int i = 0; i < n; i++) { out[i] = left; left += a[i]; }
        long right = 0;
        for (int i = n - 1; i >= 0; i--) { out[i] += right; right += a[i]; }
        return out;
    }
    static long[] oracle(int[] a) {
        long[] out = new long[a.length];
        for (int i = 0; i < a.length; i++)
            for (int j = 0; j < a.length; j++) if (j != i) out[i] += a[j];
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sumExceptSelf(new int[] {3, -1, 4}), new long[] {3, 7, 2})) throw new AssertionError("example 1");
        long[] big = sumExceptSelf(new int[] {1000000000, 1000000000, 1000000000});
        if (!Arrays.equals(big, new long[] {2000000000L, 2000000000L, 2000000000L})) throw new AssertionError("example 2");
        if (sumExceptSelf(new int[] {7})[0] != 0) throw new AssertionError("a single value leaves an empty sum");
        Random rnd = new Random(7301);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2000000001) - 1000000000;
            long[] want = oracle(a);
            if (!Arrays.equals(sumExceptSelf(a), want)) throw new AssertionError("total form differs");
            if (!Arrays.equals(twoPass(a), want)) throw new AssertionError("two-pass form differs");
        }
    }
}
```

#### Solution: [Vary] Product of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Approach.** The first pass walks left to right and writes into each slot the product of everything before it, keeping a running `left` that is multiplied by the current value only after the slot is written. The second pass walks right to left with a running `right`, starting at one, multiplies each slot by the product of everything after it, and then folds in the current value. Because each stored value is recorded before the element is folded in, the element never appears in its own answer, and nothing is divided. The oracle multiplies all the other values for each position.

**Complexity.** Two passes and O(1) extra space beyond the output array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ProductExceptSelf {
    static int[] productExceptSelf(int[] a) {
        int n = a.length;
        int[] out = new int[n];
        int left = 1;
        for (int i = 0; i < n; i++) {
            out[i] = left;
            left *= a[i];
        }
        int right = 1;
        for (int i = n - 1; i >= 0; i--) {
            out[i] *= right;
            right *= a[i];
        }
        return out;
    }
    static int[] oracle(int[] a) {
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            int p = 1;
            for (int j = 0; j < a.length; j++) if (j != i) p *= a[j];
            out[i] = p;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(productExceptSelf(new int[] {2, 3, 4, 5}), new int[] {60, 40, 30, 24})) throw new AssertionError("example 1");
        if (!Arrays.equals(productExceptSelf(new int[] {-1, 2, -3}), new int[] {-6, 3, -2})) throw new AssertionError("example 2");
        if (!Arrays.equals(productExceptSelf(new int[] {4, 9}), new int[] {9, 4})) throw new AssertionError("two values swap");
        Random rnd = new Random(7302);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (!Arrays.equals(productExceptSelf(a), oracle(a))) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Product of Array Except Self With Zeros (LeetCode 238)
<!-- id: ps-product-with-zeros -->

**Approach.** Count the zeros and multiply the non-zero values into one product. With two or more zeros, every answer is zero, since every position leaves at least one zero in its product. With exactly one zero, only that position has a non-zero answer, namely the product of the non-zero values, and every other position is zero. With no zeros, each answer is the product divided by the value, and division is safe because no value is zero. A plain divide of the grand product by each value fails on any input containing a zero, because the value at that position is zero, and the program asserts that it throws. The result is compared with the division-free two-pass method and with an oracle on random inputs rich in zeros.

**Complexity.** Two passes and O(1) extra space beyond the output.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ProductWithZeros {
    static int[] byZeroCount(int[] a) {
        int zeros = 0, product = 1;
        for (int x : a) {
            if (x == 0) zeros++;
            else product *= x;
        }
        int[] out = new int[a.length];
        if (zeros >= 2) return out;
        for (int i = 0; i < a.length; i++) {
            if (zeros == 1) out[i] = a[i] == 0 ? product : 0;
            else out[i] = product / a[i];
        }
        return out;
    }
    static int[] plainDivide(int[] a) {
        int product = 1;
        for (int x : a) product *= x;
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) out[i] = product / a[i];
        return out;
    }
    static int[] twoPass(int[] a) {
        int n = a.length;
        int[] out = new int[n];
        int left = 1;
        for (int i = 0; i < n; i++) { out[i] = left; left *= a[i]; }
        int right = 1;
        for (int i = n - 1; i >= 0; i--) { out[i] *= right; right *= a[i]; }
        return out;
    }
    static int[] oracle(int[] a) {
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            int p = 1;
            for (int j = 0; j < a.length; j++) if (j != i) p *= a[j];
            out[i] = p;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(byZeroCount(new int[] {0, 4, 5}), new int[] {20, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(byZeroCount(new int[] {0, 0, 3}), new int[] {0, 0, 0})) throw new AssertionError("example 2");
        boolean threw = false;
        try { plainDivide(new int[] {0, 4, 5}); } catch (ArithmeticException e) { threw = true; }
        if (!threw) throw new AssertionError("a plain divide should fail when a value is zero");
        if (!Arrays.equals(byZeroCount(new int[] {0, 0}), new int[] {0, 0})) throw new AssertionError("only zeros");
        Random rnd = new Random(7303);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4) == 0 ? 0 : rnd.nextInt(7) - 3;
            int[] want = oracle(a);
            if (!Arrays.equals(byZeroCount(a), want)) throw new AssertionError("zero count differs on " + Arrays.toString(a));
            if (!Arrays.equals(twoPass(a), want)) throw new AssertionError("two pass differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-prefix-suffix-maximums -->

**Approach.** A maximum cannot be undone, so no grand value gives the maximum of one side. The left pass keeps `best`, the largest value seen before the current position, starting at minus one for the empty side. It records `best` into the left array before folding the current value in. The right pass does the same from the end for the right array. Because every value is non-negative, minus one never collides with a real value. The oracle scans each side from scratch for each position.

**Complexity.** Two passes, linear time, and the two output arrays as the only extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PrefixSuffixMaximums {
    static int[][] bestOnEachSide(int[] a) {
        int n = a.length;
        int[] leftBest = new int[n], rightBest = new int[n];
        int best = -1;
        for (int i = 0; i < n; i++) {
            leftBest[i] = best;
            best = Math.max(best, a[i]);
        }
        best = -1;
        for (int i = n - 1; i >= 0; i--) {
            rightBest[i] = best;
            best = Math.max(best, a[i]);
        }
        return new int[][] {leftBest, rightBest};
    }
    static int[][] oracle(int[] a) {
        int n = a.length;
        int[] l = new int[n], r = new int[n];
        for (int i = 0; i < n; i++) {
            int bl = -1, br = -1;
            for (int j = 0; j < i; j++) bl = Math.max(bl, a[j]);
            for (int j = i + 1; j < n; j++) br = Math.max(br, a[j]);
            l[i] = bl;
            r[i] = br;
        }
        return new int[][] {l, r};
    }

    public static void main(String[] args) {
        int[][] one = bestOnEachSide(new int[] {3, 9, 2, 7});
        if (!Arrays.equals(one[0], new int[] {-1, 3, 9, 9})) throw new AssertionError("example 1 left");
        if (!Arrays.equals(one[1], new int[] {9, 7, 7, -1})) throw new AssertionError("example 1 right");
        int[][] two = bestOnEachSide(new int[] {5});
        if (two[0][0] != -1 || two[1][0] != -1) throw new AssertionError("example 2");
        Random rnd = new Random(7304);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(20);
            int[][] x = bestOnEachSide(a), y = oracle(a);
            if (!Arrays.equals(x[0], y[0]) || !Arrays.equals(x[1], y[1])) throw new AssertionError("differs on " + Arrays.toString(a));
        }
    }
}
```
