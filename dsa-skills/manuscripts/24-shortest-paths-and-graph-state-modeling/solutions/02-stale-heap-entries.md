<!-- solutions-for: 02-stale-heap-entries -->
### Stale Heap Entries

#### Solution: [Build] Two Entries For One Node (Author exercise)
<!-- id: sp-two-entries -->

**Approach.** Walk through the offers once with a `best` array that starts at the largest long. An offer that beats the board is recorded as a written slip, by its position, and the board is lowered. After the walk, every recorded slip whose hour differs from the final board value for its depot is stale. The oracle never keeps a board: for each offer it looks back at earlier offers for the same depot and says the offer was written when none of them had an hour at or below it, and says it is stale when some offer for that depot is smaller. The main method also asserts the Java claims of the lesson with counters. Removing an absent item from a `PriorityQueue` calls `equals` once for every stored slip, removing the largest hour calls it more than half as many times as there are slips, and doubling the tray roughly doubles the calls, while lifting the smallest slip needs only a few comparator calls. Iterating a queue gives storage order, not sorted order, though polling gives sorted order. Finally, `remove` on an `int[]` finds nothing, because arrays compare by identity.

**Complexity.** One pass over P offers with O(1) work each gives O(P + n) time and O(P + n) space for the board and the answer.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class TwoEntriesSolution {
    static int[] solve(int n, int[][] proposals) {
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        List<Integer> written = new ArrayList<>();
        for (int i = 0; i < proposals.length; i++) {
            int depot = proposals[i][0];
            if (proposals[i][1] < best[depot]) {
                best[depot] = proposals[i][1];
                written.add(i);
            }
        }
        List<Integer> old = new ArrayList<>();
        for (int i : written) if (proposals[i][1] != best[proposals[i][0]]) old.add(i);
        int[] out = new int[old.size()];
        for (int i = 0; i < out.length; i++) out[i] = old.get(i);
        return out;
    }

    static int[] oracle(int n, int[][] p) {
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < p.length; i++) {
            boolean beatenBefore = false, beatenAtAll = false;
            for (int j = 0; j < p.length; j++) {
                if (p[j][0] != p[i][0]) continue;
                if (j < i && p[j][1] <= p[i][1]) beatenBefore = true;
                if (p[j][1] < p[i][1]) beatenAtAll = true;
            }
            if (!beatenBefore && beatenAtAll) out.add(i);
        }
        return out.stream().mapToInt(Integer::intValue).toArray();
    }

    static final class Slip {
        static int equalsCalls;
        static int compareCalls;
        final int depot;
        final long hour;

        Slip(int depot, long hour) {
            this.depot = depot;
            this.hour = hour;
        }

        @Override
        public boolean equals(Object o) {
            equalsCalls++;
            return o instanceof Slip s && s.depot == depot && s.hour == hour;
        }

        @Override
        public int hashCode() {
            return Long.hashCode(hour) * 31 + depot;
        }
    }

    static PriorityQueue<Slip> filledTray(int m, long seed) {
        PriorityQueue<Slip> tray = new PriorityQueue<>((a, b) -> {
            Slip.compareCalls++;
            return Long.compare(a.hour, b.hour);
        });
        List<Integer> hours = new ArrayList<>();
        for (int i = 0; i < m; i++) hours.add(i);
        Collections.shuffle(hours, new Random(seed));
        for (int h : hours) tray.add(new Slip(h % 7, h));
        return tray;
    }

    static int callsToRemoveLargest(int m) {
        PriorityQueue<Slip> tray = filledTray(m, 5);
        Slip.equalsCalls = 0;
        if (!tray.remove(new Slip((m - 1) % 7, m - 1))) throw new AssertionError("largest must be removable");
        return Slip.equalsCalls;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(3, new int[][] {{1, 9}, {2, 4}, {1, 6}, {1, 7}, {1, 5}}), new int[] {0, 2}))
            throw new AssertionError("example 1");
        if (solve(2, new int[][] {{0, 0}, {1, 5}, {1, 5}, {1, 5}}).length != 0) throw new AssertionError("example 2");
        Random rnd = new Random(24201);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(5);
            int[][] p = new int[rnd.nextInt(14)][];
            for (int i = 0; i < p.length; i++) p[i] = new int[] {rnd.nextInt(n), rnd.nextInt(8)};
            int[][] copy = new int[p.length][];
            for (int i = 0; i < p.length; i++) copy[i] = p[i].clone();
            if (!Arrays.equals(solve(n, p), oracle(n, p))) throw new AssertionError("random " + Arrays.deepToString(p));
            if (!Arrays.deepEquals(p, copy)) throw new AssertionError("input changed");
        }

        int m = 2000;
        PriorityQueue<Slip> tray = filledTray(m, 7);
        Slip.equalsCalls = 0;
        if (tray.remove(new Slip(-1, -1))) throw new AssertionError("absent slip removed");
        if (Slip.equalsCalls != m) throw new AssertionError("absent removal scans every slot " + Slip.equalsCalls);
        int largest = callsToRemoveLargest(m);
        if (largest < m / 2) throw new AssertionError("largest hour sits in the last half of the array " + largest);
        int doubled = callsToRemoveLargest(2 * m);
        if (doubled < largest * 3 / 2) throw new AssertionError("equals calls must grow with tray size");
        tray = filledTray(m, 9);
        Slip.compareCalls = 0;
        tray.poll();
        if (Slip.compareCalls > 2 * 11 + 2) throw new AssertionError("poll compares O(log m) times " + Slip.compareCalls);

        PriorityQueue<Integer> pq = new PriorityQueue<>();
        for (int v : new int[] {5, 3, 8, 1}) pq.add(v);
        List<Integer> seen = new ArrayList<>(pq);
        if (!seen.equals(List.of(1, 3, 8, 5))) throw new AssertionError("storage order " + seen);
        List<Integer> sorted = new ArrayList<>(seen);
        Collections.sort(sorted);
        if (seen.equals(sorted)) throw new AssertionError("iteration must not be sorted here");
        List<Integer> polled = new ArrayList<>();
        while (!pq.isEmpty()) polled.add(pq.poll());
        if (!polled.equals(sorted)) throw new AssertionError("poll order is sorted");
        int unsortedCount = 0;
        Random r2 = new Random(3);
        for (int t = 0; t < 200; t++) {
            PriorityQueue<Integer> q = new PriorityQueue<>();
            List<Integer> vals = new ArrayList<>();
            for (int i = 0; i < 8; i++) vals.add(i);
            Collections.shuffle(vals, r2);
            q.addAll(vals);
            List<Integer> it = new ArrayList<>(q);
            if (it.get(0) != 0) throw new AssertionError("front element is the minimum");
            if (!it.equals(Arrays.asList(0, 1, 2, 3, 4, 5, 6, 7))) unsortedCount++;
        }
        if (unsortedCount < 100) throw new AssertionError("iteration is usually unsorted " + unsortedCount);

        PriorityQueue<int[]> arrays = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
        arrays.add(new int[] {1, 2});
        if (arrays.remove(new int[] {1, 2}) || arrays.size() != 1) throw new AssertionError("arrays compare by identity");
    }
}
```

#### Solution: [Vary] Skip Before Expansion (Author exercise)
<!-- id: sp-skip-before-expansion -->

**Approach.** Build adjacency lists, seed the tray with the source slip, and loop until the tray is empty. The first statement after a lift compares the slip's hour with the board and continues when they differ, so the road loop only runs for a live slip. Each depot has exactly one live slip, hence its roads are checked once. The oracle is a plain reachability search from the source: the reached count is the number of reachable depots and the check count is the sum of road counts out of those depots, with no tray in sight. The program also checks the final hours against Floyd-Warshall, and it shows that a variant without the early comparison gives the same hours yet checks strictly more roads on the first example.

**Complexity.** Each road is checked at most once, and slips are queued only on improvement, so the run costs O((n + m) log m) for m roads, with O(n + m) space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class SkipBeforeExpansionSolution {
    static long[] lastHours;

    static int[] run(int n, int[][] roads, int source, boolean skipOld) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
        long[] board = new long[n];
        Arrays.fill(board, Long.MAX_VALUE);
        board[source] = 0;
        PriorityQueue<long[]> tray = new PriorityQueue<>((a, b) ->
                a[0] == b[0] ? Long.compare(a[1], b[1]) : Long.compare(a[0], b[0]));
        tray.add(new long[] {0, source});
        int checks = 0;
        while (!tray.isEmpty()) {
            long[] slip = tray.poll();
            int depot = (int) slip[1];
            if (skipOld && slip[0] != board[depot]) continue;
            for (int[] road : adj.get(depot)) {
                checks++;
                long offer = slip[0] + road[1];
                if (offer < board[road[0]]) {
                    board[road[0]] = offer;
                    tray.add(new long[] {offer, road[0]});
                }
            }
        }
        lastHours = board;
        int reached = 0;
        for (long b : board) if (b != Long.MAX_VALUE) reached++;
        return new int[] {reached, checks};
    }

    static int[] oracle(int n, int[][] roads, int source) {
        boolean[] seen = new boolean[n];
        ArrayDeque<Integer> work = new ArrayDeque<>();
        work.push(source);
        seen[source] = true;
        while (!work.isEmpty()) {
            int u = work.pop();
            for (int[] r : roads) if (r[0] == u && !seen[r[1]]) {
                seen[r[1]] = true;
                work.push(r[1]);
            }
        }
        int reached = 0, checks = 0;
        for (int u = 0; u < n; u++) {
            if (!seen[u]) continue;
            reached++;
            for (int[] r : roads) if (r[0] == u) checks++;
        }
        return new int[] {reached, checks};
    }

    static long[] floyd(int n, int[][] roads, int source) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] r : roads) d[r[0]][r[1]] = Math.min(d[r[0]][r[1]], r[2]);
        for (int m = 0; m < n; m++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][m] + d[m][j]);
        long[] out = new long[n];
        for (int i = 0; i < n; i++) out[i] = d[source][i] >= inf ? Long.MAX_VALUE : d[source][i];
        return out;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 5}, {0, 2, 1}, {2, 1, 1}, {1, 3, 2}};
        if (!Arrays.equals(run(4, e1, 0, true), new int[] {4, 4})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1, 2}, {0, 2, 1}, {2, 1, 1}, {1, 3, 0}, {2, 3, 5}, {4, 0, 1}};
        if (!Arrays.equals(run(5, e2, 0, true), new int[] {4, 5})) throw new AssertionError("example 2");
        int[] lazy = run(4, e1, 0, false);
        if (lazy[1] != 5 || lazy[0] != 4) throw new AssertionError("without the skip depot 1 is expanded twice " + Arrays.toString(lazy));
        Random rnd = new Random(24202);
        int worse = 0;
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] roads = new int[rnd.nextInt(13)][];
            for (int i = 0; i < roads.length; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(7)};
            int source = rnd.nextInt(n);
            int[][] copy = new int[roads.length][];
            for (int i = 0; i < roads.length; i++) copy[i] = roads[i].clone();
            int[] got = run(n, roads, source, true);
            if (!Arrays.equals(got, oracle(n, roads, source))) throw new AssertionError("counts " + Arrays.deepToString(roads));
            if (!Arrays.equals(lastHours, floyd(n, roads, source))) throw new AssertionError("hours " + Arrays.deepToString(roads));
            int[] sloppy = run(n, roads, source, false);
            if (!Arrays.equals(lastHours, floyd(n, roads, source))) throw new AssertionError("hours without skip");
            if (sloppy[1] < got[1]) throw new AssertionError("skipping never adds checks");
            if (sloppy[1] > got[1]) worse++;
            if (!Arrays.deepEquals(roads, copy)) throw new AssertionError("input changed");
        }
        if (worse == 0) throw new AssertionError("random graphs must show the saving");
    }
}
```

#### Solution: [Boundary] Equal-Cost Alternatives (Author exercise)
<!-- id: sp-equal-cost-alternatives -->

**Approach.** Count one push for the starting slip and one for every offer that is strictly below the board. An offer equal to the board is not a better route, so queueing it would only create a second live-looking slip. The oracle avoids a heap altogether: it keeps the pending slips in a plain list, finds the smallest by hour and then depot with a linear scan, and counts pushes the same way, which makes the order of lifts identical because no two pending slips can be equal in both fields. A second block of assertions builds the damaged variant that queues ties. On the first example it pushes four slips instead of three and expands depot 1 twice, and on the zero-hour loop of the second example it keeps going until a cap of 10,000 lifts stops it, while the correct version finishes.

**Complexity.** There is at most one push per road plus the starting slip, and each push or lift costs a logarithm, so the time is O((n + m) log m) for m roads, using O(n + m) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class EqualCostSolution {
    static long[] search(int n, int[][] roads, int source, boolean queueTies, int liftCap) {
        List<List<int[]>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] r : roads) adj.get(r[0]).add(new int[] {r[1], r[2]});
        long[] board = new long[n];
        Arrays.fill(board, Long.MAX_VALUE);
        board[source] = 0;
        PriorityQueue<long[]> tray = new PriorityQueue<>((a, b) ->
                a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        tray.add(new long[] {0, source});
        long pushes = 1, expansions = 0, lifts = 0, finished = 1;
        while (!tray.isEmpty()) {
            if (++lifts > liftCap) {
                finished = 0;
                break;
            }
            long[] slip = tray.poll();
            int depot = (int) slip[1];
            if (slip[0] != board[depot]) continue;
            expansions++;
            for (int[] road : adj.get(depot)) {
                long offer = slip[0] + road[1];
                boolean take = queueTies ? offer <= board[road[0]] : offer < board[road[0]];
                if (take) {
                    board[road[0]] = offer;
                    tray.add(new long[] {offer, road[0]});
                    pushes++;
                }
            }
        }
        return new long[] {pushes, expansions, finished};
    }

    static int solve(int n, int[][] roads, int source) {
        return (int) search(n, roads, source, false, Integer.MAX_VALUE)[0];
    }

    static int oracle(int n, int[][] roads, int source) {
        long[] board = new long[n];
        Arrays.fill(board, Long.MAX_VALUE);
        board[source] = 0;
        List<long[]> pending = new ArrayList<>();
        pending.add(new long[] {0, source});
        int pushes = 1;
        while (!pending.isEmpty()) {
            int at = 0;
            for (int i = 1; i < pending.size(); i++) {
                long[] a = pending.get(i), b = pending.get(at);
                if (a[0] < b[0] || (a[0] == b[0] && a[1] < b[1])) at = i;
            }
            long[] slip = pending.remove(at);
            if (slip[0] != board[(int) slip[1]]) continue;
            for (int[] r : roads) {
                if (r[0] != slip[1]) continue;
                if (slip[0] + r[2] < board[r[1]]) {
                    board[r[1]] = slip[0] + r[2];
                    pending.add(new long[] {board[r[1]], r[1]});
                    pushes++;
                }
            }
        }
        return pushes;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 2}, {0, 2, 1}, {2, 1, 1}};
        int[][] e2 = {{0, 1, 0}, {1, 0, 0}, {1, 2, 0}};
        if (solve(3, e1, 0) != 3) throw new AssertionError("example 1");
        if (solve(3, e2, 0) != 3) throw new AssertionError("example 2");
        long[] tied = search(3, e1, 0, true, 10_000);
        if (tied[0] != 4 || tied[1] != 4 || tied[2] != 1) throw new AssertionError("ties double a slip " + Arrays.toString(tied));
        long[] fine = search(3, e1, 0, false, 10_000);
        if (fine[1] != 3) throw new AssertionError("each depot expands once");
        if (search(3, e2, 0, true, 10_000)[2] != 0) throw new AssertionError("tie queueing must not end on a zero loop");
        if (search(3, e2, 0, false, 10_000)[2] != 1) throw new AssertionError("strict rule ends");
        Random rnd = new Random(24203);
        int extra = 0;
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(6);
            int[][] roads = new int[rnd.nextInt(14)][];
            for (int i = 0; i < roads.length; i++) roads[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(4)};
            int source = rnd.nextInt(n);
            int[][] copy = new int[roads.length][];
            for (int i = 0; i < roads.length; i++) copy[i] = roads[i].clone();
            int got = solve(n, roads, source);
            if (got != oracle(n, roads, source)) throw new AssertionError("pushes " + Arrays.deepToString(roads) + " " + source);
            if (!Arrays.deepEquals(roads, copy)) throw new AssertionError("input changed");
            long[] sloppy = search(n, roads, source, true, 2000);
            if (sloppy[2] == 1 && sloppy[0] > got) extra++;
        }
        if (extra == 0) throw new AssertionError("ties must cost extra slips somewhere");
    }
}
```

#### Solution: [Recognize] Network Delay Time (LeetCode 743)
<!-- id: sp-network-delay-stale -->

**Approach.** Run the search from the code stage with a `long` board and a heap of `{distance, node}` slips ordered by distance and then node. Count a skip whenever the lifted distance differs from the board, and keep lifting until the heap is empty so that leftovers after the last node is final are counted too. The delay is the largest board value, or -1 if any node still holds the unreached marker. The oracle for the delay is Floyd-Warshall. The oracle for the skip count is a list-based simulation that finds the minimum by scanning, and a third version keeps a `TreeSet` of live pairs and removes the old pair on improvement, which gives the same delay and zero skips. The asserts also show that pushes equal reached nodes plus skips, that the node order of the tie rule can change the skip count, and the false friend: a version that calls `remove(new int[]{...})` on array slips removes nothing and then reads the distance of the last slip it lifts, which gives 11 instead of 8 on the graph of the first trace, along with the comparator `(int) (a - b)` that gives the wrong sign for hours near three billion.

**Complexity.** Pushes happen only on strict improvement, at most one per edge plus the start, so the heap work is O((n + E) log E) time with O(n + E) memory, and the skip count never exceeds E.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.TreeSet;

public final class StaleDelaySolution {
    static long pushesSeen;
    static long reachedSeen;

    static int[] solve(int n, int[][] times, int k) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] e : times) out.get(e[0]).add(new int[] {e[1], e[2]});
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[k] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) ->
                a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        heap.add(new long[] {0, k});
        int skipped = 0;
        pushesSeen = 1;
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] != best[u]) {
                skipped++;
                continue;
            }
            for (int[] e : out.get(u)) {
                long cand = top[0] + e[1];
                if (cand < best[e[0]]) {
                    best[e[0]] = cand;
                    heap.add(new long[] {cand, e[0]});
                    pushesSeen++;
                }
            }
        }
        long worst = 0;
        reachedSeen = 0;
        for (long b : best) {
            if (b == Long.MAX_VALUE) continue;
            reachedSeen++;
            worst = Math.max(worst, b);
        }
        return new int[] {reachedSeen < n ? -1 : (int) worst, skipped};
    }

    static int floydDelay(int n, int[][] times, int k) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][n];
        for (long[] row : d) Arrays.fill(row, inf);
        for (int i = 0; i < n; i++) d[i][i] = 0;
        for (int[] e : times) d[e[0]][e[1]] = Math.min(d[e[0]][e[1]], e[2]);
        for (int m = 0; m < n; m++)
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][m] + d[m][j]);
        long worst = 0;
        for (int j = 0; j < n; j++) {
            if (d[k][j] >= inf) return -1;
            worst = Math.max(worst, d[k][j]);
        }
        return (int) worst;
    }

    static int scanSkips(int n, int[][] times, int k, boolean lowerNodeFirst) {
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[k] = 0;
        List<long[]> bag = new ArrayList<>();
        bag.add(new long[] {0, k});
        int skipped = 0;
        while (!bag.isEmpty()) {
            int at = 0;
            for (int i = 1; i < bag.size(); i++) {
                long[] a = bag.get(i), b = bag.get(at);
                boolean earlier = a[0] < b[0] || (a[0] == b[0] && (lowerNodeFirst ? a[1] < b[1] : a[1] > b[1]));
                if (earlier) at = i;
            }
            long[] top = bag.remove(at);
            int u = (int) top[1];
            if (top[0] != best[u]) {
                skipped++;
                continue;
            }
            for (int[] e : times) {
                if (e[0] != u || top[0] + e[2] >= best[e[1]]) continue;
                best[e[1]] = top[0] + e[2];
                bag.add(new long[] {best[e[1]], e[1]});
            }
        }
        return skipped;
    }

    static int[] treeSetVersion(int n, int[][] times, int k) {
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[k] = 0;
        TreeSet<long[]> live = new TreeSet<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        live.add(new long[] {0, k});
        int skipped = 0;
        while (!live.isEmpty()) {
            long[] top = live.pollFirst();
            if (top[0] != best[(int) top[1]]) skipped++;
            for (int[] e : times) {
                if (e[0] != top[1] || top[0] + e[2] >= best[e[1]]) continue;
                if (best[e[1]] != Long.MAX_VALUE) live.remove(new long[] {best[e[1]], e[1]});
                best[e[1]] = top[0] + e[2];
                live.add(new long[] {best[e[1]], e[1]});
            }
        }
        long worst = 0;
        for (long b : best) {
            if (b == Long.MAX_VALUE) return new int[] {-1, skipped};
            worst = Math.max(worst, b);
        }
        return new int[] {(int) worst, skipped};
    }

    static long[] brokenRemoveVersion(int n, int[][] times, int k, boolean[] removeWorked) {
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[k] = 0;
        PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        heap.add(new int[] {0, k});
        long lastHour = 0;
        while (!heap.isEmpty()) {
            int[] top = heap.poll();
            lastHour = top[0];
            for (int[] e : times) {
                if (e[0] != top[1] || top[0] + e[2] >= best[e[1]]) continue;
                if (best[e[1]] != Long.MAX_VALUE && heap.remove(new int[] {(int) best[e[1]], e[1]})) removeWorked[0] = true;
                best[e[1]] = top[0] + e[2];
                heap.add(new int[] {(int) best[e[1]], e[1]});
            }
        }
        return new long[] {lastHour};
    }

    public static void main(String[] args) {
        int[][] g1 = {{0, 1, 6}, {0, 2, 3}, {2, 1, 1}, {1, 3, 2}, {2, 3, 7}, {3, 4, 1}, {2, 4, 9}};
        if (!Arrays.equals(solve(5, g1, 0), new int[] {7, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(4, new int[][] {{0, 1, 4}, {1, 2, 1}}, 0), new int[] {-1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[0][], 0), new int[] {0, 0})) throw new AssertionError("single node");

        Random rnd = new Random(24204);
        boolean orderMatters = false;
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] times = new int[rnd.nextInt(13)][];
            for (int i = 0; i < times.length; i++) times[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(8)};
            int k = rnd.nextInt(n);
            int[][] copy = new int[times.length][];
            for (int i = 0; i < times.length; i++) copy[i] = times[i].clone();
            int[] got = solve(n, times, k);
            if (got[0] != floydDelay(n, times, k)) throw new AssertionError("delay " + Arrays.deepToString(times));
            if (got[1] != scanSkips(n, times, k, true)) throw new AssertionError("skips " + Arrays.deepToString(times));
            if (pushesSeen != reachedSeen + got[1]) throw new AssertionError("pushes equal reached plus skips");
            int[] tree = treeSetVersion(n, times, k);
            if (tree[0] != got[0] || tree[1] != 0) throw new AssertionError("true decrease-key never skips");
            if (!Arrays.deepEquals(times, copy)) throw new AssertionError("input changed");
            if (scanSkips(n, times, k, false) != got[1]) orderMatters = true;
        }
        if (!orderMatters) throw new AssertionError("the tie rule should be able to change the skip count");

        boolean[] worked = {false};
        long[] broken = brokenRemoveVersion(5, new int[][] {{0, 1, 7}, {0, 2, 2}, {2, 1, 3}, {1, 3, 1}, {2, 3, 9}, {3, 4, 2}}, 0, worked);
        int[] right = solve(5, new int[][] {{0, 1, 7}, {0, 2, 2}, {2, 1, 3}, {1, 3, 1}, {2, 3, 9}, {3, 4, 2}}, 0);
        if (worked[0]) throw new AssertionError("remove on a fresh int[] must find nothing");
        if (broken[0] != 11 || right[0] != 8) throw new AssertionError("false friend gives 11, truth is 8");

        long a = 3_000_000_000L, b = 0;
        if ((int) (a - b) >= 0) throw new AssertionError("subtracting long hours wraps negative in an int");
        if (Long.compare(a, b) <= 0) throw new AssertionError("Long.compare keeps the sign");
    }
}
```
