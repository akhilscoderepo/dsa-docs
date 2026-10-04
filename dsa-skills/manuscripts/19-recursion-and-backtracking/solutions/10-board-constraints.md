<!-- solutions-for: 10-board-constraints -->
### Board Constraints

#### Solution: [Build] Four-Direction Path (Author exercise)
<!-- id: bt-grid-paths -->

**Approach.** A call at an open cell that is the bottom-right corner counts one route. Otherwise it marks its cell in a shared `boolean[][]`, tries the four neighbours that are inside the grid, open and unmarked, and clears the mark when all four are done, whatever they returned. The marks therefore describe exactly the route being walked, and the harness checks that every mark is clear when the search ends. The oracle uses a different marker: an integer bit set of used cells passed by value, so it shares no mutable state with the solution. Random grids of up to four by four cells with random blocked cells are compared.

**Complexity.** The number of simple routes on a four by four grid is in the hundreds of thousands at most, and each step costs O(1), with a stack as deep as the number of cells.

```java run
import java.util.Random;

public final class GridPaths {
    static final int[][] DIRS = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

    static long count(String[] g, int r, int c, boolean[][] marked) {
        int rows = g.length, cols = g[0].length();
        if (r == rows - 1 && c == cols - 1) return 1;
        marked[r][c] = true;
        long total = 0;
        for (int[] d : DIRS) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
            if (g[nr].charAt(nc) == '#' || marked[nr][nc]) continue;
            total += count(g, nr, nc, marked);
        }
        marked[r][c] = false;
        return total;
    }

    static long routes(String[] g, boolean[][] marked) {
        if (g[0].charAt(0) == '#' || g[g.length - 1].charAt(g[0].length() - 1) == '#') return 0;
        return count(g, 0, 0, marked);
    }

    static long oracle(String[] g, int r, int c, int used) {
        int rows = g.length, cols = g[0].length();
        if (r == rows - 1 && c == cols - 1) return 1;
        long total = 0;
        int here = used | (1 << (r * cols + c));
        for (int[] d : DIRS) {
            int nr = r + d[0], nc = c + d[1];
            if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
            if (g[nr].charAt(nc) == '#' || (here >> (nr * cols + nc) & 1) == 1) continue;
            total += oracle(g, nr, nc, here);
        }
        return total;
    }

    public static void main(String[] args) {
        if (routes(new String[] {"...", "...", "..."}, new boolean[3][3]) != 12) throw new AssertionError("example 1");
        if (routes(new String[] {"...", ".#.", "..."}, new boolean[3][3]) != 2) throw new AssertionError("example 2");
        if (routes(new String[] {"#."}, new boolean[1][2]) != 0) throw new AssertionError("blocked start");
        if (routes(new String[] {"."}, new boolean[1][1]) != 1) throw new AssertionError("single cell");
        Random rnd = new Random(191001);
        for (int t = 0; t < 1500; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            String[] g = new String[rows];
            for (int i = 0; i < rows; i++) {
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < cols; j++) sb.append(rnd.nextInt(5) == 0 ? '#' : '.');
                g[i] = sb.toString();
            }
            boolean[][] marked = new boolean[rows][cols];
            long got = routes(g, marked);
            for (boolean[] row : marked) for (boolean m : row) if (m) throw new AssertionError("a mark leaked");
            long want = (g[0].charAt(0) == '#' || g[rows - 1].charAt(cols - 1) == '#') ? 0 : oracle(g, 0, 0, 0);
            if (got != want) throw new AssertionError("differs on " + String.join("|", g));
        }
    }
}
```

#### Solution: [Vary] Word Search (LeetCode 79)
<!-- id: bt-word-search -->

**Approach.** The search checks bounds and the letter, with the in-place marker `#` failing the letter test automatically, then marks, explores the four neighbours with short-circuit `||`, stores the outcome in `found`, restores the saved letter and only then returns. The harness checks that the grid is unchanged after every search, successful or not, and shows that `char[][].clone()` is shallow, since its first row is the very same array object. The oracle is the copy-per-step method of the naive stage, which keeps a fresh flag grid for every step and never mutates the board, and the two are compared on random grids over a three-letter alphabet.

**Complexity.** At most R * C starts, each with up to 3^(L - 1) routes of constant work per step, and a stack of L frames.

```java run
import java.util.Arrays;
import java.util.Random;

public final class WordSearch {
    static boolean exists(char[][] board, String word) {
        for (int r = 0; r < board.length; r++)
            for (int c = 0; c < board[0].length; c++)
                if (search(board, word, r, c, 0)) return true;
        return false;
    }

    static boolean search(char[][] b, String w, int r, int c, int k) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;
        if (b[r][c] != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        char saved = b[r][c];
        b[r][c] = '#';
        boolean found = search(b, w, r + 1, c, k + 1) || search(b, w, r - 1, c, k + 1)
                     || search(b, w, r, c + 1, k + 1) || search(b, w, r, c - 1, k + 1);
        b[r][c] = saved;
        return found;
    }

    static boolean viaCopies(String[] stones, String word) {
        int rows = stones.length, cols = stones[0].length();
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++)
                if (walk(stones, word, r, c, 0, new boolean[rows][cols])) return true;
        return false;
    }

    static boolean walk(String[] stones, String word, int r, int c, int k, boolean[][] used) {
        if (r < 0 || c < 0 || r >= stones.length || c >= stones[0].length()) return false;
        if (used[r][c] || stones[r].charAt(c) != word.charAt(k)) return false;
        if (k == word.length() - 1) return true;
        boolean[][] next = new boolean[used.length][];
        for (int i = 0; i < used.length; i++) next[i] = used[i].clone();
        next[r][c] = true;
        int[][] steps = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] s : steps) if (walk(stones, word, r + s[0], c + s[1], k + 1, next)) return true;
        return false;
    }

    static char[][] grid(String[] rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    public static void main(String[] args) {
        if (!exists(grid(new String[] {"cat", "oxe", "dgs"}), "cod")) throw new AssertionError("example 1");
        if (exists(grid(new String[] {"aa"}), "aaa")) throw new AssertionError("example 2");
        char[][] probe = grid(new String[] {"ab", "cd"});
        if (probe.clone()[0] != probe[0]) throw new AssertionError("a clone of a 2D array shares its rows");
        Random rnd = new Random(191002);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            String[] g = new String[rows];
            for (int i = 0; i < rows; i++) {
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < cols; j++) sb.append((char) ('a' + rnd.nextInt(3)));
                g[i] = sb.toString();
            }
            StringBuilder wb = new StringBuilder();
            int len = 1 + rnd.nextInt(7);
            for (int i = 0; i < len; i++) wb.append((char) ('a' + rnd.nextInt(3)));
            String word = wb.toString();
            char[][] board = grid(g);
            boolean got = exists(board, word);
            if (!Arrays.deepEquals(board, grid(g))) throw new AssertionError("the board must be unchanged");
            if (got != viaCopies(g, word)) throw new AssertionError("differs on " + String.join("|", g) + " " + word);
        }
    }
}
```

#### Solution: [Boundary] Cell Reuse And Early Success (Author exercise)
<!-- id: bt-reuse-early-success -->

**Approach.** One `char[][]` serves every start cell, so the search must leave it untouched. The call saves its letter, marks the cell, stores the result of the four explorations in `found`, restores the letter and then returns `found`, so success and failure take the same exit. The harness runs a careless version whose success branch returns before the restore and asserts that on the first example it misses a start cell, because a later search finds a hash where it needs a letter. It also asserts after each real run that the grid equals a pristine copy. The oracle gives every start cell its own fresh copy of the grid and never shares a mutation between starts.

**Complexity.** For each start cell the cost is that of one word search, so R * C searches in all, and the stack holds at most one frame per letter.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ReuseEarlySuccess {
    static boolean search(char[][] b, String w, int r, int c, int k, boolean careless) {
        if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;
        if (b[r][c] != w.charAt(k)) return false;
        if (k == w.length() - 1) return true;
        char saved = b[r][c];
        b[r][c] = '#';
        boolean found = false;
        int[][] steps = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] s : steps) {
            if (search(b, w, r + s[0], c + s[1], k + 1, careless)) {
                found = true;
                if (careless) return true;
                break;
            }
        }
        b[r][c] = saved;
        return found;
    }

    static List<List<Integer>> starts(char[][] b, String w, boolean careless) {
        List<List<Integer>> out = new ArrayList<>();
        for (int r = 0; r < b.length; r++)
            for (int c = 0; c < b[0].length; c++)
                if (search(b, w, r, c, 0, careless)) out.add(List.of(r, c));
        return out;
    }

    static char[][] grid(String[] rows) {
        char[][] g = new char[rows.length][];
        for (int i = 0; i < rows.length; i++) g[i] = rows[i].toCharArray();
        return g;
    }

    static List<List<Integer>> oracle(String[] rows, String w) {
        List<List<Integer>> out = new ArrayList<>();
        for (int r = 0; r < rows.length; r++)
            for (int c = 0; c < rows[0].length(); c++)
                if (search(grid(rows), w, r, c, 0, false)) out.add(List.of(r, c));
        return out;
    }

    public static void main(String[] args) {
        String[] one = {"aaa", "bba"};
        if (!starts(grid(one), "bba", false).equals(List.of(List.of(1, 0), List.of(1, 1)))) throw new AssertionError("example 1");
        if (!starts(grid(new String[] {"ab"}), "ba", false).equals(List.of(List.of(0, 1)))) throw new AssertionError("example 2");
        if (!starts(grid(new String[] {"a"}), "aa", false).isEmpty()) throw new AssertionError("one cell cannot spell two letters");
        if (starts(grid(one), "bba", true).equals(starts(grid(one), "bba", false))) throw new AssertionError("early success without restoring must lose a start");
        Random rnd = new Random(191003);
        for (int t = 0; t < 4000; t++) {
            int rows = 1 + rnd.nextInt(4), cols = 1 + rnd.nextInt(4);
            String[] g = new String[rows];
            for (int i = 0; i < rows; i++) {
                StringBuilder sb = new StringBuilder();
                for (int j = 0; j < cols; j++) sb.append((char) ('a' + rnd.nextInt(2)));
                g[i] = sb.toString();
            }
            StringBuilder wb = new StringBuilder();
            int len = 1 + rnd.nextInt(6);
            for (int i = 0; i < len; i++) wb.append((char) ('a' + rnd.nextInt(2)));
            String word = wb.toString();
            char[][] board = grid(g);
            List<List<Integer>> got = starts(board, word, false);
            if (!Arrays.deepEquals(board, grid(g))) throw new AssertionError("the board must be unchanged");
            if (!got.equals(oracle(g, word))) throw new AssertionError("differs on " + String.join("|", g) + " " + word);
        }
    }
}
```

#### Solution: [Recognize] N-Queens (LeetCode 51)
<!-- id: bt-queens-boards -->

**Approach.** Each call fills one row. The three occupancy sets are `int` bit sets for columns, for diagonals indexed by `row + col`, and for diagonals indexed by `row - col + n - 1`, and they are passed to the next call with the new bits added, so the caller's sets are untouched and need no restore. Only the array that records each row's column is shared, and each call simply overwrites its own entry, so entries from deeper rows are stale but never read. A board is built into fresh strings when the last row is filled, which is the copy that protects the result. The oracle goes through all permutations of the columns in lexicographic order and keeps the ones with no two queens on a diagonal, which is the same order as the search. Known solution counts for boards 1 to 9 are asserted as well.

**Complexity.** Exponential in n, though the three sets cut the tree to a small fraction of n^n, and the stack holds n frames.

```java run
import java.util.ArrayList;
import java.util.List;

public final class QueensBoards {
    static void place(int n, int row, int cols, int d1, int d2, int[] at, List<List<String>> out) {
        if (row == n) {
            List<String> board = new ArrayList<>();
            for (int r = 0; r < n; r++) {
                char[] line = new char[n];
                java.util.Arrays.fill(line, '.');
                line[at[r]] = 'Q';
                board.add(new String(line));
            }
            out.add(board);
            return;
        }
        for (int c = 0; c < n; c++) {
            int a = 1 << c, b = 1 << (row + c), d = 1 << (row - c + n - 1);
            if ((cols & a) != 0 || (d1 & b) != 0 || (d2 & d) != 0) continue;
            at[row] = c;
            place(n, row + 1, cols | a, d1 | b, d2 | d, at, out);
        }
    }

    static List<List<String>> solve(int n) {
        List<List<String>> out = new ArrayList<>();
        place(n, 0, 0, 0, 0, new int[n], out);
        return out;
    }

    static boolean nextPermutation(int[] p) {
        int i = p.length - 2;
        while (i >= 0 && p[i] >= p[i + 1]) i--;
        if (i < 0) return false;
        int j = p.length - 1;
        while (p[j] <= p[i]) j--;
        int t = p[i]; p[i] = p[j]; p[j] = t;
        for (int a = i + 1, b = p.length - 1; a < b; a++, b--) { t = p[a]; p[a] = p[b]; p[b] = t; }
        return true;
    }

    static List<List<String>> oracle(int n) {
        List<List<String>> out = new ArrayList<>();
        int[] p = new int[n];
        for (int i = 0; i < n; i++) p[i] = i;
        do {
            boolean ok = true;
            for (int a = 0; a < n && ok; a++) for (int b = a + 1; b < n; b++) if (Math.abs(p[a] - p[b]) == b - a) { ok = false; break; }
            if (!ok) continue;
            List<String> board = new ArrayList<>();
            for (int r = 0; r < n; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < n; c++) sb.append(c == p[r] ? 'Q' : '.');
                board.add(sb.toString());
            }
            out.add(board);
        } while (nextPermutation(p));
        return out;
    }

    public static void main(String[] args) {
        List<List<String>> four = List.of(List.of(".Q..", "...Q", "Q...", "..Q."), List.of("..Q.", "Q...", "...Q", ".Q.."));
        if (!solve(4).equals(four)) throw new AssertionError("example 1");
        if (!solve(1).equals(List.of(List.of("Q")))) throw new AssertionError("example 2");
        int[] known = {1, 0, 0, 2, 10, 4, 40, 92, 352};
        for (int n = 1; n <= 9; n++) {
            List<List<String>> got = solve(n);
            if (got.size() != known[n - 1]) throw new AssertionError("known count at n=" + n);
            if (!got.equals(oracle(n))) throw new AssertionError("differs at n=" + n);
        }
    }
}
```
