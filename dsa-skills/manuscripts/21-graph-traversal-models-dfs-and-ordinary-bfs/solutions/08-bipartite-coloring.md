<!-- solutions-for: 08-bipartite-coloring -->
### Solutions For Bipartite Coloring

#### Solution: [Build] Color One Component (Author exercise)
<!-- id: gt-color-one-component -->

**Approach.**
The method builds an adjacency list `adj`, colors vertex 0 with 0 and pushes it into a queue. Each vertex taken from the queue gives every uncolored neighbor the opposite color and pushes it. A neighbor that already holds the same color as the current vertex is a conflict, and the method returns false. The loop runs once, so it never leaves the component of vertex 0. The edges of other components are never read.

After each step, every colored vertex has a color that the forced rule dictates, and every edge examined joins two different colors.

**Complexity.**
- **Time** is O(n + m), because building `adj` reads each edge once and the search visits each vertex and each edge of the component at most twice.
- **Space** is O(n + m), because `adj` holds 2m entries and the arrays hold n entries.

```java run
import java.util.*;

public final class ColorOneComponent {
    /**
     * Returns true when the component of vertex 0 can be colored with two colors.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: every edge examined so far joins two different colors.
     */
    static boolean componentOfZeroOk(int n, int[][] edges) {
        // Adjacency list with one list per vertex.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        // Each undirected edge is stored in both directions, so memory is 2m entries.
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // -1 means uncolored; the default 0 would already mean a color.
        int[] color = new int[n];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The source takes color 0 and enters the queue once.
        color[0] = 0;
        queue.add(0);
        // Each vertex of the component leaves the queue exactly once.
        while (!queue.isEmpty()) {
            int u = queue.poll();
            // Every edge of u is read here, so the total edge work is O(m).
            for (int v : adj.get(u)) {
                // A colored neighbor with the same color is a conflict, so the answer is no.
                if (color[v] == color[u]) return false;
                // An uncolored neighbor is forced to the opposite color.
                if (color[v] == -1) { color[v] = 1 - color[u]; queue.add(v); }
            }
        }
        // The component passed; vertices outside it were never read.
        return true;
    }

    /** Oracle: tries every 2-coloring of all vertices and checks only edges inside the component of 0. */
    static boolean brute(int n, int[][] edges) {
        // Grow the reachable set by repeated passes over the edge list.
        boolean[] in = new boolean[n];
        in[0] = true;
        for (boolean grew = true; grew; ) {
            grew = false;
            for (int[] e : edges) {
                if (in[e[0]] != in[e[1]]) { in[e[0]] = in[e[1]] = true; grew = true; }
            }
        }
        // Enumerate all 2^n assignments by bit mask.
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int[] e : edges) {
                if (in[e[0]] && ((mask >> e[0]) & 1) == ((mask >> e[1]) & 1)) { ok = false; break; }
            }
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (componentOfZeroOk(3, new int[][] {{0, 1}, {1, 2}, {2, 0}})) throw new AssertionError("ex1");
        if (!componentOfZeroOk(6, new int[][] {{0, 1}, {1, 2}, {3, 4}, {4, 5}, {5, 3}})) throw new AssertionError("ex2");
        // A lone vertex and a parallel pair both pass.
        if (!componentOfZeroOk(1, new int[0][])) throw new AssertionError("single vertex");
        if (!componentOfZeroOk(2, new int[][] {{0, 1}, {0, 1}})) throw new AssertionError("parallel edges");
        // Random graphs must match the exhaustive oracle.
        Random rnd = new Random(2101);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(9);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                while (b == a && n > 1) b = rnd.nextInt(n);
                if (a == b) { edges = new int[0][]; break; }
                edges[i] = new int[] {a, b};
            }
            if (componentOfZeroOk(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Process Disconnected Components (Author exercise)
<!-- id: gt-process-disconnected-components -->

**Approach.**
The method keeps the same coloring step and adds an outer loop over all vertex numbers. A vertex that is still uncolored when the loop reaches it lies in a component that no earlier search touched, so it becomes a new source with color 0. The answer is false as soon as one component reports a conflict. The only change from the first exercise is the restart, and without it a bad component hides behind a good one.

Before each source, all earlier components are fully colored and valid, and no edge joins them to an uncolored vertex.

**Complexity.**
- **Time** is O(n + m), because the outer loop costs n steps and each vertex and edge is processed once across all searches.
- **Space** is O(n + m), because the method stores `adj` and one array of colors.

```java run
import java.util.*;

public final class ProcessDisconnectedComponents {
    /**
     * Returns true when the whole graph is bipartite.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: before each source, every earlier component is colored without a conflict.
     */
    static boolean isBipartite(int n, int[][] edges) {
        // Build adjacency lists; an empty graph (n = 0) skips every loop below.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        int[] color = new int[n];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The outer loop is the restart rule: n steps in total.
        for (int source = 0; source < n; source++) {
            // A colored vertex belongs to a component that is already done.
            if (color[source] != -1) continue;
            color[source] = 0;
            queue.add(source);
            // One breadth-first pass colors exactly one component.
            while (!queue.isEmpty()) {
                int u = queue.poll();
                for (int v : adj.get(u)) {
                    // Same color on both ends of an edge settles the whole answer as false.
                    if (color[v] == color[u]) return false;
                    if (color[v] == -1) { color[v] = 1 - color[u]; queue.add(v); }
                }
            }
        }
        // Every component passed.
        return true;
    }

    /** Oracle: tries all 2^n assignments. */
    static boolean brute(int n, int[][] edges) {
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int[] e : edges) if (((mask >> e[0]) & 1) == ((mask >> e[1]) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (isBipartite(6, new int[][] {{0, 1}, {1, 2}, {3, 4}, {4, 5}, {5, 3}})) throw new AssertionError("ex1");
        if (!isBipartite(5, new int[][] {{0, 1}, {2, 3}})) throw new AssertionError("ex2");
        // The empty graph is bipartite.
        if (!isBipartite(0, new int[0][])) throw new AssertionError("n = 0");
        // Random graphs without self-loops must match the oracle.
        Random rnd = new Random(2102);
        for (int t = 0; t < 800; t++) {
            int n = 2 + rnd.nextInt(7), m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = (a + 1 + rnd.nextInt(n - 1)) % n;
                edges[i] = new int[] {a, b};
            }
            if (isBipartite(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Self-Loop And Odd Cycle (Author exercise)
<!-- id: gt-self-loop-and-odd-cycle -->

**Approach.**
The method stores the neighbors in a flat array layout, with `head`, `next` and `to` arrays, and runs the restart loop of the previous exercise. A self-loop `[v, v]` adds `v` to its own neighbor list. When the search takes `v` from the queue, the neighbor `v` already holds the color of `u = v`, so the equality test fires and the method returns false. No special case is needed. An odd cycle ends in the same test, because the forced colors around the cycle return to the start with equal colors on the last edge. Parallel copies of an edge join the same two colors twice, so they never fire the test.

When the test never fires, every examined edge, including every loop and every parallel copy, joins two different colors.

**Complexity.**
- **Time** is O(n + m), because each edge is stored twice and read twice.
- **Space** is O(n + m), because `head` holds n entries and `next` and `to` hold 2m entries each.

```java run
import java.util.*;

public final class SelfLoopAndOddCycle {
    /**
     * Returns true when the graph is bipartite; self-loops and odd cycles give false.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: every edge read so far joins two different colors.
     */
    static boolean isBipartite(int n, int[][] edges) {
        // Linked-list adjacency in flat arrays: head[v] is the first slot of v, next[] chains the slots.
        int[] head = new int[n], next = new int[2 * edges.length], to = new int[2 * edges.length];
        Arrays.fill(head, -1);
        int slot = 0;
        // Each edge fills two slots; a self-loop fills two slots of the same vertex.
        for (int[] e : edges) {
            to[slot] = e[1]; next[slot] = head[e[0]]; head[e[0]] = slot++;
            to[slot] = e[0]; next[slot] = head[e[1]]; head[e[1]] = slot++;
        }
        int[] color = new int[n];
        Arrays.fill(color, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Restart loop: one source per component.
        for (int s = 0; s < n; s++) {
            if (color[s] != -1) continue;
            color[s] = 0;
            queue.add(s);
            while (!queue.isEmpty()) {
                int u = queue.poll();
                // Walk the slot chain of u; the walk length equals the degree of u.
                for (int k = head[u]; k != -1; k = next[k]) {
                    int v = to[k];
                    // For a self-loop v == u, so this test fires with no extra branch.
                    if (color[v] == color[u]) return false;
                    if (color[v] == -1) { color[v] = 1 - color[u]; queue.add(v); }
                }
            }
        }
        return true;
    }

    /** Oracle: all 2^n assignments; a self-loop can never pass because both ends share one bit. */
    static boolean brute(int n, int[][] edges) {
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int[] e : edges) if (((mask >> e[0]) & 1) == ((mask >> e[1]) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (isBipartite(3, new int[][] {{0, 1}, {1, 1}})) throw new AssertionError("ex1 self-loop");
        if (isBipartite(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}, {4, 0}})) throw new AssertionError("ex2 pentagon");
        // Two parallel copies are consistent.
        if (!isBipartite(2, new int[][] {{0, 1}, {0, 1}})) throw new AssertionError("parallel");
        // A self-loop in a far component is still found.
        if (isBipartite(4, new int[][] {{0, 1}, {3, 3}})) throw new AssertionError("loop in second component");
        // Random multigraphs with loops must match the oracle.
        Random rnd = new Random(2103);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(9);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (isBipartite(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Is Graph Bipartite? (LeetCode 785)
<!-- id: gt-is-graph-bipartite -->

**Approach.**
The input `graph` is already the adjacency list, so the method skips construction. It uses a depth-first search with an explicit stack and the same forced rule, and it restarts from every uncolored vertex. The restart is the part that this recognition exercise tests, because a connected sample hides its absence. A depth-first order gives the same verdict as a breadth-first order, because the verdict depends on the edges and not on the visiting order.

The invariant matches the lesson: every examined edge joins two different colors.

**Complexity.**
- **Time** is O(n + m), because each vertex is colored once and each neighbor entry is read once.
- **Space** is O(n) extra, because a vertex enters the stack only when it receives its color, so the stack and the color array hold at most n entries each, and the input is reused.

```java run
import java.util.*;

public final class IsGraphBipartite {
    /**
     * Returns true when graph can be split into two groups with every edge crossing groups.
     * Time: O(n + m). Space: O(n), because each vertex is pushed once, when it is colored.
     * Invariant: every edge examined so far joins two different colors.
     */
    static boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        // Zero means uncolored here; the two colors are +1 and -1, so negation swaps them.
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        // Restart loop over all vertices.
        for (int source = 0; source < n; source++) {
            if (color[source] != 0) continue;
            color[source] = 1;
            stack.push(source);
            while (!stack.isEmpty()) {
                int u = stack.pop();
                // The input array is the adjacency list, so no copy is made.
                for (int v : graph[u]) {
                    // Equal nonzero colors on both ends are a conflict.
                    if (color[v] == color[u]) return false;
                    if (color[v] == 0) { color[v] = -color[u]; stack.push(v); }
                }
            }
        }
        return true;
    }

    /** Oracle: all 2^n assignments over the edges implied by graph. */
    static boolean brute(int[][] graph) {
        int n = graph.length;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            for (int u = 0; u < n && ok; u++)
                for (int v : graph[u]) if (((mask >> u) & 1) == ((mask >> v) & 1)) { ok = false; break; }
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (isBipartite(new int[][] {{1, 4}, {0, 2}, {1, 3}, {2, 4}, {3, 0}})) throw new AssertionError("ex1");
        if (!isBipartite(new int[][] {{2}, {3}, {0}, {1}, {}})) throw new AssertionError("ex2");
        // The input array is read and never modified.
        int[][] g = {{1}, {0}};
        int[][] copy = {{1}, {0}};
        isBipartite(g);
        if (!Arrays.deepEquals(g, copy)) throw new AssertionError("input mutated");
        // Random symmetric graphs without loops or parallel edges must match the oracle.
        Random rnd = new Random(2104);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(8);
            List<List<Integer>> adj = new ArrayList<>();
            for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if (rnd.nextInt(4) == 0) { adj.get(a).add(b); adj.get(b).add(a); }
            int[][] graph = new int[n][];
            for (int i = 0; i < n; i++) graph[i] = adj.get(i).stream().mapToInt(Integer::intValue).toArray();
            if (isBipartite(graph) != brute(graph)) throw new AssertionError("random " + t);
        }
    }
}
```
