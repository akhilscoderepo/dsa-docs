<!-- lesson-kind: combination -->
<!-- lesson-id: a-star-heuristics -->
## A-Star Heuristics

<!-- stage: context -->
### A Faster Route Planner That Lies

A navigation team speeds up its route planner by adding a guess of the remaining drive time to every road junction. The guess is the straight-line distance multiplied by a "typical detour factor" of 1.5. Benchmarks improve, and most routes look right. Then support receives a ticket: for one commuter pair the app suggests a 31 minute route while a 24 minute route exists. The team cannot tell whether the guess, the graph or the search is wrong, because no test checks the guess itself.

The search of the previous lesson is exact only when the guess obeys a rule, and a rule that nobody checks is a rule that breaks in production. This lesson asks how to test a guess against a graph before trusting it, and what the search must do when the guess satisfies the weaker of the two rules.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

Chapter 24 supplied shortest paths on weighted directed graphs. Its Dijkstra loop keeps a queue of entries ordered by cost so far, skips entries whose cost is larger than the best known cost, and finalizes a vertex when it pops. It also supplied the proof that this works because no edge weight is negative.

The lesson A Star Search supplied the priority `f = g + h`, the two properties of a guess `h`, and the proof that the first goal pop is optimal when the guess never overestimates. It worked on a grid, where Manhattan distance is the guess and no test of the guess was needed, because the grid made the guess obviously valid.

The new work is the combination on general graphs. The guess becomes an array of numbers supplied by a caller, and the program has to check it against the graph. The lesson derives a test for each of the two properties and shows that a consistent guess turns the search into Dijkstra's algorithm on adjusted edge weights, which reuses the chapter 24 proof. It then shows what changes when the guess is valid but not consistent.

<!-- stage: naive -->
### Dijkstra With A Guess Bolted On

The direct design takes the Dijkstra loop and adds the guess to the priority of every pushed entry. The graph has `n` vertices and directed edges `{u, v, w}` with `w >= 0`. The array `h` holds one guess per vertex. The loop skips stale entries and returns the cost at the first pop of the goal.

```java
final class GuessedSearch {
    static int search(int n, int[][] edges, int start, int goal, int[] h) {
        java.util.List<int[]>[] adj = new java.util.List[n];
        for (int i = 0; i < n; i++) adj[i] = new java.util.ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[]{e[1], e[2]});
        int[] best = new int[n];
        java.util.Arrays.fill(best, Integer.MAX_VALUE);
        java.util.PriorityQueue<int[]> pq = new java.util.PriorityQueue<>((x, y) -> x[0] - y[0]);
        best[start] = 0;
        pq.add(new int[]{h[start], start, 0});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[2] > best[cur[1]]) continue;               // stale entry
            if (cur[1] == goal) return cur[2];                 // first pop of the goal
            for (int[] nb : adj[cur[1]]) {
                int g = cur[2] + nb[1];
                if (g < best[nb[0]]) { best[nb[0]] = g; pq.add(new int[]{g + h[nb[0]], nb[0], g}); }
            }
        }
        return -1;
    }
}
```

With `h` set to all zeros the code is Dijkstra's algorithm. With a guess array it is faster on many inputs, and nothing in the code checks the guess.

```predict
The graph has three vertices S (0), A (1) and G (2), with edges S to G of weight 10, S to A of weight 1 and A to G of weight 1. The guess is 0 for S, 20 for A and 0 for G. What cost does the search return for the start S and the goal G? What is the cheapest cost?

The start entry has priority 0 and pops first. It pushes G with cost 10 and priority 10, and A with cost 1 and priority 21. The entry for G has the smaller priority, so G pops next and the search returns 10. The cheapest route goes through A and costs 2. The guess of 20 at A is far above the real remaining cost 1, so the search never looks at A.
```

<!-- stage: bottleneck -->
### Nothing Checks The Guess

The search costs O(E log V) time and O(V + E) space, the same as Dijkstra's algorithm. The cost is not the problem. The problem is that the answer depends on the guess, and the guess is an input that is never validated. The predict example shows a single wrong number turning the exact answer 2 into 10.

Two questions need an answer that a program can compute. First, how far is each vertex from the goal in truth? If the program knows that distance, it can compare it with the guess and report a violation. Second, a valid guess can still be loose in one particular way: it can drop by more than the edge weight when the search moves from one vertex to the next. The first lesson's proof assumed the guess never overestimates, but its stronger rule, which lets a vertex be finalized at its first pop, needs more.

A graph with many vertices also makes a manual check impossible. A planner with a million junctions has a million guesses. The test has to be a loop over the vertices and the edges, with a clear yes or no and a measure of how far the worst violation reaches.

<!-- stage: insight -->
### Test The Guess, Then Pick The Loop

<!-- names: true remaining cost, reduced weight, reopen -->

#### Computing The True Remaining Cost

The **true remaining cost** of a vertex `v`, written `h*(v)`, is the length of the cheapest path from `v` to the goal. One Dijkstra run on the reversed graph, started at the goal, computes `h*` for every vertex at once in O((V + E) log V) time. A guess is admissible when `h(v) <= h*(v)` for every vertex that can reach the goal. The test is a single comparison per vertex, and the largest value of `h(v) - h*(v)` measures how badly the guess overestimates.

#### Reduced Weights

The **reduced weight** of an edge `(u, v)` with weight `w` is `w + h(v) - h(u)`. The guess is consistent when every reduced weight is at least 0. The priority of the search is `f(v) = g(v) + h(v)`. Along any path from the start to `v`, the reduced weights add up to `g(v) + h(v) - h(start)`, because the intermediate guesses cancel in pairs. So the search orders vertices by the cost to reach them under the reduced weights, plus the constant `h(start)`. If every reduced weight is non-negative, the search is Dijkstra's algorithm on the reduced graph. The chapter 24 proof applies, and each vertex is finalized at its first pop. Every start-to-goal path changes length by the same amount, `h(goal) - h(start)`, so the cheapest path is the same in both graphs.

#### When Reduced Weights Go Negative

A guess can be admissible and still have a negative reduced weight on some edge. The search can then pop a vertex with a cost that a later pop improves. To stay exact, the search must **reopen** the vertex: when an entry with a smaller cost than the recorded cost arrives for a vertex that was already expanded, it expands the vertex again and updates its neighbours. The stale-entry skip still discards entries whose cost is larger than the recorded cost. Reopening costs extra expansions, and the optimality proof from the previous lesson still holds for an admissible guess.

The invariant is that the recorded cost of a vertex never increases, and the first goal pop is optimal as long as the guess is admissible and cheaper entries are never discarded.

<!-- stage: variables -->
### Guess, Remaining Cost And Excess

The checker and the search keep the following names.

- **best** is the array of cheapest known costs from the start. It only decreases.
- **h** is the guess array supplied by the caller, one number per vertex.
- **hstar** is the true remaining cost per vertex, computed by Dijkstra on reversed edges from the goal.
- **excess** is the largest value of `h[v] - hstar[v]`, or 0 if no guess exceeds its true remaining cost.
- **gap** is the reduced weight `w + h[v] - h[u]` of one edge. A negative gap marks an inconsistent edge.
- **reopened** counts pops of a vertex that had already been expanded.

Every vertex must be able to reach the goal for the checks to be defined. A vertex that cannot reach the goal has no finite true remaining cost.

<!-- stage: trace -->
### Tracing A Search And A Reopening

#### A Guess That Saves Work

The first trace runs the search on a graph of seven vertices placed on a plane. The guess is the Manhattan distance to the goal, and every edge is at least as long as the Manhattan distance of its endpoints, so the guess is consistent. The pointer `cur` marks the vertex that pops. The start pops first with cost 0 and priority equal to its guess. Vertex 5 pops next, because its priority is the lowest in the queue, and then the goal, vertex 6. Only three vertices are finalized, while Dijkstra's algorithm finalizes six on the same graph.

```trace
{"cells":["0","1","2","3","4","5","6"],"pointers":["cur"],"steps":[{"at":{"cur":-1},"vars":{"queue":"vertex 0 (f 4)"},"note":"Start: vertex 0 has cost 0 and guess 4, so its priority is 4."},{"at":{"cur":0},"vars":{"g":0,"h":4,"f":4,"queue":"5 (f 7), 3 (f 10)"},"note":"Vertex 0 pops with cost 0, guess 4 and priority 4. Its edges push or improve the entries in the queue."},{"at":{"cur":5},"vars":{"g":2,"h":5,"f":7,"queue":"6 (f 9), 3 (f 10), 4 (f 11)"},"note":"Vertex 5 pops with cost 2, guess 5 and priority 7. Its edges push or improve the entries in the queue."},{"at":{"cur":6},"vars":{"g":9,"f":9,"pops":3},"note":"The goal pops with cost 9 after 3 finalized vertices. The first goal pop is optimal."}]}
```

#### A Vertex Opened Twice

The second trace uses a 2 by 4 floor with enter costs and a guess that is admissible but not consistent. The cells appear row by row. The cell at row 1, column 1 pops first with cost 3 through the top route. The cell at row 1, column 0 pops later with cost 1, and its neighbour at row 1, column 1 now has a cheaper cost 2. The entry for cost 2 has a lower priority than the earlier pop, and the search expands the cell again. The note of that step says so. The goal then pops with cost 5, the cheapest cost.

```trace
{"cells":["2","2","9","1","1","1","2","1"],"pointers":["cur"],"steps":[{"at":{"cur":-1},"vars":{"queue":"cell 0 (f 0)"},"note":"Start: the top left cell has cost 0 and guess 0."},{"at":{"cur":0},"vars":{"g":0,"f":0,"reopened":0},"note":"Pop row 0, column 0 with cost 0 and priority 0."},{"at":{"cur":1},"vars":{"g":2,"f":3,"reopened":0},"note":"Pop row 0, column 1 with cost 2 and priority 3."},{"at":{"cur":5},"vars":{"g":3,"f":3,"reopened":0},"note":"Pop row 1, column 1 with cost 3 and priority 3."},{"at":{"cur":4},"vars":{"g":1,"f":4,"reopened":0},"note":"Pop row 1, column 0 with cost 1 and priority 4."},{"at":{"cur":5},"vars":{"g":2,"f":2,"reopened":1},"note":"Pop row 1, column 1 with cost 2 and priority 2. The cell was expanded before, and this entry has a smaller cost, so the search reopens it."},{"at":{"cur":6},"vars":{"g":4,"f":5,"reopened":1},"note":"Pop row 1, column 2 with cost 4 and priority 5."},{"at":{"cur":7},"vars":{"g":5,"f":5,"reopened":1},"note":"The goal pops with cost 5. The search expanded 1 cell a second time."}]}
```

<!-- stage: code -->
### Check The Guess And Search

#### The Checker

The method `trueRemaining` runs Dijkstra on the reversed edges from the goal. The method `check` compares the guess with it and tests every edge.

```java
final class GuessChecker {
    static int[] trueRemaining(int n, int[][] edges, int goal) {
        java.util.List<int[]>[] rev = new java.util.List[n];
        for (int i = 0; i < n; i++) rev[i] = new java.util.ArrayList<>();
        for (int[] e : edges) rev[e[1]].add(new int[]{e[0], e[2]});     // reversed edge
        int[] d = new int[n];
        java.util.Arrays.fill(d, Integer.MAX_VALUE);
        java.util.PriorityQueue<int[]> pq = new java.util.PriorityQueue<>((x, y) -> x[0] - y[0]);
        d[goal] = 0;
        pq.add(new int[]{0, goal});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            if (cur[0] > d[cur[1]]) continue;                           // stale entry
            for (int[] nb : rev[cur[1]])
                if (cur[0] + nb[1] < d[nb[0]]) { d[nb[0]] = cur[0] + nb[1]; pq.add(new int[]{d[nb[0]], nb[0]}); }
        }
        return d;
    }

    static int[] check(int n, int[][] edges, int goal, int[] h) {
        int[] hs = trueRemaining(n, edges, goal);
        int excess = 0, admissible = 1, consistent = 1;
        for (int v = 0; v < n; v++) {
            excess = Math.max(excess, h[v] - hs[v]);                    // how far the guess overshoots
            if (h[v] > hs[v]) admissible = 0;
        }
        for (int[] e : edges)
            if (e[2] + h[e[1]] - h[e[0]] < 0) consistent = 0;           // negative reduced weight
        return new int[]{admissible, consistent, excess};
    }
}
```

#### Cost

- **trueRemaining** costs O((V + E) log V) time and O(V + E) space.
- **check** adds O(V + E) time for the comparisons.
- **Search** with reopening costs O(E log V) per expansion round, and the number of reopenings is zero when the guess is consistent.

<!-- stage: applicability -->
### When To Test A Guess

#### Recognizing The Pattern

Use this combination when a shortest-path search has one goal, edge weights are non-negative, and a guess toward the goal comes from outside the graph, for example from coordinates, from a table or from a learned model. Before shipping the guess, compute the true remaining cost on test graphs and run the edge test. The invariant to protect is that the guess never exceeds the true remaining cost, and that a negative reduced weight triggers reopening.

#### False Friends

Scaling the guess by a constant above 1 looks like a safe speed-up and is a false friend, since it makes the guess exceed the true remaining cost whenever the path is not a straight line. A guess that is exact on a few test routes is a second false friend: the check must hold at every vertex. Passing the admissibility test does not prove consistency, and the two tests answer different questions.

#### When The Method Does Not Apply

If edge weights can be negative, neither Dijkstra's algorithm nor A* is valid. If the goal changes for every query, computing the true remaining cost once per goal costs as much as the search, so the checker belongs to test time and not to query time. If the graph is a tree with a unique path, no guess helps.

<!-- stage: exercises -->
### Exercises

#### [Build] Zero-Heuristic Search (Author exercise)
<!-- id: ah35-zero-heuristic-order -->

**Prerequisites.** The Dijkstra loop of chapter 24 and the priority `f = g + h` from the A Star Search lesson.

**Problem.** Write `int[] finalizeOrder(int n, int[][] edges, int start, int goal)`. Run the search with `h = 0` for every vertex on the directed graph with vertices `0` to `n - 1` and edges `{u, v, w}`. The queue pops the smallest cost, then the smallest vertex id. Return the vertices in the order in which non-stale pops finalize them, ending with the goal. If the goal is unreachable, return every reachable vertex in that order.

**Constraints.** The limits are:
- **Vertices** number from 1 to 1000, and edges from 0 to 5000.
- **Weights** are integers from 0 to 1000.
- **Ties** go to the smaller vertex id.
- **Start and goal** are valid vertex ids and may be equal.

**Example 1.** Input `n = 6`, `edges = [[0,1,2],[0,2,1],[1,3,1],[2,3,4],[2,4,1],[4,3,1],[3,5,2]]`, `start = 0`, `goal = 5`, output `[0, 2, 1, 4, 3, 5]`.

**Example 2.** Input `n = 3`, `edges = [[0,1,1]]`, `start = 0`, `goal = 2`, output `[0, 1]`.

**Hint.** Which entries pop with equal cost, and which vertex id goes first?

**Changed decision.** Basic case: the zero guess makes the loop Dijkstra's algorithm, and the result is the order of finalization.

#### [Vary] Manhattan Grid Search (Author exercise)
<!-- id: ah35-manhattan-graph-search -->

**Prerequisites.** The Zero-Heuristic Search exercise above. This exercise adds coordinates and a guess.

**Problem.** Write `int[] manhattanSearch(int n, int[][] pos, int[][] edges, int start, int goal)`. Vertex `i` has the integer position `pos[i] = {x, y}`. Every edge `{u, v, w}` has `w` at least the Manhattan distance between `pos[u]` and `pos[v]`. Use the guess `h(v) = |x_v - x_goal| + |y_v - y_goal|` and the priority `g + h`. The queue pops the smallest priority, then the smallest vertex id. Return `{cost, pops}`, where `cost` is the cheapest cost or -1 and `pops` is the number of non-stale pops, counting the goal pop.

**Constraints.** The limits are:
- **Vertices** number from 1 to 1000, and edges from 0 to 5000.
- **Coordinates** are integers from 0 to 1000.
- **Weights** satisfy the Manhattan bound for every edge.
- **Ties** go to the smaller vertex id.

**Example 1.** Input `n = 7`, `pos = [[0,0],[4,1],[3,3],[2,2],[1,3],[0,1],[4,0]]`, `edges = [[2,4,3],[0,5,2],[0,3,6],[3,5,4],[2,6,5],[5,6,7],[3,4,4],[5,4,3],[4,2,2],[6,1,1],[3,6,4]]`, `start = 0`, `goal = 6`, output `{9, 3}`.

**Example 2.** Input `n = 6`, `pos = [[0,0],[1,0],[0,2],[2,1],[1,3],[3,3]]`, `edges = [[0,1,1],[0,2,2],[1,3,2],[2,4,2],[3,5,3],[4,5,3],[2,3,4],[1,4,5]]`, `start = 0`, `goal = 5`, output `{6, 6}`.

**Hint.** Why does the Manhattan bound on every edge keep the guess from exceeding the true remaining cost?

**Changed decision.** The graph is general and carries coordinates, and the answer reports how many vertices were finalized.

#### [Boundary] Inadmissible Counterexample (Author exercise)
<!-- id: ah35-check-guess -->

**Prerequisites.** The Manhattan Grid Search exercise above. This exercise tests a guess instead of using it.

**Problem.** Write `int[] checkGuess(int n, int[][] edges, int goal, int[] h)`. Compute the true remaining cost of every vertex by Dijkstra on the reversed edges from `goal`. Return `{admissible, consistent, excess}`. The value `admissible` is 1 when `h[v] <= hstar[v]` for every vertex, else 0. The value `consistent` is 1 when `w + h[v] - h[u] >= 0` for every edge `{u, v, w}`, else 0. The value `excess` is the largest `h[v] - hstar[v]`, or 0 if no vertex exceeds it.

**Constraints.** The limits are:
- **Vertices** number from 1 to 1000, and edges from 0 to 5000.
- **Weights** are integers from 0 to 1000.
- **Reachability** holds: every vertex can reach the goal.
- **Guesses** are integers from 0 to 10^6.

**Example 1.** Input the graph of the first Build example with `goal = 5` and `h = [5, 3, 4, 2, 3, 0]`, output `{1, 1, 0}`.

**Example 2.** Input the same graph with `h = [7, 3, 4, 2, 3, 0]`, output `{0, 0, 2}`. Input the same graph with `h = [0, 0, 4, 0, 0, 0]`, output `{1, 0, 0}`.

**Hint.** Which graph does the Dijkstra run use to measure distances to the goal?

**Changed decision.** The guess becomes the object under test, and the answer separates admissibility from consistency.

#### [Recognize] A-Star Grid Path (Author exercise)
<!-- id: ah35-reopen-grid -->

**Prerequisites.** The Inadmissible Counterexample exercise above and the stale-entry rule from the A Star Search lesson. This exercise uses a guess that is admissible but not consistent.

**Problem.** Write `int[] searchWithReopen(int[][] cost, int sr, int sc, int gr, int gc, int[][] h)`. The matrix `cost` has 0 for a wall and 1 to 9 for the entering cost of an open cell. The matrix `h` holds an admissible guess per cell. Run the search with the priority `g + h`. A pop is stale when its `g` is larger than the recorded cost. A non-stale pop of a cell that was already expanded is a reopening. The queue pops the smallest priority, then the smallest row, then the smallest column. Return `{cost, reopened}`, where `cost` is the cheapest cost or -1 and `reopened` is the number of reopenings before the goal pops.

**Constraints.** The limits are:
- **Grid** has 1 to 30 rows and 1 to 30 columns.
- **Costs** are integers from 0 to 9, and the start and the goal are open.
- **Guess** values are integers from 0 up to the true remaining cost.
- **Moves** go to the four neighbours and pay the entering cost.

**Example 1.** Input `cost = [[2,2,9,1],[1,1,2,1]]`, start (0,0), goal (1,3), `h = [[0,1,2,0],[3,0,1,0]]`, output `{5, 1}`.

**Example 2.** Input the same grid with `h` equal to zero everywhere, output `{5, 0}`.

**Hint.** What must the search do with a cheaper entry for a cell that it has already expanded?

**Changed decision.** The guess is admissible only, so cells can be expanded more than once, and the answer counts the extra expansions.
