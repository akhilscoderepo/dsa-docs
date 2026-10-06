<!-- lesson-kind: standard -->
<!-- lesson-id: contribution-counting -->
## Count Subarrays By Their Minimum

<!-- stage: context -->
### A Cost Charged To Every Window

A capacity model charges each window of consecutive hours the request count of its quietest hour. The model adds the charges of all windows into one number for the whole day. A log of 100000 hours has about 5 x 10^9 windows, so the model cannot compute the charges one by one.

The previous lesson gave every window a single owner. The lesson answers one question. How does that ownership turn a sum over billions of windows into a sum over 100000 indices?

<!-- stage: naive -->
### Add The Minimum Of Every Window

The direct approach fixes the last index `r` of a window and extends the first index `l` backward. It keeps the running minimum and adds it to the total after each extension.

```java
static long sumOfMinimumsByWindows(int[] nums) {
    long total = 0;
    for (int r = 0; r < nums.length; r++) {
        int lowest = Integer.MAX_VALUE;
        for (int l = r; l >= 0; l--) {
            lowest = Math.min(lowest, nums[l]);
            total += lowest;
        }
    }
    return total;
}
```

The method is correct. For the readings 2, 5, 3, 5, 1, it visits 15 windows and adds 35. The 1 is the minimum of every window that ends at the last position, so it appears 5 times in the total.

<!-- stage: bottleneck -->
### The Sum Has Too Many Terms

```predict
A log holds 100000 hours. About how many additions does the direct method perform?

About 5 x 10^9. It adds one term per window, and the number of windows is 100000 x 100001 / 2.
```

The direct method takes O(n^2) time for `n` hours. The total itself is not the problem, because the answer is a single number. The problem is the number of terms. In the readings 2, 5, 3, 5, 1, the value 1 is added five times, and every one of those additions repeats the same value.

A value that is the minimum of many windows can be added once, multiplied by the number of those windows. Counting those windows needs the boundaries and the tie decision from the previous lessons.

<!-- stage: insight -->
### Add Each Value Once Times Its Count

The total over windows can be regrouped by index. Each window belongs to one index, and the index holds the window's minimum value.

<!-- names: contribution, start choices, end choices -->

#### Regroup The Sum By Index

By the ownership rule of the previous lesson, every window has one owner, and the owner holds the window's minimum. So the sum of all window minimums equals the sum, over every index `i`, of `nums[i]` times the number of windows that `i` owns. The **contribution** of index `i` is `nums[i]` times that number. The regrouped sum has `n` terms, where the direct sum has `n * (n + 1) / 2`.

#### Two Independent Choices

Index `i` owns the window from `l` to `r` when `l` lies in `left + 1` through `i` and `r` lies in `i` through `right - 1`. Here `left` is the nearest strictly smaller index on the left, and `right` is the nearest smaller-or-equal index on the right. The number of **start choices** is `i - left`. The number of **end choices** is `right - i`. A start never restricts an end, because each boundary condition looks at one side of `i` only. The count of owned windows is therefore the product of the two numbers.

The product is valid only after the tie decision is fixed. If both boundaries stopped at strictly smaller values, a window with equal minimum values would count once per equal index, and the product would count it twice.

#### Widen Before You Multiply

The two distances are `int` values. Their product can exceed the range of `int` once `n` is large, because a minimum near the middle of a long array has about `n / 2` choices on each side. Java computes `int * int` in `int` and wraps silently. The code casts one factor to `long` before the multiplication. When the problem asks for a remainder, the code reduces after the `long` product, and never reduces an overflowed `int`.

Sums of maximums follow the same plan with the comparisons reversed. Only the boundaries change, and the contribution formula stays the same.

<!-- stage: variables -->
### What The Sum Needs

The method tracks six pieces of state.

- **left** is the nearest strictly smaller index before `i`, or `-1`.
- **right** is the nearest smaller-or-equal index after `i`, or `n`.
- **start choices** equals `i - left[i]`, the number of valid first indices.
- **end choices** equals `right[i] - i`, the number of valid last indices.
- **contribution** equals `nums[i]` times the start choices times the end choices.
- **total** is the running sum of all contributions, kept as a `long`.

The boundaries come from the single stack pass of the previous lesson. This lesson adds only the multiplication and the sum.

<!-- stage: trace -->
### Following The Sum Across Indices

#### A Sum Of Minimums

The first trace reads 2, 5, 3, 5, 1. Each step shows one index, its two boundaries, its choices and its contribution. The 5 at index 1 has `left = 0` and `right = 2`, so it has one start choice and one end choice. The 3 at index 2 has two choices on each side, so it owns 4 windows and contributes 12. The 1 at index 4 has no smaller value on the left, so it has 5 start choices.

```trace
{"cells":[2,5,3,5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":-1,"right":4,"starts":1,"ends":4,"total":8},"note":"Index 0 holds 2 with 1 start choices and 4 end choices, so it owns 4 windows and adds 8."},{"at":{"i":1},"vars":{"left":0,"right":2,"starts":1,"ends":1,"total":13},"note":"Index 1 holds 5 with 1 start choices and 1 end choices, so it owns 1 windows and adds 5."},{"at":{"i":2},"vars":{"left":0,"right":4,"starts":2,"ends":2,"total":25},"note":"Index 2 holds 3 with 2 start choices and 2 end choices, so it owns 4 windows and adds 12."},{"at":{"i":3},"vars":{"left":2,"right":4,"starts":1,"ends":1,"total":30},"note":"Index 3 holds 5 with 1 start choices and 1 end choices, so it owns 1 windows and adds 5."},{"at":{"i":4},"vars":{"left":-1,"right":5,"starts":5,"ends":1,"total":35},"note":"Index 4 holds 1 with 5 start choices and 1 end choices, so it owns 5 windows and adds 5."},{"at":{"i":5},"vars":{"total":35},"note":"All 5 indices are added, and the total is 35."}]}
```

#### A Sum Of Maximums

The second trace reads the same readings and sums the maximum of each window. The boundaries now stop at larger values. The left side stops at a strictly greater value, and the right side stops at a greater-or-equal value. The 5 at index 3 owns 8 windows, which is 4 start choices times 2 end choices, and it contributes 40.

```trace
{"cells":[2,5,3,5,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":-1,"right":1,"starts":1,"ends":1,"total":2},"note":"Index 0 holds 2 with 1 start choices and 1 end choices, so it owns 1 windows and adds 2."},{"at":{"i":1},"vars":{"left":-1,"right":3,"starts":2,"ends":2,"total":22},"note":"Index 1 holds 5 with 2 start choices and 2 end choices, so it owns 4 windows and adds 20."},{"at":{"i":2},"vars":{"left":1,"right":3,"starts":1,"ends":1,"total":25},"note":"Index 2 holds 3 with 1 start choices and 1 end choices, so it owns 1 windows and adds 3."},{"at":{"i":3},"vars":{"left":-1,"right":5,"starts":4,"ends":2,"total":65},"note":"Index 3 holds 5 with 4 start choices and 2 end choices, so it owns 8 windows and adds 40."},{"at":{"i":4},"vars":{"left":3,"right":5,"starts":1,"ends":1,"total":66},"note":"Index 4 holds 1 with 1 start choices and 1 end choices, so it owns 1 windows and adds 1."},{"at":{"i":5},"vars":{"total":66},"note":"All 5 indices are added, and the total is 66."}]}
```

<!-- stage: code -->
### Contribution Sums In Java

#### The Sum Of Minimums

The method finds both boundaries in one pass and then adds the contributions. The cast `(long) nums[i]` makes the whole product `long`, so the two distance factors are widened before they multiply.

```java
static long sumOfMinimums(int[] nums) {
    int n = nums.length;
    int[] left = new int[n];
    int[] right = new int[n];
    Arrays.fill(right, n);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] >= nums[i]) {
            right[stack.pop()] = i;
        }
        left[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }
    long total = 0;
    for (int i = 0; i < n; i++) {
        total += (long) nums[i] * (i - left[i]) * (right[i] - i);
    }
    return total;
}
```

#### The Sum Of Maximums

The maximum version reverses both comparisons. The stack now holds values that strictly decrease from bottom to top.

```java
static long sumOfMaximums(int[] nums) {
    int n = nums.length;
    int[] left = new int[n];
    int[] right = new int[n];
    Arrays.fill(right, n);
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] <= nums[i]) {
            right[stack.pop()] = i;
        }
        left[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }
    long total = 0;
    for (int i = 0; i < n; i++) {
        total += (long) nums[i] * (i - left[i]) * (right[i] - i);
    }
    return total;
}
```

Both methods run in O(n) time and use O(n) extra space. With a modulus `M`, the line becomes `total = (total + (long) nums[i] % M * ((long) (i - left[i]) * (right[i] - i) % M)) % M`, which keeps every product below the `long` limit when `M` is near 10^9.

<!-- stage: applicability -->
### When A Sum Becomes A Count

#### The Cue For Contribution Counting

The cue is a sum or a count over all windows, where each window is summarized by one extreme value. The invariant is that every window has exactly one owner, and the owner of index `i` has `i - left` start choices and `right - i` end choices. The method turns the many windows into one product per index.

#### Two False Friends

The product on its own is the first false friend. The formula looks the same under every tie convention, but it is correct only for the one that gives each window one owner. On the readings 2 and 2, a strict boundary on both sides gives the counts 2 and 2, which total 4 for 3 windows.

The second false friend is the sliding window of fixed length. A window of fixed size `k` has one start per end, so the start and end choices are not independent. The product rule does not apply there.

#### When It Does Not Apply

A sum that depends on more than the minimum, such as the sum of window averages, cannot be regrouped by one owner. A question that asks for the window itself, and not for a total, also needs the windows listed or searched.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Subarrays Owned By One Index (Author exercise)
<!-- id: ms-count-owned-by-one-index -->

**Prerequisites.** The two independent choices in this lesson.

**Problem.** Arrays `left` and `right` of length `n` are given, with `-1 <= left[i] < i < right[i] <= n` for every index `i`. For each index `i`, count the pairs `(l, r)` that satisfy `left[i] < l <= i` and `i <= r < right[i]`. Return the counts.

**Constraints.** The limits are:
- **Length** is `1 <= n <= 10^5`.
- **Boundaries** are valid indices or the sentinels `-1` and `n`, with `left[i] < i < right[i]`.
- **Counts** can exceed the range of `int`, so each entry is a `long`.
- **Return** is a `long[]` of length `n`.

**Example 1.** Input `left = [-1,-1,-1]`, `right = [1,2,3]`, output `[1,2,3]`.

**Example 2.** Input `left = [-1,0,0,2]`, `right = [1,4,3,4]`, output `[1,3,2,1]`.

**Hint.** List the allowed starts and the allowed ends for one index. Does the choice of a start change which ends are allowed?

**Changed decision.** The counting rule is a product of two range sizes, and no window is listed.

#### [Vary] Sum Owned Minimum Contributions (Author exercise)
<!-- id: ms-sum-owned-minimum-contributions -->

**Prerequisites.** The exercise above and the minimum version in this lesson.

**Problem.** An array `nums` of positive integers is given. For each index `i`, let `left` be the largest earlier index with a strictly smaller value, or `-1`. Let `right` be the smallest later index with a value smaller than or equal to `nums[i]`, or `n`. Return an array whose entry `i` equals `nums[i] * (i - left) * (right - i)`, followed by one last entry with the sum of all those contributions.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are integers with `1 <= nums[i] <= 10^4`, and equal values are allowed.
- **Entries** fit in a `long`, and no modulus is applied.
- **Return** is a `long[]` of length `n + 1`.

**Example 1.** Input `[2,5,3,5,1]`, output `[8,5,12,5,5,35]`.

**Example 2.** Input `[3,3,3]`, output `[3,6,9,18]`.

**Hint.** Compute the two boundaries in one pass first. Then multiply the value by its start choices and its end choices.

**Changed decision.** The answer keeps each index's contribution, and the total is the sum of the entries.

#### [Boundary] Negative And Repeated Values (Author exercise)
<!-- id: ms-negative-and-repeated-values -->

**Prerequisites.** The two exercises above.

**Problem.** An integer array `nums` can hold negative and repeated values. Return the exact sum of `min(subarray)` over every contiguous non-empty subarray. The sum can be negative.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are integers with `-10^4 <= nums[i] <= 10^4`, and equal values are allowed.
- **Sum** fits in a `long`, and the result keeps its sign.
- **Return** is a `long`.

**Example 1.** Input `[-2,5,-2]`, output `-5`.

**Example 2.** Input `[4,1,4,1,4]`, output `24`.

**Hint.** Does the tie rule depend on the sign of a value? Which part of the formula can be negative, and which parts cannot?

**Changed decision.** Negative values change the arithmetic only. The ownership proof is the same as for positive values.

#### [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-of-subarray-minimums-modulo -->

**Prerequisites.** The three exercises above.

**Problem.** Given an array of integers `arr`, find the sum of `min(b)`, where `b` ranges over every contiguous subarray of `arr`. Return the answer modulo `10^9 + 7`.

**Constraints.** The limits are:
- **Length** is `1 <= arr.length <= 3 * 10^4`.
- **Values** are integers with `1 <= arr[i] <= 3 * 10^4`, and equal values are allowed.
- **Modulus** is `10^9 + 7`, applied to the result.
- **Return** is an `int` in the range `0` through `10^9 + 6`.

**Example 1.** Input `[7,2,9,2,5]`, output `45`.

**Example 2.** Input 30000 copies of the value `30000`, output `449905500`.

**Hint.** Where does a product leave the range of `int`? Apply the remainder only after the product is formed in a `long`.

**Changed decision.** The answer is a remainder, so every product is reduced before it is added, and the earlier exact version no longer applies.
