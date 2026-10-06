<!-- lesson-kind: standard -->
<!-- lesson-id: undirected-parent-state -->
## Undirected Parent State

<!-- stage: context -->
### Rejecting A Loop In Network Links

A network team records which switches share a cable as undirected links. A loop of cables makes broadcast packets circulate forever, so the configuration check must reject any layout that contains a cycle. A cycle is a path that returns to its start vertex without using any edge twice.

Model the switches as vertices and the cables as undirected edges. The task is to return true when the graph contains a cycle and false otherwise. The graph may be split into several separate pieces, and a cable between two switches appears in the neighbor list of both switches.

That last detail is the trap. The search walks along a cable to reach a new switch, and the new switch finds the same cable in its own list. This lesson asks how a depth-first search tells a real loop from the cable it just came along.

<!-- stage: naive -->
### Reporting Any Visited Neighbor

The first attempt marks vertices as visited and reports a cycle as soon as a vertex reads a neighbor that is already visited.

```java
static boolean hasCycle(List<List<Integer>> adj) {
    boolean[] visited = new boolean[adj.size()];
    for (int start = 0; start < adj.size(); start++) {
        if (!visited[start] && dfs(adj, visited, start)) return true;
    }
    return false;
}

private static boolean dfs(List<List<Integer>> adj, boolean[] visited, int v) {
    visited[v] = true;
    for (int next : adj.get(v)) {
        if (visited[next]) return true;
        if (dfs(adj, visited, next)) return true;
    }
    return false;
}
```

Consider the smallest graph with an edge: two vertices, 0 and 1, joined by one cable.

```predict
What does hasCycle return for this graph, and what is the correct answer?

It returns true, and the correct answer is false. The call for vertex 0 enters vertex 1. Vertex 1 reads its neighbor list, finds 0, sees that 0 is visited and reports a cycle. One cable cannot form a loop, because a cycle needs a way back that uses different edges.
```

<!-- stage: bottleneck -->
### Every Edge Looks Like A Cycle

The method visits each vertex once and reads each neighbor list once, so its time is O(V + E) and the traversal itself is fine. The defect is the test. Every edge appears twice, once in the list of each endpoint. After the search crosses an edge from `u` to `v`, the list of `v` contains `u`, and `u` already has its visited flag. Every graph with at least one edge is therefore reported as cyclic, including a path and a star.

Ignoring all visited neighbors does not repair this. The method would then never report a cycle, because the only way to meet a visited vertex is through an edge that closes a loop. The test must separate two kinds of visited neighbors: the one the search just came from, and every other one.

A repair that stores every crossed edge in a hash set works, but it costs O(E) extra memory and a hash lookup per step. The call that enters a vertex already knows which vertex it came from. A better method passes that single fact down and spends no extra memory beyond the call stack. The next stage names it.

<!-- stage: insight -->
### Passing The Entry Vertex Into Each Call

A vertex has exactly one entry, so exactly one neighbor in its list stands for the cable that the search used. Every other visited neighbor is evidence of a second route.

<!-- names: parent, tree edge, back edge -->

#### What The Parent Is

The **parent** of a vertex is the vertex whose call entered it. The start vertex of each piece has no parent, and the code uses -1 for that case. Each call takes its parent as an extra argument, which needs no array.

#### Two Kinds Of Edges

A **tree edge** is an edge that the search crosses to discover a new vertex. The tree edges of one piece never form a cycle, because each vertex has one discovery. A **back edge** is any other edge of the graph. The search meets a back edge as a neighbor that is already visited and is not the parent. The only visited neighbor that is the parent is the other end of the tree edge that led here.

#### Why The Rule Is Correct

The rule is: report a cycle when a visited neighbor is not the parent. Suppose vertex `v` reads a visited neighbor `w` that is not its parent. The tree edges give a path between `w` and `v`, and the edge between them is not on that path, so the path plus that edge closes a cycle.

The other direction also holds. If a cycle exists, its edges cannot all be tree edges, so at least one is a back edge. The search reads that edge from either end. Both endpoints have their flag set and the other end is not the parent, so the rule fires.

The invariant is that every visited neighbor skipped by the rule is the tree edge that entered the current vertex. This holds when the graph has no two edges between the same pair of vertices. A repeated edge breaks it, and an exercise below handles that case.

<!-- stage: variables -->
### What Each Call Carries

Each call carries one vertex and one entry vertex. All calls share the graph and the visited flags. Every name below has a fixed meaning.

- **adj** is the adjacency list, and `adj.get(v)` holds every neighbor of `v`, one entry per cable.
- **visited** is a boolean array; `true` means a call for that vertex has started.
- **v** is the vertex the current call works on.
- **parent** is an int argument that holds the vertex whose call entered `v`, or -1 for a start vertex.
- **next** is the neighbor currently read from `adj.get(v)`.

<!-- stage: trace -->
### Reading Neighbors On Two Graphs

#### A Graph Without A Cycle

The first graph has the edges 0 to 1, 0 to 2 and 1 to 3. The cells are the vertex ids and the pointer `v` marks the vertex that reads a neighbor. The variable `neighbor` is the entry just read, and `parent` is the entry vertex of `v`. Each vertex reads its parent once and skips it. The search never meets a visited neighbor that is not a parent, so it ends without a report.

```trace
{"cells":[0,1,2,3],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"neighbor":1,"parent":-1},"note":"Vertex 0 reads neighbor 1, which is unvisited, so the search enters it with parent 0."},{"at":{"v":1},"vars":{"neighbor":0,"parent":0},"note":"Vertex 1 reads neighbor 0, which is its parent (0), so the search skips it."},{"at":{"v":1},"vars":{"neighbor":3,"parent":0},"note":"Vertex 1 reads neighbor 3, which is unvisited, so the search enters it with parent 1."},{"at":{"v":3},"vars":{"neighbor":1,"parent":1},"note":"Vertex 3 reads neighbor 1, which is its parent (1), so the search skips it."},{"at":{"v":0},"vars":{"neighbor":2,"parent":-1},"note":"Vertex 0 reads neighbor 2, which is unvisited, so the search enters it with parent 0."},{"at":{"v":2},"vars":{"neighbor":0,"parent":0},"note":"Vertex 2 reads neighbor 0, which is its parent (0), so the search skips it."}]}
```

#### A Graph With A Triangle

The second graph is the triangle on 0, 1 and 2, plus the edge 2 to 3. The search goes from 0 to 1 and from 1 to 2. Vertex 2 first reads vertex 1, which is its parent, and skips it. Then it reads vertex 0. Vertex 0 has its flag set and is not the parent of 2, so the search reports the cycle at once.

```trace
{"cells":[0,1,2,3],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"neighbor":1,"parent":-1},"note":"Vertex 0 reads neighbor 1, which is unvisited, so the search enters it with parent 0."},{"at":{"v":1},"vars":{"neighbor":0,"parent":0},"note":"Vertex 1 reads neighbor 0, which is its parent (0), so the search skips it."},{"at":{"v":1},"vars":{"neighbor":2,"parent":0},"note":"Vertex 1 reads neighbor 2, which is unvisited, so the search enters it with parent 1."},{"at":{"v":2},"vars":{"neighbor":1,"parent":1},"note":"Vertex 2 reads neighbor 1, which is its parent (1), so the search skips it."},{"at":{"v":2},"vars":{"neighbor":0,"parent":1},"note":"Vertex 2 reads neighbor 0. It is visited and is not the parent, so the search reports a cycle."}]}
```

<!-- stage: code -->
### Depth-First Search With A Parent Argument

The outer method starts one search per unvisited vertex, so separate pieces are all covered. The inner method skips exactly one neighbor.

```java
static boolean hasCycle(List<List<Integer>> adj) {
    boolean[] visited = new boolean[adj.size()];
    for (int start = 0; start < adj.size(); start++) {
        if (!visited[start] && dfs(adj, visited, start, -1)) return true;
    }
    return false;
}

private static boolean dfs(List<List<Integer>> adj, boolean[] visited, int v, int parent) {
    visited[v] = true;
    for (int next : adj.get(v)) {
        if (next == parent) continue;
        if (visited[next]) return true;
        if (dfs(adj, visited, next, v)) return true;
    }
    return false;
}
```

The comparison `next == parent` must come before the visited test, because the parent is always visited. The time is O(V + E) and the space is O(V) for `visited` plus the recursion depth, which reaches V on a path graph. A path of many thousands of vertices overflows the default Java stack, so large inputs need an explicit stack.

<!-- stage: applicability -->
### Recognizing The Parent Test

#### Reading The Cue

Use the parent test when an undirected traversal must decide whether a loop exists. Statements ask whether cables, friendships or dependencies in both directions contain a cycle, or whether a connected graph is a tree. Every edge is visible from both endpoints, so the traversal needs to ignore the one edge it arrived by.

#### Checking The Invariant

The invariant is that the only visited neighbor skipped is the entry edge. A comparison by vertex id keeps it only for graphs without repeated edges. With two edges between the same pair, the second edge also leads to the parent vertex and gets skipped, so a cycle of two edges goes unreported. Compare edge indexes when repeated edges occur.

#### Avoiding The False Friend

The false friend is the directed method with three states: unvisited, active and finished. It is unnecessary here. In an undirected graph, an edge to a finished vertex was already read from the finished vertex, and that earlier read reported the cycle. Two states and one parent argument are enough. The opposite mistake is also common. Adding a parent test to a directed graph hides real cycles, because a pair of opposite directed edges is a cycle there.

<!-- stage: exercises -->
### Exercises

#### [Build] DFS With Parent (Author exercise)
<!-- id: dg-dfs-with-parent -->

**Prerequisites.** The parent argument of this lesson.

**Problem.** An undirected graph has vertices `0` to `n - 1`, and each edge `[a, b]` joins `a` and `b` in both directions. A cycle is a sequence of at least three distinct vertices in which consecutive vertices share an edge and the last vertex shares an edge with the first. Return `true` when the graph contains a cycle and `false` otherwise.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 2000`, with no repeated pair and no self loop.
- **Pieces** vary, and the graph can have several.
- **Result** is one `boolean`, and the input is not modified.

**Example 1.** Input `n = 7`, `edges = [[0,1],[1,2],[3,4],[4,5],[5,3],[2,6]]`, output `true`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[2,3],[1,4]]`, output `false`.

**Hint.** What must a call know about how the search entered its vertex, so that it ignores exactly that neighbor?

**Changed decision.** Each recursive call receives its entry vertex, and the method skips that one neighbor instead of every visited neighbor.

#### [Vary] Detect A Triangle (Author exercise)
<!-- id: dg-detect-triangle -->

**Prerequisites.** The exercise above.

**Problem.** Input `n` and `edges` define an undirected graph on the vertices `0` to `n - 1`. A triangle is a set of three distinct vertices `a`, `b` and `c` such that all three pairs `a b`, `b c` and `a c` are edges. Return `true` when the graph contains a triangle. A back edge is an edge that the depth-first search does not use to discover a vertex.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 2000`, with no repeated pair and no self loop.
- **Cycles** longer than three vertices do not count.
- **Result** is one `boolean`.

**Example 1.** Input `n = 6`, `edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]]`, output `false`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[2,3],[3,4],[4,0],[0,2]]`, output `true`.

**Hint.** Every cycle contains a back edge. If a triangle uses a given back edge, what must its two endpoints have in common?

**Changed decision.** The method does not stop at the first non-parent visited neighbor. It treats that neighbor as the end of a back edge and tests whether the two endpoints share a neighbor.

#### [Boundary] Single Edge And Parallel Edges (Author exercise)
<!-- id: dg-parallel-edges -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected multigraph has vertices `0` to `n - 1`, and the same pair of vertices may appear in several edges. A cycle has `k >= 2` distinct edges and `k` distinct vertices `v1` to `vk`. Edge `i` joins `vi` and `v(i+1)`, and the last edge joins `vk` and `v1`. Two parallel edges form a cycle with `k = 2`. Return `true` when the multigraph contains a cycle.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 2000`, and a pair may repeat in either order.
- **Self loops** do not occur.
- **Result** is one `boolean`.

**Example 1.** Input `n = 2`, `edges = [[0,1]]`, output `false`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[1,2],[2,1]]`, output `true`.

**Hint.** Two edges lead to the same neighbor. What can the call compare so that it does not confuse the second edge with the one it arrived by?

**Changed decision.** The call receives the index of its entry edge and skips only that index, so a second edge to the parent vertex counts as a cycle.

#### [Recognize] Graph Valid Tree (LeetCode 261)
<!-- id: dg-valid-tree -->

**Prerequisites.** All three exercises above.

**Problem.** A graph has `n` vertices numbered `0` to `n - 1` and an undirected edge list `edges`. The graph forms a tree when one piece covers all vertices and no cycle exists. Return `true` when the graph is a tree and `false` otherwise.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, with no repeated pair in either order and no self loop.
- **Single vertex** with no edge is a tree.
- **Result** is one `boolean`.

**Example 1.** Input `n = 5`, `edges = [[0,1],[0,2],[0,3],[1,4]]`, output `true`.

**Example 2.** Input `n = 4`, `edges = [[0,1],[2,3]]`, output `false`.

**Hint.** The second example has no cycle. Which second condition does the search have to check after it finishes?

**Changed decision.** The method answers true only when the search from vertex 0 meets no back edge and has visited all `n` vertices.
