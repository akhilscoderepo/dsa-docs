<!-- lesson-kind: standard -->
<!-- lesson-id: remainder-classes -->
## Group Prefixes By Remainder

<!-- stage: context -->
### Ledger Stretches That Close In Whole Bundles

A ledger lists signed adjustments in cents. Credits are positive and debits are negative. An auditor wants to find the stretches of consecutive entries whose net total is an exact multiple of `k` cents. A bank settles such stretches in whole bundles of `k` cents with nothing left over.

The ledger has tens of thousands of entries, and the auditor wants every such stretch. The previous lesson matched prefix totals that are equal. Here the totals only need to agree after a division by `k`, and the debits make some totals negative. The problem is to count these stretches without testing every pair of ends, and to do it correctly for negative totals.

<!-- stage: naive -->
### Testing Every Pair For Divisibility

The direct method fixes each start, extends the end, and tests whether the running sum leaves remainder 0 when divided by `k`.

```java
static int countDivisible(int[] nums, int k) {
    int count = 0;
    for (int start = 0; start < nums.length; start++) {
        long sum = 0;
        for (int end = start; end < nums.length; end++) {
            sum += nums[end];
            if (sum % k == 0) count++;
        }
    }
    return count;
}
```

For `[3, -1, 2, 4, -6, 1]` and `k = 4`, the method returns 5. The test `sum % k == 0` is correct for negative sums too, because a multiple of `k` leaves remainder 0 in Java.

```predict
The array holds 30,000 entries. How many (start, end) pairs does `countDivisible` test?

It tests 30,000 * 30,001 / 2 = 450,015,000 pairs. The loops visit every pair of ends, so the cost is O(n^2).
```

<!-- stage: bottleneck -->
### Pairs Hide A Shared Remainder

The method tests every pair of ends, which costs O(n^2). Most tests fail, and nothing carries information from one pair to the next. The sum of the pair from boundary `a` to boundary `b` equals `prefix[b] - prefix[a]`, so the test asks whether two prefix values differ by a multiple of `k`.

Two numbers differ by a multiple of `k` exactly when they leave the same remainder after division by `k`. The test for a pair therefore compares two remainders. The method can group all earlier prefixes by their remainder and look up the matching group, in the way the previous lesson looked up equal totals.

<!-- stage: insight -->
### Group Prefix Values By Their Remainder

A **remainder class** is the set of integers that leave the same remainder when divided by `k`. For `k = 4`, the numbers 2, 6, -2 and 10 form one class. Any two members differ by a multiple of `k`. Write `prefix[a] = p * k + r` and `prefix[b] = q * k + r`. The difference is `(q - p) * k`, which is divisible by `k`.

#### Count Earlier Boundaries In The Same Class

A subarray has a sum divisible by `k` exactly when its two boundaries lie in the same class. The loop keeps an array `freq` of length `k`, where `freq[r]` is the number of earlier boundaries in class `r`. At each boundary it adds `freq[class]` to the answer and then increases `freq[class]`. The array starts with `freq[0] = 1` for boundary 0, whose prefix is 0.

#### One Class Number For Every Prefix

The **normalized remainder** is the class number from 0 to `k - 1`. Java's operator `%` does not always return it. The result of `%` has the sign of the left operand, so `-3 % 5` is -3. The number -3 and the number 2 are in the same class, and `%` gives them different values. The call `Math.floorMod(-3, 5)` returns 2. It always returns a value from 0 to `k - 1` for positive `k`, so equal classes get equal keys.

<!-- names: remainder class, normalized remainder, floorMod -->

#### The Cost Of One Pass

The loop makes one `floorMod` call, one array read and one array write per value. The time is O(n) and the space is O(k). The prefix needs a `long`, because the total of many large entries exceeds the `int` range.

<!-- stage: variables -->
### Five Names And Their Roles

The loop keeps five values.

- **cur** is the prefix sum through the current entry and has type `long`.
- **cls** is `Math.floorMod(cur, k)`, the class number of the current boundary.
- **freq** is the array of length `k` with the number of earlier boundaries in each class.
- **count** is the number of divisible subarrays found so far.
- **k** is the divisor and never changes.

Before the first step, `freq[0]` is 1 and every other entry is 0. The class is computed before the lookup, and the lookup runs before `freq[cls]` increases.

<!-- stage: trace -->
### Two Runs With Class Numbers

#### Mixed Signs And Divisor Four

The input is `[3, -1, 2, 4, -6, 1]` and `k = 4`. The prefix values are 3, 2, 4, 8, 2 and 3, with classes 3, 2, 0, 0, 2 and 3. Class 0 holds boundary 0, which counts the first match at index 2. Each later repeat of a class adds the number of earlier members, and the total is 5.

```trace
{"cells":[3,-1,2,4,-6,1],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"freq":"{0=1}","count":"0"},"note":"Class 0 starts with one boundary, boundary 0 with prefix 0."},{"at":{"i":0},"vars":{"cur":"3","class":"3","freq":"{0=1, 3=1}","count":"0"},"note":"Prefix 3 has class 3. 0 earlier boundaries share it, so the count becomes 0."},{"at":{"i":1},"vars":{"cur":"2","class":"2","freq":"{0=1, 2=1, 3=1}","count":"0"},"note":"Prefix 2 has class 2. 0 earlier boundaries share it, so the count becomes 0."},{"at":{"i":2},"vars":{"cur":"4","class":"0","freq":"{0=2, 2=1, 3=1}","count":"1"},"note":"Prefix 4 has class 0. 1 earlier boundary share it, so the count becomes 1."},{"at":{"i":3},"vars":{"cur":"8","class":"0","freq":"{0=3, 2=1, 3=1}","count":"3"},"note":"Prefix 8 has class 0. 2 earlier boundaries share it, so the count becomes 3."},{"at":{"i":4},"vars":{"cur":"2","class":"2","freq":"{0=3, 2=2, 3=1}","count":"4"},"note":"Prefix 2 has class 2. 1 earlier boundary share it, so the count becomes 4."},{"at":{"i":5},"vars":{"cur":"3","class":"3","freq":"{0=3, 2=2, 3=2}","count":"5"},"note":"Prefix 3 has class 3. 1 earlier boundary share it, so the count becomes 5."}]}
```

#### A Negative Prefix

The input is `[-3, -2]` and `k = 5`. The first prefix is -3. The operator `%` gives -3, and `floorMod` gives 2, which is the class number. The second prefix is -5, and both calls give 0. Class 0 holds boundary 0, so the whole array counts once.

```trace
{"cells":[-3,-2],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"freq":"{0=1}","count":"0"},"note":"Class 0 starts with one boundary, boundary 0 with prefix 0."},{"at":{"i":0},"vars":{"cur":"-3","class":"2","freq":"{0=1, 2=1}","count":"0","cur % k":"-3"},"note":"Prefix -3 has class 2. 0 earlier boundaries share it, so the count becomes 0."},{"at":{"i":1},"vars":{"cur":"-5","class":"0","freq":"{0=2, 2=1}","count":"1"},"note":"Prefix -5 has class 0. 1 earlier boundary share it, so the count becomes 1."}]}
```

<!-- stage: code -->
### The One Pass In Java

```java
static int countDivisible(int[] nums, int k) {
    int[] freq = new int[k];
    freq[0] = 1;
    long cur = 0;
    int count = 0;
    for (int v : nums) {
        cur += v;
        int cls = (int) Math.floorMod(cur, (long) k);
        count += freq[cls];
        freq[cls]++;
    }
    return count;
}
```

The call `Math.floorMod(long, long)` returns a `long`, and the result is below `k`, so the cast to `int` is safe. The array has `k` entries, so `k` must be small enough to allocate. The lookup `freq[cls]` runs before the increment, which keeps a boundary from pairing with itself.

When `k` is huge, a hash map from class to count replaces the array. The loop stays the same.

<!-- stage: applicability -->
### When Remainders Replace Equal Totals

#### The Invariant

The invariant is that when the loop reaches boundary `b`, `freq[r]` counts the boundaries `a < b` with a prefix in class `r`. The lookup then counts every `a` that makes the difference divisible by `k`. Each valid pair appears once, at its later boundary.

#### The False Friend

The false friend is the raw `%` result. It matches the true class for non-negative prefixes, and it silently splits a class in two when prefixes are negative. A subarray whose ends have `%` values -3 and 2 is missed. The tests that pass with positive inputs hide the defect.

#### Conditions That Break The Fit

The method needs a divisor that stays fixed for all queries. A different `k` needs a new pass and a new `freq`. A condition such as a sum that is a multiple of `k` or of `m` needs a separate class system for each divisor. A condition about the quotient of the sum and not its remainder does not fit.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sums Divisible By K (LeetCode 974)
<!-- id: ps-divisible-974 -->

**Prerequisites.** The remainder class, `Math.floorMod` and the frequency array of this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, return the number of non-empty contiguous subarrays whose sum is divisible by `k`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 3 * 10^4`.
- **Values** are `int` values with `-10^4 <= nums[i] <= 10^4`.
- **Divisor** satisfies `2 <= k <= 10^4`.
- **Negative sums** are valid and must land in the correct class.

**Example 1.** Input `nums = [3,-1,2,4,-6,1]` and `k = 4`, output 5.

**Example 2.** Input `nums = [5]` and `k = 9`, output 0.

**Hint.** Replace the lookup key `cur - k` of the previous lesson by the class of `cur`. Which operator keeps the class in `0..k-1`?

**Changed decision.** Basic case: the key is the normalized remainder, so equal keys mean a difference divisible by `k`.

#### [Vary] Continuous Subarray Sum (LeetCode 523)
<!-- id: ps-continuous-523 -->

**Prerequisites.** The first exercise above and the earliest-index map of the previous lesson.

**Problem.** Given an array `nums` of non-negative integers and an integer `k`, return `true` when some contiguous subarray of length at least 2 has a sum that is a multiple of `k`. Zero is a multiple of `k`.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `0 <= nums[i] <= 10^9`.
- **Divisor** satisfies `1 <= k <= 2^31 - 1`.
- **Length rule** requires at least two values in the subarray.

**Example 1.** Input `nums = [5,0,0]` and `k = 6`, output `true`.

**Example 2.** Input `nums = [1,2,3]` and `k = 7`, output `false`.

**Hint.** A repeated class at boundaries `a` and `b` gives a subarray of length `b - a`. Which earlier index of the class makes that length largest?

**Changed decision.** The map keeps the earliest index per class and not a count, because the length rule needs the position.

#### [Boundary] Negative Values (Author exercise)
<!-- id: ps-negative-remainders -->

**Prerequisites.** The first exercise above and the second trace of this lesson.

**Problem.** Given `nums` and a divisor `k`, return the array of length `nums.length + 1` whose entry `i` is the class number of the sum of the first `i` values. The class number is the remainder in the range 0 to `k - 1`.

**Constraints.** The limits are:
- **Length** is `0 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Divisor** satisfies `1 <= k <= 10^9`.
- **Range** of every entry is `0 <= entry < k`.

**Example 1.** Input `nums = [-3,-2]` and `k = 5`, output `[0,2,0]`.

**Example 2.** Input `nums = [7,-8,1]` and `k = 3`, output `[0,1,2,0]`.

**Hint.** Compare the output of `%` and of `Math.floorMod` for the prefix -1 and `k = 3`.

**Changed decision.** The task is the key itself, so the normalization is the only step that can go wrong.

#### [Recognize] Longest Divisible Span (Author exercise)
<!-- id: ps-divisible-span -->

**Prerequisites.** All exercises above.

**Problem.** Given `nums` and a divisor `k`, return the length of the longest non-empty contiguous subarray whose sum is divisible by `k`. Return 0 when no subarray qualifies.

**Constraints.** The limits are:
- **Length** is `1 <= nums.length <= 10^5`.
- **Values** are `int` values with `|nums[i]| <= 10^9`.
- **Divisor** satisfies `1 <= k <= 10^9`.
- **Return value** is the length and not the count.

**Example 1.** Input `nums = [2,-2,5]` and `k = 5`, output 3.

**Example 2.** Input `nums = [1,2,3]` and `k = 4`, output 0.

**Hint.** Store the first index for each class, with the class 0 stored at index -1. A repeat at index `i` gives a span of length `i - first`.

**Changed decision.** The map value changes from a count to the earliest index, so the same class key answers a different question.
