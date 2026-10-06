<!-- lesson-kind: standard -->
<!-- lesson-id: board-constraints -->
## Mark Cells On A Grid

<!-- stage: context -->
### Why The App Rejects A Valid Word

A puzzle app checks whether a word appears on a letter grid. A spelling moves between touching cells. A cell may appear once in one spelling. The developer keeps one shared grid of flags and sets the flag of a cell when the search enters it. The grid `aa` over `ab` contains the word `aaa`, because the cells at the top right, the top left and the bottom left spell it in that order. The app answers that the word is missing.

The first attempts of the search entered cells and left their flags set. Later attempts then found those cells blocked. This lesson asks which cells a search must block at each step, and when it must release them.

<!-- stage: naive -->
### Copying The Flags For Every Step

The direct plan avoids a shared grid of flags. Each call copies the flags of its caller, sets one flag in the copy and passes the copy to the neighbours.

```java
static boolean find(char[][] b, String w, int r, int c, int k, boolean[][] seen) {
    if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;   // outside the board
    if (seen[r][c] || b[r][c] != w.charAt(k)) return false;                  // cell in use or wrong letter
    if (k == w.length() - 1) return true;                                    // every letter matched
    boolean[][] next = new boolean[b.length][];
    for (int i = 0; i < b.length; i++) next[i] = seen[i].clone();           // a full copy for each step
    next[r][c] = true;
    return find(b, w, r - 1, c, k + 1, next) || find(b, w, r + 1, c, k + 1, next)
        || find(b, w, r, c - 1, k + 1, next) || find(b, w, r, c + 1, k + 1, next);
}
```

The method answers correctly, because no branch sees the flags of another branch. Each call copies the whole grid of flags.

<!-- stage: bottleneck -->
### Counting The Copied Flags

```predict
The board has 6 rows and 6 columns, and the word has 10 letters. A call can enter at most 3 neighbours after the first letter. About how many flags do the copies move, at most?

One start cell makes at most 4 * 3^9 = 78,732 calls. The 36 start cells make at most 2.8 million calls. Each call copies 36 flags, so the copies move about 102 million flags. A search that sets and clears one flag per call writes about 2.8 million flags.
```

The copying plan costs O(R * C) extra time and memory per call, for a board with `R` rows and `C` columns. The flag grid does not change between a call and its caller except for one cell. The copy is much larger than the difference.

A single shared grid would do the same work with one write per step. The shared grid is correct only under one rule. Every flag that a call sets is cleared before the call hands control back. The next sibling branch then starts from the same grid as the first one.

<!-- stage: insight -->
### Setting A Flag And Clearing It

#### Marking The Cells Of The Path

A **path mark** is a flag on a cell that says the cell belongs to the current path. A call that enters a cell sets its path mark. The legal moves of a call are the touching cells that lie inside the board, carry no path mark and match the next letter. At every moment, the marked cells are exactly the cells of the calls on the stack, so the number of marks equals the depth.

#### Clearing The Mark On The Way Out

The **unmark step** clears the path mark of the cell after the call has explored all its neighbours. It restores the grid for the sibling branches, which may reach the same cell by a different route and need it unblocked. A mark that stays after the call returns blocks that route, and the search misses words that exist. The invariant is that on exit of a call, the grid of marks equals the grid on entry.

#### Returning Early Without Leaking

A **short-circuit return** leaves the loop as soon as one neighbour succeeds. The operator `||` in Java does this, and it skips the remaining neighbours. A return that jumps out before the unmark step leaves the cell marked. The call must store the result in a local variable, run the unmark step and then return the variable. The same rule holds when the search marks a cell by overwriting its letter in the board: the call restores the saved letter before it returns on every path.

<!-- names: path mark, unmark step, short-circuit return -->

<!-- stage: variables -->
### The Pieces Of State

Four pieces of state describe a call.

- **Cell** is the pair of a row `r` and a column `c` that the call tries to enter.
- **Letter index k** is the number of letters of the word that the path has matched.
- **Path marks** are one boolean flag for each cell, true exactly for the cells of the active calls.
- **Result** is the local boolean that the call returns after the unmark step.

Entering a cell sets its flag, and the call passes `k + 1` to each neighbour. The call clears the flag before it returns, whether the result is true or false.

<!-- stage: trace -->
### Following The Marks Through A Small Board

#### Finding The Word With Unmarks

The first trace searches the board `aa` over `ab` for the word `aaa`. The cells are numbered row by row. Cells `0` and `1` form the top row, and cells `2` and `3` form the bottom row. The pointer `cell` marks the cell that the step enters or leaves. The variable `marks` counts the flags that are set after the step.

The search starts at cell 0 and enters cell 2 below it. Neighbours of cell 2 are the marked cell 0 and the letter `b` at cell 3, so the branch fails and the unmark step clears cell 2. The search then enters cell 1, which has no neighbour that matches, and clears cell 1 and cell 0. Next, the search starts at cell 1, enters cell 0, and enters cell 2, which completes the word.

#### Tracing A Mark That Stays

The second trace leaves the flags set after each failed branch. The first start at cell 0 enters cell 2, fails and leaves cells 0, 2 and 1 marked. The next start at cell 1 finds its own cell marked and stops at once. The search reports that the word is missing.

#### Stepping Through Both Runs

```trace
{"cells":["a","a","a","b"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"marks":1,"k":1},"note":"The search enters cell 0, which holds a, and sets its mark."},{"at":{"cell":2},"vars":{"marks":2,"k":2},"note":"The search enters cell 2, which holds a, and sets its mark."},{"at":{"cell":2},"vars":{"marks":1,"k":1},"note":"No neighbour of cell 2 completes the word, so the unmark step clears its mark."},{"at":{"cell":1},"vars":{"marks":2,"k":2},"note":"The search enters cell 1, which holds a, and sets its mark."},{"at":{"cell":1},"vars":{"marks":1,"k":1},"note":"No neighbour of cell 1 completes the word, so the unmark step clears its mark."},{"at":{"cell":0},"vars":{"marks":0,"k":0},"note":"No neighbour of cell 0 completes the word, so the unmark step clears its mark."},{"at":{"cell":1},"vars":{"marks":1,"k":1},"note":"The search enters cell 1, which holds a, and sets its mark."},{"at":{"cell":0},"vars":{"marks":2,"k":2},"note":"The search enters cell 0, which holds a, and sets its mark."},{"at":{"cell":2},"vars":{"marks":2,"k":3},"note":"The cell 2 holds a, which is the last letter of the word, so the search succeeds."}]}
```

```trace
{"cells":["a","a","a","b"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"marks":1,"k":1},"note":"The search enters cell 0, which holds a, and sets its mark."},{"at":{"cell":2},"vars":{"marks":2,"k":2},"note":"The search enters cell 2, which holds a, and sets its mark."},{"at":{"cell":1},"vars":{"marks":3,"k":2},"note":"The search enters cell 1, which holds a, and sets its mark."},{"at":{"cell":1},"vars":{"marks":3,"k":0},"note":"The start at cell 1 finds its own mark still set, so it stops at once."},{"at":{"cell":2},"vars":{"marks":3,"k":0},"note":"The start at cell 2 finds its own mark still set, so it stops at once."}]}
```

<!-- stage: code -->
### Writing The Search In Java

#### Word Search With Path Marks

The method below returns whether the word appears, and it clears every mark it sets, whatever the result is.

```java
static boolean exists(char[][] b, String w) {
    boolean[][] on = new boolean[b.length][b[0].length];             // path marks, all false at the start
    for (int r = 0; r < b.length; r++)
        for (int c = 0; c < b[0].length; c++)
            if (go(b, w, r, c, 0, on)) return true;                  // every cell may start the word
    return false;
}

static boolean go(char[][] b, String w, int r, int c, int k, boolean[][] on) {
    if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;   // outside the board
    if (on[r][c] || b[r][c] != w.charAt(k)) return false;                    // cell in use or wrong letter
    if (k == w.length() - 1) return true;                                    // the last letter matches
    on[r][c] = true;                                                         // choose: mark the cell
    boolean found = go(b, w, r - 1, c, k + 1, on) || go(b, w, r + 1, c, k + 1, on)
                 || go(b, w, r, c - 1, k + 1, on) || go(b, w, r, c + 1, k + 1, on);
    on[r][c] = false;                                                        // undo: clear the mark first
    return found;                                                            // then return the stored result
}
```

#### Costs Of The Search

A word of `L` letters makes at most 4 * 3^(L-1) calls from one start cell, so the time is O(R * C * 3^L). The marks use O(R * C) memory and the stack uses O(L). The search stores no list, so it makes no copy.

<!-- stage: applicability -->
### Recognizing A Spatial Constraint

#### Spotting The Pattern

The cue is a choice that occupies a place and blocks later choices in nearby or related places. The invariant is that the marks hold exactly the places of the current path and return to their earlier state when a call exits.

#### Finding The False Friend

The false friend is a global visited mark that no call clears. It looks like the visited set of a graph search, which marks a cell once and keeps the mark. A graph search asks whether a cell is reachable, and a path search asks whether a path exists, so the path search must release the cell. A second false friend is a return that skips the unmark step on success.

#### Recognizing The No-Go Cases

The path marks do not fit when the question is only whether a cell is reachable, since a graph search with permanent marks answers that in O(R * C). They do not fit when many words share a prefix and the board is large, because a prefix tree prunes them together. A board with many open cells and a long word makes the number of paths grow like 3^L.

<!-- stage: exercises -->
### Exercises

#### [Build] Four-Direction Path (Author exercise)
<!-- id: bt-four-direction-path -->

**Prerequisites.** The path marks and the unmark step of this lesson.

**Problem.** The grid `g` has rows of the characters `.` for an open cell and `#` for a blocked cell. A path starts at the top-left cell and ends at the bottom-right cell. Each move goes to a touching cell above, below, left or right, and no cell appears twice. Return the number of different paths. A blocked start or a blocked end gives 0. A grid of one open cell has one path.

**Constraints.** The limits are:
- **Size** is `1 <= rows, columns <= 5`.
- **Characters** are `.` and `#` only.
- **Return** is an `int`.
- **Mutation** does not occur; `g` keeps its contents.

**Example 1.** Input `g = ["..", ".."]`, output 2.

**Example 2.** Input `g = ["...", ".#.", "..."]`, output 2.

**Hint.** Which cells does a call mark before it visits the neighbours? What does the call do with the mark after the count returns?

**Changed decision.** The search counts every path to the end cell and keeps going after a success, so the unmark step runs after each success too.

#### [Vary] Word Search (LeetCode 79)
<!-- id: bt-word-search-marks -->

**Prerequisites.** The previous exercise.

**Problem.** Given a board of lowercase letters and a word, return true when the word appears on the board. A path of cells spells the word, and each move goes to the cell above, below, left or right. Each cell may appear at most once in one path. Mark cells in a separate boolean grid, and leave the board unchanged.

**Constraints.** The limits are:
- **Size** is `1 <= rows, columns <= 6`.
- **Length** of the word is `1 <= word.length() <= 12`.
- **Characters** are lowercase English letters.
- **Mutation** does not occur; the board keeps its letters.

**Example 1.** Input `board = ["ab", "cd"]`, `word = "abdc"`, output true.

**Example 2.** Input `board = ["ab", "cd"]`, `word = "abcd"`, output false.

**Hint.** Which three tests reject a cell before the call marks it? Where do the touching cells b and c of the second example fail?

**Changed decision.** The search stops at the first success and returns a boolean, so the call stores the result before the unmark step.

#### [Boundary] Cell Reuse And Early Success (Author exercise)
<!-- id: bt-cell-reuse-early-success -->

**Prerequisites.** The two exercises above.

**Problem.** Solve the word search of the previous exercise again, and mark a cell by overwriting its letter in the board with `#`. The method restores every letter it overwrote before it returns, whether the result is true or false. After the call, the board holds exactly the letters it held before the call. A cell may not appear twice in one path.

**Constraints.** The limits are:
- **Size** is `1 <= rows, columns <= 6`.
- **Length** of the word is `1 <= word.length() <= 12`.
- **Characters** are lowercase English letters, so `#` never occurs in the input.
- **Mutation** may change the board inside the call, and the call restores it at the end.

**Example 1.** Input `board = ["aa"]`, `word = "aaa"`, output false, and the board stays `["aa"]`.

**Example 2.** Input `board = ["ab"]`, `word = "ba"`, output true, and the board stays `["ab"]`.

**Hint.** Which letter must the call save before it writes `#`? Which return statements run after the restore?

**Changed decision.** The mark lives in the board itself, so a missed restore damages the input as well as the search.

#### [Recognize] N-Queens (LeetCode 51)
<!-- id: bt-n-queens-boards -->

**Prerequisites.** The previous three exercises, and the N-Queens count of the lesson on provable pruning.

**Problem.** Place `n` queens on an `n` by `n` board so that no two queens share a row, a column or a diagonal. Return every placement as a list of `n` strings of length `n`, where `Q` marks a queen and `.` marks an empty cell. The search fills the rows from top to bottom and tries the columns from left to right, and the result keeps that order.

**Constraints.** The limits are:
- **Size** is `1 <= n <= 8`.
- **Characters** are `Q` and `.` only.
- **Count** of boards is 0 for `n = 2` and `n = 3`.
- **Marks** for the columns and the two diagonals are boolean arrays that return to false after the call.

**Example 1.** Input `n = 4`, output `[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]`.

**Example 2.** Input `n = 1`, output `[["Q"]]`.

**Hint.** Which values of `r - c` and `r + c` identify the two diagonals of a cell? Which state must the call clear after it explores the next row?

**Changed decision.** Touching cells give way to three marks, one for the column and one for each diagonal, and the call stores a board at the last row.
