<!-- solutions-for: 24-shortest-paths-and-graph-state-modeling -->
### Solutions For Alternate Edge Colors

#### Solution: [Build] Alternate Red And Blue (Author exercise)
<!-- id: sp-alternate-red-blue -->

**Approach.**
The method keeps one adjacency list for each color and a distance table indexed by node and last color. A pair `(v, c)` means that a walk ends at `v` with color `c`. The red-first rule needs one queued pair, `(0, 1)`, with distance 0. That pair permits red edges only, because the pair of color `c` permits color `1 - c`. Each removed pair follows the edges of the other color and queues every target pair that has no distance yet.

The invariant is that a pair receives its distance on its first arrival, and the queue order makes that distance the smallest. Each transition costs exactly one edge, which makes breadth-first order the shortest order. The answer of a node is the smaller defined entry of its two pairs. Node 0 gets 0 from the empty walk, and the pair `(0, 1)` is the stored source of that value.

**Complexity.**
- **Time** is O(V + E), because each pair enters the queue once and each edge is read only from the pair of the other color.
- **Space** is O(V + E) for the adjacency lists, the table of `2n` entries and the queue.

```java run
import java.util.*;

public final class AlternateRedBlue {
    /**
     * Returns the fewest edges of an alternating walk from node 0 with a red first edge, per node.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a pair gets its distance on first arrival, in nondecreasing distance order.
     */
    static int[] redFirst(int n, int[][] red, int[][] blue) {
        // Adjacency lists for both colors in one array: index color * n + node.
        List<List<Integer>> next = new ArrayList<>();
        for (int i = 0; i < 2 * n; i++) next.add(new ArrayList<>());
        for (int[] e : red) next.get(e[0]).add(e[1]);
        for (int[] e : blue) next.get(n + e[0]).add(e[1]);
        // Every pair starts unreached.
        int[][] dist = new int[n][2];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Only the pair "last color blue" is queued, so the first edge must be red.
        dist[0][1] = 0;
        queue.add(1);
        // Each pair is queued once, which bounds the loop by 2n iterations.
        while (!queue.isEmpty()) {
            int pair = queue.poll();
            int v = pair / 2, c = pair % 2;
            int other = 1 - c;
            // Only edges of the other color leave this pair; each edge is read once overall.
            for (int w : next.get(other * n + v)) {
                // A pair with a distance is final, so a later arrival is dropped.
                if (dist[w][other] != -1) continue;
                dist[w][other] = dist[v][c] + 1;
                queue.add(2 * w + other);
            }
        }
        // Reduce each row to the smaller defined entry.
        int[] answer = new int[n];
        for (int v = 0; v < n; v++) {
            int a = dist[v][0], b = dist[v][1];
            answer[v] = a == -1 ? b : b == -1 ? a : Math.min(a, b);
        }
        return answer;
    }

    /** Oracle: sets of reachable pairs after exactly k edges, scanned directly from the edge lists. */
    static int[] oracle(int n, int[][] red, int[][] blue) {
        int[] best = new int[n];
        Arrays.fill(best, -1);
        best[0] = 0;
        // The previous color is blue at the start, so the next edge must be red.
        Set<Integer> layer = new HashSet<>();
        layer.add(1);
        for (int k = 1; k <= 2 * n + 2 && !layer.isEmpty(); k++) {
            Set<Integer> after = new HashSet<>();
            for (int pair : layer) {
                int v = pair / 2, c = pair % 2;
                int[][] list = c == 0 ? blue : red;
                for (int[] e : list) if (e[0] == v) after.add(2 * e[1] + (c == 0 ? 1 : 0));
            }
            for (int pair : after) if (best[pair / 2] == -1) best[pair / 2] = k;
            layer = after;
        }
        return best;
    }

    static int[][] randomEdges(Random rnd, int n) {
        int m = rnd.nextInt(10);
        int[][] list = new int[m][];
        for (int i = 0; i < m; i++) list[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
        return list;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(redFirst(3, new int[][] {{0, 1}, {1, 2}}, new int[][] {{0, 1}}), new int[] {0, 1, -1})) throw new AssertionError("ex1");
        if (!Arrays.equals(redFirst(4, new int[][] {{0, 1}, {2, 3}}, new int[][] {{1, 2}, {1, 1}}), new int[] {0, 1, 2, 3})) throw new AssertionError("ex2");
        // A blue edge out of node 0 is never a legal first edge.
        if (!Arrays.equals(redFirst(2, new int[0][], new int[][] {{0, 1}}), new int[] {0, -1})) throw new AssertionError("blue first");
        // Java fact: Arrays.fill with one row object would alias every row, so the loop fill keeps rows independent.
        int[][] shared = new int[2][];
        Arrays.fill(shared, new int[] {-1, -1});
        shared[0][0] = 7;
        if (shared[1][0] != 7) throw new AssertionError("aliasing");
        // Random graphs with repeats and self loops against the layered oracle.
        Random rnd = new Random(2451);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] red = randomEdges(rnd, n), blue = randomEdges(rnd, n);
            if (!Arrays.equals(redFirst(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Two Start Modes (Author exercise)
<!-- id: sp-two-start-modes -->

**Approach.**
The method uses the same pair search as the previous exercise and changes two things. It queues both pairs of node 0 with distance 0, so the first edge may have either color. It also returns the whole table and leaves each row unreduced. Entry `[v][c]` is read directly from the distance of the pair `(v, c)`.

The invariant is that the table entry of a pair is the fewest edges of an alternating walk that ends at that node with that color. The pair `(0, 0)` permits blue edges and the pair `(0, 1)` permits red edges, so together they permit every first edge. Both entries of node 0 are 0 because the empty walk has no last color and counts for both. A later walk that returns to node 0 cannot lower either entry, since the entries are already 0.

**Complexity.**
- **Time** is O(V + E), because the queue holds each of the `2n` pairs at most once and each edge is read from one pair.
- **Space** is O(V + E) for the adjacency lists, the table and the queue.

```java run
import java.util.*;

public final class TwoStartModes {
    /**
     * Returns the table of fewest edges by node and last color, with both start pairs at 0.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: dist[v][c] is final the first time the pair is set.
     */
    static int[][] table(int n, int[][] red, int[][] blue) {
        // One list per color and node, stored at index color * n + node.
        List<List<Integer>> next = new ArrayList<>();
        for (int i = 0; i < 2 * n; i++) next.add(new ArrayList<>());
        for (int[] e : red) next.get(e[0]).add(e[1]);
        for (int[] e : blue) next.get(n + e[0]).add(e[1]);
        int[][] dist = new int[n][2];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // Both possible previous colors start at distance 0, so both first-edge colors are allowed.
        dist[0][0] = 0;
        dist[0][1] = 0;
        queue.add(0);
        queue.add(1);
        // Each pair enters the queue once, which bounds the loop at 2n iterations.
        while (!queue.isEmpty()) {
            int pair = queue.poll();
            int v = pair / 2, c = pair % 2;
            int other = 1 - c;
            // The pair of color c permits only edges of the other color.
            for (int w : next.get(other * n + v)) {
                if (dist[w][other] != -1) continue;
                dist[w][other] = dist[v][c] + 1;
                queue.add(2 * w + other);
            }
        }
        return dist;
    }

    /** Oracle: pairs reachable after exactly k edges, with both colors allowed at the empty walk. */
    static int[][] oracle(int n, int[][] red, int[][] blue) {
        int[][] best = new int[n][2];
        for (int[] row : best) Arrays.fill(row, -1);
        best[0][0] = 0;
        best[0][1] = 0;
        Set<Integer> layer = new HashSet<>(List.of(0, 1));
        for (int k = 1; k <= 2 * n + 2 && !layer.isEmpty(); k++) {
            Set<Integer> after = new HashSet<>();
            for (int pair : layer) {
                int v = pair / 2, c = pair % 2;
                // Last color c allows color 1 - c, which is red when c is 1.
                int[][] list = c == 1 ? red : blue;
                for (int[] e : list) if (e[0] == v) after.add(2 * e[1] + (1 - c));
            }
            for (int pair : after) if (best[pair / 2][pair % 2] == -1) best[pair / 2][pair % 2] = k;
            layer = after;
        }
        return best;
    }

    static int[][] randomEdges(Random rnd, int n) {
        int m = rnd.nextInt(10);
        int[][] list = new int[m][];
        for (int i = 0; i < m; i++) list[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
        return list;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.deepEquals(table(3, new int[][] {{0, 1}, {1, 2}}, new int[][] {{0, 1}}), new int[][] {{0, 0}, {1, 1}, {2, -1}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(table(4, new int[][] {{0, 1}, {2, 3}}, new int[][] {{1, 2}, {1, 1}}), new int[][] {{0, 0}, {1, 2}, {-1, 2}, {3, -1}})) throw new AssertionError("ex2");
        // A single node keeps both entries at 0.
        if (!Arrays.deepEquals(table(1, new int[][] {{0, 0}}, new int[0][]), new int[][] {{0, 0}})) throw new AssertionError("single node");
        // Random graphs with repeats and self loops against the layered oracle.
        Random rnd = new Random(2452);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] red = randomEdges(rnd, n), blue = randomEdges(rnd, n);
            if (!Arrays.deepEquals(table(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Self-Loop And Parallel Colors (Author exercise)
<!-- id: sp-self-loop-parallel -->

**Approach.**
The empty walk is not allowed here, so no pair may start with distance 0. The method scans the edges that leave node 0 and queues the target pair of each one with distance 1. A red edge to `w` queues `(w, 0)` and a blue edge queues `(w, 1)`. Parallel edges of both colors to one target queue two different pairs, and repeated edges of one color queue the pair once. The usual loop then expands each pair along edges of the other color.

The invariant is that a pair gets the length of the shortest walk of one edge or more that ends in it. A self loop is an ordinary transition from a pair to a pair of the other color, so it needs no case. A walk that returns to node 0 sets a pair of node 0 for the first time, and that pair is not 0. The answer of node 0 is -1 when no such return exists.

**Complexity.**
- **Time** is O(V + E), because the seeding scans each edge once and the search reads each edge from one pair.
- **Space** is O(V + E) for the adjacency lists, the table and the queue.

```java run
import java.util.*;

public final class SelfLoopParallel {
    /**
     * Returns the fewest edges, at least one, of an alternating walk from node 0 to each node.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: a pair holds the length of the shortest nonempty walk that ends there.
     */
    static int[] nonempty(int n, int[][] red, int[][] blue) {
        List<List<Integer>> next = new ArrayList<>();
        for (int i = 0; i < 2 * n; i++) next.add(new ArrayList<>());
        for (int[] e : red) next.get(e[0]).add(e[1]);
        for (int[] e : blue) next.get(n + e[0]).add(e[1]);
        int[][] dist = new int[n][2];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // First edges leave node 0 and arrive at distance 1; the two colors fill different pairs.
        for (int color = 0; color < 2; color++) {
            for (int w : next.get(color * n)) {
                if (dist[w][color] != -1) continue;
                dist[w][color] = 1;
                queue.add(2 * w + color);
            }
        }
        // Each pair enters the queue once.
        while (!queue.isEmpty()) {
            int pair = queue.poll();
            int v = pair / 2, c = pair % 2;
            int other = 1 - c;
            // A self loop is a normal edge here, from this pair to a pair of the other color.
            for (int w : next.get(other * n + v)) {
                if (dist[w][other] != -1) continue;
                dist[w][other] = dist[v][c] + 1;
                queue.add(2 * w + other);
            }
        }
        int[] answer = new int[n];
        for (int v = 0; v < n; v++) {
            int a = dist[v][0], b = dist[v][1];
            answer[v] = a == -1 ? b : b == -1 ? a : Math.min(a, b);
        }
        return answer;
    }

    /** Oracle: walks of exactly k edges, k from 1, kept as sets of pairs read from the edge lists. */
    static int[] oracle(int n, int[][] red, int[][] blue) {
        int[] best = new int[n];
        Arrays.fill(best, -1);
        Set<Integer> layer = new HashSet<>();
        for (int[] e : red) if (e[0] == 0) layer.add(2 * e[1]);
        for (int[] e : blue) if (e[0] == 0) layer.add(2 * e[1] + 1);
        for (int k = 1; k <= 2 * n + 2 && !layer.isEmpty(); k++) {
            for (int pair : layer) if (best[pair / 2] == -1) best[pair / 2] = k;
            Set<Integer> after = new HashSet<>();
            for (int pair : layer) {
                int v = pair / 2, c = pair % 2;
                int[][] list = c == 0 ? blue : red;
                for (int[] e : list) if (e[0] == v) after.add(2 * e[1] + (1 - c));
            }
            layer = after;
        }
        return best;
    }

    static int[][] randomEdges(Random rnd, int n) {
        int m = rnd.nextInt(10);
        int[][] list = new int[m][];
        for (int i = 0; i < m; i++) list[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
        return list;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(nonempty(3, new int[][] {{0, 0}, {0, 1}, {1, 2}}, new int[][] {{0, 1}, {1, 0}}), new int[] {1, 1, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(nonempty(2, new int[][] {{0, 1}}, new int[][] {{1, 1}}), new int[] {-1, 1})) throw new AssertionError("ex2");
        // Parallel edges of one color count once, and a lone red self loop does not repeat itself.
        if (!Arrays.equals(nonempty(1, new int[][] {{0, 0}, {0, 0}}, new int[0][]), new int[] {1})) throw new AssertionError("repeat self loop");
        // Parallel edges of both colors reach the target at distance 1 in two independent pairs.
        if (!Arrays.equals(nonempty(3, new int[][] {{0, 1}, {1, 2}}, new int[][] {{0, 1}}), new int[] {-1, 1, 2})) throw new AssertionError("parallel colors");
        // Random graphs with repeats and self loops against the layered oracle.
        Random rnd = new Random(2453);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] red = randomEdges(rnd, n), blue = randomEdges(rnd, n);
            if (!Arrays.equals(nonempty(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors-lc1129 -->

**Approach.**
The statement restricts each edge by the color of the previous edge, so the search runs over pairs of node and last color. The method queues `(0, 0)` and `(0, 1)` with distance 0, because the empty walk allows either first edge. A removed pair follows only edges of the color that differs from its own and queues each unreached target pair with the distance plus one. After the queue ends, each answer is the smaller defined entry of the row of its node.

The invariant is that the first arrival at a pair is its shortest, because every transition costs one edge and the queue keeps nondecreasing order. The check for a prior distance is on the pair and not on the node, so an arrival with the other last color is never dropped. A node that has no defined entry gets -1. Node 0 stays 0 even when a longer walk returns to it.

**Complexity.**
- **Time** is O(V + E), because each pair enters the queue once and one pair reads each edge.
- **Space** is O(V + E) for the adjacency lists, the table of `2n` entries and the queue.

```java run
import java.util.*;

public final class AlternatingColors {
    /**
     * Returns the fewest edges of an alternating walk from node 0 to each node, or -1.
     * Time: O(V + E). Space: O(V + E).
     * Invariant: the first distance set on a pair is final.
     */
    static int[] shortestAlternating(int n, int[][] redEdges, int[][] blueEdges) {
        // Targets of each color and node, stored at index color * n + node.
        List<List<Integer>> next = new ArrayList<>();
        for (int i = 0; i < 2 * n; i++) next.add(new ArrayList<>());
        for (int[] e : redEdges) next.get(e[0]).add(e[1]);
        for (int[] e : blueEdges) next.get(n + e[0]).add(e[1]);
        int[][] dist = new int[n][2];
        for (int[] row : dist) Arrays.fill(row, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The empty walk allows either first color, so both pairs of node 0 start at 0.
        dist[0][0] = 0;
        dist[0][1] = 0;
        queue.add(0);
        queue.add(1);
        // The queue holds each of the 2n pairs at most once.
        while (!queue.isEmpty()) {
            int pair = queue.poll();
            int v = pair / 2, c = pair % 2;
            int other = 1 - c;
            // Edges of the other color only; the check is on the pair, not on the node.
            for (int w : next.get(other * n + v)) {
                if (dist[w][other] != -1) continue;
                dist[w][other] = dist[v][c] + 1;
                queue.add(2 * w + other);
            }
        }
        // Each node answers with the smaller defined entry of its row.
        int[] answer = new int[n];
        for (int v = 0; v < n; v++) {
            int a = dist[v][0], b = dist[v][1];
            answer[v] = a == -1 ? b : b == -1 ? a : Math.min(a, b);
        }
        return answer;
    }

    /** Oracle: explicit walks, extended edge by edge up to 2n + 2 edges, keeping the shortest per node. */
    static int[] oracle(int n, int[][] red, int[][] blue) {
        int[] best = new int[n];
        Arrays.fill(best, -1);
        best[0] = 0;
        // A walk is {end node, last color}; last color 2 marks the empty walk.
        List<int[]> walks = new ArrayList<>();
        walks.add(new int[] {0, 2});
        for (int k = 1; k <= 2 * n + 2; k++) {
            Set<Long> seen = new HashSet<>();
            List<int[]> grown = new ArrayList<>();
            for (int[] w : walks) {
                for (int color = 0; color < 2; color++) {
                    if (color == w[1]) continue;
                    for (int[] e : color == 0 ? red : blue) {
                        if (e[0] != w[0]) continue;
                        if (seen.add(e[1] * 3L + color)) grown.add(new int[] {e[1], color});
                    }
                }
            }
            for (int[] w : grown) if (best[w[0]] == -1) best[w[0]] = k;
            walks = grown;
        }
        return best;
    }

    static int[][] randomEdges(Random rnd, int n) {
        int m = rnd.nextInt(10);
        int[][] list = new int[m][];
        for (int i = 0; i < m; i++) list[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
        return list;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(shortestAlternating(3, new int[][] {{0, 1}, {0, 2}}, new int[][] {{1, 0}}), new int[] {0, 1, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(shortestAlternating(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}}, new int[][] {{1, 2}, {2, 3}, {3, 1}, {1, 4}}), new int[] {0, 1, 2, 3, 2})) throw new AssertionError("ex2");
        // The input that defeats a visited array indexed by node alone.
        if (!Arrays.equals(shortestAlternating(3, new int[][] {{0, 1}, {1, 2}}, new int[][] {{0, 1}}), new int[] {0, 1, 2})) throw new AssertionError("two arrivals");
        // Random graphs with repeats and self loops against the explicit walk oracle.
        Random rnd = new Random(2454);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] red = randomEdges(rnd, n), blue = randomEdges(rnd, n);
            if (!Arrays.equals(shortestAlternating(n, red, blue), oracle(n, red, blue))) throw new AssertionError("random " + t);
        }
    }
}
```
