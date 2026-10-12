<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Transition Discipline

#### Solution: [Build] Separate Previous Row (Author exercise)
<!-- id: dp-trans-previous-row -->

**Approach.**
The method allocates a new array `next` of the same length and fills it from left to right. For column `j`, it starts with `prev[j]` as the best predecessor value. When `j > 0`, it replaces that value with `prev[j - 1]` if the left value is larger. It then adds `cost[j]` and stores the sum in `next[j]`. Every read targets `prev` or `cost`, and every write targets `next`, so the loop order cannot matter.

The invariant is that `prev` never changes, so each column sees the previous row exactly as the caller passed it. The method returns the new array and never returns an input array. The test below checks both facts: the inputs are equal to their copies after the call, and the result is a different object from `prev`.

**Complexity.**
- **Time** is O(w), because each column performs one comparison and one addition.
- **Space** is O(w) for the returned array, and the inputs stay unchanged.

```java run
import java.util.*;

public final class DpTransPreviousRow {
    /**
     * Builds the next row from an immutable previous row.
     * Time: O(w). Space: O(w).
     * Invariant: prev and cost are only read, and next is only written.
     */
    static int[] nextRow(int[] prev, int[] cost) {
        // A fresh array keeps the new row separate from the previous row.
        int[] next = new int[prev.length];
        // One pass over the columns costs O(w).
        for (int j = 0; j < prev.length; j++) {
            // Column 0 has only the straight-above predecessor.
            int best = prev[j];
            // A left predecessor exists only for j > 0, and the larger one wins.
            if (j > 0 && prev[j - 1] > best) best = prev[j - 1];
            // The cell cost is added to the best old value and stored in the new row.
            next[j] = cost[j] + best;
        }
        // The caller gets the new row; the inputs were never written.
        return next;
    }

    /** Oracle: collect the candidate predecessor values in a list and take the maximum. */
    static int[] oracle(int[] prev, int[] cost) {
        int[] out = new int[prev.length];
        for (int j = 0; j < prev.length; j++) {
            List<Integer> cand = new ArrayList<>();
            cand.add(prev[j]);
            if (j > 0) cand.add(prev[j - 1]);
            out[j] = cost[j] + Collections.max(cand);
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(nextRow(new int[] {3, 1, 4}, new int[] {1, 5, 9}), new int[] {4, 8, 13})) throw new AssertionError("ex1");
        if (!Arrays.equals(nextRow(new int[] {-6, -2, -8}, new int[] {2, -1, 3}), new int[] {-4, -3, 1})) throw new AssertionError("ex2");
        // Java fact: the result is a distinct object, so writing into it cannot change the previous row.
        int[] p = {1, 2, 3}, c = {0, 0, 0};
        int[] r = nextRow(p, c);
        if (r == p || r == c) throw new AssertionError("returned an input");
        r[0] = 99;
        if (p[0] != 1) throw new AssertionError("shared storage");
        // Random inputs against the oracle, and inputs must stay unchanged.
        Random rnd = new Random(2611);
        for (int t = 0; t < 3000; t++) {
            int w = 1 + rnd.nextInt(8);
            int[] prev = new int[w], cost = new int[w];
            for (int j = 0; j < w; j++) { prev[j] = rnd.nextInt(41) - 20; cost[j] = rnd.nextInt(41) - 20; }
            int[] pc = prev.clone(), cc = cost.clone();
            if (!Arrays.equals(nextRow(prev, cost), oracle(prev, cost))) throw new AssertionError("random " + t);
            if (!Arrays.equals(prev, pc) || !Arrays.equals(cost, cc)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Update One Row In Place (Author exercise)
<!-- id: dp-trans-inplace-row -->

**Approach.**
The array `row` starts as `[1, 0, ..., 0]`. In each turn, the loop visits columns from the last one down to column 0. Column `j` adds `row[j - 1]` to its own value, since the token either stayed in column `j` or arrived from column `j - 1`. After the sum, a blocked column is reset to 0. Column 0 keeps its value because nothing can arrive from the left.

The invariant is that, when the loop is at column `j`, every column below `j` still holds the previous turn's value, and every column above `j` already holds the new value. The read of `row[j - 1]` therefore sees an old value. The reset of a blocked column happens after the sum, and it affects no later read, because the next column to be written is `j - 1` and it reads `j - 2`. The ascending loop breaks this invariant, and the test shows that it returns different counts on the first example.

**Complexity.**
- **Time** is O(steps * w), because each turn visits every column once.
- **Space** is O(w) for the single array, with no extra array per turn.

```java run
import java.util.*;

public final class DpTransInplaceRow {
    /**
     * Counts token positions after the given number of turns using one array.
     * Time: O(steps * w). Space: O(w).
     * Invariant: while column j is processed, columns below j hold the previous turn and columns above j hold the new turn.
     */
    static long[] positions(int w, boolean[] blocked, int steps) {
        // One array holds the current layer, and the token starts in column 0.
        long[] row = new long[w];
        row[0] = 1;
        // Each turn rewrites the same array.
        for (int t = 0; t < steps; t++) {
            // Right to left, so row[j - 1] is still the previous turn when it is read.
            for (int j = w - 1; j >= 0; j--) {
                // A token arrives from the left neighbor or stays; column 0 has no left neighbor.
                if (j > 0) row[j] += row[j - 1];
                // A blocked column cannot hold a token at the end of the turn.
                if (blocked[j]) row[j] = 0;
            }
        }
        // The array now describes the layer after exactly steps turns.
        return row;
    }

    /** Wrong variant used only in the test: left to right reads values written in the same turn. */
    static long[] ascending(int w, int steps) {
        long[] row = new long[w];
        row[0] = 1;
        for (int t = 0; t < steps; t++) for (int j = 1; j < w; j++) row[j] += row[j - 1];
        return row;
    }

    /** Oracle: enumerate every sequence of stay/move choices and drop paths that end a turn in a blocked column. */
    static long[] oracle(int w, boolean[] blocked, int steps) {
        long[] out = new long[w];
        for (int mask = 0; mask < (1 << steps); mask++) {
            int col = 0;
            boolean ok = true;
            for (int t = 0; t < steps && ok; t++) {
                if ((mask >> t & 1) == 1) col++;
                if (col >= w || blocked[col]) ok = false;
            }
            if (ok) out[col]++;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(positions(4, new boolean[4], 3), new long[] {1, 3, 3, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(positions(4, new boolean[] {false, false, true, false}, 3), new long[] {1, 3, 0, 0})) throw new AssertionError("ex2");
        // The ascending loop gives a different, wrong answer on the first example.
        if (Arrays.equals(ascending(4, 3), new long[] {1, 3, 3, 1})) throw new AssertionError("ascending should fail");
        // Zero turns returns the start row, and width 1 never moves.
        if (!Arrays.equals(positions(3, new boolean[3], 0), new long[] {1, 0, 0})) throw new AssertionError("zero turns");
        if (!Arrays.equals(positions(1, new boolean[1], 5), new long[] {1})) throw new AssertionError("width one");
        // Maximum size: the largest count is a binomial coefficient below 2^60, so a long holds it.
        long[] big = positions(60, new boolean[60], 60);
        for (long v : big) if (v < 0) throw new AssertionError("overflow");
        // Random small cases against the oracle; a token must also stay inside the row.
        Random rnd = new Random(2612);
        for (int t = 0; t < 3000; t++) {
            int w = 1 + rnd.nextInt(6), steps = rnd.nextInt(9);
            boolean[] b = new boolean[w];
            for (int j = 0; j < w; j++) b[j] = rnd.nextInt(5) == 0;
            boolean[] copy = b.clone();
            // With steps = 0 no turn ends, so the oracle and the method both report the start row.
            if (!Arrays.equals(positions(w, b, steps), oracle(w, b, steps))) throw new AssertionError("random " + t);
            if (!Arrays.equals(b, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Boundary] Aliased Arrays (Author exercise)
<!-- id: dp-trans-aliased-rows -->

**Approach.**
The method creates the result `rows` with `steps + 1` entries. Row 0 is `start.clone()`, which gives a separate object with equal contents. For each turn `t`, the method allocates a new array, fills entry `j` by adding the previous row's entries at `j - 1`, `j` and `j + 1` that lie inside the row, and stores that array in `rows[t]`. The previous row is read from `rows[t - 1]` and never written.

The invariant is that every `rows[t]` is its own object, so a later turn cannot modify an earlier one. The aliased version keeps a single variable `cur`, stores it in every slot, and updates it in place. Then all slots refer to one array, and the result shows the final values in every row. The test below builds that version and asserts that all its slots are the same object.

**Complexity.**
- **Time** is O(steps * w), because each turn computes `w` sums of at most three terms.
- **Space** is O(steps * w) for the returned rows, since every layer is kept.

```java run
import java.util.*;

public final class DpTransAliasedRows {
    /**
     * Returns all rows from turn 0 to turn steps, each as a separate array.
     * Time: O(steps * w). Space: O(steps * w).
     * Invariant: rows[t] is a distinct object and is written only while it is being built.
     */
    static int[][] allRows(int[] start, int steps) {
        int w = start.length;
        // One slot per turn plus the start row.
        int[][] rows = new int[steps + 1][];
        // clone gives equal contents in a separate object, so the caller's array is never aliased.
        rows[0] = start.clone();
        for (int t = 1; t <= steps; t++) {
            // A new array per turn keeps the layers apart.
            int[] next = new int[w];
            for (int j = 0; j < w; j++) {
                // The center value always exists.
                int sum = rows[t - 1][j];
                // The left neighbor exists only for j > 0.
                if (j > 0) sum += rows[t - 1][j - 1];
                // The right neighbor exists only for j < w - 1.
                if (j < w - 1) sum += rows[t - 1][j + 1];
                next[j] = sum;
            }
            // Store the finished row; it is never written again.
            rows[t] = next;
        }
        return rows;
    }

    /** Wrong variant used only in the test: one array is stored in every slot. */
    static int[][] aliased(int[] start, int steps) {
        int[][] rows = new int[steps + 1][];
        int[] cur = start.clone();
        rows[0] = cur;
        for (int t = 1; t <= steps; t++) {
            int[] old = cur.clone();
            for (int j = 0; j < cur.length; j++) {
                cur[j] = old[j] + (j > 0 ? old[j - 1] : 0) + (j < cur.length - 1 ? old[j + 1] : 0);
            }
            rows[t] = cur;
        }
        return rows;
    }

    /** Oracle: repeated application of the turn to fresh copies, stored in a list. */
    static int[][] oracle(int[] start, int steps) {
        List<int[]> list = new ArrayList<>();
        int[] cur = Arrays.copyOf(start, start.length);
        list.add(cur);
        for (int t = 0; t < steps; t++) {
            int[] n = new int[cur.length];
            for (int j = 0; j < n.length; j++) {
                for (int d = -1; d <= 1; d++) if (j + d >= 0 && j + d < n.length) n[j] += cur[j + d];
            }
            list.add(n);
            cur = n;
        }
        return list.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(allRows(new int[] {1, 0, 0}, 2), new int[][] {{1, 0, 0}, {1, 1, 0}, {2, 2, 1}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(allRows(new int[] {5}, 3), new int[][] {{5}, {5}, {5}, {5}})) throw new AssertionError("ex2");
        // Java fact: assigning an array variable copies the reference, so the aliased version shares one object.
        int[][] bad = aliased(new int[] {1, 0, 0}, 2);
        if (bad[0] != bad[1] || bad[1] != bad[2]) throw new AssertionError("expected one shared object");
        if (Arrays.deepEquals(bad, new int[][] {{1, 0, 0}, {1, 1, 0}, {2, 2, 1}})) throw new AssertionError("aliasing should corrupt rows");
        // The correct version returns distinct objects, and none is the caller's array.
        int[] s = {1, 0, 0};
        int[][] good = allRows(s, 2);
        for (int i = 0; i < good.length; i++) {
            if (good[i] == s) throw new AssertionError("start aliased");
            for (int k = i + 1; k < good.length; k++) if (good[i] == good[k]) throw new AssertionError("rows share storage");
        }
        // Zero turns returns just the copy of the start row.
        if (allRows(s, 0).length != 1 || allRows(s, 0)[0] == s) throw new AssertionError("zero turns");
        // Random inputs against the oracle, and start must stay unchanged.
        Random rnd = new Random(2613);
        for (int t = 0; t < 3000; t++) {
            int w = 1 + rnd.nextInt(10), steps = rnd.nextInt(11);
            int[] st = new int[w];
            for (int j = 0; j < w; j++) st[j] = rnd.nextInt(201) - 100;
            int[] copy = st.clone();
            if (!Arrays.deepEquals(allRows(st, steps), oracle(st, steps))) throw new AssertionError("random " + t);
            if (!Arrays.equals(st, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Falling Path Sum (LeetCode 931)
<!-- id: dp-trans-falling-path -->

**Approach.**
The state is the smallest sum of a falling path that ends exactly at one cell. The method keeps two arrays, `prev` for the row above and `cur` for the row being computed. Row 0 copies the first matrix row into `prev`. For every later row, entry `c` of `cur` is the cell value plus the smallest of `prev[c - 1]`, `prev[c]` and `prev[c + 1]` that lie inside the row. After the row is finished, the two names swap roles. The answer is the smallest entry of the last `prev`.

The invariant is that `prev` holds the exact best sums for the row above and is never written while `cur` is built. The swap hands the older array to the next row, which overwrites each of its entries before any read, so stale values never matter. A single array would need the old value at both `c - 1` and `c + 1`. That requires a saved temporary, and the two arrays avoid the detail by owning the layers separately.

**Complexity.**
- **Time** is O(n^2), because each of the n rows computes n entries from at most three values.
- **Space** is O(n) for the two row arrays, and the matrix stays unchanged.

```java run
import java.util.*;

public final class DpTransFallingPath {
    /**
     * Returns the smallest sum over falling paths from the first row to the last row.
     * Time: O(n^2). Space: O(n).
     * Invariant: prev[c] is the smallest sum of a falling path ending exactly at column c of the row above.
     */
    static int minFallingPathSum(int[][] matrix) {
        int n = matrix.length;
        // Two rows of working storage, regardless of the number of matrix rows.
        int[] prev = matrix[0].clone(), cur = new int[n];
        // Rows 1 to n - 1 are computed one after another.
        for (int r = 1; r < n; r++) {
            for (int c = 0; c < n; c++) {
                // The cell straight above always exists.
                int best = prev[c];
                // The upper-left cell exists for c > 0.
                if (c > 0 && prev[c - 1] < best) best = prev[c - 1];
                // The upper-right cell exists for c < n - 1.
                if (c < n - 1 && prev[c + 1] < best) best = prev[c + 1];
                // Every entry of cur is written here before cur becomes the previous row.
                cur[c] = matrix[r][c] + best;
            }
            // Swap the roles; the old prev array will be fully overwritten on the next row.
            int[] tmp = prev;
            prev = cur;
            cur = tmp;
        }
        // The best path ends at the smallest entry of the last row.
        int ans = prev[0];
        for (int c = 1; c < n; c++) ans = Math.min(ans, prev[c]);
        return ans;
    }

    /** Oracle: depth-first search over every falling path. */
    static int oracle(int[][] m, int r, int c) {
        int n = m.length;
        if (r == n - 1) return m[r][c];
        int best = Integer.MAX_VALUE;
        for (int d = -1; d <= 1; d++) if (c + d >= 0 && c + d < n) best = Math.min(best, oracle(m, r + 1, c + d));
        return m[r][c] + best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minFallingPathSum(new int[][] {{5, -2, 4}, {3, 8, -1}, {2, 6, 7}}) != 3) throw new AssertionError("ex1");
        if (minFallingPathSum(new int[][] {{4, -9}, {7, 1}}) != -8) throw new AssertionError("ex2");
        // A single cell and a matrix of all equal values.
        if (minFallingPathSum(new int[][] {{-7}}) != -7) throw new AssertionError("one cell");
        if (minFallingPathSum(new int[][] {{2, 2}, {2, 2}}) != 4) throw new AssertionError("equal");
        // Random matrices against the oracle; the matrix must stay unchanged.
        Random rnd = new Random(2614);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] m = new int[n][n];
            for (int[] row : m) for (int c = 0; c < n; c++) row[c] = rnd.nextInt(201) - 100;
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = m[i].clone();
            int want = Integer.MAX_VALUE;
            for (int c = 0; c < n; c++) want = Math.min(want, oracle(m, 0, c));
            if (minFallingPathSum(m) != want) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(m, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```
