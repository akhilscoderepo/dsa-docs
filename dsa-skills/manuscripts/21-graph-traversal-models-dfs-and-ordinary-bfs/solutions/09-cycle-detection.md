<!-- solutions-for: 09-cycle-detection -->
### Solutions For Cycle Detection

#### Solution: [Build] Undirected Parent Check (Author exercise)
<!-- id: gt-undirected-parent-check -->

**Approach.**
The method builds an adjacency list that stores each edge in both lists and runs a DFS from every unmarked vertex. Each call receives the vertex it was entered from. The neighbor equal to that parent is the edge just used, so the call skips it. Any other neighbor that is already marked closes a route that has not been used, so the call reports a cycle. Because the graph has no parallel edges, the parent vertex identifies the used edge exactly.

Throughout the search, every marked vertex that is not the parent of the current call lies on a real cycle with the current vertex.

**Complexity.**
- **Time** is O(n + m), because each vertex is entered once and each list entry is read once.
- **Space** is O(n + m), because the lists hold 2m entries and the recursion reaches depth n on a path.

```java run
import java.util.*;

public final class UndirectedParentCheck {
    /**
     * Returns true when the simple undirected graph contains a cycle.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: a marked neighbor that is not the parent closes an unused route.
     */
    static boolean hasCycle(int n, int[][] edges) {
        // Both directions of every edge go into the lists, so memory is 2m entries.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        boolean[] visited = new boolean[n];
        // Restart loop: one call per component, n iterations in total.
        for (int s = 0; s < n; s++) {
            // -1 is the parent of a source, since no vertex has that number.
            if (!visited[s] && walk(adj, visited, s, -1)) return true;
        }
        return false;
    }

    private static boolean walk(List<List<Integer>> adj, boolean[] visited, int u, int parent) {
        // Mark on entry, so a later sight of u is detected.
        visited[u] = true;
        // Each list entry is read once over the whole search.
        for (int v : adj.get(u)) {
            // The edge back to the parent is the edge just used.
            if (v == parent) continue;
            // A marked non-parent neighbor proves a cycle; otherwise descend into the new vertex.
            if (visited[v] || walk(adj, visited, v, u)) return true;
        }
        return false;
    }

    /** Oracle: union-find; an edge whose ends are already joined closes a cycle. */
    static boolean brute(int n, int[][] edges) {
        int[] root = new int[n];
        for (int i = 0; i < n; i++) root[i] = i;
        for (int[] e : edges) {
            int a = e[0], b = e[1];
            while (root[a] != a) a = root[a];
            while (root[b] != b) b = root[b];
            if (a == b) return true;
            root[a] = b;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!hasCycle(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 1}, {3, 4}})) throw new AssertionError("ex1");
        if (hasCycle(5, new int[][] {{0, 1}, {1, 2}, {3, 4}})) throw new AssertionError("ex2");
        // A single edge is not a cycle, which shows the parent skip works.
        if (hasCycle(2, new int[][] {{0, 1}})) throw new AssertionError("single edge");
        // Random simple graphs must match the union-find oracle.
        Random rnd = new Random(2201);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if (rnd.nextInt(5) == 0) list.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            int[][] edges = list.toArray(new int[0][]);
            if (hasCycle(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Directed Three Colors (Author exercise)
<!-- id: gt-directed-three-colors -->

**Approach.**
The method stores each directed edge once and keeps one state per vertex, with 0 for unvisited, 1 for visiting and 2 for finished. A call sets its vertex to visiting on entry and to finished only after every neighbor is processed. An edge to a visiting vertex returns to the open route, so it proves a cycle. An edge to a finished vertex is skipped, because everything reachable from it was explored without a return to the open route. This rule keeps the diamond of Example 1 from being reported. A self-loop makes a vertex its own visiting neighbor, so it is found with no special case.

At every moment, the visiting vertices form exactly the route from the current source to the current vertex.

**Complexity.**
- **Time** is O(n + m), because each vertex is entered once and each directed edge is read once.
- **Space** is O(n + m), because the lists hold m entries, `state` holds n entries and the recursion reaches depth n.

```java run
import java.util.*;

public final class DirectedThreeColors {
    private static final int NEW = 0, OPEN = 1, DONE = 2;

    /**
     * Returns true when the directed graph has a directed cycle.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: vertices in state OPEN are exactly the current route from the source.
     */
    static boolean hasCycle(int n, int[][] edges) {
        // One list entry per directed edge: m entries in total.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        int[] state = new int[n];
        // Restart loop covers vertices that no earlier search reached.
        for (int s = 0; s < n; s++) {
            if (state[s] == NEW && visit(adj, state, s)) return true;
        }
        return false;
    }

    private static boolean visit(List<List<Integer>> adj, int[] state, int u) {
        // OPEN on entry: u joins the current route.
        state[u] = OPEN;
        for (int v : adj.get(u)) {
            // An edge to an OPEN vertex returns to the route, which is a cycle.
            if (state[v] == OPEN) return true;
            // A NEW vertex is explored; a DONE vertex is skipped because its subtree is complete.
            if (state[v] == NEW && visit(adj, state, v)) return true;
        }
        // DONE only after every neighbor is processed; an earlier write would hide the cycle test.
        state[u] = DONE;
        return false;
    }

    /** Oracle: transitive closure by repeated relaxation; a vertex that reaches itself lies on a cycle. */
    static boolean brute(int n, int[][] edges) {
        boolean[][] reach = new boolean[n][n];
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int i = 0; i < n; i++) if (reach[i][i]) return true;
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (hasCycle(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}})) throw new AssertionError("ex1 diamond");
        if (!hasCycle(4, new int[][] {{0, 1}, {1, 2}, {2, 0}, {3, 0}})) throw new AssertionError("ex2");
        // A self-loop is a cycle of length one.
        if (!hasCycle(1, new int[][] {{0, 0}})) throw new AssertionError("self-loop");
        // Direction matters: the same two vertices with one edge have no cycle.
        if (hasCycle(2, new int[][] {{0, 1}})) throw new AssertionError("one directed edge");
        // Random directed graphs must match the closure oracle.
        Random rnd = new Random(2202);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (hasCycle(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Two-Way Undirected Edge (Author exercise)
<!-- id: gt-two-way-undirected-edge -->

**Approach.**
Each undirected edge is stored twice, once in each list, and both stored entries carry the same edge index. The DFS passes the index of the edge by which a call was entered, and the call skips only that one index. A repeated pair has two different indexes, so the second copy is not skipped, and its far end is already marked. The method then reports the cycle of length two. A single edge has one index, so the return over it is skipped and no cycle is reported. Skipping by the parent vertex number would drop both copies and miss the cycle.

For each call, the only skipped list entry is the one edge that brought the search to the vertex.

**Complexity.**
- **Time** is O(n + m), because each vertex is entered once and each of the 2m list entries is read once.
- **Space** is O(n + m), because the lists store 2m pairs of a neighbor and an edge index, and the recursion reaches depth n.

```java run
import java.util.*;

public final class TwoWayUndirectedEdge {
    /**
     * Returns true when the undirected multigraph contains a cycle, with two parallel edges counting as one.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: the call for v skips only the list entry of the edge that entered v.
     */
    static boolean hasCycle(int n, int[][] edges) {
        // Each entry is {neighbor, edge index}; both directions of an edge share the index.
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int i = 0; i < edges.length; i++) {
            adj.get(edges[i][0]).add(new int[] {edges[i][1], i});
            adj.get(edges[i][1]).add(new int[] {edges[i][0], i});
        }
        boolean[] visited = new boolean[n];
        // The restart loop runs n times; -1 means no entering edge for a source.
        for (int s = 0; s < n; s++) {
            if (!visited[s] && walk(adj, visited, s, -1)) return true;
        }
        return false;
    }

    private static boolean walk(List<List<int[]>> adj, boolean[] visited, int u, int viaEdge) {
        visited[u] = true;
        for (int[] entry : adj.get(u)) {
            // Skip only the very edge that entered u, never another edge to the same vertex.
            if (entry[1] == viaEdge) continue;
            // A marked neighbor over a different edge closes a cycle.
            if (visited[entry[0]] || walk(adj, visited, entry[0], entry[1])) return true;
        }
        return false;
    }

    /** Oracle: counts vertices, edges and components; a multigraph is a forest only if m = n - components. */
    static boolean brute(int n, int[][] edges) {
        int[] root = new int[n];
        for (int i = 0; i < n; i++) root[i] = i;
        int components = n;
        for (int[] e : edges) {
            int a = root[e[0]], b = root[e[1]];
            if (a != b) {
                // Relabel every vertex of the merged component, which is slow but obviously correct.
                for (int i = 0; i < n; i++) if (root[i] == b) root[i] = a;
                components--;
            }
        }
        return edges.length != n - components;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (hasCycle(2, new int[][] {{0, 1}})) throw new AssertionError("ex1 single edge");
        if (!hasCycle(3, new int[][] {{0, 1}, {1, 0}, {1, 2}})) throw new AssertionError("ex2 repeated pair");
        // Two copies of the same orientation also form a cycle.
        if (!hasCycle(2, new int[][] {{0, 1}, {0, 1}})) throw new AssertionError("same orientation");
        // Random multigraphs without self-loops must match the counting oracle.
        Random rnd = new Random(2203);
        for (int t = 0; t < 800; t++) {
            int n = 2 + rnd.nextInt(6), m = rnd.nextInt(8);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n);
                edges[i] = new int[] {a, (a + 1 + rnd.nextInt(n - 1)) % n};
            }
            if (hasCycle(n, edges) != brute(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Course Schedule (LeetCode 207)
<!-- id: gt-course-schedule -->

**Approach.**
The entry `[a, b]` says that course `b` comes before course `a`, so the method adds the directed edge from `b` to `a`. The student can finish all courses exactly when this graph has no directed cycle. The method runs a three-state DFS with an explicit stack, so a long chain of courses cannot overflow the call stack. An array `next` stores how many neighbors of each vertex are already processed, so each stack step resumes where it stopped. A neighbor in the open state returns false, and a vertex whose neighbors are all processed becomes finished and leaves the stack.

The stack always holds exactly the vertices in the open state, in route order.

**Complexity.**
- **Time** is O(n + m), because each vertex is pushed once and each edge is read once through `next`.
- **Space** is O(n + m), because of the lists, the two arrays of size n and a stack of at most n vertices.

```java run
import java.util.*;

public final class CourseSchedule {
    /**
     * Returns true when all courses can be completed, meaning the prerequisite graph has no cycle.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: the stack holds exactly the vertices whose state is open, in route order.
     */
    static boolean canFinish(int numCourses, int[][] prerequisites) {
        // Entry [a, b] becomes the edge b to a, because b must be completed first.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] p : prerequisites) adj.get(p[1]).add(p[0]);
        // 0 new, 1 open, 2 finished; next[u] counts the neighbors of u already handled.
        int[] state = new int[numCourses], next = new int[numCourses];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int s = 0; s < numCourses; s++) {
            if (state[s] != 0) continue;
            state[s] = 1;
            stack.push(s);
            // Each loop turn either handles one edge or finishes one vertex: n + m turns in total.
            while (!stack.isEmpty()) {
                int u = stack.peek();
                if (next[u] < adj.get(u).size()) {
                    int v = adj.get(u).get(next[u]++);
                    // An edge to an open vertex returns to the route, so the courses cannot all be finished.
                    if (state[v] == 1) return false;
                    if (state[v] == 0) { state[v] = 1; stack.push(v); }
                } else {
                    // All neighbors are handled, so the vertex is finished and leaves the route.
                    state[u] = 2;
                    stack.pop();
                }
            }
        }
        return true;
    }

    /** Oracle: repeatedly remove a course with no remaining prerequisite; all removed means no cycle. */
    static boolean brute(int n, int[][] pre) {
        boolean[] done = new boolean[n];
        int removed = 0;
        for (boolean progress = true; progress; ) {
            progress = false;
            for (int c = 0; c < n; c++) {
                if (done[c]) continue;
                boolean free = true;
                for (int[] p : pre) if (p[0] == c && !done[p[1]]) free = false;
                if (free) { done[c] = true; removed++; progress = true; }
            }
        }
        return removed == n;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canFinish(3, new int[][] {{1, 0}, {2, 1}, {2, 0}})) throw new AssertionError("ex1");
        if (canFinish(4, new int[][] {{1, 0}, {2, 1}, {3, 2}, {1, 3}})) throw new AssertionError("ex2");
        // No prerequisites means every course can be taken.
        if (!canFinish(1, new int[0][])) throw new AssertionError("no prerequisites");
        // A long chain runs without a stack overflow because the stack is explicit.
        int len = 100000;
        int[][] chain = new int[len - 1][];
        for (int i = 1; i < len; i++) chain[i - 1] = new int[] {i, i - 1};
        if (!canFinish(len, chain)) throw new AssertionError("chain");
        // Random distinct pairs with a != b must match the removal oracle.
        Random rnd = new Random(2204);
        for (int t = 0; t < 800; t++) {
            int n = 2 + rnd.nextInt(6);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++)
                for (int b = 0; b < n; b++)
                    if (a != b && rnd.nextInt(6) == 0) list.add(new int[] {a, b});
            int[][] pre = list.toArray(new int[0][]);
            if (canFinish(n, pre) != brute(n, pre)) throw new AssertionError("random " + t);
        }
    }
}
```
