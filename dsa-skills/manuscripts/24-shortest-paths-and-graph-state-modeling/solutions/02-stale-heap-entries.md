<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Skip Outdated Heap Entries

#### Solution: [Build] Two Entries For One Node (Author exercise)
<!-- id: sp-two-entries-one-node -->

**Approach.**
The method builds adjacency lists in the order of `edges` and fills `dist` with a large sentinel. It queues `(0, src)` and counts that entry as the first push. Every removal then splits into two cases. An entry whose distance exceeds `dist[u]` is counted as a skip and ends there. Any other entry expands its vertex, and each strict improvement stores the new distance and queues a second entry for the end vertex.

The invariant is that `dist[v]` is the smallest distance offered to `v` so far. An entry whose distance differs from `dist[v]` therefore came before a better offer. Each queued entry leaves the heap once, so the pushes equal the expansions plus the skips. The comparator orders by distance and then by vertex, which makes the pop order and both counts repeatable.

**Complexity.**
- **Time** is O(E log E), because the heap receives at most E + 1 entries and each entry costs one insertion and one removal.
- **Space** is O(V + E) for the edge lists, `dist` and a heap of at most E + 1 entries.

```java run
import java.util.*;

public final class TwoEntries {
    /** Probe element that counts how many equals calls a removal makes. */
    static final class Probe implements Comparable<Probe> {
        static int equalsCalls = 0;
        final int key;
        Probe(int key) { this.key = key; }
        @Override public int compareTo(Probe o) { return Integer.compare(key, o.key); }
        @Override public boolean equals(Object o) { equalsCalls++; return o instanceof Probe p && p.key == key; }
        @Override public int hashCode() { return key; }
    }

    /**
     * Returns {pushes, skips} for the heap run from src.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: dist[v] is the smallest distance offered to v so far.
     */
    static int[] counts(int n, int[][] edges, int src) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Edge lists keep the input order, which fixes the scan order.
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        // The heap orders by distance first and by vertex second.
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, src});
        int pushes = 1, skips = 0;
        // Each loop turn removes one entry, so the loop runs once per push.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            long d = top[0];
            int u = (int) top[1];
            // A larger distance than dist[u] marks an outdated entry; count it and move on.
            if (d > dist[u]) { skips++; continue; }
            // The current entry expands its vertex once, which reads each edge once.
            for (int[] e : adj.get(u)) {
                long nd = d + e[1];
                // Only a strict improvement stores a distance and queues a second entry.
                if (nd < dist[e[0]]) {
                    dist[e[0]] = nd;
                    heap.add(new long[] {nd, e[0]});
                    pushes++;
                }
            }
        }
        return new int[] {pushes, skips};
    }

    /** Oracle: the same rules with a plain list and a linear search for the smallest entry. */
    static int[] oracle(int n, int[][] edges, int src) {
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        List<long[]> pool = new ArrayList<>();
        pool.add(new long[] {0, src});
        int pushes = 1, skips = 0;
        while (!pool.isEmpty()) {
            int best = 0;
            for (int i = 1; i < pool.size(); i++) {
                long[] a = pool.get(i), b = pool.get(best);
                if (a[0] < b[0] || (a[0] == b[0] && a[1] < b[1])) best = i;
            }
            long[] top = pool.remove(best);
            int u = (int) top[1];
            if (top[0] != dist[u]) { skips++; continue; }
            for (int[] e : edges) {
                if (e[0] != u) continue;
                if (top[0] + e[2] < dist[e[1]]) {
                    dist[e[1]] = top[0] + e[2];
                    pool.add(new long[] {dist[e[1]], e[1]});
                    pushes++;
                }
            }
        }
        return new int[] {pushes, skips};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(counts(4, new int[][] {{0, 1, 5}, {0, 2, 2}, {2, 1, 1}, {1, 3, 4}}, 0), new int[] {5, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(counts(5, new int[][] {{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 1}, {2, 3, 6}, {3, 4, 1}, {0, 4, 9}}, 0), new int[] {8, 3})) throw new AssertionError("ex2");
        // Java facts: arrays compare by reference in equals, so remove(Object) needs the very same array.
        long[] first = {1, 2};
        if (first.equals(new long[] {1, 2})) throw new AssertionError("array equals");
        PriorityQueue<long[]> q = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        q.add(first);
        if (q.remove(new long[] {1, 2})) throw new AssertionError("remove by content");
        if (!q.remove(first)) throw new AssertionError("remove by reference");
        // Java fact: the class has no decrease operation under any common name.
        for (java.lang.reflect.Method m : PriorityQueue.class.getMethods()) {
            String name = m.getName().toLowerCase();
            if (name.contains("decrease") || name.contains("changekey") || name.contains("update")) throw new AssertionError("unexpected " + name);
        }
        // Java fact: removing an element scans the backing array with equals, so a late element costs many calls.
        PriorityQueue<Probe> pq = new PriorityQueue<>();
        Probe last = null;
        for (int i = 0; i < 100; i++) { last = new Probe(i); pq.add(last); }
        Probe.equalsCalls = 0;
        pq.remove(new Probe(99));
        if (Probe.equalsCalls < 50) throw new AssertionError("remove scan " + Probe.equalsCalls);
        // Random graphs with repeats, self loops and zero weights against the list oracle.
        Random rnd = new Random(2402);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(10)};
            int src = rnd.nextInt(n);
            int[] got = counts(n, edges, src);
            if (!Arrays.equals(got, oracle(n, edges, src))) throw new AssertionError("random " + t);
            // The heap is drained, so every push is either an expansion or a skip.
            if (got[0] < got[1] + 1) throw new AssertionError("balance " + t);
        }
    }
}
```

#### Solution: [Vary] Skip Before Expansion (Author exercise)
<!-- id: sp-skip-before-expansion -->

**Approach.**
The method runs the heap procedure of the previous exercise and replaces the two counters with one counter of edge reads. It increments the counter inside the edge loop, so an outdated entry adds nothing, because it leaves the loop body through `continue` before the loop starts. A fresh entry reads all edges of its vertex once.

The invariant is that a vertex expands exactly once, at the pop of the entry whose distance equals the final `dist` of the vertex. An improvement queues a new entry only when it lowers `dist`, so two entries of one vertex never carry the same distance. The result equals the total out-degree of the vertices that are reachable from `src`, and the oracle computes exactly that with a breadth-first search.

**Complexity.**
- **Time** is O(E log E), because the heap handles at most E + 1 entries and the edge loops read E entries at most.
- **Space** is O(V + E) for the edge lists, `dist` and the heap.

```java run
import java.util.*;

public final class SkipBeforeExpansion {
    /**
     * Returns the number of adjacency entries read during the heap run.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: a vertex expands once, at the pop whose distance equals its final dist.
     */
    static int edgeReads(int n, int[][] edges, int src) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src});
        int reads = 0;
        // The loop ends when no entry remains, and the heap never holds more than E + 1 entries.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // The skip test runs before the edge loop, so an outdated entry reads no edge.
            if (top[0] != dist[u]) continue;
            for (int[] e : adj.get(u)) {
                // Each adjacency entry of an expanded vertex is read once.
                reads++;
                long nd = top[0] + e[1];
                if (nd < dist[e[0]]) {
                    dist[e[0]] = nd;
                    heap.add(new long[] {nd, e[0]});
                }
            }
        }
        return reads;
    }

    /** Oracle: sum of out-degrees over the vertices that a breadth-first search reaches. */
    static int oracle(int n, int[][] edges, int src) {
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        seen[src] = true;
        queue.add(src);
        int total = 0;
        while (!queue.isEmpty()) {
            int u = queue.poll();
            for (int[] e : edges) {
                if (e[0] != u) continue;
                total++;
                if (!seen[e[1]]) { seen[e[1]] = true; queue.add(e[1]); }
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (edgeReads(6, new int[][] {{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 1}, {4, 5, 1}}, 0) != 4) throw new AssertionError("ex1");
        if (edgeReads(5, new int[][] {{0, 1, 9}, {0, 2, 4}, {2, 1, 3}, {1, 3, 1}, {2, 3, 8}, {3, 4, 2}, {4, 1, 1}}, 0) != 7) throw new AssertionError("ex2");
        // Java fact: continue inside a while loop skips the rest of that turn only, so later turns still run.
        int turns = 0, tail = 0;
        while (turns < 3) { turns++; if (turns == 2) continue; tail++; }
        if (turns != 3 || tail != 2) throw new AssertionError("continue");
        // Random graphs against the reachability oracle.
        Random rnd = new Random(2403);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = rnd.nextInt(18);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(12)};
            int src = rnd.nextInt(n);
            if (edgeReads(n, edges, src) != oracle(n, edges, src)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Equal-Cost Alternatives (Author exercise)
<!-- id: sp-equal-cost-alternatives -->

**Approach.**
The method runs the same heap procedure and adds one branch to the relaxation. When the offered value `nd` is smaller than `dist[v]`, it stores the value and queues an entry. When `nd` equals a finite `dist[v]`, it counts a tie and does nothing else. A larger offer is ignored. The sentinel for an unreached vertex is `Long.MAX_VALUE`, and the method checks it before the equality test so that no unreached vertex counts as a tie.

The invariant is that `dist[v]` is the smallest offer so far. An equal offer carries no new information. Queueing it would create an entry that the skip test cannot tell apart from the fresh one. A zero-weight self loop on `u` offers `dist[u]` to `u` itself and always ties. The expansion of each vertex happens once, so each edge produces at most one tie.

**Complexity.**
- **Time** is O(E log E), because each edge is scanned once and each push costs O(log E).
- **Space** is O(V + E) for the edge lists, `dist` and the heap.

```java run
import java.util.*;

public final class EqualCostAlternatives {
    /**
     * Returns the number of scans whose offer equals a finite stored distance.
     * Time: O(E log E). Space: O(V + E).
     * Invariant: dist[v] is the smallest offer so far, and an equal offer adds no entry.
     */
    static int ties(int n, int[][] edges, int src) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(new int[] {e[1], e[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, src});
        int count = 0;
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // An outdated entry is skipped before any edge is scanned.
            if (top[0] != dist[u]) continue;
            for (int[] e : adj.get(u)) {
                long nd = top[0] + e[1];
                if (nd < dist[e[0]]) {
                    // A strict improvement stores the value and queues one entry.
                    dist[e[0]] = nd;
                    heap.add(new long[] {nd, e[0]});
                } else if (nd == dist[e[0]]) {
                    // An equal offer to a reached vertex is a tie, and the heap stays unchanged.
                    count++;
                }
            }
        }
        return count;
    }

    /** Oracle: repeated linear search for the unexpanded vertex with the smallest distance, no heap. */
    static int oracle(int n, int[][] edges, int src) {
        long inf = Long.MAX_VALUE;
        long[] dist = new long[n];
        Arrays.fill(dist, inf);
        dist[src] = 0;
        boolean[] done = new boolean[n];
        int count = 0;
        for (;;) {
            int u = -1;
            for (int v = 0; v < n; v++) {
                if (done[v] || dist[v] == inf) continue;
                if (u == -1 || dist[v] < dist[u]) u = v;
            }
            if (u == -1) break;
            done[u] = true;
            for (int[] e : edges) {
                if (e[0] != u) continue;
                long nd = dist[u] + e[2];
                if (nd < dist[e[1]]) dist[e[1]] = nd;
                else if (nd == dist[e[1]]) count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (ties(4, new int[][] {{0, 1, 3}, {0, 2, 3}, {1, 3, 2}, {2, 3, 2}}, 0) != 1) throw new AssertionError("ex1");
        if (ties(3, new int[][] {{0, 1, 0}, {1, 0, 0}, {1, 2, 4}, {0, 2, 4}}, 0) != 2) throw new AssertionError("ex2");
        // A zero-weight self loop ties at once.
        if (ties(1, new int[][] {{0, 0, 0}}, 0) != 1) throw new AssertionError("self loop");
        // Java fact: Long.MAX_VALUE plus a positive number wraps to a negative value, so the sentinel must be checked first.
        if (Long.MAX_VALUE + 1 >= 0) throw new AssertionError("wraparound");
        // Random graphs with many zero weights, which create many ties.
        Random rnd = new Random(2404);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(3)};
            int src = rnd.nextInt(n);
            if (ties(n, edges, src) != oracle(n, edges, src)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay-time -->

**Approach.**
The signal reaches a node at the length of the shortest path from `k`, so the answer is the largest shortest distance, or -1 when some node keeps the sentinel. The method converts the labels to zero-based indexes, runs the heap procedure with a new entry for every improvement and discards an entry whose distance differs from `dist`. It then scans `dist` once for the maximum.

The invariant is that `dist[v]` is the smallest offer so far, and an entry that disagrees with it is outdated. Weights are not negative, so the first expansion of a vertex is final, and no later offer can lower it. The result of an `n = 1` input is 0, because the maximum over the single entry `dist[k] = 0` is 0.

**Complexity.**
- **Time** is O(E log E), because each link is scanned once and the heap handles at most E + 1 entries.
- **Space** is O(N + E) for the link lists, `dist` and the heap.

```java run
import java.util.*;

public final class NetworkDelayTime {
    /**
     * Returns the time at which the last node receives the signal, or -1.
     * Time: O(E log E). Space: O(N + E).
     * Invariant: dist[v] is the smallest offer so far, and an entry that differs from it is outdated.
     */
    static int delay(int n, int[][] times, int k) {
        List<List<int[]>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        // Labels run from 1 to n, so each index shifts down by one.
        for (int[] t : times) out.get(t[0] - 1).add(new int[] {t[1] - 1, t[2]});
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[k - 1] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, k - 1});
        // Every improvement adds an entry, so the loop runs at most E + 1 times.
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            // An entry that differs from the stored distance is outdated and expands nothing.
            if (top[0] != dist[u]) continue;
            for (int[] e : out.get(u)) {
                long nd = top[0] + e[1];
                if (nd < dist[e[0]]) {
                    dist[e[0]] = nd;
                    heap.add(new long[] {nd, e[0]});
                }
            }
        }
        long worst = 0;
        // One pass finds the maximum, and an unreached node makes the answer -1.
        for (long d : dist) {
            if (d == Long.MAX_VALUE) return -1;
            worst = Math.max(worst, d);
        }
        return (int) worst;
    }

    /** Oracle: Bellman-Ford style rounds over the link list, with no heap. */
    static int oracle(int n, int[][] times, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[] dist = new long[n + 1];
        Arrays.fill(dist, inf);
        dist[k] = 0;
        for (int round = 0; round < n; round++) {
            for (int[] t : times) if (dist[t[0]] + t[2] < dist[t[1]]) dist[t[1]] = dist[t[0]] + t[2];
        }
        long worst = 0;
        for (int v = 1; v <= n; v++) {
            if (dist[v] >= inf) return -1;
            worst = Math.max(worst, dist[v]);
        }
        return (int) worst;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (delay(4, new int[][] {{1, 2, 5}, {1, 3, 2}, {3, 2, 1}, {2, 4, 4}}, 1) != 7) throw new AssertionError("ex1");
        if (delay(6, new int[][] {{1, 2, 4}, {1, 3, 1}, {3, 2, 2}, {2, 4, 1}, {5, 6, 1}}, 1) != -1) throw new AssertionError("ex2");
        // A single node needs no time, even with no links.
        if (delay(1, new int[0][], 1) != 0) throw new AssertionError("single node");
        // Java fact: the comparator difference of two longs cast to int can flip its sign.
        long a = 3_000_000_001L, b = 1;
        if ((int) (a - b) > 0) throw new AssertionError("cast sign");
        if (Long.compare(a, b) <= 0) throw new AssertionError("compare");
        // Random networks with zero weights, repeats and self loops against the rounds oracle.
        Random rnd = new Random(2405);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(18);
            int[][] times = new int[m][];
            for (int i = 0; i < m; i++) times[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n), rnd.nextInt(10)};
            int k = 1 + rnd.nextInt(n);
            if (delay(n, times, k) != oracle(n, times, k)) throw new AssertionError("random " + t);
        }
    }
}
```
