<!-- lesson-kind: standard -->
<!-- lesson-id: sliding-maximum -->
## Find The Maximum Of Every Window

<!-- stage: context -->
### A Level Meter That Falls Behind

An audio tool draws a level meter. For every position in the recording, the meter shows the loudest sample among the last `k` samples. Each position shifts the range by one sample, so neighboring ranges share all but one sample. The first version of the tool handles a short clip well. On a ten-minute recording the meter lags behind the sound, because the cost of one position grows with the amount of audio already seen.

This lesson combines the two earlier removals into one method. Which three steps run for each new sample, in which order, and why does the answer sit at the front of the deque when they finish?

<!-- stage: naive -->
### Keeping Every Entry In A Priority Queue

A priority queue returns the entry with the highest priority at its top, and each push or pop costs O(log s) for a queue of size `s`. The direct plan pushes every sample with its position. It reads the top for the answer, and it pops the top while the top lies outside the range.

```java
static int[] maxWithQueue(int[] a, int k) {
    PriorityQueue<int[]> queue = new PriorityQueue<>((p, q) -> Integer.compare(q[0], p[0]));
    int[] out = new int[a.length - k + 1];
    for (int right = 0; right < a.length; right++) {
        queue.add(new int[]{a[right], right});                  // push value and position
        while (queue.peek()[1] <= right - k) queue.poll();      // drop a top entry that left the range
        if (right >= k - 1) out[right - k + 1] = queue.peek()[0];
    }
    return out;
}
```

The method is correct. An entry that left the range but sits below the top stays in the queue until it reaches the top.

<!-- stage: bottleneck -->
### Counting What The Queue Keeps

```predict
The samples increase: 1, 2, 3, ..., n, and the range length is 3. How many entries does the queue hold after the last sample, and what does the last push cost?

It holds all n entries, because the newest entry is always the top and no old entry ever reaches the top. The last push costs about log n steps.
```

The queue discards an entry only when that entry reaches the top. On the increasing stream, the top is always the newest entry, so every older entry stays forever. The queue grows to size `n`, each push costs O(log n), and the total cost is O(n log n). The entries below the top have lost already, because each of them is older and smaller than the entry above it. The repeated work is that the queue keeps and sorts entries that can never be an answer.

<!-- stage: insight -->
### Running Three Steps In A Fixed Order

#### Holding Only The Positions That Can Win

The method keeps a **window deque**, which is a deque of positions from the current range. The positions increase from the front to the back, and their values never increase. By the earlier lessons, an entry that a newer, larger entry dominates is already gone, and an entry that is too old is already gone. The front is the maximum of the range.

#### Fixing The Update Order

Every new sample runs the same steps in the same **update order**. First, the age test removes front positions that are at most `right - k`. Second, the back removes positions whose values are strictly smaller than the new value. Third, the new position is appended. The answer is read after the third step. It is read only when `right` is at least `k - 1`, because earlier positions do not yet form a full range.

The answer is read last because the third step can change the front. When the new value empties the deque, the new position becomes the front. A read before the append would return a position that was just removed.

#### Reading Why It Stays Linear

A **stale entry** is an entry that stays stored after it can no longer be an answer. The window deque holds none, because both removal rules run on every sample. Each position enters one time and leaves at most one time, so the total cost is O(n). The deque never holds more than `k` positions. The invariant is that before each read the deque holds exactly the positions in the range that no later position in the range dominates.

<!-- names: window deque, update order, stale entry -->

<!-- stage: variables -->
### State Kept Between Samples

The method keeps five pieces of state.

- **Window deque** holds positions in increasing order, with non-increasing values.
- **right** is the position of the newest sample, and it increases by one each step.
- **k** is the range length, and it is fixed for the whole run.
- **Front** is the position of the maximum, and the method reads it after the append.
- **Output** has `n - k + 1` entries, and the method writes one entry per full range.

The output index is `right - k + 1`, so the first answer is written at `right = k - 1`.

<!-- stage: trace -->
### Reading The Front After Each Update

The first trace follows `a = [8, 3, 5, 9, 2, 7, 7, 1]` with `k = 3`. The first two samples fill the deque but give no answer, because the range is not complete. At position 2 the first range is complete, and the front reads 8. The value 9 at position 3 removes position 2 and position 1 from the back, and it expires position 0 from the front, so the deque holds only position 3. The second 7 at position 6 does not remove the first 7, since equal values stay, and the front is still the older 7 for that read. The output is `[8, 9, 9, 9, 7, 7]`.

The second trace follows the decreasing array `[6, 5, 4, 3, 2, 1]`. The back never removes anything, because no new value beats the value before it. Only the age test works, and it removes the front once per step after the range fills. The deque keeps `k` positions, which is the largest size it can reach.

```trace
{"cells":[8,3,5,9,2,7,7,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 8. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Right edge 1 brings 3. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":2},"vars":{"deque":"[0,2]","output":"[8]"},"note":"Right edge 2 brings 5. The value 5 removes index 1 from the back. The front is index 0, so the frame ending here reads 8."},{"at":{"right":3},"vars":{"deque":"[3]","output":"[8,9]"},"note":"Right edge 3 brings 9. Index 0 is expired and leaves the front. The value 9 removes index 2 from the back. The front is index 3, so the frame ending here reads 9."},{"at":{"right":4},"vars":{"deque":"[3,4]","output":"[8,9,9]"},"note":"Right edge 4 brings 2. Nothing is removed. The front is index 3, so the frame ending here reads 9."},{"at":{"right":5},"vars":{"deque":"[3,5]","output":"[8,9,9,9]"},"note":"Right edge 5 brings 7. The value 7 removes index 4 from the back. The front is index 3, so the frame ending here reads 9."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[8,9,9,9,7]"},"note":"Right edge 6 brings 7. Index 3 is expired and leaves the front. The front is index 5, so the frame ending here reads 7."},{"at":{"right":7},"vars":{"deque":"[5,6,7]","output":"[8,9,9,9,7,7]"},"note":"Right edge 7 brings 1. Nothing is removed. The front is index 5, so the frame ending here reads 7."}]}
```

```trace
{"cells":[6,5,4,3,2,1],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 6. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Right edge 1 brings 5. Nothing is removed. The first frame is not complete yet, so nothing is read."},{"at":{"right":2},"vars":{"deque":"[0,1,2]","output":"[6]"},"note":"Right edge 2 brings 4. Nothing is removed. The front is index 0, so the frame ending here reads 6."},{"at":{"right":3},"vars":{"deque":"[1,2,3]","output":"[6,5]"},"note":"Right edge 3 brings 3. Index 0 is expired and leaves the front. The front is index 1, so the frame ending here reads 5."},{"at":{"right":4},"vars":{"deque":"[2,3,4]","output":"[6,5,4]"},"note":"Right edge 4 brings 2. Index 1 is expired and leaves the front. The front is index 2, so the frame ending here reads 4."},{"at":{"right":5},"vars":{"deque":"[3,4,5]","output":"[6,5,4,3]"},"note":"Right edge 5 brings 1. Index 2 is expired and leaves the front. The front is index 3, so the frame ending here reads 3."}]}
```

<!-- stage: code -->
### The Complete Method

```java
static int[] maxOfWindows(int[] a, int k) {
    int[] out = new int[a.length - k + 1];
    Deque<Integer> d = new ArrayDeque<>();                     // positions, values non-increasing
    for (int right = 0; right < a.length; right++) {
        if (!d.isEmpty() && d.peekFirst() <= right - k) {      // step 1: age test on the front
            d.pollFirst();
        }
        while (!d.isEmpty() && a[d.peekLast()] < a[right]) {   // step 2: remove weaker values
            d.pollLast();
        }
        d.addLast(right);                                      // step 3: append the new position
        if (right >= k - 1) {
            out[right - k + 1] = a[d.peekFirst()];             // read last: the front is the maximum
        }
    }
    return out;
}
```

The age test uses `if` here because each step expires at most one position for a fixed range length. The deque holds consecutive appends, so only position `right - k` can be at the front and expired. The method needs `1 <= k <= a.length`, which the exercises state as a limit.

- **Time** is O(n), because every position takes one append and at most one removal.
- **Space** is O(k) for the deque plus the output of n - k + 1 entries.

<!-- stage: applicability -->
### Choosing This Method

#### Applying The Invariant

Use the method when every range has a fixed length, shifts by one position and asks for the maximum. The invariant is that the deque holds the in-range positions that no later in-range position dominates, in order of position. If the method keeps the invariant, the front is the answer.

#### Finding The False Friend

The false friend is a running sum or an average over each range. A sum changes by one added value and one removed value, so a plain running total gives it in O(1) and no deque is needed. A deque answers order questions, and a sum is not one.

A priority queue also solves the maximum problem. It costs O(n log n) here, and it needs lazy removal of old entries, as the naive stage showed. It is still the right tool when the range has no fixed length, or when entries leave in an order that does not follow their positions.

#### No-Go Conditions

Do not use the method for the second largest value, a median or a count. The deque has discarded the entries those queries need. Do not use it when the range can shrink from the right as well as grow, because a position removed from the back cannot return.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Of One Moving Window (Author exercise)
<!-- id: dq-one-window -->

**Prerequisites.** Weaker-value removal and the age test from the previous two lessons; this lesson.

**Problem.** An integer array `a` has `n` values, and `k` is a range length. Process the positions `0` through `n - 1` in order. For each position, run three steps with a deque of positions. The first step removes the front while it is at most `right - k`. The second step removes from the back every position whose value is strictly smaller than the new value. The third step appends the new position. After the last position, return the value at the front.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Output** is one integer, the maximum of the last `k` values.

**Example 1.** Input `a = [8, 3, 5, 9, 2, 7]`, `k = 3`, output `9`.

**Example 2.** Input `a = [4, 6]`, `k = 1`, output `6`.

**Hint.** The answer is read once, after the last append. Which three steps run before the read, and in which order?

**Changed decision.** First exercise of the lesson: the three steps run in a fixed order and the read comes last.

#### [Vary] Return Maximum Indices (Author exercise)
<!-- id: dq-max-indices -->

**Prerequisites.** The one-window exercise above.

**Problem.** For an array `a` and a range length `k`, return one position for each range of `k` consecutive values. The position for a range is the smallest position that holds the maximum value of that range. The result has `n - k + 1` entries, ordered by the range start.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** return the smallest position among equal maxima.

**Example 1.** Input `a = [2, 9, 4, 4, 1, 6]`, `k = 2`, output `[1, 1, 2, 3, 5]`.

**Example 2.** Input `a = [7, 7, 7]`, `k = 2`, output `[0, 1]`.

**Hint.** The deque already stores positions. Which stored position is the smallest among equal maxima when equal values stay?

**Changed decision.** The output switches from values to positions, which is why the deque stores positions.

#### [Boundary] Increasing, Decreasing, And Equal Arrays (Author exercise)
<!-- id: dq-three-shapes -->

**Prerequisites.** The vary exercise above.

**Problem.** Run the three-step update on an array `a` with a range length `k`. Count each position that leaves from the back, and count each position that leaves from the front. Return the array `[back, front]` with the two totals for the whole run. A position is removed at most once.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -1,000,000 and 1,000,000.
- **Ties** stay in the deque, so equal values never leave from the back.

**Example 1.** Input `a = [1, 2, 3, 4]`, `k = 2`, output `[3, 0]`.

**Example 2.** Input `a = [4, 3, 2, 1]`, `k = 2`, output `[0, 2]`.

**Hint.** Rising values empty the back at every step. In which array does the front do all of the removing?

**Changed decision.** The task counts removals at each end, so it shows which end each array shape stresses.

#### [Recognize] LC 239 Sliding Window Maximum (LeetCode 239)
<!-- id: dq-lc239 -->

**Prerequisites.** All earlier exercises in this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, consider every range of `k` consecutive values, ordered by its first position. Return the array that holds the maximum value of each range, in the same order.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Range length** `k` is between 1 and `n`.
- **Values** are integers between -10,000 and 10,000.
- **Output** has `n - k + 1` entries.

**Example 1.** Input `nums = [2, 9, 4, 4, 1, 6]`, `k = 2`, output `[9, 9, 4, 4, 6]`.

**Example 2.** Input `nums = [5, 1, 1, 1, 3]`, `k = 3`, output `[5, 1, 3]`.

**Hint.** An old maximum that is no longer in range must leave from the front. Which end removes a value that a newer, larger value beats?

**Changed decision.** The same state now serves a full problem, with the read after the append.
