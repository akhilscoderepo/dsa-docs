<!-- solutions-for: 09-cycle-detection -->
### Cycle Detection

#### Solution: [Build] Undirected Parent Check (Author exercise)
<!-- id: gt-parent-check -->

**Approach.** Build adjacency lists, then walk each unreached vertex depth first while carrying the vertex it was entered from. Looking at a neighbor, the walk ignores the parent, ends with true on any other reached vertex, and recurses on the rest. Because the input is promised to be a simple graph, the parent vertex identifies the parent edge uniquely. The oracle does no walking at all. It computes connectivity by a boolean closure and applies the rule that a graph has a cycle exactly when it has more edges than vertices minus components, since a forest has exactly that many. The assertions compare the two on random simple graphs and check that every edge shows up twice in the adjacency lists, which is the reason the parent has to be skipped.

**Complexity.** Linear in the size of the graph for time, O(n + m), because each adjacency entry is read once. The lists, the seen table and the recursion take O(n + m) memory in the worst case.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ParentCheckSolution {
    static List<List<Integer>> build(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return adj;
    }

    static boolean solve(int n, int[][] edges) {
        List<List<Integer>> adj = build(n, edges);
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && walk(adj, seen, s, -1)) return true;
        }
        return false;
    }

    private static boolean walk(List<List<Integer>> adj, boolean[] seen, int v, int parent) {
        seen[v] = true;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (seen[w] || walk(adj, seen, w, v)) return true;
        }
        return false;
    }

    static boolean oracle(int n, int[][] edges) {
        boolean[][] link = new boolean[n][n];
        for (int i = 0; i < n; i++) link[i][i] = true;
        for (int[] e : edges) link[e[0]][e[1]] = link[e[1]][e[0]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (link[i][k] && link[k][j]) link[i][j] = true;
        int comps = 0;
        for (int i = 0; i < n; i++) {
            boolean first = true;
            for (int j = 0; j < i; j++) if (link[i][j]) first = false;
            if (first) comps++;
        }
        return edges.length > n - comps;
    }

    public static void main(String[] args) {
        if (!solve(6, new int[][] {{0, 1}, {1, 2}, {2, 0}, {3, 4}})) throw new AssertionError("example 1");
        if (solve(6, new int[][] {{0, 1}, {1, 2}, {1, 3}, {4, 5}})) throw new AssertionError("example 2");
        if (solve(1, new int[][] {})) throw new AssertionError("single vertex");
        int[][] tri = {{0, 1}, {1, 2}, {2, 0}};
        int entries = 0;
        for (List<Integer> l : build(3, tri)) entries += l.size();
        if (entries != 2 * tri.length) throw new AssertionError("each edge is stored from both ends");
        Random rnd = new Random(21901);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            double p = rnd.nextDouble() * 0.5;
            for (int a = 0; a < n; a++)
                for (int b = a + 1; b < n; b++)
                    if (rnd.nextDouble() < p) list.add(rnd.nextBoolean() ? new int[] {a, b} : new int[] {b, a});
            int[][] edges = list.toArray(new int[0][]);
            if (solve(n, edges) != oracle(n, edges)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Directed Three Colors (Author exercise)
<!-- id: gt-three-colors -->

**Approach.** Keep a mark per vertex, 0 for unreached, 1 for on the current route and 2 for done. The walk marks a vertex 1 on entry and 2 when its neighbors are exhausted, and it reports a cycle exactly when an edge lands on a vertex marked 1. A self loop lands on the vertex itself, which is marked 1 at that moment, so it needs no special case. The oracle is a boolean transitive closure by Floyd and Warshall, answering true when some vertex can reach itself. The assertions compare the recursive walk, an iterative walk with an explicit stack, and the oracle on random digraphs. They also show that the shortcut of treating any reached neighbor as a cycle gets a four-vertex diamond wrong, and that the recursion overflows a deliberately small thread stack on a path of a million vertices while the iterative version handles the same path.

**Complexity.** Each vertex is entered once and each edge is read once, so time is O(n + m). Space is O(n + m) for the adjacency arrays, plus a route as deep as n in the recursion or in the explicit stack.

```java run
import java.util.Random;

public final class ThreeColorsSolution {
    static int[] head, nxt, to;

    static void build(int n, int[][] edges) {
        head = new int[n];
        java.util.Arrays.fill(head, -1);
        nxt = new int[edges.length];
        to = new int[edges.length];
        for (int i = 0; i < edges.length; i++) {
            to[i] = edges[i][1];
            nxt[i] = head[edges[i][0]];
            head[edges[i][0]] = i;
        }
    }

    static boolean solve(int n, int[][] edges) {
        build(n, edges);
        int[] mark = new int[n];
        for (int s = 0; s < n; s++) {
            if (mark[s] == 0 && enter(s, mark)) return true;
        }
        return false;
    }

    private static boolean enter(int v, int[] mark) {
        mark[v] = 1;
        for (int e = head[v]; e != -1; e = nxt[e]) {
            int w = to[e];
            if (mark[w] == 1) return true;
            if (mark[w] == 0 && enter(w, mark)) return true;
        }
        mark[v] = 2;
        return false;
    }

    static boolean solveIterative(int n, int[][] edges) {
        build(n, edges);
        int[] mark = new int[n], cursor = head.clone(), stack = new int[n];
        for (int s = 0; s < n; s++) {
            if (mark[s] != 0) continue;
            int top = 0;
            stack[top++] = s;
            mark[s] = 1;
            while (top > 0) {
                int v = stack[top - 1], e = cursor[v];
                if (e == -1) { mark[v] = 2; top--; continue; }
                cursor[v] = nxt[e];
                int w = to[e];
                if (mark[w] == 1) return true;
                if (mark[w] == 0) { mark[w] = 1; stack[top++] = w; }
            }
        }
        return false;
    }

    static boolean anyReachedIsCycle(int n, int[][] edges) {
        build(n, edges);
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && shortcut(s, seen)) return true;
        }
        return false;
    }

    private static boolean shortcut(int v, boolean[] seen) {
        seen[v] = true;
        for (int e = head[v]; e != -1; e = nxt[e]) {
            if (seen[to[e]] || shortcut(to[e], seen)) return true;
        }
        return false;
    }

    static boolean oracle(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int[] e : edges) r[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        for (int i = 0; i < n; i++) if (r[i][i]) return true;
        return false;
    }

    public static void main(String[] args) throws Exception {
        int[][] ex1 = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}};
        if (solve(5, ex1)) throw new AssertionError("example 1");
        if (!solve(4, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 1}})) throw new AssertionError("example 2");
        if (!solve(2, new int[][] {{1, 1}})) throw new AssertionError("self loop");
        int[][] diamond = {{0, 1}, {0, 2}, {1, 3}, {2, 3}};
        if (solve(4, diamond)) throw new AssertionError("diamond has no cycle");
        if (!anyReachedIsCycle(4, diamond)) throw new AssertionError("the shortcut should misreport the diamond");
        Random rnd = new Random(21902);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(10);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            boolean want = oracle(n, edges);
            if (solve(n, edges) != want) throw new AssertionError("recursive " + t);
            if (solveIterative(n, edges) != want) throw new AssertionError("iterative " + t);
        }
        int big = 1_000_000;
        int[][] path = new int[big - 1][];
        for (int i = 0; i + 1 < big; i++) path[i] = new int[] {i, i + 1};
        if (solveIterative(big, path)) throw new AssertionError("a path has no cycle");
        boolean[] overflowed = {false};
        Thread small = new Thread(null, () -> {
            try {
                solve(big, path);
            } catch (StackOverflowError expected) {
                overflowed[0] = true;
            }
        }, "small-stack", 256 * 1024);
        small.start();
        small.join();
        if (!overflowed[0]) throw new AssertionError("deep recursion should overflow a small stack");
    }
}
```

#### Solution: [Boundary] Two-Way Undirected Edge (Author exercise)
<!-- id: gt-two-way-edge -->

**Approach.** Store each edge in both adjacency lists together with its position in the input. The walk remembers the position of the edge it arrived by and skips only that entry. A parallel copy has a different position, so it leads back to a vertex that is already reached and reports a cycle of length 2. The oracle uses the closure of connectivity and the edge count rule from the Build rung, which holds for repeated edges too, since each copy adds to the count without adding a connection. The assertions compare the two on random multigraphs, check that the pair listed as `[1, 0]` after `[0, 1]` counts as parallel, and show that a walk which reuses the directed marks and skips the parent vertex, judging only from the descendant's side, reports false for a doubled edge and disagrees with the oracle on some random inputs.

**Complexity.** The time is O(n + m), counting each entry of the lists once, and the space is O(n + m) for the lists with their edge numbers and the recursion on a long chain.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class TwoWayEdgeSolution {
    static boolean solve(int n, int[][] edges) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int id = 0; id < edges.length; id++) {
            adj.get(edges[id][0]).add(new int[] {edges[id][1], id});
            adj.get(edges[id][1]).add(new int[] {edges[id][0], id});
        }
        boolean[] seen = new boolean[n];
        for (int s = 0; s < n; s++) {
            if (!seen[s] && walk(adj, seen, s, -1)) return true;
        }
        return false;
    }

    private static boolean walk(List<List<int[]>> adj, boolean[] seen, int v, int fromId) {
        seen[v] = true;
        for (int[] e : adj.get(v)) {
            if (e[1] == fromId) continue;
            if (seen[e[0]] || walk(adj, seen, e[0], e[1])) return true;
        }
        return false;
    }

    static boolean parentVertexVersion(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        int[] mark = new int[n];
        for (int s = 0; s < n; s++) {
            if (mark[s] == 0 && byVertex(adj, mark, s, -1)) return true;
        }
        return false;
    }

    private static boolean byVertex(List<List<Integer>> adj, int[] mark, int v, int parent) {
        mark[v] = 1;
        for (int w : adj.get(v)) {
            if (w == parent) continue;
            if (mark[w] == 1) return true;
            if (mark[w] == 0 && byVertex(adj, mark, w, v)) return true;
        }
        mark[v] = 2;
        return false;
    }

    static boolean oracle(int n, int[][] edges) {
        boolean[][] link = new boolean[n][n];
        for (int i = 0; i < n; i++) link[i][i] = true;
        for (int[] e : edges) link[e[0]][e[1]] = link[e[1]][e[0]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (link[i][k] && link[k][j]) link[i][j] = true;
        int comps = 0;
        for (int i = 0; i < n; i++) {
            boolean first = true;
            for (int j = 0; j < i; j++) if (link[i][j]) first = false;
            if (first) comps++;
        }
        return edges.length > n - comps;
    }

    public static void main(String[] args) {
        if (solve(3, new int[][] {{0, 1}, {1, 2}})) throw new AssertionError("example 1");
        if (!solve(4, new int[][] {{0, 1}, {2, 3}, {3, 2}})) throw new AssertionError("example 2");
        if (!solve(2, new int[][] {{0, 1}, {1, 0}})) throw new AssertionError("reversed pair is parallel");
        if (solve(2, new int[][] {{0, 1}})) throw new AssertionError("one edge is not a cycle");
        if (parentVertexVersion(2, new int[][] {{0, 1}, {0, 1}})) throw new AssertionError("parent vertex check with marks should miss the doubled edge");
        Random rnd = new Random(21903);
        int disagreements = 0;
        for (int t = 0; t < 4000; t++) {
            int n = 2 + rnd.nextInt(6), m = rnd.nextInt(9);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n - 1);
                if (b >= a) b++;
                edges[i] = new int[] {a, b};
            }
            boolean want = oracle(n, edges);
            if (solve(n, edges) != want) throw new AssertionError("random " + t);
            if (parentVertexVersion(n, edges) != want) disagreements++;
        }
        if (disagreements == 0) throw new AssertionError("parent vertex check should fail on some multigraphs");
    }
}
```

#### Solution: [Recognize] Course Schedule (LeetCode 207)
<!-- id: gt-course-schedule -->

**Approach.** Read each pair `[a, b]` as an edge from b to a, so the graph points from a prerequisite to the course it unlocks. The courses can all be taken exactly when this directed graph has no cycle, and a three-state walk finds a cycle by spotting an edge into a vertex still on the route. This version uses an explicit stack with a cursor per vertex, so a long chain of prerequisites cannot overflow the thread stack. The oracle is a Floyd and Warshall closure, with a course blocked when it can reach itself. The assertions compare the two on random pair lists, confirm that reversing every edge never changes the answer, and show that a diamond of prerequisites is schedulable while the any-reached-neighbor shortcut declares it impossible.

**Complexity.** Reading the pairs and walking the graph costs O(n + p) time for n courses and p pairs. The adjacency arrays, the marks and the stack take O(n + p) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CourseScheduleSolution {
    static boolean canFinish(int numCourses, int[][] prerequisites, boolean reversed) {
        int[] head = new int[numCourses];
        Arrays.fill(head, -1);
        int[] nxt = new int[prerequisites.length], to = new int[prerequisites.length];
        for (int i = 0; i < prerequisites.length; i++) {
            int from = reversed ? prerequisites[i][0] : prerequisites[i][1];
            to[i] = reversed ? prerequisites[i][1] : prerequisites[i][0];
            nxt[i] = head[from];
            head[from] = i;
        }
        int[] mark = new int[numCourses], cursor = head.clone(), stack = new int[numCourses];
        for (int s = 0; s < numCourses; s++) {
            if (mark[s] != 0) continue;
            int top = 0;
            stack[top++] = s;
            mark[s] = 1;
            while (top > 0) {
                int v = stack[top - 1], e = cursor[v];
                if (e == -1) { mark[v] = 2; top--; continue; }
                cursor[v] = nxt[e];
                int w = to[e];
                if (mark[w] == 1) return false;
                if (mark[w] == 0) { mark[w] = 1; stack[top++] = w; }
            }
        }
        return true;
    }

    static boolean canFinish(int numCourses, int[][] prerequisites) {
        return canFinish(numCourses, prerequisites, false);
    }

    static boolean shortcutSaysFinishable(int numCourses, int[][] prerequisites) {
        boolean[][] out = new boolean[numCourses][numCourses];
        for (int[] p : prerequisites) out[p[1]][p[0]] = true;
        boolean[] seen = new boolean[numCourses];
        for (int s = 0; s < numCourses; s++) {
            if (!seen[s] && reaches(out, seen, s)) return false;
        }
        return true;
    }

    private static boolean reaches(boolean[][] out, boolean[] seen, int v) {
        seen[v] = true;
        for (int w = 0; w < out.length; w++) {
            if (!out[v][w]) continue;
            if (seen[w] || reaches(out, seen, w)) return true;
        }
        return false;
    }

    static boolean oracle(int numCourses, int[][] prerequisites) {
        boolean[][] r = new boolean[numCourses][numCourses];
        for (int[] p : prerequisites) r[p[1]][p[0]] = true;
        for (int k = 0; k < numCourses; k++)
            for (int i = 0; i < numCourses; i++)
                for (int j = 0; j < numCourses; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        for (int i = 0; i < numCourses; i++) if (r[i][i]) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!canFinish(4, new int[][] {{1, 0}, {2, 1}, {3, 2}})) throw new AssertionError("example 1");
        if (canFinish(3, new int[][] {{0, 2}, {2, 1}, {1, 0}})) throw new AssertionError("example 2");
        if (!canFinish(1, new int[][] {})) throw new AssertionError("no prerequisites");
        int[][] diamond = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        if (!canFinish(4, diamond)) throw new AssertionError("diamond is schedulable");
        if (shortcutSaysFinishable(4, diamond)) throw new AssertionError("the shortcut should reject the diamond");
        Random rnd = new Random(21904);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(10);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (n > 1 && a == b) b = (a + 1) % n;
                if (n == 1) { pre = new int[0][]; break; }
                pre[i] = new int[] {a, b};
            }
            boolean want = oracle(n, pre);
            if (canFinish(n, pre) != want) throw new AssertionError("random " + t);
            if (canFinish(n, pre, true) != want) throw new AssertionError("reversed " + t);
        }
    }
}
```
