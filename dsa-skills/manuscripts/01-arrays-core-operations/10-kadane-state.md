<!-- lesson-kind: standard -->
<!-- lesson-id: kadane-state -->
## Kadane State

<!-- stage: context -->
### A Shop's Best Stretch Of Days

A shop owner keeps a ledger of daily profit, and some days are losses. She wants to know which stretch of consecutive days earned the most in total, because she is deciding when to run next year's sale. The stretch can be one day or the whole year, but it cannot skip days, since a sale runs on consecutive days.

She reads the ledger one day at a time. At every day she asks only one question: if a good stretch has to end today, is it better to carry yesterday's stretch forward or to start fresh with today alone? A long losing run behind her is a reason to start over. A winning run behind her is a reason to keep going. That one decision, repeated, is the whole method.

<!-- stage: naive -->
### Add Up Every Possible Stretch

The direct method tries every start day and every end day and adds up the days between.

```java
static int bestStretchByEnumeration(int[] profit) {
    int best = profit[0];
    for (int start = 0; start < profit.length; start++) {
        int sum = 0;
        for (int end = start; end < profit.length; end++) {
            sum += profit[end];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```

It already avoids re-adding each stretch from scratch, because the inner loop extends the running sum by one day. It tries every pair of start and end days and is easy to trust. For `[3, -4, 2, -1, 5, -6]` it finds 6, from the stretch `2, -1, 5`.

<!-- stage: bottleneck -->
### Every Start Day Is Tried Again

There are about `n * n / 2` pairs of start and end days, so the cost is O(n^2). With 100,000 days that is five billion additions. The extra space is O(1), so time is the issue. Most of those stretches are hopeless. A stretch that begins right after a long run of losses is never better than a stretch that begins one day later, yet the loops build it anyway.

The repeated work is the choice of start. Every stretch ending today is either today alone or a stretch ending yesterday, extended by today. So only one number per end day matters: the best total for a stretch that must end there. The method can carry that number forward instead of recomputing all the starts.

<!-- stage: insight -->
### Keep Only The Best Stretch Ending Here

For each position, the best subarray forced to end at that position is either the element alone or the best subarray ending at the previous position plus the element. That is the recurrence for the **ending state**: `ending = max(x, ending + x)`. Whenever the previous ending state is negative, adding it can only hurt, so the element starts a new stretch.

The overall answer is the largest ending state seen at any position, which we call the **overall best**. A stretch must end somewhere, so the best stretch is the best of the best-ending-at-each-position values. Updating the overall best after every step is therefore enough, and no earlier start ever needs to be revisited. This pair of values and the single pass that maintains them is **Kadane's algorithm**.

<!-- names: ending state, overall best, Kadane's algorithm -->

The invariant is that after reading a prefix, the ending state is the maximum sum of a non-empty subarray ending at the last element read, and the overall best is the maximum sum of any non-empty subarray inside the prefix. The first element sets both. The proof of the recurrence is short: any non-empty subarray ending at position `i` either has length one or consists of a subarray ending at `i - 1` plus the element at `i`, and choosing the best of the second kind means choosing the best ending state.

Do not confuse this with the best-gain scan from the previous topic. That scan fixes a buy day and a sell day, and the profit is a difference of two prices. Here the array already holds daily changes, and the quantity is a sum over a contiguous block. The objects look similar and the recurrences differ.

<!-- stage: variables -->
### Two Numbers And Their Starting Values

The ending state `ending` is the best sum of a stretch that must finish at the current position, and the overall best `best` is the best of those values so far. Both start from the first element, not from zero. Starting from zero would let an empty stretch win in an all-loss ledger, which breaks the rule that the stretch is non-empty. At each later element, `ending` is replaced by the larger of the element alone and the element added to the old `ending`, and then `best` is raised if `ending` exceeds it.

<!-- stage: trace -->
### One Pass Over A Mixed Ledger

Take `[3, -4, 2, -1, 5, -6]`. The first day sets the ending state to 3 and the overall best to 3. On day two the loss of 4 alone is -4, while carrying day one forward gives -1, which is better, so the ending state is -1 and the best stays at 3. On day three the profit 2 beats carrying -1 forward, which would give 1, so a new stretch starts at 2.

Day four brings -1, so the ending state is 1 and the best stays at 3. Day five brings 5, and the ending state is 6, which raises the best to 6. Day six brings -6 and the ending state falls to 0, but the best stays at 6. The answer is 6, from days three to five. The step to study is day three, where a negative ending state of -1 was dropped in favour of starting fresh.

Second ledger: `[-8, -3, -6]`, all losses. Day one sets both values to -8. Day two compares -3 alone with -11 and keeps -3, so the best becomes -3. Day three compares -6 alone with -9 and keeps -6, and the best stays at -3. The answer is -3, the largest single value, and not zero.

```trace
{"cells":[3,-4,2,-1,5,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ending":3,"best":3},"note":"Day 1 sets both values to 3."},{"at":{"i":1},"vars":{"ending":-1,"best":3},"note":"Day 2: -4 alone is -4, carrying gives -1, so carrying forward wins and the ending state is -1."},{"at":{"i":2},"vars":{"ending":2,"best":3},"note":"Day 3: 2 alone is 2, carrying gives 1, so starting fresh wins and the ending state is 2."},{"at":{"i":3},"vars":{"ending":1,"best":3},"note":"Day 4: -1 alone is -1, carrying gives 1, so carrying forward wins and the ending state is 1."},{"at":{"i":4},"vars":{"ending":6,"best":6},"note":"Day 5: 5 alone is 5, carrying gives 6, so carrying forward wins and the ending state is 6."},{"at":{"i":5},"vars":{"ending":0,"best":6},"note":"Day 6: -6 alone is -6, carrying gives 0, so carrying forward wins and the ending state is 0."}]}
```

```trace
{"cells":[-8,-3,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"ending":-8,"best":-8},"note":"Day 1 sets both values to -8."},{"at":{"i":1},"vars":{"ending":-3,"best":-3},"note":"Day 2: -3 alone is -3, carrying gives -11, so starting fresh wins and the ending state is -3."},{"at":{"i":2},"vars":{"ending":-6,"best":-3},"note":"Day 3: -6 alone is -6, carrying gives -9, so starting fresh wins and the ending state is -6."}]}
```

<!-- stage: code -->
### One Pass With Two Scalars

```java
static int maxSubarraySum(int[] nums) {               // contract: non-empty array, non-empty subarray
    int ending = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        ending = Math.max(nums[i], ending + nums[i]);
        best = Math.max(best, ending);
    }
    return best;
}

static int minSubarraySum(int[] nums) {
    int ending = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        ending = Math.min(nums[i], ending + nums[i]);
        best = Math.min(best, ending);
    }
    return best;
}
```

Both methods read the array once and keep two scalars, so the time is linear and the extra space is constant. Starting from the first element is what protects the non-empty contract. If sums can approach the `int` limit, the running values need `long`, because `ending + nums[i]` can overflow before the comparison is made. The minimum version is the same code with the comparison flipped.

<!-- stage: applicability -->
### When The Stretch Must Be Contiguous

Use Kadane's recurrence when the objective is the best sum of a contiguous block with no fixed length, and the block must be non-empty. The invariant is that the ending state is the best sum of a block forced to end here, and the overall best is the best of those. The shortcut is valid because extending a block by one element adds that element to its sum, so the best block ending at a position builds on the best block ending before it.

The false friend is the running-minimum scan for stock gain. That scan chooses two positions and reports a difference, and it fails here because the daily numbers are already the changes. Another false friend is a fixed window length, such as the best sum of exactly `k` days. That needs a sliding window, since the length is not free. And the recurrence changes if the objective is not a sum, because a product behaves differently once a negative number can flip the order, which is the next lesson.

In Java, initialize from `nums[0]` and not from `0` or `Integer.MIN_VALUE`. The first breaks all-negative input, and the second overflows when an element is added to it. Use `long` accumulators when the values or the length can be large, and decide the empty-array behaviour from the contract before writing the first line.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Subarray (LeetCode 53)
<!-- id: ar-maximum-subarray -->

**Prerequisites.** The running-extremum lesson; this lesson.

**Problem.** Given an integer array, find the contiguous non-empty subarray with the largest sum and return that sum.

**Constraints.** 1 <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4. Aim for one pass and two scalars.

**Example 1.** Input `nums = [3, -4, 2, -1, 5, -6]`, output 6, from the subarray `[2, -1, 5]`.

**Example 2.** Input `nums = [-7]`, output -7, since the subarray cannot be empty.

**Hint.** If you must end at this element, which two choices exist? When is the earlier total not worth carrying?

**Changed decision.** First rung: the choice of start is replaced by one decision per element, extend or restart.

#### [Vary] Minimum Subarray Sum (Author exercise)
<!-- id: ar-minimum-subarray-sum -->

**Prerequisites.** The maximum-subarray exercise above.

**Problem.** Return the smallest sum of a contiguous non-empty subarray. If every value is positive, the answer is the smallest element.

**Constraints.** 1 <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4. Aim for one pass.

**Example 1.** Input `nums = [2, -5, 1, -4, 3, -4]`, output -9, from `[-5, 1, -4, 3, -4]`.

**Example 2.** Input `nums = [4, 2, 7]`, output 2, because every longer stretch only adds more.

**Hint.** Which comparison flips when you want the smallest sum? What should the ending state do when carrying the old value forward makes things larger?

**Changed decision.** The maximum recurrence is replaced by the minimum recurrence while the structure stays the same.

#### [Boundary] All Negative (Author exercise)
<!-- id: ar-kadane-all-negative -->

**Prerequisites.** The two exercises above.

**Problem.** Return the best sum for an array in which every value is negative. Show that the answer is the largest single value and is not zero, and explain which initial values protect that.

**Constraints.** 1 <= nums.length <= 10^5 and every value is between -10^4 and -1. The subarray must be non-empty.

**Example 1.** Input `nums = [-8, -3, -6]`, output -3.

**Example 2.** Input `nums = [-5]`, output -5.

**Hint.** What would an initial value of zero report here? Why does starting from the first element avoid that?

**Changed decision.** The tests target the non-empty contract itself, where a zero start gives an impossible answer.

#### [Recognize] Maximum Absolute Sum of Any Subarray (LeetCode 1749)
<!-- id: ar-max-absolute-sum -->

**Prerequisites.** All three exercises above.

**Problem.** Return the largest absolute value of the sum of any contiguous subarray of the array. The empty subarray may be used, so the answer is never negative.

**Constraints.** 1 <= nums.length <= 10^5 and -10^4 <= nums[i] <= 10^4. Aim for one pass.

**Example 1.** Input `nums = [1, -3, 2, 3, -4]`, output 5, from the subarray `[2, 3]`.

**Example 2.** Input `nums = [-2, -1, -3]`, output 6, from the whole array.

**Hint.** The largest magnitude is either the largest sum or the most negative sum. What can you keep during one pass to know both?

**Changed decision.** Two ending states run side by side, one for the maximum and one for the minimum, because either can produce the largest magnitude.
