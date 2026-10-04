<!-- solutions-for: 05-union-by-size -->
### Union By Size

#### Solution: [Build] Merge Two Roots (Author exercise)
<!-- id: ug-merge-two-roots -->

**Approach.** Create `parent[i] = i` and `size[i] = 1`, then for each pair walk both elements up to their roots before touching any link. When the roots are equal the pair is skipped. Otherwise the root with the larger `size` receives the other (the first pair element's root wins a tie), and only the receiving root's `size` grows. The oracle never walks a tree: it keeps a label for every element and rewrites all labels of the losing group on each merge, writing the parent link at the two representatives, so a wrong root, a wrong tie or a wrong receiver all show up as a different array. The asserts also check three claims from the lesson. A fresh `int[]` is filled with zeros, which is why `size` must be filled with 1. A `size` array left at zero turns every comparison into a tie and rebuilds the chain the lesson warns about. Comparing the sizes of the original elements instead of their roots gives a different parent array on the second example.

**Complexity.** Each pair costs two root walks, and union by size keeps every walk at most log2(n) steps, so the total is O(m log n) for m pairs and O(n) memory for the two arrays.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MergeTwoRootsSolution {
    static int root(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] solve(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        for (int[] p : pairs) {
            int ra = root(parent, p[0]), rb = root(parent, p[1]);
            if (ra == rb) continue;
            if (size[ra] >= size[rb]) {
                parent[rb] = ra;
                size[ra] += size[rb];
            } else {
                parent[ra] = rb;
                size[rb] += size[ra];
            }
        }
        return parent;
    }

    static int[] sizesNeverFilled(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        for (int[] p : pairs) {
            int ra = root(parent, p[0]), rb = root(parent, p[1]);
            if (ra == rb) continue;
            if (size[ra] >= size[rb]) {
                parent[rb] = ra;
                size[ra] += size[rb];
            } else {
                parent[ra] = rb;
                size[rb] += size[ra];
            }
        }
        return parent;
    }

    static int[] elementsCompared(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        for (int[] p : pairs) {
            int a = p[0], b = p[1];
            int ra = root(parent, a), rb = root(parent, b);
            if (ra == rb) continue;
            if (size[a] >= size[b]) {
                parent[rb] = ra;
                size[a] += size[b];
            } else {
                parent[ra] = rb;
                size[b] += size[a];
            }
        }
        return parent;
    }

    static int[] oracle(int n, int[][] pairs) {
        int[] label = new int[n];
        int[] groupSize = new int[n];
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) {
            label[i] = i;
            groupSize[i] = 1;
            parent[i] = i;
        }
        for (int[] p : pairs) {
            int la = label[p[0]], lb = label[p[1]];
            if (la == lb) continue;
            int winner = groupSize[la] >= groupSize[lb] ? la : lb;
            int loser = winner == la ? lb : la;
            parent[loser] = winner;
            groupSize[winner] += groupSize[loser];
            for (int i = 0; i < n; i++) if (label[i] == loser) label[i] = winner;
        }
        return parent;
    }

    static int depth(int[] parent, int x) {
        int d = 0;
        while (parent[x] != x) {
            x = parent[x];
            d++;
        }
        return d;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1}, {2, 3}, {1, 3}};
        if (!Arrays.equals(solve(5, ex1), new int[] {0, 0, 0, 2, 4})) throw new AssertionError("example 1");
        int[][] ex2 = {{3, 2}, {1, 0}, {2, 1}, {4, 3}, {5, 4}};
        if (!Arrays.equals(solve(6, ex2), new int[] {1, 3, 3, 3, 3, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(elementsCompared(6, ex2), new int[] {1, 5, 3, 1, 1, 5}))
            throw new AssertionError("false friend shape");
        if (Arrays.equals(elementsCompared(6, ex2), solve(6, ex2))) throw new AssertionError("false friend must differ");
        int[] zeros = new int[4];
        if (!Arrays.equals(zeros, new int[] {0, 0, 0, 0})) throw new AssertionError("new int[] is zero filled");
        int n = 40;
        int[][] chain = new int[n - 1][];
        for (int k = 1; k < n; k++) chain[k - 1] = new int[] {k, 0};
        int[] good = solve(n, chain), bad = sizesNeverFilled(n, chain);
        if (depth(good, 0) != 1) throw new AssertionError("filled sizes give a star");
        if (depth(bad, 0) != n - 1) throw new AssertionError("unfilled sizes give a chain");
        Random rnd = new Random(23501);
        boolean falseFriendDiffered = false;
        for (int t = 0; t < 1500; t++) {
            int size = 1 + rnd.nextInt(12);
            int m = rnd.nextInt(16);
            int[][] pairs = new int[m][2];
            for (int i = 0; i < m; i++) pairs[i] = new int[] {rnd.nextInt(size), rnd.nextInt(size)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = pairs[i].clone();
            int[] got = solve(size, pairs);
            if (!Arrays.deepEquals(copy, pairs)) throw new AssertionError("input changed");
            if (!Arrays.equals(got, oracle(size, pairs))) throw new AssertionError("t=" + t);
            int bound = 31 - Integer.numberOfLeadingZeros(size);
            for (int v = 0; v < size; v++)
                if (depth(got, v) > bound) throw new AssertionError("height bound " + t);
            if (!Arrays.equals(elementsCompared(size, pairs), got)) falseFriendDiffered = true;
        }
        if (!falseFriendDiffered) throw new AssertionError("false friend never caught");
    }
}
```

#### Solution: [Vary] Repeated Unequal Merges (Author exercise)
<!-- id: ug-repeated-unequal -->

**Approach.** The linking rule is unchanged, so what changes is the bookkeeping: after a real merge, read the `size` of the receiving root, never of the other root, and fold it into a running maximum. A skipped pair leaves the maximum alone, and the answer for that position repeats the previous value. The oracle rebuilds the graph from the first k pairs for every k and spreads the smallest label along every edge until nothing changes, then counts how many elements share each label. The asserts show a Java detail the lesson relies on: when a root is attached its own `size` slot is left behind with the old number, so reading it later would give a stale value. They also run a variant that reads the loser's slot and show that it reports a smaller answer on the second example.

**Complexity.** The scan makes one pass over the pairs with two short root walks each, so it is O(m log n) in time, with O(n) for the arrays and O(m) for the answer, whereas the oracle spends O(m * n * m) in the worst case.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RepeatedUnequalSolution {
    static int root(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] solve(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int[] out = new int[pairs.length];
        int largest = 1;
        for (int i = 0; i < pairs.length; i++) {
            int ra = root(parent, pairs[i][0]), rb = root(parent, pairs[i][1]);
            if (ra != rb) {
                int big = size[ra] >= size[rb] ? ra : rb;
                int small = big == ra ? rb : ra;
                parent[small] = big;
                size[big] += size[small];
                largest = Math.max(largest, size[big]);
            }
            out[i] = largest;
        }
        return out;
    }

    static int[] readsLoserSize(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int[] out = new int[pairs.length];
        int largest = 1;
        for (int i = 0; i < pairs.length; i++) {
            int ra = root(parent, pairs[i][0]), rb = root(parent, pairs[i][1]);
            if (ra != rb) {
                int big = size[ra] >= size[rb] ? ra : rb;
                int small = big == ra ? rb : ra;
                parent[small] = big;
                size[big] += size[small];
                largest = Math.max(largest, size[small]);
            }
            out[i] = largest;
        }
        return out;
    }

    static int[] oracle(int n, int[][] pairs) {
        int[] out = new int[pairs.length];
        for (int k = 0; k < pairs.length; k++) {
            int[] label = new int[n];
            for (int i = 0; i < n; i++) label[i] = i;
            boolean changed = true;
            while (changed) {
                changed = false;
                for (int e = 0; e <= k; e++) {
                    int a = pairs[e][0], b = pairs[e][1];
                    int low = Math.min(label[a], label[b]);
                    if (label[a] != low) { label[a] = low; changed = true; }
                    if (label[b] != low) { label[b] = low; changed = true; }
                }
            }
            int[] count = new int[n];
            int best = 0;
            for (int i = 0; i < n; i++) best = Math.max(best, ++count[label[i]]);
            out[k] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{0, 1}, {2, 3}, {1, 3}, {4, 5}, {0, 2}};
        if (!Arrays.equals(solve(6, ex1), new int[] {2, 2, 4, 4, 4})) throw new AssertionError("example 1");
        int[][] ex2 = {{5, 6}, {4, 5}, {3, 4}, {0, 1}, {2, 3}, {1, 6}};
        if (!Arrays.equals(solve(7, ex2), new int[] {2, 3, 4, 4, 5, 7})) throw new AssertionError("example 2");
        if (Arrays.equals(readsLoserSize(7, ex2), solve(7, ex2))) throw new AssertionError("loser size is stale");
        if (solve(3, new int[0][]).length != 0) throw new AssertionError("no pairs");
        int[] parent = {0, 1, 2};
        int[] size = {1, 1, 1};
        parent[1] = 0;
        size[0] += size[1];
        if (size[1] != 1 || size[0] != 2) throw new AssertionError("loser slot keeps its old number");
        Random rnd = new Random(23502);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(10);
            int m = rnd.nextInt(14);
            int[][] pairs = new int[m][2];
            for (int i = 0; i < m; i++) pairs[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = pairs[i].clone();
            int[] got = solve(n, pairs);
            if (!Arrays.deepEquals(copy, pairs)) throw new AssertionError("input changed");
            if (!Arrays.equals(got, oracle(n, pairs))) throw new AssertionError("t=" + t);
        }
    }
}
```

#### Solution: [Boundary] Already Connected (Author exercise)
<!-- id: ug-already-connected -->

**Approach.** The only new line is the early exit: once both roots are found and they match, the pair is counted as ignored and the loop moves on before `size` or `count` is touched. That covers a repeated pair, a pair given in the other direction, a pair whose two ends joined through other pairs, and a pair that names one element twice. Real merges decrement `count` and keep the maximum of the receiving root's size. The oracle uses label propagation on the whole pair list for the component count and the largest group, and for each position it propagates over the earlier pairs only, calling a pair ignored when its two ends already share a label. The asserts also run a variant without the early exit, which doubles a size when a root is merged into itself, and show that in Java `size[r] += size[r]` really does double the entry.

**Complexity.** Every pair is handled in the time of two root walks, which is O(log n) with this rule, so the whole scan is O(m log n) with O(n) extra space, and the repeated pairs cost no more than the real ones.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AlreadyConnectedSolution {
    static int root(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] solve(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int count = n, ignored = 0, largest = 1;
        for (int[] p : pairs) {
            int ra = root(parent, p[0]), rb = root(parent, p[1]);
            if (ra == rb) {
                ignored++;
                continue;
            }
            int big = size[ra] >= size[rb] ? ra : rb;
            int small = big == ra ? rb : ra;
            parent[small] = big;
            size[big] += size[small];
            largest = Math.max(largest, size[big]);
            count--;
        }
        return new int[] {count, ignored, largest};
    }

    static int[] noEarlyExit(int n, int[][] pairs) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int count = n, largest = 1;
        for (int[] p : pairs) {
            int ra = root(parent, p[0]), rb = root(parent, p[1]);
            int big = size[ra] >= size[rb] ? ra : rb;
            int small = big == ra ? rb : ra;
            parent[small] = big;
            size[big] += size[small];
            largest = Math.max(largest, size[big]);
            count--;
        }
        return new int[] {count, 0, largest};
    }

    static int[] labels(int n, int[][] pairs, int upTo) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int e = 0; e < upTo; e++) {
                int a = pairs[e][0], b = pairs[e][1];
                int low = Math.min(label[a], label[b]);
                if (label[a] != low) { label[a] = low; changed = true; }
                if (label[b] != low) { label[b] = low; changed = true; }
            }
        }
        return label;
    }

    static int[] oracle(int n, int[][] pairs) {
        int ignored = 0;
        for (int e = 0; e < pairs.length; e++) {
            int[] before = labels(n, pairs, e);
            if (before[pairs[e][0]] == before[pairs[e][1]]) ignored++;
        }
        int[] label = labels(n, pairs, pairs.length);
        int[] tally = new int[n];
        int groups = 0, best = 0;
        for (int i = 0; i < n; i++) {
            if (tally[label[i]]++ == 0) groups++;
            best = Math.max(best, tally[label[i]]);
        }
        return new int[] {groups, ignored, best};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(4, new int[][] {{0, 1}, {1, 0}, {2, 2}}), new int[] {3, 2, 2}))
            throw new AssertionError("example 1");
        int[][] ex2 = {{0, 1}, {1, 2}, {2, 0}, {0, 2}, {3, 4}};
        if (!Arrays.equals(solve(5, ex2), new int[] {2, 2, 3})) throw new AssertionError("example 2");
        if (Arrays.equals(noEarlyExit(4, new int[][] {{0, 1}, {1, 0}}), solve(4, new int[][] {{0, 1}, {1, 0}})))
            throw new AssertionError("missing early exit must corrupt");
        if (noEarlyExit(4, new int[][] {{0, 1}, {1, 0}})[2] != 4) throw new AssertionError("size doubled");
        int[] size = {3};
        size[0] += size[0];
        if (size[0] != 6) throw new AssertionError("self add doubles");
        if (!Arrays.equals(solve(1, new int[0][]), new int[] {1, 0, 1})) throw new AssertionError("single element");
        Random rnd = new Random(23503);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(9);
            int m = rnd.nextInt(14);
            int[][] pairs = new int[m][2];
            for (int i = 0; i < m; i++) pairs[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = pairs[i].clone();
            int[] got = solve(n, pairs);
            if (!Arrays.deepEquals(copy, pairs)) throw new AssertionError("input changed");
            if (!Arrays.equals(got, oracle(n, pairs))) throw new AssertionError("t=" + t);
            if (got[0] + (m - got[1]) != n) throw new AssertionError("count identity");
        }
    }
}
```

#### Solution: [Recognize] Redundant Connection (LeetCode 684)
<!-- id: ug-redundant-connection -->

**Approach.** Walk the edges in input order with one disjoint set over the vertices 0 to n-1. For each edge find both roots first. If they match, the endpoints were already joined through earlier edges, so this edge completes a cycle and is returned as a fresh two-element array. If they differ, attach the root of the smaller group under the larger and add the sizes. Because the input is a tree plus exactly one extra edge, the first such edge is also the last edge of the input that can be deleted to leave a tree. The oracle checks exactly that second description: it tries to delete each edge from the end of the list backwards and uses a breadth-first search to see whether the remaining n-1 edges still reach every vertex. The asserts confirm that the result is a copy, that the input rows are not changed, and that a check comparing the endpoints themselves (`a == b`) never fires on a simple triangle.

**Complexity.** Each edge costs two root walks of at most log2(n) steps, which gives O(n log n) overall for n edges, and the arrays take O(n) space; the oracle is O(n^2) because it repeats a traversal per deleted edge.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class RedundantConnectionSolution {
    static int root(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] solve(int n, int[][] edges) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        for (int[] e : edges) {
            int ra = root(parent, e[0]), rb = root(parent, e[1]);
            if (ra == rb) return new int[] {e[0], e[1]};
            if (size[ra] >= size[rb]) {
                parent[rb] = ra;
                size[ra] += size[rb];
            } else {
                parent[ra] = rb;
                size[rb] += size[ra];
            }
        }
        return new int[0];
    }

    static int[] comparesElements(int n, int[][] edges) {
        for (int[] e : edges) {
            if (e[0] == e[1]) return new int[] {e[0], e[1]};
        }
        return new int[0];
    }

    static boolean reachesAll(int n, int[][] edges, int skip) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int i = 0; i < edges.length; i++) {
            if (i == skip) continue;
            adj.get(edges[i][0]).add(edges[i][1]);
            adj.get(edges[i][1]).add(edges[i][0]);
        }
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(0);
        seen[0] = true;
        int reached = 1;
        while (!queue.isEmpty()) {
            int v = queue.poll();
            for (int w : adj.get(v)) {
                if (!seen[w]) {
                    seen[w] = true;
                    reached++;
                    queue.add(w);
                }
            }
        }
        return reached == n;
    }

    static int[] oracle(int n, int[][] edges) {
        for (int i = edges.length - 1; i >= 0; i--) {
            if (reachesAll(n, edges, i)) return new int[] {edges[i][0], edges[i][1]};
        }
        throw new AssertionError("no removable edge");
    }

    public static void main(String[] args) {
        int[][] tri = {{0, 1}, {1, 2}, {0, 2}};
        if (!Arrays.equals(solve(3, tri), new int[] {0, 2})) throw new AssertionError("example 1");
        int[][] ex2 = {{0, 1}, {1, 2}, {2, 0}, {2, 3}, {3, 4}};
        if (!Arrays.equals(solve(5, ex2), new int[] {2, 0})) throw new AssertionError("example 2");
        if (comparesElements(3, tri).length != 0) throw new AssertionError("element check never fires");
        int[] answer = solve(3, tri);
        answer[0] = 99;
        if (tri[2][0] != 0) throw new AssertionError("result must be a copy");
        Random rnd = new Random(23504);
        for (int t = 0; t < 800; t++) {
            int n = 3 + rnd.nextInt(8);
            List<int[]> list = new ArrayList<>();
            boolean[][] used = new boolean[n][n];
            for (int v = 1; v < n; v++) {
                int u = rnd.nextInt(v);
                list.add(new int[] {u, v});
                used[u][v] = used[v][u] = true;
            }
            int a, b;
            do {
                a = rnd.nextInt(n);
                b = rnd.nextInt(n);
            } while (a == b || used[a][b]);
            list.add(new int[] {a, b});
            java.util.Collections.shuffle(list, rnd);
            int[][] edges = new int[n][];
            for (int i = 0; i < n; i++) {
                int[] e = list.get(i);
                edges[i] = rnd.nextBoolean() ? e : new int[] {e[1], e[0]};
            }
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = edges[i].clone();
            int[] got = solve(n, edges);
            if (!Arrays.deepEquals(copy, edges)) throw new AssertionError("input changed");
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("t=" + t);
        }
    }
}
```
