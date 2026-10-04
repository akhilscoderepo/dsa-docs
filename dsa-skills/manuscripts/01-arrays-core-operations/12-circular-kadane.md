<!-- lesson-kind: standard -->
<!-- lesson-id: circular-kadane -->
## Circular Kadane

<!-- stage: context -->
### Finding The Best Run That Wraps Around

A monitoring service stores one traffic change for each hour of a day in an array of 24 integers. Hour 23 is followed by hour 0 of the next day, so the busiest stretch can start in the evening and continue past midnight. The array is circular, because the last index connects back to the first index.

For the array `[4, -5, 2, -1, 6]` the best run is `2, -1, 6, 4`, with sum 11. It starts at index 2, reaches the end, and continues at index 0. An engineer who runs a one-pass scan from index 0 to the end never sees that run and returns 7. The question for this lesson is how to count the wrapping runs without trying every start and length.

<!-- stage: naive -->
### Trying Every Start And Length

A **circular subarray** is a non-empty run of consecutive positions where index `n - 1` is followed by index 0. Its length is at most `n`, so the run never uses the same position twice. The direct method tries every start index and every length. It reads positions with the index `(start + length - 1) % n` and keeps a running sum.

```java
static int bruteCircular(int[] nums) {
    int n = nums.length;
    int best = Integer.MIN_VALUE;
    for (int start = 0; start < n; start++) {
        int sum = 0;
        for (int length = 1; length <= n; length++) {
            sum += nums[(start + length - 1) % n];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```

This method is correct. It covers every wrapping run and every ordinary run. It takes O(n^2) time because each start extends over up to `n` positions. It takes O(1) extra space.

<!-- stage: bottleneck -->
### Many Wrapping Runs Share One Complement

```predict
For the array `[4, -5, 2, -1, 6]`, an ordinary one-pass scan for the best non-wrapping run returns 7. What is the best circular run, and which values does it leave out?

The best circular run has sum 11. It uses `2, -1, 6, 4` and leaves out only the value -5. The excluded part is one ordinary run in the middle of the array, and the sum of the whole array, 6, minus the excluded sum, -5, gives 11.
```

The direct method takes O(n^2) time, which is about five billion steps for `n = 100,000`. Most of that work repeats earlier sums. Each wrapping run is described by what it leaves out, and that leftover part is one ordinary contiguous run. Many start and length pairs lead to the same leftover.

A wrapping run that leaves out a contiguous run with sum `m` has sum `total - m`, where `total` is the sum of the whole array. To make the wrapping sum as large as possible, make the excluded sum as small as possible. The smallest sum of an ordinary contiguous run is a one-pass question that earlier lessons already solved. So the whole problem takes two ordinary scans, which is O(n) time.

<!-- stage: insight -->
### Wrapping Maximum Equals Total Minus Minimum

#### The Wrapping Candidate

Every circular subarray is either an ordinary subarray, or it wraps and leaves out one ordinary subarray. Compute the sum of the whole array as `totalSum`. Then a wrapping choice has the sum `totalSum - m`, where `m` is the sum of the ordinary subarray that it leaves out. Define `wrapCandidate = totalSum - minimumOrdinary`, where `minimumOrdinary` is the smallest sum of a non-empty ordinary subarray. The answer is the larger of the ordinary maximum and `wrapCandidate`.

<!-- names: totalSum, wrapCandidate, empty remainder -->

#### Forbidding The Empty Remainder

The formula has one trap. When the smallest ordinary subarray is the whole array, the part left over has no elements. The leftover then has no elements and is called the **empty remainder**. It makes `wrapCandidate` equal to 0, but that value does not belong to any allowed subarray, because a wrapping subarray must leave out at least one element and stay non-empty. This happens when every value is negative, because then the whole array has the smallest sum. In that case the answer is the ordinary maximum, which is the largest single value. If the ordinary maximum is not negative, the wrapping candidate of 0 never beats it, so the rule needs only one check.

#### Why The Invariant Holds

The invariant is that every value of the form `totalSum - m` for an ordinary subarray `m` that is not the whole array is the sum of a real circular subarray, namely the complement of `m`. Every wrapping subarray has this form. The largest such value uses the smallest `m`, so the maximum of the two candidates equals the best circular sum.

<!-- stage: variables -->
### Meaning And Update Time Of Each Variable

One pass keeps five values, and a loop index `i` moves from left to right.

- **`maxEnding`** holds the largest sum of a subarray ending at `i`, and it changes at every index.
- **`maxOverall`** holds the largest `maxEnding` seen so far, which is the ordinary maximum.
- **`minEnding`** holds the smallest sum of a subarray ending at `i`, and it changes at every index.
- **`minOverall`** holds the smallest `minEnding` seen so far, which is the ordinary minimum.
- **`total`** holds the sum of all values, and it adds each value once.

The four running values start at `nums[0]`, and `total` starts at 0 before the loop reads index 0. The final decision reads `maxOverall`, `minOverall` and `total` only after the last index.

<!-- stage: trace -->
### Tracing Both Scans And The Final Choice

The first trace follows `[4, -5, 2, -1, 6]`. The maximum scan ends with an ordinary maximum of 7, from the run `2, -1, 6`. The minimum scan reaches -5 at index 1 and never goes lower, so the ordinary minimum is -5. The total is 6. The wrapping candidate is 6 - (-5) = 11, which beats 7. The final step shows the comparison, and the answer is 11.

```trace
{"cells":[4,-5,2,-1,6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"maxEnding":4,"maxOverall":4,"minEnding":4,"minOverall":4,"total":4},"note":"Index 0 holds 4. All four running values start at 4 and the total is 4."},{"at":{"i":1},"vars":{"maxEnding":-1,"maxOverall":4,"minEnding":-5,"minOverall":-5,"total":-1},"note":"Index 1 holds -5. The maximum scan ends here at -1 with best 4. The minimum scan ends here at -5 with best -5. The total is -1."},{"at":{"i":2},"vars":{"maxEnding":2,"maxOverall":4,"minEnding":-3,"minOverall":-5,"total":1},"note":"Index 2 holds 2. The maximum scan ends here at 2 with best 4. The minimum scan ends here at -3 with best -5. The total is 1."},{"at":{"i":3},"vars":{"maxEnding":1,"maxOverall":4,"minEnding":-4,"minOverall":-5,"total":0},"note":"Index 3 holds -1. The maximum scan ends here at 1 with best 4. The minimum scan ends here at -4 with best -5. The total is 0."},{"at":{"i":4},"vars":{"maxEnding":7,"maxOverall":7,"minEnding":2,"minOverall":-5,"total":6},"note":"Index 4 holds 6. The maximum scan ends here at 7 with best 7. The minimum scan ends here at 2 with best -5. The total is 6."},{"at":{"i":5},"vars":{"maxOverall":7,"minOverall":-5,"total":6,"wrapCandidate":11,"answer":11},"note":"Scans finished. The wrapping candidate is 6 - (-5) = 11. It is compared with the ordinary maximum 7. The answer is 11."}]}
```

The second trace follows `[-6, -1, -4]`, where every value is negative. The ordinary maximum is -1. The minimum scan keeps extending, so the ordinary minimum is -11, which is the whole array. The wrapping candidate is -11 - (-11) = 0, which is an empty remainder and must be rejected. The ordinary maximum is negative, so the answer is -1.

```trace
{"cells":[-6,-1,-4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"maxEnding":-6,"maxOverall":-6,"minEnding":-6,"minOverall":-6,"total":-6},"note":"Index 0 holds -6. All four running values start at -6 and the total is -6."},{"at":{"i":1},"vars":{"maxEnding":-1,"maxOverall":-1,"minEnding":-7,"minOverall":-7,"total":-7},"note":"Index 1 holds -1. The maximum scan ends here at -1 with best -1. The minimum scan ends here at -7 with best -7. The total is -7."},{"at":{"i":2},"vars":{"maxEnding":-4,"maxOverall":-1,"minEnding":-11,"minOverall":-11,"total":-11},"note":"Index 2 holds -4. The maximum scan ends here at -4 with best -1. The minimum scan ends here at -11 with best -11. The total is -11."},{"at":{"i":3},"vars":{"maxOverall":-1,"minOverall":-11,"total":-11,"wrapCandidate":0,"answer":-1},"note":"Scans finished. The ordinary maximum -1 is negative, so the wrapping candidate -11 - (-11) = 0 is an empty remainder and is rejected. The answer is -1."}]}
```

<!-- stage: code -->
### Writing The Two Scans In Java

```java
static int maxCircular(int[] nums) {
    int maxEnding = nums[0], maxOverall = nums[0];
    int minEnding = nums[0], minOverall = nums[0];
    int total = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        total += x;
        maxEnding = Math.max(x, maxEnding + x);
        maxOverall = Math.max(maxOverall, maxEnding);
        minEnding = Math.min(x, minEnding + x);
        minOverall = Math.min(minOverall, minEnding);
    }
    if (maxOverall < 0) return maxOverall;
    return Math.max(maxOverall, total - minOverall);
}
```

One loop updates both scans, so the method reads each value once. It takes O(n) time and O(1) extra space. The early return handles the empty remainder, because `maxOverall < 0` holds exactly when every value is negative. Java adds one hazard. The total of many large values can overflow `int`, so use `long` when the bounds allow sums above about two billion.

<!-- stage: applicability -->
### Checking Whether The Complement Rule Applies

#### Conditions For Using The Wrapping Rule

Use the rule when the objective is the best sum of a non-empty subarray on a circular array, and the subarray has no fixed length. The invariant is that every wrapping choice corresponds to one excluded ordinary subarray with sum `m`, and its sum is `totalSum - m`. The same argument gives the smallest circular subarray, with the roles of maximum and minimum exchanged.

#### False Friend And No-Go Conditions

A false friend is the circular window of fixed length `k`. It also wraps around the end, but its state is a window sum updated as one value enters and one leaves. The excluded part is not a free ordinary subarray, because its length is `n - k` and cannot vary, so the minimum scan does not apply.

Do not use the complement rule when the array is not circular, because the ordinary scan alone is enough. Do not use it for products, because the complement of a product is a quotient, which fails when a value is zero. Check the empty remainder whenever the whole array can be the extreme subarray.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Circular Subarray (LeetCode 918)
<!-- id: ar-circular-max -->

**Prerequisites.** The ordinary maximum and minimum scans, and the wrapping candidate from this lesson.

**Problem.** Given an integer array `nums` treated as circular, return the largest sum over all non-empty circular subarrays. A circular subarray is a run of consecutive positions where index `n - 1` is followed by index 0, and no position repeats.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 3 * 10^4`.
- **Values** satisfy `-3 * 10^4 <= nums[i] <= 3 * 10^4`.
- **Subarray** is non-empty and has length at most `n`.
- **Input** is not modified.

**Example 1.** Input `[4, -5, 2, -1, 6]`, output 11, from the run `2, -1, 6, 4`.

**Example 2.** Input `[-2, 6, -3, 4, -5]`, output 7, from the ordinary run `6, -3, 4`.

**Hint.** If the best run wraps, what part of the array does it leave out, and what must be true about that part?

**Changed decision.** Baseline case: wrapping runs are counted by the smallest ordinary subarray they leave out, so no start-and-length search is needed.

#### [Vary] Circular Minimum (Author exercise)
<!-- id: ar-circular-min -->

**Prerequisites.** The maximum circular subarray exercise above.

**Problem.** Given an integer array `nums` treated as circular, return the smallest sum over all non-empty circular subarrays.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 3 * 10^4`.
- **Values** satisfy `-3 * 10^4 <= nums[i] <= 3 * 10^4`.
- **Subarray** is non-empty and has length at most `n`.
- **All-positive input** returns its smallest element.

**Example 1.** Input `[-2, 6, -3, 4, -5]`, output -7, from the wrapping run `-5, -2`.

**Example 2.** Input `[2, 5, 3]`, output 2, since the whole array is the largest run and its complement is empty.

**Hint.** Which ordinary subarray must a wrapping minimum leave out, and when would nothing be left out?

**Changed decision.** The roles exchange: the wrapping candidate subtracts the largest ordinary subarray, and the empty remainder appears when every value is positive.

#### [Boundary] All Negative (Author exercise)
<!-- id: ar-circular-all-negative -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `nums` whose values are all negative, return a pair. The first entry is the largest sum over non-empty circular subarrays. The second entry is the value of `totalSum - minimumOrdinary`. Explain why the second entry is not the sum of any allowed subarray.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `1 <= nums.length <= 3 * 10^4`.
- **Values** satisfy `-3 * 10^4 <= nums[i] <= -1`.
- **Return value** is an `int[2]` with the answer first and the wrapping value second.

**Example 1.** Input `[-6, -1, -4]`, output `[-1, 0]`.

**Example 2.** Input `[-5]`, output `[-5, 0]`.

**Hint.** Which ordinary subarray has the smallest sum when every value is negative, and what remains after removing it?

**Changed decision.** The wrapping value becomes 0 from an empty remainder, so the answer must come from the ordinary maximum alone.

#### [Recognize] Wrapping Choice Leaves One Segment (LeetCode 918)
<!-- id: ar-circular-proof -->

**Prerequisites.** The maximum circular subarray exercise above.

**Problem.** Given an integer array `nums` of length at least 3, return the largest sum over subarrays that wrap, meaning they contain both index `n - 1` and index 0 and leave out at least one element. State why every such subarray leaves out exactly one ordinary contiguous segment, and where that segment lies.

**Constraints.** The limits are:
- **`nums`** is an `int[]` with `3 <= nums.length <= 3 * 10^4`.
- **Values** satisfy `-3 * 10^4 <= nums[i] <= 3 * 10^4`.
- **Wrapping subarray** contains index 0 and index `n - 1` and omits at least one element.

**Example 1.** Input `[2, -6, 3, -1, 4]`, output 8, from the wrapping run `3, -1, 4, 2` that leaves out `-6`.

**Example 2.** Input `[-2, 6, -3, 4, -5]`, output 3, from the wrapping run `4, -5, -2, 6` that leaves out `-3`.

**Hint.** The elements kept form a prefix and a suffix. What do the elements between them form, and which indices can they use?

**Changed decision.** The excluded segment must lie strictly inside the array, so the minimum scan runs only on indices 1 through `n - 2`.
