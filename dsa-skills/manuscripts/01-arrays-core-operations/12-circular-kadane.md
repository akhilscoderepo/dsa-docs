<!-- lesson-kind: standard -->
<!-- lesson-id: circular-kadane -->
## Circular Kadane

<!-- stage: context -->
### Profits Around A Round Table

A bakery runs a seven-day cycle, and the owner keeps the daily profit in a ring, so that Sunday is followed by Monday again. She wants the best run of consecutive days to put a promotion on, and a run is allowed to cross the week boundary. A promotion from Saturday to Tuesday is perfectly legal. It simply passes through Sunday on the way.

On a straight ledger she would look at every stretch from some start to some end. On the ring, two kinds of stretch exist. Some sit inside the week and never cross the boundary, while others start late in the week and finish early in the next. The second kind is the new difficulty, and it is natural to wonder whether the straight-ledger method still works.

<!-- stage: naive -->
### Try Every Start And Every Length

With a ring, the direct approach picks every start position and every length from one to `n`, wrapping the index with a remainder.

```java
static int bestCircularByEnumeration(int[] profit) {
    int n = profit.length, best = profit[0];
    for (int start = 0; start < n; start++) {
        int sum = 0;
        for (int len = 1; len <= n; len++) {
            sum += profit[(start + len - 1) % n];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```

The inner loop extends the running sum by one element, so each choice costs a single addition. For `[4, -5, 3, -1, 4]` it finds 10, from the days `3, -1, 4, 4`, which cross the boundary.

<!-- stage: bottleneck -->
### Quadratic Again, Now With A Wrap

There are `n` starts and `n` lengths, so the cost is O(n^2), which is ten billion additions for 100,000 days. Space is O(1). The ordinary Kadane pass fixes the straight case in linear time, but it never looks across the boundary, so it would miss the answer of 10 above and report 6.

One idea is to run the straight method on the array written twice, but a window longer than `n` would then reuse an element, and clipping the length reintroduces extra work. The cleaner route is to describe what a wrapping stretch leaves out. Whatever it covers, the days it skips form one block, and that block is an ordinary stretch.

<!-- stage: insight -->
### A Wrapping Stretch Skips One Middle Block

A **wrapping subarray** covers a tail of the array and a head of the array and passes over the boundary. Everything it does not cover is one contiguous block in the middle of the straight array, the **excluded segment**. The wrapping sum is therefore the total of all elements minus the sum of the excluded segment.

To make the wrapping sum as large as possible, make the excluded segment as small as possible. The smallest sum of a contiguous block is exactly what the minimum version of Kadane's recurrence computes. So the best **wrap candidate** is `total - minimumSubarray`, and the answer is the larger of that and the ordinary maximum subarray. Both come from one pass with four running values.

<!-- names: wrapping subarray, excluded segment, wrap candidate -->

The invariant is that after the pass the four values describe the straight array fully: the total, the best maximum stretch, and the best minimum stretch, with their ending states. Every circular stretch is either a straight one, covered by the maximum, or a wrapping one, covered by the total minus some straight block. Taking the smallest straight block gives the largest wrapping one, so nothing is missed.

One case must be guarded. If the smallest straight block is the entire array, the excluded segment is everything, and the wrap candidate becomes an empty stretch with sum zero. The problem asks for a non-empty stretch. This happens exactly when every element is negative, where the best answer is the ordinary maximum, which is the largest single element. So when the ordinary maximum is negative, return it directly and ignore the wrap candidate.

<!-- stage: variables -->
### Four Running Values And A Total

The pass keeps `total`, the sum of every element, plus two pairs of ending state and best: `maxEnd` and `maxBest` for the largest straight stretch, and `minEnd` and `minBest` for the smallest. All five start from the first element. Each later element updates the totals, then both ending states with the usual extend-or-restart choice, then both bests. After the pass, `maxBest` is the ordinary answer and `total - minBest` is the wrap candidate, which is only valid when `maxBest` is not negative.

<!-- stage: trace -->
### One Pass, Two Answers

Take `[4, -5, 3, -1, 4]`. The first element sets every running value to 4. The loss of 5 brings the total to -1. Carrying the 4 forward gives -1, which beats -5 alone, so the maximum ending state is -1 while the maximum best stays at 4. The same loss makes the minimum ending state -5, because -5 alone beats 4 plus -5, and the minimum best is -5.

The next three elements are 3, -1 and 4. The 3 restarts the maximum stretch at 3, the -1 extends it to 2, and the final 4 extends it to 6, so the maximum best is 6, from the days `3, -1, 4`. The minimum ending state climbs from -2 to -3 to 1 while the minimum best stays at -5. The pass ends with a total of 5, a maximum best of 6 and a minimum best of -5. The wrap candidate is the total minus the minimum best, which is 5 minus -5, so 10. The excluded segment is the single loss day in the middle, and everything else, joined around the seam, sums to 10. The answer is the larger of 6 and 10.

Second ring: `[-3, -2, -3]`. The maximum best is -2 and the minimum best is -8, equal to the total. The wrap candidate is the total minus -8, which is zero, an empty stretch. Because the ordinary maximum is negative, the guard returns -2 and the empty candidate is never considered.

```trace
{"cells":[4,-5,3,-1,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":4,"maxEnd":4,"maxBest":4,"minEnd":4,"minBest":4},"note":"Day 1 sets every running value to 4."},{"at":{"i":1},"vars":{"total":-1,"maxEnd":-1,"maxBest":4,"minEnd":-5,"minBest":-5},"note":"Day 2 adds -5. The total is -1, the maximum best is 4 and the minimum best is -5."},{"at":{"i":2},"vars":{"total":2,"maxEnd":3,"maxBest":4,"minEnd":-2,"minBest":-5},"note":"Day 3 adds 3. The total is 2, the maximum best is 4 and the minimum best is -5."},{"at":{"i":3},"vars":{"total":1,"maxEnd":2,"maxBest":4,"minEnd":-3,"minBest":-5},"note":"Day 4 adds -1. The total is 1, the maximum best is 4 and the minimum best is -5."},{"at":{"i":4},"vars":{"total":5,"maxEnd":6,"maxBest":6,"minEnd":1,"minBest":-5},"note":"Day 5 adds 4. The total is 5, the maximum best is 6 and the minimum best is -5."}]}
```

```trace
{"cells":[-3,-2,-3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"total":-3,"maxEnd":-3,"maxBest":-3,"minEnd":-3,"minBest":-3},"note":"Day 1 sets every running value to -3."},{"at":{"i":1},"vars":{"total":-5,"maxEnd":-2,"maxBest":-2,"minEnd":-5,"minBest":-5},"note":"Day 2 adds -2. The total is -5, the maximum best is -2 and the minimum best is -5."},{"at":{"i":2},"vars":{"total":-8,"maxEnd":-3,"maxBest":-2,"minEnd":-8,"minBest":-8},"note":"Day 3 adds -3. The total is -8, the maximum best is -2 and the minimum best is -8."}]}
```

<!-- stage: code -->
### Kadane Twice With A Guard

```java
static int maxCircular(int[] nums) {                  // non-empty circular subarray, non-empty array
    int total = nums[0];
    int maxEnd = nums[0], maxBest = nums[0];
    int minEnd = nums[0], minBest = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        total += x;
        maxEnd = Math.max(x, maxEnd + x);
        maxBest = Math.max(maxBest, maxEnd);
        minEnd = Math.min(x, minEnd + x);
        minBest = Math.min(minBest, minEnd);
    }
    if (maxBest < 0) return maxBest;                  // every element negative: the wrap candidate would be empty
    return Math.max(maxBest, total - minBest);
}

static int minCircular(int[] nums) {
    int total = nums[0];
    int maxEnd = nums[0], maxBest = nums[0];
    int minEnd = nums[0], minBest = nums[0];
    for (int i = 1; i < nums.length; i++) {
        int x = nums[i];
        total += x;
        maxEnd = Math.max(x, maxEnd + x);
        maxBest = Math.max(maxBest, maxEnd);
        minEnd = Math.min(x, minEnd + x);
        minBest = Math.min(minBest, minEnd);
    }
    if (maxBest > 0 && maxBest == total) return minBest;       // wrap candidate would exclude everything
    return Math.min(minBest, total - maxBest);
}
```

Each method makes one pass with a handful of scalars, so the time is linear and the extra space is constant. The guard in the first method protects the non-empty contract when all values are negative. The second method needs the mirror guard, which triggers when the ordinary maximum equals the total, meaning the excluded segment would be the whole array and the remainder empty. Use `long` for the total if the values or the length can be large.

<!-- stage: applicability -->
### When The Stretch May Cross The Seam

Use this method when a contiguous stretch of a ring-shaped array may cross from the last index to the first, and the objective is a sum. The invariant is that a wrapping stretch equals the total minus one excluded straight block, so maximizing the wrap means minimizing the excluded block. Always compare with the ordinary maximum and always forbid an empty result.

The false friend is a fixed-length circular window, such as the best sum of exactly `k` consecutive days on the ring. That has a different state, a window that slides with a fixed size, and the complement trick does not apply. Another false friend is a circular product, because the complement of a product is a division, which fails on zeros and breaks the order reasoning of the previous lesson. For a ring where only straight stretches matter, plain Kadane is enough.

In Java the usual hazards are the all-negative case, which makes the empty wrap look like a winner, and the minimum version, where the guard compares the maximum with the total. Rather than copying the array twice, keep the single pass, which stays honest about memory.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Sum Circular Subarray (LeetCode 918)
<!-- id: ar-maximum-circular-subarray -->

**Prerequisites.** The Kadane state lesson; this lesson.

**Problem.** Given a circular array, return the largest sum of a non-empty subarray, where a subarray may wrap from the last index to the first and may use each element at most once.

**Constraints.** 1 <= nums.length <= 3 * 10^4 and -3 * 10^4 <= nums[i] <= 3 * 10^4. Aim for one pass.

**Example 1.** Input `nums = [4, -5, 3, -1, 4]`, output 10, from the wrapping stretch `3, -1, 4, 4`.

**Example 2.** Input `nums = [2, -1, 2, -6, 1]`, output 4, from the wrapping stretch `1, 2, -1, 2`.

**Hint.** What does a wrapping stretch leave out, and what shape does the left-out part have? Which quantity do you want that part to be?

**Changed decision.** First rung: the wrapping case is turned into a straight minimum-subarray problem on the excluded middle.

#### [Vary] Circular Minimum (Author exercise)
<!-- id: ar-circular-minimum -->

**Prerequisites.** The circular-maximum exercise above.

**Problem.** Return the smallest sum of a non-empty subarray of a circular array. Use the symmetric argument: a wrapping minimum is the total minus the largest straight block, but the excluded block may not be the whole array.

**Constraints.** 1 <= nums.length <= 3 * 10^4 and -3 * 10^4 <= nums[i] <= 3 * 10^4. Aim for one pass.

**Example 1.** Input `nums = [-5, 2, 3, -4]`, output -9, from the wrapping stretch `-4, -5`.

**Example 2.** Input `nums = [3, 1, 2]`, output 1, because the wrap candidate would exclude everything.

**Hint.** Which straight block should the wrapping stretch leave out to be as small as possible? When would that block be the entire array?

**Changed decision.** The roles of maximum and minimum are exchanged, and the guard moves from all-negative to all-positive input.

#### [Boundary] All Negative (Author exercise)
<!-- id: ar-circular-all-negative -->

**Prerequisites.** The two exercises above.

**Problem.** For an array in which every value is negative, return the best circular sum and explain why the wrap candidate is invalid there. Show the numbers that the candidate would produce.

**Constraints.** 1 <= nums.length <= 3 * 10^4 and every value is between -3 * 10^4 and -1. The subarray must be non-empty.

**Example 1.** Input `nums = [-3, -2, -3]`, output -2, since the wrap candidate would be the total minus the whole array, which is zero.

**Example 2.** Input `nums = [-7]`, output -7, and the candidate is again an empty stretch.

**Hint.** What is the smallest straight block when every value is negative? What does leaving that block out leave behind?

**Changed decision.** The tests target the empty remainder, which turns the wrap candidate into a stretch that does not exist.

#### [Recognize] Circular Maximum With A Proof (LeetCode 918)
<!-- id: ar-circular-proof -->

**Prerequisites.** All three exercises above.

**Problem.** Implement the circular maximum, and state in two sentences why every wrapping choice excludes exactly one ordinary contiguous middle segment of the array. The proof should say why the excluded part is contiguous and why it cannot touch either end.

**Constraints.** 1 <= nums.length <= 3 * 10^4 and -3 * 10^4 <= nums[i] <= 3 * 10^4. The proof must cover wrapping choices that use fewer than `n` elements.

**Example 1.** Input `nums = [7, -3, -4, 6]`, output 13, from the wrapping stretch `6, 7`, which excludes the middle block `-3, -4`.

**Example 2.** Input `nums = [-1, -2]`, output -1, with no valid wrap.

**Hint.** If a stretch starts at index `s` and covers `len` elements past the last index, which indices are left? Do they form one block?

**Changed decision.** The task adds a justification of the complement idea to the implementation, which is the claim every candidate rests on.
