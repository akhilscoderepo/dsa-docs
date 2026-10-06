<!-- solutions-for: 03-visited-state -->
### Solutions For Visited State

#### Solution: [Build] Reachable Vertices (Author exercise)
<!-- id: gt-reachable-vertices -->

**Approach.**
The method builds the adjacency list from the edge array and adds each undirected edge in both directions. It marks the source, adds it to the queue and then repeats one step: take the oldest vertex, scan its neighbors and, for each neighbor that is not marked, mark the neighbor and add it to the queue. Marking happens in the same step as adding, so no vertex enters the queue twice.

The invariant is that every vertex in the queue is marked, and every marked vertex was added exactly once. When the queue empties, every marked vertex has a path from the source. An unmarked vertex has none, because a path would have to leave the marked set through an edge that the scan inspected. The final loop reads the marked vertices in increasing order.

**Complexity.**
- **Time** is O(n + m) for `m` edges, because each vertex leaves the queue once and each adjacency entry is read once.
- **Space** is O(n + m), because the adjacency list stores two entries per edge and the array and queue hold at most n entries.

```java run
import java.util.*;

public final class ReachableVertices {
    /**
     * Returns every vertex reachable from source, in increasing order.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: each queued vertex is marked, and each vertex enters the queue at most once.
     */
    static int[] reachable(int n, int[][] edges, int source) {
        // One list per vertex; building all lists costs O(n) time and memory.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // An undirected edge becomes two adjacency entries, so the lists hold 2m entries.
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // A new boolean array starts all false, so no vertex is marked yet.
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Mark the source before the loop so no neighbor can add it again.
        visited[source] = true;
        queue.add(source);
        int count = 1;
        // Each vertex leaves the queue once, because each was added once.
        while (!queue.isEmpty()) {
            // poll removes the head, so the oldest scheduled vertex expands first.
            int v = queue.poll();
            // Each adjacency entry is read once over the whole run, which gives the O(m) term.
            for (int w : adj.get(v)) {
                // A marked neighbor is already scheduled, so skip it.
                if (visited[w]) continue;
                // Mark and add in one step, so the gap that causes duplicates never opens.
                visited[w] = true;
                queue.add(w);
                count++;
            }
        }
        // Collect the marked vertices in increasing order with one scan of the array.
        int[] out = new int[count];
        int k = 0;
        for (int v = 0; v < n; v++) if (visited[v]) out[k++] = v;
        return out;
    }

    /** Naive BFS from the lesson: marks when a vertex leaves the queue and returns the number of expansions. */
    static int expansionsMarkAtDequeue(List<List<Integer>> adj, int source) {
        // Marks arrive late, so duplicates can wait in the queue.
        boolean[] visited = new boolean[adj.size()];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(source);
        int expansions = 0;
        // Every queue entry is expanded, including duplicates.
        while (!queue.isEmpty()) {
            int v = queue.poll();
            // The mark is set only now, after the entry left the queue.
            visited[v] = true;
            expansions++;
            // The test passes for vertices that are queued but not yet marked.
            for (int w : adj.get(v)) if (!visited[w]) queue.add(w);
        }
        return expansions;
    }

    /** Oracle: transitive closure of the symmetric edge relation, an independent O(n^3) method. */
    static int[] brute(int n, int[][] edges, int source) {
        boolean[][] r = new boolean[n][n];
        for (int i = 0; i < n; i++) r[i][i] = true;
        for (int[] e : edges) { r[e[0]][e[1]] = true; r[e[1]][e[0]] = true; }
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (r[i][k] && r[k][j]) r[i][j] = true;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (r[source][v]) out.add(v);
        int[] a = new int[out.size()];
        for (int i = 0; i < a.length; i++) a[i] = out.get(i);
        return a;
    }

    static List<List<Integer>> listOf(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(reachable(5, new int[][] {{0, 1}, {1, 2}, {3, 4}}, 0), new int[] {0, 1, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(reachable(4, new int[][] {{2, 1}, {1, 3}, {3, 2}}, 3), new int[] {1, 2, 3})) throw new AssertionError("ex2");
        // A single vertex with no edges reaches only itself, and parallel edges change nothing.
        if (!Arrays.equals(reachable(1, new int[0][], 0), new int[] {0})) throw new AssertionError("single vertex");
        if (!Arrays.equals(reachable(2, new int[][] {{0, 1}, {1, 0}, {0, 1}}, 1), new int[] {0, 1})) throw new AssertionError("parallel edges");
        // A new boolean array holds false in every slot.
        boolean[] fresh = new boolean[3];
        if (fresh[0] || fresh[1] || fresh[2]) throw new AssertionError("default false");
        // ArrayDeque add and poll give first in, first out order.
        ArrayDeque<Integer> d = new ArrayDeque<>();
        d.add(1); d.add(2);
        if (d.poll() != 1 || d.poll() != 2) throw new AssertionError("queue order");
        // The naive method expands 7 times on the five-vertex graph and 46 times on ten fully joined vertices.
        int[][] diamond = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}};
        if (expansionsMarkAtDequeue(listOf(5, diamond), 0) != 7) throw new AssertionError("naive diamond");
        List<int[]> all = new ArrayList<>();
        for (int i = 0; i < 10; i++) for (int j = i + 1; j < 10; j++) all.add(new int[] {i, j});
        if (expansionsMarkAtDequeue(listOf(10, all.toArray(new int[0][])), 0) != 46) throw new AssertionError("naive K10");
        // Random graphs: the marked set must equal the oracle on 3000 cases.
        Random rnd = new Random(2103);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), m = n == 1 ? 0 : rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            int s = rnd.nextInt(n);
            if (!Arrays.equals(reachable(n, edges, s), brute(n, edges, s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Iterative DFS (Author exercise)
<!-- id: gt-iterative-dfs -->

**Approach.**
The recursive DFS enters a vertex, records it and then enters its first unrecorded neighbor before it looks at the second one. An explicit stack reproduces that order when the code pushes the neighbors in decreasing order, so the smallest neighbor sits on top. The mark moves from the push to the pop. A vertex can appear on the stack twice, once from each discoverer, and the first copy to reach the top is the one the recursion would enter. The later copy finds `visited` already true and the loop skips it.

If the code marked at the push instead, the second discoverer would be blocked. The vertex would then keep the position where the first discoverer pushed it. That position is deeper in the stack than the position the recursion uses, so the order changes. Example 1 shows the difference.

The invariant is that a vertex is recorded only when it is popped while unmarked, and the stack holds only vertices that are not yet recorded or stale copies. The order matches the recursion by induction on the stack top.

**Complexity.**
- **Time** is O(n + m log m), because each adjacency list is sorted once and each entry is pushed at most once.
- **Space** is O(n + m), because the stack holds at most one entry per adjacency entry, which is 2m.

```java run
import java.util.*;

public final class IterativeDfs {
    /**
     * Returns the vertices in recursive DFS order, using an explicit stack.
     * Time: O(n + m log m). Space: O(n + m).
     * Invariant: a vertex is recorded when it is popped unmarked; stale copies are skipped.
     */
    static int[] dfsOrder(int n, int[][] edges, int source) {
        // Build the undirected adjacency list; every edge adds two entries.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // Sorting each list gives the increasing scan order that the problem defines; total cost O(m log m).
        for (List<Integer> list : adj) Collections.sort(list);
        boolean[] visited = new boolean[n];
        int[] order = new int[n];
        int len = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        stack.push(source);
        // Each loop pass pops one entry, and the total number of pushes is at most 2m + 1.
        while (!stack.isEmpty()) {
            // pop removes the most recent push, so the last discovered neighbor is handled first.
            int v = stack.pop();
            // A stale copy of a recorded vertex is harmless because this test discards it.
            if (visited[v]) continue;
            // Entry is the mark point for DFS; record the vertex now.
            visited[v] = true;
            order[len++] = v;
            List<Integer> nb = adj.get(v);
            // Push in decreasing order, so the smallest unrecorded neighbor ends on top of the stack.
            for (int i = nb.size() - 1; i >= 0; i--) if (!visited[nb.get(i)]) stack.push(nb.get(i));
        }
        // Only the recorded prefix of the array is the answer.
        return Arrays.copyOf(order, len);
    }

    /** The variant that marks at push time; it is shown here to prove that its order differs. */
    static int[] markAtPushOrder(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        for (List<Integer> list : adj) Collections.sort(list);
        boolean[] visited = new boolean[n];
        List<Integer> order = new ArrayList<>();
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        visited[source] = true;
        stack.push(source);
        while (!stack.isEmpty()) {
            int v = stack.pop();
            order.add(v);
            List<Integer> nb = adj.get(v);
            for (int i = nb.size() - 1; i >= 0; i--) if (!visited[nb.get(i)]) { visited[nb.get(i)] = true; stack.push(nb.get(i)); }
        }
        int[] a = new int[order.size()];
        for (int i = 0; i < a.length; i++) a[i] = order.get(i);
        return a;
    }

    /** Oracle: the recursive definition from the problem statement. */
    static void enter(List<List<Integer>> adj, boolean[] seen, List<Integer> out, int v) {
        seen[v] = true;
        out.add(v);
        for (int w : adj.get(v)) if (!seen[w]) enter(adj, seen, out, w);
    }

    static int[] brute(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        for (List<Integer> list : adj) Collections.sort(list);
        List<Integer> out = new ArrayList<>();
        enter(adj, new boolean[n], out, source);
        int[] a = new int[out.size()];
        for (int i = 0; i < a.length; i++) a[i] = out.get(i);
        return a;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] ex1 = {{0, 2}, {0, 1}, {1, 3}, {2, 3}, {3, 4}};
        if (!Arrays.equals(dfsOrder(5, ex1, 0), new int[] {0, 1, 3, 2, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(dfsOrder(4, new int[][] {{3, 2}, {2, 1}}, 3), new int[] {3, 2, 1})) throw new AssertionError("ex2");
        // Marking at push time gives a valid traversal with a different order on example 1.
        if (!Arrays.equals(markAtPushOrder(5, ex1, 0), new int[] {0, 1, 3, 4, 2})) throw new AssertionError("mark at push order");
        // ArrayDeque push and pop work at the head, so the last push comes out first.
        ArrayDeque<Integer> s = new ArrayDeque<>();
        s.push(1); s.push(2);
        if (s.pop() != 2 || s.pop() != 1) throw new AssertionError("stack order");
        // A path of 100000 vertices runs without recursion.
        int big = 100000;
        int[][] path = new int[big - 1][];
        for (int i = 0; i + 1 < big; i++) path[i] = new int[] {i, i + 1};
        if (dfsOrder(big, path, 0).length != big) throw new AssertionError("long path");
        // Random graphs: the order must equal the recursive oracle on 3000 cases.
        Random rnd = new Random(2104);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), m = n == 1 ? 0 : rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            int src = rnd.nextInt(n);
            if (!Arrays.equals(dfsOrder(n, edges, src), brute(n, edges, src))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Cycle And Disconnected Vertex (Author exercise)
<!-- id: gt-cycle-disconnected-vertex -->

**Approach.**
The method follows edge directions only, so it builds one adjacency entry per edge. It marks the source and pushes it on a stack. When the stack yields a vertex, the method scans the outgoing edges and marks and pushes every unmarked target. A cycle and a self-loop both lead to a vertex that is already marked, so the scan skips the edge and the traversal ends. Vertices without a path from the source are never marked, even when they have edges among themselves.

The answer is the list of positions where `visited` is still false. The code never claims a vertex is visited because of an edge that starts at an unmarked vertex, since the scan expands marked vertices only.

The invariant is that `visited[v]` is true exactly for the vertices that have been pushed, and every pushed vertex has a path from the source.

**Complexity.**
- **Time** is O(n + m), because each vertex is pushed once and each outgoing edge is read once.
- **Space** is O(n + m), because the adjacency list holds one entry per edge and the stack holds at most n vertices.

```java run
import java.util.*;

public final class CycleAndDisconnected {
    /**
     * Returns the vertices that no directed path from source reaches, in increasing order.
     * Time: O(n + m). Space: O(n + m).
     * Invariant: visited[v] is true exactly when v was pushed, and each pushed vertex has a path from source.
     */
    static int[] unreachable(int n, int[][] edges, int source) {
        // One adjacency entry per directed edge, so the lists hold m entries.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] visited = new boolean[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        // The source is marked first, so a cycle back to it is cut at once.
        visited[source] = true;
        stack.push(source);
        int marked = 1;
        // Each vertex is pushed once, so the loop runs at most n times.
        while (!stack.isEmpty()) {
            int v = stack.pop();
            // Reading the outgoing edges of v costs one step per edge over the whole run.
            for (int w : adj.get(v)) {
                // A self-loop or a cycle edge meets a marked vertex here and goes no further.
                if (visited[w]) continue;
                // Mark at push, so the stack never holds a vertex twice.
                visited[w] = true;
                stack.push(w);
                marked++;
            }
        }
        // Unmarked vertices are exactly the unreachable ones; the count is n - marked.
        int[] out = new int[n - marked];
        int k = 0;
        for (int v = 0; v < n; v++) if (!visited[v]) out[k++] = v;
        return out;
    }

    /** Oracle: repeat relaxation over the edge list until no vertex changes. */
    static int[] brute(int n, int[][] edges, int source) {
        boolean[] r = new boolean[n];
        r[source] = true;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) if (r[e[0]] && !r[e[1]]) { r[e[1]] = true; changed = true; }
        }
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (!r[v]) out.add(v);
        int[] a = new int[out.size()];
        for (int i = 0; i < a.length; i++) a[i] = out.get(i);
        return a;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(unreachable(4, new int[][] {{0, 1}, {1, 2}, {2, 0}}, 0), new int[] {3})) throw new AssertionError("ex1");
        if (!Arrays.equals(unreachable(3, new int[][] {{0, 0}, {1, 2}}, 0), new int[] {1, 2})) throw new AssertionError("ex2");
        // A source with no outgoing edge leaves every other vertex unreachable, and a full cycle leaves none.
        if (!Arrays.equals(unreachable(3, new int[][] {{1, 0}}, 0), new int[] {1, 2})) throw new AssertionError("sink source");
        if (unreachable(3, new int[][] {{0, 1}, {1, 2}, {2, 0}}, 1).length != 0) throw new AssertionError("full cycle");
        // Random directed graphs with loops and repeated edges must match the oracle on 3000 cases.
        Random rnd = new Random(2105);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9), m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int s = rnd.nextInt(n);
            if (!Arrays.equals(unreachable(n, edges, s), brute(n, edges, s))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Keys and Rooms (LeetCode 841)
<!-- id: gt-keys-and-rooms -->

**Approach.**
Each room is a vertex, and each key in `rooms[i]` is a directed edge from room `i` to the room that the key opens. The list `rooms[i]` is already the adjacency list, so the code builds nothing. A recursive DFS enters room 0, marks each room at entry and enters every unmarked room that a key opens. The visitor can enter every room exactly when the number of marked rooms equals `n`.

The recursion depth is at most `n`, which is 1000 here, so no explicit stack is needed. The invariant is that a room is marked when it is entered, so each room is entered at most once, even when several keys open it.

**Complexity.**
- **Time** is O(n + k) for `k` keys in total, because each room is entered once and each key is read once.
- **Space** is O(n), because `visited` holds `n` entries and the recursion holds at most `n` frames.

```java run
import java.util.*;

public final class KeysAndRooms {
    private static int entered;

    /**
     * Returns true when the visitor can enter every room.
     * Time: O(n + k) for k keys. Space: O(n).
     * Invariant: a room is marked on entry, so each room is entered at most once.
     */
    static boolean canVisitAll(List<List<Integer>> rooms) {
        // visited has one slot per room and starts all false.
        boolean[] visited = new boolean[rooms.size()];
        entered = 0;
        // Room 0 is the only open room, so every walk starts there.
        enter(rooms, visited, 0);
        // Every room is enterable exactly when the entered count equals n.
        return entered == rooms.size();
    }

    // Marks room r on entry, then follows each key it holds; each key is read once overall.
    private static void enter(List<List<Integer>> rooms, boolean[] visited, int r) {
        // The mark comes first, so a key that points back to r finds it marked and stops.
        visited[r] = true;
        entered++;
        for (int key : rooms.get(r)) {
            // A key to a marked room adds nothing, which also ends every cycle of keys.
            if (!visited[key]) enter(rooms, visited, key);
        }
    }

    /** Oracle: boolean transitive closure of the key relation. */
    static boolean brute(List<List<Integer>> rooms) {
        int n = rooms.size();
        boolean[][] r = new boolean[n][n];
        for (int i = 0; i < n; i++) { r[i][i] = true; for (int k : rooms.get(i)) r[i][k] = true; }
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (r[i][k] && r[k][j]) r[i][j] = true;
        for (int v = 0; v < n; v++) if (!r[0][v]) return false;
        return true;
    }

    static List<List<Integer>> of(int[][] a) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : a) { List<Integer> l = new ArrayList<>(); for (int k : row) l.add(k); out.add(l); }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canVisitAll(of(new int[][] {{2}, {}, {1, 0}}))) throw new AssertionError("ex1");
        if (canVisitAll(of(new int[][] {{1}, {0}, {3}, {2}}))) throw new AssertionError("ex2");
        // A room with a key to its own door and a repeated key does not break the count.
        if (!canVisitAll(of(new int[][] {{0, 1, 1}, {}}))) throw new AssertionError("self key");
        // A locked room that no key opens makes the answer false even when others hold keys.
        if (canVisitAll(of(new int[][] {{}, {0}}))) throw new AssertionError("empty room 0");
        // A chain of 1000 rooms runs within the recursion depth.
        int[][] chain = new int[1000][];
        for (int i = 0; i < 1000; i++) chain[i] = i + 1 < 1000 ? new int[] {i + 1} : new int[0];
        if (!canVisitAll(of(chain))) throw new AssertionError("chain");
        // Random key layouts must match the oracle on 3000 cases.
        Random rnd = new Random(2106);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(7);
            int[][] a = new int[n][];
            for (int i = 0; i < n; i++) { a[i] = new int[rnd.nextInt(3)]; for (int j = 0; j < a[i].length; j++) a[i][j] = rnd.nextInt(n); }
            if (canVisitAll(of(a)) != brute(of(a))) throw new AssertionError("random " + t);
        }
    }
}
```
