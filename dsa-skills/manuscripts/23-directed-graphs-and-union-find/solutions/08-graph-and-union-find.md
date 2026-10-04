<!-- solutions-for: 08-graph-and-union-find -->
### Graph And Union-Find

#### Solution: [Build] Number of Provinces (LeetCode 547)
<!-- id: uc-province-sizes -->

**Approach.** Start with each city as its own representative with size 1. For every pair, find both representatives, skip the pair if they match, and otherwise hang the smaller under the larger and add its size to the keeper. After the last pair, a city that is its own parent contributes its stored size, and the collected sizes are sorted. The oracle uses no tree at all: every city carries a label, and the labels of the two ends of each pair are replaced by their smaller value until a full pass changes nothing, after which equal labels mean one province. The assertions replay both examples, check that the input is untouched, and compare random lists with many repeated and self-pairs.

**Complexity.** Reading the pairs is O(E * alpha(n)), the final scan and sort add O(n log n), and memory is O(n).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ProvinceSizes {
    static int[] solve(int n, int[][] pairs) {
        int[] parent = new int[n], size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        for (int[] p : pairs) {
            int ra = find(parent, p[0]), rb = find(parent, p[1]);
            if (ra == rb) continue;
            int big = size[ra] >= size[rb] ? ra : rb, small = big == ra ? rb : ra;
            parent[small] = big;
            size[big] += size[small];
        }
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < n; i++) if (parent[i] == i) out.add(size[i]);
        return out.stream().mapToInt(Integer::intValue).sorted().toArray();
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    static int[] oracle(int n, int[][] pairs) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] p : pairs) {
                int m = Math.min(label[p[0]], label[p[1]]);
                if (label[p[0]] != m) { label[p[0]] = m; changed = true; }
                if (label[p[1]] != m) { label[p[1]] = m; changed = true; }
            }
        }
        int[] count = new int[n];
        for (int l : label) count[l]++;
        return Arrays.stream(count).filter(c -> c > 0).sorted().toArray();
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1}, {1, 2}, {3, 4}, {5, 5}};
        if (!Arrays.equals(solve(7, e1), new int[] {1, 1, 2, 3})) throw new AssertionError("example 1");
        int[][] e2 = {{5, 0}, {0, 5}, {2, 3}, {3, 4}, {4, 2}};
        if (!Arrays.equals(solve(6, e2), new int[] {1, 2, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(4, new int[0][]), new int[] {1, 1, 1, 1})) throw new AssertionError("no pairs");
        int[][] copy = {{0, 1}, {1, 2}, {3, 4}, {5, 5}};
        solve(7, e1);
        if (!Arrays.deepEquals(copy, e1)) throw new AssertionError("input changed");
        Random rnd = new Random(23801);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10), m = rnd.nextInt(14);
            int[][] pairs = new int[m][];
            for (int i = 0; i < m; i++) pairs[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            if (!Arrays.equals(solve(n, pairs), oracle(n, pairs))) throw new AssertionError("t=" + t);
        }
    }
}
```

#### Solution: [Vary] Redundant Connection (LeetCode 684)
<!-- id: uc-redundant-count -->

**Approach.** The loop finds both representatives before writing anything. When they are equal the edge is redundant, so the counter rises and the first index is stored if it is still -1. Otherwise the two components merge by size. Self-edges are handled with no special case, since both endpoints have the same representative, and a repeated edge is redundant the second time for the same reason. The oracle takes each prefix of the edge list and computes a Floyd-Warshall boolean closure by relaxing every intermediate vertex, then asks whether the closure already joins the endpoints of the next edge. The assertions replay the examples, check the identity that components equal n minus the merges while the shortcut n minus the edge count is wrong as soon as one edge is redundant, and compare random general graphs.

**Complexity.** Linear in the edge count apart from the near-constant lookup, O(E * alpha(n)) time with O(n) extra memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class RedundantCount {
    static int[] solve(int n, int[][] edges) {
        int[] parent = new int[n], size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int count = 0, first = -1;
        for (int i = 0; i < edges.length; i++) {
            int ra = find(parent, edges[i][0]), rb = find(parent, edges[i][1]);
            if (ra == rb) {
                count++;
                if (first < 0) first = i;
                continue;
            }
            if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
            parent[rb] = ra;
            size[ra] += size[rb];
        }
        return new int[] {count, first};
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] oracle(int n, int[][] edges) {
        int count = 0, first = -1;
        for (int i = 0; i < edges.length; i++) {
            boolean[][] reach = new boolean[n][n];
            for (int v = 0; v < n; v++) reach[v][v] = true;
            for (int j = 0; j < i; j++) reach[edges[j][0]][edges[j][1]] = reach[edges[j][1]][edges[j][0]] = true;
            for (int k = 0; k < n; k++)
                for (int a = 0; a < n; a++)
                    for (int b = 0; b < n; b++)
                        if (reach[a][k] && reach[k][b]) reach[a][b] = true;
            if (reach[edges[i][0]][edges[i][1]]) {
                count++;
                if (first < 0) first = i;
            }
        }
        return new int[] {count, first};
    }

    static int components(int n, int[][] edges) {
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        int c = n;
        for (int[] e : edges) {
            int a = find(parent, e[0]), b = find(parent, e[1]);
            if (a != b) { parent[a] = b; c--; }
        }
        return c;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1}, {1, 2}, {2, 0}, {2, 0}, {3, 3}};
        if (!Arrays.equals(solve(4, e1), new int[] {3, 2})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1}, {2, 3}};
        if (!Arrays.equals(solve(6, e2), new int[] {0, -1})) throw new AssertionError("example 2");
        if (components(4, e1) != 2 || 4 - e1.length != -1) throw new AssertionError("false friend: n minus edges is wrong once an edge is redundant");
        if (components(6, e2) != 6 - e2.length) throw new AssertionError("forest: shortcut holds");
        Random rnd = new Random(23802);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(9);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[] got = solve(n, edges);
            if (!Arrays.equals(got, oracle(n, edges))) throw new AssertionError("t=" + t);
            if (components(n, edges) != n - m + got[0]) throw new AssertionError("identity t=" + t);
        }
    }
}
```

#### Solution: [Boundary] Accounts Merge (LeetCode 721)
<!-- id: uc-merged-accounts -->

**Approach.** The union-find runs over account indices. A map sends each email to the first account that held it; when an email is met again, its stored owner and the current account are united. After all accounts are read, the group of an account is its representative, and a set of emails per representative is filled by going over every email of every account, so a repeated email adds nothing. The answer is the number of distinct representatives and the largest set. The map stores plain `int` owners read through `Integer` and compared with `.equals`, because the Java hazard is that `==` on two boxed `Integer` values is true up to 127 and false beyond it, and the assertions show both halves of that claim. The oracle is a label propagation over accounts: two accounts exchange the smaller label whenever they share any email, repeated to a fixpoint. The random tests draw emails from a small pool so that chains of overlaps are common, and names are drawn from two values so equal names without shared emails occur.

**Complexity.** About O(S * alpha(A)) for S emails in total over A accounts, plus the hashing cost of the emails, with O(S) memory.

```java run
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class MergedAccounts {
    static int[] solve(String[][] accounts) {
        int a = accounts.length;
        int[] parent = new int[a], size = new int[a];
        for (int i = 0; i < a; i++) { parent[i] = i; size[i] = 1; }
        Map<String, Integer> owner = new HashMap<>();
        for (int i = 0; i < a; i++) {
            for (int k = 1; k < accounts[i].length; k++) {
                Integer prev = owner.putIfAbsent(accounts[i][k], i);
                if (prev != null) union(parent, size, prev, i);
            }
        }
        Map<Integer, Set<String>> emails = new HashMap<>();
        for (int i = 0; i < a; i++) {
            Set<String> set = emails.computeIfAbsent(find(parent, i), r -> new HashSet<>());
            for (int k = 1; k < accounts[i].length; k++) set.add(accounts[i][k]);
        }
        int largest = 0;
        for (Set<String> s : emails.values()) largest = Math.max(largest, s.size());
        return new int[] {emails.size(), largest};
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    static void union(int[] parent, int[] size, int x, int y) {
        int rx = find(parent, x), ry = find(parent, y);
        if (rx == ry) return;
        if (size[rx] < size[ry]) { int t = rx; rx = ry; ry = t; }
        parent[ry] = rx;
        size[rx] += size[ry];
    }

    static int[] oracle(String[][] accounts) {
        int a = accounts.length;
        int[] label = new int[a];
        for (int i = 0; i < a; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < a; i++)
                for (int j = 0; j < a; j++) {
                    boolean shared = false;
                    for (int x = 1; x < accounts[i].length; x++)
                        for (int y = 1; y < accounts[j].length; y++)
                            if (accounts[i][x].equals(accounts[j][y])) shared = true;
                    if (shared && label[i] != label[j]) {
                        label[i] = label[j] = Math.min(label[i], label[j]);
                        changed = true;
                    }
                }
        }
        Map<Integer, Set<String>> groups = new HashMap<>();
        for (int i = 0; i < a; i++) {
            Set<String> s = groups.computeIfAbsent(label[i], k -> new HashSet<>());
            for (int x = 1; x < accounts[i].length; x++) s.add(accounts[i][x]);
        }
        int best = 0;
        for (Set<String> s : groups.values()) best = Math.max(best, s.size());
        return new int[] {groups.size(), best};
    }

    public static void main(String[] args) {
        String[][] e1 = {{"Ana", "a@x", "b@x"}, {"Ben", "c@x"}, {"Ana", "b@x", "d@x"}, {"Ana", "e@x"}};
        if (!java.util.Arrays.equals(solve(e1), new int[] {3, 3})) throw new AssertionError("example 1");
        String[][] e2 = {{"Sam", "s@y", "s@y", "t@y"}, {"Sam", "u@y"}, {"Sam", "t@y"}};
        if (!java.util.Arrays.equals(solve(e2), new int[] {2, 2})) throw new AssertionError("example 2");
        Integer small1 = 100, small2 = 100, big1 = 1000, big2 = 1000;
        if (small1 != small2) throw new AssertionError("small boxed values are cached");
        if (big1 == big2) throw new AssertionError("large boxed values are distinct objects");
        if (!big1.equals(big2)) throw new AssertionError("equals compares the values");
        Random rnd = new Random(23803);
        String[] names = {"Kit", "Lou"};
        for (int t = 0; t < 2500; t++) {
            int a = 1 + rnd.nextInt(7);
            String[][] acc = new String[a][];
            for (int i = 0; i < a; i++) {
                int k = 1 + rnd.nextInt(3);
                acc[i] = new String[k + 1];
                acc[i][0] = names[rnd.nextInt(2)];
                for (int j = 1; j <= k; j++) acc[i][j] = "m" + rnd.nextInt(9);
            }
            if (!java.util.Arrays.equals(solve(acc), oracle(acc))) throw new AssertionError("t=" + t);
        }
    }
}
```

#### Solution: [Recognize] Min Cost to Connect All Points (LeetCode 1584)
<!-- id: uc-chebyshev-spanning -->

**Approach.** Build every pair of points as an edge with weight `max(|dx|, |dy|)`, sort the edges by weight, and scan them with the size-based union-find. An edge is accepted only when its two representatives differ, its weight is added to the total and kept as the running largest, and the scan stops after n - 1 accepted edges. A single point accepts nothing, so the answer is `[0, 0]`. Because every accepted edge is at least as heavy as the previous one, the largest accepted weight is the last one accepted, and it is the same in every minimum tree. The oracle tries every subset of n - 1 edges for at most six points, keeps those that connect all points by label propagation, and takes the minimum total. It also checks that every minimum subset has the same largest edge, which is the claim the output relies on. The assertions replay both examples, including the duplicate points that cost 0, and a case where Manhattan and Chebyshev totals differ.

**Complexity.** Sorting dominates, at O(P^2 log P) for P points, with O(P^2) memory for the edge list.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ChebyshevSpan {
    static int dist(int[] p, int[] q) {
        return Math.max(Math.abs(p[0] - q[0]), Math.abs(p[1] - q[1]));
    }

    static int[] solve(int[][] pts) {
        int n = pts.length, m = n * (n - 1) / 2, k = 0;
        int[][] edges = new int[m][];
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) edges[k++] = new int[] {dist(pts[i], pts[j]), i, j};
        Arrays.sort(edges, (x, y) -> Integer.compare(x[0], y[0]));
        int[] parent = new int[n], size = new int[n];
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int total = 0, largest = 0, taken = 0;
        for (int[] e : edges) {
            if (taken == n - 1) break;
            int ra = find(parent, e[1]), rb = find(parent, e[2]);
            if (ra == rb) continue;
            if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
            parent[rb] = ra;
            size[ra] += size[rb];
            total += e[0];
            largest = e[0];
            taken++;
        }
        return new int[] {total, largest};
    }

    static int find(int[] parent, int x) {
        while (parent[x] != x) x = parent[x];
        return x;
    }

    static int[] oracle(int[][] pts) {
        int n = pts.length;
        if (n == 1) return new int[] {0, 0};
        int m = n * (n - 1) / 2;
        int[] ea = new int[m], eb = new int[m], ew = new int[m];
        int k = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++) { ea[k] = i; eb[k] = j; ew[k] = dist(pts[i], pts[j]); k++; }
        int bestTotal = Integer.MAX_VALUE, minLargest = 0, maxLargest = 0;
        for (int mask = 0; mask < (1 << m); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] label = new int[n];
            for (int i = 0; i < n; i++) label[i] = i;
            boolean changed = true;
            while (changed) {
                changed = false;
                for (int e = 0; e < m; e++) {
                    if ((mask >> e & 1) == 0) continue;
                    int lo = Math.min(label[ea[e]], label[eb[e]]);
                    if (label[ea[e]] != lo || label[eb[e]] != lo) { label[ea[e]] = label[eb[e]] = lo; changed = true; }
                }
            }
            boolean connected = true;
            for (int i = 0; i < n; i++) if (label[i] != 0) connected = false;
            if (!connected) continue;
            int total = 0, mx = 0;
            for (int e = 0; e < m; e++) if ((mask >> e & 1) != 0) { total += ew[e]; mx = Math.max(mx, ew[e]); }
            if (total < bestTotal) { bestTotal = total; minLargest = maxLargest = mx; }
            else if (total == bestTotal) { minLargest = Math.min(minLargest, mx); maxLargest = Math.max(maxLargest, mx); }
        }
        if (minLargest != maxLargest) throw new AssertionError("largest edge differs between minimum trees");
        return new int[] {bestTotal, maxLargest};
    }

    public static void main(String[] args) {
        int[][] p1 = {{0, 0}, {2, 2}, {3, 10}, {5, 2}, {7, 0}};
        if (!Arrays.equals(solve(p1), new int[] {15, 8})) throw new AssertionError("example 1");
        int[][] p2 = {{1, 1}, {1, 1}, {4, 5}};
        if (!Arrays.equals(solve(p2), new int[] {4, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][] {{4, 4}}), new int[] {0, 0})) throw new AssertionError("single point");
        if (dist(new int[] {0, 0}, new int[] {3, 4}) != 4) throw new AssertionError("Chebyshev is the larger gap, not the sum 7");
        int[][] before = {{0, 0}, {2, 2}, {3, 10}, {5, 2}, {7, 0}};
        solve(p1);
        if (!Arrays.deepEquals(before, p1)) throw new AssertionError("input changed");
        Random rnd = new Random(23804);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] pts = new int[n][];
            for (int i = 0; i < n; i++) pts[i] = new int[] {rnd.nextInt(9) - 4, rnd.nextInt(9) - 4};
            if (!Arrays.equals(solve(pts), oracle(pts))) throw new AssertionError("t=" + t);
        }
    }
}
```
