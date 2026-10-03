<!-- lesson-kind: combination -->
<!-- lesson-id: stack-and-contribution-counting -->
## Stack And Contribution Counting

<!-- stage: context -->
### Two Clerks At One River Gauge

A river authority posts one gauge reading every morning, and two clerks share the ledger. The first clerk answers questions about single days: how many days until the river next stands higher than it does today, or which stretch of days has a particular reading as its lowest. The second clerk prepares the yearly report, which needs a figure for every stretch of consecutive days, such as how far apart the highest and lowest readings of the stretch were, added up over all stretches.

The ledger is long, and the authority wants both clerks to finish in one reading of it. The second clerk's report involves hundreds of thousands of stretches even for a modest ledger, and the first clerk's questions repeat for every day. The two of them notice that they keep looking for the same thing: for each day, the nearest day on either side whose reading beats it.

<!-- stage: contributions -->
### What The Stack And The Counts Bring

The ordered stack brings the walls. It keeps the days that have not yet met a beating day, in order of reading, so that every day is given its nearest beating day on the right at the moment that day arrives, and its nearest beating day on the left from whatever remains underneath. It does this in one pass and with each day handled a constant number of times. By itself it says only where the walls are. It cannot say how many stretches lie between them, or what to do when two days tie.

Contribution counting brings the arithmetic. Given the walls of a day, the number of stretches that day decides is the product of the free starting places and the free ending places, and a total over all stretches becomes one term per day. By itself it has no way to find walls quickly, and it gives wrong totals if equal readings are allowed to claim the same stretch. The ownership rule from the earlier lesson settles the ties.

The recognition cue is a question over all stretches, or over the best stretch, where each stretch is decided by its highest or lowest day, so that the answer splits into one term per day with that day's nearest beating days as the two limits.

<!-- stage: naive -->
### Examine Every Stretch For Both Extremes

The direct method examines every stretch, tracks its lowest and highest readings as it grows, and adds the difference to a running total.

```java
static long totalSpreadByStretches(int[] reading) {
    long total = 0;
    for (int start = 0; start < reading.length; start++) {
        int low = reading[start], high = reading[start];
        for (int end = start; end < reading.length; end++) {
            low = Math.min(low, reading[end]);
            high = Math.max(high, reading[end]);
            total += high - low;
        }
    }
    return total;
}
```

It is correct, and for `[2, 5, 3, 5]` it returns 15, since the ten stretches have spreads 0, 0, 0, 0, 3, 2, 2, 3, 2 and 3, and these are added together.

<!-- stage: bottleneck -->
### The Same Walls Are Rediscovered

The double loop touches `n * (n + 1) / 2` stretches, so a ledger of 100,000 days costs about five billion steps and the method is O(n^2). In every stretch it recomputes the extremes from scratch of the growing window, although a day that is the lowest of a stretch stays the lowest as the stretch grows, until the first lower reading enters. The stretch ends of those growth steps are exactly the walls of that day.

So the quadratic cost is paying many times for the answer to one question per day, namely how far each day's role extends to the left and right. Once the walls are known, the days' roles settle the total, and a single pass with an ordered stack can supply the walls. What is left to get right is the meaning of a tie, because two days with the same reading must not both be credited with a stretch that contains them.

<!-- stage: insight -->
### Walls From The Stack, Counts From Distances

Run the **waiting stack** over the readings: it holds indices whose readings keep one order from bottom to top, and a new index removes every top that it beats. At a removal the right wall of the removed index is the current index, and the left wall is the new top. This gives both **wall distances** at once: `i - left` choices of a start and `right - i` choices of an end. What the walls are used for then depends on the question. A rectangle or window needs the width `right - left - 1`, since it is the stretch strictly between the two walls. A total over stretches needs the product `(i - left) * (right - i)`, since each start is combined with each end.

Equal readings need **tie ownership**. Make the left wall stop only at a strictly beating reading and the right wall stop at a beating or equal reading, so each stretch with tied extremes has exactly one owner, the last of the tied days. For the lowest readings, "beating" means lower, and for the highest readings it means higher, and the same asymmetric rule is used in both. Then the minima and the maxima each partition the `n * (n + 1) / 2` stretches. The spread of a stretch is its highest minus its lowest reading, so the total spread is the sum over days of the reading times the stretches the day owns as a maximum, minus the same sum for the stretches the day owns as a minimum.

<!-- names: waiting stack, wall distances, tie ownership -->

Each pass costs O(n), and two passes, one for the lowest readings and one for the highest, still cost O(n) in total.

<!-- stage: variables -->
### Walls, Counts And The Two Roles

For every index there are two pairs of walls, one pair for the role of a minimum and one for the role of a maximum. The arrays `left` and `right` are filled by one pass per role, with the sentinels -1 and `n`. The owned counts are `(i - left) * (right - i)`, stored as `long`, one array for minima and one for maxima, and both must add up to `n * (n + 1) / 2`. The width used by histogram problems is a different number, `right - left - 1`, the length of the stretch between the walls, and it should not be confused with the count of stretches. A running total in `long` collects reading times count for each role, and its difference is the answer. Every index is pushed and removed once in each pass.

<!-- stage: trace -->
### Two Passes Over A Short Ledger

Take the readings `2, 5, 3, 5`. In the pass for minima, the 2 is pushed. The 5 and then the 3 follow: the 3 removes the 5, which receives right wall 2, and its left wall is index 0, so the 5 owns `1 * 1`. The last 5 is pushed above the 3. The closing step removes the 5 at index 3 with left wall 2, the 3 with left wall 0 and right wall 4, which owns `2 * 2 = 4`, and the 2 with left wall -1, which owns `4 * 1 = 4`. The counts for minima are 4, 1, 4 and 1, which add to 10.

In the pass for maxima the comparison is reversed. The second 5 removes the 3 and also the first 5, because a maximum is removed by a reading that is higher or equal, so the first 5 gets right wall 3 and, with an empty stack beneath it, left wall -1, which gives `2 * 2 = 4` stretches. The second 5 stays until the closing step, and its left wall is -1, since the earlier 5 is no longer on the stack and an equal reading is not a strict beater, so it owns `4 * 1 = 4`. The counts for maxima are 1, 4, 1 and 4, which also add to 10. The sum of readings times counts is 45 for maxima and 30 for minima, so the total spread is 15. The step to study is the tie between the two 5s, because the earlier one stops at the later one, which then passes over it and owns the stretches containing both.

```trace
{"cells":[2,5,3,5],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","owned":"[0,0,0,0]"},"note":"The reading 2 arrives. Nothing leaves the stack."},{"at":{"j":1},"vars":{"stack":"[0,1]","owned":"[0,0,0,0]"},"note":"The reading 5 arrives. Nothing leaves the stack."},{"at":{"j":2},"vars":{"stack":"[0,2]","owned":"[0,1,0,0]"},"note":"The reading 3 arrives. Index 1 leaves with left wall 0 and right wall 2, so it owns 1."},{"at":{"j":3},"vars":{"stack":"[0,2,3]","owned":"[0,1,0,0]"},"note":"The reading 5 arrives. Nothing leaves the stack."},{"at":{"j":4},"vars":{"stack":"[]","owned":"[4,1,4,1]"},"note":"The closing step arrives. Index 3 leaves with left wall 2 and right wall 4, so it owns 1. Index 2 leaves with left wall 0 and right wall 4, so it owns 4. Index 0 leaves with left wall -1 and right wall 4, so it owns 4."}]}
```

```trace
{"cells":[2,5,3,5],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","owned":"[0,0,0,0]"},"note":"The reading 2 arrives. Nothing leaves the stack."},{"at":{"j":1},"vars":{"stack":"[1]","owned":"[1,0,0,0]"},"note":"The reading 5 arrives. Index 0 leaves with left wall -1 and right wall 1, so it owns 1."},{"at":{"j":2},"vars":{"stack":"[1,2]","owned":"[1,0,0,0]"},"note":"The reading 3 arrives. Nothing leaves the stack."},{"at":{"j":3},"vars":{"stack":"[3]","owned":"[1,4,1,0]"},"note":"The reading 5 arrives. Index 2 leaves with left wall 1 and right wall 3, so it owns 1. Index 1 leaves with left wall -1 and right wall 3, so it owns 4."},{"at":{"j":4},"vars":{"stack":"[]","owned":"[1,4,1,4]"},"note":"The closing step arrives. Index 3 leaves with left wall -1 and right wall 4, so it owns 4."}]}
```

<!-- stage: code -->
### One Counting Pass Per Role

```java
static long[] owned(int[] a, boolean forMaximum) {
    int n = a.length;
    int[] left = new int[n];
    int[] right = new int[n];
    java.util.Arrays.fill(right, n);
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && (forMaximum ? a[stack.peekLast()] <= a[j] : a[stack.peekLast()] >= a[j])) {
            right[stack.removeLast()] = j;       // beaten or tied: the non-strict right wall
        }
        left[j] = stack.isEmpty() ? -1 : stack.peekLast();   // strictly beaten survivor: the strict left wall
        stack.addLast(j);
    }
    long[] count = new long[n];
    for (int i = 0; i < n; i++) count[i] = (long) (i - left[i]) * (right[i] - i);
    return count;
}

static long sumOfRanges(int[] a) {
    long[] asMaximum = owned(a, true);
    long[] asMinimum = owned(a, false);
    long total = 0;
    for (int i = 0; i < a.length; i++) total += (long) a[i] * (asMaximum[i] - asMinimum[i]);
    return total;
}
```

Each call of `owned` is a single pass over the array with every index pushed once and removed at most once, so the pair of calls is linear in time and uses O(n) memory for the stacks and the count arrays. The only difference between the two roles is the direction of the comparison. The counts are widened to `long` before the multiplication, and the final sum is a difference of two products that are each large, so it is formed term by term to keep every intermediate value within `long`.

<!-- stage: applicability -->
### When Walls Feed Both Widths And Counts

Use the stack with contribution counting when a quantity over all stretches is decided by one extreme element per stretch, and a single extreme owner can be assigned by a tie rule. The invariant is that every stretch has exactly one owner for each role, so the counts of each role add up to `n * (n + 1) / 2`, and the walls come from one pass of a stack whose order matches the role. State the tie convention before writing the pass, and use the same convention for the minimum and the maximum.

The false friend is a pair of strict walls on both sides, which is tempting because the minimum case looks symmetric. With ties, the counts of maxima in `[4, 4, 4]` then total 10 in place of 6, and the sum of ranges would be wrong in a way that the distinct-value examples never show. A second false friend is the histogram width `right - left - 1`: it is the right number for a rectangle, where only the one widest run of an element matters, and wrong for a total, where every sub-run of it counts.

Do not use the pattern when the stretch value is not decided by a single element, such as a sum, a product or a median of the stretch. Do not use it when removal of an element is limited by a count, as in dropping the best `k` digits of a number, where the stack alone has no proof that an earlier choice can be discarded. That composition belongs to Chapter 20, which supplies the exchange argument, and no problem of that kind is assigned here.

<!-- stage: exercises -->
### Exercises

#### [Build] Next Greater By Position (LeetCode 496)
<!-- id: ms-combo-next-greater-by-position -->

**Prerequisites.** The first lesson of this chapter, and the ordered stack.

**Problem.** An integer array `reference` may contain repeated values. Another array `positions` lists positions in `reference`. For each listed position `p`, return the first value after position `p` that is strictly greater than `reference[p]`, or -1 if there is none.

**Constraints.** 1 <= reference.length <= 10^5, 0 <= reference[i] <= 10^9, and every entry of `positions` is a valid index. Values are not keys, since they may repeat.

**Example 1.** Input `reference = [3, 1, 3, 2, 4]`, `positions = [1, 0, 3]`, output `[3, 4, 4]`.

**Example 2.** Input `reference = [2, 2, 2]`, `positions = [0, 2]`, output `[-1, -1]`.

**Hint.** Why would a map from values to answers fail on the first example? What can serve as the key instead?

**Changed decision.** The answer is stored by position and not by value, because equal values would collide in a value-keyed map.

#### [Vary] Wait Totals From Resolving Positions (LeetCode 739)
<!-- id: ms-combo-wait-totals -->

**Prerequisites.** The Next Greater By Position exercise above.

**Problem.** Given an array `temps` of daily readings, let the wait of day `i` be the number of days until the first strictly warmer day, and let it be 0 if there is none. Return the array `[sum of all waits, longest single wait]`.

**Constraints.** 1 <= temps.length <= 10^5 and 30 <= temps[i] <= 100. Do not build the array of waits.

**Example 1.** Input `temps = [66, 70, 68, 68, 75, 64, 72]`, output `[8, 3]`.

**Example 2.** Input `temps = [80, 70, 60]`, output `[0, 0]`.

**Hint.** What is known about a day at the moment it is removed from the stack? Which two aggregates can be updated at that moment?

**Changed decision.** The resolving position becomes a distance, and the distances are folded into two aggregates at the moment of removal.

#### [Boundary] Best Rectangle With Its Span (LeetCode 84)
<!-- id: ms-combo-best-rectangle-span -->

**Prerequisites.** The two exercises above and the histogram lesson.

**Problem.** Given an array `heights` of bar heights with at least one positive bar, return `[area, start, end]` for the largest rectangle, where `start` and `end` are the first and last bar indices that it covers. If several rectangles have the maximum area, return the one with the smallest `start`, and if still tied, the smallest `end`.

**Constraints.** 1 <= heights.length <= 10^5 and 0 <= heights[i] <= 10^4. Use both walls and flush the stack at the end.

**Example 1.** Input `heights = [2, 4, 4, 3, 1, 5, 5, 5]`, output `[15, 5, 7]`.

**Example 2.** Input `heights = [3, 0, 3]`, output `[3, 0, 0]`, so the tie goes to the earlier rectangle.

**Hint.** Which wall gives `start` and which gives `end`? How does the tie rule change the comparison used to update the best answer?

**Changed decision.** The answer must say where the rectangle is, so the walls themselves are reported, and a tie rule decides between equal areas.

#### [Recognize] Subarray Ranges From Two Ownership Passes (LeetCode 907)
<!-- id: ms-combo-subarray-ranges -->

**Prerequisites.** All three exercises above and the duplicate-attribution lesson.

**Problem.** Given an integer array `nums`, the range of a subarray is its largest value minus its smallest value. Return the sum of the ranges of all contiguous subarrays.

**Constraints.** 1 <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4, so the total stays below 10^15 and fits in `long`. Linear time.

**Example 1.** Input `nums = [1, 3, 3]`, output 4.

**Example 2.** Input `nums = [4, 4, 4]`, output 0, since every subarray has equal extremes.

**Hint.** Split the sum into a sum of maxima and a sum of minima. What must be true of the tie convention for the two passes?

**Changed decision.** The quantity is decided by two extremes, so there are two ownership passes with mirrored comparisons and the same tie convention, and the totals are subtracted.
