<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Objective Types

#### Solution: [Build] Mark The Reachable Cells (Author exercise)
<!-- id: dp-obj-reachable-states -->

**Approach.**
The method allocates a `boolean[]` of length `n + 1` and sets entry 0 to true, because the walk starts there. It then visits cells 1 through `n` from left to right. A broken cell is skipped and keeps false. For any other cell, it checks each allowed jump `j`. When `c - j` is not negative and its entry is true, the cell becomes true, and the inner loop stops early because one true predecessor is enough.

The invariant is that after cell `c` is processed, entry `c` is true exactly when a walk over working cells lands on `c`. Every predecessor lies to the left, so it is final before it is read. The OR rule is the right merge for feasibility, because one reachable predecessor is enough and others add nothing. The tests compare against a recursive search over all walks.

**Complexity.**
- **Time** is O(n * k), because each of the n cells checks at most k jump lengths.
- **Space** is O(n) for the returned array, and both inputs stay unchanged.

```java run
import java.util.*;

public final class ObjReachable {
    /**
     * Returns, for every cell, whether a walk from cell 0 lands on it.
     * Time: O(n * k). Space: O(n).
     * Invariant: after cell c is processed, ok[c] is true iff a walk over working cells reaches c.
     */
    static boolean[] reachable(int n, boolean[] broken, int[] jumps) {
        boolean[] ok = new boolean[n + 1];
        // The walk starts on cell 0, which is the base value for feasibility.
        ok[0] = true;
        // Cells are filled left to right, so each predecessor is final before it is read.
        for (int c = 1; c <= n; c++) {
            // A broken cell can never be landed on, so it keeps false.
            if (broken[c]) continue;
            // Each allowed jump names one predecessor, so the inner loop costs O(k).
            for (int j : jumps) {
                int p = c - j;
                // One reachable predecessor is enough, which is the OR merge.
                if (p >= 0 && ok[p]) {
                    ok[c] = true;
                    break;
                }
            }
        }
        // The caller receives a fresh array; the inputs were only read.
        return ok;
    }

    /** Oracle: depth-first search over every walk, marking each landing cell. */
    static void walk(int pos, int n, boolean[] broken, int[] jumps, boolean[] seen) {
        seen[pos] = true;
        for (int j : jumps) {
            int q = pos + j;
            if (q <= n && !broken[q]) walk(q, n, broken, jumps, seen);
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        boolean[] none8 = new boolean[8];
        if (!Arrays.equals(reachable(7, none8, new int[] {2, 3}), new boolean[] {true, false, true, true, true, true, true, true})) throw new AssertionError("ex1");
        if (!Arrays.equals(reachable(4, new boolean[] {false, true, true, true, false}, new int[] {1, 2}), new boolean[] {true, false, false, false, false})) throw new AssertionError("ex2");
        // A row with only cell 0 returns true for cell 0.
        if (!Arrays.equals(reachable(0, new boolean[1], new int[] {1}), new boolean[] {true})) throw new AssertionError("n=0");
        // The inputs are not changed.
        boolean[] bk = {false, true, false, false};
        int[] jp = {1, 2};
        boolean[] bkCopy = bk.clone();
        int[] jpCopy = jp.clone();
        reachable(3, bk, jp);
        if (!Arrays.equals(bk, bkCopy) || !Arrays.equals(jp, jpCopy)) throw new AssertionError("mutation");
        // Random rows against the exhaustive search.
        Random rnd = new Random(2611);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(14);
            boolean[] broken = new boolean[n + 1];
            for (int i = 1; i <= n; i++) broken[i] = rnd.nextInt(4) == 0;
            int k = 1 + rnd.nextInt(3);
            int[] jumps = new int[k];
            for (int i = 0; i < k; i++) jumps[i] = i == 0 ? 1 + rnd.nextInt(2) : 2 + i + 1;
            boolean[] expected = new boolean[n + 1];
            walk(0, n, broken, jumps, expected);
            if (!Arrays.equals(reachable(n, broken, jumps), expected)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Count The Same Paths (Author exercise)
<!-- id: dp-obj-count-sequences -->

**Approach.**
The table entry `ways[c]` is the number of jump sequences that end on cell `c`. The base value is `ways[0] = 1`, because the empty sequence is the one way to stand on the start. For every working cell, `ways[c]` is the sum of `ways[c - j]` over the allowed jumps with `c - j >= 0`. Sequences that differ in their last jump differ as lists, so no sequence is counted twice. A broken cell keeps 0.

The invariant is that after cell `c` is processed, `ways[c]` equals the number of sequences over working cells that end on `c`, reduced modulo 1000000007. The method adds in a `long` and reduces after each addition, so the stored values stay below the modulus. The tests compare against a recursive enumeration that counts complete sequences without reduction.

**Complexity.**
- **Time** is O(n * k), because each cell sums at most k predecessors.
- **Space** is O(n) for the table of counts.

```java run
import java.util.*;

public final class ObjCount {
    static final int MOD = 1_000_000_007;

    /**
     * Returns the number of jump sequences from cell 0 to cell n over working cells, modulo 1000000007.
     * Time: O(n * k). Space: O(n).
     * Invariant: after cell c, ways[c] is the sequence count into c, reduced by the modulus.
     */
    static int countSequences(int n, boolean[] broken, int[] jumps) {
        long[] ways = new long[n + 1];
        // The empty sequence is the single way to stand on cell 0.
        ways[0] = 1;
        // Cells are filled left to right, so each predecessor is final before it is read.
        for (int c = 1; c <= n; c++) {
            // A broken cell has no sequence ending on it, so it keeps 0.
            if (broken[c]) continue;
            // Each allowed jump adds the count of one predecessor.
            for (int j : jumps) {
                int p = c - j;
                if (p >= 0) ways[c] = (ways[c] + ways[p]) % MOD;
            }
        }
        // The count for the exit cell is the answer.
        return (int) ways[n];
    }

    /** Oracle: enumerate every complete sequence without any reduction. */
    static long enumerate(int pos, int n, boolean[] broken, int[] jumps) {
        if (pos == n) return 1;
        long total = 0;
        for (int j : jumps) {
            int q = pos + j;
            if (q <= n && !broken[q]) total += enumerate(q, n, broken, jumps);
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countSequences(7, new boolean[8], new int[] {1, 2, 3}) != 44) throw new AssertionError("ex1");
        boolean[] b2 = new boolean[9];
        b2[2] = true;
        b2[5] = true;
        if (countSequences(8, b2, new int[] {1, 2, 4}) != 7) throw new AssertionError("ex2");
        // The start cell alone has exactly one sequence.
        if (countSequences(0, new boolean[1], new int[] {1}) != 1) throw new AssertionError("n=0");
        // Java fact: counts of a long row exceed int, so the table must be long or reduced.
        long[] fibLike = new long[60];
        fibLike[0] = 1;
        for (int c = 1; c < 60; c++) fibLike[c] = fibLike[c - 1] + (c >= 2 ? fibLike[c - 2] : 0);
        if (fibLike[59] <= Integer.MAX_VALUE) throw new AssertionError("counts should outgrow int");
        // Random rows against the exhaustive enumeration, with no reduction needed at this size.
        Random rnd = new Random(2612);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(16);
            boolean[] broken = new boolean[n + 1];
            for (int i = 1; i <= n; i++) broken[i] = rnd.nextInt(5) == 0;
            int[] pool = {1, 2, 3, 4, 5};
            int k = 1 + rnd.nextInt(3);
            int[] jumps = Arrays.copyOf(pool, k);
            long expected = enumerate(0, n, broken, jumps) % MOD;
            if (countSequences(n, broken, jumps) != expected) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Impossible Minimum (Author exercise)
<!-- id: dp-obj-impossible-minimum -->

**Approach.**
The table entry `best[c]` is the smallest total cost of a walk that lands on cell `c`. The base value is `best[0] = 0`, and every other entry starts at the sentinel `INF`, which is half the largest `long`. For a working cell, `best[c]` is the smaller of its current value and `best[c - j] + costs[i]` for every jump `i` with `c - j >= 0`.

The sentinel is chosen so that adding one cost cannot wrap. A cost is at most 10^9 and a walk has at most 1000 jumps, so any sum stays near `INF` plus 10^12, far below the maximum of `long`. An entry that never improved is still at or above `INF`, and the method returns -1 for it. The invariant is that after cell `c`, `best[c]` is either the true minimum over walks into `c` or a value at least `INF`. The tests compare against an exhaustive search and assert the overflow facts for `int`.

**Complexity.**
- **Time** is O(n * k), because each cell tries at most k predecessors.
- **Space** is O(n) for the table of totals.

```java run
import java.util.*;

public final class ObjMinCost {
    static final long INF = Long.MAX_VALUE / 2;

    /**
     * Returns the lowest total cost from cell 0 to cell n, or -1 when no walk exists.
     * Time: O(n * k). Space: O(n).
     * Invariant: after cell c, best[c] is the true minimum into c or a value at least INF.
     */
    static long minCost(int n, boolean[] broken, int[] jumps, int[] costs) {
        long[] best = new long[n + 1];
        // Every cell starts at the sentinel; the sentinel has room to add a cost without wrapping.
        Arrays.fill(best, INF);
        // Standing on the start costs nothing, which is the base value for minimization.
        best[0] = 0;
        // Cells are filled left to right, so each predecessor is final before it is read.
        for (int c = 1; c <= n; c++) {
            // A broken cell keeps the sentinel.
            if (broken[c]) continue;
            // Each jump offers one candidate total, so the inner loop costs O(k).
            for (int i = 0; i < jumps.length; i++) {
                int p = c - jumps[i];
                // The sum cannot wrap because INF is half of the largest long.
                if (p >= 0 && best[p] + costs[i] < best[c]) best[c] = best[p] + costs[i];
            }
        }
        // A value at or above the sentinel means that no real walk reached the exit.
        return best[n] >= INF ? -1 : best[n];
    }

    /** Oracle: exhaustive search over all walks, returning INF when none exists. */
    static long search(int pos, int n, boolean[] broken, int[] jumps, int[] costs) {
        if (pos == n) return 0;
        long out = Long.MAX_VALUE;
        for (int i = 0; i < jumps.length; i++) {
            int q = pos + jumps[i];
            if (q > n || broken[q]) continue;
            long sub = search(q, n, broken, jumps, costs);
            if (sub != Long.MAX_VALUE) out = Math.min(out, sub + costs[i]);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCost(6, new boolean[7], new int[] {1, 2, 4}, new int[] {5, 3, 10}) != 9) throw new AssertionError("ex1");
        if (minCost(6, new boolean[7], new int[] {2, 3}, new int[] {1000000000, 1000000000}) != 2000000000L) throw new AssertionError("ex2");
        // An unreachable exit returns -1, and n = 0 costs nothing.
        if (minCost(5, new boolean[6], new int[] {2}, new int[] {7}) != -1) throw new AssertionError("impossible");
        if (minCost(0, new boolean[1], new int[] {1}, new int[] {9}) != 0) throw new AssertionError("n=0");
        // Java facts: int sentinel plus one wraps negative, and the long sentinel plus a cost does not.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int wrap");
        if (INF + 1_000_000_000L < INF) throw new AssertionError("long safe");
        if (1_000_000_000 + 1_000_000_000 + 1_000_000_000 >= 0) throw new AssertionError("three costs overflow int");
        // Random rows and costs against the exhaustive search.
        Random rnd = new Random(2613);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(13);
            boolean[] broken = new boolean[n + 1];
            for (int i = 1; i <= n; i++) broken[i] = rnd.nextInt(4) == 0;
            int k = 1 + rnd.nextInt(3);
            int[] jumps = new int[k];
            int[] costs = new int[k];
            for (int i = 0; i < k; i++) {
                jumps[i] = i + 2 - (i == 0 ? 1 : 0);
                costs[i] = rnd.nextInt(3) == 0 ? 1_000_000_000 : rnd.nextInt(20);
            }
            long s = search(0, n, broken, jumps, costs);
            long expected = s == Long.MAX_VALUE ? -1 : s;
            if (minCost(n, broken, jumps, costs) != expected) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Path Sum (LeetCode 64)
<!-- id: dp-obj-min-path-sum -->

**Approach.**
The state `sum[r][c]` is the smallest path sum from the top-left cell to cell `(r, c)`. A cell can be entered only from above or from the left. So `sum[r][c]` is the value of the cell plus the smaller of the two predecessor sums. The top-left cell holds its own value. The first row has only a left predecessor and the first column has only an upper predecessor, so those cells take the single available sum.

The merge step is a minimum, as in the other minimization lesson exercise, and the base value is the value of the first cell. No sentinel is needed, because every cell of a full grid is reachable. The invariant is that after cell `(r, c)` is filled, `sum[r][c]` is the minimum over all paths into that cell. The tests compare against a recursion over every path and check that the input grid is unchanged.

**Complexity.**
- **Time** is O(m * n), because each cell does one comparison and one addition.
- **Space** is O(m * n) for the table, and the input grid stays unchanged.

```java run
import java.util.*;

public final class ObjMinPath {
    /**
     * Returns the smallest sum over right-and-down paths from the top-left to the bottom-right cell.
     * Time: O(m * n). Space: O(m * n).
     * Invariant: after cell (r, c), sum[r][c] is the minimum path sum into that cell.
     */
    static int minPathSum(int[][] grid) {
        int m = grid.length, n = grid[0].length;
        int[][] sum = new int[m][n];
        // Rows are filled top to bottom and columns left to right, so predecessors are final.
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (r == 0 && c == 0) {
                    // The base value is the first cell itself.
                    sum[r][c] = grid[r][c];
                } else if (r == 0) {
                    // The first row can only be entered from the left.
                    sum[r][c] = sum[r][c - 1] + grid[r][c];
                } else if (c == 0) {
                    // The first column can only be entered from above.
                    sum[r][c] = sum[r - 1][c] + grid[r][c];
                } else {
                    // The minimum merge keeps the cheaper of the two predecessors.
                    sum[r][c] = Math.min(sum[r - 1][c], sum[r][c - 1]) + grid[r][c];
                }
            }
        }
        // The bottom-right entry covers every path.
        return sum[m - 1][n - 1];
    }

    /** Oracle: recursion over every path. */
    static int search(int[][] g, int r, int c) {
        if (r == g.length - 1 && c == g[0].length - 1) return g[r][c];
        int best = Integer.MAX_VALUE;
        if (r + 1 < g.length) best = Math.min(best, search(g, r + 1, c));
        if (c + 1 < g[0].length) best = Math.min(best, search(g, r, c + 1));
        return g[r][c] + best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minPathSum(new int[][] {{2, 5, 1}, {3, 1, 9}, {4, 2, 1}}) != 9) throw new AssertionError("ex1");
        if (minPathSum(new int[][] {{7, 0, 4, 6}}) != 17) throw new AssertionError("ex2");
        // A single cell is its own path, and a single column sums down.
        if (minPathSum(new int[][] {{0}}) != 0 || minPathSum(new int[][] {{1}, {2}, {3}}) != 6) throw new AssertionError("small");
        // The input grid is not changed.
        int[][] keep = {{1, 2}, {3, 4}};
        minPathSum(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{1, 2}, {3, 4}})) throw new AssertionError("mutation");
        // Random grids against the recursion.
        Random rnd = new Random(2614);
        for (int t = 0; t < 3000; t++) {
            int m = 1 + rnd.nextInt(5), n = 1 + rnd.nextInt(5);
            int[][] g = new int[m][n];
            for (int[] row : g) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(10);
            if (minPathSum(g) != search(g, 0, 0)) throw new AssertionError("random " + t);
        }
    }
}
```
