<!-- solutions-for: 06-path-enumeration -->
### Path Enumeration

#### Solution: [Build] Paths In A Tiny DAG (Author exercise)
<!-- id: gt-tiny-dag-paths -->

**Approach.** Keep one working list that starts with `from`. At each vertex other than the target, append a neighbor, recurse, and remove the last entry when the call returns. At the target, join the list into a string, which is a copy, and return. The oracle never follows edges while it builds. It grows every sequence of distinct vertices from `from`, layer by layer, and filters the sequences that end at `to` and use only listed edges. The assertions compare the two on random DAGs after sorting both, and check that sorted neighbor lists give lexicographic output, which is the search order. They also show three claims from the lesson: a global used set loses a route in a diamond, storing the live list leaves every entry equal to the starting vertex, and `remove(int)` on a `List<Integer>` deletes by index.

**Complexity.** The recursion makes one call per walk prefix it explores, and each success costs a copy of at most n vertices, so the time is O(P * n) plus dead-branch steps. The extra space is O(n) for the list and the stack, apart from the output.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class TinyDagPathsSolution {
    static List<String> solve(int[][] graph, int from, int to) {
        List<String> out = new ArrayList<>();
        List<Integer> path = new ArrayList<>();
        path.add(from);
        walk(graph, from, to, path, out);
        return out;
    }

    static void walk(int[][] graph, int v, int to, List<Integer> path, List<String> out) {
        if (v == to) {
            StringBuilder sb = new StringBuilder();
            for (int x : path) sb.append(sb.length() == 0 ? "" : " ").append(x);
            out.add(sb.toString());
            return;
        }
        for (int next : graph[v]) {
            path.add(next);
            walk(graph, next, to, path, out);
            path.remove(path.size() - 1);
        }
    }

    static List<String> oracle(int[][] graph, int from, int to) {
        int n = graph.length;
        boolean[][] edge = new boolean[n][n];
        for (int u = 0; u < n; u++) for (int w : graph[u]) edge[u][w] = true;
        List<List<Integer>> layer = new ArrayList<>();
        layer.add(List.of(from));
        List<String> kept = new ArrayList<>();
        while (!layer.isEmpty()) {
            List<List<Integer>> nextLayer = new ArrayList<>();
            for (List<Integer> seq : layer) {
                boolean good = seq.get(seq.size() - 1) == to;
                for (int i = 0; good && i + 1 < seq.size(); i++) good = edge[seq.get(i)][seq.get(i + 1)];
                if (good) kept.add(seq.toString().replaceAll("[\\[\\],]", "").trim());
                for (int v = 0; v < n; v++) {
                    if (seq.contains(v)) continue;
                    List<Integer> longer = new ArrayList<>(seq);
                    longer.add(v);
                    nextLayer.add(longer);
                }
            }
            layer = nextLayer;
        }
        return kept;
    }

    static int globalUsedCount(int[][] graph, int v, int to, boolean[] used) {
        used[v] = true;
        if (v == to) return 1;
        int total = 0;
        for (int next : graph[v]) if (!used[next]) total += globalUsedCount(graph, next, to, used);
        return total;
    }

    static void walkAliased(int[][] graph, int v, int to, List<Integer> path, List<List<Integer>> out) {
        if (v == to) {
            out.add(path);
            return;
        }
        for (int next : graph[v]) {
            path.add(next);
            walkAliased(graph, next, to, path, out);
            path.remove(path.size() - 1);
        }
    }

    static int[][] randomDag(Random rnd, int n, boolean sortedLists) {
        int[] label = new int[n];
        for (int i = 0; i < n; i++) label[i] = i;
        for (int i = n - 1; i > 0; i--) {
            int j = rnd.nextInt(i + 1);
            int t = label[i]; label[i] = label[j]; label[j] = t;
        }
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++)
            if (rnd.nextInt(10) < 5) adj.get(label[a]).add(label[b]);
        int[][] g = new int[n][];
        for (int v = 0; v < n; v++) {
            if (sortedLists) Collections.sort(adj.get(v)); else Collections.shuffle(adj.get(v), rnd);
            g[v] = adj.get(v).stream().mapToInt(Integer::intValue).toArray();
        }
        return g;
    }

    public static void main(String[] args) {
        if (!solve(new int[][] {{1, 2}, {3}, {3}, {}}, 0, 3).equals(List.of("0 1 3", "0 2 3")))
            throw new AssertionError("example 1");
        if (!solve(new int[][] {{2}, {0, 2}, {3}, {}}, 1, 3).equals(List.of("1 0 2 3", "1 2 3")))
            throw new AssertionError("example 2");
        int[][] diamond = {{1, 2}, {3}, {3}, {}};
        if (globalUsedCount(diamond, 0, 3, new boolean[4]) != 1 || solve(diamond, 0, 3).size() != 2)
            throw new AssertionError("a global used set must lose one diamond route");
        List<List<Integer>> aliased = new ArrayList<>();
        List<Integer> live = new ArrayList<>(List.of(0));
        walkAliased(diamond, 0, 3, live, aliased);
        if (aliased.size() != 2 || aliased.get(0) != aliased.get(1) || !aliased.get(0).equals(List.of(0)))
            throw new AssertionError("the live list must corrupt every stored entry");
        List<Integer> sample = new ArrayList<>(List.of(5, 6, 7));
        sample.remove(1);
        if (!sample.equals(List.of(5, 7))) throw new AssertionError("remove(int) removes by index");
        sample.remove(Integer.valueOf(7));
        if (!sample.equals(List.of(5))) throw new AssertionError("remove(Object) removes by value");
        Random rnd = new Random(21601);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(7);
            boolean sorted = t % 2 == 0;
            int[][] g = randomDag(rnd, n, sorted);
            int from = rnd.nextInt(n), to = rnd.nextInt(n);
            if (from == to) to = (to + 1) % n;
            int[][] copy = new int[n][];
            for (int v = 0; v < n; v++) copy[v] = g[v].clone();
            List<String> got = solve(g, from, to);
            List<String> want = oracle(g, from, to);
            if (sorted) {
                List<String> ordered = new ArrayList<>(got);
                Collections.sort(ordered);
                if (!ordered.equals(got)) throw new AssertionError("search order " + t);
            }
            Collections.sort(got);
            Collections.sort(want);
            if (!got.equals(want)) throw new AssertionError("random " + t);
            if (!java.util.Arrays.deepEquals(g, copy)) throw new AssertionError("graph modified " + t);
        }
    }
}
```

#### Solution: [Vary] All Paths From Source To Target (LeetCode 797)
<!-- id: gt-all-paths-source-target -->

**Approach.** The walk is the same append, recurse, remove loop, with two decisions fixed by the contract: the start is vertex 0, the target is vertex n - 1, and each stored path is a new `ArrayList` built from the working list at the target. The oracle fixes the first and last vertex and tries every subset of the other vertices in every order with a recursive permutation routine, keeping a sequence only when each consecutive pair is a listed edge. The assertions compare the two on random DAGs with shuffled neighbor lists, test that mutating one returned list leaves the others unchanged, and show that a chain of ten diamonds yields exactly 1024 paths, which is why listing is the wrong tool for a count. A global used set and an uncopied live list are both shown to give wrong answers on a diamond.

**Complexity.** Time is O(P * n) for P paths of length at most n, plus the steps spent in dead branches. Space apart from the answer is O(n) for the working list and recursion.

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class AllPathsSourceTargetSolution {
    static List<List<Integer>> solve(int[][] graph) {
        List<List<Integer>> answer = new ArrayList<>();
        List<Integer> trail = new ArrayList<>();
        trail.add(0);
        dfs(graph, 0, graph.length - 1, trail, answer);
        return answer;
    }

    static void dfs(int[][] graph, int v, int target, List<Integer> trail, List<List<Integer>> answer) {
        if (v == target) {
            answer.add(new ArrayList<>(trail));
            return;
        }
        for (int w : graph[v]) {
            trail.add(w);
            dfs(graph, w, target, trail, answer);
            trail.remove(trail.size() - 1);
        }
    }

    static void permute(int[][] graph, int mask, int last, int target, List<Integer> seq, List<List<Integer>> out) {
        int n = graph.length;
        if (last == target) {
            out.add(new ArrayList<>(seq));
            return;
        }
        for (int v = 0; v < n; v++) {
            if ((mask & (1 << v)) != 0) continue;
            boolean listed = false;
            for (int w : graph[last]) if (w == v) listed = true;
            if (!listed) continue;
            seq.add(v);
            permute(graph, mask | (1 << v), v, target, seq, out);
            seq.remove(seq.size() - 1);
        }
    }

    static List<List<Integer>> oracle(int[][] graph) {
        int n = graph.length;
        List<List<Integer>> every = new ArrayList<>();
        List<List<Integer>> kept = new ArrayList<>();
        List<Integer> seq = new ArrayList<>();
        seq.add(0);
        allSequences(n, 1, 0, seq, every);
        for (List<Integer> s : every) {
            if (s.get(s.size() - 1) != n - 1) continue;
            boolean ok = true;
            for (int i = 0; ok && i + 1 < s.size(); i++) {
                boolean listed = false;
                for (int w : graph[s.get(i)]) if (w == s.get(i + 1)) listed = true;
                ok = listed;
            }
            if (ok) kept.add(s);
        }
        return kept;
    }

    static void allSequences(int n, int mask, int last, List<Integer> seq, List<List<Integer>> out) {
        out.add(new ArrayList<>(seq));
        for (int v = 0; v < n; v++) {
            if ((mask & (1 << v)) != 0) continue;
            seq.add(v);
            allSequences(n, mask | (1 << v), v, seq, out);
            seq.remove(seq.size() - 1);
        }
    }

    static int withGlobalSet(int[][] graph, int v, boolean[] used) {
        used[v] = true;
        if (v == graph.length - 1) return 1;
        int total = 0;
        for (int w : graph[v]) if (!used[w]) total += withGlobalSet(graph, w, used);
        return total;
    }

    static void withoutCopy(int[][] graph, int v, List<Integer> trail, List<List<Integer>> answer) {
        if (v == graph.length - 1) {
            answer.add(trail);
            return;
        }
        for (int w : graph[v]) {
            trail.add(w);
            withoutCopy(graph, w, trail, answer);
            trail.remove(trail.size() - 1);
        }
    }

    static List<String> keys(List<List<Integer>> paths) {
        List<String> out = new ArrayList<>();
        for (List<Integer> p : paths) out.add(p.toString());
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        int[][] one = {{1, 2, 3}, {3}, {1, 3}, {}};
        if (!keys(solve(one)).equals(List.of("[0, 1, 3]", "[0, 2, 1, 3]", "[0, 2, 3]", "[0, 3]")))
            throw new AssertionError("example 1");
        if (!solve(new int[][] {{1}, {2}, {3}, {4}, {}}).equals(List.of(List.of(0, 1, 2, 3, 4))))
            throw new AssertionError("example 2");
        int[][] diamond = {{1, 2}, {3}, {3}, {}};
        if (withGlobalSet(diamond, 0, new boolean[4]) != 1) throw new AssertionError("global set loses a route");
        List<List<Integer>> bad = new ArrayList<>();
        withoutCopy(diamond, 0, new ArrayList<>(List.of(0)), bad);
        if (bad.size() != 2 || bad.get(0) != bad.get(1) || bad.get(0).size() != 1)
            throw new AssertionError("the uncopied list must be corrupted");
        List<List<Integer>> two = solve(diamond);
        two.get(0).add(99);
        if (two.get(1).contains(99) || two.get(0).equals(two.get(1))) throw new AssertionError("results must be independent");
        int k = 10, size = 3 * k + 1;
        int[][] chain = new int[size][];
        for (int i = 0; i < k; i++) {
            int top = 3 * i;
            chain[top] = new int[] {top + 1, top + 2};
            chain[top + 1] = new int[] {top + 3};
            chain[top + 2] = new int[] {top + 3};
        }
        chain[size - 1] = new int[0];
        if (solve(chain).size() != 1024) throw new AssertionError("ten diamonds make 1024 paths");
        Random rnd = new Random(21602);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(7);
            int[][] g = TinyShape.randomDag(rnd, n);
            int[][] copy = new int[n][];
            for (int v = 0; v < n; v++) copy[v] = g[v].clone();
            if (!keys(solve(g)).equals(keys(oracle(g)))) throw new AssertionError("random " + t);
            if (!java.util.Arrays.deepEquals(g, copy)) throw new AssertionError("graph modified " + t);
            List<List<Integer>> viaPermute = new ArrayList<>();
            List<Integer> s0 = new ArrayList<>();
            s0.add(0);
            permute(g, 1, 0, n - 1, s0, viaPermute);
            if (!keys(viaPermute).equals(keys(solve(g)))) throw new AssertionError("second oracle " + t);
        }
    }

    static final class TinyShape {
        static int[][] randomDag(Random rnd, int n) {
            int[] rank = new int[n];
            for (int i = 0; i < n; i++) rank[i] = i;
            for (int i = n - 1; i > 1; i--) {
                int j = 1 + rnd.nextInt(i);
                int tmp = rank[i]; rank[i] = rank[j]; rank[j] = tmp;
            }
            List<List<Integer>> adj = new ArrayList<>();
            for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++)
                if (rnd.nextInt(10) < 6) adj.get(rank[a]).add(rank[b]);
            int[][] g = new int[n][];
            for (int v = 0; v < n; v++) {
                Collections.shuffle(adj.get(v), rnd);
                g[v] = new int[adj.get(v).size()];
                for (int i = 0; i < g[v].length; i++) g[v][i] = adj.get(v).get(i);
            }
            return g;
        }
    }
}
```

#### Solution: [Boundary] Dead End And Direct Edge (Author exercise)
<!-- id: gt-dead-end-direct-edge -->

**Approach.** The test for recording is `v == to`, placed before the neighbor loop, and nothing else records. That one rule covers all three boundaries: a direct edge is a path of two vertices, a start equal to the target returns at once with the single-vertex path, and a dead end that is not the target falls through an empty loop and records nothing. The oracle expands sequences with a queue, one vertex at a time over all unused vertices, and keeps those that end at `to` and follow listed edges. The assertions compare the two on random DAGs of up to six vertices with sampled start and target pairs, and show that the tempting alternative of recording at any vertex with no neighbors returns an invalid path on the first example.

**Complexity.** Time is O(P * n) plus the steps in dead branches, with P the number of paths. Space apart from the output is O(n) for the list and the recursion.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class DeadEndDirectEdgeSolution {
    static List<List<Integer>> solve(int[][] graph, int from, int to) {
        List<List<Integer>> paths = new ArrayList<>();
        List<Integer> current = new ArrayList<>();
        current.add(from);
        explore(graph, from, to, current, paths, false);
        return paths;
    }

    static void explore(int[][] graph, int v, int to, List<Integer> current, List<List<Integer>> paths, boolean recordAtDeadEnds) {
        boolean complete = recordAtDeadEnds ? graph[v].length == 0 : v == to;
        if (complete) paths.add(new ArrayList<>(current));
        if (!recordAtDeadEnds && v == to) return;
        for (int w : graph[v]) {
            current.add(w);
            explore(graph, w, to, current, paths, recordAtDeadEnds);
            current.remove(current.size() - 1);
        }
    }

    static List<List<Integer>> oracle(int[][] graph, int from, int to) {
        int n = graph.length;
        List<List<Integer>> kept = new ArrayList<>();
        ArrayDeque<List<Integer>> queue = new ArrayDeque<>();
        queue.add(List.of(from));
        while (!queue.isEmpty()) {
            List<Integer> seq = queue.poll();
            int end = seq.get(seq.size() - 1);
            boolean follows = true;
            for (int i = 0; follows && i + 1 < seq.size(); i++) {
                boolean listed = false;
                for (int w : graph[seq.get(i)]) listed |= w == seq.get(i + 1);
                follows = listed;
            }
            if (follows && end == to) kept.add(seq);
            for (int v = 0; v < n; v++) {
                if (seq.contains(v)) continue;
                List<Integer> longer = new ArrayList<>(seq);
                longer.add(v);
                queue.add(longer);
            }
        }
        return kept;
    }

    static List<String> keys(List<List<Integer>> paths) {
        List<String> out = new ArrayList<>();
        for (List<Integer> p : paths) out.add(p.toString());
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        int[][] one = {{1, 3}, {2}, {}, {}};
        if (!solve(one, 0, 3).equals(List.of(List.of(0, 3)))) throw new AssertionError("example 1");
        if (!solve(new int[][] {{1}, {}, {1}}, 0, 2).isEmpty()) throw new AssertionError("example 2");
        if (!solve(new int[][] {{1, 2}, {2}, {}}, 1, 1).equals(List.of(List.of(1))))
            throw new AssertionError("start equal to target");
        if (!solve(new int[][] {{}}, 0, 0).equals(List.of(List.of(0)))) throw new AssertionError("single vertex");
        List<List<Integer>> wrong = new ArrayList<>();
        List<Integer> cur = new ArrayList<>(List.of(0));
        explore(one, 0, 3, cur, wrong, true);
        if (wrong.size() != 2 || !wrong.contains(List.of(0, 1, 2)))
            throw new AssertionError("recording at dead ends must produce an invalid path");
        Random rnd = new Random(21603);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(6);
            List<List<Integer>> adj = new ArrayList<>();
            for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
            int[] order = new int[n];
            for (int i = 0; i < n; i++) order[i] = i;
            for (int i = n - 1; i > 0; i--) {
                int j = rnd.nextInt(i + 1);
                int tmp = order[i]; order[i] = order[j]; order[j] = tmp;
            }
            int density = rnd.nextInt(8) + 1;
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++)
                if (rnd.nextInt(10) < density) adj.get(order[a]).add(order[b]);
            int[][] g = new int[n][];
            for (int v = 0; v < n; v++) {
                Collections.shuffle(adj.get(v), rnd);
                g[v] = adj.get(v).stream().mapToInt(Integer::intValue).toArray();
            }
            for (int pick = 0; pick < 3; pick++) {
                int from = rnd.nextInt(n), to = rnd.nextInt(n);
                if (!keys(solve(g, from, to)).equals(keys(oracle(g, from, to))))
                    throw new AssertionError("random " + t + " " + from + " " + to);
            }
        }
    }
}
```

#### Solution: [Recognize] Enumerate Simple Paths (Author exercise)
<!-- id: gt-simple-paths -->

**Approach.** Cycles break the idea that a downhill order makes repeats impossible, so the walk carries a boolean array `onPath`. A vertex is marked when the walk enters it and cleared when the call is about to leave, which keeps the marks equal to the working list at all times. A marked neighbor is skipped, and this also removes self loops. The oracle enumerates every subset of the vertices other than the two ends, and for each subset steps through all its orderings with a next-permutation routine, keeping the orderings whose consecutive pairs are listed edges. The assertions compare the two on random directed graphs with cycles and self loops, and show that a single global set loses simple paths on the first example, while running with no marks at all produces a path with a repeated vertex once the length is capped.

**Complexity.** The number of simple paths can grow factorially, so time is O(P * n) plus the dead-branch steps, where P may be exponential in n. Memory beyond the output is O(n) for the mark array, the list and the stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class SimplePathsSolution {
    static List<List<Integer>> solve(int[][] graph, int from, int to) {
        List<List<Integer>> result = new ArrayList<>();
        boolean[] onPath = new boolean[graph.length];
        List<Integer> route = new ArrayList<>();
        route.add(from);
        onPath[from] = true;
        go(graph, from, to, onPath, route, result);
        return result;
    }

    static void go(int[][] graph, int v, int to, boolean[] onPath, List<Integer> route, List<List<Integer>> result) {
        if (v == to) {
            result.add(new ArrayList<>(route));
            return;
        }
        for (int w : graph[v]) {
            if (onPath[w]) continue;
            onPath[w] = true;
            route.add(w);
            go(graph, w, to, onPath, route, result);
            route.remove(route.size() - 1);
            onPath[w] = false;
        }
    }

    static boolean nextPermutation(int[] a) {
        int i = a.length - 2;
        while (i >= 0 && a[i] >= a[i + 1]) i--;
        if (i < 0) return false;
        int j = a.length - 1;
        while (a[j] <= a[i]) j--;
        int t = a[i]; a[i] = a[j]; a[j] = t;
        for (int l = i + 1, r = a.length - 1; l < r; l++, r--) {
            t = a[l]; a[l] = a[r]; a[r] = t;
        }
        return true;
    }

    static boolean listed(int[][] graph, int u, int v) {
        for (int w : graph[u]) if (w == v) return true;
        return false;
    }

    static List<List<Integer>> oracle(int[][] graph, int from, int to) {
        int n = graph.length;
        List<Integer> others = new ArrayList<>();
        for (int v = 0; v < n; v++) if (v != from && v != to) others.add(v);
        List<List<Integer>> kept = new ArrayList<>();
        for (int mask = 0; mask < (1 << others.size()); mask++) {
            List<Integer> mid = new ArrayList<>();
            for (int i = 0; i < others.size(); i++) if ((mask >> i & 1) == 1) mid.add(others.get(i));
            int[] arr = mid.stream().mapToInt(Integer::intValue).toArray();
            do {
                List<Integer> seq = new ArrayList<>();
                seq.add(from);
                for (int x : arr) seq.add(x);
                seq.add(to);
                boolean ok = true;
                for (int i = 0; ok && i + 1 < seq.size(); i++) ok = listed(graph, seq.get(i), seq.get(i + 1));
                if (ok) kept.add(seq);
            } while (nextPermutation(arr));
        }
        return kept;
    }

    static int globalSetCount(int[][] graph, int v, int to, boolean[] used) {
        used[v] = true;
        if (v == to) return 1;
        int total = 0;
        for (int w : graph[v]) if (!used[w]) total += globalSetCount(graph, w, to, used);
        return total;
    }

    static boolean unmarkedFindsRepeat(int[][] graph, int v, int to, List<Integer> route, int cap) {
        if (route.size() > cap) return false;
        if (v == to) return route.stream().distinct().count() != route.size();
        for (int w : graph[v]) {
            route.add(w);
            boolean hit = unmarkedFindsRepeat(graph, w, to, route, cap);
            route.remove(route.size() - 1);
            if (hit) return true;
        }
        return false;
    }

    static List<String> keys(List<List<Integer>> paths) {
        List<String> out = new ArrayList<>();
        for (List<Integer> p : paths) out.add(p.toString());
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        int[][] one = {{1, 2}, {0, 2, 3}, {1, 3}, {}};
        if (!keys(solve(one, 0, 3)).equals(List.of("[0, 1, 2, 3]", "[0, 1, 3]", "[0, 2, 1, 3]", "[0, 2, 3]")))
            throw new AssertionError("example 1");
        int[][] two = {{1}, {2, 0}, {1, 3}, {}};
        if (!solve(two, 0, 3).equals(List.of(List.of(0, 1, 2, 3)))) throw new AssertionError("example 2");
        if (globalSetCount(one, 0, 3, new boolean[4]) >= 4) throw new AssertionError("a global set loses simple paths");
        if (!unmarkedFindsRepeat(two, 0, 3, new ArrayList<>(List.of(0)), 8))
            throw new AssertionError("without marks a repeated vertex appears");
        Random rnd = new Random(21604);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(6);
            int[][] g = new int[n][];
            int density = 2 + rnd.nextInt(6);
            for (int v = 0; v < n; v++) {
                List<Integer> out = new ArrayList<>();
                for (int w = 0; w < n; w++) if (rnd.nextInt(10) < density) out.add(w);
                Collections.shuffle(out, rnd);
                g[v] = out.stream().mapToInt(Integer::intValue).toArray();
            }
            int from = rnd.nextInt(n), to = rnd.nextInt(n);
            if (from == to) to = (to + 1) % n;
            int[][] copy = new int[n][];
            for (int v = 0; v < n; v++) copy[v] = g[v].clone();
            if (!keys(solve(g, from, to)).equals(keys(oracle(g, from, to)))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(g, copy)) throw new AssertionError("graph modified " + t);
        }
    }
}
```
