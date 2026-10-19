<!-- lesson-kind: standard -->
<!-- lesson-id: mutable-range-queries -->
## Mutable Range Queries

<!-- stage: context -->
### Why Corrections Break Stored Totals

A metrics service keeps one counter per minute for the last 100,000 minutes. Analysts ask for the total between two minutes, and the service answers in constant time because it stores running totals. Then late events arrive. Each one corrects a single minute, and every running total after that minute is now wrong. The service rebuilds all running totals after each correction. With a thousand corrections per second, the rebuild work swamps the work of answering queries.

The stored totals are not buggy. They answer a question about data that never changes, and the data now changes between questions. This lesson asks how to keep range totals correct when single values change, without paying a cost proportional to the whole array for each change. It also asks which structure to choose when the question is not a sum.

<!-- stage: naive -->
### Rebuilding Running Totals After Every Change

The direct design keeps an array of running totals, where `total[k]` is the sum of the first `k` values. A query subtracts two entries. A change rewrites the value and then recomputes every running total.

```java
final class RebuildingSums {
    private final long[] values;
    private final long[] total;               // total[k] = values[0] + ... + values[k - 1]

    RebuildingSums(int[] start) {
        values = new long[start.length];
        total = new long[start.length + 1];
        for (int i = 0; i < start.length; i++) values[i] = start[i];
        rebuild();
    }

    private void rebuild() {
        for (int k = 0; k < values.length; k++) total[k + 1] = total[k] + values[k];
    }

    void update(int index, int value) {
        values[index] = value;
        rebuild();                             // touches every entry after the change
    }

    long sum(int from, int to) {               // half-open range [from, to)
        return total[to] - total[from];
    }
}
```

Queries are fast and correct. Every update pays for a full pass over the array.

<!-- stage: bottleneck -->
### Updates Cost As Much As Rebuilding

```predict
An array holds 100,000 values. The program performs 100,000 updates and 100,000 queries in mixed order. About how many additions does `RebuildingSums` execute?

About ten billion additions. Each of the 100,000 updates rebuilds 100,000 entries, and the queries add almost nothing. The data is small, but the update cost multiplies with the number of updates.
```

Count the work per call. A query executes one subtraction, which is O(1). An update executes `n` additions, which is O(n). A workload with `u` updates and `q` queries therefore costs `u * n + q`. When `u` is close to `n`, the total is O(n^2), and the cheap queries no longer matter.

The opposite design makes the same mistake in the other direction. Reading the values directly makes an update O(1) and a query O(n), because each query adds the whole range. Both designs put the full cost on one side. The update and query ratio is an input to the design, so a workload with many calls of both kinds needs a structure where neither call touches the whole array.

<!-- stage: insight -->
### Share The Cost Between Updates And Queries

#### Give Each Entry A Small Range

A Fenwick tree keeps an array of `n` partial sums, where each entry stores the total of a short block of positions that it covers. Number the entries from 1. Entry `i` covers the **owned range** of positions `i - lowbit(i) + 1` through `i`, counted from 1. Here `lowbit(i)` is the largest power of two that divides `i`, which the expression `i & -i` computes. Entry 6 covers positions 5 and 6, entry 4 covers positions 1 through 4, and every odd entry covers only itself.

<!-- names: owned range, delta, lowbit -->

#### Walk Up To Update And Down To Query

A prefix query adds the entry at `i`, jumps to `i - lowbit(i)`, and repeats until the index reaches 0. The owned ranges of the visited entries tile the first `i` positions with no gap and no overlap. Each jump clears the lowest set bit of the index, so the walk takes at most log2(n) + 1 steps.

An update must reach every entry whose owned range contains the changed position. Those entries are `i`, then `i + lowbit(i)`, and so on until the index passes `n`. Each jump moves to the next larger entry that covers the position, and the walk again takes O(log n) steps.

#### Apply The Delta Instead Of The New Value

The update walk adds a **delta** to each entry on its path, where delta is the new value minus the old value stored at that position. The structure keeps a plain copy of the values so that it can compute the old value. Adding the new value itself would count the position twice. Setting a position to the value it already holds gives a delta of 0 and changes nothing.

#### Extend The Same Rule To Two Dimensions

A matrix uses one Fenwick walk nested inside another. The outer walk moves over rows and the inner walk moves over columns, and entry `(r, c)` covers a rectangle of cells. An update visits O(log m * log n) entries. A rectangle sum combines four prefix queries by inclusion and exclusion. The invariant stays the same: after every call, each entry equals the exact sum over the cells it owns.

<!-- stage: variables -->
### Fix The Meaning Of Each Index

Decide the meaning of every index and range before writing a comparison.

- **Position `p`** is a zero-based index into the caller's array, with `0 <= p < n`.
- **Entry `i`** is a one-based index into the tree, and `i = p + 1` maps a position to its first entry.
- **Prefix `end`** is exclusive, so `prefix(end)` sums positions `0` through `end - 1`.
- **Range** is half-open `[from, to)` inside the structure, and `sum(from, to) = prefix(to) - prefix(from)`.
- **Values** are `long` in the tree, because many `int` values add up past 2^31.

A closed range `[left, right]` from a caller converts once, at the boundary, to `[left, right + 1)`.

<!-- stage: trace -->
### Update One Position And Query A Range

Take the values `[3, 1, 4, 1, 5, 9]`. In one-based terms, entries 1 to 6 own the positions 1, 1 to 2, 3, 1 to 4, 5 and 5 to 6. Their stored sums are 3, 4, 4, 9, 5 and 14.

The first trace sets zero-based position 2 from 4 to 10. The delta is 6. The walk starts at entry 3, adds 6 and jumps to entry 4, because `3 + lowbit(3)` is 4. Entry 4 gains 6 and becomes 15. The next jump reaches entry 8, which lies past the last entry, so the walk stops. Entries 1, 2, 5 and 6 do not cover position 2 and stay unchanged.

The second trace queries the half-open range `[1, 5)`. It computes `prefix(5) - prefix(1)`. The prefix at 5 adds entry 5, jumps to entry 4, adds it and jumps to entry 0. The prefix at 1 reads entry 1 only. The results are 20 and 3, so the range sum is 17, which equals `1 + 10 + 1 + 5`. Each walk touches at most three entries in an array of six.

```trace
{"cells":["3","1","10","1","5","9"],"pointers":["node"],"steps":[{"at":{"node":2},"vars":{"delta":6,"tree":"3,4,4,9,5,14"},"note":"Set position 2 to 10. The delta is 6, and the walk starts at entry 3."},{"at":{"node":2},"vars":{"delta":6,"tree":"3,4,10,9,5,14"},"note":"Entry 3 owns a range that contains position 2, so it gains 6 and becomes 10. The next entry is 3 + 1 = 4."},{"at":{"node":3},"vars":{"delta":6,"tree":"3,4,10,15,5,14"},"note":"Entry 4 owns a range that contains position 2, so it gains 6 and becomes 15. The next entry is 4 + 4 = 8."},{"at":{"node":5},"vars":{"delta":6,"tree":"3,4,10,15,5,14"},"note":"The next entry would be 4 + 4 = 8, which lies past the last entry 6, so the walk stops. Only entries on the path changed."}]}
```

```trace
{"cells":["3","1","10","1","5","9"],"pointers":["node"],"steps":[{"at":{"node":4},"vars":{"hi":5,"tree":"3,4,10,15,5,14"},"note":"Entry 5 adds 5, so hi becomes 5. The next entry is 5 - 1 = 4."},{"at":{"node":3},"vars":{"hi":20,"tree":"3,4,10,15,5,14"},"note":"Entry 4 adds 15, so hi becomes 20. The next entry is 4 - 4 = 0."},{"at":{"node":0},"vars":{"lo":3,"tree":"3,4,10,15,5,14"},"note":"Entry 1 adds 3, so lo becomes 3. The next entry is 1 - 1 = 0."},{"at":{"node":4},"vars":{"hi":20,"lo":3,"sum":17,"tree":"3,4,10,15,5,14"},"note":"The range sum is 20 - 3 = 17, which equals 1 + 10 + 1 + 5."}]}
```

<!-- stage: code -->
### Implement The Tree With Update And Sum

```java
final class MutableSums {
    private final int n;
    private final long[] tree;       // tree[i] sums the owned range of entry i, one-based
    private final long[] values;     // current value at each zero-based position

    MutableSums(int n) {
        this.n = n;
        tree = new long[n + 1];
        values = new long[n];
    }

    void set(int position, long value) {
        long delta = value - values[position];       // change from the stored value
        values[position] = value;
        for (int i = position + 1; i <= n; i += i & -i) tree[i] += delta;
    }

    private long prefix(int end) {                   // sum of positions [0, end)
        long sum = 0;
        for (int i = end; i > 0; i -= i & -i) sum += tree[i];
        return sum;
    }

    long sum(int from, int to) {                     // half-open range [from, to)
        return prefix(to) - prefix(from);
    }
}
```

The delta is a `long`, so subtracting two `int`-sized values cannot wrap. The tree starts with zeros, which matches an all-zero array. A caller with starting values calls `set` once per position, for a total of O(n log n) setup time.

<!-- stage: applicability -->
### Check The Workload And The Operation

#### Match The Structure To The Calls

Reach for this structure when updates and queries interleave and both are frequent. If all updates come before all queries, one prefix array built once is simpler and faster. If calls are known in advance, sorting them offline can also remove the need for a dynamic structure. Each of those choices depends on the update and query ratio, so state it before choosing.

#### Check The Operation Has An Inverse

The invariant of the tree is that each entry equals the exact sum over its owned range after every update. The delta update preserves it only because addition can be undone by subtraction. A range minimum has no such inverse, because removing a value from a stored minimum does not reveal the next smallest one. Treating the Fenwick tree as a general range structure is a false friend. For minimum, maximum and greatest common divisor with arbitrary assignment, use a segment tree that recomputes each node from its two children.

#### Keep Endpoints And Types Consistent

Convert every caller range to half-open once, at the public method. Store sums as `long`. A mix of closed and half-open comparisons inside the tree produces off-by-one totals that pass small tests and fail near the array ends.

<!-- stage: exercises -->
### Exercises

#### [Build] Mutable Range Sum (LeetCode 307)
<!-- id: dq39-mutable-range-sum -->

**Prerequisites.** Fenwick tree walks from this lesson.

**Problem.** Design a class over an integer array `nums` with two operations. `update(index, val)` assigns `val` to `nums[index]`. `sumRange(left, right)` returns the sum of `nums[left]` through `nums[right]`, where both endpoints are included. Calls interleave in any order and arrive online, so no later call is known in advance. The update and query counts are about equal.

**Constraints.** The limits are:
- **`nums.length`** satisfies `1 <= n <= 3 * 10^4`.
- **Values** are `int` with `-100 <= nums[i], val <= 100`.
- **Indices** satisfy `0 <= index < n` and `0 <= left <= right < n`.
- **Calls** number at most `3 * 10^4` in total.
- **Return value** of `sumRange` is a `long`.

**Example 1.** Input `nums = [3, 1, 4, 1, 5, 9]` with `sumRange(1, 3)`, `update(2, 10)`, `sumRange(1, 3)`, output 6 and then 12.

**Example 2.** Input `nums = [7]` with `update(0, -2)`, `sumRange(0, 0)`, output -2.

**Hint.** Which value must the update add to every covering entry: the new value or the difference from the old one? Which index does a closed right endpoint become in a half-open prefix?

**Changed decision.** Static running totals become a tree of owned ranges, so both calls cost O(log n).

#### [Vary] Mutable Matrix Region Sum (LeetCode 308)
<!-- id: dq39-mutable-matrix-sum -->

**Prerequisites.** The mutable range sum exercise above.

**Problem.** Design a class over an integer matrix. `update(row, col, val)` assigns `val` to one cell. `sumRegion(row1, col1, row2, col2)` returns the sum of all cells with `row1 <= r <= row2` and `col1 <= c <= col2`, where all four bounds are included. Calls arrive online. Queries outnumber updates by about four to one.

**Constraints.** The limits are:
- **Dimensions** satisfy `1 <= m, n <= 200` for `m` rows and `n` columns.
- **Values** are `int` with `-1000 <= value <= 1000`.
- **Indices** are in range, with `row1 <= row2` and `col1 <= col2`.
- **Calls** number at most `5000` in total.
- **Return value** of `sumRegion` is a `long`.

**Example 1.** Input `[[1,2,3],[4,5,6],[7,8,9]]` with `sumRegion(0,0,1,1)`, `update(1,1,0)`, `sumRegion(0,0,1,1)`, `sumRegion(1,1,2,2)`, output 12, 7 and 23.

**Example 2.** Input `[[5]]` with `update(0,0,-5)`, `sumRegion(0,0,0,0)`, output -5.

**Hint.** Nest the one-dimensional walk. How many prefix rectangles combine into one region, and which signs do they carry?

**Changed decision.** Ownership extends from intervals to rectangles, so each call costs O(log m * log n).

#### [Boundary] Repeated Assignment (Author exercise)
<!-- id: dq39-repeated-assignment -->

**Prerequisites.** The two exercises above.

**Problem.** Design a ledger of `n` slots that all start at 0. `set(slot, value)` assigns `value` to a slot, and a slot may be assigned many times, including with the value it already holds. `total(from, to)` returns the sum of the slots in the half-open range `[from, to)`. The structure must apply the difference from the previous value on each assignment. Calls arrive online, with about three updates per query.

**Constraints.** The limits are:
- **`n`** satisfies `1 <= n <= 10^5`.
- **Values** are `int` over the full range, so sums need `long`.
- **Range** satisfies `0 <= from <= to <= n`, and `from == to` returns 0.
- **Calls** number at most `2 * 10^5` in total.

**Example 1.** Input `n = 4` with `set(1,5)`, `set(1,5)`, `set(1,2)`, `total(0,4)`, output 2, because each assignment replaces the old value.

**Example 2.** Input `n = 2` with `set(0, 2000000000)`, `set(1, 2000000000)`, `total(0,2)`, output 4000000000, which exceeds the `int` range.

**Hint.** What does the second `set(1,5)` add to the tree? What happens if the code adds `value` directly instead of the difference?

**Changed decision.** The same slot changes many times, so each update must be a difference from the stored value and not a fresh addition.

#### [Recognize] Mutable Range Minimum (Author exercise)
<!-- id: dq39-mutable-range-minimum -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class over an integer array with `set(index, value)` and `min(from, to)`, which returns the smallest value in the half-open range `[from, to)`. Calls arrive online, with updates and queries about equal. Choose between a Fenwick tree and a segment tree, implement the choice, and show on a concrete input why the other choice returns a wrong answer after a value increases.

**Constraints.** The limits are:
- **`n`** satisfies `1 <= n <= 10^5`.
- **Values** are `int` over the full range, and comparisons never subtract.
- **Range** satisfies `0 <= from < to <= n`, so a range is never empty.
- **Calls** number at most `2 * 10^5` in total.

**Example 1.** Input `[5, 2, 8, 6]` with `min(0,4)`, `set(1, 9)`, `min(0,4)`, output 2 and then 5.

**Example 2.** Input `[4]` with `set(0, -3)`, `min(0,1)`, output -3.

**Hint.** Can a stored minimum be corrected by subtracting the old value? Which node must change when a leaf rises?

**Changed decision.** The operation has no inverse, so ownership stays but each node is recomputed from its children and not patched by a delta.
