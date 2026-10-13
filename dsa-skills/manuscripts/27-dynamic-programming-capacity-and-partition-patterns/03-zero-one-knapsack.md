<!-- lesson-kind: standard -->
<!-- lesson-id: zero-one-knapsack -->
## Zero-One Knapsack

<!-- stage: context -->
### Choosing Files For A Small Backup Disk

A backup tool has a 6 MB disk and three files to copy. File A is 4 MB with importance 5. File B is 3 MB with importance 3. File C is 3 MB with importance 3. Each file exists once, so the tool can copy it at most once. Copying A leaves only 2 MB, which fits nothing else, so the importance total is 5. Copying B and C fills the disk and totals 6.

A developer reuses the repeatable-item table from the previous lesson for this job. The code is short and runs fast, but it reports a total of 8 for a single 3 MB file of importance 4 on a 6 MB disk. That answer pretends the file can be copied twice.

Formally, the input is arrays `weight` and `value` of equal length and a nonnegative integer `capacity`. Item `i` weighs `weight[i]` and is worth `value[i]`. A selection is a set of distinct indexes, so each item appears at most once. The task is to return the largest total value of a selection with total weight at most `capacity`. The method never changes the arrays.

This lesson asks how a table can count each item once.

<!-- stage: naive -->
### Reusing The Repeatable-Item Table

The quick idea is to run the loop from the previous lesson unchanged. It processes the items one at a time and updates capacities from small to large.

```java
static int reuseTable(int[] weight, int[] value, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weight.length; i++) {
        for (int c = weight[i]; c <= capacity; c++) {
            dp[c] = Math.max(dp[c], dp[c - weight[i]] + value[i]);
        }
    }
    return dp[capacity];
}
```

The method runs in O(capacity * k) time for k items and uses O(capacity) memory. Its structure is the right one for a capacity table. The open question is whether the inner loop treats an item that it has already placed as available again.

```predict
Run reuseTable with weights [3], values [4] and capacity 6. What does it return, and what is the true best total?

It returns 8. When the loop reaches capacity 6, it reads the entry for capacity 3, which already holds the item, and adds the item again. The true best total is 4, because the single item can be used once.
```

<!-- stage: bottleneck -->
### The Table Remembers Values Not Items

An entry of the table stores a value, and it forgets which items produced that value. When the loop reads `dp[c - weight[i]]` after item `i` already updated that entry, it cannot tell that the stored value contains item `i`. The update then adds the same item twice.

A correct but slow method lists every subset of items and sums its weight. A set of k items has 2^k subsets, and summing one subset costs O(k), so the work is O(2^k * k). For k = 40 that is more than 10^13 operations.

The table needs a way to keep the reads for item `i` separate from the writes for item `i`. If the reads come only from the table that describes items before `i`, no entry can contain item `i` when it is read. There are `k + 1` such tables of `capacity + 1` entries each, so O(k * capacity) memory is enough, and each entry needs two reads. The next section builds that layout and then shrinks it to one array.

<!-- stage: insight -->
### Read From The Rows Before The Item

Process the items in input order and keep the answers for every capacity after each item. The answers after item `i` must be computed only from the answers before item `i`.

<!-- names: previous row, descending order, item prefix -->

#### One Row For Each Item Prefix

An **item prefix** of length `i` is the first `i` items. Let `dp[i][c]` be the largest total value of a selection that uses only items from the prefix of length `i` and has weight at most `c`. Row 0 is all zeros, because the empty prefix allows only the empty selection. The final answer is `dp[k][capacity]`.

#### Both Cases Read The Previous Row

Item `i - 1` is the last item of the prefix of length `i`. A best selection either leaves it out or contains it once. If it leaves the item out, the value is `dp[i - 1][c]`, which is the entry in the **previous row** at the same capacity. If it contains the item, the other items come from the prefix of length `i - 1` with weight at most `c - weight[i - 1]`, so the value is `dp[i - 1][c - weight[i - 1]] + value[i - 1]`. Both reads come from the previous row, so no entry can contain the item twice. The entry is the larger of the two cases.

#### One Array In Descending Order

Row `i` needs only row `i - 1`, so one array can hold the current row while it overwrites the previous one. The overwrite is safe only if an entry is still unchanged when a later entry reads it. The take case reads a capacity smaller than `c`. Visiting the capacities in **descending order**, from `capacity` down to `weight[i]`, means every smaller capacity has not yet been rewritten when entry `c` reads it. That smaller entry therefore still holds the previous row. The invariant is that at the start of each step, entries at or below the current `c` describe the previous row and entries above it describe the new row.

<!-- stage: variables -->
### The Array And The Downward Index

The method leaves its three inputs alone and keeps these working values.

- **dp** is an `int[]` of length `capacity + 1`; during item `i`, entries at or below the current index hold the previous row.
- **i** is the item that the outer loop processes.
- **c** is the capacity that the inner loop rewrites, from `capacity` down to `weight[i]`.
- **skip** is `dp[c]` before the rewrite, which is the previous-row value at capacity `c`.
- **take** is `dp[c - weight[i]] + value[i]`, which reads the previous row at the smaller capacity.

Entries below `weight[i]` are not touched, because item `i` does not fit there. The index `c - weight[i]` is never negative inside the loop, since `c` starts no lower than `weight[i]`.

<!-- stage: trace -->
### Two Runs Over A Small Disk

#### Each File Counted Once

The first run uses the three files from the opening, with weights 4, 3 and 3, values 5, 3 and 3, and capacity 6. Each cell is a capacity from 0 to 6. The pointer `c` marks the entry that the loop rewrites, moving downward inside each item. The variable `item` names the file in progress, `skip` and `take` are the two candidates, and `dp` is the entry after the rewrite.

File A rewrites capacities 6, 5 and 4 with the value 5. File B starts at capacity 6 and reads capacity 3, which is still 0, so the take value is 3 and the skip value 5 wins. File C then reads capacity 3, which now holds 3 from file B, so taking gives 6 at capacity 6. The two 3 MB files fill the disk once each.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["c"],"steps":[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."},{"at":{"c":6},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"File 0, capacity 6. Skipping holds 0. Taking reads capacity 2 for 5, from an entry that still holds the earlier files, so taking wins at 5."},{"at":{"c":5},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"File 0, capacity 5. Skipping holds 0. Taking reads capacity 1 for 5, from an entry that still holds the earlier files, so taking wins at 5."},{"at":{"c":4},"vars":{"item":0,"skip":0,"take":5,"dp":5},"note":"File 0, capacity 4. Skipping holds 0. Taking reads capacity 0 for 5, from an entry that still holds the earlier files, so taking wins at 5."},{"at":{"c":6},"vars":{"item":1,"skip":5,"take":3,"dp":5},"note":"File 1, capacity 6. Skipping holds 5. Taking reads capacity 3 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 5."},{"at":{"c":5},"vars":{"item":1,"skip":5,"take":3,"dp":5},"note":"File 1, capacity 5. Skipping holds 5. Taking reads capacity 2 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 5."},{"at":{"c":4},"vars":{"item":1,"skip":5,"take":3,"dp":5},"note":"File 1, capacity 4. Skipping holds 5. Taking reads capacity 1 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 5."},{"at":{"c":3},"vars":{"item":1,"skip":0,"take":3,"dp":3},"note":"File 1, capacity 3. Skipping holds 0. Taking reads capacity 0 for 3, from an entry that still holds the earlier files, so taking wins at 3."},{"at":{"c":6},"vars":{"item":2,"skip":5,"take":6,"dp":6},"note":"File 2, capacity 6. Skipping holds 5. Taking reads capacity 3 for 6, from an entry that still holds the earlier files, so taking wins at 6."},{"at":{"c":5},"vars":{"item":2,"skip":5,"take":3,"dp":5},"note":"File 2, capacity 5. Skipping holds 5. Taking reads capacity 2 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 5."},{"at":{"c":4},"vars":{"item":2,"skip":5,"take":3,"dp":5},"note":"File 2, capacity 4. Skipping holds 5. Taking reads capacity 1 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 5."},{"at":{"c":3},"vars":{"item":2,"skip":3,"take":3,"dp":3},"note":"File 2, capacity 3. Skipping holds 3. Taking reads capacity 0 for 3, from an entry that still holds the earlier files, so skipping keeps the entry at 3."}]}
```

#### What The Upward Loop Does Instead

The second run applies the upward loop of the naive section to one file with weight 3 and value 4 and capacity 6. The correct answer is 4. At capacity 3 the take value is 4. At capacity 6 the loop reads capacity 3, which was rewritten a moment earlier and already holds the file, so the take value is 8. The trace shows the entry reaching 8, and that value counts the same file twice. The descending order of the correct loop reads capacity 3 before rewriting it, so it returns 4.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["c"],"steps":[{"at":{"c":-1},"vars":{"item":-1,"skip":0,"take":0,"dp":0},"note":"The table starts at 0 for every capacity, because the empty selection is legal."},{"at":{"c":3},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"File 0, capacity 3. Skipping holds 0. Taking reads capacity 0 for 4, from an entry that still holds the earlier files, so taking wins at 4."},{"at":{"c":4},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"File 0, capacity 4. Skipping holds 0. Taking reads capacity 1 for 4, from an entry that still holds the earlier files, so taking wins at 4."},{"at":{"c":5},"vars":{"item":0,"skip":0,"take":4,"dp":4},"note":"File 0, capacity 5. Skipping holds 0. Taking reads capacity 2 for 4, from an entry that still holds the earlier files, so taking wins at 4."},{"at":{"c":6},"vars":{"item":0,"skip":0,"take":8,"dp":8},"note":"File 0, capacity 6. Skipping holds 0. Taking reads capacity 3 for 8, from the entry that file 0 already rewrote, so taking wins at 8."}]}
```

<!-- stage: code -->
### The Compressed Array Loop

The method returns the best total value. It processes one item at a time and rewrites the array from the largest capacity down.

```java
static int oneUsePack(int[] weight, int[] value, int capacity) {
    int[] dp = new int[capacity + 1];
    for (int i = 0; i < weight.length; i++) {
        for (int c = capacity; c >= weight[i]; c--) {
            int take = dp[c - weight[i]] + value[i];
            if (take > dp[c]) dp[c] = take;
        }
    }
    return dp[capacity];
}
```

Only the direction of the inner loop differs from the repeatable version. The cost is O(capacity * k) time and O(capacity) memory for k items. An item heavier than `capacity` never enters the inner loop, because `c >= weight[i]` fails at once. The first exercise below builds the two-dimensional table from the insight.

<!-- stage: applicability -->
### Recognizing Items That Can Be Chosen Once

#### Reading The Cue

Use this method when each item is either chosen or left out, the total weight has a limit, and the goal is a total value. Words such as "each element at most once" and "a subset of the items" point here. The table indexes capacity, and every entry for an item depends on entries that describe the items before it.

#### Checking The Invariant

The invariant says that entries at or below the current index still hold the previous row, so a take never reads the item that it is adding. Try a single item with weight at most half the capacity, because it exposes a loop that runs upward. Test an item exactly as heavy as the capacity, which must be taken once. Test an item heavier than the capacity, which must change nothing.

#### Avoiding The False Friend

The first false friend is the upward loop, which passes any test where no item fits twice. The second is the ratio greedy, which fails on the disk example. The third is a two-array version that forgets to copy the finished row before the next item starts, which silently drops the earlier items.

<!-- stage: exercises -->
### Exercises

#### [Build] One-Use Items (Author exercise)
<!-- id: cap-zok-one-use-items -->

**Prerequisites.** The item-prefix table and the previous-row reads from this lesson.

**Problem.** Each item in arrays `weight` and `value` can be chosen at most once. Fill a table with one row per item prefix and one column per capacity. Return the largest total value of a selection with total weight at most `capacity`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= weight.length <= 100`, and both arrays have equal length.
- **Weight** satisfies `1 <= weight[i] <= 1000`.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Capacity** satisfies `0 <= capacity <= 5000`.
- **Mutation** is not allowed, because both arrays stay unchanged.

**Example 1.** Input `weight = [1,3,4,5]`, `value = [1,4,5,7]`, `capacity = 7`, output `9`.

**Example 2.** Input `weight = [6,7]`, `value = [3,4]`, `capacity = 5`, output `0`.

**Hint.** For prefix `i` and capacity `c`, which two entries of the previous row give the skip case and the take case?

**Changed decision.** Both cases read row `i - 1`, and the method writes row `i` into a separate array row. The row index replaces the loop direction as the guard against reuse.

#### [Vary] Descending Compression (Author exercise)
<!-- id: cap-zok-descending-compression -->

**Prerequisites.** The exercise above.

**Problem.** Items come as arrays `weight` and `value`, and no item may be chosen twice. Using one array of length `capacity + 1`, return an `int[]` of that length whose entry `c` is the largest total value of a selection with total weight at most `c`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= weight.length <= 100`, and both arrays have equal length.
- **Weight** satisfies `1 <= weight[i] <= 1000`.
- **Value** satisfies `0 <= value[i] <= 1000`.
- **Capacity** satisfies `0 <= capacity <= 5000`.
- **Mutation** is not allowed, because both input arrays stay unchanged.

**Example 1.** Input `weight = [2,3]`, `value = [3,4]`, `capacity = 5`, output `[0,0,3,4,4,7]`.

**Example 2.** Input `weight = [4]`, `value = [9]`, `capacity = 3`, output `[0,0,0,0]`.

**Hint.** If the inner loop starts from the largest capacity, which entries still hold the previous row when entry `c` is rewritten?

**Changed decision.** The method returns the whole compressed row in place of one cell. Every entry of that row must match the answer of a table that has a separate row for each item prefix.

#### [Boundary] Ascending-Loop Counterexample (Author exercise)
<!-- id: cap-zok-ascending-counterexample -->

**Prerequisites.** The two exercises above and the previous lesson.

**Problem.** Items come as arrays `weight` and `value`, each usable once. Compute the correct one-use table, and also the table that an upward capacity loop would produce. Return the smallest capacity `c` in `0..capacity` where the two tables differ, or -1 if they agree everywhere.

**Constraints.** The limits are:
- **Length** satisfies `0 <= weight.length <= 12`, and both arrays have equal length.
- **Weight** satisfies `1 <= weight[i] <= 50`.
- **Value** satisfies `0 <= value[i] <= 1000`, and an item with value 0 never causes a difference.
- **Capacity** satisfies `0 <= capacity <= 200`.
- **Mutation** is not allowed, because both arrays stay unchanged.

**Example 1.** Input `weight = [3]`, `value = [4]`, `capacity = 6`, output `6`.

**Example 2.** Input `weight = [4]`, `value = [5]`, `capacity = 7`, output `-1`.

**Hint.** A repeated item first appears at a capacity of at least twice its weight. Which capacities need to be compared at all?

**Changed decision.** The method runs both loop directions on separate arrays and compares them entry by entry. The first capacity with a different entry is the answer.

#### [Recognize] Partition Equal Subset Sum (LeetCode 416)
<!-- id: cap-zok-equal-partition -->

**Prerequisites.** All three exercises above.

**Problem.** An array `nums` of positive integers is given. Decide whether the elements can be split into two groups with equal sums, where each element belongs to exactly one group. Return `true` if such a split exists and `false` otherwise.

**Constraints.** The limits are:
- **Length** satisfies `1 <= nums.length <= 200`.
- **Value** satisfies `1 <= nums[i] <= 100`.
- **Result** is a `boolean`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `nums = [3,3,6,2,4]`, output `true`.

**Example 2.** Input `nums = [2,2,3,5]`, output `false`.

**Hint.** If the two groups have equal sums, what must one group sum to, and which sums can a one-use loop reach?

**Changed decision.** The items are the elements, each weighs its own value, and the question asks whether the sum `total / 2` is reachable exactly. The table holds booleans in place of best values.
