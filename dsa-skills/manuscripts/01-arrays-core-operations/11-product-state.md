<!-- lesson-kind: standard -->
<!-- lesson-id: product-state -->
## Product State

<!-- stage: context -->
### A Chain Of Amplifiers And Inverters

A signal passes through a chain of devices, and each device multiplies the signal by a number. Most devices amplify by a factor above 1 or shrink by a factor between 0 and 1. A few are inverters, whose factor is negative and which flip the signal upside down. One broken device multiplies by zero and kills the signal entirely.

An engineer is allowed to pick a stretch of consecutive devices and run the signal through only those. She wants the stretch that produces the strongest positive output. The trouble is that a terrible-looking stretch can turn into the best one after a single inverter, because a large negative signal becomes a large positive one when it is flipped. The strongest output depends on the weakest one seen so far.

<!-- stage: naive -->
### Multiply Out Every Stretch

The direct approach tries every start and end and keeps the largest product.

```java
static int bestProductByEnumeration(int[] factors) {
    int best = factors[0];
    for (int start = 0; start < factors.length; start++) {
        int product = 1;
        for (int end = start; end < factors.length; end++) {
            product *= factors[end];
            best = Math.max(best, product);
        }
    }
    return best;
}
```

The inner loop extends the running product by one device, so each stretch is not recomputed from scratch. For `[2, -1, 3, -2, 2]` it finds 24, from the whole chain, where two inverters cancel.

<!-- stage: bottleneck -->
### Every Pair Of Ends Is Tried

There are about `n * n / 2` pairs of start and end, so the time is O(n^2), which is five billion multiplications for 100,000 devices. The extra space is O(1). The sum version of this problem has a one-number shortcut, so it is natural to try the same one here: keep the best product ending at each position and extend it.

That shortcut fails on `[2, -1, 3, -2, 2]`. The best product ending at the third device is 3, because carrying -1 forward would give -3. But at the fourth device, the correct answer extends the stretch whose product is -6, the worst one, and multiplying it by -2 gives 12. A method that threw away -6 has no way to produce 12. The repeated work can be removed, but the single number cannot carry enough information.

<!-- stage: insight -->
### Track Both Extremes At Each Step

Multiplying by a positive number keeps the order of values: bigger stays bigger. Multiplying by a negative number reverses it: the most negative value becomes the most positive. So the product ending at the current position is best when built from the best or the worst ending at the previous position, depending on the sign of the new factor.

Keep two values. The **maximum state** is the largest product of a non-empty stretch ending at the current position, and the **minimum state** is the smallest. For a new factor `x`, the new maximum is the largest of `x` alone, `x * maximum`, and `x * minimum`, and the new minimum is the smallest of the same three. When `x` is negative, the old maximum and minimum trade places, which is the **role swap**: the favourable history becomes the unfavourable one and the reverse.

<!-- names: maximum state, minimum state, role swap -->

The invariant is that after each element, the maximum state and minimum state are the true largest and smallest products over every non-empty stretch ending at that element. Each stretch ending at `x` is either `x` alone or `x` times a stretch ending one step earlier, and the product of `x` with a stretch is largest at the stretch with the extreme value that suits the sign of `x`. So only the two extremes of the previous step are needed.

A zero is handled by the same rule. Both states become zero, because `x` alone is zero and multiplying anything by zero is zero. The next element then starts fresh through the "alone" choice, so the stretch restarts without any special branch. The overall answer is the largest maximum state seen.

<!-- stage: variables -->
### A High, A Low And A Best

The value `hi` is the maximum state and `lo` is the minimum state, both for stretches ending at the current position. The value `best` is the largest `hi` seen so far. All three start from the first element. For each new element, if it is negative, swap `hi` and `lo` first. Then set `hi` to the larger of the element and `hi * element`, set `lo` to the smaller of the element and `lo * element`, and raise `best` from `hi`. The swap is done before multiplying, so each product uses the extreme that the sign needs.

<!-- stage: trace -->
### Inverters Make The Worst Become The Best

Take `[2, -1, 3, -2, 2]`. The first device sets the high and the low to 2. The inverter -1 swaps them, which changes nothing here, and then the high becomes -1 and the low becomes -2, because -1 alone beats -2. The 3 raises the high to 3 and drops the low to -6, which is 3 times the old low of -2. The best is now 3.

The next device, -2, is the interesting step. It swaps the high and low, so the old low of -6 becomes the high, and multiplying gives 12 as the new high and -6 for the new low. The best jumps to 12. The last device, 2, raises the high to 24 and the low to -12, and the best becomes 24. The worst product from two steps earlier became the best answer, which is exactly what a single carried number would have lost.

Second chain: `[3, 0, -2, 4]`. The 3 gives high and low of 3. The zero collapses both to 0, so the stretch is restarted. The -2 swaps zeros and gives a high of 0 and a low of -2. The 4 gives a high of 4, since 4 alone beats 0, and a low of -8. The best is 4. The zero acted as a clean cut with no special case.

```trace
{"cells":[2,-1,3,-2,2],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"high":2,"low":2,"best":2},"note":"Device 1 sets the high and the low to 2."},{"at":{"i":1},"vars":{"high":-1,"low":-2,"best":2},"note":"Device 2 multiplies by -1. The negative factor swaps high and low first. The high is -1, the low is -2, the best is 2."},{"at":{"i":2},"vars":{"high":3,"low":-6,"best":3},"note":"Device 3 multiplies by 3. The high is 3, the low is -6, the best is 3."},{"at":{"i":3},"vars":{"high":12,"low":-6,"best":12},"note":"Device 4 multiplies by -2. The negative factor swaps high and low first. The high is 12, the low is -6, the best is 12."},{"at":{"i":4},"vars":{"high":24,"low":-12,"best":24},"note":"Device 5 multiplies by 2. The high is 24, the low is -12, the best is 24."}]}
```

```trace
{"cells":[3,0,-2,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"high":3,"low":3,"best":3},"note":"Device 1 sets the high and the low to 3."},{"at":{"i":1},"vars":{"high":0,"low":0,"best":3},"note":"Device 2 multiplies by 0. The high is 0, the low is 0, the best is 3."},{"at":{"i":2},"vars":{"high":0,"low":-2,"best":3},"note":"Device 3 multiplies by -2. The negative factor swaps high and low first. The high is 0, the low is -2, the best is 3."},{"at":{"i":3},"vars":{"high":4,"low":-8,"best":4},"note":"Device 4 multiplies by 4. The high is 4, the low is -8, the best is 4."}]}
```

<!-- stage: code -->
### Swap, Then Extend Both Ends

```java
static int maxProduct(int[] nums) {                   // contract: non-empty, products fit in int
    int hi = nums[0], lo = nums[0], best = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        if (x < 0) { int t = hi; hi = lo; lo = t; }
        hi = Math.max(x, hi * x);
        lo = Math.min(x, lo * x);
        best = Math.max(best, hi);
    }
    return best;
}

static int longestPositiveProduct(int[] nums) {       // sign and length state, not products
    int pos = 0, neg = 0, best = 0;                   // longest stretch ending here with a positive / negative product
    for (int x : nums) {
        if (x == 0) { pos = 0; neg = 0; }
        else if (x > 0) { pos = pos + 1; neg = neg > 0 ? neg + 1 : 0; }
        else { int newPos = neg > 0 ? neg + 1 : 0; neg = pos + 1; pos = newPos; }
        best = Math.max(best, pos);
    }
    return best;
}
```

Both methods read the array once and keep a few scalars, so they take linear time and constant extra space. The first multiplies actual values, so the product must fit in `int`, and a `long` is safer when it might not. The second stores lengths instead of products, so it cannot overflow, and shows that the idea is about favourable and unfavourable histories and not about multiplication itself.

<!-- stage: applicability -->
### When A Negative Can Reverse The Order

Use a pair of extreme states when the objective is a contiguous product, or any measure where a negative factor reverses which history is better. The invariant is that the maximum state and minimum state are the true extremes over stretches ending here, and a negative factor swaps them before the multiplication.

The false friend is the sum version of Kadane's recurrence. Addition does not reverse order: a larger number plus `x` is always larger than a smaller number plus `x`, so one ending state is enough. A second false friend is a product over non-negative numbers, such as scaling factors above zero, where the minimum state is never needed and the best product ending here is just the carried product. Counting the negatives and splitting at zeros is also possible, but the two-state method is simpler to get right and works in one pass.

Java details are the swap through a temporary variable, the overflow of `int` products for long chains, and the zero case, which needs no branch in the product version. If a problem asks for the length of a stretch with a given sign, keep lengths per sign and avoid multiplying at all.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Product Subarray (LeetCode 152)
<!-- id: ar-maximum-product-subarray -->

**Prerequisites.** The Kadane state lesson; this lesson.

**Problem.** Given an integer array, find the contiguous non-empty subarray with the largest product and return that product.

**Constraints.** 1 <= nums.length <= 2 * 10^4 and -10 <= nums[i] <= 10; the answer fits in a 32-bit integer. Aim for one pass.

**Example 1.** Input `nums = [2, -1, 3, -2, 2]`, output 24, from the whole array.

**Example 2.** Input `nums = [-4]`, output -4, because the subarray cannot be empty.

**Hint.** If the new factor is negative, which earlier product do you want to multiply? What must you keep besides the largest product?

**Changed decision.** First rung: a second ending state, the minimum, is added because a negative factor reverses the order.

#### [Vary] Product Ending Here (Author exercise)
<!-- id: ar-product-ending-here -->

**Prerequisites.** The maximum-product exercise above.

**Problem.** Return the largest product of a non-empty subarray that is forced to include the final element. No overall best is kept, only the pair of ending states.

**Constraints.** 1 <= nums.length <= 2 * 10^4 and -10 <= nums[i] <= 10; the answer fits in a 32-bit integer.

**Example 1.** Input `nums = [2, -3, 4, -1]`, output 24, from the whole array.

**Example 2.** Input `nums = [3, 0, -2]`, output 0, since every stretch ending at -2 that includes the zero is zero and the other is -2.

**Hint.** Which of the two running values is the answer at the end? Do you still need the best seen so far?

**Changed decision.** The overall best is dropped, but the maximum and minimum ending states remain.

#### [Boundary] Zeros And Negatives In Maximum Product (LeetCode 152)
<!-- id: ar-product-zeros-negatives -->

**Prerequisites.** The two exercises above.

**Problem.** Dry-run the maximum-product method on `[-2, 3, -4]` and on `[0, -2]`. Report the high, the low and the best after every element, and explain how the zero restarts the stretch without a special branch.

**Constraints.** The arrays are short, with values between -10 and 10. The states are the same ones as in the lesson, with the swap done before multiplying.

**Example 1.** Input `nums = [-2, 3, -4]`, output a best of 24, with the low reaching -6 before the last element turns it into the high.

**Example 2.** Input `nums = [0, -2]`, output a best of 0, with the low of -2 never becoming the answer.

**Hint.** What are high and low after the first element? What does a zero do to both, and why does the next element still start a fresh stretch?

**Changed decision.** The tests target the two events that break the one-number shortcut, a negative that flips the order and a zero that kills the product.

#### [Recognize] Maximum Length of Subarray With Positive Product (LeetCode 1567)
<!-- id: ar-positive-product-length -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array, return the length of the longest subarray whose product is positive. Zero breaks any stretch, and the products themselves are never needed.

**Constraints.** 1 <= nums.length <= 10^5 and -10^9 <= nums[i] <= 10^9. The product must not be computed, because it could overflow.

**Example 1.** Input `nums = [-1, 2, -3, 4, -5]`, output 4, from `[2, -3, 4, -5]`.

**Example 2.** Input `nums = [-2, 0, 3]`, output 1, from `[3]`.

**Hint.** What if you only remember the longest stretch ending here with a positive product and the longest with a negative one? What does a negative element do to those two lengths?

**Changed decision.** The state changes from products to sign and length, but a negative still swaps the favourable and unfavourable histories.
