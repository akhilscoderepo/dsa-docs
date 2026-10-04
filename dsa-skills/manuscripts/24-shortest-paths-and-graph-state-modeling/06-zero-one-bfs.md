<!-- lesson-kind: standard -->
<!-- lesson-id: zero-one-bfs -->
## Zero-One BFS

<!-- stage: context -->
### Imre's Drone Over Tarn Wharf

Imre flies a parcel drone for a chandler's shop at Tarn Wharf, where the warehouse roofs form a tidy grid of landing pads. A small wind sock is bolted to every pad, and each one points north, south, east or west. The shop's battery is the only cost that matters. When the drone leaves a pad in the direction its sock points, the wind carries it and the battery does not move. When it leaves in any of the other three directions, it must fight the air and spends exactly one unit of charge.

Every morning a rush order sits on the pad at the top-left corner and the customer waits at the bottom-right one. The drone may hop only to the pad directly north, south, east or west of where it is, and it may never leave the grid. Imre wants the fewest battery units any route to the customer can cost, which may well be zero on a lucky morning, and the answer has to come quickly even if the wharf grows to a hundred pads across.

<!-- stage: naive -->
### Try Every Route Across The Roofs

The direct approach lets the drone wander. From a pad it tries each of the four neighbors, never stepping onto a pad that is already on the current route, adds one unit whenever the hop goes against the sock, and when it reaches the customer's pad it compares the units spent with the best total found so far. A route that has already spent at least as much as the best total is dropped early.

```java
static int cheapest(int[][] socks, int r, int c, boolean[][] onRoute, int spent, int best) {
    int rows = socks.length, cols = socks[0].length;
    if (spent >= best) return best;
    if (r == rows - 1 && c == cols - 1) return spent;
    onRoute[r][c] = true;
    int[][] heading = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    for (int k = 0; k < 4; k++) {
        int nr = r + heading[k][0], nc = c + heading[k][1];
        if (nr < 0 || nc < 0 || nr >= rows || nc >= cols || onRoute[nr][nc]) continue;
        int toll = socks[r][c] == k + 1 ? 0 : 1;
        best = cheapest(socks, nr, nc, onRoute, spent + toll, best);
    }
    onRoute[r][c] = false;
    return best;
}
```

The sock codes are 1 for east, 2 for west, 3 for south and 4 for north, so `k + 1` names the direction being tried. The caller starts with `best` set to a huge number and gets the right answer for any grid, because every simple route is covered. A route that visits a pad twice could never be cheaper, so refusing repeats loses nothing.

<!-- stage: bottleneck -->
### One Pad, Countless Routes

On a grid with P pads the walk can take up to three choices at every step, since one neighbor is the pad it just came from, and a route can be as long as P pads. The work is O(3^P) in the worst case, and the pruning against `best` only helps once a cheap route has already been found. A grid of five by five pads is already beyond reach, and a hundred wide is hopeless.

The waste is plain. Thousands of different routes arrive at the pad in row 2, column 3, and every one of them goes on to explore the same pads beyond it with the same sock directions. Only the number of units spent on arrival differs, and only the smallest of those numbers can ever matter. The grid has just P pads, so a method that remembered the least cost found so far for each pad would never need to treat a worse arrival as new. What is still missing is an order of processing that lets the first good arrival be trusted, as breadth-first search does when every hop costs the same.

<!-- stage: insight -->
### Two Doors On One Queue

Here the hops come in two kinds, and the whole method follows from naming them. A **free hop** follows the sock and costs nothing. A **paid hop** goes against it and costs one unit. Dijkstra would handle this with a heap, but a heap sorts far more finely than we need. Costs only ever grow by 0 or 1, so the pads waiting to be expanded never need more than two different tentative costs at once.

Keep a double-ended queue of waiting entries, each holding a pad and the cost it was given. When a hop improves the stored cost of its far pad, the new entry is placed according to the hop. A free hop gives the far pad the same cost as the pad being expanded, which is as small as anything waiting, so it goes to the front. A paid hop gives it one more, which is as large as anything waiting, so it goes to the back. The waiting entries then always sit in one **distance band**: costs run from front to back without ever dropping, and the front and back differ by at most one. The pad taken from the front is therefore always a cheapest one, which is exactly what Dijkstra's heap would hand over.

The invariant to keep in mind is that sorted-ness. It holds only because each insertion goes to the end that matches its cost. A pad may be queued twice, once with an old larger cost and again with a better one. The later, smaller entry reaches the front first, and the old copy is recognised as out of date when it finally comes up, because its stored cost is higher than the table value, so it is skipped.

<!-- names: free hop, paid hop, distance band -->

<!-- stage: variables -->
### Costs, Entries And Two Ends

The array `socks` holds the codes 1 to 4 for east, west, south and north. The array `dist` has one slot per pad, numbered row times columns plus column, and holds the least battery cost found so far, with the largest int meaning not reached. The deque `line` holds entries of the form `{pad, cost}`: the pad that was improved and the cost it had at the moment it was queued. Inside the loop, `top` is the entry removed from the front, `d` is its stored cost, and `toll` is 0 or 1 for the hop being considered. A slot of `dist` is lowered only when `d + toll` is strictly smaller than what it holds, and the entry then goes to the front when `toll` is 0 and to the back otherwise.

<!-- stage: trace -->
### Two Runs, One With A Duplicate

The first trace is a three by three wharf with the sock codes shown as letters, R for east, L for west, D for south and U for north. The cells are the nine pads in reading order, and the pointer `cur` is the pad being expanded. Steps follow the order in which entries leave the front of the deque, so the pointer jumps around the grid. Each step reports the cost of the entry, whether it was stale, how many entries went to the front and to the back, and how many wait afterwards. The drone first slides down the left column for free, and only the last pad, at the bottom-right corner, costs one unit to reach, so the answer is 1 while a plain count of hops would say 4.

```trace
{"cells":["D","R","D","D","R","D","R","D","D"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"cost":0,"stale":0,"front":1,"back":1,"waiting":2},"note":"Pad 0 is expanded at cost 0; 1 entry went to the front and 1 to the back."},{"at":{"cur":3},"vars":{"cost":0,"stale":0,"front":1,"back":1,"waiting":3},"note":"Pad 3 is expanded at cost 0; 1 entry went to the front and 1 to the back."},{"at":{"cur":6},"vars":{"cost":0,"stale":0,"front":1,"back":0,"waiting":3},"note":"Pad 6 is expanded at cost 0; 1 entry went to the front and 0 to the back."},{"at":{"cur":7},"vars":{"cost":0,"stale":0,"front":0,"back":1,"waiting":3},"note":"Pad 7 is expanded at cost 0; 0 entries went to the front and 1 to the back."},{"at":{"cur":1},"vars":{"cost":1,"stale":0,"front":1,"back":0,"waiting":3},"note":"Pad 1 is expanded at cost 1; 1 entry went to the front and 0 to the back."},{"at":{"cur":2},"vars":{"cost":1,"stale":0,"front":1,"back":0,"waiting":3},"note":"Pad 2 is expanded at cost 1; 1 entry went to the front and 0 to the back."},{"at":{"cur":5},"vars":{"cost":1,"stale":0,"front":0,"back":0,"waiting":2},"note":"Pad 5 is expanded at cost 1; 0 entries went to the front and 0 to the back."},{"at":{"cur":4},"vars":{"cost":1,"stale":0,"front":0,"back":0,"waiting":1},"note":"Pad 4 is expanded at cost 1; 0 entries went to the front and 0 to the back."},{"at":{"cur":8},"vars":{"cost":1,"stale":0,"front":0,"back":0,"waiting":0},"note":"Pad 8 is expanded at cost 1; 0 entries went to the front and 0 to the back."}]}
```

The second trace uses an explicit graph of five junctions numbered 0 to 4, with a cycle of zero-cost edges between junctions 1 and 3 and another between 2 and 4. The pointer `cur` is the junction taken from the front, in order. The vars add `span`, the distance from the cost at the front to the cost at the back after the step, and it never exceeds 1. Junction 3 is queued first at cost 1, then improved to 0, so its old entry becomes a duplicate. It comes out later and is skipped as stale, and the zero-cost cycles stop because a cycle never gives a strictly smaller cost.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"cost":0,"stale":0,"span":1,"waiting":2},"note":"Junction 0 is expanded at cost 0; it queues 3 at 1 to the back, 1 at 0 to the front."},{"at":{"cur":1},"vars":{"cost":0,"stale":0,"span":1,"waiting":3},"note":"Junction 1 is expanded at cost 0; it queues 3 at 0 to the front, 2 at 1 to the back."},{"at":{"cur":3},"vars":{"cost":0,"stale":0,"span":0,"waiting":2},"note":"Junction 3 is expanded at cost 0; no edge lowers a stored cost."},{"at":{"cur":3},"vars":{"cost":1,"stale":1,"span":0,"waiting":1},"note":"The entry for junction 3 carries cost 1 but the table holds 0, so it is skipped."},{"at":{"cur":2},"vars":{"cost":1,"stale":0,"span":0,"waiting":1},"note":"Junction 2 is expanded at cost 1; it queues 4 at 1 to the front."},{"at":{"cur":4},"vars":{"cost":1,"stale":0,"span":0,"waiting":0},"note":"Junction 4 is expanded at cost 1; no edge lowers a stored cost."}]}
```

<!-- stage: code -->
### Deque Search Over Wind Socks

```java
final class Wind {
    static final int[][] HEADING = {{0, 0}, {0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    static int fewestUnits(int[][] socks) {
        int rows = socks.length, cols = socks[0].length;
        int[] dist = new int[rows * cols];
        Arrays.fill(dist, Integer.MAX_VALUE);
        ArrayDeque<int[]> line = new ArrayDeque<>();
        dist[0] = 0;
        line.addLast(new int[] {0, 0});
        while (!line.isEmpty()) {
            int[] top = line.pollFirst();
            int pad = top[0], d = top[1];
            if (d > dist[pad]) continue;
            int r = pad / cols, c = pad % cols;
            for (int code = 1; code <= 4; code++) {
                int nr = r + HEADING[code][0], nc = c + HEADING[code][1];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                int toll = socks[r][c] == code ? 0 : 1;
                int next = nr * cols + nc;
                if (d + toll < dist[next]) {
                    dist[next] = d + toll;
                    int[] entry = {next, d + toll};
                    if (toll == 0) line.addFirst(entry);
                    else line.addLast(entry);
                }
            }
        }
        return dist[rows * cols - 1];
    }
}
```

The stored cost in each entry is what makes the stale test possible, since a bare pad number could not say which push it came from. Each pad is expanded once with its final cost, and every improvement pushes one entry, so a grid with P pads has at most 4P pushes. Time is O(P) with constant-time deque ends, and space is O(P) for `dist` plus at most 4P queued entries.

<!-- stage: applicability -->
### When Costs Are Only Zero Or One

Look for this method when a shortest-cost question has every step costing either nothing or one unit: following an arrow or turning, passing an open door or breaking a wall, riding a line or switching lines. The cue is a cost list that contains just two values, and the answer is a total on a graph that may be given outright or may hide inside a grid. The invariant is that the queue is in nondecreasing order of stored cost and holds at most two distinct values, and each push at the right end is what keeps it so.

The nearest false friend is ordinary BFS, which counts edges and so treats a free hop and a paid hop alike. On the three by three wharf above it reports 4 hops where the true cost is 1. A second false friend is trusting a popped entry blindly: after a pad has been improved, its old larger entry is still in the deque, and expanding it again repeats work, and on repeated improvements it can repeat a lot.

Do not use it when any cost is negative, or when costs can take a third value such as 2 or 7, because then a push at either end no longer keeps the order, and a heap or buckets are needed. In Java, `push` on an `ArrayDeque` adds at the front, exactly like `addFirst`, while `add` adds at the back, so the two names are easy to mix up by accident. The class also rejects `null` entries and gives constant-time access only at its two ends, so use a deque of small arrays or a record rather than searching it.

<!-- stage: exercises -->
### Exercises

#### [Build] Choose Deque End By Weight (Author exercise)
<!-- id: sp-deque-end -->

**Prerequisites.** The two-ended push rule and the `dist` array from this lesson.

**Problem.** A zero-one search has just removed junction `u` from the front of its deque. The array `deque` lists the junction numbers still waiting, front to back, and `dist` holds the tentative cost of every junction, with `Integer.MAX_VALUE` meaning not reached. The rows of `out` are the edges leaving `u`, each as `{v, w}` with `w` equal to 0 or 1. Taking the rows in the given order, lower `dist[v]` to `dist[u] + w` when that is strictly smaller, and place `v` at the front of the deque when `w` is 0 and at the back when `w` is 1. Update `dist` in place and return the new deque contents as an `int[]`, front to back. The input `deque` is not modified, and a junction that is improved twice appears twice.

**Constraints.** 2 <= dist.length <= 8, 0 <= deque.length <= 6, 0 <= u < dist.length, `dist[u]` is finite and at most 1000, and out has at most 8 rows.

**Example 1.** Input `deque = [4, 5]`, `dist = [0, 2, MAX, MAX, 2, 3]`, `u = 1`, `out = [[2,0],[3,1],[5,0]]`, output `[5, 2, 4, 5, 3]`, and `dist` becomes `[0, 2, 2, 3, 2, 2]`.

**Example 2.** Input `deque = [2, 3]`, `dist = [0, 1, 1, 2, 2]`, `u = 1`, `out = [[2,0],[3,1],[0,1]]`, output `[2, 3]`, and `dist` stays `[0, 1, 1, 2, 2]`.

**Hint.** Which end is right for an entry whose cost equals the cost of the junction just expanded, and which for one that is one larger?

**Changed decision.** The end of the deque is chosen by the weight of the edge that caused the improvement, instead of always appending at the back as plain BFS does.

#### [Vary] Reject Nonimproving Relaxations (Author exercise)
<!-- id: sp-reject-nonimproving -->

**Prerequisites.** The Choose Deque End By Weight rung and the stale-entry skip from the code stage.

**Problem.** The graph has vertices 0 to n-1, and each row of `edges` is `{from, to, weight}` with weight 0 or 1. Run the zero-one search from vertex 0, expanding the edges of a vertex in the order they appear in `edges`. Return a `long[]` of length n + 1. The first n entries are the least cost from vertex 0 to each vertex, with -1 where there is no route, and the last entry is the total number of entries ever pushed on the deque. The first entry for vertex 0 counts as one push, and afterwards an entry is pushed only when an edge strictly lowers the stored cost of its far end. Popped entries whose stored cost is above the table value are skipped. The edge array is not modified.

**Constraints.** 1 <= n <= 8, 0 <= edges.length <= 20, and parallel edges and self-loops are allowed.

**Example 1.** Input `n = 4`, `edges = [[0,1,1],[0,2,0],[2,1,0],[1,3,1],[2,3,1]]`, output `[0, 0, 0, 1, 5]`.

**Example 2.** Input `n = 4`, `edges = [[0,0,0],[0,1,1],[1,0,0],[1,1,0],[2,3,0]]`, output `[0, 1, -1, -1, 2]`.

**Hint.** Compare the proposal with the table, not with the vertex's old position in the deque. Does an equal proposal count as an improvement?

**Changed decision.** A relaxation is accepted only when it lowers the table value, instead of whenever the far vertex is not yet marked as seen.

#### [Boundary] Zero-Cost Cycle (Author exercise)
<!-- id: sp-zero-cycle -->

**Prerequisites.** The Reject Nonimproving Relaxations rung.

**Problem.** The graph has vertices 0 to n-1 and each row of `edges` is `{from, to, weight}` with weight 0 or 1, and zero-weight edges may form cycles. Run the zero-one search from vertex 0 with the edges of every vertex taken in input order, and return the vertices in the order they are expanded, meaning popped from the front with a stored cost equal to the table value. Stale pops are skipped and add nothing to the answer. Each vertex reachable from 0 appears exactly once, and unreachable vertices do not appear. The search must stop on its own even when every reachable edge is free. The edge array is not modified.

**Constraints.** 1 <= n <= 8, 0 <= edges.length <= 20, and every cycle may have total cost 0.

**Example 1.** Input `n = 5`, `edges = [[0,1,0],[1,2,0],[2,0,0],[2,3,1],[3,4,0],[4,3,0],[1,4,1]]`, output `[0, 1, 2, 4, 3]`.

**Example 2.** Input `n = 5`, `edges = [[0,3,0],[0,1,0],[1,0,0],[3,2,0],[2,3,0],[1,4,1]]`, output `[0, 1, 3, 2, 4]`.

**Hint.** A zero edge can never produce a strictly smaller cost around a cycle. Which test stops the loop, and why would a visited flag set at push time give a wrong cost?

**Changed decision.** Termination comes from the strict-improvement test on the distance table, instead of from marking a vertex as discovered the first time it is queued.

#### [Recognize] Minimum Cost To Make At Least One Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-arrow-grid -->

**Prerequisites.** The Zero-Cost Cycle rung and the grid indexing `row * cols + col` from the code stage.

**Problem.** Every cell of the `grid` holds an arrow: 1 points right, 2 left, 3 down and 4 up. Following the arrow in a cell moves you into that neighbor cell, and a move that would leave the grid is not allowed. Starting at the top-left cell, you want some chain of arrow moves to end at the bottom-right cell. Before you start you may repoint the arrow of any cell to any of the four directions, at a cost of 1 for each cell you repoint. Return the smallest total cost that makes such a path exist. The grid is not modified.

**Constraints.** 1 <= rows, cols <= 100 and every entry is between 1 and 4. A grid with a single cell costs 0.

**Example 1.** Input `grid = [[2,2,3],[4,1,3],[1,1,1]]`, output `2`.

**Example 2.** Input `grid = [[2,2,2],[2,2,2],[2,2,2]]`, output `4`.

**Hint.** Think of a move from a cell as an edge. What does it cost when the move agrees with the cell's arrow, and what when it does not?

**Changed decision.** The cost of a move is decided by whether it agrees with the arrow in the cell it leaves, so the grid becomes a graph whose edges cost 0 or 1.
