<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Kahn Topological Order

#### Solution: [Build] Compute Indegrees (Author exercise)
<!-- id: dg-compute-indegrees -->

**Approach.**
The method allocates `indegree` with `n` zeros and reads each entry of `edges` once. For an entry `[a, b]` it adds 1 at index `b`, because the edge ends at `b`. The start vertex `a` plays no role, so repeated entries and self loops need no special branch.

The invariant is that after the first `k` entries the array equals the indegree vector of those `k` entries alone. Each entry changes exactly one cell by one, so the invariant carries to `k + 1`. When all entries are read, the vector is the answer. The code asserts that `new int[n]` starts with zeros, which the first step relies on.

**Complexity.**
- **Time** is O(n + m) for m entries, because the allocation touches n cells and the loop reads each entry once.
- **Space** is O(n) for the result array, with no other structure.

```java run
import java.util.*;

public final class ComputeIndegrees {
    /**
     * Returns the indegree of every vertex.
     * Time: O(n + m). Space: O(n).
     * Invariant: after k entries, indegree equals the counts of those k entries.
     */
    static int[] indegree(int n, int[][] edges) {
        // A fresh int array holds zeros, so each vertex starts with no incoming edge.
        int[] indegree = new int[n];
        // One read per entry gives the O(m) term.
        for (int[] e : edges) {
            // The end vertex e[1] receives the edge, whatever the start vertex is.
            indegree[e[1]]++;
        }
        // The caller owns the result and the input stays unchanged.
        return indegree;
    }

    /** Brute force: for each vertex, count the matching entries with a separate scan. */
    static int[] oracle(int n, int[][] edges) {
        int[] out = new int[n];
        for (int v = 0; v < n; v++) {
            int c = 0;
            for (int[] e : edges) if (e[1] == v) c++;
            out[v] = c;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(indegree(5, new int[][] {{0, 1}, {0, 2}, {1, 2}, {3, 2}, {2, 4}}), new int[] {0, 1, 3, 0, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(indegree(3, new int[][] {{0, 1}, {0, 1}, {2, 2}}), new int[] {0, 2, 1})) throw new AssertionError("ex2");
        // Java fact: a new int array starts with zeros.
        for (int x : new int[4]) if (x != 0) throw new AssertionError("zero fill");
        // Random graphs with repeats and self loops must match the scan oracle.
        Random rnd = new Random(2301);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(15);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = Arrays.stream(edges).map(int[]::clone).toArray(int[][]::new);
            if (!Arrays.equals(indegree(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
            // The input must not be modified.
            if (!Arrays.deepEquals(edges, copy)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Vary] Can All Courses Finish (LeetCode 207)
<!-- id: dg-course-schedule -->

**Approach.**
The method turns each entry `[a, b]` into an edge from `b` to `a` and computes the indegrees. It puts every course of indegree 0 into a queue. Each removal decrements the indegree of every follower, and a follower whose counter reaches 0 joins the queue. The method counts removals and returns whether the count equals `numCourses`.

The invariant is that the queue holds exactly the unremoved courses whose remaining prerequisites are all removed. Removed courses form a prefix of some valid order, so a full count proves an order exists. If the queue empties earlier, each remaining course still waits for another remaining course. Then the remaining prerequisites contain a cycle, and no order exists. A self entry keeps its own counter above 0 forever.

**Complexity.**
- **Time** is O(V + E), because each course enters the queue once and the method decrements each entry once.
- **Space** is O(V + E) for the adjacency list, the counters and the queue.

```java run
import java.util.*;

public final class CourseSchedule {
    /**
     * Returns true when all courses can be completed.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the queue holds the unremoved courses whose prerequisites are all removed.
     */
    static boolean canFinish(int numCourses, int[][] prerequisites) {
        // An entry [a, b] becomes the edge from b to a.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < numCourses; v++) adj.add(new ArrayList<>());
        int[] indeg = new int[numCourses];
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            indeg[p[0]]++;
        }
        // Every course without a waiting prerequisite is available at the start.
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int v = 0; v < numCourses; v++) if (indeg[v] == 0) queue.add(v);
        int removed = 0;
        // Each iteration removes one available course, which costs O(1) plus its edges.
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            removed++;
            // The decrement reads each edge once overall.
            for (int next : adj.get(cur)) {
                // A counter that reaches 0 makes the follower available exactly once.
                if (--indeg[next] == 0) queue.add(next);
            }
        }
        // A shortfall means a cycle keeps some courses waiting.
        return removed == numCourses;
    }

    /** Brute force: transitive closure by Warshall; a cycle exists exactly when some course reaches itself. */
    static boolean oracle(int n, int[][] prerequisites) {
        boolean[][] reach = new boolean[n][n];
        for (int[] p : prerequisites) reach[p[1]][p[0]] = true;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        for (int v = 0; v < n; v++) if (reach[v][v]) return false;
        return true;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canFinish(4, new int[][] {{1, 0}, {2, 1}, {3, 1}, {3, 2}})) throw new AssertionError("ex1");
        if (canFinish(3, new int[][] {{1, 0}, {2, 1}, {1, 2}})) throw new AssertionError("ex2");
        // A self entry is a cycle of length one.
        if (canFinish(1, new int[][] {{0, 0}})) throw new AssertionError("self entry");
        // Java fact: the prefix decrement returns the new value, so the test fires exactly at 0.
        int[] c = {1};
        if (--c[0] != 0 || c[0] != 0) throw new AssertionError("prefix decrement");
        // Random graphs must agree with the closure oracle.
        Random rnd = new Random(2302);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(10);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) pre[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (canFinish(n, pre) != oracle(n, pre)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Several Initial Sources (Author exercise)
<!-- id: dg-several-sources -->

**Approach.**
The method computes the indegrees and collects every vertex of indegree 0 by one scan over `0..n-1`, which yields the first round in ascending order. To build the next round, it decrements the followers of each vertex of the current round and collects the followers whose counter reaches 0. It sorts that collection, stores it as the next row and repeats until a round is empty.

The invariant is that the current round contains exactly the vertices whose indegree is 0 after all earlier rounds. The first scan includes isolated vertices, because their counters are 0. A vertex enters the next round only when its last waiting predecessor is in the current round, so no vertex appears twice. Vertices on a cycle never reach 0 and never appear. The sort makes the output independent of edge order.

**Complexity.**
- **Time** is O(V + E + V log V), because the edges are read once and the sorting of all rows costs at most V log V.
- **Space** is O(V + E) for the adjacency list, the counters and the rows.

```java run
import java.util.*;

public final class SeveralSources {
    /**
     * Returns the removal rounds, each row ascending.
     * Time: O(V + E + V log V). Space: O(V + E).
     * Invariant: the current round holds the vertices of indegree 0 after all earlier rounds.
     */
    static int[][] rounds(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        int[] indeg = new int[n];
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            indeg[e[1]]++;
        }
        // The first round holds every vertex of indegree 0, isolated vertices included.
        List<Integer> current = new ArrayList<>();
        for (int v = 0; v < n; v++) if (indeg[v] == 0) current.add(v);
        List<int[]> rows = new ArrayList<>();
        // The loop ends at the first empty round, which a cycle or the end of the graph causes.
        while (!current.isEmpty()) {
            rows.add(current.stream().mapToInt(Integer::intValue).toArray());
            List<Integer> next = new ArrayList<>();
            // Removing the whole round lowers the counters of its followers.
            for (int cur : current) {
                for (int follower : adj.get(cur)) {
                    // A counter at 0 means the last waiting predecessor was in this round.
                    if (--indeg[follower] == 0) next.add(follower);
                }
            }
            // Sorting removes the dependence on the order of the edges.
            Collections.sort(next);
            current = next;
        }
        return rows.toArray(new int[0][]);
    }

    /** Brute force: repeated scans with a removed flag and a fresh snapshot per round. */
    static int[][] oracle(int n, int[][] edges) {
        boolean[] removed = new boolean[n];
        List<int[]> rows = new ArrayList<>();
        while (true) {
            List<Integer> round = new ArrayList<>();
            for (int v = 0; v < n; v++) {
                if (removed[v]) continue;
                boolean free = true;
                for (int[] e : edges) if (e[1] == v && !removed[e[0]]) free = false;
                if (free) round.add(v);
            }
            if (round.isEmpty()) break;
            for (int v : round) removed[v] = true;
            rows.add(round.stream().mapToInt(Integer::intValue).toArray());
        }
        return rows.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(rounds(6, new int[][] {{0, 2}, {1, 2}, {2, 3}, {1, 4}, {4, 3}}), new int[][] {{0, 1, 5}, {2, 4}, {3}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(rounds(4, new int[][] {{1, 2}, {2, 1}}), new int[][] {{0, 3}})) throw new AssertionError("ex2");
        // A graph whose every vertex lies on a cycle gives no row.
        if (rounds(2, new int[][] {{0, 1}, {1, 0}}).length != 0) throw new AssertionError("all cyclic");
        // Random graphs, shuffled edges, repeats and self loops, against the scan oracle.
        Random rnd = new Random(2303);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.deepEquals(rounds(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Course Schedule With An Order (LeetCode 210)
<!-- id: dg-course-order -->

**Approach.**
The method builds the adjacency list so that the followers of a course appear in the order of the entries. It computes the indegrees, enqueues every course of indegree 0 in ascending order and then removes courses first in, first out. Each removal writes the course into the next free cell of `order`, decrements the followers and enqueues those that reach 0. At the end it returns `order` when the count equals `numCourses`, and an empty array otherwise.

The invariant is that every course already written has all its prerequisites written before it, because a course joins the queue only after its counter reaches 0. A full array is therefore a valid order. A partial count means every unwritten course waits for another unwritten course, so a cycle exists and the empty array is correct. The fixed queue rule and the fixed follower order make the result unique, which the examples rely on.

**Complexity.**
- **Time** is O(V + E), because each course enters the queue once and the method reads each entry at most twice.
- **Space** is O(V + E) for the adjacency list, the counters, the queue and the output.

```java run
import java.util.*;

public final class CourseOrder {
    /**
     * Returns a full course order, or an empty array when a cycle exists.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: each written course has all prerequisites written before it.
     */
    static int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < numCourses; v++) adj.add(new ArrayList<>());
        int[] indeg = new int[numCourses];
        // Entries are read in input order, which fixes the order of the followers.
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            indeg[p[0]]++;
        }
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The scan in ascending order fixes the initial queue order.
        for (int v = 0; v < numCourses; v++) if (indeg[v] == 0) queue.add(v);
        int[] order = new int[numCourses];
        int count = 0;
        // Each iteration writes one course, so the array fills from the left.
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            order[count++] = cur;
            // Each follower loses one waiting prerequisite.
            for (int next : adj.get(cur)) {
                if (--indeg[next] == 0) queue.add(next);
            }
        }
        // A shorter count means some courses wait on a cycle.
        return count == numCourses ? order : new int[0];
    }

    /** Oracle: validity of the order, and emptiness exactly when the closure shows a cycle. */
    static void check(int n, int[][] pre, int[] result) {
        boolean[][] reach = new boolean[n][n];
        for (int[] p : pre) reach[p[1]][p[0]] = true;
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (reach[i][k] && reach[k][j]) reach[i][j] = true;
        boolean cyclic = false;
        for (int v = 0; v < n; v++) if (reach[v][v]) cyclic = true;
        if (cyclic) {
            if (result.length != 0) throw new AssertionError("cycle needs empty result");
            return;
        }
        if (result.length != n) throw new AssertionError("length");
        int[] pos = new int[n];
        Arrays.fill(pos, -1);
        for (int i = 0; i < n; i++) {
            if (pos[result[i]] != -1) throw new AssertionError("repeat");
            pos[result[i]] = i;
        }
        for (int[] p : pre) if (pos[p[1]] >= pos[p[0]]) throw new AssertionError("entry violated");
    }

    public static void main(String[] args) {
        // The two examples of the exercise, with the exact order of the contract.
        if (!Arrays.equals(findOrder(5, new int[][] {{3, 4}, {1, 2}, {0, 1}}), new int[] {2, 4, 1, 3, 0})) throw new AssertionError("ex1");
        if (findOrder(3, new int[][] {{1, 0}, {0, 1}}).length != 0) throw new AssertionError("ex2");
        // A diamond graph has one exact queue order.
        if (!Arrays.equals(findOrder(4, new int[][] {{1, 0}, {2, 0}, {3, 1}, {3, 2}}), new int[] {0, 1, 2, 3})) throw new AssertionError("diamond");
        // Random graphs, checked by validity and by the closure test.
        Random rnd = new Random(2304);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(10);
            int[][] pre = new int[m][];
            for (int i = 0; i < m; i++) pre[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            check(n, pre, findOrder(n, pre));
        }
    }
}
```
