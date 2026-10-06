<!-- lesson-kind: standard -->
<!-- lesson-id: shortest-subarray-deque-state -->
## Find The Shortest Subarray With Negatives

<!-- stage: context -->
### A Ledger With Deposits And Withdrawals

A ledger lists the daily change of an account. Deposits are positive and withdrawals are negative. An analyst wants the shortest run of consecutive days whose total change reaches a target. The first version grows a run on the right and shrinks it on the left once the total reaches the target. It works on a ledger that has only deposits. On a ledger with withdrawals it misses runs that exist, and it reports that none exists.

This lesson asks why the shrinking method fails when values can be negative, and what a deque can keep in its place. The deque holds prefix sums, which are running totals of the ledger, and the lesson shows which totals deserve a place in it.

<!-- stage: naive -->
### Comparing Every Pair Of Running Totals

A prefix sum at position `b` is the total of the first `b` values, and the prefix sum at position 0 is zero. The total of the run from position `a` up to position `b - 1` equals `P[b] - P[a]`. The direct plan checks every pair of positions.

```java
static int shortestByPairs(int[] nums, long target) {
    int n = nums.length;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    int best = -1;
    for (int end = 1; end <= n; end++) {
        for (int start = 0; start < end; start++) {
            if (prefix[end] - prefix[start] >= target) {           // this run reaches the target
                int len = end - start;
                if (best == -1 || len < best) best = len;
            }
        }
    }
    return best;
}
```

The method is correct for every input. For `nums = [3, -2, 4]` and `target = 5` it returns 3, because only the whole array totals 5.

<!-- stage: bottleneck -->
### Why Shrinking Fails And Pairs Cost

```predict
The values are 4, -5, 6, -1, 7 and the target is 12. A method grows the run on the right and shrinks it on the left only when the total reaches the target. Does it find the run 6, -1, 7, which totals 12?

No. The total of the whole array is 11 and never reaches 12, so the method never shrinks and never tests the last three values alone. A negative value lowers the total, so a longer run can have a smaller total.
```

The shrinking method assumes that a longer run never has a smaller total. Negative values break that assumption. One successful test no longer justifies moving the left end. The pair method avoids the assumption and pays O(n^2) for it. With `n = 100,000` it makes about five billion comparisons. The repeated work is that each end position tests start positions that can never give a shorter run than a start the method already holds.

<!-- stage: insight -->
### Keeping Only Starts That Can Still Win

#### Turning Runs Into Pairs Of Prefix Sums

Write `P[i]` for the prefix sum at position `i`. A run from position `a` to position `b - 1` has total `P[b] - P[a]`, and it has length `b - a`. The task becomes: find the pair `a < b` with `P[b] - P[a] >= target` and the smallest `b - a`. Each position `a` is a **start candidate**, which is a prefix position that may still begin the best run.

#### Dropping Starts From The Back

A start candidate `a1` is useless when a later position `a2` has `P[a2] <= P[a1]`. For every end `b` after `a2`, the run from `a2` has a total at least as large and a length at least one shorter. The back of the deque therefore removes every start whose prefix sum is not smaller than the new prefix sum. The stored prefix sums then strictly increase from the front to the back.

#### Dropping Starts From The Front

The front start is the earliest, so it gives the longest run among the stored starts. When `P[b] - P[front] >= target`, the run from the front reaches the target at length `b - front`. Every later end gives a longer run from the same start, so that start is **used up** and leaves the front for good. The loop tests the next front, because it may reach the target as well. The invariant is that the deque holds start candidates with strictly increasing prefix sums, and no stored start has reached the target yet. Every position is appended in one step and popped in at most one later step, so the total cost is O(n).

<!-- names: prefix sum, start candidate, used up -->

<!-- stage: variables -->
### What The Method Keeps

The method keeps five pieces of state.

- **Prefix array** holds `n + 1` totals of type `long`, with `P[0] = 0`.
- **Deque** holds start candidates, with strictly increasing prefix sums and increasing positions.
- **b** is the end position, and it moves from 0 to `n`.
- **Best** is the shortest length found so far, and `-1` means none yet.
- **Target** is the total the run must reach.

The array type is `long` because `n` values of 10^9 sum to more than an `int` can hold.

<!-- stage: trace -->
### Following Two Removals Through A Run

The first trace follows `nums = [3, -2, 4, -1, 5]` with a target of 6. The prefix sums are `0, 3, 1, 5, 4, 9`. At position 2 the prefix sum 1 removes position 1 from the back, because 3 is not smaller than 1. At position 5 the prefix sum 9 reaches the target from the start at position 0, and the run has length 5. The front is used up and leaves. The next front, position 2, also reaches the target with length 3. The third front, position 4, does not, so the loop stops. The best length is 3.

The second trace follows `nums = [4, -5, 6, -1, 7]` with a target of 12. The prefix sums are `0, 4, -1, 5, 4, 11`. Nothing reaches the target until the last position is processed. The best length is 3, from the start at position 2 to the end at position 5. The shrinking method from the opening reports no run at all for this input.

```trace
{"cells":[0,3,1,5,4,9],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"prefix_sums":"[0]","deque":"[0]","best":-1},"note":"Prefix index 0 has prefix sum 0. The front does not reach the target. Prefix index 0 is appended."},{"at":{"b":1},"vars":{"prefix_sums":"[0,3]","deque":"[0,1]","best":-1},"note":"Prefix index 1 has prefix sum 3. The front does not reach the target. Prefix index 1 is appended."},{"at":{"b":2},"vars":{"prefix_sums":"[0,3,1]","deque":"[0,2]","best":-1},"note":"Prefix index 2 has prefix sum 1. The front does not reach the target. The back removes prefix index 1 because 1 is not larger. Prefix index 2 is appended."},{"at":{"b":3},"vars":{"prefix_sums":"[0,3,1,5]","deque":"[0,2,3]","best":-1},"note":"Prefix index 3 has prefix sum 5. The front does not reach the target. Prefix index 3 is appended."},{"at":{"b":4},"vars":{"prefix_sums":"[0,3,1,5,4]","deque":"[0,2,4]","best":-1},"note":"Prefix index 4 has prefix sum 4. The front does not reach the target. The back removes prefix index 3 because 4 is not larger. Prefix index 4 is appended."},{"at":{"b":5},"vars":{"prefix_sums":"[0,3,1,5,4,9]","deque":"[4,5]","best":3},"note":"Prefix index 5 has prefix sum 9. The front passes the target test and is removed for starts 0, 2, giving the best length 3. Prefix index 5 is appended."}]}
```

```trace
{"cells":[0,4,-1,5,4,11],"pointers":["b"],"steps":[{"at":{"b":0},"vars":{"prefix_sums":"[0]","deque":"[0]","best":-1},"note":"Prefix index 0 has prefix sum 0. The front does not reach the target. Prefix index 0 is appended."},{"at":{"b":1},"vars":{"prefix_sums":"[0,4]","deque":"[0,1]","best":-1},"note":"Prefix index 1 has prefix sum 4. The front does not reach the target. Prefix index 1 is appended."},{"at":{"b":2},"vars":{"prefix_sums":"[0,4,-1]","deque":"[2]","best":-1},"note":"Prefix index 2 has prefix sum -1. The front does not reach the target. The back removes prefix indexs 1, 0 because -1 is not larger. Prefix index 2 is appended."},{"at":{"b":3},"vars":{"prefix_sums":"[0,4,-1,5]","deque":"[2,3]","best":-1},"note":"Prefix index 3 has prefix sum 5. The front does not reach the target. Prefix index 3 is appended."},{"at":{"b":4},"vars":{"prefix_sums":"[0,4,-1,5,4]","deque":"[2,4]","best":-1},"note":"Prefix index 4 has prefix sum 4. The front does not reach the target. The back removes prefix index 3 because 4 is not larger. Prefix index 4 is appended."},{"at":{"b":5},"vars":{"prefix_sums":"[0,4,-1,5,4,11]","deque":"[4,5]","best":3},"note":"Prefix index 5 has prefix sum 11. The front passes the target test and is removed for start 2, giving the best length 3. Prefix index 5 is appended."}]}
```

<!-- stage: code -->
### The Method With Two Removal Loops

```java
static int shortestSubarray(int[] nums, long target) {
    int n = nums.length;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];   // long, because sums overflow int
    int best = -1;
    Deque<Integer> d = new ArrayDeque<>();                  // start candidates, prefix sums increasing
    for (int b = 0; b <= n; b++) {
        while (!d.isEmpty() && prefix[b] - prefix[d.peekFirst()] >= target) {
            int len = b - d.pollFirst();                    // the start is used up after this run
            if (best == -1 || len < best) best = len;
        }
        while (!d.isEmpty() && prefix[d.peekLast()] >= prefix[b]) d.pollLast();   // dominated starts leave
        d.addLast(b);
    }
    return best;
}
```

The front loop runs first because it reads the old deque, and the back loop runs second because it prepares the new start. A new position never ends a run with itself, since the run would be empty. The method assumes a positive target. A target of zero or less would let the empty run qualify, and the problem asks for a non-empty run.

- **Time** is O(n), because the two loops together never pop a position twice.
- **Space** is O(n) for the `long` prefix array, and the deque adds up to n + 1 positions.

<!-- stage: applicability -->
### Telling Shrinking From Deque Methods

#### Applying The Invariant

Use this method when a run must reach a target total, values can be negative, and the answer is the shortest length. The invariant is that the stored starts have strictly increasing prefix sums and none has reached the target. The target must be positive, so that a run of zero values cannot qualify.

#### Finding The False Friend

The false friend is the shrinking method for non-negative values. It moves the left end forward after each success, and it is correct only when extending a run never lowers its total. A single negative value breaks that rule, and the method then misses valid runs.

A second false friend is a deque that stores array positions instead of prefix positions. The run total depends on two prefix sums, so the stored items must be prefix positions.

#### No-Go Conditions

Do not use the method when the question asks for the longest run, because used-up starts are exactly the ones a longest run would need. Do not use it when the total must equal the target instead of reaching it, because the removal of dominated starts assumes that a larger total is acceptable. A hash map from prefix sums to positions fits the equality question.

<!-- stage: exercises -->
### Exercises

#### [Build] Prefix-Pair Difference (Author exercise)
<!-- id: dq-prefix-pair -->

**Prerequisites.** Prefix sums from Chapter 07; this lesson.

**Problem.** An integer array `nums` has `n` values. Its prefix array `P` has `n + 1` entries, where `P[0] = 0` and `P[i + 1] = P[i] + nums[i]`. Each query is a pair `(a, b)` with `0 <= a < b <= n`. The answer to a query is `P[b] - P[a]`, which is the total of `nums[a]` through `nums[b - 1]`. Return the array of answers in query order.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Values** are integers between -1,000,000,000 and 1,000,000,000.
- **Queries** number between 0 and 100,000, and each satisfies `0 <= a < b <= n`.
- **Output** is a `long[]`, because a total can exceed the `int` range.

**Example 1.** Input `nums = [3, -2, 4, -1, 5]`, queries `[[0, 3], [1, 5]]`, output `[5, 6]`.

**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000]`, queries `[[0, 3]]`, output `[3000000000]`.

**Hint.** The right prefix is `P[b]`, which holds the first `b` values. Which type must the prefix array have for Example 2?

**Changed decision.** First exercise of the lesson: a run becomes a difference of two prefix sums.

#### [Vary] Remove Dominated Prefixes (Author exercise)
<!-- id: dq-dominated-prefixes -->

**Prerequisites.** The prefix pair exercise above and the weaker-value removal from earlier lessons.

**Problem.** An array `P` of `long` values holds prefix sums. Process the positions `0, 1, ..., P.length - 1` in order with a deque of positions. At position `b`, remove from the back every stored position `j` with `P[j] >= P[b]`, then append `b`. Return the stored positions after the last step, from the front to the back.

**Constraints.** The limits are:
- **Length** is between 1 and 100,001.
- **Values** are `long` integers with absolute value at most 10^14.
- **Ties** are removed, because the test is greater than or equal.
- **Output** is an `int[]` whose prefix sums strictly increase.

**Example 1.** Input `P = [0, 3, 1, 5, 4, 9]`, output `[0, 2, 4, 5]`.

**Example 2.** Input `P = [5, 5, 5]`, output `[2]`.

**Hint.** A later start with a prefix sum that is not larger is at least as good for every end. Which stored positions does a smaller or equal value remove?

**Changed decision.** The deque now stores prefix positions, and equal values replace older ones.

#### [Boundary] Negative Values And Long Sums (Author exercise)
<!-- id: dq-negative-long -->

**Prerequisites.** Both exercises above.

**Problem.** The shrinking method grows a run on the right and adds each value to a running total. While the total is at least `target`, it records the run length and removes the leftmost value. The method returns the shortest recorded length, or `-1` when it records none. Let `answer` be the true shortest length of a non-empty run with a total of at least `target`, or `-1` when no such run exists. Return `true` when the shrinking method and `answer` differ, and `false` when they agree.

**Constraints.** The limits are:
- **Length** `n` is between 1 and 100,000.
- **Values** are integers between -1,000,000,000 and 1,000,000,000.
- **Target** is a `long` between 1 and 10^14.
- **Sums** exceed the `int` range, so the totals must be `long`.

**Example 1.** Input `nums = [5, -4, 3, 6, -2]`, `target = 7`, output `true`, because the shrinking method returns 4 and the true answer is 2.

**Example 2.** Input `nums = [1000000000, 1000000000, 1000000000]`, `target = 3000000000`, output `false`, because both methods return 3.

**Hint.** Run both methods by hand on Example 1. Which negative value makes the left end move too far, or too little?

**Changed decision.** The task contrasts the two methods, and it makes the long totals part of the contract.

#### [Recognize] LC 862 Shortest Subarray With Sum At Least K (LeetCode 862)
<!-- id: dq-lc862 -->

**Prerequisites.** All earlier exercises in this lesson.

**Problem.** Given an integer array `nums` and an integer `k`, return the length of the shortest non-empty contiguous subarray whose sum is at least `k`. Return `-1` when no such subarray exists.

**Constraints.** The limits are:
- **Length** is between 1 and 100,000.
- **Values** are integers between -100,000 and 100,000.
- **Target** `k` is an integer between 1 and 1,000,000,000.
- **Output** is a length from 1 to `n`, or `-1`.

**Example 1.** Input `nums = [1, -2, 6, -1, 3]`, `k = 7`, output `3`.

**Example 2.** Input `nums = [3, -1, 1]`, `k = 5`, output `-1`.

**Hint.** Which end of the deque holds starts that already reached the target, and which end holds starts that a newer prefix sum beats?

**Changed decision.** The same state now solves a full problem, with a front removal that is based on success and not on age.
