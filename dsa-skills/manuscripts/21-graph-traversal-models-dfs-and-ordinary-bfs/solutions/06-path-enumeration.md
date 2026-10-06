<!-- solutions-for: 06-path-enumeration -->
### Solutions For Path Enumeration

#### Solution: [Build] Paths In A Tiny DAG (Author exercise)
<!-- id: gt-tiny-dag-paths -->

**Approach.**
The method builds the adjacency list `adj` from `edges` in input order and then runs one recursive search from vertex 0. Each call appends its vertex to the working path and checks whether the vertex is the target. A target call stores a snapshot, and any other call recurses into every neighbor in order. At the end of the call, the last element is removed, so the list equals the chain of the caller again.

The graph is acyclic, so no vertex can appear twice in the working path, and no visited array is needed. The invariant is that the working path equals the chain of active calls at every call boundary. The code also shows two Java facts of the lesson. The call `remove(int)` on a `List<Integer>` removes by index, and the call `remove(Object)` removes by value.

**Complexity.**
- **Time** is O(P * n + V + E) on a DAG with `P` paths, because each snapshot copies at most `n` vertices and the search crosses each edge once per chain that reaches it.
- **Space** is O(n) beyond the output, because the working path and the call stack hold at most `n` entries.

```java run
import java.util.*;

public final class TinyDagPaths {
    /**
     * Returns every path from vertex 0 to vertex n - 1 in DFS order.
     * Time: O(P * n + V + E) for P paths. Space: O(n) beyond the output.
     * Invariant: the working path equals the chain of active calls.
     */
    static List<List<Integer>> allPaths(int n, int[][] edges) {
        // One neighbor list per vertex, filled in edge order, so the search order is deterministic.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        // Each directed edge goes into the list of its tail vertex only.
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        // The result list collects one snapshot per complete path.
        List<List<Integer>> found = new ArrayList<>();
        // The search starts with an empty working path at the source.
        walk(adj, 0, n - 1, new ArrayList<>(), found);
        return found;
    }

    private static void walk(List<List<Integer>> adj, int cur, int target,
                             List<Integer> path, List<List<Integer>> found) {
        // Append on entry, so the list ends with the vertex being expanded.
        path.add(cur);
        // Reaching the target completes a path; the copy costs O(n) per recorded path.
        if (cur == target) found.add(new ArrayList<>(path));
        // Otherwise try each neighbor in edge order; the DAG guarantees that none is on the path.
        else for (int next : adj.get(cur)) walk(adj, next, target, path, found);
        // Remove the last element by index, which restores the working path of the caller.
        path.remove(path.size() - 1);
    }

    /** Brute force: each ascending subset of middle vertices is a candidate; valid when consecutive edges exist. */
    static List<String> brute(int n, boolean[][] has) {
        List<String> out = new ArrayList<>();
        // Mask bit b stands for the middle vertex b + 1, so a mask covers vertices 1..n-2.
        for (int mask = 0; mask < (1 << (n - 2)); mask++) {
            // Candidate sequence in ascending vertex order; labels are topological in the random tests.
            List<Integer> seq = new ArrayList<>(List.of(0));
            for (int b = 0; b < n - 2; b++) if ((mask >> b & 1) == 1) seq.add(b + 1);
            seq.add(n - 1);
            // Check every consecutive pair against the edge matrix.
            boolean ok = true;
            for (int i = 0; i + 1 < seq.size(); i++) if (!has[seq.get(i)][seq.get(i + 1)]) ok = false;
            if (ok) out.add(seq.toString());
        }
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        // Example 1 of the exercise, with exact DFS order.
        List<List<Integer>> r1 = allPaths(4, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}});
        if (!r1.toString().equals("[[0, 1, 3], [0, 2, 3]]")) throw new AssertionError("ex1 " + r1);
        // Example 2 of the exercise.
        List<List<Integer>> r2 = allPaths(5, new int[][] {{0, 1}, {1, 2}, {0, 2}, {2, 4}, {1, 4}, {3, 4}});
        if (!r2.toString().equals("[[0, 1, 2, 4], [0, 1, 4], [0, 2, 4]]")) throw new AssertionError("ex2 " + r2);
        // No edges means no path.
        if (!allPaths(3, new int[0][]).isEmpty()) throw new AssertionError("no edges");
        // Java fact: remove(int) on List<Integer> removes by index, not by value.
        List<Integer> probe = new ArrayList<>(List.of(10, 20, 30));
        int idx = 1;
        probe.remove(idx);
        if (!probe.equals(List.of(10, 30))) throw new AssertionError("remove(int) removes the element at that index");
        // Java fact: remove(Object) removes by value.
        probe.remove(Integer.valueOf(30));
        if (!probe.equals(List.of(10))) throw new AssertionError("remove(Object) removes by value");
        // Random DAGs with forward edges must match the subset brute force.
        Random rnd = new Random(2106);
        for (int t = 0; t < 400; t++) {
            int n = 2 + rnd.nextInt(6);
            boolean[][] has = new boolean[n][n];
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(2) == 0) { has[a][b] = true; es.add(new int[] {a, b}); }
            Collections.shuffle(es, rnd);
            List<String> got = new ArrayList<>();
            for (List<Integer> p : allPaths(n, es.toArray(new int[0][]))) got.add(p.toString());
            Collections.sort(got);
            if (!got.equals(brute(n, has))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] All Paths From Source to Target (LeetCode 797)
<!-- id: gt-all-paths-source-target -->

**Approach.**
This method keeps the working path in a plain `int[]` buffer with a depth counter, and it takes a snapshot with `Arrays.copyOf(buffer, depth)` when the call reaches the target. The buffer holds the chain at indexes `0` to `depth - 1`, and a call writes its vertex at index `depth`. Leaving a call needs no removal, because the next write overwrites the slot, and the depth counter alone marks the end of the chain.

The reason for the copy is the changed decision of the exercise. The buffer is reused by every later call, so a stored reference to the buffer would show the last contents. The invariant is that the first `depth` slots equal the current chain. The code asserts that two returned lists share no storage.

**Complexity.**
- **Time** is O(P * n + V + E) for `P` paths, because each copy costs at most `n` and each edge is crossed once per chain that reaches it.
- **Space** is O(n) beyond the output, because the buffer and the call stack are bounded by the vertex count.

```java run
import java.util.*;

public final class AllPathsSourceTarget {
    /**
     * Returns every path from 0 to n - 1 as independent lists, in DFS order.
     * Time: O(P * n + V + E). Space: O(n) beyond the output.
     * Invariant: buffer[0..depth-1] equals the chain of active calls.
     */
    static List<List<Integer>> paths(int n, int[][] edges) {
        // Arrays of neighbor lists give O(1) access per vertex; edge order is kept.
        List<Integer>[] adj = new List[n];
        for (int v = 0; v < n; v++) adj[v] = new ArrayList<>();
        // Every directed edge is stored once at its tail.
        for (int[] e : edges) adj[e[0]].add(e[1]);
        // The buffer never needs more than n slots, because a path has at most n vertices.
        int[] buffer = new int[n];
        List<List<Integer>> out = new ArrayList<>();
        dfs(adj, 0, n - 1, buffer, 0, out);
        return out;
    }

    private static void dfs(List<Integer>[] adj, int cur, int target, int[] buffer, int depth, List<List<Integer>> out) {
        // Write the vertex at the next free slot; no append call and no removal is needed.
        buffer[depth] = cur;
        if (cur == target) {
            // Copy exactly depth + 1 slots, because later calls overwrite the buffer.
            List<Integer> snap = new ArrayList<>();
            for (int i = 0; i <= depth; i++) snap.add(buffer[i]);
            out.add(snap);
            return;
        }
        // Each neighbor gets depth + 1, so returning to this loop restores the chain by itself.
        for (int next : adj[cur]) dfs(adj, next, target, buffer, depth + 1, out);
    }

    /** Brute force: grow partial paths in a queue until every one ends at the target or at a dead end. */
    static List<String> brute(int n, int[][] edges) {
        List<String> out = new ArrayList<>();
        ArrayDeque<List<Integer>> queue = new ArrayDeque<>();
        queue.add(List.of(0));
        // Each partial path is extended by every edge leaving its last vertex.
        while (!queue.isEmpty()) {
            List<Integer> p = queue.poll();
            int last = p.get(p.size() - 1);
            if (last == n - 1) { out.add(p.toString()); continue; }
            for (int[] e : edges) if (e[0] == last) { List<Integer> q = new ArrayList<>(p); q.add(e[1]); queue.add(q); }
        }
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        // Example 1 of the exercise.
        List<List<Integer>> r1 = paths(6, new int[][] {{0, 1}, {0, 2}, {1, 3}, {2, 3}, {3, 4}, {3, 5}, {4, 5}});
        if (!r1.toString().equals("[[0, 1, 3, 4, 5], [0, 1, 3, 5], [0, 2, 3, 4, 5], [0, 2, 3, 5]]")) throw new AssertionError("ex1 " + r1);
        // Example 2 of the exercise.
        List<List<Integer>> r2 = paths(5, new int[][] {{0, 1}, {0, 2}, {1, 4}, {2, 3}, {0, 4}});
        if (!r2.toString().equals("[[0, 1, 4], [0, 4]]")) throw new AssertionError("ex2 " + r2);
        // Independence: changing one list leaves the other unchanged.
        r1.get(0).set(0, 99);
        if (r1.get(1).get(0) != 0) throw new AssertionError("lists must not share storage");
        // Aliasing fact: adding one reused list object stores the same object twice.
        List<List<Integer>> alias = new ArrayList<>();
        List<Integer> shared = new ArrayList<>(List.of(1));
        alias.add(shared);
        shared.add(2);
        alias.add(shared);
        shared.clear();
        if (!alias.get(0).isEmpty() || alias.get(0) != alias.get(1)) throw new AssertionError("a stored reference sees later changes");
        // Random DAGs with shuffled labels must match the queue brute force.
        Random rnd = new Random(2107);
        for (int t = 0; t < 400; t++) {
            int n = 2 + rnd.nextInt(7);
            // Relabel vertices by a random permutation that keeps 0 as source and n - 1 as target.
            List<Integer> perm = new ArrayList<>();
            for (int v = 1; v < n - 1; v++) perm.add(v);
            Collections.shuffle(perm, rnd);
            perm.add(0, 0);
            perm.add(n - 1);
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(3) > 0) es.add(new int[] {perm.get(a), perm.get(b)});
            Collections.shuffle(es, rnd);
            int[][] arr = es.toArray(new int[0][]);
            List<String> got = new ArrayList<>();
            for (List<Integer> p : paths(n, arr)) got.add(p.toString());
            Collections.sort(got);
            if (!got.equals(brute(n, arr))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Dead End And Direct Edge (Author exercise)
<!-- id: gt-dead-end-direct-edge -->

**Approach.**
This method returns the answer of each call instead of filling a shared list. The call for vertex `v` returns every path from `v` to the target. When `v` is the target, the answer is the single path that holds `v`. Otherwise the call collects the answers of its neighbors and puts `v` in front of each returned path. A vertex without outgoing edges that is not the target collects nothing, so it returns an empty list, and no incomplete path ever appears.

The direct edge from `s` to `t` needs no special case. The neighbor `t` returns the one-vertex path, and the call for `s` prepends itself, which gives the two-vertex path. The invariant is that every returned path starts at the vertex of the call and ends at the target.

**Complexity.**
- **Time** is O(P * n + V + E) in the worst case, because every returned path is rebuilt once per ancestor level and has at most `n` vertices.
- **Space** is O(P * n) for the returned lists, plus an O(n) call stack.

```java run
import java.util.*;

public final class DeadEndDirectEdge {
    /**
     * Returns every path from s to t in a DAG, built from the answers of the neighbors.
     * Time: O(P * n + V + E). Space: O(P * n) for the returned lists.
     * Invariant: every list returned by suffixes(v) starts at v and ends at t.
     */
    static List<List<Integer>> routes(int n, int[][] edges, int s, int t) {
        // Neighbor lists in edge order.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        return suffixes(adj, s, t);
    }

    private static List<List<Integer>> suffixes(List<List<Integer>> adj, int v, int t) {
        List<List<Integer>> result = new ArrayList<>();
        // The target ends every path, so its only suffix is the vertex itself.
        if (v == t) { result.add(new ArrayList<>(List.of(v))); return result; }
        // A dead end has no neighbors, so this loop adds nothing and the empty list is returned.
        for (int next : adj.get(v)) {
            for (List<Integer> tail : suffixes(adj, next, t)) {
                // Prepend v to a private copy so the tail of the neighbor stays unchanged.
                List<Integer> whole = new ArrayList<>();
                whole.add(v);
                whole.addAll(tail);
                result.add(whole);
            }
        }
        return result;
    }

    /** Brute force: try every sequence of distinct vertices that starts at s and ends at t and check its edges. */
    static void extend(int n, boolean[][] has, List<Integer> seq, int t, List<String> out) {
        int last = seq.get(seq.size() - 1);
        if (last == t) { out.add(seq.toString()); return; }
        for (int v = 0; v < n; v++) {
            if (seq.contains(v) || !has[last][v]) continue;
            seq.add(v);
            extend(n, has, seq, t, out);
            seq.remove(seq.size() - 1);
        }
    }

    public static void main(String[] args) {
        // Example 1: the branch through vertex 1 dead-ends at vertex 2 and adds nothing.
        List<List<Integer>> r1 = routes(4, new int[][] {{0, 1}, {0, 3}, {1, 2}}, 0, 3);
        if (!r1.toString().equals("[[0, 3]]")) throw new AssertionError("ex1 " + r1);
        // Example 2: the target is unreachable, so the result is empty.
        if (!routes(3, new int[][] {{0, 1}, {2, 1}}, 0, 2).isEmpty()) throw new AssertionError("ex2");
        // A direct edge alone gives a path of two vertices.
        if (!routes(2, new int[][] {{0, 1}}, 0, 1).toString().equals("[[0, 1]]")) throw new AssertionError("direct edge");
        // Random DAGs with forward edges and random s < t must match the distinct-sequence brute force.
        Random rnd = new Random(2108);
        for (int t = 0; t < 400; t++) {
            int n = 2 + rnd.nextInt(6);
            boolean[][] has = new boolean[n][n];
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(3) == 0) { has[a][b] = true; es.add(new int[] {a, b}); }
            Collections.shuffle(es, rnd);
            int s = rnd.nextInt(n - 1), tg = s + 1 + rnd.nextInt(n - 1 - s);
            List<String> got = new ArrayList<>();
            for (List<Integer> p : routes(n, es.toArray(new int[0][]), s, tg)) got.add(p.toString());
            Collections.sort(got);
            List<String> want = new ArrayList<>();
            extend(n, has, new ArrayList<>(List.of(s)), tg, want);
            Collections.sort(want);
            if (!got.equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Enumerate Simple Paths (Author exercise)
<!-- id: gt-enumerate-simple-paths -->

**Approach.**
A cycle can lead back to a vertex that is already on the chain, so the DAG argument no longer holds. The method adds a boolean array `onPath` that a call sets to true on entry and sets to false on exit. This flag describes the working path and nothing else, so a vertex that finished on one branch is allowed again on the next branch. The global rule from the naive stage differs exactly here, because it never clears the flag.

A call stops at the target and records a snapshot. Every other call skips the neighbors that are marked in `onPath` and recurses into the rest. The invariant is that `onPath[v]` is true exactly when `v` is in the working path. The code also asserts that the never-cleared rule loses paths on the second example.

**Complexity.**
- **Time** is O(P * n + number of explored chains * deg) in the worst case, and the number of simple paths can be factorial in `n`, because every ordering of the middle vertices may form a path in a dense graph.
- **Space** is O(n) beyond the output, because `onPath`, the working path and the call stack are bounded by the vertex count.

```java run
import java.util.*;

public final class SimplePaths {
    /**
     * Returns every simple path from s to t in DFS order.
     * Time: exponential in the worst case, O(P * n) plus the dead branches. Space: O(n) beyond the output.
     * Invariant: onPath[v] is true exactly when v is in the working path.
     */
    static List<List<Integer>> simplePaths(int n, int[][] edges, int s, int t, boolean clearOnExit) {
        // Neighbor lists in edge order.
        List<List<Integer>> adj = new ArrayList<>();
        for (int v = 0; v < n; v++) adj.add(new ArrayList<>());
        for (int[] e : edges) adj.get(e[0]).add(e[1]);
        List<List<Integer>> found = new ArrayList<>();
        visit(adj, s, t, new boolean[n], new ArrayList<>(), found, clearOnExit);
        return found;
    }

    private static void visit(List<List<Integer>> adj, int cur, int t, boolean[] onPath,
                              List<Integer> path, List<List<Integer>> found, boolean clearOnExit) {
        // Mark and append on entry, so both structures describe the chain through cur.
        onPath[cur] = true;
        path.add(cur);
        if (cur == t) found.add(new ArrayList<>(path));
        else for (int next : adj.get(cur)) if (!onPath[next]) visit(adj, next, t, onPath, path, found, clearOnExit);
        // Unmark and remove on exit; skipping the unmark reproduces the naive global rule.
        if (clearOnExit) onPath[cur] = false;
        path.remove(path.size() - 1);
    }

    /** Brute force: enumerate every base-n tuple of length L, keep those with distinct vertices, correct ends and existing edges. */
    static List<String> brute(int n, boolean[][] has, int s, int t) {
        List<String> out = new ArrayList<>();
        for (int len = 2; len <= n; len++) {
            int total = 1;
            for (int i = 0; i < len; i++) total *= n;
            for (int code = 0; code < total; code++) {
                int[] seq = new int[len];
                int x = code;
                for (int i = len - 1; i >= 0; i--) { seq[i] = x % n; x /= n; }
                if (seq[0] != s || seq[len - 1] != t) continue;
                boolean ok = true;
                for (int i = 0; i < len && ok; i++) {
                    for (int j = 0; j < i; j++) if (seq[i] == seq[j]) ok = false;
                    if (i > 0 && !has[seq[i - 1]][seq[i]]) ok = false;
                }
                if (ok) out.add(Arrays.toString(seq));
            }
        }
        Collections.sort(out);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: the cycle 0, 1, 2 does not add a path, because vertex 0 is already on the chain.
        List<List<Integer>> r1 = simplePaths(4, new int[][] {{0, 1}, {1, 2}, {2, 0}, {1, 3}, {2, 3}}, 0, 3, true);
        if (!r1.toString().equals("[[0, 1, 2, 3], [0, 1, 3]]")) throw new AssertionError("ex1 " + r1);
        // Example 2 with the flag cleared on exit.
        int[][] e2 = {{0, 1}, {1, 0}, {0, 2}, {1, 2}, {2, 1}, {2, 4}, {1, 4}};
        List<List<Integer>> r2 = simplePaths(5, e2, 0, 4, true);
        if (!r2.toString().equals("[[0, 1, 2, 4], [0, 1, 4], [0, 2, 1, 4], [0, 2, 4]]")) throw new AssertionError("ex2 " + r2);
        // The never-cleared rule finds only the first path on the same input.
        if (!simplePaths(5, e2, 0, 4, false).toString().equals("[[0, 1, 2, 4]]")) throw new AssertionError("global rule loses paths");
        // No route means an empty result.
        if (!simplePaths(3, new int[][] {{0, 1}}, 0, 2, true).isEmpty()) throw new AssertionError("unreachable");
        // Random digraphs with cycles must match the tuple brute force.
        Random rnd = new Random(2109);
        for (int t = 0; t < 300; t++) {
            int n = 2 + rnd.nextInt(4);
            boolean[][] has = new boolean[n][n];
            List<int[]> es = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) if (a != b && rnd.nextInt(2) == 0) { has[a][b] = true; es.add(new int[] {a, b}); }
            Collections.shuffle(es, rnd);
            int s = rnd.nextInt(n), tg = (s + 1 + rnd.nextInt(n - 1)) % n;
            List<String> got = new ArrayList<>();
            for (List<Integer> p : simplePaths(n, es.toArray(new int[0][]), s, tg, true)) got.add(p.toString());
            Collections.sort(got);
            if (!got.equals(brute(n, has, s, tg))) throw new AssertionError("random " + t);
        }
    }
}
```
