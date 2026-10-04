<!-- solutions-for: 06-zero-one-bfs -->
### Zero-One BFS

#### Solution: [Build] Choose Deque End By Weight (Author exercise)
<!-- id: sp-deque-end -->

**Approach.** Walk the outgoing rows once. For a row `{v, w}` the proposal is `dist[u] + w`; when it is strictly smaller than `dist[v]`, store it and put `v` at the front for a zero weight or at the back for a one. The run block copies the input into an `ArrayDeque`, so the caller's array is untouched. The oracle keeps the same list in an `ArrayList` and inserts at index 0 or at the end, so it shares no deque code with the solution. The same file asserts the `ArrayDeque` behaviour the lesson relies on: `addFirst` and `push` insert at the head, `addLast` and `add` at the tail, `pollFirst` and `poll` remove from the head, iteration runs front to back, and `null` is rejected.

**Complexity.** Every outgoing row costs a constant amount of work, so a call takes O(out.length + deque.length) time, the second term coming from copying the waiting list, and the result occupies the same order of memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DequeEndSolution {
    static int[] afterRelax(int[] deque, int[] dist, int u, int[][] out) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        for (int x : deque) line.addLast(x);
        for (int[] e : out) {
            int v = e[0], w = e[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) line.addFirst(v);
                else line.addLast(v);
            }
        }
        int[] res = new int[line.size()];
        int i = 0;
        for (int x : line) res[i++] = x;
        return res;
    }

    static int[] oracle(int[] deque, int[] dist, int u, int[][] out) {
        List<Integer> list = new ArrayList<>();
        for (int x : deque) list.add(x);
        for (int[] e : out) {
            long proposal = (long) dist[u] + e[1];
            if (proposal < dist[e[0]]) {
                dist[e[0]] = (int) proposal;
                if (e[1] == 0) list.add(0, e[0]);
                else list.add(e[0]);
            }
        }
        return list.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        int MAX = Integer.MAX_VALUE;
        int[] dist = {0, 2, MAX, MAX, 2, 3};
        int[] deque = {4, 5};
        int[] got = afterRelax(deque, dist, 1, new int[][] {{2, 0}, {3, 1}, {5, 0}});
        check(Arrays.equals(got, new int[] {5, 2, 4, 5, 3}), "example 1 deque");
        check(Arrays.equals(dist, new int[] {0, 2, 2, 3, 2, 2}), "example 1 dist");
        check(Arrays.equals(deque, new int[] {4, 5}), "input deque unchanged");
        int[] d2 = {0, 1, 1, 2, 2};
        got = afterRelax(new int[] {2, 3}, d2, 1, new int[][] {{2, 0}, {3, 1}, {0, 1}});
        check(Arrays.equals(got, new int[] {2, 3}), "example 2 deque");
        check(Arrays.equals(d2, new int[] {0, 1, 1, 2, 2}), "example 2 dist");

        Random rnd = new Random(24061);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(7);
            int[] di = new int[n];
            for (int i = 0; i < n; i++) di[i] = rnd.nextInt(4) == 0 ? MAX : rnd.nextInt(6);
            int u = rnd.nextInt(n);
            if (di[u] == MAX) di[u] = rnd.nextInt(6);
            int[] dq = new int[rnd.nextInt(7)];
            for (int i = 0; i < dq.length; i++) dq[i] = rnd.nextInt(n);
            int[][] out = new int[rnd.nextInt(9)][];
            for (int i = 0; i < out.length; i++) out[i] = new int[] {rnd.nextInt(n), rnd.nextInt(2)};
            int[] a = di.clone(), b = di.clone();
            int[] qa = dq.clone();
            check(Arrays.equals(afterRelax(dq, a, u, out), oracle(dq, b, u, out)), "random deque");
            check(Arrays.equals(a, b), "random dist");
            check(Arrays.equals(dq, qa), "input untouched");
        }

        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.addLast(5);
        q.addFirst(1);
        check(q.peekFirst() == 1 && q.peekLast() == 5, "addFirst goes to the head, addLast to the tail");
        q.push(0);
        check(q.peekFirst() == 0, "push inserts at the front like addFirst");
        q.add(9);
        check(q.peekLast() == 9, "add inserts at the back like addLast");
        check(q.toString().equals("[0, 1, 5, 9]"), "iteration runs front to back");
        check(q.poll() == 0 && q.pollFirst() == 1, "poll and pollFirst remove from the front");
        boolean threw = false;
        try {
            q.addFirst(null);
        } catch (NullPointerException e) {
            threw = true;
        }
        check(threw, "ArrayDeque rejects null");
        System.out.println("OK");
    }

    static void check(boolean ok, String msg) {
        if (!ok) throw new AssertionError(msg);
    }
}
```

#### Solution: [Vary] Reject Nonimproving Relaxations (Author exercise)
<!-- id: sp-reject-nonimproving -->

**Approach.** Build adjacency lists in input order, keep `dist` as a `long` array, and run the loop from the lesson, counting every entry added to the deque, with the first one for vertex 0 included. An entry is `{vertex, cost}`, and one whose cost exceeds the table value is skipped. Distances are checked against Floyd-Warshall, and the push count against a second simulation that stores the waiting list in an `ArrayList`. The file also checks two false friends. Without the stale skip every distance is still right, but a vertex is expanded more than once on a concrete graph, so popped duplicates cost work. A rule that rejects a far vertex because it was already discovered gives a wrong distance on another concrete graph.

**Complexity.** Each vertex is expanded once with its final cost and each edge can lower a table entry at most once per improvement, which bounds the pushes by the number of edges plus one, so the running time is O(n + m) for m edges, and the storage is O(n + m).

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ZeroOneDistancesSolution {
    static int expansions;

    @SuppressWarnings("unchecked")
    static List<int[]>[] adjacency(int n, int[][] edges) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[] {e[1], e[2]});
        return adj;
    }

    static long[] solve(int n, int[][] edges, boolean skipStale) {
        List<int[]>[] adj = adjacency(n, edges);
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<long[]> line = new ArrayDeque<>();
        line.addLast(new long[] {0, 0});
        long pushes = 1;
        expansions = 0;
        while (!line.isEmpty()) {
            long[] top = line.pollFirst();
            int v = (int) top[0];
            if (skipStale && top[1] > dist[v]) continue;
            expansions++;
            for (int[] e : adj[v]) {
                long proposal = top[1] + e[1];
                if (proposal < dist[e[0]]) {
                    dist[e[0]] = proposal;
                    pushes++;
                    long[] entry = {e[0], proposal};
                    if (e[1] == 0) line.addFirst(entry);
                    else line.addLast(entry);
                }
            }
        }
        long[] out = new long[n + 1];
        for (int i = 0; i < n; i++) out[i] = dist[i] == Long.MAX_VALUE ? -1 : dist[i];
        out[n] = pushes;
        return out;
    }

    static long[] discoveredFlagVersion(int n, int[][] edges) {
        List<int[]>[] adj = adjacency(n, edges);
        long[] dist = new long[n];
        Arrays.fill(dist, -1);
        dist[0] = 0;
        ArrayDeque<Integer> line = new ArrayDeque<>();
        line.addLast(0);
        while (!line.isEmpty()) {
            int v = line.pollFirst();
            for (int[] e : adj[v]) {
                if (dist[e[0]] != -1) continue;
                dist[e[0]] = dist[v] + e[1];
                if (e[1] == 0) line.addFirst(e[0]);
                else line.addLast(e[0]);
            }
        }
        return dist;
    }

    static long[] oracle(int n, int[][] edges) {
        long INF = Long.MAX_VALUE / 4;
        long[][] f = new long[n][n];
        for (long[] row : f) Arrays.fill(row, INF);
        for (int i = 0; i < n; i++) f[i][i] = 0;
        for (int[] e : edges) f[e[0]][e[1]] = Math.min(f[e[0]][e[1]], e[2]);
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) f[i][j] = Math.min(f[i][j], f[i][k] + f[k][j]);
        List<int[]>[] adj = adjacency(n, edges);
        long[] dist = new long[n];
        Arrays.fill(dist, Long.MAX_VALUE);
        dist[0] = 0;
        List<long[]> list = new ArrayList<>();
        list.add(new long[] {0, 0});
        long pushes = 1;
        while (!list.isEmpty()) {
            long[] top = list.remove(0);
            if (top[1] > dist[(int) top[0]]) continue;
            for (int[] e : adj[(int) top[0]]) {
                long proposal = top[1] + e[1];
                if (proposal < dist[e[0]]) {
                    dist[e[0]] = proposal;
                    pushes++;
                    if (e[1] == 0) list.add(0, new long[] {e[0], proposal});
                    else list.add(new long[] {e[0], proposal});
                }
            }
        }
        long[] out = new long[n + 1];
        for (int i = 0; i < n; i++) {
            out[i] = f[0][i] >= INF ? -1 : f[0][i];
            if (dist[i] == Long.MAX_VALUE ? out[i] != -1 : dist[i] != out[i]) throw new AssertionError("oracle disagrees with itself");
        }
        out[n] = pushes;
        return out;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 1}, {0, 2, 0}, {2, 1, 0}, {1, 3, 1}, {2, 3, 1}};
        check(Arrays.equals(solve(4, e1, true), new long[] {0, 0, 0, 1, 5}), "example 1");
        int[][] e2 = {{0, 0, 0}, {0, 1, 1}, {1, 0, 0}, {1, 1, 0}, {2, 3, 0}};
        check(Arrays.equals(solve(4, e2, true), new long[] {0, 1, -1, -1, 2}), "example 2");

        Random rnd = new Random(24062);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] edges = new int[rnd.nextInt(21)][];
            for (int i = 0; i < edges.length; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[][] copy = new int[edges.length][];
            for (int i = 0; i < edges.length; i++) copy[i] = edges[i].clone();
            long[] want = oracle(n, edges);
            check(Arrays.equals(solve(n, edges, true), want), "random " + t);
            check(Arrays.deepEquals(copy, edges), "edges untouched");
            long[] noSkip = solve(n, edges, false);
            check(Arrays.equals(Arrays.copyOf(noSkip, n), Arrays.copyOf(want, n)), "skipping is only an optimisation");
        }

        int[][] dup = {{0, 3, 1}, {0, 1, 0}, {1, 3, 0}, {3, 1, 0}, {1, 2, 1}, {2, 4, 0}, {4, 2, 0}};
        solve(5, dup, true);
        int withSkip = expansions;
        solve(5, dup, false);
        int withoutSkip = expansions;
        check(withSkip == 5 && withoutSkip == 6, "a popped duplicate is expanded again without the skip");

        int[][] trap = {{0, 1, 1}, {0, 2, 0}, {2, 1, 0}};
        check(solve(3, trap, true)[1] == 0, "true cost of vertex 1 is 0");
        check(discoveredFlagVersion(3, trap)[1] == 1, "a discovered flag keeps the first, larger cost");
        System.out.println("OK");
    }

    static void check(boolean ok, String msg) {
        if (!ok) throw new AssertionError(msg);
    }
}
```

#### Solution: [Boundary] Zero-Cost Cycle (Author exercise)
<!-- id: sp-zero-cycle -->

**Approach.** Use the same loop but record a vertex each time a non-stale entry leaves the front. Zero edges around a cycle never give a strictly smaller proposal, so nothing is pushed a second time and the loop empties. The oracle is an `ArrayList` simulation of the same rule, plus independent properties: every reachable vertex appears exactly once, none else appears, and the true distances from Bellman-Ford run to a fixpoint never decrease along the order. A third helper inspects the deque after every push and asserts the invariant of the lesson: stored costs read from front to back never decrease and take at most two distinct values.

**Complexity.** Each reachable vertex is expanded once and every edge is examined once at that moment, which gives time proportional to n plus the edge count and storage of the same order, even though a zero cycle might suggest an endless loop.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ZeroCycleSolution {
    @SuppressWarnings("unchecked")
    static List<int[]>[] adjacency(int n, int[][] edges) {
        List<int[]>[] adj = new List[n];
        for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) adj[e[0]].add(new int[] {e[1], e[2]});
        return adj;
    }

    static void checkBand(ArrayDeque<int[]> line) {
        int prev = -1;
        Set<Integer> values = new HashSet<>();
        for (int[] entry : line) {
            if (entry[1] < prev) throw new AssertionError("deque costs decrease front to back");
            prev = entry[1];
            values.add(entry[1]);
        }
        if (values.size() > 2) throw new AssertionError("more than two distinct costs queued");
        if (!line.isEmpty() && line.peekLast()[1] - line.peekFirst()[1] > 1) throw new AssertionError("span above one");
    }

    static int[] expansionOrder(int n, int[][] edges) {
        List<int[]>[] adj = adjacency(n, edges);
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> line = new ArrayDeque<>();
        line.addLast(new int[] {0, 0});
        List<Integer> order = new ArrayList<>();
        while (!line.isEmpty()) {
            int[] top = line.pollFirst();
            if (top[1] > dist[top[0]]) continue;
            order.add(top[0]);
            for (int[] e : adj[top[0]]) {
                if (top[1] + e[1] < dist[e[0]]) {
                    dist[e[0]] = top[1] + e[1];
                    int[] entry = {e[0], dist[e[0]]};
                    if (e[1] == 0) line.addFirst(entry);
                    else line.addLast(entry);
                    checkBand(line);
                }
            }
        }
        return order.stream().mapToInt(Integer::intValue).toArray();
    }

    static int[] discoveredFlagCosts(int n, int[][] edges) {
        List<int[]>[] adj = adjacency(n, edges);
        int[] cost = new int[n];
        Arrays.fill(cost, -1);
        cost[0] = 0;
        ArrayDeque<Integer> line = new ArrayDeque<>();
        line.addLast(0);
        while (!line.isEmpty()) {
            int v = line.pollFirst();
            for (int[] e : adj[v]) {
                if (cost[e[0]] != -1) continue;
                cost[e[0]] = cost[v] + e[1];
                if (e[1] == 0) line.addFirst(e[0]);
                else line.addLast(e[0]);
            }
        }
        return cost;
    }

    static int[] oracleOrder(int n, int[][] edges) {
        List<int[]>[] adj = adjacency(n, edges);
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        List<int[]> list = new ArrayList<>();
        list.add(new int[] {0, 0});
        List<Integer> order = new ArrayList<>();
        while (!list.isEmpty()) {
            int[] top = list.remove(0);
            if (top[1] > dist[top[0]]) continue;
            order.add(top[0]);
            for (int[] e : adj[top[0]]) {
                if (top[1] + e[1] < dist[e[0]]) {
                    dist[e[0]] = top[1] + e[1];
                    if (e[1] == 0) list.add(0, new int[] {e[0], dist[e[0]]});
                    else list.add(new int[] {e[0], dist[e[0]]});
                }
            }
        }
        return order.stream().mapToInt(Integer::intValue).toArray();
    }

    static int[] fixpoint(int n, int[][] edges) {
        int[] d = new int[n];
        Arrays.fill(d, Integer.MAX_VALUE);
        d[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges)
                if (d[e[0]] != Integer.MAX_VALUE && d[e[0]] + e[2] < d[e[1]]) {
                    d[e[1]] = d[e[0]] + e[2];
                    changed = true;
                }
        }
        return d;
    }

    public static void main(String[] args) {
        int[][] a = {{0, 1, 0}, {1, 2, 0}, {2, 0, 0}, {2, 3, 1}, {3, 4, 0}, {4, 3, 0}, {1, 4, 1}};
        check(Arrays.equals(expansionOrder(5, a), new int[] {0, 1, 2, 4, 3}), "example 1");
        int[][] b = {{0, 3, 0}, {0, 1, 0}, {1, 0, 0}, {3, 2, 0}, {2, 3, 0}, {1, 4, 1}};
        check(Arrays.equals(expansionOrder(5, b), new int[] {0, 1, 3, 2, 4}), "example 2");
        int[][] allFree = {{0, 1, 0}, {1, 0, 0}, {1, 1, 0}, {0, 0, 0}};
        check(Arrays.equals(expansionOrder(2, allFree), new int[] {0, 1}), "cycle of free edges terminates");

        Random rnd = new Random(24063);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] edges = new int[rnd.nextInt(21)][];
            for (int i = 0; i < edges.length; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(3) == 0 ? 1 : 0};
            int[] got = expansionOrder(n, edges);
            check(Arrays.equals(got, oracleOrder(n, edges)), "order " + t);
            int[] d = fixpoint(n, edges);
            Set<Integer> seen = new HashSet<>();
            int last = 0;
            for (int v : got) {
                check(seen.add(v), "vertex expanded twice");
                check(d[v] != Integer.MAX_VALUE && d[v] >= last, "order follows true distance");
                last = d[v];
            }
            int reachable = 0;
            for (int x : d) if (x != Integer.MAX_VALUE) reachable++;
            check(seen.size() == reachable, "every reachable vertex appears once");
        }

        int[][] trap = {{0, 1, 1}, {0, 2, 0}, {2, 1, 0}};
        check(fixpoint(3, trap)[1] == 0, "true cost is 0");
        check(discoveredFlagCosts(3, trap)[1] == 1, "a flag set when queued fixes the wrong cost");
        System.out.println("OK");
    }

    static void check(boolean ok, String msg) {
        if (!ok) throw new AssertionError(msg);
    }
}
```

#### Solution: [Recognize] Minimum Cost To Make At Least One Valid Path In A Grid (LeetCode 1368)
<!-- id: sp-arrow-grid -->

**Approach.** Treat each move from a cell as an edge whose weight is 0 when the move agrees with the arrow of the cell it leaves and 1 otherwise, then run the deque search from cell 0 and read the value at the last cell. Repointing the arrow of a cell on the route is the only way a disagreeing move can be made, and a route never needs to use the same cell twice, so the least route cost equals the least repointing cost. The file checks this reading against a brute force over every assignment of "keep or repoint to d" on tiny grids, and the search against Bellman-Ford on larger random grids. It also asserts the deque invariant after every push, and the false friends: counting hops with ordinary BFS gives 4 on a grid whose true cost is 1, and on a grid where a pad is improved twice the version without the stale skip expands more entries.

**Complexity.** A grid with P cells has at most four edges per cell, so the search finishes in time linear in the cell count, with array and deque storage of the same order, and no logarithmic factor as a heap-based method would add.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class ArrowGridSolution {
    static final int[][] HEADING = {{0, 0}, {0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    static int expansions;

    static void checkBand(ArrayDeque<int[]> line) {
        int prev = -1;
        Set<Integer> values = new HashSet<>();
        for (int[] entry : line) {
            if (entry[1] < prev) throw new AssertionError("costs decrease front to back");
            prev = entry[1];
            values.add(entry[1]);
        }
        if (values.size() > 2) throw new AssertionError("more than two distinct costs");
    }

    static int minCost(int[][] grid, boolean skipStale, boolean verify) {
        int rows = grid.length, cols = grid[0].length;
        int[] dist = new int[rows * cols];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[0] = 0;
        ArrayDeque<int[]> line = new ArrayDeque<>();
        line.addLast(new int[] {0, 0});
        expansions = 0;
        while (!line.isEmpty()) {
            int[] top = line.pollFirst();
            int cell = top[0], d = top[1];
            if (skipStale && d > dist[cell]) continue;
            expansions++;
            int r = cell / cols, c = cell % cols;
            for (int code = 1; code <= 4; code++) {
                int nr = r + HEADING[code][0], nc = c + HEADING[code][1];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                int toll = grid[r][c] == code ? 0 : 1;
                int next = nr * cols + nc;
                if (d + toll < dist[next]) {
                    dist[next] = d + toll;
                    int[] entry = {next, d + toll};
                    if (toll == 0) line.addFirst(entry);
                    else line.addLast(entry);
                    if (verify) checkBand(line);
                }
            }
        }
        return dist[rows * cols - 1];
    }

    static int bellmanFord(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] d = new int[rows * cols];
        Arrays.fill(d, Integer.MAX_VALUE);
        d[0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int p = 0; p < rows * cols; p++) {
                if (d[p] == Integer.MAX_VALUE) continue;
                int r = p / cols, c = p % cols;
                for (int code = 1; code <= 4; code++) {
                    int nr = r + HEADING[code][0], nc = c + HEADING[code][1];
                    if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) continue;
                    int w = grid[r][c] == code ? 0 : 1;
                    if (d[p] + w < d[nr * cols + nc]) {
                        d[nr * cols + nc] = d[p] + w;
                        changed = true;
                    }
                }
            }
        }
        return d[rows * cols - 1];
    }

    static int hopsOnly(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[] hops = new int[rows * cols];
        Arrays.fill(hops, -1);
        hops[0] = 0;
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.add(0);
        while (!q.isEmpty()) {
            int p = q.poll();
            for (int code = 1; code <= 4; code++) {
                int nr = p / cols + HEADING[code][0], nc = p % cols + HEADING[code][1];
                if (nr < 0 || nc < 0 || nr >= rows || nc >= cols || hops[nr * cols + nc] != -1) continue;
                hops[nr * cols + nc] = hops[p] + 1;
                q.add(nr * cols + nc);
            }
        }
        return hops[rows * cols - 1];
    }

    static boolean follows(int[][] grid, int[] arrows) {
        int rows = grid.length, cols = grid[0].length;
        int p = 0;
        for (int step = 0; step <= rows * cols; step++) {
            if (p == rows * cols - 1) return true;
            int nr = p / cols + HEADING[arrows[p]][0], nc = p % cols + HEADING[arrows[p]][1];
            if (nr < 0 || nc < 0 || nr >= rows || nc >= cols) return false;
            p = nr * cols + nc;
        }
        return false;
    }

    static int bruteForce(int[][] grid) {
        int cells = grid.length * grid[0].length, cols = grid[0].length;
        int best = Integer.MAX_VALUE;
        int total = 1;
        for (int i = 0; i < cells; i++) total *= 5;
        for (int mask = 0; mask < total; mask++) {
            int m = mask, cost = 0;
            int[] arrows = new int[cells];
            for (int p = 0; p < cells; p++) {
                int choice = m % 5;
                m /= 5;
                int own = grid[p / cols][p % cols];
                arrows[p] = choice == 0 ? own : choice;
                if (choice != 0 && choice != own) cost++;
            }
            if (cost < best && follows(grid, arrows)) best = cost;
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] e1 = {{2, 2, 3}, {4, 1, 3}, {1, 1, 1}};
        int[][] e2 = {{2, 2, 2}, {2, 2, 2}, {2, 2, 2}};
        check(minCost(e1, true, true) == 2, "example 1");
        check(minCost(e2, true, true) == 4, "example 2");
        check(minCost(new int[][] {{3}}, true, true) == 0, "single cell");

        Random rnd = new Random(24064);
        for (int t = 0; t < 400; t++) {
            int rows = 1 + rnd.nextInt(2), cols = 1 + rnd.nextInt(3);
            int[][] g = new int[rows][cols];
            for (int[] row : g) for (int c = 0; c < cols; c++) row[c] = 1 + rnd.nextInt(4);
            check(minCost(g, true, true) == bruteForce(g), "tiny " + Arrays.deepToString(g));
        }
        int stalePairs = 0;
        for (int t = 0; t < 1500; t++) {
            int rows = 1 + rnd.nextInt(7), cols = 1 + rnd.nextInt(7);
            int[][] g = new int[rows][cols];
            int[][] copy = new int[rows][];
            for (int r = 0; r < rows; r++) for (int c = 0; c < cols; c++) g[r][c] = 1 + rnd.nextInt(4);
            for (int r = 0; r < rows; r++) copy[r] = g[r].clone();
            int want = bellmanFord(g);
            check(minCost(g, true, true) == want, "random " + t);
            int skipped = expansions;
            check(minCost(g, false, false) == want, "no skip is still correct");
            check(expansions >= skipped, "skipping never expands more");
            if (expansions > skipped) stalePairs++;
            check(Arrays.deepEquals(copy, g), "grid untouched");
        }
        check(stalePairs > 0, "some grid shows the cost of popped duplicates");

        int[][] wharf = {{3, 1, 3}, {3, 1, 3}, {1, 3, 3}};
        check(minCost(wharf, true, true) == 1 && hopsOnly(wharf) == 4, "counting hops says 4, cost is 1");
        int[][] free = {{3, 1, 1}, {3, 4, 3}, {1, 1, 1}};
        check(minCost(free, true, true) == 0 && hopsOnly(free) == 4, "a free route exists but BFS reports 4");
        System.out.println("OK");
    }

    static void check(boolean ok, String msg) {
        if (!ok) throw new AssertionError(msg);
    }
}
```
