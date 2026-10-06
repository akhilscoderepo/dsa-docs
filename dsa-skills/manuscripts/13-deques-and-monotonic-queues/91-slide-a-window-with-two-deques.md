<!-- lesson-kind: combination -->
<!-- lesson-id: slide-a-window-with-two-deques -->
## Slide A Window With Two Deques

<!-- stage: context -->
### Counting Steady Stretches In A Sensor Log

A monitoring job reads a sensor log and counts the stretches of consecutive readings that stay inside a band of width 2. A stretch of one reading counts, and so does every longer stretch whose largest and smallest readings differ by at most 2. The first version tests every stretch, and it finishes a log of a thousand readings in a blink. On a log of one hundred thousand readings it needs several billion tests.

The job needs a window that slides along the log and that knows its own largest and smallest reading at every moment. This lesson asks how a window can keep both extremes up to date while it grows on the right and shrinks on the left, and how one pass can then count every steady stretch.

<!-- stage: contributions -->
### What Each Earlier Idea Adds

Two earlier ideas combine in this lesson, and each supplies a different half. The sliding window lessons of Chapter 09 supply the moving boundaries. A window has a left end and a right end, the right end advances on every step, and the left end advances when a rule says the window is no longer acceptable. That chapter decides when the left end moves, and it relies on a quantity that a single running total can give.

The deque lessons of this chapter supply the extremes. A deque of positions with values in a fixed order reports the largest or the smallest value of the current window in constant time, and it forgets positions that left the window. Alone, the window has no cheap way to read its extremes, and alone, the deque has no rule for where the window starts. Together they answer the question that a running total cannot: how far apart are the largest and smallest values of the window right now?

<!-- stage: naive -->
### Extending Every Start Until The Band Breaks

The direct plan fixes each start position and extends the end while the band holds. It tracks the largest and smallest value of the stretch as the end moves, so each extension costs constant time.

```java
static long countByExtending(int[] a, int limit) {
    long count = 0;
    for (int start = 0; start < a.length; start++) {
        int hi = a[start], lo = a[start];
        for (int end = start; end < a.length; end++) {
            hi = Math.max(hi, a[end]);
            lo = Math.min(lo, a[end]);
            if (hi - lo > limit) break;      // a longer stretch from this start cannot be steady
            count++;                         // the stretch start..end is steady
        }
    }
    return count;
}
```

The method is correct. A log with every reading in the band makes the inner loop run to the end for every start.

<!-- stage: bottleneck -->
### Repeating Work For Neighboring Starts

```predict
The log is 2, 4, 3, then 7, and the band width is 2. The stretch 2, 4, 3 is steady. When 7 arrives, which readings must leave the window so that the window is steady again, and what does the window need to know to decide?

Every reading before 7 must leave, because 7 differs from 4 and from 3 by more than 2. To decide, the window needs its largest and smallest values after each removal, and a rescan of the window would cost time that grows with its length.
```

On a log where every reading fits the band, the method visits `n * (n + 1) / 2` stretches, which is O(n^2). Neighboring starts repeat almost all of the work, because the stretch from start `s + 1` is the stretch from start `s` with one reading removed. A rescan of the window to find its extremes repeats the same reads in a different place. The repeated work is the recomputation of extremes for windows that overlap almost completely.

<!-- stage: insight -->
### Letting Two Deques Drive One Window

#### Keeping Both Extremes Up To Date

The window keeps two deques of positions. One deque holds maximum candidates, with values that never increase from the front to the back. The other holds minimum candidates, with values that never decrease. Each new position enters both deques and removes the weaker positions from the back of each. The **spread** of the window is the front value of the first deque minus the front value of the second. It is the largest value minus the smallest value of the window.

#### Moving The Left Pointer

A **left pointer** marks the first position of the window, and it only moves forward. While the spread exceeds the limit, the left pointer moves forward by one position. Each deque then drops its front if that position lies behind the left pointer. The pointer stops as soon as the spread is within the limit, and a window of one reading always passes, because its spread is zero. Both removal rules remain in force: the front expiry depends on position, and the back domination depends on value.

#### Counting Every Steady Stretch

A subarray of a steady window is steady, because its largest value cannot be higher and its smallest value cannot be lower. When the right end stands at position `right`, every stretch that ends at `right` and starts at or after the left pointer is steady. That is `right - left + 1` stretches. The method adds that **count per end** at each step. The invariant is that, after the left pointer settles, the window holds the longest steady stretch that ends at `right`, and both deque fronts are its extremes. Every position enters each deque once and leaves it at most once, and the left pointer never moves backward, so the total cost is O(n).

<!-- names: spread, left pointer, count per end -->

<!-- stage: variables -->
### State Shared By Window And Deques

The method keeps six pieces of state.

- **Maximum deque** holds positions with non-increasing values, and its front is the window maximum.
- **Minimum deque** holds positions with non-decreasing values, and its front is the window minimum.
- **Left pointer** is the first position of the window, and it never decreases.
- **right** is the last position of the window, and it increases by one each step.
- **limit** is the largest spread the problem allows.
- **total** is the running count of steady stretches, held in a `long` because it can reach `n * (n + 1) / 2`.

The spread is computed from the two fronts at each check, and it is not stored.

<!-- stage: trace -->
### Tracing Fixed And Moving Windows

The first trace follows a fixed window of length 3 over `a = [6, 1, 4, 4, 2, 9, 3]`. Each step runs an expiry pass at the front and a domination pass at the back before it reads the front. The two equal values 4 at positions 2 and 3 both stay, because only strictly smaller values leave. The window reads `[6, 4, 4, 9, 9]`. The trace names both passes in every step, so a pass that removes nothing is visible.

The second trace follows `b = [2, 4, 3, 7, 5]` with a limit of 2. The first three readings form a steady window, and each step adds its count per end, which gives 1, then 2, then 3. The reading 7 breaks the band, and the left pointer moves forward until the window holds only 7. The reading 5 differs from 7 by 2, so the window keeps both. The total number of steady stretches is 9.

```trace
{"cells":[6,1,4,4,2,9,3],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Edge 0 brings 6. The expiry pass removes nothing. The domination pass removes nothing. The first window is not complete."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Edge 1 brings 1. The expiry pass removes nothing. The domination pass removes nothing. The first window is not complete."},{"at":{"right":2},"vars":{"deque":"[0,2]","output":"[6]"},"note":"Edge 2 brings 4. The expiry pass removes nothing. The domination pass removes index 1 from the back. The front is index 0, so the window reads 6."},{"at":{"right":3},"vars":{"deque":"[2,3]","output":"[6,4]"},"note":"Edge 3 brings 4. The expiry pass removes index 0 from the front. The domination pass removes nothing. The front is index 2, so the window reads 4."},{"at":{"right":4},"vars":{"deque":"[2,3,4]","output":"[6,4,4]"},"note":"Edge 4 brings 2. The expiry pass removes nothing. The domination pass removes nothing. The front is index 2, so the window reads 4."},{"at":{"right":5},"vars":{"deque":"[5]","output":"[6,4,4,9]"},"note":"Edge 5 brings 9. The expiry pass removes index 2 from the front. The domination pass removes index 4, 3 from the back. The front is index 5, so the window reads 9."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[6,4,4,9,9]"},"note":"Edge 6 brings 3. The expiry pass removes nothing. The domination pass removes nothing. The front is index 5, so the window reads 9."}]}
```

```trace
{"cells":[2,4,3,7,5],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"max_deque":"[0]","min_deque":"[0]","total":1},"note":"Edge 0 brings 2. The spread is within the limit. The window 0 to 0 adds 1 steady subarrays ending here, for a total of 1."},{"at":{"left":0,"right":1},"vars":{"max_deque":"[1]","min_deque":"[0,1]","total":3},"note":"Edge 1 brings 4. The spread is within the limit. The window 0 to 1 adds 2 steady subarrays ending here, for a total of 3."},{"at":{"left":0,"right":2},"vars":{"max_deque":"[1,2]","min_deque":"[0,2]","total":6},"note":"Edge 2 brings 3. The spread is within the limit. The window 0 to 2 adds 3 steady subarrays ending here, for a total of 6."},{"at":{"left":3,"right":3},"vars":{"max_deque":"[3]","min_deque":"[3]","total":7},"note":"Edge 3 brings 7. The spread exceeds 2, so the left pointer moves 3 step(s) to 3. The window 3 to 3 adds 1 steady subarrays ending here, for a total of 7."},{"at":{"left":3,"right":4},"vars":{"max_deque":"[3,4]","min_deque":"[4]","total":9},"note":"Edge 4 brings 5. The spread is within the limit. The window 3 to 4 adds 2 steady subarrays ending here, for a total of 9."}]}
```

<!-- stage: code -->
### Fixed Windows And Counted Stretches

```java
static int[] windowMaxima(int[] a, int k) {
    int[] out = new int[a.length - k + 1];
    Deque<Integer> d = new ArrayDeque<>();
    for (int right = 0; right < a.length; right++) {
        if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();      // expiry at the front
        while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.pollLast();    // domination at the back
        d.addLast(right);
        if (right >= k - 1) out[right - k + 1] = a[d.peekFirst()];
    }
    return out;
}

static long countSteady(int[] a, int limit) {
    Deque<Integer> hi = new ArrayDeque<>(), lo = new ArrayDeque<>();
    int left = 0;
    long total = 0;
    for (int right = 0; right < a.length; right++) {
        while (!hi.isEmpty() && a[hi.peekLast()] < a[right]) hi.pollLast();
        while (!lo.isEmpty() && a[lo.peekLast()] > a[right]) lo.pollLast();
        hi.addLast(right);
        lo.addLast(right);
        while (a[hi.peekFirst()] - a[lo.peekFirst()] > limit) {              // spread too large
            left++;
            if (hi.peekFirst() < left) hi.pollFirst();                       // expiry in both deques
            if (lo.peekFirst() < left) lo.pollFirst();
        }
        total += right - left + 1;                                           // count per end
    }
    return total;
}
```

The inner loop moves the left pointer by one step per pass, so each deque can lose at most one front per pass, and an `if` is enough. The exercises keep the values small, so the spread never overflows `int`. The counter `total` is a `long`, because a log of 100,000 readings can hold about five billion steady stretches.

- **Time** is O(n) for both methods, because every position enters each deque once and the left pointer never moves backward.
- **Space** is O(k) for the fixed window and O(n) in the worst case for the counted stretches.

<!-- stage: applicability -->
### Telling When Two Deques Are Needed

#### Applying The Invariant

Use two deques when a window must stay within a limit that depends on its largest and smallest values. The invariant is that both fronts are the extremes of the current window, and that the window is the longest valid stretch that ends at `right`. Use one deque when only one extreme matters, and use a running total when the rule depends on a sum.

#### Finding The False Friend

The false friend is a window whose validity does not improve when the left end moves forward. A sum with negative values is such a case, as the previous lesson showed, because removing a value can lower the sum. The spread is safe, because removing a value from a window never raises the largest value and never lowers the smallest value. The left pointer method needs that one-way property.

A second false friend is a heap with lazy removal. It reports both extremes, but it stores stale entries and costs O(n log n), and it makes the position bookkeeping harder than a deque does.

#### No-Go Conditions

Do not use the method when the window rule depends on a sum, a median or a count of distinct values. Those rules need other state. Do not use it when removing a value can turn a valid window into an invalid one. A graph search that prefers cheap edges uses a deque too, but it needs graph state that a later chapter teaches.

<!-- stage: exercises -->
### Exercises

#### [Build] Fixed-Window Maximum Trace (Author exercise)
<!-- id: dq-fixed-window-trace -->

**Prerequisites.** The window maximum and the age test from this chapter.

**Problem.** Run the fixed-window maximum method on an integer array `a` with a range length `k`. At each position `right`, remove from the front the positions that are at most `right - k`. Then remove from the back every position whose value is strictly smaller than `a[right]`, and append `right`. After the append, record the positions the deque holds from the front to the back. Return the list of recorded states, one per position.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 1,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Output** has `n` states, and each state is an `int[]` of positions.

**Example 1.** Input `a = [6, 1, 4, 4, 2]`, `k = 3`, output `[[0], [0, 1], [0, 2], [2, 3], [2, 3, 4]]`.

**Example 2.** Input `a = [3, 2, 1]`, `k = 1`, output `[[0], [1], [2]]`.

**Hint.** Compare the states at positions 2 and 3 of Example 1. Which pass removes position 0, and which pass removes position 1?

**Changed decision.** The task records the state after every step, so the two removal passes are visible one at a time.

#### [Vary] Smallest Sliding Window Maximum (LeetCode 239)
<!-- id: dq-smallest-window-max -->

**Prerequisites.** The fixed-window trace above. This exercise reuses the window maximum of LC 239 with a changed output contract.

**Problem.** For an integer array `a` and a range length `k`, consider every range of `k` consecutive values. Each range has a maximum value. Return the smallest of those maxima over all ranges.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Output** is one integer.

**Example 1.** Input `a = [8, 2, 7, 3, 5, 1]`, `k = 2`, output `5`.

**Example 2.** Input `a = [4, 4, 4]`, `k = 3`, output `4`.

**Hint.** The window maximum is read at every full range. What must the method keep besides the deque?

**Changed decision.** The deque answers each range, and a second variable keeps the smallest answer.

#### [Boundary] Longest Continuous Subarray With Absolute Difference Less Than Or Equal To Limit, Counted (LeetCode 1438)
<!-- id: dq-count-steady -->

**Prerequisites.** The two-deque window from this lesson. This exercise reuses the range limit of LC 1438 and counts stretches instead of finding the longest one.

**Problem.** Given an integer array `a` and a non-negative integer `limit`, count the non-empty contiguous subarrays whose largest value minus smallest value is at most `limit`. Subarrays at different positions count separately, even when their values are equal.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Limit** is an integer between 0 and 1,000,000.
- **Values** are integers between 0 and 1,000,000.
- **Output** is a `long`, because the count can reach `n * (n + 1) / 2`.

**Example 1.** Input `a = [1, 3, 2]`, `limit = 1`, output `4`.

**Example 2.** Input `a = [5, 5, 5]`, `limit = 0`, output `6`.

**Hint.** When the window ending at `right` is steady, how many steady subarrays end at `right`?

**Changed decision.** The answer adds a count at every step, so the left pointer must settle before each addition.

#### [Recognize] Shortest Subarray With Sum At Least K, With Its Start (LeetCode 862)
<!-- id: dq-shortest-with-start -->

**Prerequisites.** The shortest subarray method from the previous lesson. This exercise reuses LC 862 with a changed output contract.

**Problem.** The input is `nums`, an array of integers, and a target `k`. Find the shortest non-empty contiguous subarray whose sum is at least `k`. If several have the shortest length, choose the one with the smallest start. Return the array `[start, length]`, or `[-1, -1]` when no subarray qualifies.

**Constraints.** The limits are:
- **Length** is between 1 and 100,000.
- **Values** are integers between -100,000 and 100,000.
- **Target** `k` is an integer between 1 and 1,000,000,000.
- **Output** is an `int[]` of length 2.

**Example 1.** Input `nums = [2, -3, 4, 1, -2, 5]`, `k = 6`, output `[2, 4]`.

**Example 2.** Input `nums = [2, -2, 2]`, `k = 3`, output `[-1, -1]`.

**Hint.** The length is `b - start`, where `b` is the end prefix position. How does the start follow from the length at the moment a start is used up?

**Changed decision.** The deque method stays the same, and the output adds the start position.
