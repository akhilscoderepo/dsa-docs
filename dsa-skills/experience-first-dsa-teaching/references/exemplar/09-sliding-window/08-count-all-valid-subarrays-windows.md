<!-- lesson-kind: standard -->
<!-- lesson-id: count-all-valid-subarrays-windows -->
## Count-All-Valid-Subarrays Windows

<!-- stage: context -->
### The Affordable Stretches

A traveler writes down what she spent each day of a trip: 2, 5, 1, 3, 2, 9, 1. She has a rule of thumb that a run of consecutive days is affordable when its total is below 7. A friend asks how many different affordable runs exist in the diary. A single day counts, a two-day run counts if its sum is small enough, and the same days used in a longer run count separately.

This question counts ranges, like the exactly-K lesson, but there is no subtraction involved. The condition is a ceiling, the spending values are all positive, and the answer is a total over every valid range. Counting windows with a small product, a limited number of zeros, or a total that stays under a budget all have this shape.

<!-- stage: naive -->
### Test Every Range

List every start and every end, keep a running sum from the start, and add one whenever the sum is below the ceiling.

```java
static long countAffordableBruteForce(int[] spend, int ceiling) {
    long count = 0;
    for (int start = 0; start < spend.length; start++) {
        long sum = 0;
        for (int end = start; end < spend.length; end++) {
            sum += spend[end];
            if (sum < ceiling) count++;
        }
    }
    return count;
}
```

The code gives the right answer, and for a diary of a few hundred entries it is plenty fast.

<!-- stage: bottleneck -->
### Visiting Ranges One By One

There are n(n + 1) / 2 ranges and the method looks at each one, so the cost is quadratic. The loop even keeps going after the sum has passed the ceiling, because nothing tells it to stop, and with positive numbers every further extension is also too expensive. For 100,000 entries the loop does five billion additions, and most of them confirm a conclusion the method could already have drawn.

The cost is O(n^2) time with O(1) extra space. The waste has a precise cause: the method treats each range as an independent question, but the ranges are strongly related. If a range is affordable, every range inside it is affordable too, and that fact can be used to count many ranges at once.

<!-- stage: insight -->
### Count A Whole Family At Once

Fix the right edge and ask a collective question: which starts give an affordable range ending here? Because every value is positive, a later start only removes spending, so the affordable starts form an unbroken block that ends at `right` itself. If the earliest affordable start is `left`, then `left`, `left + 1`, and every start up to `right` all work, and none before `left` does. That is `right - left + 1` subarrays counted in a single addition, with no loop over them.

We call this **counting the ending-at-right family**. The sliding window finds `left` exactly as in the longest-valid lessons, by moving it forward only while the window is invalid. The difference is what we record. Instead of the longest window, we add the size of the window to a running total, because the window size is the number of valid ranges that end at `right`.

<!-- names: ending-at-right family, valid-start block -->

The block of valid starts is a **valid-start block**, and the addition is correct only because that block has no holes. The reason it has none is a property worth naming explicitly: validity must be monotone under removing a prefix. If the range from `s` to `right` is valid, so is the range from `s + 1` to `right`. Positivity gives us that for sums, because dropping a positive value lowers the total. If the values could be negative, dropping one could raise the total and a valid start could sit to the right of an invalid one.

One more case deserves attention. The window can shrink to nothing. If a single value is already over the ceiling, no start works for this right edge, the repair loop moves `left` past `right`, and the window size is zero. Adding zero is exactly right, and no special case is needed.

<!-- stage: variables -->
### Four Variables

The indices `left` and `right` bound the window, with `left` equal to `right + 1` when the window is empty. The value `sum` is the total of the values currently inside the window. The value `count` is the running number of valid ranges found so far, and it is a `long` because the count can reach about n^2 / 2. Nothing else is stored, and the ceiling is an input.

<!-- stage: trace -->
### One Run Through

Take the diary `[2, 5, 1, 3, 2, 9, 1]` with a ceiling of 7, so a run is affordable when its sum is below 7. Index 0 holds a 2, sum 2, and one run ends there.

Index 1 adds a 5 and the sum reaches 7, which is not below 7. The left edge drops the 2, the sum falls to 5, and the window is just index 1, so one more run ends there. Index 2 brings a 1, the sum is 6, and the window covers indices 1 and 2, so two runs end here: the 1 alone and the 5 with the 1.

Index 3 adds a 3 for a sum of 9. Dropping the 5 leaves 4, and two runs end here. Index 4 adds a 2 for a sum of 6, and three runs end at index 4, which is the largest block so far.

Index 5 holds a 9, which is above the ceiling on its own. The left edge removes the 1, the 3, the 2 and finally the 9 itself, and the window is empty. No run ends at index 5, so the count does not change. Index 6 starts afresh with a 1 and adds one run. The total is 1 + 1 + 2 + 2 + 3 + 0 + 1 = 10.

```trace
{"cells":[2,5,1,3,2,9,1],"pointers":["left","right"],"steps":[{"at":{"left":0,"right":0},"vars":{"sum":2,"count":0},"note":"Take in index 0 (value 2). The sum is 2."},{"at":{"left":0,"right":0},"vars":{"sum":2,"count":1},"note":"The starts from 0 to 0 all work, so 1 subarrays end here. Count: 1."},{"at":{"left":0,"right":1},"vars":{"sum":7,"count":1},"note":"Take in index 1 (value 5). The sum is 7. That is not below 7, so the window must be repaired."},{"at":{"left":1,"right":1},"vars":{"sum":5,"count":1},"note":"Remove index 0 (value 2) from the left; the sum is 5."},{"at":{"left":1,"right":1},"vars":{"sum":5,"count":2},"note":"The starts from 1 to 1 all work, so 1 subarrays end here. Count: 2."},{"at":{"left":1,"right":2},"vars":{"sum":6,"count":2},"note":"Take in index 2 (value 1). The sum is 6."},{"at":{"left":1,"right":2},"vars":{"sum":6,"count":4},"note":"The starts from 1 to 2 all work, so 2 subarrays end here. Count: 4."},{"at":{"left":1,"right":3},"vars":{"sum":9,"count":4},"note":"Take in index 3 (value 3). The sum is 9. That is not below 7, so the window must be repaired."},{"at":{"left":2,"right":3},"vars":{"sum":4,"count":4},"note":"Remove index 1 (value 5) from the left; the sum is 4."},{"at":{"left":2,"right":3},"vars":{"sum":4,"count":6},"note":"The starts from 2 to 3 all work, so 2 subarrays end here. Count: 6."},{"at":{"left":2,"right":4},"vars":{"sum":6,"count":6},"note":"Take in index 4 (value 2). The sum is 6."},{"at":{"left":2,"right":4},"vars":{"sum":6,"count":9},"note":"The starts from 2 to 4 all work, so 3 subarrays end here. Count: 9."},{"at":{"left":2,"right":5},"vars":{"sum":15,"count":9},"note":"Take in index 5 (value 9). The sum is 15. That is not below 7, so the window must be repaired."},{"at":{"left":3,"right":5},"vars":{"sum":14,"count":9},"note":"Remove index 2 (value 1) from the left; the sum is 14."},{"at":{"left":4,"right":5},"vars":{"sum":11,"count":9},"note":"Remove index 3 (value 3) from the left; the sum is 11."},{"at":{"left":5,"right":5},"vars":{"sum":9,"count":9},"note":"Remove index 4 (value 2) from the left; the sum is 9."},{"at":{"left":6,"right":5},"vars":{"sum":0,"count":9},"note":"Remove index 5 (value 9) from the left; the sum is 0. The window is empty."},{"at":{"left":6,"right":5},"vars":{"sum":0,"count":9},"note":"No start works for this right edge, so nothing ends here. Count: 9."},{"at":{"left":6,"right":6},"vars":{"sum":1,"count":9},"note":"Take in index 6 (value 1). The sum is 1."},{"at":{"left":6,"right":6},"vars":{"sum":1,"count":10},"note":"The starts from 6 to 6 all work, so 1 subarrays end here. Count: 10."}]}
```

<!-- stage: code -->
### The Java Blueprint

```java
static long countAffordable(int[] spend, int ceiling) {
    long count = 0;
    long sum = 0;
    int left = 0;
    for (int right = 0; right < spend.length; right++) {
        sum += spend[right];
        while (left <= right && sum >= ceiling) {   // the guard stops left at right + 1 when no window can satisfy the ceiling
            sum -= spend[left];
            left++;
        }
        count += right - left + 1;                  // size of the valid-start block, possibly zero
    }
    return count;
}
```

The guard `left <= right` is the detail that earlier lessons did not need. A ceiling that is positive can always be satisfied by shrinking, because the empty window has sum zero, which is below any positive ceiling. A ceiling of zero or less can never be satisfied, not even by the empty window, since its sum of zero is still not below the ceiling. Without the guard, `left` would run past `right` and the loop would keep subtracting values that were never added, reading beyond the array. With it, `left` stops at `right + 1`, the sum returns to zero, and the addition contributes nothing.

A ceiling smaller than the newest value but still positive is a gentler case. The window shrinks until it is empty, the sum drops to zero, and the loop ends by itself.

The count is a `long`. With 100,000 positive values and a huge ceiling, every one of the roughly 5 billion subarrays is valid, which overflows an `int`. The sum is a `long` as well, in case the values are large.

Both edges move only forward, so the work is O(n) time and O(1) extra space. Contrast it with the brute force: it examined each range separately, and this version adds a whole block of them with one subtraction of indices.

<!-- stage: applicability -->
### When It Applies

Use this technique when the problem asks how many contiguous ranges satisfy a condition, and the condition survives deleting elements from the left end. The invariant to state is that after the repair loop every start from `left` to `right` yields a valid range ending at `right`, and no earlier start does.

The first false friend is a condition that is not monotone under removing a prefix. A ceiling on a sum over values that may be negative is the classic case, and a request for subarrays with a sum exactly equal to a target is another. The code runs and returns a number, and the number is wrong. For those, prefix sums with a hash map are the correct tool. The second false friend is the longest-valid recording: it takes a maximum, and this one takes a sum, so copying the recording line without changing it answers a different question.

A mirrored version also exists. When a range stays valid after extending to the right, as with covering a set of required letters, the count of valid ranges that start at a given left edge is a different expression, namely the number of remaining ends. The extension exercise shows it. Decide which direction of monotonicity applies before choosing what to add.

Check the edge cases. Allow the window to become empty. Use `long` for the count. For products, confirm that a ceiling of one or less admits nothing, since all values are at least one, and decide what a ceiling of zero means in the contract.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Subarrays With At Most One Zero (Author exercise)
<!-- id: sw-count-at-most-one-zero -->

**Prerequisites.** The longest-valid lesson for the repair loop; this lesson for counting.

**Problem.** Given a binary array, return the number of contiguous subarrays that contain at most one zero. Add the number of valid starts at each right endpoint instead of tracking the longest window.

**Constraints.** 1 <= nums.length <= 10^5 and each value is 0 or 1. Target O(n) time and a `long` result.

**Example 1.** Input `nums = [1, 0, 0, 1]`, output `6`. Four of the ten subarrays contain two zeros and are excluded.

**Example 2.** Input `nums = [1, 1, 1]`, output `6`. Every subarray qualifies.

**Hint.** At each right endpoint, after the zero counter is repaired, how many starts give a valid subarray, and which expression computes that without a loop?

**Changed decision.** First rung of the ladder: the recorded quantity changes from a maximum length to a running sum of window sizes.

#### [Vary] Count Subarrays With Sum Below K For Positive Values (Author exercise)
<!-- id: sw-count-sum-below-k -->

**Prerequisites.** The exercise above.

**Problem.** Given an array of positive integers and an integer `k`, return the number of contiguous subarrays whose sum is strictly less than `k`.

**Constraints.** 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^4, and 0 <= k <= 10^9. Target O(n) time and a `long` result.

**Example 1.** Input `nums = [1, 2, 3]`, `k = 4`, output `4`, from `[1]`, `[2]`, `[3]` and `[1, 2]`.

**Example 2.** Input `nums = [5, 6]`, `k = 5`, output `0`. A single value equal to `k` is not strictly below it.

**Hint.** Why does dropping the leftmost element never increase the sum, and what in the constraints guarantees it?

**Changed decision.** The violation is a running sum over positive values, and the monotonicity that makes the block of starts unbroken comes from positivity.

#### [Boundary] K At The Minimum (Author exercise)
<!-- id: sw-k-at-minimum -->

**Prerequisites.** The two exercises above.

**Problem.** Use the same rule as the previous exercise, but now `k` may be smaller than or equal to every element, so a single element can already be too large. Return the count of subarrays with sum strictly less than `k`, and make sure the window can become empty.

**Constraints.** 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^9, and -10^9 <= k <= 10^9. Sums can exceed `int`, so use `long`. Target O(n) time.

**Example 1.** Input `nums = [3, 4, 5]`, `k = 3`, output `0`. Every single element is too large, so every window empties.

**Example 2.** Input `nums = [1, 1, 1, 1]`, `k = 1000`, output `10`. The window never shrinks and every subarray counts.

**Hint.** What does the repair loop do when the limit is so low that even the empty window fails it, and which guard stops `left` from running past `right`?

**Changed decision.** The limit can fall below every element, so the window must be allowed to shrink to empty and contribute zero.

#### [Recognize] Subarray Product Less Than K (LeetCode 713)
<!-- id: sw-product-less-than-k -->

**Prerequisites.** The three exercises above.

**Problem.** All values in `nums` are positive integers. Return how many contiguous subarrays have a product strictly smaller than `k`.

**Constraints.** 1 <= nums.length <= 3 * 10^4, 1 <= nums[i] <= 1000, and 0 <= k <= 10^6. Target O(n) time.

**Example 1.** Input `nums = [4, 2, 5, 3]`, `k = 30`, output `7`.

**Example 2.** Input `nums = [1, 2, 3]`, `k = 1`, output `0`. Every product is at least one, so a limit of one admits nothing.

**Hint.** What replaces the running sum, how do you remove a value from a product, and what happens when `k` is at most one?

**Changed decision.** The aggregate becomes a product, which is undone by division, and a limit of one or less admits nothing.

#### [Extend] Number of Substrings Containing All Three Characters (LeetCode 1358)
<!-- id: sw-three-characters -->

**Prerequisites.** The four exercises above, and the minimum-cover lesson.

**Problem.** The string `s` contains only the letters `a`, `b` and `c`. Count the substrings that contain each of the three letters at least once.

**Constraints.** 3 <= s.length <= 5 * 10^4 and `s` contains only `a`, `b` and `c`. Target O(n) time.

**Example 1.** Input `s = "cabbac"`, output `7`.

**Example 2.** Input `s = "bbbcc"`, output `0`, because no `a` exists.

**Hint.** Here a range stays valid when it grows to the right. For a fixed right edge, which starts are valid, and how does the number of them relate to the repaired left edge?

**Changed decision.** The monotonicity runs the other way, so the number added at each step is the count of starts before the repaired left edge, not the window size.
