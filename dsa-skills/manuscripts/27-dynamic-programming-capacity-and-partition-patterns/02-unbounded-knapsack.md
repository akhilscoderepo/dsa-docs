<!-- lesson-kind: standard -->
<!-- lesson-id: unbounded-knapsack -->
## Unbounded Knapsack

<!-- stage: context -->
### Filling A Compute Window With Repeatable Jobs

A batch scheduler has a 6-hour compute window. It offers two job types that can each run any number of times. Job A needs 4 hours and pays 5 points. Job B needs 3 hours and pays 3 points. A planner that ranks jobs by points per hour picks job A first, since 1.25 beats 1.0. Only 2 hours remain after that, so the plan earns 5 points. Running job B twice fills the window and earns 6 points.

Formally, the input is two arrays `weight` and `value` of equal length, plus a nonnegative integer `capacity`. Item `i` uses `weight[i]` units of capacity and pays `value[i]`. An item may be chosen any number of times. The task is to return the largest total value of a selection whose total weight is at most `capacity`. The empty selection is legal and the method never changes the arrays.

This lesson asks how to find the best total value without testing every combination of repeats.

<!-- stage: naive -->
### Ranking Items By Value Per Unit

The quick idea is greedy. Rank the items by value divided by weight. Use as many copies of the top item as fit, then move to the next item and use the capacity that is left.

```java
static int greedyPack(int[] weight, int[] value, int capacity) {
    Integer[] order = new Integer[weight.length];
    for (int i = 0; i < order.length; i++) order[i] = i;
    Arrays.sort(order, (x, y) -> Long.compare((long) value[y] * weight[x], (long) value[x] * weight[y]));
    int left = capacity;
    int total = 0;
    for (int i : order) {
        total += (left / weight[i]) * value[i];
        left %= weight[i];
    }
    return total;
}
```

The comparator multiplies instead of dividing, so it ranks items without fractions. The method sorts the items and makes one pass, so it runs in O(k log k) time for k items. It is fast and it packs correctly on many inputs. The open question is whether the best ratio always belongs to the best selection.

```predict
Run greedyPack with weights [4, 3], values [5, 3] and capacity 6. What does it return, and what is the true best total?

It returns 5, because it takes one copy of the first item and cannot fit another. The true best total is 6, from two copies of the second item. A good ratio can leave unused capacity that a worse ratio would fill.
```

<!-- stage: bottleneck -->
### Leftover Capacity Hides The Real Cost

The greedy method judges an item by its ratio, but the real cost of a choice is the capacity it leaves behind. Whether a leftover of 2 units is wasted depends on the other items, so no fixed ranking works for every input.

A correct but slow method decides how many copies of each item to take. Item `i` allows up to `capacity / weight[i]` copies. With k items, the number of count vectors is the product of those limits, which is O(capacity^k) for weights near 1. For capacity 100 and five items of weight 2, that is already more than 10^8 vectors.

Most vectors repeat a subproblem. Taking one copy of item A and then two of item B leaves the same remaining capacity as taking two of B and then one of A. The best future value depends only on the remaining capacity, and there are only `capacity + 1` values for it. A table with one entry per capacity does k steps of work for each entry, which is O(capacity * k) time. The next section defines that table.

<!-- stage: insight -->
### Skip The Item Or Take It Again

Process the item kinds one at a time. After the first i kinds, ask for the best value of every capacity when only those kinds are allowed. Each new kind either helps or does not.

<!-- names: current row, skip, take -->

#### One Entry For Each Capacity

Let `dp[c]` be the largest total value of a selection with total weight at most `c`, using only the kinds processed so far. Before any kind is processed, every entry is 0, because the empty selection is legal. The final answer is `dp[capacity]`. The words "at most" matter here. The table needs no marker for an unreachable capacity, because leaving capacity unused is always allowed.

#### The Skip Case

To **skip** item `i` at capacity `c` means the best selection contains no copy of item `i`. Its value is the entry that the table already holds for `c`, which describes the earlier kinds only. This entry belongs to the previous row, meaning the table state before item `i` started.

#### The Take Case

To **take** item `i` at capacity `c` means the selection contains at least one copy. Remove one copy. What remains has weight at most `c - weight[i]` and may still contain copies of item `i`. So the remaining value is the entry for capacity `c - weight[i]` in the **current row**, meaning the table after item `i` has already updated that smaller capacity. The take value is that entry plus `value[i]`.

#### Increasing Capacity Reads The Current Row

The loop visits capacities from `weight[i]` up to `capacity`. When it reaches `c`, the entry at `c - weight[i]` has already been rewritten for item `i`, so it may include earlier copies. This is why repeats are allowed. The new entry is the larger of skip and take. The invariant is that after item `i` finishes, `dp[c]` is the best value for every capacity when kinds 0 through `i` are allowed.

<!-- stage: variables -->
### The Capacity Table And Two Candidates

The inputs `weight`, `value` and `capacity` stay unchanged, and the method keeps five working values.

- **dp** is an `int[]` of length `capacity + 1`; entry `c` is the best value with weight at most `c`.
- **i** is the item kind that the outer loop processes.
- **c** is the capacity that the inner loop updates, from `weight[i]` to `capacity`.
- **skip** is `dp[c]` before the update, which describes only earlier kinds.
- **take** is `dp[c - weight[i]] + value[i]`, which reads the current row.

The entries below `weight[i]` stay as they are, because item `i` does not fit there. Each value is a total that must fit in an `int`. When values reach 10^9, the totals need a `long` array.

<!-- stage: trace -->
### Two Runs Over Small Capacities

#### Taking The Smaller Item Twice

The first run uses the job example. Item 0 has weight 4 and value 5, and item 1 has weight 3 and value 3. Each cell is a capacity from 0 to 6, and the pointer `c` marks the capacity that the loop updates. The variable `item` names the kind in progress, `skip` and `take` are the two candidates, and `dp` is the entry after the update. The first step, with the pointer at -1, shows the empty table.

Item 0 fills capacities 4, 5 and 6 with the value 5, because only one copy fits. Item 1 then starts. At capacity 3 it takes 3. At capacity 6 it reads the current-row entry for capacity 3, which already holds 3, so taking gives 6 and beats the skip value 5.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["c"],"steps":[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."},{"at":{"c":4},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"Item 0, capacity 4. Skipping holds 0 and taking reads capacity 0 for 5, so taking wins at 5."},{"at":{"c":5},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"Item 0, capacity 5. Skipping holds 0 and taking reads capacity 1 for 5, so taking wins at 5."},{"at":{"c":6},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"Item 0, capacity 6. Skipping holds 0 and taking reads capacity 2 for 5, so taking wins at 5."},{"at":{"c":3},"vars":{"item":1,"skip":0,"take":3,"dp":3},"note":"Item 1, capacity 3. Skipping holds 0 and taking reads capacity 0 for 3, so taking wins at 3."},{"at":{"c":4},"vars":{"item":1,"skip":5,"take":3,"dp":5},"note":"Item 1, capacity 4. Skipping holds 5 and taking reads capacity 1 for 3, so skipping keeps the entry at 5."},{"at":{"c":5},"vars":{"item":1,"skip":5,"take":3,"dp":5},"note":"Item 1, capacity 5. Skipping holds 5 and taking reads capacity 2 for 3, so skipping keeps the entry at 5."},{"at":{"c":6},"vars":{"item":1,"skip":5,"take":6,"dp":6},"note":"Item 1, capacity 6. Skipping holds 5 and taking reads capacity 3 for 6, so taking wins at 6."}]}
```

#### One Item Used Several Times

The second run uses item 0 with weight 3 and value 4, and item 1 with weight 5 and value 7, for capacity 9. Item 0 reads its own updates. At capacity 6 it reads capacity 3 and gets 8, and at capacity 9 it reads capacity 6 and gets 12. Item 1 then helps only where it beats the stored entries. At capacity 8 it reads capacity 3 and gets 11, which beats 8. At capacity 9 it reads capacity 4 and gets 11, which loses to the stored 12.

```trace
{"cells":[0,1,2,3,4,5,6,7,8,9],"pointers":["c"],"steps":[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."},{"at":{"c":3},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"Item 0, capacity 3. Skipping holds 0 and taking reads capacity 0 for 4, so taking wins at 4."},{"at":{"c":4},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"Item 0, capacity 4. Skipping holds 0 and taking reads capacity 1 for 4, so taking wins at 4."},{"at":{"c":5},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"Item 0, capacity 5. Skipping holds 0 and taking reads capacity 2 for 4, so taking wins at 4."},{"at":{"c":6},"vars":{"item":0,"skip":0,"take":8,"dp":8},"note":"Item 0, capacity 6. Skipping holds 0 and taking reads capacity 3 for 8, so taking wins at 8."},{"at":{"c":7},"vars":{"item":0,"skip":0,"take":8,"dp":8},"note":"Item 0, capacity 7. Skipping holds 0 and taking reads capacity 4 for 8, so taking wins at 8."},{"at":{"c":8},"vars":{"item":0,"skip":0,"take":8,"dp":8},"note":"Item 0, capacity 8. Skipping holds 0 and taking reads capacity 5 for 8, so taking wins at 8."},{"at":{"c":9},"vars":{"item":0,"skip":0,"take":12,"dp":12},"note":"Item 0, capacity 9. Skipping holds 0 and taking reads capacity 6 for 12, so taking wins at 12."},{"at":{"c":5},"vars":{"item":1,"skip":4,"take":7,"dp":7},"note":"Item 1, capacity 5. Skipping holds 4 and taking reads capacity 0 for 7, so taking wins at 7."},{"at":{"c":6},"vars":{"item":1,"skip":8,"take":7,"dp":8},"note":"Item 1, capacity 6. Skipping holds 8 and taking reads capacity 1 for 7, so skipping keeps the entry at 8."},{"at":{"c":7},"vars":{"item":1,"skip":8,"take":7,"dp":8},"note":"Item 1, capacity 7. Skipping holds 8 and taking reads capacity 2 for 7, so skipping keeps the entry at 8."},{"at":{"c":8},"vars":{"item":1,"skip":8,"take":11,"dp":11},"note":"Item 1, capacity 8. Skipping holds 8 and taking reads capacity 3 for 11, so taking wins at 11."},{"at":{"c":9},"vars":{"item":1,"skip":12,"take":11,"dp":12},"note":"Item 1, capacity 9. Skipping holds 12 and taking reads capacity 4 for 11, so skipping keeps the entry at 12."}]}
```

<!-- stage: code -->
### An Item Loop Around A Capacity Loop

The method returns the best total value. It processes one item kind at a time and updates the table in increasing order of capacity.

```java
static int unboundedPack(int[] weight, int[] value, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weight.length; i++) {
        for (int c = weight[i]; c <= capacity; c++) {
            int take = dp[c - weight[i]] + value[i];
            if (take > dp[c]) dp[c] = take;
        }
    }
    return dp[capacity];
}
```

The inner loop starts at `weight[i]`, so the index `c - weight[i]` is never negative. The array starts at 0 because Java zero-fills new arrays, which matches the empty selection. The cost is O(capacity * k) time and O(capacity) memory for k kinds. An item heavier than the capacity never enters the inner loop.

<!-- stage: applicability -->
### Recognizing Repeatable Items With A Weight Limit

#### Reading The Cue

Use this method when items have a weight and a value, the total weight has a limit, and each item can be chosen again and again. The goal is the largest total value, and leftover capacity is allowed. The table indexes the capacity, and each entry reads a smaller capacity in the same row.

#### Checking The Invariant

An **invariant** is a condition that holds at the start of every loop iteration. Here it says that after item `i` finishes, `dp[c]` is the best value using kinds 0 through `i` for each `c`. Test capacity 0, which must return 0. Test an item that does not fit at all, which must leave the table alone. Test two items with equal ratios, where either may be chosen.

#### Avoiding The False Friend

A **false friend** is a method that looks right on small samples but fails on other inputs. The ratio greedy of the naive section is one. A second is the inner loop run from high capacity down to low, which lets each kind enter at most once and answers the one-use question of the next lesson. A third is a table that demands an exact weight, which returns the wrong value when the best selection leaves capacity unused.

<!-- stage: exercises -->
### Exercises

#### [Build] One Reusable Item (Author exercise)
<!-- id: cap-ukn-one-item -->

**Prerequisites.** The capacity table and the current-row read from this lesson.

**Problem.** One item has a positive integer `weight` and a nonnegative integer `value`, and it may be chosen any number of times. Return the largest total value over all choices of copies of that item whose combined weight stays within `capacity`.

**Constraints.** The limits are:
- **Weight** satisfies `1 <= weight <= 1000`.
- **Value** satisfies `0 <= value <= 1000`.
- **Capacity** satisfies `0 <= capacity <= 10000`, and capacity 0 returns 0.
- **Result** is an `int`.

**Example 1.** Input `weight = 4`, `value = 7`, `capacity = 13`, output `21`.

**Example 2.** Input `weight = 5`, `value = 9`, `capacity = 4`, output `0`.

**Hint.** With one item, which earlier capacity does each entry read, and what does an entry hold when the item does not fit?

**Changed decision.** The loop has one item, so only the capacities that are multiples of the weight gain value. All other entries copy the entry one block below through the current-row read.

#### [Vary] Maximum Value With Reuse (Author exercise)
<!-- id: cap-ukn-max-value -->

**Prerequisites.** The exercise above.

**Problem.** Arrays `weight` and `value` describe `k` item kinds, and each kind may be chosen any number of times. Return the largest total value of a selection whose total weight is at most `capacity`.

**Constraints.** The limits are:
- **Length** satisfies `1 <= weight.length <= 30`, and both arrays have equal length.
- **Weight** satisfies `1 <= weight[i] <= 1000`.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Capacity** satisfies `0 <= capacity <= 10000`.
- **Mutation** is not allowed, because both arrays stay unchanged.

**Example 1.** Input `weight = [4,3]`, `value = [5,3]`, `capacity = 6`, output `6`.

**Example 2.** Input `weight = [5,7]`, `value = [6,9]`, `capacity = 17`, output `21`.

**Hint.** For one item and one capacity, which entry means skipping the item, and which entry means taking one more copy?

**Changed decision.** Each entry compares the skip value from the previous row with the take value from the current row at the smaller capacity. One item no longer decides the whole table.

#### [Boundary] Zero Capacity (Author exercise)
<!-- id: cap-ukn-zero-capacity -->

**Prerequisites.** The two exercises above.

**Problem.** Arrays `weight` and `value` describe item kinds that may be chosen any number of times, and weights may be 0. If some item has weight 0 and positive value, the total value has no upper bound and the method returns -1. Otherwise it returns the largest total value of a selection with total weight at most `capacity`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= weight.length <= 30`, and both arrays have equal length.
- **Weight** satisfies `0 <= weight[i] <= 1000`.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Capacity** satisfies `0 <= capacity <= 10000`, and an empty item list returns 0.
- **Mutation** is not allowed, because both arrays stay unchanged.

**Example 1.** Input `weight = [0,5]`, `value = [0,6]`, `capacity = 0`, output `0`.

**Example 2.** Input `weight = [0,5]`, `value = [2,6]`, `capacity = 7`, output `-1`.

**Hint.** What happens to the inner loop when the weight is 0, and why would a repeat then add value forever?

**Changed decision.** The method checks for a zero-weight item with positive value before the loops. A zero-weight item with value 0 is skipped, because it never changes the table.

#### [Recognize] Perfect Squares (LeetCode 279)
<!-- id: cap-ukn-perfect-squares -->

**Prerequisites.** All three exercises above and the previous lesson.

**Problem.** A positive integer `n` is given. A perfect square is `1`, `4`, `9`, `16` and so on. Return the smallest number of perfect squares, with repeats allowed, whose sum is exactly `n`.

**Constraints.** The limits are:
- **Value** satisfies `1 <= n <= 10000`.
- **Result** is an `int` at least 1.
- **Terms** may repeat, and every term is a perfect square.

**Example 1.** Input `n = 12`, output `3`.

**Example 2.** Input `n = 28`, output `4`.

**Hint.** Which numbers play the role of the item weights, and what does each use cost?

**Changed decision.** The items are the squares up to `n`, every use costs 1, and the sum must be exact. The method minimizes the count and uses the marker `n + 1` for unreachable entries.
