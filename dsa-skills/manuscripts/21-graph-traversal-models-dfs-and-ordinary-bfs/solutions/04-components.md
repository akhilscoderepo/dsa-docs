<!-- solutions-for: 04-components -->
### Components

#### Solution: [Build] Count Components (Author exercise)
<!-- id: gt-count-components -->

**Approach.** Mark vertices in one shared array, loop over every vertex as a possible start, and launch one search only from an unmarked vertex, adding one to the tally each time. The search uses its own stack, which also keeps a long chain from needing deep recursion. The oracle is repeated label propagation: every vertex starts with its own number, each edge pulls both ends down to the smaller label, and the passes repeat until nothing changes, so the vertices that keep their own label are the smallest of their groups. That method uses no search at all. The assertions compare the two on random graphs, check the all-isolated case, check a chain of one hundred thousand vertices, and check that the group sizes sum to n.

**Complexity.** O(n + E) time for the loop and the searches together, and O(n + E) space for the lists, marks and stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class CountComponents {
    static int solve(int n, int[][] edges) {
        return sizesOf(n, edges).length;
    }

    static int oracle(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int c = 0;
        for (int v = 0; v < n; v++) if (label[v] == v) c++;
        return c;
    }

    static int[] labels(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                int m = Math.min(label[e[0]], label[e[1]]);
                if (label[e[0]] != m) { label[e[0]] = m; changed = true; }
                if (label[e[1]] != m) { label[e[1]] = m; changed = true; }
            }
        }
        return label;
    }

    static int[][] randomEdges(Random rnd, int n) {
        Set<Long> seen = new HashSet<>();
        List<int[]> list = new ArrayList<>();
        int tries = rnd.nextInt(2 * n + 1);
        for (int k = 0; k < tries; k++) {
            int u = rnd.nextInt(n), v = rnd.nextInt(n);
            if (u == v) continue;
            if (seen.add(Math.min(u, v) * 1000L + Math.max(u, v))) list.add(new int[] {u, v});
        }
        return list.toArray(new int[0][]);
    }

    static List<List<Integer>> lists(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int[] sizesOf(int n, int[][] edges) {
        List<List<Integer>> adj = lists(n, edges);
        boolean[] seen = new boolean[n];
        List<Integer> sizes = new ArrayList<>();
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int size = 0;
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                size++;
                for (int w : adj.get(v)) if (!seen[w]) { seen[w] = true; stack.push(w); }
            }
            sizes.add(size);
        }
        int[] out = new int[sizes.size()];
        for (int i = 0; i < out.length; i++) out[i] = sizes.get(i);
        return out;
    }

    static int[] oracleSizes(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int[] count = new int[n];
        for (int v = 0; v < n; v++) count[label[v]]++;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (count[v] > 0) out.add(count[v]);
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (solve(7, new int[][] {{0, 1}, {1, 2}, {3, 4}}) != 4) throw new AssertionError("example 1");
        if (solve(6, new int[][] {{0, 5}, {2, 3}, {3, 4}}) != 3) throw new AssertionError("example 2");
        if (solve(9, new int[0][]) != 9) throw new AssertionError("all isolated");
        int[][] chain = new int[99999][];
        for (int i = 0; i < chain.length; i++) chain[i] = new int[] {i, i + 1};
        if (solve(100000, chain) != 1) throw new AssertionError("long chain with the explicit stack");
        Random rnd = new Random(21401);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[][] edges = randomEdges(rnd, n);
            if (solve(n, edges) != oracle(n, edges)) throw new AssertionError("random " + t);
            int sum = 0;
            for (int s : sizesOf(n, edges)) sum += s;
            if (sum != n) throw new AssertionError("sizes sum " + t);
        }
    }
}
```

#### Solution: [Vary] Component Sizes (Author exercise)
<!-- id: gt-component-sizes -->

**Approach.** The loop is the same as for counting, with a counter that is set to zero when a search is launched, raised once per vertex popped, and appended to the answer when the stack empties. Because starts are tried in increasing order, each group is reported at its smallest vertex. The oracle groups vertices by their final label from repeated label propagation and lists the group sizes in order of label, which is the same order. The assertions also cover the all-isolated and fully connected cases and check that the sizes add up to n.

**Complexity.** Linear in the vertices plus the edges, with one extra list of at most n sizes.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ComponentSizes {
    static int[] solve(int n, int[][] edges) {
        return sizesOf(n, edges);
    }

    static int[] labels(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                int m = Math.min(label[e[0]], label[e[1]]);
                if (label[e[0]] != m) { label[e[0]] = m; changed = true; }
                if (label[e[1]] != m) { label[e[1]] = m; changed = true; }
            }
        }
        return label;
    }

    static int[][] randomEdges(Random rnd, int n) {
        Set<Long> seen = new HashSet<>();
        List<int[]> list = new ArrayList<>();
        int tries = rnd.nextInt(2 * n + 1);
        for (int k = 0; k < tries; k++) {
            int u = rnd.nextInt(n), v = rnd.nextInt(n);
            if (u == v) continue;
            if (seen.add(Math.min(u, v) * 1000L + Math.max(u, v))) list.add(new int[] {u, v});
        }
        return list.toArray(new int[0][]);
    }

    static List<List<Integer>> lists(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int[] sizesOf(int n, int[][] edges) {
        List<List<Integer>> adj = lists(n, edges);
        boolean[] seen = new boolean[n];
        List<Integer> sizes = new ArrayList<>();
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int size = 0;
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                size++;
                for (int w : adj.get(v)) if (!seen[w]) { seen[w] = true; stack.push(w); }
            }
            sizes.add(size);
        }
        int[] out = new int[sizes.size()];
        for (int i = 0; i < out.length; i++) out[i] = sizes.get(i);
        return out;
    }

    static int[] oracleSizes(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int[] count = new int[n];
        for (int v = 0; v < n; v++) count[label[v]]++;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (count[v] > 0) out.add(count[v]);
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(7, new int[][] {{0, 1}, {1, 2}, {3, 4}}), new int[] {3, 2, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(6, new int[][] {{0, 5}, {2, 3}, {3, 4}}), new int[] {2, 1, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(3, new int[0][]), new int[] {1, 1, 1})) throw new AssertionError("all isolated");
        if (!Arrays.equals(solve(3, new int[][] {{0, 1}, {1, 2}, {0, 2}}), new int[] {3})) throw new AssertionError("fully connected");
        Random rnd = new Random(21402);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[][] edges = randomEdges(rnd, n);
            int[] got = solve(n, edges);
            if (!Arrays.equals(got, oracleSizes(n, edges))) throw new AssertionError("random " + t);
            int sum = 0;
            for (int s : got) sum += s;
            if (sum != n) throw new AssertionError("sizes sum " + t);
        }
    }
}
```

#### Solution: [Boundary] No Edges And One Component (Author exercise)
<!-- id: gt-no-edges-one -->

**Approach.** Build one empty neighbor list per vertex so that isolated vertices still get a turn as a start, run the marking loop, and report how many searches were launched and the biggest size seen. With no edges every start launches its own search of size one, and with every pair joined the first search marks everything so no later start launches. The assertions test both extremes for every n from 1 to 40, and the random graphs are compared with the label propagation oracle.

**Complexity.** O(n + E) time and O(n + E) space, where E can be as large as n * (n - 1) / 2 in the dense case.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class BoundaryComponents {
    static int[] solve(int n, int[][] edges) {
        int[] sizes = sizesOf(n, edges);
        int best = 0;
        for (int s : sizes) best = Math.max(best, s);
        return new int[] {sizes.length, best};
    }

    static int[] labels(int n, int[][] edges) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] e : edges) {
                int m = Math.min(label[e[0]], label[e[1]]);
                if (label[e[0]] != m) { label[e[0]] = m; changed = true; }
                if (label[e[1]] != m) { label[e[1]] = m; changed = true; }
            }
        }
        return label;
    }

    static int[][] randomEdges(Random rnd, int n) {
        Set<Long> seen = new HashSet<>();
        List<int[]> list = new ArrayList<>();
        int tries = rnd.nextInt(2 * n + 1);
        for (int k = 0; k < tries; k++) {
            int u = rnd.nextInt(n), v = rnd.nextInt(n);
            if (u == v) continue;
            if (seen.add(Math.min(u, v) * 1000L + Math.max(u, v))) list.add(new int[] {u, v});
        }
        return list.toArray(new int[0][]);
    }

    static List<List<Integer>> lists(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        return adj;
    }

    static int[] sizesOf(int n, int[][] edges) {
        List<List<Integer>> adj = lists(n, edges);
        boolean[] seen = new boolean[n];
        List<Integer> sizes = new ArrayList<>();
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            int size = 0;
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                size++;
                for (int w : adj.get(v)) if (!seen[w]) { seen[w] = true; stack.push(w); }
            }
            sizes.add(size);
        }
        int[] out = new int[sizes.size()];
        for (int i = 0; i < out.length; i++) out[i] = sizes.get(i);
        return out;
    }

    static int[] oracleSizes(int n, int[][] edges) {
        int[] label = labels(n, edges);
        int[] count = new int[n];
        for (int v = 0; v < n; v++) count[label[v]]++;
        List<Integer> out = new ArrayList<>();
        for (int v = 0; v < n; v++) if (count[v] > 0) out.add(count[v]);
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(4, new int[0][]), new int[] {4, 1})) throw new AssertionError("example 1");
        int[][] all = {{0, 1}, {0, 2}, {0, 3}, {1, 2}, {1, 3}, {2, 3}};
        if (!Arrays.equals(solve(4, all), new int[] {1, 4})) throw new AssertionError("example 2");
        for (int n = 1; n <= 40; n++) {
            if (!Arrays.equals(solve(n, new int[0][]), new int[] {n, 1})) throw new AssertionError("isolated " + n);
            List<int[]> pairs = new ArrayList<>();
            for (int u = 0; u < n; u++) for (int v = u + 1; v < n; v++) pairs.add(new int[] {u, v});
            if (!Arrays.equals(solve(n, pairs.toArray(new int[0][])), new int[] {1, n})) throw new AssertionError("complete " + n);
        }
        Random rnd = new Random(21403);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[][] edges = randomEdges(rnd, n);
            int[] want = oracleSizes(n, edges);
            int best = 0, sum = 0;
            for (int s : want) { best = Math.max(best, s); sum += s; }
            if (sum != n) throw new AssertionError("oracle sum " + t);
            if (!Arrays.equals(solve(n, edges), new int[] {want.length, best})) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: gt-provinces -->

**Approach.** Treat the matrix as the graph: the neighbors of city v are the columns of row v that hold a 1. The loop over starts and the shared marks are unchanged, and each popped city scans its whole row. The oracle again uses label propagation, this time over matrix cells, and the assertions compare the two on random symmetric matrices and check the all-isolated and fully connected matrices for every size from 1 to 12.

**Complexity.** O(n * n) time, since each row is scanned once, and O(n) extra space for the marks and the stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class Provinces {
    static int solve(int[][] isConnected) {
        int n = isConnected.length;
        boolean[] seen = new boolean[n];
        int provinces = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            provinces++;
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                for (int w = 0; w < n; w++) {
                    if (isConnected[v][w] == 1 && !seen[w]) { seen[w] = true; stack.push(w); }
                }
            }
        }
        return provinces;
    }

    static int oracle(int[][] m) {
        int n = m.length;
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int u = 0; u < n; u++) {
                for (int v = 0; v < n; v++) {
                    if (m[u][v] == 1 && label[u] != label[v]) {
                        int lo = Math.min(label[u], label[v]);
                        label[u] = lo;
                        label[v] = lo;
                        changed = true;
                    }
                }
            }
        }
        int c = 0;
        for (int v = 0; v < n; v++) if (label[v] == v) c++;
        return c;
    }

    static int[][] randomMatrix(Random rnd, int n) {
        int[][] m = new int[n][n];
        for (int i = 0; i < n; i++) m[i][i] = 1;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (rnd.nextInt(5) == 0) { m[i][j] = 1; m[j][i] = 1; }
            }
        }
        return m;
    }

    public static void main(String[] args) {
        if (solve(new int[][] {{1, 1, 0, 0}, {1, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}}) != 3) throw new AssertionError("example 1");
        if (solve(new int[][] {{1, 0, 1}, {0, 1, 0}, {1, 0, 1}}) != 2) throw new AssertionError("example 2");
        for (int n = 1; n <= 12; n++) {
            int[][] iso = new int[n][n];
            int[][] full = new int[n][n];
            for (int i = 0; i < n; i++) {
                iso[i][i] = 1;
                Arrays.fill(full[i], 1);
            }
            if (solve(iso) != n) throw new AssertionError("isolated " + n);
            if (solve(full) != 1) throw new AssertionError("complete " + n);
        }
        Random rnd = new Random(21404);
        for (int t = 0; t < 3000; t++) {
            int[][] m = randomMatrix(rnd, 1 + rnd.nextInt(12));
            if (solve(m) != oracle(m)) throw new AssertionError("random " + t);
        }
    }
}
```

