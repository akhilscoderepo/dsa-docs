<!-- lesson-kind: standard -->
<!-- lesson-id: count-every-valid-subarray -->
## Count Every Valid Subarray

<!-- stage: context -->
### A Quota Report That Counts Spans

A billing system stores the usage of each day as a positive number of units. A report must count how many spans of consecutive days stay under a quota, because each such span passes a fair-use check. For a year of daily usage, the count has hundreds of thousands of possible spans. A developer writes a window that finds the longest span under the quota. The report needs the count of all spans, so the longest span is not enough.

Earlier lessons asked for one best length, and a window gave it. Counting every valid span asks for more. One window position stands for many spans, because every span inside a valid span is valid too. This lesson asks how the window can count all of them without listing them.

<!-- stage: naive -->
### Test Every Span

The direct method visits every span by its first and last day. A running sum grows as the last day moves, and each sum below the quota adds one to the answer.

```java
static long countSpansByPairs(int[] usage, int quota) {
    long answer = 0;
    for (int start = 0; start < usage.length; start++) {
        long sum = 0;
        for (int end = start; end < usage.length; end++) {
            sum += usage[end];
            if (sum < quota) answer++;
        }
    }
    return answer;
}
```

The method is correct for any values, because it tests each span on its own.

<!-- stage: bottleneck -->
### Counting Pairs One By One

```predict
For the end index 5, the span from start 2 to index 5 has a sum below the quota, and all daily values are positive. Do the spans from start 3, start 4 and start 5 to index 5 also stay below the quota?

Yes. A span inside a valid span drops some positive values, so its sum is smaller. All three spans pass the check, and the method can count them without testing each.
```

The pair loop runs about `n^2 / 2` tests, so it costs O(n^2). For a year of per-second usage, `n` is about 31 million, and the loop runs about 5 * 10^14 tests. The shrinking window runs in O(n), but it records one position per end index. The count needs more than a position. It needs the number of valid starts for that end index.

The prediction contains the answer. For one end index, the valid starts form an unbroken range from the smallest valid start to the end index itself. The method needs only the smallest valid start, and the size of the range follows from two indexes.

<!-- stage: insight -->
### Add The Valid Starts For Each End

#### The Valid Starts For One End

After the shrink loop, `left` is the smallest start whose span to `right` is valid. The **valid starts** of the index `right` are the starts `left`, `left + 1`, and so on up to `right`. There are `right - left + 1` of them. Each start gives one valid subarray that ends at `right`, so the window contributes `right - left + 1` to the answer for this end index.

#### Why Every Later Start Is Valid

The rule holds because the values are **positive values**, and removing one from the front lowers the sum. A span that starts later is a span inside the valid span, so its sum is smaller still. The same argument works for any condition that survives the removal of a prefix. Examples are at most `k` zeros, or a count of distinct values that does not rise.

#### The Empty Window

The window may shrink until it holds nothing. The **empty window** has `left = right + 1`, so `right - left + 1` is 0, and the method adds 0 for this end index. This happens when a single value alone is too large. The invariant is that after the shrink loop, every start from `left` to `right` gives a valid subarray ending at `right`, and every start before `left` does not. The sum of the contributions over all `right` counts each valid subarray exactly once, because each subarray has exactly one end index.

<!-- names: valid starts, positive values, empty window -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps the usual two indexes, a summary of the window and a running answer.

- **left** is the smallest start with a valid span to `right`, and it equals `right + 1` for an empty window.
- **right** is the end index that the method is counting for.
- **sum** is the sum of `nums[left..right]`, held in a `long`.
- **count** is the running total of `right - left + 1` over all end indexes, held in a `long`.

<!-- stage: trace -->
### Tracing Two Counts

#### Counting Spans Under A Quota Of Five

Take `nums = [2, 1, 3, 1, 2]` and the quota 5, so a span is valid when its sum is below 5. The trace below shows `left`, `right`, the window sum, and the running count. The variable `add` is the number of valid starts for the current `right`.

```trace
{"cells":[2,1,3,1,2],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"sum":"2","add":"1","count":"1"},"note":"The value 2 enters, so the sum is 2. The starts 0 to 0 are valid, so add is 1 and the count is 1."},{"at":{"left":0,"right":1},"vars":{"sum":"3","add":"2","count":"3"},"note":"The value 1 enters, so the sum is 3. The starts 0 to 1 are valid, so add is 2 and the count is 3."},{"at":{"left":1,"right":2},"vars":{"sum":"4","add":"2","count":"5"},"note":"The value 3 enters, so the sum is 6. The sum 6 is not below 5, so the value 2 leaves. The starts 1 to 2 are valid, so add is 2 and the count is 5."},{"at":{"left":2,"right":3},"vars":{"sum":"4","add":"2","count":"7"},"note":"The value 1 enters, so the sum is 5. The sum 5 is not below 5, so the value 1 leaves. The starts 2 to 3 are valid, so add is 2 and the count is 7."},{"at":{"left":3,"right":4},"vars":{"sum":"3","add":"2","count":"9"},"note":"The value 2 enters, so the sum is 6. The sum 6 is not below 5, so the value 3 leaves. The starts 3 to 4 are valid, so add is 2 and the count is 9."}]}
```

The total is 9. Every addition counts a whole range of starts at once, and no span is tested twice.

#### A Quota Of One

Take `nums = [2, 3, 1]` and the quota 1. Every value is at least 1, so no span has a sum below 1. At each end index, the window shrinks until it is empty, and `left` becomes `right + 1`. The contribution is 0 each time, and the total is 0. The method never lets `left` pass `right + 1`, because an empty window has a sum of 0 and passes the check of the loop.

```trace
{"cells":[2,3,1],"pointers":["left","right"],"steps":[{"at":{"left":1,"right":0},"vars":{"sum":"0","add":"0","count":"0"},"note":"The value 2 enters, so the sum is 2. The sum 2 is not below 1, so the value 2 leaves. The window is empty, so add is 0 and the count is 0."},{"at":{"left":2,"right":1},"vars":{"sum":"0","add":"0","count":"0"},"note":"The value 3 enters, so the sum is 3. The sum 3 is not below 1, so the value 3 leaves. The window is empty, so add is 0 and the count is 0."},{"at":{"left":3,"right":2},"vars":{"sum":"0","add":"0","count":"0"},"note":"The value 1 enters, so the sum is 1. The sum 1 is not below 1, so the value 1 leaves. The window is empty, so add is 0 and the count is 0."}]}
```

<!-- stage: code -->
### Counting Valid Spans In Java

#### The Window That Adds Valid Starts

```java
static long countBelow(int[] nums, int quota) {
    long sum = 0, count = 0;
    int left = 0;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (left <= right && sum >= quota) {
            sum -= nums[left];
            left++;
        }
        count += right - left + 1;
    }
    return count;
}
```

The condition `left <= right` stops the loop for an empty window. The sum and the count have type `long`, because the count can reach about `n * n / 2`.

#### Cost Of The Count

Each index enters once and leaves at most once. The running time is therefore linear, and the working memory is constant. The answer can reach about `n * (n + 1) / 2`, so `int` overflows for `n` above about 65,000. The `long` type holds the count for any `n` that fits in memory.

<!-- stage: applicability -->
### When The Count Rule Applies

#### Spotting A Count Of All Valid Ranges

Look for a request for the number of contiguous ranges that satisfy a condition, where a range inside a valid range is also valid. Typical conditions are a sum below a bound for positive values, a product below a bound, and at most `k` bad values. Each condition gives an at-most test that one boundary maintains.

#### The Invariant To State

After the shrink loop, every start from `left` to `right` gives a valid subarray that ends at `right`, and no earlier start does. The addition `right - left + 1` is correct only under this statement, so the reader should check it before the line that adds.

#### Negative Values Are A False Friend

The addition fails when a range inside a valid range may be invalid. Take `nums = [4, -3, 2]` and the bound 3, where a span is valid when its sum is below 3. The window sees the sum 4 at index 0, discards the start 0, and never returns to it. Later it misses the valid span `[4, -3]`, which has sum 1. The window counts 3, and the true count is 4. A negative value makes the sum rise when a prefix leaves, so the condition does not survive removal.

#### Java Habits For This Pattern

Count in a `long`, and add `right - left + 1` after the shrink loop. Guard the loop with `left <= right`, so an empty window is safe. For a product, use a `long` or a `double` carefully, and divide with integer division only when the values are positive integers. Do not write the count as a sum of window lengths computed from `best`.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-count-one-zero -->

**Prerequisites.** The valid starts and the invariant of this lesson.

**Problem.** Given a binary array `bits`, return the number of contiguous subarrays that contain at most one zero. Two subarrays are different when their start or end index differs.

**Constraints.**
- **Length** satisfies `1 <= bits.length <= 10^5`.
- **Values** are 0 or 1.
- **Return** type is `long`.
- **Mutation** does not occur; `bits` is unchanged.

**Example 1.** Input `bits = [1,0,1,0,1]`. Output `11`.

**Example 2.** Input `bits = [0,0,0]`. Output `3`.

**Hint.** Which start values stay valid for an end index after the shrink loop?

**Changed decision.** The method adds the number of valid starts for each end, in place of the longest length.

#### [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-count-sum-below -->

**Prerequisites.** The exercise above.

**Problem.** Given an array `nums` of positive integers and an integer `k`, return the number of contiguous subarrays whose sum is strictly less than `k`.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `1 <= nums[i] <= 10^4`.
- **Bound** satisfies `1 <= k <= 10^9`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,1,3,1,2]`, `k = 5`. Output `9`.

**Example 2.** Input `nums = [1,1,1]`, `k = 3`. Output `5`.

**Hint.** Why does positivity make a later start give a smaller sum?

**Changed decision.** The state is a sum, and positivity justifies the shrinking loop.

#### [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-count-k-minimum -->

**Prerequisites.** The two exercises above.

**Problem.** Given an array `nums` of positive integers and an integer `k >= 1`, return the number of contiguous subarrays whose sum is strictly less than `k`. For `k = 1`, no subarray qualifies. The method must keep `left <= right + 1` and must add 0 for an empty window.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `1 <= nums[i] <= 10^4`.
- **Bound** satisfies `1 <= k <= 10^9`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,3,1]`, `k = 1`. Output `0`.

**Example 2.** Input `nums = [1,1]`, `k = 2`. Output `2`.

**Hint.** What does the shrink loop do when one value alone reaches the bound?

**Changed decision.** The window may be empty, and an empty window contributes zero.

#### [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Prerequisites.** All three exercises above.

**Problem.** Given an array `nums` of positive integers and an integer `k`, return the number of contiguous subarrays whose product of all elements is strictly less than `k`.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 3 * 10^4`.
- **Values** satisfy `1 <= nums[i] <= 1000`.
- **Bound** satisfies `0 <= k <= 10^6`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [3,2,4,1]`, `k = 10`. Output `8`.

**Example 2.** Input `nums = [5,6]`, `k = 5`. Output `0`.

**Hint.** What is the product of an empty window, and what happens when `k` is 0 or 1?

**Changed decision.** The state is a product, and an empty window has product 1.
