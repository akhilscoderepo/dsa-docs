<!-- lesson-kind: standard -->
<!-- lesson-id: keep-best-resource -->
## Keep The Best Resource Left

<!-- stage: context -->
### Crossing Blocked Passages With Limited Charges

A level editor for a dungeon game must tell the designer whether a character can reach the exit, and with how few moves. The map is a set of rooms joined by one-way passages. Some passages are blocked. The character carries `k` charges, and a **break** crosses one blocked passage and uses one charge. When the editor reports "no route" for a level that has one, the designer removes a door that was fine.

Model the rooms as vertices and the passages as directed edges. Each edge has a cost of 0 for an open passage or 1 for a blocked one. The game character starts in room 0 with `k` charges and wants room `n - 1` in the fewest moves, where every move counts as one regardless of cost. A route is legal only if the costs along it add up to at most `k`.

The question of this lesson is what the search must remember about the character besides the room, and which remembered situations it may safely forget.

<!-- stage: naive -->
### Marking Each Room Visited Once

Chapter 21 solved fewest-move problems with a breadth-first search that marks every vertex visited the first time it appears. The natural adaptation keeps that rule and adds a charge count to each queue entry. A blocked edge is skipped when no charge is left.

```java
static int fewestMovesNaive(List<List<int[]>> adj, int k, int target) {
    boolean[] visited = new boolean[adj.size()];
    ArrayDeque<int[]> queue = new ArrayDeque<>();
    visited[0] = true;
    queue.add(new int[] {0, k, 0});
    while (!queue.isEmpty()) {
        int[] entry = queue.poll();
        if (entry[0] == target) return entry[2];
        for (int[] edge : adj.get(entry[0])) {
            int charges = entry[1] - edge[1];
            if (charges < 0 || visited[edge[0]]) continue;
            visited[edge[0]] = true;
            queue.add(new int[] {edge[0], charges, entry[2] + 1});
        }
    }
    return -1;
}
```

Take five rooms and `k = 1`. The edges are 0 to 1 with cost 1, 0 to 2 with cost 0, 2 to 3 with cost 0, 3 to 1 with cost 0, and 1 to 4 with cost 1. The target is room 4.

```predict
What does fewestMovesNaive return for this map, and what is the true answer?

It returns -1, but the true answer is 4. The search reaches room 1 first by the blocked edge from room 0, which spends the only charge. Room 1 is then marked visited, so the later arrival through rooms 2 and 3, which still holds the charge, is ignored. Without a charge, the blocked edge from room 1 to room 4 cannot be crossed. The route 0, 2, 3, 1, 4 is legal and has 4 moves.
```

<!-- stage: bottleneck -->
### One Room Holds Several Different Situations

The marking rule assumes that arriving at a room twice is the same event, so the second arrival adds nothing. Here the two arrivals differ in the number of charges left. Room 1 with zero charges and room 1 with one charge allow different continuations. A single `boolean` per room cannot record both, and it keeps whichever arrives first.

The safe repair treats the pair (room, charges left) as the vertex and marks each pair visited. That search is correct, because two entries with the same pair are truly identical. There are `n * (k + 1)` pairs and every edge is read once per charge value, so the time is O((V + E) * k). For `k` up to the number of cells in a grid, that cost is large.

Most of those pairs are useless. Once the search holds room 1 with one charge, it gains nothing from room 1 with zero charges, since every move allowed with zero is also allowed with one. The next stage states exactly when such a pair can be dropped and when it cannot.

<!-- stage: insight -->
### Dropping Only What Is Provably Worse

The repair is to keep the full pair in the queue entry and to discard a pair only under a rule that comes with a proof.

<!-- names: dominance, dominated, layer -->

#### What Dominance Means

Take two queue entries at the same room. Entry A has `a` charges left and entry B has `b` charges left, with `a >= b`. Entry A **dominates** entry B, and this relation is called **dominance**. Every sequence of edges legal from B is also legal from A, because a legal sequence from B costs at most `b`, and `a` is at least `b`. Entry A then reaches every room that entry B reaches, in the same number of further moves.

#### Why Distance Must Be Compared

The relation above ignores how many moves each entry has already used. A **layer** is the set of entries with the same move count. Breadth-first search dequeues and discovers entries in nondecreasing layer order. When it considers a new entry B, every entry already enqueued at that room belongs to the same layer as B or an earlier one.

Suppose A was discovered earlier, so its move count is at most B's, and `a >= b`. Any route that continues from B finishes no sooner than the same route continues from A. Entry B is **dominated** and can be discarded. The invariant is that the search keeps, per room, the largest charge count among its enqueued entries, and it enqueues a new entry only when its charge count is strictly larger.

#### Why The Reverse Fails

The rule is one-directional. An entry B discovered later with more charges than A is not dominated, even though it took more moves. The naive stage showed this: room 1 with one charge arrives at move 3, behind room 1 with zero charges at move 1, and only the later entry can finish. A Boolean per room discards that entry because it compares rooms and not charge counts. The correct comparison is `remaining > best[next]`, where `best` holds the largest charge count enqueued at each room.

<!-- stage: variables -->
### What The Search Keeps

The search keeps the adjacency list `adj`, one integer array `best` and one queue. Each queue entry is an int array with three fields. The code below uses the names in this list, and it adds the locals `entry`, `node`, `next` and `left`, where `left` is the charge count after one edge.

- **adj** is the adjacency list; `adj.get(v)` holds `{next, cost}` pairs with cost 0 or 1.
- **best** is an int array; `best[v]` is the largest remaining charge count enqueued at room `v`, and -1 means never reached.
- **queue** is an `ArrayDeque<int[]>` of entries `{node, remaining, dist}`.
- **remaining** is the charge count of an entry; it never goes below 0.
- **dist** is the number of moves used so far, and it grows by 1 per move.

<!-- stage: trace -->
### Following Entries On Two Maps

#### A Map Where Fewer Moves Lose

The first map is the five-room map of the naive stage with `k = 1`. The cells are room ids and the pointer `cur` marks the room of the entry just taken from the queue. The search enqueues room 1 with zero charges at move 1 and room 2 with one charge. Later it reaches room 1 again with one charge. The comparison `1 > 0` holds, so that entry joins the queue and `best[1]` becomes 1. Room 4 then comes through the blocked edge at move 4.

```trace
{"cells":[0,1,2,3,4],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"best":"1,0,1,-1,-1","queue":"1:0 2:1"},"note":"The search takes room 0 with 1 charge after 0 moves. It enqueues room 1 with 0 charges and room 2 with 1 charge."},{"at":{"cur":1},"vars":{"best":"1,0,1,-1,-1","queue":"2:1"},"note":"The search takes room 1 with 0 charges after 1 move. It discards room 4, which costs more than the 0 charges left."},{"at":{"cur":2},"vars":{"best":"1,0,1,1,-1","queue":"3:1"},"note":"The search takes room 2 with 1 charge after 1 move. It enqueues room 3 with 1 charge."},{"at":{"cur":3},"vars":{"best":"1,1,1,1,-1","queue":"1:1"},"note":"The search takes room 3 with 1 charge after 2 moves. It enqueues room 1 with 1 charge."},{"at":{"cur":1},"vars":{"best":"1,1,1,1,0","queue":"4:0"},"note":"The search takes room 1 with 1 charge after 3 moves. It enqueues room 4 with 0 charges."},{"at":{"cur":4},"vars":{"best":"1,1,1,1,0","queue":"empty"},"note":"The search takes room 4 with 0 charges after 4 moves. This is the target, so it returns 4."}]}
```

#### A Map With A Dominated Revisit

The second map has six rooms, `k = 1` and the target room 5. Its edges lead from 0 to 1 at cost 1, from 0 to 2 at cost 0, from 2 to 3 at cost 0, from 3 to 1 at cost 0, from 3 back to 0 at cost 0, from 1 to 4 at cost 0, and from 4 to 5 at cost 1. The edge from 3 back to 0 offers room 0 with one charge. The source already holds `best[0] = 1`, so `1 > 1` is false and the entry is discarded. The search never loops.

```trace
{"cells":[0,1,2,3,4,5],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"best":"1,0,1,-1,-1,-1","queue":"1:0 2:1"},"note":"The search takes room 0 with 1 charge after 0 moves. It enqueues room 1 with 0 charges and room 2 with 1 charge."},{"at":{"cur":1},"vars":{"best":"1,0,1,-1,0,-1","queue":"2:1 4:0"},"note":"The search takes room 1 with 0 charges after 1 move. It enqueues room 4 with 0 charges."},{"at":{"cur":2},"vars":{"best":"1,0,1,1,0,-1","queue":"4:0 3:1"},"note":"The search takes room 2 with 1 charge after 1 move. It enqueues room 3 with 1 charge."},{"at":{"cur":4},"vars":{"best":"1,0,1,1,0,-1","queue":"3:1"},"note":"The search takes room 4 with 0 charges after 2 moves. It discards room 5, which costs more than the 0 charges left."},{"at":{"cur":3},"vars":{"best":"1,1,1,1,0,-1","queue":"1:1"},"note":"The search takes room 3 with 1 charge after 2 moves. It enqueues room 1 with 1 charge. It discards room 0 with 1 charge, which does not beat best 1."},{"at":{"cur":1},"vars":{"best":"1,1,1,1,1,-1","queue":"4:1"},"note":"The search takes room 1 with 1 charge after 3 moves. It enqueues room 4 with 1 charge."},{"at":{"cur":4},"vars":{"best":"1,1,1,1,1,0","queue":"5:0"},"note":"The search takes room 4 with 1 charge after 4 moves. It enqueues room 5 with 0 charges."},{"at":{"cur":5},"vars":{"best":"1,1,1,1,1,0","queue":"empty"},"note":"The search takes room 5 with 0 charges after 5 moves. This is the target, so it returns 5."}]}
```

<!-- stage: code -->
### Comparing Against The Best Remaining

The method returns the fewest moves from room 0 to `target`, or -1.

```java
static int fewestMoves(List<List<int[]>> adj, int k, int target) {
    int[] best = new int[adj.size()];
    Arrays.fill(best, -1);
    ArrayDeque<int[]> queue = new ArrayDeque<>();
    best[0] = k;
    queue.add(new int[] {0, k, 0});
    while (!queue.isEmpty()) {
        int[] entry = queue.poll();
        int node = entry[0], remaining = entry[1], dist = entry[2];
        if (node == target) return dist;
        for (int[] edge : adj.get(node)) {
            int next = edge[0], left = remaining - edge[1];
            if (left < 0 || left <= best[next]) continue;
            best[next] = left;
            queue.add(new int[] {next, left, dist + 1});
        }
    }
    return -1;
}
```

Two Java details matter. The array `best` is filled with -1, because the default 0 would claim that every room was reached with zero charges and would discard a valid zero-charge arrival. The method returns when it dequeues the target. Entries leave the queue in nondecreasing move order, so the first target entry that leaves has the fewest moves, and an enqueue-time check would give the same count. The dequeue-time check lets the Boundary exercise below keep reading entries of the same layer, because a later entry may hold more charges. Each room enters the queue at most `k + 1` times, because `best` strictly increases, so the time is O((V + E) * k) in the worst case and the space is O(V * k).

<!-- stage: applicability -->
### Recognizing Searches With Limited Charges

#### Reading The Cue

Use this method when a fewest-moves search carries a consumable amount, such as wall breaks, fuel, stops or skips, and this lesson calls the remaining count charges, and the same position can be reached with different amounts left. Statements say "at most k obstacles" or "with at most k stops". If the charges only go down and more is always better, the comparison on `best` applies.

#### Checking The Invariant

The invariant is that `best[v]` holds the largest charge count among entries already enqueued at `v`, all of which have a move count no larger than a new entry's. It fails when more charges are not always better, for example when a larger count also costs more moves or opens fewer edges, or when edges have different weights so the queue no longer dequeues in nondecreasing move order.

#### Avoiding The False Friend

The false friend is the Boolean visited array by room or cell. It looks the same as the rule of chapter 21 and passes tests without charges, but it loses entries with more charges left, as the naive stage showed. Marking every pair (room, charges) visited is the opposite choice, and it is also correct. Its worst-case time O((V + E) * k) equals that of the dominance rule, so the gain is practical. A room reached first with two charges and again with one charge gives a new pair, which the pair rule queues and the dominance rule drops. Keep the pair in the entry, and discard only an entry that has no more charges than an earlier one.

<!-- stage: exercises -->
### Exercises

#### [Build] Position And Remaining Breaks (Author exercise)
<!-- id: bv5-position-remaining-breaks -->

**Prerequisites.** The queue search of this lesson.

**Problem.** A directed graph has vertices `0` to `n - 1`. Each edge `[a, b, w]` goes from `a` to `b` and has cost `w`, which is 0 or 1. A route from vertex `0` to vertex `n - 1` is legal when the sum of its edge costs is at most `k`. Return the minimum number of edges on a legal route, or `-1` when none exists. Mark each pair of vertex and remaining charges as visited.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 100`.
- **Edges** satisfy `0 <= edges.length <= 400`, and a vertex may repeat as a start or end.
- **Charges** satisfy `0 <= k <= 20`.
- **Result** is one `int`; it is 0 when `n` is 1.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[1,2,0],[2,4,1],[0,3,0],[3,4,1]]`, `k = 1`, output `2`.

**Example 2.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,1]]`, `k = 1`, output `4`.

**Hint.** What two values identify a queue entry so that two equal entries are really the same situation?

**Changed decision.** The visited array is indexed by the pair of vertex and remaining charges and not by the vertex alone.

#### [Vary] Best Resource Per Cell (Author exercise)
<!-- id: bv5-best-resource-per-cell -->

**Prerequisites.** The exercise above.

**Problem.** The graph, the costs and the legal routes are those of the previous exercise. Return the same minimum number of edges, but keep one array `best` with the largest remaining charge count enqueued at each vertex. Enqueue an entry only when its remaining charges exceed the stored value.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 4000`, with costs 0 or 1.
- **Charges** satisfy `0 <= k <= 100`.
- **Result** is one `int`, or `-1` when no legal route exists.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,3,1],[1,3,0],[3,4,0],[2,4,1],[4,0,0]]`, `k = 1`, output `2`.

**Example 2.** Input `n = 6`, `edges = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,0],[4,5,1],[5,0,0]]`, `k = 1`, output `5`.

**Hint.** When may a second arrival at a vertex be dropped, and when must it be kept?

**Changed decision.** One integer per vertex replaces the pair array, and the filter is a strict comparison of remaining charges.

#### [Boundary] Fewest Moves And Most Charges Left (Author exercise)
<!-- id: bv5-longer-path-more-resource -->

**Prerequisites.** The two exercises above.

**Problem.** The graph and the legal routes are those of the previous exercises. Return an array `[moves, remaining]`. Here `moves` is the minimum number of edges on a legal route to vertex `n - 1`, and `remaining` is the largest charge count left over all legal routes with that many edges. Return `[-1, -1]` when no legal route exists. Do not discard an entry because a route with fewer edges reached the same vertex earlier.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`.
- **Edges** satisfy `0 <= edges.length <= 4000`, with costs 0 or 1.
- **Charges** satisfy `0 <= k <= 100`.
- **Result** is an `int` array of length 2; for `n = 1` it is `[0, k]`.

**Example 1.** Input `n = 5`, `edges = [[0,1,1],[0,2,0],[2,3,0],[3,1,0],[1,4,1]]`, `k = 1`, output `[4, 0]`.

**Example 2.** Input `n = 4`, `edges = [[0,1,1],[1,3,0],[0,2,0],[2,3,0]]`, `k = 1`, output `[2, 1]`.

**Hint.** What should the method do with entries that reach the target in the same layer as the first one?

**Changed decision.** The method keeps dequeuing at the first target layer to find the largest remaining charge count, and it compares charges and not distances to discard entries.

#### [Recognize] Shortest Path in a Grid with Obstacles Elimination (LeetCode 1293)
<!-- id: bv5-grid-obstacles-elimination -->

**Prerequisites.** All three exercises above.

**Problem.** An `m` by `n` grid `grid` holds 0 for an empty cell and 1 for an obstacle. One move goes from a cell to an adjacent cell in one of four directions. A move onto an obstacle eliminates it, and at most `k` obstacles may be eliminated in total. Return the minimum number of moves from `(0,0)` to `(m-1,n-1)`, or `-1` when no route exists.

**Constraints.** The limits are:
- **Size** satisfies `1 <= m, n <= 40`.
- **Cells** are 0 or 1, and the start and end cells are 0.
- **Charges** satisfy `1 <= k <= m * n`.
- **Result** is one `int`, and the grid is not modified.

**Example 1.** Input `grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]`, `k = 1`, output `6`.

**Example 2.** Input `grid = [[0,0,1,0],[1,0,1,1],[1,0,1,0]]`, `k = 1`, output `5`.

**Hint.** What are the vertices of the implicit graph, and what does a move onto an obstacle cost?

**Changed decision.** The vertex is the triple of row, column and remaining eliminations, and `best` is a two-dimensional array of remaining eliminations per cell.
