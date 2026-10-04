<!-- lesson-kind: standard -->
<!-- lesson-id: dijkstra -->
## Dijkstra

<!-- stage: context -->
### Bartek And The Toll Roads

Bartek drives a delivery van for a seed merchant in the valley of Orlen. Every Monday he loads the van at the depot in Brindle and has to quote a delivery fee to each of the other towns on his round. The merchant charges what the trip costs him, and the only cost that changes from route to route is the tolls. Each road between two towns is one-way, because the valley has a ring of hairpin bends, and each has its own price, from a few coins for a flat causeway to a fistful for the ridge bridge.

The cheap-looking road out of Brindle often leads to a town whose only onward road is dear, while the expensive bridge sometimes opens a short run of free lanes. Bartek has stopped trusting his gut. He wants, for every town, the smallest total toll over any chain of roads from the depot, and he wants a method that works for any valley, however many towns and whatever the prices.

<!-- stage: naive -->
### Try Every Route To Every Town

The plain approach is to take one town at a time and walk every route from the depot to it. The walk never enters a town it has already passed on the current route, since going round a loop only adds toll. When it arrives, it compares the total paid with the best total so far and keeps the smaller one. Doing this for each town in turn gives all the quotes.

```java
static final long NONE = Long.MAX_VALUE;

static long cheapestRoute(List<int[]>[] roads, int town, int goal, boolean[] onRoute) {
    if (town == goal) return 0;
    onRoute[town] = true;
    long best = NONE;
    for (int[] road : roads[town]) {
        if (onRoute[road[0]]) continue;
        long rest = cheapestRoute(roads, road[0], goal, onRoute);
        if (rest != NONE) best = Math.min(best, rest + road[1]);
    }
    onRoute[town] = false;
    return best;
}
```

Calling this once per goal town answers the question correctly, because every route that never repeats a town is tried and the cheapest one wins. The price is paid in time: on a valley where every town has a road to every other, the number of routes to one goal grows like (n - 1)!, so even twelve towns means hundreds of millions of walks.

<!-- stage: bottleneck -->
### The Same Stretch Is Priced Again

The routes to different towns share long beginnings, and the walk prices those beginnings from scratch every time. If the cheapest way to Corvin goes through Brindle, Ashby and Dunmore, then the cheapest way to every town beyond Corvin that uses Corvin starts with that same stretch, yet the brute force walks it again for each goal and again for each route that branches off later. Across all goals the work is about n * (n - 1)!, which is O(n * n!) in the worst case, and almost every walk repeats a prefix whose cost was already known.

What the walk lacks is a way to say "I already know the cheapest price to this town, so nothing that arrives later needs to be looked at". With BFS that sentence was true for the first arrival, because every road counted the same. Here the first arrival at a town can be an expensive one, and a longer chain of cheap roads may beat it. The method needs a rule that says which arrival to trust, and a way to keep each town's price from being recomputed once it is trusted.

<!-- stage: insight -->
### Trust The Cheapest Open Price

Keep a price tag for every town, starting at infinity except the depot at zero. A tag is a **tentative distance**: the cost of the cheapest route found so far, which may still be beaten. Whenever a town is looked at, each road leaving it proposes a price for the town at its far end, namely the cost to the first town plus the toll. If that proposal is smaller than the tag there, the tag is replaced. This step is called **relaxation**, and it is the only way a tag ever changes.

The second idea is which town to look at next: always the one whose tag is smallest among those not yet looked at. Once that town is picked, its tag is **finalized**, meaning it is the true cheapest cost and will never change. The reason is short. Any other route to that town must leave the looked-at towns through some town that is still open, and that town already costs at least as much as the picked one. Every toll after it is zero or more, so the rest of the route can only add. No other route can come in cheaper.

The invariant is that every town taken off the board has its true cheapest cost as its tag. It rests entirely on tolls never being negative, and a single negative toll breaks it, as the trace later shows.

<!-- names: tentative distance, relaxation, finalized -->

<!-- stage: variables -->
### Tags, Heap Entries And Stale Pairs

The array `dist` holds one tag per town, `Long.MAX_VALUE` meaning "no route found yet" and `dist[depot]` being 0. The heap `board` holds pairs of a price and a town, ordered by price, and it may contain several pairs for the same town because Java's `PriorityQueue` cannot lower a price in place. Each loop pass removes a pair, whose price is `d` and whose town is `u`. If `d` is larger than `dist[u]`, the pair is stale, a leftover from before a cheaper route was found, and it is skipped. Otherwise `d` equals `dist[u]`, the town is finalized, and each road `{to, toll}` out of it produces a proposal `d + toll`. The proposal is compared with `dist[to]` and, when smaller, written there and pushed.

<!-- stage: trace -->
### Two Runs, One Of Them Breaks

The first trace is a valley of six towns numbered 0 to 5 with the depot at 0. Each cell is one pair taken off the heap, written as town@price, in the order the heap hands them over. The pointer `pop` is the position of the pair being handled. The vars give its price, how many pairs still wait in the heap and how many tags it improved. Town 1 first appears at price 7 straight from the depot, but the detour through town 2 gets there for 5, so the pair 1@7 is still sitting in the heap and is skipped as stale when its turn comes. The run ends with tags 0, 5, 2, 10, 6, 10.

```trace
{"cells":["0@0","2@2","1@5","4@6","1@7","3@10","5@10"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"cost":0,"heap":2,"improved":2},"note":"Town 0 is taken at cost 0; its tolls lower or set 1 to 7, 2 to 2."},{"at":{"pop":1},"vars":{"cost":2,"heap":3,"improved":2},"note":"Town 2 is taken at cost 2; its tolls lower or set 1 to 5, 3 to 10."},{"at":{"pop":2},"vars":{"cost":5,"heap":3,"improved":1},"note":"Town 1 is taken at cost 5; its tolls lower or set 4 to 6."},{"at":{"pop":3},"vars":{"cost":6,"heap":3,"improved":1},"note":"Town 4 is taken at cost 6; its tolls lower or set 5 to 10."},{"at":{"pop":4},"vars":{"cost":7,"heap":2,"improved":0},"note":"Entry 1@7 is stale, because town 1 is already known to cost 5; it is dropped with no work."},{"at":{"pop":5},"vars":{"cost":10,"heap":1,"improved":0},"note":"Town 3 is taken at cost 10; none of its tolls beat a known price."},{"at":{"pop":6},"vars":{"cost":10,"heap":0,"improved":0},"note":"Town 5 is taken at cost 10; none of its tolls beat a known price."}]}
```

The second trace uses a different valley of five towns that contains one road with a negative toll of minus 5, and it applies the finalization rule anyway: once a town is taken, its tag is never touched again. The vars show the price the run claims and the true cheapest cost, worked out separately. Town 1 is taken at 4, yet the road 0 to 2 followed by the negative road 2 to 1 reaches it for 0. The run ignores that proposal because town 1 is already taken, and the wrong 4 then travels on to towns 3 and 4. Three of the five answers are wrong.

```trace
{"cells":["0@0","1@4","2@5","3@6","4@7"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"cost":0,"truth":0,"wrong":0},"note":"Town 0 is taken at cost 0, which is correct."},{"at":{"pop":1},"vars":{"cost":4,"truth":0,"wrong":1},"note":"Town 1 is taken at cost 4, but the cheapest real cost is 0, so this claim is wrong."},{"at":{"pop":2},"vars":{"cost":5,"truth":5,"wrong":0},"note":"Town 2 is taken at cost 5, which is correct. Its toll toward 1, already taken, is ignored."},{"at":{"pop":3},"vars":{"cost":6,"truth":2,"wrong":1},"note":"Town 3 is taken at cost 6, but the cheapest real cost is 2, so this claim is wrong."},{"at":{"pop":4},"vars":{"cost":7,"truth":3,"wrong":1},"note":"Town 4 is taken at cost 7, but the cheapest real cost is 3, so this claim is wrong."}]}
```

<!-- stage: code -->
### Heap Of Prices With Stale Skipping

```java
final class Tolls {
    static long[] cheapestTolls(int n, int[][] roads, int depot) {
        List<int[]>[] out = new List[n];
        for (int i = 0; i < n; i++) out[i] = new ArrayList<>();
        for (int[] r : roads) out[r[0]].add(new int[] {r[1], r[2]});

        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[depot] = 0;
        PriorityQueue<long[]> board = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        board.add(new long[] {0, depot});
        while (!board.isEmpty()) {
            long[] top = board.poll();
            long d = top[0];
            int u = (int) top[1];
            if (d > dist[u]) continue;
            for (int[] road : out[u]) {
                long proposal = d + road[1];
                if (proposal < dist[road[0]]) {
                    dist[road[0]] = proposal;
                    board.add(new long[] {proposal, road[0]});
                }
            }
        }
        return dist;
    }
}
```

The comparator uses `Long.compare` and never subtracts, so large prices cannot wrap around. With V towns and E roads each successful improvement pushes one pair, so the heap holds at most E + 1 pairs and the total time is O((V + E) log E), with O(V + E) extra space. The test `d > dist[u]` is what stops a stale pair from re-expanding a town.

<!-- stage: applicability -->
### When Costs Differ But Stay Positive

Reach for Dijkstra when the question is "cheapest total cost from one source" and every step has a cost that is zero or more: tolls, travel times, fuel, delays, fees. The recognition cue is a weighted graph, directed or not, with no negative weights. The invariant to defend is that whatever leaves the heap first has its true cost, and that holds only because no later step can subtract.

The false friend is ordinary BFS. BFS counts roads, so it is right only when every road costs the same. On a valley where the direct road costs 9 and a two-road detour costs 2 + 3, BFS picks the direct road because it has fewer steps, and quotes the wrong fee. Keep it for equal-cost moves and use the heap as soon as the costs differ.

Do not use it when any edge can be negative, because the finalization argument fails, as the second trace shows, and use a method that revisits towns, such as Bellman-Ford, instead. In Java, a comparator written as `(a, b) -> a[0] - b[0]` overflows once prices pass about two billion and orders the heap wrongly, `Long.MAX_VALUE + toll` wraps to a negative number if an unreached town is expanded, and a `PriorityQueue` offers no decrease-key, so the stale check is not optional.

<!-- stage: exercises -->
### Exercises

#### [Build] Relax One Edge (Author exercise)
<!-- id: sp-relax-edge -->

**Prerequisites.** The tag array `dist` and the proposal `dist[u] + weight` from this lesson.

**Problem.** The `dist` array is a `long[]` of current tags, where `Long.MAX_VALUE` means a town has no known route. The call `relax(dist, u, v, w)` considers the road from town `u` to town `v` with toll `w`. If town `u` has a known route and the proposal `dist[u] + w` is strictly smaller than `dist[v]`, write the proposal into `dist[v]` and return `true`. In every other case return `false` and leave `dist` as it is. The array is changed in place by design; nothing else is modified.

**Constraints.** 2 <= dist.length <= 8, 0 <= u, v < dist.length, 0 <= w <= 1,000,000,000, and every known tag is between 0 and 1,000,000,000,000.

**Example 1.** Input `dist = [0, 7, Long.MAX_VALUE]`, `u = 1`, `v = 2`, `w = 4`, output `true`, and `dist` becomes `[0, 7, 11]`.

**Example 2.** Input `dist = [0, 3, 6]`, `u = 1`, `v = 2`, `w = 3`, output `false`, and `dist` stays `[0, 3, 6]`.

**Hint.** What happens to `dist[u] + w` when `dist[u]` is the largest `long`, and does an equal proposal count as better?

**Changed decision.** The tag is replaced only when the proposal is strictly smaller and the source has a real route, instead of always overwriting it with the newest proposal.

#### [Vary] Small Weighted Graph (Author exercise)
<!-- id: sp-settle-order -->

**Prerequisites.** The Relax One Edge rung, and the idea of always taking the smallest open tag.

**Problem.** Towns are numbered 0 to n - 1 and each road in `roads` is `{from, to, toll}` and runs one way. Starting at `depot`, repeatedly take the open town with the smallest tag, breaking ties by the smaller town number, and record it. Return an `int[]` of the towns in the order they are taken. Towns that cannot be reached are left out. Neither `roads` nor its rows are changed.

**Constraints.** 1 <= n <= 8, 0 <= depot < n, 0 <= roads.length <= 20, and 1 <= toll <= 20. Parallel roads and roads back into the depot are allowed.

**Example 1.** Input `n = 5`, `roads = [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,5]]`, `depot = 0`, output `[0, 2, 1, 3]`.

**Example 2.** Input `n = 4`, `roads = [[0,1,3],[0,2,3],[3,0,1]]`, `depot = 0`, output `[0, 1, 2]`.

**Hint.** When two towns hold the same tag, which one should come off first, and is town 4 ever taken in Example 1?

**Changed decision.** The answer is the order in which towns are taken, instead of the table of their final prices.

#### [Boundary] Unreachable Vertex And Large Sum (Author exercise)
<!-- id: sp-large-sum -->

**Prerequisites.** The Small Weighted Graph rung, and the way `Long.MAX_VALUE` stands for no route.

**Problem.** A valley has `n` towns, and each row of `roads` is `{from, to, toll}` for a one-way road between towns numbered from 0. Return a `long[]` with the cheapest total toll from `depot` to every town, and `Long.MAX_VALUE` in the slot of every town that cannot be reached. The depot's own entry is 0. Tolls can be as large as the biggest `int`, so a route of several roads can cost more than an `int` can hold. The input is not changed.

**Constraints.** 1 <= n <= 10, 0 <= depot < n, 0 <= roads.length <= 25, and 0 <= toll <= 2,147,483,647.

**Example 1.** Input `n = 4`, `roads = [[0,1,2000000000],[1,2,2000000000],[2,3,2000000000]]`, `depot = 0`, output `[0, 2000000000, 4000000000, 6000000000]`.

**Example 2.** Input `n = 4`, `roads = [[0,1,5],[2,1,3]]`, `depot = 0`, output `[0, 5, 9223372036854775807, 9223372036854775807]`.

**Hint.** Which variables must be `long`, and what should the loop do when the town it removed has no known route?

**Changed decision.** The unreachable sentinel is kept as a value that is never added to, and all sums are done in `long`, instead of using `int` with a large placeholder.

#### [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay -->

**Prerequisites.** The Unreachable Vertex And Large Sum rung.

**Problem.** A signal is sent from node `k` through a network of `n` nodes, and `times[i] = {u, v, w}` says a signal leaving `u` reaches `v` after `w` time units, in that direction only. This is the one exercise in the chapter where nodes are labelled 1 to n, because the LeetCode statement does it this way. Return the time at which the last node first receives the signal, or -1 if some node never receives it. The array `times` is not changed.

**Constraints.** 1 <= n <= 7, 1 <= k <= n, 0 <= times.length <= 15, and 0 <= w <= 20. Parallel edges and edges from a node to itself are allowed.

**Example 1.** Input `times = [[1,2,3],[1,3,1],[3,2,1],[2,4,2]]`, `n = 4`, `k = 1`, output `4`.

**Example 2.** Input `times = [[1,2,3],[3,1,2]]`, `n = 3`, `k = 1`, output `-1`.

**Hint.** What does the largest finite tag mean for the whole network, and what does an infinite one mean?

**Changed decision.** The answer is the largest of all cheapest distances and not the distance to one chosen target, with an infinite distance turned into -1.
