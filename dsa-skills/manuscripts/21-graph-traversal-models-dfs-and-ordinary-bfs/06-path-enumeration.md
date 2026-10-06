<!-- lesson-kind: standard -->
<!-- lesson-id: path-enumeration -->
## Path Enumeration

<!-- stage: context -->
### Listing Every Chain Of Tasks

A job scheduler runs tasks that depend on each other. Task 0 checks out the code and task 4 deploys it. A release engineer asks for every chain of tasks that leads from task 0 to task 4, so that each chain can be timed separately. A yes or no answer to "can task 0 reach task 4" does not help here, because the engineer needs the chains themselves.

Model the tasks as a graph. Each task is a vertex, and each dependency is a directed edge, an edge that can be followed in one direction only. A **path** is a sequence of vertices in which each consecutive pair is joined by an edge. A **DAG** is a directed graph with no cycle, so no path leads from a vertex back to itself. Task graphs are DAGs, because a task cannot depend on its own result.

The question of this lesson is how a depth-first search can output every path from a source to a target, and not only decide whether one exists.

<!-- stage: naive -->
### Reusing One Visited Array

The earlier lessons of this chapter taught the standard depth-first search with a `visited` array that is set once and never cleared. That rule guarantees that every vertex is expanded once. The first attempt at listing paths keeps the rule and records the current chain whenever the search reaches the target.

```java
static void listPaths(List<List<Integer>> adj, int cur, int target,
                      boolean[] visited, List<Integer> chain, List<List<Integer>> found) {
    visited[cur] = true;
    chain.add(cur);
    if (cur == target) {
        found.add(new ArrayList<>(chain));
    } else {
        for (int next : adj.get(cur)) {
            if (!visited[next]) listPaths(adj, next, target, visited, chain, found);
        }
    }
    chain.remove(chain.size() - 1);
}
```

Take the graph with vertices 0 to 3 and edges 0 to 1, 0 to 2, 1 to 3 and 2 to 3. There are two paths from 0 to 3, namely 0, 1, 3 and 0, 2, 3.

```predict
How many paths does listPaths report for source 0 and target 3 on this graph, and which vertex causes the loss?

It reports one path, 0, 1, 3. The search marks vertex 3 visited on the first path and never clears it, so the branch through vertex 2 sees 3 as visited and skips the edge 2 to 3.
```

<!-- stage: bottleneck -->
### Visited State Blocks Valid Paths

The loss is a logic error, not a speed problem. The `visited` array answers "has this vertex been reached by any branch so far", but a path listing needs a different question: "does this vertex already appear in the chain that is being built". Two different paths may share the vertex 3, and both are valid answers.

Fixing the rule exposes the true cost. A DAG with a source, `k` layers of two vertices each, and a target has `2k + 2` vertices. Every vertex of one layer has an edge to both vertices of the next layer. This graph has `2^k` paths from source to target. The output alone has an exponential size, so any correct method takes at least O(2^(n/2)) time for `n = 2k + 2` vertices, and no trick can avoid it.

The remaining task is to keep the cost proportional to the output. The method may spend O(n) per recorded path to copy it, which is O(P * n) for `P` paths, plus the work of dead branches. It must not spend more by recomputing chains from scratch. The next stage gives the rule that achieves this.

<!-- stage: insight -->
### Keeping The Current Chain Only

The fix replaces the global rule with a local one. Each recursive call owns one position in the chain from the source to the current vertex.

#### One List For The Current Chain

The **working path** is a single list that holds exactly the vertices on the current recursion chain, from the source down to the vertex being expanded. A call appends its vertex on entry. It then loops over the neighbors and recurses into each one. When the loop ends, the call removes its own vertex, which is the last element. This removal is the **restore** step. After it, the list equals the working path of the caller, so the next neighbor of the caller starts from the correct chain.

<!-- names: working path, restore, snapshot -->

#### Copying At The Target

When the call reaches the target, the working path is a complete answer. The list keeps changing afterwards, so the method must store a **snapshot**, a separate copy of the list taken at that moment. Storing the list itself would make every stored answer point to one object that ends empty.

#### Why A DAG Needs No Visited Array

A path that repeats a vertex needs a cycle. A DAG has none, so a call can never meet a vertex that is already on the working path. The check that the naive code used is therefore not only wrong but also unnecessary. The invariant is that, at every call, the working path is exactly the chain of active calls, and a vertex appears in it at most once.

<!-- stage: variables -->
### What The Search Keeps

The search needs four items, and one of them changes on every call.

- **adj** is the adjacency list; `adj.get(v)` holds the neighbors of `v` in the order of the edges.
- **path** is the working path, a list that grows on entry and shrinks on exit.
- **found** is the list of snapshots, one per path that reaches the target.
- **target** is the vertex that ends a path; reaching it records a snapshot.

<!-- stage: trace -->
### Following The Search On Two Graphs

#### A Graph With Two Branches

The first graph has edges 0 to 1, 0 to 2, 1 to 3, 2 to 3 and 3 to 4, with source 0 and target 4. The cells below are the vertex ids, and the pointer `cur` sits on the vertex whose call is active. The search enters 0, then 1, then 3, then 4, and records the snapshot 0, 1, 3, 4. It then removes vertices until the working path is 0 again and enters 2. The branch through 2 reaches 3 again, and that is the step the naive code could not take.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"path":"0","found":0},"note":"The search enters vertex 0 and appends it, so the working path now ends with 0."},{"at":{"cur":1},"vars":{"path":"0-1","found":0},"note":"The search enters vertex 1 and appends it, so the working path now ends with 1."},{"at":{"cur":3},"vars":{"path":"0-1-3","found":0},"note":"The search enters vertex 3 and appends it, so the working path now ends with 3."},{"at":{"cur":4},"vars":{"path":"0-1-3-4","found":1},"note":"The call reaches target 4, so the search stores a copy of the working path and counts path number 1."},{"at":{"cur":3},"vars":{"path":"0-1-3","found":1},"note":"The call removes its vertex and control returns to vertex 3."},{"at":{"cur":1},"vars":{"path":"0-1","found":1},"note":"The call removes its vertex and control returns to vertex 1."},{"at":{"cur":0},"vars":{"path":"0","found":1},"note":"The call removes its vertex and control returns to vertex 0."},{"at":{"cur":2},"vars":{"path":"0-2","found":1},"note":"The search enters vertex 2 and appends it, so the working path now ends with 2."},{"at":{"cur":3},"vars":{"path":"0-2-3","found":1},"note":"The search enters vertex 3 and appends it, so the working path now ends with 3."},{"at":{"cur":4},"vars":{"path":"0-2-3-4","found":2},"note":"The call reaches target 4, so the search stores a copy of the working path and counts path number 2."},{"at":{"cur":3},"vars":{"path":"0-2-3","found":2},"note":"The call removes its vertex and control returns to vertex 3."},{"at":{"cur":2},"vars":{"path":"0-2","found":2},"note":"The call removes its vertex and control returns to vertex 2."},{"at":{"cur":0},"vars":{"path":"0","found":2},"note":"The call removes its vertex and control returns to vertex 0."},{"at":{"cur":-1},"vars":{"path":"empty","found":2},"note":"The source call removes itself, so the working path is empty and the search ends."}]}
```

#### A Graph With A Dead End

The second graph has edges 0 to 1, 0 to 2, 1 to 4, 2 to 3 and 0 to 4, with target 4. Vertex 3 has no outgoing edge and is not the target. The search enters 3 through 2, finds no neighbors, records nothing and removes 3 at once. The direct edge from 0 to 4 yields the short path 0, 4. Both traces end with an empty working path, which shows that every append was paired with a removal.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"path":"0","found":0},"note":"The search enters vertex 0 and appends it, so the working path now ends with 0."},{"at":{"cur":1},"vars":{"path":"0-1","found":0},"note":"The search enters vertex 1 and appends it, so the working path now ends with 1."},{"at":{"cur":4},"vars":{"path":"0-1-4","found":1},"note":"The call reaches target 4, so the search stores a copy of the working path and counts path number 1."},{"at":{"cur":1},"vars":{"path":"0-1","found":1},"note":"The call removes its vertex and control returns to vertex 1."},{"at":{"cur":0},"vars":{"path":"0","found":1},"note":"The call removes its vertex and control returns to vertex 0."},{"at":{"cur":2},"vars":{"path":"0-2","found":1},"note":"The search enters vertex 2 and appends it, so the working path now ends with 2."},{"at":{"cur":3},"vars":{"path":"0-2-3","found":1},"note":"Vertex 3 has no outgoing edge and is not the target, so the call stores nothing and returns."},{"at":{"cur":2},"vars":{"path":"0-2","found":1},"note":"The call removes its vertex and control returns to vertex 2."},{"at":{"cur":0},"vars":{"path":"0","found":1},"note":"The call removes its vertex and control returns to vertex 0."},{"at":{"cur":4},"vars":{"path":"0-4","found":2},"note":"The call reaches target 4, so the search stores a copy of the working path and counts path number 2."},{"at":{"cur":0},"vars":{"path":"0","found":2},"note":"The call removes its vertex and control returns to vertex 0."},{"at":{"cur":-1},"vars":{"path":"empty","found":2},"note":"The source call removes itself, so the working path is empty and the search ends."}]}
```

<!-- stage: code -->
### Enumerating Paths With Backtracking

The method below is the corrected search. The three lines `add`, the recursive loop and `remove` frame every call, and the snapshot is taken with a copy constructor.

```java
static void enumerate(List<List<Integer>> adj, int cur, int target,
                      List<Integer> path, List<List<Integer>> found) {
    path.add(cur);
    if (cur == target) {
        found.add(new ArrayList<>(path));
    } else {
        for (int next : adj.get(cur)) enumerate(adj, next, target, path, found);
    }
    path.remove(path.size() - 1);
}
```

The call `path.remove(path.size() - 1)` passes an `int`, so Java removes the element at that index. The call `path.remove(cur)` with an `int` variable would also remove by index and would delete the wrong element or throw an exception. The time is O(P * n + V + E) in the worst case for a DAG with `P` paths, because each snapshot copies up to `n` vertices. The extra space is O(n) for the working path and the recursion depth, plus the output.

<!-- stage: applicability -->
### Recognizing Path Listing Tasks

#### Reading The Cue

Use this method when the output must contain every route from a source to a target and not only a yes or no answer. Statements say "return all paths", "list every route" or "count the ways" when the paths differ in their vertices.

#### Checking The Invariant

The invariant of the lesson is that the working path contains exactly the current recursion chain and is restored after each neighbor. Every bug in this family breaks one half. A missing removal leaves stale vertices in later answers. A missing copy makes all stored answers equal.

#### Avoiding The False Friend

The global visited array is the false friend of this task. It is correct for reachability and components, because there each vertex needs one visit. It is wrong here, because one vertex may belong to many valid paths. When the graph may contain cycles, the DAG argument fails, and the search needs a visited flag that is set on entry and cleared on exit, so that it describes the working path only. The last exercise of this lesson uses that flag.

<!-- stage: exercises -->
### Exercises

#### [Build] Paths In A Tiny DAG (Author exercise)
<!-- id: gt-tiny-dag-paths -->

**Prerequisites.** The working path of this lesson.

**Problem.** A directed acyclic graph has vertices `0` to `n - 1` and the directed edges in `edges`, where `edges[i] = [from, to]`. Return every path from vertex `0` to vertex `n - 1`. Visit the neighbors of a vertex in the order in which its edges appear in `edges`, and list the paths in the order in which the search finds them.

**Constraints.** The limits are:
- **Vertices** satisfy `2 <= n <= 12`.
- **Edges** contain no duplicate pair and no self loop.
- **Acyclic** holds for every input.
- **Result** is a list of vertex lists; it is empty when no path exists.
- **Mutation** does not occur; the input is not changed.

**Example 1.** Input `n = 4`, `edges = [[0,1],[0,2],[1,3],[2,3]]`, output `[[0,1,3],[0,2,3]]`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[0,2],[2,4],[1,4],[3,4]]`, output `[[0,1,2,4],[0,1,4],[0,2,4]]`.

**Hint.** What must the list contain when a call returns to its caller?

**Changed decision.** The method appends a vertex, recurses, then removes it, so the list equals the current chain.

#### [Vary] All Paths From Source to Target (LeetCode 797)
<!-- id: gt-all-paths-source-target -->

**Prerequisites.** The first exercise above.

**Problem.** This version takes the graph as `n` and `edges`, and it returns paths as independent lists. A directed acyclic graph has vertices `0` to `n - 1`. Return every path from vertex `0` to vertex `n - 1` in the order in which a depth-first search finds them, with neighbors in the order of `edges`. Changing one returned list must not change any other returned list.

**Constraints.** The limits are:
- **Vertices** satisfy `2 <= n <= 15`.
- **Edges** contain no duplicate pair and no self loop.
- **Acyclic** holds for every input.
- **Result** lists are separate objects that share no storage.

**Example 1.** Input `n = 6`, `edges = [[0,1],[0,2],[1,3],[2,3],[3,4],[3,5],[4,5]]`, output `[[0,1,3,4,5],[0,1,3,5],[0,2,3,4,5],[0,2,3,5]]`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[0,2],[1,4],[2,3],[0,4]]`, output `[[0,1,4],[0,4]]`.

**Hint.** Which moment decides whether a stored answer stays correct after the search continues?

**Changed decision.** The method copies the working path at the target, because the same storage is reused afterwards.

#### [Boundary] Dead End And Direct Edge (Author exercise)
<!-- id: gt-dead-end-direct-edge -->

**Prerequisites.** The two exercises above.

**Problem.** A directed acyclic graph has vertices `0` to `n - 1`. Given a source `s` and a target `t` with `s != t`, return every path that starts at `s` and ends at `t`. A path that ends at a vertex without outgoing edges and different from `t` is not an answer. A direct edge from `s` to `t` is a path of two vertices. When no path exists, return an empty list.

**Constraints.** The limits are:
- **Vertices** satisfy `2 <= n <= 12`.
- **Source and target** are distinct vertices in `0..n-1`.
- **Edges** contain no duplicate pair and no self loop.
- **Acyclic** holds for every input.

**Example 1.** Input `n = 4`, `edges = [[0,1],[0,3],[1,2]]`, `s = 0`, `t = 3`, output `[[0,3]]`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[2,1]]`, `s = 0`, `t = 2`, output `[]`.

**Hint.** What does a call return when it has no neighbors and is not the target?

**Changed decision.** Only a call that reaches the target contributes paths, so dead ends contribute nothing.

#### [Recognize] Enumerate Simple Paths (Author exercise)
<!-- id: gt-enumerate-simple-paths -->

**Prerequisites.** All three exercises above.

**Problem.** A directed graph may contain cycles. A simple path is a path in which no vertex appears twice. Given a source `s` and a target `t` with `s != t`, return every simple path from `s` to `t`, in the order a depth-first search finds them, with neighbors in the order of `edges`. A path stops at its first visit of `t`.

**Constraints.** The limits are:
- **Vertices** satisfy `2 <= n <= 8`.
- **Edges** contain no duplicate pair and no self loop; cycles are allowed.
- **Source and target** are distinct vertices in `0..n-1`.
- **Result** is empty when no simple path exists.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,2],[2,0],[1,3],[2,3]]`, `s = 0`, `t = 3`, output `[[0,1,2,3],[0,1,3]]`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,0],[0,2],[1,2],[2,1],[2,4],[1,4]]`, `s = 0`, `t = 4`, output `[[0,1,2,4],[0,1,4],[0,2,1,4],[0,2,4]]`.

**Hint.** What does a cycle allow that a DAG does not, and when should the flag be cleared?

**Changed decision.** The visited flag is set on entry and cleared on exit, so it describes only the working path.
