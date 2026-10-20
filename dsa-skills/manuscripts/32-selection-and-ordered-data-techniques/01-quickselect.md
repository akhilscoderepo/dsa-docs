<!-- lesson-kind: standard -->
<!-- lesson-id: quickselect -->
## Quickselect

<!-- stage: context -->
### Why Sorting Everything Wastes Time

A monitoring service collects ten million request latencies each hour. The on-call engineer wants the median latency, which is the value that would sit in the middle if the list were in order. The service needs only that one value. It does not need the other nine million nine hundred ninety-nine thousand nine hundred ninety-nine in any order.

The obvious route sorts the whole list and reads the middle slot. That works, but it orders every value when the answer depends on a single position. The same waste appears when a program needs the 90th percentile, the third highest score, or the ten nearest stores. Can a program find the value at one chosen position without ordering the rest? The answer follows below.

<!-- stage: naive -->
### Sort The Array And Read One Slot

The direct approach sorts a copy of the array and returns the element at the wanted position. The method below takes a zero-based position `k`, where `k = 0` asks for the smallest value.

```java
static int selectBySorting(int[] a, int k) {
    int[] copy = a.clone();       // keep the caller's array unchanged
    java.util.Arrays.sort(copy);  // orders every element, even those far from position k
    return copy[k];               // the wanted value now sits at index k
}
```

The code is short and correct for every input. It also does far more ordering than the question needs, because the order among the values that lie far from position `k` never affects the answer.

<!-- stage: bottleneck -->
### Sorting Costs More Than One Answer Needs

```predict
A program needs the median of 10,000,000 values. A comparison sort does about n times log2(n) comparisons. About how many comparisons per value does the sort spend, and what is the least a correct method could spend per value?

About 23 comparisons per value, because log2 of ten million is about 23. A correct method must look at every value at least once, so the least it can spend is about one comparison per value. Sorting spends over twenty times that minimum.
```

#### Count The Comparisons

A comparison sort on `n` values costs O(n log n). For `n = 10^7` that is about 2.3 * 10^8 comparisons. Any method that answers correctly must read every value at least once, because one unread value could be the answer. Selection therefore cannot beat linear time, and the sort exceeds that by a factor of log n.

#### Name The Missing Idea

The extra factor comes from ordering values that cannot affect the answer. A faster method must split the values so that one whole group can be ignored. It must also prove that the ignored group does not hold position `k`.

<!-- stage: insight -->
### Split Around One Value

#### Place A Pivot At Its Final Rank

Choose one element of the array and call it the **pivot**. A **partition** step rearranges the array so that every element smaller than the pivot comes before it and every element not smaller comes after it. After the step, the pivot sits at index `p`. That index is the **final rank** of the pivot, which means the index it would have in the sorted array. The pivot is already in its sorted place, and nothing needs to move it again.

The final rank follows from counting. Within a range that starts at index `lo`, exactly `p - lo` elements are smaller than the pivot, so the pivot has rank `p` in the whole array when `lo` is 0 and all values differ. The order inside the left group and inside the right group is still unknown, and that is fine.

<!-- names: quickselect, partition, pivot -->

#### Keep Only The Side That Holds The Target

**Quickselect** uses the final rank to discard work. Suppose the target index is `k`. If `p` equals `k`, the pivot is the answer. If `k` is less than `p`, the values that belong at index `k` are all in the left group, so the right group can never matter. If `k` is greater than `p`, the values that belong at index `k` are all in the right group, so the left group can never matter.

The method keeps two bounds, `lo` and `hi`, and repeats the partition on `a[lo..hi]` only. It passes the bounds and never copies a subarray. Each round shrinks the range to one side of the pivot.

#### State The Invariant And The Cost

The invariant is that `a[lo..hi]` always holds exactly the values whose sorted positions are `lo` to `hi`, and the target index `k` lies inside `lo..hi`. A partition keeps it true, because the pivot's final rank splits the range at a proven boundary. A partition of a range of length `m` costs O(m). If each round removes about half of the range, the work is `n + n/2 + n/4 + ...`, which sums to O(n) on average. A bad pivot that removes one element per round costs O(n^2) in the worst case.

<!-- stage: variables -->
### Quantities To Track In The Loop

Track these items during one run.

- **a** is the `int[]` that the method rearranges in place.
- **k** is the zero-based target index, where `k = 0` is the smallest value.
- **lo** and **hi** are the inclusive bounds of the range that still holds index `k`.
- **pivot** is the value that the current partition places at its final rank.
- **p** is the index where the partition leaves the pivot.
- **store** is the index of the first element that is not smaller than the pivot, found while scanning.

The method partitions in place, so it reorders the caller's array. A caller who needs the original order passes a clone. The scan inside a partition uses `store` to mark the boundary between the smaller group and the rest. The boundary is defined before any swap happens, so every swap moves one smaller element across it.

<!-- stage: trace -->
### Follow Two Searches Round By Round

Each step below shows the bounds `lo` and `hi` and the index `p` where the pivot lands after that round. The cells show the starting array, and each note spells out the array after the round. The pointer `p` rests at -1 before the first partition.

#### Find The Third Smallest Value

Take the array `7, 2, 9, 4, 1, 8, 3` and the target index `k = 2`. The range is the whole array, so `lo = 0` and `hi = 6`. The pivot is the middle element 4. The partition moves 2, 1 and 3 in front of it, and 4 lands at index 3. Index 2 is less than 3, so the method keeps the left side and sets `hi = 2`. The next partition works on `2, 3, 1` with the middle element 3 as the pivot. The value 3 lands at index 2, which equals `k`, so the answer is 3.

```trace
{"cells":[7,2,9,4,1,8,3],"pointers":["lo","hi","p"],"steps":[{"at":{"lo":0,"hi":6,"p":-1},"vars":{"k":2},"note":"The range is the whole array, lo 0 to hi 6. No partition has run yet."},{"at":{"lo":0,"hi":6,"p":3},"vars":{"pivot":4,"k":2},"note":"The pivot 4 lands at index 3. The array is now [2, 3, 1, 4, 9, 8, 7]. Index 2 is less than 3, so the left side stays and hi becomes 2."},{"at":{"lo":0,"hi":2,"p":2},"vars":{"pivot":3,"k":2},"note":"The pivot 3 lands at index 2. The array is now [2, 1, 3, 4, 9, 8, 7]. The pivot sits at index k, so it is the answer."}]}
```

#### Find The Sixth Smallest Value

The array `3, 2, 3, 1, 2, 4, 5, 5, 6` has nine elements, and the target index is `k = 5`. The first pivot is the middle element 2, and it lands at index 1. Index 5 is greater than 1, so the method keeps the right side and sets `lo = 2`. The second pivot is the middle element 4 of the range `lo..hi`, and it lands exactly at index 5, so the search ends. This is also the fourth largest value, because `9 - 5 = 4`.

```trace
{"cells":[3,2,3,1,2,4,5,5,6],"pointers":["lo","hi","p"],"steps":[{"at":{"lo":0,"hi":8,"p":-1},"vars":{"k":5},"note":"The range is the whole array, lo 0 to hi 8. No partition has run yet."},{"at":{"lo":0,"hi":8,"p":1},"vars":{"pivot":2,"k":5},"note":"The pivot 2 lands at index 1. The array is now [1, 2, 3, 3, 6, 4, 5, 5, 2]. Index 5 is greater than 1, so the right side stays and lo becomes 2."},{"at":{"lo":2,"hi":8,"p":5},"vars":{"pivot":4,"k":5},"note":"The pivot 4 lands at index 5. The array is now [1, 2, 3, 3, 2, 4, 5, 5, 6]. The pivot sits at index k, so it is the answer."}]}
```

The hardest step is the choice of side. The method compares `k` with `p` only, and it never compares values from the discarded side. The first trace discards the right side, and the second trace discards the left side.

<!-- stage: code -->
### Implement Partition And Select

```java
final class Quick {
    static int select(int[] a, int k) {
        int lo = 0, hi = a.length - 1;           // the range that still holds index k
        while (lo < hi) {
            int p = partition(a, lo, hi);        // pivot reaches its final rank p
            if (p == k) return a[p];             // the pivot is the answer
            if (k < p) hi = p - 1;               // the target is in the left group
            else lo = p + 1;                     // the target is in the right group
        }
        return a[lo];                            // one element is left, and it holds index k
    }

    static int partition(int[] a, int lo, int hi) {
        int mid = lo + (hi - lo) / 2;            // the form lo + (hi - lo) / 2 cannot overflow
        swap(a, mid, hi);                        // park the pivot at hi so the scan can skip it
        int pivot = a[hi];
        int store = lo;                          // a[lo..store-1] holds the smaller values
        for (int i = lo; i < hi; i++) {
            if (a[i] < pivot) {
                swap(a, i, store);               // move the smaller value across the boundary
                store++;
            }
        }
        swap(a, store, hi);                      // the pivot lands at its final rank
        return store;
    }

    static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
}
```

The loop ends because every round either returns or shrinks `hi - lo` by at least one. The method reads and writes only inside `lo..hi`, so no subarray is copied and the extra memory is O(1). The middle element serves as the pivot in this lesson so that the traces repeat exactly. A program that must resist crafted input picks a random index between `lo` and `hi` instead.

<!-- stage: applicability -->
### When One Rank Is Enough

#### Recognize The Pattern

Use this method when the question asks for a single rank, or for the `k` smallest values in any order. Median, percentile, kth largest and the `k` nearest items all fit. Before coding, check the invariant that `a[lo..hi]` contains exactly the values that belong at sorted positions `lo` to `hi`. Every partition must keep that statement true, and the loop must rely on nothing else.

The method also changes the array. If the caller needs the original order, copy once before the loop. That single copy costs O(n) and is not a copy per round.

#### Watch For The Nearest False Friend

A full sort is the false friend, and so is a heap of size `k`. Sorting gives the answer, but it pays the extra log n factor. A heap of size `k` costs O(n log k) and never changes the input, which makes it the better fit when values arrive one at a time or when the input must stay intact. Quickselect fits when the whole array sits in memory and in-place changes are allowed.

#### Avoid The Java Hazards

Write `lo + (hi - lo) / 2` and never `(lo + hi) / 2`, because the sum of two large `int` values overflows to a negative number. Pass `lo` and `hi` to the recursive or looping step, because `Arrays.copyOfRange` allocates a new array each round and the copies cost O(n) every time. When the key is computed, as in a squared distance, use `long` for the key, since the product of two `int` values can overflow. Finally, do not compare values with `a - b`, because the difference overflows for values of opposite signs.

<!-- stage: exercises -->
### Exercises

#### [Build] Select Kth Smallest (Author exercise)
<!-- id: sel-select-kth-smallest -->

**Prerequisites.** The partition step and the loop from this lesson.

**Problem.** Given an integer array `a` and a zero-based rank `r`, return the value that would sit at index `r` if `a` were sorted in non-decreasing order. The method may reorder `a`.

**Constraints.** The limits are:
- **`n`** is the length of `a`, an `int` with `1 <= n <= 10^5`.
- **Values** are `int` values with absolute value at most `10^9`.
- **`r`** is an `int` with `0 <= r < n`.
- **Ties** may repeat, and equal values count separately.
- **Return** is an `int`.

**Example 1.** Input `a = [9, 4, 7, 1, 8, 2]` and `r = 2`, output 4, since the sorted array is `[1, 2, 4, 7, 8, 9]`.

**Example 2.** Input `a = [5]` and `r = 0`, output 5, since one element is its own rank.

**Hint.** After a partition places the pivot at index `p`, which side contains index `r`?

**Changed decision.** Baseline case: partition and continue into the one side that holds the target index.

#### [Vary] Kth Largest Element (LeetCode 215)
<!-- id: sel-kth-largest -->

**Prerequisites.** The exercise above.

**Problem.** For an integer `k` and an integer array `nums`, return the element that would sit at the `k`-th place from the top of the sorted order, where `k = 1` asks for the maximum. Equal values count separately.

**Constraints.** The limits are:
- **`n`** is the length of `nums`, an `int` with `1 <= n <= 10^5`.
- **Values** are `int` values with absolute value at most `10^9`.
- **`k`** is an `int` with `1 <= k <= n`.
- **Return** is an `int`.

**Example 1.** Input `nums = [3, 2, 1, 5, 6, 4]` and `k = 2`, output 5, since the sorted array is `[1, 2, 3, 4, 5, 6]`.

**Example 2.** Input `nums = [4, 4, 1, 9, 9, 2, 7]` and `k = 3`, output 7, since the sorted array is `[1, 2, 4, 4, 7, 9, 9]`.

**Hint.** Which zero-based index in ascending order holds the `k`-th largest value?

**Changed decision.** The question counts from the large end, so the target index becomes `n - k`.

#### [Boundary] Duplicates And Extreme K (Author exercise)
<!-- id: sel-duplicates-extreme -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `a` and a zero-based rank `r`, return the value at index `r` of the sorted array. The array can hold long runs of one value, and `r` can be 0 or `n - 1`. The method must run in expected O(n) time even when all values are equal.

**Constraints.** The limits are:
- **`n`** is an `int` with `1 <= n <= 10^5`.
- **Values** are `int` values, and all of them may be equal.
- **`r`** is an `int` with `0 <= r < n`.
- **Mutation** of `a` is allowed.
- **Return** is an `int`.

**Example 1.** Input `a = [6, 6, 6, 6, 6]` and `r = 3`, output 6, since every rank holds 6.

**Example 2.** Input `a = [2, 9, 2, 2, 5, 2, 9]` and `r = 4`, output 5, since the sorted array is `[2, 2, 2, 2, 5, 9, 9]`.

**Hint.** If a partition keeps only strictly smaller values on the left, how many elements does it remove when all values are equal?

**Changed decision.** The partition now splits three ways, so a whole run of values equal to the pivot is settled in one round.

#### [Recognize] K Closest Points To Origin (LeetCode 973)
<!-- id: sel-k-closest-points -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `points` where each entry is `[x, y]`, and an integer `k`, return the `k` points with the smallest Euclidean distance from the origin. The answer may be in any order.

**Constraints.** The limits are:
- **`n`** is the number of points, an `int` with `1 <= k <= n <= 10^5`.
- **Coordinates** are `int` values with absolute value at most `10^9`.
- **Ties** at the cutoff do not occur, so the set of `k` points is unique.
- **Return** is a list of `k` points in any order.

**Example 1.** Input `points = [[3, 3], [5, -1], [-2, 4]]` and `k = 2`, output `[[3, 3], [-2, 4]]` in any order, since the squared distances are 18, 26 and 20.

**Example 2.** Input `points = [[1000000000, 1000000000], [1, 1], [-1, 2]]` and `k = 2`, output `[[1, 1], [-1, 2]]` in any order, since the first squared distance is 2 * 10^18.

**Hint.** Which key replaces the value in the comparison, and which type holds that key without overflow?

**Changed decision.** The partition compares a derived key, the squared distance, and the key needs `long`.
