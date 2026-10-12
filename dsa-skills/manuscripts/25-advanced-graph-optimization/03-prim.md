<!-- lesson-kind: standard -->
<!-- lesson-id: prim -->
## Grow A Spanning Tree With Prim

<!-- stage: context -->
### Wiring Offices With Least Cable

#### A Plan That Overpays

A company opens six offices in one city and must link them all to one network. A cable run between two offices has a known price, and a river or a highway blocks some pairs entirely. The first plan lays the cheapest cable out of the head office, then the cheapest cable out of the office it just reached, and so on. The plan links every office, yet the invoice is larger than a different layout would cost. The plan looks at the cables of one office and ignores the cables that other linked offices could offer.

#### Modeling The Problem

Model the offices as vertices and each possible cable run as an undirected edge with a **weight**, which is its price. A **spanning tree** is a set of edges that connects all `n` vertices and has no cycle, so it uses exactly `n - 1` edges. Its cost is the sum of its weights. The task is to find a spanning tree of minimum cost, and to report when no tree exists because some office is out of reach.

This lesson assumes an undirected graph with vertices numbered `0` to `n - 1`, edges given as triples `[a, b, weight]`, and an input that the method never changes. It asks which edge the method should add next, so that the finished tree is the cheapest one.

<!-- stage: naive -->
### Walking To The Nearest Office

The first attempt follows the plan from the story. It keeps the set of linked vertices and a current vertex, which starts at vertex 0. At each step it looks at the edges of the current vertex only. It picks the cheapest edge to a vertex that is not linked yet. It adds that vertex and makes it the new current vertex.

```java
static long nearestWalk(int n, int[][] edges) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(new int[] {e[1], e[2]});
        adj.get(e[1]).add(new int[] {e[0], e[2]});
    }
    boolean[] linked = new boolean[n];
    linked[0] = true;
    int cur = 0;
    int count = 1;
    long total = 0;
    while (count < n) {
        int bestV = -1;
        long bestW = Long.MAX_VALUE;
        for (int[] r : adj.get(cur)) {
            if (!linked[r[0]] && r[1] < bestW) {
                bestW = r[1];
                bestV = r[0];
            }
        }
        if (bestV == -1) return -1;
        linked[bestV] = true;
        total += bestW;
        cur = bestV;
        count++;
    }
    return total;
}
```

Each step scans the edges of one vertex, so the whole walk reads every edge at most twice. It always picks the lowest price it can see. The question is whether the lowest visible price leads to the lowest total.

```predict
Use the edges 0 to 1 with weight 1, 0 to 2 with weight 2, and 1 to 2 with weight 5. What total does nearestWalk return, and what is the minimum cost?

It returns 6, but the minimum is 3. The walk takes edge 0 to 1 for 1, makes vertex 1 current, and then sees only the edge 1 to 2 for 5. The cheap edge 0 to 2 for 2 belongs to vertex 0, which is no longer current, so the walk never compares it. The tree 0 to 1 and 0 to 2 costs 3.
```

<!-- stage: bottleneck -->
### The Walk Sees One Vertex

#### A Wrong Or Missing Answer

The walk compares only the edges of the latest vertex. Every earlier vertex still owns edges that may be cheaper, and the walk forgets them. This is a wrong answer, and it can be worse than a high price. Take the edges 0 to 1 and 0 to 2 in a graph where vertices 1 and 2 have no other edges. The walk moves to vertex 1 and finds no unlinked neighbor. It then returns minus one, although the graph is connected.

#### Why A Rescan Is Too Slow

A correct repair compares the edges of all linked vertices at every step. A plain version scans the full edge list in each of the `n - 1` rounds, keeps the cheapest edge with exactly one endpoint linked, and adds it. That version is correct, but it costs O(V * E) time, where V is the number of vertices and E is the number of edges. A network with 10,000 offices and 100,000 possible runs needs about a billion edge reads.

A better method must remember the useful edges of every linked vertex between steps. It must also return the cheapest of them quickly, without rescanning the list. Then each edge enters the structure once, and the cost of ordering the edges is the only extra price.

<!-- stage: insight -->
### Always Take The Cheapest Crossing Edge

The method grows one tree from vertex 0. At each step it adds the cheapest edge that joins the tree to a vertex outside the tree.

<!-- names: crossing, frontier, stale -->

#### The Crossing Edge

Call the vertices already in the tree the inside, and all other vertices the outside. An edge is **crossing** when exactly one of its endpoints is inside. Every spanning tree must contain at least one crossing edge, because the outside vertices have to connect to the inside somehow. An edge with both endpoints inside would close a cycle, and an edge with both endpoints outside does not touch the tree yet.

#### Why The Cheapest One Is Safe

Take the cheapest crossing edge `e` and any minimum spanning tree `T` built on the current tree. Suppose `T` omits `e`. Adding `e` to `T` closes a cycle. That cycle leaves the inside through `e`, so it must come back through another crossing edge `f`. Because `e` is the cheapest crossing edge, `f` weighs at least as much as `e`. Remove `f` and keep `e`. The result is still a spanning tree, and its cost is not higher. So some minimum spanning tree contains `e`, and adding `e` never spoils the final answer. Each added edge keeps that statement true, so the last tree is minimum.

#### Keeping The Frontier In A Heap

The **frontier** is the set of crossing edges at one moment. The method stores the frontier in a priority queue, a binary heap that returns its smallest weight first. When a vertex joins the tree, the method pushes every edge from that vertex to an outside vertex, as the pair of weight and far vertex. Removing the smallest pair gives the cheapest crossing edge in O(log E) time, with no rescan of the edge list.

#### Skipping Outdated Heap Entries

An edge can leave the frontier without leaving the heap. Suppose two inside vertices both have an edge to the same outside vertex `x`. The cheaper entry joins `x`, and the other entry now points to a vertex that is inside. Java's `PriorityQueue` cannot delete an arbitrary entry cheaply, so the entry stays. It is **stale**, because its far vertex is already in the tree and it is no longer crossing. When a stale entry leaves the heap, the method finds the far vertex flagged as inside and skips the entry. The second trace below uses the false friend that breaks this rule by changing the heap key.

<!-- stage: variables -->
### Tree Flags, Heap And Total

The method reads `n`, the list `edges` of triples `[a, b, weight]`, and it changes none of them. It builds an adjacency list in which each edge appears under both endpoints, and it keeps these working values.

- **inTree** is a `boolean[]` of length `n`; `true` marks a vertex that already joined the tree.
- **heap** is a `PriorityQueue<long[]>` whose entries are `{weight, vertex}`, ordered by weight with `Long.compare`.
- **total** is a `long` sum of the accepted weights, because many large weights exceed the range of `int`.
- **joined** is the number of vertices in the tree, and the tree is complete when it equals `n`.

The first heap entry is `{0, 0}`, which joins vertex 0 at no cost. A graph that is not connected leaves `joined` below `n` when the heap empties, and the method then returns minus one. That value cannot be a real cost, since weights are nonnegative.

<!-- stage: trace -->
### Two Runs On Small Networks

#### Six Offices With One Cheapest Tree

The first network has six vertices and nine edges, written as pairs with weights: 0-1 costs 4, 0-2 costs 3, 1-2 costs 1, 1-3 costs 2, 2-3 costs 4, 2-4 costs 5, 3-4 costs 6, 3-5 costs 7 and 4-5 costs 3. Each cell is one heap entry in the order in which the entries leave the heap, written as vertex and weight. The pointer `pop` marks the entry that leaves at that step. The variable `w` is the weight of that entry, `heap` is the number of entries left afterward, and `total` is the tree weight so far. At step 1, vertex 2 joins by the edge of weight 3, which is cheaper than the edge to vertex 1 of weight 4. At step 4 the entry 1@4 leaves the heap, and the method drops it as stale, because vertex 1 joined at step 2. The final tree weighs 14, and it uses the edges of weight 3, 1, 2, 5 and 3. Four of the ten heap entries are stale.

```trace
{"cells":["0@0","2@3","1@1","3@2","1@4","3@4","4@5","5@3","4@6","5@7"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"w":0,"heap":2,"total":0},"note":"The cheapest crossing edge has weight 0, so vertex 0 joins and the total becomes 0. Its edges to outside vertices put 1@4, 2@3 into the heap."},{"at":{"pop":1},"vars":{"w":3,"heap":4,"total":3},"note":"The cheapest crossing edge has weight 3, so vertex 2 joins and the total becomes 3. Its edges to outside vertices put 1@1, 3@4, 4@5 into the heap."},{"at":{"pop":2},"vars":{"w":1,"heap":4,"total":4},"note":"The cheapest crossing edge has weight 1, so vertex 1 joins and the total becomes 4. Its edges to outside vertices put 3@2 into the heap."},{"at":{"pop":3},"vars":{"w":2,"heap":5,"total":6},"note":"The cheapest crossing edge has weight 2, so vertex 3 joins and the total becomes 6. Its edges to outside vertices put 4@6, 5@7 into the heap."},{"at":{"pop":4},"vars":{"w":4,"heap":4,"total":6},"note":"The heap returns 1@4 as its smallest entry, yet vertex 1 joined earlier through a lighter edge, so the method discards this stale entry and the total stays 6."},{"at":{"pop":5},"vars":{"w":4,"heap":3,"total":6},"note":"The heap returns 3@4 as its smallest entry, yet vertex 3 joined earlier through a lighter edge, so the method discards this stale entry and the total stays 6."},{"at":{"pop":6},"vars":{"w":5,"heap":3,"total":11},"note":"The cheapest crossing edge has weight 5, so vertex 4 joins and the total becomes 11. Its edges to outside vertices put 5@3 into the heap."},{"at":{"pop":7},"vars":{"w":3,"heap":2,"total":14},"note":"The cheapest crossing edge has weight 3, so vertex 5 joins and the total becomes 14. No outside vertex remains next to it, so nothing enters the heap."},{"at":{"pop":8},"vars":{"w":6,"heap":1,"total":14},"note":"The heap returns 4@6 as its smallest entry, yet vertex 4 joined earlier through a lighter edge, so the method discards this stale entry and the total stays 14."},{"at":{"pop":9},"vars":{"w":7,"heap":0,"total":14},"note":"The heap returns 5@7 as its smallest entry, yet vertex 5 joined earlier through a lighter edge, so the method discards this stale entry and the total stays 14."}]}
```

#### A Heap Key That Adds Distances

The second network also has six vertices. A hub edge joins 0 to each of 1, 2, 3, 4 and 5 with the weights 5, 6, 7, 8 and 9, and a chain edge of weight 2 joins each neighbor pair from 1 to 5. This run changes one thing in the method. It pushes the distance from vertex 0 as the heap key and not the edge weight, which is the rule of Dijkstra's method. The variable `key` is the removed key, `edge` is the weight of the edge that attached the vertex, and `total` is the tree weight so far. Every direct edge from vertex 0 beats the chain route to its vertex. So each vertex attaches straight to vertex 0, and the keys equal the direct weights 5 to 9. The tree weighs 35, while the minimum spanning tree uses the chain and weighs 13.

```trace
{"cells":["0@0","1@5","2@6","3@7","4@8","5@9"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"key":0,"edge":0,"total":0},"note":"Key 0 is the smallest distance from vertex 0, so vertex 0 is taken next, and the edge that attaches it weighs 0. The running tree weight grows to 0."},{"at":{"pop":1},"vars":{"key":5,"edge":5,"total":5},"note":"Key 5 is the smallest distance from vertex 0, so vertex 1 is taken next, and the edge that attaches it weighs 5. The running tree weight grows to 5."},{"at":{"pop":2},"vars":{"key":6,"edge":6,"total":11},"note":"Key 6 is the smallest distance from vertex 0, so vertex 2 is taken next, and the edge that attaches it weighs 6. The running tree weight grows to 11."},{"at":{"pop":3},"vars":{"key":7,"edge":7,"total":18},"note":"Key 7 is the smallest distance from vertex 0, so vertex 3 is taken next, and the edge that attaches it weighs 7. The running tree weight grows to 18."},{"at":{"pop":4},"vars":{"key":8,"edge":8,"total":26},"note":"Key 8 is the smallest distance from vertex 0, so vertex 4 is taken next, and the edge that attaches it weighs 8. The running tree weight grows to 26."},{"at":{"pop":5},"vars":{"key":9,"edge":9,"total":35},"note":"Key 9 is the smallest distance from vertex 0, so vertex 5 is taken next, and the edge that attaches it weighs 9. The running tree weight grows to 35. The minimum spanning tree weighs 13, so this tree is 22 too heavy."}]}
```

<!-- stage: code -->
### Prim With A Priority Queue

The method returns the minimum tree weight as a `long`, or minus one when the graph is not connected. It assumes `n >= 1` and never changes `edges`.

```java
static long primTotal(int n, int[][] edges) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(new int[] {e[1], e[2]});
        adj.get(e[1]).add(new int[] {e[0], e[2]});
    }
    boolean[] inTree = new boolean[n];
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, 0});
    long total = 0;
    int joined = 0;
    while (!heap.isEmpty() && joined < n) {
        long[] top = heap.poll();
        int v = (int) top[1];
        if (inTree[v]) continue;
        inTree[v] = true;
        total += top[0];
        joined++;
        for (int[] r : adj.get(v)) {
            if (!inTree[r[0]]) heap.add(new long[] {r[1], r[0]});
        }
    }
    return joined == n ? total : -1;
}
```

The test `inTree[v]` must come before the update, so that a stale entry adds no weight. Each edge appears in two adjacency lists, so the heap receives at most 2E entries plus the first one. Every entry costs O(log E) to insert and to remove, so the method runs in O(E log E) time, which equals O(E log V). It uses O(V + E) memory for the adjacency list, the flags and the heap. A self loop lands on a vertex that is already inside, so the method never pushes it.

<!-- stage: applicability -->
### Recognizing Spanning Tree Problems

#### Reading The Cue

Use this method when the statement gives an undirected weighted graph and asks for the cheapest way to connect every vertex. Cable between offices, pipes between buildings and links between data centers all have this shape. The answer is usually the total weight, the list of chosen edges, or a number derived from the chosen edges, such as the heaviest one. A graph that gives each vertex many neighbors suits Prim well, since the method expands one vertex at a time.

#### Checking The Invariant

An invariant is a fact that no pass of the loop is allowed to break. Here the invariant is that the tree built so far lies inside some minimum spanning tree, and that the heap holds every crossing edge. It depends on two conditions in the code. The stale test must run before any update, and the method must push only edges from a newly joined vertex. Test a graph with two equal cheapest crossing edges, where either choice is safe. Test a disconnected graph, where the heap empties early. Test one vertex alone, which needs no edge and costs 0.

#### Avoiding The False Friend

A false friend is a familiar method that looks right and fails. The first false friend is Dijkstra's method. It has the same heap loop, but its key is the distance from the source, so it builds a shortest path tree and not a minimum spanning tree. The second trace shows the difference in weight. A second false friend is the nearest neighbor walk of the naive stage, which compares the edges of one vertex and not the whole frontier.

<!-- stage: exercises -->
### Exercises

#### [Build] Grow One Tree Edge (Author exercise)
<!-- id: ga-prim-one-edge -->

**Prerequisites.** The crossing edge from this lesson.

**Problem.** A two-way network has `n` sites numbered from `0`. The array `inTree` of type `boolean[]` marks the vertices that are in the tree. The array `edges` lists triples `[a, b, w]`. An edge is crossing when exactly one of `a` and `b` is in the tree. Return the index in `edges` of the crossing edge with the smallest weight, preferring the smaller index on a tie. Return `-1` when no edge is crossing.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`, and `inTree.length == n`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 2000000000`.
- **Mutation** is not allowed, and the method changes neither array.

**Example 1.** Input `inTree = [true,true,false,false]`, `edges = [[0,1,1],[1,2,6],[0,3,4],[2,3,4]]`, output `2`.

**Example 2.** Input `inTree = [true,true,true]`, `edges = [[0,1,2],[1,2,3]]`, output `-1`.

**Hint.** Which edges does the test "exactly one endpoint inside" reject, and what does a self loop do to that test?

**Changed decision.** The method returns the position of the edge and not its weight, so the tie rule decides the output.

#### [Vary] Skip Stale Heap Edges (Author exercise)
<!-- id: ga-prim-stale-edges -->

**Prerequisites.** The exercise above.

**Problem.** Consider a network of `n` offices numbered from `0`, where each element `[a, b, w]` of `edges` is a two-way cable of price `w`. Run Prim's method from vertex `0` with a heap of pairs `{w, vertex}` ordered by weight and then by vertex. When a vertex joins, push one pair for each incident edge whose other endpoint is not in the tree yet. Continue until the heap is empty. Return the number of removed pairs whose vertex is already in the tree.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 1000`.
- **Graph** may be disconnected, and only vertices reachable from vertex `0` take part.

**Example 1.** Input `n = 3`, `edges = [[0,1,1],[0,2,2],[1,2,5]]`, output `1`.

**Example 2.** Input `n = 3`, `edges = [[0,1,4],[1,2,2]]`, output `0`.

**Hint.** When does a pair stay in the heap after its vertex joined by another pair?

**Changed decision.** The method counts the skipped pairs and not the tree weight, so the order in which equal weights leave the heap decides how many pairs become stale.

#### [Boundary] Disconnected Graph (Author exercise)
<!-- id: ga-prim-disconnected -->

**Prerequisites.** The two exercises above.

**Problem.** Take `n` vertices numbered from `0` and the undirected cables `edges`, where `[a, b, w]` joins `a` and `b` at weight `w`. Return the weight of a minimum spanning tree as a `long`. Return `-1` when no spanning tree exists because the graph is not connected. A graph with one vertex has a tree of weight `0`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 8000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 2000000000`.
- **Sums** may exceed the range of `int`, and the result uses `long`.

**Example 1.** Input `n = 3`, `edges = [[0,1,2000000000],[1,2,2000000000]]`, output `4000000000`.

**Example 2.** Input `n = 4`, `edges = [[0,1,3],[2,3,1]]`, output `-1`.

**Hint.** What does the heap contain when the last reachable vertex has joined, and how many vertices joined by then?

**Changed decision.** The method compares the number of joined vertices with `n` after the heap empties, and it returns minus one in place of a partial total.

#### [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-prim-connect-points -->

**Prerequisites.** All three exercises above.

**Problem.** Each point `[x, y]` in `points` is a vertex. The edge between two points has weight `|x1 - x2| + |y1 - y2|`. Return a `long[]` of length 2. The first entry is the weight of a minimum spanning tree of the complete graph on the points. The second entry is the weight of the heaviest edge in that tree, or `0` when the tree has no edge.

**Constraints.** The limits are:
- **Points** satisfy `1 <= points.length <= 1000`, and all points are distinct.
- **Coordinates** satisfy `-1000000 <= x, y <= 1000000`.
- **Sums** may exceed the range of `int`, and the result uses `long`.
- **Mutation** is not allowed, and the method changes no array.

**Example 1.** Input `points = [[0,0],[1,1],[1,4],[6,1]]`, output `[10,5]`.

**Example 2.** Input `points = [[0,0],[0,5],[0,6]]`, output `[6,5]`.

**Hint.** The graph has an edge for every pair of points, so is a heap of edges the cheapest structure to scan?

**Changed decision.** The method returns the heaviest tree edge as well as the total. The usual statement asks for the total only.
