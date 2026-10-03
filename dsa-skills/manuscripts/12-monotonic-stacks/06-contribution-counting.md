<!-- lesson-kind: standard -->
<!-- lesson-id: contribution-counting -->
## Contribution Counting

<!-- stage: context -->
### Adding The Low Points Of A Trail

A hiking club logs the altitude at every checkpoint of a long trail. The treasurer has an unusual scoring scheme for the season. For every stretch of consecutive checkpoints, from a single checkpoint up to the whole trail, the lowest altitude inside the stretch is written down, and the season score is the sum of all those lowest altitudes. A trail with a thousand checkpoints has about half a million stretches, and the treasurer would like a score without writing half a million lines.

She notices that a low checkpoint appears in the lists of many stretches, and that a high checkpoint is hidden by a lower neighbour in most of them. If she could tell, for each checkpoint, in how many stretches it is the lowest, she would only need to multiply that count by the altitude and add up one number per checkpoint.

<!-- stage: naive -->
### List The Lowest Of Every Stretch

The direct method visits each stretch and adds its lowest altitude. Fixing the left end and growing the right end keeps the running lowest altitude, so each stretch costs one step.

```java
static long sumOfLowestBruteForce(int[] altitude) {
    long total = 0;
    for (int start = 0; start < altitude.length; start++) {
        int lowest = Integer.MAX_VALUE;
        for (int end = start; end < altitude.length; end++) {
            lowest = Math.min(lowest, altitude[end]);
            total += lowest;
        }
    }
    return total;
}
```

It is correct. For `[3, 1, 2, 4]` it returns 17, which is the sum of the ten stretch minimums 3, 1, 2, 4, 1, 1, 2, 1, 1 and 1.

<!-- stage: bottleneck -->
### Half A Million Lines For A Trail

The double loop visits `n * (n + 1) / 2` stretches. At a hundred thousand checkpoints that is five billion additions, so the method is O(n^2). Most of that time is spent adding the same altitude again and again: in `[3, 1, 2, 4]`, the altitude 1 is added six times, once for each stretch that contains it, yet a single multiplication `1 * 6` would do.

The count of stretches in which one checkpoint is the lowest has no need of the stretches themselves. It depends on how far the stretch may reach to the left before meeting a lower checkpoint, and how far to the right. These two distances are what the boundary scans of the earlier lessons produce, so the treasurer's half-million lines collapse into one multiplication per checkpoint, once the equal altitudes have been given a single owner as in the previous lesson.

<!-- stage: insight -->
### Count By Multiplying Two Distances

The **contribution** of index `i` is its value times the number of stretches it owns, and the total is the sum of the contributions of all indices. Under an ownership rule with left wall `left` and right wall `right`, the **owned stretches** of `i` are all stretches that start somewhere in `left + 1 .. i` and end somewhere in `i .. right - 1`. Any start may be combined with any end, since every such stretch lies between the walls and contains `i`, so the number of them is the product `(i - left) * (right - i)`. The contribution of `i` is therefore `a[i] * (i - left) * (right - i)`.

The multiplication is only valid after the ownership proof of the previous lesson. If equal values were allowed to claim the same stretch, the product would count it twice for two different indices, and the sum would be too large. With one strict and one non-strict side, each stretch is counted exactly once, and the sum of products equals the sum of the stretch minimums.

Because the walls are known at the moment of a pop, the scan can add the contribution immediately. When index `t` is removed by index `j`, the right wall of `t` is `j`, and the left wall is the new top of the stack, or -1. A final step with a value smaller than everything flushes the stack so that the remaining indices are priced too, with right wall `n`. The last concern is the size of the numbers, and the rule of **widen before reduce** answers it: each factor is converted to `long` before it is multiplied, and the modulus is applied only after a product has been formed, never to a product that has already wrapped.

<!-- names: contribution, owned stretches, widen before reduce -->

The time is O(n), with one removal and one price per index.

<!-- stage: variables -->
### What Each Number Counts

For a popped index `t`, the value `a[t]` is the altitude being priced, `t - left` is the number of choices for the start of a stretch, and `j - t` is the number of choices for its end. The accumulator `total` holds the sum of contributions already priced, in `long`, and it is reduced modulo the required number when the problem asks for it. The stack holds indices that are still waiting for a right wall, and every index leaves it exactly once, either by being removed during the scan or by the flush at the end. The flush is a step that pretends the next altitude is lower than anything possible, so the scan runs for `j` from 0 to `n` inclusive and uses the smallest `int` as the pretend value at `j = n`. A pretend value of the smallest possible `int` also removes an index that really holds that value, since the removal test is "at least".

<!-- stage: trace -->
### Pricing A Trail As Indices Leave

Take the altitudes `3, 1, 2, 4`. The 3 and then the 1 arrive, and the 1 removes the 3 because it is smaller. The removed index 0 has left wall -1 and right wall 1, so it owns `1 * 1 = 1` stretch and contributes `3 * 1 = 3`. Then the 1 is pushed, the 2 and the 4 follow without removals, and the stack holds indices 1, 2 and 3. The flush at `j = 4` removes index 3, whose left wall is index 2, so it owns `1 * 1` stretch and contributes 4, and the total is 7. It then removes index 2, with left wall index 1 and right wall 4, so it owns `1 * 2 = 2` stretches and contributes 4, and the total is 11. Finally it removes index 1, with left wall -1, so it owns `2 * 3 = 6` stretches and contributes 6, which gives 17. The step to study is the flush, because most of the contributions are priced there.

Now take `2, 9, 3, 3`. The 3 at index 2 removes the 9, which owns one stretch and contributes 9. The second 3 removes the first 3, because the test is "at least", so the earlier 3 has left wall index 0 and right wall 3, owns 2 stretches and contributes 6. The flush then prices the later 3 with 3 stretches, which contributes 9, and the 2 with 4 stretches, which contributes 8. The total is 9 + 6 + 9 + 8, which is 32, the same as the brute-force sum.

```trace
{"cells":[3,1,2,4],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","total":0},"note":"The value 3 arrives. Nothing leaves the stack. The total is 0."},{"at":{"j":1},"vars":{"stack":"[1]","total":3},"note":"The value 1 arrives. Index 0 leaves with left wall -1 and right wall 1, so it owns 1 times 1 stretches and contributes 3 times 1, which is 3. The total is 3."},{"at":{"j":2},"vars":{"stack":"[1,2]","total":3},"note":"The value 2 arrives. Nothing leaves the stack. The total is 3."},{"at":{"j":3},"vars":{"stack":"[1,2,3]","total":3},"note":"The value 4 arrives. Nothing leaves the stack. The total is 3."},{"at":{"j":4},"vars":{"stack":"[]","total":17},"note":"The flush step arrives, lower than every value. Index 3 leaves with left wall 2 and right wall 4, so it owns 1 times 1 stretches and contributes 4 times 1, which is 4. Index 2 leaves with left wall 1 and right wall 4, so it owns 1 times 2 stretches and contributes 2 times 2, which is 4. Index 1 leaves with left wall -1 and right wall 4, so it owns 2 times 3 stretches and contributes 1 times 6, which is 6. The total is 17."}]}
```

```trace
{"cells":[2,9,3,3],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","total":0},"note":"The value 2 arrives. Nothing leaves the stack. The total is 0."},{"at":{"j":1},"vars":{"stack":"[0,1]","total":0},"note":"The value 9 arrives. Nothing leaves the stack. The total is 0."},{"at":{"j":2},"vars":{"stack":"[0,2]","total":9},"note":"The value 3 arrives. Index 1 leaves with left wall 0 and right wall 2, so it owns 1 times 1 stretches and contributes 9 times 1, which is 9. The total is 9."},{"at":{"j":3},"vars":{"stack":"[0,3]","total":15},"note":"The value 3 arrives. Index 2 leaves with left wall 0 and right wall 3, so it owns 2 times 1 stretches and contributes 3 times 2, which is 6. The total is 15."},{"at":{"j":4},"vars":{"stack":"[]","total":32},"note":"The flush step arrives, lower than every value. Index 3 leaves with left wall 0 and right wall 4, so it owns 3 times 1 stretches and contributes 3 times 3, which is 9. Index 0 leaves with left wall -1 and right wall 4, so it owns 1 times 4 stretches and contributes 2 times 4, which is 8. The total is 32."}]}
```

<!-- stage: code -->
### Pricing Indices At Removal

```java
static long sumOfMinimums(int[] a, long modulus) {
    int n = a.length;
    long total = 0;
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j <= n; j++) {
        int current = (j == n) ? Integer.MIN_VALUE : a[j];     // the flush value at j == n
        while (!stack.isEmpty() && a[stack.peekLast()] >= current) {
            int t = stack.removeLast();
            int left = stack.isEmpty() ? -1 : stack.peekLast();
            long owned = (long) (t - left) * (j - t);            // widen before multiplying
            total = (total + (owned % modulus) * a[t]) % modulus;
        }
        if (j < n) stack.addLast(j);
    }
    return ((total % modulus) + modulus) % modulus;               // normalize negative sums
}
```

The scan makes `n + 1` steps, and each index is pushed once and removed once, so the time is O(n) and the extra space is O(n). `owned % modulus` is below the modulus, so multiplying it by a value of at most about a billion stays inside `long`. The final line turns a possibly negative remainder, which Java's `%` leaves negative for a negative left operand, into a value from 0 up to the modulus minus one.

<!-- stage: applicability -->
### When A Sum Splits By Element

Use contribution counting when the answer is a sum or a count over all stretches, and each stretch is decided by one extreme element, its minimum or maximum. The invariant is that every stretch is owned by exactly one index, whose count is the product of the free choices on its two sides, so the sum over indices equals the sum over stretches. Establish the ownership rule first, then the walls, then the product, and only then the arithmetic.

The false friend is the same product applied without the proof. On `[5, 5, 5]`, taking strict walls on both sides gives the counts 3, 4 and 3, which total 10 where there are 6 stretches. A second false friend is a stretch quantity that is not decided by one element, such as the sum of the stretch or the difference between its largest and smallest values. A difference needs two extremes, and each needs its own ownership pass, so it splits into two separate sums and cannot be done with one product per index.

Do not use it when the stretches are not all contiguous ranges, for instance subsequences, where the count of choices is a power of two and not a product of distances. Also watch the arithmetic: `int` products overflow for arrays of about 100,000 elements, a modulus must be applied to `long` values, and a negative array value makes the running remainder negative.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Subarrays Owned By One Index (Author exercise)
<!-- id: ms-count-owned-one-index -->

**Prerequisites.** The duplicate-attribution lesson of this chapter.

**Problem.** An index `i` has a left wall `left` and a right wall `right`, with `left < i < right`. Return the number of subarrays `[s, e]` that satisfy `left < s <= i <= e < right`.

**Constraints.** -1 <= left < i < right <= 10^6. The answer can exceed the range of `int`, so use `long`.

**Example 1.** Input `left = -1`, `i = 2`, `right = 5`, output 9.

**Example 2.** Input `left = 2`, `i = 3`, `right = 4`, output 1, since only the single-element subarray qualifies.

**Hint.** How many different values can `s` take, and how many can `e` take? Do the two choices depend on each other?

**Changed decision.** First rung: the count is a product of two independent choices, each measured as a distance from the index to a wall.

#### [Vary] Sum Owned Minimum Contributions (Author exercise)
<!-- id: ms-sum-owned-contributions -->

**Prerequisites.** The Count Subarrays Owned By One Index exercise above.

**Problem.** Given an integer array `a` together with arrays `left` and `right` that already hold, for every index, a left wall and a right wall obtained with one strict and one non-strict side, return the sum over all indices of `a[i] * (i - left[i]) * (right[i] - i)`.

**Constraints.** 1 <= a.length <= 10^5, 1 <= a[i] <= 10^4, and the answer fits in `long`. Do not enumerate subarrays.

**Example 1.** Input `a = [3, 1, 2, 4]`, `left = [-1, -1, 1, 2]`, `right = [1, 4, 4, 4]`, output 17.

**Example 2.** Input `a = [2, 2]`, `left = [-1, -1]`, `right = [1, 2]`, output 6.

**Hint.** What does each term of the sum represent? Which type should the product have before it is multiplied by `a[i]`?

**Changed decision.** The output is a weighted sum, so each count is multiplied by a value and the products are added.

#### [Boundary] Negative And Repeated Values (Author exercise)
<!-- id: ms-negative-repeated-values -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `a` that may contain negative and repeated values, return the sum of the minimum of every subarray, reduced modulo 1,000,000,007 to a value from 0 to 1,000,000,006.

**Constraints.** 1 <= a.length <= 10^5 and -10^4 <= a[i] <= 10^4. Linear time.

**Example 1.** Input `a = [-1, 2, -1]`, output 1000000004, since the true sum is -3.

**Example 2.** Input `a = [-5, -5]`, output 999999992, since the three subarrays each have minimum -5.

**Hint.** Which part of the solution decides who owns a stretch, and which part only handles the size and sign of the numbers? Why does a negative total need one more step after the loop?

**Changed decision.** The ownership proof is unchanged, and the new work is arithmetic only: widening to `long`, reducing, and normalizing a negative remainder.

#### [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-minimums-stack -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `arr`, return the sum of the minimum of every contiguous subarray, modulo 1,000,000,007. Use a single stack pass that prices each index at the moment it is removed, and keep no separate arrays of left and right walls.

**Constraints.** 1 <= arr.length <= 10^5 and 1 <= arr[i] <= 10^9, with repeated values allowed.

**Example 1.** Input `arr = [2, 9, 3, 3]`, output 32.

**Example 2.** Input `arr = [4, 4, 4, 4]`, output 40.

**Hint.** At the moment an index is removed, which wall is the new top and which is the current index? How do the indices still on the stack at the end get priced?

**Changed decision.** The walls are not stored. Each index is priced as it leaves the stack, with a flush step at the end, and the values reach a billion so the arithmetic needs `long`.
