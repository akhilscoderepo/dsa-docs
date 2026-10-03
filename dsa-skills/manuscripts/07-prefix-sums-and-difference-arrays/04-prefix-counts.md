<!-- lesson-kind: standard -->
<!-- lesson-id: prefix-counts -->
## Prefix Counts

<!-- stage: context -->
### A Piggy Bank And A Price Tag

A child keeps a piggy bank and writes down the change in it at the end of each day. Some days coins go in, some days coins come out, and some days nothing changes, so the notebook is a long list of positive, negative and zero numbers. The child has seen a toy that costs exactly 7 coins, and asks a curious question: for how many stretches of consecutive days did the bank's balance change by exactly 7 coins from the start of the stretch to its end?

The stretches overlap and nest inside one another, and a stretch may be a single day. The child wants a count of all of them, not just one example. A year of notes has hundreds of days, and the number of stretches is far larger than the number of days.

<!-- stage: naive -->
### Try Every Stretch

The direct approach is to take every first day, extend the stretch day by day, and count each time the total equals the price.

```java
static int countStretches(int[] change, int price) {
    int count = 0;
    for (int first = 0; first < change.length; first++) {
        int total = 0;
        for (int last = first; last < change.length; last++) {
            total += change[last];
            if (total == price) count++;
        }
    }
    return count;
}
```

It counts each stretch exactly once, so it handles zeros, negative days and overlapping stretches correctly.

<!-- stage: bottleneck -->
### Every Pair Of Days Is Visited

There are about n squared over two stretches in a notebook of n days, and the loop visits each one, so the cost is O(n^2). With a hundred thousand days that is five billion visits. The inner loop also keeps adding from scratch what the previous first day had already added, so most of the effort repeats.

The total of a stretch is the difference of two stored totals from the previous lessons, the balance after its last day and the balance before its first day. The question "does the stretch total exactly 7" is the same as "does the balance after the last day minus 7 equal the balance before some earlier day". Instead of trying every earlier day for a given last day, one lookup can say how many earlier days had that balance. That reduces the work for each last day to O(1) expected, and O(n) in total.

<!-- stage: insight -->
### Count The Earlier Balances You Need

For each last day, the balance so far is the **prefix** `p`. A stretch ending on that day has total `target` exactly when it begins after a day whose balance was `p - target`, which is the **complement**: the value that an earlier balance would need to have. The answer for this last day is the number of earlier balances equal to the complement, and it is read from a **prefix frequency** map, a table that records how many times each balance has occurred so far.

The order of operations is the heart of the method. For each day, update the balance, look up the complement in the table, add the count found to the answer, and only then record the new balance in the table. Looking up before recording means that a day is never paired with itself, so a stretch always has at least one day in it. The invariant is that, when day `i` is processed, the table holds the balances of all the days before it, together with the empty start.

<!-- names: prefix frequency, complement, seeded zero -->

The empty start is the **seeded zero**: before any day is processed the table already holds one occurrence of balance zero, standing for the moment before the first day. Without that seed, a stretch that begins on the very first day has no earlier balance to pair with, and the method undercounts. A table of how many times each balance occurred, not a plain set of balances that occurred, is required: if the same balance occurred three times, three different stretches end on the current day, and a set can only say "at least once".

<!-- stage: variables -->
### Balance, Table And Count

`balance` is the running total through the current day, kept as an `int` here because the limits keep it small, and as a `long` whenever they do not. `seen` is a map from a balance to the number of times it has been the balance after some day, with the seeded entry for zero. `need` is `balance - target`, the complement to look up. `count` is the answer so far, and it grows by `seen.getOrDefault(need, 0)` at each day. The map is read before the current balance is written into it, and that order is what keeps empty stretches out of the count.

<!-- stage: trace -->
### Counting While The Balance Moves

The first trace follows the notebook 3, 4, 7, 2, -3, 1, 4, 2 with a price of 7. The row of cells is the notebook, and the variables show the balance, the complement being looked up, and the answer so far. The step to study is the third: the balance is 14, the complement is 7, and the table says the balance 7 occurred once before, so the stretch consisting of the single day with change 7 is counted.

```trace
{"cells":["3","4","7","2","-3","1","4","2"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"balance":3,"need":-4,"found":0,"answer":0},"note":"The balance is 3, so the complement is -4. The table holds it 0 times, so the answer is 0. Then record the balance 3."},{"at":{"i":1},"vars":{"balance":7,"need":0,"found":1,"answer":1},"note":"The balance is 7, so the complement is 0. The table holds it 1 times, so the answer is 1. Then record the balance 7."},{"at":{"i":2},"vars":{"balance":14,"need":7,"found":1,"answer":2},"note":"The balance is 14, so the complement is 7. The table holds it 1 times, so the answer is 2. Then record the balance 14."},{"at":{"i":3},"vars":{"balance":16,"need":9,"found":0,"answer":2},"note":"The balance is 16, so the complement is 9. The table holds it 0 times, so the answer is 2. Then record the balance 16."},{"at":{"i":4},"vars":{"balance":13,"need":6,"found":0,"answer":2},"note":"The balance is 13, so the complement is 6. The table holds it 0 times, so the answer is 2. Then record the balance 13."},{"at":{"i":5},"vars":{"balance":14,"need":7,"found":1,"answer":3},"note":"The balance is 14, so the complement is 7. The table holds it 1 times, so the answer is 3. Then record the balance 14."},{"at":{"i":6},"vars":{"balance":18,"need":11,"found":0,"answer":3},"note":"The balance is 18, so the complement is 11. The table holds it 0 times, so the answer is 3. Then record the balance 18."},{"at":{"i":7},"vars":{"balance":20,"need":13,"found":1,"answer":4},"note":"The balance is 20, so the complement is 13. The table holds it 1 times, so the answer is 4. Then record the balance 20."}]}
```

The second trace uses the notebook 0, 0, 0 with a price of 0. Every day changes nothing, so every balance is zero, and the number of stretches is the number of pairs of equal balances. The step to study is the third: three earlier balances equal zero, the seeded one and the two recorded, so three stretches end on this day, and the total is 6.

```trace
{"cells":["0","0","0"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"balance":0,"need":0,"found":1,"answer":1},"note":"The balance is 0, so the complement is 0. The table holds it 1 times, so the answer is 1. Then record the balance 0."},{"at":{"i":1},"vars":{"balance":0,"need":0,"found":2,"answer":3},"note":"The balance is 0, so the complement is 0. The table holds it 2 times, so the answer is 3. Then record the balance 0."},{"at":{"i":2},"vars":{"balance":0,"need":0,"found":3,"answer":6},"note":"The balance is 0, so the complement is 0. The table holds it 3 times, so the answer is 6. Then record the balance 0."}]}
```

<!-- stage: code -->
### Look Up Then Record

```java
static int subarraySum(int[] nums, int k) {
    Map<Integer, Integer> seen = new HashMap<>();
    seen.put(0, 1);
    int balance = 0, count = 0;
    for (int x : nums) {
        balance += x;
        count += seen.getOrDefault(balance - k, 0);
        seen.merge(balance, 1, Integer::sum);
    }
    return count;
}

static int binarySubarraysWithSum(int[] nums, int goal) {
    int[] seen = new int[nums.length + 1];
    seen[0] = 1;
    int balance = 0, count = 0;
    for (int x : nums) {
        balance += x;
        if (balance >= goal) count += seen[balance - goal];
        seen[balance]++;
    }
    return count;
}
```

Each function makes one pass over the n values, with O(1) expected work per value, and uses space proportional to the number of distinct balances. The binary version replaces the map with an array, because a balance of zeros and ones cannot exceed the length, and it guards the subtraction so a negative index is never read.

<!-- stage: applicability -->
### When A Stretch Hits A Target

Use prefix counts when the question counts stretches whose total equals a target, and the totals can be written as a difference of two prefixes. The invariant is that the table holds the prefixes recorded before the current position, starting with the seeded zero, and each position first reads the table and then writes to it.

False friends are common here. A sliding window looks like the right tool, and it works when all values are non-negative, but it fails once negative values appear, since extending the window can lower the total. A set of balances answers whether some stretch exists, not how many. Writing before reading counts empty stretches whenever the target is zero. Forgetting the seeded zero loses every stretch that starts at the first position.

In Java, read the map with `getOrDefault` so that a missing balance counts as zero, and update with `merge`. Decide the type of the balance from the limits: an `int` balance and an `int` key are safe here, and a wider contract needs `long` for both, and then the lookup key must have the same boxed type as the stored keys, or the lookup silently finds nothing.

<!-- stage: exercises -->
### Exercises

#### [Build] Subarray Sum Equals K (LeetCode 560)
<!-- id: ps-subarray-sum-k -->

**Prerequisites.** The range queries lesson, and maps with counts from Chapter 04.

**Problem.** Given an integer array and an integer `k`, return the number of contiguous non-empty stretches whose sum is exactly `k`. Keep a table of how many times each running total has occurred, looking up the complement before recording the current total.

**Constraints.** 1 <= nums.length <= 20000, -1000 <= nums[i] <= 1000, and -10000000 <= k <= 10000000.

**Example 1.** Input `nums = [3, 4, 7, 2, -3, 1, 4, 2], k = 7`, output 4.

**Example 2.** Input `nums = [1, -1, 0], k = 0`, output 3.

**Hint.** Which earlier running total makes a stretch sum to `k`? Which entry must be in the table before any day is processed?

**Changed decision.** First rung: a count of earlier prefix totals replaces the second loop over the first day.

#### [Vary] Binary Subarrays With Sum (LeetCode 930)
<!-- id: ps-binary-subarrays-sum -->

**Prerequisites.** The Subarray Sum Equals K exercise above.

**Problem.** Given an array of zeros and ones and a non-negative goal, return the number of non-empty contiguous stretches whose sum equals the goal. The totals cannot exceed the length, so an array can replace the map, and a lookup index below zero must be avoided.

**Constraints.** 1 <= nums.length <= 30000, `nums[i]` is 0 or 1, and 0 <= goal <= nums.length.

**Example 1.** Input `nums = [1, 0, 1, 0, 1], goal = 2`, output 4.

**Example 2.** Input `nums = [0, 0, 0, 0, 0], goal = 0`, output 15.

**Hint.** What is the largest possible running total? When is the complement negative, and what does that mean?

**Changed decision.** The values are only zeros and ones, so the table can be an array indexed by the balance, with a guard before the complement lookup.

#### [Boundary] Zero Target (Author exercise)
<!-- id: ps-zero-target -->

**Prerequisites.** The two exercises above.

**Problem.** Count the non-empty stretches whose total is zero. Repeated equal running totals mean that many pairs of days enclose a zero total, so a set of seen totals would undercount. Implement the count, then implement the set version and show that it differs.

**Constraints.** 1 <= nums.length <= 20000 and -1000 <= nums[i] <= 1000.

**Example 1.** Input `nums = [0, 0, 0]`, output 6.

**Example 2.** Input `nums = [2, -2, 2, -2]`, output 4.

**Hint.** How many stretches end on a day whose balance has occurred three times before? What does a set remember about repeats?

**Changed decision.** The target is zero, so the complement equals the balance itself and the lookup must come before the record, with every repeat counted.

#### [Recognize] Count Number of Nice Subarrays (LeetCode 1248)
<!-- id: ps-nice-subarrays -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array and `k`, count the contiguous stretches that contain exactly `k` odd numbers. Replace each value by one if it is odd and zero if it is even, and the question becomes counting stretches of a binary array with sum `k`.

**Constraints.** 1 <= nums.length <= 50000, 1 <= nums[i] <= 100000, and 1 <= k <= nums.length.

**Example 1.** Input `nums = [1, 1, 2, 1, 1], k = 3`, output 2.

**Example 2.** Input `nums = [2, 4, 6], k = 1`, output 0.

**Hint.** What does the parity of each value become after the replacement? Which earlier exercise now applies?

**Changed decision.** The array is first transformed into a binary one, so the same count state is applied to a derived sequence.
