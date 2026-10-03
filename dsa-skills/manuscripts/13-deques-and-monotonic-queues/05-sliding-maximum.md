<!-- lesson-kind: standard -->
<!-- lesson-id: sliding-maximum -->
## Sliding Maximum

<!-- stage: context -->
### The Strongest Recent Gust

A mountain weather station records the wind speed once every ten minutes and posts a bulletin after every reading. The bulletin does not report the latest speed, but the strongest gust among the last four readings, which is the figure that matters for the cable car. Each new reading pushes the oldest of the four out of the bulletin's view, so a record gust stays on the board for exactly four readings and then falls off, even if nothing stronger has come since.

The station has years of readings. The clerk who prepares the bulletins is used to checking all four numbers each time, but a new station is planned with readings every minute and a bulletin covering the last six hours, and she suspects that her habit will no longer be fast enough. She would like to keep a short note on the side that is updated a little with every reading and tells her the answer at once.

<!-- stage: naive -->
### Look At Every Reading In The Frame

The direct method lists each frame of `k` consecutive readings and takes its maximum.

```java
static int[] strongestByScan(int[] speed, int k) {
    int n = speed.length;
    int[] bulletin = new int[n - k + 1];
    for (int start = 0; start + k <= n; start++) {
        int top = speed[start];
        for (int j = start + 1; j < start + k; j++) top = Math.max(top, speed[j]);
        bulletin[start] = top;
    }
    return bulletin;
}
```

It is correct. For the speeds `[5, 9, 2, 6, 4]` with `k = 3` it returns `[9, 9, 6]`.

<!-- stage: bottleneck -->
### Overlapping Frames Redo The Same Comparisons

Neighbouring frames share `k - 1` readings, yet each frame compares all `k` of them from scratch. With `n` readings the cost is about `n * k` comparisons, which is O(n * k), and it is close to quadratic when the frame is a large part of the record. The planned station, with a record of a million readings and a frame of 360, would make more than three hundred million comparisons in one pass over the record, and every doubling of the frame doubles the work.

The overlap suggests the cure. Between two bulletins, one reading leaves and one enters. A frame's maximum changes only if the departing reading was the maximum, or if the arriving reading is larger than the rest. A structure that keeps just the readings that could still become the maximum, and removes a reading when it is too old or when something later and stronger has arrived, would update by a small amount per step. A heap offers a way to do this, but it keeps stale entries until they reach the top and costs O(n log k) in total, and the previous lessons have already built something cheaper.

<!-- stage: insight -->
### Four Moves For Every Reading

The solution is the **window deque**: a deque of indices that are inside the current frame, in chronological order from front to back, whose values decrease from front to back. The front is therefore the index of the current maximum. Each new reading takes a **four-step turn**, in this order. First, expire: remove from the front every index that is at most `right - k`. Second, dominate: remove from the back every index whose value is strictly smaller than the new value. Third, append the new index at the back. Fourth, the **answer read**: once `right` has reached `k - 1` or more, the value at the front index is the maximum of the frame that ends at `right`.

<!-- names: window deque, four-step turn, answer read -->

Each of the four steps keeps the invariant that the deque holds exactly the indices that can still be the maximum of this or a future frame. Expiry removes candidates that have left the frame. Domination removes candidates that a later and at-least-as-large value will outlast. Appending adds the one new candidate, and the order of values makes the front the largest. The answer is read only after all three changes, since reading earlier could return an expired or dominated value.

The cost is O(n) time for the whole run, because each index is appended once and removed at most once, from either end. The memory is O(k), since the deque never holds more than the indices of one frame.

<!-- stage: variables -->
### Edge, Deque And Output Slot

The right edge `right` runs over every index, and it is the newest reading in the frame. The deque holds indices, never values, because the age test needs the index and the comparison reads `a[index]`. The output array has length `n - k + 1`, and the answer for the frame ending at `right` goes to slot `right - k + 1`, written only when `right >= k - 1`, since earlier frames are shorter than `k`. When `k` equals 1 every frame is a single reading and the deque holds one index. When `k` equals `n` there is exactly one answer, written at the last step.

<!-- stage: trace -->
### A Gust Record Falling Off The Board

Take the speeds `8, 3, 5, 9, 2, 7, 7, 1` with `k = 3`. The 8 and the 3 are appended, and the 5 removes the 3, so after right edge 2 the deque holds indices 0 and 2, and the first frame reads 8. At right edge 3 the age test removes index 0 from the front, since 3 minus 3 is 0, and the 9 removes the 5 from the back, leaving index 3 alone, so the frame reads 9. At right edge 4 the 2 is appended behind the 9, and the frame still reads 9. At right edge 5 the 7 removes the 2 and the frame reads 9, because index 3 is still inside the frame. At right edge 6 the age test finds that index 3 is expired, since 6 minus 3 is 3. The front is removed, and the deque, holding the first 7 at index 5, takes the second 7 behind it, so the frame reads 7.

A second run on the falling speeds `6, 5, 4, 3, 2, 1` stresses the other end. Nothing is ever removed from the back, and each frame loses its front by age, so the answers drop by one index per step. The step to study in the first run is right edge 6, where the record is removed by age and not by a larger value.

```trace
{"cells":[8,3,5,9,2,7,7,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 8. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Right edge 1 brings 3. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":2},"vars":{"deque":"[0,2]","output":"[8]"},"note":"Right edge 2 brings 5. The value 5 removes index 1 from the back. The front is index 0, so the frame ending here reads 8."},{"at":{"right":3},"vars":{"deque":"[3]","output":"[8,9]"},"note":"Right edge 3 brings 9. Index 0 is expired and leaves the front. The value 9 removes index 2 from the back. The front is index 3, so the frame ending here reads 9."},{"at":{"right":4},"vars":{"deque":"[3,4]","output":"[8,9,9]"},"note":"Right edge 4 brings 2. Nothing is removed. The front is index 3, so the frame ending here reads 9."},{"at":{"right":5},"vars":{"deque":"[3,5]","output":"[8,9,9,9]"},"note":"Right edge 5 brings 7. The value 7 removes index 4 from the back. The front is index 3, so the frame ending here reads 9."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[8,9,9,9,7]"},"note":"Right edge 6 brings 7. Index 3 is expired and leaves the front. The front is index 5, so the frame ending here reads 7."},{"at":{"right":7},"vars":{"deque":"[5,6,7]","output":"[8,9,9,9,7,7]"},"note":"Right edge 7 brings 1. Nothing is removed. The front is index 5, so the frame ending here reads 7."}]}
```

```trace
{"cells":[6,5,4,3,2,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 6. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Right edge 1 brings 5. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":2},"vars":{"deque":"[0,1,2]","output":"[6]"},"note":"Right edge 2 brings 4. Nothing is removed. The front is index 0, so the frame ending here reads 6."},{"at":{"right":3},"vars":{"deque":"[1,2,3]","output":"[6,5]"},"note":"Right edge 3 brings 3. Index 0 is expired and leaves the front. The front is index 1, so the frame ending here reads 5."},{"at":{"right":4},"vars":{"deque":"[2,3,4]","output":"[6,5,4]"},"note":"Right edge 4 brings 2. Index 1 is expired and leaves the front. The front is index 2, so the frame ending here reads 4."},{"at":{"right":5},"vars":{"deque":"[3,4,5]","output":"[6,5,4,3]"},"note":"Right edge 5 brings 1. Index 2 is expired and leaves the front. The front is index 3, so the frame ending here reads 3."}]}
```

<!-- stage: code -->
### Sliding Window Maximum

```java
static int[] slidingMaximum(int[] a, int k) {
    int n = a.length;
    int[] out = new int[n - k + 1];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    for (int right = 0; right < n; right++) {
        while (!deque.isEmpty() && deque.peekFirst() <= right - k) deque.removeFirst();   // expire
        while (!deque.isEmpty() && a[deque.peekLast()] < a[right]) deque.removeLast();    // dominate
        deque.addLast(right);                                                              // append
        if (right >= k - 1) out[right - k + 1] = a[deque.peekFirst()];                     // read
    }
    return out;
}
```

The loop body makes at most one append and amortized constant removals, so the method runs in O(n) time, and the deque holds at most `k` indices, so the working memory is O(k) in addition to the output. The two `while` conditions read the deque after the previous step changed it, which is why the order of the four moves matters. The array lookup `a[deque.peekLast()]` unboxes the stored `Integer` to an index, and the expiry test compares an unboxed index with an `int`.

<!-- stage: applicability -->
### When Every Frame Needs Its Extreme

Use the window deque when every contiguous frame of fixed length needs its maximum or minimum, and the answer has to be produced in linear total time. The invariant is that, after the first three moves of each turn, the deque contains in-frame indices in chronological order with non-increasing values, and its front is the maximum. Write the four moves in a fixed order and read the answer last.

The false friend is the heap. A `PriorityQueue` with lazy deletion also gives the maximum of a frame, but it keeps stale entries until they come to the top and costs a logarithm per operation, so a whole run is O(n log k) with more memory. Another false friend is a running maximum with the departing value subtracted, which fails because a maximum cannot be undone. A third is to store values and expire the front when it equals the departing reading. That can be made to work with equal values kept, but it fails with the replace-equals policy, and it throws away the positions that later problems need.

Do not use it when the frame has variable length and the question is not an extreme, or when the quantity is a sum or a count, where a simple running total is enough. Do not use it for a median, which needs two heaps or a balanced tree. In Java, keep the output length at `n - k + 1`, and make sure `k` is between 1 and `n` before allocating it.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Of One Moving Window (Author exercise)
<!-- id: dq-maximum-one-window -->

**Prerequisites.** The expiry and domination lessons of this chapter.

**Problem.** Given an integer array `a` and a window length `k`, process every index with the four-step turn, and return only the maximum of the last window, the one that covers indices `n - k` through `n - 1`.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time and O(k) memory.

**Example 1.** Input `a = [9, 4, 7, 1, 6, 3, 5]`, `k = 4`, output 6.

**Example 2.** Input `a = [2]`, `k = 1`, output 2.

**Hint.** In which order do you expire, dominate and append? At which step is the front read?

**Changed decision.** First rung: all four moves in one fixed order, with the front read at the end, for a single window.

#### [Vary] Return Maximum Indices (Author exercise)
<!-- id: dq-return-maximum-indices -->

**Prerequisites.** The Maximum Of One Moving Window exercise above.

**Problem.** Given `a` and `k`, return for every window of length `k` the index of the maximum, and if the maximum value occurs several times in the window, return the smallest such index.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [3, 5, 5, 2, 5]`, `k = 3`, output `[1, 1, 2]`.

**Example 2.** Input `a = [7, 7, 7]`, `k = 2`, output `[0, 1]`.

**Hint.** Which policy for equal values leaves the earliest equal maximum at the front? What does the front hold, a value or an index?

**Changed decision.** The answer is a position and not a value, and the equal-value policy now decides which of several positions is reported.

#### [Boundary] Increasing, Decreasing, And Equal Arrays (Author exercise)
<!-- id: dq-increasing-decreasing-equal -->

**Prerequisites.** The two exercises above.

**Problem.** Run the window deque over `a` with window length `k`, with equal values kept. Return `[peak, backRemovals, frontRemovals]`: the largest size the deque reaches, the total number of removals from the back, and the total number of removals from the front.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9.

**Example 1.** Input `a = [2, 2, 2, 2, 2]`, `k = 3`, output `[3, 0, 2]`.

**Example 2.** Input `a = [5, 4, 3, 2, 1]`, `k = 3`, output `[3, 0, 2]`, and for the increasing array `[1, 2, 3, 4, 5]` the same window gives `[1, 4, 0]`.

**Hint.** Which shape fills the deque to its limit, and which shape empties it at every step? Which end does each of them stress?

**Changed decision.** The three shapes of input exercise opposite ends of the deque, so the counts of removals from each end are reported, and not only the maxima.

#### [Recognize] Sliding Window Maximum (LeetCode 239)
<!-- id: dq-sliding-window-maximum -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums` and a window length `k`, return an array that holds the maximum of every contiguous window of length `k`, from left to right.

**Constraints.** 1 <= k <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4. Aim for O(n) time and O(k) extra memory.

**Example 1.** Input `nums = [8, 3, 5, 9, 2, 7, 7, 1]`, `k = 3`, output `[8, 9, 9, 9, 7, 7]`.

**Example 2.** Input `nums = [1, 5, 2]`, `k = 3`, output `[5]`, since there is a single window.

**Hint.** Which two ends do the first two moves of each turn use? Why would a heap be slower here?

**Changed decision.** All four moves are combined and every window is reported, and the cost bound is the one that matters.
