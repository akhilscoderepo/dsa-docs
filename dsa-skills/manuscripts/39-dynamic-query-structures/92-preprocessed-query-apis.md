<!-- lesson-kind: combination -->
<!-- lesson-id: preprocessed-query-apis -->
## Preprocessed Query APIs

<!-- stage: context -->
### Why The Org Chart Lookup Crawls

An internal directory service stores a company org chart with 100,000 employees. Each employee record holds one pointer to a direct manager. A reporting tool asks questions such as who sits 25 levels above an employee, and it asks them all day, 100,000 times per run. The first version walks the manager pointer once per level. On the test data the chart is shallow, and the answers return instantly. In a company that grew by promoting one chain of managers, the chart is 50,000 levels deep. A single question then walks tens of thousands of pointers, and a full run of 100,000 questions spends about 5 billion pointer reads on a chart that never changed.

Every answer is correct, so no test fails. The cost comes from repeating the same climb for each question. A second problem appears when the data does change. The same service also stores approval links between employees, each with a cost, and another tool asks whether two employees connect through links that all cost less than a limit. New links arrive all day. If the service stores extra data to speed up either question, a promotion or a new link can make that data wrong. This lesson asks what the constructor should store once, and how the number of constructor calls, updates and queries decides whether that stored data pays for itself.

<!-- stage: contributions -->
### What The Earlier Lessons Contribute

The lesson Query Planning supplied the habit of naming the workload before choosing a structure. It asked how many updates there are, how many queries there are and whether all queries are known at the start. It also supplied the sorted list of positions for one value, and the rule that a range has one stated endpoint convention. This lesson reuses the habit and the sorted lists, and it applies them to objects that answer a stream of calls.

The lesson Dynamic Graph Queries supplied the comparison between rebuilding a table after every change and repairing only what a change can affect. It also supplied the counting of operations as a function of the number of updates and queries. Those two ideas explain why an object that stores a derived index must decide when that index is still valid.

The new work is the combination. A derived index is built in the constructor, read by every query and damaged by some updates. The lesson shows how to price the three kinds of calls separately, how to detect the updates that really damage the index, and how to postpone the repair until a query needs it.

<!-- stage: naive -->
### Walking Up One Level At A Time

The direct design keeps the parent array and answers each question with a loop. The loop moves to the parent once per requested level, and it stops with `-1` when the root has no parent.

```java
final class WalkAncestor {
    private final int[] parent;                 // parent[0] is -1 for the root

    WalkAncestor(int[] parent) { this.parent = parent.clone(); }

    int kth(int node, int k) {
        int cur = node;
        for (int i = 0; i < k && cur != -1; i++) {
            cur = parent[cur];                  // one pointer read per requested level
        }
        return cur;                             // -1 when the chain ends before k levels
    }
}
```

With `parent = {-1, 0, 0, 1}`, the call `kth(3, 2)` returns 0, and `kth(3, 3)` returns -1 because the root has no parent. The class needs no setup and uses no extra memory. It is correct on every small chart.

```predict
The chart is one chain of 50000 employees, and the tool asks 100000 questions about the employee at the bottom with k near 49999. How many parent reads does the run perform, and how many different answers can those questions have?

Each question walks about 50000 levels, so the run performs about 5 billion parent reads. The chain has 50000 employees, so at most 50000 different answers exist for a fixed start, and most reads repeat a climb that an earlier question already did. The cost is the product of the number of questions and the depth, and neither factor shrinks as the questions repeat.
```

<!-- stage: bottleneck -->
### Cost That Multiplies With Depth

Let `n` be the number of employees, `q` the number of questions and `k` the number of levels asked. One call costs O(k) time, and k can reach n - 1. A run therefore costs O(q * n) in the worst case, which is 5 * 10^9 reads for q = 100,000 and n = 50,000. The class stores nothing beyond the input, so the cost never improves, however many questions arrive.

The repeated work has a clear shape. Two questions about nodes on the same chain climb through the same pointers. The answer for 25 levels is the answer for 16 levels followed by 9 levels, and each of those pieces can also be split further. The naive loop recomputes every such piece from the start for every question.

Three requirements follow. A question must cost far less than the number of levels it asks. The extra data must be small enough to keep in memory next to the input. If the chart can change, the object must also say which changes make the stored data wrong, and it must repair that data at a cost that matches how often changes happen. A design that builds fast lookups but rebuilds them on every change can lose to the loop above, which is why the counts of constructor calls, updates and queries must enter the decision.

<!-- stage: insight -->
### Store Power-Of-Two Jumps And Price Each Call

#### Jumps By Powers Of Two

Every distance k is a sum of distinct powers of two, which is the binary form of k. If the object knows the ancestor `2^j` levels up for every node and every `j`, a query of k levels needs only one jump for each set bit of k. This storage scheme is called binary lifting.

<!-- names: binary lifting, call mix, stale index -->

The table has a row `j` for each power. Row 0 is the parent array. Row `j` comes from row `j - 1`, because `2^j` levels are two jumps of `2^(j-1)` levels. A node lacking an ancestor that far holds `-1`, and no jump starts from `-1`. Building about `log n` rows of `n` entries costs O(n log n), and each query costs O(log k). With `n = 100000` the table has 17 rows, which is 1.7 million entries, and the run of 100,000 questions reads at most 1.7 million of them.

#### The Call Mix Decides

The **call mix** is the three counts of a run: constructor calls, updates and queries. Let `C` be the cost of building the index, `U` the cost of repairing it after one update and `Q` the cost of one query. A run costs about `C + u * U + q * Q`, where `u` and `q` count the updates and the queries. The naive loop has `C = 0` and a large `Q`. The jump table trades a large `C` for a small `Q`, so it wins once `q` repays `C`.

The same arithmetic shows when an index loses. Suppose every update forces a full rebuild with `U = C`, and one query follows each update. The run then costs about `u * C`, and a direct search per query can match that without extra memory. Indexing pays only when damaging updates are rarer than queries, or when repair costs far less than construction.

#### Limit Queries Use A Spanning Forest

The approval-link question asks whether `p` and `q` connect through links that all weigh less than `limit`. A **minimum spanning forest** keeps just enough cheap links to join every connected group. Kruskal's method builds it by scanning links from lightest to heaviest and accepting a link only when its endpoints sit in different trees. Between two connected vertices the forest holds one route, and its heaviest link, called the bottleneck, is the lowest ceiling that any route can achieve. A limit query returns true exactly when the bottleneck is smaller than `limit`.

Consider four vertices with links 0-1 at weight 5, 1-2 at weight 2, 0-2 at weight 9 and 2-3 at weight 7. Kruskal accepts weights 2, 5 and 7, then rejects 9 because vertices 0 and 2 are already connected. The forest route from 0 to 3 is 0-1-2-3, and its bottleneck is 7. So `query(0, 3, 8)` returns true, while `query(0, 3, 7)` returns false because 7 is not below 7. The rejected weight 9 can never matter, since a cheaper route between its endpoints exists.

#### Detect Damage And Rebuild Later

A **stale index** is an index that no longer matches the data. Not every update makes it stale. An edge added to a graph whose minimum spanning forest already contains a path with all edges at most as heavy leaves the forest unchanged, so the index stays valid. An edge damages the index only when its ends lie in different trees or its weight is below the bottleneck between them. The object checks this with one bottleneck query when the index is fresh, and it sets a stale mark only when the edge can change an answer.

After the mark is set, later updates skip the check, because a single rebuild covers them all. The next query performs that rebuild and clears the mark. One thousand damaging updates followed by one query cost a single rebuild, while harmless updates cost none. This deferral is what turns the construction cost into an amortized cost spread over the queries.

<!-- stage: variables -->
### Fields Of An Index Behind An Object

An object with a maintained index stores the data it was given, the index built from it and the facts that decide when to repair the index.

- **n** is the number of nodes, fixed at construction.
- **rows** is the number of table rows, the smallest `r` with `2^r >= n`.
- **up** is the table, where `up[j][v]` is the ancestor of `v` that is `2^j` levels up, or `-1`.
- **forest** is the index of the limit-query structure, a minimum spanning forest with its own jump table.
- **stale** is a `boolean` that is true when an update has made the index wrong.
- **rebuilds** counts the repairs performed after construction, which tests use to check the plan.

In the first trace, the pointer `node` marks the node where a query currently stands, and `-1` means the query left the tree. In the second trace, the pointers `p` and `q` mark the two nodes named by the current call, and the cells list the four vertices.

The invariant is that after every call, a clear `stale` mark means the index answers like a fresh build from the stored data, and a set mark means a rebuild before the next answer restores that property.

<!-- stage: trace -->
### Tracing Jumps And Rebuilds

#### Jumps On A Deep Chain

The tree below has 12 nodes. Node 0 is the root, nodes 0 to 7 form a chain, and nodes 8 to 11 form a second chain that hangs below node 2. The first query asks for the ancestor of node 11 that is 5 levels up. The number 5 is 101 in binary, so bits 0 and 2 are set. Bit 0 moves one level and bit 2 moves four levels, which together reach node 1 in two table reads and not in five pointer reads. The second query asks for the ancestor of node 6 that is 9 levels up. Bit 0 moves the query to node 5. Bit 3 asks for a jump of eight levels from node 5, and node 5 has only five ancestors above it, so the table holds `-1` and the answer is -1.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10","11"],"pointers":["node"],"steps":[{"at":{"node":11},"vars":{"query":"kth(11,5)","bit":"-","left":5,"result":"start"},"note":"Query kth(11, 5). The binary form of 5 is 101, so the loop reads 2 set bits."},{"at":{"node":10},"vars":{"query":"kth(11,5)","bit":0,"left":4,"result":"pending"},"note":"Bit 0 is set, so one read of the table row 0 moves the query 1 step up, to node 10."},{"at":{"node":1},"vars":{"query":"kth(11,5)","bit":2,"left":0,"result":1},"note":"Bit 2 is set, so one read of the table row 2 moves the query 4 steps up, to node 1. No bits remain, so the answer is 1."},{"at":{"node":6},"vars":{"query":"kth(6,9)","bit":"-","left":9,"result":"start"},"note":"Query kth(6, 9). The binary form of 9 is 1001, so the loop reads 2 set bits."},{"at":{"node":5},"vars":{"query":"kth(6,9)","bit":0,"left":8,"result":"pending"},"note":"Bit 0 is set, so one read of the table row 0 moves the query 1 step up, to node 5."},{"at":{"node":-1},"vars":{"query":"kth(6,9)","bit":3,"left":0,"result":-1},"note":"Bit 3 is set, so one read of the table row 3 moves the query 8 steps up, to outside the tree. No bits remain, so the answer is -1."}]}
```

#### Updates Against A Stale Mark

The second trace uses a graph with four vertices and one initial edge, and the query asks whether a path exists with every edge below a limit. The constructor builds the index and starts with a clear mark. An edge that connects two separate trees sets the mark. An edge that is not lighter than the heaviest forest edge between its ends leaves the mark clear. While the mark is set, the next insertion only stores its edge. The first query after a set mark pays for exactly one rebuild. The final count of rebuilds is 2, because the insertions of weight 7 and weight 2 each set the mark, the insertion of weight 9 leaves it clear, and the insertion of weight 3 arrives while the mark is set, so the rebuild already pending covers it.

```trace
{"cells":["0","1","2","3"],"pointers":["p","q"],"steps":[{"at":{"p":0,"q":1},"vars":{"call":"new(4,[0-1:5])","result":"none","stale":"false","rebuilds":0},"note":"The constructor builds the index once. That build is not counted, so rebuilds starts at 0."},{"at":{"p":2,"q":3},"vars":{"call":"add(2,3,7)","result":"none","stale":"true","rebuilds":0},"note":"addEdge(2,3,7) joins two different trees of the forest, because no stored path connects 2 and 3, so the index becomes stale."},{"at":{"p":0,"q":1},"vars":{"call":"query(0,1,6)","result":"true","stale":"false","rebuilds":1},"note":"The index is stale, so this query rebuilds it first. query(0,1,6) asks for a path with every edge below 6 and returns true."},{"at":{"p":0,"q":1},"vars":{"call":"add(0,1,9)","result":"none","stale":"false","rebuilds":1},"note":"addEdge(0,1,9) is not lighter than 5, the heaviest forest edge between 0 and 1, so the index stays fresh."},{"at":{"p":1,"q":2},"vars":{"call":"add(1,2,2)","result":"none","stale":"true","rebuilds":1},"note":"addEdge(1,2,2) joins two different trees of the forest, because no stored path connects 1 and 2, so the index becomes stale."},{"at":{"p":0,"q":1},"vars":{"call":"add(0,1,3)","result":"none","stale":"true","rebuilds":1},"note":"addEdge(0,1,3) only stores the edge, because the index is already stale and the next query rebuilds."},{"at":{"p":0,"q":2},"vars":{"call":"query(0,2,4)","result":"true","stale":"false","rebuilds":2},"note":"The index is stale, so this query rebuilds it first. query(0,2,4) asks for a path with every edge below 4 and returns true."},{"at":{"p":2,"q":3},"vars":{"call":"query(2,3,7)","result":"false","stale":"false","rebuilds":2},"note":"query(2,3,7) asks for a path with every edge below 7 and returns false."},{"at":{"p":2,"q":3},"vars":{"call":"query(2,3,8)","result":"true","stale":"false","rebuilds":2},"note":"query(2,3,8) asks for a path with every edge below 8 and returns true."}]}
```

<!-- stage: code -->
### A Jump Table And A Lazy Rebuild

#### The Jump Table

The class `LiftTable` builds the table from the parent array and answers a query with one read per set bit. A set `-1` entry stays `-1` all the way up. The constructor cost is the only place where the table is written, so the object never changes after construction.

```java
final class LiftTable {
    private final int[][] up;
    private final int n;

    LiftTable(int[] parent) {
        n = parent.length;
        int rows = 1;
        while ((1 << rows) < n) rows++;                  // enough rows for any distance below n
        up = new int[rows][];
        up[0] = parent.clone();
        for (int j = 1; j < rows; j++) {
            up[j] = new int[n];
            for (int v = 0; v < n; v++) {
                int mid = up[j - 1][v];                  // half of the jump
                up[j][v] = mid == -1 ? -1 : up[j - 1][mid];
            }
        }
    }

    int kth(int node, int k) {
        if (k >= n) return -1;                           // no ancestor that far exists
        int cur = node;
        for (int j = 0; k >> j != 0 && cur != -1; j++) {
            if ((k >> j & 1) == 1) cur = up[j][cur];     // one table read per set bit
        }
        return cur;
    }
}
```

#### The Forest Behind Limit Queries

The class `BottleneckForest` builds the minimum spanning forest with Kruskal's method, roots each tree and fills the same kind of jump table as `LiftTable`. A second table `heavy` stores the heaviest edge on each jump. A query lifts the deeper vertex to the depth of the other, then lifts both until their parents agree, and keeps the largest edge it crosses. It returns `Integer.MAX_VALUE` when the two vertices lie in different trees. The code of both classes follows the next paragraph.



The class `LazyIndex` wraps a real `BottleneckForest`. It stores every edge, keeps the forest built from them and sets the stale mark only for an update that can lower a bottleneck. The query rebuilds the forest first when the mark is set. In the directory, `addEdge` is a new approval link, `query` is the question about a cost limit, and a rebuild reruns Kruskal's method on all stored links.

```java
final class BottleneckForest {
    private final int[][] up;                            // up[j][v] is the 2^j-th ancestor in the forest, or -1
    private final int[][] heavy;                         // heavy[j][v] is the heaviest edge on that jump
    private final int[] depth;
    private final int rows;

    BottleneckForest(int n, java.util.List<int[]> edges) {
        java.util.List<int[]> sorted = new java.util.ArrayList<>(edges);
        sorted.sort((x, y) -> Integer.compare(x[2], y[2]));   // lightest edge first
        int[] dsu = new int[n];
        for (int i = 0; i < n; i++) dsu[i] = i;
        java.util.List<java.util.List<int[]>> adj = new java.util.ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new java.util.ArrayList<>());
        for (int[] e : sorted) {
            int a = find(dsu, e[0]), b = find(dsu, e[1]);
            if (a == b) continue;                        // the ends are already joined by lighter edges
            dsu[a] = b;
            adj.get(e[0]).add(new int[] {e[1], e[2]});
            adj.get(e[1]).add(new int[] {e[0], e[2]});
        }
        int r = 1;
        while ((1 << r) < n) r++;
        rows = r;
        up = new int[rows][n];
        heavy = new int[rows][n];
        depth = new int[n];
        java.util.Arrays.fill(up[0], -1);
        boolean[] seen = new boolean[n];
        for (int root = 0; root < n; root++) {
            if (seen[root]) continue;
            seen[root] = true;
            java.util.ArrayDeque<Integer> queue = new java.util.ArrayDeque<>();
            queue.add(root);
            while (!queue.isEmpty()) {                   // breadth-first search roots the tree
                int v = queue.poll();
                for (int[] nb : adj.get(v)) {
                    if (seen[nb[0]]) continue;
                    seen[nb[0]] = true;
                    up[0][nb[0]] = v;
                    heavy[0][nb[0]] = nb[1];
                    depth[nb[0]] = depth[v] + 1;
                    queue.add(nb[0]);
                }
            }
        }
        for (int j = 1; j < rows; j++) {
            for (int v = 0; v < n; v++) {
                int mid = up[j - 1][v];
                if (mid == -1) { up[j][v] = -1; continue; }
                up[j][v] = up[j - 1][mid];
                heavy[j][v] = Math.max(heavy[j - 1][v], heavy[j - 1][mid]);
            }
        }
    }

    private static int find(int[] d, int x) {
        while (d[x] != x) { d[x] = d[d[x]]; x = d[x]; }
        return x;
    }

    int bottleneck(int p, int q) {
        if (p == q) return 0;                            // an empty path has no edge
        if (depth[p] < depth[q]) { int t = p; p = q; q = t; }
        int best = 0, diff = depth[p] - depth[q];
        for (int j = 0; j < rows; j++) {
            if ((diff >> j & 1) == 1) { best = Math.max(best, heavy[j][p]); p = up[j][p]; }
        }
        if (p == q) return best;                         // q was an ancestor of p
        for (int j = rows - 1; j >= 0; j--) {
            if (up[j][p] != up[j][q]) {                  // jump only while the two sides stay apart
                best = Math.max(best, Math.max(heavy[j][p], heavy[j][q]));
                p = up[j][p];
                q = up[j][q];
            }
        }
        if (up[0][p] == -1) return Integer.MAX_VALUE;    // different trees have no common parent
        return Math.max(best, Math.max(heavy[0][p], heavy[0][q]));
    }
}

final class LazyIndex {
    private final int n;
    private final java.util.List<int[]> edges = new java.util.ArrayList<>();
    private BottleneckForest forest;
    private boolean stale;
    private int rebuilds;

    LazyIndex(int n, java.util.List<int[]> initial) {
        this.n = n;
        edges.addAll(initial);
        forest = new BottleneckForest(n, edges);         // the constructor build is not counted
    }

    void addEdge(int u, int v, int w) {
        edges.add(new int[] {u, v, w});                  // the data always changes
        if (stale) return;                               // a pending rebuild already covers this edge
        if (damages(u, v, w)) stale = true;              // only a damaging edge marks the index
    }

    boolean query(int p, int q, int limit) {
        if (stale) {                                     // pay the repair once, at the first read
            forest = new BottleneckForest(n, edges);
            stale = false;
            rebuilds++;
        }
        return forest.bottleneck(p, q) < limit;          // a path exists when its heaviest edge is below limit
    }

    int rebuildCount() { return rebuilds; }

    private boolean damages(int u, int v, int w) {
        return w < forest.bottleneck(u, v);              // joins two trees, or beats the heaviest forest edge
    }
}
```

#### Cost

- **Constructor** costs O(n log n) time for the table of `n log n` entries.
- **Forest build** sorts the `E` edges and fills two tables, so it costs O(E log E + n log n) time.
- **Query** costs O(log k) time and O(1) extra memory.
- **Update** costs O(1) when a rebuild is pending, O(log n) for the damage check otherwise, and one full forest build is charged to the next query.

<!-- stage: applicability -->
### When A Maintained Index Pays Off

#### Recognizing The Pattern

Use a maintained index when the data is read far more often than it changes, and when each read would otherwise repeat the same work. Before coding, write down three numbers and one promise: the number of constructor calls, updates and queries, and whether the calls are known in advance. When all calls are known in advance, an offline plan that sorts or batches the queries can avoid the index altogether. When calls arrive one at a time, the index must answer each from stored state. The invariant to protect is that every answer equals the answer of a fresh build from the stored data.

#### False Friends

A rebuild on a timer looks like a repair rule, and it is a false friend. Between two ticks the index is stale, so the answers depend on when the timer last ran. A second false friend is a larger index for a smaller workload. A jump table for a chart of 100,000 employees stores 1.7 million entries, while 1,000 queries on a chart of depth 30 walk at most 30,000 pointers, so the naive loop wins.

#### When The Method Does Not Apply

If every update damages the index and queries are rare, the lazy rebuild runs once per query and costs more than a direct search. The design then drops the index. If the updates can be repaired locally, as in the distance array of the last exercise, a repair that touches only the affected entries beats a rebuild, and the object keeps the index without any stale mark.

<!-- stage: exercises -->
### Exercises

#### [Build] Kth Ancestor Of A Tree Node (LeetCode 1483)
<!-- id: dq39-kth-ancestor -->

**Prerequisites.** The jump table and the bit-by-bit query from this lesson.

**Problem.** Design a class `TreeAncestor`. Its constructor receives the integer `n` and an array `parent` of length `n`, where `parent[i]` is the parent of node `i` and `parent[0] = -1` marks the root. The method `getKthAncestor(node, k)` returns the ancestor of `node` that is `k` edges above it, or `-1` when the path to the root has fewer than `k` edges. The tree never changes, so the workload has one constructor call, zero updates and many queries. The queries arrive one at a time, so they are not known in advance.

**Constraints.** The limits are:
- **n** satisfies `1 <= n <= 5 * 10^4`, and parent labels need not be smaller than the child label.
- **node** satisfies `0 <= node < n`, and **k** satisfies `0 <= k <= n`.
- **Calls** are one constructor call and up to `5 * 10^4` queries.
- **Return value** is an `int`, and `k = 0` returns `node`.

**Example 1.** Input `n = 9`, `parent = [-1,0,0,1,1,2,3,6,6]` and queries `(8,2)`, `(8,3)`, `(8,4)`, `(4,1)`, `(4,2)`, `(5,0)`; output `[3, 1, 0, 1, 0, 5]`.

**Example 2.** Input `n = 5`, `parent = [-1,0,1,2,3]` and queries `(4,4)`, `(4,5)`, `(2,1)`, `(0,1)`; output `[0, -1, 1, -1]`.

**Hint.** Which power-of-two jumps add up to `k`, and what must a row store for a node that has no ancestor that far away?

**Changed decision.** The constructor stores a table of about `log n` rows, so each query stops walking and reads one entry per set bit of `k`.

#### [Vary] Counting Values In A Range (LeetCode 2080)
<!-- id: dq39-value-range-count -->

**Prerequisites.** The Kth Ancestor exercise above and the sorted position lists of the lesson Query Planning. The structure is a merge-sort tree, a segment tree whose every node keeps the values of its index segment in sorted order. This exercise changes the contract of LeetCode 2080: a query counts every value inside a value range and not one fixed value.

**Problem.** Design a class `RangeValueCount`. Its constructor receives an integer array `arr`. The method `count(left, right, lo, hi)` returns the number of indices `i` with `left <= i <= right` and `lo <= arr[i] <= hi`. Both pairs of bounds are inclusive, and `lo > hi` returns 0. The array never changes, so the workload has zero updates and many queries. The queries arrive one at a time and are not known in advance, so sorting them is not available.

**Constraints.** The limits are:
- **n** is `arr.length` with `1 <= n <= 10^5`.
- **Values** are `int` values from -10^9 to 10^9, with duplicates allowed.
- **Indices** satisfy `0 <= left <= right < n`, and **lo** and **hi** are any `int` values.
- **Calls** are one constructor call and up to `10^5` queries, and the array is not modified.

**Example 1.** Input `arr = [5,1,5,9,2,5,9,1]` and queries `(0,7,1,5)`, `(2,5,5,9)`, `(3,3,10,20)`, `(0,4,6,8)`, `(1,6,2,2)`; output `[6, 3, 0, 0, 1]`.

**Example 2.** Input `arr = [-3,-3,0,7,-3]` and queries `(0,4,-3,-3)`, `(1,3,-5,0)`, `(0,4,1,6)`, `(2,4,-10,10)`; output `[3, 2, 0, 3]`.

**Hint.** One position list per value needs one search per distinct value in the range. A merge-sort tree keeps the values of each segment sorted. How many segments cover `[left, right]`, and how many binary searches does one segment need?

**Changed decision.** The summary changes from one list of positions per value to a merge-sort tree with one sorted list of values per index segment. A query touches O(log n) segments and runs two binary searches in each, so it costs O(log^2 n) time, and the tree stores `n log n` entries.

#### [Boundary] Limit Queries On A Growing Graph (LeetCode 1724)
<!-- id: dq39-growing-limited-paths -->

**Prerequisites.** The Vary exercise above, the minimum spanning forest from the lesson Query Planning and the stale mark from this lesson. This exercise changes the contract of LeetCode 1724: edges can be added after construction, and the answers must always reflect every edge added so far.

**Problem.** Design a class `GrowingPaths`. Its constructor receives `n` vertices numbered `0` to `n - 1` and an initial list of undirected edges `{u, v, w}`. The method `addEdge(u, v, w)` inserts one edge. The method `query(p, q, limit)` returns `true` when a path from `p` to `q` exists that uses only edges with weight strictly less than `limit`, and `false` otherwise. The method `rebuildCount()` returns how many times the index was rebuilt after the constructor. The index rebuilds exactly once inside a `query` call whenever an `addEdge` since the previous rebuild, made while the index was not stale, either joined two different trees of the minimum spanning forest or was strictly lighter than the heaviest forest edge between its endpoints. An insertion made while the index is already stale only stores the edge. The workload mixes insertions and queries in any order, and calls arrive one at a time.

**Constraints.** The limits are:
- **n** satisfies `1 <= n <= 10^4`, with up to `10^5` edges in total and up to `10^5` calls.
- **Weights and limits** are `int` values from 1 to 10^9, and self-loops and parallel edges may appear.
- **Vertices** satisfy `0 <= p, q, u, v < n`, and a query with `p == q` returns `true`.
- **Constructor build** does not count in `rebuildCount()`.

**Example 1.** Input `n = 5`, initial edges `{0,1,3}`, `{1,2,6}`, then calls `query(0,2,7)`, `addEdge(0,2,9)`, `query(0,2,6)`, `addEdge(0,2,4)`, `addEdge(3,4,2)`, `query(0,2,5)`, `query(3,4,3)`, `addEdge(0,1,3)`, `query(0,2,5)`, `query(2,3,100)`; output: the query results are `true, false, true, true, true, false` and `rebuildCount()` is 1.

**Example 2.** Input `n = 4`, no initial edges, then calls `query(0,1,5)`, `addEdge(0,1,4)`, `addEdge(0,1,4)`, `addEdge(0,1,2)`, `addEdge(1,1,1)`, `query(0,1,3)`, `query(0,1,2)`, `addEdge(2,3,8)`, `addEdge(1,2,1)`, `query(0,3,9)`, `query(0,3,8)`; output: the query results are `false, true, false, true, false` and `rebuildCount()` is 2.

**Hint.** Which value on the tree route between two vertices decides every limit query, and which new edges leave that value unchanged?

**Changed decision.** The static forest becomes a forest that is rebuilt on demand. An edge that cannot lower any path bottleneck never triggers a rebuild, and a burst of damaging edges pays for one rebuild.

#### [Recognize] Fixed Source Costs After Edge Decreases (LeetCode 2642)
<!-- id: dq39-source-decrease -->

**Prerequisites.** The Boundary exercise above and the incremental relaxation from the lesson Dynamic Graph Queries. This exercise keeps the theme of LeetCode 2642 but changes its contract: edges are only lowered and never added, a query asks for the cost from one fixed source, and `lower` reports whether any distance improved. All queries start at one source, and an update only lowers the cost of an existing edge.

**Problem.** Design a class `SourceCosts`. Its constructor receives `n`, a source vertex `source` and a list of directed edges `{from, to, cost}` with no parallel edges and no self-loops. The method `lower(a, b, newCost)` lowers the cost of the existing edge from `a` to `b` to `newCost` when `newCost` is smaller than its current cost, and returns `true` exactly when at least one shortest distance from the source gets smaller. The method `cost(target)` returns the minimum total cost of a directed path from the source to `target`, or `-1` when none exists. The workload has many decreases and many queries in unknown order. Choose between an all-pairs table, a fresh search per query and one maintained distance array, and justify the choice by the update and query counts.

**Constraints.** The limits are:
- **n** satisfies `1 <= n <= 10^3`, and the edge count is at most `10^4`.
- **Costs** are `int` values from 0 to 10^9, and path totals use `long`.
- **lower** throws `IllegalArgumentException` when the edge does not exist, and a larger or equal `newCost` changes nothing.
- **Calls** are one constructor call and up to `10^5` calls to `lower` and `cost` combined.

**Example 1.** Input `n = 4`, `source = 0`, edges `{0,1,6}`, `{1,2,5}`, `{2,3,2}`, `{0,2,20}`, then the calls `cost(3)`, `lower(0,2,9)`, `cost(3)`, `lower(1,2,5)`, `lower(0,2,30)`, `lower(0,1,1)`, `cost(3)`, `lower(2,3,0)`, `cost(3)`; output `[13, true, 11, false, false, true, 8, true, 6]`.

**Example 2.** Input `n = 4`, `source = 0`, edges `{1,2,5}`, `{2,3,2}`, then the calls `cost(1)`, `lower(1,2,1)`, `cost(3)`; output `[-1, false, -1]`, because node 1 is unreachable.

**Hint.** A decrease of the edge `(a, b)` can help a path only through `b`. When does the comparison of `dist[a] + newCost` with `dist[b]` already prove that nothing changes? When it does not, lower `dist[b]` and relax outward from `b` along its outgoing edges, visiting only the nodes whose distance improves.

**Changed decision.** The index is a single distance array that a decrease repairs locally and a query reads in constant time. No stale mark exists, because the repair cost depends on the nodes that actually improve.
