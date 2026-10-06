<!-- lesson-kind: standard -->
<!-- lesson-id: kruskal-foundations -->
## Kruskal Foundations

<!-- stage: context -->
### Why Cheap Links Alone Fail

A platform team must connect six data centers with private fiber. Every possible link between two centers has a quoted price, and the team wants every center reachable from every other at the lowest total price. An engineer sorts the quotes from cheapest to dearest and buys links from the top of the list. The first links are bargains. After five purchases, one center still has no link at all. Two of the purchased links form a loop that adds cost without adding reach.

The cheap quotes were not wrong. They concentrated between a few centers that already reached each other. A rule that looks only at price cannot tell whether a link connects something new. This lesson asks one question. How does a program decide, link by link, whether an edge is worth buying, and when does it know the purchases are complete?

<!-- stage: naive -->
### Buying The Cheapest Links

The direct plan sorts the edges by weight and takes the first `vertexCount - 1` of them. A network of `V` vertices needs at least `V - 1` links. Each edge is an array `{u, v, weight}`.

```java
static long cheapestLinksOnly(int vertexCount, int[][] edges) {
    int[][] sorted = edges.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
    long total = 0;
    for (int i = 0; i < vertexCount - 1; i++) {
        total += sorted[i][2];                       // take the next cheapest edge without looking at its endpoints
    }
    return total;
}
```

The method is short and fast, and it returns a plausible number on many inputs. It never looks at the endpoints of an edge.

```predict
A graph has 4 vertices and the edges 0-1 with weight 1, 1-2 with weight 1, 0-2 with weight 1 and 2-3 with weight 5. What does the method return, and is the answer correct?

It returns 3, the sum of the three weight-1 edges. Those three edges all lie among vertices 0, 1 and 2, so vertex 3 stays unreachable. A correct plan needs two of the cheap edges plus the edge 2-3, for a total of 7.
```

<!-- stage: bottleneck -->
### The Cost Of Checking Every Edge

The method fails because price is the only test. A repair must test, before each purchase, whether the two endpoints are already connected by the edges bought so far. The first idea runs a graph search over the bought edges for every candidate. That search visits up to `V` vertices and `V - 1` edges, so it costs O(V) per candidate. The loop over `E` candidates then costs O(E * V) after the sort. The sort itself costs O(E log E).

Take a graph with 100,000 vertices and 200,000 edges. The repeated searches need about 2 * 10^10 steps in the worst case, which is far too slow. The sort needs only a few million comparisons. The sort is cheap and the connectivity test is the bottleneck.

The test asks the same question every time: do these two vertices already share a group? A search answers it by rediscovering the group from scratch. The program needs a structure that remembers each group and merges two groups in nearly constant time.

<!-- stage: insight -->
### Accept Edges That Join Groups

#### What The Result Looks Like

A **spanning tree** of a connected graph with `V` vertices is a set of exactly `V - 1` edges. The set connects all vertices and contains no cycle. A cycle is a closed route that returns to its start without repeating an edge. Every connected graph has at least one spanning tree, and the cheapest one is the answer to the question of the lesson. Fewer than `V - 1` edges cannot connect `V` vertices. More than `V - 1` edges must contain a cycle, and a cycle edge can be removed without breaking connectivity, so it only adds cost.

#### Why The Cheapest Valid Edge Is Safe

An edge is a **safe edge** when some cheapest spanning tree contains it together with all the edges accepted so far. The justification is the **cut property**. Split the vertices into two non-empty sets. Among the edges that cross the split, a lightest one belongs to some cheapest spanning tree.

Apply it as follows. Process the edges in increasing weight. Suppose the next edge joins group `A` to a different group. Every lighter edge was already examined. Each lighter edge either lies inside a group because the loop accepted it, or has both ends in one group because the loop rejected it. No accepted edge leaves `A`, and no rejected edge crosses the split between `A` and the other vertices. The current edge is therefore a lightest edge that crosses that split, so it is safe.

#### Telling Groups Apart With Union-Find

Union-find keeps one representative per group. The program calls `find` on both endpoints. Equal representatives mean the edge lies inside a group, so the program skips it, because it would close a cycle. Different representatives mean the edge joins two groups, so the program accepts it, adds the weight and merges the groups. After `V - 1` acceptances, the groups have merged into one and the program stops. A graph that runs out of edges before that point is disconnected.

<!-- names: spanning tree, safe edge, cut property -->

<!-- stage: variables -->
### What The Loop Keeps Between Edges

The loop keeps four values between edges, and the traces below show them under the same names. In both traces the pointer `i` marks the edge that the loop examines, and the cells hold the edge weights in sorted order.

- **sorted** holds the edges in nondecreasing weight, and ties keep the input order because `Arrays.sort` on objects is stable.
- **parent** and **size** form the union-find arrays, where `parent[x] == x` marks a representative.
- **accepted** counts the edges taken so far, and the loop stops when it equals `V - 1`.
- **total** adds the weights of accepted edges and has type `long`, because many `int` weights can sum past the `int` range.

<!-- stage: trace -->
### Tracing Kruskal On Two Graphs

#### A Connected Graph Of Six Vertices

The first trace runs on six vertices and nine edges. Each step shows the edge, the two representatives that `find` returns, and the decision. The `parent` array uses the rule that the smaller group attaches below the larger one, and a tie keeps the representative of the first endpoint.

The two cheapest edges, 1-2 and 1-3, join separate groups, so the loop accepts them. The next edge, 2-3, has endpoints that already share a representative, so the loop skips it. That skip is the check that the naive method lacks. The loop accepts its fifth edge, which equals `V - 1`, as the sixth edge it examines, and stops before it examines the remaining three. The total is the sum of the five accepted weights.

```trace
{"cells":[1,2,2,3,3,3,4,5,6],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"accepted":"0","total":"0","parent":"[0, 1, 2, 3, 4, 5]"},"note":"Start: 6 separate groups. The edges are sorted by weight and the loop needs 5 acceptances."},{"at":{"i":0},"vars":{"accepted":"1","total":"1","parent":"[0, 1, 1, 3, 4, 5]"},"note":"Edge 1-2 with weight 1: the representatives 2 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":1},"vars":{"accepted":"2","total":"3","parent":"[0, 1, 1, 1, 4, 5]"},"note":"Edge 1-3 with weight 2: the representatives 3 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":2},"vars":{"accepted":"2","total":"3","parent":"[0, 1, 1, 1, 4, 5]"},"note":"Edge 2-3 with weight 2: find returns 1 for both ends, so the edge is skipped."},{"at":{"i":3},"vars":{"accepted":"3","total":"6","parent":"[1, 1, 1, 1, 4, 5]"},"note":"Edge 0-2 with weight 3: the representatives 0 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":4},"vars":{"accepted":"4","total":"9","parent":"[1, 1, 1, 1, 1, 5]"},"note":"Edge 3-4 with weight 3: the representatives 4 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":5},"vars":{"accepted":"5","total":"12","parent":"[1, 1, 1, 1, 1, 1]"},"note":"Edge 4-5 with weight 3: the representatives 5 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":6},"vars":{"accepted":"5","total":"12","parent":"[1, 1, 1, 1, 1, 1]"},"note":"accepted equals 5, which is V - 1, so the loop stops. The 2 later edges are never examined, and the total is 12."}]}
```

#### A Graph That Splits In Two

The second trace uses six vertices where vertices 0, 1 and 2 form one triangle and vertices 3, 4 and 5 form another. No edge joins the triangles. The loop accepts two edges inside each triangle and skips the third edge of each. It examines every edge, because `accepted` never reaches 5. The loop ends with `accepted` equal to 4, so the method returns -1 to report that no spanning tree exists.

```trace
{"cells":[1,1,2,2,3,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"accepted":"0","total":"0","parent":"[0, 1, 2, 3, 4, 5]"},"note":"Start: 6 separate groups. The edges are sorted by weight and the loop needs 5 acceptances."},{"at":{"i":0},"vars":{"accepted":"1","total":"1","parent":"[0, 1, 1, 3, 4, 5]"},"note":"Edge 1-2 with weight 1: the representatives 2 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":1},"vars":{"accepted":"2","total":"2","parent":"[0, 1, 1, 3, 4, 4]"},"note":"Edge 4-5 with weight 1: the representatives 5 and 4 differ, so the edge is accepted and the groups merge."},{"at":{"i":2},"vars":{"accepted":"3","total":"4","parent":"[1, 1, 1, 3, 4, 4]"},"note":"Edge 0-1 with weight 2: the representatives 0 and 1 differ, so the edge is accepted and the groups merge."},{"at":{"i":3},"vars":{"accepted":"4","total":"6","parent":"[1, 1, 1, 4, 4, 4]"},"note":"Edge 3-5 with weight 2: the representatives 3 and 4 differ, so the edge is accepted and the groups merge."},{"at":{"i":4},"vars":{"accepted":"4","total":"6","parent":"[1, 1, 1, 4, 4, 4]"},"note":"Edge 0-2 with weight 3: find returns 1 for both ends, so the edge is skipped."},{"at":{"i":5},"vars":{"accepted":"4","total":"6","parent":"[1, 1, 1, 4, 4, 4]"},"note":"Edge 3-4 with weight 4: find returns 4 for both ends, so the edge is skipped."},{"at":{"i":6},"vars":{"accepted":"4","total":"6","parent":"[1, 1, 1, 4, 4, 4]"},"note":"The list is exhausted with accepted = 4, which is below V - 1 = 5, so the method returns -1."}]}
```

<!-- stage: code -->
### Kruskal With Union-Find

#### The Complete Method

The method `minCost` returns the total weight of a cheapest spanning tree, or -1 when the graph is disconnected. The helper `find` uses path halving, a form of path compression that points each visited vertex at its grandparent. The block compiles as one class.

```java
import java.util.Arrays;

final class Kruskal {
    private static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];           // point x at its grandparent to shorten later searches
            x = parent[x];
        }
        return x;
    }

    static long minCost(int vertexCount, int[][] edges) {
        int[][] sorted = edges.clone();              // leave the caller's array in its original order
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));  // compare, not subtract, so extreme weights cannot overflow
        int[] parent = new int[vertexCount];
        int[] size = new int[vertexCount];
        for (int v = 0; v < vertexCount; v++) { parent[v] = v; size[v] = 1; }
        long total = 0;
        int accepted = 0;
        for (int[] e : sorted) {
            if (accepted == vertexCount - 1) break;  // the tree is complete, so later edges cannot help
            int ru = find(parent, e[0]), rv = find(parent, e[1]);
            if (ru == rv) continue;                  // both ends share a group, so the edge would close a cycle
            if (size[ru] < size[rv]) { int t = ru; ru = rv; rv = t; }
            parent[rv] = ru;                         // the smaller group attaches below the larger one
            size[ru] += size[rv];                    // keep size in step with parent
            total += e[2];                           // a long accumulator holds sums beyond the int range
            accepted++;
        }
        return accepted == vertexCount - 1 ? total : -1;
    }
}
```

#### Reading The Cost

- **Time** is O(E log E) for the sort plus O(E * alpha(V)) for the union-find calls, where alpha is below 5 for any practical `V`.
- **Space** is O(V + E), because the arrays `parent` and `size` hold `V` entries and the sorted copy holds `E` edge references.

<!-- stage: applicability -->
### Recognizing When Kruskal Applies

#### Reading The Cue

Use Kruskal when the statement asks to connect all vertices with the lowest total cost. The input is either a list of edges or points with a cost for each pair. Phrases such as "every vertex reachable", "lowest total", "no unnecessary link" and "return -1 when connection is impossible" all point to it. When the input is points, the program first generates the pairs as edges.

#### Checking The Invariant

The invariant is that the accepted edges form a forest, which is a graph with no cycle. The groups of the union-find structure equal the connected pieces of that forest. Every accepted edge is the lightest edge that leaves its group at that moment. The invariant breaks when `size` and `parent` fall out of step, or when the loop accepts an edge without the `find` comparison.

#### Avoiding The False Friend

The false friend is the plan that takes the cheapest edges without a cycle check. It matches the right answer whenever the cheapest edges happen to form a tree, so small samples can pass. A second false friend is a shortest path tree from one source. That tree minimizes the distance from the source to each vertex, and it can cost more in total than a cheapest spanning tree. A weight difference can also overflow in the comparator, so compare with `Integer.compare`.

<!-- stage: exercises -->
### Exercises

#### [Build] Cheapest Safe Edge (Author exercise)
<!-- id: dg-cheapest-safe-edge -->

**Prerequisites.** The Union By Size and Dynamic Connectivity lessons.

**Problem.** An undirected weighted graph has vertices `0` to `V - 1` and an edge list, where edge `k` is `{u, v, w}`. Process the edges in increasing weight, with ties broken by the smaller input index `k`. Accept an edge when its endpoints lie in different groups at that moment, and skip it otherwise. Return the input indices of the accepted edges in the order of acceptance. The graph is connected.

**Constraints.** The limits are:
- **Vertices** number `1 <= V <= 1000`.
- **Edges** number `V - 1 <= E <= 5000`, and every `u` and `v` lies in `[0, V - 1]`.
- **Weights** are `int` values with `1 <= w <= 1000`, and equal weights occur.
- **Parallel edges and self-loops** may occur, and a self-loop is never accepted.
- **Mutation** does not occur; the method leaves `edges` unchanged.

**Example 1.** Input `V = 4`, `edges = [[0,1,4],[1,2,1],[0,2,3],[2,3,2],[1,3,5]]`, output `[1,3,2]`.

**Example 2.** Input `V = 3`, `edges = [[0,1,2],[1,1,1],[0,1,2],[1,2,2]]`, output `[0,3]`, because the self-loop is skipped and the second copy of edge `0-1` is skipped.

**Hint.** Which comparison decides whether an edge is skipped? What does a sort that is stable on the weight do for equal weights?

**Changed decision.** The method returns the accepted input indices and not a total cost.

#### [Vary] Stop After V Minus One (Author exercise)
<!-- id: dg-stop-after-v-minus-one -->

**Prerequisites.** The first exercise above.

**Problem.** The setting of the previous exercise holds: a connected weighted graph, edges processed by increasing weight with ties broken by the smaller input index. The method stops as soon as it has accepted `V - 1` edges. Return the number of edges that the method examines before it stops, counting both accepted and skipped edges. Return 0 when `V` is 1.

**Constraints.** The limits are:
- **Vertices** number `1 <= V <= 1000`.
- **Edges** number `V - 1 <= E <= 5000`, and every `u` and `v` lies in `[0, V - 1]`.
- **Weights** are `int` values with `1 <= w <= 1000`.
- **Parallel edges and self-loops** may occur.
- **Mutation** does not occur; the method leaves `edges` unchanged.

**Example 1.** Input `V = 4`, `edges = [[0,1,1],[1,2,2],[0,2,3],[2,3,4]]`, output `4`, because the third edge is skipped and the fourth edge completes the tree.

**Example 2.** Input `V = 1`, `edges = [[0,0,7],[0,0,3]]`, output `0`, because a single vertex needs no edge and the loop never starts.

**Hint.** Where does the check against `V - 1` belong, before or after the examination of an edge? What count is correct when the last accepted edge is also the last edge in the list?

**Changed decision.** The loop ends at `V - 1` acceptances, and the answer is how many edges it examined.

#### [Boundary] Disconnected Weighted Graph (Author exercise)
<!-- id: dg-disconnected-weighted -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected weighted graph has vertices `0` to `V - 1` and an edge list of `{u, v, w}`. Return the lowest total weight of a set of edges that connects all vertices. Return -1 when the graph is disconnected, because no such set exists. A graph with one vertex has total weight 0.

**Constraints.** The limits are:
- **Vertices** number `1 <= V <= 2000`.
- **Edges** number `0 <= E <= 5000`, and an empty edge list is allowed.
- **Weights** are `int` values with `1 <= w <= 10^9`.
- **Result** has type `long`, because the sum of weights exceeds the `int` range.
- **Parallel edges and self-loops** may occur.

**Example 1.** Input `V = 5`, `edges = [[0,1,3],[1,2,4],[3,4,1]]`, output `-1`, because no edge joins `{0,1,2}` to `{3,4}`.

**Example 2.** Input `V = 4`, `edges = [[0,1,1000000000],[1,2,1000000000],[2,3,1000000000],[0,3,1000000000]]`, output `3000000000`, which exceeds the `int` maximum of 2147483647, so the sum needs the type `long`.

**Hint.** How many edges must the loop accept when the graph is connected? What does a smaller count prove?

**Changed decision.** The method compares `accepted` with `V - 1` at the end and returns -1 when it is smaller.

#### [Recognize] Connect All Points At Lowest Cost (LeetCode 1584)
<!-- id: dg-min-cost-points -->

**Prerequisites.** The Boundary exercise above.

**Problem.** An array holds `n` distinct points `{x, y}` on a plane. The cost of a link between two points is their Manhattan distance, `|x1 - x2| + |y1 - y2|`. Return the lowest total cost of links that make every point reachable from every other point through links.

**Constraints.** The limits are:
- **Points** number `1 <= n <= 500`, and all points are distinct.
- **Coordinates** are `int` values with `-10^6 <= x, y <= 10^6`.
- **Links** may join any two points, so `n * (n - 1) / 2` candidates exist.
- **Result** is `0` when `n` is 1.
- **Mutation** does not occur; the method leaves `points` unchanged.

**Example 1.** Input `points = [[1,1],[4,5],[0,6],[7,1]]`, output `17`.

**Example 2.** Input `points = [[-3,2],[4,-1],[1,9]]`, output `21`, because the two shortest links cost 10 and 11.

**Hint.** What are the vertices and what are the edges? Which of the two classical pair counts decides the size of the sorted list?

**Changed decision.** The graph is not given, so the program generates every pair as a weighted edge before it applies the loop.
