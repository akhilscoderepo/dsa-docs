<!-- lesson-kind: standard -->
<!-- lesson-id: sliding-minimum -->
## Sliding Minimum

<!-- stage: context -->
### The Coldest Night For The Greenhouse

A market gardener keeps a greenhouse of delicate seedlings, and every morning she records the lowest temperature of the night. Her rule is simple: if the coldest night among the last five recorded nights was below a threshold, the seedlings stay indoors. She reads this figure at the start of each day from a small notebook, and a cold night counts for exactly five days and then stops counting, even if the following nights have been mild.

Last winter she borrowed a trick from a friend who tracks the hottest day of the last five. The friend keeps a short list of hot days and crosses off the ones that are beaten. The gardener tries to copy it, and her first attempt keeps crossing off cold nights when a warmer one arrives, which makes the notebook say that the weather has been mild just when a frost has only just passed. Something in the friend's trick has to be turned around.

<!-- stage: naive -->
### Scan The Last Five Nights Again

The direct method reads all `k` temperatures of each frame and keeps the lowest.

```java
static int[] coldestByScan(int[] night, int k) {
    int n = night.length;
    int[] coldest = new int[n - k + 1];
    for (int start = 0; start + k <= n; start++) {
        int low = night[start];
        for (int j = start + 1; j < start + k; j++) low = Math.min(low, night[j]);
        coldest[start] = low;
    }
    return coldest;
}
```

It is correct. For the temperatures `[4, 1, 3, 5, 2]` with `k = 3` it returns `[1, 1, 2]`.

<!-- stage: bottleneck -->
### Copied Code Answers The Wrong Question

The scan has the familiar cost: `n` frames of `k` comparisons give O(n * k) time. The more instructive failure is the gardener's attempt to speed it up by copying the maximum deque unchanged. That version removes from the back every smaller entry and keeps the largest at the front, so it faithfully reports the warmest night of the frame. For `[4, 1, 3, 5, 2]` it returns `[4, 5, 5]`, which is a perfectly good answer to a question nobody asked. The code compiles, runs, and gives plausible numbers, so nothing alerts the programmer.

The remedy is not a new idea but a careful mirror image. Every comparison that decided who is dominated must be flipped, and the part of the logic that has nothing to do with order, which is the expiry of old indices, must stay exactly as it was. Afterwards, since the same mirror works on a second deque, one pass can keep both the highest and the lowest reading of a frame and answer questions about their difference.

<!-- stage: insight -->
### Mirror The Comparison, Keep The Expiry

An **increasing deque** keeps indices whose values increase from front to back. A new value removes from the back every entry that is strictly larger than itself, because an older larger value will leave first and can never be the minimum again. The front is then the smallest value in the frame. Expiry from the front is unchanged: remove indices that are at most `right - k`. The **mirrored comparison** is the only difference from the maximum version, and it has to be applied to every place where values are compared, which in the simple method is exactly one place.

The mirror image extends to **paired deques**. Keep one deque for the maximum and one for the minimum, both over the same indices and both expired by the same rule. After each arrival, the range of the frame is `a[maxDeque.peekFirst()] - a[minDeque.peekFirst()]`. Each deque costs O(n) in total, so the pair does too. For a frame of variable length the same pair works with a left pointer in place of `k`: expire both fronts when the left pointer passes them, and move the left pointer when the range becomes too large.

<!-- names: increasing deque, mirrored comparison, paired deques -->

Equal minima need the same care as equal maxima. If equal values are kept, the later of two equal minima stays in the deque after the earlier one expires, and the front still gives the correct minimum. The cost of the whole method is O(n) time and O(k) memory for a fixed frame, and O(n) memory in the worst case for the variable frame.

<!-- stage: variables -->
### Two Deques, One Edge, One Bound

The right edge `right` is the newest index. For a fixed frame the legal bound is `right - k + 1`, and for a variable frame it is a left pointer `left` that only moves forward. The maximum deque holds indices with non-increasing values and the minimum deque holds indices with non-decreasing values. They are separate, since an index that is dominated for maxima may be essential for minima, and the same index can be in both. The frame range is `a[maxFront] - a[minFront]`, and it is meaningful only when both deques are non-empty, which they are as soon as an index has been appended. Subtraction of two `int` values can overflow when values are near the limits of `int`, so use `long` when the contract allows large values.

<!-- stage: trace -->
### The Coldest Night And The Range

Take the temperatures `7, 4, 5, 2, 9, 4, 6` with `k = 3` and an increasing deque. The 7 and the 4 arrive, and the 4 removes the 7. The 5 is appended behind the 4, and the first frame reads 4. The 2 removes the 5 and the 4, so the deque holds only index 3, and the frame reads 2. The 9 is appended. At right edge 5 the 4 removes the 9 from the back, and the front, index 3 holding the 2, is still legal. At right edge 6 index 3 is expired, since 6 minus 3 is 3, and the 4 at index 5 becomes the front, so the frame reads 4. The step to study is right edge 6, where the expired record minimum is replaced by the next survivor.

A second run uses paired deques on `5, 8, 6, 7, 2, 9, 4` with a range limit of 3 and a left pointer. The window grows to the first four values, where the range is 3 and the best length becomes 4. The 2 then arrives and the range jumps to 6, so the left pointer advances one step at a time, and fronts expire as it passes them, until it reaches index 4 and the window holds only the 2. The 9 forces the pointer to index 5, and the 4 forces it to index 6, because each newcomer sits more than 3 away from the survivor before it. The best length stays at 4.

```trace
{"cells":[7,4,5,2,9,4,6],"pointers":["right"],"steps":[{"at":{"right":0},"vars":{"deque":"[0]","output":"[]"},"note":"Right edge 0 brings 7. Nothing is removed. The first frame is not complete yet."},{"at":{"right":1},"vars":{"deque":"[1]","output":"[]"},"note":"Right edge 1 brings 4. The value 4 removes index 0 from the back because it is smaller. The first frame is not complete yet."},{"at":{"right":2},"vars":{"deque":"[1,2]","output":"[4]"},"note":"Right edge 2 brings 5. Nothing is removed. The front is index 1, so the frame reads 4."},{"at":{"right":3},"vars":{"deque":"[3]","output":"[4,2]"},"note":"Right edge 3 brings 2. The value 2 removes index 2, 1 from the back because it is smaller. The front is index 3, so the frame reads 2."},{"at":{"right":4},"vars":{"deque":"[3,4]","output":"[4,2,2]"},"note":"Right edge 4 brings 9. Nothing is removed. The front is index 3, so the frame reads 2."},{"at":{"right":5},"vars":{"deque":"[3,5]","output":"[4,2,2,2]"},"note":"Right edge 5 brings 4. The value 4 removes index 4 from the back because it is smaller. The front is index 3, so the frame reads 2."},{"at":{"right":6},"vars":{"deque":"[5,6]","output":"[4,2,2,2,4]"},"note":"Right edge 6 brings 6. Index 3 is expired and leaves the front. The front is index 5, so the frame reads 4."}]}
```

```trace
{"cells":[5,8,6,7,2,9,4],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"max_deque":"[0]","min_deque":"[0]","range":0,"best":1},"note":"Index 0 (value 5) joins both deques. The range is within the limit, so the left pointer stays. The window covers indices 0 to 0 with range 0, and the best length is 1."},{"at":{"left":0,"right":1},"vars":{"max_deque":"[1]","min_deque":"[0,1]","range":3,"best":2},"note":"Index 1 (value 8) joins both deques. The range is within the limit, so the left pointer stays. The window covers indices 0 to 1 with range 3, and the best length is 2."},{"at":{"left":0,"right":2},"vars":{"max_deque":"[1,2]","min_deque":"[0,2]","range":3,"best":3},"note":"Index 2 (value 6) joins both deques. The range is within the limit, so the left pointer stays. The window covers indices 0 to 2 with range 3, and the best length is 3."},{"at":{"left":0,"right":3},"vars":{"max_deque":"[1,3]","min_deque":"[0,2,3]","range":3,"best":4},"note":"Index 3 (value 7) joins both deques. The range is within the limit, so the left pointer stays. The window covers indices 0 to 3 with range 3, and the best length is 4."},{"at":{"left":4,"right":4},"vars":{"max_deque":"[4]","min_deque":"[4]","range":0,"best":4},"note":"Index 4 (value 2) joins both deques. The range was above 3, so the left pointer moves forward 4 step(s) to 4, expiring fronts that fall behind it. The window covers indices 4 to 4 with range 0, and the best length is 4."},{"at":{"left":5,"right":5},"vars":{"max_deque":"[5]","min_deque":"[5]","range":0,"best":4},"note":"Index 5 (value 9) joins both deques. The range was above 3, so the left pointer moves forward 1 step(s) to 5, expiring fronts that fall behind it. The window covers indices 5 to 5 with range 0, and the best length is 4."},{"at":{"left":6,"right":6},"vars":{"max_deque":"[6]","min_deque":"[6]","range":0,"best":4},"note":"Index 6 (value 4) joins both deques. The range was above 3, so the left pointer moves forward 1 step(s) to 6, expiring fronts that fall behind it. The window covers indices 6 to 6 with range 0, and the best length is 4."}]}
```

<!-- stage: code -->
### Minimum And Range In One Pass

```java
static int[] slidingMinimum(int[] a, int k) {
    int[] out = new int[a.length - k + 1];
    java.util.ArrayDeque<Integer> deque = new java.util.ArrayDeque<>();
    for (int right = 0; right < a.length; right++) {
        while (!deque.isEmpty() && deque.peekFirst() <= right - k) deque.removeFirst();
        while (!deque.isEmpty() && a[deque.peekLast()] > a[right]) deque.removeLast();   // mirrored
        deque.addLast(right);
        if (right >= k - 1) out[right - k + 1] = a[deque.peekFirst()];
    }
    return out;
}

static long[] windowRanges(int[] a, int k) {
    long[] out = new long[a.length - k + 1];
    java.util.ArrayDeque<Integer> high = new java.util.ArrayDeque<>();
    java.util.ArrayDeque<Integer> low = new java.util.ArrayDeque<>();
    for (int right = 0; right < a.length; right++) {
        while (!high.isEmpty() && high.peekFirst() <= right - k) high.removeFirst();
        while (!low.isEmpty() && low.peekFirst() <= right - k) low.removeFirst();
        while (!high.isEmpty() && a[high.peekLast()] < a[right]) high.removeLast();
        while (!low.isEmpty() && a[low.peekLast()] > a[right]) low.removeLast();
        high.addLast(right);
        low.addLast(right);
        if (right >= k - 1) out[right - k + 1] = (long) a[high.peekFirst()] - a[low.peekFirst()];
    }
    return out;
}
```

Each index is appended once and removed at most once from each deque, so both methods take O(n) time, with O(k) extra memory beyond the output. The only line that differs between the maximum and the minimum is the one comparison in the second loop. In `windowRanges` the subtraction is widened to `long` before it is made, so that values near the ends of the `int` range cannot wrap.

<!-- stage: applicability -->
### When The Lowest Matters Or The Spread

Use the increasing deque when each frame needs its minimum, and use a pair of deques when the answer depends on both extremes, such as their difference or whether it stays under a limit. The invariant is that each deque holds in-frame indices in chronological order, with values ordered so that its front is the extreme, and expiry is applied to both fronts by the same rule. Treat the comparison and the expiry as two separate decisions when copying code.

The false friend is the copied maximum code. A program that reuses the maximum deque unchanged returns the maximum and looks entirely healthy, so a test on a hand-made case with an obvious minimum is the only defence. A second false friend is a single deque that tries to track both extremes, since the order that suits the maximum is the opposite of the one that suits the minimum. A third is a sorted structure holding the whole frame, which would give both extremes but costs a logarithm per update.

Do not use the pair when the question is about the median, or when the range must be read for frames that can shrink from the right as well as from the left, since the dominated entries that were discarded may be needed again. In Java, mind the type of the difference: subtracting `int` values near `Integer.MAX_VALUE` and `Integer.MIN_VALUE` overflows, and `long` fixes it.

<!-- stage: exercises -->
### Exercises

#### [Build] Minimum Of Every K-Window (Author exercise)
<!-- id: dq-minimum-every-window -->

**Prerequisites.** The sliding maximum lesson of this chapter.

**Problem.** Given an integer array `a` and a window length `k`, return an array holding the minimum of every contiguous window of length `k`, from left to right.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [7, 4, 5, 2, 9, 4, 6]`, `k = 3`, output `[4, 2, 2, 2, 4]`.

**Example 2.** Input `a = [4, 3, 2, 1]`, `k = 2`, output `[3, 2, 1]`.

**Hint.** Which comparison from the maximum version has to change, and which one must not? What would the unchanged maximum code return for the first example?

**Changed decision.** First rung: the comparison in the back loop is flipped, and the expiry from the front stays exactly the same.

#### [Vary] Window Range (Author exercise)
<!-- id: dq-window-range -->

**Prerequisites.** The Minimum Of Every K-Window exercise above.

**Problem.** Given an integer array `a` and a window length `k`, return for every window the difference between its largest and its smallest value.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9, so the difference can exceed the range of `int`; return `long` values.

**Example 1.** Input `a = [8, 2, 4, 7, 5, 3]`, `k = 3`, output `[6, 5, 3, 4]`.

**Example 2.** Input `a = [5, 5, 5]`, `k = 2`, output `[0, 0]`.

**Hint.** How many deques are needed, and do they share the expiry rule? Where must the subtraction be widened?

**Changed decision.** Two deques over the same indices are kept, one per extreme, and the answer is a difference read from both fronts.

#### [Boundary] Duplicate Minima Expire (Author exercise)
<!-- id: dq-duplicate-minima-expire -->

**Prerequisites.** The two exercises above.

**Problem.** For every window of length `k`, report two numbers: the minimum value, and how many positions in the window hold that minimum. Equal values are kept in the increasing deque.

**Constraints.** 1 <= k <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9.

**Example 1.** Input `a = [3, 1, 1, 4, 1, 6]`, `k = 3`, output `[[1, 2], [1, 2], [1, 2], [1, 1]]`.

**Example 2.** Input `a = [5, 5, 5]`, `k = 2`, output `[[5, 2], [5, 2]]`.

**Hint.** Where do all the positions holding the minimum sit in the deque? What happens to the count when the earliest of them expires?

**Changed decision.** Equal values are kept on purpose, so a later equal minimum is still there after an earlier one leaves, and the count reads off the front.

#### [Recognize] Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit (LeetCode 1438)
<!-- id: dq-longest-limit-subarray -->

**Prerequisites.** All three exercises above, and the sliding window chapter.

**Problem.** Given an integer array `nums` and an integer `limit`, return the length of the longest non-empty contiguous subarray in which the absolute difference between any two elements is at most `limit`.

**Constraints.** 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^9 and 0 <= limit <= 10^9. Linear time.

**Example 1.** Input `nums = [5, 8, 6, 7, 2, 9, 4]`, `limit = 3`, output 4.

**Example 2.** Input `nums = [5, 5, 5, 6]`, `limit = 0`, output 3.

**Hint.** The condition on every pair is the same as a condition on which two elements? When the window becomes invalid, what must be expired from both deques?

**Changed decision.** The window has a variable length, so the left pointer replaces `k` as the expiry bound, and it moves forward while the range of the window is above the limit.
