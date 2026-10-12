<!-- lesson-kind: standard -->
<!-- lesson-id: strong-components -->
## Find Strongly Connected Components

<!-- stage: context -->
### Modules That Import Each Other

A language runtime loads source modules and runs each module's start-up code once. Module A imports B, B imports C, and C imports A. The runtime cannot run A before B, B before C, or C before A, so any fixed order fails for these three. It must treat them as one unit and initialize them together. Module D imports A but nothing imports D back, so D can wait until that unit is ready.

Model the modules as vertices of a directed graph and each import as a directed edge. Vertex `v` **reaches** vertex `u` when a path of edges leads from `v` to `u`. A **strongly connected component** is a largest set of vertices in which every vertex reaches every other vertex. The three modules A, B and C form one such set, and D forms a set of its own.

The task is to label every vertex with its component, so that two vertices share a label exactly when each reaches the other. This lesson asks how to find all components in linear time, without testing every pair of vertices.

<!-- stage: naive -->
### Testing Every Pair Of Vertices

The direct definition suggests a direct method. For each vertex, run a depth-first search and record which vertices it reaches in a table `reach`. Two vertices belong together when `reach[u][v]` and `reach[v][u]` are both true. The method then gives each unlabeled vertex a new label and copies that label to every vertex that is mutually reachable with it.

```java
static int[] byPairs(int n, int[][] edges) {
    List<List<Integer>> out = new ArrayList<>();
    for (int v = 0; v < n; v++) out.add(new ArrayList<>());
    for (int[] e : edges) out.get(e[0]).add(e[1]);
    boolean[][] reach = new boolean[n][n];
    for (int s = 0; s < n; s++) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(s);
        reach[s][s] = true;
        while (!stack.isEmpty()) {
            int u = stack.pop();
            for (int v : out.get(u)) {
                if (!reach[s][v]) {
                    reach[s][v] = true;
                    stack.push(v);
                }
            }
        }
    }
    int[] label = new int[n];
    Arrays.fill(label, -1);
    int next = 0;
    for (int u = 0; u < n; u++) {
        if (label[u] != -1) continue;
        for (int v = 0; v < n; v++) {
            if (reach[u][v] && reach[v][u]) label[v] = next;
        }
        next++;
    }
    return label;
}
```

The answer is correct, because mutual reachability is exactly the definition. The question is the cost on a large module graph.

```predict
A project has 100000 modules and 300000 imports. Roughly how many edge visits does byPairs perform, and how much memory does the table reach need?

It performs about 100000 searches that each visit up to 300000 edges, which is on the order of 3 * 10^10 visits. The table has 10^10 boolean cells, so it needs about 10 GB. Both numbers are far beyond a practical limit, although the answer is correct. The cost comes from repeating a full search for every start vertex.
```

<!-- stage: bottleneck -->
### One Search Per Vertex Is Too Slow

The method runs one search from each of the V vertices, and each search may scan all E edges. The time is O(V * (V + E)). The table `reach` has V * V cells, so the memory is O(V^2). For a graph with 100000 vertices, the table alone has 10^10 cells, which is about 10 GB at one byte per cell.

Most of this work repeats facts. If vertex `a` reaches vertex `b`, then everything that `b` reaches is also reachable from `a`, and the method rediscovers this from scratch for every start. The labeling step adds another O(V^2) pair checks.

A better method must visit each vertex and each edge a constant number of times, so the time is O(V + E). It must also store O(V) values, one label per vertex, and no table of pairs. That requires a fixed order from two linear sweeps that exposes the components, instead of a separate search per vertex.

<!-- stage: insight -->
### Two Sweeps With A Reversed Graph

The method sweeps the graph twice. The first sweep records an order, and the second sweep uses that order to cut the graph into components.

<!-- names: finish order, reversed graph, condensed graph -->

#### Recording The Finish Order

A depth-first search **finishes** a vertex when it has examined every outgoing edge of that vertex and returns from it. The **finish order** lists the vertices in the sequence in which the first sweep finishes them. The first sweep starts a search from each vertex that is still unvisited, so every vertex receives a place in the list.

#### Collapsing Components Into One Graph

Merge each component into a single vertex. Keep one edge from component C to component D when some edge leads from a vertex of C to a vertex of D. The result is the **condensed graph**. It has no cycle. A cycle through two components would make every vertex of one reach every vertex of the other and back, and the two components would be one component.

A condensed graph without a cycle has at least one **source**, a component with no incoming edge.

#### Why The Latest Finisher Is Safe

The key fact is this. If the condensed graph has an edge from component C to component D, then some vertex of C finishes after every vertex of D. When the search enters C first, it can reach D, and all of D finishes before the search returns from the entry vertex of C. When the search enters D first, it cannot reach C, so all of D finishes before the search ever touches C.

It follows that the vertex with the latest finish lies in a source component of the condensed graph.

#### Searching The Reversed Graph

The **reversed graph** has the same vertices, and every edge from `a` to `b` appears as an edge from `b` to `a`. Reversal keeps the components unchanged, because a path from `u` to `v` becomes a path from `v` to `u`. It changes the direction of every condensed edge, so a source component now has no outgoing edge.

The second sweep takes vertices in decreasing finish order and searches the reversed graph from each vertex that has no label. The first start lies in a source component, and the search cannot leave it. It labels exactly that component. After removing it, the next unlabeled vertex with the latest finish lies in a source of what remains, and the argument repeats. Every search therefore labels one full component and nothing more.

<!-- stage: variables -->
### Order, Reversed Lists And Labels

The method reads the vertex count `n` and the array `edges` of pairs `[from, to]`. The graph is directed, and the vertices carry the numbers `0` to `n - 1`. Repeated edges and self loops may occur. The method does not change `edges`. It keeps these structures.

- **out** is the list of outgoing neighbours of each vertex, in the order of `edges`.
- **back** is the list of incoming neighbours of each vertex, which forms the reversed graph.
- **order** is an `int[]` of length `n` that holds the vertices in finish order.
- **cursor** is an `int[]` where `cursor[u]` is the position of the next edge of `u` to examine.
- **seen** is a `boolean[]` of length `n` that marks vertices the first sweep has pushed.
- **placed** is the number of vertices written to `order` so far.
- **label** is an `int[]` of length `n` where `-1` marks a vertex that no search has reached.

The labels count up from 0 in the order in which the second sweep opens components. In the second sweep, the method assigns a label when it pushes a vertex, so a vertex never enters a stack twice. The first sweep uses `seen` for the same purpose. The first sweep uses an explicit stack, because a recursive search over a long chain of modules can exhaust the Java call stack.

<!-- stage: trace -->
### Two Runs On Module Graphs

#### Eight Modules In Four Groups

The first graph has eight modules and eleven imports. The imports run 0 to 3, 3 to 6, 6 to 0, 6 to 1, 1 to 4 and 4 to 1. They continue with 4 to 2, 2 to 5, 5 to 2, 5 to 7 and 3 to 7. The first sweep produces the finish order 7, 5, 2, 4, 1, 6, 3, 0. The second sweep reads that order from the right, so each cell below is one vertex in the order 0, 3, 6, 1, 4, 2, 5, 7. The pointer `i` marks the vertex under examination. The variable `label` is the label of that vertex after the step. The variable `found` is the number of vertices that a new search collects. The variable `labeled` is the total number of labeled vertices afterward. At step 0, vertex 0 opens label 0 and the reversed edges lead to 6 and then to 3, so `found` is 3. Vertices 3 and 6 need no search, because they already have a label. The sweep ends with four labels, and the groups are 0 3 6, 1 4, 2 5 and 7.

The first sweep derives its order from a single search that starts at vertex 0. That search walks 0, 3, 6, 1, 4, 2, 5 and then 7. Vertex 7 has no outgoing import, so it finishes first. The search then backs up and finishes 5, 2, 4, 1, 6, 3 and 0, because every other edge of those vertices leads to a vertex that is already visited.

```trace
{"cells":["0","3","6","1","4","2","5","7"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"label":0,"found":3,"labeled":3},"note":"Vertex 0 opens label 0 and the search collects 3 vertices: 0, 3, 6."},{"at":{"i":1},"vars":{"label":0,"found":0,"labeled":3},"note":"Vertex 3 already has label 0, so no search starts."},{"at":{"i":2},"vars":{"label":0,"found":0,"labeled":3},"note":"Vertex 6 already has label 0, so no search starts."},{"at":{"i":3},"vars":{"label":1,"found":2,"labeled":5},"note":"Vertex 1 opens label 1 and the search collects 2 vertices: 1, 4."},{"at":{"i":4},"vars":{"label":1,"found":0,"labeled":5},"note":"Vertex 4 already has label 1, so no search starts."},{"at":{"i":5},"vars":{"label":2,"found":2,"labeled":7},"note":"Vertex 2 opens label 2 and the search collects 2 vertices: 2, 5."},{"at":{"i":6},"vars":{"label":2,"found":0,"labeled":7},"note":"Vertex 5 already has label 2, so no search starts."},{"at":{"i":7},"vars":{"label":3,"found":1,"labeled":8},"note":"Vertex 7 opens label 3 and the search collects 1 vertex: 7."}]}
```

#### Searching The Wrong Direction

The second graph has five modules and six imports: 0 to 1, 1 to 0, 1 to 2, 2 to 3, 3 to 2 and 3 to 4. Its true groups are 0 1, 2 3 and 4. The finish order is 4, 3, 2, 1, 0. This run is a variant that keeps the decreasing finish order but searches the original edges in the second sweep. The variable `truth` is the size of the true group of the vertex under examination. The search from vertex 0 follows the one-way edges onward and collects all five modules, so `found` is 5 where `truth` is 2. The later vertices are already labeled. The variant ends with one label instead of three, and the reversed graph is what prevents this.

```trace
{"cells":["0","1","2","3","4"],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"label":0,"found":5,"labeled":5,"truth":2},"note":"Vertex 0 opens label 0 and the search collects 5 vertices: 0, 1, 2, 3, 4."},{"at":{"i":1},"vars":{"label":0,"found":0,"labeled":5,"truth":2},"note":"Vertex 1 already has label 0, so no search starts."},{"at":{"i":2},"vars":{"label":0,"found":0,"labeled":5,"truth":2},"note":"Vertex 2 already has label 0, so no search starts."},{"at":{"i":3},"vars":{"label":0,"found":0,"labeled":5,"truth":2},"note":"Vertex 3 already has label 0, so no search starts."},{"at":{"i":4},"vars":{"label":0,"found":0,"labeled":5,"truth":1},"note":"Vertex 4 already has label 0, so no search starts."}]}
```

<!-- stage: code -->
### Kosaraju With Two Sweeps

The method returns an `int[]` of labels, where equal labels mean the same component. It uses explicit stacks in both sweeps.

```java
static int[] strongComponents(int n, int[][] edges) {
    List<List<Integer>> out = new ArrayList<>();
    List<List<Integer>> back = new ArrayList<>();
    for (int v = 0; v < n; v++) {
        out.add(new ArrayList<>());
        back.add(new ArrayList<>());
    }
    for (int[] e : edges) {
        out.get(e[0]).add(e[1]);
        back.get(e[1]).add(e[0]);
    }
    boolean[] seen = new boolean[n];
    int[] cursor = new int[n];
    int[] order = new int[n];
    int placed = 0;
    for (int s = 0; s < n; s++) {
        if (seen[s]) continue;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(s);
        seen[s] = true;
        while (!stack.isEmpty()) {
            int u = stack.peek();
            if (cursor[u] < out.get(u).size()) {
                int v = out.get(u).get(cursor[u]++);
                if (!seen[v]) {
                    seen[v] = true;
                    stack.push(v);
                }
            } else {
                stack.pop();
                order[placed++] = u;
            }
        }
    }
    int[] label = new int[n];
    Arrays.fill(label, -1);
    int next = 0;
    for (int i = n - 1; i >= 0; i--) {
        if (label[order[i]] != -1) continue;
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(order[i]);
        label[order[i]] = next;
        while (!stack.isEmpty()) {
            int u = stack.pop();
            for (int v : back.get(u)) {
                if (label[v] == -1) {
                    label[v] = next;
                    stack.push(v);
                }
            }
        }
        next++;
    }
    return label;
}
```

The first sweep appends a vertex to `order` only when its cursor has passed the last edge. The second loop walks `order` from the last index to the first, which gives decreasing finish order. Each sweep pushes each vertex once and moves each edge once, so the time is O(V + E). The two adjacency lists, the order, the cursors and the labels take O(V + E) memory in total.

<!-- stage: applicability -->
### Recognizing Mutual Reachability Problems

#### Reading The Cue

Use this method when a statement on a directed graph asks which vertices can reach each other in both directions. Typical forms are grouping mutually dependent modules, finding sets of web pages that link back to one another, and counting groups of accounts that can all transfer to each other. The answer is usually a label array, a component count, the size of the largest group, or a statement about how the groups connect.

#### Checking The Invariant

An **invariant** is a statement that holds before and after every step of a loop, and it is what proves the method correct. Here the invariant is that every search of the second sweep starts in a component with no unlabeled component pointing into it, so the search labels exactly one whole component. Two details of the code protect it. The second sweep must walk `order` from the latest finisher backward, and it must search the reversed lists. Test a vertex with a self loop, which stays alone. Test a vertex that has no edges at all, which forms a component of one.

#### Avoiding The False Friend

A **false friend** is a well-known technique that seems to fit the problem and gives wrong answers on some inputs. The false friend here is connectivity of an undirected graph, such as a union-find structure or a plain search that ignores direction. It merges two modules after a single one-way import, although the second module cannot reach the first. The second trace above shows the same failure from another side, where the order is right but the direction of the search is wrong. A related trap is to call two vertices connected after one search succeeds. Reaching `v` from `u` proves one direction only.

<!-- stage: exercises -->
### Exercises

#### [Build] Finish Order (Author exercise)
<!-- id: ga-scc-finish-order -->

**Prerequisites.** The first sweep of this lesson.

**Problem.** A directed graph consists of the vertex set `0`, ..., `n - 1`, and `edges` lists pairs `[a, b]` for an edge from `a` to `b`. Run a depth-first search that starts from vertices `0, 1, ..., n - 1` in ascending order and skips visited vertices. At each vertex the search follows outgoing edges in the order in which they appear in `edges`. Return an `int[]` of length `n` that lists the vertices in the order in which the search finishes them.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 6000`, and repeats and self loops may occur.
- **Mutation** is not allowed, and `edges` stays unchanged.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,2],[0,2],[2,3]]`, output `[3,2,1,0]`.

**Example 2.** Input `n = 5`, `edges = [[1,0],[0,1],[3,4],[2,3]]`, output `[1,0,4,3,2]`.

**Hint.** When does the search append a vertex, and does a cycle back to a vertex on the stack append it early?

**Changed decision.** The method records a vertex after its last outgoing edge completes and not when it first reaches the vertex.

#### [Vary] Reverse-Graph Components (Author exercise)
<!-- id: ga-scc-reverse-components -->

**Prerequisites.** The exercise above.

**Problem.** Take a directed graph whose vertex labels run `0` through `n - 1`, with edges `[a, b]`. Compute the finish order of the original graph as in the exercise above. Then take vertices in decreasing finish order and search the reversed graph from each vertex that has no label yet. Return an `int[]` `label` where `label[v]` names the group of `v`. The groups carry the numbers `0, 1, 2, ...` in the order in which these searches begin.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 6000`, and repeats and self loops may occur.
- **Labels** are consecutive integers from `0`.
- **Mutation** is not allowed, and `edges` stays unchanged.

**Example 1.** Input `n = 6`, `edges = [[0,1],[1,2],[2,0],[2,3],[3,4],[4,3],[5,4]]`, output `[1,1,1,2,2,0]`.

**Example 2.** Input `n = 4`, `edges = [[3,2],[2,3],[1,0],[0,1],[2,1]]`, output `[1,1,0,0]`.

**Hint.** Which vertex starts the first search, and why does that search stay inside its own component?

**Changed decision.** The method returns a label for every vertex, and the numbering depends on the order of the second sweep.

#### [Boundary] Singleton And One-Way Edge (Author exercise)
<!-- id: ga-scc-singleton-one-way -->

**Prerequisites.** The two exercises above.

**Problem.** Consider a directed graph with vertices `0` to `n - 1` and edges `[a, b]`. A component is a singleton when it contains exactly one vertex. Return the number of singleton components. A vertex with only a self loop, only a one-way edge, or no edge counts as a singleton.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 6000`, and repeats and self loops may occur.
- **Result** lies in `0..n`.
- **Mutation** is not allowed, and `edges` stays unchanged.

**Example 1.** Input `n = 3`, `edges = [[0,1],[1,2]]`, output `3`.

**Example 2.** Input `n = 4`, `edges = [[0,0],[1,2],[2,1],[2,3]]`, output `2`.

**Hint.** Does an edge from `a` to `b` without a way back from `b` to `a` put the two in one component, and what does a self loop add?

**Changed decision.** The method counts component sizes and keeps vertices apart when only one direction of reachability exists.

#### [Recognize] Condensation DAG (Author exercise)
<!-- id: ga-scc-condensation-dag -->

**Prerequisites.** The three exercises above.

**Problem.** Let a directed graph use vertex labels `0` through `n - 1` and edges `[a, b]`. Merge each strongly connected component into one node. Keep an edge from node C to node D when some edge leads from a vertex of C to a vertex of D and C differs from D. Count each such pair once. Return an `int[]` of length 3 with the number of nodes, the number of distinct edges between nodes, and the number of nodes that have no incoming edge.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 6000`, and repeats and self loops may occur.
- **Result** lists the three counts in the order given.
- **Mutation** is not allowed, and `edges` stays unchanged.

**Example 1.** Input `n = 6`, `edges = [[0,1],[1,0],[1,2],[2,3],[3,2],[0,2],[1,2],[4,5],[5,4],[3,4]]`, output `[3,2,1]`.

**Example 2.** Input `n = 3`, `edges = [[0,1],[0,1],[1,0],[2,2]]`, output `[2,0,2]`.

**Hint.** Which edges disappear after merging, and which edges now repeat between the same two nodes?

**Changed decision.** The method counts distinct edges of the merged graph, so edges inside a component and repeated edges between components must not add to the count.
