<!-- lesson-kind: standard -->
<!-- lesson-id: kadane-state -->
## Kadane State

<!-- stage: context -->
### Finding The Best Stretch Of Daily Changes

An analytics service stores the daily change in an account balance as an array of integers. A product manager asks for the contiguous run of days with the largest total change. The run may be one day or all days, and it must contain at least one day. For the array `[-2, 1, -3, 4, -1, 2, 1, -5, 4]` the answer is 6, from the run `4, -1, 2, 1`.

The first solution most engineers write checks every run of days. It returns the right answer on a test array and then times out on a year of data for every account. The question for this lesson is simple. Can one pass over the array find the best run, and what must the pass remember at each position so that it never needs to look back?

<!-- stage: naive -->
### Checking Every Subarray With A Running Sum

A **subarray** is a contiguous part of an array, described by a start index and an end index. The direct method tries every start index. For each start it extends the end one position at a time and keeps a running sum. It records the largest sum it sees.

```java
static int bruteMaxSubarray(int[] nums) {
    int best = Integer.MIN_VALUE;
    for (int start = 0; start < nums.length; start++) {
        int sum = 0;
        for (int end = start; end < nums.length; end++) {
            sum += nums[end];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```

This method is correct. The running sum avoids adding the same values again for each end index, so it already beats the cubic method that re-adds every subarray from scratch. It starts `best` at the smallest `int`, not at zero, so an all-negative array still returns its largest value. The inner loop runs `n - start` times, so the method takes O(n^2) time and O(1) extra space.

<!-- stage: bottleneck -->
### Repeated Sums Across Neighbouring Starts

```predict
For the array `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`, the best subarray that ends at index 3 has sum 4. What is the best subarray that ends at index 4, and can you compute it from the value 4 alone, without looking at earlier indices?

The best subarray that ends at index 4 has sum 3. It extends the previous best, 4, with the new value -1. The previous best is enough, because the start of the best subarray never has to be rechosen from scratch.
```

The method above has a cost problem. For `n = 100,000` the double loop runs about five billion steps. Most of that work repeats earlier work. The subarrays that start at index 2 and at index 3 share every end position after index 3, and the method adds those shared values again for each start.

Look at one end index. Every subarray that ends at index `i` is either the single value `nums[i]` or a longer subarray that also ends at index `i - 1`, extended by `nums[i]`. The method computes both possibilities again for every `i`, although the answer for `i - 1` already contains the best longer subarray. A correct method only needs the best answer for `i - 1`, which takes O(1) to reuse. That gives O(n) time for the whole pass.

<!-- stage: insight -->
### Keeping The Best Sum That Ends Here

#### State At Each Index

**Kadane's algorithm** scans the array once and keeps two numbers. The value `bestEndingHere` is the largest sum of a non-empty subarray that must end at the current index. The value `bestOverall` is the largest sum seen at any index so far. The answer is `bestOverall` after the last index.

<!-- names: Kadane's algorithm, bestEndingHere, bestOverall -->

#### Recurrence For The Ending Sum

A subarray that ends at index `i` has only two shapes. It is the single value `nums[i]`, or it is a subarray that ends at `i - 1` plus `nums[i]`. Choose the larger sum of the two. This gives `bestEndingHere = max(nums[i], bestEndingHere + nums[i])`. The first choice starts a new subarray, and the second choice extends the old one. The second choice wins exactly when the old `bestEndingHere` is positive, because only a positive sum makes the new total larger than `nums[i]` alone.

#### Why The Invariant Holds

After each index, `bestEndingHere` equals the true best sum of a subarray that ends at that index. The recurrence preserves this fact because the best subarray ending at `i` must end at `i - 1` if it has more than one value, and extending a smaller sum can never beat extending the largest one. Every optimal subarray ends at some index, so `bestOverall` takes the largest of all these ending sums and returns the global answer.

<!-- stage: variables -->
### Meaning And Update Time Of Each Variable

The scan keeps two variables, and a loop index `i` moves from left to right.

- **`bestEndingHere`** holds the best sum of a subarray that ends at `i`, and it changes at every index.
- **`bestOverall`** holds the largest `bestEndingHere` seen so far, and it changes only when a new ending sum beats it.
- **Initial value** of both variables is `nums[0]`, because the subarray must be non-empty and the first index has only one choice.

Do not initialize either variable to zero. A zero start means an empty subarray, which the problem forbids, and it returns zero for an array of negative values.

<!-- stage: trace -->
### Tracing One Pass Over Mixed Values

The first trace follows the array `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`. At index 0 both variables equal -2. At index 1 the old ending sum is negative, so starting fresh with the value 1 beats extending to -1. At index 2 extending gives 1 + (-3) = -2, which beats starting at -3, so `bestEndingHere` becomes -2. At index 3 the old sum -2 is negative, so the value 4 beats 4 + (-2) = 2. This is the reset that discards a harmful prefix.

From index 3 the ending sum stays positive and grows through the values -1, 2 and 1 to reach 6 at index 6. The value -5 at index 7 drops the ending sum to 1, but `bestOverall` keeps 6. The final index adds 4 to give 5, which does not beat 6. The answer is 6.

```trace
{"cells":[-2,1,-3,4,-1,2,1,-5,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"bestEndingHere":-2,"bestOverall":-2},"note":"Index 0 holds -2. Both variables start at -2, because the subarray must be non-empty."},{"at":{"i":1},"vars":{"bestEndingHere":1,"bestOverall":1},"note":"Index 1 holds 1. Starting fresh gives 1, which beats extending to -1. bestEndingHere is 1. bestOverall rises to 1."},{"at":{"i":2},"vars":{"bestEndingHere":-2,"bestOverall":1},"note":"Index 2 holds -3. Extending gives -2, which beats starting fresh at -3. bestEndingHere is -2. bestOverall stays 1."},{"at":{"i":3},"vars":{"bestEndingHere":4,"bestOverall":4},"note":"Index 3 holds 4. Starting fresh gives 4, which beats extending to 2. bestEndingHere is 4. bestOverall rises to 4."},{"at":{"i":4},"vars":{"bestEndingHere":3,"bestOverall":4},"note":"Index 4 holds -1. Extending gives 3, which beats starting fresh at -1. bestEndingHere is 3. bestOverall stays 4."},{"at":{"i":5},"vars":{"bestEndingHere":5,"bestOverall":5},"note":"Index 5 holds 2. Extending gives 5, which beats starting fresh at 2. bestEndingHere is 5. bestOverall rises to 5."},{"at":{"i":6},"vars":{"bestEndingHere":6,"bestOverall":6},"note":"Index 6 holds 1. Extending gives 6, which beats starting fresh at 1. bestEndingHere is 6. bestOverall rises to 6."},{"at":{"i":7},"vars":{"bestEndingHere":1,"bestOverall":6},"note":"Index 7 holds -5. Extending gives 1, which beats starting fresh at -5. bestEndingHere is 1. bestOverall stays 6."},{"at":{"i":8},"vars":{"bestEndingHere":5,"bestOverall":6},"note":"Index 8 holds 4. Extending gives 5, which beats starting fresh at 4. bestEndingHere is 5. bestOverall stays 6."}]}
```

The second trace uses the array `[-8, -3, -6]`, where every value is negative. The ending sum restarts at each index because extending always makes a sum smaller. The best value is -3, which is the largest single element.

```trace
{"cells":[-8,-3,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"bestEndingHere":-8,"bestOverall":-8},"note":"Index 0 holds -8. Both variables start at -8, because the subarray must be non-empty."},{"at":{"i":1},"vars":{"bestEndingHere":-3,"bestOverall":-3},"note":"Index 1 holds -3. Starting fresh gives -3, which beats extending to -11. bestEndingHere is -3. bestOverall rises to -3."},{"at":{"i":2},"vars":{"bestEndingHere":-6,"bestOverall":-3},"note":"Index 2 holds -6. Starting fresh gives -6, which beats extending to -9. bestEndingHere is -6. bestOverall stays -3."}]}
```

<!-- stage: code -->
### Writing The Single Pass In Java

```java
static int maxSubarray(int[] nums) {
    int bestEndingHere = nums[0];
    int bestOverall = nums[0];
    for (int i = 1; i < nums.length; i++) {
        bestEndingHere = Math.max(nums[i], bestEndingHere + nums[i]);
        bestOverall = Math.max(bestOverall, bestEndingHere);
    }
    return bestOverall;
}
```

The loop starts at index 1 because both variables already describe index 0. Each pass makes exactly one decision between starting and extending, and then folds the result into `bestOverall`. The method reads each value once, so it takes O(n) time. It stores two integers, so it takes O(1) extra space. Java adds one hazard. The sum `bestEndingHere + nums[i]` can overflow `int` when values are near the limits, so a problem with large values needs `long` variables.

<!-- stage: applicability -->
### Checking Whether The Recurrence Applies

#### Conditions For Using Kadane State

Use this state when the goal is the best sum over a non-empty contiguous subarray with no fixed length. The invariant is that `bestEndingHere` equals the true best sum ending at the current index. It holds because addition is associative and the recurrence considers both shapes of an ending subarray. The method fits the minimum sum as well, with `min` in place of `max`.

#### False Friend And No-Go Conditions

A false friend is the best time to buy and sell a stock. It also looks for the largest gain, and a running minimum solves it in one pass. That problem chooses two positions, a buy index and a later sell index, in an array of prices. It does not choose a contiguous subarray of changes with an ending sum, so the `bestEndingHere` recurrence does not describe it. The array of day-to-day price differences connects the two problems, but the recurrence applies only after you build that difference array.

Do not use this state when the subarray length is fixed, because a sliding window handles that case. Do not use it when the objective multiplies values or when the subarray must wrap around, because those need different state.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Subarray (LeetCode 53)
<!-- id: ar-max-subarray -->

**Prerequisites.** The recurrence for `bestEndingHere` and `bestOverall` from this lesson.

**Problem.** Given an integer array `nums`, return the largest sum over all non-empty contiguous subarrays of `nums`. A subarray is a run of consecutive elements.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Subarray** is non-empty, so a single element qualifies.
- **Input** is not modified.

**Example 1.** Input `[5, -9, 6, 2, -1, 3, -8]`, output 10, from the run `6, 2, -1, 3`.

**Example 2.** Input `[-7]`, output -7, since the only subarray is the single element.

**Hint.** At each index, is the old ending sum worth keeping or should the subarray restart here?

**Changed decision.** Baseline case: replaces the double loop with one pass that reuses the previous ending sum.

#### [Vary] Minimum Subarray Sum (Author exercise)
<!-- id: ar-min-subarray-sum -->

**Prerequisites.** The maximum subarray exercise above.

**Problem.** Given an integer array `nums`, return the smallest sum over all non-empty contiguous subarrays of `nums`.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Subarray** is non-empty.
- **All-positive input** returns its smallest element.

**Example 1.** Input `[3, -4, 2, -3, 5]`, output -5, from the run `-4, 2, -3`.

**Example 2.** Input `[4, 9, 2]`, output 2, since extending any run only adds a positive value.

**Hint.** Which of the two choices, start or extend, is now the better one when the old ending sum is positive?

**Changed decision.** The goal flips from largest to smallest, so the comparison becomes `min` and extending wins when the old ending sum is negative.

#### [Boundary] All Negative (Author exercise)
<!-- id: ar-all-negative-max -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` in which every value is negative, return the largest non-empty subarray sum. Explain why starting both variables at zero returns a wrong answer.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= -1`.
- **Return value** is a value from the array, never zero.

**Example 1.** Input `[-8, -3, -6]`, output -3.

**Example 2.** Input `[-1]`, output -1.

**Hint.** What subarray does the value zero stand for, and is it allowed?

**Changed decision.** The initial value matters: zero stands for an empty subarray, so the state must start from the first element.

#### [Recognize] Maximum Absolute Sum (LeetCode 1749)
<!-- id: ar-max-abs-sum -->

**Prerequisites.** The minimum subarray exercise above.

**Problem.** Given an integer array `nums`, return the largest absolute value of the sum of any contiguous subarray. The subarray may be empty, and the empty subarray has sum 0.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 10^5`.
- **Values** satisfy `-10^4 <= nums[i] <= 10^4`.
- **Empty subarray** is allowed and has absolute sum 0.

**Example 1.** Input `[2, -5, 1, -4, 3, -2]`, output 8, from the run `-5, 1, -4`.

**Example 2.** Input `[4, -1, 3]`, output 6, from the run `4, -1, 3`.

**Hint.** The largest magnitude comes from either the largest sum or the smallest sum. Can one scan track both?

**Changed decision.** Two ending states run side by side, one for the maximum and one for the minimum, because either sign can give the largest magnitude.
