<!-- lesson-kind: standard -->
<!-- lesson-id: node-state-search -->
## Node-State Search

<!-- stage: context -->
### One Free Ride In Kerrow Vale

Tamsin has two days in Kerrow Vale and one wish: to stand at the lighthouse at the far end of the peninsula. The valley has no railway beyond the halt where she gets off, only seven bus services that join the halt, the mill, the chapel, the quay and the lighthouse stop. Every service runs one way only, because the lanes are too narrow for two buses to pass, and a ride costs whatever the board at the stop says, anything from 3 to 20 coins.

At the tourist office she was handed a coupon. It pays for one single ride of her choosing, in full, and it cannot be split across two rides or kept for another day. She wants the smallest total of coins from the halt to the lighthouse, with the coupon spent on whichever ride saves her the most, and she wants a method that still works when the board lists far more stops and services.

<!-- stage: naive -->
### Try Every Route And Every Free Ride

The plain way is to walk through the network recursively. At each stop Tamsin looks at every service leaving it, and for each one she tries two futures: pay the fare, or, while the coupon is still in her pocket, ride free and arrive with the coupon gone. A route is never allowed to pass the same stop twice, and the cheapest total over all these futures is the answer.

```java
static long cheapest(List<List<int[]>> out, int at, int to, boolean[] onRoute, boolean couponLeft) {
    if (at == to) return 0;
    onRoute[at] = true;
    long best = Long.MAX_VALUE;
    for (int[] ride : out.get(at)) {
        int next = ride[0], fare = ride[1];
        if (onRoute[next]) continue;
        long rest = cheapest(out, next, to, onRoute, couponLeft);
        if (rest != Long.MAX_VALUE) best = Math.min(best, rest + fare);
        if (couponLeft) {
            rest = cheapest(out, next, to, onRoute, false);
            if (rest != Long.MAX_VALUE) best = Math.min(best, rest);
        }
    }
    onRoute[at] = false;
    return best;
}
```

Every route and every choice of free ride is tried, so the minimum is right. Refusing to revisit a stop loses nothing, because cutting a loop out of a route never raises the fare, and a coupon spent inside that loop is simply still in hand afterwards.

<!-- stage: bottleneck -->
### Every Route Re-Solves The Same Trip

A network of n stops with many services can hold on the order of (n-1)! different routes, and each ride on a route may or may not take the coupon, so the recursion runs in O((n-1)! * n) time even before the coupon doubles some of the branches. For twenty stops that is far past anything a laptop finishes.

Look at what the recursion asks over and over. Once Tamsin stands at the chapel with the coupon still unused, the cheapest way to finish the trip is a fixed number, whether she came from the mill, the quay or the halt, and whether she paid 9 coins or 40 to get there. The earlier part of the route changes only what she has already spent, never what the rest costs. So there are only two situations per stop, coupon in pocket or coupon gone, which makes 2n situations in all, yet the recursion solves each of them once per route that happens to reach it. A table with one entry per situation would turn a factorial search into a few thousand steps.

<!-- stage: insight -->
### Two Copies Of The Same Map

Give every situation its own name: a **state pair** is the stop together with the one fact that changes what she may do next, here whether the coupon is still in hand. Two arrivals at the chapel are the same vertex of the search only when both halves of the pair match. Now draw the valley twice. The upper copy is the **mode layer** where the coupon is in hand, and the lower copy is the mode layer where it is spent. A paid service joins the same two stops inside whichever layer she is in and costs its fare. The coupon ride is the only edge that crosses layers: it leaves a stop in the upper copy, lands at the next stop in the lower copy, and costs nothing. The lighthouse is reached in either layer, so the answer is the smaller of its two distances.

That drawing is an ordinary weighted graph on 2n vertices, and Dijkstra from before applies unchanged. The question left is when one arrival may be thrown away, and the word for it is **dominance**. An arrival at a stop with the coupon in hand for a fare no larger than a rival's dominates that rival, because everything the rival can do the first can do for no more. The reverse fails: a cheaper arrival with the coupon gone does not dominate a costlier arrival with it still in hand, since the costlier one may spend the coupon on a 20 coin ride later. The invariant is that every state pair keeps its own cheapest fare and its own settled mark, and a pair is discarded only when a same-stop pair with equal or better coupon status costs no more.

<!-- names: state pair, mode layer, dominance -->

<!-- stage: variables -->
### Stops, Layers And Fares

The list `out` holds, for each stop, its services as pairs of destination and fare. The array `fare` has 2n entries, indexed by `stop * 2 + spent`, where `spent` is 0 while the coupon is in hand and 1 afterwards; an entry stays at the large sentinel until some route reaches that pair. The heap `waiting` holds entries made of a fare and a pair index, ordered by fare, and an improved arrival inserts a fresh entry rather than editing an old one. In the loop, `cur` is the entry just removed, `stop` and `spent` are decoded from its index, and an entry whose fare exceeds `fare[index]` is stale and ignored. The coupon ride writes into index `next * 2 + 1` with the fare unchanged.

<!-- stage: trace -->
### Settling Pairs On Two Networks

The first trace runs the search on the valley itself: five stops numbered 0 to 4 from the halt to the lighthouse, with services 0 to 1 at 4 coins, 0 to 2 at 9, 1 to 2 at 3, 1 to 3 at 12, 2 to 3 at 6, 2 to 4 at 20 and 3 to 4 at 7. Each cell is a pair in the order it is taken off the heap for the first time, written as the stop, a slash, and whether the coupon is still `open` or already `spent`. The pointer `cur` marks the pair being expanded, and the variables give its fare and how many stale entries were thrown away so far. The lighthouse is first settled at fare 7 with the coupon spent, by riding 0, 1, 2 and then using the coupon on the 20 coin service.

```trace
{"cells":["0/open","1/spent","2/spent","1/open","3/spent","2/open","4/spent","3/open","4/open"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"fare":0,"stale":0,"waiting":4},"note":"Pair 0/open is settled at fare 0; 4 entries now wait."},{"at":{"cur":1},"vars":{"fare":0,"stale":0,"waiting":4},"note":"Pair 1/spent is settled at fare 0; 4 entries now wait."},{"at":{"cur":2},"vars":{"fare":0,"stale":0,"waiting":5},"note":"Pair 2/spent is settled at fare 0; 5 entries now wait."},{"at":{"cur":3},"vars":{"fare":4,"stale":0,"waiting":7},"note":"Pair 1/open is settled at fare 4; 7 entries now wait."},{"at":{"cur":4},"vars":{"fare":4,"stale":0,"waiting":7},"note":"Pair 3/spent is settled at fare 4; 7 entries now wait."},{"at":{"cur":5},"vars":{"fare":7,"stale":1,"waiting":8},"note":"Pair 2/open is settled at fare 7; 8 entries now wait."},{"at":{"cur":6},"vars":{"fare":7,"stale":1,"waiting":7},"note":"Pair 4/spent is settled at fare 7; 7 entries now wait. The lighthouse is settled here with the coupon spent."},{"at":{"cur":7},"vars":{"fare":13,"stale":4,"waiting":4},"note":"Pair 3/open is settled at fare 13; 4 entries now wait."},{"at":{"cur":8},"vars":{"fare":20,"stale":5,"waiting":2},"note":"Pair 4/open is settled at fare 20; 2 entries now wait."}]}
```

The second trace is the false friend, run on a different network of five stops where the services are 0 to 1 at 3, 1 to 2 at 10, 2 to 3 at 4, 0 to 4 at 6 and 4 to 2 at 9. Here the cells are plain stops, each settled once only, and the search keeps one fare per stop. Stop 1 is reached first with the coupon already spent for 0 coins, so the costlier arrival with the coupon in hand is never kept. Stop 3 ends at 13 coins, while the pair search finds 7 by paying 3 to stop 1, riding free from 1 to 2, and paying 4 to stop 3.

```trace
{"cells":[0,1,4,2,3],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"fare":0,"spent":0},"note":"Stop 0 is settled once at fare 0 with the coupon in hand; no other arrival there is kept."},{"at":{"cur":1},"vars":{"fare":0,"spent":1},"note":"Stop 1 is settled once at fare 0 with the coupon spent; no other arrival there is kept."},{"at":{"cur":2},"vars":{"fare":0,"spent":1},"note":"Stop 4 is settled once at fare 0 with the coupon spent; no other arrival there is kept."},{"at":{"cur":3},"vars":{"fare":9,"spent":1},"note":"Stop 2 is settled once at fare 9 with the coupon spent; no other arrival there is kept."},{"at":{"cur":4},"vars":{"fare":13,"spent":1},"note":"Stop 3 is settled once at fare 13 with the coupon spent; no other arrival there is kept. The answer is wrong here: the pair search gets 7."}]}
```

<!-- stage: code -->
### Dijkstra Over Stop And Coupon

```java
final class CouponTrip {
    static long cheapestFare(int n, int[][] services, int from, int to) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] s : services) out.get(s[0]).add(new int[] {s[1], s[2]});

        long[] fare = new long[2 * n];
        Arrays.fill(fare, Long.MAX_VALUE);
        PriorityQueue<long[]> waiting = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        fare[from * 2] = 0;
        waiting.add(new long[] {0, from * 2});

        while (!waiting.isEmpty()) {
            long[] cur = waiting.poll();
            int index = (int) cur[1];
            if (cur[0] > fare[index]) continue;
            int stop = index / 2, spent = index % 2;
            for (int[] ride : out.get(stop)) {
                int paid = ride[0] * 2 + spent;
                if (cur[0] + ride[1] < fare[paid]) {
                    fare[paid] = cur[0] + ride[1];
                    waiting.add(new long[] {fare[paid], paid});
                }
                int free = ride[0] * 2 + 1;
                if (spent == 0 && cur[0] < fare[free]) {
                    fare[free] = cur[0];
                    waiting.add(new long[] {fare[free], free});
                }
            }
        }
        long best = Math.min(fare[to * 2], fare[to * 2 + 1]);
        return best == Long.MAX_VALUE ? -1 : best;
    }
}
```

The pair is flattened into one `int` index so that plain arrays hold the distances, and the free ride is offered only while the coupon is in hand. Time is O((V + E) log E) on a graph of 2V vertices and 2E edges, with O(V + E) memory, since each service yields at most two edges and the heap never holds more entries than successful relaxations.

<!-- stage: applicability -->
### When One Distance Per Stop Fails

Look for this shape whenever the cost of the remaining trip depends on something besides where you stand: a coupon or pass that can be used once, a bus line you may not take twice in a row, a battery level, a count of doors already unlocked. The recognition cue is that two arrivals at the same place can have different futures. The invariant to protect is that every combination of place and extra fact owns its distance and its settled mark, and that an arrival is dropped only when another one provably does at least as well.

The false friend is the single array `dist[stop]`. It looks like Dijkstra and passes every example where the cheapest arrival also happens to keep the most options, then returns too large an answer on a network like the second trace, where the cheapest arrival has used up the very resource a costlier arrival would spend better. It never answers too small, only too large, which makes it easy to miss in testing.

Do not widen the state when the extra fact has no influence on later moves, because every added value multiplies the vertex count, and do not reach for it when the resource ranges over a large set such as a subset of fifty keys, since 2^50 layers cannot be stored. In Java, keep the pair in a flat index or a record: an `int[]` placed in a `HashSet` is compared by identity, so an equal-looking pair is never found. Keep fares in `long` and compare them with `Long.compare`, because `(int) (a - b)` in a comparator truncates a difference of 2^32 to zero.

<!-- stage: exercises -->
### Exercises

#### [Build] Node And Coupon Flag (Author exercise)
<!-- id: sp-coupon-flag -->

**Prerequisites.** The coupon ride and the paid ride from the code stage, and the idea of a pair as one vertex.

**Problem.** The network has stops numbered from 0 and `services` is an `int[][]` of rows `{from, to, fare}`. A traveller stands at stop `u`, and `spent` is 0 if the one-time coupon is in hand and 1 if it is gone. Return every single ride she can take as a `List<long[]>` of triples `{destination, spentAfter, cost}`. Walk the services in input order. For each service leaving `u`, first add the paid ride, which keeps `spent` and costs the fare, and then, only when `spent` is 0, add the coupon ride, which sets `spentAfter` to 1 and costs 0. Parallel services give separate entries, and `services` is not modified.

**Constraints.** 0 <= u < 50, up to 200 services, and every fare is between 1 and 1,000,000. A stop with no outgoing service gives an empty list.

**Example 1.** Input `services = [[0,1,5],[0,2,2],[1,2,7]], u = 0, spent = 0`, output `[[1,0,5],[1,1,0],[2,0,2],[2,1,0]]`.

**Example 2.** Input `services = [[0,1,5],[0,2,2],[1,2,7]], u = 1, spent = 1`, output `[[2,1,7]]`.

**Hint.** Which of the two entries per service is conditional, and what does the flag after the ride look like in each?

**Changed decision.** A move can change the flag as well as the stop, instead of only the stop, so the neighbor list is built from the whole pair.

#### [Vary] Distance By State (Author exercise)
<!-- id: sp-distance-by-state -->

**Prerequisites.** The Node And Coupon Flag rung and Dijkstra with stale-entry skipping.

**Problem.** The network has `n` stops numbered 0 to n-1, and `services` is an `int[][]` of one-way rows `{from, to, fare}`. A traveller starts at `source` with the coupon in hand and may spend it on at most one ride, which then costs 0. Return a `long[n][2]` called `best`, where `best[v][0]` is the least total fare of any route from `source` to `v` that arrives with the coupon still unspent, and `best[v][1]` is the least total fare of a route that arrives having spent it. Use -1 where no such route exists. A route of zero rides counts, so `best[source][0]` is 0, and `services` is not modified.

**Constraints.** 1 <= n <= 8, up to 24 services, and every fare is between 1 and 2,000,000,000, so totals can pass the range of `int`. Self-loops and parallel services are possible.

**Example 1.** Input `n = 4, services = [[0,1,6],[1,2,2],[0,2,15],[2,3,4]], source = 0`, output `[[0,-1],[6,0],[8,0],[12,4]]`.

**Example 2.** Input `n = 3, services = [[1,0,4],[1,2,6],[2,0,1]], source = 1`, output `[[4,0],[0,-1],[6,0]]`.

**Hint.** What is the first index of each entry in the distance array, and which kind of ride is the only one allowed to change the second?

**Changed decision.** The answer keeps both layers' distances for every stop, instead of reducing them to a single minimum per stop.

#### [Boundary] Same Node, Different Future (Author exercise)
<!-- id: sp-same-node-future -->

**Prerequisites.** The Distance By State rung.

**Problem.** The network has `n` stops, one-way `services` rows `{from, to, fare}`, a `source` and a `target`, and one coupon that makes a single ride free. Call a stop `v` kept when all of these hold: some cheapest total route from `source` to `target` visits `v` before its free ride starts, so it arrives with the coupon unspent; and the cheapest arrival at `v` with the coupon spent is strictly cheaper than the cheapest arrival at `v` with it unspent. Return the kept stops in increasing order. If `source` equals `target`, or the target cannot be reached, return an empty list. The input is not modified.

**Constraints.** 1 <= n <= 7, up to 20 services, and fares are between 1 and 1,000. A route in the definition may be taken to be simple, because a repeated stop never helps.

**Example 1.** Input `n = 5, services = [[0,1,3],[1,2,10],[2,3,4],[0,4,6],[4,2,9]], source = 0, target = 3`, output `[1]`.

**Example 2.** Input `n = 3, services = [[0,1,2],[1,2,2],[0,2,9]], source = 0, target = 2`, output `[]`.

**Hint.** If you know the fare to reach each pair from the source and the fare to finish from each pair, what must their sum equal at a kept stop?

**Changed decision.** A costlier arrival is retained because its coupon is still in hand, instead of being dropped for losing on fare alone.

#### [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors -->

**Prerequisites.** The Distance By State rung, and breadth-first search from chapter 21.

**Problem.** A directed graph has `n` vertices labelled 0 to n-1, and each edge is red or blue: `redEdges` and `blueEdges` are `int[][]` of rows `{from, to}`. A path may only use edges whose colours alternate, so a red edge is followed by a blue one and a blue one by a red one, and its first edge may have either colour. Return an `int[] answer` where `answer[v]` is the number of edges on the shortest alternating path from vertex 0 to `v`, or -1 when none exists. Self-loops and parallel edges are possible, and neither input is modified.

**Constraints.** 1 <= n <= 100, and each edge list has at most 400 rows, with every vertex in range.

**Example 1.** Input `n = 5, redEdges = [[0,1],[0,3],[1,4]], blueEdges = [[3,1]]`, output `[0,1,-1,1,3]`.

**Example 2.** Input `n = 4, redEdges = [[0,1],[1,1],[2,3]], blueEdges = [[0,1],[3,2]]`, output `[0,1,-1,-1]`.

**Hint.** After reaching a vertex by a red edge, which colour may leave it, and does arriving by blue at the same vertex open a different set of exits?

**Changed decision.** The seen marker belongs to the pair of vertex and colour of the last edge, instead of to the vertex alone.
