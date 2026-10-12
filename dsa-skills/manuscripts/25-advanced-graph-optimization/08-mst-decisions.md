<!-- lesson-kind: standard -->
<!-- lesson-id: mst-decisions -->
## Choose Edges For A Minimum Spanning Tree

<!-- stage: context -->
### Linking Every Office At Lowest Price

A company has six offices and wants one private network that joins all of them. A telecom provider quotes a price for each cable between two offices, and not every pair of offices has a quote. A cable works in both directions. The company must be able to send data from any office to any other office, possibly through several cables. It wants the lowest total price for the cables it buys.

Model the offices as vertices numbered 0 to n - 1 and each quoted cable as an undirected edge with a **weight**, which is its price. The input is a connected graph, and the method does not change it. The task is to choose some of the edges so that every office reaches every other office and the sum of the chosen weights is as small as possible. Weights are integers and may be zero.

This lesson asks how to decide that an edge belongs in the purchase without comparing every possible purchase, and it asks which of two standard methods fits a given input.

<!-- stage: naive -->
### Buying The Shortest Routes To Headquarters

A natural first plan is to treat office 0 as headquarters and give every other office its cheapest route to it. The engineer runs Dijkstra's method from office 0, remembers for each office the cable that last improved its distance, and buys exactly those cables. Every office then reaches headquarters, so the network is connected. The method sums the weights of the bought cables.

```java
static long routesToHeadquarters(int n, int[][] cables) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] c : cables) {
        adj.get(c[0]).add(new int[] {c[1], c[2]});
        adj.get(c[1]).add(new int[] {c[0], c[2]});
    }
    long[] dist = new long[n];
    int[] lastPrice = new int[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[0] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, 0});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        int u = (int) top[1];
        if (top[0] > dist[u]) continue;
        for (int[] e : adj.get(u)) {
            if (top[0] + e[1] < dist[e[0]]) {
                dist[e[0]] = top[0] + e[1];
                lastPrice[e[0]] = e[1];
                heap.add(new long[] {dist[e[0]], e[0]});
            }
        }
    }
    long total = 0;
    for (int v = 1; v < n; v++) total += lastPrice[v];
    return total;
}
```

The method connects all offices and runs in O(E log E) time. The open question is whether the sum it returns is the lowest possible.

```predict
Three offices have the cables 0 to 1 at price 5, 0 to 2 at price 5, and 1 to 2 at price 1. What total does routesToHeadquarters return, and is it the lowest?

It returns 10, which is not the lowest. Office 1 and office 2 each reach headquarters most cheaply by their own direct cable, so the method buys both cables of price 5. Buying the cable of price 1 together with one cable of price 5 also connects all three offices, and the total is only 6. The method minimizes the distance of each office to headquarters. The company wants the smallest sum of prices, which is a different quantity.
```

<!-- stage: bottleneck -->
### Shortest Routes Ignore The Total Price

#### Distance Is Not Price

Dijkstra's method judges a cable by how much it shortens the trip to office 0. The company does not care about trips. It pays once for each cable it buys, no matter how much data travels over it. Take a cable of price 1 between two offices that are both far from headquarters. It never improves a distance from headquarters, so the method ignores it. That cable is exactly the one that lowers the bill.

#### Trying Every Purchase Is Too Slow

The honest alternative is to try every purchase. A purchase that connects n offices needs at least n - 1 cables. The method could test every subset of n - 1 cables for connection and keep the cheapest. With E cables that is C(E, n - 1) subsets, which is O(2^E) in the worst case. The values E = 40 and n = 10 already give more than 270 million subsets to test.

#### A Test For One Edge

The gap is a local rule. The method needs a test that looks at one edge and says that this edge is safe to buy, meaning that some cheapest purchase contains it. If such a test exists and can be applied repeatedly, the method builds the answer edge by edge and never reconsiders a decision. The test must also be cheap to evaluate, so that the total work stays close to one pass over the edges plus the price of ordering them.

<!-- stage: insight -->
### Lightest Edge Across A Split Is Safe

The method buys the lightest edge that joins two groups of offices, because some cheapest purchase always contains it.

<!-- names: spanning tree, cut, crossing edge -->

#### A Network With No Spare Cable

A **spanning tree** of a connected graph is a set of exactly n - 1 edges that connects all n vertices and contains no cycle. A cycle is a closed chain of edges, and in a cycle any one cable is spare, because the other cables still connect its two ends. A purchase with the lowest total weight never keeps a spare cable when weights are positive. When weights are zero a spare cable costs nothing, so the method can drop it without changing the total. A **minimum spanning tree** is a spanning tree whose total weight is the smallest among all spanning trees. The graph may have several of them.

#### Splitting The Offices Into Two Groups

A **cut** is a division of the vertices into two nonempty groups. A **crossing edge** of a cut is an edge with one endpoint in each group. A set of chosen edges **respects** a cut when none of them is a crossing edge. For any cut of a connected graph, at least one crossing edge exists, because otherwise the two groups would have no connection at all.

#### Why The Lightest Crossing Edge Is Safe

The cut property states the rule. Let `A` be a set of edges that lies inside some minimum spanning tree `T`, and let a cut respect `A`. Let `e` be a crossing edge of the lowest weight. Then `A` plus `e` lies inside some minimum spanning tree.

The proof exchanges one edge. If `T` already contains `e`, nothing remains to show. Otherwise adding `e` to `T` creates exactly one cycle. That cycle enters one group through `e`, so it must return through a second crossing edge `f` that belongs to `T`. The edge `f` is not in `A`, because `A` respects the cut. Since `e` is lightest among the crossing edges, its weight is at most the weight of `f`. Removing `f` and keeping `e` gives a spanning tree whose weight is no larger than the weight of `T`. That tree is also minimum, and it contains `A` and `e`. The argument never uses the sign of a weight, so negative weights are allowed, in contrast to Dijkstra's method.

#### Two Ways To Pick The Cut

The rule needs a cut that the chosen edges respect, and two choices appear in practice. Prim's method keeps one growing tree and uses the cut between the tree's vertices and all other vertices. Kruskal's method looks at the lightest remaining edge in the whole graph. Suppose that edge joins two different components of the chosen edges. Then the cut between one of those components and the rest is respected, and the edge is the lightest across it. Both methods add safe edges only, so both end with a minimum spanning tree. They differ in the data they need, and the applicability stage compares them.

<!-- stage: variables -->
### Tree Membership And Best Weights

The input is `n`, an array `cables` of triples `[a, b, weight]`, and nothing else. The methods read it and change nothing. The methods use four variables.

- **inTree** is a `boolean[]` of length `n` that marks the vertices already joined to the growing tree.
- **best** is a `long[]` where `best[v]` is the weight of the lightest known edge from `v` to a vertex in the tree; `Long.MAX_VALUE` means no such edge is known.
- **total** is a `long` that sums the weights of the edges bought so far.
- **root** is an `int[]` for Kruskal in which two vertices share a root exactly when the chosen edges already connect them.

The sum is a `long`, because a thousand edges of weight near two billion exceed the range of `int`. Vertex `u` is picked by comparing `best` entries with `Long.compare` and never by subtraction. The marker `Long.MAX_VALUE` is only compared and never added to anything.

<!-- stage: trace -->
### Two Runs On Small Cable Maps

#### Prim On Six Offices

The first map has six offices and eight cables. The cables are 0 to 1 at 4, 0 to 2 at 3, 1 to 2 at 1, 1 to 3 at 2, 2 to 3 at 4, 3 to 4 at 2, 4 to 5 at 6 and 3 to 5 at 5. Each cell is one office in the order it joins the tree, written as the office and the weight of the edge that joined it. The pointer `add` marks the office that joins at that step. The variable `weight` is that edge weight, `total` is the sum so far, and `improved` counts the entries of `best` that drop at this step. At the second step, office 2 joins at weight 3 and lowers the best weights of offices 1 and 3. At the third step, office 1 joins at weight 1, which is cheaper than its direct cable of weight 4. At the fifth step, office 4 joins and lowers nothing, because office 5 already has a cable of weight 5 and the cable from office 4 costs 6. The final total is 13.

```trace
{"cells":["0@0","2@3","1@1","3@2","4@2","5@5"],"pointers":["add"],"steps":[{"at":{"add":0},"vars":{"weight":0,"total":0,"improved":2},"note":"Office 0 starts the tree at no cost; it lowers the best weight of 1 to 4, 2 to 3. The total is 0."},{"at":{"add":1},"vars":{"weight":3,"total":3,"improved":2},"note":"Office 2 joins through office 0 at weight 3, the lightest edge leaving the tree; it lowers the best weight of 1 to 1, 3 to 4. The total is 3."},{"at":{"add":2},"vars":{"weight":1,"total":4,"improved":1},"note":"Office 1 joins through office 2 at weight 1, the lightest edge leaving the tree; it lowers the best weight of 3 to 2. The total is 4."},{"at":{"add":3},"vars":{"weight":2,"total":6,"improved":2},"note":"Office 3 joins through office 1 at weight 2, the lightest edge leaving the tree; it lowers the best weight of 4 to 2, 5 to 5. The total is 6."},{"at":{"add":4},"vars":{"weight":2,"total":8,"improved":0},"note":"Office 4 joins through office 3 at weight 2, the lightest edge leaving the tree; it lowers no best weight. The total is 8."},{"at":{"add":5},"vars":{"weight":5,"total":13,"improved":0},"note":"Office 5 joins through office 3 at weight 5, the lightest edge leaving the tree; it lowers no best weight. The total is 13."}]}
```

#### Shortest Routes Overpay

The second map has five offices and six cables. The cables are 0 to 1 at 5, 0 to 2 at 5, 1 to 2 at 1, 2 to 3 at 2, 3 to 4 at 1 and 0 to 4 at 9. This run is the method of the naive stage. Each cell is an office in the order Dijkstra's method finalizes it, written as the office and its distance from office 0. The pointer `settle` marks that office. The variable `distance` is the distance, `cable` is the weight of the last cable on the route, and `total` adds those cables. Offices 1 and 2 each buy a cable of weight 5, and the cable of weight 1 between them is never bought. The tree totals 13, while the cheapest tree totals 9.

```trace
{"cells":["0@0","1@5","2@5","3@7","4@8"],"pointers":["settle"],"steps":[{"at":{"settle":0},"vars":{"distance":0,"cable":0,"total":0},"note":"Office 0 is the hub and costs nothing."},{"at":{"settle":1},"vars":{"distance":5,"cable":5,"total":5},"note":"Office 1 is reached at distance 5 through office 0, and its last cable weighs 5. The cable total is 5."},{"at":{"settle":2},"vars":{"distance":5,"cable":5,"total":10},"note":"Office 2 is reached at distance 5 through office 0, and its last cable weighs 5. The cable total is 10."},{"at":{"settle":3},"vars":{"distance":7,"cable":2,"total":12},"note":"Office 3 is reached at distance 7 through office 2, and its last cable weighs 2. The cable total is 12."},{"at":{"settle":4},"vars":{"distance":8,"cable":1,"total":13},"note":"Office 4 is reached at distance 8 through office 3, and its last cable weighs 1. The cable total is 13. The cheapest tree for these cables totals 9, so the shortest-path tree overpays by 4."}]}
```

<!-- stage: code -->
### Prim And Kruskal In Java

The first method is dense Prim. It builds a matrix of lightest weights, so parallel cables keep only the cheapest one. It returns `-1` when the graph is not connected, which the entry contract excludes but a caller can still pass by mistake.

```java
static long densePrim(int n, int[][] cables) {
    long[][] price = new long[n][n];
    for (long[] row : price) Arrays.fill(row, Long.MAX_VALUE);
    for (int[] c : cables) {
        price[c[0]][c[1]] = Math.min(price[c[0]][c[1]], c[2]);
        price[c[1]][c[0]] = price[c[0]][c[1]];
    }
    boolean[] inTree = new boolean[n];
    long[] best = new long[n];
    Arrays.fill(best, Long.MAX_VALUE);
    best[0] = 0;
    long total = 0;
    for (int round = 0; round < n; round++) {
        int u = -1;
        for (int v = 0; v < n; v++) {
            if (!inTree[v] && (u == -1 || Long.compare(best[v], best[u]) < 0)) u = v;
        }
        if (best[u] == Long.MAX_VALUE) return -1;
        inTree[u] = true;
        total += best[u];
        for (int v = 0; v < n; v++) {
            if (!inTree[v] && price[u][v] < best[v]) best[v] = price[u][v];
        }
    }
    return total;
}
```

Each round scans all vertices twice, so dense Prim runs in O(V^2) time and uses O(V^2) memory for the matrix. The tree edge is safe because `best[u]` is the lightest edge across the cut between the tree and the other vertices.

The second method is Kruskal. It sorts a copy of the edges, so the input array keeps its order. The sort compares with `Integer.compare`, because the difference of two `int` weights can overflow.

```java
static long kruskal(int n, int[][] cables) {
    int[][] sorted = cables.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
    int[] root = new int[n];
    for (int v = 0; v < n; v++) root[v] = v;
    long total = 0;
    int bought = 0;
    for (int[] c : sorted) {
        int ra = find(root, c[0]);
        int rb = find(root, c[1]);
        if (ra != rb) {
            root[ra] = rb;
            total += c[2];
            bought++;
        }
    }
    return bought == n - 1 ? total : -1;
}

static int find(int[] root, int x) {
    while (root[x] != x) {
        root[x] = root[root[x]];
        x = root[x];
    }
    return x;
}
```

Sorting costs O(E log E), and the loop makes E calls to `find`, which are close to constant with path halving. The method uses O(V) memory beyond the cloned array. The edge `c` is safe whenever its endpoints have different roots, since it is the lightest edge that leaves the component of `ra`.

<!-- stage: applicability -->
### Recognizing Minimum Connection Problems

#### Reading The Cue

Use these methods when the statement asks for the lowest total weight that keeps every vertex connected to every other. Laying cable, building roads between towns, and wiring chips are typical cases. The word total matters. A request for the shortest route from one source is a different problem.

#### Checking The Invariant

An invariant is a property that every step of the method must preserve. Here the invariant is that the chosen edges always lie inside some minimum spanning tree. Each step keeps it by adding the lightest edge across a cut that the chosen edges respect. For Prim the cut is the tree against the rest. For Kruskal it is a component against the rest. Test a graph with equal weights, where two different edges are both lightest and either may be taken. Test a single vertex, which needs zero edges.

#### Choosing Between Prim And Kruskal

The decision follows the density and the form of the input. A dense graph has close to V^2 / 2 edges. When the input is a list of edges, Kruskal sorts it at O(E log E). Suppose the input is a matrix, or the weights come from a formula for every pair, such as distances between points. Then dense Prim runs at O(V^2) and never stores an edge list. A sparse graph with an edge list favors Kruskal, and a sparse graph held as an adjacency list can use Prim with a heap. Kruskal also handles a graph that is not connected, because it simply stops with a forest.

#### Avoiding The False Friend

A false friend is a method that resembles the correct one and still returns wrong answers. The false friend here is the shortest-path tree, which the first example of this lesson shows. A second false friend is to give every vertex its own lightest edge. That choice can close a cycle and leave the offices in separate groups. Equal weights are a third trap, since they allow several correct answers and a test must accept any of them.

<!-- stage: exercises -->
### Exercises

#### [Build] Distinguish MST From Shortest Paths (Author exercise)
<!-- id: ga-mst-spt-vs-mst -->

**Prerequisites.** The naive method and the Prim method of this lesson.

**Problem.** An undirected connected graph joins `n` offices labelled `0`, ..., `n - 1` and has edges `[a, b, w]`. Let `dist[v]` be the least total weight of a path from vertex `0` to `v`. The shortest-path tree buys, for each vertex `v` other than `0`, the lightest edge `[u, v, w]` that satisfies `dist[u] + w == dist[v]`. Return a `long[]` of length 2. The first entry is the total weight of the shortest-path tree. The second entry is the total weight of a minimum spanning tree.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 200`.
- **Edges** satisfy `n - 1 <= edges.length <= 2000`, and repeats may occur.
- **Weight** satisfies `0 <= w <= 1000000000`.
- **Mutation** of the input is not allowed.

**Example 1.** Input `n = 4`, `edges = [[0,1,3],[1,2,1],[0,2,3],[2,3,2]]`, output `[8,6]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,2],[1,2,3],[2,3,4]]`, output `[9,9]`.

**Hint.** When a graph has only one spanning tree, what must the two totals be?

**Changed decision.** The method scores each tree by its total weight, so a cable that is cheap but never lies on a shortest route can still enter the cheapest tree.

#### [Vary] Cut-Safe Choice (Author exercise)
<!-- id: ga-mst-cut-safe-choice -->

**Prerequisites.** The exercise above.

**Problem.** A graph labels its vertices from `0` up to `n - 1` and has undirected edges `[a, b, w]` listed by index. The array `side` of length `n` assigns each vertex to group `true` or group `false`. An edge crosses the cut when its endpoints lie in different groups. Return the index of the crossing edge of the lowest weight, using the lowest index among equal weights. Return `-1` when no edge crosses.

**Constraints.** The limits are:
- **Vertices** satisfy `2 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 1000000000`.
- **Side** contains both `true` and `false`.

**Example 1.** Input `n = 4`, `edges = [[0,1,4],[1,2,2],[2,3,7],[0,3,2]]`, `side = [true,true,false,false]`, output `1`.

**Example 2.** Input `n = 3`, `edges = [[0,1,1]]`, `side = [true,true,false]`, output `-1`.

**Hint.** Which edges does the test skip, and what decides between two crossing edges of equal weight?

**Changed decision.** The method returns an edge index for a supplied cut and builds no tree, so only the crossing test and the tie rule remain.

#### [Boundary] Multiple Valid MSTs (Author exercise)
<!-- id: ga-mst-multiple-trees -->

**Prerequisites.** The two exercises above.

**Problem.** A connected undirected graph uses vertex labels `0` through `n - 1` and has edges `[a, b, w]`. Return a `long[]` of length 2. The first entry is the total weight of a minimum spanning tree. The second entry is `1` when exactly one minimum spanning tree exists, where trees are different when their edge sets differ, and `0` otherwise. Parallel edges are different edges.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `n - 1 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 1000000000`.
- **Sums** may exceed the range of `int`, and the result uses `long`.

**Example 1.** Input `n = 3`, `edges = [[0,1,1],[1,2,1],[0,2,1]]`, output `[2,0]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,2],[1,2,2],[2,3,1]]`, output `[5,1]`.

**Hint.** Among the edges of one weight, which ones could the method buy, and how many does it actually buy?

**Changed decision.** The method inspects every group of equal weights, because equal weights alone do not make a tree ambiguous, but two edges that compete for the same connection do.

#### [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: ga-mst-connect-points -->

**Prerequisites.** All three exercises above.

**Problem.** Points `points[i] = [x, y]` lie on a plane. A cable between points `i` and `j` costs `|xi - xj| + |yi - yj|`. The list `built` holds pairs `[i, j]` that already have a cable at cost 0. Return a `long[]` of length 2. The first entry is the least total cost of new cables that connect all points. The second entry is the number of new cables laid.

**Constraints.** The limits are:
- **Points** satisfy `1 <= n <= 1000`, and all points are different.
- **Coordinates** satisfy `-1000000000 <= x, y <= 1000000000`.
- **Built** satisfies `0 <= built.length <= 5000`, and repeats and cycles may occur.
- **Total** may exceed the range of `int`, and the result uses `long`.

**Example 1.** Input `points = [[0,0],[1,3],[4,0],[4,4]]`, `built = [[0,3]]`, output `[8,2]`.

**Example 2.** Input `points = [[0,0],[0,1],[0,2]]`, `built = [[0,1],[1,2]]`, output `[0,0]`.

**Hint.** How many candidate cables exist, and does the method need to store them?

**Changed decision.** Existing cables cost zero, so the method counts only the cables that cost something. Up to half a million pairs exist, so the form of Prim without an edge list fits.
