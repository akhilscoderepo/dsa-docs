<!-- solutions-for: 23-directed-graphs-and-union-find -->
### Solutions For Merging Groups

#### Solution: [Build] Count Provinces And Find The Largest (LeetCode 547)
<!-- id: dgc-components-and-largest -->

**Approach.**
Each city is a vertex, and each 1 above the diagonal is an event that joins two cities. The method creates `parent` and `size` arrays, then visits every pair `(i, j)` with `i < j` and merges the two cities when the entry is 1. A merge happens only when the two representatives differ. Each merge lowers `count` by one and sets `largest` to the larger of its old value and the new size at the surviving root.

The invariant is that `count` equals the number of distinct representatives and that `size[r]` is correct at every root `r`. The value `largest` starts at 1, because a table with one city holds one province of one city. The method reads only the upper triangle, because the table is symmetric. The diagonal never produces a merge, since `find(i) == find(i)`.

**Complexity.**
- **Time** is O(n^2 * alpha(n)), because the method examines each of the n^2 / 2 pairs once and each merge test costs near-constant time.
- **Space** is O(n), because the two arrays hold one entry per city and the table is only read.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class ProvinceSizes {
    private static int find(int[] parent, int x) {
        // Path halving: each visited city is repointed at its grandparent.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns {number of provinces, size of the largest province}.
     * Time: O(n^2 * alpha(n)) for the pair scan and the merges.
     * Space: O(n) for the parent and size arrays.
     * Invariant: count equals the number of roots, size is correct at each root, and largest is the maximum size so far.
     */
    static int[] provinces(int[][] isConnected) {
        int n = isConnected.length;
        int[] parent = new int[n], size = new int[n];
        // Every city starts as a province of one city.
        for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; }
        int count = n, largest = 1;
        // The table is symmetric, so the upper triangle holds every event once.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                // A 0 entry is not an event.
                if (isConnected[i][j] != 1) continue;
                int ri = find(parent, i), rj = find(parent, j);
                // The same root means the cities already belong together.
                if (ri == rj) continue;
                // The smaller province attaches below the larger one.
                if (size[ri] < size[rj]) { int t = ri; ri = rj; rj = t; }
                parent[rj] = ri;
                size[ri] += size[rj];
                // The new size can only raise the maximum.
                largest = Math.max(largest, size[ri]);
                count--;
            }
        }
        return new int[] {count, largest};
    }

    /** Oracle: a flood fill with an explicit stack counts every province and measures its size. */
    static int[] oracle(int[][] m) {
        int n = m.length;
        boolean[] seen = new boolean[n];
        int count = 0, largest = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            count++;
            int size = 0;
            ArrayDeque<Integer> stack = new ArrayDeque<>();
            stack.push(s);
            seen[s] = true;
            while (!stack.isEmpty()) {
                int cur = stack.pop();
                size++;
                for (int nb = 0; nb < n; nb++) if (m[cur][nb] == 1 && !seen[nb]) { seen[nb] = true; stack.push(nb); }
            }
            largest = Math.max(largest, size);
        }
        return new int[] {count, largest};
    }

    public static void main(String[] args) {
        // Example 1: two cities form one province and the other two stand alone.
        int[][] a = {{1, 1, 0, 0}, {1, 1, 0, 0}, {0, 0, 1, 0}, {0, 0, 0, 1}};
        if (!Arrays.equals(provinces(a), new int[] {3, 2})) throw new AssertionError("example 1");
        // Example 2: cities 0 and 2 connect only through city 1.
        int[][] b = {{1, 1, 0, 0}, {1, 1, 1, 0}, {0, 1, 1, 0}, {0, 0, 0, 1}};
        if (!Arrays.equals(provinces(b), new int[] {2, 3})) throw new AssertionError("example 2");
        // One city is one province of size one.
        if (!Arrays.equals(provinces(new int[][] {{1}}), new int[] {1, 1})) throw new AssertionError("single city");
        // A table of all ones is a single province of every city.
        if (!Arrays.equals(provinces(new int[][] {{1, 1, 1}, {1, 1, 1}, {1, 1, 1}}), new int[] {1, 3})) throw new AssertionError("all ones");
        // The method leaves the table unchanged.
        int[][] keep = {{1, 1}, {1, 1}};
        provinces(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{1, 1}, {1, 1}})) throw new AssertionError("mutation");
        // Random symmetric tables against the flood fill.
        Random rnd = new Random(2391);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] m = new int[n][n];
            double p = rnd.nextDouble() * 0.4;
            for (int i = 0; i < n; i++) {
                m[i][i] = 1;
                for (int j = i + 1; j < n; j++) if (rnd.nextDouble() < p) m[i][j] = m[j][i] = 1;
            }
            if (!Arrays.equals(provinces(m), oracle(m))) throw new AssertionError("random " + t + " " + Arrays.deepToString(m));
        }
    }
}
```

#### Solution: [Vary] List Every Edge That Closes A Cycle (LeetCode 684)
<!-- id: dgc-edges-closing-cycles -->

**Approach.**
The method stores the groups in one array `link`. A negative entry marks a root and holds the group size as a negative number. A nonnegative entry is the parent. Vertices run from 1 to `n`, so the array has `n + 1` slots and slot 0 stays unused. For each edge in input order, the method finds both roots. Equal roots mean that earlier edges already join the endpoints, so the method copies the edge into the result and does not merge anything. Different roots mean the edge joins two groups, so the method merges them.

A self-loop has two equal endpoints, so it reaches the equal-root branch without a special case. A repeated edge reaches that branch after its first copy. The invariant is that two vertices share a root exactly when a chain of earlier edges joins them. This holds before each edge, whether or not earlier edges were closing edges. The method continues after the first closing edge, because the contract asks for all of them.

**Complexity.**
- **Time** is O((n + m) * alpha(n)), because the method makes two `find` calls per edge and initializes `n + 1` slots.
- **Space** is O(n + m), because `link` holds `n + 1` entries and the result can hold every edge.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ClosingEdges {
    private static int find(int[] link, int x) {
        // A negative entry marks a root; otherwise follow the parent and repoint x at the root on the way back.
        return link[x] < 0 ? x : (link[x] = find(link, link[x]));
    }

    /**
     * Returns every edge whose endpoints are already joined by earlier edges, in input order.
     * Time: O((n + m) * alpha(n)), with two finds per edge.
     * Space: O(n + m) for the link array and the result.
     * Invariant: before each edge, two vertices share a root exactly when earlier edges join them.
     */
    static int[][] closing(int n, int[][] edges) {
        int[] link = new int[n + 1];
        // Every vertex starts as a root of size one, written as -1.
        Arrays.fill(link, -1);
        List<int[]> out = new ArrayList<>();
        // Edges are processed in input order, which fixes the order of the result.
        for (int[] e : edges) {
            int ra = find(link, e[0]), rb = find(link, e[1]);
            // Equal roots mean the endpoints are already joined, and a self-loop always lands here.
            if (ra == rb) { out.add(new int[] {e[0], e[1]}); continue; }
            // The more negative entry is the larger group, which stays as the root.
            if (link[ra] > link[rb]) { int t = ra; ra = rb; rb = t; }
            link[ra] += link[rb];
            link[rb] = ra;
        }
        return out.toArray(new int[0][]);
    }

    /** Oracle: a depth-first search over a boolean matrix of the earlier edges. */
    static int[][] oracle(int n, int[][] edges) {
        boolean[][] adj = new boolean[n + 1][n + 1];
        List<int[]> out = new ArrayList<>();
        for (int[] e : edges) {
            boolean[] seen = new boolean[n + 1];
            if (dfs(adj, e[0], e[1], seen)) out.add(new int[] {e[0], e[1]});
            adj[e[0]][e[1]] = true;
            adj[e[1]][e[0]] = true;
        }
        return out.toArray(new int[0][]);
    }

    private static boolean dfs(boolean[][] adj, int cur, int target, boolean[] seen) {
        if (cur == target) return true;
        seen[cur] = true;
        for (int nb = 1; nb < adj.length; nb++) if (adj[cur][nb] && !seen[nb] && dfs(adj, nb, target, seen)) return true;
        return false;
    }

    public static void main(String[] args) {
        // Example 1: a triangle, a repeated pair and a self-loop all close.
        int[][] a = closing(5, new int[][] {{1, 2}, {2, 3}, {3, 1}, {1, 2}, {4, 4}, {3, 5}});
        if (!Arrays.deepEquals(a, new int[][] {{3, 1}, {1, 2}, {4, 4}})) throw new AssertionError("example 1");
        // Example 2: the last edge closes a cycle through three earlier edges.
        int[][] b = closing(4, new int[][] {{1, 2}, {2, 3}, {1, 3}, {3, 4}, {4, 1}});
        if (!Arrays.deepEquals(b, new int[][] {{1, 3}, {4, 1}})) throw new AssertionError("example 2");
        // A tree has no closing edge, and an empty list gives an empty result.
        if (closing(3, new int[][] {{1, 2}, {2, 3}}).length != 0) throw new AssertionError("tree");
        if (closing(1, new int[0][]).length != 0) throw new AssertionError("empty");
        // The result keeps the input orientation of each edge.
        if (!Arrays.deepEquals(closing(2, new int[][] {{2, 1}, {1, 2}}), new int[][] {{1, 2}})) throw new AssertionError("orientation");
        // The method leaves the edge array unchanged.
        int[][] keep = {{1, 2}, {2, 1}};
        closing(2, keep);
        if (!Arrays.deepEquals(keep, new int[][] {{1, 2}, {2, 1}})) throw new AssertionError("mutation");
        // Random multigraphs against the search oracle.
        Random rnd = new Random(2392);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7), m = rnd.nextInt(12);
            int[][] g = new int[m][];
            for (int i = 0; i < m; i++) g[i] = new int[] {1 + rnd.nextInt(n), 1 + rnd.nextInt(n)};
            if (!Arrays.deepEquals(closing(n, g), oracle(n, g))) throw new AssertionError("random " + t + " " + Arrays.deepToString(g));
        }
    }
}
```

#### Solution: [Boundary] Merge Accounts Ignoring Letter Case (LeetCode 721)
<!-- id: dgc-accounts-case-insensitive -->

**Approach.**
Each account is a vertex. The method lowercases every address with `Locale.ROOT`, so the result does not depend on the machine's language settings. A `HashMap` from lowercase address to the first account that used it turns shared addresses into events. When an address already has an owner, the method merges the current account with the owner. A new address gets the current account as its owner.

After all accounts are read, the method collects the addresses of each group into a `TreeSet` keyed by the group's root. The set gives distinct addresses in ascending order. It then walks the accounts in input order. The first account seen for a root is the earliest account of the group. That account supplies the name and fixes the position of the group in the output. The invariant is that two accounts share a root exactly when a chain of shared lowercase addresses joins them. Names play no role in merging, so two accounts with different names merge when they share an address.

**Complexity.**
- **Time** is O(L * alpha(n) + L log L), where `L` is the total number of addresses. Each address costs one map lookup and one merge, and the sorted sets cost L log L together.
- **Space** is O(L), because the map, the sets and the output each hold at most one entry per address.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public final class MergeIgnoringCase {
    private static int find(int[] parent, int x) {
        // Path halving keeps the routes short as merges accumulate.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Merges accounts that share an address ignoring letter case.
     * Time: O(L * alpha(n) + L log L) for L addresses.
     * Space: O(L) for the owner map, the sorted sets and the output.
     * Invariant: two accounts share a root exactly when a chain of shared lowercase addresses joins them.
     */
    static List<List<String>> merge(List<List<String>> accounts) {
        int n = accounts.size();
        int[] parent = new int[n];
        // Every account starts as its own group.
        for (int i = 0; i < n; i++) parent[i] = i;
        Map<String, Integer> owner = new HashMap<>();
        // Reading addresses in order makes the owner the earliest account that used the address.
        for (int i = 0; i < n; i++) {
            List<String> acc = accounts.get(i);
            for (int k = 1; k < acc.size(); k++) {
                // A fixed locale keeps the conversion identical on every machine.
                String key = acc.get(k).toLowerCase(Locale.ROOT);
                Integer prior = owner.putIfAbsent(key, i);
                // An existing owner means the two accounts share an address.
                if (prior != null) parent[find(parent, i)] = find(parent, prior);
            }
        }
        Map<Integer, TreeSet<String>> emails = new HashMap<>();
        // Collect each group's distinct lowercase addresses in sorted order.
        for (int i = 0; i < n; i++) {
            TreeSet<String> set = emails.computeIfAbsent(find(parent, i), r -> new TreeSet<>());
            List<String> acc = accounts.get(i);
            for (int k = 1; k < acc.size(); k++) set.add(acc.get(k).toLowerCase(Locale.ROOT));
        }
        List<List<String>> out = new ArrayList<>();
        Set<Integer> emitted = new HashSet<>();
        // Walking in input order makes the first account of a root the earliest account of its group.
        for (int i = 0; i < n; i++) {
            int root = find(parent, i);
            if (!emitted.add(root)) continue;
            List<String> row = new ArrayList<>();
            row.add(accounts.get(i).get(0));
            row.addAll(emails.get(root));
            out.add(row);
        }
        return out;
    }

    /** Oracle: sets of addresses merge pairwise until no two sets overlap. */
    static List<List<String>> oracle(List<List<String>> accounts) {
        List<Set<String>> sets = new ArrayList<>();
        List<Integer> first = new ArrayList<>();
        for (int i = 0; i < accounts.size(); i++) {
            Set<String> s = new TreeSet<>();
            for (int k = 1; k < accounts.get(i).size(); k++) s.add(accounts.get(i).get(k).toLowerCase(Locale.ROOT));
            sets.add(s);
            first.add(i);
        }
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int a = 0; a < sets.size() && !changed; a++) {
                for (int b = a + 1; b < sets.size() && !changed; b++) {
                    Set<String> common = new HashSet<>(sets.get(a));
                    common.retainAll(sets.get(b));
                    if (common.isEmpty()) continue;
                    sets.get(a).addAll(sets.get(b));
                    first.set(a, Math.min(first.get(a), first.get(b)));
                    sets.remove(b);
                    first.remove(b);
                    changed = true;
                }
            }
        }
        // Order the groups by their earliest account.
        Integer[] order = new Integer[sets.size()];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (x, y) -> Integer.compare(first.get(x), first.get(y)));
        List<List<String>> out = new ArrayList<>();
        for (int g : order) {
            List<String> row = new ArrayList<>();
            row.add(accounts.get(first.get(g)).get(0));
            row.addAll(sets.get(g));
            out.add(row);
        }
        return out;
    }

    static List<List<String>> acc(String... parts) {
        List<List<String>> out = new ArrayList<>();
        for (String p : parts) out.add(new ArrayList<>(Arrays.asList(p.split(","))));
        return out;
    }

    public static void main(String[] args) {
        // Example 1: the second account shares b@x.io once the case is ignored.
        List<List<String>> r1 = merge(acc("Ana,A@x.io,b@x.io", "Bo,B@X.io,c@x.io", "Cy,d@x.io"));
        if (!r1.equals(acc("Ana,a@x.io,b@x.io,c@x.io", "Cy,d@x.io"))) throw new AssertionError("example 1 " + r1);
        // Example 2: a chain of three accounts with three different names keeps the earliest name.
        List<List<String>> r2 = merge(acc("Dee,k@m.org", "Eli,K@m.org,z@m.org", "Fay,Z@M.ORG", "Gus,q@m.org"));
        if (!r2.equals(acc("Dee,k@m.org,z@m.org", "Gus,q@m.org"))) throw new AssertionError("example 2 " + r2);
        // An address that repeats inside one account appears once.
        if (!merge(acc("Hal,a@b.c,A@B.C")).equals(acc("Hal,a@b.c"))) throw new AssertionError("repeat");
        // A later account can merge two earlier groups, and the earliest name still wins.
        if (!merge(acc("Ivy,p@q.r", "Jon,s@t.u", "Kim,P@Q.R,S@T.U")).equals(acc("Ivy,p@q.r,s@t.u"))) throw new AssertionError("bridge");
        // A fixed locale matters: the Turkish rule turns I into a dotless letter, but Locale.ROOT does not.
        if ("I".toLowerCase(Locale.forLanguageTag("tr")).equals("i")) throw new AssertionError("turkish rule");
        if (!"I".toLowerCase(Locale.ROOT).equals("i")) throw new AssertionError("root rule");
        // The method leaves the input unchanged.
        List<List<String>> keep = acc("Lee,A@b.c");
        merge(keep);
        if (!keep.equals(acc("Lee,A@b.c"))) throw new AssertionError("mutation");
        // Random accounts built from a small address pool with mixed case, against the pairwise-merge oracle.
        Random rnd = new Random(2393);
        String[] pool = {"aa@x", "bb@x", "cc@x", "dd@x", "ee@x", "ff@x", "gg@x"};
        String[] names = {"Ann", "Ben", "Cal", "Dot"};
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7);
            List<List<String>> in = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                List<String> row = new ArrayList<>();
                row.add(names[rnd.nextInt(names.length)]);
                int cnt = 1 + rnd.nextInt(3);
                for (int k = 0; k < cnt; k++) {
                    String e = pool[rnd.nextInt(pool.length)];
                    row.add(rnd.nextBoolean() ? e.toUpperCase(Locale.ROOT) : e);
                }
                in.add(row);
            }
            if (!merge(in).equals(oracle(in))) throw new AssertionError("random " + t + " " + in);
        }
    }
}
```

#### Solution: [Recognize] Connect Points That May Repeat (LeetCode 1584)
<!-- id: dgc-connect-repeated-points -->

**Approach.**
The vertices are the entries of the array, so two equal points are two vertices at distance 0. The method generates every pair as a packed `long`, with the distance in the high bits and the two indices in the low 20 bits. Sorting a primitive `long[]` orders the pairs by distance and avoids a comparator and an object per edge. The distance is shifted after a cast to `long`, so the shift cannot overflow `int`.

The method then runs the Kruskal loop. For each key it unpacks the two indices and compares their representatives. Equal representatives skip the pair. Different representatives merge the groups and add the distance, which may be 0. The loop stops after `n - 1` accepted pairs, and the count of accepted pairs, not the sum, decides the stop. A rule that skipped zero-cost pairs would leave equal points disconnected. The invariant is that every accepted pair is the cheapest pair that leaves its group at that moment.

**Complexity.**
- **Time** is O(n^2 log n), because the sort handles n * (n - 1) / 2 keys and the union-find work adds O(n^2 * alpha(n)).
- **Space** is O(n^2), because the array of packed keys holds one `long` per pair.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ConnectRepeatedPoints {
    private static int find(int[] parent, int x) {
        // Path halving shortens the route to the representative.
        while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
        return x;
    }

    /**
     * Returns the lowest total Manhattan cost of links that connect all entries, where equal points are allowed.
     * Time: O(n^2 log n) for sorting the packed pair keys.
     * Space: O(n^2) for the key array.
     * Invariant: every accepted pair is the cheapest pair that leaves its group when it is accepted.
     */
    static long minCost(int[][] points) {
        int n = points.length;
        long[] keys = new long[n * (n - 1) / 2];
        int m = 0;
        // Pack distance, then first index, then second index, so the sort orders by distance first.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                long d = Math.abs((long) points[i][0] - points[j][0]) + Math.abs((long) points[i][1] - points[j][1]);
                keys[m++] = (d << 20) | ((long) i << 10) | j;
            }
        }
        // A primitive sort needs no comparator and creates no edge objects.
        Arrays.sort(keys);
        int[] parent = new int[n], size = new int[n];
        // Every entry starts as a group of one.
        for (int v = 0; v < n; v++) { parent[v] = v; size[v] = 1; }
        long total = 0;
        int accepted = 0;
        // Keys are visited from the smallest distance upward.
        for (long key : keys) {
            // The accepted count, not the total, decides when the links are complete.
            if (accepted == n - 1) break;
            int i = (int) ((key >> 10) & 1023), j = (int) (key & 1023);
            int ri = find(parent, i), rj = find(parent, j);
            // Equal representatives mean the pair adds no reach.
            if (ri == rj) continue;
            // A distance of 0 is still a link, so it is accepted like any other.
            if (size[ri] < size[rj]) { int t = ri; ri = rj; rj = t; }
            parent[rj] = ri;
            size[ri] += size[rj];
            total += key >> 20;
            accepted++;
        }
        return total;
    }

    /** Oracle: Prim's method with a distance array, which treats equal points as ordinary vertices. */
    static long oracle(int[][] p) {
        int n = p.length;
        long[] best = new long[n];
        boolean[] in = new boolean[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[0] = 0;
        long total = 0;
        for (int round = 0; round < n; round++) {
            int pick = -1;
            for (int v = 0; v < n; v++) if (!in[v] && (pick == -1 || best[v] < best[pick])) pick = v;
            in[pick] = true;
            total += best[pick];
            for (int v = 0; v < n; v++) {
                long d = Math.abs((long) p[pick][0] - p[v][0]) + Math.abs((long) p[pick][1] - p[v][1]);
                if (!in[v] && d < best[v]) best[v] = d;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // Example 1: the equal pair costs 0, then links of 5 and 6.
        if (minCost(new int[][] {{1, 1}, {1, 1}, {4, 5}, {0, 6}}) != 11) throw new AssertionError("example 1");
        // Example 2: two equal pairs join at cost 0 and one link of 14 joins the pairs.
        if (minCost(new int[][] {{2, 2}, {9, 9}, {2, 2}, {9, 9}}) != 14) throw new AssertionError("example 2");
        // All points equal costs nothing, and one point needs no link.
        if (minCost(new int[][] {{5, 5}, {5, 5}, {5, 5}}) != 0) throw new AssertionError("all equal");
        if (minCost(new int[][] {{5, 5}}) != 0) throw new AssertionError("single");
        // The extreme corner distance packs and unpacks without loss.
        if (minCost(new int[][] {{-1000000, -1000000}, {1000000, 1000000}}) != 4000000L) throw new AssertionError("extremes");
        // The largest index pair (999, 998) survives packing into 10-bit fields.
        long key = (4000000L << 20) | (998L << 10) | 999;
        if (((key >> 10) & 1023) != 998 || (key & 1023) != 999 || (key >> 20) != 4000000L) throw new AssertionError("packing");
        // The method leaves the points unchanged.
        int[][] keep = {{0, 0}, {0, 0}, {3, 4}};
        minCost(keep);
        if (!Arrays.deepEquals(keep, new int[][] {{0, 0}, {0, 0}, {3, 4}})) throw new AssertionError("mutation");
        // Random points from a small range, so repeats are common, against the oracle.
        Random rnd = new Random(2394);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10), range = 1 + rnd.nextInt(6);
            int[][] pts = new int[n][];
            for (int i = 0; i < n; i++) pts[i] = new int[] {rnd.nextInt(range) - 2, rnd.nextInt(range) - 2};
            if (minCost(pts) != oracle(pts)) throw new AssertionError("random " + t + " " + Arrays.deepToString(pts));
        }
    }
}
```
