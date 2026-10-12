<!-- lesson-kind: combination -->
<!-- lesson-id: choose-a-method-for-each-graph-goal -->
## Choose A Method For Each Graph Goal

<!-- stage: context -->
### Why One Tool Fails Four Requests

A regional telecom keeps one map of its sites and links, and four requests reach the data team in the same week. Planners want the cheapest set of new cables that connects every site. Operators want the list of single links whose failure splits the network. A warehouse team wants the site that reaches the fewest other sites within a travel limit. A dispatch team wants one tour that drives every link exactly once.

An engineer owns a tested shortest path routine with a heap and tries it on all four. For the cabling request, the routine returns a plan that costs more than the cheapest set. For the single-link request, it produces no output that answers the question. For the tour request, it never says which link to drive next. Only the warehouse request fits the tool.

The four requests ask for four different kinds of answer. Each answer stays correct only while a different fact holds during the computation. This lesson asks how to read the goal in a statement and pick the method whose fact matches it.

<!-- stage: contributions -->
### What Six Earlier Lessons Add

#### What Spanning Tree Methods Supply

The Prim lesson supplies a heap of edges that cross from the built tree to a vertex outside it. The Kruskal lesson supplies a sorted edge list together with union-find. Union-find stores one `parent` entry per vertex, and `find` returns the root that names a group. Two endpoints with equal roots lie in one group, so the edge between them would close a cycle. The MST decisions lesson explains when each method fits the input better. Both methods sum edge weights in a `long`, because a total can pass the `int` range.

#### What Low Links Supply

The low links lesson supplies a depth-first search that records two numbers per vertex. The number `disc[u]` is the order in which the search first reaches `u`. The number `low[u]` is the smallest discovery time that the subtree of `u` reaches through one edge other than the edge to its parent. A tree edge from `u` to a child `v` is a bridge when `low[v] > disc[u]`. A bridge is an edge whose removal disconnects the graph.

#### What Floyd-Warshall And Hierholzer Supply

The Floyd-Warshall lesson supplies a table `dist[i][j]` of best distances for every pair, and the rule that the sentinel `Long.MAX_VALUE` never enters an addition. The Hierholzer lesson supplies a walk that deletes each link when it uses it. The walk writes a vertex to the output only when no unused link leaves that vertex, so the output lists the trail backward.

#### What The Combination Adds

The methods of these six lessons do not compete, because each keeps a different fact true. The combination adds a step before any code. Read the goal in the statement, name the fact that a correct program must keep true, and choose the method that keeps it. The nearest false friend is the heap shortest path routine of the previous chapter. It is a strong tool, yet it answers only questions about routes from one source.

<!-- stage: naive -->
### Reusing The Shortest Path Routine

The direct plan treats every request as a route question. For the cabling request it runs a shortest path search from site 0 over the undirected links. It buys the last link of each shortest route, so every site has its cheapest route from site 0 inside the bought set. The method below returns the total cost of the bought links. It returns -1 when some site has no route from site 0.

```java
static long shortestTreeCost(int n, int[][] links) {
    long[] dist = new long[n];
    int[] lastLink = new int[n];
    boolean[] done = new boolean[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[0] = 0;
    long total = 0;
    for (int round = 0; round < n; round++) {
        int u = -1;
        for (int v = 0; v < n; v++) {                      // pick the unfinished site with the smallest distance
            if (!done[v] && dist[v] != Long.MAX_VALUE && (u == -1 || dist[v] < dist[u])) u = v;
        }
        if (u == -1) return -1;
        done[u] = true;
        total += lastLink[u];                               // buy the link that gave u its best distance
        for (int[] e : links) {
            int other = e[0] == u ? e[1] : (e[1] == u ? e[0] : -1);
            if (other >= 0 && !done[other] && dist[u] + e[2] < dist[other]) {
                dist[other] = dist[u] + e[2];
                lastLink[other] = e[2];
            }
        }
    }
    return total;
}
```

The method is a correct shortest path search, so every site gets its cheapest route from site 0. The open question is whether those routes also give the cheapest set of cables.

```predict
Three sites 0, 1 and 2 have the links 0 to 1 at cost 4, 0 to 2 at cost 5 and 1 to 2 at cost 2. What does shortestTreeCost return, and what is the cheapest set of cables that connects the three sites?

The method returns 9. Site 1 is reached by the link of cost 4. Site 2 is reached directly for 5, because the route through site 1 costs 6. The bought links are 0 to 1 and 0 to 2. The cheapest connected set uses the links of cost 2 and 4, which total 6. The routine optimizes each route from site 0, not the sum of the bought links.
```

<!-- stage: bottleneck -->
### Wrong Answers And Slow Searches

#### The Cabling Answer Is Wrong

The triangle shows the first failure. A shortest path search fixes the cost of every route that starts at one site. The cabling request asks for the smallest sum over the bought links, which is a different quantity. The two answers differ whenever a direct link beats a route through a cheap detour. No change to the loop repairs this, because the loop is correct for its own question.

#### The Other Requests Cost Too Much

The bridge request fails for another reason. A shortest path search reports distances, and a bridge has no distance. A direct plan deletes each link in turn and searches again from one endpoint. With V sites and E links that costs O(E * (V + E)) time, which is about 10^12 steps for 200000 sites and one million links.

The tour request has no distance at all. A direct plan tries the orders of the links and backtracks, and the number of orders grows exponentially with the number of links. Even the warehouse request, which the routine can answer, costs O(V * (V + E) log V) when the routine starts from every site. On a dense map a table of all pairs costs O(V^3) and is simpler to write.

#### A Plan That Names The Need

A better plan names what each request needs and uses one method per need. The next stage lists the four matches.

<!-- stage: insight -->
### Match The Method To The Goal

Every request has an **objective**, which is the quantity or property that the final answer must optimize or satisfy. The objective decides which fact the program keeps true. A total over a chosen set of links points to a spanning tree method. A question about what one failure disconnects points to low links. A question about the distance between every pair points to a table that grows one intermediate vertex at a time. A requirement to use every link exactly once points to a trail.

<!-- names: objective, cut property, low link, intermediate, postorder -->

#### Cabling Follows The Cut Property

A **cut** splits the vertices into two sets. The **cut property** says that the lightest edge crossing a cut belongs to some minimum spanning tree, when no chosen edge crosses that cut. Kruskal applies it to the cut between one group and the rest. Prim applies it to the cut between the tree and the rest. Each accepted edge is therefore safe, and the chosen edges always form a forest. Stopping after `n - g` accepted edges leaves exactly `g` groups with the least total cost.

#### Bridges Follow Low Links

A **low link** is the value `low[u]` from the low links lesson. When `low[v] > disc[u]` for a child `v`, no edge from the subtree of `v` climbs to `u` or above, except the tree edge itself. That tree edge is then the only connection between the subtree and the rest, so it is a bridge. The test uses discovery times and never uses weights. The same search can also add up the vertices below `v`, which gives the size of one side of each bridge.

#### Distances Follow An Intermediate Limit

An **intermediate** is a vertex that a route passes through between its first and last vertex. After the round for `k`, the entry `dist[i][j]` holds the best route whose intermediates all have an index of at most `k`. Round `k` only compares the current entry with `dist[i][k] + dist[k][j]`. After the last round every pair has its final distance, so a question about every pair reads the table once.

#### Trails Follow Postorder

A **postorder** write happens after the walk has finished everything reachable from a vertex through unused links. Hierholzer writes a vertex only at that moment. The output read backward is a trail that uses each link once. Taking the smallest unused destination first at every vertex makes the trail the smallest in dictionary order.

<!-- stage: variables -->
### What Each Method Keeps

Every method reads its input and never changes it. Each one keeps a small piece of state that carries its fact, and the names below are the ones that the code uses.

- **parent** is an `int[]` of union-find links, and `find(x)` returns the root of the group of `x`.
- **disc** and **low** are `int[]` arrays of discovery times and low links, with -1 in `disc` meaning not yet reached and the clock starting at 0, as in the low links lesson.
- **dist** is a `long[][]` table of pair distances, and `Long.MAX_VALUE` means no route is known.
- **unused** holds one min-ordered queue of destinations per vertex, and the walk polls from it.
- **groups** counts the groups that remain, and the cabling loop stops when it reaches the target.

Every addition first checks the sentinel `Long.MAX_VALUE`, because the sum of two large values wraps to a negative number in Java.

<!-- stage: trace -->
### Two Small Networks Step By Step

#### Cabling With Union-Find

Five sites sit at the points (0,0), (1,3), (3,2), (2,6) and (6,5), and a cable between two sites costs the sum of the horizontal and vertical gaps. Each cell is one of the ten possible cables, written `a-b@cost` and sorted by cost. The pointer `edge` marks the cable under review. The variable `groups` lists the groups of sites, and `total` is the cost bought so far. At cable 0-2@5 the sites 0 and 2 already share a group through site 1, so the loop skips it. The loop stops at cable 3-4@5 because one group remains, and it never reads the last four cables.

```trace
{"cells":["1-2@3","0-1@4","1-3@4","0-2@5","2-3@5","3-4@5","2-4@6","1-4@7","0-3@8","0-4@11"],"pointers":["edge"],"steps":[{"at":{"edge":-1},"vars":{"groups":"{0} {1} {2} {3} {4}","total":0},"note":"Five groups of one site each. No cable is bought."},{"at":{"edge":0},"vars":{"groups":"{0} {1,2} {3} {4}","total":3},"note":"Cable 1-2@3 joins two groups, so the loop buys it. 4 groups remain."},{"at":{"edge":1},"vars":{"groups":"{0,1,2} {3} {4}","total":7},"note":"Cable 0-1@4 joins two groups, so the loop buys it. 3 groups remain."},{"at":{"edge":2},"vars":{"groups":"{0,1,2,3} {4}","total":11},"note":"Cable 1-3@4 joins two groups, so the loop buys it. 2 groups remain."},{"at":{"edge":3},"vars":{"groups":"{0,1,2,3} {4}","total":11},"note":"Cable 0-2@5: sites 0 and 2 share root 3, so the cable would close a cycle and the loop skips it."},{"at":{"edge":4},"vars":{"groups":"{0,1,2,3} {4}","total":11},"note":"Cable 2-3@5: sites 2 and 3 share root 3, so the cable would close a cycle and the loop skips it."},{"at":{"edge":5},"vars":{"groups":"{0,1,2,3,4}","total":16},"note":"Cable 3-4@5 joins two groups, so the loop buys it. Only one group remains, so the loop stops and never reads the last 4 cables."}]}
```

The total is 16. Notice that the skipped cables are exactly the ones whose endpoints already share a root.

#### Shortest Routes Cost More

The second network has four sites. Its links are 0 to 1 at cost 4, 0 to 2 at cost 5, 1 to 2 at cost 2 and 2 to 3 at cost 2. This trace runs the shortest path routine from site 0, which is the false friend for the cabling request. Each cell is a site, and the pointer `site` marks the site that the routine finishes. The variable `dist` lists the distances from site 0, and `bought` is the cost of the links that the routine has bought. The cheap link 1 to 2 never enters the bought set, because the direct link 0 to 2 gives site 2 a shorter route than the detour through site 1.

```trace
{"cells":[0,1,2,3],"pointers":["site"],"steps":[{"at":{"site":0},"vars":{"dist":"0,inf,inf,inf","bought":0},"note":"Only site 0 has a distance. Nothing is bought."},{"at":{"site":0},"vars":{"dist":"0,4,5,inf","bought":0},"note":"Site 0 is final at distance 0. Its links give site 1 the distance 4 and site 2 the distance 5."},{"at":{"site":1},"vars":{"dist":"0,4,5,inf","bought":4},"note":"Site 1 is final at distance 4, and the routine buys the link of cost 4. Route 0-1-2 costs 6, which is more than the stored 5, so site 2 keeps 5."},{"at":{"site":2},"vars":{"dist":"0,4,5,7","bought":9},"note":"Site 2 is final at distance 5, and the routine buys the direct link of cost 5. The cheap link 1-2@2 stays unbought. Site 3 gets distance 7."},{"at":{"site":3},"vars":{"dist":"0,4,5,7","bought":11},"note":"Site 3 is final at distance 7, and the routine buys the link of cost 2. The total is 11."}]}
```

The routine pays 11. A cheapest cable set for this four-site network buys the links of cost 2, 2 and 4, for a total of 8, so the routine overpays by 3.

<!-- stage: code -->
### Four Methods In Short Form

#### Cabling And Distances

The first method is Kruskal with union-find. It sorts a copy of the edges, so the caller's array keeps its order. It returns -1 when the sites do not end in one group.

```java
static long spanningCost(int n, int[][] edges) {
    int[][] sorted = edges.clone();
    Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));   // cheapest edge first
    int[] parent = new int[n];
    for (int i = 0; i < n; i++) parent[i] = i;
    long total = 0;
    int groups = n;
    for (int[] e : sorted) {
        int a = find(parent, e[0]), b = find(parent, e[1]);
        if (a == b) continue;                                       // equal roots: the edge would close a cycle
        parent[a] = b;
        total += e[2];
        groups--;
    }
    return groups == 1 ? total : -1;
}

static int find(int[] parent, int x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];                              // path halving keeps later finds short
        x = parent[x];
    }
    return x;
}
```

The second method counts, for every city, the other cities within a limit. The guard before the addition keeps the sentinel out of the arithmetic.

```java
static int[] countWithin(int n, int[][] roads, long limit) {
    long[][] dist = new long[n][n];
    for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE);
    for (int i = 0; i < n; i++) dist[i][i] = 0;
    for (int[] r : roads) {
        dist[r[0]][r[1]] = Math.min(dist[r[0]][r[1]], r[2]);
        dist[r[1]][r[0]] = Math.min(dist[r[1]][r[0]], r[2]);
    }
    for (int k = 0; k < n; k++)                                     // the intermediate vertex is the outer loop
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] != Long.MAX_VALUE && dist[k][j] != Long.MAX_VALUE
                        && dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
    int[] near = new int[n];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (i != j && dist[i][j] <= limit) near[i]++;           // the sentinel is larger than any limit
    return near;
}
```

#### Bridges And Trails

The third method counts bridges with one depth-first search. It skips the parent edge by edge number, so repeated links between two sites would still count as back edges.

```java
static int countBridges(int n, int[][] links) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int id = 0; id < links.length; id++) {
        adj.get(links[id][0]).add(new int[] {links[id][1], id});
        adj.get(links[id][1]).add(new int[] {links[id][0], id});
    }
    int[] disc = new int[n], low = new int[n], state = new int[2];  // state: {clock, bridges}
    Arrays.fill(disc, -1);                                          // -1 marks an unreached vertex
    for (int s = 0; s < n; s++) if (disc[s] == -1) visit(s, -1, adj, disc, low, state);
    return state[1];
}

static void visit(int u, int viaId, List<List<int[]>> adj, int[] disc, int[] low, int[] state) {
    disc[u] = low[u] = state[0]++;
    for (int[] e : adj.get(u)) {
        if (e[1] == viaId) continue;                                // never reuse the edge that entered u
        if (disc[e[0]] == -1) {
            visit(e[0], e[1], adj, disc, low, state);
            low[u] = Math.min(low[u], low[e[0]]);
            if (low[e[0]] > disc[u]) state[1]++;                    // no way around the tree edge
        } else {
            low[u] = Math.min(low[u], disc[e[0]]);                  // a back edge lowers the low link
        }
    }
}
```

The fourth method returns an Eulerian trail from a given start that takes the smallest unused destination first. It assumes that a trail exists.

```java
static List<Integer> trailFrom(int n, int[][] links, int start) {
    List<PriorityQueue<Integer>> unused = new ArrayList<>();
    for (int i = 0; i < n; i++) unused.add(new PriorityQueue<>());
    for (int[] l : links) unused.get(l[0]).add(l[1]);
    Deque<Integer> stack = new ArrayDeque<>();
    LinkedList<Integer> trail = new LinkedList<>();
    stack.push(start);
    while (!stack.isEmpty()) {
        PriorityQueue<Integer> q = unused.get(stack.peek());
        if (q.isEmpty()) trail.addFirst(stack.pop());               // dead end: the postorder write
        else stack.push(q.poll());                                  // consume the smallest unused link
    }
    return trail;
}
```

Each method costs what its lesson states. The sorted edges take O(E log E), the table takes O(V^3), the search takes O(V + E), and the trail with queues takes O(E log E).

<!-- stage: applicability -->
### Choosing Among The Graph Methods

#### Reading The Goal

Read the sentence that states what the answer must be. A smallest total cost over links that connect everything calls for a spanning tree method, and a count of groups to leave behind changes only the stopping rule. A request for the links that disconnect the network calls for low links. A request that compares every pair of sites with a distance limit calls for the table, as long as the map is small enough for a cubic loop. A request to use every link once and to print the order calls for the trail walk. A route from one source with a cost per step calls for the heap search from the previous chapter. Shortest paths with negative edges and strong components of a directed graph lie outside these four goal families. Lesson 01 covers the first, and lesson 06 covers the second.

#### Checking The Invariant

An **invariant** is a fact that holds before and after every step of a loop. For the spanning tree loops, the chosen edges always lie inside some minimum spanning tree. For low links, `low[u]` is final once the visit of `u` returns. For the table, every entry is the best route with the allowed intermediates. For the trail, the output read backward is a valid tail of the trail. Test each method on a single vertex, on a disconnected map, and on repeated links between two sites.

#### Avoiding The False Friend

A **false friend** is a method that fits the wording of a statement but keeps a different fact true. The shortest path routine is the false friend for cabling, because it fixes routes from one site and never minimizes the sum. A spanning tree is the false friend for distances, because the path between two sites inside a minimum tree can be longer than their shortest route. Deleting links one at a time is a false friend for bridges, because it works and costs far too much. Check the answer type before the method type, since one structure does not solve every objective.

<!-- stage: exercises -->
### Exercises

#### [Build] Cheapest Cables For Exactly g Groups (LeetCode 1584)
<!-- id: ga-ch-cable-groups -->

**Prerequisites.** Kruskal with union-find from this chapter.

**Problem.** Each entry `[x, y]` of `points` is a distinct site on a plane. A cable between two sites costs `|x1 - x2| + |y1 - y2|`. A set of cables leaves the sites in groups, and two sites share a group when a chain of cables joins them. Given `g`, return the smallest total cost of a set of cables that leaves exactly `g` groups, as a `long`.

**Constraints.** The limits are:
- **Sites** satisfy `1 <= points.length <= 400`, and all points differ.
- **Coordinates** are integers with `|x|, |y| <= 1000000`.
- **Groups** satisfy `1 <= g <= points.length`.
- **Result** is a `long`, and `g = points.length` gives 0.
- **Input** stays unchanged.

**Example 1.** Input `points = [[1,1],[3,4],[8,1],[6,6],[2,7]]`, `g = 2`, output `14`.

**Example 2.** Input `points = [[1,1],[3,4],[8,1],[6,6],[2,7]]`, `g = 5`, output `0`.

**Hint.** How many cables must a loop accept to turn `n` single-site groups into `g` groups?

**Changed decision.** The loop stops after `n - g` accepted cables instead of `n - 1`. The result is then a forest with `g` trees, not one spanning tree.

#### [Vary] Bridges With Large Sides (LeetCode 1192)
<!-- id: ga-ch-bridges-by-size -->

**Prerequisites.** The low links lesson and the exercise above.

**Problem.** A network has servers `0` to `n - 1` and undirected connections `[a, b]` in `connections`. The network is connected, and no connection repeats or joins a server to itself. A critical connection is a connection whose removal leaves two components. Given `s`, return every critical connection whose two components each hold at least `s` servers. Write each connection as `[smaller, larger]` and sort the list by the first entry, then by the second.

**Constraints.** The limits are:
- **Servers** satisfy `2 <= n <= 1000`.
- **Connections** satisfy `n - 1 <= connections.length <= 3000`.
- **Size bound** satisfies `1 <= s <= n`.
- **Result** is an empty list when no connection qualifies.
- **Input** stays unchanged.

**Example 1.** Input `n = 8`, `connections = [[0,1],[1,2],[2,0],[1,3],[3,4],[4,5],[5,3],[3,6],[6,7]]`, `s = 2`, output `[[1,3],[3,6]]`.

**Example 2.** Input `n = 4`, `connections = [[0,1],[1,2],[2,3]]`, `s = 2`, output `[[1,2]]`.

**Hint.** When the search returns from a child `v`, which count gives the number of servers on the far side of the tree edge?

**Changed decision.** The search also sums subtree sizes. The method reports a bridge only when its subtree size and `n` minus that size both reach `s`. It then sorts the output.

#### [Boundary] City With Fewest Strictly Near Cities (LeetCode 1334)
<!-- id: ga-ch-city-strict -->

**Prerequisites.** The Floyd-Warshall lesson.

**Problem.** There are `n` cities numbered from `0`, and `roads` lists undirected roads `[a, b, w]` of length `w`. Given `limit`, a city `y` is near a city `x` when `y != x` and the shortest distance from `x` to `y` is strictly less than `limit`. Return the city with the fewest near cities. When several cities tie, return the one with the greatest index.

**Constraints.** The limits are:
- **Cities** satisfy `2 <= n <= 100`.
- **Roads** satisfy `1 <= roads.length <= n * (n - 1) / 2`, and each pair of cities appears at most once.
- **Lengths** are integers with `1 <= w <= 10000`.
- **Limit** satisfies `1 <= limit <= 10000`.

**Example 1.** Input `n = 4`, `roads = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]`, `limit = 5`, output `3`.

**Example 2.** Input `n = 4`, `roads = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]`, `limit = 3`, output `0`.

**Hint.** A city at distance exactly `limit` is not near. Which comparison operator must the final count use?

**Changed decision.** Near means strictly below the limit, and the final scan replaces the best city on a tie, so the greatest index wins.

#### [Recognize] Reconstruct Itinerary (LeetCode 332)
<!-- id: ga-ch-itinerary-smallest -->

**Prerequisites.** The Hierholzer lesson.

**Problem.** The list `tickets` holds pairs `[from, to]` of airport codes, and each pair is one flight. A trip starts at `JFK` and uses every ticket exactly once. Return the trip as a list of airport codes. Among all valid trips, return the smallest one when the codes are compared one position at a time as strings. At least one valid trip exists.

**Constraints.** The limits are:
- **Tickets** satisfy `1 <= tickets.length <= 300`, and equal tickets may repeat.
- **Codes** are strings of three uppercase letters.
- **Validity** is guaranteed, so the result has `tickets.length + 1` codes.
- **Input** stays unchanged.

**Example 1.** Input `tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]`, output `["JFK","ATL","JFK","SFO","ATL","SFO"]`.

**Example 2.** Input `tickets = [["JFK","AAA"],["AAA","JFK"],["JFK","AAA"],["AAA","BBB"]]`, output `["JFK","AAA","JFK","AAA","BBB"]`.

**Hint.** Which vertex does the walk write to the output first, and why must the output be reversed at the end?

**Changed decision.** Each airport keeps a queue of destinations ordered from smallest to largest. The walk polls the smallest, and the method reverses the output once.
