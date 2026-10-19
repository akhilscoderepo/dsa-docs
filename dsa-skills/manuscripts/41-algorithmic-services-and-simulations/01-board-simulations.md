<!-- lesson-kind: standard -->
<!-- lesson-id: board-simulations -->
## Move Pieces On A Board

<!-- stage: context -->
### A Win Check That Rereads The Board

A server hosts tic-tac-toe on a 1000 by 1000 board, and a player wins by filling one row, column or diagonal with their marks. After every move the server rereads the board to decide whether the game ended. Each move makes it read about four million cells, and almost none of them changed since the last move.

A snake game has the same shape. The code must reject a move into the snake's own body, so it searches a list of body cells for the new head. That search takes time proportional to the snake's length, and the game slows down as the player scores.

Both games ask the same question. How can a call decide whether a move wins or fails by looking only at what the move changed? This lesson answers it for a board of marks, a snake on a grid and a robot that walks along the edge of a rectangle.

<!-- stage: naive -->
### Scanning Every Line After Each Move

The direct design stores the owner of each cell in a grid. After placing a mark it scans every row, every column and both diagonals for each player.

```java
final class ScanBoard {
    private final int n;
    private final int[][] grid;                               // 0 is empty, otherwise the player id

    ScanBoard(int n) { this.n = n; this.grid = new int[n][n]; }

    int move(int row, int col, int player) {
        if (grid[row][col] != 0) return -1;                   // a taken cell is illegal
        grid[row][col] = player;
        for (int p = 1; p <= 2; p++) {                        // test both players
            boolean diag = true, anti = true;
            for (int i = 0; i < n; i++) {
                boolean rowFull = true, colFull = true;
                for (int j = 0; j < n; j++) {                 // two reads for every inner step
                    if (grid[i][j] != p) rowFull = false;
                    if (grid[j][i] != p) colFull = false;
                }
                if (rowFull || colFull) return p;
                if (grid[i][i] != p) diag = false;
                if (grid[i][n - 1 - i] != p) anti = false;
            }
            if (diag || anti) return p;
        }
        return 0;                                             // no line is full yet
    }
}
```

The answers are correct. The cost is the problem.

```predict
The board is 1000 by 1000 and a player places one mark. About how many cells does the scan read, and how many of those cells could change the answer?

The two nested loops read two cells per inner step for two players, which is about 4 * 1000 * 1000 = four million reads. Only the marked cell's row, its column and the two diagonals can change the answer, which is at most 4000 cells. A line that does not contain the new mark has exactly the same cells as before the move.
```

<!-- stage: bottleneck -->
### Rereading Cells That Did Not Change

The scan costs O(n^2) per move on an n by n board, while a single move changes one cell. Every line that misses the new cell holds the same marks it held one call earlier, so the scan repeats work whose answer is already known. A million moves on the 1000 by 1000 board read four trillion cells in total.

The snake search has the same defect. It costs O(L) per move for a snake of length L, because it compares the new head against every body cell. The body changes by one cell at each end per move, and the search ignores that.

A third cost is correctness. A move changes several things at once, such as the head, the tail, the score and the collision answer. If the code writes some of them and then discovers an illegal move, the board is left half changed. The order of the checks and the writes matters as much as their speed.

<!-- stage: insight -->
### Count Per Line And Track Taken Cells

Keep one authoritative representation of the position, and derive every other view from it inside the same call. A derived view answers the question that the naive scan answered by rereading, and it changes by a small amount per move.

#### Counting Marks Per Line

A **counter** is an integer kept for one line of the board. An n by n board has n rows, n columns and 2 diagonals, so it has 2n + 2 counters. Player 1 adds 1 to a counter and player 2 adds -1. Each cell contributes exactly 1 or -1, so a line holds n marks of one player exactly when its counter has absolute value n.

A move at (row, col) changes at most four counters: the row, the column, the main diagonal when row equals col, and the anti-diagonal when row plus col equals n - 1. The win check reads those four values and costs O(1).

#### Tracking Taken Cells In Order

The snake needs two views. The body in order, from head to tail, is authoritative because order decides which cell is released next. A deque holds it. The **occupancy set** is a set of the body cells, and it is derived from the deque. It answers "is this cell taken" in O(1).

The order of updates carries the rule. A move that does not eat releases the tail before the head enters, so the head may enter the cell that the tail leaves. A move that eats keeps the tail. The call therefore checks first, using the occupancy set and the tail cell, and it writes nothing until the move is known to be legal.

#### Reducing Steps Around A Loop

The robot visits only the cells on the edge of a rectangle, and those cells form a loop. The **cycle length** is the number of cells on that loop, which is 2 * (width + height) - 4. After that many steps the robot stands on the same cell again.

One position index along the loop is therefore enough, and a call with `num` steps adds `num` modulo the cycle length to it. The cell follows from the index. The direction follows from the index except at index 0, where it depends on whether the robot has ever moved.

The invariant is that the authoritative position and every derived view agree after each accepted move, and a rejected move changes nothing. The target is O(1) per call for the board, the snake and the robot.

<!-- names: counter, occupancy set, cycle length -->

<!-- stage: variables -->
### State Behind Each Move

The contract is bounded and held in memory. One object owns one board, calls arrive one at a time, and a rejected call leaves every field unchanged.

- **Owner grid** is the authoritative record of which player marked each cell.
- **Line counters** are the derived signed sums for rows, columns and the two diagonals.
- **Body deque** is the authoritative snake, stored from head to tail.
- **Occupancy set** is the derived set of cells covered by the body deque.
- **Loop index** is the authoritative position of the robot along the edge, counted from the start corner.
- **Moved flag** records whether the robot has taken at least one step, because direction at index 0 depends on it.

<!-- stage: trace -->
### Following Moves On A Board

#### Counting Marks In A Small Game

The first trace plays tic-tac-toe on a 3 by 3 board. The pointer `call` sits on the latest move, and each step shows the sums of the three rows, the three columns and the two diagonals. Player 1 adds 1 and player 2 adds -1.

```trace
{"cells":["(1,1) p1","(1,1) p2","(0,0) p2","(0,1) p1","(2,2) p2","(2,1) p1","(1,0) p2"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"rows":"0,1,0","cols":"0,1,0","diag":"1","anti":"1","result":"0"},"note":"Call 0: player 1 marks (1,1), which changes the row 1 and column 1 sums and the main diagonal sum and the anti-diagonal sum. The call returns 0."},{"at":{"call":1},"vars":{"rows":"0,1,0","cols":"0,1,0","diag":"1","anti":"1","result":"-1"},"note":"Call 1: cell (1,1) already holds a mark, so the call returns -1 and every sum stays as it was."},{"at":{"call":2},"vars":{"rows":"-1,1,0","cols":"-1,1,0","diag":"0","anti":"1","result":"0"},"note":"Call 2: player 2 marks (0,0), which changes the row 0 and column 0 sums and the main diagonal sum. The call returns 0."},{"at":{"call":3},"vars":{"rows":"0,1,0","cols":"-1,2,0","diag":"0","anti":"1","result":"0"},"note":"Call 3: player 1 marks (0,1), which changes the row 0 and column 1 sums. The call returns 0."},{"at":{"call":4},"vars":{"rows":"0,1,-1","cols":"-1,2,-1","diag":"-1","anti":"1","result":"0"},"note":"Call 4: player 2 marks (2,2), which changes the row 2 and column 2 sums and the main diagonal sum. The call returns 0."},{"at":{"call":5},"vars":{"rows":"0,1,0","cols":"-1,3,-1","diag":"-1","anti":"1","result":"1"},"note":"Call 5: player 1 marks (2,1), which changes the row 2 and column 1 sums. The call returns 1. A sum reaches 3 in absolute value, so player 1 wins."},{"at":{"call":6},"vars":{"rows":"0,1,0","cols":"-1,3,-1","diag":"-1","anti":"1","result":"-1"},"note":"Call 6: the game is already won, so the call returns -1 and every sum stays as it was."}]}
```

Call 1 targets the cell that player 1 already holds, so it returns -1 and every sum stays as it was. Call 4 leaves the main diagonal sum at -1, because player 2 owns two corners and player 1 owns the center. Call 5 completes column 1 and wins, and call 6 returns -1 because the game is over.

#### A Snake That Follows Its Tail

The second trace moves a snake on a 3 by 3 grid with three pieces of food. Each step lists the body from tail to head, where a cell is written as its row digit and then its column digit, and it shows the score.

```trace
{"cells":["R","D","L","U","D","R"],"pointers":["call"],"steps":[{"at":{"call":0},"vars":{"body":"00 01","score":"1","result":"1"},"note":"Call 0: the head enters the food cell (0,1), the tail stays and the score becomes 1."},{"at":{"call":1},"vars":{"body":"00 01 11","score":"2","result":"2"},"note":"Call 1: the head enters the food cell (1,1), the tail stays and the score becomes 2."},{"at":{"call":2},"vars":{"body":"00 01 11 10","score":"3","result":"3"},"note":"Call 2: the head enters the food cell (1,0), the tail stays and the score becomes 3."},{"at":{"call":3},"vars":{"body":"01 11 10 00","score":"3","result":"3"},"note":"Call 3: the head enters (0,0), where the tail was. The move does not eat, so the tail leaves first and the move is legal."},{"at":{"call":4},"vars":{"body":"01 11 10 00","score":"3","result":"-1"},"note":"Call 4: the head would enter (1,0), which a body segment other than a released tail holds, so the game ends and the body stays as it was."},{"at":{"call":5},"vars":{"body":"01 11 10 00","score":"3","result":"-1"},"note":"Call 5: the game is over, so the call returns -1 and writes nothing."}]}
```

Call 3 moves the head onto the cell that the tail holds. The move does not eat, so the tail leaves first and the move is legal. Call 4 aims at a cell held by a middle body segment, so it ends the game and writes nothing. Call 5 returns -1 because the game is over.

<!-- stage: code -->
### Moves That Check Before Writing

The first class keeps one signed counter per line and decides the winner from at most four of them. In the code, `line` holds the line counters and `used` holds the owner grid, reduced to a flag because this class only asks whether a cell is taken.

```java
final class LineCounts {
    private final int n;
    private final int[] line;                                 // rows, then columns, then main and anti diagonal
    private final boolean[] used;                             // authoritative: which cells hold a mark
    private boolean over;

    LineCounts(int n) { this.n = n; this.line = new int[2 * n + 2]; this.used = new boolean[n * n]; }

    int move(int r, int c, int player) {
        if (over || r < 0 || c < 0 || r >= n || c >= n || used[r * n + c]) return -1;   // validate before any write
        used[r * n + c] = true;
        int d = player == 1 ? 1 : -1;                         // the sign of this player
        line[r] += d;
        line[n + c] += d;
        if (r == c) line[2 * n] += d;
        if (r + c == n - 1) line[2 * n + 1] += d;
        if (Math.abs(line[r]) == n || Math.abs(line[n + c]) == n
                || Math.abs(line[2 * n]) == n || Math.abs(line[2 * n + 1]) == n) {
            over = true;                                      // a full line ends the game
            return player;
        }
        return 0;
    }
}
```

The second class moves a snake. It reads the tail cell to judge the move, and it changes the deque and the occupancy set only after the judgment.

```java
final class SnakeMove {
    private final int rows, cols;
    private final Deque<Integer> body = new ArrayDeque<>();   // head first, tail last
    private final Set<Integer> occupancySet = new HashSet<>();
    private boolean over;

    SnakeMove(int rows, int cols) {
        this.rows = rows; this.cols = cols;
        body.addFirst(0); occupancySet.add(0);
    }

    /** Returns false when the move ends the game; eats says whether the new cell holds food. */
    boolean advance(int dr, int dc, boolean eats) {
        if (over) return false;
        int head = body.peekFirst();
        int r = head / cols + dr, c = head % cols + dc;
        if (r < 0 || c < 0 || r >= rows || c >= cols) { over = true; return false; }
        int cell = r * cols + c;
        int tail = body.peekLast();
        boolean blocked = occupancySet.contains(cell) && (eats || cell != tail);   // the tail cell is free unless the snake grows
        if (blocked) { over = true; return false; }
        if (!eats) { body.pollLast(); occupancySet.remove(tail); }                 // release the tail first
        body.addFirst(cell);
        occupancySet.add(cell);                                                    // the head enters last
        return true;
    }
}
```

Each call costs O(1) expected time. The snake class stores the body twice, so its space is O(L) for a snake of length L.

The robot needs only a loop index and a moved flag, so its calls also cost O(1).

```java
final class LoopRobot {
    private final int w, h, cycle;
    private int pos;                                          // loop index counted from the start corner
    private boolean moved;                                    // direction at index 0 depends on this flag

    LoopRobot(int w, int h) { this.w = w; this.h = h; this.cycle = 2 * (w + h) - 4; }

    void step(int num) {
        if (num == 0) return;                                 // step(0) changes nothing
        moved = true;
        pos = (int) ((pos + (long) num) % cycle);             // one position index covers any number of laps
    }

    String dir() {
        if (pos == 0) return moved ? "South" : "East";        // back at the start corner after a lap
        if (pos <= w - 1) return "East";
        if (pos <= w + h - 2) return "North";
        if (pos <= 2 * w + h - 3) return "West";
        return "South";
    }
}
```

The direction is the part that needs the flag. The cell follows from the same index ranges, and the exercise asks for it.

<!-- stage: applicability -->
### Commands That Change Positions

#### Recognizing The Pattern

The cue is a stream of commands that change a position or the set of taken cells, where each command passes a fixed sequence of legality checks. Write down which structure is authoritative and which structures are derived from it. The invariant is that the two agree after every accepted command and that a rejected command writes nothing.

#### Ordering The Checks And Writes

Run every check that can fail first, using only reads. Then apply the writes in an order that matches the rules of the game, such as releasing the tail before placing the head. A check that depends on a pending write, like the tail cell, reads the old value directly and never edits the structure to find out.

#### False Friends

Removing the tail from the occupancy set before checking the head looks natural. It is a false friend, because a failed move then leaves the tail missing from the set. Taking the remainder of the step count by the board size is another false friend for the robot, because the robot walks the edge loop and not a line of that length. Skip the derived views when the board is tiny and called rarely, since a direct scan is simpler and fast enough.

<!-- stage: exercises -->
### Exercises

#### [Build] Design Tic-Tac-Toe (LeetCode 348)
<!-- id: sv-board-tictactoe -->

**Prerequisites.** Two-dimensional indexing and signed sums.

**Problem.** Design a class `Board` for an n by n grid that starts empty and is played by players 1 and 2. The call `move(row, col, player)` places a mark for the player. A move is illegal when the cell is outside the grid, the cell already holds a mark, or an earlier move already completed a line. An illegal move returns -1 and changes nothing. A legal move that completes a full row, column or main diagonal or anti-diagonal of one player's marks returns that player. Any other legal move returns 0. Turn order is not enforced. The call `filled()` returns the number of marks placed.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 1000`.
- **Players** are the integers 1 and 2.
- **Calls** number at most `10^5`, and coordinates may lie outside the grid.
- **Return** is an `int`.

**Example 1.** Input n = 3, calls `move(0,0,1)`, `move(0,0,2)`, `move(1,1,1)`, `move(2,2,1)`, `move(0,1,2)`, `filled()`, output 0, -1, 0, 1, -1, 3.

**Example 2.** Input n = 2, calls `move(0,0,1)`, `move(2,0,1)`, `move(1,1,2)`, `move(0,1,2)`, `filled()`, output 0, -1, 0, 2, 3.

**Hint.** Which four sums can one mark change, and when is the grid itself needed?

**Changed decision.** The call validates the cell and the game state before it touches any sum, so a rejected move cannot leave a partial update.

#### [Vary] Design Snake Game (LeetCode 353)
<!-- id: sv-board-snake -->

**Prerequisites.** The tic-tac-toe exercise above, deques and hash sets.

**Problem.** Design a class `Snake` for a grid of `height` rows and `width` columns. The snake starts with length 1 at row 0, column 0. The array `food` lists cells, and only the first uneaten cell is visible at any time. The call `move(direction)` takes `U`, `D`, `L` or `R` and moves the head one cell. It returns the number of food cells eaten so far, or -1 if the game is over. The game ends when the head leaves the grid or enters a cell held by the body after the move. A move onto the visible food grows the snake by one cell, and the tail stays. Any other move releases the tail before the head enters. After the game ends, every call returns -1 and changes nothing.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= height, width <= 100`.
- **Food** has at most 50 distinct cells inside the grid.
- **Calls** number at most `10^4`.
- **Return** is an `int`.

**Example 1.** Input width 3, height 3, food `[[0,1],[1,1],[1,0]]`, calls `R`, `D`, `L`, `U`, `D`, output 1, 2, 3, 3, -1.

**Example 2.** Input width 2, height 2, food `[[0,1],[1,1],[1,0]]`, calls `R`, `D`, `L`, `U`, `R`, output 1, 2, 3, 3, 3.

**Hint.** Which cell is free for a move that does not eat, and what must stay unchanged if the move is illegal?

**Changed decision.** The occupancy set must drop the tail before the head enters, so the call judges the move first and then updates the deque and the set in that order.

#### [Boundary] Walking Robot Simulation II (LeetCode 2069)
<!-- id: sv-board-robot -->

**Prerequisites.** Modular arithmetic and the two exercises above.

**Problem.** Design a class `Robot` for a grid of `width` columns and `height` rows. The robot starts at (0, 0) facing East. The call `step(num)` repeats `num` times: if the cell ahead lies outside the grid, the robot first turns 90 degrees counterclockwise, from East to North to West to South to East, and then it moves one cell forward. The call `getPos()` returns `[x, y]`. The call `getDir()` returns `East`, `North`, `West` or `South`.

**Constraints.** The limits are:
- **Grid** satisfies `2 <= width, height <= 100`.
- **Steps** satisfy `0 <= num <= 10^9`, and `step(0)` changes nothing.
- **Calls** number at most `10^4`.
- **Return** of `getPos` is an `int` array of length 2.

**Example 1.** Input width 6, height 3, calls `step(2)`, `step(2)`, `getPos()`, `getDir()`, `step(2)`, `step(1)`, `step(4)`, `getPos()`, `getDir()`, output [4,0], East, [1,2], West.

**Example 2.** Input width 2, height 2, calls `getDir()`, `step(0)`, `getDir()`, `step(4)`, `getPos()`, `getDir()`, output East, East, [0,0], South.

**Hint.** What is the direction at the start corner before any step and after one full loop?

**Changed decision.** The step count is reduced by the cycle length, and the start corner needs a flag, because the same cell has two directions.

#### [Recognize] Layered Counts In A Cube (LeetCode 3391)
<!-- id: sv-board-layers -->

**Prerequisites.** All three exercises above and tree sets.

**Problem.** Design a class `Cube` for an n by n by n binary matrix that starts with every cell 0. The layer x is the set of n * n cells with first coordinate x. The call `setCell(x, y, z)` sets the cell to 1 and returns `true` if the value changed, or `false` otherwise. The call `unsetCell(x, y, z)` sets the cell to 0 and returns `true` if the value changed, or `false` otherwise. The call `largestLayer()` returns the layer with the most ones, and it returns the largest x among tied layers.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 100`.
- **Coordinates** are integers from 0 to n - 1.
- **Calls** number at most `10^5`.
- **Return** types are `boolean` for the two updates and `int` for `largestLayer`.

**Example 1.** Input n = 3, calls `largestLayer()`, `setCell(0,0,0)`, `largestLayer()`, `setCell(0,0,0)`, `setCell(2,1,1)`, `largestLayer()`, `unsetCell(2,1,1)`, `largestLayer()`, `unsetCell(0,1,1)`, output 2, true, 0, false, true, 2, true, 0, false.

**Example 2.** Input n = 2, calls `setCell(1,0,0)`, `setCell(1,1,1)`, `setCell(0,0,0)`, `largestLayer()`, `unsetCell(1,0,0)`, `unsetCell(1,1,1)`, `largestLayer()`, `unsetCell(0,0,0)`, `largestLayer()`, output true, true, true, 1, true, true, 0, true, 1.

**Hint.** What must happen to a layer's key in the ordered set before its count changes? A key that changes while it sits in a `TreeSet` breaks the ordering, so remove the old key first.

**Changed decision.** Each layer has an ordered key made from its count, so a repeated set or unset call returns before touching the index, and a real change removes the old key first.
