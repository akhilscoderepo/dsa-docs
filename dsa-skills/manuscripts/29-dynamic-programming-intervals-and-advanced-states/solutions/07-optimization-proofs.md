<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Optimization Proofs

#### Solution: [Build] Roll One Dimension (Author exercise)
<!-- id: dp29-roll-one-dimension -->

**Approach.**
The full table has entry `dp[r][j]` equal to `cost[r][j]` plus the smaller of `dp[r - 1][j - 1]`, `dp[r - 1][j]` and `dp[r - 1][j + 1]`, where a neighbour outside the row does not exist. Every cell in that dependency set has row `r - 1`. Row `r - 2` and earlier rows are never read once row `r - 1` exists, so two arrays suffice.

The method keeps `prev` for the finished row and `cur` for the row in progress. After each row, the two references swap, so the old `prev` becomes the next `cur` and gets overwritten. The invariant is that `prev` holds the exact table row `r - 1` whenever row `r` starts. Row 0 copies its costs, because it has no previous row.

**Complexity.**
- **Time** is O(R * C), because each entry costs at most three reads and one write.
- **Space** is O(C) for the two arrays, in place of O(R * C) for the table.

```java run
import java.util.*;

public final class Dp29RollOneDimension {
    /**
     * Returns the smallest falling path sum using two arrays of length C.
     * Time: O(R * C). Space: O(C).
     * Invariant: prev equals table row r - 1 when row r starts.
     */
    static long fallingPath(int[][] cost) {
        // cols is the width of every row, and each array holds one table row.
        int cols = cost[0].length;
        long[] prev = new long[cols];
        long[] cur = new long[cols];
        // Row 0 has no previous row, so it copies its own costs.
        for (int j = 0; j < cols; j++) prev[j] = cost[0][j];
        // Each later row reads only prev, which costs R - 1 passes of C entries.
        for (int r = 1; r < cost.length; r++) {
            for (int j = 0; j < cols; j++) {
                // Start with the cell straight above, then widen to the two diagonal cells if they exist.
                long best = prev[j];
                if (j > 0) best = Math.min(best, prev[j - 1]);
                if (j + 1 < cols) best = Math.min(best, prev[j + 1]);
                // The new entry adds its own cost to the best allowed predecessor.
                cur[j] = cost[r][j] + best;
            }
            // Swapping references reuses the old array without copying C values.
            long[] tmp = prev;
            prev = cur;
            cur = tmp;
        }
        // The answer is the smallest entry of the last finished row.
        long answer = Long.MAX_VALUE;
        for (long v : prev) answer = Math.min(answer, v);
        return answer;
    }

    /** Oracle: tries every falling path by recursion. */
    static long oracle(int[][] cost, int r, int col) {
        if (r == cost.length) return 0;
        long best = Long.MAX_VALUE;
        for (int j = Math.max(0, col - 1); j <= Math.min(cost[0].length - 1, col + 1); j++) {
            best = Math.min(best, cost[r][j] + oracle(cost, r + 1, j));
        }
        return best;
    }

    static long oracleAll(int[][] cost) {
        long best = Long.MAX_VALUE;
        for (int j = 0; j < cost[0].length; j++) best = Math.min(best, cost[0][j] + oracle(cost, 1, j));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (fallingPath(new int[][]{{3, 1, 4}, {2, 5, 1}, {4, 2, 3}}) != 4) throw new AssertionError("ex1");
        if (fallingPath(new int[][]{{7, 2}, {1, 9}}) != 3) throw new AssertionError("ex2");
        // A single row returns its smallest cost, and a single column returns the column sum.
        if (fallingPath(new int[][]{{4, 9, 2}}) != 2) throw new AssertionError("one row");
        if (fallingPath(new int[][]{{4}, {9}, {2}}) != 15) throw new AssertionError("one col");
        // Java gives a new long array zeros, and swapping two references leaves both arrays intact.
        long[] a = new long[2];
        long[] b = {5, 6};
        if (a[0] != 0 || a[1] != 0) throw new AssertionError("zero fill");
        long[] t = a;
        a = b;
        b = t;
        if (a[0] != 5 || b.length != 2) throw new AssertionError("swap");
        // The input must stay unchanged after the call.
        int[][] input = {{3, 1, 4}, {2, 5, 1}};
        fallingPath(input);
        if (!Arrays.deepEquals(input, new int[][]{{3, 1, 4}, {2, 5, 1}})) throw new AssertionError("mutated");
        // Random tables against the exhaustive path search.
        Random rnd = new Random(2907);
        for (int trial = 0; trial < 2000; trial++) {
            int rows = 1 + rnd.nextInt(5);
            int cols = 1 + rnd.nextInt(5);
            int[][] cost = new int[rows][cols];
            for (int[] row : cost) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(20);
            if (fallingPath(cost) != oracleAll(cost)) throw new AssertionError("random " + trial);
        }
    }
}
```

#### Solution: [Vary] Prefix-Minimum Transition (Author exercise)
<!-- id: dp29-prefix-minimum-transition -->

**Approach.**
Entry `dp[r][j]` equals `cost[r][j]` plus the smallest `dp[r - 1][k]` with `k < j`. The candidate range for column `j + 1` is the range for column `j` plus the single old cell `dp[r - 1][j]`. So one variable `run` carries the minimum from column to column.

The loop visits columns left to right and updates one array in place. At column `j` it reads `old = dp[j]`, writes the new value from `run`, and only then folds `old` into `run`. This order keeps `old` out of its own range, which is the strict inequality. Column 0 sees an empty range, so its value becomes unreachable. A large sentinel marks unreachable entries, and the final answer maps a sentinel to `-1`.

The invariant is that before column `j`, the array holds new values for columns below `j` and old values from `j` on, and `run` is the minimum of the old values below `j`.

**Complexity.**
- **Time** is O(R * C), because each entry costs one comparison and two array accesses.
- **Space** is O(C) for the single array.

```java run
import java.util.*;

public final class Dp29PrefixMinimumTransition {
    static final long INF = Long.MAX_VALUE / 4;

    /**
     * Returns the smallest cost of a plan with strictly increasing columns, or -1 if none exists.
     * Time: O(R * C). Space: O(C).
     * Invariant: before column j, dp holds new values below j, old values from j, and run is the old minimum below j.
     */
    static long strictPlan(int[][] cost) {
        // cols is the row width, and dp starts as row 0 because the first pick has no predecessor.
        int cols = cost[0].length;
        long[] dp = new long[cols];
        for (int j = 0; j < cols; j++) dp[j] = cost[0][j];
        // Each later row rewrites dp once, so the loops cost R - 1 passes of C steps.
        for (int r = 1; r < cost.length; r++) {
            long run = INF;
            for (int j = 0; j < cols; j++) {
                // Save the old value before the write destroys it.
                long old = dp[j];
                // An empty or unreachable range makes this entry unreachable.
                dp[j] = run >= INF ? INF : cost[r][j] + run;
                // Fold the old value in after the write, so the range stays strictly below the next column.
                run = Math.min(run, old);
            }
        }
        // The smallest final entry is the answer, and the sentinel means no plan exists.
        long answer = INF;
        for (long v : dp) answer = Math.min(answer, v);
        return answer >= INF ? -1 : answer;
    }

    /** Oracle: tries every strictly increasing column sequence. */
    static long oracle(int[][] cost, int r, int minCol) {
        if (r == cost.length) return 0;
        long best = INF;
        for (int j = minCol; j < cost[0].length; j++) {
            long rest = oracle(cost, r + 1, j + 1);
            if (rest < INF) best = Math.min(best, cost[r][j] + rest);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (strictPlan(new int[][]{{3, 1, 4}, {2, 5, 1}}) != 2) throw new AssertionError("ex1");
        if (strictPlan(new int[][]{{1}, {1}}) != -1) throw new AssertionError("ex2");
        // More rows than columns has no plan, and equal counts force the diagonal.
        if (strictPlan(new int[][]{{1, 1}, {1, 1}, {1, 1}}) != -1) throw new AssertionError("too many rows");
        if (strictPlan(new int[][]{{1, 9}, {9, 2}}) != 3) throw new AssertionError("diagonal");
        // The sentinel stays far from overflow when a cost is added to it once.
        if (INF + 10000 < INF) throw new AssertionError("sentinel overflow");
        // The input must stay unchanged after the call.
        int[][] input = {{3, 1, 4}, {2, 5, 1}};
        strictPlan(input);
        if (!Arrays.deepEquals(input, new int[][]{{3, 1, 4}, {2, 5, 1}})) throw new AssertionError("mutated");
        // Random tables against the exhaustive search.
        Random rnd = new Random(2908);
        for (int trial = 0; trial < 3000; trial++) {
            int rows = 1 + rnd.nextInt(5);
            int cols = 1 + rnd.nextInt(6);
            int[][] cost = new int[rows][cols];
            for (int[] row : cost) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(20);
            long expected = oracle(cost, 0, 0);
            if (expected >= INF) expected = -1;
            if (strictPlan(cost) != expected) throw new AssertionError("random " + trial);
        }
    }
}
```

#### Solution: [Boundary] In-Place Direction Counterexample (Author exercise)
<!-- id: dp29-direction-counterexample -->

**Approach.**
The array `ways[s]` counts subsets of the items processed so far with sum `s`. For one item of weight `w`, the new `ways[s]` equals the old `ways[s]` plus the old `ways[s - w]`. The formula needs the old value at the smaller index `s - w`.

Visiting `s` from `target` down to `w` keeps that promise, because the write at `s` happens before any smaller index is rewritten. Visiting `s` upward breaks it. By the time the loop reaches `s`, the cell `s - w` already includes the current item, so the item is counted again. The flawed loop therefore counts multisets, where an item may repeat. The method runs both loops and returns the flawed count minus the correct count.

The invariant for the downward loop is that every index below the current `s` still holds its value from before the current item. For the upward loop the invariant fails by design.

**Complexity.**
- **Time** is O(n * target), because each of the two loops makes `n` passes over at most `target` indexes.
- **Space** is O(target) for each array.

```java run
import java.util.*;

public final class Dp29DirectionCounterexample {
    /**
     * Returns flawed count minus correct count for ways[target].
     * Time: O(n * target). Space: O(target).
     * Invariant of the downward loop: indexes below s still hold values from before the current item.
     */
    static long gap(int[] weights, int target) {
        // Both arrays start with the empty subset at sum 0, and Java zero fills the rest.
        long[] correct = new long[target + 1];
        long[] flawed = new long[target + 1];
        correct[0] = 1;
        flawed[0] = 1;
        // Each item costs one pass over the table in each direction.
        for (int w : weights) {
            // Downward: the cell at s - w is still old when s is written.
            for (int s = target; s >= w; s--) correct[s] += correct[s - w];
            // Upward: the cell at s - w was already updated, so the item repeats.
            for (int s = w; s <= target; s++) flawed[s] += flawed[s - w];
        }
        // The gap is zero exactly when no repeated use changes the count at the target.
        return flawed[target] - correct[target];
    }

    /** Oracle for the correct count: tries every subset by bitmask. */
    static long subsets(int[] weights, int target) {
        long count = 0;
        for (int mask = 0; mask < (1 << weights.length); mask++) {
            int sum = 0;
            for (int i = 0; i < weights.length; i++) if ((mask >> i & 1) == 1) sum += weights[i];
            if (sum == target) count++;
        }
        return count;
    }

    /** Oracle for the flawed count: counts multiplicity choices item by item. */
    static long multisets(int[] weights, int i, int left) {
        if (i == weights.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int use = 0; use * weights[i] <= left; use++) total += multisets(weights, i + 1, left - use * weights[i]);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (gap(new int[]{2}, 4) != 1) throw new AssertionError("ex1");
        if (gap(new int[0], 0) != 0) throw new AssertionError("ex2");
        // Target 0 counts only the empty subset in both loops, and a heavy item never fits.
        if (gap(new int[]{3, 5}, 0) != 0) throw new AssertionError("target zero");
        if (gap(new int[]{9}, 4) != 0) throw new AssertionError("too heavy");
        // A weight of 1 and target 3 lets the flawed loop count one multiset that the subset count cannot.
        if (gap(new int[]{1}, 3) != 1) throw new AssertionError("repeat");
        // Java adds to a long array cell in place, so the compound assignment reads the current cell value.
        long[] cell = {2, 0};
        cell[1] += cell[0];
        cell[0] += cell[1];
        if (cell[1] != 2 || cell[0] != 4) throw new AssertionError("compound");
        // Random inputs against both oracles.
        Random rnd = new Random(2909);
        for (int trial = 0; trial < 1500; trial++) {
            int n = rnd.nextInt(8);
            int[] weights = new int[n];
            for (int i = 0; i < n; i++) weights[i] = 1 + rnd.nextInt(6);
            int target = rnd.nextInt(25);
            long expected = multisets(weights, 0, target) - subsets(weights, target);
            if (gap(weights, target) != expected) throw new AssertionError("random " + trial);
        }
    }
}
```

#### Solution: [Recognize] Optimization Audit (Author exercise)
<!-- id: dp29-optimization-audit -->

**Approach.**
The original recurrence is `dp[r][j] = cost[r][j] + min dp[r - 1][k]` over `k` with `j - w <= k <= j` and `k >= 0`. The dependency set lies in row `r - 1`, so two rows suffice for any `w`.

The lesson replaced the scan with a running minimum because its range was columns 0 to `j`, which grows by one cell per column. That range matches the original recurrence here only when the lower bound `j - w` never exceeds 0, which means `w >= C - 1`. For smaller `w`, the range drops its left cell as it gains the right one. A minimum cannot forget a cell, so the replacement would include columns the recurrence forbids and would return too small a value. The method therefore uses the running minimum in place when `w >= C - 1` and otherwise scans the window of the previous row in a second array.

The invariant is that every candidate the original recurrence compares is compared, and no other candidate is.

**Complexity.**
- **Time** is O(R * C) when `w >= C - 1`, and O(R * C * min(w + 1, C)) otherwise, because each entry scans its window.
- **Space** is O(C) in both cases.

```java run
import java.util.*;

public final class Dp29OptimizationAudit {
    /**
     * Returns the smallest plan cost when each column lies in [previous, previous + w].
     * Time: O(R * C) if w >= C - 1, otherwise O(R * C * (w + 1)). Space: O(C).
     * Invariant: each entry compares exactly the previous-row cells inside its window.
     */
    static long windowPlan(int[][] cost, int w) {
        // cols is the row width, and dp holds the finished row, starting from zeros for the empty plan.
        int cols = cost[0].length;
        long[] dp = new long[cols];
        if (w >= cols - 1) {
            // The window covers every column below j, so one running minimum equals the scan.
            for (int[] row : cost) {
                long run = Long.MAX_VALUE;
                for (int j = 0; j < cols; j++) {
                    // Read the old cell, fold it in, then overwrite it.
                    long old = dp[j];
                    run = Math.min(run, old);
                    dp[j] = row[j] + run;
                }
            }
        } else {
            // A narrow window needs old values, so a second array holds the new row.
            long[] next = new long[cols];
            for (int[] row : cost) {
                for (int j = 0; j < cols; j++) {
                    // Scan only the window, which costs at most w + 1 reads.
                    long best = Long.MAX_VALUE;
                    for (int k = Math.max(0, j - w); k <= j; k++) best = Math.min(best, dp[k]);
                    next[j] = row[j] + best;
                }
                // Swap the references so the finished row becomes the source of the next pass.
                long[] tmp = dp;
                dp = next;
                next = tmp;
            }
        }
        // The smallest entry of the last row is the answer.
        long answer = Long.MAX_VALUE;
        for (long v : dp) answer = Math.min(answer, v);
        return answer;
    }

    /** The unsafe replacement: a running minimum used for every window width. */
    static long forcedPrefix(int[][] cost) {
        long[] dp = new long[cost[0].length];
        for (int[] row : cost) {
            long run = Long.MAX_VALUE;
            for (int j = 0; j < dp.length; j++) {
                long old = dp[j];
                run = Math.min(run, old);
                dp[j] = row[j] + run;
            }
        }
        long answer = Long.MAX_VALUE;
        for (long v : dp) answer = Math.min(answer, v);
        return answer;
    }

    /** Oracle: tries every plan by recursion. */
    static long oracle(int[][] cost, int r, int prev, int w) {
        if (r == cost.length) return 0;
        long best = Long.MAX_VALUE;
        for (int j = prev; j <= Math.min(cost[0].length - 1, prev + w); j++) {
            best = Math.min(best, cost[r][j] + oracle(cost, r + 1, j, w));
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] sample = {{3, 1, 4}, {2, 5, 1}, {4, 2, 3}};
        // The two examples of the exercise.
        if (windowPlan(sample, 100) != 5) throw new AssertionError("ex1");
        if (windowPlan(sample, 0) != 8) throw new AssertionError("ex2");
        // The forced running minimum returns 5 for w = 0, which is smaller than the true 8.
        if (forcedPrefix(sample) != 5) throw new AssertionError("forced value");
        if (forcedPrefix(sample) == windowPlan(sample, 0)) throw new AssertionError("false friend hidden");
        // A window of C - 1 is the first width where the two methods must agree.
        if (windowPlan(sample, 2) != forcedPrefix(sample)) throw new AssertionError("boundary width");
        // The input must stay unchanged after the call.
        int[][] input = {{3, 1, 4}, {2, 5, 1}};
        windowPlan(input, 1);
        if (!Arrays.deepEquals(input, new int[][]{{3, 1, 4}, {2, 5, 1}})) throw new AssertionError("mutated");
        // Random tables against the exhaustive search for every width.
        Random rnd = new Random(2910);
        for (int trial = 0; trial < 3000; trial++) {
            int rows = 1 + rnd.nextInt(5);
            int cols = 1 + rnd.nextInt(6);
            int w = rnd.nextInt(cols + 2);
            int[][] cost = new int[rows][cols];
            for (int[] row : cost) for (int j = 0; j < cols; j++) row[j] = rnd.nextInt(20);
            long expected = Long.MAX_VALUE;
            for (int j = 0; j < cols; j++) expected = Math.min(expected, cost[0][j] + oracle(cost, 1, j, w));
            if (windowPlan(cost, w) != expected) throw new AssertionError("random " + trial);
        }
    }
}
```
