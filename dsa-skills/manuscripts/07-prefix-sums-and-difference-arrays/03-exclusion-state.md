<!-- lesson-kind: standard -->
<!-- lesson-id: exclusion-state -->
## Combine Totals From Both Sides

<!-- stage: context -->
### Each Rule Needs Every Other Rule

A pricing engine applies up to 100,000 rules to an order, and each rule scales the price by a multiplier. The team wants a report that shows, for every rule, the combined multiplier of all the other rules. That report tells them what the price would be without that one rule.

One rule has the multiplier 0, because it makes an item free. A shortcut that divides the total by one multiplier fails on that rule. The task is to compute, for every position, a combined value of all other positions in one linear pass.

<!-- stage: naive -->
### Multiplying All The Other Values

The direct method multiplies every value except the one at index `i`, for every `i`.

```java
static long[] productsExceptSelf(int[] nums) {
    long[] out = new long[nums.length];
    for (int i = 0; i < nums.length; i++) {
        long product = 1;
        for (int j = 0; j < nums.length; j++) {
            if (j != i) product *= nums[j];
        }
        out[i] = product;
    }
    return out;
}
```

For `[2, 3, 4, 5]` the method returns `[60, 40, 30, 24]`. Index 0 multiplies 3, 4 and 5, and index 1 multiplies 2, 4 and 5.

```predict
The array holds 100,000 values. How many multiplications does `productsExceptSelf` perform?

It performs 100,000 times 99,999 multiplications, which is 9,999,900,000. Each of the n positions loops over the other n - 1 values, so the cost is O(n^2).
```

<!-- stage: bottleneck -->
### Neighbouring Answers Share Most Factors

The answer for index 1 and the answer for index 2 share almost all their factors. Both contain the values at indexes 0 and 3 onward, and they differ only by `nums[1]` and `nums[2]`. The inner loop multiplies these shared values from scratch for every index, so the method costs O(n^2).

A shortcut exists for sums, because `total - nums[i]` is the sum of all other values. The matching shortcut for products is `total / nums[i]`. It fails when `nums[i]` is 0, and Java throws an `ArithmeticException` for an integer division by zero. It also fails when the total is 0 for another reason, because the quotient then hides which factor caused the zero.

<!-- stage: insight -->
### Multiply Left Of Each Index, Then Right

The answer for index `i` splits into two independent parts. One part is the product of the values before `i`. The other part is the product of the values after `i`. The method computes the two parts in two passes, and it never divides.

#### The Left Pass

The **left pass** walks from index 0 upward. Before it handles index `i`, a running variable holds the product of `nums[0]` through `nums[i - 1]`. The pass stores that value in `out[i]` and then multiplies the running variable by `nums[i]`. The running variable starts at 1, which is the neutral value of a product, so `out[0]` is the product of no values.

#### The Right Pass

The values after index `i` form a **suffix** of the array, which is a run of values that ends at the last index. The **right pass** walks from the last index downward with a variable `suffix`, which holds the product of the values after `i`. It multiplies `out[i]` by `suffix` and then multiplies `suffix` by `nums[i]`. After the pass, `out[i]` equals the left product times the right product.

<!-- names: left pass, right pass, suffix -->

#### The Cost Of Two Passes

Each pass costs n multiplications, so the method costs O(n) time. The result array is the output itself, so the extra memory beyond it is one `suffix` variable, O(1). The same two passes work for any combining operation that has a neutral value, such as a sum or a product.

<!-- stage: variables -->
### Four Names And Their Roles

The two passes share one array and use two running variables.

- **out** is the result array, and it holds the left product after the first pass.
- **running** is the product of the values before the current index during the left pass.
- **suffix** is the product of the values after the current index during the right pass.
- **i** is the current index, and the right pass counts it down.

Both running variables start at 1. A product over no values must be 1, because multiplying by 1 changes nothing.

<!-- stage: trace -->
### Two Arrays Through Both Passes

#### Four Positive Values

The input is `[2, 3, 4, 5]`. The left pass fills `out` with `[1, 2, 6, 24]`. The right pass starts at index 3 with `suffix = 1`. It multiplies each `out[i]` by `suffix` and then multiplies `suffix` by `nums[i]`. The array ends as `[60, 40, 30, 24]`.

```trace
{"cells":[2,3,4,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"running":"1"},"note":"The left pass starts with running = 1, the product of no values."},{"at":{"i":0},"vars":{"out":"[1, 0, 0, 0]","running":"2"},"note":"Store the product before index 0 and multiply running by 2."},{"at":{"i":1},"vars":{"out":"[1, 2, 0, 0]","running":"6"},"note":"Store the product before index 1 and multiply running by 3."},{"at":{"i":2},"vars":{"out":"[1, 2, 6, 0]","running":"24"},"note":"Store the product before index 2 and multiply running by 4."},{"at":{"i":3},"vars":{"out":"[1, 2, 6, 24]","running":"120"},"note":"Store the product before index 3 and multiply running by 5."},{"at":{"i":4},"vars":{"out":"[1, 2, 6, 24]","suffix":"1"},"note":"The right pass starts past the last index with suffix = 1."},{"at":{"i":3},"vars":{"out":"[1, 2, 6, 24]","suffix":"5"},"note":"Multiply out[3] by the product after it, then multiply suffix by 5."},{"at":{"i":2},"vars":{"out":"[1, 2, 30, 24]","suffix":"20"},"note":"Multiply out[2] by the product after it, then multiply suffix by 4."},{"at":{"i":1},"vars":{"out":"[1, 40, 30, 24]","suffix":"60"},"note":"Multiply out[1] by the product after it, then multiply suffix by 3."},{"at":{"i":0},"vars":{"out":"[60, 40, 30, 24]","suffix":"120"},"note":"Multiply out[0] by the product after it, then multiply suffix by 2."}]}
```

#### A Zero In The Input

The input is `[1, 0, 3, 4]`. The left pass produces `[1, 1, 0, 0]`, because the zero enters the running product after index 1. The right pass fixes index 1, where both sides avoid the zero. Every other answer keeps the factor 0 and stays 0. The result is `[0, 12, 0, 0]`.

```trace
{"cells":[1,0,3,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"running":"1"},"note":"The left pass starts with running = 1, the product of no values."},{"at":{"i":0},"vars":{"out":"[1, 0, 0, 0]","running":"1"},"note":"Store the product before index 0 and multiply running by 1."},{"at":{"i":1},"vars":{"out":"[1, 1, 0, 0]","running":"0"},"note":"Store the product before index 1 and multiply running by 0."},{"at":{"i":2},"vars":{"out":"[1, 1, 0, 0]","running":"0"},"note":"Store the product before index 2 and multiply running by 3."},{"at":{"i":3},"vars":{"out":"[1, 1, 0, 0]","running":"0"},"note":"Store the product before index 3 and multiply running by 4."},{"at":{"i":4},"vars":{"out":"[1, 1, 0, 0]","suffix":"1"},"note":"The right pass starts past the last index with suffix = 1."},{"at":{"i":3},"vars":{"out":"[1, 1, 0, 0]","suffix":"4"},"note":"Multiply out[3] by the product after it, then multiply suffix by 4."},{"at":{"i":2},"vars":{"out":"[1, 1, 0, 0]","suffix":"12"},"note":"Multiply out[2] by the product after it, then multiply suffix by 3."},{"at":{"i":1},"vars":{"out":"[1, 12, 0, 0]","suffix":"0"},"note":"Multiply out[1] by the product after it, then multiply suffix by 0."},{"at":{"i":0},"vars":{"out":"[0, 12, 0, 0]","suffix":"0"},"note":"Multiply out[0] by the product after it, then multiply suffix by 1."}]}
```

<!-- stage: code -->
### Two Passes In Java

```java
static long[] productsExceptSelf(int[] nums) {
    int n = nums.length;
    long[] out = new long[n];
    long running = 1;
    for (int i = 0; i < n; i++) {
        out[i] = running;
        running *= nums[i];
    }
    long suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        out[i] *= suffix;
        suffix *= nums[i];
    }
    return out;
}
```

Each loop stores a value before it updates the running variable, so index `i` never multiplies itself in. The code uses no division, so a zero causes no special case. Java multiplies `long` values without an error on overflow. The values must be small enough that the product fits in 63 bits, and the exercise limits state the bound.

<!-- stage: applicability -->
### When Two Passes Replace Division

#### The Invariant

The invariant of the left pass is that `running` equals the product of `nums[0]` through `nums[i - 1]` at the start of step `i`. The invariant of the right pass is that `out[i]` holds the left product, and `suffix` holds the product of `nums[i + 1]` through `nums[n - 1]`. The two invariants together make the final product exact.

#### The False Friend

Division by the total is the false friend. It looks shorter, and it works for an array with no zero. A zero makes the division throw, and two zeros make every answer 0 while the quotient formula cannot tell the cases apart. Division also needs exact divisibility, which fails after an overflow.

#### Conditions That Break The Fit

The operation must be associative, so the grouping of the factors may not change the result. It also needs a neutral value for the empty side. Sum and product meet both conditions. Maximum and minimum do too, once the contract names a value for an empty side. A median does not, and it needs a different method.

<!-- stage: exercises -->
### Exercises

#### [Build] Sum Except Self (Author exercise)
<!-- id: ps-sum-except-self -->

**Prerequisites.** The long type from the first lesson. The left pass and the right pass are optional here, because a total makes this version shorter.

**Problem.** Given an integer array `nums`, return an array `out` where `out[i]` is the sum of all values of `nums` except `nums[i]`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Return type** is `long[]`, because a sum can exceed the `int` range.
- **One value** gives the sum of no values, which is 0.

**Example 1.** Input `nums = [1,2,3,4]`, output `[9,8,7,6]`.

**Example 2.** Input `nums = [5]`, output `[0]`.

**Hint.** For sums, the value `total - nums[i]` gives the answer. What type must `total` have?

**Changed decision.** Basic case: an operation with an inverse can use the total, and the later exercises show where that fails.

#### [Vary] Product Of Array Except Self (LeetCode 238)
<!-- id: ps-product-except-self -->

**Prerequisites.** The first exercise and both passes of this lesson.

**Problem.** Given an integer array `nums`, return an array `out` where `out[i]` is the product of all values of `nums` except `nums[i]`. Do not use division.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 10^5`.
- **Values** are `int` values with `-30 <= nums[i] <= 30`.
- **Fit** guarantees that every product fits in a 32-bit `int`.
- **Extra space** is O(1) beyond the output array.

**Example 1.** Input `nums = [1,2,3,4]`, output `[24,12,8,6]`.

**Example 2.** Input `nums = [-1,1,0,-3,3]`, output `[0,0,9,0,0]`.

**Hint.** Store the product before `i` in the output on a first pass. On a second pass from the right, multiply by a running product of the values after `i`.

**Changed decision.** The operation changes from sum to product, so the total shortcut disappears and only the two passes remain.

#### [Boundary] Zeros In The Product (LeetCode 238)
<!-- id: ps-product-zeros -->

**Prerequisites.** The second exercise above.

**Problem.** Given an integer array `nums`, return an array `out` where `out[i]` is the product of all values except `nums[i]`, as a `long`. The array may hold zero, one or several zeros. The contract differs from LeetCode 238 in the value range, the return type and the explicit zeros.

**Constraints.** The limits are:
- **Length** is `2 <= nums.length <= 9`.
- **Values** are `int` values with `-100 <= nums[i] <= 100`.
- **Fit** holds because `100^8` is below the `long` maximum.
- **Division** is not allowed.

**Example 1.** Input `nums = [0,4,5]`, output `[20,0,0]`.

**Example 2.** Input `nums = [0,0,3]`, output `[0,0,0]`.

**Hint.** With exactly one zero, which index has a nonzero answer? With two zeros, which factor is present in every answer?

**Changed decision.** Zeros are the edge case, and the two passes handle them without any counting of zeros.

#### [Recognize] Prefix And Suffix Maximums (Author exercise)
<!-- id: ps-side-maximums -->

**Prerequisites.** All exercises above. The maximum of no values is not defined, so the contract names a replacement value.

**Problem.** Given an array `nums` of non-negative integers, return two arrays `left` and `right`. The entry `left[i]` is the largest value among `nums[0]` through `nums[i - 1]`, and `right[i]` is the largest value among `nums[i + 1]` through `nums[n - 1]`. Use -1 for a side with no values.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `0 <= nums[i] <= 10^9`.
- **Empty side** has the value -1.
- **Return value** is a two row array with `left` first.

**Example 1.** Input `nums = [3,1,4]`, output `[[-1,3,3],[4,4,-1]]`.

**Example 2.** Input `nums = [7]`, output `[[-1],[-1]]`.

**Hint.** Replace the product by `Math.max`. What value plays the role of the neutral 1 for a maximum over non-negative numbers?

**Changed decision.** The combining operation is a maximum, which has no inverse, so only the two passes work.
