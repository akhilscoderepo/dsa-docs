<!-- solutions-for: 09-matrices-and-sets -->
### Matrices And Sets

#### Solution: [Build] Row Duplicates (Author exercise)
<!-- id: hm-row-duplicates -->

**Approach.** Walk the row from left to right with one set. Skip blank cells, then call `add` on the digit. A failed add means the digit appeared earlier in this row, so the current index is the answer. If the loop ends, no digit repeated. A single set is correct here because the scope is one row. The oracle compares each cell with every earlier cell, and the assertions require the same index on random rows, including rows that are all blanks.

**Complexity.** Expected O(n) time and O(n) extra space for a row of length `n`.

```java run
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class RowDuplicates {
    static int firstRowRepeat(String row) {
        Set<Character> seen = new HashSet<>();
        for (int c = 0; c < row.length(); c++) {
            char d = row.charAt(c);
            if (d != '.' && !seen.add(d)) return c;
        }
        return -1;
    }
    static int oracle(String row) {
        for (int c = 0; c < row.length(); c++) {
            if (row.charAt(c) == '.') continue;
            for (int k = 0; k < c; k++) if (row.charAt(k) == row.charAt(c)) return c;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (firstRowRepeat("53..7..5.") != 7) throw new AssertionError("example 1");
        if (firstRowRepeat(".........") != -1) throw new AssertionError("example 2");
        if (firstRowRepeat("123456789") != -1) throw new AssertionError("all distinct");
        Random rnd = new Random(121);
        String alphabet = "123.";
        for (int t = 0; t < 4000; t++) {
            StringBuilder sb = new StringBuilder();
            int n = 1 + rnd.nextInt(9);
            for (int i = 0; i < n; i++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
            String row = sb.toString();
            if (firstRowRepeat(row) != oracle(row)) throw new AssertionError("disagrees with the earlier-cell scan on " + row);
        }
    }
}
```

#### Solution: [Vary] Row And Column Scope (Author exercise)
<!-- id: hm-row-column-scope -->

**Approach.** Create `n` row sets and `n` column sets. For each filled cell, add its digit to the set of its row and to the set of its column, and return false as soon as either add fails. A single global set would reject the first example, whose digits 1, 2 and 3 each appear in several rows, and the assertions demonstrate that. The oracle compares every pair of filled cells and reports a conflict when the digits are equal and the cells share a row or a column, and the assertions agree on random boards.

**Complexity.** Expected O(n * n) time and O(n * n) extra space.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class RowColumnScope {
    static boolean rowsAndColumnsOk(String[] board) {
        int n = board.length;
        List<Set<Character>> rows = new ArrayList<>(), cols = new ArrayList<>();
        for (int i = 0; i < n; i++) { rows.add(new HashSet<>()); cols.add(new HashSet<>()); }
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                if (!rows.get(r).add(d) || !cols.get(c).add(d)) return false;
            }
        }
        return true;
    }
    static boolean globalSet(String[] board) {
        Set<Character> all = new HashSet<>();
        for (String row : board)
            for (char d : row.toCharArray())
                if (d != '.' && !all.add(d)) return false;
        return true;
    }
    static boolean oracle(String[] board) {
        int n = board.length;
        for (int r1 = 0; r1 < n; r1++)
            for (int c1 = 0; c1 < n; c1++) {
                char d = board[r1].charAt(c1);
                if (d == '.') continue;
                for (int r2 = 0; r2 < n; r2++)
                    for (int c2 = 0; c2 < n; c2++) {
                        if (r1 == r2 && c1 == c2) continue;
                        if (board[r2].charAt(c2) == d && (r1 == r2 || c1 == c2)) return false;
                    }
            }
        return true;
    }

    public static void main(String[] args) {
        if (!rowsAndColumnsOk(new String[] {"12.", "3.1", "2.3"})) throw new AssertionError("example 1");
        if (rowsAndColumnsOk(new String[] {"1..", "...", "1.."})) throw new AssertionError("example 2");
        if (globalSet(new String[] {"12.", "3.1", "2.3"})) throw new AssertionError("a global set wrongly rejects the legal first example");
        Random rnd = new Random(122);
        String alphabet = "123..";
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(5);
            String[] b = new String[n];
            for (int r = 0; r < n; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < n; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                b[r] = sb.toString();
            }
            if (rowsAndColumnsOk(b) != oracle(b)) throw new AssertionError("disagrees with the pair check on " + String.join("/", b));
        }
    }
}
```

#### Solution: [Boundary] Box Identity (Author exercise)
<!-- id: hm-box-identity -->

**Approach.** Give every cell the key `(r / 3) * 3 + c / 3`, which is the same for the nine cells of a box and different between boxes, and keep one set per key. A failed add means a repeated digit in that box. The key `r / 3 + c / 3` is wrong because boxes (0, 1) and (1, 0) would share the value 1, and the assertions show that this variant rejects a legal board. The oracle compares every pair of cells and tests for equal digits whose cells have equal box row and equal box column, and the assertions agree on random boards.

**Complexity.** Expected O(1) per cell and O(81) total for a fixed board.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class BoxIdentity {
    static int boxKey(int r, int c) { return (r / 3) * 3 + c / 3; }

    static boolean boxesOk(String[] board, boolean correctKey) {
        List<Set<Character>> boxes = new ArrayList<>();
        for (int i = 0; i < 9; i++) boxes.add(new HashSet<>());
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                int key = correctKey ? boxKey(r, c) : r / 3 + c / 3;
                if (!boxes.get(key).add(d)) return false;
            }
        }
        return true;
    }
    static boolean oracle(String[] board) {
        for (int r1 = 0; r1 < 9; r1++)
            for (int c1 = 0; c1 < 9; c1++) {
                char d = board[r1].charAt(c1);
                if (d == '.') continue;
                for (int r2 = 0; r2 < 9; r2++)
                    for (int c2 = 0; c2 < 9; c2++) {
                        if (r1 == r2 && c1 == c2) continue;
                        if (board[r2].charAt(c2) == d && r1 / 3 == r2 / 3 && c1 / 3 == c2 / 3) return false;
                    }
            }
        return true;
    }
    static String[] blank() {
        String[] b = new String[9];
        java.util.Arrays.fill(b, ".........");
        return b;
    }
    static String[] put(String[] b, int r, int c, char d) {
        char[] row = b[r].toCharArray();
        row[c] = d;
        b[r] = new String(row);
        return b;
    }

    public static void main(String[] args) {
        String[] one = put(put(blank(), 0, 0, '5'), 1, 1, '5');
        if (boxesOk(one, true)) throw new AssertionError("example 1");
        String[] two = put(put(blank(), 0, 0, '5'), 0, 3, '5');
        if (!boxesOk(two, true)) throw new AssertionError("example 2");
        String[] other = put(put(blank(), 0, 3, '7'), 3, 0, '7');
        if (boxesOk(other, false)) throw new AssertionError("the wrong key merges boxes (0,1) and (1,0)");
        if (!boxesOk(other, true)) throw new AssertionError("the correct key keeps them apart");
        for (int r = 0; r < 9; r++) for (int c = 0; c < 9; c++)
            if (boxKey(r, c) < 0 || boxKey(r, c) > 8) throw new AssertionError("box keys lie in 0..8");
        Random rnd = new Random(123);
        String alphabet = "1234.........";
        for (int t = 0; t < 2000; t++) {
            String[] b = new String[9];
            for (int r = 0; r < 9; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 9; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                b[r] = sb.toString();
            }
            if (boxesOk(b, true) != oracle(b)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```

#### Solution: [Recognize] Valid Sudoku (LeetCode 36)
<!-- id: hm-valid-sudoku -->

**Approach.** Keep nine row sets, nine column sets and nine box sets. For every filled cell, add its digit to the three sets of its scopes and reject the board if any add reports a repeat. The three scopes use the keys `r`, `c` and `(r / 3) * 3 + c / 3`, each in its own family so that keys cannot be confused. The first example places one 1 in every row, column and box, and the assertions show that a global set would reject it while the three families accept it. The oracle checks every pair of filled cells for equal digits that share a row, a column or a box, and the assertions agree on random boards.

**Complexity.** Expected O(1) per cell, so O(81) for the board, with O(81) extra space.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ValidSudoku {
    static int boxKey(int r, int c) { return (r / 3) * 3 + c / 3; }

    static boolean isValidSudoku(String[] board) {
        List<Set<Character>> rows = new ArrayList<>(), cols = new ArrayList<>(), boxes = new ArrayList<>();
        for (int i = 0; i < 9; i++) { rows.add(new HashSet<>()); cols.add(new HashSet<>()); boxes.add(new HashSet<>()); }
        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                char d = board[r].charAt(c);
                if (d == '.') continue;
                boolean fresh = rows.get(r).add(d) & cols.get(c).add(d) & boxes.get(boxKey(r, c)).add(d);
                if (!fresh) return false;
            }
        }
        return true;
    }
    static boolean globalSet(String[] board) {
        Set<Character> all = new HashSet<>();
        for (String row : board)
            for (char d : row.toCharArray())
                if (d != '.' && !all.add(d)) return false;
        return true;
    }
    static boolean oracle(String[] board) {
        for (int r1 = 0; r1 < 9; r1++)
            for (int c1 = 0; c1 < 9; c1++) {
                char d = board[r1].charAt(c1);
                if (d == '.') continue;
                for (int r2 = 0; r2 < 9; r2++)
                    for (int c2 = 0; c2 < 9; c2++) {
                        if (r1 == r2 && c1 == c2) continue;
                        if (board[r2].charAt(c2) != d) continue;
                        if (r1 == r2 || c1 == c2 || (r1 / 3 == r2 / 3 && c1 / 3 == c2 / 3)) return false;
                    }
            }
        return true;
    }

    public static void main(String[] args) {
        String[] ones = {"1........", "...1.....", "......1..", ".1.......", "....1....", ".......1.", "..1......", ".....1...", "........1"};
        if (!isValidSudoku(ones)) throw new AssertionError("example 1");
        if (globalSet(ones)) throw new AssertionError("a global set wrongly rejects example 1");
        String[] moved = ones.clone();
        moved[8] = "1........";
        if (isValidSudoku(moved)) throw new AssertionError("example 2");
        Random rnd = new Random(124);
        String alphabet = "12345678.............";
        for (int t = 0; t < 3000; t++) {
            String[] b = new String[9];
            for (int r = 0; r < 9; r++) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 9; c++) sb.append(alphabet.charAt(rnd.nextInt(alphabet.length())));
                b[r] = sb.toString();
            }
            if (isValidSudoku(b) != oracle(b)) throw new AssertionError("disagrees with the pair check");
        }
    }
}
```
