<!-- lesson-kind: standard -->
<!-- lesson-id: components -->
## Components

<!-- stage: context -->
### Why One Search Misses Whole Groups

An operations team monitors six servers joined by network cables. When cables fail, the team asks how many separate groups of servers can still reach each other. Two servers belong to the same group when a chain of working cables joins them. A server with no working cable forms a group by itself.

A single search from one server finds only the servers in its own group. The other groups stay invisible to that search, and the team still needs a count of all of them. This lesson asks how a program counts every group, and how big each group is, when the graph can fall apart into several pieces.

<!-- stage: naive -->
### Searching Once From Vertex Zero

Take six vertices numbered 0 to 5 and the undirected edges 0-1, 1-2 and 3-4. Vertex 5 has no edge. The quick idea is to search once from vertex 0. The search reaches the vertices 0, 1 and 2. The program then counts one group for that search and one more group for each vertex that the search did not reach.

```java
static int groupsFromVertexZero(List<List<Integer>> adj) {
    boolean[] visited = new boolean[adj.size()];
    markReachable(adj, visited, 0);          // one search from vertex 0
    int unreached = 0;
    for (boolean seen : visited) {
        if (!seen) unreached++;              // every vertex outside the search counts alone
    }
    return 1 + unreached;
}

static void markReachable(List<List<Integer>> adj, boolean[] visited, int v) {
    visited[v] = true;
    for (int w : adj.get(v)) {
        if (!visited[w]) markReachable(adj, visited, w);
    }
}
```

The method visits each vertex and edge at most once, so it is fast. It returns 4 for this graph. The correct answer is 3, because the vertices 3 and 4 share an edge and belong to one group.

<!-- stage: bottleneck -->
### Why Counting Unreached Vertices Fails

```predict
The method returns 4 and the correct count is 3. Which step of the method causes the error, and does a faster search fix it?

The step that counts every unreached vertex as its own group causes the error. Vertices 3 and 4 are joined by an edge, so they are one group, but the method never follows that edge. A faster search does not help, because the search is not the problem. The method needs another search that starts inside the unreached part.
```

The method spends O(V + E) time on one search and then ignores the edges among the unreached vertices. Those edges decide the count. Treating each unreached vertex alone overcounts whenever two unreached vertices are joined. A graph with two groups of 500 vertices each, one of them containing vertex 0, returns 1 + 500 = 501 instead of 2.

The repair is simple to state. The unreached vertices form a graph of their own, and a second search from any one of them reaches its whole group. The program must keep starting searches until no vertex is left. The cost stays O(V + E), because the marks of earlier searches stop later searches from reading the same vertices again.

<!-- stage: insight -->
### Starting A Search From Every Unmarked Vertex

#### Defining A Component

A **component** of an undirected graph is a maximal set of vertices in which every pair is joined by a path, which is a chain of edges. Maximal means that the set cannot grow, because no edge leaves it. Every vertex belongs to exactly one component. A graph with more than one component is **disconnected**. A vertex with no edge is an **isolated vertex**, and it forms a component of size 1.

<!-- names: component, disconnected, isolated vertex -->

#### Counting With An Outer Loop

The algorithm keeps `visited` for the whole run and loops over every vertex number from 0 to n - 1. When the loop reaches a vertex that is already marked, the vertex belongs to a component that an earlier search found, so the loop moves on. When the loop reaches an unmarked vertex, the program starts a search there and adds 1 to a counter. The search marks every vertex of that vertex's component.

#### Why Each Start Finds One New Component

The invariant is that every outer-loop start on an unmarked vertex discovers exactly one new component. The vertex is unmarked, so no earlier search reached it, and its component is new. The search reaches all of that component, because the component is closed under edges. The search reaches nothing outside it, because no edge leaves it. After the search, the whole component is marked, so no later start can find it again. The counter therefore equals the number of components. The size of the search, meaning the number of vertices it marks, equals the size of the component.

#### Joining Components With Edges

An added edge between two different components merges them into one, and an edge inside a component changes nothing. One edge therefore lowers the component count by at most 1. A graph with `c` components needs exactly `c - 1` added edges to become connected.

<!-- stage: variables -->
### State For Counting Components

The loop needs four values. The values `visited` and `count` persist across all starts, and `size` starts again for each search.

- **visited** is a `boolean[n]` that lives for the whole loop and is never reset between starts.
- **start** is the loop index, and it is a new source whenever `visited[start]` is false.
- **count** is the number of searches launched so far, which equals the number of components found.
- **size** is the number of vertices that the current search marks.

Resetting `visited` between starts would make every start look new and would count vertices and not components.

<!-- stage: trace -->
### Two Graphs Counted By Starting Points

#### Three Components In Six Vertices

The first trace uses the graph from the naive stage, with the edges 0-1, 1-2 and 3-4. The cells are the vertices, and the pointer `start` marks the vertex that the outer loop examines. The variable `marked` lists the vertices that are marked after the step.

The loop starts a search at vertex 0 and finds three vertices. It skips vertices 1 and 2, which are marked. It starts a second search at vertex 3 and finds two vertices. Vertex 4 is skipped, and vertex 5 starts a third search that finds one vertex.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"count":1,"size":3,"marked":"[0,1,2]"},"note":"The loop finds vertex 0 unmarked and opens component 1, and the search reaches 3 vertices."},{"at":{"start":1},"vars":{"count":1,"size":"-","marked":"[0,1,2]"},"note":"The loop reaches vertex 1, finds it marked and skips it."},{"at":{"start":2},"vars":{"count":1,"size":"-","marked":"[0,1,2]"},"note":"Vertex 2 belongs to an earlier component, so no new search starts."},{"at":{"start":3},"vars":{"count":2,"size":2,"marked":"[0,1,2,3,4]"},"note":"Vertex 3 has no mark, so component 2 begins here and the search marks 2 vertices."},{"at":{"start":4},"vars":{"count":2,"size":"-","marked":"[0,1,2,3,4]"},"note":"The loop reaches vertex 4, finds it marked and skips it."},{"at":{"start":5},"vars":{"count":3,"size":1,"marked":"[0,1,2,3,4,5]"},"note":"Vertex 5 is unmarked, so the loop starts a search and counts component 3. The search marks 1 vertex."}]}
```

#### A Cycle And A Single Vertex

The second trace uses seven vertices and the edges 0-6, 2-6, 1-4, 4-5 and 5-1. The vertices 1, 4 and 5 form a cycle, and vertex 3 has no edge.

The search from vertex 0 reaches vertices 6 and 2 as well, so the loop skips vertex 2. The search from vertex 1 goes around the cycle and stops when it meets marked vertices.

```trace
{"cells":[0,1,2,3,4,5,6],"pointers":["start"],"steps":[{"at":{"start":0},"vars":{"count":1,"size":3,"marked":"[0,2,6]"},"note":"The loop reaches unmarked vertex 0, so it counts component 1, and the search marks 3 vertices."},{"at":{"start":1},"vars":{"count":2,"size":3,"marked":"[0,1,2,4,5,6]"},"note":"The loop reaches unmarked vertex 1, so it counts component 2, and the search marks 3 vertices."},{"at":{"start":2},"vars":{"count":2,"size":"-","marked":"[0,1,2,4,5,6]"},"note":"Vertex 2 already carries a mark from an earlier search, so the loop does not start another."},{"at":{"start":3},"vars":{"count":3,"size":1,"marked":"[0,1,2,3,4,5,6]"},"note":"The loop reaches unmarked vertex 3, so it counts component 3, and the search marks 1 vertex."},{"at":{"start":4},"vars":{"count":3,"size":"-","marked":"[0,1,2,3,4,5,6]"},"note":"Vertex 4 already carries a mark from an earlier search, so the loop does not start another."},{"at":{"start":5},"vars":{"count":3,"size":"-","marked":"[0,1,2,3,4,5,6]"},"note":"Vertex 5 already carries a mark from an earlier search, so the loop does not start another."},{"at":{"start":6},"vars":{"count":3,"size":"-","marked":"[0,1,2,3,4,5,6]"},"note":"Vertex 6 already carries a mark from an earlier search, so the loop does not start another."}]}
```

<!-- stage: code -->
### Counting And Sizing In Code

#### Outer Loop With A Depth-First Search

```java
static int countComponents(List<List<Integer>> adj) {
    boolean[] visited = new boolean[adj.size()];
    int count = 0;
    for (int start = 0; start < adj.size(); start++) {
        if (visited[start]) continue;          // belongs to a component found earlier
        count++;                               // an unmarked start opens a new component
        explore(adj, visited, start);
    }
    return count;
}

static int explore(List<List<Integer>> adj, boolean[] visited, int v) {
    visited[v] = true;                         // mark on entry
    int size = 1;
    for (int w : adj.get(v)) {
        if (!visited[w]) size += explore(adj, visited, w);
    }
    return size;                               // vertices marked by this call
}
```

The method `explore` returns the number of vertices that it marks, so a caller that collects those return values gets the component sizes in order of their smallest vertex.

#### Cost Of The Outer Loop

- **Time** is O(V + E), because the loop visits each vertex once and the searches read each adjacency entry once in total.
- **Space** is O(V), because `visited` holds V entries and the recursion reaches depth V on a path.

<!-- stage: applicability -->
### Recognizing Questions About Groups

#### Spotting The Cue

Look for a question that counts groups, sizes groups or asks whether everything is joined. Words such as network, cluster, friend circle and province point to components. The graph may fall into several pieces, so the program needs a search from every unmarked vertex.

#### The Invariant And Its False Friend

The invariant is that each outer-loop start on an unmarked vertex finds exactly one new component. A false friend is a single search from vertex 0. It answers whether vertex 0 reaches a target, and it looks the same as a count on connected samples. It fails as soon as the graph has a second component, as the naive method showed.

#### Java Hazards

Create `visited` once before the loop and not inside it. Count at the call site of the search, because a count placed inside the recursion counts vertices. An adjacency matrix has no neighbor list, so scan the row of the matrix for entries equal to 1 and skip the diagonal. A path of 100,000 vertices needs an explicit stack, as in the lesson Visited State.

<!-- stage: exercises -->
### Exercises

#### [Build] Count Components (Author exercise)
<!-- id: gt-count-components -->

**Prerequisites.** The outer loop and the `visited` array of this lesson.

**Problem.** Vertices are numbered `0` to `n - 1`, and the array `edges` lists undirected edges as pairs `[a, b]`. A component is a maximal set of vertices in which every pair is joined by a path. Return the number of components.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= a, b < n` and `a != b`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Return** is an `int`, and neither input changes.

**Example 1.** Input `n = 5` and `edges = [[0,1],[1,2],[3,4]]`, output 2.

**Example 2.** Input `n = 6` and `edges = [[0,1],[2,3],[3,4]]`, output 3.

**Hint.** What does the outer loop do when it reaches a vertex that an earlier search already marked?

**Changed decision.** The program starts a search from every unmarked vertex and not only from vertex 0.

#### [Vary] Component Sizes (Author exercise)
<!-- id: gt-component-sizes -->

**Prerequisites.** The previous exercise.

**Problem.** The input has the same form as in the previous exercise. Order the components by their smallest vertex number. Return an array that holds the number of vertices of each component in that order.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= a, b < n` and `a != b`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Return** is an `int[]` whose entries add up to `n`, and neither input changes.

**Example 1.** Input `n = 6` and `edges = [[0,1],[3,4],[4,5]]`, output `[2,1,3]`.

**Example 2.** Input `n = 5` and `edges = [[4,0],[0,3]]`, output `[3,1,1]`.

**Hint.** The outer loop meets the smallest vertex of each component first. What can each search report when it finishes?

**Changed decision.** The answer changes from one number to one size per start, and the search must report how many vertices it marked.

#### [Boundary] No Edges And One Component (Author exercise)
<!-- id: gt-no-edges-one-component -->

**Prerequisites.** The two exercises above.

**Problem.** The input has the form `n` and `edges`, with undirected edges. An added edge joins two chosen vertices. Return the smallest number of edges to add so that the graph has exactly one component.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= a, b < n` and `a != b`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Return** is an `int`, and it is 0 when the graph already has one component.

**Example 1.** Input `n = 4` and `edges = []`, output 3.

**Example 2.** Input `n = 4` and `edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]`, output 0.

**Hint.** How many components does each graph in the examples have, and how many components can one added edge merge?

**Changed decision.** The count of components turns into a repair cost, and the two extremes are all vertices isolated and all vertices joined.

#### [Recognize] Number of Provinces (LeetCode 547)
<!-- id: gt-number-of-provinces -->

**Prerequisites.** The count of components and the adjacency matrix from the lesson Graph Representation.

**Problem.** A country has `n` cities. The matrix `isConnected` has `isConnected[i][j] = 1` when cities `i` and `j` are joined by a direct road, and 0 otherwise. A province is a maximal set of cities in which every pair is joined by a chain of roads. Return the number of provinces.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 200`.
- **Matrix** is an `n` by `n` array whose entries are 0 or 1.
- **Diagonal** entries satisfy `isConnected[i][i] = 1`.
- **Symmetry** holds, so `isConnected[i][j] = isConnected[j][i]`.
- **Return** is an `int`, and the matrix does not change.

**Example 1.** Input `isConnected = [[1,0,0,1],[0,1,0,0],[0,0,1,0],[1,0,0,1]]`, output 3.

**Example 2.** Input `isConnected = [[1,1,1],[1,1,1],[1,1,1]]`, output 1.

**Hint.** What is the neighbor list of a city, and where do you read it?

**Changed decision.** The graph arrives as an adjacency matrix, so each row replaces the neighbor list and the scan costs O(n) per vertex.
