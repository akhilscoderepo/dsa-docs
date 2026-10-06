<!-- lesson-kind: standard -->
<!-- lesson-id: cycle-detection -->
## Cycle Detection

<!-- stage: context -->
### Why A Build Finds False Cycles

A build tool compiles four modules. Module 0 uses modules 1 and 2, and both of those use module 3. The tool runs a search over these dependencies and stops with the message "circular dependency". No module depends on itself, directly or through others. A **route** follows edges from vertex to vertex, and a **cycle** is a route that returns to its first vertex without using any listed edge twice. The four modules contain no cycle, so the message is wrong, and the project cannot compile until someone finds out why.

A second tool checks a network of switches joined by cables. A loop of cables can flood the network with endless copies of a packet, so the tool must find any loop. The tool reports a loop on a network that consists of one cable between two switches.

Both tools use a search that remembers vertices it has seen. Both tools misread what a second sight of a vertex means. The question of this lesson is when a vertex that the search sees again proves that a cycle exists.

<!-- stage: naive -->
### Reporting Any Vertex Seen Twice

The quick rule says that a cycle exists whenever the search reaches a vertex that it has already marked. The rule needs only the visited array, and it takes four lines of code inside a depth-first search (DFS).

```java
static boolean seenTwice(List<List<Integer>> adj, boolean[] visited, int u) {
    visited[u] = true;
    for (int v : adj.get(u)) {
        if (visited[v]) return true;
        if (seenTwice(adj, visited, v)) return true;
    }
    return false;
}
```

On the four modules, the search goes 0 to 1 to 3, backs up to 0, goes to 2 and finds module 3 already marked. The method returns true. On the two switches, the search goes from switch 0 to switch 1 and finds switch 0 already marked, so it returns true again. Both answers are false alarms.

<!-- stage: bottleneck -->
### Telling Real Returns From Harmless Ones

```predict
The method returns true for the four modules and for the two switches, and neither graph has a cycle. In each case, what is the marked vertex that the search sees again, and how is it related to the current vertex?

For the switches, the marked vertex is the one the search just came from, reached over the same cable. For the modules, it is a vertex that the search completed earlier on another route. Neither returns to a route that is still open.
```

A marked vertex has three possible relations to the current search. It can be the vertex that the search just left. It can be a vertex whose whole search is already complete. It can be a vertex on the route that is still open. Only the third relation closes a cycle. The naive method treats all three alike, so it is wrong on every graph that has a cable shared by two directions or a vertex reachable by two routes.

A **diamond** is a vertex that two different routes reach, as module 3 is in the first example. Trying every route to separate the cases would cost O(2^n) on a graph with many diamonds. A search that keeps a little more information about each vertex stays at O(n + m) for `n` vertices and `m` edges, because every edge is still examined a constant number of times.

<!-- stage: insight -->
### Giving Each Vertex A Search State

The two false alarms need two different fixes, because an undirected edge and a directed edge behave differently.

#### Undirected Edges Return To The Parent

An undirected edge between `u` and `v` appears in both neighbor lists. When the search moves from `u` to `v`, the list of `v` contains `u` again. That sight is the edge just used, not a cycle. The **parent** of a vertex is the vertex from which the search reached it. The rule is that a marked neighbor other than the parent proves a cycle. The search passes the parent as an argument of each call and skips a neighbor equal to it. For example, on the triangle with edges 0-1, 1-2 and 2-0, the call at vertex 2 has parent 1. It skips 1, then reads 0, which is marked and not the parent, so it reports the cycle. This lesson assumes a simple graph, one with no two edges between the same pair of vertices, because skipping by vertex number would also skip a second edge to the parent. The Boundary exercise removes that assumption.

<!-- names: parent, visiting, finished -->

#### Directed Edges Need Three States

A directed edge `u` to `v` appears only in the list of `u`, so no edge is used twice. A marked neighbor can still be harmless, as the module `3` is. The search therefore gives each vertex one of three states. A vertex is unvisited before the search reaches it. It is **visiting** while its call is still open, which means it lies on the current route. It is **finished** after all of its neighbors are processed and its call returns.

An edge to a visiting vertex proves a cycle, because the route from that vertex down to the current vertex plus the new edge returns to the start. On the edges 0 to 1, 1 to 2 and 2 to 0, the call at vertex 2 reads the edge to vertex 0, which is visiting, and the route 0, 1, 2, 0 is a cycle. An edge to a finished vertex proves nothing. Every vertex that the finished vertex can reach was explored before it finished, and none of them leads back to a visiting vertex on the open route, or the search would already have reported it. In the module example, module 3 finishes under module 1 without reaching module 0, so the later edge from module 2 to module 3 closes no route.

#### Why The Rules Are Complete

Both rules also work in the other direction. Every cycle contains a first vertex that the search enters, and the cycle then forces the search to reach an edge that returns to an open route. So the search misses no cycle, and it reports none that does not exist. On the triangle above, vertex 0 is the first vertex entered, and the edge from vertex 2 back to vertex 0 is the edge that the search reaches while vertex 0 is still open.

<!-- stage: variables -->
### What Each Search Keeps

The two searches keep different small records.

- **visited** marks a vertex that the undirected search has entered.
- **parent** is the argument that tells a call which vertex it came from.
- **state** holds 0 for unvisited, 1 for visiting and 2 for finished in the directed search.
- **adj** is the adjacency list, with each directed edge stored once and each undirected edge stored in both lists.

<!-- stage: trace -->
### Tracing An Undirected And A Directed Graph

#### A Cycle In An Undirected Graph

The first graph has 5 vertices and the edges 0-1, 1-2, 2-3, 3-1 and 3-4. The trace below shows the DFS from vertex 0. The pointer `cur` marks the vertex whose neighbor list the search is reading.

The search enters vertex 1 from vertex 0, and the list of vertex 1 begins with 0, the parent, so the search skips it. The search enters vertex 2 and then vertex 3. The list of vertex 3 holds vertex 2, which is the parent, and then vertex 1. Vertex 1 is marked and is not the parent of 3, so the search reports a cycle through 1, 2 and 3.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"parent":-1,"visited":"10000"},"note":"The search enters vertex 0 and marks it as visited."},{"at":{"cur":1},"vars":{"parent":0,"visited":"11000"},"note":"The search enters vertex 1 and marks it as visited."},{"at":{"cur":1},"vars":{"parent":0,"visited":"11000"},"note":"Neighbor 0 is the parent of vertex 1, so the search skips the edge it just used."},{"at":{"cur":2},"vars":{"parent":1,"visited":"11100"},"note":"The search enters vertex 2 and marks it as visited."},{"at":{"cur":2},"vars":{"parent":1,"visited":"11100"},"note":"Neighbor 1 is the parent of vertex 2, so the search skips the edge it just used."},{"at":{"cur":3},"vars":{"parent":2,"visited":"11110"},"note":"The search enters vertex 3 and marks it as visited."},{"at":{"cur":3},"vars":{"parent":2,"visited":"11110"},"note":"Neighbor 2 is the parent of vertex 3, so the search skips the edge it just used."},{"at":{"cur":3},"vars":{"parent":2,"visited":"11110"},"note":"Neighbor 1 is marked and is not the parent, so the edge 3-1 closes a cycle."}]}
```

#### A Directed Graph With A Late Cycle

The second graph has 5 vertices and the directed edges 0 to 1, 1 to 2, 0 to 2, 0 to 3, 3 to 4 and 4 to 3.

The search enters vertex 1 and then vertex 2. Vertex 2 has no outgoing edge, so it finishes, and vertex 1 finishes after it. Back at vertex 0, the edge to vertex 2 meets a finished vertex and is ignored. This case is the diamond that fooled the naive method. The search then enters 3 and 4. The edge from 4 returns to vertex 3, which is visiting, and the search reports the cycle.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"state":"10000"},"note":"Vertex 0 becomes visiting because its call is now open."},{"at":{"cur":1},"vars":{"state":"11000"},"note":"Vertex 1 becomes visiting because its call is now open."},{"at":{"cur":2},"vars":{"state":"11100"},"note":"Vertex 2 becomes visiting because its call is now open."},{"at":{"cur":2},"vars":{"state":"11200"},"note":"Every neighbor of vertex 2 is processed, so the vertex becomes finished."},{"at":{"cur":1},"vars":{"state":"12200"},"note":"Every neighbor of vertex 1 is processed, so the vertex becomes finished."},{"at":{"cur":0},"vars":{"state":"12200"},"note":"The edge from 0 reaches vertex 2, which is finished, so the search ignores it."},{"at":{"cur":3},"vars":{"state":"12210"},"note":"Vertex 3 becomes visiting because its call is now open."},{"at":{"cur":4},"vars":{"state":"12211"},"note":"Vertex 4 becomes visiting because its call is now open."},{"at":{"cur":4},"vars":{"state":"12211"},"note":"The edge from 4 reaches vertex 3, which is visiting, so the route returns to itself and a cycle exists."}]}
```

<!-- stage: code -->
### Two Cycle Checks In Code

#### Undirected Check With A Parent

The method receives the adjacency list that holds each edge in both lists. The call for the source passes -1 as the parent, because no vertex has a number below 0.

```java
static boolean undirectedHasCycle(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
    boolean[] visited = new boolean[n];
    for (int s = 0; s < n; s++) {
        if (!visited[s] && undirectedFrom(adj, visited, s, -1)) return true;
    }
    return false;
}

static boolean undirectedFrom(List<List<Integer>> adj, boolean[] visited, int u, int parent) {
    visited[u] = true;
    for (int v : adj.get(u)) {
        if (v == parent) continue;
        if (visited[v] || undirectedFrom(adj, visited, v, u)) return true;
    }
    return false;
}
```

#### Directed Check With Three States

The directed method stores each edge once, in the list of its tail, and then runs the restart loop over all vertices.

```java
static boolean directedHasCycle(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) adj.get(e[0]).add(e[1]);
    int[] state = new int[n];
    for (int s = 0; s < n; s++) {
        if (state[s] == 0 && directedFrom(adj, state, s)) return true;
    }
    return false;
}

static boolean directedFrom(List<List<Integer>> adj, int[] state, int u) {
    state[u] = 1;
    for (int v : adj.get(u)) {
        if (state[v] == 1) return true;
        if (state[v] == 0 && directedFrom(adj, state, v)) return true;
    }
    state[u] = 2;
    return false;
}
```

#### Cost And Stack Depth

- **Time** is O(n + m) for both methods, because each vertex is entered once and each edge is read once or twice.
- **Space** is O(n + m) for the lists and arrays, and the call stack adds up to n frames on a long path.

A recursive search on a path of 100000 vertices can overflow the Java call stack. Exercises in this lesson limit `n` so that the recursion stays shallow.

<!-- stage: applicability -->
### Using Search States On New Problems

#### Recognizing The Cue

Look for a statement that asks whether following edges can lead back to a place already on the route. Prerequisite lists, dependency graphs, ownership links and redundant cables all carry that cue. Decide first whether the edges are directed, because that choice selects the rule.

#### The Invariant To Keep

The invariant for the undirected rule is that every marked vertex other than the parent is a real cycle partner. The invariant for the directed rule is that the vertices in the visiting state form exactly the current route from the source. Each rule holds only while the state of a vertex changes at the right moment, on entry and on return.

#### The False Friend

Treating any marked neighbor as a cycle is the false friend of both rules. In an undirected graph, it fires on the edge to the parent. In a directed graph, it fires on a finished vertex, as in the diamond. A second near miss is to use the undirected rule on a directed graph, which loses cycles that use edge directions, or the directed rule on an undirected graph, which reports every edge as a cycle of two.

#### Java Hazards

Compare the parent by vertex number only when no two edges join the same pair of vertices. A repeated edge is a real cycle of two vertices, so a graph with repeated edges needs the parent edge identified by its index in the input. The method below stores each neighbor together with the index of its edge and skips only the one index it arrived by.

```java
static boolean fromEdgeIndex(List<List<int[]>> adj, boolean[] visited, int u, int parentEdge) {
    visited[u] = true;
    for (int[] arc : adj.get(u)) {            // arc[0] is the neighbor, arc[1] the edge index
        if (arc[1] == parentEdge) continue;   // skip the one edge used to arrive
        if (visited[arc[0]] || fromEdgeIndex(adj, visited, arc[0], arc[1])) return true;
    }
    return false;
}
```

Set the finished state after the loop and not before it, because an early set makes the visiting test blind.

<!-- stage: exercises -->
### Exercises

#### [Build] Undirected Parent Check (Author exercise)
<!-- id: gt-undirected-parent-check -->

**Prerequisites.** The parent rule of this lesson and the restart loop of Bipartite Coloring.

**Problem.** An undirected graph has vertices `0..n-1` and edges in `edges`, where `edges[i] = [a, b]` joins `a` and `b`. A cycle is a route that returns to its first vertex without using any listed edge twice. Return true if the graph contains a cycle, and false otherwise. Use a DFS that passes the parent of each vertex, and report a cycle when a marked neighbor differs from the parent.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`.
- **Self-loops** do not occur.
- **Parallel edges** do not occur, so every cycle uses at least three distinct vertices.
- **Return** is a boolean.

**Example 1.** Input `n = 5` and `edges = [[0,1],[1,2],[2,3],[3,1],[3,4]]`, output true.

**Example 2.** Input `n = 5` and `edges = [[0,1],[1,2],[3,4]]`, output false, because the graph is a forest.

**Hint.** When the search stands at `v` and reads the neighbor `u` it came from, which test must skip it?

**Changed decision.** A marked neighbor is a cycle only when it is not the vertex the search came from.

#### [Vary] Directed Three Colors (Author exercise)
<!-- id: gt-directed-three-colors -->

**Prerequisites.** The previous exercise and the three states of this lesson.

**Problem.** A directed graph has vertices `0..n-1` and edges in `edges`, where `edges[i] = [a, b]` is an edge from `a` to `b`. A directed cycle is a route that follows edges in their direction and returns to its first vertex. Return true if the graph has a directed cycle, and false otherwise. Give every vertex one of three states during the DFS, and report a cycle on an edge to a vertex in the visiting state.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`.
- **Self-loops** may occur, and a self-loop is a cycle of length one.
- **Parallel edges** may occur.
- **Return** is a boolean.

**Example 1.** Input `n = 4` and `edges = [[0,1],[0,2],[1,3],[2,3]]`, output false, even though vertex 3 is reached twice.

**Example 2.** Input `n = 4` and `edges = [[0,1],[1,2],[2,0],[3,0]]`, output true.

**Hint.** Which of the three states means the vertex lies on the route that is still open?

**Changed decision.** Edges have direction, so one boolean per vertex is no longer enough and the method uses three states.

#### [Boundary] Two-Way Undirected Edge (Author exercise)
<!-- id: gt-two-way-undirected-edge -->

**Prerequisites.** The Undirected Parent Check exercise.

**Problem.** An undirected graph has vertices `0..n-1` and a list `edges` that may contain the same pair of vertices more than once. A single edge appears in both neighbor lists, and the search must not mistake that return for a cycle. Two listed edges between the same two vertices form a cycle of two vertices, which follows the cycle definition of the lesson. Return true if the graph contains a cycle, counting two parallel edges as a cycle, and false otherwise.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`.
- **Self-loops** do not occur.
- **Parallel edges** may occur, and the pair `[a, b]` equals the pair `[b, a]`.
- **Return** is a boolean.

**Example 1.** Input `n = 2` and `edges = [[0,1]]`, output false.

**Example 2.** Input `n = 3` and `edges = [[0,1],[1,0],[1,2]]`, output true.

**Hint.** If two edges join the same pair, can the search tell them apart by the vertex number of the parent alone?

**Changed decision.** The parent is identified by the index of the edge used, not by the vertex number.

#### [Recognize] Course Schedule (LeetCode 207)
<!-- id: gt-course-schedule -->

**Prerequisites.** The Directed Three Colors exercise.

**Problem.** A student must take `numCourses` courses, numbered `0..numCourses-1`. Each entry `prerequisites[i] = [a, b]` states that course `b` must be completed before course `a`. Return true if the student can complete every course, and false otherwise. The answer is true exactly when the graph that has an edge from `b` to `a` for each entry contains no directed cycle.

**Constraints.** The limits are:
- **Courses** satisfy `1 <= numCourses <= 2000`.
- **Entries** satisfy `0 <= prerequisites.length <= 5000`.
- **Values** satisfy `a != b` and both lie in `0..numCourses-1`.
- **Uniqueness** holds, so no entry repeats.

**Example 1.** Input `numCourses = 3` and `prerequisites = [[1,0],[2,1],[2,0]]`, output true.

**Example 2.** Input `numCourses = 4` and `prerequisites = [[1,0],[2,1],[3,2],[1,3]]`, output false.

**Hint.** In which direction should the edge for the entry `[a, b]` point, and which exercise above then applies?

**Changed decision.** The statement hides the graph, so the method first builds the directed edges and then asks for the opposite answer, true when no cycle exists.
