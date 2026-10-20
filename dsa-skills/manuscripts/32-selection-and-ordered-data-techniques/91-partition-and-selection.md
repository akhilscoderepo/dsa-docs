<!-- lesson-kind: combination -->
<!-- lesson-id: partition-and-selection -->
## Partition And Selection

<!-- stage: context -->
### A Percentile Report On A Million Samples

A web service records the response time of every request in an `int[]` of 1,000,000 entries, measured in milliseconds. The on-call engineer wants the 95th-percentile time, and the alert must also name how many requests were strictly slower than that time. Many requests share the same time, so the count of ties matters as much as the value.

Sorting the whole array answers the question, but it also orders 999,999 entries that the answer never reads. The report needs one value at one rank plus two counts, and the full order is wasted work.

Formally, the input is an `int[] a` and a zero-based rank `r` with `0 <= r < n`. The output is the value `v` that sits at index `r` when `a` is sorted in increasing order, the number `below` of entries strictly smaller than `v`, and the number `equal` of entries equal to `v`.

This lesson asks how to find `v`, `below` and `equal` in expected O(n) time, and how to tell this problem apart from questions that look similar but need the order between pairs of entries.

<!-- stage: contributions -->
### What Three Earlier Lessons Add

#### Quickselect Adds Discarding One Side

Quickselect partitions the array around a pivot. The pivot lands at its final sorted index, so a target rank on one side lets the search drop the other side completely. Only the side that holds the target is searched again.

#### Partition Invariants Add An Equal Region

The three-way partition from the Partition Invariants lesson splits a range into entries smaller than the pivot, entries equal to the pivot and entries larger than the pivot. Duplicates stay together in the middle region, so one pass reports how many entries tie with the pivot. That count is the extra output this lesson needs.

#### Merge Counting Adds A Contrast

Merge counting counts, during a merge sort, the pairs that take one entry from each half. It answers questions about two entries at once. This lesson uses it only at the end, to show which questions selection cannot answer.

<!-- stage: naive -->
### Sort Everything And Read One Index

The direct method sorts a copy of the array, reads index `r`, and then scans once to count the smaller and equal entries. It is correct for every input and works as a reference answer to test faster code against.

```java
static int[] selectBySorting(int[] a, int r) {
    int[] sorted = a.clone();
    java.util.Arrays.sort(sorted);
    int v = sorted[r];
    int below = 0, equal = 0;
    for (int x : sorted) {
        if (x < v) below++;
        else if (x == v) equal++;
    }
    return new int[]{v, below, equal};
}
```

The sort dominates the work. For 1,000,000 entries it performs about 20 million comparisons, and the counting scan adds one more pass.

<!-- stage: bottleneck -->
### The Sort Orders Entries Nobody Needs

```predict
After the sort, the code reads only sorted[r] and then counts entries. Which part of the sorted order did the answer actually use, and is there a cheaper way to learn it?

The answer used only one position and the knowledge of which entries lie before and after it. The order inside the smaller entries and inside the larger entries was never read. A single partition around any value already tells how many entries are smaller, equal and larger, so a rank inside the middle region is answered without sorting the sides.
```

#### Count The Wasted Work

Sorting costs O(n log n) time. For n = 1,000,000 that is about 20 comparisons per entry. The answer uses one position, so the log n factor pays for order that the output never shows. A single pass over the array costs O(n), and the goal is to reach the answer with a few such passes.

#### Find What One Pass Can Decide

One pass can compare every entry with a chosen pivot and count three groups. If `r` falls inside the group of smaller entries, the answer lies in that group. If `r` falls in the group of larger entries, the answer lies there. In both cases the other two groups are never examined again. The open question is how to move entries so the next pass sees only the group that holds `r`.

<!-- stage: insight -->
### Partition Then Keep One Side

A three-way partition solves both parts. It rearranges the current range in place and gives exact counts.

<!-- names: pivot rank, equal block, cross pair -->

#### Use The Pivot Rank To Discard

Pick a pivot value `p` and partition the range `lo..hi` into three blocks, in this order: entries smaller than `p`, the **equal block** of entries equal to `p`, and entries larger than `p`. Let `lt` be the first index of the equal block and `gt` its last index. Every entry left of `lt` is smaller than `p`, so the **pivot rank** of the block is the index range `lt..gt`, and those indices hold `p` in the final sorted order.

Compare `r` with that range. If `r < lt`, the answer is in the smaller block, so the search continues on `lo..lt - 1`. If `r > gt`, the answer is in the larger block, so it continues on `gt + 1..hi`. If `lt <= r <= gt`, the answer is `p`, and the search stops.

#### Read The Counts From The Last Partition

The two counts need no extra scan. Every entry discarded on the left is strictly smaller than every entry in the current range, and every entry discarded on the right is strictly larger. All entries equal to the answer therefore lie inside the last equal block. The last values of `lt` and `gt` give `below = lt` and `equal = gt - lt + 1`.

The invariant is that the answer index `r` always lies inside the current range, and everything outside the range keeps its position relative to the answer. Each round removes at least the equal block, so the loop ends.

#### Separate Selection From Pair Questions

Selection knows how each entry compares with one pivot. It does not know how two entries compare with each other. A question such as "for every index, how many later entries are smaller" needs the relation of each pair. Counting a **cross pair**, a pair with one entry in each half of a split array, is the job of merge counting. The applicability stage returns to this difference.

<!-- stage: variables -->
### Quantities For The Selection Loop

The code and the traces use the following quantities.

- **a** is the working copy of the input, rearranged by every round.
- **r** is the zero-based target rank in the sorted order.
- **lo** and **hi** mark the first and last index of the current range.
- **pivot** is the value at the middle index of the range, `a[lo + (hi - lo) / 2]`.
- **lt** and **gt** mark the first and last index of the equal block after a round.
- **below** and **equal** are the final outputs and equal `lt` and `gt - lt + 1` after the last round.

In the traces, the variable `array` shows the contents of `a` after each round, and `move` states which side the search keeps.

<!-- stage: trace -->
### Select A Rank From Two Arrays

#### An Array With Many Ties

The first array is `[7, 2, 9, 2, 5, 7, 7, 1, 8]` with `r = 6`. The sorted order is `[1, 2, 2, 5, 7, 7, 7, 8, 9]`, so the answer is 7 with 4 smaller entries and 3 equal entries.

Round 1 uses the middle entry 5 as pivot and moves the three smaller entries to the front. The equal block holds the single 5 at index 3, and `r = 6` lies to its right, so the search keeps the larger side, indices 4 to 8. Round 2 uses pivot 9, which ends alone at index 8. Now `r` lies to its left, so the search keeps indices 4 to 7. Round 3 uses pivot 7, and the equal block holds all three 7s at indices 4 to 6. Rank 6 falls inside it, so the loop stops. The counts come from `lt` and `gt`: `below = 4` and `equal = 3`.

```trace
{"cells":[7,2,9,2,5,7,7,1,8],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":8},"vars":{"r":6,"array":"[7, 2, 9, 2, 5, 7, 7, 1, 8]"},"note":"The range is the whole array and the target rank is r = 6."},{"at":{"lo":0,"hi":8},"vars":{"pivot":5,"lt":3,"gt":3,"array":"[1, 2, 2, 5, 7, 7, 9, 8, 7]","move":"keep the larger side"},"note":"Round 1 on indices 0 to 8 uses pivot 5. The equal block covers indices 3 to 3, and r = 6, so the search keeps the larger side."},{"at":{"lo":4,"hi":8},"vars":{"pivot":9,"lt":8,"gt":8,"array":"[1, 2, 2, 5, 7, 7, 8, 7, 9]","move":"keep the smaller side"},"note":"Round 2 on indices 4 to 8 uses pivot 9. The equal block covers indices 8 to 8, and r = 6, so the search keeps the smaller side."},{"at":{"lo":4,"hi":7},"vars":{"pivot":7,"lt":4,"gt":6,"array":"[1, 2, 2, 5, 7, 7, 7, 8, 9]","move":"stop"},"note":"Round 3 on indices 4 to 7 uses pivot 7. The equal block covers indices 4 to 6, and r = 6, so the search stops because the pivot is the answer."},{"at":{"lo":4,"hi":7},"vars":{"value":7,"below":4,"equal":3},"note":"The loop stops. The answer is 7, with 4 smaller entries and 3 equal entries."}]}
```

#### An Array With A Target Near The Front

The second array is `[4, 4, 4, 3, 10, -6, 4, 8]` with `r = 1`. The sorted order is `[-6, 3, 4, 4, 4, 4, 8, 10]`, so the answer is 3 with one smaller entry and one equal entry.

The middle entry of the whole array is 3, so the first round uses pivot 3. One entry, -6, is smaller, and the equal block holds only the 3 at index 1. Rank 1 falls inside that block, so the loop stops after one round. The four 4s and the other larger entries are never examined again. This array shows that a pivot equal to the answer ends the search at once.

```trace
{"cells":[4,4,4,3,10,-6,4,8],"pointers":["lo","hi"],"steps":[{"at":{"lo":0,"hi":7},"vars":{"r":1,"array":"[4, 4, 4, 3, 10, -6, 4, 8]"},"note":"The range is the whole array and the target rank is r = 1."},{"at":{"lo":0,"hi":7},"vars":{"pivot":3,"lt":1,"gt":1,"array":"[-6, 3, 4, 10, 4, 4, 8, 4]","move":"stop"},"note":"Round 1 on indices 0 to 7 uses pivot 3. The equal block covers indices 1 to 1, and r = 1, so the search stops because the pivot is the answer."},{"at":{"lo":0,"hi":7},"vars":{"value":3,"below":1,"equal":1},"note":"The loop stops. The answer is 3, with 1 smaller entry and 1 equal entry."}]}
```

<!-- stage: code -->
### Select With A Three-Way Partition

The method below returns `{value, below, equal}` and leaves the input array unchanged.

```java
final class Selector {
    static int[] select(int[] input, int r) {
        int[] a = input.clone();
        int lo = 0, hi = a.length - 1;
        while (true) {
            int pivot = a[lo + (hi - lo) / 2];
            int lt = lo, i = lo, gt = hi;
            while (i <= gt) {
                if (a[i] < pivot) swap(a, lt++, i++);
                else if (a[i] > pivot) swap(a, i, gt--);
                else i++;
            }
            if (r < lt) hi = lt - 1;
            else if (r > gt) lo = gt + 1;
            else return new int[]{pivot, lt, gt - lt + 1};
        }
    }

    static void swap(int[] a, int x, int y) {
        int t = a[x]; a[x] = a[y]; a[y] = t;
    }
}
```

Each round costs O(hi - lo + 1), and the range shrinks by at least one entry. A pivot near the middle value halves the range, so the expected total is O(n). A fixed middle-index pivot has an input that shrinks the range by one entry per round and costs O(n^2) time, so production code picks the pivot index at random. The method uses O(n) memory for the copy. When every entry is equal, the first round ends the loop, because the equal block covers the whole range.

<!-- stage: applicability -->
### When Selection Fits And When It Fails

#### Recognize The Cue

Use selection when the output depends on one rank, or on a group at a rank, and not on the full order. Typical signals are a median, a percentile, the k-th largest value, and the k closest items with a tie rule. The equal block also supports a tie rule, because it states how many entries tie at the boundary.

#### Check The Invariant

The invariant is that the target rank stays inside the current range and the discarded entries sit on the correct side of every later value. Test an array of one entry, all-equal entries, ascending and descending input, `r = 0`, `r = n - 1`, and `Integer.MIN_VALUE` with `Integer.MAX_VALUE`. Compare the output with sorting on random small arrays.

#### Watch For The False Friend

The false friend is a per-index question that looks like a rank question. "How many later entries are smaller than this one" mentions order and smaller entries, but the answer differs for every index and depends on positions. A pivot partition destroys the original positions of the entries. Partition cannot answer it. Merge counting keeps the position information while it sorts. A second false friend is the pair condition `nums[i] > 2 * nums[j]`, which compares two entries with each other. No single pivot decides it, so selection does not apply. A related slip is the product `2 * nums[j]` in `int`, which overflows near the type limits and needs `long`.

#### Know When Not To Use It

Skip selection when the full sorted order is needed, when many different ranks of the same array are queried, or when the array changes between queries. In those cases sort once, or use an ordered structure. For a small fixed k on a stream, a heap is simpler.

<!-- stage: exercises -->
### Exercises

#### [Build] Kth Largest Element In An Array With Position Range (LeetCode 215)
<!-- id: ps-kth-range -->

**Prerequisites.** The three-way partition and the loop that keeps one side, from this lesson.

**Problem.** This is a variant of LeetCode 215 that also reports positions. An `int[] nums` and an integer `k` are given. Let `s` be `nums` sorted in non-increasing order. Return an `int[]` of three entries. The first entry is `s[k - 1]`. The second and third entries are the smallest and the largest zero-based index `t` with `s[t] == s[k - 1]`.

**Constraints.** The limits are:
- **Length** `n` is from 1 to 100,000.
- **k** satisfies 1 <= k <= n.
- **Entries** are any `int` values, including the extreme values, and may repeat.
- **Mutation** of the input array is not allowed.

**Example 1.** Input `nums = [4, 9, 4, 1, 4, 9, 6]`, `k = 5`, output `[4, 3, 5]`.

**Example 2.** Input `nums = [5, 5, 5, 5]`, `k = 3`, output `[5, 0, 3]`, since all entries tie.

**Hint.** How many entries are larger than the answer? How many tie with it? Which of the two numbers gives the first index of the range?

**Changed decision.** The partition puts larger entries first, and the output is a position range and not a single value. The counts of larger and equal entries replace the index of the last pivot.

#### [Vary] K Closest Points To Origin With Tie Counts (LeetCode 973)
<!-- id: ps-closest-ties -->

**Prerequisites.** The exercise above and the equal block from this lesson.

**Problem.** This is a variant of LeetCode 973 that reports a tie boundary. An array `points` of pairs `{x, y}` and an integer `k` are given. The squared distance of a point to the origin is `x * x + y * y`. Let `d` be the k-th smallest squared distance, counting repeated distances. Return a `long[]` of three entries: `d`, the number of points with squared distance below `d`, and the number of points with squared distance equal to `d`.

**Constraints.** The limits are:
- **Count** of points is from 1 to 100,000.
- **k** satisfies 1 <= k <= the count of points.
- **Coordinates** are `int` values between -10^9 and 10^9.
- **Distances** need `long` arithmetic, and the points may repeat.
- **Mutation** of the input is not allowed.

**Example 1.** Input `points = [[3, 4], [-3, -4], [0, 5], [1, 1], [5, 0]]`, `k = 3`, output `[25, 1, 4]`.

**Example 2.** Input `points = [[1000000000, 1000000000], [0, 0]]`, `k = 2`, output `[2000000000000000000, 1, 1]`.

**Hint.** Which array do you partition, the points or a derived array? What happens to `x * x` when `x` is an `int`?

**Changed decision.** The selection key is derived from each point and is a `long`. The output reports the boundary of a tie group, so the points themselves are never returned.

#### [Boundary] Count Of Smaller Numbers After Self Within A Distance (LeetCode 315)
<!-- id: ps-window-smaller-right -->

**Prerequisites.** The false friend in the applicability stage and merge counting from the earlier lesson.

**Problem.** This is a variant of LeetCode 315 with a value window. An `int[] nums` and a `long d` are given. For every index `i`, count the indices `j > i` with `0 < nums[i] - nums[j] <= d`. Return an `int[]` with one count per index.

**Constraints.** The limits are:
- **Length** is from 1 to 100,000.
- **Entries** are any `int` values, including the extreme values.
- **d** is a `long` between 0 and 4,294,967,295.
- **Differences** are computed in `long`, and `d = 0` gives all zeros.
- **Mutation** of the input array is not allowed.

**Example 1.** Input `nums = [8, 5, 7, 3, 5, 2]`, `d = 3`, output `[3, 2, 1, 1, 1, 0]`.

**Example 2.** Input `nums = [2147483647, -2147483648]`, `d = 4294967295`, output `[1, 0]`.

**Hint.** Why does selection fail here? When both halves are sorted by value, how do the two window ends move as the left entry grows?

**Changed decision.** The count is restricted to a window of values below each entry, so the merge needs two moving positions in the sorted right half instead of one. The result is stored per original index.

#### [Recognize] Reverse Pairs With A Triple Threshold (LeetCode 493)
<!-- id: ps-triple-pairs -->

**Prerequisites.** All three exercises above.

**Problem.** This is a variant of LeetCode 493 with factor 3. An `int[] nums` is given. Return the number of index pairs `(i, j)` with `i < j` and `nums[i] >= 3 * nums[j]`, where the product is computed without overflow.

**Constraints.** The limits are:
- **Length** is from 1 to 100,000.
- **Entries** are any `int` values, including the extreme values.
- **Result** is a `long`, since it can exceed the `int` range.
- **Products** are computed in `long`.
- **Mutation** of the input array is not allowed.

**Example 1.** Input `nums = [9, 2, 6, -1, 3, -4]`, output `10`.

**Example 2.** Input `nums = [0, 0, 0]`, output `3`, since `0 >= 0` holds for each of the three pairs.

**Hint.** Does any single pivot decide a pair? Which counting method keeps the order of the positions while it sorts?

**Changed decision.** The factor is 3 and the comparison is non-strict, so the pointer in the sorted left half stops at the first entry that reaches the threshold. Equal values now count.
