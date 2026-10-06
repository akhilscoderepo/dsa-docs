<!-- lesson-kind: standard -->
<!-- lesson-id: visited-state -->
## Visited State

<!-- stage: context -->
### Why A Crawler Fetches Pages Twice

A link checker starts at one page and follows every link to find all pages reachable from it. The home page links to the about page, and the about page links back to the home page. A checker that remembers nothing follows that pair of links forever. A checker that remembers pages, but records a page too late, fetches the same page several times before the first fetch finishes.

Both failures come from one question: at which moment does the program record that it has claimed a vertex? This lesson answers it for breadth-first search (BFS) and depth-first search (DFS). The answer decides how much work the traversal does and how much memory it holds.

<!-- stage: naive -->
### Marking When A Vertex Leaves The Queue

Take a graph with five vertices numbered 0 to 4 and the undirected edges 0-1, 0-2, 1-3, 2-3 and 3-4. Vertex 3 has two paths from vertex 0, one through vertex 1 and one through vertex 2. The adjacency list is `adj`, and the vertex where the search starts is the source.

The natural first version of BFS keeps a boolean array `visited` and sets `visited[v]` when it takes `v` from the queue. It adds a neighbor to the queue only when `visited[w]` is still false.

```java
static int expansionsMarkAtDequeue(List<List<Integer>> adj, int source) {
    boolean[] visited = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(source);
    int expansions = 0;
    while (!queue.isEmpty()) {
        int v = queue.poll();
        visited[v] = true;                  // marked only after leaving the queue
        expansions++;
        for (int w : adj.get(v)) {
            if (!visited[w]) queue.add(w);  // vertex 3 passes this test twice
        }
    }
    return expansions;
}
```

The method finishes and reaches every vertex, so it looks correct. It returns 7 for the graph above, which has only 5 vertices.

<!-- stage: bottleneck -->
### Counting The Repeated Work

```predict
The method returns 7 expansions for 5 vertices. Which vertices does it expand twice, and how large can the waste grow?

Vertices 3 and 4 are each expanded twice, because vertex 3 enters the queue once from vertex 1 and once from vertex 2 before either copy leaves the queue. Every extra copy of vertex 3 adds a copy of vertex 4. On a graph where every vertex has an edge to every other vertex, the count grows far faster than the vertex count.
```

The method expands every entry that leaves the queue. Each expansion scans every neighbor of the vertex. A vertex that has k copies in the queue scans its neighbors k times and adds more copies of its neighbors. The copies multiply. On 10 vertices with an edge between every pair, the method performs 46 expansions. Marking at dequeue time therefore costs O(V) expansions in the best case and many more in dense graphs, and the queue holds those copies in memory.

The cause is a gap in time. A vertex sits in the queue after a neighbor discovers it and before it is dequeued. During that gap `visited` is still false, so a second neighbor discovers the same vertex again. The lesson closes that gap.

<!-- stage: insight -->
### Marking At The Moment Of Scheduling

The fix moves the mark to the moment the traversal decides to process a vertex. Call that moment scheduling. A vertex is scheduled once, and the mark must exist before any other vertex can schedule it again.

#### Marking In Breadth-First Search

BFS schedules a vertex when it adds the vertex to the queue. The queue is also called the frontier, because it holds vertices that the search has discovered and not yet expanded. The rule is to set `visited[w] = true` in the same step that adds `w`. The word enqueue names that addition. After that step, no later neighbor passes the test `!visited[w]`. Each vertex enters the frontier at most once, so the frontier never holds more than `n` entries in total.

<!-- names: frontier, enqueue, stack -->

#### Marking In Depth-First Search

DFS schedules a vertex when it enters the vertex. In the recursive form, entering means the start of the call, so the first statement of the call sets the mark. The call stack then holds the vertices on the current path. An iterative form uses an explicit stack, which is last in and first out. The stack can hold the same vertex twice if the mark is set only at entry. Section "Choosing The Mark Point" below explains when that is harmless.

#### Choosing The Mark Point

The mark point is a choice with two sound answers. Marking when pushing keeps every container free of duplicates, and it suits BFS, where the order of discovery already fixes the visit order. Marking at entry suits DFS when the exact depth-first order matters. A stale copy that reaches the top of the stack is then skipped by one test. A stale copy is harmless only because that test exists. Marking at dequeue in BFS has no such repair in the naive code above, so the copies expand.

<!-- stage: variables -->
### State Kept By A Traversal

A traversal needs four pieces of state, and each one has one job.

- **visited** is a `boolean[n]` where `visited[v]` is true once `v` is scheduled.
- **source** is the vertex where the search starts, and the traversal marks it before the loop.
- **frontier** is an `ArrayDeque<Integer>` that holds scheduled vertices that are not yet expanded.
- **count** is the number of marked vertices, and it equals the number of vertices reachable from the source.

A new `boolean[n]` holds `false` in every slot, so a traversal needs no filling loop. Every vertex that is never marked is not reachable from the source.

<!-- stage: trace -->
### Two Searches With Marks At Scheduling

#### Two Paths To The Same Vertex

The first trace uses the graph from the naive stage, with five vertices and the source 0. The cells are the vertex numbers, and the pointer `cur` marks the vertex that has just left the frontier. The variable `frontier` lists the vertices waiting after each step.

Vertex 0 schedules vertices 1 and 2. Vertex 1 schedules vertex 3. When vertex 2 expands, vertex 3 is already marked, so vertex 2 schedules nothing. That step removes the repeated entry that the naive method creates. Vertex 3 then schedules vertex 4, and the search ends with each vertex scheduled once.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"frontier":"[1,2]","marked":"[0,1,2]"},"note":"Vertex 0 leaves the frontier and marks its neighbors 1 and 2 as it adds them."},{"at":{"cur":1},"vars":{"frontier":"[2,3]","marked":"[0,1,2,3]"},"note":"Vertex 1 finds vertex 0 already marked and adds only vertex 3."},{"at":{"cur":2},"vars":{"frontier":"[3]","marked":"[0,1,2,3]"},"note":"Vertex 2 sees vertex 3 already marked, so it adds nothing and no repeated entry forms."},{"at":{"cur":3},"vars":{"frontier":"[4]","marked":"[0,1,2,3,4]"},"note":"Vertex 3 skips the marked vertices 1 and 2 and adds vertex 4."},{"at":{"cur":4},"vars":{"frontier":"[]","marked":"[0,1,2,3,4]"},"note":"Vertex 4 has no unmarked neighbor, so the frontier becomes empty."},{"at":{"cur":-1},"vars":{"frontier":"[]","marked":"[0,1,2,3,4]"},"note":"The frontier is empty and every vertex is marked, so each vertex was scheduled once."}]}
```

#### A Cycle And An Unreachable Vertex

The second trace uses five vertices and the directed edges 0 to 1, 1 to 2, 2 to 0 and 2 to 3, with the source 0. Vertex 4 has no edge that leads to it.

The edge from vertex 2 back to vertex 0 meets a marked vertex, so the cycle ends there. The trace finishes with an empty frontier, and vertex 4 was never marked. The unmarked cell is the correct answer, because no path from the source reaches vertex 4.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"frontier":"[1]","marked":"[0,1]"},"note":"Vertex 0 marks vertex 1 and adds it to the frontier."},{"at":{"cur":1},"vars":{"frontier":"[2]","marked":"[0,1,2]"},"note":"Vertex 1 reaches and marks vertex 2 and adds it to the frontier."},{"at":{"cur":2},"vars":{"frontier":"[3]","marked":"[0,1,2,3]"},"note":"Vertex 2 has an edge back to marked vertex 0, so the cycle stops there, and it adds vertex 3."},{"at":{"cur":3},"vars":{"frontier":"[]","marked":"[0,1,2,3]"},"note":"Vertex 3 has no outgoing edge, so nothing joins the frontier."},{"at":{"cur":-1},"vars":{"frontier":"[]","marked":"[0,1,2,3]"},"note":"The frontier is empty. Vertex 4 was never marked, because no edge leads to it from a marked vertex."}]}
```

<!-- stage: code -->
### A Traversal That Marks On Entry

#### Breadth-First Search With Early Marks

```java
static boolean[] reach(List<List<Integer>> adj, int source) {
    boolean[] visited = new boolean[adj.size()];
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    visited[source] = true;                     // the source is scheduled first
    queue.add(source);
    while (!queue.isEmpty()) {
        int v = queue.poll();                   // oldest scheduled vertex
        for (int w : adj.get(v)) {
            if (visited[w]) continue;           // already scheduled, skip
            visited[w] = true;                  // mark before the vertex waits
            queue.add(w);
        }
    }
    return visited;
}
```

The method returns the `visited` array, so the caller reads reachability from it. `ArrayDeque.add` appends at the tail and `poll` removes from the head, so the queue is first in and first out.

#### Cost Of The Traversal

- **Time** is O(V + E), because each vertex is scheduled once and each adjacency entry is read once.
- **Space** is O(V), because `visited` and the queue each hold at most V entries.

<!-- stage: applicability -->
### Deciding Where To Mark

#### Recognizing The Situation

Look for a graph where several paths can reach the same vertex. Undirected edges, cycles and shared descendants all create such paths. Any traversal on such input needs `visited`, and the first design question is the mark point.

#### The Invariant And Its False Friend

The invariant is that a vertex is marked at the moment it is scheduled, so it is scheduled at most once. A false friend of this rule is marking at dequeue, which looks tidy because the mark sits next to the work. It leaves a gap in which neighbors add the same vertex again. Tree BFS never shows the problem, because a tree has one path to each vertex.

#### Java Hazards

Test `visited[w]` before the push and not after the pop, unless the code also skips stale entries at entry. A recursive DFS needs one stack frame per vertex on the current path, so a path of 100,000 vertices calls for an explicit stack. Call `ArrayDeque.push` and `pop` for a stack and `add` and `poll` for a queue, and do not mix the two ends in one structure.

<!-- stage: exercises -->
### Exercises

#### [Build] Reachable Vertices (Author exercise)
<!-- id: gt-reachable-vertices -->

**Prerequisites.** The `visited` array and the BFS of this lesson.

**Problem.** The input describes an undirected graph on the vertices `0` to `n - 1`. The pair `edges[i] = [a, b]` states that vertices `a` and `b` share an edge. A vertex is reachable from `source` when some chain of edges leads from `source` to it, and `source` itself is reachable. Return every reachable vertex in increasing order.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= a, b < n` and `a != b`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Source** satisfies `0 <= source < n`.
- **Return** is an `int[]` in increasing order, and neither input changes.

**Example 1.** Input `n = 5`, `edges = [[0,1],[1,2],[3,4]]` and `source = 0`, output `[0,1,2]`.

**Example 2.** Input `n = 4`, `edges = [[2,1],[1,3],[3,2]]` and `source = 3`, output `[1,2,3]`.

**Hint.** Which array tells you, after the search ends, whether a vertex was reached?

**Changed decision.** Basic case: the result is read from `visited` and not from the order of discovery.

#### [Vary] Iterative DFS (Author exercise)
<!-- id: gt-iterative-dfs -->

**Prerequisites.** The previous exercise and the marking rule for DFS in this lesson.

**Problem.** The input is an undirected graph in the form of the previous exercise, with `n`, `edges` and `source`. For each vertex, the neighbors are scanned in increasing order of vertex number. The recursive DFS from `source` records a vertex when it enters the vertex, then enters each unrecorded neighbor in scan order. Return the recorded vertices in order. The method must not call itself.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= a, b < n` and `a != b`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Return** is an `int[]` of recorded vertices, and neither input changes.

**Example 1.** Input `n = 5`, `edges = [[0,2],[0,1],[1,3],[2,3],[3,4]]` and `source = 0`, output `[0,1,3,2,4]`.

**Example 2.** Input `n = 4`, `edges = [[3,2],[2,1]]` and `source = 3`, output `[3,2,1]`.

**Hint.** If the stack marks a vertex when it pushes the vertex, does the output order still match the recursive order?

**Changed decision.** The recursion becomes an explicit stack, and the mark moves from the push to the pop.

#### [Boundary] Cycle And Disconnected Vertex (Author exercise)
<!-- id: gt-cycle-disconnected-vertex -->

**Prerequisites.** The two exercises above.

**Problem.** A directed graph has `n` vertices numbered `0` to `n - 1`. Each entry `edges[i] = [from, to]` is an edge that leads from `from` to `to`. A vertex is reachable from `source` when a path that follows edge directions leads to it, and `source` is reachable. Return the vertices that are not reachable, in increasing order.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 10^5`.
- **Edges** satisfy `0 <= edges.length <= 2 * 10^5`.
- **Endpoints** satisfy `0 <= from, to < n`.
- **Self-loops** may occur, so `from` can equal `to`.
- **Repeats** may occur, so the same edge can appear more than once.
- **Return** is an `int[]`, empty when every vertex is reachable.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,2],[2,0]]` and `source = 0`, output `[3]`.

**Example 2.** Input `n = 3`, `edges = [[0,0],[1,2]]` and `source = 0`, output `[1,2]`.

**Hint.** The vertices 1 and 2 have an edge between them. Why does that edge not make them reachable?

**Changed decision.** The edges now have direction, and the answer lists the vertices whose `visited` value is still false.

#### [Recognize] Keys and Rooms (LeetCode 841)
<!-- id: gt-keys-and-rooms -->

**Prerequisites.** The `visited` array and the directed reachability of the previous exercise.

**Problem.** A building has `n` rooms numbered `0` to `n - 1`. Room 0 is open and every other room is locked. The list `rooms[i]` holds the keys inside room `i`, and key `k` opens room `k`. A visitor who enters a room takes all its keys at once. Return true if the visitor can enter every room.

**Constraints.** The limits are:
- **Rooms** satisfy `2 <= n <= 1000`.
- **Keys** satisfy `0 <= key < n` in every list.
- **Total** key count over all rooms is at most 3000.
- **Repeats** may occur, so a room can hold a key twice or a key to its own door.
- **Return** is a `boolean`, and `rooms` does not change.

**Example 1.** Input `rooms = [[2],[],[1,0]]`, output true.

**Example 2.** Input `rooms = [[1],[0],[3],[2]]`, output false.

**Hint.** What are the vertices, and what does a key correspond to?

**Changed decision.** The graph has no edge array, so each key list is the adjacency list and the test compares a count with `n`.
