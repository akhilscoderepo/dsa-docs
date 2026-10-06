<!-- lesson-kind: standard -->
<!-- lesson-id: dfs-topological-state -->
## DFS Topological State

<!-- stage: context -->
### Checking Dependencies With Recursion

A package installer resolves dependencies with a recursive function. Package `web` needs `core` and `api`, and `api` also needs `core`. The installer visits `web`, then `api`, then `core`, and later returns to `web` and meets `core` a second time. A checker that treats every second meeting as a loop reports an error for this project, although nothing is wrong. The installer then refuses to install a valid project. A different project, where `core` needs `api` and `api` needs `core`, must produce the error. Both projects meet some package twice, so the checker needs one more fact than a single "seen before" answer.

Model the packages as vertices and each dependency as a directed edge. The task is to decide whether the edges contain a directed cycle, and to list the vertices in a topological order when no cycle exists. A topological order places every vertex after all vertices that point to it. The previous lesson built one with Kahn's method, which repeatedly places a vertex without unplaced predecessors.

This lesson asks what a recursive search must remember about a vertex, so that only a real cycle raises the error.

<!-- stage: naive -->
### Marking Each Vertex As Seen

The first attempt keeps one flag for each vertex. The search sets the flag on entry. It reports a cycle when it reaches a vertex whose flag is already set.

```java
static boolean seenTwice(List<List<Integer>> adj, boolean[] seen, int cur) {
    seen[cur] = true;
    for (int next : adj.get(cur)) {
        if (seen[next]) return true;
        if (seenTwice(adj, seen, next)) return true;
    }
    return false;
}
```

The caller starts the method from every vertex whose flag is still false. The method finds every real cycle, because a cycle always leads the search back to a vertex that it entered earlier. The question is whether it finds only real cycles.

```predict
Take the edges 0 to 1, 0 to 2, 1 to 3 and 2 to 3, which contain no cycle. What does seenTwice return from vertex 0?

It returns true, which is wrong. The search enters 0, then 1, then 3, and 3 has no outgoing edge. It returns to 0 and enters 2. The edge from 2 to 3 reaches a vertex with the flag set, so the method reports a cycle. Vertex 3 is finished and cannot lead back to 2, but the single flag cannot express that difference.
```

<!-- stage: bottleneck -->
### One Flag Cannot Separate Two Cases

The method visits each vertex once and reads each edge once, so its cost is O(V + E), and the cost is not the problem. The problem is the answer. A set flag covers two different situations. In the first, the vertex is still on the chain of calls that leads to the current vertex, so an edge to it closes a cycle. In the second, the vertex is finished and every path from it has been explored, so an edge to it only joins two routes.

The diamond graph shows the second situation, and it appears in most real dependency graphs, because shared modules are normal. Without the distinction, the method reports false cycles on correct input. It also produces no order. The flag records that a vertex was reached, but it does not record when the vertex was finished, and an order needs exactly that moment.

A correct method must store a second piece of information for each vertex and keep the cost at O(V + E). The next stage describes the states and the moment that yields the order.

<!-- stage: insight -->
### Three States Replace One Flag

Each vertex needs one of three states, and the position in the search decides which one it has.

<!-- names: gray, black, postorder -->

#### The Three States

White means unvisited: the search has not entered the vertex. A vertex becomes **gray**, meaning active, at entry and stays gray while its recursive call waits on the stack. It becomes **black**, meaning complete, when that call returns, and then every vertex reachable from it is finished. An `int[]` stores the state. Each vertex changes state twice, first from white to gray and later from gray to black.

#### Which Edge Proves A Cycle

When the search scans an edge from `u` to `v`, the state of `v` decides what happens. A white `v` starts a recursive call. A black `v` is skipped, because it is finished and cannot reach `u`. A gray `v` is an ancestor of `u` on the call stack, and the stack path from `v` to `u` plus the edge from `u` to `v` forms a cycle. Only the gray case proves a cycle. This is the case that the single flag could not separate from the black case.

#### Recording The Finish Order

The **postorder** is the list of vertices in the order in which their calls return. The search appends `u` when `u` turns black, which is after the loop over its outgoing edges ends. At that point each successor `v` has returned, either in a call that `u` started or in earlier work. So `v` precedes `u` in the list.

#### Why Reversal Gives An Order

When every edge points from a later list position to an earlier one, reading the list backward makes every edge point forward. The reversed postorder is a valid order when no gray edge occurs. The invariant is that every gray vertex lies on the current call stack, and every black vertex has all its successors black and already in the list. A gray edge is the only way to break the second half, so its absence proves the order correct.

<!-- stage: variables -->
### What The Search Keeps

The search reads `n` and `edges` and changes neither. It builds `adj` as in the earlier lesson of this chapter, with neighbors in the order of the edges. Three structures hold the state.

- **color** is an `int[]` of length `n`; 0 means white, 1 means gray and 2 means black.
- **post** is a `List<Integer>` that receives each vertex when its call returns.
- **cur** is the vertex of the call that is running, and its neighbors are scanned in list order.

The call stack itself holds the gray vertices, with the entry order from bottom to top.

<!-- stage: trace -->
### Entering And Leaving Vertices On Two Graphs

#### A Graph With A Cross Edge

The first graph has the edges 0 to 1, 0 to 2, 1 to 3, 2 to 3 and 4 to 2. The search starts at vertex 0 and later at vertex 4, because that vertex is still white after the first call returns. Each cell holds a vertex id, and the pointer `cur` marks the vertex of the event. The variable `color` lists the states of vertices 0 to 4 as the letters W, G and B, and `post` lists the vertices that returned so far. Two steps matter most. At step 7 the search scans the edge from 2 to 3 and finds 3 black, so it skips the edge. At step 11 the edge from 4 to 2 meets a black vertex as well.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"color":"GWWWW","post":"empty"},"note":"The search enters vertex 0 and turns it gray."},{"at":{"cur":1},"vars":{"color":"GGWWW","post":"empty"},"note":"The search enters vertex 1 and turns it gray."},{"at":{"cur":3},"vars":{"color":"GGWGW","post":"empty"},"note":"The search enters vertex 3 and turns it gray."},{"at":{"cur":3},"vars":{"color":"GGWBW","post":"3"},"note":"All edges of vertex 3 are scanned, so it turns black and joins the postorder."},{"at":{"cur":1},"vars":{"color":"GBWBW","post":"3-1"},"note":"All edges of vertex 1 are scanned, so it turns black and joins the postorder."},{"at":{"cur":2},"vars":{"color":"GBGBW","post":"3-1"},"note":"The search enters vertex 2 and turns it gray."},{"at":{"cur":2},"vars":{"color":"GBGBW","post":"3-1"},"note":"The edge from 2 to 3 reaches a black vertex, so the search skips it."},{"at":{"cur":2},"vars":{"color":"GBBBW","post":"3-1-2"},"note":"All edges of vertex 2 are scanned, so it turns black and joins the postorder."},{"at":{"cur":0},"vars":{"color":"BBBBW","post":"3-1-2-0"},"note":"All edges of vertex 0 are scanned, so it turns black and joins the postorder."},{"at":{"cur":4},"vars":{"color":"BBBBG","post":"3-1-2-0"},"note":"The search enters vertex 4 and turns it gray."},{"at":{"cur":4},"vars":{"color":"BBBBG","post":"3-1-2-0"},"note":"The edge from 4 to 2 reaches a black vertex, so the search skips it."},{"at":{"cur":4},"vars":{"color":"BBBBB","post":"3-1-2-0-4"},"note":"All edges of vertex 4 are scanned, so it turns black and joins the postorder."}]}
```

#### A Graph With A Real Cycle

The second graph has the edges 0 to 1, 1 to 2, 2 to 3 and 3 to 1. The search enters 0, 1, 2 and 3 in a chain, so all four are gray. Vertex 3 then scans its edge to vertex 1 and finds a gray vertex. Vertex 0 is gray as well, but it does not lie on the cycle, and the method reports the edge from 3 to 1.

```trace
{"cells":[0,1,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"color":"GWWW","post":"empty"},"note":"The search enters vertex 0 and turns it gray."},{"at":{"cur":1},"vars":{"color":"GGWW","post":"empty"},"note":"The search enters vertex 1 and turns it gray."},{"at":{"cur":2},"vars":{"color":"GGGW","post":"empty"},"note":"The search enters vertex 2 and turns it gray."},{"at":{"cur":3},"vars":{"color":"GGGG","post":"empty"},"note":"The search enters vertex 3 and turns it gray."},{"at":{"cur":3},"vars":{"color":"GGGG","post":"empty"},"note":"The edge from 3 to 1 reaches a gray vertex, so it closes a cycle and the method reports the pair 3 and 1."}]}
```

<!-- stage: code -->
### Depth-First Order With Three States

The helper returns true as soon as it meets a gray vertex. The wrapper returns the reversed postorder, or an empty array when the helper reports a cycle.

```java
static boolean visit(List<List<Integer>> adj, int[] color, List<Integer> post, int cur) {
    color[cur] = 1;
    for (int next : adj.get(cur)) {
        if (color[next] == 1) return true;
        if (color[next] == 0 && visit(adj, color, post, next)) return true;
    }
    color[cur] = 2;
    post.add(cur);
    return false;
}

static int[] dfsOrder(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) adj.get(e[0]).add(e[1]);
    int[] color = new int[n];
    List<Integer> post = new ArrayList<>();
    for (int v = 0; v < n; v++) {
        if (color[v] == 0 && visit(adj, color, post, v)) return new int[0];
    }
    int[] order = new int[n];
    for (int i = 0; i < n; i++) order[i] = post.get(n - 1 - i);
    return order;
}
```

The order of the two tests in the loop matters. A gray neighbor must return before any recursion, and a black neighbor must be skipped without a call. The method runs in O(V + E) time. It uses O(V + E) memory, which includes a stack of up to V calls. A chain of 100000 vertices exceeds the default Java thread stack, so large inputs need an explicit stack or a thread with a larger stack size.

<!-- stage: applicability -->
### Recognizing Depth-First Cycle Problems

#### Reading The Cue

Use three states when the statement asks whether a directed structure contains a cycle, or asks for an order and wants the offending edge or chain when none exists. Statements about deadlock between locks, import loops or cyclic references in a configuration have this shape. The same search also fits when the answer needs the finishing time of each vertex.

#### Checking The Invariant

The invariant is that gray vertices form one chain on the call stack, and black vertices are completely explored. It holds only when the method sets gray before the loop and sets black after the loop, and never in another place. Moving the black assignment into the loop makes a vertex black while its other edges are still unexplored. Test a self loop, which must end in the gray branch at once.

#### Avoiding The False Friend

The false friend is the single seen flag, or the rule from undirected graphs that a seen neighbor other than the parent closes a cycle. Directed edges break that rule, because a seen neighbor can be a finished vertex. The diamond graph is the smallest counterexample. A second false friend is to read the reversed postorder as an order without first checking for a gray edge. When a cycle exists, the list still has V entries, but some edge points backward.

<!-- stage: exercises -->
### Exercises

#### [Build] Three-Color Trace (Author exercise)
<!-- id: dg-three-color-trace -->

**Prerequisites.** The three states of this lesson.

**Problem.** Consider the vertices `0` to `n - 1` and the list `edges`, where each entry `[a, b]` is a directed edge from `a` to `b`. Run a depth-first search that starts a new tree at every white vertex in ascending order and scans the neighbors of a vertex in the order of `edges`. A counter `clock` starts at 0. A vertex receives `enter = clock` and then `clock` rises by 1 when the search makes it gray. It receives `exit = clock` and `clock` rises by 1 again when it turns black. Return an `int[][]` named `times` where `times[v] = {enter, exit}`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Cycles** may occur, and the search skips an edge to a gray vertex.
- **Result** has `2n` distinct values, which are exactly `0..2n-1`.

**Example 1.** Input `n = 4`, `edges = [[0,1],[0,2],[1,3],[2,3]]`, output `[[0,7],[1,4],[5,6],[2,3]]`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[1,2],[2,0]]`, output `[[0,5],[1,4],[2,3]]`.

**Hint.** At which two moments does a vertex change its state, and which moment advances the clock?

**Changed decision.** The method records `enter` when the vertex turns gray and `exit` when it turns black, and it reads a gray neighbor without recursing.

#### [Vary] Postorder Topological List (Author exercise)
<!-- id: dg-postorder-list -->

**Prerequisites.** The exercise above.

**Problem.** A directed acyclic graph on the vertices `0` to `n - 1` is given by `edges`, where `[a, b]` is an edge from `a` to `b`. Run the depth-first search of the first exercise, starting new trees in ascending order and scanning neighbors in edge order. Append a vertex to a list when it turns black. Return the reverse of that list as an `int[]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats may occur.
- **Acyclic** input is guaranteed, so no self loop occurs.
- **Result** has length `n` and contains every vertex once.

**Example 1.** Input `n = 5`, `edges = [[4,3],[2,1],[1,0]]`, output `[4,3,2,1,0]`.

**Example 2.** Input `n = 4`, `edges = [[0,1],[0,2],[1,3],[2,3]]`, output `[0,2,1,3]`.

**Hint.** Which moment places a vertex into the list, and what must already be true of its successors at that moment?

**Changed decision.** The method appends a vertex only after the loop over its outgoing edges ends, and it reads the finished list from the back.

#### [Boundary] Cross Edge To Black (Author exercise)
<!-- id: dg-cross-edge-black -->

**Prerequisites.** The two exercises above.

**Problem.** A directed graph has `n` vertices numbered from 0, and `edges` lists its edges as pairs `[a, b]` that run from `a` to `b`. Run the depth-first search of the first exercise. Every time the search scans an entry of `edges` it looks at the state of the end vertex. Return an `int[]` of length 2 that holds the number of scans that find a black vertex and the number of scans that find a gray vertex. Scans that find a white vertex start a recursive call and count in neither entry.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Self loop** scans find a gray vertex, because the start vertex is gray.
- **Result** is `{black, gray}`.

**Example 1.** Input `n = 4`, `edges = [[0,1],[0,2],[1,3],[2,3]]`, output `[1,0]`.

**Example 2.** Input `n = 4`, `edges = [[0,1],[1,2],[2,1],[0,2],[3,0]]`, output `[2,1]`.

**Hint.** When the edge from 2 to 3 is scanned in the first example, has the call of vertex 3 returned already?

**Changed decision.** The method accepts a black end vertex without any action, and it counts a gray end vertex as the only evidence of a cycle.

#### [Recognize] Course Order With The Blocking Edge (LeetCode 210)
<!-- id: dg-course-order-edge -->

**Prerequisites.** All three exercises above.

**Problem.** A catalog holds `numCourses` courses with ids `0` to `numCourses - 1`. An entry `[a, b]` of `prerequisites` means that course `b` comes earlier than course `a`, which gives the edge from `b` to `a`. Run a depth-first search that starts new trees in ascending order and scans the followers of a course in the order of the entries. Return an `int[][]` with two rows. Row 0 is the reversed postorder when no cycle exists, and it is empty otherwise. Row 1 is empty when no cycle exists. Otherwise it holds `{u, v}` for the first scan that reaches a gray vertex `v` from the vertex `u`.

**Constraints.** The limits are:
- **Courses** satisfy `1 <= numCourses <= 2000`.
- **Entries** satisfy `0 <= prerequisites.length <= 5000`, with values in `0..numCourses-1`.
- **Self entries** such as `[a, a]` may occur and give the pair `{a, a}`.
- **Result** has exactly one nonempty row.

**Example 1.** Input `numCourses = 5`, `prerequisites = [[1,3],[0,1],[2,3],[4,0]]`, output `[[3,2,1,0,4],[]]`.

**Example 2.** Input `numCourses = 4`, `prerequisites = [[1,0],[2,1],[3,2],[1,3]]`, output `[[],[3,1]]`.

**Hint.** Which of the courses on the call stack at the moment of detection lie on the cycle, and which do not?

**Changed decision.** The method stops at the first gray end vertex and returns the pair of scanned edge ends, and otherwise it reads the postorder from the back.
