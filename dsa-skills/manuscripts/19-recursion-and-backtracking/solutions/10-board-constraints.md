<!-- solutions-for: 10-board-constraints -->
### Solutions For Marking Cells On A Grid

#### Solution: [Build] Four-Direction Path (Author exercise)
<!-- id: bt-four-direction-path -->

**Approach.**
A call returns 0 when its cell lies outside the grid, is blocked or carries a path mark. Reaching the bottom-right cell counts one path, and the call still unmarks nothing there because it never marked the cell. For any other cell, the call sets the mark, adds the counts of the four neighbours and clears the mark, so every sibling branch starts from the same marks. The call does not stop after a success, since the exercise counts every path. A blocked start or a blocked end gives 0 through the same checks.

**Complexity.**
- **Time** is O(4 * 3^(R*C - 1)) in the worst case, because each of the R * C cells can start at most three further moves along a path.
- **Space** is O(R * C) for the marks and the stack.

```java run
import java.util.*;

public final class FourDirectionPath {
    /**
     * Counts the simple paths from the top-left to the bottom-right cell through open cells.
     * Time: O(3^(R*C)) worst case. Space: O(R*C).
     * Invariant: the marks are true exactly for the cells of the calls on the stack.
     */
    static int paths(String[] g) {
        boolean[][] on = new boolean[g.length][g[0].length()];
        return go(g, 0, 0, on);
    }

    private static int go(String[] g, int r, int c, boolean[][] on) {
        if (r < 0 || c < 0 || r >= g.length || c >= g[0].length()) return 0;   // outside the grid
        if (g[r].charAt(c) == '#' || on[r][c]) return 0;                      // blocked or already on the path
        if (r == g.length - 1 && c == g[0].length() - 1) return 1;            // the end cell completes one path
        on[r][c] = true;                                                      // choose: mark the cell
        int total = go(g, r - 1, c, on) + go(g, r + 1, c, on) + go(g, r, c - 1, on) + go(g, r, c + 1, on);
        on[r][c] = false;                                                     // undo: clear the mark
        return total;
    }

    /** Oracle: bitmask dynamic programming over (set of visited cells, last cell). */
    static long oracle(String[] g) {
        int R = g.length, C = g[0].length(), n = R * C;
        if (g[0].charAt(0) == '#' || g[R - 1].charAt(C - 1) == '#') return 0;
        if (n == 1) return 1;
        long[][] f = new long[1 << n][n];
        f[1][0] = 1; long total = 0;
        for (int mask = 1; mask < (1 << n); mask++) for (int cell = 0; cell < n; cell++) {
            long ways = f[mask][cell]; if (ways == 0) continue;
            if (cell == n - 1) { total += ways; continue; }       // a path ends when it reaches the last cell
            int r = cell / C, c = cell % C;
            int[][] d = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
            for (int[] m : d) {
                int nr = r + m[0], nc = c + m[1];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || g[nr].charAt(nc) == '#') continue;
                int nx = nr * C + nc;
                if ((mask >> nx & 1) == 0) f[mask | 1 << nx][nx] += ways;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (paths(new String[] {"..", ".."}) != 2) throw new AssertionError("ex1");
        if (paths(new String[] {"...", ".#.", "..."}) != 2) throw new AssertionError("ex2");
        if (paths(new String[] {"."}) != 1) throw new AssertionError("one cell");
        if (paths(new String[] {"#."}) != 0) throw new AssertionError("blocked start");
        // Known counts of corner-to-corner paths on open grids.
        if (paths(new String[] {"...", "...", "..."}) != 12) throw new AssertionError("3x3");
        if (paths(new String[] {"....", "....", "....", "...."}) != 184) throw new AssertionError("4x4");
        if (paths(new String[] {".....", ".....", ".....", ".....", "....."}) != 8512) throw new AssertionError("5x5");
        // Random grids up to 4 by 4 must match the bitmask oracle.
        Random rnd = new Random(2001);
        for (int t = 0; t < 200; t++) {
            int R = 1 + rnd.nextInt(4), C = 1 + rnd.nextInt(4);
            String[] g = new String[R];
            for (int i = 0; i < R; i++) { StringBuilder sb = new StringBuilder(); for (int j = 0; j < C; j++) sb.append(rnd.nextInt(5) == 0 ? '#' : '.'); g[i] = sb.toString(); }
            if (paths(g) != oracle(g)) throw new AssertionError("random " + t + " " + Arrays.toString(g));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Word Search (LeetCode 79)
<!-- id: bt-word-search-marks -->

**Approach.**
Every cell may start the word, so the method tries each cell as a start. A call rejects a cell outside the board, a cell with a path mark and a cell whose letter differs from the letter at index `k`. The last letter returns true at once. Otherwise the call sets the mark, tries the four neighbours with `||`, stores the result in a local variable, clears the mark and then returns the variable. The operator `||` stops at the first success, and the unmark step still runs because it comes after the expression. The board is never written, so the caller's letters stay unchanged.

**Complexity.**
- **Time** is O(R * C * 3^L) in the worst case, because each start makes at most 4 * 3^(L-1) calls.
- **Space** is O(R * C) for the marks plus O(L) for the stack.

```java run
import java.util.*;

public final class WordSearchMarks {
    /**
     * Returns true when the word can be spelled by a path of touching cells without reusing a cell.
     * Time: O(R * C * 3^L). Space: O(R * C + L).
     * Invariant: on[r][c] is true exactly for the cells of the calls on the stack.
     */
    static boolean exists(char[][] b, String w) {
        boolean[][] on = new boolean[b.length][b[0].length];
        for (int r = 0; r < b.length; r++)
            for (int c = 0; c < b[0].length; c++)
                if (go(b, w, r, c, 0, on)) return true;     // every cell may start the word
        return false;
    }

    private static boolean go(char[][] b, String w, int r, int c, int k, boolean[][] on) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;   // outside the board
        if (on[r][c] || b[r][c] != w.charAt(k)) return false;                    // cell in use or wrong letter
        if (k == w.length() - 1) return true;                                    // the last letter matches
        on[r][c] = true;                                                         // choose: mark the cell
        boolean found = go(b, w, r - 1, c, k + 1, on) || go(b, w, r + 1, c, k + 1, on)
                     || go(b, w, r, c - 1, k + 1, on) || go(b, w, r, c + 1, k + 1, on);
        on[r][c] = false;                                                        // undo before returning
        return found;
    }

    /** Oracle: breadth-first search over (last cell, set of used cells) states, one level for each letter. */
    static boolean oracle(char[][] b, String w) {
        int R = b.length, C = b[0].length;
        Set<Long> level = new HashSet<>();
        for (int r = 0; r < R; r++) for (int c = 0; c < C; c++) if (b[r][c] == w.charAt(0)) level.add(((long) (1 << (r * C + c))) << 8 | (r * C + c));
        for (int k = 1; k < w.length() && !level.isEmpty(); k++) {
            Set<Long> next = new HashSet<>();
            for (long s : level) {
                int cell = (int) (s & 255), mask = (int) (s >> 8), r = cell / C, c = cell % C;
                int[][] d = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
                for (int[] m : d) {
                    int nr = r + m[0], nc = c + m[1];
                    if (nr < 0 || nc < 0 || nr >= R || nc >= C || b[nr][nc] != w.charAt(k)) continue;
                    int nx = nr * C + nc;
                    if ((mask >> nx & 1) == 0) next.add(((long) (mask | 1 << nx)) << 8 | nx);
                }
            }
            level = next;
        }
        return !level.isEmpty();
    }

    static int counter;
    static boolean hit() { counter++; return true; }

    public static void main(String[] args) {
        // The two examples of the exercise.
        char[][] b = {{'a', 'b'}, {'c', 'd'}};
        if (!exists(b, "abdc")) throw new AssertionError("ex1");
        if (exists(b, "abcd")) throw new AssertionError("ex2");
        // The motivating board: the word aaa exists on aa/ab.
        if (!exists(new char[][] {{'a', 'a'}, {'a', 'b'}}, "aaa")) throw new AssertionError("aaa");
        // The Java claim: || skips its right operand once the left operand is true.
        counter = 0; boolean x = hit() || hit();
        if (!x || counter != 1) throw new AssertionError("short circuit");
        // Random boards up to 3 by 4 must match the state-set oracle, and the board must stay unchanged.
        Random rnd = new Random(2002);
        for (int t = 0; t < 400; t++) {
            int R = 1 + rnd.nextInt(3), C = 1 + rnd.nextInt(4);
            char[][] bd = new char[R][C];
            for (char[] row : bd) for (int j = 0; j < C; j++) row[j] = (char) ('a' + rnd.nextInt(2));
            char[][] copy = new char[R][]; for (int i = 0; i < R; i++) copy[i] = bd[i].clone();
            StringBuilder sb = new StringBuilder();
            for (int i = 0, len = 1 + rnd.nextInt(7); i < len; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            if (exists(bd, sb.toString()) != oracle(bd, sb.toString())) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(bd, copy)) throw new AssertionError("mutation " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Cell Reuse And Early Success (Author exercise)
<!-- id: bt-cell-reuse-early-success -->

**Approach.**
The call saves the letter of its cell in a local variable, then overwrites the cell with `#`. A cell holding `#` fails the letter test, because `#` never occurs in a word, so the overwrite acts as the path mark and also forbids reuse. After the four neighbours, the call writes the saved letter back and returns the stored result. The restore sits before the return, so an early success restores the board as well as a failure does. The last letter returns true before any write. The caller therefore finds every letter of the board where it left it, in both outcomes.

**Complexity.**
- **Time** is O(R * C * 3^L) in the worst case.
- **Space** is O(L) for the stack, and the marks need no extra grid.

```java run
import java.util.*;

public final class CellReuseEarlySuccess {
    /**
     * Returns true when the word appears on the board, marking cells in place with '#'.
     * Time: O(R * C * 3^L). Space: O(L).
     * Invariant: on exit of every call, each cell holds the letter that it held on entry.
     */
    static boolean exists(char[][] b, String w) {
        for (int r = 0; r < b.length; r++)
            for (int c = 0; c < b[0].length; c++)
                if (go(b, w, r, c, 0)) return true;
        return false;
    }

    private static boolean go(char[][] b, String w, int r, int c, int k) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;   // outside the board
        if (b[r][c] != w.charAt(k)) return false;                                // wrong letter, or a cell marked '#'
        if (k == w.length() - 1) return true;                                    // the last letter needs no mark
        char saved = b[r][c];                                                    // remember the letter
        b[r][c] = '#';                                                           // choose: mark the cell in place
        boolean found = go(b, w, r - 1, c, k + 1) || go(b, w, r + 1, c, k + 1)
                     || go(b, w, r, c - 1, k + 1) || go(b, w, r, c + 1, k + 1);
        b[r][c] = saved;                                                         // undo: restore before every return
        return found;
    }

    static char[][] copy(char[][] b) { char[][] out = new char[b.length][]; for (int i = 0; i < b.length; i++) out[i] = b[i].clone(); return out; }

    /** Oracle: the same search with a separate boolean grid, which never writes to the board. */
    static boolean oracle(char[][] b, String w) {
        boolean[][] on = new boolean[b.length][b[0].length];
        for (int r = 0; r < b.length; r++) for (int c = 0; c < b[0].length; c++) if (side(b, w, r, c, 0, on)) return true;
        return false;
    }

    private static boolean side(char[][] b, String w, int r, int c, int k, boolean[][] on) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length || on[r][c] || b[r][c] != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        on[r][c] = true;
        boolean f = side(b, w, r - 1, c, k + 1, on) || side(b, w, r + 1, c, k + 1, on) || side(b, w, r, c - 1, k + 1, on) || side(b, w, r, c + 1, k + 1, on);
        on[r][c] = false;
        return f;
    }

    public static void main(String[] args) {
        // The two examples of the exercise, with the board checked after each call.
        char[][] a = {{'a', 'a'}};
        if (exists(a, "aaa")) throw new AssertionError("ex1 result");
        if (!Arrays.deepEquals(a, new char[][] {{'a', 'a'}})) throw new AssertionError("ex1 board");
        char[][] b = {{'a', 'b'}};
        if (!exists(b, "ba")) throw new AssertionError("ex2 result");
        if (!Arrays.deepEquals(b, new char[][] {{'a', 'b'}})) throw new AssertionError("ex2 board");
        // Random boards must match the oracle, and the board must be restored after success and after failure.
        Random rnd = new Random(2003);
        int successes = 0, failures = 0;
        for (int t = 0; t < 600; t++) {
            int R = 1 + rnd.nextInt(4), C = 1 + rnd.nextInt(4);
            char[][] bd = new char[R][C];
            for (char[] row : bd) for (int j = 0; j < C; j++) row[j] = (char) ('a' + rnd.nextInt(2));
            char[][] before = copy(bd);
            StringBuilder sb = new StringBuilder();
            for (int i = 0, len = 1 + rnd.nextInt(8); i < len; i++) sb.append((char) ('a' + rnd.nextInt(2)));
            boolean got = exists(bd, sb.toString());
            if (got != oracle(before, sb.toString())) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(bd, before)) throw new AssertionError("board damaged " + t);
            if (got) successes++; else failures++;
        }
        if (successes == 0 || failures == 0) throw new AssertionError("the test needs both outcomes");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] N-Queens (LeetCode 51)
<!-- id: bt-n-queens-boards -->

**Approach.**
The call at row `r` places one queen in row `r`, so no two queens share a row. Two cells share a column when their columns are equal, and they share a diagonal when `r - c` or `r + c` is equal. The search keeps three boolean arrays for these keys and an array `cols` that holds the chosen column of each row. A call tries the columns from left to right and skips a column whose marks are set. For a free column, it sets the three marks, stores the column and explores the next row. Then it clears the same marks. At row `n`, the call builds one board from `cols` and stores it. The board strings are new objects, so later marks cannot change them.

**Complexity.**
- **Time** is O(n!) in the worst case, plus O(n^2) for each of the stored boards.
- **Space** is O(n) for the marks and the stack, plus the output.

```java run
import java.util.*;

public final class NQueensBoards {
    /**
     * Returns every placement of n non-attacking queens as board strings, rows top to bottom and columns left to right.
     * Time: O(n!) worst case. Space: O(n) besides the output.
     * Invariant: the marks are true exactly for the columns and diagonals of the queens in the rows above r.
     */
    static List<List<String>> solve(int n) {
        List<List<String>> out = new ArrayList<>();
        go(0, n, new int[n], new boolean[n], new boolean[2 * n - 1], new boolean[2 * n - 1], out);
        return out;
    }

    private static void go(int r, int n, int[] cols, boolean[] col, boolean[] diff, boolean[] sum, List<List<String>> out) {
        if (r == n) {                                        // every row holds a queen: build the board
            List<String> board = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                char[] row = new char[n]; Arrays.fill(row, '.');
                row[cols[i]] = 'Q';
                board.add(new String(row));
            }
            out.add(board);
            return;
        }
        for (int c = 0; c < n; c++) {
            int d = r - c + n - 1, s = r + c;                // the indices of the two diagonals
            if (col[c] || diff[d] || sum[s]) continue;       // an earlier queen attacks this cell
            col[c] = diff[d] = sum[s] = true; cols[r] = c;   // choose: set the marks and record the column
            go(r + 1, n, cols, col, diff, sum, out);         // explore the next row
            col[c] = diff[d] = sum[s] = false;               // undo: clear the same three marks
        }
    }

    /** Oracle: permutations of the columns in lexicographic order, filtered by pairwise diagonal tests. */
    static List<List<String>> oracle(int n) {
        List<List<String>> out = new ArrayList<>();
        int[] p = new int[n]; for (int i = 0; i < n; i++) p[i] = i;
        do {
            boolean ok = true;
            for (int i = 0; i < n && ok; i++) for (int j = i + 1; j < n; j++) if (Math.abs(p[i] - p[j]) == j - i) { ok = false; break; }
            if (ok) {
                List<String> board = new ArrayList<>();
                for (int i = 0; i < n; i++) { char[] row = new char[n]; Arrays.fill(row, '.'); row[p[i]] = 'Q'; board.add(new String(row)); }
                out.add(board);
            }
        } while (next(p));
        return out;
    }

    private static boolean next(int[] p) {                   // the next lexicographic permutation, false after the last
        int i = p.length - 2;
        while (i >= 0 && p[i] >= p[i + 1]) i--;
        if (i < 0) return false;
        int j = p.length - 1;
        while (p[j] <= p[i]) j--;
        int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int a = i + 1, b = p.length - 1; a < b; a++, b--) { t = p[a]; p[a] = p[b]; p[b] = t; }
        return true;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!solve(4).equals(List.of(List.of(".Q..", "...Q", "Q...", "..Q."), List.of("..Q.", "Q...", "...Q", ".Q..")))) throw new AssertionError("ex1");
        if (!solve(1).equals(List.of(List.of("Q")))) throw new AssertionError("ex2");
        if (!solve(2).isEmpty() || !solve(3).isEmpty()) throw new AssertionError("no solutions for 2 and 3");
        // Every size up to 8 must match the permutation oracle in the same order, and n = 8 has 92 boards.
        for (int n = 1; n <= 8; n++) if (!solve(n).equals(oracle(n))) throw new AssertionError("oracle " + n);
        if (solve(8).size() != 92) throw new AssertionError("count 8");
        System.out.println("ok");
    }
}
```
