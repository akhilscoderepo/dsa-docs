<!-- lesson-kind: combination -->
<!-- lesson-id: matrices-and-sets -->
## Matrices And Sets

<!-- stage: context -->
### A Puzzle Board That Rejects Legal Moves

A number-puzzle app checks every move on a 9 by 9 board. Each cell holds a digit from 1 to 9 or stays empty. A board is legal when no digit appears twice in a row, twice in a column, or twice in a 3 by 3 block. The first version of the check keeps one set of digits for the whole board. It rejects a legal move whenever the digit 5 already stands anywhere else, so almost every board looks illegal after a few moves.

The check must forbid repeats inside three kinds of groups and still allow the same digit in different groups. The question is what the program must remember while it reads the board cell by cell, and how it keeps the three groups apart.

<!-- stage: contributions -->
### What The Grid And Sets Add

The matrix supplies coordinates. A loop over rows and columns visits every cell with its row number `r` and column number `c`. The coordinates also name the three groups that contain the cell, namely row `r`, column `c`, and the 3 by 3 block that covers `(r, c)`.

The sets supply memory. A set answers whether a digit has already appeared, and it needs no count and no order. The combined question asks for uniqueness inside several overlapping groups. The matrix names the groups of each cell, and one set for each group remembers the digits that group already holds. Neither part works alone. Coordinates without sets cannot recall earlier cells, and sets without coordinates do not know which group a cell belongs to.

<!-- stage: naive -->
### Rescanning Row, Column And Block

The direct method takes each filled cell and compares its digit with the other cells of its row, its column and its block.

```java
static boolean isLegal(char[][] board) {
    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            char d = board[r][c];
            if (d == '.') {
                continue;
            }
            for (int k = 0; k < 9; k++) {
                int br = 3 * (r / 3) + k / 3;
                int bc = 3 * (c / 3) + k % 3;
                if (k != c && board[r][k] == d) {
                    return false;
                }
                if (k != r && board[k][c] == d) {
                    return false;
                }
                if ((br != r || bc != c) && board[br][bc] == d) {
                    return false;
                }
            }
        }
    }
    return true;
}
```

On a board with a repeated digit in some row, the method returns false at the second of the two cells. On a board without repeats it reads 27 cells for each filled cell.

<!-- stage: bottleneck -->
### Every Pair Of Cells Gets Compared Twice

```predict
A 9 by 9 board has every cell filled. About how many cell reads does the method make, and how does the count grow for a board of side n with blocks of side about the square root of n?

Each filled cell reads 27 cells, so the total is 81 * 27 = 2187 reads. For side n, each cell reads about 3 * n cells, so the total grows as O(n^3). The comparison of cell A with cell B repeats when the loop reaches B and reads A back.
```

For the 9 by 9 board the total is 81 * 27 = 2187 reads, which looks harmless. The growth shows when the side grows or when a program validates millions of boards. The method asks, for every cell, a question that the neighbors in its groups answer too. Two cells in one row compare against each other once from each side. A program that remembers the digits of each group needs one lookup for each group of a cell, so the work for a whole board falls to O(n^2).

<!-- stage: insight -->
### Keep One Set For Each Group

#### Name The Groups That Must Stay Unique

A **scope** is a group of cells in which a digit may appear at most once. A cell belongs to three scopes: its row, its column and its block. The board is legal exactly when every scope holds each digit at most once.

<!-- names: scope, box index, scope sets -->

#### Number The Blocks

The **box index** names the block of the cell `(r, c)` by `(r / 3) * 3 + c / 3`, which gives a number from 0 to 8. Blocks 0, 1 and 2 cover the top three rows from left to right, and blocks 3 to 8 continue below. The formula `r / 3 + c / 3` is wrong, because the cells `(0, 3)` and `(3, 0)` both give 1 although they lie in different blocks.

#### Keep The Scope Sets Apart

The **scope sets** are three lists of nine sets, one list for the rows, one for the columns and one for the blocks. For the digit `d` at `(r, c)`, the loop tests `rows[r]`, `cols[c]` and `boxes[b]`, where `b` is the box index. If any of the three holds `d`, the board is illegal. Otherwise the loop adds `d` to all three. The same digit can sit in `rows[0]` and `rows[4]` without a conflict, because the sets belong to different scopes.

#### The Invariant

After the loop has read the cells before `(r, c)` in row-major order, each scope set holds exactly the digits of the filled cells of its scope among those cells. No scope holds a repeat. Each cell costs three set tests and three insertions of expected constant time, so the loop costs O(n^2) on average. The sets hold at most one entry per filled cell for each of the three scopes, so the space is O(n^2).

<!-- stage: variables -->
### Three Set Lists And A Cell

The loop uses four pieces of state.

- **rows** holds nine sets, and `rows[r]` holds the digits already seen in row `r`.
- **cols** holds nine sets, and `cols[c]` holds the digits already seen in column `c`.
- **boxes** holds nine sets, and `boxes[b]` holds the digits already seen in block `b`.
- **(r, c)** names the cell the loop reads, and the loop moves through the board row by row.

<!-- stage: trace -->
### Reading Filled Cells Of Two Boards

#### A Legal Board With Repeated Digits

Take the filled cells `(0,0)=5`, `(0,3)=7`, `(1,0)=6`, `(2,5)=9` and `(4,4)=5`. The first cell puts 5 into row 0, column 0 and block 0. The cell `(4,4)` also holds a 5, but it belongs to row 4, column 4 and block 4, and none of those sets holds 5. The board stays legal, although the digit 5 occurs twice on it.

#### A Conflict That Only The Block Sees

Now take `(0,0)=5`, `(1,4)=3` and `(2,2)=5`. The cell `(2,2)` has row 2 and column 2, and neither set holds 5. Its block is block 0, which holds the 5 from `(0,0)`. The test on `boxes[0]` finds the conflict. A check of rows and columns alone would accept this board.

#### Stepping Through Both Boards

```trace
{"cells":["(0,0)=5","(0,3)=7","(1,0)=6","(2,5)=9","(4,4)=5"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"Start: all 27 sets are empty."},{"at":{"i":0},"vars":{"cell":"(0,0)=5","row":"{}","col":"{}","box":"0:{}"},"note":"Digit 5 is new in row 0, column 0 and block 0. Add it to all three sets."},{"at":{"i":1},"vars":{"cell":"(0,3)=7","row":"{5}","col":"{}","box":"1:{}"},"note":"Digit 7 is new in row 0, column 3 and block 1. Add it to all three sets."},{"at":{"i":2},"vars":{"cell":"(1,0)=6","row":"{}","col":"{5}","box":"0:{5}"},"note":"Digit 6 is new in row 1, column 0 and block 0. Add it to all three sets."},{"at":{"i":3},"vars":{"cell":"(2,5)=9","row":"{}","col":"{}","box":"1:{7}"},"note":"Digit 9 is new in row 2, column 5 and block 1. Add it to all three sets."},{"at":{"i":4},"vars":{"cell":"(4,4)=5","row":"{}","col":"{}","box":"4:{}"},"note":"Digit 5 is new in row 4, column 4 and block 4. Add it to all three sets."},{"at":{"i":5},"vars":{},"note":"Every filled cell passed, so the board is legal."}]}
```

```trace
{"cells":["(0,0)=5","(1,4)=3","(2,2)=5"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{},"note":"Start: all 27 sets are empty."},{"at":{"i":0},"vars":{"cell":"(0,0)=5","row":"{}","col":"{}","box":"0:{}"},"note":"Digit 5 is new in row 0, column 0 and block 0. Add it to all three sets."},{"at":{"i":1},"vars":{"cell":"(1,4)=3","row":"{}","col":"{}","box":"1:{}"},"note":"Digit 3 is new in row 1, column 4 and block 1. Add it to all three sets."},{"at":{"i":2},"vars":{"cell":"(2,2)=5","row":"{}","col":"{}","box":"0:{5}"},"note":"Digit 5 is already in the block set of this cell, so the board is illegal."}]}
```

<!-- stage: code -->
### Three Lists Of Sets

#### Checking A Nine By Nine Board

```java
static boolean isLegal(char[][] board) {
    List<Set<Character>> rows = new ArrayList<>();
    List<Set<Character>> cols = new ArrayList<>();
    List<Set<Character>> boxes = new ArrayList<>();
    for (int k = 0; k < 9; k++) {
        rows.add(new HashSet<>());
        cols.add(new HashSet<>());
        boxes.add(new HashSet<>());
    }
    for (int r = 0; r < 9; r++) {
        for (int c = 0; c < 9; c++) {
            char d = board[r][c];
            if (d == '.') {
                continue;
            }
            int b = (r / 3) * 3 + c / 3;
            if (!rows.get(r).add(d) || !cols.get(c).add(d) || !boxes.get(b).add(d)) {
                return false;
            }
        }
    }
    return true;
}
```

#### What The Method Costs

The loops visit each cell once, and each filled cell makes up to three `add` calls of expected constant time. The time is O(n^2) on average for side n, which is 81 cells here. The sets hold at most one entry for each filled cell and scope, so the space is O(n^2). The `add` call both tests and stores, and the short-circuit `||` stops at the first scope that reports a repeat.

<!-- stage: applicability -->
### When Several Groups Overlap

#### Look For Uniqueness In Overlapping Groups

Use one set for each group when a validity rule demands uniqueness inside several overlapping groups of a grid, such as rows, columns and blocks. The invariant is that each set holds exactly the values of its group among the cells processed so far. The same idea checks the seats of an exam hall, where a candidate number must not repeat in a row or in a column. The scope of a cell must come from its coordinates, so the key of each set is the row number, the column number or the box index.

#### One Global Set Is A False Friend

A false friend here is a single set for the whole board. That set rejects a legal digit that appears in different rows, different columns and different blocks, which is how the opening version failed. The opposite mistake also occurs. Checking only rows and columns accepts a board whose only conflict lies inside one block, as the second trace shows.

#### Java Details That Cause Failures

An array of generic sets such as `Set<Character>[]` does not compile cleanly, so use a `List<Set<Character>>` or one `boolean` table for each scope. The character `'.'` marks an empty cell. The loop must skip it before the set sees it. The integer division `r / 3` rounds toward zero, which is correct for the non-negative rows used here.

<!-- stage: exercises -->
### Exercises

#### [Build] Row Duplicates (Author exercise)
<!-- id: hm-row-duplicates -->

**Prerequisites.** The membership test with `add` from the first lesson.

**Problem.** Let `row` be a string of nine characters. Each character is a digit from `'1'` to `'9'` or the character `'.'`, which marks an empty cell. Return the index of the first character that repeats a digit that appears earlier in `row`. Return -1 when no digit repeats.

**Constraints.** The limits are:
- **Length** is exactly 9.
- **Characters** are `'1'` to `'9'` or `'.'`.
- **Empty** cells never count as repeats.
- **Answer** is an index from 1 to 8, or -1.

**Example 1.** Input `row = "4.2.1.4.."`, output 6, because the second 4 sits at index 6.

**Example 2.** Input `row = "123456789"`, output -1.

**Hint.** Which character must the loop skip before it asks the set anything?

**Changed decision.** Basic case: one set for one group, and empty cells stay out of the set.

#### [Vary] Row And Column Scope (Author exercise)
<!-- id: hm-row-column-scope -->

**Prerequisites.** Row Duplicates above.

**Problem.** Let `board` be an `n` by `n` array of strings, with each character a digit from `'1'` to `'9'` or `'.'`. Return true when no digit occurs twice in any row and no digit occurs twice in any column. Blocks do not matter.

**Constraints.** The limits are:
- **Side** satisfies `1 <= n <= 9`, and every string has length `n`.
- **Characters** are `'1'` to `'9'` or `'.'`.
- **Sets** are one per row and one per column.
- **Answer** is a boolean.

**Example 1.** Input `board = ["12..", "..2.", ".3..", "...1"]`, output true.

**Example 2.** Input `board = ["1...", "2...", "1...", "...."]`, output false, because the digit 1 occurs twice in column 0.

**Hint.** How many sets does one cell need, and what must stay separate between rows and columns?

**Changed decision.** A cell now belongs to two groups, so each cell tests and updates two sets.

#### [Boundary] Box Identity (Author exercise)
<!-- id: hm-box-identity -->

**Prerequisites.** The two exercises above and the box index from this lesson.

**Problem.** Let `board` be an `n` by `n` array of strings, where `n` is a multiple of 3. The blocks are the 3 by 3 squares that tile the board. Return true when no digit occurs twice inside one block. Rows and columns do not matter.

**Constraints.** The limits are:
- **Side** is one of 3, 6 or 9, and every string has length `n`.
- **Characters** are `'1'` to `'9'` or `'.'`.
- **Block** key comes from `(r / 3, c / 3)` and must give different keys to different blocks.
- **Answer** is a boolean.

**Example 1.** Input `board = ["5..5..", "......", "......", "5..5..", "......", "......"]`, output true. The digit 5 occurs in four different blocks, and each block holds one 5.

**Example 2.** Input `board = ["5.....", "......", "..5...", "......", "......", "......"]`, output false, because both 5s lie in block `(0, 0)`.

**Hint.** What key do the cells `(0, 3)` and `(3, 0)` receive if the program uses `r / 3 + c / 3`?

**Changed decision.** The program derives a block key from the coordinates and must keep different blocks apart.

#### [Recognize] Valid Sudoku (LeetCode 36)
<!-- id: hm-valid-sudoku -->

**Prerequisites.** All three exercises above.

**Problem.** Let `board` be a 9 by 9 array of strings with digits `'1'` to `'9'` and `'.'` for empty cells. Return true when the filled cells break no rule: each row, each column and each 3 by 3 block holds each digit at most once. The board does not need to be solvable.

**Constraints.** The limits are:
- **Side** is exactly 9, with 9 characters in each string.
- **Characters** are `'1'` to `'9'` or `'.'`.
- **Scopes** are rows, columns and blocks, each with its own sets.
- **Answer** is a boolean.

**Example 1.** Input: `["1...5...9", ".5...9...", "..9...4..", "...5...9.", "5...9...4", ".9...4...", "..5...9..", "...9...4.", "9...4...8"]`, output true, although the digit 5 occurs in several rows.

**Example 2.** Input: the same board with row 1 replaced by `".51..9..."`, output false, because the new 1 shares block 0 with the 1 at `(0, 0)`.

**Hint.** Which of the three sets reports the conflict in the second example, and which two stay silent?

**Changed decision.** All three scopes work together, and each filled cell updates three sets with three different keys.
