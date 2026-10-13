<!-- lesson-kind: standard -->
<!-- lesson-id: target-sum -->
## Target Sum

<!-- stage: context -->
### Marking Adjustments As Credits Or Debits

A reconciliation tool receives five ledger adjustments of 1 unit each. A reviewer must mark every adjustment as a credit or a debit, and the net change must equal 3 units. A credit counts +1 and a debit counts -1. Four credits and one debit give 4 - 1 = 3. The reviewer wants to know how many different markings reach the net change 3. The tool must also answer for lists of 20 adjustments with larger amounts, and the totals and ranges there grow large.

Formally, the input is an array `nums` of nonnegative integers and an integer `target`. A **sign assignment** puts a plus sign or a minus sign in front of every element, and its value is the signed sum. Two assignments differ when they differ at some index, even if the elements at those indexes are equal. The task is to count the assignments whose value equals `target`. The method never changes the array.

This lesson asks how to count sign assignments without listing all 2^n of them.

<!-- stage: naive -->
### Tracking Every Signed Running Sum

The quick idea tracks the running sum directly. A map from running sum to the number of ways to reach it starts with sum 0 and one way. Each element replaces the map by a new one in which every sum moves up by the element and down by the element.

```java
static long countBySignedSums(int[] nums, int target) {
    Map<Integer, Long> ways = new HashMap<>();
    ways.put(0, 1L);
    for (int x : nums) {
        Map<Integer, Long> next = new HashMap<>();
        for (Map.Entry<Integer, Long> e : ways.entrySet()) {
            next.merge(e.getKey() + x, e.getValue(), Long::sum);
            next.merge(e.getKey() - x, e.getValue(), Long::sum);
        }
        ways = next;
    }
    return ways.getOrDefault(target, 0L);
}
```

This method is correct. It merges the two moves of equal sums, so it does not enumerate assignments one by one. The open question is how large the map grows and what it spends on sums that can never reach the target.

```predict
Run countBySignedSums on [1, 1, 1, 1, 1] with target 3. What does it return, and how many distinct sums does the map hold after the last element?

It returns 5, because four plus signs and one minus sign can be arranged in five places. The map holds 6 sums: -5, -3, -1, 1, 3 and 5. The map spans the values of the same parity as the total, from minus the total to plus the total.
```

<!-- stage: bottleneck -->
### The State Range Is Twice As Wide

The map must cover the signed sums from minus the total to plus the total that share the parity of the total. With total T, that is up to 2T + 1 keys, and each key is a boxed `Integer` with a boxed `Long` count. Every element rebuilds the whole map, so the work is O(n * T) hash operations and O(T) memory for boxed objects.

Most of that range is wasted. A target above T or below -T has no assignment, yet the method still builds the whole map before it answers 0. The method also hides a simpler structure. A sign assignment splits the elements into two groups by sign, and the values of the two groups are tied together by the total and the target.

A method that uses this tie needs only one number per sum between 0 and a derived goal. That is half the range or less, and it needs no boxed keys, only an array of counts. The time is O(n * goal), and the next section derives the goal.

<!-- stage: insight -->
### Turn Signs Into A Subset Question

A sign assignment sorts the elements into two groups. A small piece of algebra shows that the target fixes the sum of each group.

<!-- names: plus group, minus group, subset count -->

#### Two Groups From One Assignment

The **plus group** is the set of indexes that receive a plus sign, and the **minus group** is the set that receives a minus sign. Let P be the sum of the plus group and N the sum of the minus group. The value of the assignment is P - N, and the total of all elements is P + N. If the value equals `target`, then P - N = target and P + N = total. Adding the two equations gives 2P = total + target, so P = (total + target) / 2.

#### The Derived Goal Must Be Valid

The goal P must be a whole number, so `total + target` must be even. The goal must also lie between 0 and `total`, because P is a sum of nonnegative elements that are part of the total. That condition is the same as `|target| <= total`. When either condition fails, no assignment reaches the target, and the answer is 0 without any table.

#### Count Subsets With Sum P

An assignment is determined by its plus group, and every subset of indexes can be a plus group. So the number of assignments with value `target` equals the **subset count** for sum P, which is the number of subsets of indexes whose elements add up to P. Let `ways[s]` be the number of subsets of the processed elements with sum `s`. Only `ways[0]` is 1 at the start, for the empty subset. For each element `x`, the update `ways[s] += ways[s - x]` runs in descending order of `s`, so each element joins a subset at most once. The invariant is that after each element, `ways[s]` counts the subsets of the processed elements that sum to `s`. The answer is `ways[P]`.

<!-- stage: variables -->
### Counts For Sums Up To The Goal

The method leaves `nums` unchanged. It keeps these working values.

- **total** is a `long` that holds the sum of all elements.
- **goal** is `(total + target) / 2`, the sum that the plus group must reach.
- **ways** is a `long[]` of length `goal + 1`; entry `s` counts the subsets of the processed elements that sum to `s`.
- **x** is the element added in the current outer iteration.
- **s** is the sum that the inner loop updates, from `goal` down to `x`.

The counts are `long` values because the number of assignments can be 2^n. The goal is computed only after the validity checks, so the array length is never negative or larger than the total plus 1.

<!-- stage: trace -->
### Two Runs Over Small Lists

#### Counting Subsets That Reach The Goal

The first run uses `nums = [1, 2, 3, 4]` and `target = 2`. The total is 10 and the goal is 6. Each cell is a sum from 0 to 6, and the pointer `s` marks the entry that changes. The variable `x` is the element being added, `add` is the amount added to the entry, and `ways` is the entry after the update. The trace lists only the updates that change an entry, and the first step shows the starting state.

After the elements 1 and 2, sums 1, 2 and 3 are each reached once. The element 3 then adds to sums 6, 5, 4 and 3, so `ways[6]` is 1 and `ways[3]` becomes 2. The element 4 adds one more way to sums 6, 5 and 4. The final entry `ways[6]` is 2, from the subsets {2, 4} and {1, 2, 3}.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"x":0,"add":0,"ways":1},"note":"Only the empty subset exists at the start, so the count for sum 0 is 1."},{"at":{"s":1},"vars":{"x":1,"add":1,"ways":1},"note":"Adding the element 1, sum 1 gains 1 from sum 0, so its count becomes 1."},{"at":{"s":3},"vars":{"x":2,"add":1,"ways":1},"note":"Adding the element 2, sum 3 gains 1 from sum 1, so its count becomes 1."},{"at":{"s":2},"vars":{"x":2,"add":1,"ways":1},"note":"Adding the element 2, sum 2 gains 1 from sum 0, so its count becomes 1."},{"at":{"s":6},"vars":{"x":3,"add":1,"ways":1},"note":"Adding the element 3, sum 6 gains 1 from sum 3, so its count becomes 1."},{"at":{"s":5},"vars":{"x":3,"add":1,"ways":1},"note":"Adding the element 3, sum 5 gains 1 from sum 2, so its count becomes 1."},{"at":{"s":4},"vars":{"x":3,"add":1,"ways":1},"note":"Adding the element 3, sum 4 gains 1 from sum 1, so its count becomes 1."},{"at":{"s":3},"vars":{"x":3,"add":1,"ways":2},"note":"Adding the element 3, sum 3 gains 1 from sum 0, so its count becomes 2."},{"at":{"s":6},"vars":{"x":4,"add":1,"ways":2},"note":"Adding the element 4, sum 6 gains 1 from sum 2, so its count becomes 2."},{"at":{"s":5},"vars":{"x":4,"add":1,"ways":2},"note":"Adding the element 4, sum 5 gains 1 from sum 1, so its count becomes 2."},{"at":{"s":4},"vars":{"x":4,"add":1,"ways":2},"note":"Adding the element 4, sum 4 gains 1 from sum 0, so its count becomes 2."}]}
```

#### Zero Values Double The Count

The second run uses `nums = [0, 0, 1]` and `target = 1`. The total is 1 and the goal is 1. A zero joins any subset without changing its sum, so each zero doubles every entry. The first zero changes `ways[0]` from 1 to 2, and the second changes it to 4. The element 1 then adds `ways[0]` to `ways[1]`, which gives 4. The four assignments are the four ways to sign the two zeros, with the plus sign on the 1.

```trace
{"cells":[0,1],"pointers":["s"],"steps":[{"at":{"s":0},"vars":{"x":0,"add":0,"ways":1},"note":"Only the empty subset exists at the start, so the count for sum 0 is 1."},{"at":{"s":0},"vars":{"x":0,"add":1,"ways":2},"note":"Adding the element 0, sum 0 gains 1 from sum 0, so its count becomes 2."},{"at":{"s":0},"vars":{"x":0,"add":2,"ways":4},"note":"Adding the element 0, sum 0 gains 2 from sum 0, so its count becomes 4."},{"at":{"s":1},"vars":{"x":1,"add":4,"ways":4},"note":"Adding the element 1, sum 1 gains 4 from sum 0, so its count becomes 4."}]}
```

<!-- stage: code -->
### Check The Goal Then Count Subsets

The method returns the number of sign assignments. It rejects impossible targets first and then counts subsets in descending order.

```java
static long countSigns(int[] nums, int target) {
    long total = 0;
    for (int x : nums) total += x;
    if (Math.abs((long) target) > total || (total + target) % 2 != 0) return 0;
    int goal = (int) ((total + target) / 2);
    long[] ways = new long[goal + 1];
    ways[0] = 1;
    for (int x : nums) {
        for (int s = goal; s >= x; s--) ways[s] += ways[s - x];
    }
    return ways[goal];
}
```

The range test runs first, so `total + target` is nonnegative when the parity test reads it, and `% 2` cannot be negative. The method runs in O(n * goal) time and uses O(goal) memory. A zero element enters the inner loop for every `s` and doubles each entry.

<!-- stage: applicability -->
### Recognizing Signed Sums With A Target

#### Reading The Cue

Use this method when every element must receive one of two opposite roles, such as plus or minus, and the question asks how many assignments reach a target value or whether any does. Words such as "add or subtract each number" and "number of expressions" point here. The two roles define two groups, and the target fixes the sum of one group.

#### Checking The Invariant

The invariant ties each entry to a count: `ways[s]` equals the number of subsets of the elements seen so far with sum `s`. Test a target larger than the total, which must return 0 before any allocation. Test a target whose parity differs from the total, which must also return 0. Test zeros, whose count doubles the answer, and test a negative target, which is symmetric to the positive one.

#### Avoiding The False Friend

The map over signed sums is correct and heavy, so it works as a cross-check and not as the recommended method. A loop that runs upward lets an element join a subset repeatedly and counts a different question. Checking parity with `(total + target) % 2 == 1` accepts a wrong odd case when the sum is negative. An `int` count overflows when many zeros or equal elements make the answer large.

<!-- stage: exercises -->
### Exercises

#### [Build] Derive The Subset Equation (Author exercise)
<!-- id: cap-tgt-derive-equation -->

**Prerequisites.** The derivation of the plus-group sum from this lesson.

**Problem.** The inputs are an array `nums` of nonnegative integers and an integer `target`. If some sign assignment can reach `target`, the plus group must sum to `(total + target) / 2`. Return that sum when it is a whole number between 0 and `total`, and return -1 otherwise.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 100`, and an empty array has total 0.
- **Value** satisfies `0 <= nums[i] <= 1000`.
- **Target** satisfies `-100000 <= target <= 100000`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [1,2,3,4]`, `target = 2`, output `6`.

**Example 2.** Input `nums = [2,3]`, `target = 2`, output `-1`.

**Hint.** Which two conditions on `total + target` and on the size of `target` make the plus-group sum a valid value?

**Changed decision.** The method builds no table. It checks the range with an absolute value and the parity with `% 2`, and it returns the derived sum or -1.

#### [Vary] Count Derived Subsets (Author exercise)
<!-- id: cap-tgt-count-subsets -->

**Prerequisites.** The exercise above.

**Problem.** An array `nums` of nonnegative integers and a nonnegative integer `goal` are given. Count the subsets of indexes whose elements sum to exactly `goal`. Two subsets differ when their sets of indexes differ, even if the elements are equal.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 40`.
- **Value** satisfies `1 <= nums[i] <= 100`.
- **Goal** satisfies `0 <= goal <= 4000`, and the empty subset counts when `goal` is 0.
- **Result** is a `long`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [1,2,3,4,5]`, `goal = 5`, output `3`.

**Example 2.** Input `nums = [2,2,2]`, `goal = 4`, output `3`.

**Hint.** What does each entry of the table count, and why must the update run from the goal down?

**Changed decision.** Each entry holds a count in place of a boolean, and the update adds the count one element below. The base entry is 1, not true.

#### [Boundary] Zero Values And Parity (Author exercise)
<!-- id: cap-tgt-zeros-and-parity -->

**Prerequisites.** The two exercises above.

**Problem.** An array `nums` of nonnegative integers, which may contain zeros, and an integer `target` are given. Count the sign assignments whose signed sum equals `target`. Return 0 when the parity or the range rules out every assignment.

**Constraints.** The limits are:
- **Length** satisfies `0 <= nums.length <= 60`, and zeros may fill the whole array.
- **Value** satisfies `0 <= nums[i] <= 20`.
- **Target** satisfies `-1300 <= target <= 1300`.
- **Result** is a `long`, and an empty array with target 0 returns 1.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [0,0,1]`, `target = 1`, output `4`.

**Example 2.** Input `nums = [1,2]`, `target = 0`, output `0`.

**Hint.** What does a zero do to the number of assignments, and can the zeros be set aside before the table is built?

**Changed decision.** The method counts the zeros first, removes them, and multiplies the final count by 2 for each zero. The table then sees only positive elements.

#### [Recognize] Target Sum (LeetCode 494)
<!-- id: cap-tgt-signed-expressions -->

**Prerequisites.** All three exercises above.

**Problem.** An array `nums` of nonnegative integers and an integer `target` are given. Put a plus or minus sign in front of every element. Return the number of sign assignments whose signed sum equals `target`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 20`.
- **Value** satisfies `0 <= nums[i] <= 1000`, and the total is at most 1000.
- **Target** satisfies `-1000 <= target <= 1000`.
- **Result** is an `int`, and the answer fits in an `int`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [2,3,5,1]`, `target = 1`, output `2`.

**Example 2.** Input `nums = [4,1,3]`, `target = 9`, output `0`.

**Hint.** Which sum must the plus group reach, and how does that turn the signed-sum question into counting subsets?

**Changed decision.** The method applies the algebra from this lesson and then counts subsets. It never stores negative sums, because the plus group alone determines the assignment.
