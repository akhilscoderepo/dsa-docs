<!-- lesson-kind: standard -->
<!-- lesson-id: resource-dominance -->
## Resource Dominance

<!-- stage: context -->
### Rope Tokens On Harrow Fell

Ines Calder guides day hikes over Harrow Fell, a hillside the park service has drawn as a grid of squares. Most squares are ordinary trail. A few are cliff bands, and the rule at a cliff band is strict: to step onto one you hand in a rope-climb token, and the token is gone for good. Every guide is issued the same small pocketful, and Ines is carrying two today.

She wants the fewest steps from the trailhead in the top-left square to the lookout in the bottom-right square, moving one square at a time up, down, left or right. Spending tokens is allowed, wasting them is not, because a guide who runs dry halfway has to turn a group around. Ines does not want a clever answer for this one map. She wants a method that works for any map and any number of tokens, including a map where the straight line is blocked and a long detour saves a token for later.

<!-- stage: naive -->
### Try Every Walk And Count Tokens

The direct method does what a careful guide would do with a pencil. Start at the trailhead with all the tokens, try each of the four neighbours, hand in a token when the square is a cliff band, refuse the move when there is no token, and keep going until the lookout is reached. Then back up and try the other branches. A square already on the current walk is skipped so the walk cannot circle, and the shortest complete walk found is the answer.

```java
static final int NONE = Integer.MAX_VALUE / 2;

static int shortestByTrying(String[] fell, boolean[][] onWalk, int r, int c, int tokens, int steps) {
    int rows = fell.length, cols = fell[0].length();
    if (r == rows - 1 && c == cols - 1) return steps;
    int best = NONE;
    onWalk[r][c] = true;
    int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || onWalk[nr][nc]) continue;
        int left = tokens - (fell[nr].charAt(nc) == '#' ? 1 : 0);
        if (left < 0) continue;
        best = Math.min(best, shortestByTrying(fell, onWalk, nr, nc, left, steps + 1));
    }
    onWalk[r][c] = false;
    return best;
}
```

The method is correct, because it looks at every walk that never repeats a square and checks the token rule at each move. It reads the map without changing it, and it restores each square as it backs out. The caller turns a result of `NONE` into "no route".

<!-- stage: bottleneck -->
### Walks Multiply While Futures Repeat

The number of walks that never repeat a square grows roughly like 3^(R * C) on an open map with R rows and C columns, and every one of them is walked to the end. A map of six by six squares can already hold millions of walks, and a ten by ten map is out of reach. The running time is therefore O(3^(R * C)) in the worst case, which is not a method anyone can lend to a park office.

Most of that effort is repeated. Two walks that arrive at the same square on the same step with the same number of tokens in the pocket have identical futures, so only the first of them needed to be followed. The route behind the hiker never matters, only where she stands and what she can still afford. What the search lacks is a way to name that pair, remember it, and refuse to follow a pair a second time.

<!-- stage: insight -->
### Squares Plus Tokens Make The State

The unit of search is not a square but a **queue state**: a square together with the number of tokens left in the pocket. Standing on one square with two tokens and with none are different situations, since only the first can still climb. Pack the pair into one int, `cell * (k + 1) + left`, and an ordinary breadth-first search over these states is already correct. A state is expanded the first time it is seen, and the layer that first sees it is its fewest steps. The price is one seen flag for every square and token count, R * C * (k + 1) flags in all.

Most of those flags guard states that never need a visit, and **dominance** says which. State A dominates state B when both stand on the same square, A arrived in no more steps than B, and A holds at least as many tokens. Whatever B can still finish, A can finish too, because a cliff costs one token however the hiker got there. A always has the tokens for the same moves and gets to the lookout no later, so B can be dropped. The proof leans on one fact about this puzzle: more tokens never forbid a move and never change what a move costs. Both conditions must hold together. A richer state that arrived later dominates nothing yet.

Breadth-first order makes the test cheap. A **best table** keeps, for each square, the largest token count among states already queued there. States are queued in non-decreasing step count, so everything in the table is at least as quick as the newcomer, and only the token comparison remains. The newcomer is queued only if it holds strictly more tokens than the table entry. A flat seen flag per square looks like the same idea and is not, since it throws away a richer state just because the square was seen before.

The invariant is that each table entry equals the largest token count ever queued on that square, and a state is dropped only when an earlier or equal-step state with at least as many tokens is already queued.

<!-- names: queue state, dominance, best table -->

<!-- stage: variables -->
### Fell, Tokens And The Table

The array `fell` holds one string per row, where `'#'` is a cliff band and anything else is trail. The integer `tokens` is the starting pocketful, and `width` is `tokens + 1`, the number of different token counts a hiker can hold. The array `best` has one entry per square, indexed by cell number `r * cols + c`, and every entry starts at -1, which means that nothing has been queued there. The integer `state` is a packed pair taken from the queue, and `cell` and `left` are decoded from it with division and remainder by `width`. The counter `steps` is the layer number, and `nl` is the token count a neighbor would have after the move.

<!-- stage: trace -->
### Two Maps Through The Table

The first trace uses a map of three rows and three columns stored as one flat row-major list, so the pointer `cur` is a flat index and square (1, 2) is index 5. The hiker holds one token. The vars give the layer, the tokens in her pocket at that state, and how many states wait in the queue after the expansion. Both squares beside the trailhead are cliff bands, so the first expansion spends the token on one of them, and from then on every state holds zero tokens and the walk follows trail. The note on each step also lists the neighbors that the table refused. The walk ends with the lookout taken at step 4.

```trace
{"cells":[".","#",".","#","#",".",".",".","."],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"step":0,"left":1,"queued":2},"note":"Take cell 0 (row 0, column 0) at step 0 holding 1 token; it queues cell 3 with 0 left, cell 1 with 0 left."},{"at":{"cur":3},"vars":{"step":1,"left":0,"queued":2},"note":"Take cell 3 (row 1, column 0) at step 1 holding 0 tokens; it queues cell 6 with 0 left; refused as not richer than the table: cell 0 with 0 left."},{"at":{"cur":1},"vars":{"step":1,"left":0,"queued":2},"note":"Take cell 1 (row 0, column 1) at step 1 holding 0 tokens; it queues cell 2 with 0 left; refused as not richer than the table: cell 0 with 0 left."},{"at":{"cur":6},"vars":{"step":2,"left":0,"queued":2},"note":"Take cell 6 (row 2, column 0) at step 2 holding 0 tokens; it queues cell 7 with 0 left."},{"at":{"cur":2},"vars":{"step":2,"left":0,"queued":2},"note":"Take cell 2 (row 0, column 2) at step 2 holding 0 tokens; it queues cell 5 with 0 left."},{"at":{"cur":7},"vars":{"step":3,"left":0,"queued":2},"note":"Take cell 7 (row 2, column 1) at step 3 holding 0 tokens; it queues cell 8 with 0 left; refused as not richer than the table: cell 6 with 0 left."},{"at":{"cur":5},"vars":{"step":3,"left":0,"queued":1},"note":"Take cell 5 (row 1, column 2) at step 3 holding 0 tokens; it queues nothing; refused as not richer than the table: cell 2 with 0 left, cell 8 with 0 left."},{"at":{"cur":8},"vars":{"step":4,"left":0,"queued":0},"note":"Take cell 8 (row 2, column 2) at step 4 holding 0 tokens; it queues nothing."}]}
```

The second trace is the map where a flat seen flag fails, three rows and five columns, again with one token. The key moment is the square at index 2. It is taken at step 2 with no tokens, having been entered through the cliff band at index 1. Two steps later it appears again, this time holding one token, after a longer walk around the cliff through indexes 5, 6 and 7. A flat seen flag would refuse that second arrival, and the table accepts it because one is greater than zero. The lookout is at index 14, and its cliff neighbour at index 9 can only be entered by the state that kept its token.

```trace
{"cells":[".","#",".",".",".",".",".",".","#","#",".",".","#","#","."],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"step":0,"left":1,"queued":2},"note":"Take cell 0 (row 0, column 0) at step 0 holding 1 token; it queues cell 5 with 1 left, cell 1 with 0 left."},{"at":{"cur":5},"vars":{"step":1,"left":1,"queued":3},"note":"Take cell 5 (row 1, column 0) at step 1 holding 1 token; it queues cell 10 with 1 left, cell 6 with 1 left; refused as not richer than the table: cell 0 with 1 left."},{"at":{"cur":1},"vars":{"step":1,"left":0,"queued":3},"note":"Take cell 1 (row 0, column 1) at step 1 holding 0 tokens; it queues cell 2 with 0 left; refused as not richer than the table: cell 6 with 0 left, cell 0 with 0 left."},{"at":{"cur":10},"vars":{"step":2,"left":1,"queued":3},"note":"Take cell 10 (row 2, column 0) at step 2 holding 1 token; it queues cell 11 with 1 left; refused as not richer than the table: cell 5 with 1 left."},{"at":{"cur":6},"vars":{"step":2,"left":1,"queued":3},"note":"Take cell 6 (row 1, column 1) at step 2 holding 1 token; it queues cell 7 with 1 left; refused as not richer than the table: cell 1 with 0 left, cell 11 with 1 left, cell 5 with 1 left."},{"at":{"cur":2},"vars":{"step":2,"left":0,"queued":3},"note":"Take cell 2 (row 0, column 2) at step 2 holding 0 tokens; it queues cell 3 with 0 left; refused as not richer than the table: cell 7 with 0 left."},{"at":{"cur":11},"vars":{"step":3,"left":1,"queued":3},"note":"Take cell 11 (row 2, column 1) at step 3 holding 1 token; it queues cell 12 with 0 left; refused as not richer than the table: cell 6 with 1 left, cell 10 with 1 left."},{"at":{"cur":7},"vars":{"step":3,"left":1,"queued":4},"note":"Take cell 7 (row 1, column 2) at step 3 holding 1 token; it queues cell 2 with 1 left, cell 8 with 0 left; refused as not richer than the table: cell 12 with 0 left, cell 6 with 1 left."},{"at":{"cur":3},"vars":{"step":3,"left":0,"queued":4},"note":"Take cell 3 (row 0, column 3) at step 3 holding 0 tokens; it queues cell 4 with 0 left; refused as not richer than the table: cell 2 with 0 left."},{"at":{"cur":12},"vars":{"step":4,"left":0,"queued":3},"note":"Take cell 12 (row 2, column 2) at step 4 holding 0 tokens; it queues nothing; refused as not richer than the table: cell 7 with 0 left, cell 11 with 0 left."},{"at":{"cur":2},"vars":{"step":4,"left":1,"queued":3},"note":"Take cell 2 (row 0, column 2) at step 4 holding 1 token; it queues cell 3 with 1 left; refused as not richer than the table: cell 7 with 1 left, cell 1 with 0 left."},{"at":{"cur":8},"vars":{"step":4,"left":0,"queued":2},"note":"Take cell 8 (row 1, column 3) at step 4 holding 0 tokens; it queues nothing; refused as not richer than the table: cell 3 with 0 left, cell 7 with 0 left."},{"at":{"cur":4},"vars":{"step":4,"left":0,"queued":1},"note":"Take cell 4 (row 0, column 4) at step 4 holding 0 tokens; it queues nothing; refused as not richer than the table: cell 3 with 0 left."},{"at":{"cur":3},"vars":{"step":5,"left":1,"queued":1},"note":"Take cell 3 (row 0, column 3) at step 5 holding 1 token; it queues cell 4 with 1 left; refused as not richer than the table: cell 8 with 0 left, cell 2 with 1 left."},{"at":{"cur":4},"vars":{"step":6,"left":1,"queued":1},"note":"Take cell 4 (row 0, column 4) at step 6 holding 1 token; it queues cell 9 with 0 left; refused as not richer than the table: cell 3 with 1 left."},{"at":{"cur":9},"vars":{"step":7,"left":0,"queued":1},"note":"Take cell 9 (row 1, column 4) at step 7 holding 0 tokens; it queues cell 14 with 0 left; refused as not richer than the table: cell 4 with 0 left."},{"at":{"cur":14},"vars":{"step":8,"left":0,"queued":0},"note":"Take cell 14 (row 2, column 4) at step 8 holding 0 tokens; it queues nothing."}]}
```

<!-- stage: code -->
### Layered Search With A Best Table

```java
final class Fell {
    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    static int fewestSteps(String[] fell, int tokens) {
        int rows = fell.length, cols = fell[0].length(), width = tokens + 1;
        int[] best = new int[rows * cols];
        java.util.Arrays.fill(best, -1);
        best[0] = tokens;
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        frontier.add(tokens);
        for (int steps = 0; !frontier.isEmpty(); steps++) {
            for (int size = frontier.size(); size > 0; size--) {
                int state = frontier.poll();
                int cell = state / width, left = state % width;
                if (cell == rows * cols - 1) return steps;
                int r = cell / cols, c = cell % cols;
                for (int d = 0; d < 4; d++) {
                    int nr = r + DR[d], nc = c + DC[d];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    int nl = left - (fell[nr].charAt(nc) == '#' ? 1 : 0);
                    if (nl < 0) continue;
                    int next = nr * cols + nc;
                    if (nl <= best[next]) continue;
                    best[next] = nl;
                    frontier.add(next * width + nl);
                }
            }
        }
        return -1;
    }
}
```

The last two gates before queueing are the whole idea: no tokens means no move, and a state that is not richer than the table entry is dropped. A square can be queued at most `tokens + 1` times, because each queueing raises its entry, so time and queue size are O(R * C * k) in the worst case. The table itself takes only O(R * C), against R * C * (k + 1) flags for full state marking. The start square enters the table directly, with its full pocketful, before the first layer runs.

<!-- stage: applicability -->
### Budgets, Fuel And Wall Breaks

Reach for this model when a shortest-path question comes with a consumable allowance, such as wall breaks, fuel stops, free transfers or rope tokens, and the same place can be reached with different amounts left. The invariant to defend is that the best table holds the richest token count queued per square and that nothing was dropped without a quicker, richer-or-equal state already queued. Say that proof out loud before pruning anything, because the pruning is only as good as it is.

The nearest false friend is a flat seen array indexed by square. It is the right tool in ordinary breadth-first search, and here it quietly loses answers, as the second trace shows: the square at index 2 is first reached poor, and the richer arrival two steps later is discarded, so the lookout becomes unreachable on a map where it is reachable in eight steps. Treat any "visited by place" array as suspect as soon as the state grows a second field.

Dominance has a no-go condition. It needs resource that only ever helps. If more of the resource can forbid a move, if the goal is to end with exactly some amount, or if the question asks how much is left on arrival within a step limit, then a later richer state is not beaten by an earlier poorer one and both must be kept. In Java, the table must be filled with -1 on purpose: a new `int[]` holds zeros, and zero is a real token count, so a state arriving with no tokens would be mistaken for one already seen.

<!-- stage: exercises -->
### Exercises

#### [Build] Position And Remaining Breaks (Author exercise)
<!-- id: bv-remaining-breaks -->

**Prerequisites.** The packed state `cell * (k + 1) + left` and layer-by-layer queueing from this lesson.

**Problem.** The `grid` is an array of strings. The character `'S'` marks the start square, `'T'` the target square, `'.'` open ground and `'#'` a wall. A move goes to one of the four edge neighbors, and entering a `'#'` square breaks it and uses up one of the `k` breaks. Return the fewest moves from `S` to `T`, or -1 if there is no way with at most `k` breaks. The contract is that `grid` is only read. Mark states by the pair of square and breaks left, so that no state is ever merged with a poorer or richer one.

**Constraints.** The grid has between 2 and 400 squares, exactly one `'S'` and one `'T'` at different squares, and 0 <= k <= 20.

**Example 1.** Input rows `"S#..."`, `"...##"`, `"..##T"` and `k = 1`, output `8`.

**Example 2.** Input the same rows and `k = 2`, output `6`.

**Hint.** What has to be true of two arrivals at one square before the second may be ignored, and what does a count of zero breaks left still allow?

**Changed decision.** The seen marker belongs to the pair of square and breaks left, not to the square alone, so the queue state carries both fields.

#### [Vary] Best Resource Per Cell (Author exercise)
<!-- id: bv-best-per-cell -->

**Prerequisites.** The Position And Remaining Breaks rung and the best table from the lesson.

**Problem.** The `grid` is an array of strings of `'.'` and `'#'`, and the start is the top-left square, which is open. Entering a `'#'` square uses one of the `k` breaks. Return an `int[][]` of the same shape in which each entry is the greatest number of breaks that can still be unused on arrival at that square, over all walks of any length, or -1 if the square cannot be reached. The start square holds `k`. The contract is that `grid` is only read. A square is reached more than once only when a state brings more breaks than any earlier one.

**Constraints.** 1 <= rows, cols <= 20 and 0 <= k <= 10, so the answer has at most 400 entries, each between -1 and `k`.

**Example 1.** Input rows `".#."`, `"..."` and `k = 1`, output `[[1,0,1],[1,1,1]]`.

**Example 2.** Input rows `".##"`, `".#."` and `k = 1`, output `[[1,0,-1],[1,0,0]]`.

**Hint.** The question never asks for steps, so does an older state with fewer breaks ever beat a newer one with more?

**Changed decision.** The answer is a table of the richest arrival per square instead of a step count, so only the token comparison decides whether a state is kept.

#### [Boundary] Longer Path With More Resource (Author exercise)
<!-- id: bv-longer-richer -->

**Prerequisites.** The Best Resource Per Cell rung and the proof conditions from the lesson.

**Problem.** The `grid` is an array of strings of `'.'` and `'#'`, with the start at the top-left square and the target at the bottom-right square, both open. A step onto a `'#'` square costs one of the `k` breaks. With at most `limit` moves allowed, return the greatest number of breaks that can remain unused on arriving at the target, or -1 if the target cannot be reached within `limit` moves. Do not stop at the first arrival, since a longer walk can arrive richer. Your solution must drop a state only when a state at the same square with no more moves and at least as many breaks is already queued. In your own words, give a grid where dropping a longer but richer state loses the answer, and say exactly when dominance is proved. The contract is that `grid` is only read.

**Constraints.** 1 <= rows, cols <= 15, 0 <= k <= 6 and 0 <= limit <= 60. A one-square grid has the start equal to the target.

**Example 1.** Input rows `".#..."`, `"...#."`, `"...#."` with `k = 1` and `limit = 6`, output `0`.

**Example 2.** Input the same rows with `k = 1` and `limit = 8`, output `1`.

**Hint.** With `limit` equal to 6 the cliff band at the top is the only way through in time, and with 8 a walk around it keeps the break. Which of the two arrivals at the top-middle square would a flat seen flag keep?

**Changed decision.** A cap on moves makes the step count part of the objective, so a later richer state is no longer beaten by an earlier poorer one, and dominance holds only for earlier-or-equal and richer-or-equal states.

#### [Recognize] Shortest Path In A Grid With Obstacles Elimination (LeetCode 1293)
<!-- id: bv-obstacle-elimination -->

**Prerequisites.** The Longer Path With More Resource rung.

**Problem.** The `grid` is an `int[][]` where `0` is an empty cell and `1` is an obstacle. You start at the top-left cell and must reach the bottom-right cell, moving up, down, left or right, and you may eliminate at most `k` obstacles along the way. Return the minimum number of steps, or -1 if it is impossible. The contract is that `grid` is not modified, and both the start and the end cell are empty.

**Constraints.** 1 <= rows, cols <= 40, 0 <= k <= 1600, and each entry is 0 or 1. Large values of `k` should not make the search allocate more than the map needs.

**Example 1.** Input `grid = [[0,1,0],[1,1,0],[0,0,0]], k = 1`, output `4`.

**Example 2.** Input `grid = [[0,1,1],[1,1,1],[1,1,0]], k = 1`, output `-1`.

**Hint.** What is the greatest number of obstacles any shortest route can need, and what does that say about a very large k?

**Changed decision.** Keeping a count of eliminations left in the state replaces plain visited-by-cell, and a state is dropped only when a quicker-or-equal state with at least as many eliminations is already queued.
