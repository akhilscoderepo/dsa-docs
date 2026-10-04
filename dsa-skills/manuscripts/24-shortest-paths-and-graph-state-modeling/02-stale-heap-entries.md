<!-- lesson-kind: standard -->
<!-- lesson-id: stale-heap-entries -->
## Stale Heap Entries

<!-- stage: context -->
### Slips In The Dispatch Tray

Tamsin runs the dispatch desk at the Orrin Wharf post office, and this morning a recall notice has to reach every sorting depot in the region. Depots are joined by one-way van routes, and each route takes a known whole number of hours. Tamsin keeps a wooden tray on her desk. Every slip in it reads "depot, hour", meaning the notice could arrive at that depot at that hour. She always lifts the slip with the earliest hour, and when two slips share an hour she takes the lower depot number.

Trouble starts when a quicker route to a depot turns up after a slip for it is already in the tray. A new slip is easy to drop on top, but the old one is buried somewhere under the others, and digging through the tray for it takes longer than reading the slips. Tamsin wants to know the hour at which the last depot hears the notice, or that some depot never will, and she wants a method that does not slow down as the tray fills.

<!-- stage: naive -->
### Dig Out The Old Slip

The tidy idea is to keep exactly one slip per depot. Whenever a quicker route is found, Tamsin digs out the old slip for that depot, throws it away and drops in the new one. In Java the tray is a `PriorityQueue` and the digging is its `remove(Object)` method.

```java
final class NaiveDelay {
    record Slip(int depot, long hour) {}

    static long delay(int n, int[][] roads, int source) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] r : roads) out.get(r[0]).add(new int[] {r[1], r[2]});
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[source] = 0;
        PriorityQueue<Slip> tray = new PriorityQueue<>(
                Comparator.comparingLong(Slip::hour).thenComparingInt(Slip::depot));
        tray.add(new Slip(source, 0));
        while (!tray.isEmpty()) {
            Slip top = tray.poll();
            for (int[] r : out.get(top.depot())) {
                long cand = top.hour() + r[1];
                if (cand >= best[r[0]]) continue;
                if (best[r[0]] != Long.MAX_VALUE) tray.remove(new Slip(r[0], best[r[0]]));
                best[r[0]] = cand;
                tray.add(new Slip(r[0], cand));
            }
        }
        long worst = 0;
        for (long b : best) {
            if (b == Long.MAX_VALUE) return -1;
            worst = Math.max(worst, b);
        }
        return worst;
    }
}
```

The answer is right: the tray never holds two slips for one depot, so every slip that is read is current. It is a correct method that pays for the digging on every improvement.

<!-- stage: bottleneck -->
### Digging Costs A Whole Tray

A binary heap can hand over its smallest item in O(log m) time, but it has no index from an item to its position. So `remove(Object)` starts at the front of the underlying array and asks each slot whether it equals the item until one says yes. That scan is O(m) for a tray of m slips, and only after it finds the slot does the cheap O(log m) repair run. With V depots the tray holds up to V slips, and each of the E roads can trigger one removal, so the digging adds up to O(E * V) comparisons, against the O(E log V) that the heap was supposed to give.

The repeated work is the search for a slip we could have recognised later at no cost. The old slip is never read in any useful way; it only has to stop being believed. Every scan re-examines slots that an earlier scan already walked past, in a structure where the answer to "where is it?" is never remembered. A rule that leaves the old slip alone, and lets the desk check each slip against a single board of current best hours at the moment it is lifted, replaces the scan with one array lookup per slip.

<!-- stage: insight -->
### Believe The Board, Not The Tray

Stop trying to remove anything. Keep one array, `best`, holding the earliest hour known for each depot, and treat it as the only source of truth. When a road offers a strictly smaller hour, write it into the array and drop a second slip into the tray. The first slip is now a **stale entry**: a queued pair whose stored hour no longer equals the board's value for its depot. It is harmless as long as it is never believed.

The check happens at the other end. When a slip comes off the tray, compare its hour with the board. If they differ, the slip is stale and is thrown away without looking at any road from that depot. If they match, this is the one true slip for the depot, and its roads are expanded. Postponing the cleanup until an entry is lifted is called **lazy deletion**, and it turns the O(m) dig into an O(1) comparison.

Because a heap may hold equal hours, the order of equal slips must be written down: a **tie rule**. Here the lower depot number goes first. The rule does not change any distance, but it fixes the exact sequence of pushes and therefore how many stale slips are lifted, which is why the contract below can ask for that count.

The invariant: for each reachable depot, exactly one slip carrying the hour `best[depot]` is either waiting in the tray or already read, every other slip for that depot carries a larger hour, and a slip is expanded only when its hour equals the board.

<!-- names: stale entry, lazy deletion, tie rule -->

<!-- stage: variables -->
### Board, Tray And Skip Count

The array `best` is the board: one `long` per depot, starting at the largest long value to mean "not reached", and `best[source]` is 0. The `tray` is the priority queue of `long[]` slips holding `{hour, depot}`, ordered by hour and then by depot. The variable `top` is the slip just taken out, and `u` is its depot. The counter `skipped` goes up by one each time `top[0]` differs from `best[u]`. For each road, `cand` is the offered hour, and it is stored and queued only when it is strictly below `best[v]`, which changes `best` and grows the tray at the same moment, never one without the other.

<!-- stage: trace -->
### Two Trays Read Slip By Slip

The first trace uses five depots and the roads 0 to 1 in 7 hours, 0 to 2 in 2, 2 to 1 in 3, 1 to 3 in 1, 2 to 3 in 9 and 3 to 4 in 2. The cells are the slips in the order they come off the tray, written depot-at-hour, and the pointer `cur` is the position being read. The vars show the board value for that depot, the number of skips so far and how many slips are still waiting. Depot 1 gets two slips, 1@7 from the direct road and 1@5 by way of depot 2, and the later and smaller one comes off first, which leaves 1@7 behind as a stale entry. Depot 3 is in the same position with 3@11. Both are discarded when lifted, and the delay is 8.

```trace
{"cells":["0@0","2@2","1@5","3@6","1@7","4@8","3@11"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"board":0,"skipped":0,"tray":2},"note":"Slip 0@0 matches the board and is expanded; it writes 1@7, 2@2."},{"at":{"cur":1},"vars":{"board":2,"skipped":0,"tray":3},"note":"Slip 2@2 matches the board and is expanded; it writes 1@5, 3@11."},{"at":{"cur":2},"vars":{"board":5,"skipped":0,"tray":3},"note":"Slip 1@5 matches the board and is expanded; it writes 3@6."},{"at":{"cur":3},"vars":{"board":6,"skipped":0,"tray":3},"note":"Slip 3@6 matches the board and is expanded; it writes 4@8."},{"at":{"cur":4},"vars":{"board":5,"skipped":1,"tray":2},"note":"Slip 1@7 comes off the tray, but the board shows depot 1 at 5, so it is skipped without reading its roads."},{"at":{"cur":5},"vars":{"board":8,"skipped":1,"tray":1},"note":"Slip 4@8 matches the board and is expanded; no neighbor improves."},{"at":{"cur":6},"vars":{"board":6,"skipped":2,"tray":0},"note":"Slip 3@11 comes off the tray, but the board shows depot 3 at 6, so it is skipped without reading its roads."}]}
```

The second trace is a different graph on six depots, with equal hours and a zero-hour road, and depot 5 has no route into it. The cells are again the lifted slips. Ties show up at hour 1, where depots 2 and 3 are lifted in that order under the tie rule, and an offer that merely equals the board is never queued, so depot 2's offers to 3 and 1 change nothing. The late discovery of 1@1 through the zero-hour road leaves 1@4 stale, and depot 4 leaves 4@6 stale after 4@3 is found. Because depot 5 is never reached, the answer is -1 even though two slips were skipped.

```trace
{"cells":["0@0","2@1","3@1","1@1","4@3","1@4","4@6"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"board":0,"skipped":0,"tray":3},"note":"Slip 0@0 matches the board and is expanded; it writes 1@4, 2@1, 3@1."},{"at":{"cur":1},"vars":{"board":1,"skipped":0,"tray":2},"note":"Slip 2@1 matches the board and is expanded; no neighbor improves."},{"at":{"cur":2},"vars":{"board":1,"skipped":0,"tray":3},"note":"Slip 3@1 matches the board and is expanded; it writes 1@1, 4@6."},{"at":{"cur":3},"vars":{"board":1,"skipped":0,"tray":3},"note":"Slip 1@1 matches the board and is expanded; it writes 4@3."},{"at":{"cur":4},"vars":{"board":3,"skipped":0,"tray":2},"note":"Slip 4@3 matches the board and is expanded; no neighbor improves."},{"at":{"cur":5},"vars":{"board":1,"skipped":1,"tray":1},"note":"Slip 1@4 comes off the tray, but the board shows depot 1 at 1, so it is skipped without reading its roads."},{"at":{"cur":6},"vars":{"board":3,"skipped":2,"tray":0},"note":"Slip 4@6 comes off the tray, but the board shows depot 4 at 3, so it is skipped without reading its roads."}]}
```

<!-- stage: code -->
### Heap Search With Lazy Deletion

```java
final class Desk {
    static int[] delayAndSkips(int n, int[][] roads, int source) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] r : roads) out.get(r[0]).add(new int[] {r[1], r[2]});
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[source] = 0;
        PriorityQueue<long[]> tray = new PriorityQueue<>((a, b) ->
                a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        tray.add(new long[] {0, source});
        int skipped = 0;
        while (!tray.isEmpty()) {
            long[] top = tray.poll();
            int u = (int) top[1];
            if (top[0] != best[u]) {
                skipped++;
                continue;
            }
            for (int[] r : out.get(u)) {
                long cand = top[0] + r[1];
                if (cand < best[r[0]]) {
                    best[r[0]] = cand;
                    tray.add(new long[] {cand, r[0]});
                }
            }
        }
        long worst = 0;
        for (long b : best) {
            if (b == Long.MAX_VALUE) return new int[] {-1, skipped};
            worst = Math.max(worst, b);
        }
        return new int[] {(int) worst, skipped};
    }
}
```

The comparison inside the comparator uses `Long.compare`, so no subtraction can overflow. Every successful offer adds one slip, so the tray receives at most E + 1 slips over the whole run and each costs O(log E) to insert and to lift. Time is O((V + E) log E) and space is O(V + E) for the adjacency lists and the tray. The skip test is placed before the road loop on purpose, since expanding a stale slip would repeat every road check from its depot.

<!-- stage: applicability -->
### When The Heap Cannot Decrease

Use this whenever a priority queue has no operation to lower an item's priority and the same key can be improved several times: shortest paths over a graph, a scheduler where jobs are re-rated, a merge of streams where a source can offer a better head. The recognition cue is "an item I already queued has just become cheaper". The invariant to defend is that one array holds the current truth and every queued entry is compared with it at the moment it is removed, never trusted blindly.

The false friend is the dig-out-the-old-entry habit: `remove(Object)` looks like decrease-key, is correct, and costs a full scan of the tray each time. A second, nastier version is `remove` on array entries, since arrays compare by identity, so a freshly built `int[]` matches nothing, the call quietly returns false and the old entry stays in the queue unchecked.

Do not rely on this when the weights can be negative, because then a depot finalised early may later be improved and the one-expansion guarantee fails, or when the queue is meant to answer "what is waiting?" by iterating it. In Java, iterating a `PriorityQueue` shows the heap array in storage order, not sorted order, and a comparator written as `(int) (a - b)` on long hours wraps around once the difference passes the int range.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Entries For One Node (Author exercise)
<!-- id: sp-two-entries -->

**Prerequisites.** The relaxation rule from the previous lesson, which keeps an offered hour only when it beats the board.

**Problem.** There are `n` depots, and `proposals` is an `int[][]` of pairs `{depot, hour}` in the order the offers arrive. The board starts empty for every depot, so the first offer for a depot always counts. An offer is written onto a new tray slip only when its hour is strictly smaller than the board's current value for that depot, and it then becomes the board's value. Return an `int[]` of the positions in `proposals`, in increasing order, of the offers that were written to the tray and are stale at the end, meaning their hour is larger than the board's final value for their depot. The input is not modified.

**Constraints.** 1 <= n <= 50, 0 <= proposals.length <= 200, every depot is in 0..n-1 and every hour is between 0 and 1,000,000,000.

**Example 1.** Input `n = 3, proposals = [[1,9],[2,4],[1,6],[1,7],[1,5]]`, output `[0, 2]`.

**Example 2.** Input `n = 2, proposals = [[0,0],[1,5],[1,5],[1,5]]`, output `[]`.

**Hint.** Which offers actually reach the tray, and which of those slips would disagree with the board once every offer has been seen?

**Changed decision.** A slip is never taken out when it is improved on, and it is recognised as old later by comparing it with the board.

#### [Vary] Skip Before Expansion (Author exercise)
<!-- id: sp-skip-before-expansion -->

**Prerequisites.** The Two Entries For One Node rung and the code stage of this lesson.

**Problem.** The `roads` array holds `{from, to, hours}` for one-way routes between depots `0..n-1`, and the notice starts at `source`. Run the tray method with the tie rule of this lesson. When a slip is lifted whose hour differs from the board, discard it before any road is looked at. Return an `int[]` of two values: the number of depots with a final board value, including the source, and the total number of road checks made, where one check is one road tested for one expanded depot. Parallel roads and loops may occur. The `roads` array is not modified.

**Constraints.** 1 <= n <= 60, 0 <= roads.length <= 300, 0 <= hours <= 100, and 0 <= source < n.

**Example 1.** Input `n = 4, roads = [[0,1,5],[0,2,1],[2,1,1],[1,3,2]], source = 0`, output `[4, 4]`.

**Example 2.** Input `n = 5, roads = [[0,1,2],[0,2,1],[2,1,1],[1,3,0],[2,3,5],[4,0,1]], source = 0`, output `[4, 5]`.

**Hint.** If a stale slip were expanded, which roads would be checked a second time, and where in the loop must the comparison with the board sit?

**Changed decision.** The comparison with the board moves from the moment of offering to the moment of lifting, so that every depot's roads are checked exactly once.

#### [Boundary] Equal-Cost Alternatives (Author exercise)
<!-- id: sp-equal-cost-alternatives -->

**Prerequisites.** The Skip Before Expansion rung.

**Problem.** Use the same input format as the previous rung: `n`, `roads` as `{from, to, hours}`, and `source`. Run the tray method with this tie rule: the earliest hour is lifted first, and for equal hours the lower depot number goes first. An offer is queued only when it is strictly smaller than the board, so an offer that equals the board is dropped. Return the number of slips ever put on the tray, counting the starting slip for the source. Zero-hour roads are allowed, and the program must finish on a graph whose zero-hour roads form a loop. The input is not modified.

**Constraints.** 1 <= n <= 60, 0 <= roads.length <= 300, 0 <= hours <= 100, and 0 <= source < n.

**Example 1.** Input `n = 3, roads = [[0,1,2],[0,2,1],[2,1,1]], source = 0`, output `3`.

**Example 2.** Input `n = 3, roads = [[0,1,0],[1,0,0],[1,2,0]], source = 0`, output `3`.

**Hint.** What would happen to the number of slips, and to the number of times a depot is expanded, if an offer equal to the board were also queued?

**Changed decision.** An offer that only ties the board is rejected, instead of being queued as a second equally good slip.

#### [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay-stale -->

**Prerequisites.** The Equal-Cost Alternatives rung, and plain Dijkstra from the previous lesson.

**Problem.** A signal is sent from node `k` through a directed network of `n` nodes. This lesson numbers the nodes `0..n-1`, whereas the original LeetCode statement numbers them `1..n`, so shift every label by one when comparing. Each entry of `times` is `{from, to, travel}`. Return an `int[]` of two values. The first is the time at which the last node receives the signal, or -1 if some node never does. The second is the number of stale heap entries skipped, counted by running a `PriorityQueue` ordered by distance and then by node number, queueing only strictly improving offers, and running until the queue is empty. A popped entry is stale when its distance differs from the node's best known distance. The `times` array is not modified.

**Constraints.** 1 <= n <= 100, 0 <= times.length <= 400, 0 <= travel <= 100, and 0 <= k < n. Self loops and parallel edges are allowed.

**Example 1.** Input `n = 5, times = [[0,1,6],[0,2,3],[2,1,1],[1,3,2],[2,3,7],[3,4,1],[2,4,9]], k = 0`, output `[7, 3]`.

**Example 2.** Input `n = 4, times = [[0,1,4],[1,2,1]], k = 0`, output `[-1, 0]`.

**Hint.** Where does the delay come from in a table that is only ever lowered, and which comparison tells a leftover slip from the live one?

**Changed decision.** The answer carries a second number, so the loop must keep running past the point where all nodes are final and count every leftover it lifts.
