<!-- lesson-kind: standard -->
<!-- lesson-id: exactly-k-by-subtraction -->
## Count Exactly K By Subtraction

<!-- stage: context -->
### A Count That Moves Two Boundaries

A fraud team flags some transactions in a ledger. An analyst needs the number of ranges of consecutive transactions that hold exactly three flagged ones, because such a range triggers a manual review. The ledger has 100,000 entries. A developer tries the shrinking window from the last lessons and gets wrong counts. Whenever a new flagged entry arrives, the window shrinks until it holds three flagged entries. The window then names one range, but many ranges ending at the same entry also hold exactly three.

The earlier lessons asked for a longest or shortest range, so one boundary was enough. This lesson counts ranges. It asks how a count of "exactly three" can be built from counts that a single shrinking boundary does produce correctly. The slow program below reads a `boolean` array, where `true` marks a flagged entry. The fast method reads an `int` array and treats an odd number as the flagged entry, so one test, `nums[i] % 2 != 0`, replaces the stored flag.

<!-- stage: naive -->
### Test Every Range

The direct method tests every pair of start and end indexes. It keeps a running count of flagged entries as the end index moves, and it adds one to the answer whenever the count equals `k`.

```java
static long countExactlyByPairs(boolean[] flagged, int k) {
    long answer = 0;
    for (int start = 0; start < flagged.length; start++) {
        int count = 0;
        for (int end = start; end < flagged.length; end++) {
            if (flagged[end]) count++;
            if (count == k) answer++;
        }
    }
    return answer;
}
```

The method is correct for any input, including a `k` that is larger than the number of flagged entries.

<!-- stage: bottleneck -->
### Why One Boundary Is Not Enough

```predict
A range ending at index 8 holds exactly 3 flagged entries and starts at index 2. Entry 2 is not flagged. Does the range starting at index 3 and ending at index 8 also hold exactly 3?

Yes. Removing an entry that is not flagged does not change the count. So several starts can give exactly 3 for one end, and the shrinking window finds only one of them.
```

The pair loop costs O(n^2), which for `n = 100,000` is about 5 billion steps. A shrinking window would cost O(n), but it needs one stable position of `left` for each `right`. For "exactly `k`" there is none. The valid starts for one `right` form a range of starts, with a smallest and a largest start. Removing an unflagged value at the left keeps the count at `k`. The condition does not hold for every sub-block of a valid block, so shrinking on "count above `k`" skips valid ranges.

The condition "at most `k`" behaves differently. A block with at most `k` flagged entries stays valid when entries leave. Counting such ranges needs only one boundary. The remaining question is how to turn two of these counts into the count of "exactly `k`".

<!-- stage: insight -->
### Subtract Two Counts Of At Most

#### The At-Most Count With One Boundary

The earlier `boolean` flag becomes an odd test on an `int` input here, and the window counts odd numbers where the slow program counted `true` values. The **at-most count** for a limit `x` is the number of ranges that hold at most `x` flagged entries. For each `right`, the shrinking window gives the smallest valid `left`. Every start from `left` to `right` also gives a valid range ending at `right`, because removing entries keeps the range valid. The number of valid ranges that end at `right` is therefore `right - left + 1`. The total is the sum of these numbers over all `right`.

#### Why The Subtraction Is Exact

Every range holds some number `c` of flagged entries. The at-most count for `k` covers the ranges with `c <= k`. The at-most count for `k - 1` covers the ranges with `c <= k - 1`. The second group lies inside the first. The ranges left over have `c == k`. The **subtraction identity** is `exactly(k) = atMost(k) - atMost(k - 1)`, and it is exact as arithmetic for any integer count `k`. It is useful when `atMost` needs only one boundary.

#### The Empty Budget

When `k = 0`, the second term asks for `atMost(-1)`. This limit is the **empty budget**. No range holds at most -1 flagged entries, so the count is 0. The method returns 0 for a negative limit and does not run the loop. The invariant is that each call counts every range whose number of flagged entries is at most its limit, and it counts each range once.

<!-- names: at-most count, subtraction identity, empty budget -->

<!-- stage: variables -->
### What The Method Keeps

Each call of the at-most count keeps its own small state.

- **limit** is the largest allowed number of flagged entries, and a negative limit returns 0 at once.
- **left** and **right** are the first and last index of the current window.
- **odd** is the number of flagged entries in the window, and the flagged entries are the odd numbers.
- **add** is `right - left + 1`, the number of valid ranges that end at `right`. In the code it is written inline.
- **total** is the running sum of `add`, held in a `long`, because it can exceed the `int` range.

<!-- stage: trace -->
### Tracing The Two Counts

#### Counting Ranges With At Most Two Odd Numbers

Take `nums = [2, 1, 3, 4, 1]`. A flagged entry is an odd number, so the variable `odd` counts the flagged entries in the window. The target is exactly 2 odd numbers. The trace below runs the at-most count for the limit 2. At each step, the variable `add` is `right - left + 1`, the number of valid ranges that end at `right`.

```trace
{"cells":[2,1,3,4,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"odd":"0","add":"1","total":"1"},"note":"The value 2 enters. The starts 0 to 0 are valid, so add is 1 and the total is 1."},{"at":{"left":0,"right":1},"vars":{"odd":"1","add":"2","total":"3"},"note":"The value 1 enters. It is odd, so the odd count is 1. The starts 0 to 1 are valid, so add is 2 and the total is 3."},{"at":{"left":0,"right":2},"vars":{"odd":"2","add":"3","total":"6"},"note":"The value 3 enters. It is odd, so the odd count is 2. The starts 0 to 2 are valid, so add is 3 and the total is 6."},{"at":{"left":0,"right":3},"vars":{"odd":"2","add":"4","total":"10"},"note":"The value 4 enters. The starts 0 to 3 are valid, so add is 4 and the total is 10."},{"at":{"left":2,"right":4},"vars":{"odd":"2","add":"3","total":"13"},"note":"The value 1 enters. It is odd, so the odd count is 3. The even value 2 leaves. The odd value 1 leaves, so the odd count is 2. The starts 2 to 4 are valid, so add is 3 and the total is 13."}]}
```

The total for the limit 2 is 13. That total counts every range with at most two odd numbers.

#### Counting Ranges With At Most One Odd Number

The same array with the limit 1 gives the second count. The window shrinks sooner, because the second odd number at index 2 already breaks the limit.

```trace
{"cells":[2,1,3,4,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"odd":"0","add":"1","total":"1"},"note":"The value 2 enters. The starts 0 to 0 are valid, so add is 1 and the total is 1."},{"at":{"left":0,"right":1},"vars":{"odd":"1","add":"2","total":"3"},"note":"The value 1 enters. It is odd, so the odd count is 1. The starts 0 to 1 are valid, so add is 2 and the total is 3."},{"at":{"left":2,"right":2},"vars":{"odd":"1","add":"1","total":"4"},"note":"The value 3 enters. It is odd, so the odd count is 2. The even value 2 leaves. The odd value 1 leaves, so the odd count is 1. The starts 2 to 2 are valid, so add is 1 and the total is 4."},{"at":{"left":2,"right":3},"vars":{"odd":"1","add":"2","total":"6"},"note":"The value 4 enters. The starts 2 to 3 are valid, so add is 2 and the total is 6."},{"at":{"left":3,"right":4},"vars":{"odd":"1","add":"2","total":"8"},"note":"The value 1 enters. It is odd, so the odd count is 2. The odd value 3 leaves, so the odd count is 1. The starts 3 to 4 are valid, so add is 2 and the total is 8."}]}
```

The total for the limit 1 is 8. The answer for exactly two odd numbers is 13 - 8 = 5. The five ranges are `[1,3]`, `[2,1,3]`, `[1,3,4]`, `[2,1,3,4]` and `[3,4,1]`.

<!-- stage: code -->
### The Two Counts In Java

#### The At-Most Count And The Difference

```java
static long countExactly(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}

static long atMost(int[] nums, int limit) {
    if (limit < 0) return 0;
    int left = 0, odd = 0;
    long total = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] % 2 != 0) odd++;
        while (odd > limit) {
            if (nums[left] % 2 != 0) odd--;
            left++;
        }
        total += right - left + 1;
    }
    return total;
}
```

The test `nums[i] % 2 != 0` is correct for negative numbers, because `-3 % 2` is -1 in Java. The test `nums[i] % 2 == 1` would miss every negative odd number.

#### Cost Of The Difference

Each call of `atMost` costs O(n), and `countExactly` makes two calls, so the whole count runs in linear time. The extra memory is constant. The sum is a `long`, because a range count of about `n * n / 2` overflows `int` for `n` near 100,000.

<!-- stage: applicability -->
### When The Subtraction Applies

#### Spotting An Exactly-K Count

Look for a request to count the ranges with exactly `k` of something, such as odd numbers or distinct values. The condition "at most `k`" must be easy to maintain with one shrinking boundary. The property must have an integer count that never rises when the range loses an entry.

#### The Invariant To State

Each call counts the ranges with at most its limit, and the two calls count nested sets. The second set lies inside the first, so the difference is exactly the set with count `k`. State this before writing the code.

#### A Direct Exactly-K Window Is A False Friend

A single window that shrinks while the count exceeds `k` looks natural, and it finds only one start for each `right`. Valid starts form a range, because removing an entry that does not change the count keeps the range exact. The direct window therefore undercounts, and it passes samples where each `right` has only one valid start.

#### Java Habits For This Pattern

Return 0 for a negative limit at the top of the helper. Count in a `long`. Test oddness with `% 2 != 0`, not `% 2 == 1`. Keep the helper independent of `k`, so both calls share one tested method.

<!-- stage: exercises -->
### Exercises

#### [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Prerequisites.** The at-most count and the subtraction identity of this lesson.

**Problem.** Given an integer array `nums`, return the number of contiguous subarrays that contain exactly one odd number. Compute it as `atMost(1) - atMost(0)`, where `atMost(x)` is the number of subarrays with at most `x` odd numbers.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^9 <= nums[i] <= 10^9`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,1,3,4,1]`. Output `6`.

**Example 2.** Input `nums = [4,6]`. Output `0`.

**Hint.** What does `atMost(0)` count? Which Java test finds an odd negative number?

**Changed decision.** The method makes two passes with fixed limits, and it subtracts the counts.

#### [Vary] Count Number Of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Prerequisites.** The exercise above.

**Problem.** For an integer array `nums` and a target `k`, return the number of contiguous subarrays that contain exactly `k` odd numbers.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^9 <= nums[i] <= 10^9`.
- **Limit** satisfies `1 <= k <= nums.length`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,1,3,4,1]`, `k = 2`. Output `5`.

**Example 2.** Input `nums = [2,4,6]`, `k = 1`. Output `0`.

**Hint.** Which limits does the subtraction use when the target is `k`?

**Changed decision.** The target `k` is a parameter, and the two limits are `k` and `k - 1`.

#### [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` and an integer `k` with `k >= 0`, return the number of contiguous subarrays that contain exactly `k` odd numbers. For `k = 0`, the subarrays have no odd number. Define `atMost(-1)` as 0, so the same subtraction covers `k = 0`.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^9 <= nums[i] <= 10^9`.
- **Limit** satisfies `0 <= k <= nums.length`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,1,3,4,1]`, `k = 0`. Output `2`, from `[2]` and `[4]`.

**Example 2.** Input `nums = [4,6]`, `k = 0`. Output `3`.

**Hint.** What does the shrink loop do with a negative limit, when `left` can run past the end of the array? Which line of the helper avoids it?

**Changed decision.** A guard on the limit replaces a loop that can run `left` off the array.

#### [Recognize] Subarrays With K Different Integers (LeetCode 992)
<!-- id: sw-k-different -->

**Prerequisites.** All three exercises above.

**Problem.** Count the contiguous subarrays of `nums` that contain exactly `k` different integers. Maintain a map from value to count for the at-most count.

**Constraints.**
- **Length** satisfies `1 <= nums.length <= 10^5`.
- **Values** satisfy `1 <= nums[i] <= nums.length`.
- **Limit** satisfies `1 <= k <= nums.length`.
- **Return** type is `long`.
- **Mutation** does not occur; `nums` is unchanged.

**Example 1.** Input `nums = [2,1,2,3,1]`, `k = 2`. Output `5`.

**Example 2.** Input `nums = [3,3,3]`, `k = 2`. Output `0`.

**Hint.** Which earlier lesson keeps a map and removes a key at count 0? What replaces the odd-number test?

**Changed decision.** The property is the number of distinct values, held in a count map.
