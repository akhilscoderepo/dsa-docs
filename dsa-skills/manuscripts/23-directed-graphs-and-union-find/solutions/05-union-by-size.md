<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Union By Size

#### Solution: [Build] Merge Two Roots (Author exercise)
<!-- id: dg-merge-two-roots -->

**Approach.**
The method creates `parent` with every element as its own root and `size` with every entry 1. For each pair it walks `parent` from both elements to find the roots `ra` and `rb`, and it stops when they are equal. Otherwise it compares `size[ra]` and `size[rb]`. Only a strictly smaller `ra` loses the comparison, so on a tie `rb` becomes the child of `ra`, as the specification demands. The loser gets the winner as its parent, and the winner's count grows by the loser's count.

The invariant is that `size[r]` equals the number of elements below r, including r, for every root r. Both reads of `size` happen at roots, so stale counts of inner elements never influence a decision. The method never shortens a path, which keeps the returned array equal to the tree that the rule produces. The oracle keeps a label per element and counts members from scratch, so it shares no code with the array walk.

**Complexity.**
- **Time** is O(m log n) for m operations, because the size rule bounds every walk by log2(n) steps.
- **Space** is O(n) for `parent` and `size`, and the result reuses `parent`.

```java run
import java.util.*;

public final class MergeTwoRoots {
    /**
     * Returns the parent array after union by size without path compression.
     * Time: O(m log n). Space: O(n).
     * Invariant: size[r] counts the elements of the tree of every root r.
     */
    static int[] unionBySize(int n, int[][] ops) {
        // Every element starts as the root of a tree with one element.
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        // Each operation costs two walks, and each walk has at most log2(n) steps.
        for (int[] op : ops) {
            int ra = op[0];
            // Climb until an element is its own parent.
            while (parent[ra] != ra) ra = parent[ra];
            int rb = op[1];
            while (parent[rb] != rb) rb = parent[rb];
            // Equal roots mean the elements are connected already.
            if (ra == rb) continue;
            // Only a strictly smaller ra loses; a tie keeps ra on top.
            int big = ra, small = rb;
            if (size[ra] < size[rb]) { big = rb; small = ra; }
            // Link the loser and move its count in the same step.
            parent[small] = big;
            size[big] += size[small];
        }
        return parent;
    }

    /** Oracle: relabels members of the losing group and counts members from scratch. */
    static int[] oracle(int n, int[][] ops) {
        int[] label = new int[n];
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) { label[i] = i; parent[i] = i; }
        for (int[] op : ops) {
            int la = label[op[0]], lb = label[op[1]];
            if (la == lb) continue;
            int ca = 0, cb = 0;
            for (int v = 0; v < n; v++) { if (label[v] == la) ca++; if (label[v] == lb) cb++; }
            int big = ca < cb ? lb : la;
            int small = big == la ? lb : la;
            parent[small] = big;
            for (int v = 0; v < n; v++) if (label[v] == small) label[v] = big;
        }
        return parent;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(unionBySize(6, new int[][] {{0, 1}, {2, 1}, {3, 4}, {4, 2}}), new int[] {0, 0, 0, 0, 3, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(unionBySize(4, new int[][] {{0, 1}, {2, 3}, {1, 3}}), new int[] {0, 0, 0, 2})) throw new AssertionError("ex2");
        // Random operations must produce the same parent array as the label oracle.
        Random rnd = new Random(2305);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(12);
            int m = rnd.nextInt(20);
            int[][] ops = new int[m][];
            for (int k = 0; k < m; k++) ops[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(unionBySize(n, ops), oracle(n, ops))) throw new AssertionError("random " + t);
        }
        // The size rule bounds every walk by log2(n) steps.
        int n = 256;
        int[][] chain = new int[n - 1][];
        for (int i = 0; i + 1 < n; i++) chain[i] = new int[] {i, i + 1};
        int[] p = unionBySize(n, chain);
        for (int v = 0; v < n; v++) {
            int steps = 0, x = v;
            while (p[x] != x) { x = p[x]; steps++; }
            if (steps > 8) throw new AssertionError("height " + steps);
        }
    }
}
```

#### Solution: [Vary] Repeated Unequal Merges (Author exercise)
<!-- id: dg-repeated-unequal -->

**Approach.**
The method runs the same merge loop as the first exercise and stores the count of each tree at its root. When a single element joins a large group, the single element's root is the smaller root, and the large root receives the added count. After the last pair, the method answers each element with `size[find(i)]`.

The invariant is that the count of a root equals the size of its group. The answer of any element is therefore the count of its root. Reading `size[i]` directly is wrong for an element that is not a root, because that entry stopped changing when the element became a child. The oracle merges explicit lists of members and reports the list length for each element.

**Complexity.**
- **Time** is O((n + m) log n), because each of the m merges and each of the n answers walks at most log2(n) links.
- **Space** is O(n) for `parent`, `size` and the result.

```java run
import java.util.*;

public final class RepeatedUnequal {
    /**
     * Returns the size of the group of every element after all pairs.
     * Time: O((n + m) log n). Space: O(n).
     * Invariant: size[r] equals the group size for every root r.
     */
    static int[] groupSize(int n, int[][] ops) {
        int[] parent = new int[n];
        int[] size = new int[n];
        // Each element starts alone, so every count is 1.
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        for (int[] op : ops) {
            int a = find(parent, op[0]);
            int b = find(parent, op[1]);
            // The same root on both sides adds no element to any group.
            if (a == b) continue;
            // The larger count stays on top so that walks stay short.
            if (size[a] < size[b]) { int t = a; a = b; b = t; }
            parent[b] = a;
            // Only the receiving root accumulates the added count.
            size[a] += size[b];
        }
        int[] out = new int[n];
        // Each answer reads the count at the root, never at the element.
        for (int i = 0; i < n; i++) out[i] = size[find(parent, i)];
        return out;
    }

    static int find(int[] parent, int x) {
        // Climb parent links until a root appears.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: explicit member lists, merged by copying. */
    static int[] oracle(int n, int[][] ops) {
        List<Set<Integer>> group = new ArrayList<>();
        for (int i = 0; i < n; i++) group.add(new HashSet<>(List.of(i)));
        for (int[] op : ops) {
            Set<Integer> ga = group.get(op[0]), gb = group.get(op[1]);
            if (ga == gb) continue;
            ga.addAll(gb);
            for (int v : gb) group.set(v, ga);
        }
        int[] out = new int[n];
        for (int i = 0; i < n; i++) out[i] = group.get(i).size();
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(groupSize(7, new int[][] {{0, 1}, {0, 2}, {0, 3}, {4, 5}, {6, 0}}), new int[] {5, 5, 5, 5, 2, 2, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(groupSize(6, new int[][] {{5, 4}, {4, 3}, {3, 2}, {2, 1}}), new int[] {1, 5, 5, 5, 5, 5})) throw new AssertionError("ex2");
        // Random pairs, with repeated and equal values, must match the list oracle.
        Random rnd = new Random(2306);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(12);
            int m = rnd.nextInt(20);
            int[][] ops = new int[m][];
            for (int k = 0; k < m; k++) ops[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(groupSize(n, ops), oracle(n, ops))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Already Connected (Author exercise)
<!-- id: dg-already-connected -->

**Approach.**
The method keeps `groups`, which starts at n, and `size`. For each pair it finds both roots. When the roots are equal, it skips the pair. A repeated pair, a reversed pair, a pair that closes a cycle and a pair with `a == b` all change nothing. When the roots differ, it links the smaller root under the larger root and adds the count. Then it lowers `groups` by one and updates the maximum with the count of the surviving root.

The invariant is that `groups` equals n minus the number of successful merges, and that `largest` equals the maximum count over all roots. The maximum can only change at a merge, and only the surviving root has a new count, so one comparison per merge keeps it exact. The early skip is what prevents double counting. Without it, `size` would exceed the number of elements and `groups` could go below the true value.

**Complexity.**
- **Time** is O(m log n), because each pair costs two walks of at most log2(n) steps.
- **Space** is O(n) for `parent` and `size`.

```java run
import java.util.*;

public final class AlreadyConnected {
    /**
     * Returns {number of groups, size of the largest group}.
     * Time: O(m log n). Space: O(n).
     * Invariant: groups = n - merges, and largest is the maximum root count.
     */
    static int[] summary(int n, int[][] ops) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int groups = n;
        int largest = 1;
        for (int[] op : ops) {
            int a = find(parent, op[0]);
            int b = find(parent, op[1]);
            // Equal roots cover repeats, reversals, cycles and a == b.
            if (a == b) continue;
            if (size[a] < size[b]) { int t = a; a = b; b = t; }
            parent[b] = a;
            size[a] += size[b];
            // Only a real merge lowers the group count.
            groups--;
            // Only the surviving root has a new count, so one comparison suffices.
            largest = Math.max(largest, size[a]);
        }
        return new int[] {groups, largest};
    }

    static int find(int[] parent, int x) {
        // Climb parent links until the root.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: builds the adjacency matrix and counts components with a depth-first search. */
    static int[] oracle(int n, int[][] ops) {
        boolean[][] adj = new boolean[n][n];
        for (int[] op : ops) { adj[op[0]][op[1]] = true; adj[op[1]][op[0]] = true; }
        boolean[] seen = new boolean[n];
        int groups = 0, largest = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            groups++;
            int count = 0;
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                count++;
                for (int w = 0; w < n; w++) if (adj[v][w] && !seen[w]) { seen[w] = true; stack.push(w); }
            }
            largest = Math.max(largest, count);
        }
        return new int[] {groups, largest};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(summary(4, new int[][] {{0, 1}, {1, 0}, {2, 2}, {1, 2}, {0, 2}}), new int[] {2, 3})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(3, new int[][] {{0, 1}, {1, 2}, {2, 0}, {0, 2}}), new int[] {1, 3})) throw new AssertionError("ex2");
        // Random pairs with many repeats must match the search oracle.
        Random rnd = new Random(2307);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(10);
            int m = rnd.nextInt(25);
            int[][] ops = new int[m][];
            for (int k = 0; k < m; k++) ops[k] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(summary(n, ops), oracle(n, ops))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Redundant Connection (LeetCode 684)
<!-- id: dg-redundant-connection -->

**Approach.**
The method scans the edges in input order and keeps a union by size structure over the vertices 1 to n. For each edge it finds the roots of both endpoints. Different roots mean the edge joins two separate trees, so the method merges them. Equal roots mean a path between the endpoints exists already, and this edge closes a cycle, so the method returns it at once.

The invariant is that after k edges the structure holds exactly the connected components of the first k edges. Those k edges contain no cycle. The graph is a tree plus one edge, so it has exactly one cycle. The first edge that closes a cycle is the cycle edge that appears last in the input. Every other cycle edge came earlier, and the scan merged it. That is the edge the statement asks for. The oracle removes each edge from the end and checks that the remaining graph is connected.

**Complexity.**
- **Time** is O(n log n), because the method performs n unions or finds with walks of at most log2(n) steps.
- **Space** is O(n) for `parent` and `size`.

```java run
import java.util.*;

public final class RedundantConnection {
    /**
     * Returns the first edge whose endpoints already share a root.
     * Time: O(n log n). Space: O(n).
     * Invariant: after k edges the structure equals the components of those k edges.
     */
    static int[] redundant(int[][] edges) {
        int n = edges.length;
        int[] parent = new int[n + 1];
        int[] size = new int[n + 1];
        for (int i = 0; i <= n; i++) { parent[i] = i; size[i] = 1; }
        // One pass over the edges in input order.
        for (int[] e : edges) {
            int a = find(parent, e[0]);
            int b = find(parent, e[1]);
            // Equal roots mean a path exists, so this edge closes the cycle.
            if (a == b) return e;
            // Different roots mean a safe merge of two trees.
            if (size[a] < size[b]) { int t = a; a = b; b = t; }
            parent[b] = a;
            size[a] += size[b];
        }
        // The input guarantees one cycle, so the loop returns before this line.
        return new int[0];
    }

    static int find(int[] parent, int x) {
        // Climb parent links until the root.
        while (parent[x] != x) x = parent[x];
        return x;
    }

    /** Oracle: remove each edge from the end and test whether the rest is connected. */
    static int[] oracle(int[][] edges) {
        int n = edges.length;
        for (int skip = n - 1; skip >= 0; skip--) {
            List<List<Integer>> adj = new ArrayList<>();
            for (int v = 0; v <= n; v++) adj.add(new ArrayList<>());
            for (int i = 0; i < n; i++) {
                if (i == skip) continue;
                adj.get(edges[i][0]).add(edges[i][1]);
                adj.get(edges[i][1]).add(edges[i][0]);
            }
            boolean[] seen = new boolean[n + 1];
            Deque<Integer> stack = new ArrayDeque<>();
            stack.push(1);
            seen[1] = true;
            int count = 0;
            while (!stack.isEmpty()) {
                int v = stack.pop();
                count++;
                for (int w : adj.get(v)) if (!seen[w]) { seen[w] = true; stack.push(w); }
            }
            if (count == n) return edges[skip];
        }
        return new int[0];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(redundant(new int[][] {{1, 2}, {2, 3}, {3, 4}, {1, 4}, {1, 5}}), new int[] {1, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(redundant(new int[][] {{2, 3}, {1, 2}, {1, 3}, {3, 4}}), new int[] {1, 3})) throw new AssertionError("ex2");
        // Random trees plus one extra edge, in random order, must match the removal oracle.
        Random rnd = new Random(2308);
        for (int t = 0; t < 500; t++) {
            int n = 3 + rnd.nextInt(8);
            Set<Long> used = new HashSet<>();
            List<int[]> es = new ArrayList<>();
            // A random tree: vertex v attaches to a smaller vertex.
            for (int v = 2; v <= n; v++) {
                int u = 1 + rnd.nextInt(v - 1);
                es.add(new int[] {u, v});
                used.add(u * 100L + v);
            }
            // One extra edge between two vertices not yet joined directly.
            while (true) {
                int u = 1 + rnd.nextInt(n - 1);
                int v = u + 1 + rnd.nextInt(n - u);
                if (used.add(u * 100L + v)) { es.add(new int[] {u, v}); break; }
            }
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            if (!Arrays.equals(redundant(arr), oracle(arr))) throw new AssertionError("random " + t);
        }
    }
}
```
