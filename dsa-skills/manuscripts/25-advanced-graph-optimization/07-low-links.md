<!-- lesson-kind: standard -->
<!-- lesson-id: low-links -->
## Find Bridges With Low Links

<!-- stage: context -->
### One Cable Can Split A Network

A data center connects its servers with network cables. An operator asks which single cable, if it fails, leaves some servers unable to reach others. The first script tests the cables one at a time. It unplugs a cable in memory, checks whether every server still reaches every other server, and plugs the cable back. With 20,000 cables, the script runs 20,000 full reachability checks, and the nightly report takes hours. The question is ordinary, and a much faster answer exists.

Model the servers as vertices numbered 0 to n - 1 and the cables as undirected edges. Two cables may join the same pair of servers, and the input arrays stay unchanged. A **connected component** is a maximal group of vertices in which every vertex reaches every other vertex along edges. A **bridge** is an edge whose removal increases the number of connected components. Network operators call such a cable a single point of failure.

This lesson asks how to list every bridge with one traversal of the graph, without testing each edge on its own.

<!-- stage: naive -->
### Removing Each Edge And Searching Again

The direct method follows the definition. For each edge, it builds the graph without that edge and runs a breadth-first search from one endpoint. When the search does not reach the other endpoint, the edge is a bridge.

```java
static List<int[]> bridgesByRemoval(int n, int[][] cables) {
    List<int[]> found = new ArrayList<>();
    for (int skip = 0; skip < cables.length; skip++) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int i = 0; i < cables.length; i++) {
            if (i == skip) continue;
            adj.get(cables[i][0]).add(cables[i][1]);
            adj.get(cables[i][1]).add(cables[i][0]);
        }
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(cables[skip][0]);
        seen[cables[skip][0]] = true;
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int next : adj.get(cur)) {
                if (!seen[next]) { seen[next] = true; queue.add(next); }
            }
        }
        if (!seen[cables[skip][1]]) found.add(cables[skip]);
    }
    return found;
}
```

The method is correct, because a search without the edge reaches the far endpoint exactly when another route joins the two endpoints. The cost depends on the number of edges, since each edge triggers a new search.

```predict
A network has 5,000 servers and 20,000 cables. About how many cable visits does bridgesByRemoval make in total?

It makes about 20,000 searches, and each search visits up to 40,000 adjacency entries, which is two entries for each of the 20,000 cables. The total is near 800 million entry visits, plus the cost of rebuilding the lists 20,000 times. The method has no memory between searches. Every search rediscovers almost the same graph, so the time grows as the product of edges and graph size.
```

<!-- stage: bottleneck -->
### One Graph Is Searched Again And Again

Each of the E searches explores nearly the entire graph, and the graphs of two searches differ by a single edge. The total cost is O(E * (V + E)), where V is the number of vertices and E is the number of edges. For the network above that is hundreds of millions of steps, and a network ten times larger needs a hundred times more.

Most of this work is wasted, because most edges are not bridges. An edge lies on a cycle in nearly every real network, since operators add redundant cables on purpose. Once one search shows that a cycle covers an edge, the same fact covers every other edge on that cycle, and the method never reuses it.

A single depth-first search already visits every vertex and every edge once. While it runs, it can record how far back each part of the search can reach by a second route. The facts the repeated searches recompute are then collected in one pass of O(V + E) time. The next stage defines what to record.

<!-- stage: insight -->
### Asking What A Subtree Can Reach

A tree edge from a parent to a child is a bridge exactly when nothing in the child's subtree has another route to the parent or above.

<!-- names: discovery time, back edge, low link -->

#### The Depth-First Tree

Run depth-first search from vertex 0 and keep the edge along which each new vertex was first found. These **tree edges** form a spanning tree of the component, with each vertex except the root joined to one **parent**. The vertices below a vertex `u` in the tree, including `u`, form the **subtree** of `u`. Every other edge of the graph is a non-tree edge.

#### Discovery Time Orders The Vertices

The **discovery time** `disc[u]` is the number of vertices the search has discovered before `u`, so the root has `disc` 0. A vertex discovered later has a larger value. Discovery times give a cheap test for ancestry. A vertex on the path from the root to `u` has a smaller discovery time than `u`.

#### Every Other Edge Is A Back Edge

In an undirected graph, each non-tree edge joins a vertex to one of its ancestors. This kind of edge is a **back edge**. The reason is the order of the search. When the search stands at `u` and scans an edge to `v`, an undiscovered `v` becomes a child of `u`. A discovered `v` was found earlier on the current path, so it is an ancestor of `u`. Otherwise it was found inside the subtree of `u`, so it is a descendant. No edge can point to a finished branch elsewhere, because the search would have crossed that edge from the other end first.

#### The Low Link Value

The **low link** `low[u]` is the smallest discovery time that the subtree of `u` can reach by taking one back edge. The route may start at any vertex of the subtree. The back edge may not be the tree edge that joins `u` to its parent. Written as a rule, `low[u]` is the minimum of three kinds of value. The first is `disc[u]` itself. The second is `disc[w]` for every back edge from `u` to an ancestor `w`. The third is `low[c]` for every child `c` of `u`. The third part passes reach upward from deep vertices to their ancestors.

#### The Bridge Test

Take the tree edge from `u` to its child `v`. The edge is a bridge exactly when `low[v] > disc[u]`. If the condition holds, every route out of the subtree of `v` lands on a vertex discovered at time `disc[u] + 1` or later. Such a vertex lies inside the subtree of `v` itself. Removing the edge strands the whole subtree. If the condition fails, some back edge leaves the subtree and lands on `u` or on an ancestor of `u`. That edge and the tree path form a second route, and removing the tree edge keeps the graph connected. A non-tree edge is never a bridge, because it closes a cycle with the tree path between its endpoints.

#### Skipping The Parent By Edge Number

When the search at `v` scans its edge to the parent `u`, that edge must not count as a back edge. Otherwise every `low[v]` would reach `disc[u]`, and no bridge could appear. The safe rule skips the edge by its number in the input and not by the parent vertex. Two cables between the same servers have two numbers. The search skips only the one it arrived by, and the second cable correctly counts as a route back. The second trace below shows what goes wrong with a skip by vertex.

<!-- stage: variables -->
### Arrays And The Search Clock

The finder reads `n` and the array `cables` of pairs `[a, b]`, and it changes neither. It builds an adjacency list in which each entry holds the neighbor and the number of the cable, and it keeps four working values.

- **disc** is an `int[]` of length `n`; the value -1 marks a vertex that the search has not reached.
- **low** is an `int[]` of length `n`; it starts equal to `disc[u]` and only decreases.
- **timer** is the next discovery time to give out; it increases by one at each new vertex.
- **parentId** is the number of the cable the search used to enter the current vertex; the root receives -1.

The method writes each pair that passes the bridge test to a list as it finds the pair. All values are small nonnegative counts or -1, so `int` is enough and no overflow guard is needed. The search runs recursively, so the call depth equals the longest tree path, and the exercises keep graphs small enough for the default stack.

<!-- stage: trace -->
### Two Runs On Small Cable Maps

#### Two Triangles Joined By A Cable

The first map has seven servers and eight cables. Servers 0, 1 and 2 form a triangle. Servers 3, 4 and 5 form a second triangle. Cable 2-3 joins the triangles, and server 6 hangs from server 5 by cable 5-6. Each cell is a server in order of discovery, and the pointer `at` marks the server whose values change at this step. The variables are `disc`, `low` and `flagged`, which counts the bridges found so far. At step 4, server 2 sees the back edge to server 0 and `low` drops to 0. At step 8, server 5 sees the back edge to server 3 and `low` drops to 3. Server 6 returns with `low` 6, which exceeds `disc` 5 of server 5, so cable 5-6 is a bridge. Server 3 later returns with `low` 3, which exceeds `disc` 2 of server 2, so cable 2-3 is a bridge. Every other return fails the test, and the run finds exactly two bridges.

```trace
{"cells":["v0","v1","v2","v3","v4","v5","v6"],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"disc":0,"low":0,"flagged":0},"note":"Vertex 0 is discovered at time 0, so disc and low both start at 0."},{"at":{"at":1},"vars":{"disc":1,"low":1,"flagged":0},"note":"Vertex 1 is discovered at time 1, so disc and low both start at 1."},{"at":{"at":2},"vars":{"disc":2,"low":2,"flagged":0},"note":"Vertex 2 is discovered at time 2, so disc and low both start at 2."},{"at":{"at":2},"vars":{"disc":2,"low":0,"flagged":0},"note":"Vertex 2 sees the back edge to vertex 0 with disc 0, so low becomes 0."},{"at":{"at":3},"vars":{"disc":3,"low":3,"flagged":0},"note":"Vertex 3 is discovered at time 3, so disc and low both start at 3."},{"at":{"at":4},"vars":{"disc":4,"low":4,"flagged":0},"note":"Vertex 4 is discovered at time 4, so disc and low both start at 4."},{"at":{"at":5},"vars":{"disc":5,"low":5,"flagged":0},"note":"Vertex 5 is discovered at time 5, so disc and low both start at 5."},{"at":{"at":5},"vars":{"disc":5,"low":3,"flagged":0},"note":"Vertex 5 sees the back edge to vertex 3 with disc 3, so low becomes 3."},{"at":{"at":6},"vars":{"disc":6,"low":6,"flagged":0},"note":"Vertex 6 is discovered at time 6, so disc and low both start at 6."},{"at":{"at":5},"vars":{"disc":5,"low":3,"flagged":1},"note":"Child 6 returns with low 6. Vertex 5 has disc 5, and 6 exceeds 5, so edge 5-6 is a bridge."},{"at":{"at":4},"vars":{"disc":4,"low":3,"flagged":1},"note":"Child 5 returns with low 3. Vertex 4 has disc 4, and 3 does not exceed 4, so edge 4-5 is not a bridge."},{"at":{"at":3},"vars":{"disc":3,"low":3,"flagged":1},"note":"Child 4 returns with low 3. Vertex 3 has disc 3, and 3 does not exceed 3, so edge 3-4 is not a bridge."},{"at":{"at":2},"vars":{"disc":2,"low":0,"flagged":2},"note":"Child 3 returns with low 3. Vertex 2 has disc 2, and 3 exceeds 2, so edge 2-3 is a bridge."},{"at":{"at":1},"vars":{"disc":1,"low":0,"flagged":2},"note":"Child 2 returns with low 0. Vertex 1 has disc 1, and 0 does not exceed 1, so edge 1-2 is not a bridge."},{"at":{"at":0},"vars":{"disc":0,"low":0,"flagged":2},"note":"Child 1 returns with low 0. Vertex 0 has disc 0, and 0 does not exceed 0, so edge 0-1 is not a bridge."}]}
```

#### Skipping The Parent Vertex Fails

The second map has four servers and four cables. Cable 0-1 and cable 2-3 are single cables, and two cables join servers 1 and 2. Neither of the double cables is a bridge, because the other one still carries traffic. This run uses the wrong rule that skips every edge toward the parent vertex. At server 2, the second cable toward server 1 is skipped, so `low` of server 2 stays 2. When server 2 returns, the value 2 exceeds `disc` 1 of server 1, and the run flags the pair 1-2 as a bridge. The correct rule, which skips only the cable of arrival, lets server 2 see the second cable as a back edge to server 1 and sets `low` to 1. The flagged count ends at 3 where the true count is 2.

```trace
{"cells":["v0","v1","v2","v3"],"pointers":["at"],"steps":[{"at":{"at":0},"vars":{"disc":0,"low":0,"flagged":0},"note":"Vertex 0 is discovered at time 0, so disc and low both start at 0."},{"at":{"at":1},"vars":{"disc":1,"low":1,"flagged":0},"note":"Vertex 1 is discovered at time 1, so disc and low both start at 1."},{"at":{"at":2},"vars":{"disc":2,"low":2,"flagged":0},"note":"Vertex 2 is discovered at time 2, so disc and low both start at 2."},{"at":{"at":3},"vars":{"disc":3,"low":3,"flagged":0},"note":"Vertex 3 is discovered at time 3, so disc and low both start at 3."},{"at":{"at":2},"vars":{"disc":2,"low":2,"flagged":1},"note":"Child 3 returns with low 3. Vertex 2 has disc 2, and 3 exceeds 2, so edge 2-3 is a bridge."},{"at":{"at":1},"vars":{"disc":1,"low":1,"flagged":2},"note":"Child 2 returns with low 2. Vertex 1 has disc 1, and 2 exceeds 1, so edge 1-2 is a bridge. The edge has a twin cable, so this answer is wrong."},{"at":{"at":0},"vars":{"disc":0,"low":0,"flagged":3},"note":"Child 1 returns with low 1. Vertex 0 has disc 0, and 1 exceeds 0, so edge 0-1 is a bridge."}]}
```

<!-- stage: code -->
### Finding Bridges In One Search

The class stores the graph and the two arrays once, and the method `visit` fills them. The loop in `find` starts a search from every undiscovered vertex, so a graph with several components also works.

```java
final class BridgeFinder {
    private final List<List<int[]>> adj = new ArrayList<>();
    private final int[] disc;
    private final int[] low;
    private final List<int[]> bridges = new ArrayList<>();
    private int timer = 0;

    BridgeFinder(int n, int[][] cables) {
        disc = new int[n];
        low = new int[n];
        Arrays.fill(disc, -1);
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int id = 0; id < cables.length; id++) {
            adj.get(cables[id][0]).add(new int[] {cables[id][1], id});
            adj.get(cables[id][1]).add(new int[] {cables[id][0], id});
        }
    }

    List<int[]> find() {
        for (int s = 0; s < disc.length; s++) {
            if (disc[s] == -1) visit(s, -1);
        }
        return bridges;
    }

    private void visit(int u, int parentId) {
        disc[u] = low[u] = timer++;
        for (int[] step : adj.get(u)) {
            int v = step[0];
            if (step[1] == parentId) continue;
            if (disc[v] == -1) {
                visit(v, step[1]);
                low[u] = Math.min(low[u], low[v]);
                if (low[v] > disc[u]) bridges.add(new int[] {u, v});
            } else {
                low[u] = Math.min(low[u], disc[v]);
            }
        }
    }
}
```

The order of two lines inside the tree branch matters. The call to `visit(v, ...)` comes first, because `low[v]` is final only after the child returns. The bridge test comes after the update of `low[u]`, and it reads `low[v]`, which does not depend on that update. In the other branch, `disc[v]` is smaller than `disc[u]` for an ancestor and larger for a descendant already finished. The larger value cannot lower `low[u]`, so the code needs no extra test. The search visits each adjacency entry once, so the time is O(V + E). The adjacency list, the two arrays and the call stack use O(V + E) memory.

<!-- stage: applicability -->
### Recognizing Bridge Problems

#### Reading The Cue

Use this method when an undirected graph and a question about the loss of one edge appear together. Typical statements ask which cables, roads, or dependencies are critical, whether a network survives any single failure, or how many edges a redundant design still needs. The answer is usually a list of edges, a count, or a yes or no for a whole graph. With the same two arrays, the test `low[v] >= disc[u]` finds articulation points, the vertices whose removal splits the graph.

#### Checking The Invariant

The invariant is that `low[u]` is final when `visit(u, ...)` returns. It equals the smallest discovery time that the subtree of `u` reaches through one back edge, other than the edge to its parent. It holds because `low[u]` starts at `disc[u]`, every back edge of `u` can only lower it, and every child hands up its own final value. Check the cases that break it. Test a graph with two cables between the same pair. Test a graph with no edge at all. Test a root that has several children, where the bridge test works unchanged but the articulation test needs a separate rule.

#### Avoiding The False Friend

A false friend is a familiar idea that looks right for the problem and fails on it. The first false friend is the cycle check from directed graphs. In a directed graph, a search also produces edges that join unrelated branches, so the ancestor argument fails. The question about losing one edge changes there, and strongly connected components answer the related question. The second false friend is the skip by parent vertex, shown in the second trace. It is correct for simple graphs and wrong as soon as a pair of vertices has two edges. Do not use this method when edges have capacities and the question asks for the cheapest set of edges to cut. That question needs flow, which this chapter does not cover.

<!-- stage: exercises -->
### Exercises

#### [Build] Discovery And Low Values (Author exercise)
<!-- id: ga-low-disc-values -->

**Prerequisites.** The variables and the code of this lesson.

**Problem.** An undirected connected graph has vertices `0` to `n - 1` and the edges in `edges`, where edge number `i` joins `edges[i][0]` and `edges[i][1]`. Run a depth-first search from vertex `0`. At each vertex, scan its edges in the order of their numbers, and treat a self loop as one edge scanned twice. Return an `int[][]` of two rows. Row 0 is the discovery time of every vertex. Row 1 is the low link of every vertex, where the edge used to enter a vertex does not count as a back edge, and any other edge does.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 300`.
- **Edges** satisfy `0 <= edges.length <= 1500`, and repeated pairs and self loops may occur.
- **Connectivity** is guaranteed, so every vertex receives a discovery time.
- **Mutation** of `edges` is not allowed.

**Example 1.** Input `n = 5`, `edges = [[0,1],[0,2],[1,2],[2,3],[3,4]]`, output `[[0,1,2,3,4],[0,0,0,3,4]]`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[0,1],[1,2]]`, output `[[0,1,2],[0,0,2]]`.

**Hint.** When the search stands at vertex 1 in the second example, does the second cable to vertex 0 count as a way back?

**Changed decision.** The method returns the two arrays and does not test for bridges, so the only work is updating `low` from child returns and back edges.

#### [Vary] Bridge Test (Author exercise)
<!-- id: ga-low-bridge-test -->

**Prerequisites.** The exercise above.

**Problem.** A depth-first search of a connected undirected graph produced three arrays of length `n`. Entry `parent[v]` is the parent of `v` in the search tree, with `parent[0] = -1`. Entry `disc[v]` is the discovery time of `v`. Entry `low[v]` is the low link of `v`. Return an `int[]` that lists in increasing order every vertex `v` other than the root whose tree edge to `parent[v]` is a bridge.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 300`.
- **Arrays** come from a real search, with `low` computed by skipping the arrival edge by number.
- **Result** is empty when the graph has no bridge.
- **Mutation** of the three arrays is not allowed.

**Example 1.** Input `parent = [-1,0,1,2,3,4]`, `disc = [0,1,2,3,4,5]`, `low = [0,0,0,3,4,5]`, output `[3,4,5]`.

**Example 2.** Input `parent = [-1,0,1]`, `disc = [0,1,2]`, `low = [0,0,0]`, output `[]`.

**Hint.** In the second example, `low[1]` equals `disc[0]`. Does an equal value mean that the subtree escapes?

**Changed decision.** The method makes a decision from finished arrays and does not search, and it must use a strict comparison.

#### [Boundary] Root Articulation Rule (Author exercise)
<!-- id: ga-low-root-articulation -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected graph has vertices `0` to `n - 1` and the edges in `edges`. An **articulation point** is a vertex whose removal, together with its edges, increases the number of connected components among the remaining vertices. Return an `int[]` of all articulation points in increasing order. Start a depth-first search from every undiscovered vertex in increasing order. A search root is an articulation point when it has at least two children in its tree. Any other vertex `u` is one when it has a child `c` with `low[c] >= disc[u]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 300`.
- **Edges** satisfy `0 <= edges.length <= 1500`, and repeated pairs and self loops may occur.
- **Components** may be several, and an isolated vertex is never a result.
- **Mutation** of `edges` is not allowed.

**Example 1.** Input `n = 6`, `edges = [[0,1],[0,2],[0,3],[3,4],[4,5],[5,3]]`, output `[0,3]`.

**Example 2.** Input `n = 7`, `edges = [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[5,6]]`, output `[5]`.

**Hint.** What does the nonroot rule report for a root, and how many children does a root need before its removal splits the graph?

**Changed decision.** The method counts children at the root and uses the nonstrict comparison `>=` below it, where the bridge test uses a strict one.

#### [Recognize] Critical Connections in a Network (LeetCode 1192)
<!-- id: ga-low-critical-connections -->

**Prerequisites.** All three exercises above.

**Problem.** A network has servers `0` to `n - 1` and undirected connections in `connections`. The network is connected. A critical connection is a connection whose removal disconnects the network. Removing a critical connection leaves two components, and its **small side** is the smaller of the two component sizes. Return an `int[]` of length 2. The first entry is the number of critical connections. The second entry is the largest small side over all critical connections, or `0` when none exists.

**Constraints.** The limits are:
- **Servers** satisfy `1 <= n <= 1000`.
- **Connections** satisfy `0 <= connections.length <= 3000`, and repeated pairs and self loops may occur.
- **Connectivity** is guaranteed.
- **Result** has length 2, and the two entries are nonnegative.

**Example 1.** Input `n = 7`, `connections = [[0,1],[1,2],[2,0],[2,3],[3,4],[4,5],[5,3],[5,6],[6,5]]`, output `[1,3]`.

**Example 2.** Input `n = 6`, `connections = [[0,1],[1,2],[2,0],[2,3],[3,4],[4,5]]`, output `[3,3]`.

**Hint.** If the search also returns the size of each subtree, how large is the side below a bridge, and how large is the other side?

**Changed decision.** The method returns a count and a size and not the list of connections. It must also add up subtree sizes during the same search.
