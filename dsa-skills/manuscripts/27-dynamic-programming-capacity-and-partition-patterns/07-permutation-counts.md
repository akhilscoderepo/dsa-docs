<!-- lesson-kind: standard -->
<!-- lesson-id: permutation-counts -->
## Permutation Counts

<!-- stage: context -->
### Counting Schedules For A Maintenance Window

A job scheduler fills a 4-minute maintenance window with tasks that last 1 or 2 minutes. The tasks run one after another, so the order is part of the schedule. Running a 1-minute task and then a 2-minute task is a different schedule from running the 2-minute task first. The window of 4 minutes has five schedules: 1 + 1 + 1 + 1, 1 + 1 + 2, 1 + 2 + 1, 2 + 1 + 1 and 2 + 2.

An engineer reuses the change-counting code from the previous lesson to display the number of schedules. It prints 3, because it treats 1 + 1 + 2, 1 + 2 + 1 and 2 + 1 + 1 as a single schedule. The display is wrong whenever a window has more than one task order.

Formally, `nums` is an array of distinct positive integers, and `target` is a nonnegative integer. A **sequence** is a list of values from `nums`, with repeats allowed, and two sequences are equal only when they have the same values in the same positions. The task is to count the sequences whose values add up to `target`. The empty sequence adds up to 0. The method never changes the array.

This lesson asks how to count sequences without listing them.

<!-- stage: naive -->
### Reusing The Combination Loop

The quick idea runs the method from the previous lesson unchanged. It processes one value at a time in the outer loop and updates the totals upward in the inner loop.

```java
static long countByValues(int[] nums, int target) {
    long[] ways = new long[target + 1];
    ways[0] = 1;
    for (int value : nums) {
        for (int t = value; t <= target; t++) ways[t] += ways[t - value];
    }
    return ways[target];
}
```

The method runs in O(target * k) time for k values and uses O(target) memory. It is correct for the question that the previous lesson asked. The open question is whether it also answers a question where the order of the values counts.

```predict
Run countByValues on nums [1, 2] with target 4. What does it return, and how many sequences add up to 4?

It returns 3, and 5 sequences add up to 4. The method writes every collection of values in one fixed order, with all the 1s before all the 2s. The sequences 1 + 2 + 1 and 2 + 1 + 1 never appear, so they are never counted.
```

<!-- stage: bottleneck -->
### The Fixed Order Hides Reordered Sequences

The combination loop fixes the order in which values may appear. That rule is the reason it counts each multiset once, and it is also the reason it cannot see a reordering. The count of sequences needs the opposite rule: after any prefix, every value must be allowed to come next.

A correct but slow method builds sequences one value at a time and recurses on the remaining sum. With k values and a smallest value `m`, the recursion branches k ways at each level and has depth up to `target / m`, so its call count is bounded by O(k^(target / m)). For the values 1, 2 and 3 and target 40, the recursion makes about 5 * 10^10 calls.

Most of those calls repeat. After the prefixes 1 + 2 and 2 + 1, the remaining sum is the same, and the number of ways to finish depends only on that remaining sum. There are `target + 1` possible remaining sums. A table with one entry per total does k reads per entry, which is O(target * k) time. The next section builds that table.

<!-- stage: insight -->
### Let Every Value Come Last

A sequence is a prefix followed by one final value. If the table knows how many sequences each smaller total has, the final value extends them.

<!-- names: last element, totals outside, candidates inside -->

#### One Entry For Each Total

Let `ways[t]` be the number of sequences whose values add up to `t`. The seed is `ways[0] = 1`, because the empty sequence adds up to 0. The answer is `ways[target]`. A total that no sequence reaches keeps the count 0.

#### The Last Element Splits Every Sequence

Take any nonempty sequence with sum `t`, and look at its **last element**, which is some value `v` from `nums` with `v <= t`. Removing it leaves a sequence with sum `t - v`. The reverse also works: appending `v` to any sequence with sum `t - v` gives a sequence with sum `t` whose last element is `v`. This pairing is one to one, so the sequences with last element `v` number exactly `ways[t - v]`. Different values for the last element give different sequences. So `ways[t]` is the sum of `ways[t - v]` over all values `v` with `v <= t`.

#### Totals Outside And Candidates Inside

Computing `ways[t]` needs the entries `ways[t - v]` to be final for every `v`. The loop therefore keeps the **totals outside**, in increasing order, and the **candidates inside**, where each value tries to be the last element. When the loop reaches `t`, all smaller totals are done. The invariant is that `ways[s]` is the exact number of sequences for every `s` the loop has passed. This is the loop that gave the wrong count in the previous lesson, and it answers the order-sensitive question here.

<!-- stage: variables -->
### Counts For Each Total

The inputs `nums` and `target` stay unchanged, and the method keeps these values.

- **ways** is a `long[]` of length `target + 1`; entry `t` counts the sequences that add up to `t`.
- **t** is the total that the outer loop computes, from 1 to `target`.
- **value** is the candidate that the inner loop tries as the last element.
- **ways[0]** is the seed 1 for the empty sequence.

The counts are `long` values, because sequences multiply quickly. For the values 1, 2 and 3 and target 40, the count is about 2.4 * 10^10, which exceeds the `int` range. Every value must be positive. A value of 0 or less would make `t - value` equal to `t` or larger, which reads an entry that is not final or lies outside the table.

<!-- stage: trace -->
### Two Runs Over Small Totals

#### The Maintenance Window

The first run uses the values 1 and 2 and target 4. Each cell is a total from 0 to 4, and the pointer `t` marks the entry that changes. The variable `value` is the candidate last element, `add` is the amount it contributes, and `ways` is the entry after the contribution. The first step shows the seed.

Total 2 receives 1 from the last element 1 and 1 from the last element 2, so it holds 2. Total 3 receives 2 and then 1, so it holds 3. Total 4 receives 3 from the last element 1 and 2 from the last element 2, so it holds 5, which matches the five schedules.

```trace
{"cells":[0,1,2,3,4],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"value":0,"add":0,"ways":1},"note":"The seed is the empty sequence, so the count for total 0 is 1."},{"at":{"t":1},"vars":{"value":1,"add":1,"ways":1},"note":"Total 1 with the last element 1 gains 1 from total 0, so its count becomes 1."},{"at":{"t":2},"vars":{"value":1,"add":1,"ways":1},"note":"Total 2 with the last element 1 gains 1 from total 1, so its count becomes 1."},{"at":{"t":2},"vars":{"value":2,"add":1,"ways":2},"note":"Total 2 with the last element 2 gains 1 from total 0, so its count becomes 2."},{"at":{"t":3},"vars":{"value":1,"add":2,"ways":2},"note":"Total 3 with the last element 1 gains 2 from total 2, so its count becomes 2."},{"at":{"t":3},"vars":{"value":2,"add":1,"ways":3},"note":"Total 3 with the last element 2 gains 1 from total 1, so its count becomes 3."},{"at":{"t":4},"vars":{"value":1,"add":3,"ways":3},"note":"Total 4 with the last element 1 gains 3 from total 3, so its count becomes 3."},{"at":{"t":4},"vars":{"value":2,"add":2,"ways":5},"note":"Total 4 with the last element 2 gains 2 from total 2, so its count becomes 5."}]}
```

#### Totals That Nothing Reaches

The second run uses the values 2 and 3 and target 7. Total 1 has no value that fits, so it stays 0 and the trace has no step for it. Total 5 receives 1 from the last element 2, which extends the sequence for 3, and 1 from the last element 3, which extends the sequence for 2. Total 7 receives 2 from the last element 2 and 1 from the last element 3, so it holds 3. The sequences are 2 + 2 + 3, 2 + 3 + 2 and 3 + 2 + 2.

```trace
{"cells":[0,1,2,3,4,5,6,7],"pointers":["t"],"steps":[{"at":{"t":0},"vars":{"value":0,"add":0,"ways":1},"note":"The seed is the empty sequence, so the count for total 0 is 1."},{"at":{"t":2},"vars":{"value":2,"add":1,"ways":1},"note":"Total 2 with the last element 2 gains 1 from total 0, so its count becomes 1."},{"at":{"t":3},"vars":{"value":3,"add":1,"ways":1},"note":"Total 3 with the last element 3 gains 1 from total 0, so its count becomes 1."},{"at":{"t":4},"vars":{"value":2,"add":1,"ways":1},"note":"Total 4 with the last element 2 gains 1 from total 2, so its count becomes 1."},{"at":{"t":5},"vars":{"value":2,"add":1,"ways":1},"note":"Total 5 with the last element 2 gains 1 from total 3, so its count becomes 1."},{"at":{"t":5},"vars":{"value":3,"add":1,"ways":2},"note":"Total 5 with the last element 3 gains 1 from total 2, so its count becomes 2."},{"at":{"t":6},"vars":{"value":2,"add":1,"ways":1},"note":"Total 6 with the last element 2 gains 1 from total 4, so its count becomes 1."},{"at":{"t":6},"vars":{"value":3,"add":1,"ways":2},"note":"Total 6 with the last element 3 gains 1 from total 3, so its count becomes 2."},{"at":{"t":7},"vars":{"value":2,"add":2,"ways":2},"note":"Total 7 with the last element 2 gains 2 from total 5, so its count becomes 2."},{"at":{"t":7},"vars":{"value":3,"add":1,"ways":3},"note":"Total 7 with the last element 3 gains 1 from total 4, so its count becomes 3."}]}
```

<!-- stage: code -->
### Totals Outside And Values Inside

The method returns the number of sequences. It computes the totals in increasing order and tries every value as the last element.

```java
static long countSequences(int[] nums, int target) {
    long[] ways = new long[target + 1];
    ways[0] = 1;
    for (int t = 1; t <= target; t++) {
        for (int value : nums) {
            if (value <= t) ways[t] += ways[t - value];
        }
    }
    return ways[target];
}
```

The condition `value <= t` keeps the index `t - value` inside the table. The cost is O(target * k) time and O(target) memory. An empty `nums` array returns 1 for target 0 and 0 for every positive target.

<!-- stage: applicability -->
### Recognizing Counts That Respect Order

#### Reading The Cue

Use this method when reusable values must add up to an exact total and the order of the values makes sequences different. Phrases such as "different sequences", "ordered ways" and "1 + 2 and 2 + 1 are different" point here. The table indexes the total, and every entry sums over the possible last elements.

#### Checking The Invariant

The invariant says that, for every total the loop has passed, the entry equals the number of sequences with that sum. Test target 0, which must return 1. Test a positive target with an empty array, which must return 0. Test a value larger than the target, which must contribute nothing. Test a long run of totals to see the counts outgrow an `int`.

#### Avoiding The False Friend

The false friend is the combination loop of the previous lesson, which returns 3 for the maintenance window. A second one is a table of `int` entries, which overflows silently. A third is a value of 0 or a negative value in the input, which breaks the order of evaluation because the entry would read itself or a later entry. A last one is a recursion without memoization, which repeats the same remaining total many times.

<!-- stage: exercises -->
### Exercises

#### [Build] Ordered Sums To Four (Author exercise)
<!-- id: cap-prm-ordered-sums -->

**Prerequisites.** The last-element split and the totals-outside loop from this lesson.

**Problem.** A sequence uses only the values 1 and 2, and its order matters. Return the number of sequences whose values add up to exactly `total`. The case `total = 4` has five sequences.

**Constraints.** The limits are:
- **Total** satisfies `0 <= total <= 60`.
- **Empty** sequence is the only one that adds up to 0.
- **Result** is a `long`.

**Example 1.** Input `total = 4`, output `5`.

**Example 2.** Input `total = 0`, output `1`.

**Hint.** Which two earlier totals can precede the last element, and what does each last element contribute?

**Changed decision.** The method keeps the totals outside and has two fixed candidates inside. Each entry adds exactly the entries one and two below it.

#### [Vary] Combination Sum IV (LeetCode 377)
<!-- id: cap-prm-combination-sum-four -->

**Prerequisites.** The exercise above.

**Problem.** An array `nums` of distinct positive integers and an integer `target` are given. Count the sequences of values from `nums`, with repeats allowed, whose sum is exactly `target`. Sequences with the same values in different orders are different sequences.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 50`.
- **Value** satisfies `1 <= nums[i] <= 200`, and values are distinct.
- **Target** satisfies `0 <= target <= 500`.
- **Result** is a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [2,3,6]`, `target = 8`, output `6`.

**Example 2.** Input `nums = [5]`, `target = 3`, output `0`.

**Hint.** For one total, which values can be the last element, and which smaller total does each leave?

**Changed decision.** Every value in `nums` is a candidate last element for every total. The method sums the entries below the current total in place of using two fixed steps.

#### [Boundary] Overflow And Nonpositive Values (Author exercise)
<!-- id: cap-prm-overflow-nonpositive -->

**Prerequisites.** The two exercises above.

**Problem.** An array `nums` of distinct integers may contain zero or negative values. Sequences may use only the positive values of `nums`, with repeats allowed, and order matters. Return the number of such sequences whose sum is exactly `target`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 20`.
- **Value** satisfies `-50 <= nums[i] <= 50`, and values are distinct.
- **Target** satisfies `0 <= target <= 60`, and the empty sequence adds up to 0.
- **Result** is a `long`, and the answer can exceed the `int` range.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [0,-2,3]`, `target = 6`, output `1`.

**Example 2.** Input `nums = []`, `target = 0`, output `1`.

**Hint.** Which transitions would read an entry that is not final yet, and which values cause them?

**Changed decision.** The method skips every value that is zero or negative, because such a value does not shrink the remaining total. The table type is `long` so large counts stay exact.

#### [Recognize] Compare With Coin Change II (Author exercise)
<!-- id: cap-prm-compare-coin-change -->

**Prerequisites.** All three exercises above and the previous lesson.

**Problem.** An array `coins` of distinct positive denominations and a nonnegative integer `amount` are given. For each `a` from 0 to `amount`, let `combos(a)` be the number of combinations that add up to `a`, where order does not matter, and `seqs(a)` the number of sequences, where order matters. Return how many values of `a` satisfy `seqs(a) > combos(a)`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= coins.length <= 8`.
- **Denomination** satisfies `1 <= coins[i] <= 30`, and values are distinct.
- **Amount** satisfies `0 <= amount <= 60`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `coins = [1,2]`, `amount = 4`, output `2`.

**Example 2.** Input `coins = [3]`, `amount = 10`, output `0`.

**Hint.** Both tables use the same update with different loop owners. Which loop must be outside for each table?

**Changed decision.** The method builds both tables with the same update and swapped loops, and then compares them entry by entry. Equal entries do not count.
