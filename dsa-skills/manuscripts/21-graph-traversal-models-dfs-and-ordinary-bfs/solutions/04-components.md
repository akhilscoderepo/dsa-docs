<!-- solutions-for: 04-components -->
### Solutions For Components

#### Solution: [Build] Count Components (Author exercise)
<!-- id: gt-count-components -->

**Approach.**
The method builds the adjacency list, with each undirected edge entered in both directions, and creates one `visited` array for the whole run. The outer loop walks the vertex numbers in order. A marked vertex belongs to a component that an earlier start found, so the loop skips it. An unmarked vertex opens a new component, so the method adds 1 to the counter and runs a search that marks everything reachable from that vertex.

The search uses an explicit stack and marks each vertex when it pushes it, so no vertex enters the stack twice. The invariant is that after the loop handles vertex `s`, every component that contains a vertex up to `s` is fully marked. The counter equals the number of those components. The search cannot leave its component, because no edge crosses a component boundary, so each start adds exactly one component.

**Complexity.**
- **Time** is O(n + m) for `m` edges, because the outer loop makes n checks and the searches together read each of the 2m adjacency entries once.
- **Space** is O(n + m), because the adjacency list stores 2m entries and the stack and `visited` hold at most n entries each.

```java run
import java.util.*;

public final class CountComponents {
    /**
     * Returns the number of components of an undirected graph.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: every start on an unmarked vertex marks exactly one whole new component.
     */
    static int count(int n, int[][] edges) {
        // Build the adjacency list; each edge contributes two entries.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // One visited array for the whole run; resetting it per start would recount vertices.
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        int components = 0;
        // The outer loop makes n checks, one per vertex number.
        for (int start = 0; start < n; start++) {
            // A marked vertex is part of a component that an earlier start found.
            if (visited[start]) continue;
            // An unmarked start has no earlier discoverer, so it opens a new component.
            components++;
            visited[start] = true;
            stack.push(start);
            // The search marks the whole component; across all starts each vertex is pushed once.
            while (!stack.isEmpty()) {
                int v = stack.pop();
                // Each adjacency entry is read once over the whole run, which gives the O(m) term.
                for (int w : adj.get(v)) {
                    if (!visited[w]) { visited[w] = true; stack.push(w); }
                }
            }
        }
        // The counter holds one unit per search that the outer loop launched.
        return components;
    }

    /** Oracle: transitive closure of the symmetric edge relation, then count distinct smallest members. */
    static int brute(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int i = 0; i < n; i++) r[i][i] = true;
        for (int[] e : edges) { r[e[0]][e[1]] = true; r[e[1]][e[0]] = true; }
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (r[i][k] && r[k][j]) r[i][j] = true;
        int c = 0;
        // A vertex is the smallest of its component when no smaller vertex reaches it.
        for (int v = 0; v < n; v++) {
            boolean smallest = true;
            for (int u = 0; u < v; u++) if (r[u][v]) smallest = false;
            if (smallest) c++;
        }
        return c;
    }

    /** Naive method from the lesson: one search from vertex 0, every unreached vertex counted alone. */
    static int groupsFromVertexZero(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        markReachable(adj, visited, 0);
        int unreached = 0;
        for (boolean seen : visited) if (!seen) unreached++;
        return 1 + unreached;
    }

    static void markReachable(List<List<Integer>> adj, boolean[] visited, int v) {
        visited[v] = true;
        for (int w : adj.get(v)) if (!visited[w]) markReachable(adj, visited, w);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(5, new int[][] {{0, 1}, {1, 2}, {3, 4}}) != 2) throw new AssertionError("ex1");
        if (count(6, new int[][] {{0, 1}, {2, 3}, {3, 4}}) != 3) throw new AssertionError("ex2");
        // The lesson graph: three components, while the one-search method answers 4.
        int[][] lesson = {{0, 1}, {1, 2}, {3, 4}};
        if (count(6, lesson) != 3) throw new AssertionError("lesson graph");
        if (groupsFromVertexZero(6, lesson) != 4) throw new AssertionError("naive answer");
        // A second graph from the trace: a cycle, a path and one single vertex.
        if (count(7, new int[][] {{0, 6}, {2, 6}, {1, 4}, {4, 5}, {5, 1}}) != 3) throw new AssertionError("trace graph");
        // Edge cases: one vertex, no edges, parallel edges.
        if (count(1, new int[0][]) != 1) throw new AssertionError("one vertex");
        if (count(5, new int[0][]) != 5) throw new AssertionError("all isolated");
        if (count(2, new int[][] {{0, 1}, {1, 0}}) != 1) throw new AssertionError("parallel edges");
        // Random graphs: the count must equal the oracle on 3000 cases.
        Random rnd = new Random(2107);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), m = n == 1 ? 0 : rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            if (count(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Component Sizes (Author exercise)
<!-- id: gt-component-sizes -->

**Approach.**
The method keeps the outer loop of the previous solution. For every unmarked start it runs a breadth-first search and counts the vertices that the search marks. It then appends that count to a list of sizes. The outer loop reaches the smallest vertex of each component first, because every smaller vertex of that component would have been reached earlier and marked the whole component. The order of the list therefore matches the order that the problem asks for.

The invariant is that the sizes already stored belong to complete components, and their sum equals the number of marked vertices. Each search ends only after it has marked its whole component, so no size is partial.

**Complexity.**
- **Time** is O(n + m), because the outer loop and the searches read each vertex and adjacency entry a constant number of times.
- **Space** is O(n + m), because of the adjacency list, the queue and the list of at most n sizes.

```java run
import java.util.*;

public final class ComponentSizes {
    /**
     * Returns the component sizes, ordered by the smallest vertex of each component.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: the stored sizes describe complete components, and their sum equals the marked count.
     */
    static int[] sizes(int n, int[][] edges) {
        // Adjacency list with both directions of each edge.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        List<Integer> found = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Increasing vertex numbers make the first vertex of each component its smallest vertex.
        for (int start = 0; start < n; start++) {
            // A marked start belongs to a recorded component.
            if (visited[start]) continue;
            visited[start] = true;
            queue.add(start);
            // Counts the vertices this search marks, which is the size of the new component.
            int size = 0;
            while (!queue.isEmpty()) {
                int v = queue.poll();
                size++;
                // Mark at the moment of adding, so the queue holds each vertex once.
                for (int w : adj.get(v)) if (!visited[w]) { visited[w] = true; queue.add(w); }
            }
            // The search is finished, so the size is complete and the list order follows the starts.
            found.add(size);
        }
        // Copy into an int array in the same order.
        int[] out = new int[found.size()];
        for (int i = 0; i < out.length; i++) out[i] = found.get(i);
        return out;
    }

    /** Oracle: label vertices by repeated relaxation of the smallest reachable label. */
    static int[] brute(int n, int[][] edges) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                int m = Math.min(label[e[0]], label[e[1]]);
                if (label[e[0]] != m) { label[e[0]] = m; changed = true; }
                if (label[e[1]] != m) { label[e[1]] = m; changed = true; }
            }
        }
        // A vertex whose label equals its own number is the smallest of its component.
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            if (label[v] != v) continue;
            int c = 0;
            for (int u = 0; u < n; u++) if (label[u] == v) c++;
            out.add(c);
        }
        int[] a = new int[out.size()];
        for (int i = 0; i < a.length; i++) a[i] = out.get(i);
        return a;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(sizes(6, new int[][] {{0, 1}, {3, 4}, {4, 5}}), new int[] {2, 1, 3})) throw new AssertionError("ex1");
        if (!Arrays.equals(sizes(5, new int[][] {{4, 0}, {0, 3}}), new int[] {3, 1, 1})) throw new AssertionError("ex2");
        // The sizes always add up to n, and the lesson graph gives 3, 2 and 1.
        int[] s = sizes(6, new int[][] {{0, 1}, {1, 2}, {3, 4}});
        if (!Arrays.equals(s, new int[] {3, 2, 1})) throw new AssertionError("lesson graph");
        // Random graphs: sizes must equal the oracle on 3000 cases, and their sum must be n.
        Random rnd = new Random(2108);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), m = n == 1 ? 0 : rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            int[] got = sizes(n, edges);
            if (!Arrays.equals(got, brute(n, edges))) throw new AssertionError("random " + t);
            int sum = 0;
            for (int z : got) sum += z;
            if (sum != n) throw new AssertionError("sum " + t);
        }
    }
}
```

#### Solution: [Boundary] No Edges And One Component (Author exercise)
<!-- id: gt-no-edges-one-component -->

**Approach.**
Let `c` be the number of components. One added edge joins at most two components, so it lowers the component count by at most 1, and at least `c - 1` additions are necessary. The count `c - 1` is also enough, because an edge from a vertex of the first component to a vertex of each other component joins them all. The method therefore counts components and returns `c - 1`.

The two extremes behave as the boundary requires. A graph with no edges has `n` components and needs `n - 1` additions. A graph with one component needs 0. The invariant is that the outer loop starts one search per component, and the loop never starts a search inside a marked component.

**Complexity.**
- **Time** is O(n + m), because the count of components needs one pass over the vertices and the adjacency entries.
- **Space** is O(n + m), because of the adjacency list, the stack and `visited`.

```java run
import java.util.*;

public final class NoEdgesOneComponent {
    /**
     * Returns the smallest number of added edges that makes the graph connected.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: one search starts per component, so the counter equals the component count.
     */
    static int edgesToAdd(int n, int[][] edges) {
        // Adjacency list with both directions of each edge.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        int components = 0;
        // Each unmarked vertex starts a search, and that search marks its whole component.
        for (int start = 0; start < n; start++) {
            if (visited[start]) continue;
            components++;
            visited[start] = true;
            stack.push(start);
            while (!stack.isEmpty()) {
                int v = stack.pop();
                for (int w : adj.get(v)) if (!visited[w]) { visited[w] = true; stack.push(w); }
            }
        }
        // Each added edge merges at most two components, so c - 1 additions are necessary and enough.
        return components - 1;
    }

    /** Oracle: try every set of added edges in order of size, for tiny graphs, and test connectivity directly. */
    static int brute(int n, int[][] edges) {
        List<int[]> pairs = new ArrayList<>();
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) pairs.add(new int[] {i, j});
        for (int k = 0; k <= pairs.size(); k++) {
            // Mask enumerates subsets of the candidate pairs; only subsets with exactly k bits count.
            for (int mask = 0; mask < (1 << pairs.size()); mask++) {
                if (Integer.bitCount(mask) != k) continue;
                boolean[][] r = new boolean[n][n];
                for (int i = 0; i < n; i++) r[i][i] = true;
                for (int[] e : edges) { r[e[0]][e[1]] = true; r[e[1]][e[0]] = true; }
                for (int b = 0; b < pairs.size(); b++) if ((mask >> b & 1) == 1) { r[pairs.get(b)[0]][pairs.get(b)[1]] = true; r[pairs.get(b)[1]][pairs.get(b)[0]] = true; }
                for (int x = 0; x < n; x++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (r[i][x] && r[x][j]) r[i][j] = true;
                boolean connected = true;
                for (int v = 0; v < n; v++) if (!r[0][v]) connected = false;
                if (connected) return k;
            }
        }
        throw new AssertionError("unreachable");
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (edgesToAdd(4, new int[0][]) != 3) throw new AssertionError("ex1");
        int[][] complete = {{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}};
        if (edgesToAdd(4, complete) != 0) throw new AssertionError("ex2");
        // A single vertex is already one component.
        if (edgesToAdd(1, new int[0][]) != 0) throw new AssertionError("one vertex");
        // Random tiny graphs: the formula must equal the exhaustive oracle on 600 cases.
        Random rnd = new Random(2109);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(5), m = n == 1 ? 0 : rnd.nextInt(6);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            if (edgesToAdd(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Number of Provinces (LeetCode 547)
<!-- id: gt-number-of-provinces -->

**Approach.**
Each city is a vertex, and `isConnected[i][j] = 1` is an edge between `i` and `j`. The matrix is the adjacency matrix, so the neighbors of city `i` are the columns `j` of row `i` that hold 1 and differ from `i`. The method runs the outer loop over the cities with one `visited` array. An unmarked city starts a depth-first search and adds 1 to the province count. The search marks each city on entry and recurses into every unmarked neighbor in the row.

The invariant is that an unmarked start finds exactly one new province, because the search reaches all cities joined by a chain of roads and no others. The diagonal entry is 1 for every city, so the scan marks the city before it reads its row and the self entry finds a marked city.

**Complexity.**
- **Time** is O(n^2), because every city is entered once and each entry scans a full row of n cells.
- **Space** is O(n), because `visited` holds n entries and the recursion reaches depth n on a chain of cities.

```java run
import java.util.*;

public final class NumberOfProvinces {
    /**
     * Returns the number of provinces described by an adjacency matrix.
     * Time: O(n^2). Space: O(n).
     * Invariant: each start on an unmarked city marks exactly one whole province.
     */
    static int provinces(int[][] isConnected) {
        int n = isConnected.length;
        // One visited array for the whole loop, so a province is counted once.
        boolean[] visited = new boolean[n];
        int count = 0;
        // The outer loop checks each city once.
        for (int city = 0; city < n; city++) {
            // A marked city belongs to a province that an earlier start found.
            if (visited[city]) continue;
            // An unmarked city opens a new province.
            count++;
            enter(isConnected, visited, city);
        }
        return count;
    }

    // Marks city c on entry, then scans the row of c for roads; each row is scanned once, which costs O(n^2) overall.
    private static void enter(int[][] m, boolean[] visited, int c) {
        // The mark comes before the scan, so the diagonal entry of c finds c already marked.
        visited[c] = true;
        for (int d = 0; d < m.length; d++) {
            // A road to an unmarked city extends the province; marked cities add nothing.
            if (m[c][d] == 1 && !visited[d]) enter(m, visited, d);
        }
    }

    /** Oracle: transitive closure of the road relation, then count the smallest city of each province. */
    static int brute(int[][] m) {
        int n = m.length;
        boolean[][] r = new boolean[n][n];
        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) r[i][j] = m[i][j] == 1;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (r[i][k] && r[k][j]) r[i][j] = true;
        int c = 0;
        for (int v = 0; v < n; v++) {
            boolean smallest = true;
            for (int u = 0; u < v; u++) if (r[u][v]) smallest = false;
            if (smallest) c++;
        }
        return c;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (provinces(new int[][] {{1, 0, 0, 1}, {0, 1, 0, 0}, {0, 0, 1, 0}, {1, 0, 0, 1}}) != 3) throw new AssertionError("ex1");
        if (provinces(new int[][] {{1, 1, 1}, {1, 1, 1}, {1, 1, 1}}) != 1) throw new AssertionError("ex2");
        // One city is one province, and an identity matrix has n provinces.
        if (provinces(new int[][] {{1}}) != 1) throw new AssertionError("one city");
        if (provinces(new int[][] {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}) != 3) throw new AssertionError("identity");
        // Random symmetric matrices with a full diagonal must match the oracle on 3000 cases.
        Random rnd = new Random(2110);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] m = new int[n][n];
            for (int i = 0; i < n; i++) {
                m[i][i] = 1;
                for (int j = i + 1; j < n; j++) { int bit = rnd.nextInt(4) == 0 ? 1 : 0; m[i][j] = bit; m[j][i] = bit; }
            }
            if (provinces(m) != brute(m)) throw new AssertionError("random " + t);
        }
    }
}
```
