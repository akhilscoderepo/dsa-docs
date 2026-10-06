<!-- solutions-for: 11-stacks-and-queues -->
### Solutions For Queue Searches

#### Solution: [Build] Process A Supplied Frontier (Author exercise)
<!-- id: sq-supplied-frontier -->

**Approach.**
The method marks `start` and adds it to a queue. Each round removes the front node, records it, and scans its successor list in the given order. A successor that is unmarked gets marked and appended, so a node listed by two earlier nodes enters once, behind the first node that listed it. Marking at the append and not at the removal is the step that prevents duplicates. The invariant is that the queue holds marked, unrecorded nodes, and every recorded node was removed before any node appended after it.

**Complexity.**
- **Time** is O(n + e) for n nodes and e successor entries, because each node is removed once and each list is scanned once.
- **Space** is O(n), because the mark array, the queue and the result each hold at most n nodes.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class FrontierOrder {
    /**
     * Returns the nodes in the order a queue removes them from start.
     * Time: O(n + e), each node is removed once and each list is scanned once.
     * Space: O(n) for marks, queue and result.
     * Invariant: queued nodes are marked and not yet recorded.
     */
    static int[] order(int[][] adj, int start) {
        boolean[] marked = new boolean[adj.length];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        // Mark at insertion so the start can never be inserted again.
        marked[start] = true;
        queue.addLast(start);
        // Each iteration serves the oldest queued node.
        while (!queue.isEmpty()) {
            int cur = queue.removeFirst();
            out.add(cur);
            // Successors keep their listed order behind the nodes already waiting.
            for (int nxt : adj[cur]) {
                if (marked[nxt]) continue;
                marked[nxt] = true;
                queue.addLast(nxt);
            }
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    /** Reference: builds each layer from the previous one without a queue. */
    static int[] oracle(int[][] adj, int start) {
        boolean[] seen = new boolean[adj.length];
        List<Integer> out = new ArrayList<>();
        List<Integer> layer = new ArrayList<>(List.of(start));
        seen[start] = true;
        // Layer k holds the nodes whose fewest steps from start equal k.
        while (!layer.isEmpty()) {
            List<Integer> next = new ArrayList<>();
            for (int u : layer) {
                out.add(u);
                for (int v : adj[u]) if (!seen[v]) { seen[v] = true; next.add(v); }
            }
            layer = next;
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        // Both examples from the exercise text.
        if (!Arrays.equals(order(new int[][] {{2, 1}, {3}, {3, 4}, {1}, {}}, 0), new int[] {0, 2, 1, 3, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[][] {{1}, {2}, {0, 3}, {}}, 2), new int[] {2, 0, 3, 1})) throw new AssertionError("example 2");
        // Random graphs, with self-loops and repeats, match the layer-by-layer reference.
        Random rnd = new Random(21);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] adj = new int[n][];
            for (int i = 0; i < n; i++) {
                adj[i] = new int[rnd.nextInt(4)];
                for (int j = 0; j < adj[i].length; j++) adj[i][j] = rnd.nextInt(n);
            }
            int s = rnd.nextInt(n);
            if (!Arrays.equals(order(adj, s), oracle(adj, s))) throw new AssertionError("random");
        }
    }
}
```

#### Solution: [Vary] Minimum Add-One Or Double Steps (Author exercise)
<!-- id: sq-add-one-or-double -->

**Approach.**
The states are the values from 1 to `bound`, and each state has up to two successors, `v + 1` and `2 * v`. The method stores the move count of each discovered value in an array and uses -1 for undiscovered values. It removes values from a queue, returns the stored count when the target is removed, and appends each in-range undiscovered successor with the count plus one. The queue order serves all values with count `k` before any value with count `k + 1`, so the first removal of the target carries the fewest moves. The invariant is that stored counts never decrease from the front of the queue to the back. The method tests doubling as `v <= bound / 2` so the product `2 * v` cannot overflow.

**Complexity.**
- **Time** is O(bound), because each value enters the queue once and tries two moves.
- **Space** is O(bound), because the count array and the queue hold at most `bound` values.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class AddOrDouble {
    /**
     * Returns the fewest add-one or double moves from start to target within bound, or -1.
     * Time: O(bound), each value is queued once.
     * Space: O(bound) for counts and queue.
     * Invariant: stored counts never decrease from queue front to back.
     */
    static int fewest(int start, int target, int bound) {
        int[] moves = new int[bound + 1];
        // -1 marks a value the search has not discovered yet.
        Arrays.fill(moves, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        moves[start] = 0;
        queue.addLast(start);
        while (!queue.isEmpty()) {
            int v = queue.removeFirst();
            // The stored count of a removed value is final, so the first target removal is the answer.
            if (v == target) return moves[v];
            // Add one stays in range only below the bound.
            if (v + 1 <= bound && moves[v + 1] == -1) { moves[v + 1] = moves[v] + 1; queue.addLast(v + 1); }
            // Doubling is tested as v <= bound / 2 so the product cannot overflow.
            if (v <= bound / 2 && moves[2 * v] == -1) { moves[2 * v] = moves[v] + 1; queue.addLast(2 * v); }
        }
        return -1;
    }

    /** Reference: repeated relaxation of all values until no count improves. */
    static int oracle(int start, int target, int bound) {
        int INF = Integer.MAX_VALUE / 2;
        int[] d = new int[bound + 1];
        Arrays.fill(d, INF);
        d[start] = 0;
        boolean changed = true;
        // Each pass tries every move from every value, so it is quadratic but obviously correct.
        while (changed) {
            changed = false;
            for (int v = 1; v <= bound; v++) {
                if (d[v] == INF) continue;
                if (v + 1 <= bound && d[v] + 1 < d[v + 1]) { d[v + 1] = d[v] + 1; changed = true; }
                if (2 * v <= bound && d[v] + 1 < d[2 * v]) { d[2 * v] = d[v] + 1; changed = true; }
            }
        }
        return d[target] == INF ? -1 : d[target];
    }

    public static void main(String[] args) {
        // Both examples from the exercise text.
        if (fewest(3, 10, 20) != 3) throw new AssertionError("example 1");
        if (fewest(5, 3, 20) != -1) throw new AssertionError("example 2");
        // Doubling near the int limit must not overflow.
        if (fewest(1, 1, 2_000_000_000 / 1000) != 0) throw new AssertionError("large bound");
        // Random bounds, starts and targets match the relaxation reference.
        Random rnd = new Random(22);
        for (int t = 0; t < 4000; t++) {
            int b = 1 + rnd.nextInt(60), s = 1 + rnd.nextInt(b), g = 1 + rnd.nextInt(b);
            if (fewest(s, g, b) != oracle(s, g, b)) throw new AssertionError("random " + s + " " + g + " " + b);
        }
    }
}
```

#### Solution: [Boundary] Start Is Target (Author exercise)
<!-- id: sq-start-is-target -->

**Approach.**
The method marks the start before the loop and adds it to the queue, so the first removal is the start itself. The target test runs right after a removal and before any move is generated, so `start == target` returns 0 with no successor work. Each move that stays within 0 to `bound` and goes to an unmarked value marks that value as it enters the queue. Marking at insertion means each value is inserted at most once, which the harness counts and bounds by `bound + 1`. Marking at removal would allow one value to sit in the queue several times. The invariant is that every value in the queue is marked and was inserted exactly once.

**Complexity.**
- **Time** is O(bound), because each of at most `bound + 1` values is inserted once and tries two moves.
- **Space** is O(bound), because the marks and the queue hold at most `bound + 1` entries.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class StartIsTarget {
    static int inserts;

    /**
     * Returns the fewest subtract-one or add-four moves within 0..bound, or -1.
     * Time: O(bound), each value is inserted once.
     * Space: O(bound) for marks and queue.
     * Invariant: a value is marked exactly when it has been inserted.
     */
    static int fewest(int start, int target, int bound) {
        inserts = 0;
        int[] dist = new int[bound + 1];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // The start is marked before the loop, so no move can insert it again.
        dist[start] = 0;
        queue.addLast(start);
        inserts++;
        while (!queue.isEmpty()) {
            int v = queue.removeFirst();
            // The target test comes before any move, so an equal start returns 0 immediately.
            if (v == target) return dist[v];
            for (int d : new int[] {-1, 4}) {
                int w = v + d;
                if (w < 0 || w > bound || dist[w] != -1) continue;
                // Marking here, at insertion, keeps every value in the queue at most once.
                dist[w] = dist[v] + 1;
                queue.addLast(w);
                inserts++;
            }
        }
        return -1;
    }

    /** Reference: repeated relaxation until no distance improves. */
    static int oracle(int start, int target, int bound) {
        int INF = 1 << 29;
        int[] d = new int[bound + 1];
        Arrays.fill(d, INF);
        d[start] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int v = 0; v <= bound; v++) {
                if (d[v] == INF) continue;
                if (v - 1 >= 0 && d[v] + 1 < d[v - 1]) { d[v - 1] = d[v] + 1; changed = true; }
                if (v + 4 <= bound && d[v] + 1 < d[v + 4]) { d[v + 4] = d[v] + 1; changed = true; }
            }
        }
        return d[target] == INF ? -1 : d[target];
    }

    public static void main(String[] args) {
        // Example 1: the start equals the target and nothing else is inserted.
        if (fewest(7, 7, 10) != 0 || inserts != 1) throw new AssertionError("example 1");
        // Example 2: add four to reach 4, then subtract one to reach 3.
        if (fewest(0, 3, 10) != 2) throw new AssertionError("example 2");
        // A bound of 0 leaves a single value and no legal move.
        if (fewest(0, 0, 0) != 0) throw new AssertionError("bound zero");
        // Random cases match the reference, and no value is inserted twice.
        Random rnd = new Random(23);
        for (int t = 0; t < 4000; t++) {
            int b = rnd.nextInt(40), s = rnd.nextInt(b + 1), g = rnd.nextInt(b + 1);
            if (fewest(s, g, b) != oracle(s, g, b)) throw new AssertionError("random");
            if (inserts > b + 1) throw new AssertionError("duplicate insert");
        }
    }
}
```

#### Solution: [Recognize] Shortest Word Transform From Supplied Neighbors (Author exercise)
<!-- id: sq-word-transform-neighbors -->

**Approach.**
Each word index is a state, and each listed neighbor is a move that costs one step. The method counts the words in the sequence, so the start has count 1 and each move adds 1. A queue serves indices in nondecreasing count, and an array of counts doubles as the mark. The method returns the count when `end` leaves the queue, and returns 0 when the queue empties first. The sequence length equals the number of moves plus one, which is why the count starts at 1. The invariant is that counts never decrease from front to back and each index enters the queue once.

**Complexity.**
- **Time** is O(w + e) for w words and e neighbor entries, because each index is removed once and each list is scanned once.
- **Space** is O(w), because the count array and the queue hold at most w indices.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class WordTransform {
    /**
     * Returns the number of words in the shortest transform sequence, or 0.
     * Time: O(w + e), each index is queued once and each list is scanned once.
     * Space: O(w) for counts and queue.
     * Invariant: counts never decrease from queue front to back.
     */
    static int shortest(int[][] neighbors, int begin, int end) {
        int[] len = new int[neighbors.length];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        // A zero count means undiscovered, and the begin word counts as one word.
        len[begin] = 1;
        queue.addLast(begin);
        while (!queue.isEmpty()) {
            int cur = queue.removeFirst();
            // The first removal of end carries the fewest words.
            if (cur == end) return len[cur];
            for (int nxt : neighbors[cur]) {
                if (len[nxt] != 0) continue;
                // Each new word extends the sequence by one word.
                len[nxt] = len[cur] + 1;
                queue.addLast(nxt);
            }
        }
        return 0;
    }

    /** Reference: Floyd-Warshall distances over the neighbor relation. */
    static int oracle(int[][] neighbors, int begin, int end) {
        int n = neighbors.length, INF = 1 << 20;
        int[][] d = new int[n][n];
        for (int[] row : d) java.util.Arrays.fill(row, INF);
        for (int i = 0; i < n; i++) { d[i][i] = 0; for (int j : neighbors[i]) d[i][j] = 1; }
        // Standard triple loop over intermediate words.
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++)
            if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
        return d[begin][end] >= INF ? 0 : d[begin][end] + 1;
    }

    /** Builds neighbor lists by comparing words letter by letter. */
    static int[][] neighborsOf(String[] w) {
        int[][] nb = new int[w.length][];
        for (int i = 0; i < w.length; i++) {
            java.util.List<Integer> l = new java.util.ArrayList<>();
            for (int j = 0; j < w.length; j++) {
                int diff = 0;
                for (int c = 0; c < w[i].length(); c++) if (w[i].charAt(c) != w[j].charAt(c)) diff++;
                if (diff == 1) l.add(j);
            }
            nb[i] = l.stream().mapToInt(Integer::intValue).toArray();
        }
        return nb;
    }

    public static void main(String[] args) {
        // Example 1 uses the supplied lists and counts four words from cat to dog.
        if (shortest(new int[][] {{1, 5}, {0, 2, 4}, {1, 3}, {2, 4}, {1, 3}, {0}}, 0, 3) != 4) throw new AssertionError("example 1");
        // Example 2 has an isolated word, so the answer is 0.
        if (shortest(new int[][] {{1, 2}, {0, 2}, {0, 1, 3}, {2}, {}}, 0, 4) != 0) throw new AssertionError("example 2");
        // The same index returns 1 word.
        if (shortest(new int[][] {{}}, 0, 0) != 1) throw new AssertionError("same word");
        // Random distinct words over a small alphabet match the all-pairs reference.
        Random rnd = new Random(24);
        for (int t = 0; t < 1500; t++) {
            java.util.LinkedHashSet<String> set = new java.util.LinkedHashSet<>();
            int want = 1 + rnd.nextInt(12);
            while (set.size() < want) {
                StringBuilder sb = new StringBuilder();
                for (int c = 0; c < 3; c++) sb.append((char) ('a' + rnd.nextInt(3)));
                set.add(sb.toString());
            }
            String[] w = set.toArray(new String[0]);
            int[][] nb = neighborsOf(w);
            int b = rnd.nextInt(w.length), e = rnd.nextInt(w.length);
            if (shortest(nb, b, e) != oracle(nb, b, e)) throw new AssertionError("random");
        }
    }
}
```
