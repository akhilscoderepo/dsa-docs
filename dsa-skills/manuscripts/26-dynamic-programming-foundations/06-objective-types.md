<!-- lesson-kind: standard -->
<!-- lesson-id: objective-types -->
## Objective Types

<!-- stage: context -->
### One Track And Three Questions

A game level is a row of cells numbered from 0 to n. The character starts on cell 0 and the exit is cell n. A jump moves the character forward by one of the allowed lengths, for example 1, 3 or 4. Some cells are broken, and the character cannot land on them. A level designer asks three questions about every level. Can the character reach the exit at all? How many different jump sequences reach it? What is the fewest number of jumps?

A developer wrote a table that answers the first question. Each entry says whether the character can stand on that cell. The developer then copied the method for the second question and kept the same logical operator. The counts came out as 0 and 1, never anything else. Copying again for the third question produced a different bug, a wrong number for every level that cannot be finished.

All three questions use the same cells and the same jumps. A **jump sequence** is the ordered list of cells that the character lands on, from cell 0 to cell n. This lesson asks which parts of the table method stay fixed across the questions and which parts must change. The method reads the arrays it receives and never changes them.

<!-- stage: naive -->
### Trying Every Jump Sequence

The direct method follows each jump sequence to the end. At cell `pos` it tries every allowed jump that stays inside the row and lands on a working cell. It asks the same recursive call to report three facts about the cells ahead: whether the exit is reachable, how many sequences reach it, and the fewest jumps.

```java
static final int NONE = Integer.MAX_VALUE;

static long[] explore(int pos, int n, boolean[] broken, int[] jumps) {
    if (pos == n) return new long[] {1, 1, 0};
    long reach = 0, ways = 0, fewest = NONE;
    for (int j : jumps) {
        int next = pos + j;
        if (next > n || broken[next]) continue;
        long[] sub = explore(next, n, broken, jumps);
        if (sub[0] == 1) reach = 1;
        ways += sub[1];
        if (sub[2] != NONE) fewest = Math.min(fewest, sub[2] + 1);
    }
    return new long[] {reach, ways, fewest};
}
```

The method is correct, and it shows the three different ways to merge answers from the cells ahead. The cost is the concern. Two different prefixes that land on the same cell run the same search from that cell again.

```predict
With jumps 1 and 2, no broken cells and n equal to 40, about how many jump sequences reach the exit, and what does that say about the number of calls?

More than 165 million sequences reach cell 40, because the count follows a Fibonacci recurrence. Every sequence is a separate path through the recursion, so the method makes at least that many calls. The answer from a given cell does not depend on how the character got there, yet the method recomputes it for every prefix.
```

<!-- stage: bottleneck -->
### The Same Cell Is Searched Again

The recursion has at least one call for each complete jump sequence, and the number of sequences grows exponentially with n. For jumps 1 and 2, the count of calls is on the order of 1.6^n, which is O(c^n) for a constant c above 1. At n equal to 40 the method already needs seconds, and at n equal to 80 it never finishes.

The number of distinct questions is small. The answer to each of the three questions from cell `pos` depends only on `pos`. A row of n + 1 cells has n + 1 such questions, and each question has at most k jumps to try, where k is the number of allowed jump lengths. A table with one entry per cell therefore needs only O(n * k) steps.

The open question is what an entry stores and how entries combine. The three questions need three different answers, and a mistake in the initial value or the merge step gives silent wrong results. The next section shows that the table layout stays the same while three choices change with the question.

<!-- stage: insight -->
### Pick The Merge Step By The Question

The table has one entry for each cell. Each entry describes the best answer for arriving at that cell, and it is built from the entries of the cells one jump behind.

<!-- names: base value, combine rule, sentinel -->

#### One Table Layout For All Three Questions

Entry `dp[c]` answers the question for the cells from 0 to `c`. The predecessors of cell `c` are the cells `c - j` for every allowed jump `j`, when `c - j >= 0`. A broken cell keeps its starting entry, because no sequence may land on it. The loop fills cells from left to right, so every predecessor is complete before it is read.

#### Choose The Base Value For Cell Zero

The **base value** is the entry of cell 0, which no jump produces. For feasibility, it is `true`. For counting, it is 1, because the empty sequence of jumps is exactly one way to stand on cell 0. For the minimum, it is 0 jumps. A wrong base value, such as 0 for counting, makes every later entry 0.

#### Choose The Combine Rule

The **combine rule** merges the entries of all predecessors into the entry of `c`. For feasibility, cell `c` is reachable when at least one predecessor is reachable, so the rule is OR. For counting, every sequence into a predecessor extends by one jump to a sequence into `c`, and sequences with different last jumps are different, so the rule is addition. For the minimum, the best sequence into `c` extends the best sequence into some predecessor, so the rule is the smallest predecessor value plus the cost of one jump. The rule decides what the loop does, and the table layout is unchanged.

#### Keep The Sentinel From Overflowing

A **sentinel** is a special value that marks an entry for which no answer exists. For feasibility, the sentinel is `false`. For counting, it is 0, which is also the correct count and needs no special handling. For the minimum, the sentinel is a number larger than every real answer. Choosing `Integer.MAX_VALUE` is dangerous, because adding one jump to it wraps to a negative number, which looks like the best answer of all. The method either skips a predecessor that holds the sentinel or uses a sentinel with room to add, such as half the largest value of the type.

#### Counts Need Room

The count for a cell is at most 2^(c - 1), because it never exceeds the number of ways to split `c` into ordered positive parts. A count over a large row exceeds the range of `int`, so the method stores counts in a `long` or reduces them by a modulus when the statement asks for it.

<!-- stage: variables -->
### Three Tables Over One Row

The method reads `n`, the array `broken` with `n + 1` entries, and the array `jumps` of positive lengths. It changes none of them. It keeps three tables, each of length `n + 1`.

- **reach** is a `boolean[]` where `reach[c]` is true when some jump sequence lands on cell `c`.
- **ways** is a `long[]` where `ways[c]` is the number of jump sequences that land on cell `c`.
- **fewest** is an `int[]` where `fewest[c]` is the smallest number of jumps to land on cell `c`, or `NONE` when no sequence exists.

The constant `NONE` is `Integer.MAX_VALUE`. The loop checks `fewest[c - j] != NONE` before it adds 1, so the sum never wraps. The three tables start with the base values at cell 0 and the sentinels elsewhere.

<!-- stage: trace -->
### Two Levels Filled Cell By Cell

#### A Level With One Broken Cell

The first level has cells 0 through 9, with the jumps 1, 3 and 4 and cell 4 broken. The cells in the trace are the ten table positions, and the pointer `c` marks the cell being filled. The variable `reach` is 1 for a reachable cell and 0 otherwise. The variable `ways` holds the count, and `fewest` holds the smallest number of jumps, with -1 in the trace standing for the sentinel.

Cell 4 keeps the sentinel values because it is broken, yet cells 5 through 9 stay reachable through other predecessors. Cell 6 gets its count from cells 5, 3 and 2, so 2 + 2 + 1 gives 5. The exit, cell 9, has 16 sequences and a shortest sequence of 3 jumps.

```trace
{"cells":["c0","c1","c2","c3","c4 x","c5","c6","c7","c8","c9"],"pointers":["c"],"steps":[{"at":{"c":0},"vars":{"reach":1,"ways":1,"fewest":0},"note":"Cell 0 receives the base values: reachable, one way and zero jumps."},{"at":{"c":1},"vars":{"reach":1,"ways":1,"fewest":1},"note":"Cell 1 is entered from cells 0. Adding their counts gives 1, and the best predecessor gives 1 jumps."},{"at":{"c":2},"vars":{"reach":1,"ways":1,"fewest":2},"note":"Cell 2 is entered from cells 1. Adding their counts gives 1, and the best predecessor gives 2 jumps."},{"at":{"c":3},"vars":{"reach":1,"ways":2,"fewest":1},"note":"Cell 3 is entered from cells 2, 0. Adding their counts gives 2, and the best predecessor gives 1 jumps."},{"at":{"c":4},"vars":{"reach":0,"ways":0,"fewest":-1},"note":"Cell 4 is broken, so it keeps the sentinel values: not reachable, no ways and no jump count."},{"at":{"c":5},"vars":{"reach":1,"ways":2,"fewest":2},"note":"Cell 5 is entered from cells 4, 2, 1. Adding their counts gives 2, and the best predecessor gives 2 jumps."},{"at":{"c":6},"vars":{"reach":1,"ways":5,"fewest":2},"note":"Cell 6 is entered from cells 5, 3, 2. Adding their counts gives 5, and the best predecessor gives 2 jumps."},{"at":{"c":7},"vars":{"reach":1,"ways":7,"fewest":2},"note":"Cell 7 is entered from cells 6, 4, 3. Adding their counts gives 7, and the best predecessor gives 2 jumps."},{"at":{"c":8},"vars":{"reach":1,"ways":9,"fewest":3},"note":"Cell 8 is entered from cells 7, 5, 4. Adding their counts gives 9, and the best predecessor gives 3 jumps."},{"at":{"c":9},"vars":{"reach":1,"ways":16,"fewest":3},"note":"Cell 9 is entered from cells 8, 6, 5. Adding their counts gives 16, and the best predecessor gives 3 jumps."}]}
```

#### A Level That Cannot Be Finished

The second level has cells 0 through 6, the jumps 1 and 2, and broken cells 3 and 4. Cell 5 can be entered only from cells 4 and 3, and both are broken. Cell 6 can be entered only from cells 5 and 4, so it has no usable predecessor either.

The reach flag, the count and the jump total all stay at their sentinel values from cell 3 onward. The count of 0 is a real answer for counting, while the -1 in `fewest` means that no number of jumps exists.

```trace
{"cells":["c0","c1","c2","c3 x","c4 x","c5","c6"],"pointers":["c"],"steps":[{"at":{"c":0},"vars":{"reach":1,"ways":1,"fewest":0},"note":"Cell 0 receives the base values: reachable, one way and zero jumps."},{"at":{"c":1},"vars":{"reach":1,"ways":1,"fewest":1},"note":"Cell 1 is entered from cells 0. Adding their counts gives 1, and the best predecessor gives 1 jumps."},{"at":{"c":2},"vars":{"reach":1,"ways":2,"fewest":1},"note":"Cell 2 is entered from cells 1, 0. Adding their counts gives 2, and the best predecessor gives 1 jumps."},{"at":{"c":3},"vars":{"reach":0,"ways":0,"fewest":-1},"note":"Cell 3 is broken, so it keeps the sentinel values: not reachable, no ways and no jump count."},{"at":{"c":4},"vars":{"reach":0,"ways":0,"fewest":-1},"note":"Cell 4 is broken, so it keeps the sentinel values: not reachable, no ways and no jump count."},{"at":{"c":5},"vars":{"reach":0,"ways":0,"fewest":-1},"note":"Cell 5 is entered from cells 4, 3, and none of them is reachable, so the entries stay at the sentinel values."},{"at":{"c":6},"vars":{"reach":0,"ways":0,"fewest":-1},"note":"Cell 6 is entered from cells 5, 4, and none of them is reachable, so the entries stay at the sentinel values."}]}
```

<!-- stage: code -->
### Filling Three Tables In One Pass

The method fills all three tables in one pass and returns the answers for cell n as a `long[]` of three values: 1 or 0 for reachability, the count, and the fewest jumps or -1.

```java
static long[] solveLevel(int n, boolean[] broken, int[] jumps) {
    final int NONE = Integer.MAX_VALUE;
    boolean[] reach = new boolean[n + 1];
    long[] ways = new long[n + 1];
    int[] fewest = new int[n + 1];
    Arrays.fill(fewest, NONE);
    reach[0] = true;
    ways[0] = 1;
    fewest[0] = 0;
    for (int c = 1; c <= n; c++) {
        if (broken[c]) continue;
        for (int j : jumps) {
            int p = c - j;
            if (p < 0) continue;
            if (reach[p]) reach[c] = true;
            ways[c] += ways[p];
            if (fewest[p] != NONE) fewest[c] = Math.min(fewest[c], fewest[p] + 1);
        }
    }
    return new long[] {reach[n] ? 1 : 0, ways[n], fewest[n] == NONE ? -1 : fewest[n]};
}
```

The three lines inside the inner loop use three different merge steps: assign true, add, and take the smaller value. The broken cell is skipped before the inner loop, so it keeps its starting values. The guard `fewest[p] != NONE` comes before the addition. The method runs in O(n * k) time and uses O(n) memory for the three tables.

<!-- stage: applicability -->
### Telling The Three Objectives Apart

#### Reading The Cue

The wording of the question names the objective. "Can" or "is it possible" asks for feasibility. "How many ways" asks for counting. "Fewest", "smallest total" or "largest total" asks for optimization. The state graph is often the same, and only the merge step changes.

#### Checking The Invariant

An **invariant** is a fact about the tables that stays true as the loop advances. Here, after cell `c` is filled, each table holds the answer of its objective for the cells from 0 to `c`, and the entry of a broken or unreachable cell holds that objective's sentinel. Test cell 0 alone, where the base value is the answer. Test a level with no usable path, which must return false, 0 and -1. Test costs large enough that a sentinel plus a cost would overflow.

#### Avoiding The False Friend

A **false friend** is a method that resembles the right one but answers a different question. The first false friend is counting reachable cells instead of counting paths, which gives the same number for a row with one path and a row with a thousand. The second is a minimum table that starts at zero, because the zero then wins every comparison. The third is reusing the feasibility merge, OR, for counting, which collapses every count to 0 or 1.

<!-- stage: exercises -->
### Exercises

#### [Build] Reachable Boolean States (Author exercise)
<!-- id: dp-obj-reachable-states -->

**Prerequisites.** The base value and the OR merge step of this lesson.

**Problem.** A row has cells numbered `0..n`. The array `broken` has `n + 1` entries, and `broken[c]` is true when cell `c` cannot be landed on. The array `jumps` lists the allowed jump lengths, each a positive integer. A walk starts on cell 0 and repeats jumps forward, landing only on cells that are not broken. Return a `boolean[]` of length `n + 1` whose entry `c` is true exactly when some walk lands on cell `c`.

**Constraints.** The limits are:
- **Row** satisfies `0 <= n <= 100000`, and `broken[0]` is false.
- **Jumps** satisfy `1 <= jumps.length <= 10`, with distinct values in `1..n + 1`.
- **Mutation** is not allowed, because both input arrays stay unchanged.

**Example 1.** Input `n = 7`, `broken = [F,F,F,F,F,F,F,F]`, `jumps = [2,3]`, output `[T,F,T,T,T,T,T,T]`.

**Example 2.** Input `n = 4`, `broken = [F,T,T,T,F]`, `jumps = [1,2]`, output `[T,F,F,F,F]`.

**Hint.** What does cell 1 read when no allowed jump has length 1, and why does a broken cell never become true?

**Changed decision.** The table holds booleans and the base value is true. A cell becomes true when any predecessor is true, and a broken cell keeps false.

#### [Vary] Count The Same Paths (Author exercise)
<!-- id: dp-obj-count-sequences -->

**Prerequisites.** The exercise above.

**Problem.** Use the same row, broken cells and jump lengths as the exercise above. A jump sequence is the ordered list of cells landed on from cell 0 to cell `n`, using only working cells. Two sequences differ when their lists differ. Return the number of jump sequences that end on cell `n`, modulo 1000000007, as an `int`.

**Constraints.** The limits are:
- **Row** satisfies `0 <= n <= 100000`, and `broken[0]` is false.
- **Jumps** satisfy `1 <= jumps.length <= 10`, with distinct values in `1..n + 1`.
- **Result** is returned in the range `0..1000000006`.
- **Empty case** gives 1 for `n = 0`, because the empty sequence ends on cell 0.

**Example 1.** Input `n = 7`, `broken` has no true entry, `jumps = [1,2,3]`, output `44`.

**Example 2.** Input `n = 8`, `broken` is true only at cells 2 and 5, `jumps = [1,2,4]`, output `7`.

**Hint.** What does a cell store when it cannot be reached, and why does the base value have to be 1 and not 0?

**Changed decision.** The merge step changes from OR to addition and the base value changes from true to 1. The remainder runs after each addition so the stored counts stay below the modulus.

#### [Boundary] Impossible Minimum (Author exercise)
<!-- id: dp-obj-impossible-minimum -->

**Prerequisites.** The two exercises above.

**Problem.** Use the row and broken cells of the first exercise. The array `costs` has the same length as `jumps`, and a jump of length `jumps[i]` costs `costs[i]`. Return the smallest total cost over all walks from cell 0 to cell `n` that land only on working cells. Return -1 when no such walk exists. Return a `long`.

**Constraints.** The limits are:
- **Row** satisfies `0 <= n <= 1000`, and `broken[0]` is false.
- **Jumps** satisfy `1 <= jumps.length <= 8`, with distinct values in `1..n + 1`.
- **Costs** satisfy `0 <= costs[i] <= 1000000000`.
- **Result** can exceed the range of `int`, so the method stores totals in `long`.

**Example 1.** Input `n = 6`, no broken cells, `jumps = [1,2,4]`, `costs = [5,3,10]`, output `9`.

**Example 2.** Input `n = 6`, no broken cells, `jumps = [2,3]`, `costs = [1000000000,1000000000]`, output `2000000000`.

**Hint.** What does a sentinel plus a cost of one billion do in an `int`, and which value is large enough for the sentinel in a `long`?

**Changed decision.** The sentinel is a `long` value of half the largest `long`, so adding one cost cannot wrap. The method converts any total at or above the sentinel to -1 at the end.

#### [Recognize] Minimum Path Sum (LeetCode 64)
<!-- id: dp-obj-min-path-sum -->

**Prerequisites.** All three exercises above.

**Problem.** A grid `grid` has `m` rows and `n` columns of non-negative integers. A path starts at the top-left cell and ends at the bottom-right cell. Each move goes one cell right or one cell down. The sum of a path is the sum of the values of all cells it visits, including both ends. Return the smallest sum over all paths.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= m, n <= 200`.
- **Values** satisfy `0 <= grid[r][c] <= 100`.
- **Mutation** is not allowed, because the input grid stays unchanged.

**Example 1.** Input `grid = [[2,5,1],[3,1,9],[4,2,1]]`, output `9`.

**Example 2.** Input `grid = [[7,0,4,6]]`, output `17`.

**Hint.** Which two cells can a path come from to reach cell (r, c), and what changes on the first row and the first column?

**Changed decision.** The merge step takes the smaller of two predecessor sums and adds the value of the current cell. The first row and the first column have only one predecessor, so they need no comparison.
