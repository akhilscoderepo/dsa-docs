<!-- solutions-for: 06-dynamic-connectivity -->
### Dynamic Connectivity

#### Solution: [Build] Online Connect And Query (Author exercise)
<!-- id: ug-online-connect-query -->

**Approach.** Keep a `parent` array and a `size` array, and answer the operations strictly in arrival order. A lay operation finds both labels and, when they differ, hangs the lighter label under the heavier one. An ask operation only compares two finds and appends one boolean. The `find` here uses path halving, which rewrites each visited slot to its grandparent in a single upward pass, so it needs no second loop. The oracle is deliberately the static method: after every operation it recomputes a full Warshall closure over the lines laid so far and reads the answer from that table, which agrees with the structure on thousands of random small streams. The run also asserts the false friend as a count. On a street of 2000 houses where every new line is followed by the question "can house 0 reach the newest house", a fresh depth-first search touches exactly 2,000,999 houses in total, while the structure performs a few thousand parent hops, and the assertion demands a ratio of at least 100 to 1. Two Java claims from the lesson are checked as well: `new int[n]` is zero-filled, so a forgotten `parent[i] = i` loop makes every house lead to house 0 and every question answer yes, and the `boolean[]` result has to be sized by counting the asks first.

**Complexity.** Each operation costs two finds, and with union by size and path halving the amortised cost per find is nearly constant (inverse-Ackermann growth), so m operations take close to O(m) time in practice and O(n) memory, against O(m * (n + L)) for L lines when a search is re-run per question.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class OnlineConnectSolution {
    static long hops;

    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
            hops++;
        }
        return x;
    }

    static boolean[] solve(int n, int[][] ops) {
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int asks = 0;
        for (int[] op : ops) if (op[0] == 1) asks++;
        boolean[] answers = new boolean[asks];
        int next = 0;
        for (int[] op : ops) {
            int ra = find(parent, op[1]), rb = find(parent, op[2]);
            if (op[0] == 1) {
                answers[next++] = ra == rb;
            } else if (ra != rb) {
                if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
                parent[rb] = ra;
                size[ra] += size[rb];
            }
        }
        return answers;
    }

    static boolean[] oracle(int n, int[][] ops) {
        boolean[][] reach = new boolean[n][n];
        for (int i = 0; i < n; i++) reach[i][i] = true;
        List<Boolean> out = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) {
                reach[op[1]][op[2]] = true;
                reach[op[2]][op[1]] = true;
            } else {
                boolean[][] c = new boolean[n][];
                for (int i = 0; i < n; i++) c[i] = reach[i].clone();
                for (int k = 0; k < n; k++)
                    for (int i = 0; i < n; i++)
                        for (int j = 0; j < n; j++)
                            if (c[i][k] && c[k][j]) c[i][j] = true;
                out.add(c[op[1]][op[2]]);
            }
        }
        boolean[] arr = new boolean[out.size()];
        for (int i = 0; i < arr.length; i++) arr[i] = out.get(i);
        return arr;
    }

    static long dfsTouches(int n) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        long touched = 0;
        for (int i = 0; i + 1 < n; i++) {
            adj.get(i).add(i + 1);
            adj.get(i + 1).add(i);
            boolean[] seen = new boolean[n];
            int[] stack = new int[n];
            int top = 0;
            stack[top++] = 0;
            seen[0] = true;
            while (top > 0) {
                int x = stack[--top];
                touched++;
                if (x == i + 1) break;
                for (int y : adj.get(x))
                    if (!seen[y]) { seen[y] = true; stack[top++] = y; }
            }
        }
        return touched;
    }

    public static void main(String[] args) {
        int[][] ops1 = {{1, 0, 4}, {0, 0, 1}, {0, 3, 4}, {1, 0, 4}, {0, 1, 3}, {1, 0, 4}};
        if (!java.util.Arrays.equals(solve(5, ops1), new boolean[] {false, false, true}))
            throw new AssertionError("example 1");
        int[][] ops2 = {{0, 2, 2}, {1, 2, 2}, {1, 0, 3}, {0, 0, 3}, {0, 3, 0}, {1, 3, 0}};
        if (!java.util.Arrays.equals(solve(4, ops2), new boolean[] {true, false, true}))
            throw new AssertionError("example 2");
        if (solve(3, new int[][] {{0, 0, 1}}).length != 0) throw new AssertionError("no asks");
        int[] unfilled = new int[5];
        if (find(unfilled, 3) != 0 || find(unfilled, 4) != 0) throw new AssertionError("zero fill points everyone at house 0");
        Random rnd = new Random(23601);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(16);
            int[][] ops = new int[m][];
            for (int i = 0; i < m; i++) ops[i] = new int[] {rnd.nextInt(2), rnd.nextInt(n), rnd.nextInt(n)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = ops[i].clone();
            if (!java.util.Arrays.equals(solve(n, ops), oracle(n, ops))) throw new AssertionError("random " + t);
            if (!java.util.Arrays.deepEquals(ops, copy)) throw new AssertionError("input changed");
        }
        int n = 2000;
        int[][] street = new int[2 * (n - 1)][];
        for (int i = 0; i + 1 < n; i++) {
            street[2 * i] = new int[] {0, i, i + 1};
            street[2 * i + 1] = new int[] {1, 0, i + 1};
        }
        hops = 0;
        boolean[] answers = solve(n, street);
        for (boolean a : answers) if (!a) throw new AssertionError("street must stay connected");
        long searchWork = dfsTouches(n);
        if (searchWork != (long) n * (n + 1) / 2 - 1) throw new AssertionError("search work " + searchWork);
        if (searchWork < 100 * hops) throw new AssertionError("ratio " + searchWork + " vs " + hops);
    }
}
```

#### Solution: [Vary] Number Of Provinces (LeetCode 547)
<!-- id: ug-provinces-by-row -->

**Approach.** Start with `n` separate cities and a counter equal to `n`. For row `i` of the matrix, scan every column `j`, and for each 1 with `j != i` call union on `i` and `j`; each union that really joins two groups lowers the counter. After the whole row has been scanned, append the counter to the result. The counter therefore counts every city in the matrix, not only the ones whose rows have been seen, so the last entry is the classic province count and earlier entries can only be larger or equal. A symmetric matrix repeats each friendship in a later row, and those repeats are exactly the already-joined case that changes nothing. The oracle ignores union-find: after each row it adds that row's edges to a list and runs label propagation, repeatedly replacing every city's label by the smaller label across each edge until a full pass changes nothing, then counts distinct labels. The assertions cover both examples, a matrix with no friendships, a full matrix, the non-increasing shape of the output, and the unmodified input.

**Complexity.** Reading the matrix is Theta(n^2) cells, and each of at most n^2 union calls is nearly constant amortised, so the time is O(n^2 * alpha(n)) with O(n) memory beyond the n-entry output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ProvincesByRowSolution {
    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static int[] solve(int[][] isConnected) {
        int n = isConnected.length;
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int groups = n;
        int[] after = new int[n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (j == i || isConnected[i][j] == 0) continue;
                int ra = find(parent, i), rb = find(parent, j);
                if (ra == rb) continue;
                if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
                parent[rb] = ra;
                size[ra] += size[rb];
                groups--;
            }
            after[i] = groups;
        }
        return after;
    }

    static int[] oracle(int[][] m) {
        int n = m.length;
        int[] out = new int[n];
        List<int[]> edges = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) if (j != i && m[i][j] == 1) edges.add(new int[] {i, j});
            int[] label = new int[n];
            for (int v = 0; v < n; v++) label[v] = v;
            boolean changed = true;
            while (changed) {
                changed = false;
                for (int[] e : edges) {
                    int low = Math.min(label[e[0]], label[e[1]]);
                    if (label[e[0]] != low || label[e[1]] != low) {
                        label[e[0]] = low;
                        label[e[1]] = low;
                        changed = true;
                    }
                }
            }
            Set<Integer> distinct = new HashSet<>();
            for (int v : label) distinct.add(v);
            out[i] = distinct.size();
        }
        return out;
    }

    static int[][] symmetric(int n, Random rnd, int percent) {
        int[][] m = new int[n][n];
        for (int i = 0; i < n; i++) {
            m[i][i] = 1;
            for (int j = i + 1; j < n; j++) if (rnd.nextInt(100) < percent) m[i][j] = m[j][i] = 1;
        }
        return m;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 1, 0, 0}, {1, 1, 0, 0}, {0, 0, 1, 1}, {0, 0, 1, 1}};
        if (!Arrays.equals(solve(a), new int[] {3, 3, 2, 2})) throw new AssertionError("example 1");
        int[][] b = {{1, 1, 1, 0, 0}, {1, 1, 0, 0, 0}, {1, 0, 1, 1, 0}, {0, 0, 1, 1, 1}, {0, 0, 0, 1, 1}};
        if (!Arrays.equals(solve(b), new int[] {3, 3, 2, 1, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(new int[][] {{1}}), new int[] {1})) throw new AssertionError("single city");
        int[][] lone = {{1, 0, 0}, {0, 1, 0}, {0, 0, 1}};
        if (!Arrays.equals(solve(lone), new int[] {3, 3, 3})) throw new AssertionError("no friendships");
        int[][] all = {{1, 1, 1}, {1, 1, 1}, {1, 1, 1}};
        if (!Arrays.equals(solve(all), new int[] {1, 1, 1})) throw new AssertionError("full matrix");
        Random rnd = new Random(23602);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] m = symmetric(n, rnd, rnd.nextInt(60));
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = m[i].clone();
            int[] got = solve(m);
            if (!Arrays.equals(got, oracle(m))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(m, copy)) throw new AssertionError("input changed");
            for (int i = 1; i < n; i++) if (got[i] > got[i - 1]) throw new AssertionError("must not increase");
        }
    }
}
```

#### Solution: [Boundary] Duplicate Union (Author exercise)
<!-- id: ug-duplicate-union -->

**Approach.** Process the edges with a size-aware structure whose union does nothing when both labels match. After the last edge the number of groups is `n` minus the number of unions that really merged, and the number of connected pairs is the sum over each label of `s * (s - 1) / 2`, computed with `long` arithmetic. A repeated edge, a reversed copy, a self-loop and an edge inside an existing group all reach the same early exit, so none of them can disturb a size. The test file includes the broken version that skips the equality check, which doubles a size on the first repeated edge, and asserts that it fails the first example. The oracle builds a boolean Warshall table from the edges and counts distinct rows and true entries above the diagonal. Java claims are asserted directly: for a group of 60000 vertices the product `s * (s - 1)` computed in `int` already wraps to a negative number, and for 100000 vertices in one group the true pair count, 4,999,950,000, is larger than `Integer.MAX_VALUE`, so the `long` version is required.

**Complexity.** Every edge costs two finds with near-constant amortised time, so the run is O(m * alpha(n)) for m edges, and the final sweep over the labels adds O(n), with O(n) memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicateUnionSolution {
    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static long[] solve(int n, int[][] edges, boolean guard) {
        int[] parent = new int[n];
        long[] size = new long[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
        int groups = n;
        for (int[] e : edges) {
            int ra = find(parent, e[0]), rb = find(parent, e[1]);
            if (guard && ra == rb) continue;
            if (size[ra] < size[rb]) { int t = ra; ra = rb; rb = t; }
            parent[rb] = ra;
            size[ra] += size[rb];
            groups--;
        }
        long pairs = 0;
        for (int v = 0; v < n; v++) if (parent[v] == v) pairs += size[v] * (size[v] - 1) / 2;
        return new long[] {groups, pairs};
    }

    static long[] oracle(int n, int[][] edges) {
        boolean[][] r = new boolean[n][n];
        for (int i = 0; i < n; i++) r[i][i] = true;
        for (int[] e : edges) r[e[0]][e[1]] = r[e[1]][e[0]] = true;
        for (int k = 0; k < n; k++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                    if (r[i][k] && r[k][j]) r[i][j] = true;
        long pairs = 0;
        java.util.Set<String> rows = new java.util.HashSet<>();
        for (int i = 0; i < n; i++) {
            rows.add(Arrays.toString(r[i]));
            for (int j = i + 1; j < n; j++) if (r[i][j]) pairs++;
        }
        return new long[] {rows.size(), pairs};
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1}, {1, 0}, {0, 1}, {2, 3}};
        if (!Arrays.equals(solve(5, e1, true), new long[] {3, 2})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1}, {1, 2}, {2, 0}, {3, 3}};
        if (!Arrays.equals(solve(4, e2, true), new long[] {2, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[0][], true), new long[] {1, 0})) throw new AssertionError("no edges");
        if (Arrays.equals(solve(5, e1, false), new long[] {3, 2})) throw new AssertionError("missing guard must fail");
        int mid = 60000;
        int wrapped = mid * (mid - 1);
        if (wrapped >= 0) throw new AssertionError("int product should wrap");
        int s = 100000;
        if ((long) s * (s - 1) / 2 != 4_999_950_000L || 4_999_950_000L <= Integer.MAX_VALUE)
            throw new AssertionError("long product");
        int[][] chain = new int[s - 1][];
        for (int i = 0; i + 1 < s; i++) chain[i] = new int[] {i, i + 1};
        if (solve(s, chain, true)[1] != 4_999_950_000L) throw new AssertionError("large group");
        Random rnd = new Random(23603);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8), m = rnd.nextInt(14);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) {
                edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
                if (i > 0 && rnd.nextInt(3) == 0) edges[i] = new int[] {edges[i - 1][1], edges[i - 1][0]};
            }
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = edges[i].clone();
            if (!Arrays.equals(solve(n, edges, true), oracle(n, edges))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(edges, copy)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Recognize] Accounts Merge (LeetCode 721)
<!-- id: ug-accounts-merge -->

**Approach.** The elements to merge are accounts, but the thing that links them is an email, so the structure runs over account indices and a `HashMap<String, Integer>` remembers the first account that showed each email. When an email is seen again, the current account is unioned with that first account. After all accounts are processed, every email is placed in a `TreeSet` owned by its account's label, and each group is written as the name followed by the sorted set. Names are never used to decide anything, since two different people may share one, and that is why two accounts named alike but with no common email stay apart. The finished groups are sorted by comparing their lists element by element, so the output is deterministic. The oracle is label propagation: every account starts with its own label, and any two accounts that share an email repeatedly take the smaller label until a full pass changes nothing, after which groups are collected by label and sorted in the same way. The assertions cover both examples, one account repeating an email inside itself, two same-named strangers, uppercase emails sorting before lowercase under natural `String` order, and equal email text from separate `String` objects hitting the same map key.

**Complexity.** With E emails in total and N accounts, hashing and the unions cost O(E * alpha(N)) expected, and sorting the emails of all groups adds O(E log E) comparisons of strings, so the whole run is O(E log E) apart from the string lengths.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;
import java.util.TreeSet;

public final class AccountsMergeSolution {
    static int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static int compareLists(List<String> a, List<String> b) {
        int k = Math.min(a.size(), b.size());
        for (int i = 0; i < k; i++) {
            int c = a.get(i).compareTo(b.get(i));
            if (c != 0) return c;
        }
        return Integer.compare(a.size(), b.size());
    }

    static List<List<String>> solve(String[][] accounts) {
        int n = accounts.length;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
        Map<String, Integer> firstSeen = new HashMap<>();
        for (int i = 0; i < n; i++) {
            for (int k = 1; k < accounts[i].length; k++) {
                Integer owner = firstSeen.putIfAbsent(accounts[i][k], i);
                if (owner != null) {
                    int ra = find(parent, i), rb = find(parent, owner);
                    if (ra != rb) parent[ra] = rb;
                }
            }
        }
        Map<Integer, TreeSet<String>> emails = new HashMap<>();
        for (int i = 0; i < n; i++) {
            TreeSet<String> bucket = emails.computeIfAbsent(find(parent, i), r -> new TreeSet<>());
            for (int k = 1; k < accounts[i].length; k++) bucket.add(accounts[i][k]);
        }
        List<List<String>> out = new ArrayList<>();
        for (Map.Entry<Integer, TreeSet<String>> e : emails.entrySet()) {
            List<String> group = new ArrayList<>();
            group.add(accounts[e.getKey()][0]);
            group.addAll(e.getValue());
            out.add(group);
        }
        out.sort(AccountsMergeSolution::compareLists);
        return out;
    }

    static List<List<String>> oracle(String[][] accounts) {
        int n = accounts.length;
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) {
                    boolean share = false;
                    for (int a = 1; a < accounts[i].length; a++)
                        for (int b = 1; b < accounts[j].length; b++)
                            if (accounts[i][a].equals(accounts[j][b])) share = true;
                    if (share && label[i] != label[j]) {
                        int low = Math.min(label[i], label[j]);
                        label[i] = low;
                        label[j] = low;
                        changed = true;
                    }
                }
        }
        Map<Integer, TreeSet<String>> byLabel = new TreeMap<>();
        for (int i = 0; i < n; i++) {
            byLabel.computeIfAbsent(label[i], k -> new TreeSet<>());
            for (int k = 1; k < accounts[i].length; k++) byLabel.get(label[i]).add(accounts[i][k]);
        }
        List<List<String>> out = new ArrayList<>();
        for (Map.Entry<Integer, TreeSet<String>> e : byLabel.entrySet()) {
            List<String> group = new ArrayList<>();
            group.add(accounts[e.getKey()][0]);
            group.addAll(e.getValue());
            out.add(group);
        }
        out.sort(AccountsMergeSolution::compareLists);
        return out;
    }

    public static void main(String[] args) {
        String[][] a = {{"Ada", "a@x", "b@x"}, {"Bo", "c@x"}, {"Ada", "b@x", "d@x"}, {"Ada", "e@x"}};
        List<List<String>> want1 = List.of(List.of("Ada", "a@x", "b@x", "d@x"), List.of("Ada", "e@x"), List.of("Bo", "c@x"));
        if (!solve(a).equals(want1)) throw new AssertionError("example 1");
        String[][] b = {{"Eve", "x1", "x2"}, {"Eve", "x3"}, {"Eve", "x2", "x3"}, {"Fay", "y1"}, {"Fay", "y1", "y2"}};
        List<List<String>> want2 = List.of(List.of("Eve", "x1", "x2", "x3"), List.of("Fay", "y1", "y2"));
        if (!solve(b).equals(want2)) throw new AssertionError("example 2");
        String[][] twice = {{"Gus", "g@x", "g@x", "h@x"}};
        if (!solve(twice).equals(List.of(List.of("Gus", "g@x", "h@x")))) throw new AssertionError("repeat inside one account");
        String[][] strangers = {{"Hal", "p@x"}, {"Hal", "q@x"}};
        if (solve(strangers).size() != 2) throw new AssertionError("same name, no shared email");
        if ("B@x".compareTo("a@x") >= 0) throw new AssertionError("uppercase sorts first");
        Map<String, Integer> probe = new HashMap<>();
        probe.put(new String("k@x"), 1);
        if (probe.get(new String("k@x")) == null) throw new AssertionError("equal text, equal key");
        String[][] copyOfB = new String[b.length][];
        for (int i = 0; i < b.length; i++) copyOfB[i] = b[i].clone();
        solve(b);
        if (!Arrays.deepEquals(b, copyOfB)) throw new AssertionError("input changed");
        Random rnd = new Random(23604);
        String[] names = {"Ivy", "Jon", "Kit"};
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(7);
            String[][] acc = new String[n][];
            for (int i = 0; i < n; i++) {
                int k = 1 + rnd.nextInt(3), who = rnd.nextInt(names.length);
                String[] row = new String[k + 1];
                row[0] = names[who];
                for (int j = 1; j <= k; j++) row[j] = "m" + (who * 4 + rnd.nextInt(4));
                acc[i] = row;
            }
            List<List<String>> want = oracle(acc);
            List<List<String>> got = solve(acc);
            if (!got.equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```
