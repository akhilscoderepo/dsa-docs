<!-- lesson-kind: combination -->
<!-- lesson-id: deque-and-sliding-window -->
## Deque And Sliding Window

<!-- stage: context -->
### The Concert Hall Noise Monitor

A concert hall has a microphone that records the loudest sound in each minute. The safety officer asks two kinds of question. The first is a rolling one: at every minute, what is the loudest reading among the last five minutes, since a hearing warning is displayed while that figure is high. The second is a retrospective one: over the whole evening, how many stretches of consecutive minutes were calm, meaning that the loudest and the quietest reading inside the stretch differ by no more than a set tolerance.

The evening has thousands of readings, and the officer would like both answers from a single pass. Her assistant has already learned two separate tricks, one for keeping a moving stretch with an edge that only moves forward, and one for remembering only those readings that could still be the extreme. She suspects that the questions need both tricks working together, and that they will fail if one of them is applied without the other.

<!-- stage: contributions -->
### What Each Technique Brings

The sliding window brings chronology. It gives the moving stretch two edges that only move forward, so that every reading enters once and expires once, and it supplies the rule for when a reading is too old to count: a fixed length for the rolling question, or a left edge pushed forward until a condition holds for the retrospective one. By itself it knows nothing about which readings matter. Asking a window for its largest value sends it back to scanning the whole stretch.

The monotonic deque brings value order. It stores only the readings that could still be an extreme, so the front is the answer in constant time, and it drops a reading as soon as a newer and no-worse reading arrives. By itself it has no sense of age. A deque that ignores the stretch edges will hand back a record that was set an hour ago.

The recognition cue is a question about the extreme value of a stretch whose edge moves forward by rule. The extreme must be read at each step, so the state needs both an age check and a value order.

<!-- stage: naive -->
### Scan The Whole Stretch Every Time

The direct method checks every possible stretch, tracking the loudest and quietest readings as the stretch grows, and counts those within tolerance.

```java
static int calmStretchesByScan(int[] loud, int tolerance) {
    int count = 0;
    for (int start = 0; start < loud.length; start++) {
        int top = loud[start], bottom = loud[start];
        for (int end = start; end < loud.length; end++) {
            top = Math.max(top, loud[end]);
            bottom = Math.min(bottom, loud[end]);
            if (top - bottom > tolerance) break;
            count++;
        }
    }
    return count;
}
```

It is correct, and for `[2, 4, 3, 7, 5]` with a tolerance of 2 it returns 9. The `break` is safe, because a longer stretch from the same start can only have a wider spread.

<!-- stage: bottleneck -->
### Quadratic Scanning Of Stretches

The scan restarts from every start minute and runs until the spread is too wide, so on an evening of calm readings it examines about half of all pairs, which is O(n^2) work. For the rolling question the direct method rescans five readings per minute, which is cheap, but a rolling question over the last six hours of minute-by-minute readings costs 360 readings per minute, and the cost grows with the length of the stretch, O(n * k) for the whole evening.

Neighbouring starts overlap almost completely. Two consecutive starts examine the same readings except for one, yet the scan forgets everything it has learned in between. The left edge never needs to move backward, because a stretch that is already too wide for one start is too wide for every earlier start. What has to be recovered quickly is the pair of extremes after each change of edges, and a plain pair of running variables cannot do that, since the extreme that leaves the window is gone for good and the runner-up was never stored.

<!-- stage: insight -->
### Two Passes And One Joint Rule

The combined state is a window with edges, plus one deque per extreme that is needed, holding positions. The **joint invariant** says that every deque holds only positions inside the current window, in position order from front to back, with values ordered so that the front is the extreme of the window. Each step of the right edge keeps this invariant with two passes. The **expiry pass** removes from the front every position that has fallen out of the window, where the window is defined either by a fixed length or by a left pointer that has just moved. The **domination pass** removes from the back every position whose value is beaten by the newcomer, and then the newcomer is appended.

<!-- names: joint invariant, expiry pass, domination pass -->

For a fixed length the expiry pass uses the test `front <= right - k`. For a variable window the left pointer moves forward while the spread of the front values is too large, and after each step the expiry pass is applied to both deques with the test `front < left`. The two passes are independent decisions. Mixing them up is the usual source of error, since a position can be removed for being old or for being beaten, and only the first reason depends on the window.

The cost is linear in both forms, since every position is appended once to each deque and removed at most once, and the left pointer moves forward at most n times in total.

<!-- stage: variables -->
### Edges, Deques And What Is Counted

The right edge `right` runs over all positions. For a fixed window the left edge is implied by `right - k + 1`, and for a variable window `left` is a separate variable that never decreases. Each deque stores positions, and its comparison reads values through them. A count of calm stretches adds `right - left + 1` after the window has been made valid, since every start from `left` to `right` gives a calm stretch ending at `right`. The totals can exceed `int` for long inputs, so they are held in `long`.

<!-- stage: trace -->
### The Same Two Passes On Two Questions

Take the readings `6, 1, 4, 4, 2, 9, 3` with a window of 3. The 6 and the 1 are appended, and the 4 at edge 2 removes the 1 from the back, so the first window reads 6. At edge 3 the expiry pass removes index 0, since 3 minus 3 is 0, and the second 4 is appended without removing the first 4, which leaves two equal readings in the deque. The window reads 4. At edge 5 the front, index 2, has expired, and the 9 removes the second 4 and the 2 from the back, so the deque holds one index and the window reads 9.

A second run counts calm stretches on `2, 4, 3, 7, 5` with a tolerance of 2. Through edge 2 the spread never exceeds 2, so the stretches ending at each edge number 1, 2 and 3. At edge 3 the 7 makes the spread too wide, and the left pointer moves three steps, to index 3, expiring fronts as it passes them, so only one stretch ends at that edge. Edge 4 adds two more, for a total of 9.

```trace
{"cells":[6,1,4,4,2,9,3],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Edge 0 brings 6. The expiry pass removes nothing. The domination pass removes nothing. The first window is not complete."},{"at":{"right":1},"vars":{"deque":"[0,1]","output":"[]"},"note":"Edge 1 brings 1. The expiry pass removes nothing. The domination pass removes nothing. The first window is not complete."},{"at":{"right":2},"vars":{"deque":"[0,2]","output":"[6]"},"note":"Edge 2 brings 4. The expiry pass removes nothing. The domination pass removes index 1 from the back. The front is index 0, so the window reads 6."},{"at":{"right":3},"vars":{"deque":"[2,3]","output":"[6,4]"},"note":"Edge 3 brings 4. The expiry pass removes index 0 from the front. The domination pass removes nothing. The front is index 2, so the window reads 4."},{"at":{"right":4},"vars":{"deque":"[2,3,4]","output":"[6,4,4]"},"note":"Edge 4 brings 2. The expiry pass removes nothing. The domination pass removes nothing. The front is index 2, so the window reads 4."},{"at":{"right":5},"vars":{"deque":"[5]","output":"[6,4,4,9]"},"note":"Edge 5 brings 9. The expiry pass removes index 2 from the front. The domination pass removes index 4, 3 from the back. The front is index 5, so the window reads 9."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[6,4,4,9,9]"},"note":"Edge 6 brings 3. The expiry pass removes nothing. The domination pass removes nothing. The front is index 5, so the window reads 9."}]}
```

```trace
{"cells":[2,4,3,7,5],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"max_deque":"[0]","min_deque":"[0]","total":1},"note":"Edge 0 brings 2. The range is within the limit. The window 0 to 0 adds 1 calm subarrays ending here, for a total of 1."},{"at":{"left":0,"right":1},"vars":{"max_deque":"[1]","min_deque":"[0,1]","total":3},"note":"Edge 1 brings 4. The range is within the limit. The window 0 to 1 adds 2 calm subarrays ending here, for a total of 3."},{"at":{"left":0,"right":2},"vars":{"max_deque":"[1,2]","min_deque":"[0,2]","total":6},"note":"Edge 2 brings 3. The range is within the limit. The window 0 to 2 adds 3 calm subarrays ending here, for a total of 6."},{"at":{"left":3,"right":3},"vars":{"max_deque":"[3]","min_deque":"[3]","total":7},"note":"Edge 3 brings 7. The range exceeds 2, so the left pointer moves 3 step(s) to 3. The window 3 to 3 adds 1 calm subarrays ending here, for a total of 7."},{"at":{"left":3,"right":4},"vars":{"max_deque":"[3,4]","min_deque":"[4]","total":9},"note":"Edge 4 brings 5. The range is within the limit. The window 3 to 4 adds 2 calm subarrays ending here, for a total of 9."}]}
```

<!-- stage: code -->
### One Skeleton, Three Questions

```java
static long sumOfWindowMaxima(int[] a, int k) {
    long total = 0;
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    for (int right = 0; right < a.length; right++) {
        while (!deque.isEmpty() && deque.peekFirst() <= right - k) deque.removeFirst();
        while (!deque.isEmpty() && a[deque.peekLast()] < a[right]) deque.removeLast();
        deque.addLast(right);
        if (right >= k - 1) total += a[deque.peekFirst()];
    }
    return total;
}

static long countCalmSubarrays(int[] a, long limit) {
    java.util.ArrayDeque<Integer> high = new java.util.ArrayDeque<>();
    java.util.ArrayDeque<Integer> low = new java.util.ArrayDeque<>();
    long total = 0;
    int left = 0;
    for (int right = 0; right < a.length; right++) {
        while (!high.isEmpty() && a[high.peekLast()] < a[right]) high.removeLast();
        while (!low.isEmpty() && a[low.peekLast()] > a[right]) low.removeLast();
        high.addLast(right);
        low.addLast(right);
        while ((long) a[high.peekFirst()] - a[low.peekFirst()] > limit) {
            left++;
            if (high.peekFirst() < left) high.removeFirst();
            if (low.peekFirst() < left) low.removeFirst();
        }
        total += right - left + 1;
    }
    return total;
}

static int shortestWithinCap(int[] nums, long target, int cap) {
    long[] p = new long[nums.length + 1];
    for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    int best = Integer.MAX_VALUE;
    for (int b = 0; b < p.length; b++) {
        while (!deque.isEmpty() && b - deque.peekFirst() > cap) deque.removeFirst();
        while (!deque.isEmpty() && p[b] - p[deque.peekFirst()] >= target) best = Math.min(best, b - deque.removeFirst());
        while (!deque.isEmpty() && p[deque.peekLast()] >= p[b]) deque.removeLast();
        deque.addLast(b);
    }
    return best == Integer.MAX_VALUE ? -1 : best;
}
```

All three loops append each position once and remove it at most once, so they are linear. The third method has two reasons to remove from the front, age and success, and the age test is applied first.

<!-- stage: applicability -->
### Spotting The Pair Of Techniques

Reach for the pair when a question asks for an extreme value, or for a spread between two extremes, over a stretch whose edges move forward, and when the extreme must be available after every move. The joint invariant is that each deque holds in-window positions in position order, ordered by value so that the front is the extreme, and every step applies the expiry pass before reading the front. Fixed length, a left pointer driven by a condition, and a length cap on a prefix-sum start are three forms of the same state.

The false friend is a plain window with running variables for the maximum and minimum, which works while values only enter and fails once the extreme expires. A second false friend is a deque without the expiry pass, which returns a stale record. A third is a deque that is trimmed from the back but never from the front when the left pointer jumps by more than one, since several positions can expire in a single move.

Do not use it for medians, for sums that need every element, or for conditions that are not monotone in the window, since the left edge cannot move backward to repair a mistake. In Java, keep positions in `ArrayDeque<Integer>`, compare them with `<` and `<=` and never with `==`, and widen differences to `long` when values are large.

<!-- stage: exercises -->
### Exercises

#### [Build] Fixed-Window Maximum Trace (Author exercise)
<!-- id: dqw-fixed-window-trace -->

**Prerequisites.** The sliding maximum and index expiry lessons of this chapter.

**Problem.** Given an integer array `a` and a window length `k`, run the fixed-window deque with strict back removal and return, for every right edge, a pair `[frontRemovals, backRemovals]` giving how many positions the expiry pass and the domination pass removed at that edge.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [2, 5, 1, 1, 4]`, `k = 2`, output `[[0, 0], [0, 1], [0, 0], [1, 0], [1, 1]]`.

**Example 2.** Input `a = [3, 2, 1]`, `k = 3`, output `[[0, 0], [0, 0], [0, 0]]`.

**Hint.** Which pass runs first? Can both passes remove something at the same edge, and what does the second example show about a window that is never full before the end?

**Changed decision.** First rung: the two passes are kept apart and counted separately, so that expiry by age and removal by domination can be told apart.

#### [Vary] Sliding Window Maximum (LeetCode 239)
<!-- id: dqw-sum-of-maxima -->

**Prerequisites.** The Fixed-Window Maximum Trace exercise above.

**Problem.** Given an integer array `nums` and a window length `k`, return the sum of the maxima of all contiguous windows of length `k`, instead of the list of maxima.

**Constraints.** 1 <= k <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. The sum can exceed the range of `int`, so return a `long`.

**Example 1.** Input `nums = [4, 2, 12, 3, 8, 1]`, `k = 3`, output 44.

**Example 2.** Input `nums = [-5, -6]`, `k = 1`, output -11.

**Hint.** The deque is the same as before, so what replaces the output array? Where could the sum overflow?

**Changed decision.** The answer is one accumulated total in a `long`, not an array, so nothing is stored per window.

#### [Boundary] Count Of Calm Subarrays (LeetCode 1438)
<!-- id: dqw-count-calm-subarrays -->

**Prerequisites.** The two exercises above, and the sliding minimum lesson.

**Problem.** Given an integer array `nums` and an integer `limit`, return how many non-empty contiguous subarrays have a largest value minus smallest value of at most `limit`.

**Constraints.** 1 <= nums.length <= 10^5, -10^9 <= nums[i] <= 10^9 and 0 <= limit <= 2 * 10^9. The count can exceed the range of `int`, so return a `long`.

**Example 1.** Input `nums = [2, 4, 3, 7, 5]`, `limit = 2`, output 9.

**Example 2.** Input `nums = [5, 5, 5]`, `limit = 0`, output 6.

**Hint.** If the window ending at `right` starts at `left`, how many calm subarrays end at `right`? Why does the left pointer never need to move backward?

**Changed decision.** The answer is a count added at every edge, not a best length, and the left pointer can jump by several steps, so both deques must be expired at each step.

#### [Recognize] Shortest Subarray with Sum at Least K (LeetCode 862)
<!-- id: dqw-shortest-within-cap -->

**Prerequisites.** All three exercises above, and the shortest-subarray lesson of this chapter.

**Problem.** Given an integer array `nums`, a target `k` and a cap `m`, return the length of the shortest non-empty subarray whose sum is at least `k` and whose length is at most `m`. If there is none, return -1.

**Constraints.** 1 <= nums.length <= 10^5, -10^4 <= nums[i] <= 10^4, 1 <= k <= 10^9 and 1 <= m <= nums.length. Linear time.

**Example 1.** Input `nums = [4, -3, 2, -1, 5]`, `k = 7`, `m = 5`, output 5.

**Example 2.** Input `nums = [4, -3, 2, -1, 5]`, `k = 7`, `m = 4`, output -1.

**Hint.** Starts can now leave the front for two reasons. Which test is applied first, and does trimming dominated starts from the back still help under a cap?

**Changed decision.** A cap on the length makes the front expire by age as well as by success, so the deque of cut points follows the combined rule of this lesson.
