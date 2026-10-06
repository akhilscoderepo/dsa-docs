<!-- lesson-kind: standard -->
<!-- lesson-id: bipartite-coloring -->
## Bipartite Coloring

<!-- stage: context -->
### Why Some Pairs Must Be Separated

A test suite has six test cases, numbered 0 to 5. Some pairs of tests write to the same database table, so the two tests in a pair must never run on the same machine. The suite has two machines. The pairs are `(0,1)`, `(2,3)`, `(3,4)` and `(4,2)`. A script starts at test 0, puts it on machine A, puts test 1 on machine B, and reports that the split works.

The report is wrong. Tests 2, 3 and 4 form a ring of three pairs, and no assignment of two machines separates every pair of a ring of three. The script never looked at them, because test 0 never reaches them through any pair.

The question of this lesson is how to decide, for a whole graph, whether every vertex can receive one of two colors so that each edge joins two different colors, and how to avoid the silent miss above.

<!-- stage: naive -->
### Coloring From Vertex Zero Only

The quick method colors vertex 0 with color 0 and runs a breadth-first search (BFS). Each time the search follows an edge from a colored vertex to a new vertex, it gives the new vertex the other color. When the search meets an already colored vertex, it checks that the two colors differ.

```java
static boolean twoGroupsFromZero(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    int[] color = new int[n];
    Arrays.fill(color, -1);
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    color[0] = 0;
    queue.add(0);
    while (!queue.isEmpty()) {
        int u = queue.poll();
        for (int v : adj.get(u)) {
            if (color[v] == -1) { color[v] = 1 - color[u]; queue.add(v); }
            else if (color[v] == color[u]) return false;
        }
    }
    return true;
}
```

On the test suite above, this method returns true. It is short and runs in linear time. It also answers a smaller question than the one asked, because it examines only the vertices that vertex 0 reaches.

<!-- stage: bottleneck -->
### Counting What The Search Never Sees

```predict
The method returns true on the six-test suite, yet tests 2, 3 and 4 cannot be split across two machines. Which vertices does the search visit, and what must change so that every edge gets checked?

The search visits only the component of vertex 0, which is vertices 0 and 1. The graph has other components, and each one needs its own starting vertex. Then every edge is checked once, in O(n + m) time.
```

A search from one source reaches exactly one component. In the suite, that component holds 2 of the 6 vertices and 1 of the 4 edges. The other 3 edges are never examined, so the method cannot know whether they are consistent. The cost of the method is O(n + m) for a graph with `n` vertices and `m` edges, but the work covers only part of the input.

A graph with `k` components needs `k` separate starts. Checking all pairs of vertices for consistency would cost O(n^2), which is far too slow at `n = 100000`. A restart loop costs nothing extra, because each vertex is colored once. The loop only has to decide when a start is needed and what answer one component can give.

<!-- stage: insight -->
### Giving Every Component Its Own Start

The fix has two parts. A restart loop covers every component. A single rule decides whether one component is consistent.

#### What The Words Mean

A graph is **bipartite** when its vertices can be split into two groups so that every edge joins a vertex of one group to a vertex of the other. Giving each vertex color 0 or 1 is the same split, and the two groups are the two colors. A **cycle** is a chain of edges that leads from a vertex back to itself without reusing an edge. An **odd cycle** is a cycle with an odd number of edges, such as the ring of three pairs in the suite. A **conflict** is an edge whose two endpoints hold the same color.

<!-- names: bipartite, odd cycle, conflict -->

#### One Rule Inside A Component

After the source receives color 0, every other vertex of its component is forced. Each neighbor of a colored vertex must hold the opposite color, and a neighbor of that neighbor must hold the first color again. No choice remains, so a component has exactly one valid coloring up to swapping the two colors. The search therefore never needs to guess. It colors by the forced rule and watches for a conflict.

A conflict proves the answer is no. A path is a chain of edges from one vertex to another, and colors alternate along every path the search follows. A path between two vertices of the same color therefore has an even number of edges. The conflicting edge joins those two vertices and adds one more edge, so the path and the edge form a cycle with an odd number of edges. The converse also holds. A graph without any odd cycle never produces a conflict, so the forced coloring succeeds. A graph is bipartite exactly when it has no odd cycle.

#### One Restart Rule Across Components

The components do not influence one another, because no edge joins them. The restart loop visits every vertex number in order. A vertex that is still uncolored belongs to a component that no earlier search reached, so it becomes the next source with color 0. The whole graph is bipartite when every component passes. The first conflict in any component settles the answer as no, and the loop stops.

<!-- stage: variables -->
### What The Search Keeps

The search needs one array of colors, one queue and the names of the current pair of vertices.

- **color** holds -1 for an uncolored vertex, and 0 or 1 once the vertex has a color.
- **queue** holds colored vertices whose neighbors the search has not yet examined.
- **u** is the vertex taken from the front of the queue.
- **v** is a neighbor of `u`.
- **source** is the first vertex of a component, the one the restart loop colors with 0.

<!-- stage: trace -->
### Tracing Two Graphs Step By Step

#### A Graph That Passes

The first graph has 6 vertices and the edges 0-1, 0-2, 1-3, 2-3 and 3-4. Vertex 5 has no edges. In the trace below, the pointer `cur` marks the vertex that the search takes from the queue.

The search starts at vertex 0 with color 0 and colors vertices 1 and 2 with color 1. Vertex 1 colors vertex 3 with 0, and vertex 2 finds vertex 3 already holding 0, which differs from its own color 1. Vertex 3 then colors vertex 4 with 1. The restart loop reaches vertex 5, which is uncolored, and starts a second component there. That component has no edges, so it passes at once.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"color":"0.....","queue":"[0]"},"note":"Vertex 0 is uncolored, so it becomes a new source and receives color 0."},{"at":{"cur":0},"vars":{"color":"011...","queue":"[1, 2]"},"note":"Vertex 0 leaves the queue and gives color 1 to neighbors [1, 2]."},{"at":{"cur":1},"vars":{"color":"0110..","queue":"[2, 3]"},"note":"Vertex 1 leaves the queue and gives color 0 to neighbors [3]."},{"at":{"cur":2},"vars":{"color":"0110..","queue":"[3]"},"note":"Vertex 2 leaves the queue, and every neighbor already holds the opposite color."},{"at":{"cur":3},"vars":{"color":"01101.","queue":"[4]"},"note":"Vertex 3 leaves the queue and gives color 1 to neighbors [4]."},{"at":{"cur":4},"vars":{"color":"01101.","queue":"[]"},"note":"Vertex 4 leaves the queue, and every neighbor already holds the opposite color."},{"at":{"cur":5},"vars":{"color":"011010","queue":"[5]"},"note":"Vertex 5 is uncolored, so it becomes a new source and receives color 0."},{"at":{"cur":5},"vars":{"color":"011010","queue":"[]"},"note":"Vertex 5 leaves the queue, and every neighbor already holds the opposite color."},{"at":{"cur":-1},"vars":{"color":"011010","queue":"[]"},"note":"The loop passes vertex 5 and finds every vertex colored, so the graph passes."}]}
```

#### A Graph That Fails In Its Second Component

The second graph has 6 vertices and the edges 0-1, 2-3, 3-4, 4-2 and 4-5. Vertices 2, 3 and 4 form a ring of three edges.

The first component, vertices 0 and 1, passes in three steps. The restart loop then starts at vertex 2. Vertex 2 colors vertices 3 and 4 with color 1. When the search takes vertex 3 from the queue, it finds vertex 4 with the same color 1. That is a conflict, and the method stops with the answer false. Vertex 5 is never reached, and the method does not need it.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"color":"0.....","queue":"[0]"},"note":"Vertex 0 is uncolored, so it becomes a new source and receives color 0."},{"at":{"cur":0},"vars":{"color":"01....","queue":"[1]"},"note":"Vertex 0 leaves the queue and gives color 1 to neighbors [1]."},{"at":{"cur":1},"vars":{"color":"01....","queue":"[]"},"note":"Vertex 1 leaves the queue, and every neighbor already holds the opposite color."},{"at":{"cur":2},"vars":{"color":"010...","queue":"[2]"},"note":"Vertex 2 is uncolored, so it becomes a new source and receives color 0."},{"at":{"cur":2},"vars":{"color":"01011.","queue":"[3, 4]"},"note":"Vertex 2 leaves the queue and gives color 1 to neighbors [3, 4]."},{"at":{"cur":3},"vars":{"color":"01011.","queue":"[4]"},"note":"Vertex 3 meets neighbor 4, and both hold color 1. The edge is a conflict, so the answer is false."}]}
```

<!-- stage: code -->
### Coloring Every Component In Code

#### The Restart Loop And Its Helper

The method colors each component with a helper and stops at the first failure. The helper `paint` receives the same adjacency list `adj` that the earlier lessons build.

```java
static boolean canSplitInTwo(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    int[] color = new int[n];
    Arrays.fill(color, -1);
    for (int source = 0; source < n; source++) {
        if (color[source] == -1 && !paint(adj, color, source)) return false;
    }
    return true;
}

static boolean paint(List<List<Integer>> adj, int[] color, int source) {
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    color[source] = 0;
    queue.add(source);
    while (!queue.isEmpty()) {
        int u = queue.poll();
        for (int v : adj.get(u)) {
            if (color[v] == color[u]) return false;
            if (color[v] == -1) { color[v] = 1 - color[u]; queue.add(v); }
        }
    }
    return true;
}
```

The conflict test runs before the coloring step. A neighbor that is still uncolored holds -1, which never equals a color 0 or 1, so the test cannot fire for it. A self-loop gives `v == u`, so the test fires at once.

#### Cost Of The Two Methods

- **Time** is O(n + m), because each vertex is colored once and each edge is examined twice.
- **Space** is O(n + m), because of the adjacency list, the color array and the queue.

The queue is not required. A depth-first search with the same coloring rule gives the same answer, because the rule depends on the edge and not on the visiting order.

<!-- stage: applicability -->
### Spotting Two-Group Questions

#### Recognizing The Cue

Look for a statement that asks to split items into two groups so that every listed pair lands in different groups. Words such as "two teams", "two machines", "opposite sides" and "no two linked items share a group" carry the same cue. Each item becomes a vertex and each forbidden pair becomes an edge.

#### The Invariant To Keep

The invariant is that every edge examined so far joins two different colors, and every vertex in the queue already holds its final color. A new color is assigned only through an edge from a colored vertex. The restart loop keeps the invariant true across components, because each component begins with a fresh source.

#### The False Friend

Checking only the component of vertex 0 is the false friend of this pattern. It passes every sample whose graph is connected, and it fails the first graph whose second component contains an odd cycle. The graph needs no separate test for cycle length, because the forced coloring checks the parity of every cycle for free.

#### Java Hazards

Initialize `color` with -1, not 0, because the default 0 would mean a vertex already holds the first color. Keep the equality test in front of the coloring step. An uncolored neighbor holds -1, which never equals 0 or 1, so the test cannot fire for it. A self-loop is a legal edge in some statements, and it must return false.

<!-- stage: exercises -->
### Exercises

#### [Build] Color One Component (Author exercise)
<!-- id: gt-color-one-component -->

**Prerequisites.** The forced coloring rule and the BFS method of this lesson.

**Problem.** A graph has vertices `0..n-1` and undirected edges in `edges`, where `edges[i] = [a, b]` joins vertices `a` and `b`. The component of vertex 0 is the set of vertices reachable from vertex 0 by edges. Give vertex 0 the color 0, and use BFS to give every other vertex of that component a color in `{0, 1}`. Return true if every edge with both endpoints in that component joins two different colors, and false otherwise. Vertices outside the component are ignored.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, and every edge names two vertices in `0..n-1`.
- **Self-loops** do not occur, and parallel edges may occur.
- **Return** is a boolean.
- **Mutation** of `edges` does not occur.

**Example 1.** Input `n = 3` and `edges = [[0,1],[1,2],[2,0]]`, output false.

**Example 2.** Input `n = 6` and `edges = [[0,1],[1,2],[3,4],[4,5],[5,3]]`, output true, because the ring of three edges lies outside the component of vertex 0.

**Hint.** Which vertices does the queue ever hold, and which edges does the loop therefore see?

**Changed decision.** The method starts from one source and never restarts.

#### [Vary] Process Disconnected Components (Author exercise)
<!-- id: gt-process-disconnected-components -->

**Prerequisites.** The previous exercise.

**Problem.** Take an undirected graph on vertices `0..n-1` with the edge list `edges`. Return true if the whole graph is bipartite, meaning every vertex can receive a color in `{0, 1}` so that each edge joins two different colors. Return false otherwise. A vertex with no edge is bipartite on its own.

**Constraints.** The limits are:
- **Vertices** satisfy `0 <= n <= 10^5`, and `n = 0` returns true.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Self-loops** do not occur, and parallel edges may occur.
- **Return** is a boolean.

**Example 1.** Input `n = 6` and `edges = [[0,1],[1,2],[3,4],[4,5],[5,3]]`, output false.

**Example 2.** Input `n = 5` and `edges = [[0,1],[2,3]]`, output true, and vertex 4 forms a component of its own.

**Hint.** When does the outer loop decide that a vertex needs a new source?

**Changed decision.** The method restarts at every uncolored vertex, and the verdict covers the whole graph.

#### [Boundary] Self-Loop And Odd Cycle (Author exercise)
<!-- id: gt-self-loop-and-odd-cycle -->

**Prerequisites.** The two exercises above.

**Problem.** The edge list `edges` describes an undirected graph on vertices `0..n-1`. An edge `[v, v]` is a self-loop, and it joins a vertex to itself. Return true if the graph is bipartite, and false otherwise. A self-loop makes the answer false, because one vertex cannot hold two different colors. An odd cycle makes the answer false too. Two parallel copies of the same edge do not make the answer false.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 5000`.
- **Self-loops** may occur.
- **Parallel edges** may occur.
- **Return** is a boolean.

**Example 1.** Input `n = 3` and `edges = [[0,1],[1,1]]`, output false.

**Example 2.** Input `n = 5` and `edges = [[0,1],[1,2],[2,3],[3,4],[4,0]]`, output false, and the cycle has 5 edges.

**Hint.** What does the neighbor test see when the neighbor of `u` is `u` itself?

**Changed decision.** The input may contain an edge from a vertex to itself, and the test must reject it with no special case.

#### [Recognize] Is Graph Bipartite? (LeetCode 785)
<!-- id: gt-is-graph-bipartite -->

**Prerequisites.** All three exercises above.

**Problem.** An undirected graph has `n` vertices numbered `0..n-1`. The array `graph` is its adjacency list, so `graph[u]` lists every neighbor of vertex `u`. Return true if the vertices can be split into two groups so that every edge joins a vertex of one group to a vertex of the other. Return false otherwise.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 100`, where `n = graph.length`.
- **Neighbors** in `graph[u]` are distinct values in `0..n-1`, and none equals `u`.
- **Symmetry** holds, so `v` appears in `graph[u]` exactly when `u` appears in `graph[v]`.
- **Connectivity** is not guaranteed.

**Example 1.** Input `graph = [[1,4],[0,2],[1,3],[2,4],[3,0]]`, output false.

**Example 2.** Input `graph = [[2],[3],[0],[1],[]]`, output true.

**Hint.** The input already has the form of `adj`, so which lesson step is the only one left?

**Changed decision.** The graph arrives as an adjacency list and needs no conversion, so the work is the whole-graph restart loop.
