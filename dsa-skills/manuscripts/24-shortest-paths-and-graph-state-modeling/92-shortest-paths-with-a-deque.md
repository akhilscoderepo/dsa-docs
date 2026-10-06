<!-- lesson-kind: combination -->
<!-- lesson-id: shortest-paths-with-a-deque -->
## Shortest Paths With A Deque

<!-- stage: context -->
### Counting Region Crossings Of A Request

A service mesh routes a request from service `0` to service `n - 1`. Each service runs in one region, and each link joins two services. A link inside one region adds nothing to the bill. A link between two regions adds one cross-region charge. The operations team wants the route with the fewest charges, and the length of the route does not matter.

The first tool is the breadth-first search from chapter 21, which finds the route with the fewest links. On one deployment it returns a direct link across a region boundary, with one charge. A longer route of three links stays inside one region and costs nothing. The search picked the wrong route because it counted links, and the bill counts only charges.

Dijkstra's method from earlier in this chapter solves the problem for any nonnegative charges. A heap costs O(log V) per operation, and here every charge is 0 or 1. A request graph can have millions of links, and the heap becomes the main cost of the planner.

This lesson asks how a search can keep routes in order of total charge without any heap, when every edge costs exactly 0 or 1.

<!-- stage: contributions -->
### What Four Lessons And One Chapter Add

Four lessons of this chapter and the deque chapter supply the pieces. Dijkstra supplies the array `dist` that holds the best known cost of each vertex, and the improvement test `dist[u] + w < dist[v]`. A vertex is final when the search removes it with its best cost. Stale Heap Entries supplies the rule that duplicate entries are legal, and that an entry whose cost is larger than the stored `dist` is skipped at removal.

Node-State Search supplies the habit of treating any position, such as a grid cell, as a vertex with its own entry in `dist`. The grid exercises below use this directly. Zero-One BFS supplies the central trick of choosing the deque end from the edge weight. Chapter 13 supplies the `ArrayDeque` operations `pollFirst`, `addFirst` and `addLast`, each at constant cost.

The combination adds one fact to these parts. When every weight is 0 or 1, the deque never holds more than two distinct costs, so the order of the entries stays sorted without comparisons. The nearest false friend is the visited flag of ordinary BFS, which freezes a vertex at its first cost, even when a later zero-cost route is cheaper.

<!-- stage: naive -->
### Marking Vertices The Way BFS Does

The direct plan reuses the queue of ordinary BFS. The search marks a vertex when it first sees it, and it stores the cost of the edge that found it. It never revisits a marked vertex.

```java
static int[] firstSeenCost(List<List<int[]>> adj, int src) {
    int[] cost = new int[adj.size()];
    Arrays.fill(cost, -1);
    cost[src] = 0;
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(src);
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        for (int[] edge : adj.get(cur)) {
            if (cost[edge[0]] != -1) continue;       // a marked vertex keeps its first cost
            cost[edge[0]] = cost[cur] + edge[1];
            queue.add(edge[0]);
        }
    }
    return cost;
}
```

Each entry of `adj.get(u)` is a pair `{target, weight}`. The method reads every edge once. The question is whether the first cost that a vertex receives is also its smallest.

```predict
The edges are 0 to 3 with weight 1, 0 to 1 with weight 0, 1 to 2 with weight 0 and 2 to 3 with weight 0. What does firstSeenCost store for vertex 3?

It stores 1, but the smallest cost is 0. Vertex 0 scans the edge to 3 first and marks vertex 3 with cost 1. The route through 1 and 2 costs 0 and reaches vertex 3 later, where the mark blocks the update. The first sighting follows the fewest edges, and the cost follows the weights.
```

<!-- stage: bottleneck -->
### Edge Count And Cost Disagree

The method runs in O(V + E), and the time is not the problem. The answer is wrong, because the queue order follows the number of edges, while the answer follows the sum of weights. A vertex that is two edges away at cost 0 loses against a vertex that is one edge away at cost 1.

The repair from the earlier lessons is to drop the mark and keep a distance array. The search then accepts a later route that lowers the stored distance. With a plain queue, this repair needs a priority order, because a vertex must be processed only after every cheaper vertex. A heap gives that order at a price of O(E log V) for the whole search.

The weights offer a shortcut. A heap must handle arbitrary costs, but the entries here differ by at most one in cost at any time. A structure that keeps the cheaper entries ahead of the dearer ones, and that costs O(1) per insertion, would bring the total back to O(V + E). The next stage explains why a deque has that property.

<!-- stage: insight -->
### Two Deque Ends Keep The Order

The search keeps the `dist` array of Dijkstra and adds a deque in place of the heap.

<!-- names: relaxation, addFirst, addLast -->

#### What One Relaxation Does

A **relaxation** of the edge from `u` to `v` with weight `w` tests whether `dist[u] + w` is smaller than `dist[v]`. When it is, the method stores the smaller value and inserts an entry for `v`. The entry holds the vertex and the cost at the moment of insertion. The deque holds entries, and a vertex can own several entries at once.

#### Why Two Costs Are Enough

Suppose the front entry has cost `d`. The deque is sorted, so every entry has a cost of at least `d`. Every entry was created by a relaxation from a vertex of cost `d` or from one of cost `d - 1` that was removed earlier, so its cost is at most `d + 1`. The deque therefore holds only the costs `d` and `d + 1`, with all entries of cost `d` ahead of all entries of cost `d + 1`.

#### Choosing The End From The Weight

A relaxation with weight 0 creates an entry of cost `d`, and `addFirst` places it before the entries of cost `d + 1` and keeps the sorted order. A relaxation with weight 1 creates an entry of cost `d + 1`, and `addLast` places it behind every entry that exists. Both insertions keep the deque sorted, so the removal at the front always takes a smallest cost, as the heap did.

#### Stale Entries And The Push Bound

A vertex can first receive cost `d + 1` at the back and later cost `d` at the front. The old entry stays in the deque. The search compares the cost in the removed entry with `dist` and skips the entry when it is larger. A second entry for a vertex appears only through such an improvement. The cost can drop only from `d + 1` to `d`, so no vertex ever owns more than two entries, and the total number of insertions is at most 2V. The invariant that the search maintains is the sorted order together with the two-cost limit, and it lets the whole search finish in linear time.

<!-- stage: variables -->
### What The Search Keeps

The search reads the adjacency list `adj` and the source `src`, and it changes neither. Four items hold the state.

- **dist** is an `int[]` with one entry for each vertex; the value is the best known cost, and a large sentinel marks a vertex not yet reached.
- **deque** is an `ArrayDeque<int[]>` of pairs `{vertex, cost}` sorted by cost from front to back.
- **cur** is the vertex of the entry that was just removed from the front.
- **edge** is one pair `{target, weight}` of `adj.get(cur)`, and the weight is 0 or 1.

A grid uses the same structure with the vertex number `row * columns + col`.

<!-- stage: trace -->
### Watching The Deque On Two Inputs

#### An Explicit Graph With A Stale Entry

The first input has five vertices and the edges 0 to 3 with weight 1, 0 to 1 with weight 0, 1 to 3 with weight 0, 3 to 4 with weight 1 and 1 to 2 with weight 1. The cell row shows the vertex ids, and the pointer `cur` marks the vertex of the event. The variable `dist` lists the stored costs of vertices 0 to 4, where `x` means not reached. The variable `deque` lists the entries as `vertex@cost` from the front to the back. Vertex 3 first receives cost 1 from vertex 0 at the back. Later it receives cost 0 through vertex 1 at the front, and the old entry becomes stale and is discarded when it reaches the front.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":"0-x-x-x-x","deque":"0@0"},"note":"The search stores distance 0 for the source and puts the entry for vertex 0 in the deque."},{"at":{"cur":0},"vars":{"dist":"0-x-x-x-x","deque":"empty"},"note":"The search takes vertex 0 from the front with distance 0."},{"at":{"cur":0},"vars":{"dist":"0-x-x-1-x","deque":"3@1"},"note":"The edge from 0 to 3 costs 1 and improves vertex 3 to 1, so its entry goes to the back."},{"at":{"cur":0},"vars":{"dist":"0-0-x-1-x","deque":"1@0-3@1"},"note":"The edge from 0 to 1 costs 0 and improves vertex 1 to 0, so its entry goes to the front."},{"at":{"cur":1},"vars":{"dist":"0-0-x-1-x","deque":"3@1"},"note":"The search takes vertex 1 from the front with distance 0."},{"at":{"cur":1},"vars":{"dist":"0-0-x-0-x","deque":"3@0-3@1"},"note":"The edge from 1 to 3 costs 0 and improves vertex 3 to 0, so its entry goes to the front."},{"at":{"cur":1},"vars":{"dist":"0-0-1-0-x","deque":"3@0-3@1-2@1"},"note":"The edge from 1 to 2 costs 1 and improves vertex 2 to 1, so its entry goes to the back."},{"at":{"cur":3},"vars":{"dist":"0-0-1-0-x","deque":"3@1-2@1"},"note":"The search takes vertex 3 from the front with distance 0."},{"at":{"cur":3},"vars":{"dist":"0-0-1-0-1","deque":"3@1-2@1-4@1"},"note":"The edge from 3 to 4 costs 1 and improves vertex 4 to 1, so its entry goes to the back."},{"at":{"cur":3},"vars":{"dist":"0-0-1-0-1","deque":"2@1-4@1"},"note":"The front entry for vertex 3 carries distance 1, but the stored distance is 0, so the search discards it."},{"at":{"cur":2},"vars":{"dist":"0-0-1-0-1","deque":"4@1"},"note":"The search takes vertex 2 from the front with distance 1."},{"at":{"cur":4},"vars":{"dist":"0-0-1-0-1","deque":"empty"},"note":"The search takes vertex 4 from the front with distance 1."}]}
```

#### A Grid With Arrows

The second input is a grid with two rows and three columns. Arrow codes 1, 2, 3 and 4 mean right, left, down and up. A move in the arrow direction costs 0, and a move in any other direction costs 1. The cells list the arrow codes in row order, and the pointer `cell` marks the index `row * 3 + col`. The goal is the bottom right cell, which is index 5, and the vertex number of a cell equals its index. Zero-cost moves jump ahead of the cost 1 entries that already wait. Cells 4 and 5 each receive a second entry of cost 2 before a zero-cost move improves them, and both old entries end as stale.

```trace
{"cells":[2,1,1,1,1,3],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"dist":"0-x-x-x-x-x","deque":"0@0"},"note":"The search stores distance 0 for the source and puts the entry for vertex 0 in the deque."},{"at":{"cell":0},"vars":{"dist":"0-x-x-x-x-x","deque":"empty"},"note":"The search takes vertex 0 from the front with distance 0."},{"at":{"cell":0},"vars":{"dist":"0-1-x-x-x-x","deque":"1@1"},"note":"The edge from 0 to 1 costs 1 and improves vertex 1 to 1, so its entry goes to the back."},{"at":{"cell":0},"vars":{"dist":"0-1-x-1-x-x","deque":"1@1-3@1"},"note":"The edge from 0 to 3 costs 1 and improves vertex 3 to 1, so its entry goes to the back."},{"at":{"cell":1},"vars":{"dist":"0-1-x-1-x-x","deque":"3@1"},"note":"The search takes vertex 1 from the front with distance 1."},{"at":{"cell":1},"vars":{"dist":"0-1-1-1-x-x","deque":"2@1-3@1"},"note":"The edge from 1 to 2 costs 0 and improves vertex 2 to 1, so its entry goes to the front."},{"at":{"cell":1},"vars":{"dist":"0-1-1-1-2-x","deque":"2@1-3@1-4@2"},"note":"The edge from 1 to 4 costs 1 and improves vertex 4 to 2, so its entry goes to the back."},{"at":{"cell":2},"vars":{"dist":"0-1-1-1-2-x","deque":"3@1-4@2"},"note":"The search takes vertex 2 from the front with distance 1."},{"at":{"cell":2},"vars":{"dist":"0-1-1-1-2-2","deque":"3@1-4@2-5@2"},"note":"The edge from 2 to 5 costs 1 and improves vertex 5 to 2, so its entry goes to the back."},{"at":{"cell":3},"vars":{"dist":"0-1-1-1-2-2","deque":"4@2-5@2"},"note":"The search takes vertex 3 from the front with distance 1."},{"at":{"cell":3},"vars":{"dist":"0-1-1-1-1-2","deque":"4@1-4@2-5@2"},"note":"The edge from 3 to 4 costs 0 and improves vertex 4 to 1, so its entry goes to the front."},{"at":{"cell":4},"vars":{"dist":"0-1-1-1-1-2","deque":"4@2-5@2"},"note":"The search takes vertex 4 from the front with distance 1."},{"at":{"cell":4},"vars":{"dist":"0-1-1-1-1-1","deque":"5@1-4@2-5@2"},"note":"The edge from 4 to 5 costs 0 and improves vertex 5 to 1, so its entry goes to the front."},{"at":{"cell":5},"vars":{"dist":"0-1-1-1-1-1","deque":"4@2-5@2"},"note":"The search takes vertex 5 from the front with distance 1."},{"at":{"cell":4},"vars":{"dist":"0-1-1-1-1-1","deque":"5@2"},"note":"The front entry for vertex 4 carries distance 2, but the stored distance is 1, so the search discards it."},{"at":{"cell":5},"vars":{"dist":"0-1-1-1-1-1","deque":"empty"},"note":"The front entry for vertex 5 carries distance 2, but the stored distance is 1, so the search discards it."}]}
```

<!-- stage: code -->
### Zero-One Search With A Deque

The method returns the cost of every vertex, with `-1` for a vertex that no path reaches. It stores the pair `{vertex, cost}` in each entry, so the stale test needs no extra array.

```java
static int[] zeroOneCosts(List<List<int[]>> adj, int src) {
    int n = adj.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[src] = 0;
    ArrayDeque<int[]> deque = new ArrayDeque<>();
    deque.addFirst(new int[] {src, 0});
    while (!deque.isEmpty()) {
        int[] head = deque.pollFirst();
        int cur = head[0];
        if (head[1] > dist[cur]) continue;
        for (int[] edge : adj.get(cur)) {
            int next = edge[0];
            int cost = head[1] + edge[1];
            if (cost >= dist[next]) continue;
            dist[next] = cost;
            if (edge[1] == 0) deque.addFirst(new int[] {next, cost});
            else deque.addLast(new int[] {next, cost});
        }
    }
    for (int v = 0; v < n; v++) if (dist[v] == Integer.MAX_VALUE) dist[v] = -1;
    return dist;
}
```

The test `cost >= dist[next]` uses a strict improvement, so a zero-cost cycle stops after one lap. The method runs in O(V + E) time, because each vertex has at most two entries and each entry scans its edges once. The memory is O(V + E) for the lists and the deque. The sentinel `Integer.MAX_VALUE` never takes part in an addition, because only reached vertices are removed from the deque.

<!-- stage: applicability -->
### Recognizing Zero-One Problems

#### Reading The Cue

Use the deque search when a shortest-path question has edge costs that are exactly 0 or 1, or that can be reduced to those two values. A grid where moving along a marked direction is free and any other move costs one unit has this shape. So does a grid where entering an empty cell is free and entering an obstacle costs one removal. A graph with a flag on each edge, such as "crosses a boundary", also fits.

#### Checking The Invariant

The invariant says that entries stay in cost order and that only two neighboring cost values coexist. It breaks when one edge has weight 2 or more, because an entry could land in the middle of the deque. It also breaks when the zero-cost entry goes to the back or the one-cost entry goes to the front. Check the weights of the input before choosing this method, and fall back to the heap method for other values.

#### Avoiding The False Friend

The false friend is ordinary BFS with a visited flag. It gives the right answer only when every edge costs 1, and the disguised cases are those with free moves. A second false friend is early exit at the first removal of the goal in code that skips the stale test. Stopping when the goal leaves the deque with its final cost is safe, but stopping when it enters the deque is not.

<!-- stage: exercises -->
### Exercises

#### [Build] Zero-One Relaxation (Author exercise)
<!-- id: sp-zero-one-relaxation -->

**Prerequisites.** The deque search of this lesson.

**Problem.** A directed graph has the vertices `0` to `n - 1`. The list `edges` holds triples `[a, b, w]`, each an edge from `a` to `b` with weight `w`, where `w` is 0 or 1. Given a source vertex `src`, return an `int[]` of length `n`. Entry `v` is the minimum total weight of a path from `src` to `v`, or `-1` when no path exists.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 6000`, and repeats and self loops may occur.
- **Weights** are 0 or 1, and zero-weight cycles may occur.
- **Source** satisfies `0 <= src < n`, and its entry is 0.

**Example 1.** Input `n = 4`, `edges = [[0,1,1],[0,2,0],[2,1,0],[1,3,1]]`, `src = 0`, output `[0,0,0,1]`.

**Example 2.** Input `n = 5`, `edges = [[0,1,0],[1,2,0],[2,1,0],[0,3,1],[3,2,1]]`, `src = 0`, output `[0,0,0,1,-1]`.

**Hint.** Which end of the deque keeps a zero-cost improvement ahead of the entries that cost one more?

**Changed decision.** The method inserts an improved vertex at the front for weight 0 and at the back for weight 1, and it updates a vertex only on strict improvement.

#### [Vary] Minimum Cost To Make At Least One Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-arrow-grid-ties -->

**Prerequisites.** The exercise above.

**Problem.** A grid `grid` has `m` rows and `n` columns, and each cell holds an arrow code: 1 right, 2 left, 3 down, 4 up. A move goes to one of the four neighbors inside the grid. A move in the direction of the current cell's arrow costs 0, and a move in any other direction costs 1. Let `best[r][c]` be the minimum total cost of a path from cell `(0, 0)` to cell `(r, c)`. Return an `int[]` of length 2. Entry 0 is `best[m-1][n-1]`. Entry 1 is the number of cells, including the bottom right cell, whose `best` value equals entry 0.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 60`.
- **Codes** are integers from 1 to 4.
- **Cost** counts each cost-1 move once, and the path may pass a cell twice.
- **Result** has entry 1 at least 1.

**Example 1.** Input `grid = [[1,2],[4,3]]`, output `[1,2]`.

**Example 2.** Input `grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]`, output `[3,4]`.

**Hint.** Why does stopping the search at the first removal of the bottom right cell give a wrong second entry?

**Changed decision.** The method reads the whole `best` table, so it runs until the deque is empty and counts the cells equal to the goal cost.

#### [Boundary] Minimum Obstacle Removal To Reach Corner (LeetCode 2290)
<!-- id: sp-obstacle-corner -->

**Prerequisites.** The two exercises above.

**Problem.** A grid `grid` of 0 and 1 has `m` rows and `n` columns. A cell with value 1 holds an obstacle, and a cell with value 0 is empty. A move steps to a cell above, below, left or right of the current cell, inside the grid. Entering a cell costs its value, and the start cell `(0, 0)` costs nothing because the path begins there. Return the minimum total cost of a path from `(0, 0)` to `(m-1, n-1)`, which equals the fewest obstacle cells that the path enters.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 100`.
- **Values** are 0 or 1, and the start and the goal cell may hold 1.
- **Single cell** grids occur, and the answer for them is 0.
- **Charge** applies to the destination cell of each move, including the goal.

**Example 1.** Input `grid = [[0,1,1],[1,1,0],[1,1,0]]`, output `2`.

**Example 2.** Input `grid = [[1,1],[1,1]]`, output `2`.

**Hint.** Is the cost of a move decided by the cell that the move leaves or by the cell that it enters?

**Changed decision.** The method derives the weight of each move from the value of the destination cell, and it never charges the start cell.

#### [Recognize] Minimum Zero-One Toll (Author exercise)
<!-- id: sp-zero-one-toll -->

**Prerequisites.** All three exercises above.

**Problem.** A road network has the junctions `0` to `n - 1`. The list `roads` holds triples `[a, b, t]`, each an undirected road between `a` and `b` with toll `t`, where `t` is 0 or 1. A trip may use a road in both directions. Return the minimum total toll of a trip from junction `0` to junction `n - 1`, or `-1` when no trip exists.

**Constraints.** The limits are:
- **Junctions** satisfy `1 <= n <= 5000`.
- **Roads** satisfy `0 <= roads.length <= 20000`, and parallel roads and self loops may occur.
- **Tolls** are 0 or 1.
- **Single junction** networks have the answer 0.

**Example 1.** Input `n = 5`, `roads = [[0,1,1],[1,4,0],[0,2,0],[2,3,1],[3,4,0],[2,2,1]]`, output `1`.

**Example 2.** Input `n = 4`, `roads = [[0,1,1],[2,3,0]]`, output `-1`.

**Hint.** Which fact about the tolls lets a deque replace the heap, and what must each road add to the adjacency list?

**Changed decision.** The method stores every road in both directions, and it reads the answer at the target or reports -1 when the target keeps its sentinel.
