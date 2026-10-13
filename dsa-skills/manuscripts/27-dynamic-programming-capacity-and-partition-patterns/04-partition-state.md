<!-- lesson-kind: standard -->
<!-- lesson-id: partition-state -->
## Partition State

<!-- stage: context -->
### Splitting Files Across Two Servers

A deployment script copies five data files of 3, 3, 2, 2 and 2 GB to two servers. Both servers must receive the same number of gigabytes, or a later merge step refuses to start. The script walks the files in order and sends each one to the server with the smaller load. The loads grow as 3 and 0, then 3 and 3, then 5 and 3, then 5 and 5, and the last file makes them 7 and 5. The merge fails, yet a correct split exists. Sending 3 and 3 to one server and 2, 2 and 2 to the other gives 6 and 6.

Formally, the input is an array `nums` of positive integers. A **split** assigns every index to one of two groups. The task is to decide whether a split exists in which both groups have the same sum. The method never changes the array.

This lesson asks how to answer that question without testing every assignment of files.

<!-- stage: naive -->
### Sending Each File To The Lighter Server

The quick idea keeps two running loads. Each file goes to the server whose load is currently smaller, and the method reports success when the two loads end equal.

```java
static boolean lighterFirst(int[] nums) {
    long a = 0;
    long b = 0;
    for (int x : nums) {
        if (a <= b) a += x;
        else b += x;
    }
    return a == b;
}
```

A single scan of the array gives O(n) time and O(1) memory. It balances many inputs correctly, and it never reads a file twice. The open question is whether a balanced split exists whenever this rule fails to find one.

```predict
Run lighterFirst on the file sizes [3, 3, 2, 2, 2]. What does it return, and does an equal split exist?

It returns false, because the final loads are 7 and 5. An equal split exists: 3 and 3 form one group with sum 6, and 2, 2 and 2 form the other group with sum 6. The rule fixes each file's server before it sees the files that come later.
```

<!-- stage: bottleneck -->
### Early Choices Block Later Matches

The running-load rule commits to a server for each file in turn. Whether a file belongs in the first group depends on the files after it, which the rule has not examined. Choosing by input order, by size or by a random shuffle fails on some input.

A correct but slow method tests every assignment. Each of n files has two possible groups, so there are 2^n assignments, and summing one assignment costs O(n). The work is O(2^n * n), and for n = 50 that exceeds 10^16 operations.

Many assignments end with the same sum for the first group, and only that sum matters for the rest of the decision. Two different sets of files with the same total leave identical choices for the remaining files. The number of distinct sums that can matter is at most `total / 2 + 1`. A table that records which sums are possible does O(1) work per element and sum, which is O(n * total) time. The next section defines that table.

<!-- stage: insight -->
### Track Which Sums Are Possible

An equal split asks for one group with a known sum. Once that sum is known, the task becomes a question about subsets, and a table can answer it.

<!-- names: parity, target, reachable sum -->

#### Equal Groups Need Half The Total

If both groups have the same sum, each equals `total / 2`, where `total` is the sum of all elements. An odd total has no integer half, so the answer is false at once. This quick check uses **parity**, which means whether a number is even or odd. For an even total, call `total / 2` the **target**. A split exists exactly when some subset of the elements sums to the target, because the elements outside that subset then sum to the target as well.

#### A Reachable Sum Stands For Many Subsets

A **reachable sum** `s` is a value for which some subset of the processed elements adds up to `s`. Let `reach[s]` be true for those values. Different subsets often give the same `s`, and the rest of the decision depends only on `s`, not on which subset produced it. So one boolean replaces all subsets with that sum. Before any element, only `reach[0]` is true, because the empty subset sums to 0.

#### Descending Updates Use Each Element Once

Adding an element `x` makes the sum `s` reachable when `s - x` was reachable before `x` was added. The update `reach[s] = reach[s] or reach[s - x]` must read the state from before `x`. The loop therefore visits sums from the target down to `x`, the same descending order as the one-use knapsack. The invariant is that after each element, `reach[s]` is true exactly for sums of subsets of the processed elements. The answer is `reach[target]`.

<!-- stage: variables -->
### The Sum Flags And The Target

The method leaves `nums` unchanged. It keeps these working values.

- **total** is a `long` that holds the sum of all elements, so a large input cannot overflow.
- **target** is `total / 2`, and it exists only when `total` is even.
- **reach** is a `boolean[]` of length `target + 1`; entry `s` says whether a subset sums to `s`.
- **x** is the element that the outer loop adds.
- **s** is the sum that the inner loop updates, from `target` down to `x`.

Only sums up to the target matter, because a subset above the target cannot be completed to an equal split. The array has `target + 1` entries, so its memory grows with the target and not with the number of elements.

<!-- stage: trace -->
### Two Runs Over Small Files

#### A Split That Exists

The first run uses the file sizes `[3, 3, 2, 2, 2]`. The total is 12 and the target is 6. Each cell is a sum from 0 to 6, and the pointer `s` marks a sum that becomes reachable. The variable `x` is the element being added, and `count` is the number of reachable sums after the update, and `reach` is 1 once the sum at the pointer is reachable. The trace lists only the steps that change an entry. The first step shows the starting state, and the last step checks the target.

The first 3 makes sum 3 reachable. The second 3 makes sum 6 reachable, and the target is already true after two elements. The next 2s make sums 5, 2 and 4 reachable. The last step puts the pointer on the target, where `reach[6]` is true.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"x":0,"count":1,"reach":1},"note":"Only sum 0 is reachable at the start, because the empty subset sums to 0."},{"at":{"s":3},"vars":{"x":3,"count":2,"reach":1},"note":"Adding the element 3, sum 3 becomes reachable because sum 0 was reachable before it, so the count of reachable sums is 2."},{"at":{"s":6},"vars":{"x":3,"count":3,"reach":1},"note":"Adding the element 3, sum 6 becomes reachable because sum 3 was reachable before it, so the count of reachable sums is 3."},{"at":{"s":5},"vars":{"x":2,"count":4,"reach":1},"note":"Adding the element 2, sum 5 becomes reachable because sum 3 was reachable before it, so the count of reachable sums is 4."},{"at":{"s":2},"vars":{"x":2,"count":5,"reach":1},"note":"Adding the element 2, sum 2 becomes reachable because sum 0 was reachable before it, so the count of reachable sums is 5."},{"at":{"s":4},"vars":{"x":2,"count":6,"reach":1},"note":"Adding the element 2, sum 4 becomes reachable because sum 2 was reachable before it, so the count of reachable sums is 6."},{"at":{"s":6},"vars":{"x":0,"count":6,"reach":1},"note":"The target is 6 and the final flag is true, so an equal split exists."}]}
```

#### A Split That Does Not Exist

The second run uses `[7, 3, 3, 9]`. The total is 22 and the target is 11. The elements produce only the sums 3, 6, 7, 9 and 10 between 1 and the target. No subset sums to 11, since 7 plus 3 is 10 and 9 plus 3 is 12. The trace ends with the pointer on 11, and the final `reach` value of 0 shows that no step ever flagged it. The method returns false.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9,10,11],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"x":0,"count":1,"reach":1},"note":"Only sum 0 is reachable at the start, because the empty subset sums to 0."},{"at":{"s":7},"vars":{"x":7,"count":2,"reach":1},"note":"Adding the element 7, sum 7 becomes reachable because sum 0 was reachable before it, so the count of reachable sums is 2."},{"at":{"s":10},"vars":{"x":3,"count":3,"reach":1},"note":"Adding the element 3, sum 10 becomes reachable because sum 7 was reachable before it, so the count of reachable sums is 3."},{"at":{"s":3},"vars":{"x":3,"count":4,"reach":1},"note":"Adding the element 3, sum 3 becomes reachable because sum 0 was reachable before it, so the count of reachable sums is 4."},{"at":{"s":6},"vars":{"x":3,"count":5,"reach":1},"note":"Adding the element 3, sum 6 becomes reachable because sum 3 was reachable before it, so the count of reachable sums is 5."},{"at":{"s":9},"vars":{"x":9,"count":6,"reach":1},"note":"Adding the element 9, sum 9 becomes reachable because sum 0 was reachable before it, so the count of reachable sums is 6."},{"at":{"s":11},"vars":{"x":0,"count":6,"reach":0},"note":"The target is 11 and the final flag is false, so no subset reaches the target and no equal split exists."}]}
```

<!-- stage: code -->
### Flags Up To A Limit

The first method returns the flag array for every sum up to a limit. The second uses it to answer the equal-split question.

```java
static boolean[] reachableSums(int[] nums, int limit) {
    boolean[] reach = new boolean[limit + 1];
    reach[0] = true;
    for (int x : nums) {
        for (int s = limit; s >= x; s--) {
            if (reach[s - x]) reach[s] = true;
        }
    }
    return reach;
}

static boolean equalSplit(int[] nums) {
    long total = 0;
    for (int x : nums) total += x;
    if (total % 2 != 0) return false;
    int target = (int) (total / 2);
    return reachableSums(nums, target)[target];
}
```

The array costs O(target) memory and the loops cost O(n * target) time. The cast to `int` is safe only when the target fits in an `int`, and an input with a very large target needs a different method. Elements larger than the limit never enter the inner loop.

<!-- stage: applicability -->
### Recognizing Questions About Subset Sums

#### Reading The Cue

Use this method when the input splits into groups with a required sum, or when the question asks which totals a subset can produce. Phrases such as "two groups with equal sum", "difference as small as possible" and "can some of the numbers add up to" point here. The table indexes the sum, and a boolean per sum is enough when the question asks only whether a sum can occur.

#### Checking The Invariant

The invariant says that after each element, `reach[s]` is true exactly for the sums of subsets of the processed elements. Test an odd total, which must stop before any table is built. Test an element equal to the target, which makes the answer true after one step. Test an element larger than the target, which must leave the table alone.

#### Avoiding The False Friend

The balancing rule of the naive section is one false friend. Another is sorting the elements and alternating groups, which fails on `[3, 3, 2, 2, 2]` as well. A third is a table that is large enough for the total and not the target, which wastes half the memory, and a fourth is an `int` total that overflows for big elements and produces a negative target.

<!-- stage: exercises -->
### Exercises

#### [Build] Reachable Subset Sums (Author exercise)
<!-- id: cap-part-reachable-sums -->

**Prerequisites.** The sum flags and the descending update from this lesson.

**Problem.** Positive integers arrive in an array `nums`. A subset sum is the sum of the elements at some set of distinct indexes, and the empty set gives 0. Return the number of distinct subset sums.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 50`, and an empty array returns 1.
- **Value** satisfies `1 <= nums[i] <= 100`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [1,2,2]`, output `6`.

**Example 2.** Input `nums = [5,5]`, output `3`.

**Hint.** Which array length lets the table hold every possible subset sum, and which direction keeps each element from counting twice?

**Changed decision.** The limit is the total of all elements, not half of it. The method counts the true entries of the final table in place of reading one entry.

#### [Vary] Smallest Equal Group (LeetCode 416)
<!-- id: cap-part-smallest-group -->

**Prerequisites.** The exercise above.

**Problem.** The array `nums` holds positive integers. A split puts every index into one of two groups, and it is equal when both groups have the same sum. Return the smallest possible number of elements in a group that belongs to an equal split, or -1 if no equal split exists.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 100`.
- **Value** satisfies `1 <= nums[i] <= 100`.
- **Total** is at most 10000, and an odd total returns -1.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [4,6,5,3,2]`, output `2`.

**Example 2.** Input `nums = [3,5,9,2]`, output `-1`.

**Hint.** What can the table store for each sum in place of a boolean, so that a smaller group size replaces a larger one?

**Changed decision.** Each entry holds the fewest elements that reach its sum, with a marker for sums that no subset reaches. The update takes the smaller of the stored count and the count one element below plus 1.

#### [Boundary] Odd Total And Large Target (Author exercise)
<!-- id: cap-part-odd-and-large -->

**Prerequisites.** The two exercises above.

**Problem.** The inputs are positive integers `nums` and an integer `cellBudget`. The method may allocate at most `cellBudget` table entries. Return 0 if the total is odd. Otherwise return 3 if the target `total / 2` needs more than `cellBudget` entries, which means `target + 1 > cellBudget`. Otherwise return 1 if an equal split exists and 2 if it does not.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 100`.
- **Value** satisfies `1 <= nums[i] <= 1000000000`, so the total can exceed the `int` range.
- **Budget** satisfies `1 <= cellBudget <= 1000000`.
- **Order** of checks is fixed: parity first, then the budget, then the table.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [1,2,4]`, `cellBudget = 100`, output `0`.

**Example 2.** Input `nums = [5,5,10]`, `cellBudget = 5`, output `3`.

**Hint.** Which two quantities can be computed before the table exists, and what type must the total have so that the target stays correct for large elements?

**Changed decision.** The method returns a status code and skips the table when parity or the budget already decides. The total is a `long`, so the target and the budget comparison stay correct for large elements.

#### [Recognize] Last Stone Weight II (LeetCode 1049)
<!-- id: cap-part-last-stone -->

**Prerequisites.** All three exercises above.

**Problem.** An array `stones` of positive integer weights is given. One move picks two stones with weights `x <= y` and smashes them. If `x == y` both are removed. Otherwise the stone `y` is replaced by a stone of weight `y - x`. Moves continue until at most one stone remains. Return the smallest possible weight of the remaining stone, or 0 if none remains.

**Constraints.** The limits are:
- **Length** satisfies `1 <= stones.length <= 30`.
- **Weight** satisfies `1 <= stones[i] <= 100`.
- **Result** is an `int` from 0 to the largest stone weight.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `stones = [10,4,3,1]`, output `2`.

**Example 2.** Input `stones = [6,11,4,9]`, output `0`.

**Hint.** Each stone ends up with a plus sign or a minus sign in the final value. How does that relate to two groups, and what makes the difference between their sums small?

**Changed decision.** The method does not ask for an exact half. It finds the largest reachable sum that is at most `total / 2`, and it returns `total` minus twice that sum.
