<!-- lesson-kind: combination -->
<!-- lesson-id: graph-and-deque -->
## Graph And Deque

<!-- stage: context -->
### The Plough Of Kestrel Pass

Every winter night Odile Brandt drives the one snowplough of Kestrel Pass out of the depot, and by dawn she has to reach the school in the far hamlet. The valley has a few dozen hamlets joined by single-track lanes. Some lanes were scoured clean by the wind, and she drives along them for nothing. Other lanes lie under drifts, and ploughing through one snaps exactly one shear pin on the blade, however long the lane is. She carries a box of spare pins, and the dispatcher's only question is how few pins the best route to a given hamlet will use.

Odile has tried the tidy approach of listing, for every hamlet, the lowest pin count known so far, and she keeps recomputing the list after every lane she hears about. The dispatcher has a larger valley and a radio full of new reports every hour, and the recomputing no longer finishes before the plough has to leave.

<!-- stage: contributions -->
### What Each Structure Brings

The graph brings transitions with only two prices. Every move from one place to another costs zero or one, so the cost of a whole route is a plain count of the priced moves, and the input already says which moves are free. Nothing more elaborate than that single bit per edge is needed from it.

The deque brings an ordering without a heap. Because it can be entered at both ends, an improvement that costs nothing can be placed ahead of everything waiting, and an improvement that costs one can be placed behind everything waiting, so the entries stay sorted by distance without any comparisons. The edge weight alone chooses the end.

The combination is recognized when a shortest-route question lives on a graph, or on a grid that behaves like one, where the move prices are exactly zero and one, such as following an arrow versus turning it, or stepping on open ground versus breaking an obstacle.

<!-- stage: naive -->
### Sweep Every Lane Until Calm

The direct method keeps a pin count for every hamlet, starts it at infinity except for the depot, and then sweeps through the whole list of lanes again and again. In each sweep, a lane improves its far end whenever the count at its near end plus the lane's price is smaller. The sweeps stop when one entire sweep changes nothing.

```java
static int[] sweepCounts(int n, int[][] lanes, int depot) {
    int inf = Integer.MAX_VALUE / 2;
    int[] pins = new int[n];
    java.util.Arrays.fill(pins, inf);
    pins[depot] = 0;
    boolean changed = true;
    while (changed) {
        changed = false;
        for (int[] lane : lanes) {
            if (pins[lane[0]] + lane[2] < pins[lane[1]]) {
                pins[lane[1]] = pins[lane[0]] + lane[2];
                changed = true;
            }
        }
    }
    return pins;
}
```

This is correct for any lane prices that are not negative, and it terminates because every count only decreases and never goes below the true minimum.

<!-- stage: bottleneck -->
### Many Sweeps Rediscover The Same Counts

A single sweep touches every lane, which is O(E), and the number of sweeps can be as large as the number of hamlets, because a good route may be found one lane per sweep when the lanes are listed in an unlucky order. The method therefore costs O(V * E). For fifty thousand hamlets and two hundred thousand lanes that is ten billion lane checks, almost all of which find nothing to improve. A lane is looked at again and again although the count at its near end has not changed since the last time.

A heap would already cut this to O(E log V), because it expands hamlets in the order of their pin counts and looks at each lane once. That is much better, but it pays a logarithm for sorting prices that can only be 0 or 1, and the heap compares and moves entries around to keep an order that is much simpler than it looks. The target is O(V + E): look at each lane once, and keep the waiting hamlets in order without comparing anything.

<!-- stage: insight -->
### Two Ends Keep The Order

Suppose the hamlets waiting to be expanded are kept in a deque, and the hamlet at the front is always taken next. Each entry is stored with the best pin count known when it was queued. The central claim is the **distance order**: reading the deque from front to back, the counts never decrease, and they take at most two values, some d and d + 1. Both halves of the claim are easy to keep alive. When the hamlet at the front has count d, a free lane gives its neighbour count d, which is no larger than anything waiting, so the neighbour goes to the front. A lane with a toll gives d + 1, which is no smaller than anything waiting, so the neighbour goes to the back. The deque therefore stays sorted by construction, and no comparison is ever made.

Choosing the insertion side from the lane price is the **end rule**, and it is the only place where the weight is used. Everything else is the same relaxation as in the heap version: a hamlet is queued only if the new count is strictly smaller than the stored one, so a lane that does not help is dropped on the spot.

Because the front is always a smallest waiting count, expanding it is the same decision a heap would make, and by the usual argument the count of a hamlet is final when it first comes off the front. A hamlet can be queued twice, once at d + 1 from a toll lane and later at d from a free one, but never a third time, since every later count is at least d. Each lane is therefore expanded a bounded number of times, and the whole search is linear. This works only because the **double-ended frontier** has just two live priorities, and a third price would need more than two ends.

<!-- names: distance order, end rule, double-ended frontier -->

<!-- stage: variables -->
### Counts, Deque And Candidate

The array `dist` holds the best pin count known per place, filled with a large value except for the start, which is 0. The deque `dq` holds place numbers, and for grids it holds a `long` that packs the count into the high half and the place into the low half, so that a leftover entry can be recognised by comparing its count with `dist`. The variable `u` is the place taken from the front, `w` is the price of the move being examined, and `cand` is `dist[u] + w`, the number the move would give its far end. A move is accepted only when `cand` is strictly smaller than `dist[v]`. For grids, a cell number is `row * cols + col`, and the arrow in the cell decides whether a move costs 0 or 1, while in the obstacle grid the value of the entered cell is the price. The counter `zeros` tallies the cells whose final count is 0.

<!-- stage: trace -->
### Free Lanes Jump The Queue

The first trace runs the search on five hamlets with lanes 0 to 1 costing 1, 0 to 2 free, 2 to 1 free, 2 to 3 costing 1 and 3 to 2 free. Hamlet 4 has no lane into it. The pointer `v` marks the hamlet taken from the front. The interesting step is the first one: hamlet 1 is queued at the back with count 1, and the free lane to hamlet 2 then puts it in front, so when hamlet 2 later offers hamlet 1 a free lane, the count of 1 drops to 0 and a second entry is placed at the front. The old entry for 1 is expanded later and changes nothing.

```trace
{"cells":["h0","h1","h2","h3","h4"],"pointers":["v"],"steps":[{"at":{"v":0},"vars":{"count":0,"deque":"[2,1]"},"note":"Hamlet 0 is taken from the front with count 0; lane to 1 gives 1, queued at the back; lane to 2 gives 0, queued at the front."},{"at":{"v":2},"vars":{"count":0,"deque":"[1,1,3]"},"note":"Hamlet 2 is taken from the front with count 0; lane to 1 gives 0 (was 1), queued at the front; lane to 3 gives 1, queued at the back."},{"at":{"v":1},"vars":{"count":0,"deque":"[1,3]"},"note":"Hamlet 1 is taken from the front with count 0; no lane improves anything, so nothing is queued."},{"at":{"v":1},"vars":{"count":0,"deque":"[3]"},"note":"Hamlet 1 is taken from the front with count 0; no lane improves anything, so nothing is queued."},{"at":{"v":3},"vars":{"count":1,"deque":"[]"},"note":"Hamlet 3 is taken from the front with count 1; no lane improves anything, so nothing is queued."}]}
```

The second trace runs the grid version on a three by three board whose cells hold the arrows R, R, D, U, L, L, D, D, R, and the pointer `cell` marks the cell taken from the front. Following an arrow is free and any other direction costs 1. The first six cells taken are all reached for free around the loop of arrows, so six cells have count 0. After them come cells with count 1, and the last cell receives count 1 when the arrow at its upper neighbour is turned downwards.

```trace
{"cells":["R","R","D","U","L","L","D","D","R"],"pointers":["cell"],"steps":[{"at":{"cell":0},"vars":{"count":0,"zeros":1,"waiting":2},"note":"Cell 0 is taken with count 0; cell 1 gets 0, cell 3 gets 1."},{"at":{"cell":1},"vars":{"count":0,"zeros":2,"waiting":3},"note":"Cell 1 is taken with count 0; cell 2 gets 0, cell 4 gets 1."},{"at":{"cell":2},"vars":{"count":0,"zeros":3,"waiting":3},"note":"Cell 2 is taken with count 0; cell 5 gets 0."},{"at":{"cell":5},"vars":{"count":0,"zeros":4,"waiting":4},"note":"Cell 5 is taken with count 0; cell 4 gets 0, cell 8 gets 1."},{"at":{"cell":4},"vars":{"count":0,"zeros":5,"waiting":5},"note":"Cell 4 is taken with count 0; cell 3 gets 0, cell 7 gets 1."},{"at":{"cell":3},"vars":{"count":0,"zeros":6,"waiting":5},"note":"Cell 3 is taken with count 0; cell 6 gets 1."},{"at":{"cell":8},"vars":{"count":1,"zeros":6,"waiting":2},"note":"Cell 8 is taken with count 1; it improves no neighbour."},{"at":{"cell":7},"vars":{"count":1,"zeros":6,"waiting":1},"note":"Cell 7 is taken with count 1; it improves no neighbour."},{"at":{"cell":6},"vars":{"count":1,"zeros":6,"waiting":0},"note":"Cell 6 is taken with count 1; it improves no neighbour."}]}
```

<!-- stage: code -->
### Zero-One Search On Lanes And Arrows

```java
final class PlowSearch {
    static int[] lanesFrom(int n, int[][] lanes, int depot) {
        int[] head = new int[n], nxt = new int[lanes.length];
        java.util.Arrays.fill(head, -1);
        for (int i = 0; i < lanes.length; i++) { nxt[i] = head[lanes[i][0]]; head[lanes[i][0]] = i; }
        int[] dist = new int[n];
        java.util.Arrays.fill(dist, Integer.MAX_VALUE);
        dist[depot] = 0;
        java.util.ArrayDeque<Integer> dq = new java.util.ArrayDeque<>();
        dq.offerFirst(depot);
        while (!dq.isEmpty()) {
            int u = dq.pollFirst();
            for (int i = head[u]; i != -1; i = nxt[i]) {
                int v = lanes[i][1], w = lanes[i][2];
                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    if (w == 0) dq.offerFirst(v); else dq.offerLast(v);
                }
            }
        }
        return dist;
    }

    static int[] arrowSummary(int[][] arrows) {
        int rows = arrows.length, cols = arrows[0].length;
        int[] dist = new int[rows * cols];
        java.util.Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        java.util.ArrayDeque<Long> dq = new java.util.ArrayDeque<>();
        dq.offerFirst(0L);
        int[] dr = {0, 0, 1, -1}, dc = {1, -1, 0, 0};
        while (!dq.isEmpty()) {
            long entry = dq.pollFirst();
            int cost = (int) (entry >>> 32), cell = (int) entry;
            if (cost > dist[cell]) continue;
            for (int k = 0; k < 4; k++) {
                int nr = cell / cols + dr[k], nc = cell % cols + dc[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int w = arrows[cell / cols][cell % cols] == k + 1 ? 0 : 1;
                int to = nr * cols + nc;
                if (cost + w < dist[to]) {
                    dist[to] = cost + w;
                    long packed = ((long) dist[to] << 32) | to;
                    if (w == 0) dq.offerFirst(packed); else dq.offerLast(packed);
                }
            }
        }
        int zeros = 0;
        for (int d : dist) if (d == 0) zeros++;
        return new int[] {dist[rows * cols - 1], zeros};
    }
}
```

The lane search stores the lanes in arrays and runs in O(V + E). The arrow search touches each cell and its four neighbours a bounded number of times, so it takes O(R * C) time and memory.

<!-- stage: applicability -->
### Prices Of Zero Or One Only

Reach for this pairing when every move in a search costs 0 or 1 and the question asks for the cheapest total: crossing a board by breaking as few walls as possible, repairing as few arrows as possible, or switching as few lines as possible on a transit map where staying on a line is free. The invariant is that the deque is sorted by count with at most two distinct values, which is why taking the front is always taking a minimum.

The first false friend is ordinary breadth-first search, which counts edges and marks a place as done when it is first seen. On a graph where a toll lane reaches a place before a chain of free lanes does, it fixes the wrong count, and it is wrong for a reason that no amount of care in the loop can repair. The second is Dijkstra with a heap, which gives correct answers and merely pays a logarithm that the two-ended queue avoids.

A no-go condition is any price outside 0 and 1. A lane that costs 2, or a different cost per lane such as its length, breaks the two-value claim, and the search then needs the heap of the first lesson of this chapter. Negative prices break even that and belong to Chapter 25. In Java, `ArrayDeque` rejects `null`, so a place number must be a real value, and `push` puts at the front while `offer` and `add` put at the back, so mixing them by habit sends a toll lane to the wrong end without any error message.

<!-- stage: exercises -->
### Exercises

#### [Build] Zero-One Relaxation (Author exercise)
<!-- id: sd-zero-one-relaxation -->

**Prerequisites.** The Zero-One BFS lesson and the deque basics of Chapter 13.

**Problem.** A directed graph has `n` vertices labelled from 0 to `n - 1`, and each edge is `{from, to, weight}` with weight 0 or 1. Return an array that gives, for every vertex, the smallest total weight of a path that starts at vertex 0, or -1 for a vertex that cannot be reached. A path of no edges has weight 0.

**Constraints.** 1 <= n <= 100000, 0 <= edges.length <= 200000, and edges may repeat, form cycles or loop back to the same vertex.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,1,0],[2,3,1],[3,2,0]]`, output `[0, 0, 0, 1, -1]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,0],[1,0,0]]`, output `[0, 0, -1, -1]`.

**Hint.** Vertex 1 in the first example is queued with a worse number first. What must the loop check before it queues a vertex, and which end does a free edge use?

**Changed decision.** A free improvement goes to the front and a priced improvement goes to the back, and a vertex is queued only when its number becomes strictly smaller.

#### [Vary] Minimum Cost to Make at Least One Valid Path in a Grid (LeetCode 1368)
<!-- id: sd-valid-path-zero-cells -->

**Prerequisites.** The Build rung and the cell numbering `row * cols + col`.

**Problem.** Each cell of a grid holds an arrow, 1 for right, 2 for left, 3 for down and 4 for up. Starting at the top-left cell, a move in the direction of the arrow in the current cell is free, and a move in any other direction costs 1, which stands for turning that arrow. Moves that leave the grid are not allowed. Return `[a, b]`, where `a` is the minimum total cost to reach the bottom-right cell and `b` is the number of cells whose own cheapest cost from the top-left cell is exactly 0, counting the start.

**Constraints.** 1 <= rows, cols <= 100, and every value is between 1 and 4.

**Example 1.** Input `grid = [[1,1,3],[4,2,2],[3,3,1]]`, output `[1, 6]`.

**Example 2.** Input `grid = [[2,2,2],[2,2,2]]`, output `[3, 1]`.

**Hint.** Is the cost of the move decided by the cell you leave or the cell you enter, and what happens to a cell that was first reached at cost 1?

**Changed decision.** The search must keep a cost for every cell and report how many of them stay at 0, so a cell first reached through a turned arrow can still be improved to a free arrival.

#### [Boundary] Minimum Obstacle Removal to Reach Corner (LeetCode 2290)
<!-- id: sd-obstacle-removal -->

**Prerequisites.** The Vary rung and the free-front, priced-back rule.

**Problem.** A grid holds 0 for an empty cell and 1 for an obstacle. From a cell you may step up, down, left or right, and entering an obstacle costs one removal while entering an empty cell costs nothing. The top-left and bottom-right cells are empty. Return the minimum number of removals needed to walk from the top-left cell to the bottom-right cell.

**Constraints.** 1 <= rows * cols <= 100000, every value is 0 or 1, and both corner cells are 0.

**Example 1.** Input `grid = [[0,1,1],[1,1,0],[1,1,0]]`, output `2`.

**Example 2.** Input `grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]`, output `0`.

**Hint.** Which cell is charged for a step, and what number does the start cell begin with when the grid has only one cell?

**Changed decision.** The price belongs to the cell being entered and never to the start cell, so a grid of one cell or a clear corridor answers 0 without any priced move.

#### [Recognize] Minimum Zero-One Toll (Author exercise)
<!-- id: sd-minimum-toll -->

**Prerequisites.** The Boundary rung and the no-go condition for other weights.

**Problem.** A road map has `n` junctions labelled from 0 to `n - 1`, and each road is `{a, b, toll}` that can be driven in either direction, with a toll of 0 or 1 paid each time it is used. Given a `start` and a `goal`, return the smallest total toll of a drive from `start` to `goal`, or -1 if no drive exists. Roads may repeat and a road may begin and end at the same junction.

**Constraints.** 1 <= n <= 100000, 0 <= roads.length <= 200000, and start and goal are valid junctions.

**Example 1.** Input `n = 6`, `roads = [[0,1,1],[1,2,1],[0,3,0],[3,4,0],[4,2,0],[2,5,1],[5,5,0],[0,0,1]]`, `start = 0`, `goal = 5`, output `1`.

**Example 2.** Input `n = 4`, `roads = [[0,1,1],[1,1,0],[2,3,0]]`, `start = 0`, `goal = 3`, output `-1`.

**Hint.** Which of the two features of the map, the number of roads or their tolls, does the answer count, and how is a two-way road stored?

**Changed decision.** Each road is stored in both directions and the answer sums tolls and not roads, so the search keeps ordering by price instead of by the number of roads driven.
