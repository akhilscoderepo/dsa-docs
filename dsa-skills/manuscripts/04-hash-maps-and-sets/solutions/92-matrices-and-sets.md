<!-- solutions-for: 04-hash-maps-and-sets -->
### Solutions For Matrices And Sets

#### Solution: [Build] Row Duplicates (Author exercise)
<!-- id: hm-row-duplicates -->

**Approach.**
One set holds the digits of the row read so far. For each position, the method skips `'.'`, then calls `add` on the digit. A result of false means that an earlier position holds the same digit, so the method returns the current index. The invariant is that after position `i`, the set holds exactly the distinct digits among `row[0..i]`. A row without repeats runs to the end and returns -1.

**Complexity.**
- **Time** is O(1) for the fixed length 9, and O(n) in general, because each position makes one `add` of expected constant time.
- **Space** is O(1) for the fixed length, and O(n) in general, since the set holds at most one entry for each position.

```java run
import java.util.*;

public final class RowDuplicates {
    /**
     * Returns the index of the first digit that repeats an earlier digit, or -1.
     * Time: O(n) expected. Space: O(n).
     * Invariant: after position i, seen holds the distinct digits of row[0..i].
     */
    static int firstRepeat(String row) {
        Set<Character> seen = new HashSet<>();
        // One iteration per cell of the row.
        for (int i = 0; i < row.length(); i++) {
            char d = row.charAt(i);
            // An empty cell is never a digit, so it stays out of the set.
            if (d == '.') continue;
            // add returns false when an earlier cell holds the same digit.
            if (!seen.add(d)) {
                return i;
            }
        }
        return -1;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (firstRepeat("4.2.1.4..") != 6) throw new AssertionError("example 1");
        if (firstRepeat("123456789") != -1) throw new AssertionError("example 2");
        // Empty cells are never repeats.
        if (firstRepeat(".........") != -1) throw new AssertionError("all empty");
        // The first repeat is reported, not the last.
        if (firstRepeat("11.22....") != 1) throw new AssertionError("first of several");
        // Random rows are checked against a quadratic oracle.
        Random rnd = new Random(71);
        for (int t = 0; t < 800; t++) {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < 9; i++) sb.append(rnd.nextInt(3) == 0 ? '.' : (char) ('1' + rnd.nextInt(9)));
            String row = sb.toString();
            int expect = -1;
            for (int i = 0; i < 9 && expect < 0; i++)
                for (int j = 0; j < i; j++)
                    if (row.charAt(i) != '.' && row.charAt(i) == row.charAt(j)) { expect = i; break; }
            if (firstRepeat(row) != expect) throw new AssertionError(row);
        }
    }
}
```

#### Solution: [Vary] Row And Column Scope (Author exercise)
<!-- id: hm-row-column-scope -->

**Approach.**
A cell belongs to two scopes, so the method keeps one set for each row and one for each column. For the digit `d` at `(r, c)`, it tests `rows[r]` and `cols[c]`. If either holds `d`, the method returns false. Otherwise it adds `d` to both. The same digit may appear in different rows and in different columns, because those sets are separate. The invariant is that after the cells before `(r, c)` in row-major order, each set holds the digits of its scope among those cells.

**Complexity.**
- **Time** is O(n^2) on average for side n, because each cell makes at most two set operations.
- **Space** is O(n^2), because the 2n sets hold at most one entry for each filled cell and scope.

```java run
import java.util.*;

public final class RowColumnScope {
    /**
     * Reports whether no digit repeats in any row or column.
     * Time: O(n^2) expected. Space: O(n^2).
     * Invariant: rows[r] and cols[c] hold the digits of their scope among the cells read so far.
     */
    static boolean rowsAndColumnsUnique(String[] board) {
        int n = board.length;
        List<Set<Character>> rows = new ArrayList<>(), cols = new ArrayList<>();
        for (int k = 0; k < n; k++) { rows.add(new HashSet<>()); cols.add(new HashSet<>()); }
        // Row-major scan of every cell.
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                // Both tests must pass; the same digit in other scopes is allowed.
                if (!rows.get(r).add(d) || !cols.get(c).add(d)) {
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples and a one-cell board.
        if (!rowsAndColumnsUnique(new String[] {"12..", "..2.", ".3..", "...1"})) throw new AssertionError("example 1");
        if (rowsAndColumnsUnique(new String[] {"1...", "2...", "1...", "...."})) throw new AssertionError("example 2");
        if (!rowsAndColumnsUnique(new String[] {"7"})) throw new AssertionError("one cell");
        // A global set would reject example 1, because the digit 2 occurs in two rows.
        Set<Character> global = new HashSet<>();
        boolean globalRejects = false;
        for (String row : new String[] {"12..", "..2.", ".3..", "...1"})
            for (char ch : row.toCharArray()) if (ch != '.' && !global.add(ch)) globalRejects = true;
        if (!globalRejects) throw new AssertionError("a global set fails on a legal board");
        // Random boards are checked against a rescanning oracle.
        Random rnd = new Random(72);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(5);
            String[] b = new String[n];
            for (int r = 0; r < n; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < n; c++) sb.append(rnd.nextInt(3) == 0 ? (char) ('1' + rnd.nextInt(4)) : '.');
                b[r] = sb.toString();
            }
            boolean expect = true;
            for (int r = 0; r < n; r++)
                for (int c = 0; c < n; c++) {
                    if (b[r].charAt(c) == '.') continue;
                    for (int k = 0; k < n; k++) {
                        if (k != c && b[r].charAt(k) == b[r].charAt(c)) expect = false;
                        if (k != r && b[k].charAt(c) == b[r].charAt(c)) expect = false;
                    }
                }
            if (rowsAndColumnsUnique(b) != expect) throw new AssertionError(String.join("/", b));
        }
    }
}
```

#### Solution: [Boundary] Box Identity (Author exercise)
<!-- id: hm-box-identity -->

**Approach.**
The pair `(r / 3, c / 3)` names the block of the cell `(r, c)`. With side `n`, the board holds `n / 3` blocks in each block row. The method therefore numbers a block by `(r / 3) * (n / 3) + c / 3`, which gives different numbers to different blocks. One set for each block holds its digits, and a digit already in the set of its block returns false. The shortcut `r / 3 + c / 3` gives the same number to blocks `(0, 1)` and `(1, 0)`, so the harness shows that it rejects a legal board. The invariant is that after the cells before `(r, c)`, each block set holds the digits of the filled cells of its block among them.

**Complexity.**
- **Time** is O(n^2) on average for side n, because each filled cell makes one set operation.
- **Space** is O(n^2), because the block sets hold at most one entry for each filled cell.

```java run
import java.util.*;

public final class BoxIdentity {
    /**
     * Reports whether no 3 by 3 block holds a digit twice.
     * Time: O(n^2) expected. Space: O(n^2).
     * Invariant: boxes.get(b) holds the digits of block b among the cells read so far.
     */
    static boolean boxesUnique(String[] board) {
        int n = board.length, perRow = n / 3;
        List<Set<Character>> boxes = new ArrayList<>();
        for (int k = 0; k < perRow * perRow; k++) boxes.add(new HashSet<>());
        // Row-major scan of every cell.
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                // The number of blocks in a block row is n / 3, so the row of the block scales by it.
                int b = (r / 3) * perRow + c / 3;
                if (!boxes.get(b).add(d)) {
                    return false;
                }
            }
        }
        return true;
    }

    /** The mistake: the block number is r / 3 + c / 3, which merges different blocks. */
    static boolean wrongKey(String[] board) {
        int n = board.length;
        List<Set<Character>> boxes = new ArrayList<>();
        for (int k = 0; k < 2 * (n / 3); k++) boxes.add(new HashSet<>());
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++) {
                char d = board[r].charAt(c);
                if (d != '.' && !boxes.get(r / 3 + c / 3).add(d)) return false;
            }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        String[] four = {"5..5..", "......", "......", "5..5..", "......", "......"};
        if (!boxesUnique(four)) throw new AssertionError("example 1");
        if (boxesUnique(new String[] {"5.....", "......", "..5...", "......", "......", "......"})) throw new AssertionError("example 2");
        // The wrong key merges blocks (0, 1) and (1, 0), so it rejects a legal board.
        if (wrongKey(four)) throw new AssertionError("the wrong key should reject the first example");
        // A 3 by 3 board is one block.
        if (boxesUnique(new String[] {"1..", ".1.", "..."})) throw new AssertionError("one block");
        // Random boards are checked against a coordinate oracle.
        Random rnd = new Random(73);
        for (int t = 0; t < 600; t++) {
            int n = 3 * (1 + rnd.nextInt(3));
            String[] b = new String[n];
            for (int r = 0; r < n; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < n; c++) sb.append(rnd.nextInt(4) == 0 ? (char) ('1' + rnd.nextInt(3)) : '.');
                b[r] = sb.toString();
            }
            boolean expect = true;
            for (int r1 = 0; r1 < n; r1++)
                for (int c1 = 0; c1 < n; c1++)
                    for (int r2 = 0; r2 < n; r2++)
                        for (int c2 = 0; c2 < n; c2++) {
                            boolean same = r1 / 3 == r2 / 3 && c1 / 3 == c2 / 3 && !(r1 == r2 && c1 == c2);
                            if (same && b[r1].charAt(c1) != '.' && b[r1].charAt(c1) == b[r2].charAt(c2)) expect = false;
                        }
            if (boxesUnique(b) != expect) throw new AssertionError(String.join("/", b));
        }
    }
}
```

#### Solution: [Recognize] Valid Sudoku (LeetCode 36)
<!-- id: hm-valid-sudoku -->

**Approach.**
Each filled cell belongs to one row, one column and one block, so the method keeps nine sets for each of the three scopes. For the digit `d` at `(r, c)` with block number `b = (r / 3) * 3 + c / 3`, the `add` calls on `rows[r]`, `cols[c]` and `boxes[b]` must all succeed. A failed `add` returns false. The invariant is that after the cells before `(r, c)` in row-major order, each set holds the digits of the filled cells of its scope among those cells. The harness checks a board whose only conflict lies inside one block, and a board with the digit 5 in many rows that stays legal.

**Complexity.**
- **Time** is O(1) for the fixed 9 by 9 board, which is O(n^2) for side n, because each cell makes at most three set operations of expected constant time.
- **Space** is O(1) for the fixed board and O(n^2) for side n, because the 27 sets hold at most 81 entries each scope.

```java run
import java.util.*;

public final class ValidSudoku {
    /**
     * Reports whether no row, column or block holds a digit twice.
     * Time: O(n^2) expected for side n, constant for side 9. Space: O(n^2).
     * Invariant: each scope set holds the digits of its scope among the cells read so far.
     */
    static boolean isValid(String[] board) {
        List<Set<Character>> rows = new ArrayList<>(), cols = new ArrayList<>(), boxes = new ArrayList<>();
        for (int k = 0; k < 9; k++) { rows.add(new HashSet<>()); cols.add(new HashSet<>()); boxes.add(new HashSet<>()); }
        // Row-major scan of the 81 cells.
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                int b = (r / 3) * 3 + c / 3;
                // Every scope must accept the digit; the first refusal ends the check.
                if (!rows.get(r).add(d) || !cols.get(c).add(d) || !boxes.get(b).add(d)) {
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // The statement examples.
        String[] ok = {"1...5...9", ".5...9...", "..9...4..", "...5...9.", "5...9...4", ".9...4...", "..5...9..", "...9...4.", "9...4...8"};
        if (!isValid(ok)) throw new AssertionError("example 1");
        String[] bad = ok.clone();
        bad[1] = ".51..9...";
        if (isValid(bad)) throw new AssertionError("example 2");
        // The conflict of the second example is a block conflict only: rows and columns stay unique.
        if (!RowsCols.rowsAndColumnsUnique(bad)) throw new AssertionError("rows and columns see no conflict");
        // The lesson traces expressed as boards.
        String[] t1 = new String[9];
        Arrays.fill(t1, ".........");
        t1[0] = "5..7.....";
        t1[1] = "6........";
        t1[2] = ".....9...";
        t1[4] = "....5....";
        if (!isValid(t1)) throw new AssertionError("trace 1");
        String[] t2 = new String[9];
        Arrays.fill(t2, ".........");
        t2[0] = "5........";
        t2[1] = "....3....";
        t2[2] = "..5......";
        if (isValid(t2)) throw new AssertionError("trace 2");
        // Random boards are checked against the rescanning method from the lesson.
        Random rnd = new Random(74);
        for (int t = 0; t < 800; t++) {
            String[] b = new String[9];
            for (int r = 0; r < 9; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 9; c++) sb.append(rnd.nextInt(5) == 0 ? (char) ('1' + rnd.nextInt(9)) : '.');
                b[r] = sb.toString();
            }
            char[][] g = new char[9][];
            for (int r = 0; r < 9; r++) g[r] = b[r].toCharArray();
            if (isValid(b) != naive(g)) throw new AssertionError(String.join("/", b));
        }
    }

    /** Lesson code: rescan the row, the column and the block of each filled cell. */
    static boolean naive(char[][] board) {
        for (int r = 0; r < 9; r++)
            for (int c = 0; c < 9; c++) {
                char d = board[r][c];
                if (d == '.') continue;
                for (int k = 0; k < 9; k++) {
                    int br = 3 * (r / 3) + k / 3, bc = 3 * (c / 3) + k % 3;
                    if (k != c && board[r][k] == d) return false;
                    if (k != r && board[k][c] == d) return false;
                    if ((br != r || bc != c) && board[br][bc] == d) return false;
                }
            }
        return true;
    }

    /** Helper with the rows-and-columns check, to show that the block conflict is invisible to it. */
    static final class RowsCols {
        static boolean rowsAndColumnsUnique(String[] board) {
            for (int r = 0; r < 9; r++) {
                Set<Character> row = new HashSet<>(), col = new HashSet<>();
                for (int c = 0; c < 9; c++) {
                    if (board[r].charAt(c) != '.' && !row.add(board[r].charAt(c))) return false;
                    if (board[c].charAt(r) != '.' && !col.add(board[c].charAt(r))) return false;
                }
            }
            return true;
        }
    }
}
```
