<!-- lesson-kind: standard -->
<!-- lesson-id: count-by-layers -->
## Count By Whole Layers

<!-- stage: context -->
### Timing An Update Across A Cluster

A deployment tool pushes a configuration update from one server to a cluster. Every server that holds the update sends it to all of its direct neighbors, and one transfer takes one time unit. Servers that received the update in the same time unit send in parallel. The dashboard must print how many time units pass until the last reachable server holds the update. A wrong figure either hides a slow rollout or raises an alert for a healthy one.

Model the servers as vertices and the links as undirected edges. The task is to return the number of time units that the update needs to reach every vertex it can reach, and 0 when the source has no neighbor.

This lesson asks how a breadth-first search should count time, when many vertices act in the same time unit.

<!-- stage: naive -->
### Adding One Time Unit Per Vertex

The search from the previous chapter already visits vertices in order of distance, so the first attempt adds one to a counter each time it removes a vertex from the queue.

```java
static int spreadTime(List<List<Integer>> adj, int source) {
    boolean[] visited = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    visited[source] = true;
    queue.add(source);
    int time = -1;
    while (!queue.isEmpty()) {
        int current = queue.poll();
        time++;
        for (int next : adj.get(current)) {
            if (visited[next]) continue;
            visited[next] = true;
            queue.add(next);
        }
    }
    return time;
}
```

Take a source 0 that is linked to the vertices 1, 2 and 3, with no other edge.

```predict
What does spreadTime return for this star graph, and what is the correct number of time units?

It returns 3, because the queue holds four vertices and the counter starts at -1 and rises once for each of them. The correct answer is 1, because the three neighbors of vertex 0 all receive the update in the same time unit. The counter measures how many vertices the search removed, and not how many time units passed.
```

<!-- stage: bottleneck -->
### Counting Vertices Instead Of Time

The method visits every vertex once and reads every edge once, so its running time is O(V + E) and that part is fine. The defect is in what the counter measures. Each removal adds one, so the result always equals the number of reached vertices minus one, and it ignores the shape of the graph. A star with a thousand leaves would report 1000, and a path of three vertices with the source in the middle would report 2 although all vertices hold the update after one time unit.

One repair stores a `distance` value for every vertex, as in the earlier distance method, and returns the largest value. That is correct, and it costs O(V) extra memory and a second pass over the array. Many tasks need less. They ask only for the number of time units, or for one count per time unit, and they never ask for the distance of a given vertex.

A better method keeps the O(V + E) time and uses no per-vertex distance. It must know, while it runs, which queued vertices act in the same time unit. The next stage names the quantity that tells it.

<!-- stage: insight -->
### Processing The Queue Layer By Layer

The queue of a breadth-first search always holds vertices of at most two distances. That fact lets the search count time without storing any distance.

<!-- names: layer, frontier, snapshot -->

#### What A Layer Is

A **layer** is the set of all vertices at the same distance from the source. Layer 0 is the source alone, layer 1 holds its neighbors, and layer 2 holds the vertices whose shortest path from the source has two edges. All vertices of one layer receive the update in the same time unit.

#### Reading The Frontier Size

The **frontier** is the content of the queue at the moment a pass begins. Because vertices leave the queue in nondecreasing distance, that content is exactly one layer and nothing else. The search reads `size = queue.size()` before it removes anything. This value is the **snapshot** of the frontier, and it stays fixed while the queue grows. The first lesson called the unexpanded part of a layer the frontier, and the two meanings agree, because at the start of a pass the unexpanded part is the whole layer.

#### Expanding Exactly One Layer

The inner loop runs `size` times. Each run removes one vertex and appends its unvisited neighbors, and those neighbors belong to the next layer, because they are one edge farther from the source. After `size` removals the old layer is gone and the queue holds precisely the next layer. If at least one vertex was appended, the time counter rises by one, and it rises once for the whole layer, whatever the layer's size.

#### Why The Count Is Correct

The invariant is that at the start of each pass the queue holds every vertex of one layer, and no vertex of any other layer. The first pass holds the source alone. Each pass turns layer `k` into layer `k + 1`, so the number of passes that append something equals the largest distance. A pass that appends nothing marks the end and adds no time.

<!-- stage: variables -->
### What The Search Keeps

The search keeps one list, one array, one queue, two integers and one flag. The name `adj` is the adjacency list, and `adj.get(v)` holds the neighbors of `v`. Each of the other names has a fixed starting value.

- **visited** is a boolean array; `true` means the vertex is already in the queue or was removed.
- **queue** is an `ArrayDeque` that holds the current layer first and the next layer behind it.
- **size** is an int read once per pass; it equals the number of vertices in the current layer.
- **layers** is an int that starts at 0 and counts the passes that discover a new vertex.
- **found** is a boolean that starts false in every pass and turns true when the pass appends a vertex.

<!-- stage: trace -->
### Counting Layers On Two Graphs

#### A Graph With Two Equal Routes

The first graph has the edges 0 to 1, 0 to 2, 1 to 3, 2 to 3, 3 to 4 and 5 to 6. The cells are the vertex ids, and the pointer `cur` is the vertex just removed from the queue. The variable `size` is the snapshot of the current pass, and `layers` is the counter after that removal, which changes only at the last removal of a pass. The first pass removes vertex 0 alone and appends 1 and 2. The second pass has size 2, and it removes 1 and 2 before the counter changes again. Vertices 5 and 6 never enter the queue, so they do not add time.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"size":1,"layers":1,"queue":"1-2"},"note":"The search takes vertex 0 from a pass of size 1 and appends 1 and 2. The pass appended vertices, so layers becomes 1."},{"at":{"cur":1},"vars":{"size":2,"layers":1,"queue":"2-3"},"note":"The search takes vertex 1 from a pass of size 2 and appends 3."},{"at":{"cur":2},"vars":{"size":2,"layers":2,"queue":"3"},"note":"The search takes vertex 2 from a pass of size 2 and finds no unvisited neighbor. The pass appended vertices, so layers becomes 2."},{"at":{"cur":3},"vars":{"size":1,"layers":3,"queue":"4"},"note":"The search takes vertex 3 from a pass of size 1 and appends 4. The pass appended vertices, so layers becomes 3."},{"at":{"cur":4},"vars":{"size":1,"layers":3,"queue":"empty"},"note":"The search takes vertex 4 from a pass of size 1 and finds no unvisited neighbor. The pass appended nothing, so layers keeps its value."}]}
```

#### A Graph With An Edge Inside A Layer

The second graph is a triangle on the vertices 0, 1 and 2, with the edge 2 to 3. The edge 1 to 2 joins two vertices of the same layer. The search removes 1 and finds 2 already visited, so the edge adds nothing. The last pass removes vertex 3, finds nothing to append and leaves the counter at 2.

```trace
{"cells":[0,1,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"size":1,"layers":1,"queue":"1-2"},"note":"The search takes vertex 0 from a pass of size 1 and appends 1 and 2. The pass appended vertices, so layers becomes 1."},{"at":{"cur":1},"vars":{"size":2,"layers":1,"queue":"2"},"note":"The search takes vertex 1 from a pass of size 2 and finds no unvisited neighbor."},{"at":{"cur":2},"vars":{"size":2,"layers":2,"queue":"3"},"note":"The search takes vertex 2 from a pass of size 2 and appends 3. The pass appended vertices, so layers becomes 2."},{"at":{"cur":3},"vars":{"size":1,"layers":2,"queue":"empty"},"note":"The search takes vertex 3 from a pass of size 1 and finds no unvisited neighbor. The pass appended nothing, so layers keeps its value."}]}
```

<!-- stage: code -->
### Counting Layers With A Queue Snapshot

The method returns the number of passes that discover at least one new vertex.

```java
static int layerCount(List<List<Integer>> adj, int source) {
    boolean[] visited = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    visited[source] = true;
    queue.add(source);
    int layers = 0;
    while (!queue.isEmpty()) {
        int size = queue.size();
        boolean found = false;
        for (int i = 0; i < size; i++) {
            int current = queue.poll();
            for (int next : adj.get(current)) {
                if (visited[next]) continue;
                visited[next] = true;
                queue.add(next);
                found = true;
            }
        }
        if (found) layers++;
    }
    return layers;
}
```

The value `size` must be copied into a local variable before the inner loop. The expression `queue.size()` in the loop header would change after every append and mix two layers. The flag `found` keeps the last pass, which appends nothing, from adding one extra time unit. The time is O(V + E), and the space is O(V) for `visited` and the queue.

<!-- stage: applicability -->
### Recognizing Counts Per Layer

#### Reading The Cue

Use the snapshot when the answer counts a quantity that advances once for the whole frontier. Statements ask for minutes until everything spreads, rounds of an operation, or the number of moves, where all states of one distance act together. Tasks that need the sizes of the layers, or the vertices in each layer, use the same loop and record data inside it.

#### Checking The Invariant

The invariant is that the queue holds exactly one layer at the start of each pass. It holds only if every vertex is marked visited when it enters the queue and the size is read before the inner loop starts. If a vertex could enter the queue twice, a pass could contain vertices of two distances, and the count would drift.

#### Avoiding The False Friend

The false friend is a counter that rises once per removed vertex. It looks like the time that passed, and it equals the number of reached vertices minus one. The opposite error also occurs. A counter that rises after every pass, including the final pass that finds nothing, overcounts by one. Ask each time what the counter should equal when the graph is one vertex alone.

<!-- stage: exercises -->
### Exercises

#### [Build] Label BFS Layers (Author exercise)
<!-- id: bv2-label-layers -->

**Prerequisites.** The layer snapshot of this lesson.

**Problem.** An undirected graph has vertices `0` to `n - 1`, and each edge `[a, b]` joins `a` and `b` in both directions. Given a `source` vertex, return an `int[][]` named `layers`. The row `layers[k]` lists every vertex whose minimum number of edges from `source` equals `k`, in ascending order. The result has one row for each `k` from 0 up to the largest finite distance. Vertices that no path reaches appear in no row.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Source** is a vertex in `0..n-1`.
- **Result** has `layers[0] = [source]`, and every row is nonempty.

**Example 1.** Input `n = 7`, `edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[5,6]]`, `source = 0`, output `[[0],[1,2],[3],[4]]`.

**Example 2.** Input `n = 4`, `edges = [[1,2],[2,3]]`, `source = 0`, output `[[0]]`.

**Hint.** When must the size of the queue be read so that it counts one layer exactly?

**Changed decision.** The method reads the queue size before each pass and stores every vertex of that pass in one row sorted in ascending order.

#### [Vary] Stop At First Target Layer (Author exercise)
<!-- id: bv2-first-target-layer -->

**Prerequisites.** The first exercise above.

**Problem.** An undirected graph on the vertices `0` to `n - 1` is given by `n` and `edges`. For a `source` and a `target`, let `d` be the minimum number of edges on a path from `source` to `target`. Return an `int[]` of length 2 that holds `d` and the number of vertices whose distance from `source` equals `d`. Return `[-1, 0]` when no path exists.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Source and target** are vertices in `0..n-1`, and they may be equal.
- **Result** is `[d, count]` or `[-1, 0]`.

**Example 1.** Input `n = 8`, `edges = [[0,1],[0,2],[1,3],[2,3],[2,4],[3,5],[4,5],[5,6],[6,7]]`, `source = 0`, `target = 4`, output `[2, 2]`.

**Example 2.** Input `n = 6`, `edges = [[0,1],[1,2],[3,4]]`, `source = 0`, `target = 4`, output `[-1, 0]`.

**Hint.** At which moment does the search know the whole layer that contains the target, and which later layers can it ignore?

**Changed decision.** The method stops after the pass that discovers the target and reports the size of that layer, and it never starts the next pass.

#### [Boundary] Initially Complete State (Author exercise)
<!-- id: bv2-initially-complete -->

**Prerequisites.** The two exercises above.

**Problem.** Consider `n` servers numbered `0` to `n - 1` that are joined by the undirected links in `edges`. An update starts at `source`, and in each time unit every vertex that holds the update passes it to all of its neighbors. Return the number of time units after which every vertex connected to `source` holds the update. Return 0 when the state is complete before any time unit passes.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with no duplicate edge and no self loop.
- **Source** is a vertex in `0..n-1`.
- **Result** is one `int`, and vertices outside the component of `source` are ignored.

**Example 1.** Input `n = 1`, `edges = []`, `source = 0`, output `0`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[1,2],[0,2]]`, `source = 0`, output `1`.

**Hint.** What must the counter equal when the queue holds only the source and the source has no neighbor?

**Changed decision.** The method counts a pass only when it appends a new vertex, so the final empty pass and an isolated source add no time.

#### [Recognize] Rotting Oranges With Minute Counts (LeetCode 994)
<!-- id: bv2-rotting-counts -->

**Prerequisites.** All three exercises above.

**Problem.** A grid `grid` has `m` rows and `n` columns. A cell holds 0 for empty, 1 for a fresh orange or 2 for a rotten orange. In each minute, every fresh orange that shares an edge with a rotten orange at the start of that minute becomes rotten. This contract differs from the usual one, which returns a single minute count. Return an `int[]` named `counts`, where `counts[t]` is the number of fresh oranges that become rotten during minute `t + 1`. A fresh orange that no rotten orange can ever reach stays fresh and appears in no entry. Return an empty array when no fresh orange ever becomes rotten.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 10`.
- **Cells** are 0, 1 or 2.
- **Neighbors** are the four cells that share an edge.
- **Result** has no zero entry, and its sum is at most the number of fresh oranges.

**Example 1.** Input `grid = [[2,1,1,0],[1,1,0,1],[0,1,1,1]]`, output `[2,2,1,1,1,1]`.

**Example 2.** Input `grid = [[2,1,0],[0,0,1],[1,0,2]]`, output `[2]`.

**Hint.** Which value describes the whole minute, and which condition tells that a pass produced no rotten orange at all?

**Changed decision.** The method records the number of newly rotten oranges per pass and appends it only when it is positive, so unreachable oranges and the final empty pass add no entry.
