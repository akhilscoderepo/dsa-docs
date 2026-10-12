<!-- lesson-kind: standard -->
<!-- lesson-id: kruskal -->
## Build A Spanning Tree With Kruskal

<!-- stage: context -->
### Cheap Links Can Leave Islands

#### A Plan That Leaves Two Islands

A database team runs six replicas in different data halls. Any two replicas can sync over a dedicated line, and every line has a monthly bill. The team wants each replica to reach every other one, directly or through other replicas, at the lowest total bill. An engineer sorts the quotes and buys lines from the cheapest upward. The engineer skips a line when both of its replicas already own some line. After four purchases, two replicas still sit in separate islands, and no remaining quote is allowed to join them. The total looks cheap, but the network is broken.

#### The Graph Model

Model the replicas as vertices numbered `0` to `n - 1` and each line as an undirected edge with a weight, the monthly bill. A **spanning tree** is a set of exactly `n - 1` edges that connects all `n` vertices. The task is to find the spanning tree with the smallest total weight, or to report that none exists for a disconnected graph.

The graph is undirected. The vertices are numbered `0` to `n - 1`. The input list of edges stays unchanged. This lesson asks how a program decides, one edge at a time, whether an edge belongs in the cheapest network.

<!-- stage: naive -->
### Skip Edges Between Used Vertices

The first attempt sorts the edges by weight and walks through them. It keeps a boolean array `touched`, where `touched[v]` is true once some bought edge ends at `v`. The method buys an edge unless both of its endpoints are already touched. The reasoning is that such an edge adds no new vertex.

```java
static long touchedRule(int n, int[][] edges) {
    int[][] sorted = edges.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
    boolean[] touched = new boolean[n];
    long total = 0;
    for (int[] e : sorted) {
        if (touched[e[0]] && touched[e[1]]) continue;
        touched[e[0]] = true;
        touched[e[1]] = true;
        total += e[2];
    }
    return total;
}
```

The method sorts once and scans each edge once. It never buys an edge that touches only used vertices, so it looks careful. The question is whether the bought edges connect everything.

```predict
A graph has five vertices and the edges 0-1 with weight 1, 2-3 with weight 2, 1-2 with weight 3, 3-4 with weight 4 and 0-3 with weight 5. What does touchedRule return, and is the network connected?

It returns 7, the sum of the edges 0-1, 2-3 and 3-4. The edge 1-2 is skipped, because vertices 1 and 2 are both touched by earlier purchases. But vertex 1 belongs to the pair 0-1 and vertex 2 belongs to the chain 2-3-4, and those two parts have no edge between them. The network has two islands, and a connected one needs the edge 1-2 as well, for a total of 10.
```

<!-- stage: bottleneck -->
### A Used Vertex Does Not Mean Connected

#### What The Flag Cannot Tell

The flag `touched[v]` records that some edge ends at `v`. It does not record which other vertices `v` can reach through the bought edges. Two touched vertices can sit in different islands, and the method has no way to see that. The rule skips edges that it must buy.

A correct rule asks a different question before each purchase. Can the first endpoint already reach the second one through the edges bought so far? If it can, the new edge closes a cycle and wastes money. If it cannot, the edge joins two islands and is worth buying.

#### The Cost Of Asking By Search

The direct way to answer is a graph search over the bought edges. A search visits up to `n` vertices and `n - 1` edges, so it costs O(n) per candidate edge. With `m` candidates the loop costs O(m * n) after the sort. For 100,000 vertices and 200,000 edges, that is about 2 * 10^10 steps, which is far too slow. The sort needs only a few million comparisons, so the repeated question is the bottleneck.

The question never changes: do these two vertices share an island? A search rediscovers the island from scratch each time. The program needs a structure that remembers the islands and merges two of them in almost constant time.

<!-- stage: insight -->
### Buy An Edge Only Between Groups

The method keeps the islands as groups and buys the cheapest edge that joins two different groups.

<!-- names: forest, safe edge, cut property -->

#### Groups Stored As Parent Links

Each vertex has one **group**, the set of vertices it reaches through bought edges. The array `parent` stores each group as a tree of links. The entry `parent[v]` is the next vertex toward the **root** of the group, and a root satisfies `parent[v] == v`. The call `find(v)` follows the links from `v` and returns the root. Two vertices share a group exactly when `find` returns the same root for both. This representation comes from the union-find lesson, and the definition here is the only one the code below needs.

The array `size` holds the number of vertices of a group at its root. To merge two groups, the method links the root of the smaller group below the root of the larger one, which keeps the trees shallow. The call `find` also halves its path, so that a later search walks fewer links.

#### The Bought Edges Form A Forest

A **forest** is a graph without a cycle. Before the first purchase, the bought edges form a forest of `n` single vertices. The method buys an edge only when `find` returns two different roots. Such an edge joins two trees of the forest and cannot close a cycle. The method skips an edge with equal roots, because that edge would close a cycle. So the bought edges stay a forest after every step, and each purchase lowers the number of groups by one. A spanning tree appears when one group is left, after exactly `n - 1` purchases.

#### Why The Cheapest Joining Edge Is Safe

A **safe edge** is an edge that some cheapest spanning tree contains together with all edges bought so far. The reason a cheapest joining edge is safe is the **cut property**. Split the vertices into two nonempty sets. Among the edges that cross the split, a lightest edge belongs to some cheapest spanning tree.

Apply this to one group `A` at the moment the method examines an edge that leaves `A`. Every lighter edge was examined earlier. Each of those edges either lies inside a group or was bought. So no edge lighter than the current one leaves `A`. The current edge is a lightest edge crossing the split between `A` and the other vertices. Any cheapest tree that contains the bought edges can swap in this edge without raising the total.

#### Equal Weights And Stopping Early

When several edges have the same weight, any order among them is fine. The cut property only needs that no lighter edge crosses the split. The tree may differ between orders, but the total weight is the same. After `n - 1` purchases the tree is complete, so the method stops. A disconnected graph never reaches `n - 1` purchases, and the method reports that instead.

<!-- stage: variables -->
### Groups, Sizes And A Running Total

The method reads `n`, the list `edges` of triples `{u, v, weight}`, and it changes none of them. It sorts a copy and keeps five values between edges.

- **sorted** is a copy of `edges` in nondecreasing weight, and ties keep their input order because `Arrays.sort` on objects is stable.
- **parent** is an `int[]` of length `n` where `parent[v] == v` marks a root.
- **size** is an `int[]` of length `n` that holds the group size and is read only at a root.
- **bought** counts the accepted edges, and the loop stops when it equals `n - 1`.
- **total** is a `long` that adds the weights of the bought edges, because many `int` weights sum past the `int` range.

In the traces, the pointer `i` marks the edge under examination, and the cells hold the sorted edges written as endpoints and weight. The values `ru` and `rv` are the roots that `find` returns for the two endpoints. The method returns `-1` when `bought` is below `n - 1` at the end. That value cannot collide with a total, because every weight is nonnegative.

<!-- stage: trace -->
### Two Runs On Small Graphs

#### Seven Vertices With Equal Weights

The first graph has seven vertices and eleven edges. The cells show the sorted order. Each step shows the two roots and the decision. The first five edges join separate groups, so the method buys each one. The edge 0-1 has equal roots, because vertex 0 joined vertex 2 and vertex 2 joined vertex 1 earlier. The method skips it without paying. The edges 1-3 and 2-3 both weigh 5, and the stable sort puts 1-3 first. The method buys 1-3 and reaches `n - 1 = 6` purchases, so it stops. The last four edges are never examined. The total is 16.

```trace
{"cells":["5-6@1","1-2@2","3-4@2","0-2@3","4-5@3","0-1@4","1-3@5","2-3@5","3-5@6","4-6@7","2-6@9"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"bought":0,"total":0,"ru":-1,"rv":-1},"note":"Start: 7 groups of one vertex each. The loop needs 6 purchases."},{"at":{"i":0},"vars":{"bought":1,"total":1,"ru":5,"rv":6},"note":"Edge 5-6 joins the roots 5 and 6, so the method buys it for 1."},{"at":{"i":1},"vars":{"bought":2,"total":3,"ru":1,"rv":2},"note":"Edge 1-2 joins the roots 1 and 2, so the method buys it for 2."},{"at":{"i":2},"vars":{"bought":3,"total":5,"ru":3,"rv":4},"note":"Edge 3-4 joins the roots 3 and 4, so the method buys it for 2."},{"at":{"i":3},"vars":{"bought":4,"total":8,"ru":1,"rv":0},"note":"Edge 0-2 joins the roots 1 and 0, so the method buys it for 3."},{"at":{"i":4},"vars":{"bought":5,"total":11,"ru":3,"rv":5},"note":"Edge 4-5 joins the roots 3 and 5, so the method buys it for 3."},{"at":{"i":5},"vars":{"bought":5,"total":11,"ru":1,"rv":1},"note":"Edge 0-1 has equal roots 1 and 1, so it would close a cycle and the method skips it."},{"at":{"i":6},"vars":{"bought":6,"total":16,"ru":3,"rv":1},"note":"Edge 1-3 joins the roots 3 and 1, so the method buys it for 5. That is purchase 6, so the loop stops and the last 4 edges are never examined."}]}
```

#### The Touched Rule Against Kruskal

The second graph has six vertices and eight edges. Each step compares the touched rule from the naive stage with the group rule. The variables `naive` and `kruskal` count the edges each rule has bought, and `gap` is their difference. Both rules buy the first three edges, which join separate vertices. At the fourth edge, 1-2, both endpoints are touched, so the touched rule skips it. The roots differ, so the group rule buys it. After that the touched rule buys nothing more. It ends with 3 edges and total 4, so three groups remain. The group rule stops after 5 edges and total 10.

```trace
{"cells":["0-1@1","2-3@1","4-5@2","1-2@3","3-4@3","2-5@4","1-4@5","0-5@6"],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"naive":0,"kruskal":0,"gap":0},"note":"Start: nothing is bought by either rule."},{"at":{"i":0},"vars":{"naive":1,"kruskal":1,"gap":0},"note":"Edge 0-1: the touched rule buys the edge, and the group rule buys it."},{"at":{"i":1},"vars":{"naive":2,"kruskal":2,"gap":0},"note":"Edge 2-3: the touched rule buys the edge, and the group rule buys it."},{"at":{"i":2},"vars":{"naive":3,"kruskal":3,"gap":0},"note":"Edge 4-5: the touched rule buys the edge, and the group rule buys it."},{"at":{"i":3},"vars":{"naive":3,"kruskal":4,"gap":1},"note":"Edge 1-2: the touched rule skips the edge, and the group rule buys it."},{"at":{"i":4},"vars":{"naive":3,"kruskal":5,"gap":2},"note":"Edge 3-4: the touched rule skips the edge, and the group rule buys it."},{"at":{"i":5},"vars":{"naive":3,"kruskal":5,"gap":2},"note":"Edge 2-5: the touched rule skips the edge, and the group rule has already stopped."},{"at":{"i":6},"vars":{"naive":3,"kruskal":5,"gap":2},"note":"Edge 1-4: the touched rule skips the edge, and the group rule has already stopped."},{"at":{"i":7},"vars":{"naive":3,"kruskal":5,"gap":2},"note":"Edge 0-5: the touched rule skips the edge, and the group rule has already stopped."}]}
```

<!-- stage: code -->
### Kruskal With Parent Links

The method returns the total weight of a cheapest spanning tree as a `long`, or `-1` when the graph is disconnected. The comparator uses `Integer.compare`, because the subtraction of two `int` weights can overflow and flip the sign. The helper `find` halves its path.

```java
import java.util.Arrays;

final class KruskalTree {
    private static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static long cheapestTree(int n, int[][] edges) {
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int v = 0; v < n; v++) {
            parent[v] = v;
            size[v] = 1;
        }
        long total = 0;
        int bought = 0;
        for (int[] e : sorted) {
            if (bought == n - 1) break;
            int ru = find(parent, e[0]);
            int rv = find(parent, e[1]);
            if (ru == rv) continue;
            if (size[ru] < size[rv]) {
                int t = ru;
                ru = rv;
                rv = t;
            }
            parent[rv] = ru;
            size[ru] += size[rv];
            total += e[2];
            bought++;
        }
        return bought == n - 1 ? total : -1;
    }
}
```

The test `ru == rv` must run before the merge, because a merge of two vertices of one group would corrupt `size`. The early `break` keeps the loop from calling `find` on edges that cannot change the answer. The call `edges.clone()` copies only the array of references, which is enough because the method never writes into an edge. The method never changes the caller's array order.

Sorting costs O(m log m) for `m` edges. With both rules in place, each `find` runs in amortized near constant time. The loop adds O(m * alpha(n)), where alpha is the inverse Ackermann function. It stays below 5 for any `n` that fits in memory. The total time is O(m log m). The space is O(n + m), because `parent` and `size` hold `n` entries each and the sorted copy holds `m` references.

<!-- stage: applicability -->
### Recognizing When Kruskal Applies

#### Reading The Cue

Use Kruskal when the statement asks to connect every vertex at the lowest total weight. The edges are listed or can be generated. Words such as "lowest total", "every site reachable", "no redundant link" and "report failure when it cannot connect" point to it. The edge list can be sorted once, and a union-find structure answers the group question. When the input is points with a cost for each pair, the program first generates the pairs as edges.

#### Checking The Invariant

The invariant is a statement that stays true before and after every loop step. Here the bought edges form a forest. The groups of `parent` equal the connected pieces of that forest. Every bought edge was a lightest edge leaving its group at that moment. The invariant breaks when the merge forgets to update `size`. It also breaks when the loop buys an edge without comparing roots, or sorts by a different key. Test a graph with parallel edges, a self-loop and a single vertex. A self-loop always has equal roots and is never bought. A single vertex needs zero purchases and returns 0.

#### Avoiding The False Friend

A false friend is a plausible method that gives a wrong answer on some input. The false friend here is the touched rule of the naive stage, which tests vertices and not groups. It passes on graphs where the cheapest edges happen to form a tree. A second false friend is a shortest path tree from one source. That tree minimizes each distance from the source, and it can cost more in total than a cheapest spanning tree. A third mistake is to skip the cycle test when all weights are distinct and assume no cycle can form. Distinct weights do not prevent a cycle among cheap edges.

<!-- stage: exercises -->
### Exercises

#### [Build] Sorted Safe Edges (Author exercise)
<!-- id: ga-kr-sorted-safe-edges -->

**Prerequisites.** The group rule and the `find` helper of this lesson.

**Problem.** An undirected graph labels its vertices from `0` up to `n - 1`. The array `edges` holds triples `{u, v, w}` and is already sorted by nondecreasing `w`. Scan the edges in the given order and keep groups of vertices that the accepted edges connect. Accept edge `k` when its endpoints lie in different groups at that moment, and skip it otherwise. Scan every edge, with no early stop. Return a `boolean[]` of length `edges.length` where entry `k` is `true` when edge `k` is accepted.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self-loops may occur.
- **Weights** are `int` values in `1..1000000000`.
- **Mutation** does not occur, and `edges` stays unchanged.

**Example 1.** Input `n = 4`, `edges = [[0,1,1],[2,3,2],[1,2,3],[0,3,4],[1,3,5]]`, output `[true,true,true,false,false]`.

**Example 2.** Input `n = 3`, `edges = [[0,0,1],[0,1,1],[0,1,2],[1,2,2]]`, output `[false,true,false,true]`, because the self-loop and the repeated edge 0-1 are skipped.

**Hint.** Which two values must differ for an edge to join two groups, and what do they equal for a self-loop?

**Changed decision.** The method reports the decision for every edge as a flag and does not add up any weights.

#### [Vary] Stop At V Minus One (Author exercise)
<!-- id: ga-kr-stop-count -->

**Prerequisites.** The exercise above.

**Problem.** An undirected connected graph draws vertices from `0` to `n - 1` and has the unsorted edge array `edges` of triples `{u, v, w}`. Sort a copy by `w`, keeping the input order among equal weights. Scan the sorted copy and stop as soon as `n - 1` edges are accepted. Return the number of edges that the scan skips because their endpoints already share a group. Edges after the stop are not examined and are not counted.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `n - 1 <= edges.length <= 5000`, and the graph is connected.
- **Weights** are `int` values in `0..1000000000`, and equal weights occur.
- **Mutation** does not occur, and `edges` stays unchanged.

**Example 1.** Input `n = 5`, `edges = [[0,1,4],[1,2,1],[0,2,3],[2,3,2],[1,3,5],[3,4,6],[0,3,2],[1,4,7]]`, output `3`.

**Example 2.** Input `n = 4`, `edges = [[0,1,2],[1,2,2],[0,2,2],[2,3,9],[0,3,9]]`, output `1`, because the last edge comes after the stop.

**Hint.** At which sorted position does the count of accepted edges reach `n - 1`, and which skipped edges lie before that position?

**Changed decision.** The method counts skipped edges and not examined edges, so the early stop decides which skips are counted.

#### [Boundary] Equal Weights And Disconnection (Author exercise)
<!-- id: ga-kr-forest-tally -->

**Prerequisites.** The two exercises above.

**Problem.** An undirected graph uses vertex labels `0` through `n - 1` and the edge array `edges` of triples `{u, v, w}`. The graph may be disconnected. Accept the edges by Kruskal's rule over the whole sorted list, with any order among equal weights. The result is a `long[]` with two slots. Slot 0 holds the number of groups left at the end, and slot 1 holds the total weight of the accepted edges.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self-loops may occur.
- **Weights** are `int` values in `0..2000000000`, and the total uses `long`.
- **Ties** between equal weights may be broken in any order, and the result does not depend on it.

**Example 1.** Input `n = 3`, `edges = [[0,1,2000000000],[1,2,2000000000],[0,2,2000000000]]`, output `[1,4000000000]`.

**Example 2.** Input `n = 5`, `edges = [[0,1,2],[1,0,2],[2,3,7]]`, output `[3,9]`, because vertex 4 stays alone.

**Hint.** What does the number of accepted edges tell about the number of groups, and which type holds the sum of two large weights?

**Changed decision.** The method returns a count of groups and a total for a possibly disconnected graph and does not return `-1`.

#### [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-kr-heaviest-link -->

**Prerequisites.** All three exercises above.

**Problem.** The array `points` holds distinct integer points `{x, y}`. The cost of a connection between two points is their Manhattan distance, the value `|x1 - x2| + |y1 - y2|`. A set of connections joins all points when every point reaches every other point through them. Among all such sets of minimum total cost, every set has the same largest connection. Return that largest connection cost, or `0` when there is one point. Use Kruskal's method on all pairs.

**Constraints.** The limits are:
- **Points** satisfy `1 <= points.length <= 500`, and all points are distinct.
- **Coordinates** are `int` values in `-1000000..1000000`.
- **Distances** are at most `4000000` and fit in an `int`.
- **Mutation** does not occur, and `points` stays unchanged.

**Example 1.** Input `points = [[0,0],[1,1],[1,0],[5,5]]`, output `8`.

**Example 2.** Input `points = [[0,0],[0,4],[9,0]]`, output `9`.

**Hint.** Which accepted edge of the sorted scan carries the largest weight, and when does the scan stop?

**Changed decision.** The method returns the largest accepted edge and not the total cost. The solution also compares the `n * (n - 1) / 2` stored edges with the memory that Prim needs.
