<!-- solutions-for: 01-kahn-topological-order -->
### Kahn Topological Order

#### Solution: [Build] Compute Indegrees (Author exercise)
<!-- id: ug-compute-indegrees -->

**Approach.** Allocate a fresh `int[n]`, which Java fills with zeros, and add one at index `edge[1]` for every row. Only the second entry of each pair is touched, so a vertex with no incoming arrow stays at zero, a repeated arrow is counted each time, and a self-loop adds one at its own vertex. The oracle builds an n by n matrix of arrow multiplicities and sums each column, which shares no code with the loop. The run block also asserts that the input rows are unchanged afterwards and that a fresh `int[]` really starts at zero.

**Complexity.** One pass over the m arrows after an O(n) allocation gives O(n + m) time, and the only extra memory is the returned array of n ints.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ComputeIndegreesSolution {
    static int[] solve(int n, int[][] edges) {
        int[] indegree = new int[n];
        for (int[] e : edges) indegree[e[1]]++;
        return indegree;
    }

    static int[] oracle(int n, int[][] edges) {
        int[][] mult = new int[n][n];
        for (int[] e : edges) mult[e[0]][e[1]]++;
        int[] out = new int[n];
        for (int to = 0; to < n; to++) {
            for (int from = 0; from < n; from++) out[to] += mult[from][to];
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(5, new int[][] {{0, 1}, {0, 2}, {3, 2}, {1, 2}, {0, 1}}), new int[] {0, 2, 3, 0, 0}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(solve(4, new int[][] {{2, 2}, {1, 3}}), new int[] {0, 0, 1, 1}))
            throw new AssertionError("example 2");
        if (!Arrays.equals(new int[3], new int[] {0, 0, 0})) throw new AssertionError("fresh array is zero");
        if (!Arrays.equals(solve(3, new int[0][]), new int[3])) throw new AssertionError("no arrows");
        Random rnd = new Random(23101);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(20);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            int[] got = solve(n, edges);
            if (!Arrays.deepEquals(edges, copy)) throw new AssertionError("input changed");
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("mismatch n=" + n);
            int sum = 0;
            for (int x : got) sum += x;
            if (sum != m) throw new AssertionError("total must equal arrow count");
        }
    }
}
```

#### Solution: [Vary] Courses Finishable In Order (LeetCode 207)
<!-- id: ug-courses-completable -->

**Approach.** Each pair `{a, b}` becomes the arrow b to a, so the pair adds one to the count of a and puts a in b's target list. Courses with count zero start in an `ArrayDeque`, and the loop removes the front course, adds one to a tally, and subtracts one from each target, queueing a target when its count reaches zero. The tally is returned as it stands. The oracle uses a Floyd-Warshall reachability closure: a course can be finished exactly when it is not on a cycle and no cycle course can reach it. The assertions also check that the cheaper guess, counting courses that start with no prerequisite, gives a wrong answer on a chain, and that `Collections.nCopies` hands back one shared list.

**Complexity.** Reading the pairs, running the queue and subtracting along each arrow all touch every course and every pair a constant number of times, so time and space are both linear in numCourses plus the number of pairs.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class CoursesCompletableSolution {
    static int solve(int numCourses, int[][] prerequisites) {
        int[] indegree = new int[numCourses];
        List<List<Integer>> after = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) after.add(new ArrayList<>());
        for (int[] p : prerequisites) {
            after.get(p[1]).add(p[0]);
            indegree[p[0]]++;
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int v = 0; v < numCourses; v++) {
            if (indegree[v] == 0) ready.add(v);
        }
        int removed = 0;
        while (!ready.isEmpty()) {
            int cur = ready.poll();
            removed++;
            for (int next : after.get(cur)) {
                if (--indegree[next] == 0) ready.add(next);
            }
        }
        return removed;
    }

    static int startsFree(int numCourses, int[][] prerequisites) {
        boolean[] hasNeed = new boolean[numCourses];
        for (int[] p : prerequisites) hasNeed[p[0]] = true;
        int free = 0;
        for (boolean b : hasNeed) if (!b) free++;
        return free;
    }

    static int oracle(int n, int[][] prerequisites) {
        boolean[][] reach = new boolean[n][n];
        for (int[] p : prerequisites) reach[p[1]][p[0]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        int ok = 0;
        for (int v = 0; v < n; v++) {
            boolean blocked = false;
            for (int c = 0; c < n; c++) {
                if (reach[c][c] && (c == v || reach[c][v])) blocked = true;
            }
            if (!blocked) ok++;
        }
        return ok;
    }

    public static void main(String[] args) {
        if (solve(4, new int[][] {{1, 0}, {2, 1}, {3, 2}}) != 4) throw new AssertionError("example 1");
        if (solve(5, new int[][] {{1, 0}, {2, 1}, {1, 2}, {3, 2}, {4, 3}}) != 1) throw new AssertionError("example 2");
        if (solve(2, new int[][] {{1, 1}}) != 1) throw new AssertionError("self loop blocks only itself");
        if (startsFree(4, new int[][] {{1, 0}, {2, 1}, {3, 2}}) == 4) throw new AssertionError("false friend must fail");
        List<List<Integer>> shared = Collections.nCopies(3, new ArrayList<Integer>());
        shared.get(0).add(7);
        if (shared.get(2).size() != 1 || shared.get(0) != shared.get(1)) throw new AssertionError("nCopies shares one list");
        int[] k = {2};
        if (--k[0] != 1 || k[0] != 1) throw new AssertionError("prefix decrement");
        Random rnd = new Random(23102);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(14);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) pre[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = pre[i].clone();
            int got = solve(n, pre);
            for (int i = 0; i < m; i++)
                if (!java.util.Arrays.equals(copy[i], pre[i])) throw new AssertionError("input changed");
            if (got != oracle(n, pre)) throw new AssertionError("mismatch n=" + n + " got " + got);
        }
    }
}
```

#### Solution: [Boundary] Several Initial Sources (Author exercise)
<!-- id: ug-several-sources -->

**Approach.** Count indegrees, then put every vertex whose count is zero into the first layer, isolated ones included. The loop handles one layer at a time: it freezes the queue size, removes exactly that many vertices, subtracts along their arrows, and queues newly freed vertices for the next layer. A counter goes up once for each non-empty layer, and a running total of removed vertices decides between the counter and -1. The oracle first uses a reachability closure to find whether any vertex is blocked by a cycle, and otherwise computes each vertex's level by repeated relaxation as one more than the largest level among its predecessors, so it never uses a queue. The checks also cover a graph of isolated vertices, which must finish in one round, and show that seeding only one source gives the wrong round count.

**Complexity.** The layered loop visits every vertex once and every arrow once, which is O(n + m) in time, and the lists, counts and queue together use O(n + m) memory.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SeveralSourcesSolution {
    static int solve(int n, int[][] edges) {
        int[] indegree = new int[n];
        List<List<Integer>> after = new ArrayList<>();
        for (int i = 0; i < n; i++) after.add(new ArrayList<>());
        for (int[] e : edges) {
            after.get(e[0]).add(e[1]);
            indegree[e[1]]++;
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int v = 0; v < n; v++) {
            if (indegree[v] == 0) ready.add(v);
        }
        int rounds = 0, removed = 0;
        while (!ready.isEmpty()) {
            rounds++;
            for (int left = ready.size(); left > 0; left--) {
                int cur = ready.poll();
                removed++;
                for (int next : after.get(cur)) {
                    if (--indegree[next] == 0) ready.add(next);
                }
            }
        }
        return removed == n ? rounds : -1;
    }

    static int oneSourceOnly(int n, int[][] edges) {
        int[] indegree = new int[n];
        List<List<Integer>> after = new ArrayList<>();
        for (int i = 0; i < n; i++) after.add(new ArrayList<>());
        for (int[] e : edges) {
            after.get(e[0]).add(e[1]);
            indegree[e[1]]++;
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int v = 0; v < n; v++) {
            if (indegree[v] == 0) {
                ready.add(v);
                break;
            }
        }
        int rounds = 0, removed = 0;
        while (!ready.isEmpty()) {
            rounds++;
            for (int left = ready.size(); left > 0; left--) {
                int cur = ready.poll();
                removed++;
                for (int next : after.get(cur)) {
                    if (--indegree[next] == 0) ready.add(next);
                }
            }
        }
        return removed == n ? rounds : -1;
    }

    static int oracle(int n, int[][] edges) {
        boolean[][] reach = new boolean[n][n];
        for (int[] e : edges) reach[e[0]][e[1]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int v = 0; v < n; v++) if (reach[v][v]) return -1;
        int[] level = new int[n];
        java.util.Arrays.fill(level, 1);
        for (int pass = 0; pass <= n; pass++)
            for (int[] e : edges) level[e[1]] = Math.max(level[e[1]], level[e[0]] + 1);
        int best = 0;
        for (int x : level) best = Math.max(best, x);
        return best;
    }

    public static void main(String[] args) {
        if (solve(6, new int[][] {{0, 1}, {2, 1}, {1, 3}}) != 3) throw new AssertionError("example 1");
        if (solve(4, new int[][] {{1, 2}, {2, 1}}) != -1) throw new AssertionError("example 2");
        if (solve(5, new int[0][]) != 1) throw new AssertionError("all isolated finish in one round");
        if (oneSourceOnly(5, new int[0][]) != -1) throw new AssertionError("one seed leaves vertices behind");
        if (oneSourceOnly(6, new int[][] {{0, 1}, {2, 1}, {1, 3}}) == 3) throw new AssertionError("false friend must fail");
        Random rnd = new Random(23103);
        int cyclic = 0;
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            int got = solve(n, edges);
            for (int i = 0; i < m; i++)
                if (!java.util.Arrays.equals(copy[i], edges[i])) throw new AssertionError("input changed");
            int want = oracle(n, edges);
            if (want == -1) cyclic++;
            if (got != want) throw new AssertionError("mismatch n=" + n + " got " + got + " want " + want);
        }
        if (cyclic == 0 || cyclic == 1500) throw new AssertionError("test mix");
    }
}
```

#### Solution: [Recognize] Course Order From Prerequisites (LeetCode 210)
<!-- id: ug-course-order -->

**Approach.** Turn each pair `{a, b}` into the arrow b to a, count how many arrows end at each course, and seed an `ArrayDeque` with the zero-count courses in ascending order. The loop appends the front course to `order`, then subtracts one from every course it points at and queues those that reach zero. After the queue empties, a full array is returned if it was filled completely, otherwise a new empty array. The oracle does not rebuild the order. It checks that the answer is a permutation in which every pair has b before a, and that the answer is empty exactly when the reachability closure shows some course on a cycle. The fixed examples pin the deterministic order, and the asserts also show that ascending labels fail the validity check on the first example's mirror image.

**Complexity.** Building the lists, seeding the queue and removing each course once all scale with courses plus pairs, so the run takes linear time in that sum and uses the same order of extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CourseOrderSolution {
    static int[] solve(int numCourses, int[][] prerequisites) {
        int[] indegree = new int[numCourses];
        List<List<Integer>> after = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) after.add(new ArrayList<>());
        for (int[] p : prerequisites) {
            after.get(p[1]).add(p[0]);
            indegree[p[0]]++;
        }
        ArrayDeque<Integer> ready = new ArrayDeque<>();
        for (int v = 0; v < numCourses; v++) {
            if (indegree[v] == 0) ready.add(v);
        }
        int[] order = new int[numCourses];
        int done = 0;
        while (!ready.isEmpty()) {
            int cur = ready.poll();
            order[done++] = cur;
            for (int next : after.get(cur)) {
                if (--indegree[next] == 0) ready.add(next);
            }
        }
        return done == numCourses ? order : new int[0];
    }

    static boolean valid(int n, int[][] pre, int[] order) {
        if (order.length != n) return false;
        int[] pos = new int[n];
        Arrays.fill(pos, -1);
        for (int i = 0; i < n; i++) {
            if (order[i] < 0 || order[i] >= n || pos[order[i]] != -1) return false;
            pos[order[i]] = i;
        }
        for (int[] p : pre) if (pos[p[1]] >= pos[p[0]]) return false;
        return true;
    }

    static boolean hasCycle(int n, int[][] pre) {
        boolean[][] reach = new boolean[n][n];
        for (int[] p : pre) reach[p[1]][p[0]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int v = 0; v < n; v++) if (reach[v][v]) return true;
        return false;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(5, new int[][] {{1, 3}, {4, 1}}), new int[] {0, 2, 3, 1, 4}))
            throw new AssertionError("example 1");
        if (solve(4, new int[][] {{1, 0}, {2, 1}, {1, 2}, {3, 0}}).length != 0) throw new AssertionError("example 2");
        int[][] backwards = {{2, 3}, {1, 2}};
        int[] byLabel = {0, 1, 2, 3};
        if (valid(4, backwards, byLabel)) throw new AssertionError("label order must fail");
        if (!valid(4, backwards, solve(4, backwards))) throw new AssertionError("kahn order must pass");
        Random rnd = new Random(23104);
        int empty = 0;
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(12);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) pre[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = pre[i].clone();
            int[] got = solve(n, pre);
            for (int i = 0; i < m; i++)
                if (!Arrays.equals(copy[i], pre[i])) throw new AssertionError("input changed");
            boolean cyc = hasCycle(n, pre);
            if (cyc) {
                empty++;
                if (got.length != 0) throw new AssertionError("cycle must give empty, n=" + n);
            } else if (!valid(n, pre, got)) {
                throw new AssertionError("invalid order n=" + n + " " + Arrays.toString(got));
            }
        }
        if (empty == 0 || empty == 1500) throw new AssertionError("test mix");
    }
}
```
