<!-- solutions-for: 04-coordinate-compression -->
### Solutions For Coordinate Compression

#### Solution: [Build] Compress Distinct Values (Author exercise)
<!-- id: rq31-compress-distinct -->

**Approach.** The method sorts a copy of `values` and keeps the first element of each run of equal values. The result is the rank table. Each query then runs a binary search on the table.

The invariant is that the table is strictly increasing. Under that condition, a found position `p` identifies the unique matching entry, and `p + 1` is its rank. A query that is missing from the table yields a negative search result, which the method maps to 0.

**Complexity.**

- **Time** is O(n log n + q log m), because sorting costs O(n log n) and each of the `q` queries searches `m` distinct entries.
- **Space** is O(n) for the sorted copy, plus O(q) for the answers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CompressDistinct {
    /**
     * Returns the 1-based position of each query in the sorted distinct values, or 0 if absent.
     * Time: O(n log n + q log m). Space: O(n + q).
     * Invariant: table is strictly increasing, so binary search finds at most one match.
     */
    static int[] positions(int[] values, int[] queries) {
        // Copy first so that the caller's array stays unmodified.
        int[] copy = values.clone();
        // Sorting puts equal values next to each other and costs O(n log n).
        Arrays.sort(copy);
        // m counts the distinct values written so far.
        int m = 0;
        // One pass over the sorted copy, so this loop is O(n).
        for (int i = 0; i < copy.length; i++) {
            // Keep a value only when it starts a new run of equal values.
            if (i == 0 || copy[i] != copy[i - 1]) copy[m++] = copy[i];
        }
        // The table is the first m entries of the copy.
        int[] table = Arrays.copyOf(copy, m);
        // One answer per query.
        int[] out = new int[queries.length];
        // Each iteration does one O(log m) binary search.
        for (int k = 0; k < queries.length; k++) {
            // A negative result means the query is absent from the table.
            int pos = Arrays.binarySearch(table, queries[k]);
            // Convert a 0-based table position into a 1-based rank.
            out[k] = pos < 0 ? 0 : pos + 1;
        }
        // The answers are in query order.
        return out;
    }

    /** Oracle: counts distinct smaller values directly and checks membership by scanning. Time O(n q). */
    static int[] brute(int[] values, int[] queries) {
        int[] out = new int[queries.length];
        for (int k = 0; k < queries.length; k++) {
            boolean present = false;
            for (int v : values) if (v == queries[k]) present = true;
            if (!present) continue;
            // The rank is 1 plus the number of distinct values below the query.
            int distinctBelow = 0;
            for (int cand : Arrays.stream(values).distinct().toArray()) if (cand < queries[k]) distinctBelow++;
            out[k] = distinctBelow + 1;
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: duplicates collapse and an absent query returns 0.
        if (!Arrays.equals(positions(new int[]{40, 7, 40, 1000000, 7}, new int[]{7, 1000000, 5}), new int[]{1, 3, 0})) throw new AssertionError("example 1");
        // Checks Example 2: all-equal input has one distinct value.
        if (!Arrays.equals(positions(new int[]{3, 3, 3, 3}, new int[]{3, 4}), new int[]{1, 0})) throw new AssertionError("example 2");
        // Checks empty input: every query is absent, and no query gives an empty answer.
        if (!Arrays.equals(positions(new int[0], new int[]{1}), new int[]{0})) throw new AssertionError("empty values");
        if (positions(new int[]{1}, new int[0]).length != 0) throw new AssertionError("empty queries");
        // Checks the input stays unmodified.
        int[] keep = {5, 1, 5};
        positions(keep, new int[]{1});
        if (!Arrays.equals(keep, new int[]{5, 1, 5})) throw new AssertionError("input mutated");
        // Compares with the oracle on random inputs from a fixed seed.
        Random rnd = new Random(31041);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(12), q = rnd.nextInt(8);
            int[] v = new int[n], qs = new int[q];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(15) - 5;
            for (int i = 0; i < q; i++) qs[i] = rnd.nextInt(15) - 5;
            if (!Arrays.equals(positions(v, qs), brute(v, qs))) throw new AssertionError("random case " + t);
        }
    }
}
```

#### Solution: [Vary] Preserve Equal Ranks (Author exercise)
<!-- id: rq31-equal-ranks -->

**Approach.** The method builds the rank table as in the previous solution and then ranks every element by binary search. The table holds each value once, so every copy of a value reaches the same table position.

The invariant is that `ranks[i] - 1` equals the number of distinct values smaller than `values[i]`. Binary search on a strictly increasing table returns exactly that count as the match position. Ranking by sorted index would instead give equal values different numbers, so the method avoids that approach.

**Complexity.**

- **Time** is O(n log n), because sorting costs O(n log n) and each of the `n` lookups costs O(log m).
- **Space** is O(n), because the sorted copy and the rank array each hold up to `n` entries.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class EqualRanks {
    /**
     * Returns the dense rank of every element, with equal values sharing one rank.
     * Time: O(n log n). Space: O(n).
     * Invariant: ranks[i] - 1 is the number of distinct values below values[i].
     */
    static int[] denseRanks(int[] values) {
        // Sort a copy so that duplicates become adjacent.
        int[] copy = values.clone();
        Arrays.sort(copy);
        // m counts the distinct values written so far.
        int m = 0;
        // One pass removes duplicates in place, costing O(n).
        for (int i = 0; i < copy.length; i++) {
            // Keep only the first value of each run.
            if (i == 0 || copy[i] != copy[i - 1]) copy[m++] = copy[i];
        }
        // The binary search below only needs the first m entries.
        int[] table = Arrays.copyOf(copy, m);
        // One rank per input element.
        int[] ranks = new int[values.length];
        // Each iteration costs O(log m).
        for (int i = 0; i < values.length; i++) {
            // The value is always present, so the result is never negative.
            ranks[i] = Arrays.binarySearch(table, values[i]) + 1;
        }
        // Ranks are in input order.
        return ranks;
    }

    /** Oracle: a TreeSet's headSet size counts distinct smaller values. Time O(n log n). */
    static int[] brute(int[] values) {
        TreeSet<Integer> set = new TreeSet<>();
        for (int v : values) set.add(v);
        int[] out = new int[values.length];
        for (int i = 0; i < values.length; i++) out[i] = set.headSet(values[i]).size() + 1;
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: repeated values share ranks.
        if (!Arrays.equals(denseRanks(new int[]{100, 5, 100, 70, 5}), new int[]{3, 1, 3, 2, 1})) throw new AssertionError("example 1");
        // Checks Example 2: all equal values give rank 1.
        if (!Arrays.equals(denseRanks(new int[]{8, 8, 8}), new int[]{1, 1, 1})) throw new AssertionError("example 2");
        // Checks the empty input.
        if (denseRanks(new int[0]).length != 0) throw new AssertionError("empty");
        // Compares with the oracle on random inputs from a fixed seed.
        Random rnd = new Random(31042);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(14);
            int[] v = new int[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(10) - 4;
            if (!Arrays.equals(denseRanks(v), brute(v))) throw new AssertionError("random case " + t);
        }
    }
}
```

#### Solution: [Boundary] Negative And Extreme Values (Author exercise)
<!-- id: rq31-extreme-values -->

**Approach.** The method follows the previous solution but works on `long` and compares only with `Arrays.sort`, `!=` and `Arrays.binarySearch`. None of them subtracts, so no overflow can occur.

A comparator written as `(int) (a - b)` fails because `Long.MAX_VALUE - Long.MIN_VALUE` wraps around to -1. That comparator would order the largest value before the smallest. The method also never uses a value as an index, because ranks come from table positions.

The invariant is the same as before: the table is strictly increasing under the natural `long` order.

**Complexity.**

- **Time** is O(n log n), because of one sort and `n` binary searches.
- **Space** is O(n) for the copy and the result.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class ExtremeValues {
    /**
     * Returns the dense rank of each long value over the full long range.
     * Time: O(n log n). Space: O(n).
     * Invariant: the table is strictly increasing under the natural order of long.
     */
    static int[] denseRanks(long[] values) {
        // Primitive sort uses the natural order and cannot overflow.
        long[] copy = values.clone();
        Arrays.sort(copy);
        // m counts the distinct values written so far.
        int m = 0;
        // One pass removes duplicates, costing O(n).
        for (int i = 0; i < copy.length; i++) {
            // != on long never subtracts, so extreme neighbours compare correctly.
            if (i == 0 || copy[i] != copy[i - 1]) copy[m++] = copy[i];
        }
        // The table holds the m distinct values.
        long[] table = Arrays.copyOf(copy, m);
        // One rank per input element.
        int[] ranks = new int[values.length];
        // Each lookup costs O(log m).
        for (int i = 0; i < values.length; i++) {
            // The position plus one is the 1-based dense rank.
            ranks[i] = Arrays.binarySearch(table, values[i]) + 1;
        }
        // Ranks are in input order.
        return ranks;
    }

    /** Oracle: counts distinct smaller values with a TreeSet of boxed longs. Time O(n log n). */
    static int[] brute(long[] values) {
        TreeSet<Long> set = new TreeSet<>();
        for (long v : values) set.add(v);
        int[] out = new int[values.length];
        for (int i = 0; i < values.length; i++) out[i] = set.headSet(values[i]).size() + 1;
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1: both ends of the long range and a repeated negative value.
        long[] ex = {Long.MAX_VALUE, -1, Long.MIN_VALUE, 0, -1};
        if (!Arrays.equals(denseRanks(ex), new int[]{4, 2, 1, 3, 2})) throw new AssertionError("example 1");
        // Checks Example 2: empty input gives empty output.
        if (denseRanks(new long[0]).length != 0) throw new AssertionError("empty");
        // Checks the Java claim: subtraction wraps around, so the comparator trick gives a wrong sign.
        if (!((int) (Long.MAX_VALUE - Long.MIN_VALUE) < 0)) throw new AssertionError("subtraction must overflow");
        if (Long.compare(Long.MAX_VALUE, Long.MIN_VALUE) <= 0) throw new AssertionError("Long.compare is safe");
        // Compares with the oracle on random inputs that mix extreme and small values.
        Random rnd = new Random(31043);
        long[] pool = {Long.MIN_VALUE, Long.MIN_VALUE + 1, -1, 0, 1, Long.MAX_VALUE - 1, Long.MAX_VALUE};
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(14);
            long[] v = new long[n];
            for (int i = 0; i < n; i++) v[i] = rnd.nextInt(3) == 0 ? rnd.nextLong() : pool[rnd.nextInt(pool.length)];
            if (!Arrays.equals(denseRanks(v), brute(v))) throw new AssertionError("random case " + t);
        }
    }
}
```

#### Solution: [Recognize] Create Sorted Array Cost (LeetCode 1649)
<!-- id: rq31-sorted-array-cost -->

**Approach.** The method compresses the values to dense ranks and keeps a Fenwick tree of counts, one position per rank.

Before inserting an element of rank `r`, the less count is `prefix(r - 1)`, the number of inserted elements with a smaller rank. The count of inserted elements with rank up to `r` is `prefix(r)`, so the greater count is the number inserted so far minus `prefix(r)`. Equal elements fall in `prefix(r)` and not in `prefix(r - 1)`, so they enter neither count. The cost is the smaller count. Then `add(r - 1, 1)` records the element, and the running total is kept modulo 1,000,000,007.

The invariant is that after `k` insertions, `prefix(p)` equals the number of inserted elements whose rank is at most `p`.

**Complexity.**

- **Time** is O(n log n), because compression costs O(n log n) and each insertion does two prefix queries and one update of O(log m).
- **Space** is O(n) for the table, the ranks and the tree.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SortedArrayCost {
    /** Fenwick tree over positions; external positions are 0-based, the internal array is 1-based. */
    static final class Fenwick {
        final long[] tree;

        Fenwick(int size) {
            // Slot 0 stays unused so that the lowest-set-bit step terminates.
            tree = new long[size + 1];
        }

        /** Adds delta at 0-based position pos. Time: O(log n). Space: O(1). */
        void add(int pos, long delta) {
            // Convert to the 1-based internal index, then climb by the lowest set bit.
            for (int i = pos + 1; i < tree.length; i += i & -i) tree[i] += delta;
        }

        /** Returns the sum of the first pos positions (internal indices 1..pos). Time: O(log n). */
        long prefix(int pos) {
            long sum = 0;
            // Descend by clearing the lowest set bit; at most log n steps.
            for (int i = pos; i > 0; i -= i & -i) sum += tree[i];
            return sum;
        }
    }

    static final long MOD = 1_000_000_007L;

    /**
     * Returns the total insertion cost modulo 1,000,000,007.
     * Time: O(n log n). Space: O(n).
     * Invariant: after k insertions, prefix(p) counts inserted elements with rank at most p.
     */
    static long totalCost(int[] instructions) {
        // Build the rank table: sorted distinct values.
        int[] copy = instructions.clone();
        Arrays.sort(copy);
        int m = 0;
        // Deduplicate in one O(n) pass.
        for (int i = 0; i < copy.length; i++) {
            if (i == 0 || copy[i] != copy[i - 1]) copy[m++] = copy[i];
        }
        int[] table = Arrays.copyOf(copy, m);
        // The tree has one position per distinct value, not per possible value.
        Fenwick fen = new Fenwick(m);
        // Total is a long and is reduced modulo MOD after every addition.
        long total = 0;
        // One iteration per instruction, each costing O(log m).
        for (int k = 0; k < instructions.length; k++) {
            // The 1-based dense rank of the current value.
            int r = Arrays.binarySearch(table, instructions[k]) + 1;
            // Inserted elements strictly below: ranks 1..r-1.
            long less = fen.prefix(r - 1);
            // Inserted elements strictly above: all k inserted so far, minus ranks 1..r.
            long greater = k - fen.prefix(r);
            // The cost is the cheaper side, and equal elements count on neither side.
            total = (total + Math.min(less, greater)) % MOD;
            // Record this element at external position r - 1.
            fen.add(r - 1, 1);
        }
        // Return the reduced total.
        return total;
    }

    /** Oracle: counts both sides by scanning all earlier elements. Time O(n^2). */
    static long brute(int[] ins) {
        long total = 0;
        for (int i = 0; i < ins.length; i++) {
            long less = 0, greater = 0;
            for (int j = 0; j < i; j++) {
                if (ins[j] < ins[i]) less++;
                if (ins[j] > ins[i]) greater++;
            }
            total = (total + Math.min(less, greater)) % MOD;
        }
        return total;
    }

    public static void main(String[] args) {
        // Checks Example 1: costs 0, 0, 0, 0, 1, 1.
        if (totalCost(new int[]{4, 9, 4, 1, 7, 7}) != 2) throw new AssertionError("example 1");
        // Checks Example 2: equal elements are strictly neither less nor greater.
        if (totalCost(new int[]{3, 3, 3, 3}) != 0) throw new AssertionError("example 2");
        // Checks a single element and the trace input.
        if (totalCost(new int[]{1000000000}) != 0) throw new AssertionError("single");
        if (totalCost(new int[]{8, 2, 5, 5, 9, 1, 5}) != 4) throw new AssertionError("trace input");
        // Compares with the oracle on random inputs from a fixed seed, with sparse large values.
        Random rnd = new Random(31044);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] v = new int[n];
            int span = rnd.nextBoolean() ? 6 : 1_000_000_000;
            for (int i = 0; i < n; i++) v[i] = 1 + rnd.nextInt(span);
            if (totalCost(v) != brute(v)) throw new AssertionError("random case " + t);
        }
    }
}
```
