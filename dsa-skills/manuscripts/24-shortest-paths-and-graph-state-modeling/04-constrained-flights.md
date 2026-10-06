<!-- lesson-kind: standard -->
<!-- lesson-id: constrained-flights -->
## Limit A Route By Stops

<!-- stage: context -->
### Searching Tickets With A Connection Limit

A booking system lists the cheapest itinerary between two cities, and a traveler sets a limit of one connection. Each flight is a directed edge with a price, and the cities are numbered 0 to 3. The flights are 0 to 1 for 10, 1 to 2 for 10, 2 to 3 for 10 and 0 to 2 for 50. The cheapest trip from city 0 to city 3 costs 30 and uses three flights, so it has two connections. A search that returns it breaks the limit. The right answer for one connection is 60.

A **stop** is an intermediate city of a route, so a route with `k` stops uses at most `k + 1` flights. The task is to find the cheapest route from `src` to `dst` that uses at most `k` stops, or to report that none exists. Earlier lessons of this chapter stored one heap distance for each city, and later for each pair of city and state.

This lesson asks what a search must remember about an arrival at a city. A cheap arrival with no flights left must not hide a pricier arrival that can still continue.

<!-- stage: naive -->
### Pruning By The Cheapest Cost Per City

The first attempt reuses the heap search with one `dist` entry for each city. Each heap entry holds the cost, the city and the number of flights used so far. The search skips an entry whose cost exceeds `dist[city]`, and it stops expanding an entry that has used `k + 1` flights.

```java
static long cheapestNaive(int n, int[][] flights, int src, int dst, int k) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] f : flights) adj.get(f[0]).add(new int[] {f[1], f[2]});
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, src, 0});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        long cost = top[0];
        int city = (int) top[1];
        int used = (int) top[2];
        if (cost > dist[city]) continue;
        if (city == dst) return cost;
        if (used == k + 1) continue;
        for (int[] f : adj.get(city)) {
            if (cost + f[1] < dist[f[0]]) {
                dist[f[0]] = cost + f[1];
                heap.add(new long[] {cost + f[1], f[0], used + 1});
            }
        }
    }
    return -1;
}
```

On a graph without a limit, this method is correct. The question is what the count of flights does to it.

```predict
Run cheapestNaive on the four cities and four flights above with src = 0, dst = 3 and k = 1. What does it return, and what is the right answer?

It returns -1, but the right answer is 60. The search reaches city 1 for 10 and city 2 for 50 with one flight each. Then it reaches city 2 again for 20 with two flights and overwrites dist[2]. The entry for 20 has used both allowed flights and cannot continue. The entry for 50 could continue to city 3 with its second flight, but its cost exceeds dist[2], so the search skips it. No entry reaches city 3.
```

<!-- stage: bottleneck -->
### One Number Per City Loses Cheaper Options

The method runs in O(E log E) time, so the cost of the search is not the problem. The problem is the information that `dist[city]` keeps. It answers how little a city costs to reach, and it ignores how many flights that cheapest arrival has already spent.

Two arrivals at the same city compare in two ways. The arrival for 20 is cheaper, and the arrival for 50 has one flight left. Neither is better in both ways, so discarding either one can change the answer. Plain shortest paths never face this, because every continuation from a city costs the same for all arrivals, and the cheaper arrival always wins. A limit on flights breaks that argument, because the number of flights used changes which continuations remain legal.

Raising `k` shows the failure growing. Each extra allowed flight creates more pairs of arrivals that cost and length rank in opposite order. A correct method must keep a separate best cost for each number of flights used, and it must find a rule that keeps the work near O(k · E). The fix should cost about k + 1 passes over the edges.

<!-- stage: insight -->
### One Best Cost For Each Flight Count

Two facts describe an arrival, the city and the number of flights used. So the search state is a pair and not a single city.

<!-- names: layer, dominance, snapshot -->

#### Comparing Arrivals With Two Numbers

One arrival at a city beats another by **dominance** when it costs no more and uses no more flights. The search can safely discard a dominated arrival. Every continuation of the dominated arrival is also open to the dominating one, at the same price or lower. An arrival that is cheaper but longer does not dominate a pricier but shorter one. The naive method discarded arrivals without this test, which is why it lost the answer.

#### One Row For Each Flight Count

A **layer** is an array `best` of length `n`, where `best[v]` is the lowest cost to reach city `v` with at most `j` flights. Layer 0 holds 0 for `src` and infinity elsewhere. Layer `j + 1` follows from layer `j`. A route with at most `j + 1` flights either has at most `j` flights, or it ends with one more flight from a city that layer `j` reaches. So each flight offers `best[from] + price` to `to`, and each city also keeps its own value from layer `j`. After `k + 1` layers, the entry for `dst` is the answer.

#### Why A Copy Of The Row Is Needed

The pass builds the new layer from a **snapshot** of the old layer. A snapshot is a copy that the pass never modifies. Without it, one pass can chain flights. A flight from 0 to 1 updates city 1, and a later flight from 1 to 2 in the same pass reads the new value and extends it. That pass then buys two flights while it counts one, and the limit stops working. Reading only the snapshot guarantees that each pass adds exactly one flight to every route.

#### Turning Stops Into Flights

Stops and flights differ by one. A route with `k` stops has `k + 1` flights, so the loop runs `k + 1` passes. For `k = 0` the loop runs once and the answer is a direct flight. The invariant is that after pass `j`, the array holds the true minimum over all routes with at most `j` flights.

<!-- stage: variables -->
### What The Passes Keep

The method reads `n`, `flights`, `src`, `dst` and `k`, and it changes none of them. Each flight is a triple `{from, to, price}`.

- **best** is a `long[]` of length `n`, the layer after the last finished pass.
- **next** is a `long[]` copy of `best`, which receives the offers of the running pass.
- **INF** is `Long.MAX_VALUE / 4`, a value that survives the addition of a price.
- **pass** numbers the running pass and runs from 1 to `k + 1`, which gives `k + 1` passes in total.

The array `best` is read-only during a pass, and `next` is write-only apart from its comparison.

<!-- stage: trace -->
### Passes Over The Flight List

#### Two Passes With A Snapshot

The graph has four cities and the flights 0 to 1 for 10, 1 to 2 for 10, 2 to 3 for 10 and 0 to 2 for 50. The limit is `k = 1`, so two passes run. The cells are the four flights in list order, and the pointer `f` marks the flight under examination. The variable `pass` is the running pass and `frozen` is the snapshot cost at the start city. The variable `offer` is the price that the flight proposes, and `stored` is the cost of the end city in `next` after the step. Two steps carry the lesson. In pass 1 the flight 1 to 2 finds no price in the snapshot, so city 2 is not extended from city 1 yet. In pass 2 the flight 2 to 3 reads 50 from the snapshot, and the destination gets 60.

```trace
{"cells":["0>1 for 10","1>2 for 10","2>3 for 10","0>2 for 50"],"pointers":["f"],"steps":[{"at":{"f":0},"vars":{"pass":1,"frozen":0,"offer":10,"stored":10},"note":"The flight from 0 to 1 reads 0 at city 0 and offers 10, which lowers city 1 to 10."},{"at":{"f":1},"vars":{"pass":1,"frozen":"none","offer":"none","stored":"none"},"note":"The flight from 1 to 2 finds no price at city 1, so it offers nothing."},{"at":{"f":2},"vars":{"pass":1,"frozen":"none","offer":"none","stored":"none"},"note":"The flight from 2 to 3 finds no price at city 2, so it offers nothing."},{"at":{"f":3},"vars":{"pass":1,"frozen":0,"offer":50,"stored":50},"note":"The flight from 0 to 2 reads 0 at city 0 and offers 50, which lowers city 2 to 50."},{"at":{"f":0},"vars":{"pass":2,"frozen":0,"offer":10,"stored":10},"note":"The flight from 0 to 1 reads 0 at city 0 and offers 10, but city 1 already holds 10."},{"at":{"f":1},"vars":{"pass":2,"frozen":10,"offer":20,"stored":20},"note":"The flight from 1 to 2 reads 10 at city 1 and offers 20, which lowers city 2 to 20."},{"at":{"f":2},"vars":{"pass":2,"frozen":50,"offer":60,"stored":60},"note":"The flight from 2 to 3 reads 50 at city 2 and offers 60, which lowers city 3 to 60."},{"at":{"f":3},"vars":{"pass":2,"frozen":0,"offer":50,"stored":20},"note":"The flight from 0 to 2 reads 0 at city 0 and offers 50, but city 2 already holds 20."}]}
```

#### One Pass Without A Snapshot

The second run uses the same flights, but it updates the array in place and allows only one flight, which means `k = 0`. The cells and the pointer keep their meaning, and the variable `read` replaces `frozen` and holds the value that the flight reads from the live array. The correct answer for city 3 is "none", because no single flight leaves city 0 for city 3. The in-place pass reads the value that the first flight has just written, and chains the next flights. City 3 ends with 30, a cost that needs three flights.

```trace
{"cells":["0>1 for 10","1>2 for 10","2>3 for 10","0>2 for 50"],"pointers":["f"],"steps":[{"at":{"f":0},"vars":{"pass":1,"read":0,"offer":10,"stored":10},"note":"The flight from 0 to 1 reads 0 at city 0 and offers 10, which lowers city 1 to 10."},{"at":{"f":1},"vars":{"pass":1,"read":10,"offer":20,"stored":20},"note":"The flight from 1 to 2 reads 10 at city 1 and offers 20, which lowers city 2 to 20."},{"at":{"f":2},"vars":{"pass":1,"read":20,"offer":30,"stored":30},"note":"The flight from 2 to 3 reads 20 at city 2 and offers 30, which lowers city 3 to 30."},{"at":{"f":3},"vars":{"pass":1,"read":0,"offer":50,"stored":20},"note":"The flight from 0 to 2 reads 0 at city 0 and offers 50, but city 2 already holds 20."}]}
```

<!-- stage: code -->
### Bounded Passes Over All Flights

The method keeps the layer in `best` and builds each new layer in `next`. It returns -1 when `dst` stays at infinity.

```java
static long cheapestWithin(int n, int[][] flights, int src, int dst, int k) {
    final long INF = Long.MAX_VALUE / 4;
    long[] best = new long[n];
    Arrays.fill(best, INF);
    best[src] = 0;
    for (int pass = 1; pass <= k + 1; pass++) {
        long[] next = best.clone();
        for (int[] f : flights) {
            if (best[f[0]] < INF && best[f[0]] + f[2] < next[f[1]]) {
                next[f[1]] = best[f[0]] + f[2];
            }
        }
        best = next;
    }
    return best[dst] >= INF ? -1 : best[dst];
}
```

The call `clone()` copies the array, so writes to `next` never reach `best`. The guard `best[f[0]] < INF` skips cities that no route reaches. With `INF` at a quarter of the `long` range, even the unguarded sum could not overflow, while `int` arithmetic with `Integer.MAX_VALUE` would wrap to a negative number. The method takes O((k + 1) · E) time and O(V) memory.

<!-- stage: applicability -->
### Recognizing Limits On Edges Used

#### Reading The Cue

Look for a shortest or cheapest route problem where the statement also bounds the number of edges, stops, transfers or hops. Ticket search, network routing with a hop limit and payment paths with a maximum number of intermediaries have this form. When the bound is small compared with the graph, the layers fit well. Count the layers by translating the statement into a number of edges before writing a loop.

#### Checking The Invariant

The invariant is that layer `j` holds the minimum over routes with at most `j` edges. It breaks when a pass reads values that the same pass has written. Test a graph where a chain of cheap flights tempts the code to extend within one pass. Also test `k = 0` and a source with no outgoing flight. The unreachable destination must return the sentinel, never a sum built on infinity.

#### Avoiding The False Friend

The false friend is plain Dijkstra with one distance for each city. It is correct when only cost matters, and it fails when a cheaper arrival has fewer edges left. A second false friend is a depth-first search that prunes on the best cost seen at a city, which loses the same arrivals. An explicit heap on pairs of city and flights used also works. It must discard an arrival only when an earlier arrival at that city costs no more and used no more flights.

<!-- stage: exercises -->
### Exercises

#### [Build] At Most Two Edges (Author exercise)
<!-- id: sp-at-most-two-edges -->

**Prerequisites.** The layers of this lesson.

**Problem.** A directed graph has the cities `0` to `n - 1`, and each entry `[a, b, w]` of `flights` is a flight from `a` to `b` with price `w`. A route is a walk that starts at city 0, and its cost is the sum of its prices. Return a `long[]` of length `n`. Entry `v` is the lowest cost of a route from city 0 to `v` with at most two flights, or `-1` when no such route exists.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 100`.
- **Flights** satisfy `0 <= flights.length <= 400`, and repeated pairs may occur.
- **Prices** satisfy `1 <= w <= 1000`.
- **Result** holds `0` for city 0, and a route uses no more than two flights.

**Example 1.** Input `n = 4`, `flights = [[0,1,10],[1,2,10],[2,3,10],[0,2,50]]`, output `[0,10,20,60]`.

**Example 2.** Input `n = 3`, `flights = [[0,1,5],[1,2,5],[2,0,5]]`, output `[0,5,10]`.

**Hint.** When the second pass reads the cost of city 1, may it already contain a price that the second pass itself wrote?

**Changed decision.** The method builds each new row from a copy of the previous row and runs exactly two passes.

#### [Vary] Cost By Stops Used (Author exercise)
<!-- id: sp-cost-by-stops-used -->

**Prerequisites.** The exercise above.

**Problem.** The cities `0` to `n - 1` and the list `flights` are as in the previous exercise, and `src` is the start city. For every `j` from 0 to `limit`, let `cost[j][v]` be the lowest cost of a route from `src` to `v` with at most `j` flights. The value is `-1` when no such route exists. Return the table as a `long[][]` with `limit + 1` rows and `n` columns.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 100`.
- **Flights** satisfy `0 <= flights.length <= 400`, and repeated pairs may occur.
- **Prices** satisfy `1 <= w <= 1000`.
- **Limit** satisfies `0 <= limit <= 50`, and row 0 holds `0` for `src` and `-1` elsewhere.

**Example 1.** Input `n = 4`, `flights = [[0,1,10],[1,2,10],[2,3,10],[0,2,50]]`, `src = 0`, `limit = 2`, output `[[0,-1,-1,-1],[0,10,50,-1],[0,10,20,60]]`.

**Example 2.** Input `n = 3`, `flights = [[0,1,7],[1,2,1],[0,2,9]]`, `src = 0`, `limit = 3`, output `[[0,-1,-1],[0,7,9],[0,7,8],[0,7,8]]`.

**Hint.** Which row do you copy before the offers of the next row start, and does an entry ever rise from one row to the next?

**Changed decision.** The method stores every row and not only the last one, and each row starts as a copy of the row before it.

#### [Boundary] Direct Flight And K Zero (Author exercise)
<!-- id: sp-direct-flight-k-zero -->

**Prerequisites.** The two exercises above.

**Problem.** The cities `0` to `n - 1`, the list `flights` and the start city `src` are as before, and `dst` is the target city. A route may have at most `k` stops, where a stop is an intermediate city, so it uses at most `k + 1` flights. Among the routes with the lowest cost, choose the one with the fewest flights. Return an `int[]` of length 2 that holds that cost and that number of flights, or `{-1, -1}` when no route exists. The empty route is a route when `src == dst`.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 100`.
- **Flights** satisfy `0 <= flights.length <= 400`, and repeated pairs may occur.
- **Prices** satisfy `1 <= w <= 1000`, and `0 <= k <= 100`.
- **Equal ends** may occur, and then the result is `{0, 0}`.

**Example 1.** Input `n = 4`, `flights = [[0,1,10],[1,2,10],[2,3,10],[0,2,50],[0,3,70]]`, `src = 0`, `dst = 3`, `k = 0`, output `[70,1]`.

**Example 2.** Input `n = 3`, `flights = [[0,1,4]]`, `src = 2`, `dst = 2`, `k = 0`, output `[0,0]`.

**Hint.** For `k = 0`, how many passes run, and in which pass does the cost of `dst` first reach its final value?

**Changed decision.** The method runs `k + 1` passes and records the first pass that lowers the cost of `dst`, which gives the fewest flights for the lowest cost. When `src == dst`, the method records pass 0.

#### [Recognize] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sp-cheapest-flights-k-stops -->

**Prerequisites.** All three exercises above.

**Problem.** There are `n` cities numbered from 0. Each entry `[from, to, price]` of `flights` is a directed flight. Given `src`, `dst` and `k`, return the lowest total price of a route from `src` to `dst` that has at most `k` stops, where a stop is an intermediate city. Return `-1` when no such route exists.

**Constraints.** The limits are:
- **Cities** satisfy `1 <= n <= 100`.
- **Flights** satisfy `0 <= flights.length <= n * (n - 1) / 2`, and no pair `[from, to]` repeats.
- **Prices** satisfy `1 <= price <= 10000`, and `0 <= k < n`.
- **Ends** satisfy `src != dst`, and the result fits in an `int`.

**Example 1.** Input `n = 4`, `flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]`, `src = 0`, `dst = 3`, `k = 1`, output `700`.

**Example 2.** Input `n = 3`, `flights = [[0,1,100],[1,2,100],[0,2,500]]`, `src = 0`, `dst = 2`, `k = 0`, output `500`.

**Hint.** If a heap search stores one distance for each city, which arrival can it discard wrongly in the first example, where the route through cities 1 and 2 costs 400 but uses 3 flights?

**Changed decision.** The method keeps a state of city and flights used. It discards an arrival only when an earlier arrival at that city costs no more and used no more flights.
