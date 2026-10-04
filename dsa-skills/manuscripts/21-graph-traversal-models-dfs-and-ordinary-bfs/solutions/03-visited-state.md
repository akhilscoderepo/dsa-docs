<!-- solutions-for: 03-visited-state -->
### Visited State

#### Solution: [Build] Reachable Vertices (Author exercise)
<!-- id: gt-reachable-vertices -->

**Approach.** Build the out-lists, set the flag of the source, and queue it. Each vertex taken from the queue offers its heads, and a head is flagged in the same breath as it is queued, so a vertex that two others point at is queued only once. The oracle is a boolean transitive closure computed with Warshall's triple loop, and the assertions compare one row of it with the traversal on random directed graphs. A diamond graph then counts queue insertions under both marking rules, which gives 4 when flagged at enqueue and 5 when flagged at dequeue, and shows the duplicate sitting in the queue.

**Complexity.** Each vertex enters the queue once and each edge is examined once, so the time is O(n + E) with O(n) space for flags and queue beside the lists.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ReachableVertices {
    static List<List<Integer>> lists(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        return adj;
    }

    static boolean[] solve(int n, int[][] edges, int source) {
        List<List<Integer>> adj = lists(n, edges);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        seen[source] = true;
        queue.add(source);
        while (!queue.isEmpty()) {
            int v = queue.poll();
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    queue.add(w);
                }
            }
        }
        return seen;
    }

    static boolean[] oracle(int n, int[][] edges, int source) {
        boolean[][] reach = new boolean[n][n];
        for (int v = 0; v < n; v++) reach[v][v] = true;
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        return reach[source];
    }

    static int insertions(List<List<Integer>> adj, int source, boolean markAtEnqueue) {
        boolean[] seen = new boolean[adj.size()];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        int inserted = 1;
        queue.add(source);
        if (markAtEnqueue) seen[source] = true;
        while (!queue.isEmpty()) {
            int v = queue.poll();
            if (!markAtEnqueue) {
                if (seen[v]) continue;
                seen[v] = true;
            }
            for (int w : adj.get(v)) {
                if (markAtEnqueue) {
                    if (seen[w]) continue;
                    seen[w] = true;
                }
                queue.add(w);
                inserted++;
            }
        }
        return inserted;
    }

    static void check(boolean cond, String msg) {
        if (!cond) throw new AssertionError(msg);
    }

    public static void main(String[] args) {
        check(java.util.Arrays.toString(solve(6, new int[][] {{0, 1}, {1, 2}, {3, 2}, {4, 5}}, 0))
            .equals("[true, true, true, false, false, false]"), "example 1");
        check(java.util.Arrays.toString(solve(4, new int[][] {{2, 1}, {1, 0}, {0, 3}}, 2))
            .equals("[true, true, true, true]"), "example 2");

        // Diamond 0 -> 1, 0 -> 2, 1 -> 3, 2 -> 3: vertex 3 has two parents.
        List<List<Integer>> diamond = lists(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}});
        check(insertions(diamond, 0, true) == 4, "mark at enqueue inserts each vertex once");
        check(insertions(diamond, 0, false) == 5, "mark at dequeue inserts vertex 3 twice");
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        boolean[] seen = new boolean[4];
        queue.add(0);
        while (!queue.isEmpty()) {
            int v = queue.poll();
            seen[v] = true;
            for (int w : diamond.get(v)) if (!seen[w]) queue.add(w);
            if (v == 2) {
                check(queue.size() == 2 && queue.peekFirst() == 3 && queue.peekLast() == 3,
                    "two copies of 3 wait together");
            }
        }

        Random rnd = new Random(21301);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            int tries = rnd.nextInt(20);
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (used.add(u * 100 + v)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            int source = rnd.nextInt(n);
            boolean[] got = solve(n, edges, source);
            boolean[] want = oracle(n, edges, source);
            check(java.util.Arrays.equals(got, want), "random " + t);
            int count = 0;
            for (boolean b : got) if (b) count++;
            check(insertions(lists(n, edges), source, true) == count, "inserted once each " + t);
            check(insertions(lists(n, edges), source, false) >= count, "dequeue rule never inserts fewer " + t);
        }
    }
}
```

#### Solution: [Vary] Iterative DFS (Author exercise)
<!-- id: gt-iterative-dfs-stack -->

**Approach.** The flag moves to the moment of the push, exactly as in the queue version. The stack is a plain `int` array with `n` cells and a top index, and every vertex is pushed at most once, so the index can never pass `n`. The result list is read off the flags in ascending order. The oracle is the same boolean transitive closure. The assertions also run a deliberately careless variant that flags at the pop, record its deepest stack, and show on a diamond that it needs more than `n` cells in some graphs while the real method never does.

**Complexity.** Linear in the graph, O(n + E) time, and the stack plus flags add only O(n) cells.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class IterativeDfs {
    static int deepest;

    static List<Integer> solve(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        int[] stack = new int[n];
        int top = 0;
        seen[source] = true;
        stack[top++] = source;
        deepest = top;
        while (top > 0) {
            int v = stack[--top];
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    stack[top++] = w;
                    deepest = Math.max(deepest, top);
                }
            }
        }
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (seen[v]) out.add(v);
        return out;
    }

    static int careless(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        ArrayList<Integer> stack = new ArrayList<>();
        stack.add(source);
        int most = 1;
        while (!stack.isEmpty()) {
            int v = stack.remove(stack.size() - 1);
            if (seen[v]) continue;
            seen[v] = true;
            for (int w : adj.get(v)) stack.add(w);
            most = Math.max(most, stack.size());
        }
        return most;
    }

    static List<Integer> oracle(int n, int[][] edges, int source) {
        boolean[][] reach = new boolean[n][n];
        for (int v = 0; v < n; v++) reach[v][v] = true;
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (reach[source][v]) out.add(v);
        return out;
    }

    static void check(boolean cond, String msg) {
        if (!cond) throw new AssertionError(msg);
    }

    public static void main(String[] args) {
        check(solve(5, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 1}}, 0).toString().equals("[0, 1, 2, 3]"), "example 1");
        check(solve(4, new int[][] {{2, 0}, {2, 3}, {1, 2}}, 2).toString().equals("[0, 2, 3]"), "example 2");

        // Complete directed graph on 6 vertices: the careless stack outgrows n cells, the real one cannot.
        List<int[]> dense = new ArrayList<>();
        for (int u = 0; u < 6; u++)
            for (int v = 0; v < 6; v++) if (u != v) dense.add(new int[] {u, v});
        int[][] all = dense.toArray(new int[0][]);
        check(careless(6, all, 0) > 6, "mark at pop holds duplicates beyond n cells");
        solve(6, all, 0);
        check(deepest <= 6, "mark at push stays within n cells");

        Random rnd = new Random(21302);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            int tries = rnd.nextInt(24);
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (used.add(u * 100 + v)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            int source = rnd.nextInt(n);
            check(solve(n, edges, source).equals(oracle(n, edges, source)), "random " + t);
            check(deepest <= n, "stack bound " + t);
        }
    }
}
```

#### Solution: [Boundary] Cycle And Disconnected Vertex (Author exercise)
<!-- id: gt-cycle-and-disconnected -->

**Approach.** Traverse from the source with flags set at the enqueue, then collect every vertex whose flag stayed false. A self loop or a closing edge meets a head that is already flagged and stops there, and an edge that points into the reached region is never followed backwards, so its tail stays unflagged. The oracle takes the transitive closure and lists the vertices missing from the source row. The assertions cover self loops, isolated vertices and tails of incoming edges on random graphs, and an `ArrayDeque` is shown to throw `NullPointerException` on `add(null)`, which is why the sentinel in the lesson is a number.

**Complexity.** One pass over the vertices and edges gives O(n + E) time, and the flags and queue need O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class CycleAndDisconnected {
    static List<Integer> solve(int n, int[][] edges, int source) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        seen[source] = true;
        queue.add(source);
        while (!queue.isEmpty()) {
            int v = queue.poll();
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    queue.add(w);
                }
            }
        }
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (!seen[v]) out.add(v);
        return out;
    }

    static List<Integer> oracle(int n, int[][] edges, int source) {
        boolean[][] reach = new boolean[n][n];
        for (int v = 0; v < n; v++) reach[v][v] = true;
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (!reach[source][v]) out.add(v);
        return out;
    }

    static void check(boolean cond, String msg) {
        if (!cond) throw new AssertionError(msg);
    }

    public static void main(String[] args) {
        check(solve(5, new int[][] {{0, 1}, {1, 2}, {2, 0}, {3, 0}}, 0).toString().equals("[3, 4]"), "example 1");
        check(solve(4, new int[][] {{1, 1}, {2, 1}}, 1).toString().equals("[0, 2, 3]"), "example 2");
        boolean threw = false;
        try {
            new ArrayDeque<Integer>().add(null);
        } catch (NullPointerException expected) {
            threw = true;
        }
        check(threw, "ArrayDeque rejects null");

        Random rnd = new Random(21303);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            Set<Integer> used = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            int tries = rnd.nextInt(16);
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (used.add(u * 100 + v)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            int source = rnd.nextInt(n);
            List<Integer> got = solve(n, edges, source);
            check(got.equals(oracle(n, edges, source)), "random " + t);
            check(!got.contains(source), "source is always reached " + t);
        }
    }
}
```

#### Solution: [Recognize] Keys And Rooms (LeetCode 841)
<!-- id: gt-keys-and-rooms -->

**Approach.** Read each key `k` found in room `i` as a directed edge from `i` to `k`, then run the depth first walk from room 0 with an explicit stack that flags a room when it is pushed. The answer is true exactly when the number of flagged rooms equals `n`. The oracle repeats the closure computation on a boolean matrix built from the key lists, and the assertions use random key lists with repeated keys and keys to already open rooms. A recursive version is also run in a thread with a small stack on a chain of 200000 rooms to show it ends in `StackOverflowError`, while the explicit stack handles the same chain.

**Complexity.** The work is proportional to the rooms plus the total keys, O(n + K) time, and the flags and stack take O(n) space.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class KeysAndRooms {
    static boolean canVisitAllRooms(List<List<Integer>> rooms) {
        int n = rooms.size();
        boolean[] seen = new boolean[n];
        int[] stack = new int[n];
        int top = 0, marked = 1;
        seen[0] = true;
        stack[top++] = 0;
        while (top > 0) {
            int room = stack[--top];
            for (int key : rooms.get(room)) {
                if (!seen[key]) {
                    seen[key] = true;
                    marked++;
                    stack[top++] = key;
                }
            }
        }
        return marked == n;
    }

    static boolean oracle(List<List<Integer>> rooms) {
        int n = rooms.size();
        boolean[][] reach = new boolean[n][n];
        for (int v = 0; v < n; v++) reach[v][v] = true;
        for (int i = 0; i < n; i++) for (int k : rooms.get(i)) reach[i][k] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int v = 0; v < n; v++) if (!reach[0][v]) return false;
        return true;
    }

    static void recurse(List<List<Integer>> rooms, boolean[] seen, int room) {
        seen[room] = true;
        for (int key : rooms.get(room)) if (!seen[key]) recurse(rooms, seen, key);
    }

    static List<List<Integer>> of(int[]... rows) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : rows) {
            List<Integer> keys = new ArrayList<>();
            for (int k : row) keys.add(k);
            out.add(keys);
        }
        return out;
    }

    static void check(boolean cond, String msg) {
        if (!cond) throw new AssertionError(msg);
    }

    public static void main(String[] args) throws Exception {
        check(canVisitAllRooms(of(new int[] {2}, new int[] {}, new int[] {1, 3}, new int[] {0})), "example 1");
        check(!canVisitAllRooms(of(new int[] {1}, new int[] {0}, new int[] {3}, new int[] {2})), "example 2");

        int chain = 200000;
        List<List<Integer>> long1 = new ArrayList<>();
        for (int i = 0; i < chain; i++) long1.add(i + 1 < chain ? List.of(i + 1) : List.of());
        check(canVisitAllRooms(long1), "explicit stack handles a long chain");
        boolean[] overflow = new boolean[1];
        Thread worker = new Thread(null, () -> {
            try {
                recurse(long1, new boolean[chain], 0);
            } catch (StackOverflowError expected) {
                overflow[0] = true;
            }
        }, "deep", 256 * 1024);
        worker.start();
        worker.join();
        check(overflow[0], "recursion on a long chain overflows a small call stack");

        Random rnd = new Random(21304);
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(8);
            List<List<Integer>> rooms = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                List<Integer> keys = new ArrayList<>();
                int count = rnd.nextInt(3);
                for (int k = 0; k < count; k++) keys.add(rnd.nextInt(n));
                rooms.add(keys);
            }
            check(canVisitAllRooms(rooms) == oracle(rooms), "random " + t);
        }
    }
}
```
