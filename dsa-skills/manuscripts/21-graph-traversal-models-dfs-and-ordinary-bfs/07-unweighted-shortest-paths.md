<!-- lesson-kind: standard -->
<!-- lesson-id: unweighted-shortest-paths -->
## Unweighted Shortest Paths

<!-- stage: context -->
### Counting Hops Between Two Members

A professional network shows each member how many introductions separate them from another member. If Ana knows Ben and Ben knows Cleo, then Cleo is two introductions from Ana. A user searches for a person and the page must print the smallest such number. A wrong number is visible at once, because the user can count the introductions on the profile.

Model the members as vertices and the acquaintances as undirected edges, so an edge joins two vertices in both directions. Each edge counts as one introduction, which makes all edges cost the same. The **length** of a path is its number of edges. The task is to find the minimum length over all paths between a given source and a given target, or to report that no path exists.

This lesson asks which traversal finds that minimum, and why it is not the one used in the lesson Path Enumeration.

<!-- stage: naive -->
### Reporting The First Path Found

The depth-first search is the traversal we know best, and it finds a path when one exists. The first attempt returns the length of the first path it finds.

```java
static int firstPathLength(List<List<Integer>> adj, int cur, int target, boolean[] visited) {
    if (cur == target) return 0;
    visited[cur] = true;
    for (int next : adj.get(cur)) {
        if (visited[next]) continue;
        int rest = firstPathLength(adj, next, target, visited);
        if (rest >= 0) return rest + 1;
    }
    return -1;
}
```

Take four vertices with the edges 0 to 1, 1 to 2, 2 to 3 and 0 to 3, all undirected, and ask for the length from vertex 0 to vertex 3.

```predict
What length does firstPathLength return for source 0 and target 3, and what is the correct minimum?

It returns 3, because the search follows 0, 1, 2, 3 before it looks at the edge from 0 to 3. The correct minimum is 1, from the direct edge. The search stops at the first path it finds, and the first path is not the shortest.
```

<!-- stage: bottleneck -->
### Stopping Too Early Or Too Late

The search is not wrong about reachability. It is wrong about order, because the neighbor order decides which path it finds first. Reordering the neighbors helps on this graph and breaks another one, so no fixed order repairs the method.

The safe alternative is to compare every path. The method lists all simple paths, as the lesson Path Enumeration did, and takes the smallest length. The cost is the number of simple paths, which grows exponentially. A graph with `k` layers of two vertices each, where each vertex touches both vertices of the next layer, has `2^k` paths. The time is therefore O(P * n) for `P` paths, and `P` is exponential in `n`.

The graph only has `V` vertices and `E` edges, so a better method should read each edge a constant number of times and take O(V + E) time. It needs one new property: the order in which the search discovers vertices must follow the length of the path, and not the neighbor order. The next stage names that property.

<!-- stage: insight -->
### Discovering Vertices In Order Of Length

Breadth-first search provides the missing order. It expands the source first, then all neighbors of the source, then their neighbors, and so on.

#### What Distance Means

The **distance** of a vertex is the length of the shortest path from the source to that vertex. The source has distance 0. A **level** is the set of all vertices with the same distance. Level 0 is the source alone, level 1 holds the neighbors of the source, and level 2 holds the vertices that are neighbors of level 1 and not in an earlier level.

<!-- names: distance, level, predecessor -->

#### Why First Discovery Is Shortest

The search keeps a queue of discovered vertices that wait for expansion. It removes the front vertex `current`. Every unvisited neighbor `next` of that vertex is marked visited, receives `distance[next] = distance[current] + 1` and joins the back of the queue. At any moment the queue contains the rest of one level, then a part of the following level, and nothing else. Therefore removals never return to a smaller distance. A vertex is first discovered by an expanded vertex of the smallest possible level, so that first assigned value is its true distance. The invariant is that BFS dequeues vertices in nondecreasing distance.

#### Remembering Where A Vertex Came From

The discovering vertex of `next` is its **predecessor**. Storing `predecessor[next] = current` at the same moment records one shortest path. To restore it, follow the predecessors from the target back to the source and reverse the sequence. A vertex is never discovered twice, so each vertex has exactly one predecessor and the chain is a simple path.

<!-- stage: variables -->
### What The Search Keeps

The search keeps four arrays and one queue, and each has a fixed starting value.

- **adj** is the adjacency list; `adj.get(v)` holds the neighbors of `v`.
- **visited** is a boolean array; `true` means the vertex was already discovered.
- **distance** is an int array; the source gets 0 and a vertex that is never reached keeps -1.
- **predecessor** is an int array; the source and unreached vertices keep -1.
- **queue** is an `ArrayDeque` that holds discovered vertices in the order of discovery.

<!-- stage: trace -->
### Following Distances On Two Graphs

#### A Graph With Two Equal Routes

The first graph has the edges 0 to 1, 0 to 2, 1 to 3, 2 to 3, 3 to 4 and 4 to 5, with source 0. Here the cells are the vertex ids, and the pointer `cur` shows the vertex that was just taken from the queue. The search takes 0 and discovers 1 and 2 at distance 1. It then takes 1 and discovers 3 at distance 2. When it takes 2, the vertex 3 is already visited, so the second route to 3 changes nothing. The distances grow by one at each level, up to 4 for vertex 5.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distance":"0,1,1,-1,-1,-1","queue":"1-2"},"note":"The search takes vertex 0 from the queue and discovers 1, 2, each at distance 1."},{"at":{"cur":1},"vars":{"distance":"0,1,1,2,-1,-1","queue":"2-3"},"note":"The search takes vertex 1 from the queue and discovers 3, each at distance 2."},{"at":{"cur":2},"vars":{"distance":"0,1,1,2,-1,-1","queue":"3"},"note":"After taking vertex 2, the search finds nothing new to enqueue."},{"at":{"cur":3},"vars":{"distance":"0,1,1,2,3,-1","queue":"4"},"note":"The search takes vertex 3 from the queue and discovers 4, each at distance 3."},{"at":{"cur":4},"vars":{"distance":"0,1,1,2,3,4","queue":"5"},"note":"The search takes vertex 4 from the queue and discovers 5, each at distance 4."},{"at":{"cur":5},"vars":{"distance":"0,1,1,2,3,4","queue":"empty"},"note":"After taking vertex 5, the search finds nothing new to enqueue."}]}
```

#### A Graph With Unreachable Vertices

The second graph has the edges 0 to 1, 1 to 2, 0 to 2, 2 to 3 and 4 to 5. Vertices 4 and 5 form a separate piece. The queue becomes empty after vertex 3, so the loop ends, and vertices 4 and 5 keep distance -1. That value is the answer for an unreachable target.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"distance":"0,1,1,-1,-1,-1","queue":"1-2"},"note":"The search takes vertex 0 from the queue and discovers 1, 2, each at distance 1."},{"at":{"cur":1},"vars":{"distance":"0,1,1,-1,-1,-1","queue":"2"},"note":"The queue gives vertex 1, and it has no undiscovered neighbor to add."},{"at":{"cur":2},"vars":{"distance":"0,1,1,2,-1,-1","queue":"3"},"note":"The search takes vertex 2 from the queue and discovers 3, each at distance 2."},{"at":{"cur":3},"vars":{"distance":"0,1,1,2,-1,-1","queue":"empty"},"note":"Vertex 3 comes off the queue, but all its neighbors are visited already, so nothing changes."}]}
```

<!-- stage: code -->
### Computing Distances With A Queue

The method returns the distance array for one source.

```java
static int[] distances(List<List<Integer>> adj, int source) {
    int n = adj.size();
    boolean[] visited = new boolean[n];
    int[] distance = new int[n];
    Arrays.fill(distance, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    visited[source] = true;
    distance[source] = 0;
    queue.add(source);
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

Two Java details matter. A new `int[]` holds zeros, so without `Arrays.fill` an unreachable vertex would report distance 0, which is the distance of the source. The method also marks a vertex visited when it enters the queue and not when it leaves, so each vertex enters the queue once. The time is O(V + E), because every vertex is dequeued once and every adjacency entry is read once. The space is O(V) for the arrays and the queue.

<!-- stage: applicability -->
### Recognizing Minimum Edge Tasks

#### Reading The Cue

Use breadth-first search when every move costs the same and the question asks for the fewest moves, hops or edges. Statements say "minimum number of steps", "fewest transfers" or "shortest path" without any weights. A grid where each step to a free cell costs one move is the same task, because the cells are the vertices.

#### Checking The Invariant

The invariant of the lesson is that BFS dequeues vertices in nondecreasing distance, so the first discovery of a vertex is shortest. The invariant breaks if a vertex is marked visited late, or if edges have different costs. A queue then no longer holds a single level followed by the next one.

#### Avoiding The False Friend

Depth-first search is the false friend of this task. It may find a path first, but it does not find the shortest one, as the naive stage showed. The reverse choice also errs. Breadth-first search with a queue is the wrong tool for listing every path, because the visited rule hides all routes except one. Weighted edges need a different method, which a later chapter teaches.

<!-- stage: exercises -->
### Exercises

#### [Build] Distance From One Source (Author exercise)
<!-- id: gt-distance-one-source -->

**Prerequisites.** The queue search of this lesson.

**Problem.** An undirected graph has vertices `0` to `n - 1`, and each edge `[a, b]` joins `a` and `b` in both directions. Given a source vertex, return an array `d` of length `n`, where `d[v]` is the minimum number of edges on a path from the source to `v`. When no path exists, `d[v]` is `-1`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Edge list** has no duplicate edge and no self loop.
- **Source** is a vertex in `0..n-1`.
- **Result** is an `int` array of length `n`.

**Example 1.** Input `n = 6`, `edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]`, `source = 0`, output `[0,1,1,2,3,-1]`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[0,2],[2,3]]`, `source = 0`, output `[0,1,1,2,-1]`.

**Hint.** At what moment does a vertex receive its final distance?

**Changed decision.** The method assigns `distance[next] = distance[current] + 1` when it first discovers a vertex.

#### [Vary] Restore One Shortest Path (Author exercise)
<!-- id: gt-restore-shortest-path -->

**Prerequisites.** The first exercise above.

**Problem.** Consider an undirected graph on the vertices `0` to `n - 1`. For a pair `source` and `target`, return one shortest path as the list of its vertices from `source` to `target`. Scan the neighbors of each vertex in the order of `edges`, and let the first vertex that discovers a vertex be its predecessor. When `target` cannot be reached, return an empty list.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Source and target** are vertices in `0..n-1`; they may be equal.
- **Result** lists the vertices in order, starting with `source`.

**Example 1.** Input `n = 6`, `edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[4,5]]`, `source = 0`, `target = 5`, output `[0,1,3,4,5]`.

**Example 2.** Input `n = 5`, `edges = [[0,3],[0,1],[1,2],[2,3],[3,4]]`, `source = 0`, `target = 4`, output `[0,3,4]`.

**Hint.** What single value must the search store per vertex, besides its distance?

**Changed decision.** The method stores a predecessor at each first discovery, so it can walk back from the target.

#### [Boundary] Source Equals Target And Unreachable Target (Author exercise)
<!-- id: gt-source-target-boundary -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected graph is given by `n` and `edges`, with vertices numbered from `0`. For the pair `source` and `target`, return the minimum number of edges on a path between them. Return `0` when `source` equals `target`. Return `-1` when no path exists.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Source and target** are vertices in `0..n-1`.
- **Result** is one `int`.

**Example 1.** Input `n = 3`, `edges = [[0,1]]`, `source = 2`, `target = 2`, output `0`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[3,4]]`, `source = 0`, `target = 4`, output `-1`.

**Hint.** Which answer is correct before the queue is even created?

**Changed decision.** The method returns the stated value before the search when the source is the target, and it returns the failure value after the queue empties.

#### [Recognize] Shortest Path in Binary Matrix (LeetCode 1091)
<!-- id: gt-shortest-path-binary-matrix -->

**Prerequisites.** All three exercises above.

**Problem.** A square grid `grid` of size `n` by `n` holds 0 for a free cell and 1 for a blocked cell. A clear path is a sequence of free cells that starts at `(0,0)` and ends at `(n-1,n-1)`, in which consecutive cells differ by at most 1 in each coordinate, so the eight neighbors of a cell are allowed. Return the number of cells on the shortest clear path, or `-1` when no clear path exists.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 100`.
- **Cells** are 0 or 1.
- **Endpoints** may be blocked, and then the answer is `-1`.
- **Length** counts cells, so a single free cell gives 1.

**Example 1.** Input `grid = [[0,1,0],[1,0,1],[0,0,0]]`, output `3`.

**Example 2.** Input `grid = [[0,0,0],[1,1,0],[1,1,0]]`, output `4`.

**Hint.** What are the vertices and the neighbors of one vertex in this graph?

**Changed decision.** The graph is implicit with eight neighbors per cell, and the distance counts cells and not edges.
