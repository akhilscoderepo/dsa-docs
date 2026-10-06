<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Find Compression

#### Solution: [Build] Follow Parents To Root (Author exercise)
<!-- id: dg-follow-to-root -->

**Approach.**
For each query the method starts at the query vertex and replaces the vertex by its parent until the vertex is its own parent. A counter holds the number of replacements. The pair of the final vertex and the counter is the answer row. The method only reads `parent`, so every query repeats its full walk.

The invariant is that the current vertex lies on the path from the query to its root. The counter equals the distance from the query to the current vertex. The forest guarantee rules out a longer cycle, so the loop ends. A root answers with itself and zero steps, because the loop condition fails before the first replacement.

**Complexity.**
- **Time** is O(q * h), where q is the number of queries and h is the largest depth, so O(q * n) on a single chain.
- **Space** is O(q) for the answer rows, with O(1) extra memory for the walk.

```java run
import java.util.*;

public final class FollowToRoot {
    /**
     * Returns {root, steps} for every query without changing parent.
     * Time: O(q * h). Space: O(q) for the result.
     * Invariant: steps equals the distance from the query to the current vertex.
     */
    static int[][] followToRoot(int[] parent, int[] queries) {
        int[][] out = new int[queries.length][];
        for (int i = 0; i < queries.length; i++) {
            int v = queries[i];
            int steps = 0;
            // A root links to itself, so the loop stops there; each pass moves one link toward it.
            while (parent[v] != v) {
                v = parent[v];
                steps++;
            }
            out[i] = new int[] {v, steps};
        }
        return out;
    }

    /** Brute force: root and depth by plain recursion on the parent link. */
    static int[] oracle(int[] parent, int v) {
        if (parent[v] == v) return new int[] {v, 0};
        int[] up = oracle(parent, parent[v]);
        return new int[] {up[0], up[1] + 1};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(followToRoot(new int[] {0, 0, 1, 2, 3}, new int[] {4, 0, 2}), new int[][] {{0, 4}, {0, 0}, {0, 2}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(followToRoot(new int[] {0, 1, 1, 2, 4, 4}, new int[] {3, 5, 1}), new int[][] {{1, 2}, {4, 1}, {1, 0}})) throw new AssertionError("ex2");
        // Java fact: the method leaves its input array unchanged.
        int[] keep = {0, 0, 1, 2, 3};
        followToRoot(keep, new int[] {4, 3});
        if (!Arrays.equals(keep, new int[] {0, 0, 1, 2, 3})) throw new AssertionError("mutation");
        // Random forests with shuffled labels must match the recursive oracle.
        Random rnd = new Random(2343);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] raw = new int[n];
            for (int v = 0; v < n; v++) raw[v] = (v == 0 || rnd.nextInt(4) == 0) ? v : rnd.nextInt(v);
            // A random relabeling hides the order parent[v] <= v.
            List<Integer> perm = new ArrayList<>();
            for (int v = 0; v < n; v++) perm.add(v);
            Collections.shuffle(perm, rnd);
            int[] parent = new int[n];
            for (int v = 0; v < n; v++) parent[perm.get(v)] = perm.get(raw[v]);
            int q = rnd.nextInt(6);
            int[] queries = new int[q];
            for (int i = 0; i < q; i++) queries[i] = rnd.nextInt(n);
            int[][] got = followToRoot(parent, queries);
            for (int i = 0; i < q; i++) {
                if (!Arrays.equals(got[i], oracle(parent, queries[i]))) throw new AssertionError("random " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Compress A Chain (Author exercise)
<!-- id: dg-compress-chain -->

**Approach.**
The method copies `parent` and handles each query with two loops. The first loop follows the links from the query to the root. The second loop starts at the query again. It saves the old link in a local variable, sets the link of the current vertex to the root and moves to the saved vertex. It stops when the current vertex already points at the root.

The invariant is that every rewrite replaces a link by the root of the same tree, so the vertex still leads to the same root. Vertices off the queried path are never visited and keep their links. Saving the old link before the write keeps the walk on the original path. The copy leaves the input array intact.

**Complexity.**
- **Time** is O(n + q log n) amortized, because the first query on a long chain pays up to n links and path compression keeps later queries cheap.
- **Space** is O(n) for the copy of the array.

```java run
import java.util.*;

public final class CompressChain {
    /**
     * Returns the parent array after each query compressed its path to the root.
     * Time: O(n + q log n) amortized. Space: O(n).
     * Invariant: a rewritten link points at the root the vertex already led to.
     */
    static int[] compress(int[] parentIn, int[] queries) {
        int[] parent = parentIn.clone();
        for (int x : queries) {
            // First pass: walk the links until a vertex is its own parent.
            int root = x;
            while (parent[root] != root) root = parent[root];
            // Second pass: rewrite each visited link to the root.
            int cur = x;
            while (parent[cur] != root) {
                // The old link is saved first, or the walk would lose the path.
                int next = parent[cur];
                parent[cur] = root;
                cur = next;
            }
        }
        return parent;
    }

    /** Brute force: the textbook recursive find with compression on the way back. */
    static int find(int[] p, int v) {
        if (p[v] == v) return v;
        p[v] = find(p, p[v]);
        return p[v];
    }

    static int[] oracle(int[] parentIn, int[] queries) {
        int[] p = parentIn.clone();
        for (int x : queries) find(p, x);
        return p;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(compress(new int[] {0, 0, 1, 2, 3}, new int[] {4}), new int[] {0, 0, 0, 0, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(compress(new int[] {0, 0, 1, 2, 3}, new int[] {2, 3}), new int[] {0, 0, 0, 0, 3})) throw new AssertionError("ex2");
        // Java fact: the iterative loops survive a chain of 100000 vertices, and the input stays unchanged.
        int[] chain = new int[100000];
        for (int i = 1; i < chain.length; i++) chain[i] = i - 1;
        int[] flat = compress(chain, new int[] {99999});
        if (flat[99999] != 0 || flat[50000] != 0 || chain[99999] != 99998) throw new AssertionError("long chain");
        // Random forests with shuffled labels must match the recursive oracle.
        Random rnd = new Random(2353);
        for (int t = 0; t < 1000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] raw = new int[n];
            for (int v = 0; v < n; v++) raw[v] = (v == 0 || rnd.nextInt(4) == 0) ? v : rnd.nextInt(v);
            List<Integer> perm = new ArrayList<>();
            for (int v = 0; v < n; v++) perm.add(v);
            Collections.shuffle(perm, rnd);
            int[] parent = new int[n];
            for (int v = 0; v < n; v++) parent[perm.get(v)] = perm.get(raw[v]);
            int q = rnd.nextInt(6);
            int[] queries = new int[q];
            for (int i = 0; i < q; i++) queries[i] = rnd.nextInt(n);
            if (!Arrays.equals(compress(parent, queries), oracle(parent, queries))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Singleton Components (Author exercise)
<!-- id: dg-singleton-components -->

**Approach.**
The structure starts with `parent[i] = i`, so every element is the root of a group of one. A merge calls `find` on both arguments and links one root to the other only when the roots differ. A question compares the two roots. Equal arguments have equal roots, so a merge of an element with itself and a repeated merge both change nothing.

The invariant is that following `parent` from any element reaches exactly one root, and only roots are ever linked. An untouched element has itself as root, so a question about two different untouched elements answers false and a question about one element and itself answers true. Compression in `find` rewrites links to the same root, so it cannot change an answer.

**Complexity.**
- **Time** is O(n + m log n) amortized for m operations. The n term is the initialization, and two finds dominate each operation.
- **Space** is O(n) for the `parent` array.

```java run
import java.util.*;

public final class SingletonComponents {
    static final class Groups {
        private final int[] parent;

        Groups(int n) {
            // Every element is its own root, so n groups of size one exist.
            parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        int find(int x) {
            // First pass finds the root.
            int root = x;
            while (parent[root] != root) root = parent[root];
            // Second pass points each visited element at the root.
            int cur = x;
            while (parent[cur] != root) {
                int next = parent[cur];
                parent[cur] = root;
                cur = next;
            }
            return root;
        }

        void merge(int a, int b) {
            int ra = find(a), rb = find(b);
            // Linking equal roots would create a cycle of links, so equal roots are skipped.
            if (ra != rb) parent[ra] = rb;
        }

        boolean same(int a, int b) {
            return find(a) == find(b);
        }
    }

    /**
     * Returns one answer per type 1 operation.
     * Time: O(n + m log n) amortized. Space: O(n).
     * Invariant: only roots are linked, so every element leads to one root.
     */
    static boolean[] process(int n, int[][] ops) {
        Groups groups = new Groups(n);
        List<Boolean> answers = new ArrayList<>();
        for (int[] op : ops) {
            // Type 0 merges, type 1 asks.
            if (op[0] == 0) groups.merge(op[1], op[2]);
            else answers.add(groups.same(op[1], op[2]));
        }
        boolean[] out = new boolean[answers.size()];
        for (int i = 0; i < out.length; i++) out[i] = answers.get(i);
        return out;
    }

    /** Brute force: a label array that relabels the whole second group on each merge. */
    static boolean[] oracle(int n, int[][] ops) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        List<Boolean> answers = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) {
                int from = label[op[2]], to = label[op[1]];
                for (int i = 0; i < n; i++) if (label[i] == from) label[i] = to;
            } else answers.add(label[op[1]] == label[op[2]]);
        }
        boolean[] out = new boolean[answers.size()];
        for (int i = 0; i < out.length; i++) out[i] = answers.get(i);
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(process(3, new int[][] {{1, 0, 0}, {1, 0, 1}, {0, 0, 1}, {1, 0, 1}}), new boolean[] {true, false, true})) throw new AssertionError("ex1");
        if (!Arrays.equals(process(4, new int[][] {{0, 2, 2}, {1, 2, 3}, {0, 2, 3}, {0, 3, 2}, {1, 3, 2}, {1, 1, 1}}), new boolean[] {false, true, true})) throw new AssertionError("ex2");
        // Java fact: a fresh structure gives every element itself as root.
        Groups fresh = new Groups(5);
        for (int i = 0; i < 5; i++) if (fresh.find(i) != i) throw new AssertionError("singleton root");
        // Random operation lists, with equal arguments allowed, must match the label oracle.
        Random rnd = new Random(2363);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            int m = rnd.nextInt(14);
            int[][] ops = new int[m][];
            for (int i = 0; i < m; i++) ops[i] = new int[] {rnd.nextInt(2), rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(process(n, ops), oracle(n, ops))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Number Of Provinces (LeetCode 547)
<!-- id: dg-provinces -->

**Approach.**
The method starts with `n` singleton groups and a counter equal to `n`. It reads the upper triangle of the matrix. For each entry equal to 1 it finds the roots of the two cities and links them when they differ, and each successful link lowers the counter by one. The counter then equals the number of groups.

The invariant is that the counter equals the number of roots in the structure. Each successful link removes exactly one root, and a failed link means the cities already share a group. Every pair joined through other cities ends in one group, because the matrix entries along a path link its cities one by one. The diagonal and the lower triangle add no information.

**Complexity.**
- **Time** is O(n^2 log n) amortized, because the method reads n^2 / 2 entries and each successful or failed entry costs two finds.
- **Space** is O(n) for the `parent` array.

```java run
import java.util.*;

public final class Provinces {
    /**
     * Returns the number of connected groups of cities.
     * Time: O(n^2 log n) amortized. Space: O(n).
     * Invariant: count equals the number of roots in parent.
     */
    static int provinces(int[][] isConnected) {
        int n = isConnected.length;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int count = n;
        // Only entries above the diagonal are read, since the matrix is symmetric.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isConnected[i][j] == 0) continue;
                int ri = find(parent, i), rj = find(parent, j);
                // Equal roots mean the cities already share a group, so no group disappears.
                if (ri == rj) continue;
                // Linking two different roots removes exactly one group.
                parent[ri] = rj;
                count--;
            }
        }
        return count;
    }

    private static int find(int[] parent, int x) {
        // First pass finds the root; second pass points the visited path at it.
        int root = x;
        while (parent[root] != root) root = parent[root];
        int cur = x;
        while (parent[cur] != root) {
            int next = parent[cur];
            parent[cur] = root;
            cur = next;
        }
        return root;
    }

    /** Brute force: count the start vertices of a recursive depth-first search. */
    static int oracle(int[][] m) {
        boolean[] seen = new boolean[m.length];
        int groups = 0;
        for (int s = 0; s < m.length; s++) {
            if (seen[s]) continue;
            groups++;
            visit(m, seen, s);
        }
        return groups;
    }

    private static void visit(int[][] m, boolean[] seen, int v) {
        seen[v] = true;
        for (int w = 0; w < m.length; w++) if (m[v][w] == 1 && !seen[w]) visit(m, seen, w);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (provinces(new int[][] {{1, 1, 0}, {1, 1, 0}, {0, 0, 1}}) != 2) throw new AssertionError("ex1");
        int[][] second = {{1, 0, 0, 1, 0}, {0, 1, 0, 1, 0}, {0, 0, 1, 0, 0}, {1, 1, 0, 1, 0}, {0, 0, 0, 0, 1}};
        if (provinces(second) != 3) throw new AssertionError("ex2");
        // Java fact: the method leaves the input matrix unchanged.
        if (second[3][1] != 1 || second[1][3] != 1) throw new AssertionError("mutation");
        // Random symmetric matrices with a full diagonal must match the search count.
        Random rnd = new Random(2373);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            int[][] m = new int[n][n];
            for (int i = 0; i < n; i++) {
                m[i][i] = 1;
                for (int j = i + 1; j < n; j++) m[i][j] = m[j][i] = rnd.nextInt(4) == 0 ? 1 : 0;
            }
            if (provinces(m) != oracle(m)) throw new AssertionError("random " + t);
        }
    }
}
```
