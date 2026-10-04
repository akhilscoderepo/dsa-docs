<!-- lesson-kind: standard -->
<!-- lesson-id: constrained-flights -->
## Constrained Flights

<!-- stage: context -->
### A Crate Of Pump Parts, Three Landings

Odile Brandt flies a twin-prop freighter for the Skerry Cargo Co-op, and this week she has one job: a crate of replacement pump parts has to get from Harrow Strip to the fish plant at Tern Island before the plant's cooling system gives out. The co-op's booking sheet numbers its airfields from 0 upward, and every scheduled hop between two airfields has a landing and handling fee printed next to it. Hops are one way, and some pairs of airfields are linked by no direct hop at all.

The insurance policy on the crate adds a rule. Every time the crate is lifted out of the hold and put back in, the claim risk grows, so the insurer allows at most three stopovers between Harrow Strip and Tern Island. Odile wants the smallest total of fees over all routes that obey that cap, and she wants a method that still works when the sheet grows to a hundred airfields or the insurer changes the cap.

<!-- stage: naive -->
### Try Every Route Under The Cap

The direct approach tries every route. From the current airfield it looks at each hop that leaves it, pays that hop's fee, and continues from the airfield it lands on with one fewer hop allowed. When the hops allowed reach zero, the route stops, and the cheapest route that arrived at the destination wins. A stopover cap of k means at most k + 1 hops, because the first and last airfields are not stopovers.

```java
static long cheapest(int at, int dst, int[][] flights, int hopsLeft) {
    if (at == dst) return 0;
    if (hopsLeft == 0) return Long.MAX_VALUE / 4;
    long best = Long.MAX_VALUE / 4;
    for (int[] f : flights) {
        if (f[0] != at) continue;
        best = Math.min(best, f[2] + cheapest(f[1], dst, flights, hopsLeft - 1));
    }
    return best;
}

static int cheapestWithin(int[][] flights, int src, int dst, int k) {
    long best = cheapest(src, dst, flights, k + 1);
    return best >= Long.MAX_VALUE / 4 ? -1 : (int) best;
}
```

This is correct. Every legal route is a sequence of at most k + 1 hops, the recursion visits every such sequence, and a route that loops back to an airfield it already used only costs more fees without breaking anything. It is simple, and it is slow in a way that grows with the cap.

<!-- stage: bottleneck -->
### The Same Airfield At The Same Count

Say each airfield has d outgoing hops. Then the recursion makes about d^(k+1) calls, and each call also scans the whole list of F hops to find the ones leaving `at`, so the total is O(F * d^(k+1)). With ten hops out of every airfield and a cap of five stopovers, that is a million routes before the scanning cost is even counted, and the sheet for a hundred airfields makes it far worse.

Most of that work is repeated. Two different routes can both land at airfield 7 after exactly two hops, perhaps by different fees, and from there the rest of the trip depends only on the airfield and on how many hops remain. The recursion explores everything that follows airfield 7 once for each way of arriving, even though only the cheaper arrival can ever be part of a cheapest route. There are only n airfields and k + 2 possible hop counts, so the number of genuinely different situations is about n * (k + 2), not d^(k+1). A method that remembers the cheapest fee for each airfield at each hop count would pay for each situation once.

<!-- stage: insight -->
### One Price Table Per Number Of Hops

Start by turning the insurer's wording into arithmetic. A cap of k stopovers is the same as a **leg limit** of k + 1 flights, since every flight but the last ends at a stopover. Everything below counts flights, and only the last line of the method converts back from stops.

Now keep one row of prices for each number of flights used so far. Row r is a **leg layer**: for every airfield, the cheapest total fee to reach it using at most r flights, or a marker for none. Row 0 is trivial, because only the start is reachable and it costs nothing. Row r + 1 is computed from row r alone. Begin with a copy of row r, since having a route of r flights is also fine under a limit of r + 1, then look at every flight from airfield u to airfield v with fee w and offer `row r[u] + w` as a price for v.

The detail that decides correctness is where those offers read from. They must read from a frozen **snapshot** of row r, never from the row that is being filled in. If an offer could read a price that was only just improved in the same pass, a route could silently take two flights while the table believes it took one, and the leg limit would leak. A copy made at the start of each pass, with reads from the old array and writes to the new one, closes that hole.

After k + 1 passes, the entry for the destination is the answer. The invariant is that row r always holds the exact best price among routes of at most r flights.

<!-- names: leg limit, leg layer, snapshot -->

<!-- stage: variables -->
### Prices, Passes And The None Marker

The array `flights` holds one `{from, to, fee}` triple per hop, `src` and `dst` are the two ends of the trip, and `k` is the number of stopovers the insurer allows. The array `best` is the current row of prices indexed by airfield, and `next` is the row under construction, created as a copy of `best` at the start of every pass. The constant `NONE` marks an airfield not yet reachable within the flights counted so far, and it is a large `long` so that adding a fee to it cannot wrap around. The loop counter `leg` counts passes, and a loop that runs for `leg` from 0 through `k` makes exactly k + 1 of them.

<!-- stage: trace -->
### Two Runs Of The Price Table

The first trace is a graph with four airfields and five hops, run with k = 1 so that two passes are allowed. The cells are the hops in the order the sheet lists them, and the pointer `f` is the hop being offered. The vars show the pass number, the price at the departure airfield in the frozen row, the price that hop offers and the price now stored at the arrival airfield. The hops 0 to 1, 1 to 2 and 2 to 3 would make a three-hop route costing 300 if passes could reuse each other's work, but the snapshot stops that: in pass 1 the hop from 1 finds no price at airfield 1 in the old row, so nothing leaks, and the destination ends at 600 by way of 0 to 2 and then 2 to 3.

```trace
{"cells":["0>1 100","1>2 100","2>3 100","0>2 500","1>3 600"],"pointers":["f"],"steps":[{"at":{"f":0},"vars":{"pass":1,"frozen":0,"offer":100,"stored":100},"note":"Pass 1, hop 0 to 1: the frozen price at 0 is 0, so the offer is 100; it beats the stored value and airfield 1 now holds 100."},{"at":{"f":1},"vars":{"pass":1,"frozen":"none","offer":"none","stored":"none"},"note":"Pass 1, hop 1 to 2: airfield 1 has no price in the frozen row, so nothing is offered."},{"at":{"f":2},"vars":{"pass":1,"frozen":"none","offer":"none","stored":"none"},"note":"Pass 1, hop 2 to 3: airfield 2 has no price in the frozen row, so nothing is offered."},{"at":{"f":3},"vars":{"pass":1,"frozen":0,"offer":500,"stored":500},"note":"Pass 1, hop 0 to 2: the frozen price at 0 is 0, so the offer is 500; it beats the stored value and airfield 2 now holds 500."},{"at":{"f":4},"vars":{"pass":1,"frozen":"none","offer":"none","stored":"none"},"note":"Pass 1, hop 1 to 3: airfield 1 has no price in the frozen row, so nothing is offered."},{"at":{"f":0},"vars":{"pass":2,"frozen":0,"offer":100,"stored":100},"note":"Pass 2, hop 0 to 1: the frozen price at 0 is 0, so the offer is 100; airfield 1 already holds 100, so it stays."},{"at":{"f":1},"vars":{"pass":2,"frozen":100,"offer":200,"stored":200},"note":"Pass 2, hop 1 to 2: the frozen price at 1 is 100, so the offer is 200; it beats the stored value and airfield 2 now holds 200."},{"at":{"f":2},"vars":{"pass":2,"frozen":500,"offer":600,"stored":600},"note":"Pass 2, hop 2 to 3: the frozen price at 2 is 500, so the offer is 600; it beats the stored value and airfield 3 now holds 600."},{"at":{"f":3},"vars":{"pass":2,"frozen":0,"offer":500,"stored":200},"note":"Pass 2, hop 0 to 2: the frozen price at 0 is 0, so the offer is 500; airfield 2 already holds 200, so it stays."},{"at":{"f":4},"vars":{"pass":2,"frozen":100,"offer":700,"stored":600},"note":"Pass 2, hop 1 to 3: the frozen price at 1 is 100, so the offer is 700; airfield 3 already holds 600, so it stays."}]}
```

The second trace is smaller and shows the rows themselves. The cells are the three rows for zero, one and two flights, the pointer `r` is the row just finished, and the vars give the stored prices for airfield 2 and for the destination, airfield 3. Airfield 2 holds 50 after one flight and 20 after two, so a single price per airfield would have to throw one of them away. The cheaper value of 20 is no use to a trip that must end within two flights, because the last hop would be a third, while the dearer 50 is exactly what the answer of 60 is built from. This is the arrival that a plain shortest-path method discards.

```trace
{"cells":["row 0","row 1","row 2"],"pointers":["r"],"steps":[{"at":{"r":0},"vars":{"airfield2":"none","airfield3":"none"},"note":"Row for no flights: airfield 2 costs none and the destination costs none."},{"at":{"r":1},"vars":{"airfield2":50,"airfield3":"none"},"note":"Row for one flight: airfield 2 costs 50 and the destination costs none."},{"at":{"r":2},"vars":{"airfield2":20,"airfield3":60},"note":"Row for two flights: airfield 2 costs 20 and the destination costs 60."}]}
```

<!-- stage: code -->
### Passes Over The Flight List

```java
static int cheapestWithin(int n, int[][] flights, int src, int dst, int k) {
    final long NONE = Long.MAX_VALUE / 4;
    long[] best = new long[n];
    Arrays.fill(best, NONE);
    best[src] = 0;
    for (int leg = 0; leg <= k; leg++) {
        long[] next = best.clone();
        for (int[] f : flights) {
            if (best[f[0]] == NONE) continue;
            long offer = best[f[0]] + f[2];
            if (offer < next[f[1]]) next[f[1]] = offer;
        }
        best = next;
    }
    return best[dst] == NONE ? -1 : (int) best[dst];
}
```

The test on `best[f[0]]` skips hops that leave an airfield nobody has reached, and reads always go to `best` while writes go to `next`. The cost is O((k + 1) * (n + F)) time, one copy and one scan per pass, and O(n) memory because only two rows exist at once. The final cast to `int` is safe when fees are modest and a route has at most n hops, which holds for the usual limits.

<!-- stage: applicability -->
### When A Count Limits The Route

Think of this pattern when a cheapest route is limited by a count of edges: stops, transfers, border crossings, relay hops. The recognition cue is that a cheaper arrival may still be worse, because it has used up more of the allowance than a dearer one. The invariant to guard is that row r means "at most r flights" and is built only from row r - 1, so the cap is never exceeded by a pass that read its own fresh writes.

The false friend is the ordinary shortest-path routine with a single best price per airfield. It marks airfield 2 as settled at 20 after two flights, refuses the arrival at 50 after one flight as not an improvement, and then finds that the 20 has no flight left to continue with. The correct answer was hiding in the discarded arrival. A heap-based search can be repaired by adding the flights used to its state, and the combination lesson on graph and heap returns to that version, but it is not the tool for this lesson.

Do not use layers when the cap is at least n - 1, because then a cheapest route never needs to repeat an airfield and a plain Dijkstra run is cheaper. Also avoid them when the limit is on a second quantity, such as total travel time, since a count of rows no longer captures it. In Java, filling a `long` array with `Long.MAX_VALUE` and adding a fee wraps to a large negative number, and doing the same with `int` breaks the same way. Calling `clone()` on a two-dimensional array copies only the outer array, so the rows are shared and a layered table built that way overwrites itself.

<!-- stage: exercises -->
### Exercises

#### [Build] At Most Two Edges (Author exercise)
<!-- id: sp-two-edges -->

**Prerequisites.** The leg layer idea from this lesson, and the copy-then-relax pass from the code stage.

**Problem.** Airfields are numbered 0 to n - 1, and `flights` is an `int[][]` of `{from, to, fee}` triples, each a one-way hop. Return the smallest total fee of a route from `src` to `dst` that uses one or two flights, or -1 if no such route exists. Build the answer as exactly two passes over the flight list, where the second pass reads only prices stored by the first. The input arrays are not modified.

**Constraints.** 2 <= n <= 50, 0 <= flights.length <= 200, 0 <= fee <= 10,000, and `src` differs from `dst`. Several flights may link the same pair.

**Example 1.** Input `n = 4, flights = [[0,1,100],[1,2,100],[2,3,100],[0,2,500]], src = 0, dst = 3`, output `600`.

**Example 2.** Input `n = 5, flights = [[0,1,10],[1,2,10],[2,3,10],[3,4,10]], src = 0, dst = 4`, output `-1`.

**Hint.** What would the second pass do wrong if it were allowed to read the price that the first pass had just written for the same airfield?

**Changed decision.** Prices for two flights are computed from a frozen copy of the prices for one flight, instead of updating a single array in place.

#### [Vary] Cost By Stops Used (Author exercise)
<!-- id: sp-cost-by-legs -->

**Prerequisites.** The At Most Two Edges rung, and the idea that row r holds the best price using at most r flights.

**Problem.** With the same flight list as before, and a given `maxLegs`, return an `int[]` of length `maxLegs + 1` whose entry j is the cheapest fee from `src` to `dst` using at most j flights, or -1 when no such route exists. Entry 0 is -1 because `src` differs from `dst`. Keep one stored price for every airfield and every number of flights, so that the whole table is available at the end. Nothing in the input is modified.

**Constraints.** 2 <= n <= 40, 0 <= flights.length <= 150, 0 <= fee <= 10,000, 0 <= maxLegs <= 12, and `src` differs from `dst`.

**Example 1.** Input `n = 4, flights = [[0,1,100],[1,2,100],[2,3,100],[0,2,500]], src = 0, dst = 3, maxLegs = 3`, output `[-1,-1,600,300]`.

**Example 2.** Input `n = 3, flights = [[0,1,2],[1,2,3],[0,2,9]], src = 0, dst = 2, maxLegs = 2`, output `[-1,9,5]`.

**Hint.** Which earlier row must a new row start as a copy of, and why does that make the entries never go up as j grows?

**Changed decision.** The whole table of rows is kept and reported, instead of discarding every row but the latest.

#### [Boundary] Direct Flight And K Zero (Author exercise)
<!-- id: sp-direct-k-zero -->

**Prerequisites.** The Cost By Stops Used rung, and the rule that k stopovers allow k + 1 flights.

**Problem.** Given `k`, the number of intermediate stopovers allowed, return the cheapest fee from `src` to `dst` over routes with at most k + 1 flights. This time `src` may equal `dst`, in which case the empty route costs 0 and is the answer. When k is 0 only a single direct flight qualifies, and if several direct flights link the pair the cheapest of them counts. Return -1 when no route fits. The input is not modified.

**Constraints.** 1 <= n <= 30, 0 <= flights.length <= 120, 0 <= fee <= 10,000, and 0 <= k <= 40. The value k may exceed n.

**Example 1.** Input `n = 3, flights = [[0,1,80],[0,1,60],[1,2,10],[0,2,200]], src = 0, dst = 2, k = 0`, output `200`.

**Example 2.** Input `n = 2, flights = [[1,0,5],[0,1,5]], src = 1, dst = 1, k = 2`, output `0`.

**Hint.** What is the price of the start in row 0, and does the first pass over the flights still have to run when `k` is 0?

**Changed decision.** The number of passes is k + 1 with the start already priced at zero, instead of assuming the destination differs from the start.

#### [Recognize] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sp-cheapest-k-stops -->

**Prerequisites.** The Direct Flight And K Zero rung, and the false friend named in this lesson.

**Problem.** There are `n` cities numbered 0 to n - 1 and a list `flights` of `{from, to, price}` one-way flights. Return the cheapest total price of a trip from `src` to `dst` that makes at most `k` stops in between, or -1 if there is no such trip. A stop is a city entered and left again, so the trip may use up to k + 1 flights. The array is not modified.

**Constraints.** 2 <= n <= 100, 0 <= flights.length <= n * (n - 1) / 2, 1 <= price <= 10,000, `src` differs from `dst`, and 0 <= k < n. Cities are numbered from 0 here.

**Example 1.** Input `n = 5, flights = [[0,1,30],[1,2,30],[2,3,30],[3,4,30],[0,2,100],[2,4,100]], src = 0, dst = 4, k = 1`, output `200`.

**Example 2.** Input `n = 5, flights = [[0,1,30],[1,2,30],[2,3,30],[3,4,30],[0,2,100],[2,4,100]], src = 0, dst = 4, k = 3`, output `120`.

**Hint.** Which arrival at an intermediate city could a one-price-per-city search discard, and what extra fact must be stored beside the city?

**Changed decision.** The cheapest price is stored for each city and each number of flights, instead of one price per city regardless of how it was reached.
