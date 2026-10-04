<!-- lesson-kind: standard -->
<!-- lesson-id: board-constraints -->
## Board Constraints

<!-- stage: context -->
### The Stepping Stones Of Lake Ormer

The lake garden at Ormer lays flat stones across a shallow pond in a rectangular grid, and a gardener leads visitors from stone to stone, always stepping to a stone directly beside the one she stands on. A route must never use the same stone twice, because the stones are slippery and the second visit is a fall. To keep track, she carries a stick of chalk, draws a cross on each stone as she stands on it, and rubs the cross off with her sleeve the moment she steps back off it for good.

When a visitor asks whether a certain spelling can be traced across the lettered stones, she tries a route, and when the route fails she retraces it and tries another, rubbing off the crosses as she retreats. One summer a young helper stopped rubbing them off after a successful tour, and the next visitor was told that a perfectly good route did not exist.

<!-- stage: naive -->
### Give Every Step A Fresh Map

The safest way to remember which stones are used is to hand each step its own copy of the map. A call receives a grid of flags for the stones on the route so far, makes a new grid that also flags the stone it stands on, and gives that new grid to every neighbour it tries.

```java
static boolean spellsByCopies(String[] stones, String word) {
    int rows = stones.length, cols = stones[0].length();
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (walk(stones, word, r, c, 0, new boolean[rows][cols])) return true;
    return false;
}

private static boolean walk(String[] stones, String word, int r, int c, int k, boolean[][] used) {
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
```

No call can disturb the flags of another, so the answer is right for every grid, and the method is a sound oracle for the faster one.

<!-- stage: bottleneck -->
### Every Step Copies The Whole Pond

For a grid of R rows and C columns, each call that goes deeper copies R * C flags, so a route of L stones costs O(R * C) at every step on top of the walking itself. A search that makes thousands of calls spends nearly all of its time duplicating a map in which a single cell changed. On a thirty by thirty pond that is nine hundred flags copied for every stone stepped on, and the garbage of discarded copies fills the memory.

Only one fact about the map ever changes from one call to its child, which is that one more stone is in use. Everything the call needs to know about the grid is therefore the same single flag set and cleared again as the route advances and retreats, in O(1) per step. What makes that safe is the discipline that every flag set on the way forward is cleared on the way back, for failure and for success alike.

<!-- stage: insight -->
### Chalk On Entry, Rub Off On Exit

Keep one board of markers that represents the stones on the current route and no others. A **path marker** is a flag, or any other recorded value, attached to a cell or a column or a diagonal, which says that the cell is in use on the current path. A call checks the marker before moving to a cell, sets it on entering, explores from there, and then runs the **restore step** that clears or reinstates exactly what it set, before the call returns.

The restore step has to run on every exit. It is easy to clear the marker after a failed exploration and forget it when an exploration succeeds and the call wants to return the good news straight away. The safe shape stores the outcome in a variable, restores, and then returns the variable, so there is no exit between the mark and the restore.

Some searches keep the marker inside the data itself, for example by overwriting a letter on the grid with a character that cannot match anything. That **in-place mark** costs no extra memory, and the restore step must put the original letter back. Other searches avoid the work by keeping marker state in values that are passed down by value, such as integer bit sets; the callee then holds its own copy and the caller's copy is untouched, so nothing needs undoing.

A board constraint can also be spatial in a looser way than adjacency. For queens on a chessboard the relevant markers are the column and the two diagonals, so that a square is blocked when any of its three markers is set, and the same set-explore-restore discipline applies to those three.

The invariant is that on entry to each call the markers describe exactly the cells or lines used by the current path, and on exit they describe them again.

<!-- names: path marker, restore step, in-place mark -->

<!-- stage: variables -->
### Position, Letter Index And Markers

The pair `r` and `c` is the stone a call stands on, and `k` is the number of letters of the word already matched, which grows by one with each step. The grid itself is the board, and for the in-place version the character `#` in a cell means that the cell is on the current route. The local `saved` holds the original letter of the cell, and it lives in the call's own frame, so each level restores its own cell. The local `found` carries the outcome across the restore step. For queens, the three marker sets are one for columns and two for diagonals, each updated on placement and cleared when the placement is withdrawn.

<!-- stage: trace -->
### Tracing A Word On A Small Pond

The first trace looks for the word `aaba` on the grid with rows `aaa` and `baa`, scanning start cells from the top left. The cells are numbered row by row, so cell 3 is the first stone of the second row. The pointer `cell` is the stone being examined, and the variable `board` shows the markers, with a hash on each stone that is on the current route. Look at the rubbing off after each failed route, and at the final success, which still restores its own stone as it returns.

```trace
{"cells":["a","a","a","b","a","a"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"matched":1,"board":"#aa/baa","clean":"yes"},"note":"The stone at row 0, column 0 matches a and is marked with a hash, so 1 letters are matched."},{"at":{"cell":3},"vars":{"matched":1,"board":"#aa/baa","clean":"yes"},"note":"The stone at row 1, column 0 holds b, but letter 2 of the word is a, so this route fails here."},{"at":{"cell":1},"vars":{"matched":2,"board":"##a/baa","clean":"yes"},"note":"The stone at row 0, column 1 matches a and is marked with a hash, so 2 letters are matched."},{"at":{"cell":4},"vars":{"matched":2,"board":"##a/baa","clean":"yes"},"note":"The stone at row 1, column 1 holds a, but letter 3 of the word is b, so this route fails here."},{"at":{"cell":2},"vars":{"matched":2,"board":"##a/baa","clean":"yes"},"note":"The stone at row 0, column 2 holds a, but letter 3 of the word is b, so this route fails here."},{"at":{"cell":0},"vars":{"matched":2,"board":"##a/baa","clean":"yes"},"note":"The stone at row 0, column 0 holds #, but letter 3 of the word is b, so this route fails here."},{"at":{"cell":1},"vars":{"matched":1,"board":"#aa/baa","clean":"yes"},"note":"Every neighbour of the stone at row 0, column 1 has been tried or the route has succeeded, so its letter a is put back and the board reads #aa/baa."},{"at":{"cell":0},"vars":{"matched":0,"board":"aaa/baa","clean":"yes"},"note":"Every neighbour of the stone at row 0, column 0 has been tried or the route has succeeded, so its letter a is put back and the board reads aaa/baa."},{"at":{"cell":1},"vars":{"matched":1,"board":"a#a/baa","clean":"yes"},"note":"The stone at row 0, column 1 matches a and is marked with a hash, so 1 letters are matched."},{"at":{"cell":4},"vars":{"matched":2,"board":"a#a/b#a","clean":"yes"},"note":"The stone at row 1, column 1 matches a and is marked with a hash, so 2 letters are matched."},{"at":{"cell":1},"vars":{"matched":2,"board":"a#a/b#a","clean":"yes"},"note":"The stone at row 0, column 1 holds #, but letter 3 of the word is b, so this route fails here."},{"at":{"cell":5},"vars":{"matched":2,"board":"a#a/b#a","clean":"yes"},"note":"The stone at row 1, column 2 holds a, but letter 3 of the word is b, so this route fails here."},{"at":{"cell":3},"vars":{"matched":3,"board":"a#a/##a","clean":"yes"},"note":"The stone at row 1, column 0 matches b and is marked with a hash, so 3 letters are matched."},{"at":{"cell":0},"vars":{"matched":4,"board":"a#a/##a","clean":"yes"},"note":"The stone at row 0, column 0 holds a, the last letter, so the word is traced."},{"at":{"cell":3},"vars":{"matched":2,"board":"a#a/b#a","clean":"yes"},"note":"Every neighbour of the stone at row 1, column 0 has been tried or the route has succeeded, so its letter b is put back and the board reads a#a/b#a."},{"at":{"cell":4},"vars":{"matched":1,"board":"a#a/baa","clean":"yes"},"note":"Every neighbour of the stone at row 1, column 1 has been tried or the route has succeeded, so its letter a is put back and the board reads a#a/baa."},{"at":{"cell":1},"vars":{"matched":0,"board":"aaa/baa","clean":"yes"},"note":"Every neighbour of the stone at row 0, column 1 has been tried or the route has succeeded, so its letter a is put back and the board reads aaa/baa."}]}
```

The second trace is the helper's mistake. It looks for `bba` on the rows `aaa` and `bba` and scans every start cell, but a successful search returns without rubbing off its markers. The variable `board` shows the stones, and `clean` turns to no when markers are left on the board after a search has ended. The second start cell then finds a hash where it needs a letter, so a route that exists is reported as missing.

```trace
{"cells":["a","a","a","b","b","a"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"matched":0,"board":"aaa/bba","clean":"yes"},"note":"The stone at row 0, column 0 holds a, but letter 1 of the word is b, so this route fails here."},{"at":{"cell":1},"vars":{"matched":0,"board":"aaa/bba","clean":"yes"},"note":"The stone at row 0, column 1 holds a, but letter 1 of the word is b, so this route fails here."},{"at":{"cell":2},"vars":{"matched":0,"board":"aaa/bba","clean":"yes"},"note":"The stone at row 0, column 2 holds a, but letter 1 of the word is b, so this route fails here."},{"at":{"cell":3},"vars":{"matched":1,"board":"aaa/#ba","clean":"yes"},"note":"The stone at row 1, column 0 matches b and is marked with a hash, so 1 letters are matched."},{"at":{"cell":0},"vars":{"matched":1,"board":"aaa/#ba","clean":"yes"},"note":"The stone at row 0, column 0 holds a, but letter 2 of the word is b, so this route fails here."},{"at":{"cell":4},"vars":{"matched":2,"board":"aaa/##a","clean":"yes"},"note":"The stone at row 1, column 1 matches b and is marked with a hash, so 2 letters are matched."},{"at":{"cell":1},"vars":{"matched":3,"board":"aaa/##a","clean":"yes"},"note":"The stone at row 0, column 1 holds a, the last letter, so the word is traced."},{"at":{"cell":4},"vars":{"matched":2,"board":"aaa/##a","clean":"no"},"note":"The route succeeded, and the careless code returns now without restoring the stone at row 1, column 1, so the hash stays on the board."},{"at":{"cell":3},"vars":{"matched":1,"board":"aaa/##a","clean":"no"},"note":"The route succeeded, and the careless code returns now without restoring the stone at row 1, column 0, so the hash stays on the board."},{"at":{"cell":4},"vars":{"matched":0,"board":"aaa/##a","clean":"no"},"note":"The stone at row 1, column 1 holds #, but letter 1 of the word is b, so this route fails here."},{"at":{"cell":5},"vars":{"matched":0,"board":"aaa/##a","clean":"no"},"note":"The stone at row 1, column 2 holds a, but letter 1 of the word is b, so this route fails here."}]}
```

<!-- stage: code -->
### Mark In Place And Restore Before Returning

```java
static boolean exists(char[][] board, String word) {
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++)
            if (search(board, word, r, c, 0)) return true;
    return false;
}

private static boolean search(char[][] b, String w, int r, int c, int k) {
    if (r < 0 || c < 0 || r >= b.length || c >= b[0].length) return false;
    if (b[r][c] != w.charAt(k)) return false;       // also rejects '#'
    if (k == w.length() - 1) return true;
    char saved = b[r][c];
    b[r][c] = '#';                                  // in-place mark
    boolean found = search(b, w, r + 1, c, k + 1) || search(b, w, r - 1, c, k + 1)
                 || search(b, w, r, c + 1, k + 1) || search(b, w, r, c - 1, k + 1);
    b[r][c] = saved;                                // restore on every exit
    return found;
}
```

The marker character must be one that the word cannot contain, which holds for lowercase words. The short-circuit `||` stops at the first success, and that is safe only because the restore comes after the whole expression and not inside it. A copy made with `board.clone()` is shallow and shares its row arrays with the original, so a search on the copy would still change the caller's board. The work is bounded by O(R * C * 3^L) calls for a word of length L, since each step has at most three unused neighbours.

<!-- stage: applicability -->
### Choices That Occupy Space

Use marker state when choices occupy positions and later choices are limited by earlier ones: paths on a grid that may not revisit a cell, words traced through letters, queens on a board, and tiles laid in a floor. The invariant to protect is that the markers describe exactly the current path, so after any exit from a call the board is what it was on entry.

The nearest false friend is a visited set that is never cleared. For a search that asks only whether one cell is reachable, such a set is correct and quick, since reaching a cell once is enough. For a search over routes it blocks a stone for every sibling route after the first one has used it, and routes that need that stone are never found. The question to ask is whether the answer depends on the whole route or only on which cells can be reached. A second false friend is the copy-per-step method of the naive stage, which is correct and keeps no state to restore, and which is worth using only on a very small grid.

Do not mutate a board that the caller still owns unless restoring it is guaranteed on every path of control, including exceptions and early successes. In Java, remember that a shallow clone of a two-dimensional array shares its rows, that the restore must come after a short-circuited expression and not inside it, and that bit sets passed by value need no restore at all.

<!-- stage: exercises -->
### Exercises

#### [Build] Four-Direction Path (Author exercise)
<!-- id: bt-grid-paths -->

**Prerequisites.** The working path with its undo step, and the idea of a marker for a cell on the route.

**Problem.** A grid is given as strings of `.` for an open cell and `#` for a blocked one. Count the routes from the top-left cell to the bottom-right cell that move one step up, down, left or right at a time, enter only open cells, and never use a cell twice. If either corner is blocked the count is zero.

**Constraints.** The grid has between 1 and 4 rows and between 1 and 4 columns, and the corner cells may be blocked.

**Example 1.** Input `grid = ["...", "...", "..."]`, output `12`.

**Example 2.** Input `grid = ["...", ".#.", "..."]`, output `2`.

**Hint.** Which cell must be unmarked after all four directions have been tried, and does it matter whether any of them reached the corner?

**Changed decision.** A cell is marked on entry and unmarked after all four neighbours are explored, so the marks always describe the route being walked.

#### [Vary] Word Search (LeetCode 79)
<!-- id: bt-word-search -->

**Prerequisites.** The Four-Direction Path rung.

**Problem.** Given a grid of lowercase letters and a word, decide whether the word can be traced through the grid by stepping to a neighbour directly above, below, left or right, with each cell used at most once in one trace. Use the in-place marker `#` and restore each letter before returning.

**Constraints.** The grid has 1 to 5 rows and 1 to 5 columns, and the word has 1 to 8 lowercase letters.

**Example 1.** Input `board = ["cat", "oxe", "dgs"]`, `word = "cod"`, output `true`.

**Example 2.** Input `board = ["aa"]`, `word = "aaa"`, output `false`.

**Hint.** What would happen to the second example if a cell could be used again after it had been used for the first letter?

**Changed decision.** A letter must match at each step, so the marker also doubles as a mismatch, since the marker character equals no letter of the word.

#### [Boundary] Cell Reuse And Early Success (Author exercise)
<!-- id: bt-reuse-early-success -->

**Prerequisites.** The Word Search rung.

**Problem.** Given a grid of lowercase letters and a word, return every start cell from which the word can be traced, as `[row, column]` pairs in row-major order. The same grid object is used for every start cell, and the search marks cells in place, so each search must leave the grid exactly as it found it, even when it succeeds at once.

**Constraints.** The grid has 1 to 4 rows and 1 to 4 columns, and the word has 1 to 6 lowercase letters.

**Example 1.** Input `board = ["aaa", "bba"]`, `word = "bba"`, output `[[1, 0], [1, 1]]`.

**Example 2.** Input `board = ["ab"]`, `word = "ba"`, output `[[0, 1]]`.

**Hint.** If a successful search returns before restoring, which later start cell is the first to see a changed grid?

**Changed decision.** The restore step moves out of the failure branch and runs after every exploration, so success and failure leave the same grid behind.

#### [Recognize] N-Queens (LeetCode 51)
<!-- id: bt-queens-boards -->

**Prerequisites.** The Cell Reuse And Early Success rung, and the column and diagonal flags met in the pruning lesson.

**Problem.** Place `n` queens on an `n` by `n` board so that no two share a row, column or diagonal, and return every board as a list of `n` strings with `Q` for a queen and `.` for an empty square. Fill rows from the top, try columns from left to right, and keep the occupied columns and diagonals as integer bit sets that are passed down by value.

**Constraints.** 1 <= n <= 9, so the largest board has 352 solutions.

**Example 1.** Input `n = 4`, output `[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]`.

**Example 2.** Input `n = 1`, output `[["Q"]]`.

**Hint.** Which of the three marker sets need an explicit restore when they are passed by value, and which array does need one?

**Changed decision.** Spatial adjacency gives way to three occupancy sets, and the by-value bit sets restore themselves, so only the placement record is overwritten.
