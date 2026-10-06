<!-- lesson-kind: standard -->
<!-- lesson-id: stale-heap-entries -->
## Skip Outdated Heap Entries

<!-- stage: context -->
### Fixing A Distance That Is Already Queued

A navigation service computes driving times from one depot to every town. It keeps the towns that it has reached in a priority queue, ordered by travel time, and always takes the nearest one next. Then it finds a faster road to a town that already waits in the queue with a slower time. The queue now holds a wrong number for that town. If the service takes the wrong number, it expands the town too late and may report a time that is too long.

The previous lesson in this chapter built Dijkstra's method on a weighted graph. The method keeps `dist[v]`, the best known distance to vertex `v`, and a heap of candidates. When an edge offers a smaller value for `v`, the method relaxes the edge, which means it lowers `dist[v]` and queues the new candidate.

Java's `PriorityQueue` offers `add`, `poll`, `peek` and `remove(Object)`. None of them changes the priority of an element that is already inside. This lesson asks how the method stays correct when a queued distance becomes wrong.

<!-- stage: naive -->
### Removing The Old Entry First

The direct idea mimics an operation that other languages provide. Before the method queues a better distance for `v`, it removes the entry for `v` that waits in the heap. The array `waiting[v]` remembers that entry, so the call `pq.remove(waiting[v])` can find it.

```java
static long[] withRemoval(int n, List<List<int[]>> adj, int src) {
    long[] best = new long[n];
    Arrays.fill(best, Long.MAX_VALUE);
    best[src] = 0;
    long[][] waiting = new long[n][];
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    waiting[src] = new long[] {0, src};
    pq.add(waiting[src]);
    while (!pq.isEmpty()) {
        long[] top = pq.poll();
        int u = (int) top[1];
        waiting[u] = null;
        for (int[] e : adj.get(u)) {
            int v = e[0];
            long cand = best[u] + e[1];
            if (cand < best[v]) {
                best[v] = cand;
                if (waiting[v] != null) pq.remove(waiting[v]);
                waiting[v] = new long[] {cand, v};
                pq.add(waiting[v]);
            }
        }
    }
    return best;
}
```

Each entry is a `long[]` that holds a distance and a vertex. The method returns correct distances, because the heap never holds a wrong number for a waiting vertex. The question is what each `remove` call costs.

```predict
A vertex improves 1000 times while the heap holds about 50000 entries. How many entries does one call of pq.remove(waiting[v]) examine in the worst case, and does the heap order help the search?

It examines up to 50000 entries, and the heap order does not help. The method remove(Object) walks the backing array from index 0 and compares each element with equals until it finds a match. A heap orders only parent against child, so it cannot guide a search for an arbitrary element. After the match, the removal also repairs the heap order, which costs a logarithmic number of swaps. The linear walk dominates.
```

<!-- stage: bottleneck -->
### Removal Costs A Full Scan

A relaxation that succeeds triggers one `remove`. A heap with `h` entries needs O(h) time to find the entry, and the repair afterwards needs O(log h) time. The graph has up to E successful relaxations, and the heap can grow toward V entries. The total reaches O(E * V) in the worst case. A dense graph with 5000 vertices and 20 million edges turns this into a shortage of time, while a method with O(E log V) cost finishes in a moment.

The cost has nothing to do with the shortest path logic. It comes entirely from the attempt to keep the heap free of wrong numbers. The attempt is also unnecessary. The method reads a distance from the heap only at the moment of a `poll`, and at that moment it can compare the polled number with `dist[v]` in constant time. A wrong number that waits inside the heap does no harm until someone takes it.

The remaining question is how the method recognizes and treats such a number, so that no search through the heap is needed.

<!-- stage: insight -->
### Leave Old Entries And Skip Them

The method adds a new entry for every improvement and never touches the old one. The heap then holds more entries than vertices, and the reader needs three terms to describe them.

<!-- names: stale, duplicate, lazy deletion -->

#### Adding A Second Entry

A **duplicate** is a second heap entry for a vertex that already has one. The relaxation of an edge from `u` to `v` computes `nd = d + w`. When `nd` is smaller than `dist[v]`, the method assigns `dist[v] = nd` and calls `add` with the pair `(nd, v)`. Nothing else happens. The cost of the step is one assignment and one O(log h) insertion.

#### Recognizing An Outdated Entry

An entry `(d, v)` is **stale** when `d` is larger than `dist[v]`. The method detects this when it polls the entry. Each assignment to `dist[v]` only lowers the value. So `dist[v]` never exceeds the distance of any entry that the method added for `v`. The entry that carries the current `dist[v]` is therefore the smallest one for that vertex, and every other entry for `v` shows a larger number, so it is stale.

#### Skipping Before Expansion

**Lazy deletion** means that the method leaves a stale entry in the heap and discards it when `poll` returns it. The method discards it with one comparison, `d != dist[u]`, placed before the loop over the edges of `u`. The placement matters. A stale entry would otherwise run the edge loop again and repeat work that the fresh entry already did, although it would never improve any distance.

#### Counting The Extra Entries

The invariant is that `dist[v]` is the smallest candidate ever offered for `v`, and the fresh entry for `v` leaves the heap no later than any stale one. Only an improving edge adds an entry. Each vertex scans its edges once, because the method skips every stale entry. So the heap receives at most E + 1 entries in total, and the work stays at O(E log V).

<!-- stage: variables -->
### What The Method Keeps

The method reads the vertex count `n`, the weighted edge lists and the source `src`. It changes none of them. Three structures and four local values carry the state.

- **dist** is a `long[]` of length `n` that holds the best known distance, with `Long.MAX_VALUE` for a vertex that has no route yet.
- **heap** is a `PriorityQueue<long[]>` whose entries are pairs `{distance, vertex}`, ordered by the first element.
- **d** and **u** are the distance and the vertex of the entry that `poll` returned.
- **v** and **nd** are the end vertex of the scanned edge and the offered distance `d + w`.

The same vertex can appear in `heap` several times with different distances. Only the entry whose distance equals `dist[u]` leads to an expansion.

<!-- stage: trace -->
### Following Entries Through The Heap

#### A Vertex That Improves Twice

The first graph has five vertices. Its edges are 0 to 1 with weight 7, 0 to 2 with weight 2 and 2 to 1 with weight 3. The remaining edges are 1 to 3 with weight 1, 2 to 3 with weight 9 and 3 to 4 with weight 2. The source is 0. The pointer `u` marks the vertex of the popped entry. The pointer `v` marks the end of the scanned edge and holds -1 when no edge is scanned. In the variable `dist`, a dash means that no route is known yet. The variable `heap` lists the entries as distance:vertex in ascending order. Vertex 1 first receives 7 and later 5, and vertex 3 first receives 11 and later 6. The two outdated entries 7:1 and 11:3 stay in the heap until the pops near the end, where the method skips both.

```trace
{"cells":[0,1,2,3,4],"pointers":["u","v"],"steps":[{"at":{"u":-1,"v":-1},"vars":{"dist":"0,-,-,-,-","heap":"0:0"},"note":"The heap holds the single entry for source 0 with distance 0."},{"at":{"u":0,"v":-1},"vars":{"dist":"0,-,-,-,-","heap":"empty"},"note":"The method pops the entry 0:0. It equals the stored distance, so the method expands vertex 0."},{"at":{"u":0,"v":1},"vars":{"dist":"0,7,-,-,-","heap":"7:1"},"note":"The edge from 0 to 1 offers 7, which beats the stored value, so the method stores it and pushes 7:1."},{"at":{"u":0,"v":2},"vars":{"dist":"0,7,2,-,-","heap":"2:2 7:1"},"note":"The edge from 0 to 2 offers 2, which beats the stored value, so the method stores it and pushes 2:2."},{"at":{"u":2,"v":-1},"vars":{"dist":"0,7,2,-,-","heap":"7:1"},"note":"The method pops the entry 2:2. It equals the stored distance, so the method expands vertex 2."},{"at":{"u":2,"v":1},"vars":{"dist":"0,5,2,-,-","heap":"5:1 7:1"},"note":"The edge from 2 to 1 offers 5, which beats the stored value, so the method stores it and pushes 5:1."},{"at":{"u":2,"v":3},"vars":{"dist":"0,5,2,11,-","heap":"5:1 7:1 11:3"},"note":"The edge from 2 to 3 offers 11, which beats the stored value, so the method stores it and pushes 11:3."},{"at":{"u":1,"v":-1},"vars":{"dist":"0,5,2,11,-","heap":"7:1 11:3"},"note":"The method pops the entry 5:1. It equals the stored distance, so the method expands vertex 1."},{"at":{"u":1,"v":3},"vars":{"dist":"0,5,2,6,-","heap":"6:3 7:1 11:3"},"note":"The edge from 1 to 3 offers 6, which beats the stored value, so the method stores it and pushes 6:3."},{"at":{"u":3,"v":-1},"vars":{"dist":"0,5,2,6,-","heap":"7:1 11:3"},"note":"The method pops the entry 6:3. It equals the stored distance, so the method expands vertex 3."},{"at":{"u":3,"v":4},"vars":{"dist":"0,5,2,6,8","heap":"7:1 8:4 11:3"},"note":"The edge from 3 to 4 offers 8, which beats the stored value, so the method stores it and pushes 8:4."},{"at":{"u":1,"v":-1},"vars":{"dist":"0,5,2,6,8","heap":"8:4 11:3"},"note":"The method pops the entry 7:1. The stored distance of 1 is 5, so the entry is outdated and the method skips it."},{"at":{"u":4,"v":-1},"vars":{"dist":"0,5,2,6,8","heap":"11:3"},"note":"The method pops the entry 8:4. It equals the stored distance, so the method expands vertex 4."},{"at":{"u":3,"v":-1},"vars":{"dist":"0,5,2,6,8","heap":"empty"},"note":"The method pops the entry 11:3. The stored distance of 3 is 6, so the entry is outdated and the method skips it."}]}
```

#### An Equal Offer That Adds Nothing

The second graph has four edges of weight 2, namely 0 to 1, 0 to 2, 1 to 3 and 2 to 3. It also has the edge 3 to 4 with weight 1. Two routes of length 4 reach vertex 3. The first route to be scanned stores 4 and pushes the entry. The second route offers 4 again. The offer is not smaller than `dist[3]`, so the method pushes nothing, and no outdated entry appears during the whole run.

```trace
{"cells":[0,1,2,3,4],"pointers":["u","v"],"steps":[{"at":{"u":-1,"v":-1},"vars":{"dist":"0,-,-,-,-","heap":"0:0"},"note":"The heap holds the single entry for source 0 with distance 0."},{"at":{"u":0,"v":-1},"vars":{"dist":"0,-,-,-,-","heap":"empty"},"note":"The method pops the entry 0:0. It equals the stored distance, so the method expands vertex 0."},{"at":{"u":0,"v":1},"vars":{"dist":"0,2,-,-,-","heap":"2:1"},"note":"The edge from 0 to 1 offers 2, which beats the stored value, so the method stores it and pushes 2:1."},{"at":{"u":0,"v":2},"vars":{"dist":"0,2,2,-,-","heap":"2:1 2:2"},"note":"The edge from 0 to 2 offers 2, which beats the stored value, so the method stores it and pushes 2:2."},{"at":{"u":1,"v":-1},"vars":{"dist":"0,2,2,-,-","heap":"2:2"},"note":"The method pops the entry 2:1. It equals the stored distance, so the method expands vertex 1."},{"at":{"u":1,"v":3},"vars":{"dist":"0,2,2,4,-","heap":"2:2 4:3"},"note":"The edge from 1 to 3 offers 4, which beats the stored value, so the method stores it and pushes 4:3."},{"at":{"u":2,"v":-1},"vars":{"dist":"0,2,2,4,-","heap":"4:3"},"note":"The method pops the entry 2:2. It equals the stored distance, so the method expands vertex 2."},{"at":{"u":2,"v":3},"vars":{"dist":"0,2,2,4,-","heap":"4:3"},"note":"The edge from 2 to 3 offers 4, which does not beat 4, so the method pushes nothing."},{"at":{"u":3,"v":-1},"vars":{"dist":"0,2,2,4,-","heap":"empty"},"note":"The method pops the entry 4:3. It equals the stored distance, so the method expands vertex 3."},{"at":{"u":3,"v":4},"vars":{"dist":"0,2,2,4,5","heap":"5:4"},"note":"The edge from 3 to 4 offers 5, which beats the stored value, so the method stores it and pushes 5:4."},{"at":{"u":4,"v":-1},"vars":{"dist":"0,2,2,4,5","heap":"empty"},"note":"The method pops the entry 5:4. It equals the stored distance, so the method expands vertex 4."}]}
```

<!-- stage: code -->
### Shortest Distances With Entries Left In Place

The method adds an entry on every strict improvement and rejects an outdated entry right after the poll.

```java
static long[] shortest(int n, List<List<int[]>> adj, int src) {
    long[] dist = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[src] = 0;
    PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    heap.add(new long[] {0, src});
    while (!heap.isEmpty()) {
        long[] top = heap.poll();
        long d = top[0];
        int u = (int) top[1];
        if (d != dist[u]) continue;
        for (int[] e : adj.get(u)) {
            int v = e[0];
            long nd = d + e[1];
            if (nd < dist[v]) {
                dist[v] = nd;
                heap.add(new long[] {nd, v});
            }
        }
    }
    return dist;
}
```

Three details carry the correctness. The comparator calls `Long.compare`, because the subtraction `a[0] - b[0]` can overflow a `long`, and a cast of the difference to `int` can flip its sign. The test on the edge uses `<` and not `<=`, so an equal offer adds no entry. The check `d != dist[u]` sits before the edge loop. The method runs in O(E log V) time and uses O(V + E) memory for the heap and the edge lists.

<!-- stage: applicability -->
### Recognizing When Entries Pile Up

#### Spotting The Cue

Use this technique when a heap-driven search improves the priority of items that already wait in the queue, and the language heap has no decrease operation. Shortest paths with Dijkstra are the standard case. Prim's minimum spanning tree and a scheduler that re-prices tasks have the same shape. The statement of the problem usually says "the smallest total cost to reach" something.

#### Testing The Invariant

The invariant is that the fresh entry of a vertex carries `dist[v]`, and any older entry carries a larger number. The skip test relies on it. It holds only while every update lowers `dist[v]`. A negative edge weight breaks the argument. An expanded vertex can then receive a smaller value later. The first expansion is no longer final. Test the method with a zero-weight edge and with two equal offers, and check that no vertex expands twice.

#### Naming The False Friend

The false friend is `PriorityQueue.remove(Object)`, which looks like a decrease operation but scans the whole array. The related methods `contains` and `removeIf` scan the array as well. A second false friend is a visited array that blocks every second push for a vertex. It blocks the improved entry as well, so the method keeps the first, larger distance. The skip test compares distances, and a visited flag compares nothing.

<!-- stage: exercises -->
### Exercises

#### [Build] Two Entries For One Node (Author exercise)
<!-- id: sp-two-entries-one-node -->

**Prerequisites.** The heap-based shortest path method with relaxation from the earlier lesson of this chapter, and the lesson above.

**Problem.** Consider a weighted directed graph whose vertices are numbered `0` through `n - 1`. Every entry `[a, b, w]` of `edges` is an edge from `a` to `b` with weight `w`. A heap holds entries `(distance, vertex)` and removes the smallest distance first, with the smaller vertex winning a tie. The array `dist` starts at infinity, except `dist[src] = 0`, and the heap starts with the entry `(0, src)`, which counts as one push. The method removes an entry `(d, u)`. When `d` is larger than `dist[u]`, the entry is outdated, the method counts one skip and removes the next entry. Otherwise it scans the edges of `u` in the order of `edges`. For an edge to `v` with `nd = d + w`, when `nd < dist[v]`, it sets `dist[v] = nd`, pushes `(nd, v)` and counts one push. Return an `int[]` that holds the number of pushes and the number of skips.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`, and `0 <= src < n`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weights** are integers with `0 <= w <= 1000`.
- **Result** is `{pushes, skips}`, and the heap is empty when the method ends.

**Example 1.** Input `n = 4`, `edges = [[0,1,5],[0,2,2],[2,1,1],[1,3,4]]`, `src = 0`, output `[5,1]`.

**Example 2.** Input `n = 5`, `edges = [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[2,3,6],[3,4,1],[0,4,9]]`, `src = 0`, output `[8,3]`.

**Hint.** Which entry of vertex 1 is left in the heap after the first example improves it, and at which pop does the method meet it?

**Changed decision.** The method pushes a second entry on each improvement and recognizes the old entry only when it leaves the heap.

#### [Vary] Skip Before Expansion (Author exercise)
<!-- id: sp-skip-before-expansion -->

**Prerequisites.** The exercise above.

**Problem.** A directed graph and the heap procedure are given as in the previous exercise. The method rejects an outdated entry before it reads any edge of the vertex. Return the number of edge entries that the method reads during the whole run, where each read of one entry of an adjacency list counts once.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`, and `0 <= src < n`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weights** are integers with `0 <= w <= 1000`.
- **Result** is one `int`, and edges of unreachable vertices are never read.

**Example 1.** Input `n = 6`, `edges = [[0,1,4],[0,2,1],[2,1,2],[1,3,1],[4,5,1]]`, `src = 0`, output `4`.

**Example 2.** Input `n = 5`, `edges = [[0,1,9],[0,2,4],[2,1,3],[1,3,1],[2,3,8],[3,4,2],[4,1,1]]`, `src = 0`, output `7`.

**Hint.** How many times does the method expand a vertex that is reachable from the source, no matter how many entries that vertex had?

**Changed decision.** The method places the outdated-entry test before the edge loop, so an entry that fails the test reads no edges.

#### [Boundary] Equal-Cost Alternatives (Author exercise)
<!-- id: sp-equal-cost-alternatives -->

**Prerequisites.** The two exercises above.

**Problem.** A directed graph and the heap procedure are given as in the first exercise. A scan of an edge to `v` is a tie when `dist[v]` is finite and `nd` equals `dist[v]`. A tie changes nothing and pushes nothing. Return the number of ties that occur during the whole run.

**Constraints.** The limits are:
- **Vertices** satisfy `1 <= n <= 1000`, and `0 <= src < n`.
- **Edges** satisfy `0 <= edges.length <= 5000`, and repeats and self loops may occur.
- **Weights** are integers with `0 <= w <= 1000`, so zero-weight edges and zero-weight cycles may occur.
- **Result** is one `int`.

**Example 1.** Input `n = 4`, `edges = [[0,1,3],[0,2,3],[1,3,2],[2,3,2]]`, `src = 0`, output `1`.

**Example 2.** Input `n = 3`, `edges = [[0,1,0],[1,0,0],[1,2,4],[0,2,4]]`, `src = 0`, output `2`.

**Hint.** In the second example, what does the edge from 1 to 0 of weight 0 offer to vertex 0, and does the offer beat the stored value?

**Changed decision.** The method compares with a strict less-than before it stores a distance and pushes an entry, so an equal offer never reaches the heap.

#### [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay-time -->

**Prerequisites.** All three exercises above.

**Problem.** A network has `n` nodes labeled `1` to `n`. Each entry `[u, v, w]` of `times` is a directed link on which a signal travels from `u` to `v` in `w` time units. A signal starts at node `k` at time 0 and spreads over every link at once. Return the smallest time at which all `n` nodes have received the signal, or `-1` when some node never receives it. Compute the time with a heap that receives a new entry for each improvement and discards outdated entries after removal.

**Constraints.** The limits are:
- **Nodes** satisfy `1 <= n <= 1000`, and `1 <= k <= n`.
- **Links** satisfy `0 <= times.length <= 5000`, and repeats and self loops may occur.
- **Weights** are integers with `0 <= w <= 1000`.
- **Result** is one `int`, where `0` is possible when `n = 1`.

**Example 1.** Input `n = 4`, `times = [[1,2,5],[1,3,2],[3,2,1],[2,4,4]]`, `k = 1`, output `7`.

**Example 2.** Input `n = 6`, `times = [[1,2,4],[1,3,1],[3,2,2],[2,4,1],[5,6,1]]`, `k = 1`, output `-1`.

**Hint.** The signal reaches the last node at the largest entry of the final distance array. What does a missing entry mean?

**Changed decision.** The method keeps every improvement as its own heap entry and rejects an entry whose distance differs from the stored one.
