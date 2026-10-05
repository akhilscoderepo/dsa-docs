<!-- solutions-for: 07-prefix-sums-and-difference-arrays -->
### Solutions For Range Sum Queries

#### Solution: [Build] Range Sum Query Immutable (LeetCode 303)
<!-- id: ps-range-sum-303 -->

**Approach.**
One pass builds the prefix array with the sentinel entry 0. Each query then reads `prefix[right + 1]` and `prefix[left]` and subtracts. The two entries both contain the first `left` values, and the subtraction cancels them. The invariant is that `prefix[b] - prefix[a]` equals the sum of `nums[a..b-1]` for every `a <= b`, so each answer is exact.

**Complexity.**
- **Time** is O(n + q), because the build costs n additions and each query costs one subtraction.
- **Space** is O(n) for the prefix array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RangeSum303 {
    /**
     * Answers each inclusive window sum with the prefix array.
     * Time: O(n + q), one build and one subtraction per query.
     * Space: O(n) for the prefix array.
     * Invariant: prefix[b] - prefix[a] is the sum of nums[a..b-1] for a <= b.
     */
    static long[] answer(int[] nums, int[][] queries) {
        long[] prefix = new long[nums.length + 1];
        // The build runs once, so its cost is paid before the first query.
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long[] out = new long[queries.length];
        // Each query costs two reads and one subtraction, with no inner loop.
        for (int q = 0; q < queries.length; q++) {
            // The shared first left values cancel in the difference.
            out[q] = prefix[queries[q][1] + 1] - prefix[queries[q][0]];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        long[] a = answer(new int[] {-2, 0, 3, -5, 2, -1}, new int[][] {{0, 2}, {2, 5}, {0, 5}});
        if (!Arrays.equals(a, new long[] {1, -1, -3})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new int[] {7}, new int[][] {{0, 0}}), new long[] {7})) throw new AssertionError("example 2");
        // Random arrays and queries against a loop over each window.
        Random rnd = new Random(5);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] nums = rnd.ints(n, -100_000, 100_000).toArray();
            int[][] qs = new int[6][];
            for (int k = 0; k < qs.length; k++) {
                int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
                qs[k] = new int[] {l, r};
            }
            long[] got = answer(nums, qs);
            for (int k = 0; k < qs.length; k++) {
                long s = 0;
                for (int i = qs[k][0]; i <= qs[k][1]; i++) s += nums[i];
                if (got[k] != s) throw new AssertionError("random");
            }
        }
    }
}
```

#### Solution: [Vary] Half-Open Query (Author exercise)
<!-- id: ps-half-open-query -->

**Approach.**
The prefix entry `prefix[i]` is the sum of the first `i` values, so it already excludes `nums[i]`. A window that excludes its end index is therefore the difference `prefix[end] - prefix[start]` with no `+ 1`. A query with `start == end` subtracts an entry from itself and returns 0, so an empty window needs no branch. The empty array has a single entry, and the only valid query is `[0, 0]`.

**Complexity.**
- **Time** is O(n + q), because the build costs n additions and each query costs one subtraction.
- **Space** is O(n) for the prefix array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class HalfOpenQuery {
    /**
     * Answers each window [start, end) with the prefix array.
     * Time: O(n + q), one build and one subtraction per query.
     * Space: O(n) for the prefix array.
     * Invariant: prefix[i] is the sum of the first i values.
     */
    static long[] answer(int[] nums, int[][] queries) {
        long[] prefix = new long[nums.length + 1];
        // The build visits each value once.
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
        long[] out = new long[queries.length];
        for (int q = 0; q < queries.length; q++) {
            // Both indexes name prefix entries directly, because the end is excluded.
            out[q] = prefix[queries[q][1]] - prefix[queries[q][0]];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(answer(new int[] {3, 1, 4, 1, 5}, new int[][] {{1, 4}, {0, 5}}), new long[] {6, 14})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new int[] {3, 1, 4}, new int[][] {{2, 2}, {3, 3}}), new long[] {0, 0})) throw new AssertionError("example 2");
        // The empty array accepts only the empty window.
        if (answer(new int[0], new int[][] {{0, 0}})[0] != 0) throw new AssertionError("empty array");
        // Random arrays against a loop over each half-open window.
        Random rnd = new Random(6);
        for (int t = 0; t < 2000; t++) {
            int n = rnd.nextInt(10);
            int[] nums = rnd.ints(n, -1_000_000_000, 1_000_000_000).toArray();
            int s = rnd.nextInt(n + 1), e = s + rnd.nextInt(n - s + 1);
            long expect = 0;
            for (int i = s; i < e; i++) expect += nums[i];
            if (answer(nums, new int[][] {{s, e}})[0] != expect) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Boundary] Whole Array (Author exercise)
<!-- id: ps-whole-array -->

**Approach.**
The whole array is the window `[0, n - 1]`, so its answer is `prefix[n] - prefix[0]`, and the subtracted entry is the sentinel 0. The first value is `prefix[1] - prefix[0]`. The last value is `prefix[n] - prefix[n - 1]`, which reads the largest valid index. A one-value array makes all three differences equal. No expression reads `prefix[-1]`, because the sentinel entry takes its place.

**Complexity.**
- **Time** is O(n), because the build dominates and each answer costs one subtraction.
- **Space** is O(n) for the prefix array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class WholeArray {
    /**
     * Returns {sum of [0, n-1], sum of [0, 0], sum of [n-1, n-1]}.
     * Time: O(n), one build and three subtractions.
     * Space: O(n) for the prefix array.
     * Invariant: prefix[b] - prefix[a] is the sum of nums[a..b-1].
     */
    static long[] ends(int[] nums) {
        int n = nums.length;
        long[] prefix = new long[n + 1];
        // The build leaves prefix[0] = 0 as the sentinel.
        for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
        // The whole array subtracts the sentinel and reads the largest index.
        long all = prefix[n] - prefix[0];
        // The first window starts at 0, so it also subtracts the sentinel.
        long first = prefix[1] - prefix[0];
        // The last window ends at the largest valid prefix index.
        long last = prefix[n] - prefix[n - 1];
        return new long[] {all, first, last};
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(ends(new int[] {4, -2, 7}), new long[] {9, 4, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(ends(new int[] {5}), new long[] {5, 5, 5})) throw new AssertionError("example 2");
        // Random arrays against direct sums.
        Random rnd = new Random(7);
        for (int t = 0; t < 2000; t++) {
            int[] a = rnd.ints(1 + rnd.nextInt(8), -1_000_000_000, 1_000_000_000).toArray();
            long s = 0;
            for (int v : a) s += v;
            long[] got = ends(a);
            if (got[0] != s || got[1] != a[0] || got[2] != a[a.length - 1]) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Recognize] XOR Queries Of A Subarray (LeetCode 1310)
<!-- id: ps-xor-queries -->

**Approach.**
The array `px` has length `n + 1`, with `px[0] = 0` and `px[i + 1] = px[i] ^ arr[i]`. The entry `px[right + 1]` holds the XOR of `arr[0..right]`, and `px[left]` holds the XOR of `arr[0..left-1]`. The shared leading values appear twice in `px[right + 1] ^ px[left]`, and `x ^ x` is 0, so only `arr[left..right]` remains. The invariant is that `px[i]` is the XOR of the first `i` values, and 0 is the neutral element of XOR, so the sentinel is correct.

**Complexity.**
- **Time** is O(n + q), because the build costs n XOR operations and each query costs one.
- **Space** is O(n) for the array `px`.

```java run
import java.util.Arrays;
import java.util.Random;

public final class XorQueries1310 {
    /**
     * Returns the XOR of each window arr[left..right].
     * Time: O(n + q), one build and one XOR per query.
     * Space: O(n) for the prefix XOR array.
     * Invariant: px[i] is the XOR of the first i values, and px[0] = 0.
     */
    static int[] answer(int[] arr, int[][] queries) {
        int[] px = new int[arr.length + 1];
        // Each entry extends the previous XOR by one value.
        for (int i = 0; i < arr.length; i++) px[i + 1] = px[i] ^ arr[i];
        int[] out = new int[queries.length];
        for (int q = 0; q < queries.length; q++) {
            // The shared leading values appear twice, and x ^ x is 0.
            out[q] = px[queries[q][1] + 1] ^ px[queries[q][0]];
        }
        return out;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (!Arrays.equals(answer(new int[] {1, 3, 4, 8}, new int[][] {{0, 1}, {1, 2}, {0, 3}, {3, 3}}), new int[] {2, 7, 14, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new int[] {4, 8, 2, 10}, new int[][] {{2, 3}, {1, 3}, {0, 0}, {0, 3}}), new int[] {8, 0, 4, 4})) throw new AssertionError("example 2");
        // The cancellation property that the approach relies on.
        for (int x : new int[] {0, 1, 7, 1_000_000_000, Integer.MAX_VALUE}) if ((x ^ x) != 0) throw new AssertionError("x ^ x");
        // Random arrays against a loop over each window.
        Random rnd = new Random(8);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] arr = rnd.ints(n, 1, 1_000_000_001).toArray();
            int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
            int expect = 0;
            for (int i = l; i <= r; i++) expect ^= arr[i];
            if (answer(arr, new int[][] {{l, r}})[0] != expect) throw new AssertionError("random");
        }
    }
}
```
