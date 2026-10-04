<!-- solutions-for: 08-bipartite-coloring -->
### Bipartite Coloring

#### Solution: [Build] Color One Component (Author exercise)
<!-- id: gt-color-one-component -->

**Approach.** Fill the color array with -1, give vertex 0 the color 0, and drain a queue. A neighbor with no color receives `1 - color[u]` and is queued, and a neighbor that already has a color is compared with `color[u]`, which ends the run with an empty array when they match. Because the graph is connected, the coloring that starts with vertex 0 at color 0 is unique when it exists, so the oracle can enumerate all 2^n assignments with vertex 0 fixed and keep the one that satisfies every edge. A second oracle never walks the graph: it closes a parity matrix over states (vertex, parity) and says the graph is two-colorable exactly when no vertex reaches itself with odd parity. The assertions compare the solution with both oracles on random connected graphs of up to ten vertices and confirm the lesson claim that a default `new int[n]` hides the unseated state.

**Complexity.** Every vertex is queued once and every adjacency entry is read once, so time is O(V + E) and the color array and queue add O(V) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ColorOneComponentSolution {
    static int[] solve(int[][] adj) {
        int n = adj.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        color[0] = 0;
        line.add(0);
        while (!line.isEmpty()) {
            int u = line.poll();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = 1 - color[u];
                    line.add(v);
                } else if (color[v] == color[u]) {
                    return new int[0];
                }
            }
        }
        return color;
    }

    static int[] bruteOracle(int[][] adj) {
        int n = adj.length;
        for (int mask = 0; mask < (1 << n); mask += 2) {
            boolean ok = true;
            for (int u = 0; u < n && ok; u++)
                for (int v : adj[u])
                    if (((mask >> u) & 1) == ((mask >> v) & 1)) { ok = false; break; }
            if (ok) {
                int[] out = new int[n];
                for (int g = 0; g < n; g++) out[g] = (mask >> g) & 1;
                return out;
            }
        }
        return new int[0];
    }

    static boolean parityOracle(int n, List<int[]> edges) {
        boolean[][] reach = new boolean[2 * n][2 * n];
        for (int[] e : edges)
            for (int p = 0; p < 2; p++) {
                reach[2 * e[0] + p][2 * e[1] + 1 - p] = true;
                reach[2 * e[1] + p][2 * e[0] + 1 - p] = true;
            }
        for (int k = 0; k < 2 * n; k++)
            for (int i = 0; i < 2 * n; i++)
                if (reach[i][k])
                    for (int j = 0; j < 2 * n; j++)
                        if (reach[k][j]) reach[i][j] = true;
        for (int u = 0; u < n; u++) if (reach[2 * u][2 * u + 1]) return false;
        return true;
    }

    static int[][] build(int n, List<int[]> edges) {
        List<List<Integer>> lists = new ArrayList<>();
        for (int i = 0; i < n; i++) lists.add(new ArrayList<>());
        for (int[] e : edges) { lists.get(e[0]).add(e[1]); lists.get(e[1]).add(e[0]); }
        int[][] adj = new int[n][];
        for (int i = 0; i < n; i++) adj[i] = lists.get(i).stream().mapToInt(Integer::intValue).toArray();
        return adj;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(new int[][] {{1, 2}, {0, 3}, {0}, {1}}), new int[] {0, 1, 1, 0}))
            throw new AssertionError("example 1");
        if (solve(new int[][] {{1, 2}, {0, 2}, {0, 1}}).length != 0) throw new AssertionError("example 2");
        int[] fresh = new int[5];
        for (int x : fresh) if (x != 0) throw new AssertionError("default is color 0, not unseated");
        Random rnd = new Random(21801);
        int sawOdd = 0, sawEven = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            List<int[]> edges = new ArrayList<>();
            boolean[][] has = new boolean[n][n];
            for (int v = 1; v < n; v++) {
                int u = rnd.nextInt(v);
                edges.add(new int[] {u, v});
                has[u][v] = has[v][u] = true;
            }
            int extra = rnd.nextInt(n + 1);
            for (int k = 0; k < extra; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u == v || has[u][v]) continue;
                has[u][v] = has[v][u] = true;
                edges.add(new int[] {u, v});
            }
            int[][] adj = build(n, edges);
            int[] got = solve(adj), want = bruteOracle(adj);
            if (!Arrays.equals(got, want)) throw new AssertionError("brute " + t);
            if ((got.length > 0) != parityOracle(n, edges)) throw new AssertionError("parity " + t);
            if (got.length > 0) sawEven++; else sawOdd++;
        }
        if (sawOdd < 100 || sawEven < 100) throw new AssertionError("both outcomes must occur");
    }
}
```

#### Solution: [Vary] Process Disconnected Components (Author exercise)
<!-- id: gt-disconnected-components -->

**Approach.** Build the adjacency lists from the edge list and scan every vertex. Each vertex still colored -1 starts a new search, increments the component count, and runs the same queue loop, and any equal pair of colors returns -1 at once. When the scan ends the count is the answer. The oracles share nothing with the traversal. One enumerates all 2^n two-colorings and tests every edge, and the other computes a Warshall closure of plain reachability to count components, taking vertex u as a representative when no smaller vertex reaches it, and a parity closure to decide two-colorability. The assertions compare all three on random graphs of up to ten vertices, and they show the false friend: a search from vertex 0 alone accepts the graph from Example 2 while the full scan rejects it.

**Complexity.** O(V + E) time, because the outer scan and all searches together touch each vertex and edge a fixed number of times, with O(V + E) memory for the lists and the color array.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class DisconnectedComponentsSolution {
    static int[][] lists(int n, int[][] edges) {
        int[] deg = new int[n];
        for (int[] e : edges) { deg[e[0]]++; deg[e[1]]++; }
        int[][] adj = new int[n][];
        for (int i = 0; i < n; i++) adj[i] = new int[deg[i]];
        int[] fill = new int[n];
        for (int[] e : edges) { adj[e[0]][fill[e[0]]++] = e[1]; adj[e[1]][fill[e[1]]++] = e[0]; }
        return adj;
    }

    static boolean paint(int[][] adj, int[] color, int start) {
        ArrayDeque<Integer> line = new ArrayDeque<>();
        color[start] = 0;
        line.add(start);
        while (!line.isEmpty()) {
            int u = line.poll();
            for (int v : adj[u]) {
                if (color[v] == -1) { color[v] = 1 - color[u]; line.add(v); }
                else if (color[v] == color[u]) return false;
            }
        }
        return true;
    }

    static int solve(int n, int[][] edges) {
        int[][] adj = lists(n, edges);
        int[] color = new int[n];
        Arrays.fill(color, -1);
        int parts = 0;
        for (int start = 0; start < n; start++) {
            if (color[start] != -1) continue;
            parts++;
            if (!paint(adj, color, start)) return -1;
        }
        return parts;
    }

    static boolean zeroOnly(int n, int[][] edges) {
        int[] color = new int[n];
        Arrays.fill(color, -1);
        return paint(lists(n, edges), color, 0);
    }

    static boolean bruteBipartite(int n, int[][] edges) {
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int[] e : edges)
                if (((mask >> e[0]) & 1) == ((mask >> e[1]) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    static boolean[][] closure(int size, boolean[][] step) {
        boolean[][] r = new boolean[size][];
        for (int i = 0; i < size; i++) r[i] = step[i].clone();
        for (int k = 0; k < size; k++)
            for (int i = 0; i < size; i++)
                if (r[i][k])
                    for (int j = 0; j < size; j++) r[i][j] |= r[k][j];
        return r;
    }

    static int oracle(int n, int[][] edges) {
        boolean[][] plain = new boolean[n][n];
        boolean[][] twin = new boolean[2 * n][2 * n];
        for (int i = 0; i < n; i++) plain[i][i] = true;
        for (int[] e : edges) {
            plain[e[0]][e[1]] = plain[e[1]][e[0]] = true;
            for (int p = 0; p < 2; p++) {
                twin[2 * e[0] + p][2 * e[1] + 1 - p] = true;
                twin[2 * e[1] + p][2 * e[0] + 1 - p] = true;
            }
        }
        boolean[][] reach = closure(n, plain), parity = closure(2 * n, twin);
        for (int u = 0; u < n; u++) if (parity[2 * u][2 * u + 1]) {
            if (bruteBipartite(n, edges)) throw new AssertionError("oracles disagree");
            return -1;
        }
        if (!bruteBipartite(n, edges)) throw new AssertionError("oracles disagree");
        int parts = 0;
        for (int u = 0; u < n; u++) {
            boolean rep = true;
            for (int v = 0; v < u; v++) if (reach[v][u]) rep = false;
            if (rep) parts++;
        }
        return parts;
    }

    public static void main(String[] args) {
        if (solve(6, new int[][] {{0, 1}, {1, 2}, {3, 4}}) != 3) throw new AssertionError("example 1");
        int[][] tri = {{0, 1}, {2, 3}, {3, 4}, {4, 2}};
        if (solve(5, tri) != -1) throw new AssertionError("example 2");
        if (!zeroOnly(5, tri)) throw new AssertionError("vertex 0 alone wrongly accepts the far triangle");
        Random rnd = new Random(21802);
        int rejected = 0, accepted = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9), tries = rnd.nextInt(2 * n);
            boolean[][] has = new boolean[n][n];
            int[][] buf = new int[tries][];
            int m = 0;
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u == v || has[u][v]) continue;
                has[u][v] = has[v][u] = true;
                buf[m++] = new int[] {u, v};
            }
            int[][] edges = Arrays.copyOf(buf, m);
            int got = solve(n, edges), want = oracle(n, edges);
            if (got != want) throw new AssertionError("random " + t + " " + got + " " + want);
            if (got < 0) rejected++; else accepted++;
        }
        if (rejected < 100 || accepted < 100) throw new AssertionError("both outcomes must occur");
    }
}
```

#### Solution: [Boundary] Self-Loop And Odd Cycle (Author exercise)
<!-- id: gt-self-loop-odd-cycle -->

**Approach.** Store the edges in forward-star arrays, where a loop is simply an edge whose two ends are the same vertex and is therefore listed once from that vertex to itself, and a repeated pair is listed twice. Scan all vertices and color each unseen one by a queue. A vertex that meets itself finds `color[v] == color[u]` with no special branch, so loops are rejected by the ordinary comparison, and repeated pairs only repeat a comparison that already passed. An odd cycle ends in the same comparison. The oracle tries all 2^n colorings and tests every listed edge, and a second oracle checks that some vertex reaches itself with odd parity in a closed matrix of (vertex, parity) states. The assertions run random multigraphs with loops, check the lesson claims about loops and repeated pairs, and confirm that rings of length 3, 5 and 7 fail while 4, 6 and 8 pass.

**Complexity.** Time is O(V + E) even with repeated pairs, since each listed edge is read from each end once, and memory is O(V + E) for the arrays.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SelfLoopOddCycleSolution {
    static boolean solve(int n, int[][] edges) {
        int[] head = new int[n], next = new int[2 * edges.length], to = new int[2 * edges.length];
        Arrays.fill(head, -1);
        int slot = 0;
        for (int[] e : edges) {
            to[slot] = e[1]; next[slot] = head[e[0]]; head[e[0]] = slot++;
            to[slot] = e[0]; next[slot] = head[e[1]]; head[e[1]] = slot++;
        }
        int[] color = new int[n], line = new int[n];
        Arrays.fill(color, -1);
        for (int start = 0; start < n; start++) {
            if (color[start] != -1) continue;
            int lo = 0, hi = 0;
            color[start] = 0;
            line[hi++] = start;
            while (lo < hi) {
                int u = line[lo++];
                for (int s = head[u]; s != -1; s = next[s]) {
                    int v = to[s];
                    if (color[v] == -1) { color[v] = 1 - color[u]; line[hi++] = v; }
                    else if (color[v] == color[u]) return false;
                }
            }
        }
        return true;
    }

    static boolean bruteOracle(int n, int[][] edges) {
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int[] e : edges)
                if (((mask >> e[0]) & 1) == ((mask >> e[1]) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    static boolean oddWalkOracle(int n, int[][] edges) {
        boolean[][] r = new boolean[2 * n][2 * n];
        for (int[] e : edges)
            for (int p = 0; p < 2; p++) {
                r[2 * e[0] + p][2 * e[1] + 1 - p] = true;
                r[2 * e[1] + p][2 * e[0] + 1 - p] = true;
            }
        for (int k = 0; k < 2 * n; k++)
            for (int i = 0; i < 2 * n; i++)
                for (int j = 0; j < 2 * n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        for (int u = 0; u < n; u++) if (r[2 * u][2 * u + 1]) return false;
        return true;
    }

    static int[][] ring(int len) {
        int[][] e = new int[len][];
        for (int i = 0; i < len; i++) e[i] = new int[] {i, (i + 1) % len};
        return e;
    }

    public static void main(String[] args) {
        if (solve(3, new int[][] {{0, 1}, {1, 1}})) throw new AssertionError("example 1");
        if (!solve(4, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 0}, {0, 1}})) throw new AssertionError("example 2");
        if (solve(1, new int[][] {{0, 0}})) throw new AssertionError("a lone self-loop must be rejected");
        if (!solve(2, new int[][] {{0, 1}, {1, 0}, {0, 1}})) throw new AssertionError("repeats change nothing");
        for (int len = 3; len <= 8; len++)
            if (solve(len, ring(len)) != (len % 2 == 0)) throw new AssertionError("ring " + len);
        Random rnd = new Random(21803);
        int yes = 0, no = 0, loops = 0;
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9), m = rnd.nextInt(2 * n + 1);
            int[][] edges = new int[m][];
            boolean hasLoop = false;
            for (int k = 0; k < m; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u == v && rnd.nextInt(4) != 0) v = (u + 1) % n;
                if (u == v) hasLoop = true;
                edges[k] = new int[] {u, v};
            }
            boolean got = solve(n, edges);
            if (got != bruteOracle(n, edges)) throw new AssertionError("brute " + t);
            if (got != oddWalkOracle(n, edges)) throw new AssertionError("parity " + t);
            if (hasLoop && got) throw new AssertionError("loop accepted " + t);
            if (hasLoop) loops++;
            if (got) yes++; else no++;
        }
        if (yes < 100 || no < 100 || loops < 100) throw new AssertionError("coverage");
    }
}
```

#### Solution: [Recognize] Is Graph Bipartite (LeetCode 785)
<!-- id: gt-is-graph-bipartite -->

**Approach.** Recognize the split into two sets as a two-coloring and run the queue search from every vertex that is still uncolored, comparing the color of each already colored neighbor with the current vertex. Any equal pair returns false, and finishing the scan returns true. The oracle never searches. It tries every assignment of the n vertices to two sets, and a second oracle uses a closure over (vertex, parity) states to find an odd closed walk. The assertions run on random symmetric graphs of up to ten vertices, show that a search limited to vertex 0 wrongly accepts Example 2, and confirm that an unfilled `new int[n]` holds 0 everywhere, which is why the color array has to start at -1.

**Complexity.** The scan and the searches visit each vertex and each adjacency entry a constant number of times, so time is O(V + E) with O(V) extra space for the colors and the queue.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class IsGraphBipartiteSolution {
    static boolean solve(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        Arrays.fill(color, -1);
        for (int root = 0; root < n; root++) {
            if (color[root] != -1) continue;
            ArrayDeque<Integer> line = new ArrayDeque<>();
            color[root] = 0;
            line.add(root);
            while (!line.isEmpty()) {
                int u = line.poll();
                for (int v : graph[u]) {
                    if (color[v] == color[u]) return false;
                    if (color[v] == -1) { color[v] = 1 - color[u]; line.add(v); }
                }
            }
        }
        return true;
    }

    static boolean zeroOnly(int[][] graph) {
        int[] color = new int[graph.length];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> line = new ArrayDeque<>();
        color[0] = 0;
        line.add(0);
        while (!line.isEmpty()) {
            int u = line.poll();
            for (int v : graph[u]) {
                if (color[v] == color[u]) return false;
                if (color[v] == -1) { color[v] = 1 - color[u]; line.add(v); }
            }
        }
        return true;
    }

    static boolean bruteOracle(int[][] graph) {
        int n = graph.length;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int u = 0; u < n && ok; u++)
                for (int v : graph[u])
                    if (((mask >> u) & 1) == ((mask >> v) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    static boolean parityOracle(int[][] graph) {
        int n = graph.length;
        boolean[][] r = new boolean[2 * n][2 * n];
        for (int u = 0; u < n; u++)
            for (int v : graph[u])
                for (int p = 0; p < 2; p++) r[2 * u + p][2 * v + 1 - p] = true;
        for (int k = 0; k < 2 * n; k++)
            for (int i = 0; i < 2 * n; i++)
                for (int j = 0; j < 2 * n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        for (int u = 0; u < n; u++) if (r[2 * u][2 * u + 1]) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!solve(new int[][] {{2, 3}, {3}, {0}, {0, 1}, {}})) throw new AssertionError("example 1");
        int[][] far = {{1}, {0}, {3, 4}, {2, 4}, {2, 3}};
        if (solve(far)) throw new AssertionError("example 2");
        if (!zeroOnly(far)) throw new AssertionError("vertex 0 alone wrongly accepts example 2");
        int[] unfilled = new int[6];
        for (int x : unfilled) if (x != 0) throw new AssertionError("defaults are 0");
        Random rnd = new Random(21804);
        int yes = 0, no = 0, trap = 0;
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9), tries = rnd.nextInt(2 * n + 1);
            boolean[][] has = new boolean[n][n];
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u != v) has[u][v] = has[v][u] = true;
            }
            int[][] graph = new int[n][];
            for (int u = 0; u < n; u++) {
                int c = 0;
                for (int v = 0; v < n; v++) if (has[u][v]) c++;
                graph[u] = new int[c];
                c = 0;
                for (int v = 0; v < n; v++) if (has[u][v]) graph[u][c++] = v;
            }
            boolean got = solve(graph);
            if (got != bruteOracle(graph)) throw new AssertionError("brute " + t);
            if (got != parityOracle(graph)) throw new AssertionError("parity " + t);
            if (!got && zeroOnly(graph)) trap++;
            if (got) yes++; else no++;
        }
        if (yes < 100 || no < 100 || trap < 20) throw new AssertionError("coverage " + yes + " " + no + " " + trap);
    }
}
```
