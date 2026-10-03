<!-- solutions-for: 09-count-all-valid-subarrays-windows -->
### Count-All-Valid-Subarrays Windows

#### Solution: [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-one-zero -->

**Approach.** Keep the number of zeros inside the window. When the new element makes it two, move the left marker forward past the earliest zero, and then add `right - left + 1` to the tally, because every start from `left` to `right` gives a subarray with at most one zero. Cutting the front of such a subarray cannot add a zero, which is why the starts form one block. The check compares with a triple loop that counts zeros directly, asserts that the left marker moves at most n times in total, and checks an all-zeros array and an array with no zeros.

**Complexity.** Each index joins the window once and leaves once, so O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class OneZero {
    static int leftMoves;

    static long countAtMostOneZero(int[] values) {
        long runs = 0;
        int zeros = 0, left = 0;
        for (int right = 0; right < values.length; right++) {
            if (values[right] == 0) zeros++;
            while (zeros > 1) {
                if (values[left] == 0) zeros--;
                left++;
                leftMoves++;
            }
            runs += right - left + 1;
        }
        return runs;
    }
    static long brute(int[] values) {
        long runs = 0;
        for (int i = 0; i < values.length; i++) {
            for (int j = i; j < values.length; j++) {
                int zeros = 0;
                for (int x = i; x <= j; x++) if (values[x] == 0) zeros++;
                if (zeros <= 1) runs++;
            }
        }
        return runs;
    }

    public static void main(String[] args) {
        if (countAtMostOneZero(new int[] {1, 0, 2, 0, 3}) != 11) throw new AssertionError("example 1");
        if (countAtMostOneZero(new int[] {0, 0, 0}) != 3) throw new AssertionError("example 2");
        if (countAtMostOneZero(new int[0]) != 0) throw new AssertionError("empty");
        if (countAtMostOneZero(new int[] {0}) != 1) throw new AssertionError("single zero");
        int[] plain = {5, 5, 5, 5};
        if (countAtMostOneZero(plain) != 10) throw new AssertionError("no zeros: every subarray counts");
        int[] big = new int[100000];
        leftMoves = 0;
        long got = countAtMostOneZero(big);
        if (got != 100000L) throw new AssertionError("all zeros: only single elements qualify " + got);
        if (leftMoves > big.length) throw new AssertionError("left moved too often: " + leftMoves);
        Random rnd = new Random(911);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(4) - 1;
            leftMoves = 0;
            if (countAtMostOneZero(a) != brute(a)) throw new AssertionError("differs on " + java.util.Arrays.toString(a));
            if (leftMoves > n) throw new AssertionError("moves exceed n");
        }
    }
}
```

#### Solution: [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-sum-below-k -->

**Approach.** With positive values, dropping the front element lowers the total, so after the total reaches `k` the marker moves forward until it falls below `k`, or until the window is empty. The starts from `left` to `right` are all valid, so the day adds their number. The total and the tally are `long`. The check compares with a brute force on random arrays, confirms the array is unchanged, shows that an `int` accumulator gives a different answer on two values of two billion with `k` equal to the largest `int`, and shows that a log of 100000 ones gives a count above the `int` range.

**Complexity.** The marker and the right edge each move forward at most n steps, giving O(n) time with constant extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SumBelowK {
    static long countBelow(int[] nums, int k) {
        long runs = 0, total = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            while (left <= right && total >= k) total -= nums[left++];
            runs += right - left + 1;
        }
        return runs;
    }
    static long brokenWithInt(int[] nums, int k) {
        long runs = 0;
        int total = 0, left = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            while (left <= right && total >= k) total -= nums[left++];
            runs += right - left + 1;
        }
        return runs;
    }
    static long brute(int[] nums, long k) {
        long runs = 0;
        for (int i = 0; i < nums.length; i++) {
            long sum = 0;
            for (int j = i; j < nums.length; j++) {
                sum += nums[j];
                if (sum < k) runs++;
            }
        }
        return runs;
    }

    public static void main(String[] args) {
        if (countBelow(new int[] {2, 1, 3, 1}, 5) != 7) throw new AssertionError("example 1");
        if (countBelow(new int[] {5, 5}, 6) != 2) throw new AssertionError("example 2");
        if (countBelow(new int[0], 10) != 0) throw new AssertionError("empty");
        if (countBelow(new int[] {3}, 0) != 0) throw new AssertionError("k zero");
        if (countBelow(new int[] {4, 4, 4}, 5) != 3) throw new AssertionError("all equal");
        int[] huge = {2000000000, 2000000000};
        if (countBelow(huge, Integer.MAX_VALUE) != 2) throw new AssertionError("long accumulator");
        if (brokenWithInt(huge, Integer.MAX_VALUE) == 2) throw new AssertionError("int accumulator should break");
        int[] ones = new int[100000];
        Arrays.fill(ones, 1);
        long expected = 100000L * 100001L / 2;
        if (countBelow(ones, Integer.MAX_VALUE) != expected) throw new AssertionError("large count");
        if (expected <= Integer.MAX_VALUE) throw new AssertionError("count should exceed int");
        Random rnd = new Random(912);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(6);
            int[] copy = Arrays.copyOf(a, n);
            int k = rnd.nextInt(25);
            if (countBelow(a, k) != brute(a, k)) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-k-at-minimum -->

**Approach.** Run the same window and guard the repair loop with `left <= right`. When one element alone reaches `k`, the marker steps over it, `left` becomes `right + 1`, and the contribution `right - left + 1` is zero. Count the right ends at which that happens. If `k` is 0 or 1, no positive total can be below it, so every right end is empty. The check asserts that `left` never exceeds `right + 1`, compares with a brute force for both numbers, and covers `k` equal to 0 and 1 for every array.

**Complexity.** O(n) time, since the marker moves forward at most n times in all, and O(1) extra space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KAtMinimum {
    static boolean overshoot;

    static long[] countWithEmpties(int[] nums, int k) {
        long runs = 0, empties = 0, total = 0;
        int left = 0;
        for (int right = 0; right < nums.length; right++) {
            total += nums[right];
            while (left <= right && total >= k) total -= nums[left++];
            if (left > right + 1) overshoot = true;
            if (left == right + 1) empties++;
            runs += right - left + 1;
        }
        return new long[] {runs, empties};
    }
    static long[] brute(int[] nums, int k) {
        long runs = 0, empties = 0;
        for (int right = 0; right < nums.length; right++) {
            int firstGood = right + 1;
            for (int start = right; start >= 0; start--) {
                long sum = 0;
                for (int x = start; x <= right; x++) sum += nums[x];
                if (sum < k) { runs++; firstGood = start; }
            }
            if (firstGood == right + 1) empties++;
        }
        return new long[] {runs, empties};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(countWithEmpties(new int[] {4, 1, 7}, 2), new long[] {1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(countWithEmpties(new int[] {3, 3}, 1), new long[] {0, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(countWithEmpties(new int[0], 0), new long[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(countWithEmpties(new int[] {1}, 2), new long[] {1, 0})) throw new AssertionError("one element fits");
        Random rnd = new Random(913);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(5);
            for (int k = 0; k <= 12; k++) {
                overshoot = false;
                long[] got = countWithEmpties(a, k);
                if (overshoot) throw new AssertionError("marker passed right + 1");
                if (!Arrays.equals(got, brute(a, k))) throw new AssertionError("differs on " + Arrays.toString(a) + " k " + k);
                if (k <= 1 && (got[0] != 0 || got[1] != n)) throw new AssertionError("tiny k must give zero runs and n empties");
            }
        }
    }
}
```

#### Solution: [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Approach.** Keep a running product of the window and a left marker. A limit of at most one returns zero at once, since every product of positive integers is at least one. Otherwise multiply in the new value, divide out front values while the product is not below the limit, and add `right - left + 1`. The division is exact because the departing value is a factor of the product, and the product becomes 1 for the empty window. The check compares with a `BigInteger` brute force, asserts that the largest product held before repair exceeds the `int` range on a chosen input and stays below the limit times the largest value, and asserts that the arrays stay unchanged.

**Complexity.** O(n) time and O(1) extra space, since each index is multiplied in once and divided out at most once.

```java run
import java.math.BigInteger;
import java.util.Arrays;
import java.util.Random;

public final class ProductLessThanK {
    static long peak;

    static long countProductBelow(int[] values, long limit) {
        if (limit <= 1) return 0;
        long product = 1, runs = 0;
        int left = 0;
        for (int right = 0; right < values.length; right++) {
            product *= values[right];
            peak = Math.max(peak, product);
            while (product >= limit) {
                if (product % values[left] != 0) throw new AssertionError("division not exact");
                product /= values[left++];
            }
            runs += right - left + 1;
        }
        return runs;
    }
    static long brute(int[] values, long limit) {
        long runs = 0;
        for (int i = 0; i < values.length; i++) {
            BigInteger product = BigInteger.ONE;
            for (int j = i; j < values.length; j++) {
                product = product.multiply(BigInteger.valueOf(values[j]));
                if (product.compareTo(BigInteger.valueOf(limit)) < 0) runs++;
            }
        }
        return runs;
    }

    public static void main(String[] args) {
        if (countProductBelow(new int[] {4, 2, 3, 1, 6}, 25) != 13) throw new AssertionError("example 1");
        if (countProductBelow(new int[] {7, 9}, 1) != 0) throw new AssertionError("example 2");
        if (countProductBelow(new int[0], 50) != 0) throw new AssertionError("empty");
        if (countProductBelow(new int[] {1, 1, 1}, 2) != 6) throw new AssertionError("all ones");
        if (countProductBelow(new int[] {3, 3}, 0) != 0) throw new AssertionError("k zero");
        int[] wide = {100000, 100000, 3};
        peak = 0;
        long got = countProductBelow(wide, 1_000_000_000L);
        if (got != brute(wide, 1_000_000_000L)) throw new AssertionError("wide values");
        if (peak <= Integer.MAX_VALUE) throw new AssertionError("product should pass the int range: " + peak);
        if (peak >= 1_000_000_000L * 100000L) throw new AssertionError("product bound");
        Random rnd = new Random(914);
        int[] pool = {1, 2, 3, 5, 100000};
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            int[] copy = Arrays.copyOf(a, n);
            long limit = rnd.nextInt(3) == 0 ? rnd.nextInt(40) : 1 + rnd.nextInt(1_000_000_000);
            if (countProductBelow(a, limit) != brute(a, limit)) throw new AssertionError("differs on " + Arrays.toString(a) + " limit " + limit);
            if (!Arrays.equals(a, copy)) throw new AssertionError("input changed");
        }
    }
}
```
