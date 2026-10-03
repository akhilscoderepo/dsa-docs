<!-- solutions-for: 04-bfs-queue-state -->
### BFS Queue State

#### Solution: [Build] Process A Supplied Frontier (Author exercise)
<!-- id: sq-supplied-frontier -->

**Approach.** Mark the start, append it, and loop while the queue is nonempty: remove the front state, record it, and for each successor that is not marked, mark it and append it. Marking at append time keeps each state in the queue at most once, so a self-loop or a second incoming edge adds nothing. The assertions compare with a second implementation that stores the queue in an array with head and tail indices, and check that the output has no repeated state, which is what the insertion mark guarantees.

**Complexity.** O(V + E) time and O(V) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class SuppliedFrontier {
    static int[] order(int[][] next, int start) {
        boolean[] marked = new boolean[next.length];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        List<Integer> out = new ArrayList<>();
        marked[start] = true;
        queue.addLast(start);
        while (!queue.isEmpty()) {
            int s = queue.removeFirst();
            out.add(s);
            for (int t : next[s]) if (!marked[t]) { marked[t] = true; queue.addLast(t); }
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }
    static int[] arrayQueue(int[][] next, int start) {
        int n = next.length;
        int[] q = new int[n];
        boolean[] seen = new boolean[n];
        int head = 0, tail = 0;
        q[tail++] = start;
        seen[start] = true;
        while (head < tail) {
            int s = q[head++];
            for (int t : next[s]) if (!seen[t]) { seen[t] = true; q[tail++] = t; }
        }
        return Arrays.copyOf(q, tail);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(order(new int[][] {{1, 2}, {3}, {3}, {}}, 0), new int[] {0, 1, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[][] {{0, 0}}, 0), new int[] {0})) throw new AssertionError("example 2");
        Random rnd = new Random(11401);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] next = new int[n][];
            for (int i = 0; i < n; i++) {
                next[i] = new int[rnd.nextInt(4)];
                for (int j = 0; j < next[i].length; j++) next[i][j] = rnd.nextInt(n);
            }
            int start = rnd.nextInt(n);
            int[] got = order(next, start);
            if (!Arrays.equals(got, arrayQueue(next, start))) throw new AssertionError("differs from the array queue");
            Set<Integer> distinct = new HashSet<>();
            for (int s : got) if (!distinct.add(s)) throw new AssertionError("a state was removed twice");
        }
    }
}
```

#### Solution: [Vary] Minimum Add-One Or Double Steps (Author exercise)
<!-- id: sq-add-one-or-double -->

**Approach.** The states are the integers from 0 to the limit, so the distance array has limit plus one entries. Search from the start, generate `x + 1` and `2 * x`, ignore anything above the limit, and mark on insertion. The target is tested when it is removed, and its distance is returned. A state beyond the limit is never created, so the search is finite. Doubling zero gives zero again, which the mark absorbs. The assertions compare with a dynamic-programming relaxation that repeats improvements of the distance array until nothing changes, on random small cases.

**Complexity.** O(limit) time and O(limit) space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class AddOneOrDouble {
    static int steps(int start, int target, int limit) {
        int[] dist = new int[limit + 1];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> frontier = new ArrayDeque<>();
        dist[start] = 0;
        frontier.addLast(start);
        while (!frontier.isEmpty()) {
            int x = frontier.removeFirst();
            if (x == target) return dist[x];
            int[] successors = {x + 1, x * 2};
            for (int y : successors) {
                if (y <= limit && dist[y] == -1) { dist[y] = dist[x] + 1; frontier.addLast(y); }
            }
        }
        return -1;
    }
    static int relaxation(int start, int target, int limit) {
        int inf = Integer.MAX_VALUE / 2;
        int[] d = new int[limit + 1];
        Arrays.fill(d, inf);
        d[start] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int x = 0; x <= limit; x++) {
                if (d[x] == inf) continue;
                if (x + 1 <= limit && d[x] + 1 < d[x + 1]) { d[x + 1] = d[x] + 1; changed = true; }
                if (x * 2 <= limit && d[x] + 1 < d[x * 2]) { d[x * 2] = d[x] + 1; changed = true; }
            }
        }
        return d[target] == inf ? -1 : d[target];
    }

    public static void main(String[] args) {
        if (steps(3, 10, 100) != 3) throw new AssertionError("example 1");
        if (steps(5, 3, 100) != -1) throw new AssertionError("example 2");
        if (steps(0, 0, 0) != 0) throw new AssertionError("zero doubles to zero");
        if (steps(0, 5, 5) != 4) throw new AssertionError("from zero, adding one and then doubling gives 0, 1, 2, 4, 5");
        Random rnd = new Random(11402);
        for (int t = 0; t < 4000; t++) {
            int limit = rnd.nextInt(60);
            int s = rnd.nextInt(limit + 1), g = rnd.nextInt(limit + 1);
            if (steps(s, g, limit) != relaxation(s, g, limit)) throw new AssertionError("differs on " + s + " " + g + " " + limit);
        }
    }
}
```

#### Solution: [Boundary] Start Is Target (Author exercise)
<!-- id: sq-start-is-target -->

**Approach.** Return `[0, 1]` immediately when the start equals the target, before any successor is generated. Otherwise mark the start, append it, and count one enqueue. Remove states one at a time with their distances; when the target is removed return its distance and the count so far; otherwise append every unmarked successor, marking it and counting it. Because states are marked on insertion, the count never exceeds n. The assertions run the same search with the mark placed at removal and show that it appends more states on the first example, compare with an independent breadth-first computation that uses a list as the queue, and cover the unreachable case with a modulus that shares a factor with both steps.

**Complexity.** O(n) time and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class StartIsTarget {
    static int[] search(int n, int start, int target, boolean markAtInsert) {
        if (start == target) return new int[] {0, 1};
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        boolean[] processed = new boolean[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[start] = 0;
        queue.addLast(start);
        int enqueues = 1;
        while (!queue.isEmpty()) {
            int x = queue.removeFirst();
            if (x == target) return new int[] {dist[x], enqueues};
            if (!markAtInsert) { if (processed[x]) continue; processed[x] = true; }
            int[] successors = {(x + 2) % n, (x + 3) % n};
            for (int y : successors) {
                boolean fresh = markAtInsert ? dist[y] == -1 : !processed[y];
                if (fresh) {
                    if (dist[y] == -1) dist[y] = dist[x] + 1;
                    queue.addLast(y);
                    enqueues++;
                }
            }
        }
        return new int[] {-1, enqueues};
    }
    static int[] listQueue(int n, int start, int target) {
        if (start == target) return new int[] {0, 1};
        List<int[]> q = new ArrayList<>();
        boolean[] seen = new boolean[n];
        q.add(new int[] {start, 0});
        seen[start] = true;
        int head = 0;
        while (head < q.size()) {
            int[] cur = q.get(head++);
            if (cur[0] == target) return new int[] {cur[1], q.size()};
            for (int y : new int[] {(cur[0] + 2) % n, (cur[0] + 3) % n}) {
                if (!seen[y]) { seen[y] = true; q.add(new int[] {y, cur[1] + 1}); }
            }
        }
        return new int[] {-1, q.size()};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(search(7, 0, 4, true), new int[] {2, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(search(6, 2, 2, true), new int[] {0, 1})) throw new AssertionError("example 2");
        if (search(7, 0, 4, false)[1] <= search(7, 0, 4, true)[1]) throw new AssertionError("marking at removal appends duplicates");
        if (search(4, 0, 1, true)[0] != 2) throw new AssertionError("on a ring of four, 0 reaches 2 and then 1");
        Random rnd = new Random(11403);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            int[] got = search(n, s, g, true);
            if (!Arrays.equals(got, listQueue(n, s, g))) throw new AssertionError("differs on " + n + " " + s + " " + g);
            if (got[1] > n) throw new AssertionError("a state was appended twice");
        }
    }
}
```

#### Solution: [Recognize] Shortest Word Transform From Supplied Neighbors (Author exercise)
<!-- id: sq-word-transform-neighbors -->

**Approach.** The words are the states and the supplied lists are the transitions, so the queue invariant applies directly. Run the search from the beginning word, marking on insertion and recording each word's distance in transitions. When the end word is reached, return its distance plus one, because the chain counts both ends. If the queue empties first, return 0. A chain whose begin and end are the same word has length one. The assertions compare with a Floyd-style relaxation over all pairs on random symmetric neighbour lists.

**Complexity.** O(n + m) time for n words and m listed neighbours, and O(n) space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class WordTransformNeighbours {
    static int chainLength(int[][] neighbours, int begin, int end) {
        int[] dist = new int[neighbours.length];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[begin] = 0;
        queue.addLast(begin);
        while (!queue.isEmpty()) {
            int w = queue.removeFirst();
            if (w == end) return dist[w] + 1;
            for (int nb : neighbours[w]) if (dist[nb] == -1) { dist[nb] = dist[w] + 1; queue.addLast(nb); }
        }
        return 0;
    }
    static int allPairs(int[][] neighbours, int begin, int end) {
        int n = neighbours.length, inf = 1_000_000;
        int[][] d = new int[n][n];
        for (int[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) { d[i][i] = 0; for (int nb : neighbours[i]) d[i][nb] = Math.min(d[i][nb], 1); }
        for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
        return d[begin][end] >= inf ? 0 : d[begin][end] + 1;
    }

    public static void main(String[] args) {
        if (chainLength(new int[][] {{1}, {0, 2, 4}, {1, 3}, {2}, {1}}, 0, 3) != 4) throw new AssertionError("example 1");
        if (chainLength(new int[][] {{1}, {0}, {}}, 0, 2) != 0) throw new AssertionError("example 2");
        if (chainLength(new int[][] {{}}, 0, 0) != 1) throw new AssertionError("a chain of one word");
        Random rnd = new Random(11404);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            boolean[][] adj = new boolean[n][n];
            for (int e = 0; e < n * 2; e++) { int a = rnd.nextInt(n), b = rnd.nextInt(n); if (a != b) { adj[a][b] = true; adj[b][a] = true; } }
            int[][] nbs = new int[n][];
            for (int i = 0; i < n; i++) {
                int c = 0;
                for (int j = 0; j < n; j++) if (adj[i][j]) c++;
                nbs[i] = new int[c];
                c = 0;
                for (int j = 0; j < n; j++) if (adj[i][j]) nbs[i][c++] = j;
            }
            int b = rnd.nextInt(n), e = rnd.nextInt(n);
            if (chainLength(nbs, b, e) != allPairs(nbs, b, e)) throw new AssertionError("differs on " + Arrays.deepToString(nbs));
        }
    }
}
```
