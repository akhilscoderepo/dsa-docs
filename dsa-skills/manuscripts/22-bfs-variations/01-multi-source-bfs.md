<!-- lesson-kind: standard -->
<!-- lesson-id: multi-source-start -->
## Start From Many Sources

<!-- stage: context -->
### Distance To The Closest Charging Station

A map application draws a grid of city blocks. Some blocks hold a charging station, and every other block must show how many blocks a driver walks to reach the closest station. A slow answer is visible at once, because the application recomputes the numbers each time the user adds or removes a station. A wrong number is visible too, because the user counts blocks on the screen.

Model the blocks as vertices and each step between neighboring blocks as an edge of length 1. A **source** is a vertex that already holds a station. The task is to compute, for every vertex, the length of the shortest path to any source, or -1 when no source can be reached. The lesson Unweighted Shortest Paths solved the case of exactly one source.

This lesson asks how a search handles many sources at once, and whether it must run once per source.

<!-- stage: naive -->
### Running One Search Per Source

The known tool is the breadth-first search from a single source. The first attempt runs it once for every source and keeps the smallest value for each vertex.

```java
static int[] distances(List<List<Integer>> adj, int source) {
    int[] d = new int[adj.size()];
    Arrays.fill(d, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>(List.of(source));
    d[source] = 0;
    while (!queue.isEmpty()) {
        int current = queue.poll();
        for (int next : adj.get(current)) {
            if (d[next] >= 0) continue;
            d[next] = d[current] + 1;
            queue.add(next);
        }
    }
    return d;
}

static int[] nearestPerSource(List<List<Integer>> adj, int[] sources) {
    int n = adj.size();
    int[] best = new int[n];
    Arrays.fill(best, -1);
    for (int s : sources) {
        int[] d = distances(adj, s);
        for (int v = 0; v < n; v++) {
            if (d[v] >= 0 && (best[v] < 0 || d[v] < best[v])) best[v] = d[v];
        }
    }
    return best;
}
```

The method `distances` is the single-source search of the lesson Unweighted Shortest Paths, written with the distance array as the visited mark. Take the path of six vertices 0, 1, 2, 3, 4, 5, joined in a line, with sources 0 and 5.

```predict
How many vertices does this method visit in total on the six-vertex path with sources 0 and 5, and how many does the answer need?

It visits 12 vertices, because each of the two searches reaches all six vertices. The answer needs only 6 values, one per vertex. With `S` sources and `n` vertices on a connected graph the method visits about `S * n` vertices, so most of the work repeats information that an earlier search already found.
```

<!-- stage: bottleneck -->
### Repeating The Same Region Many Times

The method is correct, because the minimum over all sources is the definition of the answer. The cost is the problem. Each single-source search takes O(V + E) time, and the method runs `S` of them, so the time is O(S * (V + E)). The method also scans all `n` entries of `d` after each search.

On a grid of 1000 by 1000 blocks with 100000 stations, that is about 10^11 steps, while the grid has only 10^6 blocks. Every search spreads over regions that a closer station already covers. The search from a far station even measures distances that the method then throws away.

A better method would read each vertex and each edge a constant number of times and take O(V + E) time, no matter how many sources exist. It needs one structure that lets every source spread at the same speed, so that each vertex hears first from its closest source. The next stage names that structure.

<!-- stage: insight -->
### Putting Every Source In One Queue

Think of one extra vertex, called the **super-source**, joined by an edge to every real source. A search from the super-source reaches every source at distance 1 and every other vertex at its nearest-source distance plus 1. The search never needs the extra vertex itself. It is enough to put all the real sources into the queue at distance 0 before the first removal.

<!-- names: super-source, layer, frontier -->

#### What A Layer Is

A **layer** is the set of vertices with the same distance to their nearest source. Layer 0 holds all sources. Layer 1 holds the vertices that are one edge away from a source and not in layer 0. Each later layer follows the same rule.

#### How One Queue Serves All Sources

The queue starts with every source, each marked visited with `distance[source] = 0`. The loop is the ordinary breadth-first loop: take `current`, and give every unvisited neighbor `next` the value `distance[current] + 1`. The queue holds the **frontier**, which is the part of layer `k` still waiting for expansion, followed by the part of layer `k + 1` that is already discovered. A duplicate source must not be enqueued twice, so the start checks the visited mark first.

#### Why The First Discovery Is Final

The ordinary search relies on the invariant that vertices leave the queue in nondecreasing distance. Starting with several vertices at distance 0 keeps that invariant, because all of them sit at the front of the queue with the same value. A vertex is first discovered by the earliest expanded vertex that is adjacent to it. That vertex belongs to the smallest possible layer, so the assigned value is the minimum over all sources. A search from the super-source would produce the same order, and the work is O(V + E) once.

<!-- stage: variables -->
### What The Search Keeps

The search needs the adjacency list `adj`, one array for discovery, one for distance and one queue. The code below uses `visited`, `distance` and `queue`, and the trace uses the same names. Each name has a fixed starting value.

- **adj** is the adjacency list; `adj.get(v)` holds the neighbors of `v`.
- **visited** is a boolean array; `true` means the vertex is a source or was discovered from an earlier vertex.
- **distance** is an int array; every source holds 0 and a vertex that is never reached keeps -1.
- **queue** is an `ArrayDeque` that starts with all distinct sources and then holds the discovered vertices in order.
- **minutes** is an int that counts completed layers in the second trace and in the exercises that ask for a spread time.

<!-- stage: trace -->
### Following Many Sources Together

#### Two Sources On A Path

The first graph has the edges 0 to 1, 1 to 2, 2 to 3, 3 to 4, 4 to 5 and 2 to 6, with sources 0 and 5. The cells are the vertex ids, and the pointer `cur` shows the vertex that was just taken from the queue. The pointer `cur` is the variable `current` in the code below. The queue holds both sources at the start, so the first two removals discover vertices 1 and 4, each at distance 1. Vertex 3 is three edges from source 0 and two edges from source 5. The search assigns it 2 when vertex 4 is expanded, before vertex 2 can offer a longer route.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distance":"0,1,-1,-1,-1,0,-1","queue":"5-1"},"note":"The search takes vertex 0 from the queue and discovers 1 at distance 1."},{"at":{"cur":5},"vars":{"distance":"0,1,-1,-1,1,0,-1","queue":"1-4"},"note":"The search takes vertex 5 from the queue and discovers 4 at distance 1."},{"at":{"cur":1},"vars":{"distance":"0,1,2,-1,1,0,-1","queue":"4-2"},"note":"The search takes vertex 1 from the queue and discovers 2 at distance 2."},{"at":{"cur":4},"vars":{"distance":"0,1,2,2,1,0,-1","queue":"2-3"},"note":"The search takes vertex 4 from the queue and discovers 3 at distance 2."},{"at":{"cur":2},"vars":{"distance":"0,1,2,2,1,0,3","queue":"3-6"},"note":"The search takes vertex 2 from the queue and discovers 6 at distance 3."},{"at":{"cur":3},"vars":{"distance":"0,1,2,2,1,0,3","queue":"6"},"note":"The search takes vertex 3 from the queue and finds no undiscovered neighbor."},{"at":{"cur":6},"vars":{"distance":"0,1,2,2,1,0,3","queue":"empty"},"note":"The search takes vertex 6 from the queue and finds no undiscovered neighbor."}]}
```

#### Layers Of A Spreading Grid

The second input is a grid with three rows and three columns, written row by row. The value 2 marks the single source, 1 marks a cell that the spread must reach, and 0 marks a cell the spread cannot enter. Cell index `r * 3 + c` names the cell in row `r` and column `c`. The search takes cell 0 first and reaches cells 1 and 3. The empty cells 5 and 6 never enter the queue, and their distance stays -1. The last cell, 8, receives distance 4, and that value is the number of layers after the source layer.

```trace
{"cells":[2,1,1,1,1,0,0,1,1],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distance":"0,1,-1,1,-1,-1,-1,-1,-1","queue":"3-1"},"note":"The search takes cell 0 from the queue and discovers cells 3 and 1 at distance 1."},{"at":{"cur":3},"vars":{"distance":"0,1,-1,1,2,-1,-1,-1,-1","queue":"1-4"},"note":"The search takes cell 3 from the queue and discovers cell 4 at distance 2."},{"at":{"cur":1},"vars":{"distance":"0,1,2,1,2,-1,-1,-1,-1","queue":"4-2"},"note":"The search takes cell 1 from the queue and discovers cell 2 at distance 2."},{"at":{"cur":4},"vars":{"distance":"0,1,2,1,2,-1,-1,3,-1","queue":"2-7"},"note":"The search takes cell 4 from the queue and discovers cell 7 at distance 3."},{"at":{"cur":2},"vars":{"distance":"0,1,2,1,2,-1,-1,3,-1","queue":"7"},"note":"The search takes cell 2 from the queue and finds no fresh neighbor."},{"at":{"cur":7},"vars":{"distance":"0,1,2,1,2,-1,-1,3,4","queue":"8"},"note":"The search takes cell 7 from the queue and discovers cell 8 at distance 4."},{"at":{"cur":8},"vars":{"distance":"0,1,2,1,2,-1,-1,3,4","queue":"empty"},"note":"The search takes cell 8 from the queue and finds no fresh neighbor."}]}
```

<!-- stage: code -->
### Computing Distances From All Sources

The method returns, for each vertex, the distance to its closest source.

```java
static int[] nearestDistances(List<List<Integer>> adj, int[] sources) {
    int n = adj.size();
    boolean[] visited = new boolean[n];
    int[] distance = new int[n];
    Arrays.fill(distance, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    for (int s : sources) {
        if (visited[s]) continue;
        visited[s] = true;
        distance[s] = 0;
        queue.add(s);
    }
    while (!queue.isEmpty()) {
        int current = queue.poll();
        for (int next : adj.get(current)) {
            if (visited[next]) continue;
            visited[next] = true;
            distance[next] = distance[current] + 1;
            queue.add(next);
        }
    }
    return distance;
}
```

The only change from the single-source method is the loop that fills the queue before the main loop starts. The `Arrays.fill` call still matters, because a new `int[]` holds zeros and an unreached vertex would look like a source. An empty `sources` array leaves the queue empty, so the method returns all -1 without error. The time is O(V + E + S), because every vertex is dequeued once, every adjacency entry is read once and the start loop reads `S` sources. The space is O(V) for the arrays and the queue.

<!-- stage: applicability -->
### Recognizing Spread From Many Starts

#### Reading The Cue

Use this method when the statement names several starting points that act at the same moment and asks for the distance to the closest one, or for the time until everything is covered. Typical sentences are "distance to the nearest zero", "minutes until every cell is affected" and "closest exit for each cell". The moves must all cost the same, as in the ordinary search.

#### Checking The Invariant

The invariant is that every source enters the queue at distance 0 before any removal, so first discovery gives the minimum distance to any source. The invariant breaks if the code enqueues one source, runs the loop, and only then adds the next source. The first source would then claim vertices that a later source reaches sooner. A source must also be marked visited at enqueue time, or a duplicate source enters the queue twice.

#### Avoiding The False Friend

Running one search per source is the false friend. It returns correct values and repeats most of the work, as the naive stage showed. A second trap appears when the task asks for a time. The count of layers includes a final layer that discovers nothing, and the code must not add one minute for it. Exercise 3 below trains that check.

<!-- stage: exercises -->
### Exercises

#### [Build] Nearest Source Distances (Author exercise)
<!-- id: bv1-nearest-source-distances -->

**Prerequisites.** The single-source queue search of the lesson Unweighted Shortest Paths.

**Problem.** Consider `n` vertices numbered `0` to `n - 1` and an undirected edge list `edges`, where `[a, b]` connects `a` with `b`. A list `sources` names some vertices. Return an array `d` of length `n`, where `d[v]` is the minimum number of edges on a path from `v` to any vertex in `sources`. When no source can reach `v`, `d[v]` is `-1`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no self loop.
- **Sources** has `0 <= sources.length <= n`, and a vertex may appear more than once.
- **Result** is an `int` array of length `n`.

**Example 1.** Input `n = 7`, `edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]`, `sources = [0,5]`, output `[0,1,2,2,1,0,-1]`.

**Example 2.** Input `n = 6`, `edges = [[0,1],[1,2],[3,4]]`, `sources = [1,1]`, output `[1,0,1,-1,-1,-1]`.

**Hint.** What must be true of the queue before the first vertex leaves it?

**Changed decision.** The method enqueues every source with distance 0 before the loop starts and skips a source that is already visited.

#### [Vary] 01 Matrix (LeetCode 542)
<!-- id: bv1-zero-one-matrix -->

**Prerequisites.** The exercise above.

**Problem.** A matrix `mat` of size `m` by `n` holds only 0 and 1. Return a matrix of the same size where each entry is the distance from that cell to the nearest 0. A move goes to one of the four cells that share a side with the current cell, and each move has length 1.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 10^4` and `m * n <= 10^4`.
- **Cells** are 0 or 1.
- **Zero** appears at least once in `mat`.
- **Result** is a new matrix, and `mat` is not changed.

**Example 1.** Input `mat = [[0,0,0],[0,1,0],[1,1,1]]`, output `[[0,0,0],[0,1,0],[1,2,1]]`.

**Example 2.** Input `mat = [[1,1,1],[1,1,1],[1,1,0]]`, output `[[4,3,2],[3,2,1],[2,1,0]]`.

**Hint.** Which cells are the sources, and what value does each hold before the search starts?

**Changed decision.** The sources are the cells that hold 0, found by scanning the matrix, and the graph is implicit with four neighbors per cell.

#### [Boundary] No Source Or All Sources (Author exercise)
<!-- id: bv1-no-source-all-sources -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected graph has vertices `0` to `n - 1` and an edge list `edges`. At round 0 every vertex in `sources` is reached. In each later round, every vertex that has an edge to a reached vertex becomes reached. Return the number of rounds in which at least one new vertex becomes reached. Vertices that no source can reach are ignored.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no self loop.
- **Sources** has `0 <= sources.length <= n`, with no repeated vertex.
- **Result** is one `int`, and it is 0 when `sources` is empty or holds every vertex.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,2],[2,3]]`, `sources = []`, output `0`.

**Example 2.** Input `n = 7`, `edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]`, `sources = [0,5]`, output `2`.

**Hint.** When the queue is empty after a round, did that round add a vertex?

**Changed decision.** The method adds one to the count only when a round discovers a new vertex, so the last round of the loop does not count.

#### [Recognize] Rotting Oranges (LeetCode 994)
<!-- id: bv1-rotting-oranges -->

**Prerequisites.** All three exercises above.

**Problem.** A grid `grid` holds 0 for an empty cell, 1 for a fresh orange and 2 for a rotten orange. Each minute, every fresh orange that shares a side with a rotten orange becomes rotten. Return the minimum number of minutes until no cell holds a fresh orange. Return `-1` when some fresh orange never becomes rotten.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 10`.
- **Cells** are 0, 1 or 2.
- **Fresh oranges** may be absent, and then the answer is 0.
- **Result** is one `int`.

**Example 1.** Input `grid = [[2,1,1],[1,1,0],[0,1,1]]`, output `4`.

**Example 2.** Input `grid = [[2,1,1],[0,1,1],[1,0,1]]`, output `-1`.

**Hint.** What does one pass over the current queue contents represent?

**Changed decision.** The method processes the queue one layer at a time, and each completed layer that rots a fresh orange is one minute.
