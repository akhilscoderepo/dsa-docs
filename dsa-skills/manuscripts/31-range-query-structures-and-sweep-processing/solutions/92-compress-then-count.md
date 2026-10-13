<!-- solutions-for: 31-range-query-structures-and-sweep-processing -->
### Solutions For Compress Values Then Count Ranks

#### Solution: [Build] Compress Sparse Coordinates (Author exercise)
<!-- id: rq31-compress-sparse -->

**Approach.** Sorting and removing duplicates produces the array `keys`, whose index plus 1 is the rank of a value.

A query is answered by binary search on `keys`. A found index `p` gives rank `p + 1`. A missing value gives a negative result from `Arrays.binarySearch`, and that case returns 0, which no rank uses. The invariant is that `keys` is strictly increasing, so binary search is valid and equal values land on one index.

**Complexity.**

- **Time** is O((n + q) log n) for `n` values and `q` queries, with the O(n log n) sort paid once and one O(log n) search per query.
- **Space** is O(n) for the sorted copy and O(q) for the answers, because the input arrays stay unchanged.

```java run
import java.util.*;

public final class CompressSparse {
    /**
     * Returns the 1-based rank of each query among the distinct values, or 0 when absent.
     * Time: O((n + q) log n). Space: O(n + q).
     * Invariant: keys[0..m-1] is strictly increasing, so binary search finds each value at most once.
     */
    static int[] ranksOf(int[] values, int[] queries) {
        // Copy the input so that the caller's array stays unchanged.
        int[] sorted = values.clone();
        // Sorting costs O(n log n) and places equal values next to each other.
        Arrays.sort(sorted);
        // m counts the distinct values written to the front of the sorted copy.
        int m = 0;
        // One pass removes duplicates, so this loop costs O(n).
        for (int v : sorted) {
            // Keep a value only when it differs from the last kept value.
            if (m == 0 || sorted[m - 1] != v) sorted[m++] = v;
        }
        // Trim to the distinct values, which are the keys.
        int[] keys = Arrays.copyOf(sorted, m);
        // One answer per query.
        int[] out = new int[queries.length];
        // Each iteration performs one O(log m) binary search.
        for (int i = 0; i < queries.length; i++) {
            // A present value gives an index at or above 0.
            int p = Arrays.binarySearch(keys, 0, m, queries[i]);
            // Present values map to index + 1; absent values map to 0.
            out[i] = p >= 0 ? p + 1 : 0;
        }
        // Return the answers in query order.
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: duplicates share a rank and an absent query returns 0.
        if (!Arrays.equals(ranksOf(new int[]{900, -40, 900, 12, 7000000}, new int[]{12, 900, 13, -40, 7000000}), new int[]{2, 3, 0, 1, 4}))
            throw new AssertionError("example 1");
        // Checks Example 2: an empty value array makes every query absent.
        if (!Arrays.equals(ranksOf(new int[]{}, new int[]{5}), new int[]{0})) throw new AssertionError("example 2");
        // Checks the Java behaviour that an absent value yields a negative search result.
        if (Arrays.binarySearch(new int[]{1, 3}, 2) >= 0) throw new AssertionError("absent value must be negative");
        // Checks the input arrays stay unchanged.
        int[] vals = {5, 1, 5};
        ranksOf(vals, new int[]{1});
        if (!Arrays.equals(vals, new int[]{5, 1, 5})) throw new AssertionError("input mutated");
        // Compares with a TreeSet oracle on random inputs with a fixed seed.
        Random rnd = new Random(9201);
        for (int iter = 0; iter < 2000; iter++) {
            int n = rnd.nextInt(10);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(15) - 7;
            int[] q = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < q.length; i++) q[i] = rnd.nextInt(19) - 9;
            TreeSet<Integer> set = new TreeSet<>();
            for (int x : v) set.add(x);
            int[] expect = new int[q.length];
            for (int i = 0; i < q.length; i++) expect[i] = set.contains(q[i]) ? set.headSet(q[i]).size() + 1 : 0;
            if (!Arrays.equals(ranksOf(v, q), expect)) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Vary] Range Sum With Sparse Keys (LeetCode 307)
<!-- id: rq31-sparse-key-sum -->

**Approach.** All operations are known first, so the keys of the set operations are collected, sorted and deduplicated into `keys`.

The tree has one position per key. A set operation finds the rank of its key, computes `value - current[rank]` and adds that difference. Adding the difference makes the tree entry equal the new value, and a repeated set adds 0. A sum operation needs the number of keys below `lo` and the number of keys at or below `hi`. Those two counts come from binary searches and are valid positions even when the bounds are not keys. The answer is `prefix(atMostHi) - prefix(below lo)`.

The invariant is that the tree position of each key holds its current value, and keys never set hold 0.

**Complexity.**

- **Time** is O(q log q) for `q` operations, because sorting the keys costs O(q log q) and each operation costs O(log q) for the searches and the tree.
- **Space** is O(q) for the keys, the current values, the tree and the answers.

```java run
import java.util.*;

public final class SparseKeySum {
    /** Fenwick tree over positions 1..size, storing long sums. */
    static final class Fenwick {
        final long[] tree;

        Fenwick(int size) {
            // Index 0 stays unused because the structure is 1-based.
            tree = new long[size + 1];
        }

        /**
         * Adds delta at pos. Time: O(log size). Space: O(1).
         * Invariant: tree[i] holds the sum of the block of positions that ends at i.
         */
        void add(int pos, long delta) {
            // Each step moves to the next block that covers pos, so the loop runs O(log size) times.
            for (int i = pos; i < tree.length; i += i & -i) tree[i] += delta;
        }

        /**
         * Returns the sum of positions 1..pos. Time: O(log size). Space: O(1).
         * Invariant: the blocks visited are disjoint and together cover 1..pos.
         */
        long prefix(int pos) {
            // The running sum is a long so that large values cannot overflow.
            long sum = 0;
            // Clearing the lowest set bit jumps to the next disjoint block.
            for (int i = pos; i > 0; i -= i & -i) sum += tree[i];
            return sum;
        }
    }

    /** Returns the number of keys that are less than or equal to bound. */
    static int countAtMost(long[] keys, long bound) {
        // Binary search for the first key greater than bound.
        int lo = 0, hi = keys.length;
        // Each iteration halves the candidate range, so the loop costs O(log m).
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            // A key at or below the bound lies left of the answer.
            if (keys[mid] <= bound) lo = mid + 1; else hi = mid;
        }
        // The index of the first larger key equals the count of keys at or below the bound.
        return lo;
    }

    /**
     * Processes set and sum operations with a Fenwick tree over the sorted distinct keys.
     * Time: O(q log q). Space: O(q).
     * Invariant: the tree position of each key holds that key's current value.
     */
    static long[] run(long[][] ops) {
        // Collect the keys of set operations, which are the only keys that can hold a value.
        long[] all = new long[ops.length];
        int c = 0;
        for (long[] op : ops) if (op[0] == 0) all[c++] = op[1];
        // Sort so that equal keys are adjacent and ranks follow key order.
        long[] sorted = Arrays.copyOf(all, c);
        Arrays.sort(sorted);
        // Remove duplicates in place; m is the number of distinct keys.
        int m = 0;
        for (long k : sorted) if (m == 0 || sorted[m - 1] != k) sorted[m++] = k;
        long[] keys = Arrays.copyOf(sorted, m);
        // The tree and the stored values start at 0, matching keys that were never set.
        Fenwick tree = new Fenwick(m);
        long[] current = new long[m + 1];
        // Answers are appended in the order of the sum operations.
        List<Long> answers = new ArrayList<>();
        // One iteration per operation, each costing O(log q).
        for (long[] op : ops) {
            if (op[0] == 0) {
                // Rank of the key is its index in keys plus 1.
                int rank = Arrays.binarySearch(keys, op[1]) + 1;
                // The tree receives only the change, so a repeated set adds 0.
                tree.add(rank, op[2] - current[rank]);
                // Remember the stored value for the next overwrite.
                current[rank] = op[2];
            } else {
                // Keys at or below hi minus keys below lo are exactly the keys inside [lo, hi].
                int upper = countAtMost(keys, op[2]);
                int lower = countAtMost(keys, op[1] - 1);
                answers.add(tree.prefix(upper) - tree.prefix(lower));
            }
        }
        // Convert the answers to an array in order.
        long[] out = new long[answers.size()];
        for (int i = 0; i < out.length; i++) out[i] = answers.get(i);
        return out;
    }

    /** Brute-force oracle that keeps the values in a map and scans it for each sum. */
    static long[] oracle(long[][] ops) {
        Map<Long, Long> map = new HashMap<>();
        List<Long> answers = new ArrayList<>();
        for (long[] op : ops) {
            if (op[0] == 0) map.put(op[1], op[2]);
            else {
                long s = 0;
                for (Map.Entry<Long, Long> e : map.entrySet()) if (e.getKey() >= op[1] && e.getKey() <= op[2]) s += e.getValue();
                answers.add(s);
            }
        }
        long[] out = new long[answers.size()];
        for (int i = 0; i < out.length; i++) out[i] = answers.get(i);
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 with negative, small and huge keys.
        long[][] ex1 = {{0, 100, 5}, {0, -3, 7}, {1, -10, 100}, {0, 100, 2}, {1, 0, 99}, {1, 100, 100}, {0, 1000000000000L, -4}, {1, -3, 1000000000000L}};
        if (!Arrays.equals(run(ex1), new long[]{12, 0, 2, 5})) throw new AssertionError("example 1");
        // Checks Example 2: setting the same key twice does not double the value.
        if (!Arrays.equals(run(new long[][]{{0, 5, 3}, {0, 5, 3}, {1, 5, 5}}), new long[]{3})) throw new AssertionError("example 2");
        // Checks a sum over a range that holds no key and a sum before any key is set.
        if (!Arrays.equals(run(new long[][]{{1, 0, 0}, {0, 9, 1}, {1, 10, 20}}), new long[]{0, 0})) throw new AssertionError("empty ranges");
        // Compares with the oracle on random operation lists with a fixed seed.
        Random rnd = new Random(9202);
        for (int iter = 0; iter < 2000; iter++) {
            int n = 1 + rnd.nextInt(14);
            long[][] ops = new long[n][];
            for (int i = 0; i < n; i++) {
                if (rnd.nextBoolean()) {
                    long key = rnd.nextInt(8) == 0 ? (rnd.nextBoolean() ? 1000000000000L : -1000000000000L) : rnd.nextInt(13) - 6;
                    ops[i] = new long[]{0, key, rnd.nextInt(21) - 10};
                } else {
                    long a = rnd.nextInt(17) - 8, b = rnd.nextInt(17) - 8;
                    ops[i] = new long[]{1, Math.min(a, b), Math.max(a, b)};
                    if (rnd.nextInt(6) == 0) ops[i][2] = 1000000000000L;
                }
            }
            if (!Arrays.equals(run(ops), oracle(ops))) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Boundary] Negative And Extreme Coordinates (Author exercise)
<!-- id: rq31-extreme-coordinates -->

**Approach.** The method sorts a copy with the primitive sort, which orders `int` values correctly at both extremes.

It removes duplicates to get `keys`, then finds each rank by binary search. The largest neighbour difference widens one operand to `long` before the subtraction, so the result is exact. The expression `a - b` in `int` arithmetic wraps for extreme values, which is why the code never subtracts in `int`. The invariant is that `keys` is strictly increasing, so every rank is unique to one value and no raw value serves as an array index.

**Complexity.**

- **Time** grows as O(n log n), since the sort of the copy outweighs the later searches, which cost O(log n) each.
- **Space** is O(n) for the sorted copy and the result.

```java run
import java.util.*;

public final class ExtremeCoordinates {
    /**
     * Returns the rank of each entry followed by the largest gap between neighbouring distinct values.
     * Time: O(n log n). Space: O(n).
     * Invariant: keys is strictly increasing, so each value has one rank.
     */
    static long[] ranksAndGap(int[] values) {
        int n = values.length;
        // Sort a copy with the primitive sort, which compares int values without subtraction.
        int[] sorted = values.clone();
        Arrays.sort(sorted);
        // Keep one copy of each value; m counts the distinct values.
        int m = 0;
        for (int v : sorted) if (m == 0 || sorted[m - 1] != v) sorted[m++] = v;
        // The result holds n ranks and then the gap.
        long[] out = new long[n + 1];
        // Each rank is one binary search plus 1.
        for (int i = 0; i < n; i++) out[i] = Arrays.binarySearch(sorted, 0, m, values[i]) + 1;
        // Scan the neighbours of the distinct values to find the largest gap.
        long gap = 0;
        for (int i = 1; i < m; i++) {
            // Widening one operand to long keeps the subtraction exact.
            gap = Math.max(gap, (long) sorted[i] - sorted[i - 1]);
        }
        // The last entry carries the gap, which is 0 when fewer than two distinct values exist.
        out[n] = gap;
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 with both extreme values and a duplicate.
        if (!Arrays.equals(ranksAndGap(new int[]{2147483647, -2147483648, 0, -2147483648}), new long[]{3, 1, 2, 1, 2147483648L}))
            throw new AssertionError("example 1");
        // Checks Example 2: one distinct value has no neighbour.
        if (!Arrays.equals(ranksAndGap(new int[]{7, 7, 7}), new long[]{1, 1, 1, 0})) throw new AssertionError("example 2");
        // Checks the Java behaviour behind the hint: int subtraction wraps at the extremes.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("int subtraction must wrap");
        if ((long) Integer.MAX_VALUE - Integer.MIN_VALUE != 4294967295L) throw new AssertionError("long subtraction is exact");
        // Compares with a TreeSet and BigInteger oracle on random inputs with a fixed seed.
        Random rnd = new Random(9203);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, -1, 1, 1000000000, -1000000000, 5};
        for (int iter = 0; iter < 2000; iter++) {
            int n = 1 + rnd.nextInt(9);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = pool[rnd.nextInt(pool.length)];
            TreeSet<Integer> set = new TreeSet<>();
            for (int x : v) set.add(x);
            long[] expect = new long[n + 1];
            for (int i = 0; i < n; i++) expect[i] = set.headSet(v[i]).size() + 1;
            java.math.BigInteger best = java.math.BigInteger.ZERO;
            Integer prev = null;
            for (int x : set) {
                if (prev != null) best = best.max(java.math.BigInteger.valueOf(x).subtract(java.math.BigInteger.valueOf(prev)));
                prev = x;
            }
            expect[n] = best.longValueExact();
            if (!Arrays.equals(ranksAndGap(v), expect)) throw new AssertionError("random " + iter);
        }
    }
}
```

#### Solution: [Recognize] Insertion Cost By Smaller Count (LeetCode 1649)
<!-- id: rq31-smaller-insertion-cost -->

**Approach.** The cost of an insertion is the number of stored entries strictly below it, which is a prefix count over ranks.

The ranks come from the sorted distinct entries. For each entry, the code reads `prefix(rank - 1)` before it adds 1 at `rank`. Reading first keeps the entry out of its own count, and `rank - 1` excludes equal entries. The costs are summed in a `long`, because the total can reach about 5 billion, and the remainder is taken at the end. The invariant is that the tree holds one count per inserted entry at its rank.

**Complexity.**

- **Time** grows as O(n log n), since each entry needs one search, one query and one update of O(log n) each, after the initial sort.
- **Space** is O(n) for the keys and the tree.

```java run
import java.util.*;

public final class SmallerInsertionCost {
    static final long MOD = 1_000_000_007L;

    /**
     * Returns the total of strictly-smaller counts, modulo 1,000,000,007.
     * Time: O(n log n). Space: O(n).
     * Invariant: before entry i is added, the tree holds one count per earlier entry at its rank.
     */
    static int totalCost(int[] instructions) {
        // Sort a copy and drop duplicates to get the dense ranks.
        int[] sorted = instructions.clone();
        Arrays.sort(sorted);
        int m = 0;
        for (int v : sorted) if (m == 0 || sorted[m - 1] != v) sorted[m++] = v;
        // The Fenwick array has m + 1 slots because index 0 is unused.
        long[] tree = new long[m + 1];
        // The total is a long, since it can exceed the int range before the reduction.
        long total = 0;
        // One iteration per inserted entry.
        for (int x : instructions) {
            // The rank is the index in the distinct values plus 1.
            int rank = Arrays.binarySearch(sorted, 0, m, x) + 1;
            // Query first: positions 1..rank-1 hold only strictly smaller earlier entries.
            long smaller = 0;
            for (int i = rank - 1; i > 0; i -= i & -i) smaller += tree[i];
            total += smaller;
            // Add the entry after the query so it never counts itself.
            for (int i = rank; i <= m; i += i & -i) tree[i]++;
        }
        // Reduce once at the end; the long total holds the exact sum.
        return (int) (total % MOD);
    }

    /** Brute-force oracle that mirrors the problem statement with a list. */
    static int oracle(int[] a) {
        long total = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = 0; j < i; j++) if (a[j] < a[i]) total++;
        return (int) (total % MOD);
    }

    public static void main(String[] args) {
        // Checks Example 1 with duplicates, a negative entry and a large entry.
        if (totalCost(new int[]{8, -2, 8, 5, -2, 1000000000, 5}) != 9) throw new AssertionError("example 1");
        // Checks Example 2: the true total passes the modulus, so the reduction matters.
        int[] asc = new int[100000];
        for (int i = 0; i < asc.length; i++) asc[i] = i + 1;
        if (totalCost(asc) != 999949972) throw new AssertionError("example 2");
        if (4999950000L <= MOD) throw new AssertionError("the exact total exceeds the modulus");
        // Checks equal entries add nothing.
        if (totalCost(new int[]{3, 3, 3}) != 0) throw new AssertionError("equal entries");
        // Compares with the oracle on random inputs with a fixed seed.
        Random rnd = new Random(9204);
        for (int iter = 0; iter < 2000; iter++) {
            int n = 1 + rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(12) - 6;
            if (totalCost(a) != oracle(a)) throw new AssertionError("random " + iter);
        }
    }
}
```
