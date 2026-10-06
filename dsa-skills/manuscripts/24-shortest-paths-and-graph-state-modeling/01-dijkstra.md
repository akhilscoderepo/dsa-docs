<!-- lesson-kind: standard -->
<!-- lesson-id: dijkstra -->
## Find Cheapest Routes With Dijkstra

<!-- stage: context -->
### Cheapest Route Is Not Fewest Roads

A navigation app plans trips over a road network where some roads charge a toll. A driver leaves town 0 for town 1. The direct road from town 0 to town 1 costs 7, and a detour through town 2 reaches town 1 for 2 plus 3, which is only 5. The app counts roads and picks the direct one, because one road is fewer than two. The driver pays 7 where 5 was possible. The app measures the wrong quantity, since a road count treats a free road and an expensive road alike.

Model the towns as vertices and each road as a directed edge that carries a **weight**, the toll for using it. The cost of a route is the sum of its weights. The task is to find, from one source town, the minimum cost to every other town, and to report that a town is unreachable when no route leads to it. All weights in this lesson are zero or positive.

This lesson asks which town the search should expand next, so that the first cost it accepts for a town is already the lowest one.

<!-- stage: naive -->
### Counting Roads With A Queue

The first attempt is breadth-first search. It keeps a queue of towns and a `cost` array. The first time a road reaches a town, the search stores the cost of that road chain and never changes it.

```java
static long[] fewestRoads(int n, int[][] roads, int src) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
    long[] cost = new long[n];
    Arrays.fill(cost, -1);
    cost[src] = 0;
    ArrayDeque<Integer> queue = new ArrayDeque<>();
    queue.add(src);
    while (!queue.isEmpty()) {
        int cur = queue.poll();
        for (int[] r : adj.get(cur)) {
            if (cost[r[0]] == -1) {
                cost[r[0]] = cost[cur] + r[1];
                queue.add(r[0]);
            }
        }
    }
    return cost;
}
```

The method visits each town once and each road once. It reaches exactly the towns that have a route, and it stores the first cost it sees for each town. The question is whether the stored cost is the cheapest one.

```predict
Use the roads 0 to 1 with weight 7, 0 to 2 with weight 2, and 2 to 1 with weight 3. What cost does fewestRoads store for town 1?

It stores 7, which is wrong. Town 0 is taken from the queue first and reaches town 1 and town 2. Town 1 is marked with the direct cost 7 at that moment, so the later chain through town 2 is rejected by the check against minus one. The true minimum is 5. The method fixes a cost at the first arrival, and the first arrival is the one with the fewest roads, not the lowest toll.
```

<!-- stage: bottleneck -->
### Queue Order Ignores Road Cost

The queue releases towns in order of road count, so every town at depth 1 leaves the queue before any town at depth 2. Cost and depth agree only when each road costs the same. With uneven tolls, a town at depth 2 can be cheaper than a town at depth 1, and the queue still handles the shallow one first.

Allowing the search to overwrite a stored cost does not repair this. A town whose cost drops must be expanded again, and so must every town that depends on it. With an unlucky order, the same town is expanded many times. A first-in first-out queue with re-expansion has a worst case of O(V * E) edge scans, where V is the number of towns and E is the number of roads. The cost array also stays unreliable until the queue is empty, because any entry may still drop.

A better method must choose the next town by cost. It must also guarantee that the chosen town never needs a second visit. Then the total work stays close to one scan of each road, plus the price of ordering the candidates.

<!-- stage: insight -->
### Taking The Smallest Tentative Cost First

The method keeps a best known cost for every town and always expands the town with the smallest candidate cost.

<!-- names: tentative, relax, finalized -->

#### The Tentative Cost Of Each Town

The array `dist` holds a **tentative** distance for every town, which is the cheapest route found so far and an upper bound on the true answer. It starts at infinity for every town except the source, which starts at 0. A tentative value only moves downward. A town is **finalized** when its distance can no longer improve, and the tentative value of a finalized town is exact.

#### Relaxing One Road

To **relax** a road from `u` to `v` with weight `w`, the method computes `dist[u] + w` and compares it with `dist[v]`. When the sum is smaller, the method stores it in `dist[v]` and adds the pair of that cost and `v` to a priority queue. The queue is a binary heap that returns its smallest cost first. The relaxation cannot raise any value, so every stored cost stays achievable by a real route.

#### Why The Smallest Entry Is Final

Take the entry with the smallest cost `d` from the heap, for the town `u`. The claim is that `u` is finalized now. Any other route to `u` must leave the finalized towns through a road whose far end is still waiting in the heap. That far end has a tentative cost of at least `d`, because `d` is the smallest. The remaining roads of the route add weights that are zero or more. So the other route costs at least `d`, and `d` is the minimum.

#### Skipping Outdated Heap Entries

A town can enter the heap several times, once for each improvement. Java's `PriorityQueue` has no operation that lowers an entry in place. The old entry stays in the heap with its higher cost. It is called **stale**, because its cost exceeds the current `dist` of its town. When a stale entry leaves the heap, the method compares the cost with `dist[u]` and skips the entry without any work.

#### Why Weights Must Not Be Negative

The argument above uses the sentence "the remaining roads add zero or more". A negative road breaks it, because a route through a waiting town could end up cheaper after that road. The second trace below shows a wrong answer that results. Distances use `long`, since a path of many large weights exceeds the range of `int`.

<!-- stage: variables -->
### Distances And The Heap

The search reads `n`, the list `roads` of triples `[from, to, weight]`, and the source `src`. It changes none of them. It builds an adjacency list from `roads` and keeps two structures and one working value.

- **dist** is a `long[]` of length `n`; `Long.MAX_VALUE` marks a town with no known route.
- **heap** is a `PriorityQueue<long[]>` whose entries are `{cost, town}`, ordered by `cost` with `Long.compare`.
- **cost** is the first field of the entry that was just removed, and `u` is its town.

Only finite costs enter the heap, so the sum `cost + weight` never starts from the infinity marker and cannot overflow through it.

<!-- stage: trace -->
### Two Runs On Small Road Maps

#### Six Towns With Uneven Tolls

The first map has eight roads. Town 0 reaches town 1 for 7 and town 2 for 2. Town 2 reaches town 1 for 3 and town 3 for 8. Town 1 reaches town 4 for 1, and town 3 reaches town 4 for 2 and town 5 for 1. Town 4 reaches town 5 for 4. Each cell is one heap entry in the order in which the entries leave the heap, written as town and cost. The pointer `pop` marks the entry that leaves at that step. The variable `cost` is the cost of the removed entry, `heap` is the number of entries left afterward, and `improved` counts the distances that dropped at this step. At step 2, town 2 leaves at cost 2 and lowers town 1 from 7 to 5. That adds a second entry for town 1. At step 5 the old entry 1@7 leaves the heap, and the method drops it as stale. The final distances are 0, 5, 2, 10, 6 and 10.

```trace
{"cells":["0@0","2@2","1@5","4@6","1@7","3@10","5@10"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"cost":0,"heap":2,"improved":2},"note":"Town 0 is taken at cost 0; its tolls lower or set 1 to 7, 2 to 2."},{"at":{"pop":1},"vars":{"cost":2,"heap":3,"improved":2},"note":"Town 2 is taken at cost 2; its tolls lower or set 1 to 5, 3 to 10."},{"at":{"pop":2},"vars":{"cost":5,"heap":3,"improved":1},"note":"Town 1 is taken at cost 5; its tolls lower or set 4 to 6."},{"at":{"pop":3},"vars":{"cost":6,"heap":3,"improved":1},"note":"Town 4 is taken at cost 6; its tolls lower or set 5 to 10."},{"at":{"pop":4},"vars":{"cost":7,"heap":2,"improved":0},"note":"Entry 1@7 is stale, because town 1 is already known to cost 5; it is dropped with no work."},{"at":{"pop":5},"vars":{"cost":10,"heap":1,"improved":0},"note":"Town 3 is taken at cost 10; none of its tolls beat a known price."},{"at":{"pop":6},"vars":{"cost":10,"heap":0,"improved":0},"note":"Town 5 is taken at cost 10; none of its tolls beat a known price."}]}
```

#### A Negative Road Breaks The Rule

The second map has five roads. Town 0 reaches town 1 for 4 and town 2 for 5. Town 2 reaches town 1 for minus 5. Town 1 reaches town 3 for 2, and town 3 reaches town 4 for 1. This run is a variant that closes each town at its first removal. The code in the code stage does not close towns, so with a negative road it would expand towns again and lose its bound on the work. The variable `truth` is the cheapest real cost, and `wrong` is 1 when the claimed cost differs from it. Town 1 leaves the heap at cost 4, but the route 0, 2, 1 costs 0. By the time the entry for town 2 arrives, town 1 is closed, and the negative road cannot lower it. Towns 3 and 4 inherit the error, so three of the five claims are wrong.

```trace
{"cells":["0@0","1@4","2@5","3@6","4@7"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"cost":0,"truth":0,"wrong":0},"note":"Town 0 is taken at cost 0, which is correct."},{"at":{"pop":1},"vars":{"cost":4,"truth":0,"wrong":1},"note":"Town 1 is taken at cost 4, but the cheapest real cost is 0, so this claim is wrong."},{"at":{"pop":2},"vars":{"cost":5,"truth":5,"wrong":0},"note":"Town 2 is taken at cost 5, which is correct. Its toll toward 1, already taken, is ignored."},{"at":{"pop":3},"vars":{"cost":6,"truth":2,"wrong":1},"note":"Town 3 is taken at cost 6, but the cheapest real cost is 2, so this claim is wrong."},{"at":{"pop":4},"vars":{"cost":7,"truth":3,"wrong":1},"note":"Town 4 is taken at cost 7, but the cheapest real cost is 3, so this claim is wrong."}]}
```

<!-- stage: code -->
### Dijkstra With A Priority Queue

The method returns a `long[]` in which `Long.MAX_VALUE` marks an unreachable town. The comparator uses `Long.compare`, because a subtraction of two `long` values can overflow when cast to `int`.

```java
static long[] cheapest(int n, int[][] roads, int src) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
    for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, src});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        long cost = top[0];
        int u = (int) top[1];
        if (cost > dist[u]) continue;
        for (int[] r : adj.get(u)) {
            long next = cost + r[1];
            if (next < dist[r[0]]) {
                dist[r[0]] = next;
                heap.add(new long[] {next, r[0]});
            }
        }
    }
    return dist;
}
```

The test `cost > dist[u]` must come before the loop, so that a stale entry costs nothing. Each nonstale removal relaxes each road of its town once. Each successful relaxation adds one heap entry, so the heap holds at most E + 1 entries, counting the entry of the source. The method runs in O(E log E) time, which equals O(E log V). It uses O(V + E) memory for the adjacency list, the array and the heap.

<!-- stage: applicability -->
### Recognizing Cheapest Route Problems

#### Reading The Cue

Use this method when the statement gives edges with nonnegative weights and asks for the minimum total cost from one source. Delivery fees, network latency between servers, and travel time between stations all have this shape. The answer is usually a distance array, the distance to one target, or the largest of the finite distances.

#### Checking The Invariant

The invariant is that every town removed as a nonstale entry holds its final distance, and every heap entry is an achievable route cost. It depends on two conditions in the code. The skip test for stale entries must run before any relaxation, and no weight may be negative. Test a zero weight, which is allowed and keeps the argument valid. Test an unreachable town, which must keep the infinity marker and never take part in a sum.

#### Avoiding The False Friend

A false friend is a familiar method that looks right and fails. The false friend here is breadth-first search. It is correct when every road has the same cost, and the first example of this lesson shows the failure when costs differ. A second false friend is stopping the search when the target is first added to the heap. The first cost pushed for a town is only tentative, and only the removal from the heap makes it final.

<!-- stage: exercises -->
### Exercises

#### [Build] Relax One Edge (Author exercise)
<!-- id: sp-dijkstra-relax-edge -->

**Prerequisites.** The relaxation step of this lesson.

**Problem.** An array `dist` of type `long[]` holds a tentative distance for each town, and `Long.MAX_VALUE` means that no route is known. A road goes from town `u` to town `v` with weight `w`. Relax the road: when `dist[u]` is finite and `dist[u] + w < dist[v]`, store `dist[u] + w` in `dist[v]`. Return `true` when the method changed `dist[v]`, and `false` otherwise.

**Constraints.** The limits are:
- **Towns** satisfy `1 <= dist.length <= 1000`, and `u` and `v` are valid indices.
- **Weight** satisfies `0 <= w <= 2000000000`.
- **Distances** are either `Long.MAX_VALUE` or in `0..10^12`.
- **Mutation** is allowed on `dist[v]` only.

**Example 1.** Input `dist = [0,9,2]`, `u = 2`, `v = 1`, `w = 3`, output `true`, and `dist` becomes `[0,5,2]`.

**Example 2.** Input `dist = [9223372036854775807,4,9223372036854775807]`, `u = 0`, `v = 2`, `w = 5`, output `false`, and `dist` is unchanged.

**Hint.** What does the sum `dist[u] + w` become when `dist[u]` is the largest `long` value?

**Changed decision.** The method updates `dist[v]` only for a strictly smaller proposal and skips the sum when the source distance is unknown.

#### [Vary] Small Weighted Graph (Author exercise)
<!-- id: sp-dijkstra-small-graph -->

**Prerequisites.** The exercise above.

**Problem.** A directed graph has towns `0` to `n - 1`, and `roads` lists triples `[a, b, w]` for a road from `a` to `b` with weight `w`. Run Dijkstra's method from town `0`, ordering heap entries by cost and then by town index. Return an `int[]` that lists the towns in the order of their first nonstale removal from the heap. Towns with no route do not appear.

**Constraints.** The limits are:
- **Towns** satisfy `1 <= n <= 1000`.
- **Roads** satisfy `0 <= roads.length <= 5000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 1000`.
- **Result** starts with `0` and has one entry for each reachable town.

**Example 1.** Input `n = 6`, `roads = [[0,1,7],[0,2,2],[2,1,3],[2,3,8],[1,4,1],[3,4,2],[4,5,4],[3,5,1]]`, output `[0,2,1,4,3,5]`.

**Example 2.** Input `n = 4`, `roads = [[0,1,0],[0,2,0],[2,3,1],[1,3,1]]`, output `[0,1,2,3]`.

**Hint.** When two towns have the same cost, which one does the tie rule remove first, and does a zero weight change that?

**Changed decision.** The method returns the order of removal and not the distances, so the tie rule and the skip of stale entries both change the output.

#### [Boundary] Unreachable Vertex And Large Sum (Author exercise)
<!-- id: sp-dijkstra-unreachable-large -->

**Prerequisites.** The two exercises above.

**Problem.** Consider `n` towns numbered from 0 and the one-way roads in `roads`, where each triple `[a, b, w]` joins `a` to `b` at toll `w`. Return a `long[]` `d` of length `n`. Entry `d[v]` is the minimum total weight of a route from town `0` to town `v`, or `-1` when no route exists.

**Constraints.** The limits are:
- **Towns** satisfy `1 <= n <= 2000`.
- **Roads** satisfy `0 <= roads.length <= 6000`, and repeats and self loops may occur.
- **Weight** satisfies `0 <= w <= 2000000000`.
- **Sums** may exceed the range of `int`, and the result uses `long`.

**Example 1.** Input `n = 3`, `roads = [[0,1,2000000000],[1,2,2000000000]]`, output `[0,2000000000,4000000000]`.

**Example 2.** Input `n = 4`, `roads = [[0,1,5],[2,3,1]]`, output `[0,5,-1,-1]`.

**Hint.** Which value marks an unreachable town during the search, and what happens if the method adds a weight to it?

**Changed decision.** The method keeps an infinity marker that never enters a sum, and it converts the marker to minus one only when it builds the result.

#### [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-dijkstra-network-delay -->

**Prerequisites.** All three exercises above.

**Problem.** A network has nodes labeled `1` to `n`. A signal crosses the link `[u, v, w]` of `times` from `u` to `v` in `w` time units. A signal starts at node `k`. Return an `int[]` of length 2. The first entry is the largest finite arrival time over all nodes, with node `k` counting as time 0. The second entry is the number of nodes that the signal never reaches.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 500`.
- **Links** satisfy `0 <= times.length <= 6000`, and repeats and self loops may occur.
- **Time** satisfies `0 <= w <= 100`.
- **Start** satisfies `1 <= k <= n`.

**Example 1.** Input `n = 4`, `times = [[2,1,1],[2,3,1],[3,4,1]]`, `k = 2`, output `[2,0]`.

**Example 2.** Input `n = 3`, `times = [[1,2,4]]`, `k = 1`, output `[4,1]`.

**Hint.** Which distances count toward the maximum, and how does the method tell a reached node from an unreached one?

**Changed decision.** The method ignores unreached nodes in the maximum and counts them separately. The usual statement returns minus one when any node is unreached.
