<!-- lesson-kind: combination -->
<!-- lesson-id: shortest-paths-with-a-heap -->
## Shortest Paths With A Heap

<!-- stage: context -->
### Why Repeated Scans Fail On Large Graphs

A monitoring team keeps four tools that all run on weighted links. The first tool reports how long an alert needs to reach every server. The second tool plans a hiking route whose steepest single step is as small as possible. The third tool finds the cheapest flight itinerary that uses at most a given number of stops. The fourth tool finds the network route whose packets are most likely to arrive.

The first version of every tool scans all links again and again until no number changes. On a test network of 500 servers it answers at once. On the production network of 200000 servers and 1 million links, a single answer takes minutes, and the flight tool also returns itineraries that exceed the stop limit.

The four tools look unrelated, because they add, take a maximum, count stops and multiply. This lesson asks whether one search loop can answer all four by changing only the rule that scores a route.

<!-- stage: contributions -->
### What Four Earlier Lessons Add

#### The Heap Loop And Its Entries

Four lessons of this chapter supply the parts. The Dijkstra lesson supplies the basic loop. The loop finalizes the vertex with the smallest known distance, and the outgoing edges of that vertex improve the distances of its neighbors. That loop is correct only for weights that are not negative, and it needs `long` sums when totals can pass the `int` range.

The stale heap entries lesson supplies the way to use `PriorityQueue`, which has no decrease-key. The loop inserts a new entry for every improvement and skips an entry on removal when its distance is worse than the stored one.

#### States And Layers

The node-state search lesson supplies the idea that the unit of search can be a pair of a vertex and extra information, with one stored distance per pair. The constrained flights lesson supplies the layers by number of flights used, which fit a stop limit.

#### The Rule That Joins Them

The combination adds one rule. The heap, the skip test and the stored best values work for any score that a route cannot improve by growing longer. The invariant is that the first current entry removed for a state carries that state's final score. The nearest false friend is the plain distance array of a single vertex, because it forgets the stop count.

<!-- stage: naive -->
### Scanning Every Link Until Nothing Changes

The direct plan starts with an infinite distance for every node and zero for the source. It then loops over the whole list of links. For each link it checks whether the start node plus the link weight beats the stored distance of the end node, and it stores the better value. It repeats the loop over all links until one full pass changes nothing.

```java
static long[] scanUntilStable(int n, int[][] links, int src) {
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int[] e : links) {                        // one full pass over every link
            if (dist[e[0]] != Long.MAX_VALUE && dist[e[0]] + e[2] < dist[e[1]]) {
                dist[e[1]] = dist[e[0]] + e[2];
                changed = true;
            }
        }
    }
    return dist;
}
```

The method is correct for nonnegative weights, because a pass that changes nothing proves that no link can improve any distance. The open question is how many passes it needs.

```predict
A chain has nodes 0 to 999, and the links are listed in reverse order: first 998 to 999, then 997 to 998, and so on down to 0 to 1. The source is node 0. How many full passes does scanUntilStable make?

It makes 1000 passes. In the first pass only the last listed link, from 0 to 1, finds a finite start distance, so only node 1 receives a value. Each later pass gives a value to exactly one more node. After 999 passes every distance is final, and one more pass confirms that nothing changes. That is about one million link reads for a chain with only 999 links.
```

<!-- stage: bottleneck -->
### Passes Multiply And Stops Are Ignored

The chain shows the cost. Each pass reads every link, and in the worst order each pass finalizes one node. With V nodes and E links the method performs V passes of E reads, so it takes O(V * E) time. For 200000 nodes and 1 million links that is 2 * 10^11 link reads, which is the minutes-long delay of the first tool. The cause is that the scan has no order. It tests links whose start node has no useful distance yet, and it improves the same node many times.

A second problem hides in the flight tool. The plain distance array keeps one number per city, so it keeps only the cheapest way to reach the city. A cheap way can use too many flights to continue, while a costlier way with fewer flights could still reach the destination. Storing only the cheaper number discards the route that the stop limit requires.

A better method chooses which node to process next, so that each node is final at that moment. It also lets the stored state carry more than the city. The next stage describes both changes.

<!-- stage: insight -->
### One Loop For Four Kinds Of Score

Every one of the four tools searches for the best route to a state, and a route has a score.

<!-- names: relaxation, stale entry, path score -->

#### The Path Score

The **path score** is the single value that the search compares between two routes to the same state. The score is a sum of weights for the delay tool and the largest single height step for the hiking tool. It is a product of probabilities for the network tool and a total price for the flight tool. A route is never improved by adding an edge, which means the score of an extended route is at least as bad as the score before the extension. Nonnegative weights give this property for sums. Absolute differences give it for the maximum. Probabilities between 0 and 1 give it for products.

#### Relaxation And The Heap

**Relaxation** means combining the score of a finalized state with one outgoing edge and storing the result when it beats the stored best score of the end state. Every successful relaxation pushes an entry with the new score into a `PriorityQueue`. The heap returns the entry with the best score among all entries, so the loop always works on the most promising candidate. An entry is a pair of a score and a state.

#### Stale Entries Replace Decrease-Key

`PriorityQueue` cannot lower the score of an entry that is already inside. The loop pushes a second entry instead. The old entry is removed later with a score worse than the stored best of its state. Such an entry is a **stale entry**. The loop skips it with one comparison. An entry that is not stale is a **current entry**. A stale entry costs one heap removal and nothing else, and the number of entries is at most the number of successful relaxations.

#### Why The First Current Entry Is Final

The invariant is that the removed entry has the best score among all entries in the heap. Any other route to the same state passes through an entry that is still in the heap, or through a state that is finalized already. Its score cannot beat the removed one, because extending never improves a score. So the first current entry removed for a state holds the final score, and the loop can stop at the destination. The state is a city for the delay tool. It is a pair of a city and a count of flights used for the flight tool, which keeps the cheap but long route apart from the costlier short one.

<!-- stage: variables -->
### What The Loop Keeps

The loop reads the graph and the source and never changes them. It builds an adjacency list so that each state lists its outgoing edges. Three values drive every variant of the loop.

- **best** is an array with one stored score per state, and it starts at the worst possible score except at the source.
- **heap** is a `PriorityQueue` of entries, each holding a score and a state, ordered so that the best score comes out first.
- **top** is the entry that the last removal returned, and the loop tests its score against `best` before reading any edge.

For the flight tool the state pairs a city with the number of flights used. Then `best` has one row for each city and one column for each count from 0 to k + 1.

<!-- stage: trace -->
### Heap Entries On Two Small Inputs

#### Delay With A Stale Entry

The first graph has four nodes numbered from 0. Its links are 0 to 1 of weight 4, 0 to 2 of weight 1, 2 to 1 of weight 2 and 1 to 3 of weight 1. The source is node 0. Each cell is a node, and the pointer `node` marks the node of the removed entry. The variable `dist` lists the stored distances of nodes 0 to 3, and `heap` lists the entries as pairs of distance and node. At step 3 node 2 improves node 1 from 4 to 3, so the heap holds two entries for node 1. At step 5 the older entry (4,1) comes out and the loop skips it, because `dist` of node 1 is 3.

```trace
{"cells":[0,1,2,3],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"dist":"0,inf,inf,inf","heap":"(0,0)"},"note":"Only the source has a distance. The heap starts with the entry (0,0)."},{"at":{"node":0},"vars":{"dist":"0,4,1,inf","heap":"(1,2) (4,1)"},"note":"Node 0 is final at distance 0, and its links are read."},{"at":{"node":2},"vars":{"dist":"0,3,1,inf","heap":"(3,1) (4,1)"},"note":"Node 2 is final at distance 1, and its links are read."},{"at":{"node":1},"vars":{"dist":"0,3,1,4","heap":"(4,1) (4,3)"},"note":"Node 1 is final at distance 3, and its links are read."},{"at":{"node":1},"vars":{"dist":"0,3,1,4","heap":"(4,3)"},"note":"Entry (4,1) comes out, yet dist[1] already holds 3. The entry is stale and the loop drops it."},{"at":{"node":3},"vars":{"dist":"0,3,1,4","heap":"empty"},"note":"Node 3 is final at distance 4, and its links are read."}]}
```

The final distances are 0, 3, 1 and 4. Notice that node 1 appeared twice inside the heap, yet the loop expanded it only once, with its smaller value.

#### Flights With A Stop Limit

The second input has four cities. Its flights are 0 to 1 of price 1, 1 to 2 of price 1, 0 to 2 of price 5 and 2 to 3 of price 1. The source is city 0, the destination is city 3, and at most one stop is allowed, so at most 2 flights. An entry reads cost, city and flights used. The cheap route through cities 1 and 2 reaches city 2 at cost 2 with 2 flights, and it cannot add a third flight. The costlier entry (5,2,1) is a separate state, so it survives, and it leads to the destination at cost 6. A plain distance array would have overwritten the 5 with the 2 and lost this route.

```trace
{"cells":[0,1,2,3],"pointers":["city"],"steps":[{"at":{"city":0},"vars":{"heap":"(0,0,0)"},"note":"The heap starts with (0,0,0), read as cost 0, city 0, no flight used yet."},{"at":{"city":0},"vars":{"heap":"(1,1,1) (5,2,1)"},"note":"Entry (0,0,0) is current. Each flight from city 0 adds an entry with flights used = 1 when it beats the stored price."},{"at":{"city":1},"vars":{"heap":"(2,2,2) (5,2,1)"},"note":"Entry (1,1,1) is current. Each flight from city 1 adds an entry with flights used = 2 when it beats the stored price."},{"at":{"city":2},"vars":{"heap":"(5,2,1)"},"note":"Entry (2,2,2) has spent all 2 allowed flights, so no flight leaves it."},{"at":{"city":2},"vars":{"heap":"(6,3,2)"},"note":"Entry (5,2,1) is current. Each flight from city 2 adds an entry with flights used = 2 when it beats the stored price."},{"at":{"city":3},"vars":{"heap":"empty"},"note":"City 3 is the destination. Its first current entry gives price 6 with 1 stop, and the search ends."}]}
```

Compare the two sequences. Both end when the heap yields what the question asks for, but they treat extra entries differently. In the weighted search, the stale entry costs one removal and no edge reads, while the limited search keeps parallel candidates alive because their remaining budgets differ.

<!-- stage: code -->
### Heap Search With A Skip Test

#### Sum Of Weights On A City

The first method is the delay loop. It stores each entry as a `long` array of distance and node, and it compares with `Long.compare`, because subtracting two longs can overflow.

```java
static long[] heapDistances(int n, int[][] links, int src) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : links) adj.get(e[0]).add(new int[] {e[1], e[2]});
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, src});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        int u = (int) top[1];
        if (top[0] > dist[u]) continue;                // stale entry: a better one was stored later
        for (int[] e : adj.get(u)) {
            long cand = top[0] + e[1];
            if (cand < dist[e[0]]) {                   // relaxation succeeds only when it improves
                dist[e[0]] = cand;
                heap.add(new long[] {cand, e[0]});
            }
        }
    }
    return dist;
}
```

#### Cost On A City And A Flight Count

The second method changes only the state. The array `best[city][used]` holds the cheapest price for reaching a city with exactly `used` flights, and a removed entry with `used == k + 1` pushes nothing. Prices are small, so `int` holds every sum.

```java
static int cheapestWithLimit(int n, int[][] flights, int src, int dst, int k) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] f : flights) adj.get(f[0]).add(new int[] {f[1], f[2]});
    int[][] best = new int[n][k + 2];
    for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
    best[src][0] = 0;
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    heap.add(new int[] {0, src, 0});
    while (!heap.isEmpty()) {
        int[] top = heap.poll();
        if (top[0] > best[top[1]][top[2]]) continue;   // stale entry for this state
        if (top[1] == dst) return top[0];              // first current removal of the destination is final
        if (top[2] == k + 1) continue;                 // no flight left to spend
        for (int[] e : adj.get(top[1])) {
            int cand = top[0] + e[1];
            if (cand < best[e[0]][top[2] + 1]) {
                best[e[0]][top[2] + 1] = cand;
                heap.add(new int[] {cand, e[0], top[2] + 1});
            }
        }
    }
    return -1;
}
```

The first method runs in O((V + E) log E) time. The heap holds at most one entry per successful relaxation, and each entry costs O(log E). The flight method multiplies the state count by k + 2. Hiking and probability change only the combining line and the heap order. A heap that returns the largest value first needs a comparator that reverses the comparison.

<!-- stage: applicability -->
### Recognizing Heap Shortest Path Problems

#### Reading The Cue

Use this loop when the statement asks for the best route between states, each step has a cost, and a longer route never scores better. Typical wordings are the least total time, the smallest largest step, the highest chance of success, and the lowest price under a limit on steps. When the limit or another condition changes what a state means, add that condition to the state.

#### Checking The Invariant

The invariant is that every removed current entry has the final score of its state. It holds when the combining rule never improves a route by extending it, and when the heap order matches the meaning of best. A negative weight breaks the first condition, and a heap order that does not match the comparison in the skip test breaks the second. Test a source equal to the destination, a node without links, and a zero weight, which must not create an endless loop.

#### Avoiding The False Friend

The false friend is the breadth-first search with a visited flag. It finalizes a node at its first visit, which is correct only when every edge has equal cost. A second false friend is a plain distance array for a problem whose answer depends on the number of flights, since the array discards the route that the limit needs. A third is a distance sum stored in `int`, which wraps around silently when the total passes about 2.1 billion.

<!-- stage: exercises -->
### Exercises

#### [Build] Network Delay With Unreached Count (LeetCode 743)
<!-- id: sp-delay-unreached-count -->

**Prerequisites.** The heap loop of this lesson.

**Problem.** A network has nodes numbered `1` to `n`. Each entry `[u, v, w]` of `times` is a directed link from `u` to `v` that a signal crosses in `w` time units. A signal starts at node `k` at time 0 and travels over every link at once. Let `d(x)` be the smallest total weight of a directed path from `k` to `x`, with `d(k) = 0`. A node is reached when at least one such path exists. Return an `int[]` of length 2: the largest `d(x)` over reached nodes, then the number of nodes that are not reached. This version never returns `-1` for an unreachable node.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100` and `1 <= k <= n`.
- **Links** satisfy `0 <= times.length <= 6000`, and parallel links and self loops may occur.
- **Weights** are integers with `0 <= w <= 100`.
- **Result** is `{delay, unreached}`, and `delay` is 0 when only the source is reached.

**Example 1.** Input `n = 5`, `times = [[1,2,2],[1,3,5],[3,2,1],[2,4,3],[4,5,2]]`, `k = 1`, output `[7,0]`.

**Example 2.** Input `n = 3`, `times = [[1,1,5],[1,2,0]]`, `k = 1`, output `[0,1]`.

**Hint.** Which nodes keep the infinite value after the loop ends, and should they enter the maximum?

**Changed decision.** The method reads the finished distance array for two values, the maximum over finite entries and the count of infinite entries, instead of returning one value or `-1`.

#### [Vary] Path With Minimum Effort (LeetCode 1631)
<!-- id: sp-min-effort-route -->

**Prerequisites.** The exercise above.

**Problem.** A grid `heights` has `rows` rows and `cols` columns. A move goes from a cell to a neighbor above, below, left or right. The effort of a route is the largest absolute height difference between two consecutive cells of the route. Return the smallest effort over all routes from the cell `(0, 0)` to the cell `(rows - 1, cols - 1)`.

**Constraints.** The limits are:
- **Grid** satisfies `1 <= rows, cols <= 100`.
- **Heights** are integers with `0 <= heights[r][c] <= 1000000`.
- **Single cell** grids are allowed, and their effort is 0.
- **Routes** may revisit cells, and the grid is not changed.

**Example 1.** Input `heights = [[3,3,9],[8,2,4],[7,1,6]]`, output `2`.

**Example 2.** Input `heights = [[5,1],[5,9]]`, output `4`.

**Hint.** When a route extends by one move, which of the two values, the old effort or the step difference, becomes the new effort?

**Changed decision.** The method combines a route score with a step by taking the maximum, not the sum, and the heap orders entries by that maximum.

#### [Boundary] Cheapest Flights With The Stop Count (LeetCode 787)
<!-- id: sp-flights-stop-count -->

**Prerequisites.** The two exercises above.

**Problem.** There are `n` cities numbered from `0`. Each entry `[a, b, p]` of `flights` is a one-way flight from `a` to `b` with price `p`. A route from `src` to `dst` is a sequence of flights in which each flight starts where the previous one ends. Its stops are the cities between the first and the last flight, so a route of `m` flights has `m - 1` stops. Among routes with at most `k` stops, return an `int[]` of length 2 that holds the least total price and the number of stops of the cheapest route. A tie in price goes to the route with fewer stops. Return `{-1, -1}` when no route exists. This version returns the stop count in addition to the price.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 60` and `src != dst`, with both in `0..n-1`.
- **Flights** satisfy `0 <= flights.length <= 300`, and parallel flights may occur.
- **Prices** are integers with `0 <= p <= 1000`.
- **Limit** satisfies `0 <= k <= n`.

**Example 1.** Input `n = 5`, `flights = [[0,1,20],[1,2,20],[2,4,20],[0,3,30],[3,4,90]]`, `src = 0`, `dst = 4`, `k = 1`, output `[120,1]`.

**Example 2.** Input `n = 3`, `flights = [[0,1,0],[1,2,0],[0,2,0]]`, `src = 0`, `dst = 2`, `k = 1`, output `[0,0]`.

**Hint.** If two routes reach a city with different flight counts, which one can a later flight still use when the limit is tight?

**Changed decision.** The method stores one best price for each pair of city and flights used. It reads the stop count from the flight count of the first removed destination entry. Among equal prices, the entry with fewer flights leaves the heap first, so a tie goes to fewer stops.

#### [Recognize] Path With Maximum Probability (LeetCode 1514)
<!-- id: sp-max-probability-path -->

**Prerequisites.** All three exercises above.

**Problem.** An undirected graph has nodes `0` to `n - 1`. Entry `i` of `edges` is a pair `[a, b]`, and `succProb[i]` is the probability that a message crosses that edge. The probability of a path is the product of the probabilities of its edges. Return the largest probability over all paths from `start` to `end` as a `double`, or `0.0` when no path exists.

**Constraints.** The limits are:
- **Nodes** satisfy `2 <= n <= 100` and `start != end`.
- **Edges** satisfy `0 <= edges.length <= 300`, and parallel edges may occur.
- **Probabilities** are doubles with `0.0 <= succProb[i] <= 1.0`.
- **Result** is accepted within an absolute error of `1e-9`.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,3],[0,2],[2,3]]`, `succProb = [0.5,0.5,0.75,0.5]`, `start = 0`, `end = 3`, output `0.375`.

**Example 2.** Input `n = 4`, `edges = [[0,1],[2,3]]`, `succProb = [0.5,0.5]`, `start = 0`, `end = 3`, output `0.0`.

**Hint.** Which comparison must the heap use so that the largest probability comes out first, and why does a product never grow along a path?

**Changed decision.** The method multiplies scores, keeps the larger stored value, and orders the heap with the largest probability first.
