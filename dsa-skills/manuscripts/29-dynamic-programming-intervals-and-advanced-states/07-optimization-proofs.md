<!-- lesson-kind: standard -->
<!-- lesson-id: optimization-proofs -->
## Optimization Proofs

<!-- stage: context -->
### A Scheduler That Runs Out Of Memory

A batch system runs a pipeline of 100,000 stages on a row of 10,000 servers. Stage `r` costs `cost[r][j]` on server `j`. A stage may not run on a server with a smaller number than the server of the stage before it, because data only flows toward higher server numbers. The scheduler must pick one server per stage and minimize the total cost.

A correct recurrence exists. The first test run still fails, because the table of best totals holds 10^9 entries. At 4 bytes each, that is 4 GB. Even with enough memory, the table fill takes about 5 * 10^12 steps, which is far beyond a practical run.

Formally, the input is an `int[][] cost` with `R` rows and `C` columns. A **plan** is a sequence of columns `c_0 <= c_1 <= ... <= c_(R-1)`, one per row. Its cost is the sum of `cost[r][c_r]`. The task is to return the smallest plan cost. The input stays unchanged.

This lesson asks how to shrink a correct recurrence in time and memory without changing a single answer.

<!-- stage: naive -->
### Enumerating Plans And Filling A Full Table

The direct method tries every plan. At row `r` it tries every column from the previous column onward.

```java
static long tryAll(int[][] cost, int r, int from) {
    if (r == cost.length) return 0;
    long best = Long.MAX_VALUE;
    for (int j = from; j < cost[0].length; j++) {
        best = Math.min(best, cost[r][j] + tryAll(cost, r + 1, j));
    }
    return best;
}
```

Call `tryAll(cost, 0, 0)`. The call tree has one leaf for each plan. For `R` rows and `C` columns, the number of plans is the binomial coefficient of `R + C - 1` over `R`, which is exponential in `R`.

A table removes the repeated calls. Entry `dp[r][j]` holds the cheapest plan that covers rows 0 to `r` and ends in column `j`. Each entry scans the whole previous row up to column `j`.

```java
static long fullTable(int[][] cost) {
    int rows = cost.length;
    int cols = cost[0].length;
    long[][] dp = new long[rows][cols];
    for (int j = 0; j < cols; j++) dp[0][j] = cost[0][j];
    for (int r = 1; r < rows; r++) {
        for (int j = 0; j < cols; j++) {
            long best = Long.MAX_VALUE;
            for (int k = 0; k <= j; k++) best = Math.min(best, dp[r - 1][k]);
            dp[r][j] = cost[r][j] + best;
        }
    }
    long answer = Long.MAX_VALUE;
    for (int j = 0; j < cols; j++) answer = Math.min(answer, dp[rows - 1][j]);
    return answer;
}
```

The table is correct. It costs O(R * C^2) time and O(R * C) memory.

<!-- stage: bottleneck -->
### Repeated Scans And Rows Nobody Rereads

```predict
In fullTable, which rows of dp does the code read while it computes row 40? And how many entries of row 39 does the entry for column 700 scan?

It reads only row 39, and it never reads rows 0 to 38 again. The entry for column 700 scans 701 entries of row 39, and the entry for column 701 scans the same 701 entries plus one more.
```

The prediction shows two separate wastes. The first is memory. Rows 0 to 38 sit in the table, yet no later statement reads them. For R = 100,000 and C = 10,000 the table holds 10^9 entries, and only 2 * 10^4 of them matter at any moment.

The second waste is time. The inner loop over `k` computes a minimum over columns 0 to `j`. The next entry computes a minimum over columns 0 to `j + 1`. Those two ranges share all but one column, so the work for column `j + 1` repeats the work for column `j`. Across a row, the scans cost 1 + 2 + ... + C, which is O(C^2). Across all rows, the total is O(R * C^2), which is 5 * 10^12 steps for the opening input.

Both wastes have a cheap cure, but each cure carries a risk. Dropping rows is safe only if nothing later reads them. Replacing a scan with a stored value is safe only if the stored value equals the scan result for every column. Writing new values over old ones is safe only if every old value is read before it disappears. The next section turns these three risks into proofs.

<!-- stage: insight -->
### Prove What Each Entry Reads

An optimization is correct when it keeps every value the original recurrence reads and every candidate it compares. The proof lists those reads first and then shows that the cheaper code makes the same reads.

<!-- names: dependency set, running minimum, update direction -->

#### List The Dependency Set

The **dependency set** of an entry is the set of table cells its formula reads. For `dp[r][j]` the set is `dp[r - 1][0]` to `dp[r - 1][j]`. Every member has row `r - 1`. No cell from row `r - 2` or earlier appears. Therefore, once row `r` is complete, rows before `r - 1` can be discarded. Two arrays of length `C` replace the table, and the memory drops from O(R * C) to O(C).

#### Keep A Running Minimum

The scan computes `min(dp[r - 1][0..j])`. Call this value `m_j`. The next scan computes `m_(j+1)`, whose candidate set is the candidate set of `m_j` plus the single cell `dp[r - 1][j + 1]`. So `m_(j+1) = min(m_j, dp[r - 1][j + 1])`. A **running minimum** is a variable that holds `m_j` while the loop moves from column to column. It starts as infinity, and one comparison per column updates it. The candidate set is identical to the scan, so every answer is identical, and the row costs O(C) in place of O(C^2).

#### Choose The Update Direction

The two arrays can shrink to one. The new value `dp[r][j]` may overwrite the old value `dp[r - 1][j]` only if no later statement still needs the old value. The running minimum already consumed the old value at column `j`, and later columns need only the running minimum, not the cell. Walking left to right, read the old cell, fold it into the running minimum, and then write the new value. The **update direction** is this order of visiting cells. It is part of the proof. Walking right to left would overwrite old cells that columns on the left still need.

The same question decides other single-array tables. A recurrence that reads the old value at a smaller index must visit indexes from high to low. A recurrence that must read the new value at a smaller index must visit them from low to high. The invariant for the plan table is that before column `j` is processed, the array holds new values for columns below `j` and old values for columns from `j` on, and the running minimum equals the minimum of the old values below `j`.

<!-- stage: variables -->
### One Array And One Running Value

The method takes the cost table unchanged and keeps these working values.

- **dp** is a `long[C]` array that holds the best totals of the most recent finished row; before row 0 it holds zeros.
- **r** is the row being processed, from 0 to `R - 1`.
- **j** is the column being processed, from 0 to `C - 1`.
- **old** is the value `dp[j]` had before this row touched it, which is the total for column `j` after row `r - 1`.
- **run** is the running minimum of the old values in columns 0 to `j`; it restarts at infinity for each row.

The zeros before row 0 stand for an empty plan with total 0, and they let row 0 use the same formula as every other row. Sums use `long`, because the total over 100,000 rows can pass the `int` limit of about 2.1 * 10^9 when costs reach 10^5.

<!-- stage: trace -->
### Two Runs Of The Single Array

#### Three Servers And Three Stages

The first run uses `cost = [[3,1,4],[2,5,1],[4,2,3]]`. The cells below list the cost table row by row, so cells 0 to 2 are row 0, cells 3 to 5 are row 1, and cells 6 to 8 are row 2. The pointer `cell` marks the entry in progress. The variable `old` is the value read from `dp` before the write, `run` is the running minimum after folding `old` in, and `dp` is the value written.

Row 0 sees only zeros, so it copies its costs: 3, 1 and 4. Row 1 starts with `old = 3`, and it writes 2 + 3 = 5 at column 0. At column 1 the running minimum becomes 1, and the entry writes 5 + 1 = 6. At column 2 the running minimum stays 1, and the entry writes 1 + 1 = 2. Row 2 repeats the pattern over the values 5, 6 and 2. It ends with 9, 7 and 5, and the smallest is 5.

```trace
{"cells":[3,1,4,2,5,1,4,2,3],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"r":-1,"j":-1,"old":0,"run":0,"dp":0},"note":"Start: dp holds zeros, which stand for an empty plan with total 0."},{"at":{"cell":0},"vars":{"r":0,"j":0,"old":0,"run":0,"dp":3},"note":"Row 0, column 0: old is 0, so the running minimum is 0. The entry writes 3 + 0 = 3."},{"at":{"cell":1},"vars":{"r":0,"j":1,"old":0,"run":0,"dp":1},"note":"Row 0, column 1: old is 0, so the running minimum is 0. The entry writes 1 + 0 = 1."},{"at":{"cell":2},"vars":{"r":0,"j":2,"dp":4},"note":"Row 0, column 2: old is 0, so the running minimum is 0. The entry writes 4 + 0 = 4."},{"at":{"cell":3},"vars":{"r":1,"j":0,"old":3,"run":3,"dp":5},"note":"Row 1, column 0: old is 3, so the running minimum is 3. The entry writes 2 + 3 = 5."},{"at":{"cell":4},"vars":{"r":1,"j":1,"old":1,"run":1,"dp":6},"note":"Row 1, column 1: old is 1, so the running minimum is 1. The entry writes 5 + 1 = 6."},{"at":{"cell":5},"vars":{"r":1,"j":2,"old":4,"run":1,"dp":2},"note":"Row 1, column 2: old is 4, so the running minimum is 1. The entry writes 1 + 1 = 2."},{"at":{"cell":6},"vars":{"r":2,"j":0,"old":5,"run":5,"dp":9},"note":"Row 2, column 0: old is 5, so the running minimum is 5. The entry writes 4 + 5 = 9."},{"at":{"cell":7},"vars":{"r":2,"j":1,"old":6,"run":5,"dp":7},"note":"Row 2, column 1: old is 6, so the running minimum is 5. The entry writes 2 + 5 = 7."},{"at":{"cell":8},"vars":{"r":2,"j":2,"old":2,"run":2,"dp":5},"note":"Row 2, column 2: old is 2, so the running minimum is 2. The entry writes 3 + 2 = 5."},{"at":{"cell":8},"vars":{"r":2,"j":2,"dp":5},"note":"All rows are done. The smallest value in dp is 5, which is the cheapest plan."}]}
```

#### Four Servers And Three Stages

The second run uses `cost = [[5,2,6,3],[4,7,1,5],[6,3,2,1]]`. The running minimum drops at different columns in each row, and it always covers old values only. Row 0 writes 5, 2, 6 and 3. In row 1 the running minimum falls to 2 at column 1, so column 2 writes 1 + 2 = 3. Row 2 then sees the old values 9, 9, 3 and 7. Its running minimum falls to 3 at column 2, so columns 2 and 3 write 5 and 4. The smallest final value is 4.

```trace
{"cells":[5,2,6,3,4,7,1,5,6,3,2,1],"pointers":["cell"],"steps":[{"at":{"cell":-1},"vars":{"r":-1,"j":-1,"old":0,"run":0,"dp":0},"note":"Start: dp holds zeros, which stand for an empty plan with total 0."},{"at":{"cell":0},"vars":{"r":0,"j":0,"dp":5},"note":"Row 0, column 0: old is 0, so the running minimum is 0. The entry writes 5 + 0 = 5."},{"at":{"cell":1},"vars":{"r":0,"j":1,"old":0,"run":0,"dp":2},"note":"Row 0, column 1: old is 0, so the running minimum is 0. The entry writes 2 + 0 = 2."},{"at":{"cell":2},"vars":{"r":0,"j":2,"old":0,"run":0,"dp":6},"note":"Row 0, column 2: old is 0, so the running minimum is 0. The entry writes 6 + 0 = 6."},{"at":{"cell":3},"vars":{"r":0,"j":3,"old":0,"run":0,"dp":3},"note":"Row 0, column 3: old is 0, so the running minimum is 0. The entry writes 3 + 0 = 3."},{"at":{"cell":4},"vars":{"r":1,"j":0,"old":5,"run":5,"dp":9},"note":"Row 1, column 0: old is 5, so the running minimum is 5. The entry writes 4 + 5 = 9."},{"at":{"cell":5},"vars":{"r":1,"j":1,"old":2,"run":2,"dp":9},"note":"Row 1, column 1: old is 2, so the running minimum is 2. The entry writes 7 + 2 = 9."},{"at":{"cell":6},"vars":{"r":1,"j":2,"old":6,"run":2,"dp":3},"note":"Row 1, column 2: old is 6, so the running minimum is 2. The entry writes 1 + 2 = 3."},{"at":{"cell":7},"vars":{"r":1,"j":3,"old":3,"run":2,"dp":7},"note":"Row 1, column 3: old is 3, so the running minimum is 2. The entry writes 5 + 2 = 7."},{"at":{"cell":8},"vars":{"r":2,"j":0,"old":9,"run":9,"dp":15},"note":"Row 2, column 0: old is 9, so the running minimum is 9. The entry writes 6 + 9 = 15."},{"at":{"cell":9},"vars":{"r":2,"j":1,"old":9,"run":9,"dp":12},"note":"Row 2, column 1: old is 9, so the running minimum is 9. The entry writes 3 + 9 = 12."},{"at":{"cell":10},"vars":{"r":2,"j":2,"old":3,"run":3,"dp":5},"note":"Row 2, column 2: old is 3, so the running minimum is 3. The entry writes 2 + 3 = 5."},{"at":{"cell":11},"vars":{"r":2,"j":3,"old":7,"run":3,"dp":4},"note":"Row 2, column 3: old is 7, so the running minimum is 3. The entry writes 1 + 3 = 4."},{"at":{"cell":11},"vars":{"r":2,"j":3,"dp":4},"note":"All rows are done. The smallest value in dp is 4, which is the cheapest plan."}]}
```

<!-- stage: code -->
### Rolling The Table Into One Array

The method returns the smallest plan cost. It keeps one array and one running value for each row.

```java
static long cheapestPlan(int[][] cost) {
    int cols = cost[0].length;
    long[] dp = new long[cols];
    for (int[] row : cost) {
        long run = Long.MAX_VALUE;
        for (int j = 0; j < cols; j++) {
            long old = dp[j];
            run = Math.min(run, old);
            dp[j] = row[j] + run;
        }
    }
    long answer = Long.MAX_VALUE;
    for (long v : dp) answer = Math.min(answer, v);
    return answer;
}
```

Time drops to O(R * C), and memory drops to O(C). For the opening input, that is 10^9 steps and 10,000 stored values. The read of `old` comes before the write to `dp[j]`, and this order is the whole proof of the single array. If `R` or `C` is 0, the input is outside the contract. The exercises below practice each proof step on its own.

<!-- stage: applicability -->
### Checking An Optimization Before Using It

#### Reading The Cue

Look for a recurrence that is already correct but too large or too slow. Two cues matter. A table whose entries read only the previous row can shrink to one or two rows. A scan over a range that grows by one cell per column can become a maintained aggregate. Write the original recurrence first, list its dependency set, and name the structure that replaces the scan.

#### Checking The Invariant

The invariant is that the optimized code reads every cell and considers every candidate the original reads and considers. Test it by running both versions on random small inputs and comparing every answer. Include a single row, a single column, equal costs everywhere and costs that make the best plan stay in one column.

#### Avoiding The False Friend

The false friend is a scan whose range slides in place of growing. If the previous column must lie within a fixed distance of `j`, the range drops a cell on the left as it gains one on the right. A minimum cannot forget a dropped cell, so the running minimum gives wrong answers. A second false friend is the in-place loop in the wrong direction. It compiles, runs fast and returns plausible numbers, but it lets one item or one stage reuse a value that the recurrence forbids.

#### Knowing The Limits

This method does not apply when later rows read rows older than the previous one, unless the code keeps that many rows. Faster recurrence-specific techniques such as Knuth optimization, divide-and-conquer optimization and the convex hull trick need their own proofs of structure. They are out of scope here, and a later chapter owns them.

<!-- stage: exercises -->
### Exercises

#### [Build] Roll One Dimension (Author exercise)
<!-- id: dp29-roll-one-dimension -->

**Prerequisites.** The dependency set and the single array from this lesson.

**Problem.** An `int[][] cost` with `R` rows and `C` columns is given. A **falling path** picks one column per row, and each column differs from the previous pick by at most 1. Return the smallest sum of the picked costs. Use only arrays of length `C` for the table.

**Constraints.** The limits are:
- **Size** satisfies `1 <= R <= 200` and `1 <= C <= 200`.
- **Values** satisfy `0 <= cost[r][j] <= 10000`.
- **Result** is a `long`.
- **Mutation** is not allowed, so the method leaves `cost` unchanged.

**Example 1.** Input `cost = [[3,1,4],[2,5,1],[4,2,3]]`, output `4`.

**Example 2.** Input `cost = [[7,2],[1,9]]`, output `3`.

**Hint.** List which cells the entry `(r, j)` reads. If every one has row `r - 1`, which earlier rows can go?

**Changed decision.** The table keeps two rows in place of all rows. A new row can overwrite the row before the previous one, because nothing reads it.

#### [Vary] Prefix-Minimum Transition (Author exercise)
<!-- id: dp29-prefix-minimum-transition -->

**Prerequisites.** The exercise above and the running minimum.

**Problem.** A matrix `int[][] cost` has `R` rows and `C` columns. Pick one column per row so that each picked column is strictly greater than the previous pick. Return the smallest sum of picked costs, or `-1` if no such plan exists.

**Constraints.** The limits are:
- **Size** satisfies `1 <= R <= 200` and `1 <= C <= 200`.
- **Values** satisfy `0 <= cost[r][j] <= 10000`.
- **Result** is a `long`, or `-1` when `R > C`.
- **Mutation** is not allowed, so the method leaves `cost` unchanged.

**Example 1.** Input `cost = [[3,1,4],[2,5,1]]`, output `2`.

**Example 2.** Input `cost = [[1],[1]]`, output `-1`.

**Hint.** The set of allowed previous columns for column `j` is columns 0 to `j - 1`. What is that set for column 0, and which old cell joins the minimum next?

**Changed decision.** The range ends one column earlier, so the running minimum folds in the old cell after the new value is written. Column 0 has an empty range and must stay unreachable.

#### [Boundary] In-Place Direction Counterexample (Author exercise)
<!-- id: dp29-direction-counterexample -->

**Prerequisites.** The two exercises above.

**Problem.** An `int[] weights` and an integer `target` are given. The single-array table `ways[s]` counts item subsets with sum `s`. A correct loop visits `s` from `target` down to each weight. A flawed loop visits `s` from each weight up to `target`. Return the flawed count minus the correct count for `ways[target]`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= weights.length <= 20`, and the array may be empty.
- **Values** satisfy `1 <= weights[i] <= 20` and `0 <= target <= 60`.
- **Result** is a `long`.
- **Mutation** is not allowed, so the method leaves `weights` unchanged.

**Example 1.** Input `weights = [2]`, `target = 4`, output `1`.

**Example 2.** Input `weights = []`, `target = 0`, output `0`.

**Hint.** In the upward loop, `ways[s - w]` may already include the current item. Which count does that produce for `weights = [2]`?

**Changed decision.** The loop direction flips, so each item can be used any number of times. The value of `target` is unchanged, but the meaning of the table entry is not.

#### [Recognize] Optimization Audit (Author exercise)
<!-- id: dp29-optimization-audit -->

**Prerequisites.** All three exercises above.

**Problem.** An `int[][] cost` and an integer `w` are given. Pick one column per row so that each picked column `c_r` satisfies `c_(r-1) <= c_r <= c_(r-1) + w`. Return the smallest sum of picked costs.

**Constraints.** The limits are:
- **Size** satisfies `1 <= R <= 100` and `1 <= C <= 100`.
- **Values** satisfy `0 <= cost[r][j] <= 10000`.
- **Window** satisfies `0 <= w <= 100`.
- **Result** is a `long`, and the method leaves `cost` unchanged.

**Example 1.** Input `cost = [[3,1,4],[2,5,1],[4,2,3]]`, `w = 100`, output `5`.

**Example 2.** Input `cost = [[3,1,4],[2,5,1],[4,2,3]]`, `w = 0`, output `8`.

**Hint.** Compare the range of previous columns for column `j` with the range the lesson used. For which values of `w` do the two ranges match?

**Changed decision.** The previous column range now has an upper limit, so a running minimum is valid only when the limit never cuts a cell. Otherwise the code scans the range.
