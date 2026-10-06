<!-- lesson-kind: standard -->
<!-- lesson-id: kahn-topological-order -->
## Kahn Topological Order

<!-- stage: context -->
### Compiling Modules In Dependency Order

A build tool must compile a project with six modules. Module `app` imports `net`, `net` imports `util`, and `app` also imports `log`. The compiler fails on any module whose imports are not compiled yet. Compiling in alphabetical order puts `app` first and fails at once. Sorting by name, by file size or by any other label cannot respect arbitrary imports. The tool needs an order in which every module appears after all modules it imports. In some projects two modules import each other, and then no such order exists. The tool must report that case instead of looping forever.

Model the modules as vertices and each import as a directed edge from the imported module to the importing module. The task is to return a list of all vertices in which every edge points forward, or to report that the edges contain a cycle.

This lesson asks how a program finds such an order, and how it notices that none exists.

<!-- stage: naive -->
### Scanning For A Module That Can Go

The first attempt repeats one question. It looks for any unplaced vertex whose incoming edges all start at placed vertices, places that vertex and starts over.

```java
static int[] scanOrder(int n, int[][] edges) {
    boolean[] placed = new boolean[n];
    int[] order = new int[n];
    int count = 0;
    while (count < n) {
        int pick = -1;
        for (int v = 0; v < n && pick < 0; v++) {
            if (placed[v]) continue;
            boolean free = true;
            for (int[] e : edges) {
                if (e[1] == v && !placed[e[0]]) free = false;
            }
            if (free) pick = v;
        }
        if (pick < 0) return new int[0];
        placed[pick] = true;
        order[count++] = pick;
    }
    return order;
}
```

The method is correct. Every placed vertex has all its predecessors placed before it, and an empty result means that every unplaced vertex still waits for another unplaced vertex.

```predict
Take a chain of V vertices with V - 1 edges, where the labels run against the edge direction. How many edge reads does the method perform, as a function of V?

The method makes V rounds. In round k the scan tests about V - k vertices before it meets the free one, and each test reads all V - 1 edges. The total is on the order of V times V times V, so a chain of 2000 modules needs billions of reads. Almost all of them repeat a fact that an earlier round already read.
```

<!-- stage: bottleneck -->
### Recounting The Same Dependencies

The method places V vertices, and each placement scans up to V candidates against all E edges. The running time is O(V · V · E), which is O(V³) on a chain. An adjacency list removes one factor. The time is still O(V · (V + E)), because every round re-tests vertices that stayed blocked in the previous round.

The waste has a clear source. Whether vertex `v` is free depends only on how many of its incoming edges start at unplaced vertices. That number changes only at the placement of one of those predecessors. The scan recomputes it from scratch in every round, for every vertex, although it changes by one at most for each placement.

A faster method stores that number for each vertex. It updates the number only at the placement of a predecessor. It also needs a way to find a free vertex without scanning. The next stage names both pieces. The target is O(V + E) time, with one visit per vertex and one visit per edge.

<!-- stage: insight -->
### Counting Unplaced Predecessors Per Vertex

Free vertices can be found immediately, if each vertex carries a counter that tells how many predecessors still wait.

<!-- names: indegree, decrement, removal -->

#### What The Counter Holds

The **indegree** of a vertex is the number of edges that end at it. Here it also means the number of predecessors that are not placed yet, because an edge from a placed vertex no longer counts. A vertex with indegree 0 has no waiting predecessor, so placing it next never breaks an edge. One pass over the edge list computes all indegrees, and parallel edges count once each.

#### Taking A Vertex Out Of The Graph

The **removal** of a vertex means placing it next in the output and forgetting its outgoing edges. The program implements this with one **decrement** for each outgoing edge. The end vertex of that edge loses one waiting predecessor, so its indegree drops by one. When a decrement brings an indegree to 0, that vertex becomes available at that moment and joins the queue.

#### Why A Queue Is Enough

The queue holds exactly the vertices that are available now and not yet placed. Each vertex enters the queue once, at the instant its indegree reaches 0, so the program never scans for a free vertex. Starting the queue requires every vertex whose indegree is 0 before any removal, and there can be several of them, including vertices without any edge.

#### Detecting A Cycle

The invariant has two parts. Every vertex in the output had indegree 0 at its removal. Every vertex in the queue has indegree 0 now. A vertex on a cycle waits for another vertex of the cycle, so its indegree never falls to 0. The loop then ends with fewer than V vertices in the output. That shortfall is the exact test for a cycle.

<!-- stage: variables -->
### What The Method Keeps

The method reads `n` and `edges`, and it never changes either of them. The method builds an adjacency list `adj` from `edges`. The call `adj.get(u)` returns the end vertices of the edges that start at `u`. Five names carry the state of the loop.

- **indeg** is an `int[]` of length `n`; entry `v` counts incoming edges of `v` whose start is not removed yet.
- **queue** is an `ArrayDeque<Integer>` that holds the vertices with `indeg` 0 that wait for removal.
- **order** is an `int[]` of length `n`, filled from index 0 in removal order.
- **count** is an int that starts at 0 and equals the number of vertices removed so far.
- **cur** is the vertex that the current iteration took from the queue.

<!-- stage: trace -->
### Removing Vertices On Two Graphs

#### A Graph With Three Sources

The first graph has six vertices and the edges 0 to 2, 1 to 2, 2 to 3, 1 to 4 and 4 to 3. Vertex 5 has no edge. The indegrees at the start are 0, 0, 2, 2, 1 and 0, so vertices 0, 1 and 5 enter the queue before the loop begins. Each cell holds a vertex id, and the pointer `cur` marks the vertex that the loop just removed. The variable `indeg` shows the counters after that removal, `queue` shows the waiting vertices and `order` shows the output so far. Vertex 2 enters the queue only after both of its predecessors, 0 and 1, are gone. Vertex 3 enters after vertices 2 and 4 are gone.

```trace
{"cells": [0, 1, 2, 3, 4, 5], "pointers": ["cur"], "steps": [{"at": {"cur": 0}, "vars": {"indeg": "0,0,1,2,1,0", "queue": "1-5", "order": "0"}, "note": "The loop removes vertex 0, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 1}, "vars": {"indeg": "0,0,0,2,0,0", "queue": "5-2-4", "order": "0-1"}, "note": "The loop removes vertex 1, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 5}, "vars": {"indeg": "0,0,0,2,0,0", "queue": "2-4", "order": "0-1-5"}, "note": "The loop removes vertex 5, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 2}, "vars": {"indeg": "0,0,0,1,0,0", "queue": "4", "order": "0-1-5-2"}, "note": "The loop removes vertex 2, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 4}, "vars": {"indeg": "0,0,0,0,0,0", "queue": "3", "order": "0-1-5-2-4"}, "note": "The loop removes vertex 4, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 3}, "vars": {"indeg": "0,0,0,0,0,0", "queue": "empty", "order": "0-1-5-2-4-3"}, "note": "The loop removes vertex 3, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 3}, "vars": {"indeg": "0,0,0,0,0,0", "queue": "empty", "order": "0-1-5-2-4-3"}, "note": "The queue is empty and count equals n = 6, so the method returns the order."}]}
```

#### A Graph That Contains A Cycle

The second graph has five vertices and the edges 0 to 1, 1 to 2, 2 to 1, 2 to 3 and 4 to 3. Vertices 1 and 2 form a cycle. Only vertices 0 and 4 start with indegree 0. Removing them lowers the counters of vertices 1 and 3 by one each, and neither falls to 0. The queue is empty after two removals, and the final step compares `count` with `n`.

```trace
{"cells": [0, 1, 2, 3, 4], "pointers": ["cur"], "steps": [{"at": {"cur": 0}, "vars": {"indeg": "0,1,1,2,0", "queue": "4", "order": "0"}, "note": "The loop removes vertex 0, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 4}, "vars": {"indeg": "0,1,1,1,0", "queue": "empty", "order": "0-4"}, "note": "The loop removes vertex 4, lowers its followers' counters and queues those that reach 0."}, {"at": {"cur": 4}, "vars": {"indeg": "0,1,1,1,0", "queue": "empty", "order": "0-4"}, "note": "The queue is empty and count is 2 while n is 5, so a cycle blocks the other vertices and the method returns an empty array."}]}
```

<!-- stage: code -->
### Kahn Order With A Counter Array

The method returns a full order, or an empty array when a cycle blocks some vertices.

```java
static int[] kahnOrder(int n, int[][] edges) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] e : edges) {
        adj.get(e[0]).add(e[1]);
        indeg[e[1]]++;
    }
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    for (int v = 0; v < n; v++) {
        if (indeg[v] == 0) queue.add(v);
    }
    int[] order = new int[n];
    int count = 0;
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        order[count++] = cur;
        for (int next : adj.get(cur)) {
            if (--indeg[next] == 0) queue.add(next);
        }
    }
    return count == n ? order : new int[0];
}
```

The counters are a local array, so the caller's `edges` stays unchanged. The test `--indeg[next] == 0` decrements first and compares the new value, which makes each vertex enter the queue exactly once. A repeated edge raises the counter twice and lowers it twice, so duplicates need no special case. The method runs in O(V + E) time and keeps O(V + E) memory in `adj`, `indeg`, the queue and `order`.

<!-- stage: applicability -->
### Recognizing Order Problems On Directed Graphs

#### Reading The Cue

Use this method when the statement says that some items must come before others. Typical statements mention prerequisites, build steps, task dependencies or a schedule in which no step starts early. A request for any valid order, or for a yes or no answer about whether one exists, points to the same loop. Questions that ask for the order with the smallest labels, or for the number of rounds, need a small change to the queue and keep the counters.

#### Checking The Invariant

The invariant is that the queue holds exactly the unremoved vertices whose indegree is 0. It holds only when the method counts every edge once at the start and decrements it once at its removal. A vertex that enters the queue twice breaks the final comparison of `count` with `n`. An edge that the method decrements twice does the same. Every graph with a cycle must end with `count < n`, so test one before trusting the loop.

#### Avoiding The False Friend

The false friend is sorting by label, by degree or by any property of a single vertex. Such a sort looks at one vertex at a time, and a valid order depends on pairs of vertices. A second false friend is an undirected degree count. It ignores edge direction, so it cannot tell a predecessor from a successor. A graph with a single directed edge shows the failure, because both endpoints have degree 1 and only one of them can go first.

<!-- stage: exercises -->
### Exercises

#### [Build] Compute Indegrees (Author exercise)
<!-- id: dg-compute-indegrees -->

**Prerequisites.** The adjacency and edge-list idea of this lesson.

**Problem.** A directed graph has vertices `0` to `n - 1`, and each entry `[a, b]` of `edges` is one directed edge from `a` to `b`. The indegree of a vertex `v` is the number of entries of `edges` whose second value equals `v`. Return an `int[]` named `indegree` of length `n` where `indegree[v]` is the indegree of `v`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Repeats** may occur: the same pair can appear twice, and each copy counts.
- **Self loops** may occur, and `[v, v]` adds 1 to `indegree[v]`.

**Example 1.** Input `n = 5`, `edges = [[0,1],[0,2],[1,2],[3,2],[2,4]]`, output `[0,1,3,0,1]`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[0,1],[2,2]]`, output `[0,2,1]`.

**Hint.** Which value of each entry decides the position that receives the increment?

**Changed decision.** The method adds 1 at the end vertex of every edge, and it never groups edges by their start vertex.

#### [Vary] Can All Courses Finish (LeetCode 207)
<!-- id: dg-course-schedule -->

**Prerequisites.** The exercise above.

**Problem.** There are `numCourses` courses numbered `0` to `numCourses - 1`. Each entry `[a, b]` of `prerequisites` states that course `b` needs completion before course `a`. Return `true` if some order completes all courses while respecting every entry, and return `false` otherwise.

**Constraints.** The limits are:
- **Courses** satisfy `1 <= numCourses <= 2000`.
- **Entries** satisfy `0 <= prerequisites.length <= 5000`.
- **Values** of each entry lie in `0..numCourses-1`.
- **Self entries** such as `[a, a]` may occur, and they make the answer `false`.

**Example 1.** Input `numCourses = 4`, `prerequisites = [[1,0],[2,1],[3,1],[3,2]]`, output `true`.

**Example 2.** Input `numCourses = 3`, `prerequisites = [[1,0],[2,1],[1,2]]`, output `false`.

**Hint.** What does the number of removed vertices equal when every course can finish?

**Changed decision.** The method returns only whether `count` equals `numCourses` and builds no order.

#### [Boundary] Several Initial Sources (Author exercise)
<!-- id: dg-several-sources -->

**Prerequisites.** The two exercises above.

**Problem.** A directed graph on the vertices `0` to `n - 1` comes from `edges`, where `[a, b]` is an edge from `a` to `b`. Remove vertices in rounds. Round 1 removes every vertex whose indegree is 0. Each later round removes every vertex whose indegree is 0 after all earlier rounds. Return an `int[][]` named `rounds` where row `k` lists the vertices of round `k + 1` in ascending order. Vertices that no round removes appear in no row.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`, with repeats and self loops allowed.
- **Isolated** vertices have no edge, and they belong to round 1.
- **Result** is empty when no vertex has indegree 0 at the start.

**Example 1.** Input `n = 6`, `edges = [[0,2],[1,2],[2,3],[1,4],[4,3]]`, output `[[0,1,5],[2,4],[3]]`.

**Example 2.** Input `n = 4`, `edges = [[1,2],[2,1]]`, output `[[0,3]]`.

**Hint.** Which vertices must the queue contain before the first removal, and does a vertex without any edge belong there?

**Changed decision.** The method starts the queue with every vertex of indegree 0 and removes it one whole round at a time, in ascending order.

#### [Recognize] Course Schedule With An Order (LeetCode 210)
<!-- id: dg-course-order -->

**Prerequisites.** All three exercises above.

**Problem.** A catalog holds `numCourses` courses with ids `0` to `numCourses - 1`, and every entry `[a, b]` of `prerequisites` requires course `b` earlier than course `a` in a list. Return an `int[]` that lists all courses and satisfies every entry. Return an empty array when no such list exists. To make the answer unique, the queue starts with the courses of indegree 0 in ascending order. A course's followers follow the order of the entries.

**Constraints.** The limits are:
- **Courses** satisfy `1 <= numCourses <= 2000`.
- **Entries** satisfy `0 <= prerequisites.length <= 5000`, and values lie in `0..numCourses-1`.
- **Queue** is first in, first out.
- **Result** has length `numCourses`, or length 0 when a cycle exists.

**Example 1.** Input `numCourses = 5`, `prerequisites = [[3,4],[1,2],[0,1]]`, output `[2,4,1,3,0]`.

**Example 2.** Input `numCourses = 3`, `prerequisites = [[1,0],[0,1]]`, output `[]`.

**Hint.** Which counter comparison separates a complete order from a partial one, and where does the isolated course 2 of the second example fit?

**Changed decision.** The method records each removed course in an array and returns it only when its length equals `numCourses`.
