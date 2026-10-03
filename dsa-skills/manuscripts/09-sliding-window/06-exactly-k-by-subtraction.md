<!-- lesson-kind: standard -->
<!-- lesson-id: exactly-k-by-subtraction -->
## Exactly-K By Subtraction

<!-- stage: context -->
### A Toll Inspector And Her Stickers

A toll inspector watches cars pass through one lane all day, and a log records how many passengers each car carried, in the order the cars came. A car with an odd number of passengers gets a small sticker on its windscreen, and a car with an even number gets none. At the end of the day her manager asks a strange question: how many stretches of consecutive cars in the log contain exactly k stickered cars?

A stretch can be one car or the whole day, and two stretches count separately even if they overlap, or differ by a single unstickered car at one end. She can pick a first car and a last car and count the stickers between them, but there are far too many pairs for that to be pleasant. She also has a feeling that the unstickered cars at the ends of a stretch make the counting awkward, because they can be added or dropped without changing the number of stickers.

<!-- stage: naive -->
### Walk From Every First Car

The straightforward plan is to try every car as the first of a stretch, walk right counting stickers, and add one to the tally whenever the count equals k exactly. When the count passes k, no longer stretch from that start can match, so the walk stops.

```java
static long countByWalking(int[] log, int k) {
    long stretches = 0;
    for (int first = 0; first < log.length; first++) {
        int stickers = 0;
        for (int last = first; last < log.length; last++) {
            stickers += log[last] % 2 != 0 ? 1 : 0;
            if (stickers == k) stretches++;
            if (stickers > k) break;
        }
    }
    return stretches;
}
```

The answer is exact for every log, because each stretch is looked at once, and stretches with k stickers are found even when k is zero.

<!-- stage: bottleneck -->
### Every Start Walks The Same Cars

When most of the log is unstickered, a walk from each first car runs almost to the end without ever passing k, so the total work is about n squared over two readings, which is O(n^2). A day with two hundred thousand cars is far too large for that.

One might hope for a single moving window that tracks exactly k stickers, but it does not work. Suppose the window holds exactly k stickers and the leftmost car is unstickered. Dropping it keeps the count at k, so the window is still good, and so is the one after that. For a given right end, the good left ends are not one boundary but a whole range, and each right end needs the size of that range. A direct exactly-k window has no single position to hold. What is needed is a question for which the left end is one stable boundary, and an arithmetic way back to the question that was asked.

<!-- stage: insight -->
### Two Easy Counts Make The Hard One

Count the stretches with at most k stickers, which is the **at-most count**. This question is monotone: if a stretch has at most k stickers, so does every stretch inside it. For each right end the valid left ends form one unbroken run starting at a single boundary that only moves right, so a window of two edges finds it. At each right end, if the window is `[left, right]`, all `right - left + 1` stretches that end here are valid, and the sum of those over all right ends is the at-most count.

Now split the stretches that have at most k stickers by their exact **property count**. Each one has exactly k stickers or at most k minus one, and never both. So the number with exactly k is the at-most count for k minus the at-most count for k minus one. That is the **subtraction identity**, and it turns one awkward question into two questions of the same easy kind, each costing one pass.

The invariant of each pass is the same as in the earlier window lessons: after the shrink loop, the window ending at `right` is the longest one that still satisfies the limit, and its odd count is exactly the number of stickers inside. The only new care is the boundary: when the limit is below zero, no stretch qualifies at all, because a count can never be negative. So the helper must return zero for a negative limit without starting a loop, and then exactly zero stickers is simply the at-most count for zero minus zero.

<!-- names: at-most count, property count, subtraction identity -->

The same identity works for any property that counts something monotone, such as the number of different values in a stretch, not only odd numbers. All that changes is the bookkeeping that tells the loop whether the window is within the limit.

<!-- stage: variables -->
### Window, Limit And Running Total

`left` and `right` are the inclusive edges of the window, and `odd` is the number of stickered cars inside it. The limit `k` is the cap for the pass, and the helper is called twice with `k` and `k - 1`. `total` is the running sum of `right - left + 1`, which counts the stretches ending at each right edge. It must be a `long`, because a log of one hundred thousand cars can hold five billion stretches, more than an `int` can hold. When the window is empty after trimming, `left` is `right + 1` and the contribution is zero.

<!-- stage: trace -->
### One Pass For Each Limit

The first trace computes the at-most count for a limit of two on the log 2, 1, 4, 3, 2, 5, where odd values are the stickered cars. The window grows over the first five cars, adding one more stretch than the previous step each time, since the left edge stays at zero. The step to study is the last one, at position 5, where the new odd value makes three stickers and the left edge moves two places to bring the count back to two.

```trace
{"cells":[2,1,4,3,2,5],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"odd":0,"added":1,"total":1},"note":"Position 0 holds 2, which is even, so the window holds 0 odd values after trimming. Every start from 0 to 0 gives a valid subarray ending here, which is 1, so the running total is 1."},{"at":{"left":0,"right":1},"vars":{"odd":1,"added":2,"total":3},"note":"Position 1 holds 1, which is odd, so the window holds 1 odd value after trimming. Every start from 0 to 1 gives a valid subarray ending here, which is 2, so the running total is 3."},{"at":{"left":0,"right":2},"vars":{"odd":1,"added":3,"total":6},"note":"Position 2 holds 4, which is even, so the window holds 1 odd value after trimming. Every start from 0 to 2 gives a valid subarray ending here, which is 3, so the running total is 6."},{"at":{"left":0,"right":3},"vars":{"odd":2,"added":4,"total":10},"note":"Position 3 holds 3, which is odd, so the window holds 2 odd values after trimming. Every start from 0 to 3 gives a valid subarray ending here, which is 4, so the running total is 10."},{"at":{"left":0,"right":4},"vars":{"odd":2,"added":5,"total":15},"note":"Position 4 holds 2, which is even, so the window holds 2 odd values after trimming. Every start from 0 to 4 gives a valid subarray ending here, which is 5, so the running total is 15."},{"at":{"left":2,"right":5},"vars":{"odd":2,"added":4,"total":19},"note":"Position 5 holds 5, which is odd, so the window holds 2 odd values after trimming (the left edge moved 2 steps, to 2). Every start from 2 to 5 gives a valid subarray ending here, which is 4, so the running total is 19."}]}
```

The second trace uses a different log, 1, 2, 1, 2, 2, 1, and computes the at-most count for a limit of zero, the pass that gets subtracted when exactly one sticker is wanted. Here the window is often empty. The step to study is at position 2, where the left edge ends at position 3, one past the right edge, and zero stretches are added. The last step shows the arithmetic that finishes the job.

```trace
{"cells":[1,2,1,2,2,1],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":0},"vars":{"odd":0,"added":0,"total":0},"note":"Position 0 holds 1, which is odd, so the window holds 0 odd values after trimming (the left edge moved 1 step, to 1). Every start from 1 to 0 gives a valid subarray ending here, which is 0, so the running total is 0."},{"at":{"left":1,"right":1},"vars":{"odd":0,"added":1,"total":1},"note":"Position 1 holds 2, which is even, so the window holds 0 odd values after trimming. Every start from 1 to 1 gives a valid subarray ending here, which is 1, so the running total is 1."},{"at":{"left":3,"right":2},"vars":{"odd":0,"added":0,"total":1},"note":"Position 2 holds 1, which is odd, so the window holds 0 odd values after trimming (the left edge moved 2 steps, to 3). Every start from 3 to 2 gives a valid subarray ending here, which is 0, so the running total is 1."},{"at":{"left":3,"right":3},"vars":{"odd":0,"added":1,"total":2},"note":"Position 3 holds 2, which is even, so the window holds 0 odd values after trimming. Every start from 3 to 3 gives a valid subarray ending here, which is 1, so the running total is 2."},{"at":{"left":3,"right":4},"vars":{"odd":0,"added":2,"total":4},"note":"Position 4 holds 2, which is even, so the window holds 0 odd values after trimming. Every start from 3 to 4 gives a valid subarray ending here, which is 2, so the running total is 4."},{"at":{"left":6,"right":5},"vars":{"odd":0,"added":0,"total":4},"note":"Position 5 holds 1, which is odd, so the window holds 0 odd values after trimming (the left edge moved 3 steps, to 6). Every start from 6 to 5 gives a valid subarray ending here, which is 0, so the running total is 4. With atMost(1) equal to 15 and atMost(0) equal to 4, the exactly-one count is 11."}]}
```

<!-- stage: code -->
### Helper Called Twice

```java
static long atMostOdd(int[] a, int limit) {
    if (limit < 0) return 0;                          // no stretch has a negative count
    long total = 0;
    int left = 0, odd = 0;
    for (int right = 0; right < a.length; right++) {
        odd += a[right] & 1;
        while (odd > limit) odd -= a[left++] & 1;
        total += right - left + 1;
    }
    return total;
}

static long exactlyOdd(int[] a, int k) {
    return atMostOdd(a, k) - atMostOdd(a, k - 1);
}

static long atMostKinds(int[] a, int limit) {
    if (limit < 0) return 0;
    Map<Integer, Integer> seen = new HashMap<>();
    long total = 0;
    int left = 0;
    for (int right = 0; right < a.length; right++) {
        seen.merge(a[right], 1, Integer::sum);
        while (seen.size() > limit) {
            int gone = a[left++];
            if (seen.merge(gone, -1, Integer::sum) == 0) seen.remove(gone);
        }
        total += right - left + 1;
    }
    return total;
}
```

Each helper makes one pass, so the pair costs two passes, still linear, and the odd version needs constant extra space while the kinds version holds at most limit plus one keys. The addition `right - left + 1` is an `int` and is widened to `long` before it joins the total, which is safe because a single window length never exceeds the array length. The `limit < 0` guard sits before any loop, because the shrink loop below it is only correct when the limit is zero or more.

<!-- stage: applicability -->
### When The Question Says Exactly

A question that asks how many stretches have exactly k of something is a signal to look for the matching at-most question. Check three things before coding: the property must be a count that only goes down when elements leave, the at-most version must be monotone, and the answer must be a count of stretches, not a longest or shortest length. State the invariant once, for the helper, and the identity takes care of the rest.

A false friend is a single window that tries to hold exactly k, since it has no single left boundary when removable elements sit at the ends. Another is the longest-window pattern, which asks for a maximum and would be satisfied by one boundary. A third is a prefix tally of stickers used without a counter of how often each prefix value has occurred, which forgets that many earlier cut points can share one value.

In Java, accumulate in `long`, call the helper with `k - 1` only after the guard handles negative limits, and keep the two passes independent so that neither helper depends on state from the other. When the property is a number of different values, size the map for at most limit plus one keys and evict at zero.

<!-- stage: exercises -->
### Exercises

#### [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Prerequisites.** The at-most-k distinct windows lesson, and the habit of stating the window invariant.

**Problem.** Given an array of integers, return how many contiguous subarrays contain exactly one odd value. Compute it as the number of subarrays with at most one odd value minus the number with at most zero odd values.

**Constraints.** 0 <= nums.length <= 100000 and any `int` values, negative values allowed. The result may exceed the range of `int`.

**Example 1.** Input `nums = [2, 3, 4, 6, 5]`, output 9.

**Example 2.** Input `nums = [8, 8, 8]`, output 0.

**Hint.** What does the pass for limit zero count? Why does each pass add `right - left + 1` at every right edge?

**Changed decision.** First rung: the identity is used with fixed limits one and zero, so only the helper needs a window.

#### [Vary] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Prerequisites.** The exactly-one exercise above.

**Problem.** Given an array and an integer `k`, a subarray is nice if it contains exactly `k` odd values. Return the number of nice subarrays.

**Constraints.** 1 <= nums.length <= 50000, 1 <= nums[i] <= 100000 and 1 <= k <= nums.length. Use `long` for the result.

**Example 1.** Input `nums = [1, 2, 2, 1, 3, 2], k = 2`, output 7.

**Example 2.** Input `nums = [4, 6, 8], k = 1`, output 0.

**Hint.** If you pass the limit as a parameter, which two limits give the answer? What should the shrink loop subtract when it moves the left edge?

**Changed decision.** The limit becomes a parameter, and the count of odd values replaces the fixed limit of one.

#### [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Prerequisites.** The two exercises above.

**Problem.** Return the number of contiguous subarrays of an array that contain exactly `k` odd values, where `k` may be zero. Define the at-most helper to return zero for a limit of minus one without running its loop, so that the subtraction stays safe for k equal to zero.

**Constraints.** 0 <= nums.length <= 50000, 0 <= k <= 60000 and any `int` values. The result may not fit in an `int`.

**Example 1.** Input `nums = [2, 4, 1, 6], k = 0`, output 4.

**Example 2.** Input `nums = [1, 1], k = 3`, output 0.

**Hint.** What is the at-most count for a limit of minus one, and why? What does the shrink loop do if it is run with that limit on a nonempty array?

**Changed decision.** The second helper call gets a negative limit, so the guard before the loop is what keeps the identity valid.

#### [Recognize] Subarrays with K Different Integers (LeetCode 992)
<!-- id: sw-k-different-integers -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array of positive integers and an integer `k`, return the number of subarrays that contain exactly `k` different integers. Maintain counts in a map and apply the same identity.

**Constraints.** 1 <= nums.length <= 20000, 1 <= nums[i] <= nums.length and 1 <= k <= nums.length. Use two passes of expected linear time.

**Example 1.** Input `nums = [3, 1, 3, 2, 2], k = 2`, output 5.

**Example 2.** Input `nums = [5, 5, 5], k = 2`, output 0.

**Hint.** What property is being counted now, and what does the map's size tell the shrink loop? Which key must be removed when a count reaches zero?

**Changed decision.** The counted property is the number of different values, so the odd counter is replaced by a map whose size is the quantity compared with the limit.
