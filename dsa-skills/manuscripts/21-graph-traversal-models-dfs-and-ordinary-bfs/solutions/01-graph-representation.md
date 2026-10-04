<!-- solutions-for: 01-graph-representation -->
### Graph Representation

#### Solution: [Build] Undirected Adjacency Lists (Author exercise)
<!-- id: gt-undirected-lists -->

**Approach.** Create `n` empty lists first, then walk the edges once and append each end to the list of the other. The entries then number twice the edge count, and each list keeps arrival order. The oracle answers every vertex by scanning the whole edge list, which is the slow method of the lesson, and the assertions compare the two on random simple graphs, check the degree sum, and show that `Collections.nCopies` really would share one list.

**Complexity.** O(n + E) time to build, and O(n + E) space for the lists.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class UndirectedLists {
    static List<List<Integer>> solve(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) {
            adj.get(e[0]).add(e[1]);
            adj.get(e[1]).add(e[0]);
        }
        return adj;
    }

    static List<List<Integer>> oracle(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            List<Integer> hops = new ArrayList<>();
            for (int[] e : edges) {
                if (e[0] == v) hops.add(e[1]);
                else if (e[1] == v) hops.add(e[0]);
            }
            out.add(hops);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(4, new int[][] {{0, 1}, {1, 2}, {1, 3}}).toString().equals("[[1], [0, 2, 3], [1], [1]]"))
            throw new AssertionError("example 1");
        if (!solve(3, new int[][] {{2, 0}, {1, 2}}).toString().equals("[[2], [2], [0, 1]]"))
            throw new AssertionError("example 2");
        List<List<Integer>> shared = Collections.nCopies(3, new ArrayList<Integer>());
        shared.get(0).add(7);
        if (shared.get(2).size() != 1) throw new AssertionError("nCopies should share one list");
        Random rnd = new Random(21101);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<Long> seen = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            int tries = rnd.nextInt(14);
            for (int k = 0; k < tries; k++) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (u == v) continue;
                long key = Math.min(u, v) * 1000L + Math.max(u, v);
                if (seen.add(key)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            List<List<Integer>> got = solve(n, edges);
            if (!got.equals(oracle(n, edges))) throw new AssertionError("random " + t);
            int sum = 0;
            for (List<Integer> pile : got) sum += pile.size();
            if (sum != 2 * edges.length) throw new AssertionError("degree sum " + t);
        }
    }
}
```

#### Solution: [Vary] Directed Adjacency Lists (Author exercise)
<!-- id: gt-directed-lists -->

**Approach.** The list for each vertex is created before any edge is read, so a vertex that never appears keeps an empty list. Each pair then appends only its head to the list of its tail. The oracle recomputes every list by filtering the pairs on their first number. Random directed inputs, including pairs that point both ways between two vertices, and check that the entries across all lists equal the number of edges rather than twice that number.

**Complexity.** O(n + E) time and O(n + E) space.

```java run
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DirectedLists {
    static List<List<Integer>> solve(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        return adj;
    }

    static List<List<Integer>> oracle(int n, int[][] edges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            List<Integer> heads = new ArrayList<>();
            for (int[] e : edges) if (e[0] == v) heads.add(e[1]);
            out.add(heads);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!solve(4, new int[][] {{0, 1}, {2, 1}, {1, 3}}).toString().equals("[[1], [3], [1], []]"))
            throw new AssertionError("example 1");
        if (!solve(5, new int[][] {{3, 0}, {3, 4}}).toString().equals("[[], [], [], [0, 4], []]"))
            throw new AssertionError("example 2");
        Random rnd = new Random(21102);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            Set<Integer> seen = new HashSet<>();
            List<int[]> list = new ArrayList<>();
            for (int k = rnd.nextInt(16); k > 0; k--) {
                int u = rnd.nextInt(n), v = rnd.nextInt(n);
                if (seen.add(u * 100 + v)) list.add(new int[] {u, v});
            }
            int[][] edges = list.toArray(new int[0][]);
            List<List<Integer>> got = solve(n, edges);
            if (!got.equals(oracle(n, edges))) throw new AssertionError("random " + t);
            int total = 0;
            for (List<Integer> pile : got) total += pile.size();
            if (total != edges.length) throw new AssertionError("entry count " + t);
        }
    }
}
```

#### Solution: [Boundary] Parallel And Self Edges (Author exercise)
<!-- id: gt-parallel-and-self -->

**Approach.** The contract says the network is simple, so each vertex keeps a `HashSet` of neighbors. An edge whose ends are equal is skipped, and every other edge is added to the set of each end, so `[1,0]` after `[0,1]` changes nothing. The answer is the size of each set. The oracle uses a boolean matrix as an independent filing, which makes repeats and the order of the ends irrelevant by construction, and counts the true cells of each row off the diagonal. The assertions compare the two on random inputs that are rich in repeats and self edges.

**Complexity.** O(n + E) expected time, using hashing, and O(n + E) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ParallelAndSelf {
    static int[] solve(int n, int[][] edges) {
        List<Set<Integer>> nbrs = new ArrayList<>();
        for (int v = 0; v < n; v++) nbrs.add(new HashSet<>());
        for (int[] e : edges) {
            if (e[0] == e[1]) continue;
            nbrs.get(e[0]).add(e[1]);
            nbrs.get(e[1]).add(e[0]);
        }
        int[] out = new int[n];
        for (int v = 0; v < n; v++) out[v] = nbrs.get(v).size();
        return out;
    }

    static int[] oracle(int n, int[][] edges) {
        boolean[][] has = new boolean[n][n];
        for (int[] e : edges) {
            has[e[0]][e[1]] = true;
            has[e[1]][e[0]] = true;
        }
        int[] out = new int[n];
        for (int u = 0; u < n; u++)
            for (int v = 0; v < n; v++)
                if (u != v && has[u][v]) out[u]++;
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(3, new int[][] {{0, 1}, {1, 0}, {2, 2}}), new int[] {1, 1, 0}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(solve(4, new int[][] {{0, 1}, {0, 1}, {0, 2}, {3, 3}, {3, 0}}), new int[] {3, 1, 1, 1}))
            throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[][] {{0, 0}, {0, 0}}), new int[] {0}))
            throw new AssertionError("only self edges");
        Random rnd = new Random(21103);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7);
            int m = rnd.nextInt(20);
            int[][] edges = new int[m][2];
            for (int k = 0; k < m; k++) {
                edges[k][0] = rnd.nextInt(n);
                edges[k][1] = rnd.nextInt(n);
            }
            if (!Arrays.equals(solve(n, edges), oracle(n, edges))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Find Center Of Star Graph (LeetCode 1791)
<!-- id: gt-star-center -->

**Approach.** In a star with at least three vertices, the center is on every edge and each leaf is on exactly one, so the first two edges share exactly one label, and that label is the center. The check is a pair of comparisons and needs no filing at all. The oracle counts the degree of every label and returns the one with degree `n - 1`. The assertions build random stars with shuffled labels, edge order and end order, and compare both methods with the planted center.

**Complexity.** O(1) time and O(1) space for the shortcut, against O(n) for the degree count.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class StarCenter {
    static int solve(int[][] edges) {
        int a = edges[0][0], b = edges[0][1];
        return (a == edges[1][0] || a == edges[1][1]) ? a : b;
    }

    static int oracle(int[][] edges) {
        int n = edges.length + 1;
        int[] deg = new int[n + 1];
        for (int[] e : edges) { deg[e[0]]++; deg[e[1]]++; }
        for (int v = 1; v <= n; v++) if (deg[v] == n - 1) return v;
        throw new AssertionError("no center");
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{1, 2}, {2, 3}, {4, 2}}) != 2) throw new AssertionError("example 1");
        if (solve(new int[][] {{5, 1}, {5, 2}, {3, 5}, {5, 4}}) != 5) throw new AssertionError("example 2");
        Random rnd = new Random(21104);
        for (int t = 0; t < 3000; t++) {
            int n = 3 + rnd.nextInt(10);
            int center = 1 + rnd.nextInt(n);
            List<int[]> list = new ArrayList<>();
            for (int v = 1; v <= n; v++) {
                if (v == center) continue;
                list.add(rnd.nextBoolean() ? new int[] {center, v} : new int[] {v, center});
            }
            Collections.shuffle(list, rnd);
            int[][] edges = list.toArray(new int[0][]);
            if (solve(edges) != center) throw new AssertionError("shortcut " + t);
            if (oracle(edges) != center) throw new AssertionError("oracle " + t);
        }
    }
}
```
