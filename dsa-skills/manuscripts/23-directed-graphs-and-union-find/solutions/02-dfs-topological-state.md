<!-- solutions-for: 02-dfs-topological-state -->
### DFS Topological State

#### Solution: [Build] Three-Color Trace (Author exercise)
<!-- id: ug-three-color-trace -->

**Approach.** Pack the plates into one flat `to` array with a `start` offset per vertex, using a counting pass, and sort each vertex's slice so the walk visits neighbours in ascending order. The recursive visit stamps the entry time when the vertex turns gray, walks every white neighbour, then stamps the exit time when it turns black. Neighbours that are already gray or black are skipped without touching the clock, which is why parallel edges are harmless. The oracle uses a different shape entirely: an explicit stack of vertex and next-position pairs over nested lists, and the random acyclic graphs are drawn from a shuffled vertex order with duplicate edges allowed. Beyond comparing the two tables, the checks confirm that the 2n stamps are exactly the numbers 0 to 2n - 1 once each, that every vertex has entry before exit, and that for every edge the target exits before the source, which is the property the next rung relies on.

**Complexity.** Counting, filling and the per-slice sort give O(n + m log m) time in the worst case, with O(n + m) memory for the flat arrays plus recursion up to depth n.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class ThreeColorTraceSolution {
    static int[][] solve(int n, int[][] edges) {
        int[] start = new int[n + 1];
        for (int[] e : edges) start[e[0] + 1]++;
        for (int i = 0; i < n; i++) start[i + 1] += start[i];
        int[] cursor = Arrays.copyOf(start, n);
        int[] to = new int[edges.length];
        for (int[] e : edges) to[cursor[e[0]]++] = e[1];
        for (int u = 0; u < n; u++) Arrays.sort(to, start[u], start[u + 1]);
        int[][] times = new int[2][n];
        int[] color = new int[n];
        int[] clock = {0};
        for (int r = 0; r < n; r++) if (color[r] == 0) visit(r, start, to, color, times, clock);
        return times;
    }

    private static void visit(int u, int[] start, int[] to, int[] color, int[][] times, int[] clock) {
        color[u] = 1;
        times[0][u] = clock[0]++;
        for (int k = start[u]; k < start[u + 1]; k++)
            if (color[to[k]] == 0) visit(to[k], start, to, color, times, clock);
        color[u] = 2;
        times[1][u] = clock[0]++;
    }

    static int[][] oracle(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        for (List<Integer> l : adj) Collections.sort(l);
        int[][] times = new int[2][n];
        boolean[] seen = new boolean[n];
        int clock = 0;
        for (int r = 0; r < n; r++) {
            if (seen[r]) continue;
            int[] stackV = new int[n + 1], stackP = new int[n + 1];
            int top = 0;
            stackV[0] = r;
            seen[r] = true;
            times[0][r] = clock++;
            while (top >= 0) {
                int v = stackV[top];
                if (stackP[top] < adj.get(v).size()) {
                    int w = adj.get(v).get(stackP[top]++);
                    if (!seen[w]) {
                        seen[w] = true;
                        times[0][w] = clock++;
                        stackV[++top] = w;
                        stackP[top] = 0;
                    }
                } else {
                    times[1][v] = clock++;
                    top--;
                }
            }
        }
        return times;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}};
        if (!Arrays.deepEquals(solve(5, e1), new int[][] {{0, 1, 7, 2, 3}, {9, 6, 8, 5, 4}}))
            throw new AssertionError("example 1");
        int[][] e2 = {{4, 1}, {4, 0}, {0, 3}, {1, 3}, {2, 5}};
        if (!Arrays.deepEquals(solve(6, e2), new int[][] {{0, 4, 6, 1, 10, 7}, {3, 5, 9, 2, 11, 8}}))
            throw new AssertionError("example 2");
        int[][] lone = solve(1, new int[0][]);
        if (lone[0][0] != 0 || lone[1][0] != 1) throw new AssertionError("single vertex");
        Random rnd = new Random(23201);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(8);
            List<Integer> perm = new ArrayList<>();
            for (int i = 0; i < n; i++) perm.add(i);
            Collections.shuffle(perm, rnd);
            List<int[]> list = new ArrayList<>();
            int m = rnd.nextInt(2 * n + 1);
            for (int k = 0; k < m && n > 1; k++) {
                int a = rnd.nextInt(n - 1), b = a + 1 + rnd.nextInt(n - a - 1);
                list.add(new int[] {perm.get(a), perm.get(b)});
            }
            int[][] edges = list.toArray(new int[0][]);
            int[][] copy = new int[edges.length][];
            for (int i = 0; i < edges.length; i++) copy[i] = edges[i].clone();
            int[][] got = solve(n, edges);
            if (!Arrays.deepEquals(edges, copy)) throw new AssertionError("input changed " + t);
            if (!Arrays.deepEquals(got, oracle(n, edges))) throw new AssertionError("oracle " + t);
            boolean[] used = new boolean[2 * n];
            for (int v = 0; v < n; v++) {
                if (got[0][v] >= got[1][v]) throw new AssertionError("entry before exit " + t);
                used[got[0][v]] = true;
                used[got[1][v]] = true;
            }
            for (boolean u : used) if (!u) throw new AssertionError("clock values " + t);
            for (int[] e : edges) if (got[1][e[1]] >= got[1][e[0]]) throw new AssertionError("edge order " + t);
        }
    }
}
```

#### Solution: [Vary] Postorder Topological List (Author exercise)
<!-- id: ug-postorder-list -->

**Approach.** A chain of 50000 vertices is allowed, so this solution avoids recursion. It sorts a copy of the edge list by source and then target, builds start offsets from that sorted copy, and keeps an `int[]` stack of vertices beside an `int[]` of the next plate position for each vertex. A vertex is written into the answer, from the last slot downward, only when its position pointer has run off the end of its slice, which is the moment it turns black. The oracle is a plain recursive version over nested lists that gives the exact same answer on small graphs, together with a checker that every edge's source comes earlier. The assertions also back four statements from the lesson: the recursive walk throws `StackOverflowError` on a chain of 100000 rooms when run in a thread with a 64 KB stack, the iterative one finishes that chain, listing rooms on entry breaks the order for plates 0 to 1, 0 to 2 and 2 to 1, and parallel edges change nothing.

**Complexity.** The sort dominates at O(m log m), after which the walk is linear, so the total is O(n + m log m) time and O(n + m) space with no recursion depth at all.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class PostorderListSolution {
    static int[] solve(int n, int[][] edges) {
        int[][] sorted = edges.clone();
        Arrays.sort(sorted, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int[] begin = new int[n + 1];
        for (int[] e : sorted) begin[e[0] + 1]++;
        for (int i = 0; i < n; i++) begin[i + 1] += begin[i];
        int[] pos = Arrays.copyOf(begin, n);
        boolean[] entered = new boolean[n];
        int[] answer = new int[n];
        int slot = n;
        int[] stack = new int[n];
        for (int r = 0; r < n; r++) {
            if (entered[r]) continue;
            int top = 0;
            stack[0] = r;
            entered[r] = true;
            while (top >= 0) {
                int v = stack[top];
                if (pos[v] < begin[v + 1]) {
                    int w = sorted[pos[v]++][1];
                    if (!entered[w]) {
                        entered[w] = true;
                        stack[++top] = w;
                    }
                } else {
                    answer[--slot] = v;
                    top--;
                }
            }
        }
        return answer;
    }

    static int[] recursiveOrder(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        for (List<Integer> l : adj) Collections.sort(l);
        boolean[] seen = new boolean[n];
        List<Integer> post = new ArrayList<>();
        for (int r = 0; r < n; r++) if (!seen[r]) dive(r, adj, seen, post);
        Collections.reverse(post);
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[i] = post.get(i);
        return out;
    }

    private static void dive(int u, List<List<Integer>> adj, boolean[] seen, List<Integer> post) {
        seen[u] = true;
        for (int w : adj.get(u)) if (!seen[w]) dive(w, adj, seen, post);
        post.add(u);
    }

    static int[] entryOrder(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        for (List<Integer> l : adj) Collections.sort(l);
        boolean[] seen = new boolean[n];
        List<Integer> pre = new ArrayList<>();
        for (int r = 0; r < n; r++) if (!seen[r]) first(r, adj, seen, pre);
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[i] = pre.get(i);
        return out;
    }

    private static void first(int u, List<List<Integer>> adj, boolean[] seen, List<Integer> pre) {
        seen[u] = true;
        pre.add(u);
        for (int w : adj.get(u)) if (!seen[w]) first(w, adj, seen, pre);
    }

    static boolean valid(int n, int[][] edges, int[] order) {
        if (order.length != n) return false;
        int[] at = new int[n];
        Arrays.fill(at, -1);
        for (int i = 0; i < n; i++) {
            if (order[i] < 0 || order[i] >= n || at[order[i]] >= 0) return false;
            at[order[i]] = i;
        }
        for (int[] e : edges) if (at[e[0]] >= at[e[1]]) return false;
        return true;
    }

    static int[][] chain(int n) {
        int[][] edges = new int[n - 1][];
        for (int i = 0; i + 1 < n; i++) edges[i] = new int[] {i, i + 1};
        return edges;
    }

    static boolean recursionOverflows(int n) {
        int[][] edges = chain(n);
        boolean[] hit = {false};
        Thread t = new Thread(null, () -> {
            try {
                recursiveOrder(n, edges);
            } catch (StackOverflowError err) {
                hit[0] = true;
            }
        }, "small-stack", 64 * 1024);
        t.start();
        try {
            t.join();
        } catch (InterruptedException ex) {
            throw new AssertionError(ex);
        }
        return hit[0];
    }

    public static void main(String[] args) {
        int[][] e1 = {{5, 2}, {5, 0}, {4, 0}, {4, 1}, {2, 3}, {3, 1}};
        if (!Arrays.equals(solve(6, e1), new int[] {5, 4, 2, 3, 1, 0})) throw new AssertionError("example 1");
        int[][] e2 = {{3, 1}, {3, 1}, {1, 0}, {4, 2}};
        if (!Arrays.equals(solve(5, e2), new int[] {4, 3, 2, 1, 0})) throw new AssertionError("example 2");
        int[][] trio = {{0, 1}, {0, 2}, {2, 1}};
        if (valid(3, trio, entryOrder(3, trio))) throw new AssertionError("entry order must fail");
        if (!valid(3, trio, solve(3, trio))) throw new AssertionError("postorder must pass");
        if (!recursionOverflows(100000)) throw new AssertionError("recursion should overflow");
        int[] deep = solve(100000, chain(100000));
        if (!valid(100000, chain(100000), deep)) throw new AssertionError("deep chain");
        Random rnd = new Random(23202);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(9);
            List<Integer> perm = new ArrayList<>();
            for (int i = 0; i < n; i++) perm.add(i);
            Collections.shuffle(perm, rnd);
            List<int[]> list = new ArrayList<>();
            int m = rnd.nextInt(2 * n + 1);
            for (int k = 0; k < m && n > 1; k++) {
                int a = rnd.nextInt(n - 1), b = a + 1 + rnd.nextInt(n - a - 1);
                list.add(new int[] {perm.get(a), perm.get(b)});
            }
            int[][] edges = list.toArray(new int[0][]);
            int[][] copy = new int[edges.length][];
            for (int i = 0; i < edges.length; i++) copy[i] = edges[i].clone();
            int[] got = solve(n, edges);
            if (!valid(n, edges, got)) throw new AssertionError("invalid order " + t);
            if (!Arrays.equals(got, recursiveOrder(n, edges))) throw new AssertionError("oracle " + t);
            for (int i = 0; i < edges.length; i++)
                if (!Arrays.equals(edges[i], copy[i])) throw new AssertionError("input changed " + t);
        }
    }
}
```

#### Solution: [Boundary] Cross Edge To Black (Author exercise)
<!-- id: ug-cross-edge-black -->

**Approach.** Keep a colour per vertex, and for each plate tested in ascending target order look at the target colour only. White bumps the first counter and recurses, gray bumps the second counter, and black bumps the third, with no early exit anywhere. The oracle never reads a colour. It runs an explicit-stack walk that records entry and exit times and the number of walks started, then derives the three counts from intervals: a gray test is an edge whose target's interval contains the source's, white tests equal n minus the number of walks started, and black is whatever remains of the m edges. A Floyd-Warshall closure also confirms that a gray test occurs exactly when the graph has a directed cycle. The assertions pin the diamond graph from the first example to zero gray tests, show that a single `visited` flag reports a cycle there, and show that a self loop is counted as gray.

**Complexity.** Each vertex is entered once and each plate tested once, so the running time is O(n + m log m) with the sorted neighbour lists, and the space is O(n + m).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class CrossEdgeBlackSolution {
    static int[] solve(int n, int[][] edges) {
        List<List<Integer>> doors = new ArrayList<>();
        for (int i = 0; i < n; i++) doors.add(new ArrayList<>());
        for (int[] e : edges) doors.get(e[0]).add(e[1]);
        for (List<Integer> d : doors) Collections.sort(d);
        int[] color = new int[n];
        int[] tally = new int[3];
        for (int r = 0; r < n; r++) if (color[r] == 0) walk(r, doors, color, tally);
        return tally;
    }

    private static void walk(int u, List<List<Integer>> doors, int[] color, int[] tally) {
        color[u] = 1;
        for (int w : doors.get(u)) {
            if (color[w] == 0) {
                tally[0]++;
                walk(w, doors, color, tally);
            } else if (color[w] == 1) {
                tally[1]++;
            } else {
                tally[2]++;
            }
        }
        color[u] = 2;
    }

    static boolean visitedFlagSaysCycle(int n, int[][] edges) {
        List<List<Integer>> doors = new ArrayList<>();
        for (int i = 0; i < n; i++) doors.add(new ArrayList<>());
        for (int[] e : edges) doors.get(e[0]).add(e[1]);
        boolean[] seen = new boolean[n];
        for (int r = 0; r < n; r++)
            if (!seen[r] && flagWalk(r, doors, seen)) return true;
        return false;
    }

    private static boolean flagWalk(int u, List<List<Integer>> doors, boolean[] seen) {
        seen[u] = true;
        for (int w : doors.get(u)) {
            if (seen[w]) return true;
            if (flagWalk(w, doors, seen)) return true;
        }
        return false;
    }

    static int[] oracle(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        for (List<Integer> l : adj) Collections.sort(l);
        int[] in = new int[n], out = new int[n];
        boolean[] seen = new boolean[n];
        int clock = 0, roots = 0;
        for (int r = 0; r < n; r++) {
            if (seen[r]) continue;
            roots++;
            int[] sv = new int[n + 1], sp = new int[n + 1];
            int top = 0;
            sv[0] = r;
            seen[r] = true;
            in[r] = clock++;
            while (top >= 0) {
                int v = sv[top];
                if (sp[top] < adj.get(v).size()) {
                    int w = adj.get(v).get(sp[top]++);
                    if (!seen[w]) {
                        seen[w] = true;
                        in[w] = clock++;
                        sv[++top] = w;
                        sp[top] = 0;
                    }
                } else {
                    out[v] = clock++;
                    top--;
                }
            }
        }
        int gray = 0;
        for (int[] e : edges)
            if (in[e[1]] <= in[e[0]] && out[e[0]] <= out[e[1]]) gray++;
        int white = n - roots;
        return new int[] {white, gray, edges.length - gray - white};
    }

    static boolean hasCycle(int n, int[][] edges) {
        boolean[][] reach = new boolean[n][n];
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int v = 0; v < n; v++) if (reach[v][v]) return true;
        return false;
    }

    public static void main(String[] args) {
        int[][] diamond = {{0, 1}, {0, 2}, {1, 3}, {2, 3}};
        if (!Arrays.equals(solve(4, diamond), new int[] {3, 0, 1})) throw new AssertionError("example 1");
        if (!visitedFlagSaysCycle(4, diamond)) throw new AssertionError("a single flag must misjudge the diamond");
        int[][] e2 = {{0, 1}, {1, 2}, {2, 1}, {2, 2}, {0, 3}, {3, 4}, {0, 4}, {0, 1}};
        if (!Arrays.equals(solve(5, e2), new int[] {4, 2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[][] {{0, 0}}), new int[] {0, 1, 0})) throw new AssertionError("self loop");
        if (!Arrays.equals(solve(3, new int[0][]), new int[] {0, 0, 0})) throw new AssertionError("no edges");
        Random rnd = new Random(23203);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(13);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            int[] got = solve(n, edges);
            if (!Arrays.deepEquals(edges, copy)) throw new AssertionError("input changed " + t);
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("oracle " + t);
            if ((got[1] > 0) != hasCycle(n, edges)) throw new AssertionError("cycle link " + t);
            if (got[0] + got[1] + got[2] != m) throw new AssertionError("total " + t);
        }
    }
}
```

#### Solution: [Recognize] Course Schedule II (LeetCode 210)
<!-- id: ug-course-schedule-dfs -->

**Approach.** Each pair `[a, b]` becomes a door from `b` to `a`, so walking a door goes from a prerequisite to the course that depends on it. After sorting every list, the search enters courses from 0 upward and marks a course gray on the way in. A gray target means a loop and the method returns the empty array at once, while a black target is ignored. Each course is appended to a list on turning black, and the final order is that list reversed. The oracle tries all permutations of up to six courses and keeps those that satisfy every pair. An empty answer must occur exactly when no permutation works, and any non-empty answer must be one of the valid permutations. The assertions add the two examples, check that the input is untouched, and show two false friends failing: a plain visited flag rejects a diamond that has a valid order, and the entry-order list breaks a pair.

**Complexity.** The doors are built and sorted once and every course and pair is then handled a constant number of times, so time is O(n + m log m) and memory is O(n + m), with recursion at most n deep and n at most 2000.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class CourseScheduleDfsSolution {
    private static List<List<Integer>> doors(int n, int[][] pairs) {
        List<List<Integer>> d = new ArrayList<>();
        for (int i = 0; i < n; i++) d.add(new ArrayList<>());
        for (int[] p : pairs) d.get(p[1]).add(p[0]);
        for (List<Integer> l : d) Collections.sort(l);
        return d;
    }

    static int[] solve(int numCourses, int[][] prerequisites) {
        List<List<Integer>> doors = doors(numCourses, prerequisites);
        int[] color = new int[numCourses];
        List<Integer> finished = new ArrayList<>();
        for (int c = 0; c < numCourses; c++)
            if (color[c] == 0 && !descend(c, doors, color, finished)) return new int[0];
        Collections.reverse(finished);
        int[] order = new int[numCourses];
        for (int i = 0; i < numCourses; i++) order[i] = finished.get(i);
        return order;
    }

    private static boolean descend(int c, List<List<Integer>> doors, int[] color, List<Integer> finished) {
        color[c] = 1;
        for (int next : doors.get(c)) {
            if (color[next] == 1) return false;
            if (color[next] == 0 && !descend(next, doors, color, finished)) return false;
        }
        color[c] = 2;
        finished.add(c);
        return true;
    }

    static boolean flagSaysLoop(int n, int[][] pairs) {
        List<List<Integer>> doors = doors(n, pairs);
        boolean[] seen = new boolean[n];
        for (int c = 0; c < n; c++) if (!seen[c] && flagDescend(c, doors, seen)) return true;
        return false;
    }

    private static boolean flagDescend(int c, List<List<Integer>> doors, boolean[] seen) {
        seen[c] = true;
        for (int next : doors.get(c)) if (seen[next] || flagDescend(next, doors, seen)) return true;
        return false;
    }

    static int[] entryList(int n, int[][] pairs) {
        List<List<Integer>> doors = doors(n, pairs);
        boolean[] seen = new boolean[n];
        List<Integer> list = new ArrayList<>();
        for (int c = 0; c < n; c++) if (!seen[c]) entryDescend(c, doors, seen, list);
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[i] = list.get(i);
        return out;
    }

    private static void entryDescend(int c, List<List<Integer>> doors, boolean[] seen, List<Integer> list) {
        seen[c] = true;
        list.add(c);
        for (int next : doors.get(c)) if (!seen[next]) entryDescend(next, doors, seen, list);
    }

    static boolean respects(int n, int[][] pairs, int[] order) {
        if (order.length != n) return false;
        int[] at = new int[n];
        Arrays.fill(at, -1);
        for (int i = 0; i < n; i++) {
            if (order[i] < 0 || order[i] >= n || at[order[i]] >= 0) return false;
            at[order[i]] = i;
        }
        for (int[] p : pairs) if (at[p[1]] >= at[p[0]]) return false;
        return true;
    }

    static boolean anyPermutationWorks(int n, int[][] pairs, int[] cur, boolean[] used, int k) {
        if (k == n) return respects(n, pairs, cur);
        for (int v = 0; v < n; v++) {
            if (used[v]) continue;
            used[v] = true;
            cur[k] = v;
            boolean ok = anyPermutationWorks(n, pairs, cur, used, k + 1);
            used[v] = false;
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        int[][] p1 = {{1, 4}, {2, 4}, {3, 1}, {3, 2}, {0, 3}};
        if (!Arrays.equals(solve(5, p1), new int[] {4, 2, 1, 3, 0})) throw new AssertionError("example 1");
        int[][] p2 = {{1, 0}, {2, 1}, {1, 2}, {3, 0}};
        if (solve(4, p2).length != 0) throw new AssertionError("example 2");
        int[][] diamond = {{1, 0}, {2, 0}, {3, 1}, {3, 2}};
        if (!respects(4, diamond, solve(4, diamond))) throw new AssertionError("diamond must have an order");
        if (!flagSaysLoop(4, diamond)) throw new AssertionError("a plain flag must misjudge the diamond");
        int[][] trio = {{1, 0}, {2, 0}, {1, 2}};
        if (respects(3, trio, entryList(3, trio))) throw new AssertionError("entry order must fail");
        if (!respects(3, trio, solve(3, trio))) throw new AssertionError("finishing order must pass");
        if (!Arrays.equals(solve(1, new int[0][]), new int[] {0})) throw new AssertionError("single course");
        Random rnd = new Random(23204);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++)
                for (int b = 0; b < n; b++)
                    if (a != b && rnd.nextInt(100) < 18) list.add(new int[] {a, b});
            int[][] pairs = list.toArray(new int[0][]);
            int[][] copy = new int[pairs.length][];
            for (int i = 0; i < pairs.length; i++) copy[i] = pairs[i].clone();
            int[] got = solve(n, pairs);
            if (!Arrays.deepEquals(pairs, copy)) throw new AssertionError("input changed " + t);
            boolean exists = anyPermutationWorks(n, pairs, new int[n], new boolean[n], 0);
            if (exists) {
                if (!respects(n, pairs, got)) throw new AssertionError("invalid order " + t);
            } else if (got.length != 0) {
                throw new AssertionError("should be empty " + t);
            }
        }
    }
}
```
