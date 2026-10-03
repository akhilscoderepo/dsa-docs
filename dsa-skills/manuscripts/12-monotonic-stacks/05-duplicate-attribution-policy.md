<!-- lesson-kind: standard -->
<!-- lesson-id: duplicate-attribution-policy -->
## Duplicate-Attribution Policy

<!-- stage: context -->
### One Badge For Each Stretch Of Days

A weather club keeps a daily record of the lowest temperature. At the end of the season the secretary looks at every stretch of consecutive days, from a single day up to the whole season, and gives one "coldest day" badge to each stretch. The badge goes to a day inside the stretch that had the lowest temperature. For a season of `n` days there are `n * (n + 1) / 2` stretches, so exactly that many badges must be handed out, no more and no fewer.

The trouble starts when two days in the same stretch have the same lowest temperature. Both days have an equal claim, and an unwise secretary might give the badge to both, which makes too many badges, or to neither because each of them looks tied, which makes too few. The committee wants a rule that settles every tie in the same way, and a quick way to say how many badges each day collects.

<!-- stage: naive -->
### Hand Out Every Badge By Hand

The direct method visits every stretch, finds its lowest day, and gives the badge to the last day in the stretch that holds that lowest value. Fixing the left end and growing the right end keeps the running lowest value as it goes.

```java
static long[] badgesByStretch(int[] t) {
    int n = t.length;
    long[] badges = new long[n];
    for (int start = 0; start < n; start++) {
        int owner = start;
        for (int end = start; end < n; end++) {
            if (t[end] <= t[owner]) owner = end;
            badges[owner]++;
        }
    }
    return badges;
}
```

It follows the committee's rule, and for `[2, 2]` it gives `[1, 2]`: the first day owns only its own stretch, and the second day takes the stretch of both days because ties go to the later day.

<!-- stage: bottleneck -->
### Every Stretch Is Visited Again

The two loops visit all `n * (n + 1) / 2` stretches one by one. For a season of 100,000 days that is about five billion visits, so the method is O(n^2) time, and it does that work although the answer for each day is only a single number.

The visits are not independent. The stretches won by one day all contain that day, and they are exactly those whose left end lies to the right of the nearest earlier day that would take the badge away, and whose right end lies to the left of the nearest later day that would take it away. These two limits can be computed for every day with the boundary scans of the previous lesson, and the number of stretches won is the product of the free choices on each side. The method counts stretches one at a time that could be counted by multiplying two distances. The remaining difficulty is the meaning of "take it away" when the other day has an equal temperature.

<!-- stage: insight -->
### Break Every Tie On One Side

An **ownership rule** assigns each stretch to exactly one day. The rule chosen here is that the lowest value wins, and among equal lowest values the later day wins. Day `i` then owns a stretch exactly when every day before `i` in the stretch is at least as warm as day `i`, and every day after `i` in the stretch is strictly warmer. Written as walls, the left wall of `i` is the nearest earlier day that is strictly colder, which is the **strict side**, and the right wall is the nearest later day that is colder or equal, which is the **non-strict side**. The walls use opposite comparisons, and that asymmetry is the whole point.

Both strict walls would let two equal days each extend over the other, so a stretch holding both would be owned twice. Both non-strict walls would stop each of the two equal days at the other, so a stretch containing both would be owned by nobody. With one side strict and one side non-strict, the stretch holding two equal days is owned by exactly the later one, because the earlier day is stopped by its equal partner on the right, while the later day sees the earlier one only as an equal on its strict left side and passes over it.

<!-- names: ownership rule, strict side, non-strict side -->

The number of stretches owned by day `i` is the number of left ends between its left wall and `i`, times the number of right ends from `i` up to its right wall, which is `(i - left) * (right - i)`. The proof that the rule is correct is the total: the counts of all days must add up to `n * (n + 1) / 2`. The mirror rule, with the strict side on the right, gives the earlier day the badge, and it is just as correct. Which side is strict is a convention to choose once, and not a law of the problem.

<!-- stage: variables -->
### Two Walls With Two Meanings

For each index, the `left` wall is the index of the nearest earlier value that is strictly smaller, or -1, and the `right` wall is the index of the nearest later value that is smaller or equal, or `n`. A stretch owned by `i` starts at one of the indices `left + 1` through `i` and ends at one of the indices `i` through `right - 1`, so there are `i - left` starts and `right - i` ends. The product is held in a `long`, since for `n` near 100,000 the number of stretches is above two billion. A single scan with removal of every top that is at least the current value produces exactly these walls, because a removed index meets a later value that is smaller or equal, and the survivor beneath it is strictly smaller.

<!-- stage: trace -->
### Ownership On A Short Season

Take the season `3, 1, 3, 1`. The first 3 has left wall -1 and right wall 1, since the next day, a 1, is colder, so it owns one stretch. The first 1 has no strictly colder day to its left, so its left wall is -1, and its right wall is the later 1 at index 3, which is equal and therefore non-strict. It owns `2 * 2 = 4` stretches. The second 3 has left wall 1 and right wall 3, so it owns 1. The last 1 has no strictly colder day on its left, so its left wall is -1, and its right wall is the sentinel 4, which gives `4 * 1 = 4`. The four counts add up to 10, which is `4 * 5 / 2`. The step to study is the first 1, which stops at the later 1 on its right and so does not claim the stretches that contain both.

Now take `2, 2, 2` and the single scan that removes every top that is at least the current value. The second 2 removes the first and gives it the right wall 1. The third 2 removes the second. After the scan the remaining index gets the sentinel 3, and the counts are 1, 2 and 3, which add up to 6.

```trace
{"cells":[3,1,3,1],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"left":-1,"right":1,"owned":1,"total":1},"note":"Index 0 has left wall the sentinel -1 and right wall index 1, so it has 1 left ends and 1 right ends and owns 1 subarrays."},{"at":{"i":1},"vars":{"left":-1,"right":3,"owned":4,"total":5},"note":"Index 1 has left wall the sentinel -1 and right wall index 3, so it has 2 left ends and 2 right ends and owns 4 subarrays. The right wall has an equal value and still stops the walk."},{"at":{"i":2},"vars":{"left":1,"right":3,"owned":1,"total":6},"note":"Index 2 has left wall index 1 and right wall index 3, so it has 1 left ends and 1 right ends and owns 1 subarrays."},{"at":{"i":3},"vars":{"left":-1,"right":4,"owned":4,"total":10},"note":"Index 3 has left wall the sentinel -1 and right wall the sentinel 4, so it has 4 left ends and 1 right ends and owns 4 subarrays."}]}
```

```trace
{"cells":[2,2,2],"pointers":["j"],"steps":[{"at":{"j":0},"vars":{"stack":"[0]","right":"[3,3,3]"},"note":"Nothing is removed. The stack is empty, so the left wall of index 0 is -1."},{"at":{"j":1},"vars":{"stack":"[1]","right":"[1,3,3]"},"note":"The value 2 removes index 0, because it is smaller or equal, so each gets right wall 1. The stack is empty, so the left wall of index 1 is -1."},{"at":{"j":2},"vars":{"stack":"[2]","right":"[1,2,3]"},"note":"The value 2 removes index 1, because it is smaller or equal, so each gets right wall 2. The stack is empty, so the left wall of index 2 is -1."}]}
```

<!-- stage: code -->
### One Scan Gives Both Walls

```java
static long[] ownedCounts(int[] a) {
    int n = a.length;
    int[] left = new int[n];
    int[] right = new int[n];
    java.util.Arrays.fill(right, n);
    java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
    for (int j = 0; j < n; j++) {
        while (!stack.isEmpty() && a[stack.peekLast()] >= a[j]) {
            right[stack.removeLast()] = j;          // a[j] is smaller or equal: non-strict right wall
        }
        left[j] = stack.isEmpty() ? -1 : stack.peekLast();   // survivor is strictly smaller
        stack.addLast(j);
    }
    long[] owned = new long[n];
    for (int i = 0; i < n; i++) owned[i] = (long) (i - left[i]) * (right[i] - i);
    return owned;
}
```

The scan costs O(n) time and O(n) extra space, and the single comparison `>=` produces the strict left wall and the non-strict right wall together, without a second pass. To obtain the mirror rule, scan from the right with the same comparison, or flip the test to `>` and let the survivor be the non-strict left wall. The cast to `long` comes before the multiplication, since `(i - left[i]) * (right[i] - i)` in `int` arithmetic can wrap for a long season.

<!-- stage: applicability -->
### When Ties Could Claim The Same Stretch

Use an ownership rule whenever a sum or a count is taken over all stretches and each stretch is credited to one of its extreme elements, so that equal extremes could claim the same stretch. The invariant is that every stretch has exactly one owner, which holds when one wall stops at equal values and the other passes over them, and the check is that the owned counts sum to `n * (n + 1) / 2`. State which side is strict before writing any boundary code, and say why.

The false friend is symmetric treatment. Strict comparisons on both sides look neat and are right for arrays with distinct values, and non-strict on both sides is equally tidy, yet on `[5, 5, 5]` the first rule counts 10 stretches in place of 6 and the second counts 3. Neither is a bug in the scan itself. The bug is the missing decision about the ties. Another false friend is the habit of remembering that a certain direction takes `>=`, since the correct side depends on the convention chosen, and the mirror convention flips it.

Do not rely on the rule when the question asks for the distinct values of the minimums or the number of different stretches, since there the equal elements do not each get their own count. Arrays with distinct values never need the rule, and then the sides may be chosen freely, but the habit of stating the convention costs nothing and protects the first test with a repeated value.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Equal Minima Ownership (Author exercise)
<!-- id: ms-two-equal-minima -->

**Prerequisites.** The boundary lesson of this chapter.

**Problem.** Given an integer array `a`, every contiguous subarray is given to exactly one index: the last index inside the subarray that holds the subarray's minimum value. Return an array `owned` where `owned[i]` is the number of subarrays given to index `i`.

**Constraints.** 1 <= a.length <= 2000 and -10^9 <= a[i] <= 10^9. Enumerating subarrays directly is acceptable for this rung.

**Example 1.** Input `a = [2, 2]`, output `[1, 2]`, since the subarray `[2, 2]` goes to the later index.

**Example 2.** Input `a = [3, 1, 3, 1]`, output `[1, 4, 1, 4]`.

**Hint.** List the three subarrays of `[2, 2]` by hand and say who owns each. How many subarrays does a length of 4 produce in total, and do your counts add up to it?

**Changed decision.** First rung: a tie is settled by a stated rule, and every subarray gets exactly one owner.

#### [Vary] Strict Left, Non-Strict Right (Author exercise)
<!-- id: ms-strict-left-nonstrict-right -->

**Prerequisites.** The Two Equal Minima Ownership exercise above.

**Problem.** For each index `i` of an integer array `a`, return the pair `[left, right]` where `left` is the nearest earlier index whose value is strictly smaller than `a[i]`, or -1, and `right` is the nearest later index whose value is smaller than or equal to `a[i]`, or `n`.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. Linear time.

**Example 1.** Input `a = [3, 1, 3, 1]`, output `[[-1, 1], [-1, 3], [1, 3], [-1, 4]]`.

**Example 2.** Input `a = [2, 2, 1, 2]`, output `[[-1, 1], [-1, 2], [-1, 4], [2, 4]]`.

**Hint.** Which single comparison, used to remove tops in one forward scan, produces both walls? Which wall is read when an index is removed, and which is read from the survivor?

**Changed decision.** The two sides use opposite comparisons, so that equal values are passed over on one side and stop the walk on the other.

#### [Boundary] All Equal Array (Author exercise)
<!-- id: ms-all-equal-ownership -->

**Prerequisites.** The two exercises above.

**Problem.** For an integer array `a`, compute the total number of owned subarrays, meaning the sum of `(i - left) * (right - i)` over all indices, under three conventions: both walls strict, both walls non-strict, and strict left with non-strict right. Return the three totals in that order as an array of `long`.

**Constraints.** 1 <= a.length <= 10^5 and -10^9 <= a[i] <= 10^9. The totals can exceed the range of `int`.

**Example 1.** Input `a = [5, 5, 5]`, output `[10, 3, 6]`.

**Example 2.** Input `a = [4]`, output `[1, 1, 1]`, since a single element has one subarray under any convention.

**Hint.** Which of the three totals must equal `n * (n + 1) / 2` for every input, and what do the other two tell you about the tie handling when the values are all equal?

**Changed decision.** The check changes from boundary positions to a total, so a wrong convention shows up as a count that does not match the number of subarrays.

#### [Recognize] Sum of Subarray Minimums (LeetCode 907)
<!-- id: ms-sum-minimums-convention -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `arr`, return two numbers in an array: the sum of the minimum of every contiguous subarray, taken modulo 1,000,000,007, and the number of subarrays that your ownership rule assigned, which must equal `n * (n + 1) / 2` for the rule to be correct.

**Constraints.** 1 <= arr.length <= 30000 and 1 <= arr[i] <= 30000, with repeated values allowed. State the ownership rule before computing the sum.

**Example 1.** Input `arr = [3, 1, 2, 4]`, output `[17, 10]`.

**Example 2.** Input `arr = [1, 2, 1, 2, 1]`, output `[17, 15]`.

**Hint.** What does each index own under the rule from this lesson? How would you notice that the rule is wrong from the second number alone?

**Changed decision.** Besides the sum, the answer carries the count of owned subarrays, so the tie convention is verified in the output and not assumed.
