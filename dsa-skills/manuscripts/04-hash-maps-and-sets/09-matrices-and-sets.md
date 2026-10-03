<!-- lesson-kind: combination -->
<!-- lesson-id: matrices-and-sets -->
## Matrices And Sets

<!-- stage: context -->
### Checking A Number Puzzle Grid

A puzzle magazine prints a nine-by-nine grid of digits, with blanks, and an editor has to confirm that no digit repeats inside any row, inside any column, or inside any of the nine three-by-three boxes. A digit may of course repeat across different rows: the five in the top row and a five in the fifth row are fine, and a puzzle where that was forbidden would be unplayable.

The editor works with a tray of index cards. She writes a heading on each card, such as "row 0", "column 4" or "box 4", and as she reads each filled cell she checks the three cards that cell belongs to. If a card already lists the digit, the grid is invalid. Otherwise she adds the digit to all three cards. She never rereads a row or a box, because the cards remember what each one has seen.

<!-- stage: contributions -->
### Coordinates And Memory Per Scope

Matrix traversal supplies coordinates. Every cell has a row and a column, and from them the code can derive the box a cell lies in, so each cell can name the several overlapping groups it belongs to. The matrix itself cannot say whether a value has occurred earlier in one of those groups, because the earlier cells may be far away in the traversal order.

Sets supply that memory. A set owned by one row, one column or one box remembers exactly which digits that group has already contained and answers a membership question in expected constant time. The recognition cue for the combination is a validity rule that depends on uniqueness within several overlapping scopes. The traversal decides which scopes a cell belongs to, and the sets decide whether the digit is new in each of them.

<!-- stage: naive -->
### Scan Every Cell's Neighbourhood

The direct check takes every filled cell and scans the cells that share a row, a column or a box with it, looking for the same digit.

```java
static boolean validByScanning(String[] board) {
    int n = board.length;
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) {
            char d = board[r].charAt(c);
            if (d == '.') continue;
            for (int k = 0; k < n; k++) {
                if (k != c && board[r].charAt(k) == d) return false;      // same row
                if (k != r && board[k].charAt(c) == d) return false;      // same column
            }
            int r0 = r / 3 * 3, c0 = c / 3 * 3;
            for (int i = r0; i < r0 + 3; i++)
                for (int j = c0; j < c0 + 3; j++)
                    if ((i != r || j != c) && board[i].charAt(j) == d) return false;   // same box
        }
    }
    return true;
}
```

It accepts a grid that holds one 5 in every row, column and box, and rejects one with two 5s in column 0.

<!-- stage: bottleneck -->
### Every Cell Rereads Its Neighbourhood

Each filled cell reads about `3n` other cells, and there are `n * n` cells, so the work is O(n * n * n) for an `n` by `n` grid. For the 9 by 9 puzzle that is a couple of thousand reads, which nobody notices, and the pattern matters because the same idea runs on larger grids and on repeated checks while a solver searches. For a 2,500 by 2,500 grid it would be fifteen billion reads.

The waste is rereading. When a cell is examined, its row has been examined by every earlier cell in that row, and each of them already knew everything in it. A cell needs one answer from each of its three scopes, whether this digit is already present, and it needs it without reading any other cell. That is exactly the question a set answers, provided there is one set per scope and a cell knows which three to ask.

<!-- stage: insight -->
### One Memory For Each Overlapping Scope

A **scope set** is a set that belongs to one group of cells, a single row, a single column or a single box, and holds the digits that group has already shown. For a nine-by-nine grid there are nine row sets, nine column sets and nine box sets. A cell at `(r, c)` with digit `d` asks three questions, one in each of its scope sets, and the grid is invalid as soon as any answer is yes. Otherwise `d` is added to all three. The invariant is that, after the cells read so far, each scope set contains exactly the digits found in that scope among those cells.

The box set needs a name for the group. The **box key** is derived from the coordinates by integer division: the box row is `r / 3`, the box column is `c / 3`, and `(r / 3) * 3 + c / 3` gives a number from 0 to 8 that is the same for all nine cells of a box and different between boxes. Getting this key wrong is the usual bug, for example by dividing after combining, or by using `r / 3 + c / 3`, which gives the same number to boxes that lie on the same anti-diagonal.

<!-- names: scope set, box key, false collision -->

The most tempting mistake is a single set for the whole grid. It produces a **false collision**: it rejects a legal grid because the same digit appears in two different rows, which the rules allow. Every digit appears nine times in a solved puzzle, so a global set would reject every solution. The fix is not a smarter global set but keeping scopes apart. A single set can still do the job if its elements carry the scope in their key, such as a record of the scope kind, the scope number and the digit, using the compound keys of the previous lesson.

<!-- stage: variables -->
### Three Set Families And A Box Key

The state is three arrays of sets, `rows`, `cols` and `boxes`, each of length 9, created empty before the traversal, which is the correct state for no cells read. The traversal variables are `r` and `c`, and the digit `d` is read from the cell. Blank cells, marked with a dot, are skipped, since a blank claims nothing. The box key is computed from `r` and `c` and indexes into `boxes`. The check precedes the insertion, so a cell can never conflict with itself, and the first conflict ends the work with a false answer.

<!-- stage: trace -->
### Same Digit, Different Scopes

```trace
{"cells":["5@(0,0)","5@(4,4)","5@(1,2)"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"digit":5,"row":0,"col":0,"box":0,"result":"ok"},"note":"Digit 5 at row 0, column 0, box 0. All three scope sets are free of 5, so add it to each."},{"at":{"i":1},"vars":{"digit":5,"row":4,"col":4,"box":4,"result":"ok"},"note":"Digit 5 at row 4, column 4, box 4. All three scope sets are free of 5, so add it to each."},{"at":{"i":2},"vars":{"digit":5,"row":1,"col":2,"box":0,"result":"invalid"},"note":"Digit 5 at row 1, column 2, box 0. The box set already holds 5. The grid is invalid."}]}
```

Take three cells holding the digit 5: at row 0 and column 0, at row 4 and column 4, and at row 1 and column 2. The first cell adds the 5 to row set 0, column set 0 and box set 0. The second cell is in row 4, column 4 and box 4, all of which are empty, so it adds the 5 to them and no conflict occurs, though a single global set would already have failed here. The third cell is in row 1 and column 2, which are empty, but its box is box 0, which already holds a 5, so the grid is invalid.

```trace
{"cells":["(0,0)","(2,2)","(3,0)","(4,5)","(8,8)"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"r":0,"c":0,"boxRow":0,"boxCol":0,"key":0},"note":"Cell (0,0): box row 0/3 = 0, box column 0/3 = 0, key 0*3 + 0 = 0."},{"at":{"i":1},"vars":{"r":2,"c":2,"boxRow":0,"boxCol":0,"key":0},"note":"Cell (2,2): box row 2/3 = 0, box column 2/3 = 0, key 0*3 + 0 = 0."},{"at":{"i":2},"vars":{"r":3,"c":0,"boxRow":1,"boxCol":0,"key":3},"note":"Cell (3,0): box row 3/3 = 1, box column 0/3 = 0, key 1*3 + 0 = 3."},{"at":{"i":3},"vars":{"r":4,"c":5,"boxRow":1,"boxCol":1,"key":4},"note":"Cell (4,5): box row 4/3 = 1, box column 5/3 = 1, key 1*3 + 1 = 4."},{"at":{"i":4},"vars":{"r":8,"c":8,"boxRow":2,"boxCol":2,"key":8},"note":"Cell (8,8): box row 8/3 = 2, box column 8/3 = 2, key 2*3 + 2 = 8."}]}
```

The second trace shows only the box key. The cells (0,0) and (2,2) both give key 0, since 0 divided by 3 and 2 divided by 3 are both 0. The cell (3,0) gives 3, the cell (4,5) gives 4, and the cell (8,8) gives 8. Each key is the box row times 3 plus the box column, so the keys 0 to 8 run along the boxes row by row.

<!-- stage: code -->
### Rows, Boxes And The Whole Board

```java
static int firstRowRepeat(String row) {
    Set<Character> seen = new HashSet<>();
    for (int c = 0; c < row.length(); c++) {
        char d = row.charAt(c);
        if (d != '.' && !seen.add(d)) return c;
    }
    return -1;
}

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

static int boxKey(int r, int c) {
    return (r / 3) * 3 + c / 3;
}

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
```

The board check reads every cell once and makes three set operations per filled cell, so the time is expected O(n * n) and the space is O(n * n) for the sets. The non-short-circuit `&` is used on purpose in `isValidSudoku` so that all three sets are updated, though the method returns false immediately when any of them reports a repeat, so the difference only matters for readers who expect the sets to stay consistent. The row-and-column method uses `||`, which stops at the first conflict, since a conflict ends the method anyway.

<!-- stage: applicability -->
### When Uniqueness Has Several Scopes

Use sets per scope when validity depends on uniqueness within several overlapping groups of cells, and each cell can name its groups from its coordinates. The invariant is that every scope set holds exactly the values seen so far in that scope, and the check precedes the insertion. Derive each scope key from the coordinates in one small function and test that function on its own.

The false friend is one global set. It confuses uniqueness in a scope with uniqueness in the whole grid and rejects legal inputs. A second false friend is a count of digits per row alone, which cannot see column or box conflicts, so checking scopes one family at a time and combining the results is correct only if every family is checked.

In Java, use `Set.add` as the combined test and insert, and never rely on the iteration order of a set. Remember that `char` digits compare as characters, so `'5'` is not the integer 5, and a conversion with `d - '0'` is needed only if you index an array. Use integer division for the box key, because floating-point division would give fractions. Build the arrays of sets before the loop, since `new HashSet[9]` generic arrays need a cast, and a `List` of sets avoids that.

<!-- stage: exercises -->
### Exercises

#### [Build] Row Duplicates (Author exercise)
<!-- id: hm-row-duplicates -->

**Prerequisites.** Membership sets; the scope set in this lesson.

**Problem.** A row is a string of digits `1` to `9` and dots for blanks. Return the index of the first cell whose digit already appeared earlier in the row, or -1 if no digit repeats. Blanks never count as repeats.

**Constraints.** 1 <= row.length() <= 9. Each character is a digit from 1 to 9 or a dot. Scan once and keep one set.

**Example 1.** Input `row = "53..7..5."`, output 7, since the second 5 is at index 7.

**Example 2.** Input `row = "........."`, output -1, because blanks are ignored.

**Hint.** What does the return value of `Set.add` tell you? Why must dots be skipped before the set is consulted?

**Changed decision.** First rung: a set owned by one scope answers the uniqueness question for that scope only.

#### [Vary] Row And Column Scope (Author exercise)
<!-- id: hm-row-column-scope -->

**Prerequisites.** The build exercise above.

**Problem.** A square board has `n` rows of `n` characters, each a digit from `1` to `9` or a dot. Return true if no row and no column contains a repeated digit, ignoring boxes. Keep one set per row and one set per column.

**Constraints.** 1 <= n <= 9. The rows are strings of equal length. A digit may repeat in different rows and different columns.

**Example 1.** Input `board = ["12.", "3.1", "2.3"]`, output true.

**Example 2.** Input `board = ["1..", "...", "1.."]`, output false, because column 0 holds two 1s.

**Hint.** Which two families of sets does a cell at row `r` and column `c` consult? Would one global set accept Example 1?

**Changed decision.** A cell now belongs to two scopes at once, so two families of sets are updated together.

#### [Boundary] Box Identity (Author exercise)
<!-- id: hm-box-identity -->

**Prerequisites.** The two exercises above.

**Problem.** Given a nine-by-nine board, return true if no three-by-three box contains a repeated digit, ignoring rows and columns. Derive the box of each cell from `(row / 3, col / 3)` and keep one set per box.

**Constraints.** The board has 9 rows of 9 characters, each a digit from `1` to `9` or a dot. Equal digits in different boxes are legal even when they share a row or column.

**Example 1.** Input a board with a 5 at row 0, column 0 and a 5 at row 1, column 1, all other cells blank, output false.

**Example 2.** Input a board with a 5 at row 0, column 0 and a 5 at row 0, column 3, all other cells blank, output true, because the two cells lie in different boxes.

**Hint.** Which cells share box key 0? What goes wrong if the key is computed as `r / 3 + c / 3`?

**Changed decision.** The scope is not a row or a column but a block, so the key must be derived from both coordinates.

#### [Recognize] Valid Sudoku (LeetCode 36)
<!-- id: hm-valid-sudoku -->

**Prerequisites.** All three exercises above.

**Problem.** Determine whether a partially filled nine-by-nine board is valid: each row, each column and each three-by-three box may contain each digit from 1 to 9 at most once. Only the filled cells are checked, and the board need not be solvable.

**Constraints.** The board has 9 rows of 9 characters, each a digit from `1` to `9` or a dot. Do not modify the board. Three families of sets are expected.

**Example 1.** Input a board holding a single 1 in each row, at columns 0, 3, 6, 1, 4, 7, 2, 5, 8 for rows 0 to 8, output true, since the nine 1s share no row, column or box.

**Example 2.** Input the same board with the 1 in row 8 moved to column 0, output false, because column 0 now holds two 1s.

**Hint.** Which three scope keys does the cell at row `r`, column `c` have, and in which order should you test and insert?

**Changed decision.** All three scopes are maintained at once, and the key for each must never be confused with the key of another family.
