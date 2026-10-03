<!-- lesson-kind: standard -->
<!-- lesson-id: exactly-k-by-subtraction -->
## Exactly-K By Subtraction

<!-- stage: context -->
### Counting The Quiet Stretches

A hospital ward logs, for each hour, whether an alarm sounded. A manager wants a count, not a length. How many different stretches of consecutive hours contained exactly three alarm hours? Two stretches that cover different hours count separately, even if one sits inside the other, and a stretch of five hours with three alarms and a stretch of seven hours with the same three alarms are both counted.

The question changed in two ways. The answer is a number of ranges, not the length of the best one. And the condition is an exact count instead of a limit. Counting how many subarrays contain exactly `k` odd numbers, exactly `k` ones, or exactly `k` different values all have this shape.

<!-- stage: naive -->
### Try Every Pair Of Edges

Pick every start, extend through every end, keep a running count of alarm hours, and add one to the answer whenever the count equals `k`.

```java
static long countExactlyBruteForce(int[] alarms, int k) {
    long total = 0;
    for (int start = 0; start < alarms.length; start++) {
        int seen = 0;
        for (int end = start; end < alarms.length; end++) {
            seen += alarms[end];
            if (seen == k) total++;
        }
    }
    return total;
}
```

It is correct for every input, including negative values and a count of zero, because it checks each range separately.

<!-- stage: bottleneck -->
### Every Range Visited Once

There are about n^2 / 2 ranges, and the method visits each of them, so the time is O(n^2). A year of hourly logs has 8,760 entries and produces 38 million ranges, which is fine, but a week of per-second logs has 604,800 entries and produces 183 billion ranges, which is not. The method keeps no state between starts, even though every start's running count equals the previous start's count minus one entry.

The tempting repair is to bring in the window machinery and keep a single window with exactly `k` alarms. That fails for a concrete reason, and the next section explains it.

<!-- stage: insight -->
### Count The Easy Question Twice

Try to maintain a window that holds exactly `k` alarms and see where it breaks. Suppose the window has exactly three alarms and the leftmost entry is a quiet hour. Remove it and the window still has exactly three. So the left edge has no single correct position. Any of several starts is valid for the same `right`, and the number of valid starts is what we need, which is not something a single boundary can tell us.

The way out is to ask a different, easier question. How many subarrays contain at most `k` alarms? That question is monotone. If a window has at most `k`, shrinking it keeps it valid, so the longest-valid machinery applies. For each `right`, the repaired window starts at `left`, and every start from `left` through `right` gives a valid subarray ending at `right`, which is `right - left + 1` of them.

Now notice the counts nest. Every subarray with exactly `k` alarms also has at most `k`, and the subarrays with at most `k` split cleanly into those with exactly `k` and those with at most `k - 1`. Subtracting gives the identity that names this lesson: `exactly(k) = atMost(k) - atMost(k - 1)`. We call the technique **exactly-K by subtraction**, and each of its two parts is an **at-most count**.

<!-- names: at-most count, exactly-K by subtraction -->

The cost is two passes instead of one. Each pass is a plain monotone window running in linear time, so the sum is still linear. The subtraction is exact because every subarray falls into exactly one of the two groups, so nothing is counted twice and nothing is missed.

<!-- stage: variables -->
### Per Pass State

Each pass keeps `left` and `right` for the window, an integer `odds` that counts the alarm entries inside it, and a running `total` of valid subarrays so far. The pass takes the budget as an argument. After the repair loop, the window holds at most the budget, and the number of subarrays ending at `right` that satisfy the budget is `right - left + 1`. The answer combines the two totals once at the end and uses no other state.

<!-- stage: trace -->
### One Run Through

Take the array `[1, 1, 2, 1, 1]` and count the subarrays with exactly three odd numbers. The first pass uses a budget of three. At index 0 the window holds one odd value, and one subarray ends there. At index 1 there are two odd values and two subarrays end there. Index 2 is even, so the window holds the same two odd values and three subarrays end there. At index 3 the odd count reaches three, which is still within budget, so four subarrays end there.

Index 4 pushes the odd count to four, over the budget. One removal at the left, the odd value at index 0, brings it back to three, and the window covers indices 1 through 4, so four more subarrays end there. The first total is 1 + 2 + 3 + 4 + 4 = 14. Of the fifteen subarrays in total, only the whole array has four odd values, so fourteen is right.

The second pass uses a budget of two. The first three positions give 1, 2 and 3 again, a total of 6. At index 3 the odd count is three, so the left edge drops index 0, and three subarrays end there. At index 4 the count reaches three again and the left edge drops index 1, leaving three more. The second total is 12.

Fourteen minus twelve leaves two. Those two subarrays are `[1, 1, 2, 1]` and `[1, 2, 1, 1]`, each containing exactly three odd values.

```trace
{"cells":[1,1,2,1,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"pass":"atMost(3)","odds":1,"total":0},"note":"Take in index 0 (value 1)."},{"at":{"left":0,"right":0},"vars":{"pass":"atMost(3)","odds":1,"total":1},"note":"Every start from 0 to 0 works, so 1 subarrays end here. Running total: 1."},{"at":{"left":0,"right":1},"vars":{"pass":"atMost(3)","odds":2,"total":1},"note":"Take in index 1 (value 1)."},{"at":{"left":0,"right":1},"vars":{"pass":"atMost(3)","odds":2,"total":3},"note":"Every start from 0 to 1 works, so 2 subarrays end here. Running total: 3."},{"at":{"left":0,"right":2},"vars":{"pass":"atMost(3)","odds":2,"total":3},"note":"Take in index 2 (value 2)."},{"at":{"left":0,"right":2},"vars":{"pass":"atMost(3)","odds":2,"total":6},"note":"Every start from 0 to 2 works, so 3 subarrays end here. Running total: 6."},{"at":{"left":0,"right":3},"vars":{"pass":"atMost(3)","odds":3,"total":6},"note":"Take in index 3 (value 1)."},{"at":{"left":0,"right":3},"vars":{"pass":"atMost(3)","odds":3,"total":10},"note":"Every start from 0 to 3 works, so 4 subarrays end here. Running total: 10."},{"at":{"left":0,"right":4},"vars":{"pass":"atMost(3)","odds":4,"total":10},"note":"Take in index 4 (value 1). The window now holds 4 odd values, over the budget of 3."},{"at":{"left":1,"right":4},"vars":{"pass":"atMost(3)","odds":3,"total":10},"note":"Remove index 0 (value 1) from the left. The budget is respected again."},{"at":{"left":1,"right":4},"vars":{"pass":"atMost(3)","odds":3,"total":14},"note":"Every start from 1 to 4 works, so 4 subarrays end here. Running total: 14."},{"at":{"left":0,"right":0},"vars":{"pass":"atMost(2)","odds":1,"total":0},"note":"Take in index 0 (value 1)."},{"at":{"left":0,"right":0},"vars":{"pass":"atMost(2)","odds":1,"total":1},"note":"Every start from 0 to 0 works, so 1 subarrays end here. Running total: 1."},{"at":{"left":0,"right":1},"vars":{"pass":"atMost(2)","odds":2,"total":1},"note":"Take in index 1 (value 1)."},{"at":{"left":0,"right":1},"vars":{"pass":"atMost(2)","odds":2,"total":3},"note":"Every start from 0 to 1 works, so 2 subarrays end here. Running total: 3."},{"at":{"left":0,"right":2},"vars":{"pass":"atMost(2)","odds":2,"total":3},"note":"Take in index 2 (value 2)."},{"at":{"left":0,"right":2},"vars":{"pass":"atMost(2)","odds":2,"total":6},"note":"Every start from 0 to 2 works, so 3 subarrays end here. Running total: 6."},{"at":{"left":0,"right":3},"vars":{"pass":"atMost(2)","odds":3,"total":6},"note":"Take in index 3 (value 1). The window now holds 3 odd values, over the budget of 2."},{"at":{"left":1,"right":3},"vars":{"pass":"atMost(2)","odds":2,"total":6},"note":"Remove index 0 (value 1) from the left. The budget is respected again."},{"at":{"left":1,"right":3},"vars":{"pass":"atMost(2)","odds":2,"total":9},"note":"Every start from 1 to 3 works, so 3 subarrays end here. Running total: 9."},{"at":{"left":1,"right":4},"vars":{"pass":"atMost(2)","odds":3,"total":9},"note":"Take in index 4 (value 1). The window now holds 3 odd values, over the budget of 2."},{"at":{"left":2,"right":4},"vars":{"pass":"atMost(2)","odds":2,"total":9},"note":"Remove index 1 (value 1) from the left. The budget is respected again."},{"at":{"left":2,"right":4},"vars":{"pass":"atMost(2)","odds":2,"total":12},"note":"Every start from 2 to 4 works, so 3 subarrays end here. Running total: 12."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static long atMost(int[] nums, int k) {
    if (k < 0) return 0;                     // no subarray can have fewer than zero items
    long total = 0;
    int left = 0, odds = 0;
    for (int right = 0; right < nums.length; right++) {
        odds += nums[right] & 1;
        while (odds > k) {
            odds -= nums[left] & 1;
            left++;
        }
        total += right - left + 1;           // every start in left..right is valid
    }
    return total;
}

static long countExactly(int[] nums, int k) {
    return atMost(nums, k) - atMost(nums, k - 1);
}
```

The guard on the first line matters when `k` is zero. The second call then asks for the at-most count with a budget of minus one, and without the guard the repair loop would run `left` past `right`, because no window can ever satisfy a negative budget. Defining that count as zero keeps the subtraction safe, and it is also the right answer, since no subarray has fewer than zero items.

The accumulator is a `long`. An array of 100,000 entries has about five billion subarrays, which does not fit in an `int`. The expression `nums[right] & 1` is one for odd values and zero for even ones, and it also works for negative odd numbers, where `x % 2` would give minus one.

A single pass is linear because its edges never move backward, so the pair of passes costs O(n) time and O(1) extra space.

<!-- stage: applicability -->
### When It Applies

Use this technique when the task counts subarrays with an exact value of some quantity, and a related at-most version of the same quantity is monotone under removal from either side. The invariant to state is that `atMost(k)` counts every subarray with property count at most `k`, so the difference counts those with exactly `k`.

The false friend is a direct exact-`k` window. Its left boundary is not unique, as the insight showed, and attempts to track it with one pointer give answers that look right on small inputs and fail on inputs with long quiet stretches. There is a second false friend, which is to apply the identity to a quantity that is not monotone. If removing an element can raise the quantity, as with sums over arrays that include negatives, neither at-most count is computed correctly, and prefix sums with a hash map are the tool instead.

Use it for distinct values too. The count of distinct values inside a window is monotone under removal, so `atMost` for distinct counts uses a count map exactly as in the previous lesson, and the identity gives subarrays with exactly `k` different integers.

Before coding, confirm that the quantity can be updated when an element enters and when one leaves, define the at-most count for a budget of minus one, and choose `long` for the totals.

<!-- stage: exercises -->
### Exercises

#### [Build] Exactly One Odd Number (Author exercise)
<!-- id: sw-exactly-one-odd -->

**Prerequisites.** The at-most distinct lesson for the repair loop; this lesson for the subtraction.

**Problem.** Given an integer array, return the number of contiguous subarrays that contain exactly one odd number. Compute it as `atMost(1) - atMost(0)`.

**Constraints.** 1 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. Target O(n) time and O(1) extra space.

**Example 1.** Input `nums = [1, 2, 2]`, output `3`, from `[1]`, `[1, 2]` and `[1, 2, 2]`.

**Example 2.** Input `nums = [2, 4]`, output `0`, because the array has no odd numbers.

**Hint.** For one right endpoint, how many starts keep at most one odd number in the window, and why does counting twice with different budgets isolate the exact case?

**Changed decision.** First rung of the ladder: the output changes from a length to a count, and one pass becomes the difference of two.

#### [Vary] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: sw-nice-subarrays -->

**Prerequisites.** The exercise above.

**Problem.** Given an integer array `nums` and a target `k`, return how many contiguous subarrays of `nums` contain exactly `k` odd values.

**Constraints.** 1 <= nums.length <= 50000, 1 <= nums[i] <= 10^5, and 1 <= k <= nums.length. Target O(n) time.

**Example 1.** Input `nums = [2, 1, 2, 1, 1, 2]`, `k = 2`, output `6`.

**Example 2.** Input `nums = [4, 6]`, `k = 1`, output `0`, since no odd values exist.

**Hint.** The budget is now an input. What does the subtraction use as its second budget, and does it ever need the value minus one here?

**Changed decision.** The exact count becomes a parameter, so the same two-pass structure is driven by `k` and `k - 1`.

#### [Boundary] Empty At-Most Budget (Author exercise)
<!-- id: sw-empty-budget -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary array `nums` and an integer `k >= 0`, return the number of subarrays that contain exactly `k` ones. The value `k` may be zero, so the second pass may ask for a budget of minus one.

**Constraints.** 1 <= nums.length <= 3 * 10^4, each value is 0 or 1, and 0 <= k <= nums.length. Target O(n) time and a `long` result.

**Example 1.** Input `nums = [0, 0, 0]`, `k = 0`, output `6`. Every subarray has zero ones.

**Example 2.** Input `nums = [1, 0, 1]`, `k = 3`, output `0`. The budget exceeds the number of ones available.

**Hint.** What should the at-most count return for a negative budget, and what goes wrong in the repair loop if you let it run instead?

**Changed decision.** The exact count can be zero, which forces the at-most count of a negative budget to be defined as zero.

#### [Recognize] Subarrays with K Different Integers (LeetCode 992)
<!-- id: sw-k-different-integers -->

**Prerequisites.** The three exercises above, and the at-most distinct lesson.

**Problem.** Given an integer array `nums` and a target `k`, return how many contiguous subarrays of `nums` contain exactly `k` different values.

**Constraints.** 1 <= nums.length <= 2 * 10^4 and 1 <= nums[i], k <= nums.length. Target O(n) time.

**Example 1.** Input `nums = [3, 1, 3, 1, 2]`, `k = 2`, output `7`.

**Example 2.** Input `nums = [2, 2, 2]`, `k = 2`, output `0`, because every subarray has one distinct value.

**Hint.** The quantity is now the number of distinct values in the window. Which structure from the previous lesson maintains it, and what is the second budget?

**Changed decision.** The maintained quantity changes from an odd or one count to a distinct count held in a map, with the same subtraction.
