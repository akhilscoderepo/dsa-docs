<!-- lesson-kind: combination -->
<!-- lesson-id: graph-and-heap -->
## Graph And Heap

<!-- stage: context -->
### Flares Over Tarn Meadow

Every September the town of Tarn Meadow holds a balloon festival, and on the opening night nine launch pads are scattered over the plateau. The festival map numbers them from 1. Nobody walks between pads in the dark. Instead the head marshal, Odile Brandt, fires a green flare from her own pad, and each crew that can see a lit flare answers it with a flare of its own after a pause. The pause depends on how long the crew needs to finish its checks, and it differs from one sight line to the next. Hills and wind make every sight line one-way, so pad 4 may see pad 7 without pad 7 seeing pad 4.

Odile wants two facts from the first flare: how long it takes before every pad has lit, and which pad is the last one. The second fact matters because that crew gets the tow truck. The map has a few hundred sight lines, and next year it will have more, so the method must not depend on the map staying small.

<!-- stage: contributions -->
### What Graph And Heap Bring

The graph brings the improvements. Every time a pad is finished, each of its outgoing sight lines offers a time for the pad at the far end, and when that offer beats everything seen so far it is an improved candidate. The graph decides which offers exist and what each one costs, and it knows nothing about the order in which to look at them.

The heap brings the order. It keeps all open offers together and always exposes the smallest one, so the loop never has to search for it. A heap cannot lower an offer that is already inside it, so a better offer for the same pad is simply pushed as a new entry, and the old entry is recognised and thrown away when it comes to the top. That stale rejection replaces the decrease-key operation that textbooks assume.

Neither is enough alone. The graph without a heap must scan every open pad each round, and the heap without a graph has no source of new offers. The cue for the pair is a question about best routes in a graph whose steps cannot make a route better by being added.

<!-- stage: naive -->
### Follow Every Chain Of Sight Lines

The direct method imitates what the crews would do if each flare could travel along every possible chain. Starting at the marshal's pad, a depth-first search follows each sight line to a pad not yet on the current chain, records the time of arrival if it beats the best time written so far for that pad, and then backs out so that another chain can be tried. At the end the table holds the earliest time for each pad, and a final scan finds the largest value and the smallest label that holds it.

```java
static long[] lastToLight(int n, int[][] sights, int first) {
    long[] best = new long[n + 1];
    java.util.Arrays.fill(best, Long.MAX_VALUE);
    chain(sights, first, 0, new boolean[n + 1], best);
    long worst = -1;
    int who = -1;
    for (int pad = 1; pad <= n; pad++) {
        if (best[pad] == Long.MAX_VALUE) return new long[] {-1, -1};
        if (best[pad] > worst) { worst = best[pad]; who = pad; }
    }
    return new long[] {worst, who};
}

static void chain(int[][] sights, int pad, long time, boolean[] onChain, long[] best) {
    best[pad] = Math.min(best[pad], time);
    onChain[pad] = true;
    for (int[] s : sights)
        if (s[0] == pad && !onChain[s[1]]) chain(sights, s[1], time + s[2], onChain, best);
    onChain[pad] = false;
}
```

The method is correct for any map with nonnegative pauses, because every simple chain from the first pad is tried and the best time per pad is kept.

<!-- stage: bottleneck -->
### Chains Multiply Faster Than Pads

The number of chains is the trouble. If every pad can see every other, a map of n pads has about (n - 1)! simple chains from the first pad, and each step scans the whole list of E sight lines, so the work is roughly O(E * n!) in the worst case. Twelve pads that all see one another already give hundreds of millions of chains, and a festival with forty pads would never finish before the balloons rose.

Almost all of that work repeats itself. Two different chains that arrive at pad 9 with times 14 and 20 continue in exactly the same way afterwards, so the slower one can only produce times that the faster one beats. What is needed is a loop that holds one best time per pad, improves it only when a better offer arrives, and looks at the pads in the order of their times, so that each pad is expanded once and the cost drops to about O((V + E) log E).

<!-- stage: insight -->
### Pop The Cheapest, Reject The Old

Keep one best-known time for each pad and a heap of offers, each offer being a time together with the pad it belongs to. The loop takes the smallest offer from the heap. If its time is larger than the best-known time of its pad, a better offer for that pad arrived after it was pushed, and the old entry is dropped without a glance. This **stale rejection** is the whole price of having no decrease-key. If its time equals the best-known time, the entry is current, and the pad can be expanded: each outgoing sight line proposes the time plus its pause, and a proposal that beats the target's best-known time becomes an **improved candidate**, which is written into the table and pushed as a fresh entry.

A pad that has passed the test is final, and the reason is the whole combined invariant. Every entry still in the heap is at least as large as the entry just taken, and every route that has not been found yet must leave through some entry in the heap and can only grow from there, because a pause is never negative. So nothing can arrive at this pad earlier. A **settled mark** in a separate array is not needed for correctness and it would hide the failures that appear when the assumption is broken, which is why the comparison with the table is the better guard.

The aggregation can change without touching the loop. A route priced by the largest single step still never improves when extended, and so does a probability that is multiplied by factors of at most one. What changes is how an offer is formed and which direction the heap favours. When the pad alone is not enough to describe where the traveller stands, as with a limit on flights, the table and the heap are keyed by the pad together with the extra count.

<!-- names: stale rejection, improved candidate, settled mark -->

<!-- stage: variables -->
### Table, Heap And Offer Fields

The array `best` holds one time per pad, with `Long.MAX_VALUE` for a pad that no offer has reached, and an unreached pad is never used in a sum. A heap entry is an offer: the time, the pad, and, in the flight version, the number of flights used so far. The comparator orders by time first, then by flights used, then by pad, so equal times come off in a fixed order. The counter `skipped` is not needed for the answer and only helps the trace. For the flight version the table is two-dimensional, `best[pad][used]`, and the key of a stale test is the pair. Times are `long`, because a few legs of a billion each overflow an `int`.

<!-- stage: trace -->
### Two Runs Of The Heap

The first trace follows the loop on the map `[[2,1,2],[2,3,1],[3,4,3],[1,4,1],[4,5,2]]` with the first flare on pad 2. The cells are the pads, and the pointer `u` marks the pad whose entry has just come off the heap. Pad 4 receives the offer 4 through pad 3 and later the better offer 3 through pad 1, so its first entry is still in the heap when the better one has been written, and it is rejected when it surfaces.

```trace
{"cells":["1","2","3","4","5"],"pointers":["u"],"steps":[{"at":{"u":1},"vars":{"time":0,"best":0,"skipped":0,"waiting":2},"note":"Pad 2 is final at time 0; it pushes pad 1 at 2, pad 3 at 1."},{"at":{"u":2},"vars":{"time":1,"best":1,"skipped":0,"waiting":2},"note":"Pad 3 is final at time 1; it pushes pad 4 at 4."},{"at":{"u":0},"vars":{"time":2,"best":2,"skipped":0,"waiting":2},"note":"Pad 1 is final at time 2; it pushes pad 4 at 3."},{"at":{"u":3},"vars":{"time":3,"best":3,"skipped":0,"waiting":2},"note":"Pad 4 is final at time 3; it pushes pad 5 at 5."},{"at":{"u":3},"vars":{"time":4,"best":3,"skipped":1,"waiting":1},"note":"The entry (4, pad 4) is older than the recorded time 3, so stale rejection drops it and pad 4 is not expanded again."},{"at":{"u":4},"vars":{"time":5,"best":5,"skipped":1,"waiting":0},"note":"Pad 5 is final at time 5 and offers nothing better. The largest time is 5, held by pad 5."}]}
```

The second trace is the flight version on four airstrips with flights `0 to 1` for 1, `1 to 2` for 1, `2 to 3` for 1 and `0 to 2` for 5, from strip 0 to strip 3 with at most one stop. Each cell is a state written as strip and flights used, listed in the order the heap releases them. Strip 2 is released twice, once with two flights and once with one flight, and both are valid because the pair is the key. The cheap arrival has used up the flights and cannot continue, which is why the dearer direct flight to strip 2 has to survive.

```trace
{"cells":["0/0","1/1","2/2","2/1","3/2"],"pointers":["pop"],"steps":[{"at":{"pop":0},"vars":{"cost":0,"flights":0,"waiting":2},"note":"State 0/0 costs 0; it pushes 1/1 at 1, 2/1 at 5."},{"at":{"pop":1},"vars":{"cost":1,"flights":1,"waiting":2},"note":"State 1/1 costs 1; it pushes 2/2 at 2."},{"at":{"pop":2},"vars":{"cost":2,"flights":2,"waiting":1},"note":"State 2/2 is current but all 2 flights are used, so nothing is expanded."},{"at":{"pop":3},"vars":{"cost":5,"flights":1,"waiting":1},"note":"State 2/1 costs 5; it pushes 3/2 at 6."},{"at":{"pop":4},"vars":{"cost":6,"flights":2,"waiting":0},"note":"Strip 3 is the destination, released with cost 6 and 2 flights, so the answer is 6 with 2 flights."}]}
```

<!-- stage: code -->
### Heap Loops For Last Pad And Flights

```java
final class Festival {
    static long[] lastToLight(int n, int[][] sights, int first) {
        java.util.List<int[]>[] out = new java.util.List[n + 1];
        for (int i = 1; i <= n; i++) out[i] = new java.util.ArrayList<>();
        for (int[] s : sights) out[s[0]].add(new int[] {s[1], s[2]});
        long[] best = new long[n + 1];
        java.util.Arrays.fill(best, Long.MAX_VALUE);
        best[first] = 0;
        java.util.PriorityQueue<long[]> heap = new java.util.PriorityQueue<>(java.util.Comparator.comparingLong(o -> o[0]));
        heap.add(new long[] {0, first});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int pad = (int) top[1];
            if (top[0] > best[pad]) continue;
            for (int[] e : out[pad]) {
                long offer = top[0] + e[1];
                if (offer < best[e[0]]) { best[e[0]] = offer; heap.add(new long[] {offer, e[0]}); }
            }
        }
        long worst = -1;
        int who = -1;
        for (int pad = 1; pad <= n; pad++) {
            if (best[pad] == Long.MAX_VALUE) return new long[] {-1, -1};
            if (best[pad] > worst) { worst = best[pad]; who = pad; }
        }
        return new long[] {worst, who};
    }

    record Leg(long cost, int used, int strip) {}

    static long[] cheapestFewest(int n, int[][] flights, int from, int to, int stops) {
        int cap = stops + 1;
        long[][] best = new long[n][cap + 1];
        for (long[] row : best) java.util.Arrays.fill(row, Long.MAX_VALUE);
        best[from][0] = 0;
        java.util.PriorityQueue<Leg> heap = new java.util.PriorityQueue<>(
            java.util.Comparator.comparingLong(Leg::cost).thenComparingInt(Leg::used).thenComparingInt(Leg::strip));
        heap.add(new Leg(0, 0, from));
        while (!heap.isEmpty()) {
            Leg cur = heap.poll();
            if (cur.cost() > best[cur.strip()][cur.used()]) continue;
            if (cur.strip() == to) return new long[] {cur.cost(), cur.used()};
            if (cur.used() == cap) continue;
            for (int[] f : flights) {
                if (f[0] != cur.strip()) continue;
                long next = cur.cost() + f[2];
                if (next < best[f[1]][cur.used() + 1]) {
                    best[f[1]][cur.used() + 1] = next;
                    heap.add(new Leg(next, cur.used() + 1, f[1]));
                }
            }
        }
        return new long[] {-1, -1};
    }
}
```

With V pads and E sight lines, every improvement pushes one entry, so the heap never holds more than E + 1 entries and the first method runs in O((V + E) log E) time with O(V + E) space. The flight version has at most V * (stops + 2) states, so it costs O((stops + 2) * E log E) time. Because the first entry for the target that leaves the heap has the smallest cost and, among equals, the fewest flights, it can be returned at once.

<!-- stage: applicability -->
### Where The Heap Loop Applies

Reach for this combination when a graph has steps that never make a route better by being added and the question is about the best route to one pad or to all of them: smallest delay, smallest worst climb on a ride, cheapest fare, most reliable chain of links. The invariant is that the entry leaving the heap with a current time is final, because everything still waiting is at least as large. Changing the aggregation to a maximum, or to a product of factors that are at most one with the heap turned around, keeps that invariant intact.

The nearest false friend is to keep summing when the question asks for a worst step, or to keep one distance per node when the route also has a count to respect. Both give a clean answer, and both are wrong on small graphs. A graph with a single negative edge is a no-go condition: the first entry to leave the heap is no longer final, so use the relaxation passes of Chapter 25. When every step costs zero or one, the deque of the next lesson is lighter than a heap, and a table of distances between all pairs belongs to Chapter 25 as well.

In Java, the comparator must never subtract. Writing `(int) (a - b)` on a long time wraps around for large values and the heap quietly misorders them, and truncating a `double` difference to an int collapses every probability gap to zero. Use `Long.compare` and `Double.compare`, and keep sums of times in `long`.

<!-- stage: exercises -->
### Exercises

#### [Build] Network Delay Time (LeetCode 743)
<!-- id: sh-last-to-light -->

**Prerequisites.** The Dijkstra and Stale Heap Entries lessons, and the pause-adding relaxation of this lesson.

**Problem.** Signals travel through a network of `n` nodes labelled 1 to n, because the LeetCode statement uses these labels, and `times[i] = {u, v, w}` means a signal leaving `u` reaches `v` after `w` time units, in that direction only. A signal starts at node `k`. Return a `long[]` of two values: the time at which the last node first receives the signal, and the label of that last node, choosing the smallest label when several nodes share the largest time. If some node never receives the signal, return `{-1, -1}`. The array `times` is not changed.

**Constraints.** 1 <= n <= 7, 1 <= k <= n, 0 <= times.length <= 15, and 0 <= w <= 1,000,000,000. Parallel edges, self-loops and zero-time edges are allowed.

**Example 1.** Input `n = 5`, `times = [[2,1,2],[2,3,1],[3,4,3],[1,4,1],[4,5,2]]`, `k = 2`, output `[5, 5]`.

**Example 2.** Input `n = 4`, `times = [[3,1,0],[3,2,4],[1,4,4],[3,4,5]]`, `k = 3`, output `[4, 2]`.

**Hint.** Which nodes share the largest finite time in Example 2, and what must a stale entry never do to the answer?

**Changed decision.** The answer is the pair of the largest cheapest time and the smallest label that holds it, instead of the time alone, and an unreached node turns the whole pair into -1.

#### [Vary] Path With Minimum Effort (LeetCode 1631)
<!-- id: sh-min-effort -->

**Prerequisites.** The Build rung, and the idea that a route can be priced by something other than a sum.

**Problem.** A chase crew rides from the top-left square to the bottom-right square of a grid of heights, moving one square up, down, left or right at a time. The effort of a ride is the largest absolute height difference between two consecutive squares on it, and the crew wants the ride of least effort. Return that least effort as an `int`; a grid of one square has effort 0. The grid is not changed.

**Constraints.** 1 <= rows, cols <= 5 and 1 <= heights[r][c] <= 1,000,000.

**Example 1.** Input `heights = [[3,3,3],[3,9,3],[3,3,3]]`, output `0`.

**Example 2.** Input `heights = [[4,9,3],[6,8,2],[1,8,5]]`, output `3`.

**Hint.** Is the cheapest ride in Example 2 the one with the smallest total of differences, and what should an offer be when the route is extended by one more step?

**Changed decision.** An offer for the next square is the larger of the route's effort so far and the new step, instead of their sum, while the heap order and the stale test stay the same.

#### [Boundary] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sh-fewest-cheapest -->

**Prerequisites.** The Vary rung and the Constrained Flights lesson, where the number of flights used was a layer.

**Problem.** Airstrips are numbered 0 to n - 1 and `flights[i] = {from, to, price}` is a one-way flight. Fly from `src` to `dst` using at most `k` intermediate stops, that is at most k + 1 flights. Return a `long[]` of the cheapest total price and the fewest flights among routes with that price, or `{-1, -1}` if no route fits. The array `flights` is not changed.

**Constraints.** 2 <= n <= 6, 0 <= flights.length <= 14, 0 <= price <= 1,000,000,000, `src` differs from `dst`, and 0 <= k <= 4. Parallel flights and repeated airstrips on a route are allowed.

**Example 1.** Input `n = 5`, `flights = [[0,1,2],[1,2,2],[2,4,2],[0,3,3],[3,4,9],[0,2,7]]`, `src = 0`, `dst = 4`, `k = 2`, output `[6, 3]`.

**Example 2.** Input `n = 4`, `flights = [[0,1,4],[1,3,4],[0,2,2],[2,3,6],[0,3,8]]`, `src = 0`, `dst = 3`, `k = 1`, output `[8, 1]`.

**Hint.** If strip 2 is first reached cheaply with all flights used, can a dearer arrival with fewer flights be thrown away, and which of the two equal-price routes in Example 2 should win?

**Changed decision.** The table and the heap are keyed by strip and flights used, instead of by strip alone, and the heap breaks cost ties by flights used so that the first arrival at `dst` is the answer.

#### [Recognize] Path with Maximum Probability (LeetCode 1514)
<!-- id: sh-max-probability -->

**Prerequisites.** The Vary rung, and the idea of reversing the heap order.

**Problem.** Weather beacons are numbered 0 to n - 1, and `edges[i] = {a, b}` joins two beacons by a two-way link that delivers a reading with probability `succProb[i]`, independently of the other links. Return the largest probability that a reading sent from `start` reaches `end` along one route, which is the product of the link probabilities, or 0.0 if the beacons are not connected. The heap must release the most probable entry first. The search compares doubles exactly and uses no tolerance; only the checks of a test compare with a small tolerance. Inputs are not changed.

**Constraints.** 2 <= n <= 7, 0 <= edges.length <= 10, `start` differs from `end`, and every probability is a multiple of 0.01 from 0.00 to 1.00. Parallel links are allowed.

**Example 1.** Input `n = 4`, `edges = [[0,1],[1,2],[0,2],[2,3]]`, `succProb = [0.5,0.5,0.2,0.9]`, `start = 0`, `end = 3`, output `0.225`.

**Example 2.** Input `n = 5`, `edges = [[0,1],[1,2],[2,4],[0,3],[3,4]]`, `succProb = [0.9,0.9,0.9,0.7,1.0]`, `start = 0`, `end = 4`, output `0.729`.

**Hint.** Which of the two routes in Example 2 has fewer links, and why can the product of a longer chain still win?

**Changed decision.** Offers are multiplied and the largest is preferred, instead of adding and preferring the smallest, and the stale test keeps an entry only when it equals the best probability recorded for its beacon.
