<!-- solutions-for: 05-alternating-colors -->
### Alternating Colors

#### Solution: [Build] Alternate Red And Blue (Author exercise)
<!-- id: sp-alt-moves -->

**Approach.** Scan the sections in input order and keep each one that leaves `v` and whose paint is not `last`, writing a fresh `{to, paint}` row for it. The oracle decides eligibility with arithmetic instead of comparison: a section flips the paint exactly when its paint plus `last` equals 1, and the two answers are compared as strings on 800 random layouts, together with a check that the input is unchanged. The run also asserts the Java claims of the applicability stage: an `int[]` stored in a `HashSet` is not found by a new array with equal contents, while the packed int `node * 2 + paint` is found, and the returned rows are copies that do not alias the input.

**Complexity.** One pass over m sections gives O(m) time, with at most the out-degree of `v` rows of memory for the result.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class RailMovesSolution {
    static int[][] solve(int[][] edges, int v, int last) {
        List<int[]> out = new ArrayList<>();
        for (int[] e : edges) {
            if (e[0] == v && e[2] != last) out.add(new int[] {e[1], e[2]});
        }
        return out.toArray(new int[0][]);
    }

    // independent oracle: classify every section by its two endpoints' meaning, then filter by index
    static List<String> oracle(int[][] edges, int v, int last) {
        List<String> out = new ArrayList<>();
        for (int i = 0; i < edges.length; i++) {
            boolean leaves = edges[i][0] == v;
            boolean flips = (edges[i][2] + last) == 1;
            if (leaves && flips) out.add(edges[i][1] + ":" + edges[i][2]);
        }
        return out;
    }

    static List<String> show(int[][] r) {
        List<String> s = new ArrayList<>();
        for (int[] p : r) s.add(p[0] + ":" + p[1]);
        return s;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 0}, {0, 2, 1}, {0, 3, 0}, {1, 0, 1}, {0, 0, 1}};
        if (!Arrays.deepEquals(solve(e1, 0, 0), new int[][] {{2, 1}, {0, 1}})) throw new AssertionError("example 1a");
        if (!Arrays.deepEquals(solve(e1, 0, 1), new int[][] {{1, 0}, {3, 0}})) throw new AssertionError("example 1b");
        int[][] e2 = {{2, 2, 0}, {2, 2, 1}, {2, 4, 0}, {3, 2, 1}};
        if (!Arrays.deepEquals(solve(e2, 2, 1), new int[][] {{2, 0}, {4, 0}})) throw new AssertionError("example 2");
        if (solve(e2, 4, 0).length != 0) throw new AssertionError("dead end gives empty result");
        // Java claim: an int[] used as a set element matches by identity, so equal contents are not found
        Set<int[]> byRef = new HashSet<>();
        byRef.add(new int[] {2, 1});
        if (byRef.contains(new int[] {2, 1})) throw new AssertionError("arrays hash by identity");
        // the encoded int does match, which is why states are packed as node * 2 + color
        Set<Integer> packed = new HashSet<>();
        packed.add(2 * 2 + 1);
        if (!packed.contains(2 * 2 + 1)) throw new AssertionError("packed state found");
        // returned rows are fresh copies: editing them must not touch the input
        int[][] copy = {{0, 1, 0}};
        int[][] got = solve(copy, 0, 1);
        got[0][0] = 99;
        if (copy[0][1] != 1) throw new AssertionError("input untouched");
        Random rnd = new Random(24501);
        for (int t = 0; t < 800; t++) {
            int n = 1 + rnd.nextInt(5), m = rnd.nextInt(9);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[][] snapshot = Arrays.stream(edges).map(int[]::clone).toArray(int[][]::new);
            int v = rnd.nextInt(n), last = rnd.nextInt(2);
            if (!show(solve(edges, v, last)).equals(oracle(edges, v, last))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(edges, snapshot)) throw new AssertionError("mutated");
        }
        System.out.println("OK");
    }
}
```

#### Solution: [Vary] Two Start Modes (Author exercise)
<!-- id: sp-alt-start-modes -->

**Approach.** Queue states encoded as `yard * 2 + paint`. A forced first paint c is modelled by queuing only the yard-0 state whose last paint is the other color, so the first section must be c; when `first` is -1 both yard-0 states are queued at distance zero. The yard answer is the smaller of its two state distances, with -1 only when neither was reached. The oracle is a layered reachability table, one layer per section count up to 2n + 1, run for all three values of `first` on 1200 random layouts. The false friend is built concretely: on the layout `{{0,1,0},{0,2,0},{2,1,1},{1,3,0}}` yard 3 is truly 3 sections away, but a search with one visited flag per yard marks yard 1 on its red arrival and reports -1. The run also checks that a new `int[]` holds zeros.

**Complexity.** Each state is queued once and each section is looked at once per paint of its start yard, so O(n + m) time, and O(n + m) space for the adjacency lists, the 2n distances and the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class StartModesSolution {
    // state id = node * 2 + color of the last section run; color 0 red, 1 blue
    static int[] solve(int n, int[][] edges, int first) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] e : edges) out.get(e[0]).add(new int[] {e[1], e[2]});
        int[] state = new int[2 * n];
        Arrays.fill(state, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int prev = 0; prev < 2; prev++) {
            if (first != -1 && prev == first) continue; // forced first color c means "previous" was the other one
            state[prev] = 0;
            queue.add(prev);
        }
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int[] e : out.get(cur / 2)) {
                if (e[1] == cur % 2) continue;
                int next = e[0] * 2 + e[1];
                if (state[next] >= 0) continue;
                state[next] = state[cur] + 1;
                queue.add(next);
            }
        }
        int[] best = new int[n];
        for (int v = 0; v < n; v++) {
            int a = state[2 * v], b = state[2 * v + 1];
            best[v] = a < 0 ? b : b < 0 ? a : Math.min(a, b);
        }
        return best;
    }

    // the tempting shortcut: one visited flag per node
    static int[] nodeOnly(int n, int[][] edges) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        dist[0] = 0;
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        queue.add(new int[] {0, -1});
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            for (int[] e : edges) {
                if (e[0] != cur[0] || e[2] == cur[1] || dist[e[1]] >= 0) continue;
                dist[e[1]] = dist[cur[0]] + 1;
                queue.add(new int[] {e[1], e[2]});
            }
        }
        return dist;
    }

    // layered oracle: which (node, color) is reachable by exactly k sections
    static int[] oracle(int n, int[][] edges, int first) {
        int[] best = new int[n];
        Arrays.fill(best, -1);
        best[0] = 0;
        boolean[][] now = new boolean[n][2];
        for (int[] e : edges) {
            if (e[0] == 0 && (first == -1 || first == e[2])) now[e[1]][e[2]] = true;
        }
        for (int k = 1; k <= 2 * n + 1; k++) {
            boolean[][] nxt = new boolean[n][2];
            for (int v = 0; v < n; v++) {
                for (int c = 0; c < 2; c++) {
                    if (!now[v][c]) continue;
                    if (best[v] < 0) best[v] = k;
                    for (int[] e : edges) if (e[0] == v && e[2] != c) nxt[e[1]][e[2]] = true;
                }
            }
            now = nxt;
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] g = {{0, 1, 0}, {1, 2, 0}, {0, 3, 1}, {3, 2, 1}, {2, 4, 1}, {4, 1, 0}, {1, 5, 1}};
        if (!Arrays.equals(solve(6, g, -1), new int[] {0, 1, -1, 1, -1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(6, g, 1), new int[] {0, -1, -1, 1, -1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(6, g, 0), new int[] {0, 1, -1, -1, -1, 2})) throw new AssertionError("red first");
        // false friend: one visited flag per node loses the blue arrival at node 1
        int[][] trap = {{0, 1, 0}, {0, 2, 0}, {2, 1, 1}, {1, 3, 0}};
        if (solve(4, trap, -1)[3] != 3) throw new AssertionError("true distance is 3");
        if (nodeOnly(4, trap)[3] != -1) throw new AssertionError("node-only flag must miss node 3");
        // Java claim: a fresh int array holds zeros, which would read as distance 0 without the fill
        int[] fresh = new int[3];
        if (fresh[1] != 0) throw new AssertionError("default is zero");
        Random rnd = new Random(24502);
        for (int t = 0; t < 1200; t++) {
            int n = 1 + rnd.nextInt(6), m = rnd.nextInt(12);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[][] snap = Arrays.stream(edges).map(int[]::clone).toArray(int[][]::new);
            for (int first = -1; first <= 1; first++) {
                if (!Arrays.equals(solve(n, edges, first), oracle(n, edges, first))) throw new AssertionError("random " + t + " mode " + first);
            }
            if (!Arrays.deepEquals(edges, snap)) throw new AssertionError("mutated");
        }
        System.out.println("OK");
    }
}
```

#### Solution: [Boundary] Self-Loop And Parallel Colors (Author exercise)
<!-- id: sp-alt-loops-parallel -->

**Approach.** Give the start yard no distance of its own: the queue is filled by the sections that leave `s`, each arriving state getting distance 1, which makes a route from `s` back to `s` count only when it uses at least one section. After that, plain BFS over encoded states handles loops and parallel sections automatically, since each is just another arc into a state that is skipped when already known. The oracle is a depth-first enumeration of every alternating route up to 2n sections on layouts of at most four yards, compared on 1500 random cases. The false friend is a deduplication that keeps one section per pair of yards; on `{{0,1,0},{0,1,1},{1,2,0}}` it deletes the blue section and turns a true answer of 2 into -1, and the run asserts both values.

**Complexity.** Time is O(n + m) for m sections, because each state is expanded once and scans its yard's sections, and space is O(n + m); the brute-force oracle is exponential and is used only on tiny layouts.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class LoopsParallelSolution {
    // fewest sections of a non-empty alternating walk from s to t; the start is NOT a state of distance zero
    static int solve(int n, int[][] edges, int s, int t) {
        int[] dist = new int[2 * n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int[] e : edges) {
            int id = e[1] * 2 + e[2];
            if (e[0] == s && dist[id] < 0) {
                dist[id] = 1;
                queue.add(id);
            }
        }
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int[] e : edges) {
                if (e[0] != cur / 2 || e[2] == cur % 2) continue;
                int id = e[1] * 2 + e[2];
                if (dist[id] >= 0) continue;
                dist[id] = dist[cur] + 1;
                queue.add(id);
            }
        }
        int a = dist[2 * t], b = dist[2 * t + 1];
        return a < 0 ? b : b < 0 ? a : Math.min(a, b);
    }

    // brute force: depth-first over every alternating walk up to 2n sections
    static int best;

    static void walk(int[][] edges, int at, int last, int used, int t, int limit) {
        if (used > 0 && at == t && (best < 0 || used < best)) best = used;
        if (used == limit) return;
        for (int[] e : edges) {
            if (e[0] == at && e[2] != last) walk(edges, e[1], e[2], used + 1, t, limit);
        }
    }

    static int oracle(int n, int[][] edges, int s, int t) {
        best = -1;
        walk(edges, s, -1, 0, t, 2 * n);
        return best;
    }

    // wrong shortcut: treat a parallel edge of the other color as a duplicate and drop it
    static int dedupParallel(int n, int[][] edges, int s, int t) {
        boolean[][] seen = new boolean[n][n];
        int[][] kept = new int[edges.length][];
        int k = 0;
        for (int[] e : edges) {
            if (seen[e[0]][e[1]]) continue;
            seen[e[0]][e[1]] = true;
            kept[k++] = e;
        }
        return solve(n, Arrays.copyOf(kept, k), s, t);
    }

    public static void main(String[] args) {
        int[][] g = {{0, 0, 0}, {0, 1, 0}, {0, 1, 1}, {1, 1, 1}, {1, 2, 0}, {2, 0, 1}};
        if (solve(3, g, 2, 2) != 4) throw new AssertionError("example 1");
        if (solve(3, g, 0, 0) != 1) throw new AssertionError("example 2");
        if (solve(3, g, 1, 1) != 1) throw new AssertionError("blue self-loop");
        // a lone loop is a closed route of one section
        if (solve(1, new int[][] {{0, 0, 0}}, 0, 0) != 1) throw new AssertionError("single loop");
        // false friend: dropping the parallel blue edge hides the only alternating route
        int[][] twin = {{0, 1, 0}, {0, 1, 1}, {1, 2, 0}};
        if (solve(3, twin, 0, 2) != 2) throw new AssertionError("true distance is 2");
        if (dedupParallel(3, twin, 0, 2) != -1) throw new AssertionError("dedup must lose the route");
        Random rnd = new Random(24503);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(4), m = rnd.nextInt(8);
            int[][] edges = new int[m][];
            for (int i = 0; i < m; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2)};
            int[][] snap = Arrays.stream(edges).map(int[]::clone).toArray(int[][]::new);
            int s = rnd.nextInt(n), tg = rnd.nextInt(n);
            if (solve(n, edges, s, tg) != oracle(n, edges, s, tg)) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(edges, snap)) throw new AssertionError("mutated");
        }
        System.out.println("OK");
    }
}
```

#### Solution: [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alt-color-pairs -->

**Approach.** Build one adjacency list that stores the arriving state `far * 2 + paint` for each section, put the states reached by the sections out of yard 0 in the queue at distance 1, and run BFS in which a state with paint p expands only the arcs whose paint is not p. The result table is filled with -1 for every row first. Two wrong shortcuts are built and asserted: seeding both states of yard 0 at distance zero reports 0 for yard 0 while the true value is -1 on the first example, and a single visited flag per yard misses yard 3 on the layout with red `{0,1},{0,2},{1,3}` and blue `{2,1}`, where the truth is `[[-1,-1],[1,2],[1,-1],[3,-1]]`. The oracle is a layered reachability table, one layer per section count, checked on 1500 random layouts, and the run confirms that the input arrays are unchanged and that a fresh `int[n][2]` starts at zeros.

**Complexity.** The search expands each of the 2n states once and scans the sections of its yard, which is O(n + m) time with m the total number of sections, and the adjacency lists, table and queue occupy O(n + m) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class ColorPairsSolution {
    static int[][] solve(int n, int[][] redEdges, int[][] blueEdges) {
        List<List<Integer>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] e : redEdges) out.get(e[0]).add(e[1] * 2);         // arriving by red
        for (int[] e : blueEdges) out.get(e[0]).add(e[1] * 2 + 1);    // arriving by blue
        int[][] answer = new int[n][2];
        for (int[] row : answer) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        for (int id : out.get(0)) {
            if (answer[id / 2][id % 2] < 0) {
                answer[id / 2][id % 2] = 1;
                queue.add(id);
            }
        }
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            int dist = answer[cur / 2][cur % 2];
            for (int id : out.get(cur / 2)) {
                if (id % 2 == cur % 2 || answer[id / 2][id % 2] >= 0) continue;
                answer[id / 2][id % 2] = dist + 1;
                queue.add(id);
            }
        }
        return answer;
    }

    // wrong shortcut 1: seed both colors at node 0 with distance zero and read the table directly
    static int[][] seededAtZero(int n, int[][] redEdges, int[][] blueEdges) {
        int[][] answer = new int[n][2];
        for (int[] row : answer) Arrays.fill(row, -1);
        answer[0][0] = 0;
        answer[0][1] = 0;
        ArrayDeque<Integer> queue = new ArrayDeque<>(List.of(0, 1));
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            int v = cur / 2, c = cur % 2;
            for (int col = 0; col < 2; col++) {
                if (col == c) continue;
                for (int[] e : col == 0 ? redEdges : blueEdges) {
                    if (e[0] == v && answer[e[1]][col] < 0) {
                        answer[e[1]][col] = answer[v][c] + 1;
                        queue.add(e[1] * 2 + col);
                    }
                }
            }
        }
        return answer;
    }

    // wrong shortcut 2: one visited flag per node
    static int[][] nodeOnly(int n, int[][] redEdges, int[][] blueEdges) {
        int[][] answer = new int[n][2];
        for (int[] row : answer) Arrays.fill(row, -1);
        boolean[] seen = new boolean[n];
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        queue.add(new int[] {0, -1, 0});
        seen[0] = true;
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            for (int col = 0; col < 2; col++) {
                if (col == cur[1]) continue;
                for (int[] e : col == 0 ? redEdges : blueEdges) {
                    if (e[0] != cur[0] || seen[e[1]]) continue;
                    seen[e[1]] = true;
                    answer[e[1]][col] = cur[2] + 1;
                    queue.add(new int[] {e[1], col, cur[2] + 1});
                }
            }
        }
        return answer;
    }

    // oracle: layered reachability, one layer per section count
    static int[][] oracle(int n, int[][] redEdges, int[][] blueEdges) {
        int[][] answer = new int[n][2];
        for (int[] row : answer) Arrays.fill(row, -1);
        boolean[][] now = new boolean[n][2];
        for (int[] e : redEdges) if (e[0] == 0) now[e[1]][0] = true;
        for (int[] e : blueEdges) if (e[0] == 0) now[e[1]][1] = true;
        for (int k = 1; k <= 2 * n + 2; k++) {
            boolean[][] nxt = new boolean[n][2];
            for (int v = 0; v < n; v++) {
                for (int c = 0; c < 2; c++) {
                    if (!now[v][c]) continue;
                    if (answer[v][c] < 0) answer[v][c] = k;
                    if (c == 1) for (int[] e : redEdges) if (e[0] == v) nxt[e[1]][0] = true;
                    if (c == 0) for (int[] e : blueEdges) if (e[0] == v) nxt[e[1]][1] = true;
                }
            }
            now = nxt;
        }
        return answer;
    }

    public static void main(String[] args) {
        int[][] r1 = {{0, 1}, {2, 3}, {3, 3}}, b1 = {{1, 2}, {3, 4}, {2, 0}};
        if (!Arrays.deepEquals(solve(5, r1, b1), new int[][] {{-1, -1}, {1, -1}, {-1, 2}, {3, -1}, {-1, 4}}))
            throw new AssertionError("example 1");
        int[][] r2 = {{0, 1}, {1, 2}, {3, 4}, {2, 3}}, b2 = {{0, 1}, {2, 0}, {4, 5}, {3, 3}};
        if (!Arrays.deepEquals(solve(6, r2, b2), new int[][] {{-1, 3}, {1, 1}, {2, -1}, {-1, -1}, {-1, -1}, {-1, -1}}))
            throw new AssertionError("example 2");
        // false friend 1: seeding node 0 at distance zero reports a walk that uses no section
        if (seededAtZero(5, r1, b1)[0][0] != 0 || solve(5, r1, b1)[0][0] != -1) throw new AssertionError("zero seed claim");
        // false friend 2: one flag per node loses the blue arrival at node 1 (true [3, 1] needs red first)
        int[][] tr = {{0, 1}, {0, 2}, {1, 3}}, tb = {{2, 1}};
        if (!Arrays.deepEquals(solve(4, tr, tb), new int[][] {{-1, -1}, {1, 2}, {1, -1}, {3, -1}}))
            throw new AssertionError("trap truth");
        if (nodeOnly(4, tr, tb)[3][0] != -1) throw new AssertionError("node-only must miss node 3");
        // Java claim: new int[n][2] starts as zeros, so -1 must be written into every row
        int[][] fresh = new int[2][2];
        if (fresh[1][1] != 0) throw new AssertionError("rows start at zero");
        Random rnd = new Random(24504);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(6);
            int mr = rnd.nextInt(8), mb = rnd.nextInt(8);
            int[][] red = new int[mr][], blue = new int[mb][];
            for (int i = 0; i < mr; i++) red[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            for (int i = 0; i < mb; i++) blue[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[][] sr = Arrays.stream(red).map(int[]::clone).toArray(int[][]::new);
            int[][] sb = Arrays.stream(blue).map(int[]::clone).toArray(int[][]::new);
            if (!Arrays.deepEquals(solve(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(red, sr) || !Arrays.deepEquals(blue, sb)) throw new AssertionError("mutated");
        }
        System.out.println("OK");
    }
}
```
