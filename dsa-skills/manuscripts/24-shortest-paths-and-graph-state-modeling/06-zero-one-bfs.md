<!-- lesson-kind: standard -->
<!-- lesson-id: zero-one-bfs -->
## Search With Zero And One Costs

<!-- stage: context -->
### Counting Only The Paid Links

A network planner measures how many paid switch crossings a packet needs between two machines. Links inside one rack are free, and a link that leaves the rack costs one crossing. One route from machine A to machine B uses a single paid link and six free links. A second route uses two paid links and nothing else. A breadth-first search that counts links ranks the second route first, since it has two links against seven. The planner then reports two crossings, while the real minimum is one.

Model the machines as vertices and the links as directed edges with a cost of exactly 0 or exactly 1. The cost of a path is the sum of its edge costs, and the task is to find the smallest cost from a start vertex to every other vertex. Earlier lessons in this chapter solved weighted problems with a priority queue, which orders candidates at a price of a logarithmic factor per operation.

This lesson asks how a search can keep candidates in cost order when only two edge costs exist, so that the logarithmic factor disappears.

<!-- stage: naive -->
### Running Breadth-First Search On Costs

The first attempt reuses the ordinary queue search from the graph chapters. It stores the distance of a vertex when the vertex is first reached and never changes that value.

```java
static int[] bfsCost(int n, List<List<int[]>> adj) {
    int[] dist = new int[n];
    Arrays.fill(dist, -1);
    dist[0] = 0;
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(0);
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        for (int[] edge : adj.get(cur)) {
            if (dist[edge[0]] == -1) {
                dist[edge[0]] = dist[cur] + edge[1];
                queue.add(edge[0]);
            }
        }
    }
    return dist;
}
```

Each entry of `adj.get(u)` holds the end vertex and the cost. The method adds the cost where a plain search would add 1. It works when all costs are 1. The question is what happens when a free edge exists.

```predict
Take the edges 0 to 1 with cost 1, 0 to 2 with cost 0, 2 to 3 with cost 0 and 3 to 1 with cost 0. What does bfsCost store for vertex 1?

It stores 1, which is wrong, because the route 0, 2, 3, 1 costs 0. The search reaches vertex 1 directly from vertex 0 and fixes its distance at once. The cheaper route is found later through vertices 2 and 3, but the test dist[edge[0]] == -1 is already false, so the improvement is ignored.
```

<!-- stage: bottleneck -->
### First Arrival Is Not The Cheapest Arrival

The method runs in O(V + E) time, so speed is not the defect. The defect is the rule that the first arrival fixes the answer. In a search over edge counts, the first arrival uses the fewest edges, because the queue releases vertices in order of edge count. With costs, a vertex reached by one paid edge may also be reachable by many free edges, and the free route arrives later in queue order but with a smaller sum.

A repair exists from the previous lessons. A priority queue releases the smallest cost first, so the first arrival at the front of the queue is the cheapest. That repair costs O(E log V) time, because every accepted improvement is one heap insertion of O(log V). For a grid with a million cells, the extra factor is about twenty comparisons per insertion, and the structure needs a comparator and an object for each entry.

The structure that the repair needs is weaker than a heap. It must release candidates in nondecreasing cost order, and two costs exist. The next stage shows that a double-ended queue is enough.

<!-- stage: insight -->
### One Deque Holds Two Neighboring Costs

A plain queue orders entries by arrival and a heap orders them by cost. Two edge costs allow a cheaper structure that still orders by cost.

<!-- names: deque, tentative, nondecreasing -->

#### The Best Distance Found So Far

A **tentative** distance of a vertex is the smallest cost of any path that the search has found to it so far. The array `dist` stores it. A tentative distance only decreases, and it becomes final when the search takes the vertex from the front, as the next part shows. The search pushes an entry `(vertex, distance)` each time an edge lowers `dist` of its end vertex.

#### Two Ends For Two Costs

A **deque** is a double-ended queue that adds and removes entries at both ends in O(1). The search always removes from the front. Suppose the front entry has distance `d`. A zero-cost edge from it gives the end vertex distance `d`, so the new entry belongs before every entry with a larger distance, and the search pushes it at the front. A one-cost edge gives `d + 1`, which is not smaller than any distance in the deque, so the search pushes it at the back.

#### Why Order Is Kept

The invariant is that the distances in the deque are **nondecreasing** from front to back, and they take at most two values, `d` and `d + 1`. Removing the front entry keeps the order. A front push of value `d` keeps it, because the front was already at least `d`. A back push of value `d + 1` keeps it, because no entry is larger. Since entries leave in nondecreasing order, the first non-stale removal of a vertex carries its smallest cost.

#### Handling Superseded Entries

A vertex can sit in the deque twice. It first enters at the back with distance `d + 1`, and later a zero-cost path pushes it at the front with distance `d`. The search compares the distance of a removed entry with `dist` and skips the entry when it is larger. The strict test `nd < dist[v]` before each push also rejects equal costs, so a cycle of zero-cost edges stops after one lap. Each vertex enters the deque at most twice, which gives O(V + E) time.

<!-- stage: variables -->
### What The Search Keeps

The search reads `n` and the edge list and changes neither. It builds an adjacency list in the order of the edges, where each entry holds an end vertex and a cost of 0 or 1. Three structures carry the state.

- **dist** is an `int[]` of length `n`, filled with `Integer.MAX_VALUE` as the unreached value, and `dist[0] = 0`.
- **deque** is an `ArrayDeque<int[]>` of pairs `{vertex, distance}`, with the smallest distance at the front.
- **cur** is the vertex of the entry that the search removed last, and its edges are scanned in list order.

The sum `d + cost` involves only a finite `d`, because the search never scans edges of an unreached vertex. The value `Integer.MAX_VALUE` therefore never overflows, and distances stay below `n`.

<!-- stage: trace -->
### Pushing At Both Ends On Two Graphs

#### A Free Route Beats A Direct Edge

The first graph has the edges 0 to 1 with cost 1, 0 to 2 with cost 0, 2 to 3 with cost 0, 3 to 1 with cost 0 and 1 to 4 with cost 1. This is the graph of the earlier prediction. Each cell holds a vertex id, and the pointer `cur` marks the vertex of the event. The variable `dist` lists the distances of vertices 0 to 4, with `inf` for unreached ones, and `deque` lists the entries as `vertex:distance` from front to back. At step 4 the free edge from 0 to 2 goes to the front, so vertex 2 is taken before vertex 1. At step 8 the free edge from 3 to 1 lowers `dist` of vertex 1 from 1 to 0 and puts a second entry for it at the front. At step 11 the old entry of vertex 1 reaches the front and is skipped.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":"0 inf inf inf inf","deque":"0:0"},"note":"The deque holds the start vertex 0 with distance 0."},{"at":{"cur":0},"vars":{"dist":"0 inf inf inf inf","deque":"empty"},"note":"The search takes vertex 0 with distance 0 from the front and scans its edges."},{"at":{"cur":0},"vars":{"dist":"0 1 inf inf inf","deque":"1:1"},"note":"The edge from 0 to 1 costs 1 and gives distance 1, which is an improvement, so the search pushes vertex 1 at the back."},{"at":{"cur":0},"vars":{"dist":"0 1 0 inf inf","deque":"2:0 1:1"},"note":"The edge from 0 to 2 costs 0 and gives distance 0, which is an improvement, so the search pushes vertex 2 at the front."},{"at":{"cur":2},"vars":{"dist":"0 1 0 inf inf","deque":"1:1"},"note":"The search takes vertex 2 with distance 0 from the front and scans its edges."},{"at":{"cur":2},"vars":{"dist":"0 1 0 0 inf","deque":"3:0 1:1"},"note":"The edge from 2 to 3 costs 0 and gives distance 0, which is an improvement, so the search pushes vertex 3 at the front."},{"at":{"cur":3},"vars":{"dist":"0 1 0 0 inf","deque":"1:1"},"note":"The search takes vertex 3 with distance 0 from the front and scans its edges."},{"at":{"cur":3},"vars":{"dist":"0 0 0 0 inf","deque":"1:0 1:1"},"note":"The edge from 3 to 1 costs 0 and gives distance 0, which is an improvement, so the search pushes vertex 1 at the front."},{"at":{"cur":1},"vars":{"dist":"0 0 0 0 inf","deque":"1:1"},"note":"The search takes vertex 1 with distance 0 from the front and scans its edges."},{"at":{"cur":1},"vars":{"dist":"0 0 0 0 1","deque":"1:1 4:1"},"note":"The edge from 1 to 4 costs 1 and gives distance 1, which is an improvement, so the search pushes vertex 4 at the back."},{"at":{"cur":1},"vars":{"dist":"0 0 0 0 1","deque":"4:1"},"note":"The entry for vertex 1 carries distance 1, but the best known distance is 0, so the search skips it."},{"at":{"cur":4},"vars":{"dist":"0 0 0 0 1","deque":"empty"},"note":"The search takes vertex 4 with distance 1 from the front and scans its edges."}]}
```

#### A Cycle Of Free Edges

The second graph has the edges 0 to 1 with cost 1, 0 to 2 with cost 1, 1 to 2 with cost 0, 2 to 1 with cost 0 and 2 to 3 with cost 1. Vertices 1 and 2 form a cycle of free edges. At step 6 the edge from 1 to 2 gives distance 1, which equals `dist` of vertex 2, so the strict test discards it. At step 8 the edge back from 2 to 1 is discarded in the same way. The cycle ends without a visited flag, and the search takes vertex 3 at step 10.

```trace
{"cells":[0,1,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"dist":"0 inf inf inf","deque":"0:0"},"note":"The deque holds the start vertex 0 with distance 0."},{"at":{"cur":0},"vars":{"dist":"0 inf inf inf","deque":"empty"},"note":"The search takes vertex 0 with distance 0 from the front and scans its edges."},{"at":{"cur":0},"vars":{"dist":"0 1 inf inf","deque":"1:1"},"note":"The edge from 0 to 1 costs 1 and gives distance 1, which is an improvement, so the search pushes vertex 1 at the back."},{"at":{"cur":0},"vars":{"dist":"0 1 1 inf","deque":"1:1 2:1"},"note":"The edge from 0 to 2 costs 1 and gives distance 1, which is an improvement, so the search pushes vertex 2 at the back."},{"at":{"cur":1},"vars":{"dist":"0 1 1 inf","deque":"2:1"},"note":"The search takes vertex 1 with distance 1 from the front and scans its edges."},{"at":{"cur":1},"vars":{"dist":"0 1 1 inf","deque":"2:1"},"note":"The edge from 1 to 2 costs 0 and gives distance 1, which does not beat 1, so the search discards it."},{"at":{"cur":2},"vars":{"dist":"0 1 1 inf","deque":"empty"},"note":"The search takes vertex 2 with distance 1 from the front and scans its edges."},{"at":{"cur":2},"vars":{"dist":"0 1 1 inf","deque":"empty"},"note":"The edge from 2 to 1 costs 0 and gives distance 1, which does not beat 1, so the search discards it."},{"at":{"cur":2},"vars":{"dist":"0 1 1 2","deque":"3:2"},"note":"The edge from 2 to 3 costs 1 and gives distance 2, which is an improvement, so the search pushes vertex 3 at the back."},{"at":{"cur":3},"vars":{"dist":"0 1 1 2","deque":"empty"},"note":"The search takes vertex 3 with distance 2 from the front and scans its edges."}]}
```

<!-- stage: code -->
### Zero-One Search With A Deque

The method returns the distance array, with -1 for a vertex that the start cannot reach. The caller passes edges as triples `{from, to, cost}`.

```java
static int[] zeroOneDist(int n, int[][] edges) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[0] = 0;
    ArrayDeque<int[]> deque = new ArrayDeque<>();
    deque.addLast(new int[] {0, 0});
    while (!deque.isEmpty()) {
        int[] top = deque.pollFirst();
        int cur = top[0];
        if (top[1] > dist[cur]) continue;
        for (int[] edge : adj.get(cur)) {
            int next = edge[0];
            int cand = top[1] + edge[1];
            if (cand < dist[next]) {
                dist[next] = cand;
                if (edge[1] == 0) deque.addFirst(new int[] {next, cand});
                else deque.addLast(new int[] {next, cand});
            }
        }
    }
    for (int v = 0; v < n; v++) if (dist[v] == Integer.MAX_VALUE) dist[v] = -1;
    return dist;
}
```

The Java names matter here. On `ArrayDeque`, the method `push` adds at the front and `add` adds at the back, so a reader who mixes them swaps the two cases silently. The code spells out `addFirst` and `addLast` for that reason. The method runs in O(V + E) time, because each vertex enters the deque at most twice and each edge is scanned once per removal that is not skipped. It uses O(V + E) memory for the adjacency list and the deque.

<!-- stage: applicability -->
### Recognizing Zero-One Cost Problems

#### Reading The Cue

Use this search when every edge costs 0 or 1 and the task asks for the minimum total cost. Typical statements charge for a change and nothing for a continuation: turning a direction, removing an obstacle, switching a line or crossing a boundary. A grid where entering one kind of cell costs 0 and another kind costs 1 has this shape. Unreached cells appear as unreached entries of `dist`, and the answer is a single entry.

#### Checking The Invariant

The invariant is that the deque is nondecreasing from front to back and spans at most two consecutive values. It holds only if the push end follows the edge cost, and a one-cost edge never goes to the front. It also needs the strict improvement test. A test that compares `cand <= dist[next]` pushes equal entries again, and a zero-cost cycle then never leaves the loop.

#### Avoiding The False Friend

The false friend is ordinary breadth-first search, which counts edges, and a visited flag set on the first push. A flag fixes a distance that a later free route can still lower. A second false friend is a heap, which also gives the right answer, but it pays a logarithmic factor that the two-end structure avoids. The method is wrong once a third cost appears, such as 2, because the deque would then hold more than two distinct values and a back push could break the order.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Deque End By Weight (Author exercise)
<!-- id: sp-zero-one-end -->

**Prerequisites.** The deque search of this lesson.

**Problem.** A directed graph has vertices `0` to `n - 1`, and `edges` lists entries `[a, b, w]`, each an edge from `a` to `b` with cost `w`, where `w` is 0 or 1. The search starts with the entry `(0, 0)` in a deque. It removes the front entry `(u, d)` and skips it when `d` exceeds the best known distance of `u`. Otherwise it records `u`, then scans the entries of `edges` that start at `u` in list order. For an entry with end `v` and cost `w`, it computes `d + w`. When that value is smaller than the best known distance of `v`, it stores the value and adds `(v, d + w)` at the front when `w` is 0 and at the back when `w` is 1. Return the recorded vertices in order as an `int[]`.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Costs** are only 0 or 1.
- **Result** lists each reachable vertex once, and the start vertex comes first.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,1]]`, output `[0,2,3,1,4]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,1],[0,2,1],[1,3,1]]`, output `[0,1,2,3]`.

**Hint.** After the start vertex is removed, which of its two edges lands at the front of the deque?

**Changed decision.** The method picks the end of the deque from the edge cost and removes only from the front.

#### [Vary] Reject Nonimproving Relaxations (Author exercise)
<!-- id: sp-reject-nonimproving -->

**Prerequisites.** The exercise above.

**Problem.** Consider vertices `0` to `n - 1` and a list `edges` of entries `[a, b, w]`, each a directed edge from `a` to `b` with cost `w` in `{0, 1}`. Return an `int[]` `dist` of length `n`, where `dist[v]` is the smallest sum of costs over all paths from vertex 0 to `v`, and `-1` when no path exists. The array `dist` starts at an unreached value for every vertex except `dist[0] = 0`, and an edge is applied only when it gives a strictly smaller value.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Costs** are only 0 or 1.
- **Result** holds `-1` for every vertex that vertex 0 cannot reach.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,1]]`, output `[0,0,0,0,1]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,1],[2,3,0]]`, output `[0,1,-1,-1]`.

**Hint.** When vertex 1 receives distance 1 first and 0 later, which entry of the deque must the search ignore?

**Changed decision.** The method returns the distance array of the search and reads no order, and it replaces a visited flag with the strict comparison against `dist`.

#### [Boundary] Zero-Cost Cycle (Author exercise)
<!-- id: sp-zero-cost-cycle -->

**Prerequisites.** The two exercises above.

**Problem.** A directed graph has vertices `0` to `n - 1`, and `edges` lists entries `[a, b, w]` with `w` equal to 0 or 1. Let `dist[v]` be the smallest sum of costs over all paths from vertex 0 to `v`. Return an `int[]` of length 2. Its first entry is the number of vertices with `dist[v] = 0`, and its second entry is `dist[n - 1]`, or `-1` when vertex `n - 1` is unreachable.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and cycles of cost 0 may occur.
- **Self loops** with cost 0 may occur and never change a distance.
- **Result** counts vertex 0 in its first entry.

**Example 1.** Input `n = 4`, `edges = [[0,1,0],[1,0,0],[1,2,1],[2,3,0],[3,2,0]]`, output `[2,1]`.

**Example 2.** Input `n = 3`, `edges = [[0,0,0],[0,1,1],[1,1,0]]`, output `[1,-1]`.

**Hint.** What does the search do with the edge from vertex 1 back to vertex 0, whose sum equals the stored distance?

**Changed decision.** The method accepts an edge only when the sum is strictly smaller than the stored distance, and it computes two summary values from the final array.

#### [Recognize] Minimum Cost To Make A Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-grid-valid-path -->

**Prerequisites.** All three exercises above.

**Problem.** A grid `grid` has `m` rows and `n` columns. Each cell holds an arrow code: 1 points right, 2 points left, 3 points down and 4 points up. A move goes from a cell to the adjacent cell in any of the four directions inside the grid. A move in the direction of the arrow of its start cell costs 0, and a move in any other direction costs 1. Return the smallest total cost of a path from the cell `(0, 0)` to the cell `(m - 1, n - 1)`.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 100`.
- **Codes** are integers from 1 to 4.
- **Single cell** grids occur and give 0.
- **Arrows** never change, and a path may revisit cells.

**Example 1.** Input `grid = [[3,3,2],[1,4,4],[2,1,1]]`, output `1`.

**Example 2.** Input `grid = [[4,4],[4,4]]`, output `2`.

**Hint.** Which cells does a free move from the start reach before any paid move is taken?

**Changed decision.** The method derives each edge cost from the cell code and the move direction, and it applies the deque search to the grid cells as vertices.
