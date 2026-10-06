<!-- lesson-kind: combination -->
<!-- lesson-id: count-subarrays-from-stack-boundaries -->
## Count Subarrays From Stack Boundaries

<!-- stage: context -->
### Scoring Every Range Of A Latency Log

A monitoring service stores one response time per minute. To score a day, it takes every range of consecutive minutes, finds the fastest response inside the range, and adds all those fastest times. A log of 1,000 minutes has about 500,000 ranges, and the score appears at once. A log of 100,000 minutes has about 5 billion ranges, and the same code needs several seconds and grows fourfold when the log doubles.

The service needs the same score without visiting every range. This lesson asks how one scan of the log can add up the fastest response of every range, and how the same scan sums the largest value of every range.

<!-- stage: contributions -->
### What Each Earlier Idea Adds

Two kinds of earlier work meet here, and each supplies a different half of the answer. The stack lessons of Chapter 11 supply the container. A stack holds the indices that still wait for a decision, and the top is always the newest of them. The first lessons of this chapter add an order to that stack. When an arriving value beats the top, the top leaves, and the arriving index becomes the first value on its right that beats it.

The later lessons of this chapter supply the counting. In the array 3, 5, 3, 4, the 5 at index 1 has the smaller neighbors at index 0 and index 2. The two neighbors limit the ranges where 5 is the largest to the ranges that contain index 1 and stay between them. The tie lesson decides which of two equal values owns a range that holds both, and the rectangle lesson turns the distance between neighbors into a width. Alone, the ordered stack names neighbors but counts nothing. Alone, the counting formulas need neighbors and have no cheap way to find them. Together they answer both questions at the moment a value leaves.

<!-- stage: naive -->
### Take The Minimum Of Every Range

The direct plan fixes a start index and extends the end one step at a time. It keeps the minimum of the range so far, so each extension costs constant time.

```java
static long scoreByRanges(int[] latency) {
    long score = 0;
    for (int from = 0; from < latency.length; from++) {
        int fastest = latency[from];
        for (int to = from; to < latency.length; to++) {
            fastest = Math.min(fastest, latency[to]);   // running minimum of the range from..to
            score += fastest;                           // every range adds its own minimum
        }
    }
    return score;
}
```

The method is correct for any log. It visits every pair `(from, to)` with `from <= to`.

<!-- stage: bottleneck -->
### Most Of The Work Repeats One Answer

```predict
The log is 2, 5, 3, 5. It has 10 ranges. An index owns a range when its value is the minimum of that range. How many ranges does each index own?

Index 0 and index 2 each own 4 ranges, and index 1 and index 3 each own 1. Index 0 owns every range that starts at 0. Index 2 owns the four ranges inside indices 1 to 3 that contain index 2. The four counts add up to 10.
```

The method visits `n * (n + 1) / 2` ranges, so its cost is O(n^2). Most of that work repeats one answer. The four ranges that start at index 0 all report the value 2, and the method rediscovers 2 as their minimum every time. A faster method must count how many ranges report each value, then multiply by the value, so that each index is handled once.

<!-- stage: insight -->
### Count A Value As It Leaves

#### One Pop Gives Both Neighbors

The method scans the log with a stack of indices whose values never decrease from bottom to top. When the value at index `j` is less than or equal to the value at the top, the top leaves. The index `j` is then the right boundary of the leaving index `t`, which is the first value on its right that is not larger. The index below `t` on the stack is its left boundary, which is the last strictly smaller value on its left, or `-1` for an empty stack. Every range that contains `t` and stays strictly between the two boundaries has the value at `t` as its minimum.

#### The Owned Count Is A Product

The **owned count** of `t` is the number of ranges for which `t` is the minimum. A range picks a start from the `t - left` indices after the left boundary, up to `t`. It picks an end from the `right - t` indices from `t` up to before the right boundary. The two choices are independent, so the owned count is `(t - left) * (right - t)`. The method adds `value * owned count` to the score at the moment `t` leaves.

#### The Tie Rule And The Closing Step

Two equal values must not both claim a range that contains them. The **tie rule** here lets the rightmost minimum own the range. An arriving value that equals the top removes the top, so the earlier index stops at the later one, and the later index owns every range that contains both. The **closing step** is a final round with `j` equal to `n`. It removes every index still on the stack with right boundary `n`, so no range is lost. The invariant is that every range is counted exactly once, by the rightmost index that holds its minimum. Every index enters the stack once and leaves once, so the whole scan costs O(n).

<!-- names: owned count, tie rule, closing step -->

<!-- stage: variables -->
### State For One Counting Scan

The scan keeps five pieces of state.

- **stack** holds indices whose values never decrease from bottom to top, and the top is the newest.
- **j** is the index of the arriving value, and it runs from 0 to `n`, where `n` marks the closing step.
- **t** is the index that just left the stack, and the pass reads its value once.
- **left** is the index now on top of the stack after `t` leaves, or `-1` when the stack is empty.
- **total** is the running score, held in a `long`, because a sum over billions of ranges overflows `int`.

The owned count of `t` is computed from `left`, `t` and `j`, and the method does not store it.

<!-- stage: trace -->
### Following Pops And Owned Counts

The first trace scores the log `[3, 5, 3, 4]` by minimums. The array has 10 ranges, and each step shows the stack after the arriving index is handled. The arriving 3 at index 2 removes the 5 and also the equal 3 at index 0, so index 2 owns every range that contains both 3 values. The closing step removes the rest of the stack. The owned counts are 2, 1, 6 and 1, which add to 10, and the score is 33.

The second trace runs the same log by maximums. The method changes one comparison: an arriving value now removes the top when the top is smaller or equal. The owned counts are 1, 6, 1 and 2, which also add to 10. The score is 44. The difference 44 minus 33 equals 11, which is the sum over all ranges of the largest value minus the smallest value.

```trace
{"cells":[3,5,3,4],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","owned":"[0,0,0,0]"},"note":"The reading 3 arrives. Nothing leaves the stack."},{"at":{"j":1},"vars":{"stack":"[0,1]","owned":"[0,0,0,0]"},"note":"The reading 5 arrives. Nothing leaves the stack."},{"at":{"j":2},"vars":{"stack":"[2]","owned":"[2,1,0,0]"},"note":"The reading 3 arrives. Index 1 leaves with left boundary 0 and right boundary 2, so it owns 1. Index 0 leaves with left boundary -1 and right boundary 2, so it owns 2."},{"at":{"j":3},"vars":{"stack":"[2,3]","owned":"[2,1,0,0]"},"note":"The reading 4 arrives. Nothing leaves the stack."},{"at":{"j":4},"vars":{"stack":"[]","owned":"[2,1,6,1]"},"note":"The closing step arrives. Index 3 leaves with left boundary 2 and right boundary 4, so it owns 1. Index 2 leaves with left boundary -1 and right boundary 4, so it owns 6."}]}
```

```trace
{"cells":[3,5,3,4],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","owned":"[0,0,0,0]"},"note":"The reading 3 arrives. Nothing leaves the stack."},{"at":{"j":1},"vars":{"stack":"[1]","owned":"[1,0,0,0]"},"note":"The reading 5 arrives. Index 0 leaves with left boundary -1 and right boundary 1, so it owns 1."},{"at":{"j":2},"vars":{"stack":"[1,2]","owned":"[1,0,0,0]"},"note":"The reading 3 arrives. Nothing leaves the stack."},{"at":{"j":3},"vars":{"stack":"[1,3]","owned":"[1,0,1,0]"},"note":"The reading 4 arrives. Index 2 leaves with left boundary 1 and right boundary 3, so it owns 1."},{"at":{"j":4},"vars":{"stack":"[]","owned":"[1,6,1,2]"},"note":"The closing step arrives. Index 3 leaves with left boundary 1 and right boundary 4, so it owns 2. Index 1 leaves with left boundary -1 and right boundary 4, so it owns 6."}]}
```

<!-- stage: code -->
### One Scan For Minimums And Maximums

```java
static long sumOfExtremes(int[] a, boolean maxima) {
    int n = a.length;
    int[] stack = new int[n];
    int size = 0;                                              // number of indices on the stack
    long total = 0;
    for (int j = 0; j <= n; j++) {                             // j == n is the closing step
        while (size > 0 && (j == n || (maxima ? a[stack[size - 1]] <= a[j] : a[stack[size - 1]] >= a[j]))) {
            int t = stack[--size];                             // t leaves with right boundary j
            int left = size == 0 ? -1 : stack[size - 1];       // the new top is the left boundary
            total += (long) a[t] * (t - left) * (j - t);       // value times owned count
        }
        if (j < n) stack[size++] = j;                          // every arriving index waits on the stack
    }
    return total;
}

static long sumOfRanges(int[] a) {
    return sumOfExtremes(a, true) - sumOfExtremes(a, false);   // largest minus smallest, summed over ranges
}
```

The cast to `long` happens before the first multiplication, so the product cannot overflow `int` on the way. Both comparisons include equality, so the rightmost extreme owns every range that holds a tie.

- **Time** is O(n), since the loop pushes each index once and removes it once.
- **Space** is O(n) for the stack array.

<!-- stage: applicability -->
### Telling When Boundaries Give The Answer

#### Applying The Invariant

Use this method when the answer is a sum or a maximum over regions, and each region is determined by the one value that limits it. The invariant is that an index leaves the stack exactly when both of its boundaries are known, and the product of the two distances is final at that moment. Use the same loop for rectangles, where the owned count becomes a width and the value becomes a height.

#### Finding The False Friend

The false friend is the wrong tie rule. If both sides stop at equal values, no index owns the ranges that hold both, and the total shrinks. If neither side stops at equal values, two equal values each claim those ranges, and the total grows too large. The tie rule must treat one side strictly and the other side non-strictly. A second false friend is a sum of values inside the range. A range sum needs prefix sums, and no boundary pair determines it.

#### No-Go Conditions

Do not use the method when a range does not have one limiting value, such as a count of distinct values or a median. Do not use it when a removal must stay within a fixed budget, because the stack alone never proves that a removal is safe. A later chapter on greedy proofs covers that case.

<!-- stage: exercises -->
### Exercises

#### [Build] Next Greater Element I Pairs (LeetCode 496)
<!-- id: ms-combo-pop-pairs -->

**Prerequisites.** The ordered stack of the first lesson. The problem reuses the next greater idea of LC 496, with a changed output contract.

**Problem.** The input is an integer array `a`. When an index `j` arrives, every index `t` on the stack whose value is strictly less than `a[j]` leaves the stack, from the top downward. Return the pairs `[t, j]` in the order the indices leave. Indices that never leave do not appear.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Values** are integers between -1,000,000,000 and 1,000,000,000.
- **Output** is an `int[][]` of pairs, possibly empty.

**Example 1.** Input `a = [4, 1, 2, 5]`, output `[[1, 2], [2, 3], [0, 3]]`.

**Example 2.** Input `a = [3, 3, 3]`, output `[]`.

**Hint.** Which index leaves first when a value arrives, the newest waiting index or the oldest?

**Changed decision.** The method records both indices at the leaving moment, and no result array is indexed by position.

#### [Vary] Daily Temperatures With The Longest Wait (LeetCode 739)
<!-- id: ms-combo-longest-wait -->

**Prerequisites.** The leaving index and its resolving index. The problem reuses LC 739 with a changed output contract.

**Problem.** For each day `i`, the wait is `j - i`, where `j` is the first later day with a strictly higher temperature. A day with no such `j` has no wait. Return `[start, wait]` for the day with the largest wait, and choose the smallest start when waits tie. Return `[-1, -1]` when no day has a wait.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Temperatures** are integers between -100 and 100.
- **Output** is an `int[]` of length 2.

**Example 1.** Input `t = [73, 74, 75, 71, 69, 72, 76, 73]`, output `[2, 4]`.

**Example 2.** Input `t = [5, 4, 3]`, output `[-1, -1]`.

**Hint.** The wait is known when the day leaves the stack. Which update keeps the best pair so far?

**Changed decision.** The distance is compared at the leaving moment, and the answer keeps a single pair.

#### [Boundary] Largest Rectangle With Its Left Index (LeetCode 84)
<!-- id: ms-combo-best-rectangle-left -->

**Prerequisites.** Both boundaries of a leaving bar and the closing step. The problem reuses LC 84 with a changed output contract.

**Problem.** A histogram has bars of width 1 and integer heights. A rectangle covers consecutive bars, and its height is the shortest bar it covers. Return `[area, left]` for a rectangle of the largest area, where `left` is the index of its first bar. When several rectangles share the largest area, choose the smallest `left`.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Heights** are integers between 1 and 10,000.
- **Output** is an `int[]` of length 2.

**Example 1.** Input `h = [2, 1, 5, 6, 2, 3]`, output `[10, 2]`.

**Example 2.** Input `h = [1, 2, 3, 4]`, output `[6, 1]`.

**Hint.** In Example 2 no bar is shorter than its predecessor. Which step finally reports a rectangle?

**Changed decision.** A leaving bar reports its left index with the area, and equal areas prefer the smaller index.

#### [Recognize] Sum Of Subarray Maximums (LeetCode 907)
<!-- id: ms-combo-sum-maximums -->

**Prerequisites.** The owned count and the tie rule. The problem mirrors LC 907 with maximums, negative values and no modulus.

**Problem.** For an integer array `a`, add up the largest value of every non-empty contiguous subarray. Subarrays at different positions count separately, even when their values are equal. Return the sum.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 30,000.
- **Values** are integers between -100,000 and 100,000.
- **Output** is a `long`.

**Example 1.** Input `a = [3, 1, 2]`, output `14`.

**Example 2.** Input `a = [-2, -2, -2]`, output `-12`.

**Hint.** Which comparison lets the rightmost maximum own a range with two equal maxima?

**Changed decision.** The comparison flips from minimums to maximums, and the product uses a negative value without any special case.
