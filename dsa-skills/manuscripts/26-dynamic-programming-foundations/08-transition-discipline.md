<!-- lesson-kind: standard -->
<!-- lesson-id: transition-discipline -->
## Transition Discipline

<!-- stage: context -->
### One Array That Gives Wrong Counts

A route counter for a game level keeps one `long[]` named `row`. Entry `row[j]` holds the number of ways a token can stand in column `j` after some number of turns. In each turn the token either stays in its column or moves one column to the right. The programmer saves memory by updating the same array in place for every turn, instead of storing a table with one row per turn.

The token starts in column 0. On a test row with two columns, the code gives the right counts after every turn. On a row with five columns, the first turn should turn `[1, 0, 0, 0, 0]` into `[1, 1, 0, 0, 0]`, yet the code prints `[1, 1, 1, 1, 1]`. The formula is right, the short test passed, and the numbers are still wrong.

A **transition** is one application of the formula that turns the counts of one turn into the counts of the next turn. This lesson asks how an in-place loop can keep every read tied to the turn it is supposed to read from.

<!-- stage: naive -->
### Updating One Array Left To Right

The formula says that the count in column `j` after a turn is the old count in column `j`, which covers a token that stayed, plus the old count in column `j - 1`, which covers a token that moved right. Column 0 has no left neighbor, so it keeps its old count. The direct way to write this is one loop over the columns.

```java
static void takeTurnWrong(long[] row) {
    for (int j = 1; j < row.length; j++) {
        row[j] = row[j] + row[j - 1];
    }
}
```

The loop touches each column once, so one turn costs O(W) time and no extra memory. Each line reads `row[j]` and `row[j - 1]`, which looks exactly like the formula.

```predict
Start with row = [1, 2, 1, 0, 0] and call takeTurnWrong once. What does the array hold afterward, and what should it hold?

It holds [1, 3, 4, 4, 4], while the correct result is [1, 3, 3, 1, 0]. The loop writes column 1 first, so when it reaches column 2 the value in column 1 is already the new count 3, not the old count 2. Each later column adds a value that this same turn has just changed. The formula asks for old counts, and the loop reads a mixture.
```

<!-- stage: bottleneck -->
### Reads Land On Values Already Overwritten

The loop breaks because of the order of its own writes. Assigning `row[j]` destroys the old value of column `j`. The next iteration then reads `row[j]` as its left neighbor and gets the new value instead. Every column after the first receives a sum that includes this turn's changes, so the error spreads along the array, and a token appears to move several columns in one turn.

Small tests hide the problem. In a row with two columns, the only write is to column 1, and its left neighbor, column 0, is never overwritten. The fault appears only when a row has a third column, whose left neighbor the loop has just changed.

The obvious repair is a full table with one row per turn. That costs O(T * W) memory for `T` turns and `W` columns, which defeats the purpose of the in-place array. A second repair copies the row at the start of every turn, which costs O(W) extra work and memory per turn but keeps the O(W) total memory if the copy is released. The better question is when a single array is enough, and which loop direction or saved value makes it safe. The next section answers that with a rule about which cells a transition reads.

<!-- stage: insight -->
### Each Turn Reads The Layer Before

A transition is correct when every value it reads belongs to the previous turn and every value it writes belongs to the current turn.

<!-- names: layer, alias, reverse order -->

#### A Layer Holds One Turn

A **layer** is the complete set of values for one step of the recurrence, such as one grid row or one turn count. Layer `t` is defined only from layer `t - 1`. Correctness means that, while layer `t` is being built, no read touches a cell that already holds a value of layer `t`.

#### Two Arrays Keep Layers Apart

The safe design keeps two arrays, `prev` for layer `t - 1` and `next` for layer `t`. The loop reads only `prev` and writes only `next`. When the loop ends, the roles swap, and the old `prev` array becomes the target for the following layer. Because `next` is written in full before it is read, stale contents from two layers ago do no harm. The memory stays at two arrays, which is O(W).

#### An Alias Merges Two Layers

An **alias** is a second variable that refers to the same array object. In Java, the assignment `next = prev` copies the reference, not the contents. After it, both names point at one object, and every write through `next` also appears in `prev`. The layers merge into one, and the code behaves like the in-place loop, with a different surface. To get an independent array, call `prev.clone()`, `Arrays.copyOf(prev, prev.length)`, or `new long[prev.length]`.

#### Reverse Order Protects The Left Reads

A single array is safe when the loop visits cells so that each read happens before the cell is overwritten. If the transition at `j` reads `j` and `j - 1` of the previous layer, then visiting `j` from the last column down to 1 works. When the loop writes `row[j]`, the cell `row[j - 1]` has not been touched yet. This is **reverse order**. When a transition reads both `j - 1` and `j + 1`, one direction is not enough, and the loop keeps the overwritten old value in a temporary variable before moving on. Choose the direction from the read pattern, never from habit.

<!-- stage: variables -->
### Previous Row, Next Row And Loop Index

The two-array version of the turn receives `prev`, a `long[]` of length `W`. It never writes to it. It keeps these working values.

- **next** is a new `long[]` of length `W`; the loop writes it and never reads it.
- **j** is the column index being computed, from 0 to `W - 1`.
- **old** is the value of `prev[j - 1]` when `j > 0`, and it is read only from `prev`.

The in-place version keeps one array `row` and visits `j` from `W - 1` down to 1. Both versions return the same counts, and the in-place version trades the second array for a loop direction that must match the read pattern.

<!-- stage: trace -->
### Two Orders On The Same Row

#### Visiting Columns From The Right

The start row is `[1, 2, 1, 0, 0]`, and one turn must produce `[1, 3, 3, 1, 0]`. The loop here visits columns 4, 3, 2 and 1 in that order. The pointer `j` selects the column being written. The variable `old` shows the value of the left neighbor at read time, and `written` shows the new count for column `j`.

Each read finds a left neighbor that no earlier iteration has touched, so `old` always equals the previous turn's value. Column 0 is never written, because it has no left neighbor.

```trace
{"cells":["col 0","col 1","col 2","col 3","col 4"],"pointers":["j"],"steps":[{"at":{"j":-1},"vars":{"old":0,"written":0},"note":"Before the turn, the row reads [1, 2, 1, 0, 0]."},{"at":{"j":4},"vars":{"old":0,"written":0},"note":"Column 4 reads 0 on its left and stores 0, so the row becomes [1, 2, 1, 0, 0]. That left neighbor still holds its value from the previous turn."},{"at":{"j":3},"vars":{"old":1,"written":1},"note":"Column 3 reads 1 on its left and stores 1, so the row becomes [1, 2, 1, 1, 0]. That left neighbor still holds its value from the previous turn."},{"at":{"j":2},"vars":{"old":2,"written":3},"note":"Column 2 reads 2 on its left and stores 3, so the row becomes [1, 2, 3, 1, 0]. That left neighbor still holds its value from the previous turn."},{"at":{"j":1},"vars":{"old":1,"written":3},"note":"Column 1 reads 1 on its left and stores 3, so the row becomes [1, 3, 3, 1, 0]. That left neighbor still holds its value from the previous turn."}]}
```

#### Visiting Columns From The Left

The second run applies the same formula to the same row but visits columns 1, 2, 3 and 4. The variable `old` now reads a left neighbor that the previous iteration has just overwritten. The error is small at column 2 and grows with each step, ending with three counts of 4.

The final array `[1, 3, 4, 4, 4]` differs from the correct result in columns 2, 3 and 4. The formula is identical in both runs, and only the visiting order changed.

```trace
{"cells":["col 0","col 1","col 2","col 3","col 4"],"pointers":["j"],"steps":[{"at":{"j":-1},"vars":{"old":0,"written":0},"note":"Before the turn, the row reads [1, 2, 1, 0, 0]."},{"at":{"j":1},"vars":{"old":1,"written":3},"note":"Column 1 reads 1 on its left and stores 3, so the row becomes [1, 3, 1, 0, 0]. Column 0 is never written, so this read is still correct."},{"at":{"j":2},"vars":{"old":3,"written":4},"note":"Column 2 reads 3 on its left and stores 4, so the row becomes [1, 3, 4, 0, 0]. That left neighbor was just overwritten, so the sum uses a changed value."},{"at":{"j":3},"vars":{"old":4,"written":4},"note":"Column 3 reads 4 on its left and stores 4, so the row becomes [1, 3, 4, 4, 0]. That left neighbor was just overwritten, so the sum uses a changed value."},{"at":{"j":4},"vars":{"old":4,"written":4},"note":"Column 4 reads 4 on its left and stores 4, so the row becomes [1, 3, 4, 4, 4]. That left neighbor was just overwritten, so the sum uses a changed value."}]}
```

<!-- stage: code -->
### Two Arrays And One Reverse Loop

The first method returns a new row and leaves its input unchanged. The second method updates a single array and relies on the loop direction. Both compute the stay-or-move-right turn.

```java
static long[] takeTurn(long[] prev) {
    long[] next = new long[prev.length];
    next[0] = prev[0];
    for (int j = 1; j < prev.length; j++) {
        next[j] = prev[j] + prev[j - 1];
    }
    return next;
}

static void takeTurnInPlace(long[] row) {
    for (int j = row.length - 1; j >= 1; j--) {
        row[j] = row[j] + row[j - 1];
    }
}
```

The call `new long[prev.length]` creates an independent object, so writes to `next` never reach `prev`. The reverse loop writes column `j` only after column `j` has been used as the left neighbor of column `j + 1`, so the read of `row[j - 1]` always sees an old value. Both methods run in O(W) time per turn. The first uses O(W) extra memory per turn, and the second uses O(1) extra memory.

<!-- stage: applicability -->
### Recognizing Unsafe Reads

#### Reading The Cue

Check the loop order whenever one array is reused across rows, turns or items, and the new value of a cell depends on neighbors from the previous layer. Typical cases are a row of a grid table that is rolled into one array, a count table that moves one step at a time, and any code that assigns one array variable to another. Ask for each read in the loop body whether it points at the previous layer or at a cell the loop has already written.

#### Checking The Invariant

The **invariant** here is that every read in the body of the loop touches a value from the previous layer. Test it with a row that has two adjacent nonzero cells, because a row with a single nonzero cell hides the fault. Test a row of width 1, where the loop body never runs. Test that the input array is unchanged after the two-array version returns. Test that two returned rows are distinct objects by writing into one and reading the other.

#### Avoiding The False Friend

A **false friend** is a technique that looks right but fails on some inputs. Here the first false friend is the assignment `next = prev`, which looks like a copy and is only a second name. The second is the single-array loop in the wrong direction, which passes the first turn and fails later. The third is a swap of two arrays that skips writing every cell of the target, so stale values from an older layer survive. A reverse loop is also no cure when a transition reads cells on both sides.

<!-- stage: exercises -->
### Exercises

#### [Build] Separate Previous Row (Author exercise)
<!-- id: dp-trans-previous-row -->

**Prerequisites.** The two-array turn of this lesson.

**Problem.** An `int[]` named `prev` and an `int[]` named `cost` have the same length `w`. Compute a new `int[]` named `next` of length `w`. For each column `j`, `next[j]` equals `cost[j]` plus the larger of `prev[j]` and, when `j > 0`, `prev[j - 1]`. Return `next`. The array `prev` is the previous row, and the method must not write to it.

**Constraints.** The limits are:
- **Width** satisfies `1 <= w <= 1000`.
- **Values** satisfy `-100000 <= prev[j], cost[j] <= 100000`.
- **Return** is a new array, never `prev` or `cost`.
- **Mutation** is not allowed, because both inputs stay unchanged.

**Example 1.** Input `prev = [3,1,4]`, `cost = [1,5,9]`, output `[4,8,13]`.

**Example 2.** Input `prev = [-6,-2,-8]`, `cost = [2,-1,3]`, output `[-4,-3,1]`.

**Hint.** If the method wrote into `prev` instead, which value would column 1 read for its left neighbor in the first example?

**Changed decision.** The method allocates a new array and reads only from the old one. The first column has a single choice, because it has no left neighbor.

#### [Vary] Safe In-Place Grid Row (Author exercise)
<!-- id: dp-trans-inplace-row -->

**Prerequisites.** The exercise above.

**Problem.** A token starts in column 0 of a row with `w` columns. In each of `steps` turns it stays in its column or moves one column to the right, and it cannot leave the row. A column `j` with `blocked[j]` equal to `true` cannot hold the token at the end of a turn. Return a `long[]` of length `w` whose entry `j` is the number of ways the token can stand in column `j` after exactly `steps` turns. Use one array for all turns.

**Constraints.** The limits are:
- **Width** satisfies `1 <= w <= 60`.
- **Turns** satisfy `0 <= steps <= 60`.
- **Blocked** columns may include column 0, which is blocked only at the end of each turn.
- **Mutation** is not allowed, because `blocked` stays unchanged.

**Example 1.** Input `w = 4`, `blocked = [false,false,false,false]`, `steps = 3`, output `[1,3,3,1]`.

**Example 2.** Input `w = 4`, `blocked = [false,false,true,false]`, `steps = 3`, output `[1,3,0,0]`.

**Hint.** In the update of column `j`, which neighbor belongs to the previous turn, and which direction of the loop keeps it unchanged until it is read?

**Changed decision.** The loop visits columns from right to left, and a blocked column is set to 0 after its sum is computed. With zero turns, the start row `[1,0,...,0]` is returned unchanged, apart from a blocked column 0.

#### [Boundary] Aliased Arrays (Author exercise)
<!-- id: dp-trans-aliased-rows -->

**Prerequisites.** The two exercises above.

**Problem.** An `int[]` named `start` holds the first row of values. One turn builds a new row in which entry `j` is the sum of the previous row's entries `j - 1`, `j` and `j + 1`, and an index outside the row counts as 0. Return an `int[][]` with `steps + 1` rows. Row 0 holds the values of `start`, and row `t` is the result of `t` turns. Every returned row is a separate array object, including row 0.

**Constraints.** The limits are:
- **Width** satisfies `1 <= start.length <= 10`.
- **Turns** satisfy `0 <= steps <= 10`.
- **Values** satisfy `-100 <= start[j] <= 100`.
- **Mutation** is not allowed, because `start` stays unchanged and no returned row shares storage with it.

**Example 1.** Input `start = [1,0,0]`, `steps = 2`, output `[[1,0,0],[1,1,0],[2,2,1]]`.

**Example 2.** Input `start = [5]`, `steps = 3`, output `[[5],[5],[5],[5]]`.

**Hint.** If the method kept one variable `cur` and wrote `rows[t] = cur` after each turn, what would every row of the result contain at the end?

**Changed decision.** The method creates a fresh array for every row and copies `start` into row 0. The result keeps all layers, so no row may be reused as the target of a later turn.

#### [Recognize] Minimum Falling Path Sum (LeetCode 931)
<!-- id: dp-trans-falling-path -->

**Prerequisites.** All three exercises above.

**Problem.** An `n` by `n` integer matrix `matrix` is given. A falling path starts at any cell of the first row. From cell `(r, c)` it moves to row `r + 1`, in column `c - 1`, `c` or `c + 1`, and the new column must lie inside the matrix. The path ends in the last row. Return the smallest sum of the cells on any falling path as an `int`.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 100`.
- **Values** satisfy `-100 <= matrix[r][c] <= 100`.
- **Result** fits in an `int`.
- **Mutation** is not allowed, because `matrix` stays unchanged.

**Example 1.** Input `matrix = [[5,-2,4],[3,8,-1],[2,6,7]]`, output `3`.

**Example 2.** Input `matrix = [[4,-9],[7,1]]`, output `-8`.

**Hint.** Each new row reads three cells of the previous row. Can a single array update in one pass, or does the left read and the right read both need old values?

**Changed decision.** The new cost depends on a window of three old costs, so the method keeps a previous row and a next row and swaps their roles after each row. A one-column matrix is a plain sum of its cells.
