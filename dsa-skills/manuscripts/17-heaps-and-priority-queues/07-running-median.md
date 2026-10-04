<!-- lesson-kind: standard -->
<!-- lesson-id: running-median -->
## Running Median

<!-- stage: context -->
### The River Gauge Midpoint

A hydrologist monitors a river with a gauge that reports the water level every few minutes. She does not trust the average of all the readings so far, because a single flood surge drags it upward for days. She prefers the median, the middle value when the readings are put in order, which a surge hardly moves. After every new reading she wants the median of everything recorded so far, to be shown on the dashboard in her office.

The first season produced a few hundred readings and her spreadsheet coped. The new gauge reports every ten seconds and has been running for a year. She has noticed that each new reading takes longer to appear than the one before, and the dashboard is now slower than the river.

<!-- stage: naive -->
### Keep A Sorted List

The direct method keeps all readings in a sorted `ArrayList`. A new reading is inserted at its sorted position, found by binary search, and the median is read from the middle of the list.

```java
static double addAndReadMedian(java.util.ArrayList<Integer> sorted, int reading) {
    int pos = java.util.Collections.binarySearch(sorted, reading);
    if (pos < 0) pos = -pos - 1;
    sorted.add(pos, reading);
    int n = sorted.size();
    return n % 2 == 1 ? sorted.get(n / 2) : ((double) sorted.get(n / 2 - 1) + sorted.get(n / 2)) / 2;
}
```

It is correct. After the readings `5, 15, 1` it reports 5.0, then 10.0, then 5.0.

<!-- stage: bottleneck -->
### Insertion Shifts Half The List

The binary search is cheap, but `add(pos, reading)` must slide every later element one place to the right, so an insertion costs O(n) in the worst case, and a stream of `n` readings costs O(n^2). For a year of ten-second readings, about three million values, the list moves billions of elements, and each of those moves serves only to keep exact positions that nobody reads. Sorting the whole list after each reading is worse, at O(n log n) per reading.

The dashboard asks for one or two numbers at the centre of the order. It never asks where a reading ranks in the upper tail or the lower tail, so the exact order of the outer values is not needed. What is needed is to know which values sit just below the middle and which sit just above it, and to be able to hand one value across the boundary when a new reading shifts the middle. A structure that exposes the largest of the low values and the smallest of the high values would answer both questions at once.

<!-- stage: insight -->
### Two Heaps Meet At The Middle

Split the readings into two groups around the median. The **lower half** is a max-heap that holds the smaller readings, so its root is the largest of them. The **upper half** is a min-heap that holds the larger readings, so its root is the smallest of them. The two roots are the two values next to the middle, and they are the only values the median ever needs. The invariant has two parts: every value in the lower half is no greater than every value in the upper half, and the sizes differ by at most one, with the lower half the larger one when the count is odd.

Each reading is inserted by a **balance move**, a fixed short routine that keeps both parts of the invariant. Offer the reading to the lower half, then poll the lower half's root and offer it to the upper half. This guarantees that the order between the halves still holds, since the largest low value is the one that crosses. If the upper half is now bigger than the lower half, poll the upper half's root and offer it back to the lower half. For an odd count the median is the lower root, and for an even count it is the average of the two roots.

<!-- names: lower half, upper half, balance move -->

An insertion makes at most five heap operations, so it costs O(log n), and reading the median costs O(1). A stream of `n` readings costs O(n log n) in total, and the memory is O(n) for the readings that must be kept. The two heaps together keep exactly as much order as the median needs, and the order within each half is left as loose as a heap leaves it.

<!-- stage: variables -->
### Two Roots, Two Sizes And Parity

The lower half is a max-first queue and the upper half is a min-first queue, and every reading lives in exactly one of them. The two sizes drive the whole logic: the lower size is either equal to the upper size or larger by one, and that is restored at the end of each insertion. The parity of the total count says how to read the median, since an odd count has one more value in the lower half and an even count has equal halves. The median is derived from the roots at the moment of the query and is not stored. When the lower half is empty there is no reading yet, and the median is undefined, so a query must not run before the first insertion.

<!-- stage: trace -->
### A Reading Crosses The Middle

The first run feeds the readings `5, 15, 1, 3, 8, 7`. The 5 goes to the lower half through the upper half and back, so it is the only value and the median. The 15 enters the lower half, is the largest there, and crosses to the upper half. The sizes are now equal, so nothing returns, the roots are 5 and 15, and the median is 10. The 1 enters the lower half below the 5, so the 5 is the value that crosses upward, and the upper half would then be the larger one, so the 5 is sent down again. After six readings the halves are `1, 3, 5` and `7, 8, 15`, and the median is 6.

The second run feeds the falling readings `9, 7, 5, 3, 1`. Each new reading is smaller than everything seen, so it lands in the lower half and pushes the old lower root across to the upper half, and the medians are 9, 8, 7, 6 and 5. The step to study is the third reading of the first run, where the median falls from 10 to 5 because the 5 is brought back to the lower half.

```trace
{"cells":[5,15,1,3,8,7],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lower":"[5]","upper":"[]","median":5},"note":"Reading 5 is offered to the lower half, and its root 5 crosses to the upper half. The upper half is now larger, so its root 5 moves back to the lower half. The count is odd, so the median is the lower root 5."},{"at":{"i":1},"vars":{"lower":"[5]","upper":"[15]","median":10.0},"note":"Reading 15 is offered to the lower half, and its root 15 crosses to the upper half. The sizes already satisfy the rule, so nothing moves back. The count is even, so the median is the average of 5 and 15, which is 10.0."},{"at":{"i":2},"vars":{"lower":"[5,1]","upper":"[15]","median":5},"note":"Reading 1 is offered to the lower half, and its root 5 crosses to the upper half. The upper half is now larger, so its root 5 moves back to the lower half. The count is odd, so the median is the lower root 5."},{"at":{"i":3},"vars":{"lower":"[3,1]","upper":"[5,15]","median":4.0},"note":"Reading 3 is offered to the lower half, and its root 5 crosses to the upper half. The sizes already satisfy the rule, so nothing moves back. The count is even, so the median is the average of 3 and 5, which is 4.0."},{"at":{"i":4},"vars":{"lower":"[5,3,1]","upper":"[8,15]","median":5},"note":"Reading 8 is offered to the lower half, and its root 8 crosses to the upper half. The upper half is now larger, so its root 5 moves back to the lower half. The count is odd, so the median is the lower root 5."},{"at":{"i":5},"vars":{"lower":"[5,3,1]","upper":"[7,8,15]","median":6.0},"note":"Reading 7 is offered to the lower half, and its root 7 crosses to the upper half. The sizes already satisfy the rule, so nothing moves back. The count is even, so the median is the average of 5 and 7, which is 6.0."}]}
```

```trace
{"cells":[9,7,5,3,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lower":"[9]","upper":"[]","median":9},"note":"Reading 9 is offered to the lower half, and its root 9 crosses to the upper half. The upper half is now larger, so its root 9 moves back to the lower half. The count is odd, so the median is the lower root 9."},{"at":{"i":1},"vars":{"lower":"[7]","upper":"[9]","median":8.0},"note":"Reading 7 is offered to the lower half, and its root 9 crosses to the upper half. The sizes already satisfy the rule, so nothing moves back. The count is even, so the median is the average of 7 and 9, which is 8.0."},{"at":{"i":2},"vars":{"lower":"[7,5]","upper":"[9]","median":7},"note":"Reading 5 is offered to the lower half, and its root 7 crosses to the upper half. The upper half is now larger, so its root 7 moves back to the lower half. The count is odd, so the median is the lower root 7."},{"at":{"i":3},"vars":{"lower":"[5,3]","upper":"[7,9]","median":6.0},"note":"Reading 3 is offered to the lower half, and its root 7 crosses to the upper half. The sizes already satisfy the rule, so nothing moves back. The count is even, so the median is the average of 5 and 7, which is 6.0."},{"at":{"i":4},"vars":{"lower":"[5,3,1]","upper":"[7,9]","median":5},"note":"Reading 1 is offered to the lower half, and its root 5 crosses to the upper half. The upper half is now larger, so its root 5 moves back to the lower half. The count is odd, so the median is the lower root 5."}]}
```

<!-- stage: code -->
### Median Of A Growing Stream

```java
final class RunningMedian {
    private final java.util.PriorityQueue<Integer> lower =
        new java.util.PriorityQueue<>(java.util.Comparator.reverseOrder());   // max-heap
    private final java.util.PriorityQueue<Integer> upper = new java.util.PriorityQueue<>();

    void add(int reading) {
        lower.offer(reading);
        upper.offer(lower.poll());                    // largest low value crosses upward
        if (upper.size() > lower.size()) lower.offer(upper.poll());   // restore the size rule
    }

    double median() {
        if (lower.size() > upper.size()) return lower.peek();
        return ((double) lower.peek() + upper.peek()) / 2;
    }
}
```

Each `add` makes at most five heap operations of logarithmic cost, so it runs in O(log n), and `median` runs in O(1). The cast `(double) lower.peek()` widens before the addition, so two large readings cannot overflow an `int`. In an odd count the lower half is larger by one, and the first branch of `median` returns its root, which an `int` converts to `double` without loss. Calling `median` on an empty object would unbox a `null` and throw a `NullPointerException`, so the caller must add at least one reading first.

<!-- stage: applicability -->
### When The Middle Keeps Moving

Use the two-heap layout when values arrive online and the median, or another fixed quantile, of everything so far is needed after each arrival. The invariant is that the lower half holds the smaller values and the upper half the larger ones, with sizes balanced to within one, so that the middle is always visible at the two roots. The same layout supports a median of a window when expiry is handled by lazy deletion and the sizes are counted logically, as in the previous lesson.

The false friend is a single heap. A max-heap or a min-heap shows only one extreme, so to find the middle it would have to be emptied half way, and a single sorted structure would pay O(n) per insertion if it were an array. A balanced search tree does work at O(log n), but it is a heavier tool than the question needs. Another false friend is an average, which is easy to maintain and has the surge problem that motivated the median.

Do not use it for an arbitrary rank that changes between queries, since the halves are tied to one split point. For a fixed fraction such as the 90th percentile, the sizes are kept at that ratio instead of a one-to-one split. In Java, widen to `long` or `double` before adding two values, keep the size rule in one place, and make the lower half a max-first queue through an explicit comparator.

<!-- stage: exercises -->
### Exercises

#### [Build] Rebalance Two Halves (Author exercise)
<!-- id: hp-rebalance-two-halves -->

**Prerequisites.** The balance move, the lower half and the upper half of this lesson.

**Problem.** Insert the positive integers of `values` one at a time, using a lower max-heap and an upper min-heap and the balance move described in the lesson. After the last insertion return `[lowerSize, upperSize, lowerRoot, upperRoot]`, with 0 for a root of an empty heap.

**Constraints.** 1 <= values.length <= 10^5 and 1 <= values[i] <= 10^9.

**Example 1.** Input `values = [5, 15, 1]`, output `[2, 1, 5, 15]`.

**Example 2.** Input `values = [4]`, output `[1, 0, 4, 0]`.

**Hint.** Which heap receives the new value first? What would happen to the order between the halves if you inserted straight into the half that the value seems to belong to, without the crossing step?

**Changed decision.** First rung: the two sizes and the two roots are the whole state, and the crossing step is the one rule that has to keep the order between the halves.

#### [Vary] Find Median from Data Stream (LeetCode 295)
<!-- id: hp-find-median-stream -->

**Prerequisites.** Rebalance Two Halves above.

**Problem.** Support two operations on a growing collection of positive integers. A positive number `x` in `ops` adds `x`, and the value 0 asks for the median of all numbers added so far. For an odd count the median is the middle value, and for an even count it is the average of the two middle values. Return the answer to each query as a `double`. At least one number has been added before each query.

**Constraints.** 1 <= ops.length <= 10^5 and each added value is between 1 and 10^9.

**Example 1.** Input `ops = [5, 15, 0, 1, 0, 3, 0]`, output `[10.0, 5.0, 4.0]`.

**Example 2.** Input `ops = [2, 0]`, output `[2.0]`.

**Hint.** For which parity of the count do you return one root, and for which do you average two? Which sizes does each parity imply?

**Changed decision.** The median is now read at chosen moments and must be computed from the roots, with one root for an odd count and two for an even count.

#### [Boundary] Overflow-Safe Even Median (Author exercise)
<!-- id: hp-overflow-safe-median -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `values` of arbitrary `int` values, return the median of the prefix after each insertion, as a `double` array of the same length. For an even prefix the median is the exact average of the two middle values.

**Constraints.** 1 <= values.length <= 10^5, and every value is any `int`, including `-2147483648` and `2147483647`.

**Example 1.** Input `values = [2147483647, 2147483647]`, output `[2147483647.0, 2147483647.0]`.

**Example 2.** Input `values = [-2147483648, -2147483648]`, output `[-2147483648.0, -2147483648.0]`.

**Hint.** What does `a + b` evaluate to for two large `int` values, before the division is applied? Where must the widening happen?

**Changed decision.** The extreme values make the sum of two roots overflow an `int`, so the average has to be formed in a wider type.

#### [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-window-lower-median-report -->

**Prerequisites.** All three exercises above, and the lazy deletion lesson.

**Problem.** Given an integer array `nums` and a window length `k`, take the lower median of each window of `k` consecutive values, which is the element at index `(k - 1) / 2` of the sorted window, so even windows use the smaller of the two middle values and every median is an `int`. Return `[sum of the lower medians as a long, number of windows whose median differs from the previous window's median]`.

**Constraints.** 1 <= k <= nums.length <= 10^5 and every value is any `int`.

**Example 1.** Input `nums = [5, 1, 9, 7, 7, 2, 8]`, `k = 4`, output `[26, 1]`.

**Example 2.** Input `nums = [-2147483648, -2147483648, 2147483647]`, `k = 2`, output `[-4294967296, 0]`.

**Hint.** What decides whether an entry in a heap is stale when values leave in arrival order? How do the logical sizes of the halves change when the oldest value expires?

**Changed decision.** The contract asks for a lower median with a wide sum and a count of changes, so expiry must keep the halves exactly balanced and no averaging occurs.
