<!-- lesson-kind: standard -->
<!-- lesson-id: floyd-warshall -->
## Find All Distances With Floyd Warshall

<!-- stage: context -->
### One Lookup For Every Server Pair

#### Latency Between Any Two Servers

A service mesh runs five servers, and the operations team has measured the one-way latency in milliseconds on some of the links between them. A message from server 0 to server 1 often travels faster through server 2 than over the direct link. The router must answer "what is the lowest latency from server a to server b" for any pair, thousands of times per second. Recomputing a route for every query is too slow. The team wants a table that the program fills once and reads in constant time.

#### The Servers As A Graph

Number the servers 0 to n - 1. Each measured link is a directed edge with a nonnegative **weight**, which is its latency. A **route** is a sequence of edges, and its cost is the sum of the weights. The **distance** from a to b is the lowest cost over all routes from a to b. If no route exists, the pair has no distance. The input lists the edges, and the method must not change that list.

The mesh is small and dense, so many pairs are linked directly or almost directly. This lesson asks how to fill the whole n by n table of distances with code that stays short and reuses work between pairs.

<!-- stage: naive -->
### Searching Every Route For Every Pair

The first attempt treats each pair on its own. For a pair (a, b), a depth-first search starts at a and walks along edges. It never visits a server twice on one route. Whenever it reaches b, it compares the cost of the current route with the best cost so far, and then it backs up to try other routes.

```java
static long[][] allRoutes(int n, int[][] edges) {
    long[][] w = new long[n][n];
    for (long[] row : w) Arrays.fill(row, -1);
    for (int[] e : edges) {
        if (w[e[0]][e[1]] == -1 || e[2] < w[e[0]][e[1]]) w[e[0]][e[1]] = e[2];
    }
    long[][] best = new long[n][n];
    for (int a = 0; a < n; a++) {
        for (int b = 0; b < n; b++) {
            best[a][b] = -1;
            if (a == b) { best[a][b] = 0; continue; }
            boolean[] used = new boolean[n];
            used[a] = true;
            best[a][b] = search(w, used, a, b, 0, -1);
        }
    }
    return best;
}

static long search(long[][] w, boolean[] used, int at, int goal, long cost, long best) {
    if (at == goal) return best == -1 || cost < best ? cost : best;
    for (int next = 0; next < w.length; next++) {
        if (w[at][next] == -1 || used[next]) continue;
        used[next] = true;
        best = search(w, used, next, goal, cost + w[at][next], best);
        used[next] = false;
    }
    return best;
}
```

The method is correct, because it looks at every route that repeats no server. A route with a repeated server never costs less when all weights are nonnegative. The remaining question is how many routes it looks at.

```predict
Ten servers are linked in both directions by every pair. About how many routes does the search look at for one pair, and how many for the whole table?

For one pair (a, b), the search follows every ordered choice of a subset of the other eight servers as stops. That is 109601 routes for one pair. The table has 90 pairs with a different a and b, so the method follows about 9.9 million routes for only ten servers. Each added server multiplies the work again.
```

<!-- stage: bottleneck -->
### Routes Are Counted Again And Again

The number of routes grows like the factorial of n, so the worst case is O(n!) per pair. Twenty servers are already far beyond any time limit. The work is also wasteful. The route 0, 2, 3 is the route to server 3, and it is also the start of routes from 0 to 4 and from 0 to 1. The search rebuilds that start for each of them. The cost of the cheapest part from 2 to 3 is computed again for every route that passes through 2.

A faster method must store a cheapest cost for each pair and reuse it. The n by n table has only n squared entries, which is tiny next to the number of routes. The open question is the order in which to improve the entries. Every entry must end with the true minimum after a small, fixed number of passes.

An answer that costs O(n^3) in time and O(n^2) in memory suits a small dense graph. The table must also treat a missing route as a value that never takes part in a sum.

<!-- stage: insight -->
### Allow One More Intermediate At A Time

The method keeps a table `dist` and lets more servers act as stops, one server per pass, until every server is allowed.

<!-- names: intermediate, round, sentinel -->

#### Intermediate Servers Of A Route

An **intermediate** of a route is any server on it except the first and the last one. The table has a precise meaning at every moment. After the round for server `k`, the entry `dist[i][j]` is the lowest cost of a route from `i` to `j` whose intermediates all have an index from 0 to `k`. Before any round, no intermediate is allowed, so the table holds only direct edges and a zero on the diagonal.

#### One Round For Server k

A **round** is one pass over every pair (i, j) for a fixed `k`. It compares the stored `dist[i][j]` with the sum `dist[i][k] + dist[k][j]` and keeps the smaller value. The claim is that this single comparison extends the meaning from "intermediates 0 to k - 1" to "intermediates 0 to k". Take the best route from `i` to `j` that may use `k`. If it does not stop at `k`, the old entry already holds its cost. If it stops at `k`, it stops there once, because a repeated stop never helps with nonnegative weights. Then it splits into a part from `i` to `k` and a part from `k` to `j`. Both parts use intermediates below `k`, so the old entries `dist[i][k]` and `dist[k][j]` already hold their best costs.

#### Updating The Table In Place

A round reads row `k` and column `k` while it writes other entries. These two lines do not change during the round. The entry `dist[k][k]` is 0, so the sum for `dist[i][k]` equals the old value, and the same holds for `dist[k][j]`. The round therefore needs no second table, and the method can write into one array. After the round for `n - 1`, every server is allowed, and each entry is a true distance. The three nested loops make O(n^3) comparisons.

#### The Sentinel For A Missing Route

A **sentinel** is a reserved value that stands for "no route", and this lesson uses `Long.MAX_VALUE` for it. The method never adds the sentinel to anything. It skips the comparison when `dist[i][k]` or `dist[k][j]` equals the sentinel. Without that guard, `Long.MAX_VALUE + 1` wraps to a large negative number that looks like a bargain. The table uses `long`, because a route of many edges with weights near two billion exceeds the range of `int`.

<!-- stage: variables -->
### The Table And The Three Loops

The method reads `n`, the number of servers, and `edges`, a list of triples `[from, to, weight]`. It changes neither. It creates one table and three loop counters.

- **dist** is a `long[n][n]` with `0` on the diagonal and `Long.MAX_VALUE` where no route is known.
- **k** is the server allowed as an intermediate in the current round, and it runs in the outermost loop.
- **i** and **j** are the first and last server of the pair under comparison.

Repeated edges between the same two servers keep the lowest weight. A self loop never lowers a diagonal entry, because every weight is nonnegative. The sum `dist[i][k] + dist[k][j]` is formed only when both parts are finite, so it cannot overflow through the sentinel.

<!-- stage: trace -->
### Two Runs On Five Servers

#### Correct Order With k Outermost

The first run uses seven links. Server 0 reaches server 1 with weight 4 and server 2 with weight 1. Server 2 reaches server 1 with weight 2 and server 3 with weight 5. Server 1 reaches server 3 with weight 1. Server 3 reaches server 4 with weight 3, and server 4 reaches server 0 with weight 2. Each cell is one round, and the pointer `k` marks the server allowed in that round. The variable `lowered` counts the entries that drop in the round. The variable `known` counts the pairs of different servers that have a finite entry after the round. Round 0 gives server 4 a route to server 1 through server 0, with cost 6. Round 2 lowers the entry from 0 to 1 from 4 to 3, because the route 0, 2, 1 costs 1 plus 2. After round 4, all 20 pairs are known and the table is final.

```trace
{"cells":["k=0","k=1","k=2","k=3","k=4"],"pointers":["k"],"steps":[{"at":{"k":0},"vars":{"lowered":2,"known":9},"note":"Intermediate 0 lowers 2 pairs; the first is 4 to 1, now 6."},{"at":{"k":1},"vars":{"lowered":3,"known":11},"note":"Intermediate 1 lowers 3 pairs; the first is 0 to 3, now 5."},{"at":{"k":2},"vars":{"lowered":4,"known":11},"note":"Intermediate 2 lowers 4 pairs; the first is 0 to 1, now 3."},{"at":{"k":3},"vars":{"lowered":3,"known":14},"note":"Intermediate 3 lowers 3 pairs; the first is 0 to 4, now 7."},{"at":{"k":4},"vars":{"lowered":6,"known":20},"note":"Intermediate 4 lowers 6 pairs; the first is 1 to 0, now 6."}]}
```

#### Wrong Order With k Innermost

The second run uses a ring of five links. Server 0 reaches server 1 with weight 2, and server 1 reaches server 2 with weight 2. Server 2 reaches server 3 with weight 3, and server 3 reaches server 4 with weight 6. Server 4 reaches server 0 with weight 5. This run moves `k` into the innermost loop and makes a single pass over the rows. Each cell is one finished row `i`. The variable `wrong` counts entries of that row that differ from the true distance, and `total` adds them up. Row 1 needs the route 1, 2, 3, 4, 0 with cost 16. When the pass handles `j = 0`, the entries from 1 to 4 and from 3 to 0 are still empty, so the row keeps no route. Row 2 has the same problem for its pairs with servers 0 and 1. Rows 3 and 4 happen to be right, so three wrong entries remain in the final table.

```trace
{"cells":["row 0","row 1","row 2","row 3","row 4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"wrong":0,"total":0},"note":"Row 0 ends with 0 wrong entries."},{"at":{"i":1},"vars":{"wrong":1,"total":1},"note":"Row 1 ends with 1 wrong entry. For example 1 to 0 holds no route, but the cheapest route costs 16."},{"at":{"i":2},"vars":{"wrong":2,"total":3},"note":"Row 2 ends with 2 wrong entries. For example 2 to 0 holds no route, but the cheapest route costs 14."},{"at":{"i":3},"vars":{"wrong":0,"total":3},"note":"Row 3 ends with 0 wrong entries."},{"at":{"i":4},"vars":{"wrong":0,"total":3},"note":"Row 4 ends with 0 wrong entries."}]}
```

<!-- stage: code -->
### Floyd Warshall With Three Loops

The method returns a new `long[][]` and leaves `edges` untouched. Pairs without a route keep `Long.MAX_VALUE`.

```java
static long[][] allDistances(int n, int[][] edges) {
    long[][] dist = new long[n][n];
    for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE);
    for (int v = 0; v < n; v++) dist[v][v] = 0;
    for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            if (dist[i][k] == Long.MAX_VALUE) continue;
            for (int j = 0; j < n; j++) {
                if (dist[k][j] == Long.MAX_VALUE) continue;
                long through = dist[i][k] + dist[k][j];
                if (through < dist[i][j]) dist[i][j] = through;
            }
        }
    }
    return dist;
}
```

The loop over `k` must stay outermost, so the loops over `i` and `j` see a table whose meaning is "intermediates 0 to k - 1". The early `continue` on `dist[i][k]` skips a whole row of comparisons when server `i` cannot reach `k`. The method runs in O(n^3) time and uses O(n^2) memory for the table. Reading the table afterward costs O(1) for each query.

<!-- stage: applicability -->
### Recognizing All Pairs Problems

#### Reading The Cue

Use this method when the statement asks for the lowest cost between many or all pairs of vertices on a graph with at most a few hundred vertices. Typical cases are a latency table between servers, a route matrix between warehouses, and a count of how many places lie within a cost limit of each place. When the graph is large and sparse, running Dijkstra's method from every source costs less than O(n^3). Floyd Warshall also works with negative edges when no negative cycle exists. If a negative cycle exists, some diagonal entry `dist[i][i]` ends below zero, which reveals it. This lesson's inputs stay nonnegative.

#### Checking The Invariant

An invariant is a condition that stays true at the start and end of each round of a loop. The invariant here is that after the round for `k`, each entry `dist[i][j]` equals the lowest cost of a route that uses only intermediates 0 to `k`. Two conditions in the code protect it. The loop over `k` is the outermost loop, and no sum starts from the sentinel. Test a graph with no edges, a pair with two equal routes, a self loop, and weights near two billion, where a sum leaves the range of `int`.

#### Avoiding The False Friend

A false friend is a familiar approach that looks right and fails. The false friend here is reordering the loops. The three loops look symmetric, and putting `k` innermost compiles and runs, yet the second trace shows wrong entries. With `k` innermost, an entry for `i` and `j` reads values in other rows that are not finished. Another false friend is Dijkstra's method run once and read as a table, because one run gives distances from a single source only. Bellman Ford is not a false friend here, because it answers a different question with one source.

<!-- stage: exercises -->
### Exercises

#### [Build] Allow One Intermediate (Author exercise)
<!-- id: ga-fw-one-intermediate -->

**Prerequisites.** The round for one server `k` in this lesson.

**Problem.** An `n` by `n` table `dist` of type `long[][]` holds the cost of the best known route between each pair. The value `Long.MAX_VALUE` means that no route is known. Given a server `k`, return a new table whose entry (i, j) is the smaller of `dist[i][j]` and `dist[i][k] + dist[k][j]`. Form the sum only when both parts are finite. The input table stays unchanged.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 200`, and `0 <= k < n`.
- **Entries** are `Long.MAX_VALUE` or in `0..10^12`.
- **Diagonal** entries are 0.
- **Mutation** of the input is not allowed.

**Example 1.** Input `dist = [[0,5,9223372036854775807],[9223372036854775807,0,2],[1,9223372036854775807,0]]`, `k = 1`, output `[[0,5,7],[9223372036854775807,0,2],[1,9223372036854775807,0]]`.

**Example 2.** Input the same `dist` with `k = 0`, output `[[0,5,9223372036854775807],[9223372036854775807,0,2],[1,6,0]]`.

**Hint.** What does the sum become when one of the two parts is `Long.MAX_VALUE`?

**Changed decision.** The method tries one intermediate only and reads from the old table, so no entry sees an update from the same call.

#### [Vary] All-Pairs Table (Author exercise)
<!-- id: ga-fw-prefix-table -->

**Prerequisites.** The exercise above.

**Problem.** A directed graph has servers `0` to `n - 1`, and `edges` lists triples `[a, b, w]` for a link from `a` to `b` with weight `w`. Given a limit `m`, return an `n` by `n` table of type `long[][]`. Entry (i, j) is the lowest cost of a route from `i` to `j` whose intermediate servers all have an index below `m`, or `-1` when no such route exists. The diagonal is 0.

**Constraints.** The limits are:
- **Servers** satisfy `1 <= n <= 60`.
- **Edges** satisfy `0 <= edges.length <= 400`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 1000`.
- **Limit** satisfies `0 <= m <= n`.

**Example 1.** Input `n = 4`, `edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,9]]`, `m = 2`, output `[[0,1,2,9],[-1,0,1,-1],[-1,-1,0,1],[-1,-1,-1,0]]`.

**Example 2.** Input the same graph with `m = 4`, output `[[0,1,2,3],[-1,0,1,2],[-1,-1,0,1],[-1,-1,-1,0]]`.

**Hint.** Which loop of the method decides which servers may act as intermediates?

**Changed decision.** The method stops after `m` rounds, so the table shows a partial meaning and not the final distances.

#### [Boundary] Infinity Arithmetic (Author exercise)
<!-- id: ga-fw-infinity-arith -->

**Prerequisites.** The two exercises above.

**Problem.** Take `n` servers numbered from 0, with directed links `[a, b, w]` in `edges` that run from `a` to `b` at weight `w`. Consider every ordered pair of different servers. Return a `long[]` that holds two values. Position 0 holds the largest finite distance over these pairs, or 0 when no pair has a route. Position 1 holds the count of these pairs with no route.

**Constraints.** The limits are:
- **Servers** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= edges.length <= 2000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 2000000000`.
- **Result** uses `long`, since a distance can exceed the range of `int`.

**Example 1.** Input `n = 3`, `edges = [[0,1,2000000000],[1,2,2000000000]]`, output `[4000000000,3]`.

**Example 2.** Input `n = 2`, `edges = []`, output `[0,2]`.

**Hint.** Which value marks a missing route, and what happens when the method adds one to it?

**Changed decision.** The method guards every sum against the sentinel and counts missing routes separately, so no sentinel value leaks into the largest distance.

#### [Recognize] Find the City With the Smallest Number of Neighbors at a Threshold Distance (LeetCode 1334)
<!-- id: ga-fw-city-threshold -->

**Prerequisites.** All three exercises above.

**Problem.** There are `n` cities numbered `0` to `n - 1`, and `edges` lists undirected roads as triples `[a, b, w]` with length `w`. Given `distanceThreshold`, the neighbors of a city are the other cities whose shortest distance from it is at most the threshold. Return an `int[]` that holds two values. Position 0 holds the city with the fewest neighbors, and position 1 holds its neighbor count. When several cities tie, return the one with the smallest index.

**Constraints.** The limits are:
- **Cities** satisfy `2 <= n <= 100`.
- **Roads** satisfy `1 <= edges.length <= n * (n - 1) / 2`, and each pair of cities appears at most once.
- **Length** satisfies `1 <= w <= 10000`.
- **Threshold** satisfies `1 <= distanceThreshold <= 10000`.

**Example 1.** Input `n = 4`, `edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]`, `distanceThreshold = 4`, output `[0,2]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,1],[2,3,1]]`, `distanceThreshold = 1`, output `[0,1]`.

**Hint.** Does an undirected road fill one table entry or two?

**Changed decision.** The method returns the neighbor count with the city, and a tie goes to the smallest index. The usual statement returns only the city with the greatest index on a tie.
