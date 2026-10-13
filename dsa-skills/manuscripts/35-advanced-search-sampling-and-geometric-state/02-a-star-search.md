<!-- lesson-kind: standard -->
<!-- lesson-id: a-star-search -->
## A Star Search

<!-- stage: context -->
### A Route Planner That Searches Everywhere

A warehouse robot must drive from a dock to a shelf ten cells away on the same row. The planner uses Dijkstra's algorithm on the floor grid. It finds the right path, but a log of the run shows it visited 111 cells, and most of them lie behind the robot or far to the side. On a floor of a million cells, the same planner visits hundreds of thousands of cells for a trip of thirty steps. The robot waits, and the battery drains while the search wanders.

The planner is correct and wasteful. It has no idea where the shelf is, so it grows a circle of explored cells in every direction. A person with a map would walk toward the shelf first. This lesson asks how to add a sense of direction to the search, and how to do it without ever returning a longer route than Dijkstra's algorithm would.

<!-- stage: naive -->
### Expand By Cost From The Start

The direct planner is Dijkstra's algorithm on a grid. Each cell has an entering cost, and 0 marks a wall. A priority queue holds entries `(g, row, col)`, where `g` is the cost of the best known route from the start. The planner pops the cheapest entry, skips it if a cheaper route to that cell is already known, and pushes the four neighbours with updated costs. It stops when the goal cell pops.

```java
final class GridDijkstra {
    static int shortest(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) java.util.Arrays.fill(row, Integer.MAX_VALUE);
        java.util.PriorityQueue<int[]> pq = new java.util.PriorityQueue<>((x, y) -> x[0] - y[0]);
        best[sr][sc] = 0;
        pq.add(new int[]{0, sr, sc});
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[0] > best[cur[1]][cur[2]]) continue;       // a cheaper route was found later
            if (cur[1] == gr && cur[2] == gc) return cur[0];   // the goal pops with its best cost
            for (int d = 0; d < 4; d++) {
                int nr = cur[1] + dr[d], nc = cur[2] + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int g = cur[0] + cost[nr][nc];
                if (g < best[nr][nc]) { best[nr][nc] = g; pq.add(new int[]{g, nr, nc}); }
            }
        }
        return -1;                                              // the goal is unreachable
    }
}
```

The planner is exact, and tests with small floors pass. A tempting repair is to stop the search early at some cost limit, but a limit that is too tight loses valid routes.

```predict
The floor is open, every enter cost is 1, the start is at column 0, and the goal is 10 cells to the right on the same row. Roughly how many cells does the loop pop before it returns? If the planner could add to each entry a guess of how far the goal still is, which cells would never be popped?

Every cell within cost 9 of the start pops first, which is a diamond of 181 cells, and some cells at cost 10 pop before the goal. The run on a floor of 21 by 21 cells pops 111 cells because the start sits at the edge of the diamond on some sides. Cells that sit above or below the row do not lie on any cheapest route, yet they pop because their cost from the start is small. A guess of the remaining distance would push those entries behind the entries on the row.
```

<!-- stage: bottleneck -->
### Cost So Far Ignores The Goal

The loop costs O(V log V) time and O(V) space for `V` cells that can pop. In the open case above, `V` is the number of cells within the goal's cost from the start, and it grows with the square of the distance. The priority `g` measures only the past. A cell above the row and a cell on the row have the same `g` when they are the same number of steps from the start, so the queue treats them the same. The goal is on the row, and only one of them leads there.

The missing piece is information about the future. For every cell, the planner can cheaply compute a number `h` that tells how much cost might remain, for example the count of rows and columns between the cell and the goal. Combining `g` and `h` into one priority would reorder the queue so that cells headed toward the goal pop first.

A careless guess breaks the exact answer. If `h` claims the remaining cost is larger than it truly is, a cheap route can hide behind a cell that the queue ranks too low. The search then pops the goal through a worse route. The repair must say precisely which guesses are allowed.

<!-- stage: insight -->
### Rank By Cost So Far Plus Guess

<!-- names: admissible, consistent, stale entry -->

#### The Priority Is g Plus h

A\* search keeps Dijkstra's loop and changes one line. The queue orders entries by `f = g + h`, where `g` is the cost of the best known route from the start to the cell and `h` is the heuristic, a guess of the remaining cost from the cell to the goal. With `h` equal to 0 for every cell, `f` equals `g` and the loop is exactly Dijkstra's algorithm.

#### A Guess That Never Overestimates

A heuristic is **admissible** when `h(v)` is at most the true cheapest remaining cost from `v` to the goal, for every cell `v`. The Manhattan distance, which is the row difference plus the column difference, is admissible on a grid where every move costs at least 1, because a route needs at least that many moves. The proof that A\* then returns an optimal route runs as follows. Suppose the goal pops with cost `G`, and suppose a cheaper route of cost `C < G` exists. Some cell `n` on that route is already in the queue with its best `g`. Its priority `g(n) + h(n)` is at most `C`, by admissibility, so it is less than `G`. The queue would pop `n` before the goal, which contradicts the goal popping first with `G`.

#### Closing Cells And Rejecting Old Entries

A heuristic is **consistent** when `h(u) <= w(u, v) + h(v)` for every move from `u` to `v` with entering cost `w(u, v)`. Manhattan distance is consistent on this grid. With a consistent heuristic the priorities along any route never decrease, so the first time a cell pops, its `g` is final and the planner never reopens it. An admissible heuristic that is not consistent keeps the answer exact only if cells can be reopened.

The queue may hold several entries for one cell, because each improvement of `g` pushes a new entry. An old entry whose `g` is larger than the best known value is a **stale entry**. The planner skips it when it pops. The invariant of the search is that the entry popped with the smallest `f` never has a larger `f` than the cost of the optimal route, so the first goal pop is optimal.

<!-- stage: variables -->
### Cost, Guess And Best Known

The search keeps five pieces of state.

- **best** is a matrix with the cheapest known cost from the start to each cell. It starts at a huge value and only decreases.
- **h** is the heuristic value of a cell. Here it equals `|row - gr| + |col - gc|`, the Manhattan distance to the goal cell.
- **f** is `g + h` for an entry. The queue orders entries by `f`, then by row, then by column, so ties are deterministic.
- **prev** is a matrix that stores the cell from which `best` was reached. It rebuilds the route after the goal pops.
- **expanded** is the count of non-stale pops. It measures how much of the floor the search touched.

The entry cost matrix uses 0 for a wall and values from 1 to 9 for open cells. Every move costs at least 1, so each step lowers the Manhattan distance by at most 1 and that distance stays admissible.

<!-- stage: trace -->
### Tracing Two Searches

#### A Search That Goes Straight

The first trace runs A\* with Manhattan distance on a 3 by 4 floor. The cells appear row by row, with 0 for a wall. The start is the top left cell and the goal is the bottom right cell. The pointer `cur` marks the cell that pops. At the start `f` is 5, the Manhattan distance, and every pop keeps `f` at 5, so the search never leaves the cheapest route. The two cells on the right edge of the first two rows never pop. The search pops 7 cells and returns the cost 5.

```trace
{"cells":["1","1","1","2","0","1","0","1","0","1","1","1"],"pointers":["cur"],"steps":[{"at":{"cur":-1},"vars":{"queue":1,"best":"start 0"},"note":"Start: the start cell has g 0 and f 5, the Manhattan distance."},{"at":{"cur":0},"vars":{"g":0,"f":5,"pushed":1,"queue":1},"note":"Pop row 0, column 0 with g 0 and f 5. Push 1 neighbour entries."},{"at":{"cur":1},"vars":{"g":1,"f":5,"pushed":2,"queue":2},"note":"Pop row 0, column 1 with g 1 and f 5. Push 2 neighbour entries."},{"at":{"cur":2},"vars":{"g":2,"f":5,"pushed":1,"queue":2},"note":"Pop row 0, column 2 with g 2 and f 5. Push 1 neighbour entries."},{"at":{"cur":5},"vars":{"g":2,"f":5,"pushed":1,"queue":2},"note":"Pop row 1, column 1 with g 2 and f 5. Push 1 neighbour entries."},{"at":{"cur":9},"vars":{"g":3,"f":5,"pushed":1,"queue":2},"note":"Pop row 2, column 1 with g 3 and f 5. Push 1 neighbour entries."},{"at":{"cur":10},"vars":{"g":4,"f":5,"pushed":1,"queue":2},"note":"Pop row 2, column 2 with g 4 and f 5. Push 1 neighbour entries."},{"at":{"cur":11},"vars":{"g":5,"f":5,"queue":1},"note":"The goal pops with g 5. The first goal pop is optimal, so the search returns 5 after 7 expansions."}]}
```

#### A Search That Skips An Old Entry

The second trace uses a 2 by 4 floor with enter costs up to 4. The goal is the bottom right cell. One cell receives a first entry through an expensive step and a second entry through a cheaper route. When the first entry pops, the planner sees that its `g` is larger than `best` and skips it. The note of that step says so, and no neighbour is pushed. The skip costs one pop and does not change the answer, which is the cost 8.

```trace
{"cells":["1","4","1","1","1","1","3","3"],"pointers":["cur"],"steps":[{"at":{"cur":-1},"vars":{"queue":1,"best":"start 0"},"note":"Start: the start cell has g 0 and f 4, the Manhattan distance."},{"at":{"cur":0},"vars":{"g":0,"f":4,"pushed":2,"queue":2},"note":"Pop row 0, column 0 with g 0 and f 4. Push 2 neighbour entries."},{"at":{"cur":4},"vars":{"g":1,"f":4,"pushed":1,"queue":2},"note":"Pop row 1, column 0 with g 1 and f 4. Push 1 neighbour entries."},{"at":{"cur":5},"vars":{"g":2,"f":4,"pushed":1,"queue":2},"note":"Pop row 1, column 1 with g 2 and f 4. Push 1 neighbour entries."},{"at":{"cur":6},"vars":{"g":5,"f":6,"pushed":2,"queue":3},"note":"Pop row 1, column 2 with g 5 and f 6. Push 2 neighbour entries."},{"at":{"cur":1},"vars":{"g":4,"f":7,"pushed":1,"queue":3},"note":"Pop row 0, column 1 with g 4 and f 7. Push 1 neighbour entries."},{"at":{"cur":2},"vars":{"g":5,"f":7,"pushed":1,"queue":3},"note":"Pop row 0, column 2 with g 5 and f 7. Push 1 neighbour entries."},{"at":{"cur":3},"vars":{"g":6,"f":7,"pushed":0,"queue":2},"note":"Pop row 0, column 3 with g 6 and f 7. Push 0 neighbour entries."},{"at":{"cur":2},"vars":{"g":6,"best":5,"f":8,"queue":1},"note":"The entry for row 0, column 2 has g 6, but best is 5. The entry is stale, so the planner skips it."},{"at":{"cur":7},"vars":{"g":8,"f":8,"queue":0},"note":"The goal pops with g 8. The first goal pop is optimal, so the search returns 8 after 8 expansions."}]}
```

<!-- stage: code -->
### A Star On A Cost Grid

#### The Search

The method keeps the loop of the naive planner. The queue entries hold `f`, `g`, row and column, and the comparator breaks `f` ties by row and then column.

```java
final class AStarGrid {
    static int shortest(int[][] cost, int sr, int sc, int gr, int gc) {
        int R = cost.length, C = cost[0].length;
        int[][] best = new int[R][C];
        for (int[] row : best) java.util.Arrays.fill(row, Integer.MAX_VALUE);
        java.util.PriorityQueue<int[]> pq = new java.util.PriorityQueue<>(
            (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0])
                    : x[2] != y[2] ? Integer.compare(x[2], y[2]) : Integer.compare(x[3], y[3]));
        best[sr][sc] = 0;
        pq.add(new int[]{Math.abs(sr - gr) + Math.abs(sc - gc), 0, sr, sc});
        int[] dr = {-1, 1, 0, 0}, dc = {0, 0, -1, 1};
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int r = cur[2], c = cur[3];
            if (cur[1] > best[r][c]) continue;                // stale entry: a cheaper route was recorded
            if (r == gr && c == gc) return cur[1];            // first goal pop is optimal
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nc < 0 || nr >= R || nc >= C || cost[nr][nc] == 0) continue;
                int g = cur[1] + cost[nr][nc];                 // cost so far of the neighbour
                if (g < best[nr][nc]) {
                    best[nr][nc] = g;
                    int h = Math.abs(nr - gr) + Math.abs(nc - gc);   // admissible guess
                    pq.add(new int[]{g + h, g, nr, nc});
                }
            }
        }
        return -1;
    }
}
```

#### Cost

- **Time** is O(V log V) in the worst case, the same bound as Dijkstra, with `V` the count of cells.
- **Space** is O(V) for `best` and the queue.
- **Expansions** shrink in most inputs against Dijkstra's, because every cell with `g + h` above the optimal cost stays in the queue.

<!-- stage: applicability -->
### When A Star Applies

#### Recognizing The Pattern

Use A\* when a shortest-path search has one goal state, the graph is large, and a cheap lower bound on the remaining cost is available. Grid routing, puzzle solving and map navigation have this shape. Before coding, state the heuristic and check two things: it never exceeds the true remaining cost, and it satisfies `h(u) <= w + h(v)` on every move. The invariant to keep is that `f = g + h` never exceeds the cost of the optimal route for the entry that pops.

#### False Friends

Greedy best-first search ranks by `h` alone. It looks like A\* and runs faster on many inputs, but it can return a long route because it ignores `g`. Dijkstra's algorithm with an early stop at the goal is another false friend, since it ranks by `g` alone and gains no direction. Breadth-first search is exact only when all moves cost the same.

#### When The Method Does Not Apply

If the search needs distances to every cell, as in a map of reachable areas, the heuristic toward one goal helps nothing, and Dijkstra's algorithm is the right tool. If no lower bound better than 0 exists, A\* equals Dijkstra and adds only a constant factor. If edge costs can be negative, neither algorithm is valid.

<!-- stage: exercises -->
### Exercises

#### [Build] Dijkstra With Zero Heuristic (Author exercise)
<!-- id: as35-zero-heuristic -->

**Prerequisites.** The priority `f = g + h` and the stale-entry skip from this lesson.

**Problem.** Write `int[] zeroHeuristic(int[][] cost, int sr, int sc, int gr, int gc)`. The grid `cost` has entries 0 for a wall and 1 to 9 for an open cell with that entering cost. A move goes to one of four neighbours and pays the entering cost of the target cell. Run the search with `h = 0` for every cell. The queue pops the smallest `f`, then the smallest row, then the smallest column. Return `{c, e}`, where `c` is the cheapest cost from the start to the goal or -1 if unreachable, and `e` is the number of non-stale pops, counting the goal pop, before the method returns.

**Constraints.** The limits are:
- **Grid** has 1 to 50 rows and 1 to 50 columns.
- **Cells** the start and the goal are open cells.
- **Costs** are integers from 0 to 9.
- **Unreachable** goals return `{-1, e}` after the queue is empty.

**Example 1.** Input `cost = [[1,1,1],[1,0,1],[1,1,1]]`, start (0,0), goal (2,2), output `{4, 8}`.

**Example 2.** Input `cost = [[1,0,1]]`, start (0,0), goal (0,2), output `{-1, 1}`.

**Hint.** What does `f` equal when `h` is 0, and which pops count as stale?

**Changed decision.** Basic case: the heuristic is fixed at 0, so the loop is Dijkstra's algorithm with a counter.

#### [Vary] Manhattan Grid Heuristic (Author exercise)
<!-- id: as35-manhattan-grid -->

**Prerequisites.** The Dijkstra With Zero Heuristic exercise above. This exercise changes one decision: the priority adds the Manhattan distance.

**Problem.** Write `int[] manhattan(int[][] cost, int sr, int sc, int gr, int gc)` with the same grid, move and tie rules as the previous exercise. Use `h = |row - gr| + |col - gc|` and the priority `f = g + h`. Return `{c, e}` with the same meaning as before.

**Constraints.** The limits are:
- **Grid** has 1 to 50 rows and 1 to 50 columns.
- **Costs** are integers from 0 to 9, and an open cell costs at least 1 to enter.
- **Cost** `c` equals the Dijkstra cost for the same input.
- **Expansions** `e` usually shrinks against the count for `h = 0`, and ties at the optimal cost can make the two counts equal.

**Example 1.** Input a 3 by 4 grid of all 1, start (0,0), goal (0,3), output `{3, 4}`.

**Example 2.** Input `cost = [[1,2,1,1],[1,1,1,3],[2,1,1,1]]`, start (0,0), goal (2,3), output `{5, 7}`, while the zero heuristic gives `{5, 11}`.

**Hint.** Why does a cheaper entering cost than 1 never occur, and why does that keep `h` admissible?

**Changed decision.** The heuristic grows from 0 to the Manhattan distance, and the answer stays equal while the expansions shrink.

#### [Boundary] Overestimating Heuristic (Author exercise)
<!-- id: as35-overestimating-heuristic -->

**Prerequisites.** The Manhattan Grid Heuristic exercise above. This exercise changes the guess from admissible to inflated.

**Problem.** Write `int inflated(int[][] cost, int sr, int sc, int gr, int gc, int w)`. Use the same grid, moves and tie rules, but set `h = w * (|row - gr| + |col - gc|)` for an integer `w >= 1`. Skip stale entries as before, never reopen a cell that has been expanded, and return the cost `g` of the first goal pop, or -1 if the queue empties. The result can be larger than the cheapest cost.

**Constraints.** The limits are:
- **Grid** has 1 to 12 rows and 1 to 12 columns.
- **Costs** are integers from 0 to 9, and the start and the goal are open.
- **Weight** `w` is from 1 to 10.
- **Closed** cells are never reopened, even if a cheaper route to them appears later.

**Example 1.** Input `cost = [[1,1,1,2],[0,1,0,1],[0,1,1,1]]`, start (0,0), goal (2,3), `w = 1`, output `5`.

**Example 2.** The same input with `w = 4` outputs `6`, which is larger than the cheapest cost.

**Hint.** Which cell gets popped first when the guess dominates the cost so far, and what does that cell commit to?

**Changed decision.** The guess is allowed to exceed the true remaining cost, and the exercise shows the answer stops being optimal.

#### [Recognize] A-Star Grid Path (Author exercise)
<!-- id: as35-grid-path -->

**Prerequisites.** The Overestimating Heuristic exercise above. This exercise returns the route, not only its cost.

**Problem.** Write `List<int[]> route(int[][] cost, int sr, int sc, int gr, int gc)`. Use the Manhattan heuristic, the tie rule and the move rules from the previous exercises. Store for each cell the predecessor that gave its best known cost, and replace it only when a strictly cheaper cost appears. Neighbours are tried in the order up, down, left, right. Return the cells of the route from the start to the goal inclusive, or an empty list if the goal is unreachable.

**Constraints.** The limits are:
- **Grid** has 1 to 100 rows and 1 to 100 columns.
- **Costs** are integers from 0 to 9, with 0 for a wall.
- **Start and goal** are open cells and may be the same cell.
- **Route** consecutive cells are neighbours, and its cost is the entering cost of every cell except the start.

**Example 1.** Input `cost = [[1,1,1,2],[0,1,0,1],[0,1,1,1]]`, start (0,0), goal (2,3), output `[(0,0),(0,1),(1,1),(2,1),(2,2),(2,3)]`.

**Example 2.** Input `cost = [[7]]`, start (0,0), goal (0,0), output `[(0,0)]`.

**Hint.** State the heuristic and check admissibility before coding. Then ask what must be recorded when a stale entry pops.

**Changed decision.** The state grows by one matrix of predecessors, and the stale-entry rule must keep that matrix in step with `best`.
