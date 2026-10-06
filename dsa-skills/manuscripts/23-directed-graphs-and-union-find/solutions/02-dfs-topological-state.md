<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For DFS Topological State

#### Solution: [Build] Three-Color Trace (Author exercise)
<!-- id: dg-three-color-trace -->

**Approach.**
The method builds an adjacency list in the order of `edges`, so the scan order of the neighbors is fixed. A recursive helper turns its vertex gray, stores `enter` from the shared clock and advances the clock. It then scans the neighbors and recurses only into white ones. Gray and black neighbors are read and skipped. After the loop it stores `exit`, advances the clock and turns the vertex black. The outer loop starts a helper at every vertex that is still white, in ascending order.

The invariant is that the clock equals the number of state changes made so far, and each vertex changes state twice. Both changes get distinct clock values, so the result holds every value from 0 to 2n - 1 once. Intervals of two vertices are either nested or disjoint, because a callee returns before its caller does. The skip of gray neighbors makes the method safe on cycles.

**Complexity.**
- **Time** is O(V + E), because each vertex has one call and each adjacency entry is read once.
- **Space** is O(V + E) for the adjacency list and the arrays, plus a call stack of at most V frames.

```java run
import java.util.*;

public final class ThreeColorTrace {
    /**
     * Returns {enter, exit} clock values for each vertex.
     * Time: O(V + E). Space: O(V + E), including the recursion depth.
     * Invariant: the clock counts the state changes made so far.
     */
    static int[][] times(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        int[] color = new int[n];
        int[][] out = new int[n][2];
        int[] clock = {0};
        // Every white vertex roots a new tree, in ascending order.
        for (int v = 0; v < n; v++) if (color[v] == 0) walk(adj, color, out, clock, v);
        return out;
    }

    private static void walk(List<List<Integer>> adj, int[] color, int[][] out, int[] clock, int cur) {
        // Entry: white becomes gray and the clock advances once.
        color[cur] = 1;
        out[cur][0] = clock[0]++;
        // Each adjacency entry is read once, which gives the O(E) term.
        for (int next : adj.get(cur)) {
            // Only a white neighbor needs a call; gray and black neighbors are skipped.
            if (color[next] == 0) walk(adj, color, out, clock, next);
        }
        // Exit: gray becomes black after every neighbor was scanned.
        color[cur] = 2;
        out[cur][1] = clock[0]++;
    }

    /** Oracle: the same search with an explicit stack and a next-neighbor index per vertex. */
    static int[][] oracle(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        int[][] out = new int[n][];
        int[] idx = new int[n];
        int clock = 0;
        for (int s = 0; s < n; s++) {
            if (out[s] != null) continue;
            ArrayDeque<Integer> stack = new ArrayDeque<>();
            out[s] = new int[] {clock++, -1};
            stack.push(s);
            while (!stack.isEmpty()) {
                int u = stack.peek();
                if (idx[u] < adj.get(u).size()) {
                    int v = adj.get(u).get(idx[u]++);
                    if (out[v] == null) { out[v] = new int[] {clock++, -1}; stack.push(v); }
                } else {
                    out[u][1] = clock++;
                    stack.pop();
                }
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(times(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}}), new int[][] {{0, 7}, {1, 4}, {5, 6}, {2, 3}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(times(3, new int[][] {{0, 1}, {1, 2}, {2, 0}}), new int[][] {{0, 5}, {1, 4}, {2, 3}})) throw new AssertionError("ex2");
        // Java fact: the postfix increment returns the old value, so enter gets the clock before the advance.
        int[] c = {5};
        if (c[0]++ != 5 || c[0] != 6) throw new AssertionError("postfix increment");
        // Random graphs with cycles, repeats and self loops against the explicit-stack search.
        Random rnd = new Random(2310);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] got = times(n, edges);
            if (!Arrays.deepEquals(got, oracle(n, edges))) throw new AssertionError("random " + t);
            // The 2n clock values are distinct.
            boolean[] used = new boolean[2 * n];
            for (int[] p : got) { used[p[0]] = true; used[p[1]] = true; }
            for (boolean u : used) if (!u) throw new AssertionError("clock values " + t);
        }
    }
}
```

#### Solution: [Vary] Postorder Topological List (Author exercise)
<!-- id: dg-postorder-list -->

**Approach.**
The method runs the three-state search of the previous exercise and adds one action. A vertex is appended to `post` only after the loop over its outgoing edges has ended. The method then copies `post` into the result from the last index to the first.

The invariant is that a vertex in `post` has every successor in `post` before it. An edge to a white successor starts a call that returns first, and an edge to a black successor reaches a vertex that is already in the list. The input has no cycle, so no edge reaches a gray vertex, and the invariant holds for every vertex. Reading the list from the back turns "successor before vertex" into "vertex before successor", which is the order condition. The scan order of neighbors fixes the result, so the exact examples are repeatable.

**Complexity.**
- **Time** is O(V + E), because the search reads each entry once and the copy costs O(V).
- **Space** is O(V + E) for the adjacency list, the colors and the list, plus the recursion depth.

```java run
import java.util.*;

public final class PostorderList {
    /**
     * Returns the reversed postorder of an acyclic graph.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a listed vertex has all successors listed before it.
     */
    static int[] reversePostorder(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] done = new boolean[n];
        boolean[] active = new boolean[n];
        List<Integer> post = new ArrayList<>();
        for (int v = 0; v < n; v++) if (!done[v] && !active[v]) dive(adj, done, active, post, v);
        // The copy reads the list from the back, which reverses the postorder.
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[i] = post.get(n - 1 - i);
        return out;
    }

    private static void dive(List<List<Integer>> adj, boolean[] done, boolean[] active, List<Integer> post, int cur) {
        active[cur] = true;
        // Every successor is finished once this loop ends.
        for (int next : adj.get(cur)) {
            if (!done[next] && !active[next]) dive(adj, done, active, post, next);
        }
        // The vertex joins the list only now, after all its successors.
        active[cur] = false;
        done[cur] = true;
        post.add(cur);
    }

    /** Oracle: an explicit-stack search that records finish order, plus a position check of every edge. */
    static void check(int n, int[][] edges, int[] got) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        int[] next = new int[n];
        int[] finish = new int[n];
        int fc = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            Deque<Integer> st = new ArrayDeque<>();
            seen[s] = true;
            st.push(s);
            while (!st.isEmpty()) {
                int u = st.peek();
                if (next[u] < adj.get(u).size()) {
                    int v = adj.get(u).get(next[u]++);
                    if (!seen[v]) { seen[v] = true; st.push(v); }
                } else {
                    finish[fc++] = u;
                    st.pop();
                }
            }
        }
        for (int i = 0; i < n; i++) if (got[i] != finish[n - 1 - i]) throw new AssertionError("differs from reference at " + i);
        int[] pos = new int[n];
        for (int i = 0; i < n; i++) pos[got[i]] = i;
        for (int[] e : edges) if (pos[e[0]] >= pos[e[1]]) throw new AssertionError("edge points backward");
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(reversePostorder(5, new int[][] {{4, 3}, {2, 1}, {1, 0}}), new int[] {4, 3, 2, 1, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(reversePostorder(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}}), new int[] {0, 2, 1, 3})) throw new AssertionError("ex2");
        // Random acyclic graphs: edges go forward in a random hidden ranking, with repeats.
        Random rnd = new Random(2311);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<Integer> rank = new ArrayList<>();
            for (int v = 0; v < n; v++) rank.add(v);
            Collections.shuffle(rank, rnd);
            List<int[]> es = new ArrayList<>();
            int m = rnd.nextInt(14);
            for (int i = 0; i < m && n > 1; i++) {
                int a = rnd.nextInt(n - 1);
                int b = a + 1 + rnd.nextInt(n - 1 - a);
                es.add(new int[] {rank.get(a), rank.get(b)});
            }
            int[][] edges = es.toArray(new int[0][]);
            check(n, edges, reversePostorder(n, edges));
        }
    }
}
```

#### Solution: [Boundary] Cross Edge To Black (Author exercise)
<!-- id: dg-cross-edge-black -->

**Approach.**
The method runs the search and inspects the state of the end vertex at every scan of an entry. A white end vertex starts a recursive call and counts nowhere. A black end vertex adds 1 to the black count, and the method takes no other action. A gray end vertex adds 1 to the gray count. The state of a self loop is gray, because the vertex turned gray on entry and has not turned black.

The invariant is that a vertex is gray exactly while its call is on the stack. A scan that finds a black vertex meets a vertex whose call already returned, so that vertex cannot reach the scanning vertex and no cycle follows. This includes the edge to a vertex of another finished tree, and the edge from an ancestor to a finished descendant. Repeated entries count once per scan, because each scan finds the state again.

**Complexity.**
- **Time** is O(V + E), because the method reads each entry once and each vertex starts one call.
- **Space** is O(V + E) for the adjacency list, the colors and the recursion depth.

```java run
import java.util.*;

public final class CrossEdgeBlack {
    private static int blackScans;
    private static int grayScans;

    /**
     * Returns {scans that find black, scans that find gray}.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a vertex is gray exactly while its call is on the stack.
     */
    static int[] classify(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        int[] color = new int[n];
        blackScans = 0;
        grayScans = 0;
        for (int v = 0; v < n; v++) if (color[v] == 0) explore(adj, color, v);
        return new int[] {blackScans, grayScans};
    }

    private static void explore(List<List<Integer>> adj, int[] color, int cur) {
        color[cur] = 1;
        // One scan per adjacency entry, which gives the O(E) term.
        for (int next : adj.get(cur)) {
            // A finished vertex is accepted and counted; it cannot lead back to cur.
            if (color[next] == 2) blackScans++;
            // A gray vertex is on the stack, so this entry is the evidence of a cycle.
            else if (color[next] == 1) grayScans++;
            else explore(adj, color, next);
        }
        color[cur] = 2;
    }

    /**
     * Oracle: explicit-stack search with time stamps and a tree-edge flag per entry.
     * A non-tree entry is gray when its end vertex is an ancestor of the start, or the start itself.
     */
    static int[] oracle(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) out.add(new ArrayList<>());
        for (int i = 0; i < edges.length; i++) out.get(edges[i][0]).add(i);
        int[] enter = new int[n];
        int[] exit = new int[n];
        Arrays.fill(enter, -1);
        boolean[] tree = new boolean[edges.length];
        int[] ptr = new int[n];
        int clock = 0;
        for (int s = 0; s < n; s++) {
            if (enter[s] >= 0) continue;
            Deque<Integer> st = new ArrayDeque<>();
            enter[s] = clock++;
            st.push(s);
            while (!st.isEmpty()) {
                int u = st.peek();
                if (ptr[u] < out.get(u).size()) {
                    int ei = out.get(u).get(ptr[u]++);
                    int v = edges[ei][1];
                    if (enter[v] < 0) { tree[ei] = true; enter[v] = clock++; st.push(v); }
                } else {
                    exit[u] = clock++;
                    st.pop();
                }
            }
        }
        int black = 0, gray = 0;
        for (int i = 0; i < edges.length; i++) {
            if (tree[i]) continue;
            int u = edges[i][0], v = edges[i][1];
            if (enter[v] <= enter[u] && exit[u] <= exit[v]) gray++; else black++;
        }
        return new int[] {black, gray};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(classify(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}}), new int[] {1, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(classify(4, new int[][] {{0, 1}, {1, 2}, {2, 1}, {0, 2}, {3, 0}}), new int[] {2, 1})) throw new AssertionError("ex2");
        // A self loop finds its own gray vertex.
        if (!Arrays.equals(classify(1, new int[][] {{0, 0}}), new int[] {0, 1})) throw new AssertionError("self loop");
        // Random graphs with repeats and self loops against the time-stamp classification.
        Random rnd = new Random(2312);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(classify(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Course Order With The Blocking Edge (LeetCode 210)
<!-- id: dg-course-order-edge -->

**Approach.**
The method turns each entry `[a, b]` into the edge from `b` to `a`, keeping the entry order for the scan. A recursive helper turns a course gray, scans its followers and returns true at the first gray follower, after it stores the pair of the scanned course and that follower. Otherwise it turns the course black and appends it to the postorder. The outer loop starts the helper at every white course in ascending order and stops at the first cycle report.

The invariant is that the helper reaches a gray follower only through an edge that closes a cycle with the call stack. The reported pair is the first such edge in scan order, and the early return keeps later edges from replacing it. Without a report, every black course has its followers appended before it, so the reversed postorder is a valid order. The result has two rows, and exactly one is nonempty, so the caller can distinguish both cases by the length of row 0.

**Complexity.**
- **Time** is O(V + E), because each course starts one call and each entry is read once.
- **Space** is O(V + E) for the adjacency list, the colors, the postorder and the recursion depth.

```java run
import java.util.*;

public final class CourseOrderEdge {
    private static int[] blocking;

    /**
     * Returns {order, blocking edge}; exactly one row is nonempty.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a gray follower closes a cycle with the call stack.
     */
    static int[][] orderOrEdge(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < numCourses; v++) adj.add(new ArrayList<>());
        // Entry [a, b] is the edge from b to a, stored in input order.
        for (int[] p : prerequisites) adj.get(p[1]).add(p[0]);
        int[] color = new int[numCourses];
        List<Integer> post = new ArrayList<>();
        blocking = new int[0];
        for (int v = 0; v < numCourses; v++) {
            // The first cycle report ends the whole search.
            if (color[v] == 0 && descend(adj, color, post, v)) return new int[][] {new int[0], blocking};
        }
        int[] order = new int[numCourses];
        for (int i = 0; i < numCourses; i++) order[i] = post.get(numCourses - 1 - i);
        return new int[][] {order, new int[0]};
    }

    private static boolean descend(List<List<Integer>> adj, int[] color, List<Integer> post, int cur) {
        color[cur] = 1;
        for (int next : adj.get(cur)) {
            // A gray follower is on the call stack, so store the scanned pair and stop.
            if (color[next] == 1) { blocking = new int[] {cur, next}; return true; }
            if (color[next] == 0 && descend(adj, color, post, next)) return true;
        }
        // All followers are finished, so the course is appended and turns black.
        color[cur] = 2;
        post.add(cur);
        return false;
    }

    /** Oracle: closure test for cycles, then the same search with an explicit stack for the exact output. */
    static void check(int n, int[][] pre, int[][] got) {
        boolean[][] reach = new boolean[n][n];
        for (int[] p : pre) reach[p[1]][p[0]] = true;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        boolean cyclic = false;
        for (int v = 0; v < n; v++) if (reach[v][v]) cyclic = true;
        if (got.length != 2) throw new AssertionError("two rows");
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] p : pre) adj.get(p[1]).add(p[0]);
        int[] color = new int[n];
        int[] ptr = new int[n];
        List<Integer> post = new ArrayList<>();
        int[] edge = null;
        outer:
        for (int s = 0; s < n; s++) {
            if (color[s] != 0) continue;
            Deque<Integer> st = new ArrayDeque<>();
            color[s] = 1;
            st.push(s);
            while (!st.isEmpty()) {
                int u = st.peek();
                if (ptr[u] < adj.get(u).size()) {
                    int v = adj.get(u).get(ptr[u]++);
                    if (color[v] == 1) { edge = new int[] {u, v}; break outer; }
                    if (color[v] == 0) { color[v] = 1; st.push(v); }
                } else {
                    color[u] = 2;
                    post.add(u);
                    st.pop();
                }
            }
        }
        if ((edge != null) != cyclic) throw new AssertionError("cycle flag");
        if (cyclic) {
            if (got[0].length != 0 || !Arrays.equals(got[1], edge)) throw new AssertionError("blocking edge");
            // The pair must be a real entry, and its end must reach its start.
            boolean real = false;
            for (int[] p : pre) if (p[1] == got[1][0] && p[0] == got[1][1]) real = true;
            if (!real || (got[1][0] != got[1][1] && !reach[got[1][1]][got[1][0]])) throw new AssertionError("pair is not on a cycle");
        } else {
            if (got[1].length != 0 || got[0].length != n) throw new AssertionError("order row");
            for (int i = 0; i < n; i++) if (got[0][i] != post.get(n - 1 - i)) throw new AssertionError("order differs");
            int[] pos = new int[n];
            for (int i = 0; i < n; i++) pos[got[0][i]] = i;
            for (int[] p : pre) if (pos[p[1]] >= pos[p[0]]) throw new AssertionError("entry violated");
        }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(orderOrEdge(5, new int[][] {{1, 3}, {0, 1}, {2, 3}, {4, 0}}), new int[][] {{3, 2, 1, 0, 4}, {}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(orderOrEdge(4, new int[][] {{1, 0}, {2, 1}, {3, 2}, {1, 3}}), new int[][] {{}, {3, 1}})) throw new AssertionError("ex2");
        // A self entry reports the pair of one course with itself.
        if (!Arrays.deepEquals(orderOrEdge(2, new int[][] {{1, 1}}), new int[][] {{}, {1, 1}})) throw new AssertionError("self entry");
        // Random graphs with cycles, repeats and self entries.
        Random rnd = new Random(2313);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(10);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) pre[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            check(n, pre, orderOrEdge(n, pre));
        }
    }
}
```
