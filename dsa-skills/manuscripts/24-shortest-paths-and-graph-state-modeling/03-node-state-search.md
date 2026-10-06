<!-- lesson-kind: standard -->
<!-- lesson-id: node-state-search -->
## Search Over Place And State

<!-- stage: context -->
### A Fare Search With One Coupon

#### A Wrong Answer Without A Crash

A fare planner stores airports and flights. Each flight has an integer price, and each traveler owns one coupon that halves the price of a single flight, rounded down. The traveler wants the lowest total price from a start airport to a destination. The planner runs the nearest-first search from the earlier lessons of this chapter, which keeps one `long` distance per airport and a heap of candidate routes. On a small test network it reports 106. A person who adds the prices by hand finds a route that costs 60. The planner is not slow and it does not crash. It returns a wrong number with full confidence.

#### What A Route Costs

The graph is directed, and every weight is nonnegative. A route is a sequence of edges. Its cost is the sum of the edge costs, with the coupon applied to at most one edge. The coupon changes what a route costs, but it also changes what a route may do next, because a spent coupon cannot be spent again. So two routes that end at the same airport are not always interchangeable.

This lesson asks what a search must remember about a route besides its last airport. The answer must keep every route that still has a cheaper future.

<!-- stage: naive -->
### Keeping One Distance For Each Airport

The first attempt adds a flag to each heap entry that tells whether the coupon is spent. It still stores a single best cost for every airport. The code drops an entry when its cost is not below that stored cost.

```java
static long oneDistance(int n, int[][] edges, int src, int dst) {
    List<List<int[]>> out = new ArrayList<>();
    for (int v = 0; v < n; v++) out.add(new ArrayList<>());
    for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, src, 0});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        int u = (int) top[1];
        int spent = (int) top[2];
        if (top[0] > dist[u]) continue;
        for (int[] e : out.get(u)) {
            long full = top[0] + e[1];
            if (full < dist[e[0]]) { dist[e[0]] = full; heap.add(new long[] {full, e[0], spent}); }
            long half = top[0] + e[1] / 2;
            if (spent == 0 && half < dist[e[0]]) { dist[e[0]] = half; heap.add(new long[] {half, e[0], 1}); }
        }
    }
    return dist[dst] == Long.MAX_VALUE ? -1 : dist[dst];
}
```

The code looks like a correct nearest-first search with one extra check. The flag travels with each entry, and the coupon is spent at most once on any route that the code builds.

```predict
Take four flights: 0 to 1 costs 8, 1 to 2 costs 2, 2 to 3 costs 100, and 0 to 2 costs 30. What does oneDistance return from airport 0 to airport 3, and what is the true lowest price?

It returns 106, and the true lowest price is 60. The code first reaches airport 1 by spending the coupon on the first flight, which costs 4. The later route with price 8 and an unused coupon is not below 4, so the code drops it. The price 60 comes from paying 8 and 2 in full and spending the coupon on the flight that costs 100, which halves it to 50. That route needs the dropped entry.
```

<!-- stage: bottleneck -->
### One Number Hides Two Different Futures

#### What The Single Number Hides

The method visits each airport a bounded number of times and reads each flight a bounded number of times, so its cost is O((V + E) log E). The cost is acceptable. The defect is in what the single number `dist[v]` stands for. At airport 1 the search holds two routes, and each is better in one respect. The route with price 4 is cheaper by 4, and it has no coupon left. The route with price 8 is more expensive, and it still holds a coupon that can save 50 on the last flight.

A route comparison is meaningful only when both routes have the same remaining options. Costs alone answer the question "which route is cheaper so far". They do not answer the question "which route finishes cheaper". When the cheaper arrival has fewer options, a later flight can reverse the order, and a search that kept only the cheaper arrival has already lost the answer.

#### Where Else The Failure Appears

The same failure appears whenever the next move depends on more than the position. The extra fact can be the number of stops used so far, the keys that a player carries, or the color of the last edge. A fix must keep one figure for each combination of airport and extra fact. Its cost must stay near O((V + E) log E) times the number of extra facts. The next stage describes that fix.

<!-- stage: insight -->
### Treating The Pair As The Position

The repair changes what counts as one position of the search. The pair of airport and extra fact becomes the position, and the search runs as before over those positions.

<!-- names: state index, dominates, settled -->

#### The Extra Fact Becomes Part Of The Position

Write `S` for the number of values the extra fact can take. For the coupon, `S` is 2: the coupon is unspent or spent. A position is a pair `(v, s)` with `0 <= s < S`. The search keeps `dist` for every pair, so `dist` has `V * S` entries. An outgoing flight from `(v, s)` leads to a pair at the destination of the flight. The new extra fact follows from the old one and from the choice made on the flight. Paying the full price keeps `s`. Spending the coupon moves from `s = 0` to `s = 1`.

#### One Number For Each Pair

Arrays index by one integer, so the pair is packed into a **state index** `v * S + s`. Division by `S` returns `v`, and the remainder returns `s`. Nothing else changes in the nearest-first search. A heap entry holds the cost and the state index. The search detects a stale entry by comparing its cost with `dist[stateIndex]`. It relaxes each edge once for every value of `s` that the position allows.

#### When One Arrival Beats Another

An arrival `a` **dominates** an arrival `b` at the same airport when `a` costs no more and offers every option that `b` offers. At airport 1 the arrival with price 4 and a spent coupon does not dominate the arrival with price 8 and an unspent coupon. The second arrival keeps an option that the first lacks. Two arrivals with equal flags are different, since the cheaper one dominates. Pruning by dominance is safe, but pruning by cost alone is not. The search needs no explicit dominance test, because one `dist` slot per pair discards exactly the arrivals that share a flag and cost more.

#### Why The Heap Order Still Holds

A position is **settled** when its smallest entry leaves the heap. At that moment no cheaper route to that pair exists, because every edge cost is nonnegative and every unsettled entry costs at least as much. The invariant is that the settled cost of a pair equals the cost of the cheapest route that ends at that airport with that extra fact. The answer at the destination is the minimum over the pairs there.

<!-- stage: variables -->
### What The Search Keeps

The search reads `n`, `edges`, `src` and `dst` and changes none of them. It builds `out`, a list of `{target, price}` pairs for each airport, in the order of `edges`. Three structures hold the search state.

- **dist** is a `long[]` of length `2 * n`; the slot `2 * v + s` holds the lowest known cost of reaching airport `v` with coupon flag `s`.
- **heap** is a `PriorityQueue<long[]>` of `{cost, stateIndex}` entries ordered by cost.
- **cost** and **stateIndex** are the two numbers of the entry that was removed last.

The flag `s` equals 0 while the coupon is unspent. The unreached marker is `Long.MAX_VALUE`, and the search never adds a price to it, because only reached positions enter the heap.

<!-- stage: trace -->
### Following Entries Through Two Searches

#### The Fare Network With One Coupon

The network has four airports and the flights 0 to 1 at 8, 1 to 2 at 2, 2 to 3 at 100 and 0 to 2 at 30. The pointer `cur` marks the airport of the removed entry. The variable `dist` lists each airport as `unspent/spent`, where a dash means unreached, and `pop` names the removed entry. Three moments matter. At step 2 the search removes the cheap entry of airport 1 with the coupon spent. It makes airport 2 reachable at 6 with a spent coupon, and step 3 then sends the price 106 to airport 3. At step 4 the entry of airport 1 with price 8 and an unspent coupon is still in the heap, because it has its own slot. It lowers the unspent slot of airport 2 from 30 to 10. At step 5 that entry reaches airport 3 with price 60, which is the answer.

```trace
{"cells":[0,1,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"pop":"node 0, coupon unused, cost 0","dist":"0:0/- 1:8/4 2:30/15 3:-/-"},"note":"The search removes the entry of node 0 with the coupon unused at cost 0 and relaxes its edges."},{"at":{"cur":1},"vars":{"pop":"node 1, coupon used, cost 4","dist":"0:0/- 1:8/4 2:30/6 3:-/-"},"note":"The search removes the entry of node 1 with the coupon used at cost 4 and relaxes its edges."},{"at":{"cur":2},"vars":{"pop":"node 2, coupon used, cost 6","dist":"0:0/- 1:8/4 2:30/6 3:-/106"},"note":"The search removes the entry of node 2 with the coupon used at cost 6 and relaxes its edges."},{"at":{"cur":1},"vars":{"pop":"node 1, coupon unused, cost 8","dist":"0:0/- 1:8/4 2:10/6 3:-/106"},"note":"The search removes the entry of node 1 with the coupon unused at cost 8 and relaxes its edges."},{"at":{"cur":2},"vars":{"pop":"node 2, coupon unused, cost 10","dist":"0:0/- 1:8/4 2:10/6 3:110/60"},"note":"The search removes the entry of node 2 with the coupon unused at cost 10 and relaxes its edges."},{"at":{"cur":3},"vars":{"pop":"node 3, coupon used, cost 60","dist":"0:0/- 1:8/4 2:10/6 3:110/60"},"note":"The search removes the entry of node 3 with the coupon used at cost 60 and relaxes its edges."},{"at":{"cur":3},"vars":{"pop":"node 3, coupon unused, cost 110","dist":"0:0/- 1:8/4 2:10/6 3:110/60"},"note":"The search removes the entry of node 3 with the coupon unused at cost 110 and relaxes its edges."}]}
```

#### Alternating Colors With Three Last Colors

The second search is a breadth-first search, because every edge has length one. The network has the red edges 0 to 1, 0 to 2 and 2 to 3, and the blue edges 1 to 2 and 1 to 0. A walk must alternate colors. The extra fact is the color of the last edge, which takes the values red, blue and start. The variable `dist` lists each airport as `red/blue/start`. Airport 2 is reached at distance 1 by a red edge, and that arrival cannot take the red edge to airport 3. Airport 2 is reached again at distance 2 through a blue edge, and only that arrival continues to airport 3 at distance 3. The two arrivals share an airport and carry different futures.

```trace
{"cells":[0,1,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"pop":"node 0, last start, distance 0","dist":"0:-/-/0 1:1/-/- 2:1/-/- 3:-/-/-"},"note":"The search removes the position of node 0 with last color start and adds (1,red), (2,red)."},{"at":{"cur":1},"vars":{"pop":"node 1, last red, distance 1","dist":"0:-/2/0 1:1/-/- 2:1/2/- 3:-/-/-"},"note":"The search removes the position of node 1 with last color red and adds (2,blue), (0,blue)."},{"at":{"cur":2},"vars":{"pop":"node 2, last red, distance 1","dist":"0:-/2/0 1:1/-/- 2:1/2/- 3:-/-/-"},"note":"The search removes the position of node 2 with last color red and adds no new position."},{"at":{"cur":2},"vars":{"pop":"node 2, last blue, distance 2","dist":"0:-/2/0 1:1/-/- 2:1/2/- 3:3/-/-"},"note":"The search removes the position of node 2 with last color blue and adds (3,red)."},{"at":{"cur":0},"vars":{"pop":"node 0, last blue, distance 2","dist":"0:-/2/0 1:1/-/- 2:1/2/- 3:3/-/-"},"note":"The search removes the position of node 0 with last color blue and adds no new position."},{"at":{"cur":3},"vars":{"pop":"node 3, last red, distance 3","dist":"0:-/2/0 1:1/-/- 2:1/2/- 3:3/-/-"},"note":"The search removes the position of node 3 with last color red and adds no new position."}]}
```

<!-- stage: code -->
### Search Code For Both Variants

The first method is the nearest-first search with the state index. The second method is the breadth-first search for the colored edges. Both use the same packing of a pair into one integer.

```java
static long cheapestWithCoupon(int n, int[][] flights, int src, int dst) {
    List<List<int[]>> out = new ArrayList<>();
    for (int v = 0; v < n; v++) out.add(new ArrayList<>());
    for (int[] f : flights) out.get(f[0]).add(new int[] {f[1], f[2]});
    long[] dist = new long[2 * n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[2 * src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
    heap.add(new long[] {0, 2 * src});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        int idx = (int) top[1];
        if (top[0] > dist[idx]) continue;
        int u = idx / 2;
        int spent = idx % 2;
        for (int[] f : out.get(u)) {
            long pay = top[0] + f[1];
            int keep = 2 * f[0] + spent;
            if (pay < dist[keep]) { dist[keep] = pay; heap.add(new long[] {pay, keep}); }
            if (spent == 0) {
                long cut = top[0] + f[1] / 2;
                int moved = 2 * f[0] + 1;
                if (cut < dist[moved]) { dist[moved] = cut; heap.add(new long[] {cut, moved}); }
            }
        }
    }
    long best = Math.min(dist[2 * dst], dist[2 * dst + 1]);
    return best == Long.MAX_VALUE ? -1 : best;
}

static int[] alternatingLengths(int n, int[][] red, int[][] blue) {
    List<List<Integer>> redOut = new ArrayList<>();
    List<List<Integer>> blueOut = new ArrayList<>();
    for (int v = 0; v < n; v++) { redOut.add(new ArrayList<>()); blueOut.add(new ArrayList<>()); }
    for (int[] e : red) redOut.get(e[0]).add(e[1]);
    for (int[] e : blue) blueOut.get(e[0]).add(e[1]);
    int[][] dist = new int[n][3];
    for (int[] row : dist) Arrays.fill(row, -1);
    dist[0][2] = 0;
    ArrayDeque<int[]> queue = new ArrayDeque<>();
    queue.add(new int[] {0, 2});
    while (!queue.isEmpty()) {
        int[] cur = queue.poll();
        for (int color = 0; color < 2; color++) {
            if (cur[1] == color) continue;
            List<Integer> next = color == 0 ? redOut.get(cur[0]) : blueOut.get(cur[0]);
            for (int v : next) {
                if (dist[v][color] != -1) continue;
                dist[v][color] = dist[cur[0]][cur[1]] + 1;
                queue.add(new int[] {v, color});
            }
        }
    }
    int[] ans = new int[n];
    for (int v = 0; v < n; v++) {
        ans[v] = -1;
        for (int d : dist[v]) if (d != -1 && (ans[v] == -1 || d < ans[v])) ans[v] = d;
    }
    return ans;
}
```

The first method relaxes each flight at most twice per airport, so it runs in O((V + E) log E) time and uses O(V + E) memory. The second method visits each of the `3V` positions once, so it runs in O(V + E) time. A weight sum can pass the `int` range, which is why every cost is a `long`. The start position needs its own third color slot. If the code treated the start as red, the walk could not begin with a red edge.

<!-- stage: applicability -->
### Recognizing Problems With Extra State

#### Reading The Cue

Look for a statement in which the legal next move or the next cost depends on a fact other than the current node. Typical facts are the number of edges used so far and a coupon or key that is held or spent. The color or direction of the last move is another common fact. A route planner with a toll pass has this form. So does a puzzle where a player may carry one key. So does a network where traffic must alternate between two link types. Count the values the extra fact can take. That count `S` multiplies the number of positions and the cost.

#### Checking The Invariant

The invariant is that every stored distance belongs to one complete pair, and every transition computes the new pair from the old pair and the chosen edge. It breaks when the code updates a pair from a different extra fact than the one that the transition produces. Test a position that can reach the same airport with two different facts, and test a start position that has no last color. When the extra fact only counts something that never limits a move, the pair is wasted work and the plain search is enough.

#### Avoiding The False Friend

The false friend is the array with one distance for each node. It is correct for plain shortest paths, where any two arrivals at a node have the same future. It is wrong as soon as two arrivals differ in what they may do next. A second false friend is a pair that is too coarse, for example a flag for "any coupon used" when the problem allows two coupons. Pick the smallest extra fact that determines the legal moves and costs. A third hazard is a large `S`. With 1000 nodes and 100 states the search holds 100000 positions, and the memory must fit.

<!-- stage: exercises -->
### Exercises

#### [Build] Node And Coupon Flag (Author exercise)
<!-- id: sp-coupon-flag -->

**Prerequisites.** The state index and the nearest-first search of this lesson.

**Problem.** A directed graph has the nodes `0` to `n - 1`. Each entry `[u, v, w]` of `edges` is an edge from `u` to `v` with price `w`. A route from `src` to `dst` pays the full price of every edge, except that it may pay `w / 2` (integer division) for at most one edge. Return the lowest total price of such a route, or `-1` when `dst` cannot be reached from `src`.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Prices** satisfy `0 <= w <= 1000000000`, and the result needs a `long`.
- **Endpoints** `src` and `dst` lie in `0..n-1` and may be equal, which gives 0.

**Example 1.** Input `n = 4`, `edges = [[0,1,8],[1,2,2],[2,3,100],[0,2,30]]`, `src = 0`, `dst = 3`, output `60`.

**Example 2.** Input `n = 3`, `edges = [[0,1,5]]`, `src = 0`, `dst = 2`, output `-1`.

**Hint.** After a route reaches a node, which two facts about it decide its future, and why can the cheaper route lose?

**Changed decision.** The method stores one distance for each pair of node and coupon flag, and it spends the coupon only from a position whose flag is 0.

#### [Vary] Distance By State (Author exercise)
<!-- id: sp-distance-by-state -->

**Prerequisites.** The exercise above.

**Problem.** The graph and the edge prices are as in the previous exercise, but the traveler owns `k` coupons. Each coupon halves the price of one edge (integer division), and a route may spend a coupon on an edge only while it has one left. Return a `long[][]` named `table` with `n` rows and `k + 1` columns. The entry `table[v][j]` is the lowest price of a route from `src` to `v` that spends exactly `j` coupons, or `-1` when no such route exists. The empty route gives `table[src][0] = 0`.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 500`.
- **Edges** satisfy `0 <= edges.length <= 2000`, and repeats and self loops may occur.
- **Prices** satisfy `0 <= w <= 1000000000`.
- **Coupons** satisfy `0 <= k <= 3`, and a coupon spent on a price of 0 or 1 still counts.

**Example 1.** Input `n = 3`, `k = 1`, `edges = [[0,1,6],[1,2,4]]`, `src = 0`, output `[[0,-1],[6,3],[10,7]]`.

**Example 2.** Input `n = 4`, `k = 2`, `edges = [[0,1,5],[1,0,3],[1,2,9]]`, `src = 0`, output `[[0,5,3],[5,2,7],[14,9,6],[-1,-1,-1]]`.

**Hint.** How many values does the extra fact take now, and in which direction can its value change along a route?

**Changed decision.** The flag grows into a coupon count with `k + 1` values, and the method keeps the columns apart because the output asks for exactly `j` coupons.

#### [Boundary] Same Node, Different Future (Author exercise)
<!-- id: sp-same-node-future -->

**Prerequisites.** The two exercises above.

**Problem.** The graph and the one coupon are as in the first exercise. Return a `long[]` of length 2 that holds two answers for the pair `src`, `dst`. The first entry is the lowest price of a route, as in the first exercise. The second entry comes from a pruned search that keeps one state for each node. The pruned search removes triples `(cost, node, spent)` in ascending order of cost, then node, then spent. It skips a triple whose node was removed before. For each edge it pushes the full-price triple. When `spent` is 0, it also pushes the halved triple with `spent` set to 1. The second entry is the cost of the first triple removed at `dst`, or `-1` when none is.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 2000`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Prices** satisfy `0 <= w <= 1000000000`.
- **Result** is `{exact, pruned}`, and `pruned >= exact` whenever both exist.

**Example 1.** Input `n = 4`, `edges = [[0,1,8],[1,2,2],[2,3,100],[0,2,30]]`, `src = 0`, `dst = 3`, output `[60,106]`.

**Example 2.** Input `n = 3`, `edges = [[0,1,7],[1,2,9],[0,2,20]]`, `src = 0`, `dst = 2`, output `[10,10]`.

**Hint.** Which arrival at the middle node does the pruned search discard, and which later edge needed it?

**Changed decision.** The method runs the exact search with the flag inside the position next to a search that closes each node once, and it reports both results.

#### [Recognize] Shortest Path With Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors -->

**Prerequisites.** All three exercises above.

**Problem.** Consider `n` nodes numbered from `0`. The list `red` holds the red edges `[a, b]` from `a` to `b`, and the list `blue` holds the blue edges in the same form. A walk alternates colors when no two consecutive edges of the walk have the same color. Return an `int[]` named `answer` of length `n`, where `answer[x]` is the fewest edges in an alternating walk from node `0` to node `x`, or `-1` when none exists. The empty walk gives `answer[0] = 0`.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 100`.
- **Red and blue lists** each have length in `0..400`, and repeats and self loops may occur.
- **Start** has no previous color, so the walk may begin with either color.
- **Result** has length `n`, and `answer[0]` is always 0.

**Example 1.** Input `n = 3`, `red = [[0,1],[1,2]]`, `blue = []`, output `[0,1,-1]`.

**Example 2.** Input `n = 5`, `red = [[0,1],[2,3],[3,4]]`, `blue = [[1,2],[1,3],[0,0],[4,4]]`, output `[0,1,2,2,3]`.

**Hint.** If a node is reached first by a red edge, which edges can its walk take next, and what happens to a later blue arrival at the same node?

**Changed decision.** The method adds the color of the last edge to the breadth-first position, with a third value for the start that allows both colors.
