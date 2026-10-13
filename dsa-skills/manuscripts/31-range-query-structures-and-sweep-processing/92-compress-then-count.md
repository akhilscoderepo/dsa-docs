<!-- lesson-kind: combination -->
<!-- lesson-id: compress-then-count -->
## Compress Values Then Count Ranks

<!-- stage: context -->
### A Counter Too Large For Memory

A monitoring service receives sensor readings one at a time. Each reading is a signed 32-bit integer, and readings such as -2,000,000,000 and 1,500,000,000 occur. For every new reading, the service must report how many earlier readings were strictly smaller. A stream of 100,000 readings arrives, and many readings repeat.

The first idea is a counter array with one slot per possible value. A slot for every 32-bit integer needs about 4.3 billion cells. A `long[]` of that size takes about 34 gigabytes, and a stream of 100,000 readings uses at most 100,000 of those cells. The memory request fails long before the first reading is processed.

Formally, the input is an `int[] values`. For each position `i`, the output is the number of positions `j < i` with `values[j] < values[i]`. The answer must use equality correctly, because a repeated reading is not smaller than itself.

This lesson asks how to answer that question for sparse values in O(n log n) time while the memory stays proportional to the number of readings.

<!-- stage: contributions -->
### What Two Earlier Skills Add

#### Compression Adds A Small Key Space

Coordinate compression sorts the distinct values and replaces each value with its position in that sorted list, starting at 1. The replacement keeps order and equality. If `a < b` holds for two readings, the same holds for their positions, and equal readings share one position. The key space shrinks from billions of possible values to at most `n` positions.

#### The Fenwick Tree Adds Cheap Prefix Sums

The Fenwick tree from the first lesson of this chapter stores one `long` per position in a one-based array. It supports `add(pos, delta)` and `prefix(pos)`, which returns the sum of positions 1 through `pos`. Both operations take O(log m) time for `m` positions. The code in this lesson uses the internal one-based form, so `add` takes the rank itself. The first lesson's `add` took a zero-based position and added 1 before the loop.

The two skills fit because each covers the weakness of the other. Compression gives small positions that a tree array can hold, and the tree answers how many stored items lie at or below a position. Neither skill alone solves the sensor problem.

<!-- stage: naive -->
### Scanning Every Earlier Reading

The direct method compares each reading with all readings before it. It needs no extra memory and is correct for any input.

```java
static int[] smallerBeforeScan(int[] values) {
    int n = values.length;
    int[] out = new int[n];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (values[j] < values[i]) out[i]++;
        }
    }
    return out;
}
```

The method is easy to trust, and it also makes a good test oracle for faster code. The inner loop reads every earlier position once. For a stream of 100,000 readings, the total is about 5 billion comparisons.

<!-- stage: bottleneck -->
### The Scan Repeats Work On Every Reading

```predict
A stream has 100,000 readings. The scan compares each reading with every earlier one. About how many comparisons does it make in total, and can a counter array indexed by value avoid them?

About 5 billion comparisons, because the inner loop runs 0, 1, 2 and so on up to 99,999 times, and that sum is n(n - 1) / 2. A counter array indexed by value avoids the comparisons but needs a cell for every possible 32-bit value, which is about 4.3 billion cells and far too much memory.
```

#### Count The Comparisons

The scan costs O(n^2) time. At roughly one billion simple comparisons per second, 5 billion comparisons take several seconds, and a stream ten times longer takes minutes. The scan also learns nothing that later readings can reuse. When reading 70,000 arrives, the scan examines readings 0 to 69,999 again, although it examined nearly all of them for reading 69,999.

#### Find The Two Opposing Costs

A counter array indexed by value answers a query by summing the cells below the reading. That sum still costs time proportional to the number of cells, and the array needs a cell per possible value. The scan needs O(1) extra memory but O(n^2) time. The value-indexed array needs O(V) memory for the largest value `V`, and a query still costs O(V) time. Both costs are too high. The goal is a structure whose memory depends on the number of readings and whose query cost depends on the logarithm of that number.

<!-- stage: insight -->
### Rank Values Then Count With A Tree

The two weaknesses have separate fixes. Order is the only property the question uses, so exact values can be replaced. A tree that adds up stored counts by position can then answer the query.

<!-- names: dense rank, rank lookup, prefix count -->

#### Replace Values With A Dense Rank

Sort the distinct values of the input into a list `keys` in increasing order. The **dense rank** of a value is its index in `keys` plus 1, so ranks run from 1 to `m`, where `m` is the number of distinct values. Equal values share one rank, and no rank is skipped. For `[30, -5, 30, 1000000, -5, 7]`, the keys are `[-5, 7, 30, 1000000]`, and the ranks are 3, 1, 3, 4, 1, 2.

The **rank lookup** finds a value's rank with binary search on `keys`. It costs O(log m) time per reading and needs no hash table. When the value is absent, `Arrays.binarySearch` returns `-p - 1`, where `p` is the number of keys smaller than the value, so the same call also counts the keys below any bound. Sorting costs O(n log n) time once, and the array `keys` uses O(m) memory. The lookup uses the sorted array, so the order of the values stays intact.

#### Count Stored Readings With A Prefix Query

Create a Fenwick tree over positions 1 to `m`. When a reading arrives, add 1 at the position of its rank. The tree then holds, for each rank, how many readings with that rank have been seen. The **prefix count** is the sum of positions 1 through `rank - 1`, and it equals the number of earlier readings with a strictly smaller rank. Because compression preserves order, those are exactly the earlier readings with a strictly smaller value.

The query happens before the add. Reading the prefix first keeps the current reading out of its own count. The query is `prefix(rank - 1)` for strictly smaller readings and `prefix(rank)` for smaller or equal readings. A reading of rank 1 asks for `prefix(0)`, which is 0 and needs no special case.

The invariant is that after `i` readings are processed, the tree holds one count for each earlier reading at the position of its rank. Every query therefore describes only the readings before it.

<!-- stage: variables -->
### Quantities For The Rank Counter

The code below uses these quantities for the stream `[30, -5, 30, 1000000, -5, 7]`.

- **keys** is the sorted array of distinct values, here `[-5, 7, 30, 1000000]`, with `m = 4`.
- **rank** is the position of the current reading in `keys` plus 1, between 1 and `m`.
- **tree** is the Fenwick array of `m + 1` longs, where index 0 stays unused.
- **smaller** is `prefix(rank - 1)`, the number of earlier readings with a strictly smaller value.
- **total** is the running sum of `smaller` over all processed readings.

In the code, the Fenwick object is named `seen`, and `smaller` is stored directly in `out[i]`. The running `total` appears only in the trace, as a check on the sum of the answers. In the trace, the variable `counts` shows how many readings of each rank have been added, listed from rank 1 to rank `m`. The array `tree` holds sums of blocks of those counts, so a trace shows `counts` because it is easier to read.

<!-- stage: trace -->
### Process Two Streams Of Readings

#### A Stream With Repeated Values

The first stream is `[30, -5, 30, 1000000, -5, 7]`. The keys are `[-5, 7, 30, 1000000]`. The pointer `i` marks the reading in progress, and each step shows the answer for that reading, taken before the reading is added.

The first reading, 30, has rank 3 and finds an empty tree, so its answer is 0. The second reading, -5, has rank 1, so its query covers no ranks and returns 0. The third reading, 30, has rank 3 again, and `prefix(2)` finds only the -5, so the answer is 1. The earlier 30 is not counted, because an equal value is not smaller.

The reading 1000000 has rank 4, and `prefix(3)` counts the two 30s and the -5, so the answer is 3. The next -5 answers 0, and the final 7 has rank 2, so it counts only the two readings of -5 and answers 2.

```trace
{"cells":[30,-5,30,1000000,-5,7],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"keys":"[-5, 7, 30, 1000000]","counts":"[0, 0, 0, 0]","total":0},"note":"Compression gives the keys [-5, 7, 30, 1000000]. The tree starts empty, so every count is 0."},{"at":{"i":0},"vars":{"value":30,"rank":3,"smaller":0,"counts":"[0, 0, 1, 0]","total":0},"note":"Step 1 reads 30, which has rank 3. The query over ranks below 3 returns 0, so the running total becomes 0. The count stored at rank 3 is now 1."},{"at":{"i":1},"vars":{"value":-5,"rank":1,"smaller":0,"counts":"[1, 0, 1, 0]","total":0},"note":"Step 2 reads -5, which has rank 1. The query over ranks below 1 returns 0, so the running total becomes 0. The count stored at rank 1 is now 1."},{"at":{"i":2},"vars":{"value":30,"rank":3,"smaller":1,"counts":"[1, 0, 2, 0]","total":1},"note":"Step 3 reads 30, which has rank 3. The query over ranks below 3 returns 1, so the running total becomes 1. The count stored at rank 3 is now 2."},{"at":{"i":3},"vars":{"value":1000000,"rank":4,"smaller":3,"counts":"[1, 0, 2, 1]","total":4},"note":"Step 4 reads 1000000, which has rank 4. The query over ranks below 4 returns 3, so the running total becomes 4. The count stored at rank 4 is now 1."},{"at":{"i":4},"vars":{"value":-5,"rank":1,"smaller":0,"counts":"[2, 0, 2, 1]","total":4},"note":"Step 5 reads -5, which has rank 1. The query over ranks below 1 returns 0, so the running total becomes 4. The count stored at rank 1 is now 2."},{"at":{"i":5},"vars":{"value":7,"rank":2,"smaller":2,"counts":"[2, 1, 2, 1]","total":6},"note":"Step 6 reads 7, which has rank 2. The query over ranks below 2 returns 2, so the running total becomes 6. The count stored at rank 2 is now 1."}]}
```

#### A Stream With Extreme Values

The second stream is `[9, 2000000000, -3, 9, 2000000000, 0, -3]`. The keys are `[-3, 0, 9, 2000000000]`. The value 2,000,000,000 is far above the others, and compression gives it rank 4, the same as any other largest value.

The hardest step is the fifth reading. The value 2,000,000,000 appears for the second time. Its rank is 4, and `prefix(3)` counts the readings 9, -3 and 9, so the answer is 3. The earlier 2,000,000,000 does not count. The last step repeats the lowest value -3 and answers 0, because no earlier reading is smaller.

```trace
{"cells":[9,2000000000,-3,9,2000000000,0,-3],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"keys":"[-3, 0, 9, 2000000000]","counts":"[0, 0, 0, 0]","total":0},"note":"Compression gives the keys [-3, 0, 9, 2000000000]. The tree starts empty, so every count is 0."},{"at":{"i":0},"vars":{"value":9,"rank":3,"smaller":0,"counts":"[0, 0, 1, 0]","total":0},"note":"Step 1 reads 9, which has rank 3. The query over ranks below 3 returns 0, so the running total becomes 0. The count stored at rank 3 is now 1."},{"at":{"i":1},"vars":{"value":2000000000,"rank":4,"smaller":1,"counts":"[0, 0, 1, 1]","total":1},"note":"Step 2 reads 2000000000, which has rank 4. The query over ranks below 4 returns 1, so the running total becomes 1. The count stored at rank 4 is now 1."},{"at":{"i":2},"vars":{"value":-3,"rank":1,"smaller":0,"counts":"[1, 0, 1, 1]","total":1},"note":"Step 3 reads -3, which has rank 1. The query over ranks below 1 returns 0, so the running total becomes 1. The count stored at rank 1 is now 1."},{"at":{"i":3},"vars":{"value":9,"rank":3,"smaller":1,"counts":"[1, 0, 2, 1]","total":2},"note":"Step 4 reads 9, which has rank 3. The query over ranks below 3 returns 1, so the running total becomes 2. The count stored at rank 3 is now 2."},{"at":{"i":4},"vars":{"value":2000000000,"rank":4,"smaller":3,"counts":"[1, 0, 2, 2]","total":5},"note":"Step 5 reads 2000000000, which has rank 4. The query over ranks below 4 returns 3, so the running total becomes 5. The count stored at rank 4 is now 2."},{"at":{"i":5},"vars":{"value":0,"rank":2,"smaller":1,"counts":"[1, 1, 2, 2]","total":6},"note":"Step 6 reads 0, which has rank 2. The query over ranks below 2 returns 1, so the running total becomes 6. The count stored at rank 2 is now 1."},{"at":{"i":6},"vars":{"value":-3,"rank":1,"smaller":0,"counts":"[2, 1, 2, 2]","total":6},"note":"Step 7 reads -3, which has rank 1. The query over ranks below 1 returns 0, so the running total becomes 6. The count stored at rank 1 is now 2."}]}
```

<!-- stage: code -->
### Rank Values And Query The Tree

The class below holds the tree, the compression step and the counting loop.

```java
final class RankCounter {
    static final class Fenwick {
        final long[] tree;
        Fenwick(int size) { tree = new long[size + 1]; }
        void add(int pos, long delta) {
            for (int i = pos; i < tree.length; i += i & -i) tree[i] += delta;
        }
        long prefix(int pos) {
            long sum = 0;
            for (int i = pos; i > 0; i -= i & -i) sum += tree[i];
            return sum;
        }
    }

    static int[] distinctSorted(int[] values) {
        int[] sorted = values.clone();
        java.util.Arrays.sort(sorted);
        int m = 0;
        for (int v : sorted) {
            if (m == 0 || sorted[m - 1] != v) sorted[m++] = v;
        }
        return java.util.Arrays.copyOf(sorted, m);
    }

    static int[] smallerBefore(int[] values) {
        int[] keys = distinctSorted(values);
        Fenwick seen = new Fenwick(keys.length);
        int[] out = new int[values.length];
        for (int i = 0; i < values.length; i++) {
            int rank = java.util.Arrays.binarySearch(keys, values[i]) + 1;
            out[i] = (int) seen.prefix(rank - 1);
            seen.add(rank, 1);
        }
        return out;
    }
}
```

The code runs in O(n log n) time. Sorting takes O(n log n), and each reading costs one binary search plus one prefix query and one add, each O(log m). Memory is O(n) for the copy, the keys and the tree. The binary search always finds a hit, because every reading is in `keys`. An empty input gives an empty `keys`, a tree of size 0 and an empty result. The tree stores `long` values, because the sums in later exercises can pass the `int` range.

<!-- stage: applicability -->
### When Ranks And A Tree Fit

#### Recognize The Cue

Use this pair when the question compares values by order, the values are sparse or huge, and the data changes between queries. Typical signals are counting earlier smaller items, counting inversions, and keeping a running count of values in a range while items arrive. Plain compression is enough when nothing changes. The tree is needed when the answer must follow each addition.

#### Check The Invariant

The invariant is that the tree holds one count per processed reading at the position of its rank. Test it with an empty input, one value, all-equal values, strictly ascending and descending input, and the extreme values `Integer.MIN_VALUE` and `Integer.MAX_VALUE`. Compare the result against the scan on random small inputs.

#### Watch For The False Friend

The first false friend is a plain `HashMap` from value to count. A hash map answers how often one exact value occurred, and it cannot answer how many values lie below it without scanning. The second false friend is the comparison `a - b` inside a custom sort. It overflows for extreme values and breaks the order that the ranks rely on. Use `Integer.compare` or sort primitives directly.

#### Know When Not To Use It

Skip compression when the values already form a small dense range, since a direct array is simpler. Skip it when the query values are not known when the structure is built and cannot be ranked in advance. In that case an ordered tree structure supports insertion directly. Also stay with the scan for very small inputs, where the logarithmic factors cost more than they save.

<!-- stage: exercises -->
### Exercises

#### [Build] Compress Sparse Coordinates (Author exercise)
<!-- id: rq31-compress-sparse -->

**Prerequisites.** The sorted distinct keys and the rank lookup from this lesson.

**Problem.** An `int[] values` and an `int[] queries` are given. Let `keys` be the distinct entries of `values` in increasing order. The rank of a value is its 1-based position in `keys`. For each query, return how many entries of `keys` are strictly smaller than the query, whether or not the query occurs in `values`. Return the answers in query order.

**Constraints.** The limits are:
- **`values`** has length from 0 to 100,000, and the array may be empty.
- **`queries`** has length from 1 to 100,000.
- **Entries** are `int` values between -10^9 and 10^9, and equal entries count once.
- **Result** is an `int[]` with one entry per query.
- **Mutation** of the input arrays is not allowed.

**Example 1.** Input `values = [900, -40, 900, 12, 7000000]`, `queries = [12, 900, 13, -40, 7000000]`, output `[1, 2, 2, 0, 3]`.

**Example 2.** Input `values = []`, `queries = [5]`, output `[0]`, since no value is stored and no key is smaller.

**Hint.** How do you remove duplicates after sorting? What does `Arrays.binarySearch` return for a value that is absent?

**Changed decision.** The task asks for the count of smaller keys and not the rank, so an absent query must still get an answer. The lookup must turn a missing value into its insertion point.

#### [Vary] Range Sum With Sparse Keys (LeetCode 307)
<!-- id: rq31-sparse-key-sum -->

**Prerequisites.** The exercise above and the Fenwick tree from this lesson.

**Problem.** This is a variant of LeetCode 307 in which positions are arbitrary keys. Every key starts with value 0. An operation `{0, key, value}` sets the value stored at `key` to `value`, replacing any earlier value. An operation `{1, lo, hi}` asks for the sum of the values stored at keys `k` with `lo <= k <= hi`. The bounds `lo` and `hi` need not be keys that were ever set. Return the answers of the sum operations in order.

**Constraints.** The limits are:
- **Operations** number from 1 to 100,000, and all are known before processing starts.
- **Keys** and bounds are `long` values between -10^12 and 10^12, with `lo <= hi`.
- **Values** are `long` values between -10^9 and 10^9.
- **Result** is a `long[]` with one entry per sum operation.
- **Mutation** of the operation array is not allowed.

**Example 1.** Input `ops = [[0,100,5],[0,-3,7],[1,-10,100],[0,100,2],[1,0,99],[1,100,100],[0,1000000000000,-4],[1,-3,1000000000000]]`, output `[12, 0, 2, 5]`.

**Example 2.** Input `ops = [[0,5,3],[0,5,3],[1,5,5]]`, output `[3]`, because setting the same key twice does not add the value twice.

**Hint.** Which keys can ever hold a value? What delta must the tree receive when a key is overwritten? How do you turn a bound that is not a key into a rank?

**Changed decision.** Updates replace a value and do not add to it, so the tree needs the difference from the stored value. Range ends can fall between keys, so each end needs a count of keys at or below it.

#### [Boundary] Negative And Extreme Coordinates (Author exercise)
<!-- id: rq31-extreme-coordinates -->

**Prerequisites.** The two exercises above and the overflow warning in the applicability stage.

**Problem.** An `int[] values` is given. Compute the 1-based rank of every entry among the distinct entries in increasing order. Also compute the largest difference between two neighbouring distinct values, as a `long`. If fewer than two distinct values exist, that difference is 0. Return a `long[]` of length `n + 1`. Entry `i` for `i < n` is the rank of `values[i]`, and the last entry is the largest difference.

**Constraints.** The limits are:
- **Length** `n` is from 1 to 100,000.
- **Entries** are any `int` values, including `Integer.MIN_VALUE` and `Integer.MAX_VALUE`.
- **Ties** share one rank, and ranks have no gaps.
- **Difference** is computed as a `long`, because the true value can exceed `Integer.MAX_VALUE`.
- **Mutation** of the input array is not allowed.

**Example 1.** Input `values = [2147483647, -2147483648, 0, -2147483648]`, output `[3, 1, 2, 1, 2147483648]`.

**Example 2.** Input `values = [7, 7, 7]`, output `[1, 1, 1, 0]`, since one distinct value has no neighbour.

**Hint.** What does `a - b` return in `int` arithmetic when the true result is above `Integer.MAX_VALUE`? Which conversion prevents the overflow?

**Changed decision.** The comparison must be safe and the neighbour difference must widen to `long` before it subtracts. A value is never used as an array index.

#### [Recognize] Insertion Cost By Smaller Count (LeetCode 1649)
<!-- id: rq31-smaller-insertion-cost -->

**Prerequisites.** All three exercises above and the counting loop from this lesson.

**Problem.** This is a variant of LeetCode 1649 with a one-sided cost. The entries of `instructions` are inserted one at a time into an initially empty sorted container. The cost of inserting an entry equals the number of entries already in the container that are strictly smaller than it. Entries that are equal or larger add nothing. Return the total cost modulo 1,000,000,007.

**Constraints.** The limits are:
- **Length** is from 1 to 100,000.
- **Entries** are `int` values between -10^9 and 10^9.
- **Ties** are not smaller, so equal entries add 0.
- **Result** is an `int` in the range 0 to 1,000,000,006.
- **Mutation** of the input array is not allowed.

**Example 1.** Input `instructions = [8, -2, 8, 5, -2, 1000000000, 5]`, output `9`.

**Example 2.** Input `instructions = [1, 2, 3, ..., 100000]` in ascending order, output `999949972`, because the true total 4,999,950,000 is reduced by the modulus.

**Hint.** Which prefix query counts strictly smaller entries? Why must the total be a `long` before the reduction?

**Changed decision.** The cost uses only the count of strictly smaller entries, with no minimum against the larger side. The total passes the modulus, so it needs `long` accumulation.
