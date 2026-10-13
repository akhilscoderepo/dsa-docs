<!-- solutions-for: 01-fenwick-trees -->
### Solutions For Fenwick Trees

#### Solution: [Build] Prefix Query (Author exercise)
<!-- id: rq31-fenwick-prefix -->

**Approach.** The query adds the blocks that together cover positions 1 to `k`.

Entry `tree[k]` covers the `k & -k` counts that end at `k`. Subtracting that low bit from `k` leaves the index where the next block ends, so the blocks do not overlap and leave no gap. The loop repeats until the index reaches 0, and the invariant is that `sum` equals the total of the counts above the current index, up to `k`. For `k = 5` the loop reads `tree[5]` and `tree[4]`, which gives 5 + 9 = 14. For `k = 0` the loop body never runs.

**Complexity.**

- **Time** is O(log k), because every step clears the lowest set bit of the index and `k` has at most 17 set bits for `k <= 10^5`.
- **Space** is O(1), because the loop keeps one index and one sum.

```java run
import java.util.Random;

public final class FenwickPrefix {
    /**
     * Returns the sum of the first k counts stored in a one-based Fenwick array.
     * Time: O(log k), one step per set bit of k.
     * Space: O(1), one index and one running sum.
     * Invariant: sum holds the counts at positions i+1 to k, and i is the end of the next unread block.
     */
    static long prefix(long[] tree, int k) {
        // The running sum starts empty, so k = 0 returns 0 without reading tree.
        long sum = 0;
        // Each step clears the lowest set bit, so the loop runs once per set bit of k.
        for (int i = k; i > 0; i -= i & -i) {
            // The block ending at i covers i & -i counts, which no earlier block covered.
            sum += tree[i];
        }
        // The blocks read together cover positions 1 to k exactly.
        return sum;
    }

    /** Builds the tree from the definition: tree[i] sums the i & -i counts ending at i. */
    static long[] buildByDefinition(long[] a) {
        // One slot per count plus the unused slot 0.
        long[] tree = new long[a.length + 1];
        // Visit each internal index once.
        for (int i = 1; i <= a.length; i++) {
            // The block starts at i - (i & -i) + 1 in one-based terms.
            for (int p = i - (i & -i); p < i; p++) {
                // Position p + 1 in one-based terms is a[p] in zero-based terms.
                tree[i] += a[p];
            }
        }
        // The finished array is the input to prefix.
        return tree;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2 on the lesson tree.
        long[] tree = {0, 3, 4, 4, 9, 5, 14, 2, 31};
        if (prefix(tree, 5) != 14) throw new AssertionError("example 1");
        if (prefix(tree, 0) != 0) throw new AssertionError("example 2");
        // Checks that the definition builder reproduces the lesson tree.
        long[] built = buildByDefinition(new long[]{3, 1, 4, 1, 5, 9, 2, 6});
        if (!java.util.Arrays.equals(built, tree)) throw new AssertionError("definition builder");
        // Checks every prefix against a brute-force sum on random arrays with a fixed seed.
        Random rnd = new Random(31);
        for (int round = 0; round < 300; round++) {
            int n = rnd.nextInt(40);
            long[] a = new long[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            long[] t = buildByDefinition(a);
            long expected = 0;
            for (int k = 0; k <= n; k++) {
                if (k > 0) expected += a[k - 1];
                if (prefix(t, k) != expected) throw new AssertionError("round " + round + " k " + k);
            }
        }
    }
}
```

#### Solution: [Vary] Point Update (Author exercise)
<!-- id: rq31-fenwick-point-update -->

**Approach.** An assignment becomes a delta, and the delta travels along the update path.

The tree only supports adding, so the program keeps a plain array `values` with the current count of each position. The delta for an assignment is the new value minus `values[pos]`. After the delta is added along the path, the program stores the new value, which keeps `values` equal to the true counts. The path starts at `pos + 1` and adds the low bit each step, so each visited block contains the changed position and every other block stays correct. A repeated position works because the second assignment subtracts the first value through its delta.

**Complexity.**

- **Time** is O(m log n) for `m` assignments, because each assignment walks at most `log2(n) + 1` blocks.
- **Space** is O(n), for the `values` array and the `tree` array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FenwickAssign {
    /**
     * Applies assignments (pos, value) to an all-zero Fenwick array and returns the array.
     * Time: O(m log n), one update path of at most log2(n) + 1 blocks per assignment.
     * Space: O(n), for the current counts and the tree.
     * Invariant: values[p] is the true count at p, and tree[i] sums the i & -i counts ending at i.
     */
    static long[] assign(int n, int[][] ops) {
        // Slot 0 stays unused, so the tree has n + 1 slots.
        long[] tree = new long[n + 1];
        // The current counts let each assignment compute its delta.
        long[] values = new long[n];
        // One iteration per assignment.
        for (int[] op : ops) {
            int pos = op[0];
            // The delta turns the old count into the new one.
            long delta = op[1] - values[pos];
            // The path starts at the internal index and moves to the next larger block each step.
            for (int i = pos + 1; i <= n; i += i & -i) {
                // Each visited block contains position pos, so it shifts by the delta.
                tree[i] += delta;
            }
            // Remember the new count so a later assignment computes the right delta.
            values[pos] = op[1];
        }
        // The finished tree is returned to the caller.
        return tree;
    }

    /** Builds the tree directly from final counts using the block definition. */
    static long[] byDefinition(long[] a) {
        // One slot per count plus the unused slot 0.
        long[] tree = new long[a.length + 1];
        // Visit each internal index once.
        for (int i = 1; i <= a.length; i++) {
            // Sum the i & -i counts that end at i.
            for (int p = i - (i & -i); p < i; p++) tree[i] += a[p];
        }
        return tree;
    }

    public static void main(String[] args) {
        // Checks Example 1.
        long[] e1 = assign(6, new int[][]{{2, 5}, {0, 3}, {2, 1}, {5, 4}});
        if (!Arrays.equals(e1, new long[]{0, 3, 3, 1, 4, 0, 4})) throw new AssertionError("example 1 " + Arrays.toString(e1));
        // Checks Example 2, where a position repeats.
        long[] e2 = assign(5, new int[][]{{4, 9}, {4, 2}, {1, 6}});
        if (!Arrays.equals(e2, new long[]{0, 0, 6, 0, 6, 2})) throw new AssertionError("example 2 " + Arrays.toString(e2));
        // Checks random assignment lists against the tree built from the final counts.
        Random rnd = new Random(32);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(30);
            int m = rnd.nextInt(40);
            int[][] ops = new int[m][2];
            long[] expected = new long[n];
            for (int j = 0; j < m; j++) {
                ops[j][0] = rnd.nextInt(n);
                ops[j][1] = rnd.nextInt(2001) - 1000;
                expected[ops[j][0]] = ops[j][1];
            }
            if (!Arrays.equals(assign(n, ops), byDefinition(expected))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Index Conversion (Author exercise)
<!-- id: rq31-fenwick-index-conversion -->

**Approach.** Each external position converts to an internal index once, at the boundary.

The class stores positions one-based, so `add(pos, delta)` starts its loop at `pos + 1`. The method `prefix(k)` returns the sum of the first `k` counts, which are external positions 0 to `k - 1`. The inclusive range `left..right` is therefore `prefix(right + 1) - prefix(left)`. When `left` is 0, `prefix(0)` returns 0 because the loop never runs, so no read of index -1 occurs. When `right` is `n - 1`, the call `prefix(n)` reads the last valid slot. An internal index of 0 would never advance, because `0 & -0` equals 0, and the program asserts that fact.

**Complexity.**

- **Time** is O((n + q) log n), because the build performs `n` updates and each of the `q` queries performs two prefixes.
- **Space** is O(n), for the tree array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FenwickRanges {
    /**
     * Fenwick tree over zero-based external positions with one-based internal storage.
     * Time: O(log n) per add and per prefix.
     * Space: O(n).
     * Invariant: tree[i] sums the i & -i counts ending at internal index i.
     */
    static final class Fenwick {
        // Internal one-based storage, with slot 0 unused.
        final long[] tree;

        Fenwick(int n) {
            // The extra slot keeps internal indexes 1..n valid.
            tree = new long[n + 1];
        }

        void add(int pos, long delta) {
            // Convert once: external position pos is internal index pos + 1.
            for (int i = pos + 1; i < tree.length; i += i & -i) {
                // Every visited block contains the changed position.
                tree[i] += delta;
            }
        }

        long prefix(int k) {
            // An empty prefix returns 0 because the loop does not run.
            long sum = 0;
            // Each step removes the lowest set bit of the index.
            for (int i = k; i > 0; i -= i & -i) {
                sum += tree[i];
            }
            return sum;
        }
    }

    /** Answers inclusive zero-based range queries; Time O((n + q) log n); Space O(n). */
    static long[] answer(long[] a, int[][] queries) {
        // Load the counts one add at a time.
        Fenwick f = new Fenwick(a.length);
        for (int p = 0; p < a.length; p++) f.add(p, a[p]);
        long[] out = new long[queries.length];
        // One answer per query.
        for (int j = 0; j < queries.length; j++) {
            // The inclusive range is a difference of two prefixes over the half-open range left..right + 1.
            out[j] = f.prefix(queries[j][1] + 1) - f.prefix(queries[j][0]);
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        long[] a = {4, -2, 7, 0, 5, -3};
        long[] r = answer(a, new int[][]{{0, 0}, {0, 5}, {2, 4}, {5, 5}});
        if (!Arrays.equals(r, new long[]{4, 11, 12, -3})) throw new AssertionError("example 1 " + Arrays.toString(r));
        if (answer(a, new int[][]{{0, 2}})[0] != 9) throw new AssertionError("example 2");
        // Checks the Java fact behind the index trap: the low bit of 0 is 0, so a zero index never advances.
        int zero = 0;
        if ((zero & -zero) != 0) throw new AssertionError("low bit of zero");
        // Checks the empty prefix and the full prefix.
        Fenwick f = new Fenwick(a.length);
        for (int p = 0; p < a.length; p++) f.add(p, a[p]);
        if (f.prefix(0) != 0) throw new AssertionError("empty prefix");
        if (f.prefix(a.length) != 11) throw new AssertionError("full prefix");
        // Checks random arrays and all ranges against a brute-force loop.
        Random rnd = new Random(33);
        for (int round = 0; round < 200; round++) {
            int n = 1 + rnd.nextInt(30);
            long[] b = new long[n];
            for (int i = 0; i < n; i++) b[i] = rnd.nextInt(2001) - 1000;
            for (int l = 0; l < n; l++) {
                for (int rr = l; rr < n; rr++) {
                    long expected = 0;
                    for (int i = l; i <= rr; i++) expected += b[i];
                    if (answer(b, new int[][]{{l, rr}})[0] != expected) throw new AssertionError("round " + round + " " + l + " " + rr);
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Mutable Range Sum (LeetCode 307)
<!-- id: rq31-fenwick-range-sum-mutable -->

**Approach.** A Fenwick tree plus a copy of the values supports both calls.

The constructor loads each value with an add. The method `update` computes the delta as the new value minus the stored one, adds it along the update path and stores the new value. The method `sumRange` returns a difference of two prefixes. The tree holds `long` sums internally, and the answer fits in an `int` under the stated limits, so the cast is safe. The invariant is that `values[i]` equals the current `nums[i]` and `tree[i]` sums the `i & -i` counts ending at internal index `i`.

**Complexity.**

- **Time** is O(n log n) for construction and O(log n) for each call, because each call walks at most `log2(n) + 1` blocks.
- **Space** is O(n), for the `values` and `tree` arrays.

```java run
import java.util.Random;

public final class MutableRangeSum {
    /**
     * Supports point assignment and inclusive range sums on an int array.
     * Time: O(log n) per call after an O(n log n) build.
     * Space: O(n).
     * Invariant: values mirrors the array, and tree[i] sums the i & -i counts ending at i.
     */
    static final class NumArray {
        // Internal one-based sums, with slot 0 unused.
        private final long[] tree;
        // The current values let update compute its delta.
        private final int[] values;

        NumArray(int[] nums) {
            // Copy the input so later calls do not depend on the caller's array.
            values = nums.clone();
            tree = new long[nums.length + 1];
            // Load each value as an add on an all-zero tree.
            for (int p = 0; p < nums.length; p++) add(p, nums[p]);
        }

        private void add(int pos, long delta) {
            // The update path visits every block that contains pos.
            for (int i = pos + 1; i < tree.length; i += i & -i) tree[i] += delta;
        }

        private long prefix(int k) {
            long sum = 0;
            // Clearing the low bit moves to the next unread block.
            for (int i = k; i > 0; i -= i & -i) sum += tree[i];
            return sum;
        }

        void update(int index, int val) {
            // The delta replaces the old value with the new one.
            add(index, (long) val - values[index]);
            // Keep the mirror equal to the true array.
            values[index] = val;
        }

        int sumRange(int left, int right) {
            // Two prefixes bound the inclusive range; the result fits in an int by the constraints.
            return (int) (prefix(right + 1) - prefix(left));
        }
    }

    public static void main(String[] args) {
        // Checks Example 1: a query, an update, then the same query.
        NumArray na = new NumArray(new int[]{6, -1, 4, 3, 8});
        if (na.sumRange(1, 3) != 6) throw new AssertionError("before update");
        na.update(2, 10);
        if (na.sumRange(1, 3) != 12) throw new AssertionError("after update");
        // Checks Example 2 on the updated array.
        if (na.sumRange(0, 4) != 26) throw new AssertionError("full range");
        if (na.sumRange(4, 4) != 8) throw new AssertionError("single position");
        // Checks random operation sequences against a plain array with a fixed seed.
        Random rnd = new Random(34);
        for (int round = 0; round < 200; round++) {
            int n = 1 + rnd.nextInt(30);
            int[] b = new int[n];
            for (int i = 0; i < n; i++) b[i] = rnd.nextInt(201) - 100;
            NumArray s = new NumArray(b);
            for (int op = 0; op < 60; op++) {
                if (rnd.nextBoolean()) {
                    int idx = rnd.nextInt(n);
                    int v = rnd.nextInt(201) - 100;
                    b[idx] = v;
                    s.update(idx, v);
                } else {
                    int l = rnd.nextInt(n);
                    int r = l + rnd.nextInt(n - l);
                    int expected = 0;
                    for (int i = l; i <= r; i++) expected += b[i];
                    if (s.sumRange(l, r) != expected) throw new AssertionError("round " + round + " op " + op);
                }
            }
        }
    }
}
```
