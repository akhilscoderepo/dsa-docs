<!-- lesson-kind: standard -->
<!-- lesson-id: fenwick-trees -->
## Fenwick Trees

<!-- stage: context -->
### Why Running Totals Slow Down After Edits

A dashboard shows the number of requests per minute for the last 200,000 minutes. Operators ask for the total between two minutes many times a second. Late events also arrive, and each one changes the count of a single minute that already passed.

A prefix-sum array answers each total with one subtraction, so the questions are cheap. The trouble starts when a count changes. Every prefix sum after the changed minute is now wrong, and the array must be repaired. The program needs both operations to stay fast at the same time, and the prefix-sum array makes only one of them fast. The question for this lesson is how a program keeps point changes and range totals cheap together.

<!-- stage: naive -->
### Rebuilding The Prefix Array After Each Change

The direct approach keeps the prefix-sum array and rebuilds the affected part after every change. The method below changes one count and repairs every prefix sum from that position onward.

```java
static void update(long[] prefix, int pos, long delta) {
    for (int i = pos + 1; i < prefix.length; i++) {
        prefix[i] += delta;            // every prefix that contains position pos shifts by delta
    }
}

static long rangeSum(long[] prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];   // two reads answer any total
}
```

Here `prefix[k]` holds the sum of the first `k` counts, and `prefix[0]` is 0. The range query is a single subtraction. The update touches every entry after `pos`, which is up to `n` entries. A change near the start of the data repairs almost the whole array.

<!-- stage: bottleneck -->
### Updates Cost O(n) Each

```predict
A prefix-sum array holds 200,000 counts. A program runs 200,000 operations, and half of them change a count at a random position. About how many array writes do the changes cost in total?

About ten billion writes. Each change rewrites on average half of the 200,000 entries, which is 100,000 writes, and there are 100,000 changes. The total grows as the number of changes times the array length.
```

#### Count The Writes

One update writes up to `n` entries, so it costs O(n). With `q` updates mixed into the workload, the total cost is O(n * q). For `n = q = 200,000` the product is 4 * 10^10 in the worst case, and a typical run still writes ten billion entries. A program that does that much work per second misses any real-time deadline.

#### Compare The Two Extremes

Dropping the prefix array and summing the range on demand has the opposite profile. An update becomes one write, but each query reads up to `n` counts, so a query costs O(n). One extreme makes queries cheap and updates expensive. The other extreme does the reverse. Both extremes cost O(n * q) for a workload that mixes the two operations evenly. The structure we need must store partial sums in a way that lets one update repair only a few of them and lets one query combine only a few of them.

<!-- stage: insight -->
### Store Partial Sums By Low Bit

#### Define The Low Bit

The **low bit** of a positive integer `i` is the value of its lowest set bit in binary, and Java computes it as `i & -i`. The number 6 is `110` in binary, and its low bit is 2. The number 8 is `1000`, and its low bit is 8. Java stores negative numbers in two's complement, where `-i` equals the bitwise complement of `i` plus one. That operation flips every bit above the lowest set bit and keeps the lowest set bit and the zeros below it. The bitwise AND of `i` and `-i` therefore keeps only the lowest set bit.

#### Give Every Index A Block Length

A **Fenwick tree** is an array `tree` of sums, indexed from 1. Entry `tree[i]` stores the sum of the `i & -i` counts that end at position `i`. The entry `tree[6]` stores positions 5 and 6, because the low bit of 6 is 2. The entry `tree[8]` stores positions 1 to 8, and `tree[7]` stores only position 7. Each entry covers a **block length** equal to its low bit, so odd indexes cover one count and indexes that are powers of two cover everything before them.

<!-- names: Fenwick tree, low bit, update path -->

#### Query By Clearing The Low Bit

The sum of the first `k` counts splits into blocks. Start at `i = k`, add `tree[i]`, and replace `i` by `i - (i & -i)`. That step removes the lowest set bit of `i`, and the removed block ends exactly where the next block must begin. Repeat until `i` reaches 0. The loop runs once per set bit of `k`, which is at most `log2(n) + 1` times.

#### Update By Adding The Low Bit

A change at position `p` affects every block that contains `p`. Start at `i = p`, add the delta to `tree[i]`, and replace `i` by `i + (i & -i)`. This step moves to the next larger block that contains `p`. The indexes visited form the **update path**. Each step raises the lowest set bit, so the path leaves the array after at most `log2(n) + 1` steps. Both operations cost O(log n), and the invariant that makes them correct is that `tree[i]` always equals the sum of the `i & -i` counts ending at `i`.

<!-- stage: variables -->
### Quantities To Track In The Array

Track these items while reading or changing the array.

- **tree** is a `long[]` of length `n + 1`, and slot 0 stays unused.
- **i** is the internal one-based index that the loops move.
- **i & -i** is the low bit, which is both the block length and the step size.
- **pos** is the zero-based position that the caller uses.
- **delta** is the signed amount that a change adds to one count.

The caller passes a zero-based `pos`, and the class converts it to the internal index `pos + 1` before any loop starts. The method `prefix(k)` returns the sum of the first `k` counts, which are internal positions 1 to `k`. The range sum of external positions `left` to `right` is `prefix(right + 1) - prefix(left)`.

<!-- stage: trace -->
### Follow One Update And One Query

Take eight counts `3, 1, 4, 1, 5, 9, 2, 6`. The array `tree` for them is `0, 3, 4, 4, 9, 5, 14, 2, 31`, where the leading 0 is the unused slot.

#### Add Ten At Position Two

The call `add(2, 10)` converts position 2 to internal index 3. The entry `tree[3]` covers one count, so it changes first. Index 3 plus its low bit 1 gives 4. The entry `tree[4]` covers positions 1 to 4, which contain position 3, so it changes next. Index 4 plus its low bit 4 gives 8, and `tree[8]` covers all eight positions, so it changes last. Index 8 plus 8 is 16, which is past the array, so the loop stops.

```trace
{"cells":[0,3,4,4,9,5,14,2,31],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"pos":2,"delta":10},"note":"The call converts position 2 to internal index 3. No entry has changed yet."},{"at":{"i":3},"vars":{"lowBit":1,"newValue":14},"note":"Index 3 has low bit 1, so its block covers positions 3 to 3. The entry becomes 14."},{"at":{"i":4},"vars":{"lowBit":4,"newValue":19},"note":"Index 4 has low bit 4, so its block covers positions 1 to 4. The entry becomes 19."},{"at":{"i":8},"vars":{"lowBit":8,"newValue":41},"note":"Index 8 has low bit 8, so its block covers positions 1 to 8. The entry becomes 41. The next index is 16, which is past the last slot 8, so the loop stops."}]}
```

#### Sum The First Six Positions

The call `prefix(6)` runs on the updated array. It starts at index 6, where `tree[6]` covers positions 5 and 6. Removing the low bit 2 leaves index 4. The entry `tree[4]` covers positions 1 to 4 and now includes the added ten. Removing the low bit 4 leaves index 0, and the loop stops after two reads.

```trace
{"cells":[0,3,4,14,19,5,14,2,41],"pointers":["i"],"steps":[{"at":{"i":6},"vars":{"sum":0},"note":"The query starts at index 6 with a running sum of 0."},{"at":{"i":6},"vars":{"lowBit":2,"sum":14},"note":"The entry at index 6 covers positions 5 to 6 and adds 14. The running sum is 14."},{"at":{"i":4},"vars":{"lowBit":4,"sum":33},"note":"The entry at index 4 covers positions 1 to 4 and adds 19. The running sum is 33."},{"at":{"i":0},"vars":{"lowBit":0,"sum":33},"note":"The index reaches 0, so the loop stops with the answer 33."}]}
```

The hardest step is the first jump in the update, from index 3 to index 4. Index 3 is odd, so its block holds one count, and the next block that contains it is the larger block ending at 4. The two traces use different jumps, and each visits only three or fewer entries out of eight.

<!-- stage: code -->
### Implement Add And Prefix

```java
final class Fenwick {
    final long[] tree;                       // internal one-based storage, slot 0 unused

    Fenwick(int n) {
        tree = new long[n + 1];              // n counts need n + 1 slots
    }

    void add(int pos, long delta) {
        for (int i = pos + 1; i < tree.length; i += i & -i) {
            tree[i] += delta;                // each visited block contains the changed position
        }
    }

    long prefix(int k) {
        long sum = 0;
        for (int i = k; i > 0; i -= i & -i) {
            sum += tree[i];                  // each visited block ends where the next one begins
        }
        return sum;
    }

    long range(int left, int right) {
        return prefix(right + 1) - prefix(left);   // counts left..right as a difference of prefixes
    }
}
```

The class has no separate build method, because a new tree holds all zeros and a loop of `add` calls loads the starting counts. That load costs O(n log n). The update loop ends because `i` grows and passes `tree.length`. The query loop ends because `i` shrinks to 0. The sums use `long`, so large counts do not overflow an `int`.

<!-- stage: applicability -->
### When A Fenwick Tree Applies

#### Recognize The Pattern

Use this structure when point changes and prefix or range sums must both stay O(log n). The data must be a sequence of numbers where a sum of a range equals a difference of two prefix sums. That rule holds for sums, counts and bitwise exclusive-or, and it fails for minimum and maximum, which cannot be subtracted.

The invariant to check before coding is that `tree[i]` equals the sum of the `i & -i` counts ending at `i`. Every change must keep it true, and every query must rely only on it.

#### Watch For The Nearest False Friend

A prefix-sum array is a false friend here. It looks like the right tool because it answers range sums, but it only works when the data never changes. If the data is fixed, prefer the prefix-sum array, because its query reads two entries and it needs no loop. If the program needs range minimum on fixed data, a different structure fits better, and a later lesson covers the segment tree for operations that cannot be subtracted.

#### Avoid The Java Index Trap

The loops need a one-based index. With index 0 the expression `0 & -0` is 0, so the update loop never moves and runs forever. The class therefore converts every external zero-based position to `pos + 1` once, at the boundary. Keep the sums in `long`, and let the query for an empty prefix return 0 without reading `tree[0]`.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix Query (Author exercise)
<!-- id: rq31-fenwick-prefix -->

**Prerequisites.** The low bit and the block lengths from this lesson.

**Problem.** A Fenwick tree for `n` counts is stored in an array `tree` of length `n + 1`. Slot 0 is unused, and `tree[i]` is the sum of the `i & -i` counts that end at position `i`. Given `tree` and an integer `k`, return the sum of the first `k` counts.

**Constraints.** The limits are:
- **`n`** is an `int` with `0 <= n <= 10^5`.
- **`k`** is an `int` with `0 <= k <= n`.
- **Counts** are `long` values with absolute value at most `10^9`.
- **Return** is a `long`, and `k = 0` returns 0.
- **Mutation** of `tree` is not allowed.

**Example 1.** Input `tree = [0, 3, 4, 4, 9, 5, 14, 2, 31]` and `k = 5`, output 14, from `tree[5] + tree[4]`.

**Example 2.** Input the same `tree` and `k = 0`, output 0, since no block is read.

**Hint.** Which blocks end at 5 and then at the index you reach by clearing the low bit?

**Changed decision.** Baseline case: reads partial sums by clearing the low bit.

#### [Vary] Point Update (Author exercise)
<!-- id: rq31-fenwick-point-update -->

**Prerequisites.** The prefix query exercise above.

**Problem.** Start with `n` counts that are all 0 and an empty Fenwick tree. Process a list of assignments. Each assignment `(pos, value)` sets the count at zero-based position `pos` to `value`, replacing the old count. Return the array `tree` after all assignments.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 10^5`.
- **`pos`** is an `int` with `0 <= pos < n`.
- **`value`** is a `long` with absolute value at most `10^9`.
- **Assignments** number at most `10^5`, and a position can repeat.
- **Return** is a `long[]` of length `n + 1` with slot 0 equal to 0.

**Example 1.** Input `n = 6` and assignments `(2, 5), (0, 3), (2, 1), (5, 4)`, output `[0, 3, 3, 1, 4, 0, 4]`.

**Example 2.** Input `n = 5` and assignments `(4, 9), (4, 2), (1, 6)`, output `[0, 0, 6, 0, 6, 2]`.

**Hint.** The tree adds a delta and does not store assignments. What delta turns the old count into the new one?

**Changed decision.** The operation changes from adding a delta to replacing a value, so the program must remember the current count.

#### [Boundary] Index Conversion (Author exercise)
<!-- id: rq31-fenwick-index-conversion -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `a` of `n` counts and a list of queries `(left, right)` with zero-based inclusive bounds, return the sum of `a[left..right]` for each query. Answer them with a Fenwick tree built from `a`, and convert between external and internal indexes at the boundary.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 10^5`.
- **Bounds** satisfy `0 <= left <= right < n`.
- **Counts** are `long` values with absolute value at most `10^9`, and may be negative or 0.
- **Queries** number at most `10^5`.
- **Return** is a `long[]` with one sum per query.

**Example 1.** Input `a = [4, -2, 7, 0, 5, -3]` and queries `(0, 0), (0, 5), (2, 4), (5, 5)`, output `4, 11, 12, -3`.

**Example 2.** Input the same `a` and the query `(0, 2)`, output 9, which needs the empty prefix `prefix(0)`.

**Hint.** Which internal prefixes does the query `(left, right)` need, and what does the prefix for `left = 0` return?

**Changed decision.** The boundary queries start at the first position and end at the last, where a wrong index conversion fails.

#### [Recognize] Mutable Range Sum (LeetCode 307)
<!-- id: rq31-fenwick-range-sum-mutable -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class built from an integer array `nums`. The call `update(index, val)` assigns `val` to position `index`. The call `sumRange(left, right)` returns the total of positions `left` to `right`, both included. Indexes are zero-based.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `1 <= n <= 3 * 10^4`.
- **Values** are `int` values with absolute value at most `100`.
- **Calls** to either method number at most `3 * 10^4`.
- **Bounds** satisfy `0 <= left <= right < n` and `0 <= index < n`.
- **Return** of `sumRange` is an `int`.

**Example 1.** Input `nums = [6, -1, 4, 3, 8]` with the calls `sumRange(1, 3)`, `update(2, 10)`, `sumRange(1, 3)`, output 6 and then 12.

**Example 2.** Input the updated array and the calls `sumRange(0, 4)`, `sumRange(4, 4)`, output 26 and then 8.

**Hint.** Both operations alternate on one array. Which structure keeps each of them logarithmic?

**Changed decision.** The array changes between queries, so the fixed prefix-sum array no longer works.
