<!-- lesson-kind: standard -->
<!-- lesson-id: partition-invariants -->
## Partition Invariants

<!-- stage: context -->
### Why Splitting Values In Place Is Hard

A billing service holds one million order amounts in an array. A report needs the orders below a price limit first, then the orders exactly at the limit, then the orders above it. The amounts inside each group may stay in any order. The service has little spare memory, so it must rearrange the array it already has.

Sorting would produce this layout, but sorting does far more work than the report needs. A hand-written loop is faster, and it is also easy to get wrong. A swap in the wrong place loses an order, a pointer that never moves hangs the program, and a pointer that moves too far skips a value. This lesson asks how a program can split an array into three groups in place while it knows at every moment which part is already correct.

<!-- stage: naive -->
### Copying Values Into Three Lists

The direct approach reads the array once and appends each value to one of three new lists. It then writes the lists back into the array one after another.

```java
static void splitByCopy(int[] a, int limit) {
    java.util.List<Integer> below = new java.util.ArrayList<>();
    java.util.List<Integer> equal = new java.util.ArrayList<>();
    java.util.List<Integer> above = new java.util.ArrayList<>();
    for (int v : a) {
        if (v < limit) below.add(v);          // goes to the first group
        else if (v == limit) equal.add(v);    // goes to the middle group
        else above.add(v);                    // goes to the last group
    }
    int k = 0;
    for (int v : below) a[k++] = v;           // write the groups back in order
    for (int v : equal) a[k++] = v;
    for (int v : above) a[k++] = v;
}
```

The method is correct and easy to read. It reads the array twice and holds a second copy of every value in the three lists.

<!-- stage: bottleneck -->
### Extra Memory And Repeated Copies

```predict
A recursive routine splits an array of n values, then splits each part again, and copies the parts into new arrays at every level. If each level copies all n values, about how many values does it copy over 20 levels?

About 20 times n. Every level copies every value once, so the copy cost grows with the number of levels times n, and it adds nothing to the answer.
```

#### Count The Extra Work

The copy method needs O(n) extra memory, because the three lists together hold n values plus the list overhead. Boxing each `int` into an `Integer` adds an object per value. A routine that splits and then splits again copies O(n) values at each level, so a recursion with `L` levels spends O(n * L) on copies alone. Sorting instead costs O(n log n) comparisons, and it also orders values inside each group, which the report never asked for.

#### Name What Is Missing

The copying method knows which group each value belongs to only after it has moved the value to a new place. An in-place method must do the opposite. It must keep one array and promise, at every step, which index ranges hold finished groups and which range has not been looked at. That promise is called a loop invariant, and the rest of this lesson builds it.

<!-- stage: insight -->
### Keep Finished Groups As Index Ranges

#### Split The Array Into Regions

A **partition** rearranges the values of `a[lo..hi]` around a pivot value, so that smaller values come first and larger values come last. The array stays in one piece. Each index range of the array has a fixed meaning, and a pointer marks where one range ends and the next begins. The values inside a finished range may still be in any order.

<!-- names: Lomuto partition, three-way partition, unresolved region -->

#### Build The Lomuto Partition

The **Lomuto partition** uses the last element as the pivot and two pointers. The pointer `j` scans from `lo` to `hi - 1`. The pointer `i` marks the first slot after the values that are strictly below the pivot. The invariant has four regions. The range `a[lo..i-1]` holds values below the pivot. The range `a[i..j-1]` holds values at least as large as the pivot. The range `a[j..hi-1]` is the **unresolved region**, which means values the scan has not examined yet. The slot `a[hi]` holds the pivot.

When `a[j]` is below the pivot, the loop swaps `a[i]` and `a[j]` and then increases `i`. The swap moves the small value into the first slot of the large range, and it moves the large value that was there to position `j`. When `a[j]` is not below the pivot, the loop does nothing, because the value already sits in the large range. In both cases `j` advances, so the unresolved region shrinks by one slot. After the scan the unresolved region is empty, and one final swap of `a[i]` with `a[hi]` puts the pivot between the two groups. The pivot index `i` is now its final position in sorted order.

#### Build The Three-Way Partition

The Lomuto partition lumps equal values with the large ones. A **three-way partition** keeps them in their own range. It uses three pointers `lt`, `i` and `gt`. The range `a[lo..lt-1]` holds values below the pivot value, `a[lt..i-1]` holds values equal to it, and `a[gt+1..hi]` holds values above it. The unresolved region is `a[i..gt]`.

Each step looks at `a[i]`. A smaller value swaps with `a[lt]`, and both `lt` and `i` advance, because the value that arrives at `i` came from the equal range and is already known to be equal. A larger value swaps with `a[gt]`, and only `gt` moves, because the value that arrives at `i` is new and unexamined, so `i` must stay. An equal value needs only `i` to advance. The loop ends when `i` passes `gt`, which means the unresolved region is empty.

<!-- stage: variables -->
### Pointers And Regions To Track

Track these items while the partition runs.

- **lo** and **hi** are the inclusive bounds of the part of the array being partitioned.
- **pivot** is the value that the regions compare against.
- **i** in the Lomuto partition is the first slot after the strictly smaller values.
- **j** is the scan pointer, and everything at an index below `j` is resolved.
- **lt**, **i** and **gt** in the three-way partition mark the ends of the smaller, equal and larger regions.

The bounds `lo` and `hi` are inclusive, and the caller passes them in, so a recursive call never copies a subarray. Every region is described by an index range, and a region is empty when its start is greater than its end. The pivot slot `a[hi]` in the Lomuto partition lies outside the scan range until the final swap. The count of unresolved slots is `hi - j` in the Lomuto partition and `gt - i + 1` in the three-way partition.

<!-- stage: trace -->
### Follow Two Partitions Step By Step

Each step below lists the whole array in the variable `arr`, so the reader can check every region against the pointers.

#### Lomuto On Seven Values

The array is `7, 2, 9, 4, 1, 8, 5` and the pivot is the last value, 5. The pointer `j` scans the first six slots. The values 7, 9 and 8 are not below 5, so they stay in the large range and only `j` moves. The values 2, 4 and 1 are below 5, so each swaps with the slot at `i`, and `i` moves right after each swap. After the scan, `i` is 3, and the last swap exchanges the slot 3 with the pivot slot 6.

```trace
{"cells":[7,2,9,4,1,8,5],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":0},"vars":{"pivot":5,"arr":"[7, 2, 9, 4, 1, 8, 5]"},"note":"The pivot is 5, the last value. The pointers i and j both start at slot 0."},{"at":{"i":0,"j":1},"vars":{"pivot":5,"arr":"[7, 2, 9, 4, 1, 8, 5]"},"note":"The value 7 is not below 5, so it stays in the large range."},{"at":{"i":1,"j":2},"vars":{"pivot":5,"arr":"[2, 7, 9, 4, 1, 8, 5]"},"note":"The value 2 is below 5, so it swaps with the slot at the old i and i moves to 1."},{"at":{"i":1,"j":3},"vars":{"pivot":5,"arr":"[2, 7, 9, 4, 1, 8, 5]"},"note":"The value 9 is not below 5, so it stays in the large range."},{"at":{"i":2,"j":4},"vars":{"pivot":5,"arr":"[2, 4, 9, 7, 1, 8, 5]"},"note":"The value 4 is below 5, so it swaps with the slot at the old i and i moves to 2."},{"at":{"i":3,"j":5},"vars":{"pivot":5,"arr":"[2, 4, 1, 7, 9, 8, 5]"},"note":"The value 1 is below 5, so it swaps with the slot at the old i and i moves to 3."},{"at":{"i":3,"j":6},"vars":{"pivot":5,"arr":"[2, 4, 1, 7, 9, 8, 5]"},"note":"The value 8 is not below 5, so it stays in the large range."},{"at":{"i":3,"j":7},"vars":{"pivot":5,"arr":"[2, 4, 1, 5, 9, 8, 7]"},"note":"The scan is done. The pivot swaps into slot 3, which is its final index."}]}
```

The hard step is the swap of 4 at `j = 3`. At that moment `i` is 1 and `a[1]` holds 7, a large value. The swap moves 7 to position 3, which is still inside the large range, so the invariant holds. The final array has 2, 4, 1 before the pivot and 9, 8, 7 after it, and the pivot sits at index 3.

#### Three-Way On Eight Values

The array is `4, 7, 1, 4, 9, 2, 4, 0` and the pivot value is 4. The pointer `lt` starts at 0, `i` at 0, and `gt` at 7. A value of 7 or 9 swaps with `a[gt]` and `i` stays, and a value of 1, 2 or 0 swaps with `a[lt]` and both advance. The loop ends when `i` is greater than `gt`.

```trace
{"cells":[4,7,1,4,9,2,4,0],"pointers":["lt","i","gt"],"steps":[{"at":{"lt":0,"i":0,"gt":7},"vars":{"pivot":4,"arr":"[4, 7, 1, 4, 9, 2, 4, 0]"},"note":"The pivot value is 4. The unresolved region is the whole array."},{"at":{"lt":0,"i":1,"gt":7},"vars":{"pivot":4,"arr":"[4, 7, 1, 4, 9, 2, 4, 0]"},"note":"The value 4 equals 4, so only i advances."},{"at":{"lt":0,"i":1,"gt":6},"vars":{"pivot":4,"arr":"[4, 0, 1, 4, 9, 2, 4, 7]"},"note":"The value 7 is above 4, so it swaps with slot gt. Only gt moves, and i stays to examine the arrival."},{"at":{"lt":1,"i":2,"gt":6},"vars":{"pivot":4,"arr":"[0, 4, 1, 4, 9, 2, 4, 7]"},"note":"The value 0 is below 4, so it swaps with slot lt. Both lt and i advance."},{"at":{"lt":2,"i":3,"gt":6},"vars":{"pivot":4,"arr":"[0, 1, 4, 4, 9, 2, 4, 7]"},"note":"The value 1 is below 4, so it swaps with slot lt. Both lt and i advance."},{"at":{"lt":2,"i":4,"gt":6},"vars":{"pivot":4,"arr":"[0, 1, 4, 4, 9, 2, 4, 7]"},"note":"The value 4 equals 4, so only i advances."},{"at":{"lt":2,"i":4,"gt":5},"vars":{"pivot":4,"arr":"[0, 1, 4, 4, 4, 2, 9, 7]"},"note":"The value 9 is above 4, so it swaps with slot gt. Only gt moves, and i stays to examine the arrival."},{"at":{"lt":2,"i":5,"gt":5},"vars":{"pivot":4,"arr":"[0, 1, 4, 4, 4, 2, 9, 7]"},"note":"The value 4 equals 4, so only i advances."},{"at":{"lt":3,"i":6,"gt":5},"vars":{"pivot":4,"arr":"[0, 1, 2, 4, 4, 4, 9, 7]"},"note":"The value 2 is below 4, so it swaps with slot lt. Both lt and i advance."}]}
```

The hardest step is the first large value, 7. It swaps with the last slot, which holds 0, and `i` does not move. The next step then examines the 0 that just arrived. It is below the pivot, so it swaps into the front. If `i` had moved after the first swap, the program would have skipped that 0 and left it inside the equal range.

<!-- stage: code -->
### Implement Both Partitions With Bounds

```java
final class Partition {
    static void swap(int[] a, int x, int y) {
        int t = a[x];
        a[x] = a[y];
        a[y] = t;
    }

    // Lomuto: pivot is a[hi]; returns the final index of the pivot.
    static int lomuto(int[] a, int lo, int hi) {
        int pivot = a[hi];                 // fix the pivot value before any swap
        int i = lo;                        // a[lo..i-1] holds values below the pivot
        for (int j = lo; j < hi; j++) {    // a[j..hi-1] is the unresolved region
            if (a[j] < pivot) {
                swap(a, i, j);             // move the small value to the end of the small range
                i++;
            }
        }
        swap(a, i, hi);                    // place the pivot between the two ranges
        return i;
    }

    // Three-way: returns {lt, gt} so that a[lt..gt] equals the pivot value.
    static int[] threeWay(int[] a, int lo, int hi, int pivot) {
        int lt = lo, i = lo, gt = hi;      // the unresolved region is a[i..gt]
        while (i <= gt) {
            if (a[i] < pivot) {
                swap(a, lt++, i++);        // the value from a[lt] is equal, so i moves too
            } else if (a[i] > pivot) {
                swap(a, i, gt--);          // the value from a[gt] is unexamined, so i stays
            } else {
                i++;                       // an equal value is already in place
            }
        }
        return new int[]{lt, gt};
    }
}
```

Both methods take the bounds `lo` and `hi` and never copy a subarray. The pivot value is read into a local variable before any swap, so no swap can change it. A swap of a slot with itself is harmless, because the value is written back unchanged. Each loop does constant work per slot, so both methods cost O(hi - lo + 1) time and O(1) extra space.

<!-- stage: applicability -->
### When A Partition Applies

#### Recognize The Pattern

Use a partition when values must be divided around a pivot in place and the order inside each group does not matter. The invariant to write down before coding is the list of index ranges and what each one holds. Every loop step must keep that list true, and the loop must end when the unresolved region is empty. Pick the Lomuto partition when you need one final pivot position, as in a selection step. Pick the three-way partition when many values can equal the pivot, because the equal range is finished work that later steps skip.

#### Watch For The Nearest False Friend

Sorting is a false friend. It also leaves the pivot in place, but it orders every group and costs O(n log n). A partition costs O(n) and gives only the grouping. If the problem asks for sorted output, partition alone is not enough. A second false friend is the Lomuto partition on many equal values. Equal values count as large there, so an array of identical values leaves the pivot at index `lo` and a right part of `n - 1` values that the next call must partition again. A recursion on that input does O(n) work per level for n levels.

#### Avoid The Java Index Traps

Define `lo`, `hi` and the pivot before the first swap. Pass the bounds to a recursive call instead of calling `Arrays.copyOfRange`, because a copy changes the copy and leaves the original array unchanged. Compute a middle index as `lo + (hi - lo) / 2`, because `(lo + hi) / 2` overflows `int` for large indexes. In the three-way loop, keep `i` in place after a swap with `gt`.

<!-- stage: exercises -->
### Exercises

#### [Build] Lomuto Partition (Author exercise)
<!-- id: par-lomuto-partition -->

**Prerequisites.** The Lomuto regions from this lesson.

**Problem.** Given an `int` array `a` and inclusive bounds `lo` and `hi`, take the pivot `a[hi]`. Rearrange `a[lo..hi]` in place so that every value below the pivot comes first, the pivot comes next, and every other value comes last. Use the scan described in this lesson. Return the final index of the pivot.

**Constraints.** The limits are:
- **Length** of `a` is an `int` with `1 <= n <= 10^5`.
- **Bounds** satisfy `0 <= lo <= hi < n`.
- **Values** are `int` values and may repeat.
- **Mutation** is limited to `a[lo..hi]`, and other slots stay unchanged.

**Example 1.** Input `a = [6, 3, 9, 2, 7, 4]`, `lo = 0`, `hi = 5`. Output 2, and `a` becomes `[3, 2, 4, 6, 7, 9]`.

**Example 2.** Input `a = [5, 1, 5, 5, 2]`, `lo = 1`, `hi = 3`. Output 2, and `a` stays `[5, 1, 5, 5, 2]`, since slots 0 and 4 are outside the bounds.

**Hint.** What does the slot `i` hold when the scan meets a value that is not below the pivot?

**Changed decision.** Baseline case: keeps a prefix of strictly smaller values.

#### [Vary] Three-Way Partition (Author exercise)
<!-- id: par-three-way-partition -->

**Prerequisites.** The Lomuto exercise above.

**Problem.** Given an `int` array `a` and an `int` value `p`, rearrange `a` in place into three consecutive ranges. The first range holds values below `p`, the second holds values equal to `p`, and the third holds values above `p`. Return `{lt, gt}`, where the second range is `a[lt..gt]`. The value `p` need not occur in `a`.

**Constraints.** The limits are:
- **Length** of `a` is an `int` with `0 <= n <= 10^5`.
- **Values** and `p` are `int` values.
- **Return** is an `int[]` of length 2, and `gt = lt - 1` when no value equals `p`.
- **Order** inside each range is not specified.

**Example 1.** Input `a = [4, 7, 1, 4, 9, 2, 4, 0]` and `p = 4`. Output `[3, 5]`, since three values are below 4 and three are equal to it.

**Example 2.** Input `a = [8, 9, 6]` and `p = 5`. Output `[0, -1]`, because no value is below or equal to 5.

**Hint.** After a swap with the end of the unresolved region, has the value now at `i` been compared?

**Changed decision.** The output changes from one pivot index to a range of equal values, so the program needs a third pointer.

#### [Boundary] All Equal Values (Author exercise)
<!-- id: par-all-equal-values -->

**Prerequisites.** The two exercises above.

**Problem.** Given an `int` array `a`, inclusive bounds `lo` and `hi`, and an index `k` with `lo <= k <= hi`, take the pivot value `a[hi]`. Partition `a[lo..hi]` into values below, equal to, and above the pivot, in place. If the position `k` lies in the equal range, return `{-1, -1}`. Otherwise return the bounds of the smaller or larger range that contains `k`.

**Constraints.** The limits are:
- **Length** of `a` is an `int` with `1 <= n <= 10^5`.
- **Bounds** satisfy `0 <= lo <= hi < n`.
- **Values** are `int` values, and all of them may be equal.
- **Mutation** is limited to `a[lo..hi]`.

**Example 1.** Input `a = [3, 8, 3, 1, 3, 9, 3]`, `lo = 0`, `hi = 6`, `k = 5`. Output `[5, 6]`, because the equal range is `a[1..4]` and `k` lies above it.

**Example 2.** Input `a = [5, 5, 5, 5, 5]`, `lo = 0`, `hi = 4`, `k = 2`. Output `[-1, -1]`, because the whole range is equal and one pass finishes the search.

**Hint.** When every value equals the pivot, which pointer moves on each step, and where does the loop stop?

**Changed decision.** The input is all one value, so a two-way split would leave n - 1 values to examine, while a three-way split leaves none.

#### [Recognize] Kth Largest Element In An Array (LeetCode 215)
<!-- id: par-kth-largest-unchanged -->

**Prerequisites.** All three exercises above.

**Problem.** Given an `int` array `nums` and an integer `k`, find the `k`-th largest value, where each repeated value counts as its own entry in the sorted order. The input array must not be modified. Use partition with index bounds and discard the ranges that cannot contain the answer.

**Constraints.** The limits are:
- **Length** of `nums` is an `int` with `1 <= n <= 10^5`.
- **`k`** is an `int` with `1 <= k <= n`.
- **Values** are `int` values and may repeat.
- **Mutation** of `nums` is not allowed, so one working copy is allowed.

**Example 1.** Input `nums = [4, 9, 2, 9, 7, 1]` and `k = 3`. Output 7, since the sorted order from the top is 9, 9, 7.

**Example 2.** Input `nums = [5, 5, 5, 5]` and `k = 4`. Output 5, and the equal range ends the search at once.

**Hint.** Which index in ascending order holds the `k`-th largest, and which three-way range can the search drop?

**Changed decision.** The contract keeps the caller's array unchanged and counts duplicates separately, so the program partitions a working copy and relies on the equal range.
