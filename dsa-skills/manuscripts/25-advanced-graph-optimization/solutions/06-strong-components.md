<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Strong Components

#### Solution: [Build] Finish Order (Author exercise)
<!-- id: ga-scc-finish-order -->

**Approach.**
The method builds an adjacency list that keeps each neighbour list in input order. It then starts a depth-first search from every unvisited vertex, taking the starts in ascending order. The search keeps an explicit stack and one cursor per vertex, where the cursor holds the position of the next outgoing edge to examine. A vertex stays on the stack while its cursor still points at an edge. When the cursor runs past the last edge, the method pops the vertex and appends it to the result, because its outgoing work is complete.

The invariant is that the method appends a vertex only after it appends every vertex reachable from it through unvisited vertices. A vertex that is already on the stack is never pushed again, so a cycle cannot cause a second visit. The explicit stack replaces recursion, so a long chain of vertices cannot exhaust the Java call stack.

**Complexity.**
- **Time** is O(V + E), because the method pushes and pops each vertex once and examines each edge once through its cursor.
- **Space** is O(V + E) for the adjacency list, plus O(V) for the stack, the cursors and the result.

```java run
import java.util.*;

public final class SccFinishOrder {
    /**
     * Returns the vertices in the order in which their outgoing search completes.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a vertex is appended only after all vertices reachable through unvisited ones are appended.
     */
    static int[] finishOrder(int n, int[][] edges) {
        // The adjacency list keeps neighbours in input order, so the output is deterministic.
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        // cursor[u] is the position of the next outgoing edge of u to examine.
        int[] cursor = new int[n];
        int[] stack = new int[n];
        int[] order = new int[n];
        int count = 0;
        // Starts are taken in ascending order, so every vertex gets visited.
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int top = 0;
            stack[top++] = s;
            seen[s] = true;
            // Each iteration either advances one cursor or pops one vertex, so the loop runs V + E times in total.
            while (top > 0) {
                int u = stack[top - 1];
                if (cursor[u] < out.get(u).size()) {
                    // Take the next outgoing edge and advance the cursor so the edge is never examined twice.
                    int v = out.get(u).get(cursor[u]++);
                    // Push only unvisited vertices, which bounds the stack at n entries.
                    if (!seen[v]) {
                        seen[v] = true;
                        stack[top++] = v;
                    }
                } else {
                    // All outgoing edges are done, so this vertex finishes now.
                    top--;
                    order[count++] = u;
                }
            }
        }
        return order;
    }

    /** Oracle: the textbook recursive search on small inputs. */
    static int[] oracle(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        List<Integer> order = new ArrayList<>();
        for (int s = 0; s < n; s++) visit(s, out, seen, order);
        int[] res = new int[n];
        for (int i = 0; i < n; i++) res[i] = order.get(i);
        return res;
    }

    static void visit(int u, List<List<Integer>> out, boolean[] seen, List<Integer> order) {
        if (seen[u]) return;
        seen[u] = true;
        for (int v : out.get(u)) visit(v, out, seen, order);
        order.add(u);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(finishOrder(4, new int[][] {{0, 1}, {1, 2}, {0, 2}, {2, 3}}), new int[] {3, 2, 1, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(finishOrder(5, new int[][] {{1, 0}, {0, 1}, {3, 4}, {2, 3}}), new int[] {1, 0, 4, 3, 2})) throw new AssertionError("ex2");
        // An empty edge list finishes the vertices in ascending order.
        if (!Arrays.equals(finishOrder(3, new int[0][]), new int[] {0, 1, 2})) throw new AssertionError("empty");
        // A self loop does not push its vertex twice.
        if (!Arrays.equals(finishOrder(2, new int[][] {{0, 0}, {0, 1}}), new int[] {1, 0})) throw new AssertionError("self");
        // A chain far deeper than the default call stack still works because the stack is explicit.
        int deep = 100_000;
        int[][] chain = new int[deep - 1][];
        for (int i = 0; i + 1 < deep; i++) chain[i] = new int[] {i, i + 1};
        int[] deepOrder = finishOrder(deep, chain);
        if (deepOrder[0] != deep - 1 || deepOrder[deep - 1] != 0) throw new AssertionError("deep");
        // The input array is not modified.
        int[][] keep = {{2, 1}, {1, 0}};
        finishOrder(3, keep);
        if (keep[0][0] != 2 || keep[0][1] != 1 || keep[1][0] != 1 || keep[1][1] != 0) throw new AssertionError("mutated");
        // Random graphs against the recursive oracle.
        Random rnd = new Random(2506);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(finishOrder(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Reverse-Graph Components (Author exercise)
<!-- id: ga-scc-reverse-components -->

**Approach.**
The method first computes the finish order of the original graph with the explicit-stack search from the previous solution. It then builds a second adjacency list in which every edge from `a` to `b` also appears from `b` to `a`. The second pass walks the finish order from the last entry to the first. A vertex that has no label yet receives the next label, and a search over the reversed lists gives the same label to every unlabeled vertex it reaches.

The invariant is that every search of the second pass starts in a component that has no unlabeled component pointing into it, so the search labels exactly that component. The reversed lists point from each component back toward its callers, and all callers are already labeled. A search over the original lists would leave the component and label vertices of later components.

**Complexity.**
- **Time** is O(V + E), because both passes touch each vertex and each edge a constant number of times.
- **Space** is O(V + E) for the two adjacency lists, plus O(V) for the order, the stack and the labels.

```java run
import java.util.*;

public final class SccReverseComponents {
    /**
     * Labels every vertex with its strongly connected component, numbering components in discovery order.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a search of the second pass stays inside one component because all edges into it come from labeled vertices.
     */
    static int[] labels(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        List<List<Integer>> back = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            out.add(new ArrayList<>());
            back.add(new ArrayList<>());
        }
        // Each edge a to b is stored forward for pass one and reversed for pass two.
        for (int[] e : edges) {
            out.get(e[0]).add(e[1]);
            back.get(e[1]).add(e[0]);
        }
        int[] order = finish(n, out);
        int[] label = new int[n];
        // The value minus one marks a vertex that no search has reached yet.
        Arrays.fill(label, -1);
        int next = 0;
        int[] stack = new int[n];
        // Walk the finish order from the latest finisher to the earliest.
        for (int i = n - 1; i >= 0; i--) {
            int s = order[i];
            // A labeled vertex belongs to a component that an earlier search has already collected.
            if (label[s] != -1) continue;
            int top = 0;
            stack[top++] = s;
            label[s] = next;
            // Each vertex is pushed once, so the second pass costs O(V + E) in total.
            while (top > 0) {
                int u = stack[--top];
                for (int v : back.get(u)) {
                    // Label on push so that no vertex enters the stack twice.
                    if (label[v] == -1) {
                        label[v] = next;
                        stack[top++] = v;
                    }
                }
            }
            // The next unlabeled start opens a new component.
            next++;
        }
        return label;
    }

    /** Finish order by an explicit-stack search over the given adjacency lists. */
    static int[] finish(int n, List<List<Integer>> out) {
        boolean[] seen = new boolean[n];
        int[] cursor = new int[n];
        int[] stack = new int[n];
        int[] order = new int[n];
        int count = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int top = 0;
            stack[top++] = s;
            seen[s] = true;
            while (top > 0) {
                int u = stack[top - 1];
                if (cursor[u] < out.get(u).size()) {
                    int v = out.get(u).get(cursor[u]++);
                    if (!seen[v]) {
                        seen[v] = true;
                        stack[top++] = v;
                    }
                } else {
                    top--;
                    order[count++] = u;
                }
            }
        }
        return order;
    }

    /** Oracle: u and v share a component exactly when each reaches the other in the transitive closure. */
    static boolean[][] closure(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int v = 0; v < n; v++) r[v][v] = true;
        for (int[] e : edges) r[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(labels(6, new int[][] {{0, 1}, {1, 2}, {2, 0}, {2, 3}, {3, 4}, {4, 3}, {5, 4}}), new int[] {1, 1, 1, 2, 2, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(labels(4, new int[][] {{3, 2}, {2, 3}, {1, 0}, {0, 1}, {2, 1}}), new int[] {1, 1, 0, 0})) throw new AssertionError("ex2");
        // Searching the original lists in pass two merges components, which shows why the lists are reversed.
        int[][] hazard = {{0, 1}, {1, 0}, {1, 2}, {2, 3}, {3, 2}, {3, 4}};
        int[] right = labels(5, hazard);
        if (right[0] == right[2] || right[2] == right[4]) throw new AssertionError("hazard setup");
        // Random graphs: same partition as the closure, and labels are consecutive from zero.
        Random rnd = new Random(2507);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[] got = labels(n, edges);
            boolean[][] r = closure(n, edges);
            int max = -1;
            for (int u = 0; u < n; u++) {
                max = Math.max(max, got[u]);
                for (int v = 0; v < n; v++) {
                    boolean same = r[u][v] && r[v][u];
                    if (same != (got[u] == got[v])) throw new AssertionError("random " + t);
                }
            }
            // Labels 0..max are all used, so they are consecutive.
            boolean[] used = new boolean[max + 1];
            for (int x : got) used[x] = true;
            for (boolean b : used) if (!b) throw new AssertionError("gap " + t);
        }
    }
}
```

#### Solution: [Boundary] Singleton And One-Way Edge (Author exercise)
<!-- id: ga-scc-singleton-one-way -->

**Approach.**
The method runs the two passes and counts how many vertices each label receives. Components of size one are then counted. A one-way edge from `a` to `b` lets `a` reach `b`, but `b` cannot return, so the two vertices end in separate components. A self loop on `a` gives `a` a path to itself, which every vertex already has, so it does not join `a` to anyone else.

The invariant is that two vertices share a label only when the second pass reaches one from the other on the reversed lists. The order of the first pass guarantees that such a reach stays inside one component. A one-way edge points from the earlier finisher to the later one, so the reversed list does not lead back across it. The self loop adds no new vertex to any search because its endpoint is already labeled.

**Complexity.**
- **Time** is O(V + E), because the two passes dominate and the count is one scan of the labels.
- **Space** is O(V + E) for the adjacency lists, plus O(V) for the order, the labels and the size counters.

```java run
import java.util.*;

public final class SccSingletons {
    /**
     * Counts the components that contain exactly one vertex.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: two vertices share a label only when each reaches the other.
     */
    static int singletons(int n, int[][] edges) {
        int[][] out = adjacency(n, edges, false);
        int[][] back = adjacency(n, edges, true);
        // Pass one: the finish order of the original graph.
        int[] order = new int[n];
        boolean[] seen = new boolean[n];
        int[] cursor = new int[n];
        int[] stack = new int[n];
        int count = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int top = 0;
            stack[top++] = s;
            seen[s] = true;
            while (top > 0) {
                int u = stack[top - 1];
                if (cursor[u] < out[u].length) {
                    int v = out[u][cursor[u]++];
                    if (!seen[v]) {
                        seen[v] = true;
                        stack[top++] = v;
                    }
                } else {
                    top--;
                    order[count++] = u;
                }
            }
        }
        // Pass two: size[c] counts the vertices that component c collects.
        boolean[] done = new boolean[n];
        int[] size = new int[n];
        int comps = 0;
        // Walk the order from the latest finisher to the earliest.
        for (int i = n - 1; i >= 0; i--) {
            int s = order[i];
            if (done[s]) continue;
            int top = 0;
            stack[top++] = s;
            done[s] = true;
            while (top > 0) {
                int u = stack[--top];
                // Every popped vertex joins the current component exactly once.
                size[comps]++;
                for (int v : back[u]) {
                    if (!done[v]) {
                        done[v] = true;
                        stack[top++] = v;
                    }
                }
            }
            comps++;
        }
        // Count the components that collected a single vertex.
        int alone = 0;
        for (int c = 0; c < comps; c++) if (size[c] == 1) alone++;
        return alone;
    }

    /** Builds out-lists, or in-lists when flip is true. */
    static int[][] adjacency(int n, int[][] edges, boolean flip) {
        int[] deg = new int[n];
        for (int[] e : edges) deg[flip ? e[1] : e[0]]++;
        int[][] g = new int[n][];
        for (int v = 0; v < n; v++) g[v] = new int[deg[v]];
        int[] fill = new int[n];
        for (int[] e : edges) {
            int from = flip ? e[1] : e[0];
            int to = flip ? e[0] : e[1];
            g[from][fill[from]++] = to;
        }
        return g;
    }

    /** Oracle: a vertex is alone when no other vertex is mutually reachable with it. */
    static int oracle(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int v = 0; v < n; v++) r[v][v] = true;
        for (int[] e : edges) r[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        int alone = 0;
        for (int u = 0; u < n; u++) {
            boolean partner = false;
            for (int v = 0; v < n; v++) if (v != u && r[u][v] && r[v][u]) partner = true;
            if (!partner) alone++;
        }
        return alone;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (singletons(3, new int[][] {{0, 1}, {1, 2}}) != 3) throw new AssertionError("ex1");
        if (singletons(4, new int[][] {{0, 0}, {1, 2}, {2, 1}, {2, 3}}) != 2) throw new AssertionError("ex2");
        // One vertex and no edges is one singleton.
        if (singletons(1, new int[0][]) != 1) throw new AssertionError("single");
        // A self loop alone does not merge anything.
        if (singletons(2, new int[][] {{0, 0}, {1, 1}}) != 2) throw new AssertionError("loops");
        // A two-cycle removes both vertices from the count.
        if (singletons(2, new int[][] {{0, 1}, {1, 0}}) != 0) throw new AssertionError("pair");
        // Random graphs against the closure oracle.
        Random rnd = new Random(2508);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (singletons(n, edges) != oracle(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Condensation DAG (Author exercise)
<!-- id: ga-scc-condensation-dag -->

**Approach.**
The method labels every vertex with its component, using the two passes of this lesson. It then scans the edges. An edge whose endpoints carry different labels becomes a pair of labels, and a hash set stores each pair once, so parallel edges between two components count once. The method ignores an edge inside one component. The method counts the pairs and counts the labels that never appear as the target of a pair, which are the components that nothing points into.

The invariant is that the condensed graph has no cycle. If two components lay on a cycle, every vertex of one would reach every vertex of the other and back, so the two components would be one. The test harness checks this claim with a topological sort that consumes every component of the condensed graph.

**Complexity.**
- **Time** is O(V + E) on average, because the two passes are linear and each edge makes one expected O(1) hash insertion.
- **Space** is O(V + E) for the lists, the labels and the set of distinct pairs.

```java run
import java.util.*;

public final class SccCondensation {
    /**
     * Returns {component count, distinct edges between components, components with no incoming edge}.
     * Time: O(V + E) expected. Space: O(V + E).
     * Invariant: the condensed graph has no cycle, because a cycle would merge its components.
     */
    static int[] summary(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int comps = 0;
        for (int x : label) comps = Math.max(comps, x + 1);
        // A pair key packs two labels into one long, so no boxing of arrays is needed.
        Set<Long> pairs = new HashSet<>();
        boolean[] hasIncoming = new boolean[comps];
        for (int[] e : edges) {
            int a = label[e[0]];
            int b = label[e[1]];
            // Edges inside a component disappear in the condensed graph.
            if (a == b) continue;
            // The set keeps one copy of each pair, so repeated edges count once.
            if (pairs.add((long) a * comps + b)) hasIncoming[b] = true;
        }
        int sources = 0;
        // A component with no incoming pair is a source of the condensed graph.
        for (boolean h : hasIncoming) if (!h) sources++;
        return new int[] {comps, pairs.size(), sources};
    }

    /** Kosaraju labels in discovery order of the second pass. */
    static int[] labels(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        List<List<Integer>> back = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            out.add(new ArrayList<>());
            back.add(new ArrayList<>());
        }
        for (int[] e : edges) {
            out.get(e[0]).add(e[1]);
            back.get(e[1]).add(e[0]);
        }
        boolean[] seen = new boolean[n];
        int[] cursor = new int[n];
        int[] stack = new int[n];
        int[] order = new int[n];
        int count = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int top = 0;
            stack[top++] = s;
            seen[s] = true;
            while (top > 0) {
                int u = stack[top - 1];
                if (cursor[u] < out.get(u).size()) {
                    int v = out.get(u).get(cursor[u]++);
                    if (!seen[v]) {
                        seen[v] = true;
                        stack[top++] = v;
                    }
                } else {
                    top--;
                    order[count++] = u;
                }
            }
        }
        int[] label = new int[n];
        Arrays.fill(label, -1);
        int next = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (label[order[i]] != -1) continue;
            int top = 0;
            stack[top++] = order[i];
            label[order[i]] = next;
            while (top > 0) {
                int u = stack[--top];
                for (int v : back.get(u)) {
                    if (label[v] == -1) {
                        label[v] = next;
                        stack[top++] = v;
                    }
                }
            }
            next++;
        }
        return label;
    }

    /** Oracle: components from the transitive closure, then a set of component pairs. */
    static int[] oracle(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int v = 0; v < n; v++) r[v][v] = true;
        for (int[] e : edges) r[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        // The smallest vertex of each component serves as its name.
        int[] rep = new int[n];
        for (int u = 0; u < n; u++) {
            rep[u] = u;
            for (int v = 0; v < u; v++) if (r[u][v] && r[v][u]) { rep[u] = v; break; }
        }
        Set<String> pairs = new HashSet<>();
        Set<Integer> names = new HashSet<>();
        Set<Integer> targets = new HashSet<>();
        for (int u = 0; u < n; u++) names.add(rep[u]);
        for (int[] e : edges) {
            if (rep[e[0]] != rep[e[1]]) {
                pairs.add(rep[e[0]] + ":" + rep[e[1]]);
                targets.add(rep[e[1]]);
            }
        }
        return new int[] {names.size(), pairs.size(), names.size() - targets.size()};
    }

    /** Harness check: a topological sort consumes every component of the condensed graph. */
    static boolean isAcyclic(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int comps = 0;
        for (int x : label) comps = Math.max(comps, x + 1);
        List<List<Integer>> g = new ArrayList<>();
        for (int c = 0; c < comps; c++) g.add(new ArrayList<>());
        int[] indeg = new int[comps];
        for (int[] e : edges) {
            if (label[e[0]] != label[e[1]]) {
                g.get(label[e[0]]).add(label[e[1]]);
                indeg[label[e[1]]]++;
            }
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int c = 0; c < comps; c++) if (indeg[c] == 0) ready.add(c);
        int taken = 0;
        while (!ready.isEmpty()) {
            int c = ready.poll();
            taken++;
            for (int d : g.get(c)) if (--indeg[d] == 0) ready.add(d);
        }
        return taken == comps;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] e1 = {{0, 1}, {1, 0}, {1, 2}, {2, 3}, {3, 2}, {0, 2}, {1, 2}, {4, 5}, {5, 4}, {3, 4}};
        if (!Arrays.equals(summary(6, e1), new int[] {3, 2, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(3, new int[][] {{0, 1}, {0, 1}, {1, 0}, {2, 2}}), new int[] {2, 0, 2})) throw new AssertionError("ex2");
        // A hash set stores one copy of a repeated pair, which the count relies on.
        Set<Long> probe = new HashSet<>();
        if (!probe.add(5L) || probe.add(5L)) throw new AssertionError("set");
        // Random graphs: same summary as the oracle, and the condensed graph is acyclic.
        Random rnd = new Random(2509);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(16);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(summary(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
            if (!isAcyclic(n, edges)) throw new AssertionError("cycle " + t);
        }
    }
}
```
