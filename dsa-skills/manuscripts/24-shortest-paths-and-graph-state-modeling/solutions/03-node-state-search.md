<!-- solutions-for: 03-node-state-search -->
### Node-State Search

#### Solution: [Build] Node And Coupon Flag (Author exercise)
<!-- id: sp-coupon-flag -->

**Approach.** Scan the services once in input order. Every service that leaves `u` contributes the paid ride first, with the same `spent` flag and the fare as cost, and then the coupon ride when `spent` is 0, with flag 1 and cost 0. Nothing is deduplicated, so parallel services and self-loops each show up as written. The oracle never builds the list in order: it counts, for every candidate triple in a grid of destinations, flags and costs, how many services would justify it, and compares those counts with a multiset of the routine's output, then checks the stated order by walking the services again. The run also asserts that the input rows are untouched and that two separately built `int[]` pairs with equal contents are not found in a `HashSet`, which is why the lesson flattens the pair.

**Complexity.** One pass over the S services with at most two output rows each gives O(S) time and O(S) memory for the result, independent of the number of stops.

```java run
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

public final class CouponFlagSolution {
    static List<long[]> solve(int[][] services, int u, int spent) {
        List<long[]> out = new ArrayList<>();
        for (int[] s : services) {
            if (s[0] != u) continue;
            out.add(new long[] {s[1], spent, s[2]});
            if (spent == 0) out.add(new long[] {s[1], 1, 0});
        }
        return out;
    }

    static String key(long a, long b, long c) {
        return a + "," + b + "," + c;
    }

    static void check(int[][] services, int u, int spent, int n, int maxFare) {
        int[][] before = new int[services.length][];
        for (int i = 0; i < services.length; i++) before[i] = services[i].clone();
        List<long[]> got = solve(services, u, spent);
        for (int i = 0; i < services.length; i++)
            if (!java.util.Arrays.equals(before[i], services[i])) throw new AssertionError("input changed");
        Map<String, Integer> have = new HashMap<>();
        for (long[] t : got) have.merge(key(t[0], t[1], t[2]), 1, Integer::sum);
        Map<String, Integer> want = new HashMap<>();
        for (int v = 0; v < n; v++)
            for (int f = 0; f < 2; f++)
                for (int cost = 0; cost <= maxFare; cost++) {
                    int count = 0;
                    for (int[] s : services) {
                        if (s[0] != u || s[1] != v) continue;
                        if (f == spent && cost == s[2]) count++;
                        if (spent == 0 && f == 1 && cost == 0) count++;
                    }
                    if (count > 0) want.put(key(v, f, cost), count);
                }
        if (!have.equals(want)) throw new AssertionError("multiset " + have + " vs " + want);
        int at = 0;
        for (int[] s : services) {
            if (s[0] != u) continue;
            long[] paid = got.get(at++);
            if (paid[0] != s[1] || paid[1] != spent || paid[2] != s[2]) throw new AssertionError("paid order");
            if (spent == 0) {
                long[] free = got.get(at++);
                if (free[0] != s[1] || free[1] != 1 || free[2] != 0) throw new AssertionError("free order");
            }
        }
        if (at != got.size()) throw new AssertionError("extra rows");
    }

    static String render(List<long[]> rows) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < rows.size(); i++) {
            long[] r = rows.get(i);
            sb.append(i == 0 ? "" : ",").append("[").append(r[0]).append(",").append(r[1]).append(",").append(r[2]).append("]");
        }
        return sb.append("]").toString();
    }

    public static void main(String[] args) {
        int[][] sample = {{0, 1, 5}, {0, 2, 2}, {1, 2, 7}};
        if (!render(solve(sample, 0, 0)).equals("[[1,0,5],[1,1,0],[2,0,2],[2,1,0]]")) throw new AssertionError("example 1");
        if (!render(solve(sample, 1, 1)).equals("[[2,1,7]]")) throw new AssertionError("example 2");
        if (!solve(sample, 2, 0).isEmpty()) throw new AssertionError("dead end");
        int[][] twin = {{3, 3, 4}, {3, 3, 4}};
        if (solve(twin, 3, 0).size() != 4) throw new AssertionError("parallel self-loops stay separate");
        if (solve(twin, 3, 1).size() != 2) throw new AssertionError("no coupon ride after spending");
        Set<int[]> byIdentity = new HashSet<>();
        byIdentity.add(new int[] {1, 0});
        if (byIdentity.contains(new int[] {1, 0})) throw new AssertionError("arrays hash by identity");
        Random rnd = new Random(24301);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(4), m = rnd.nextInt(8);
            int[][] services = new int[m][];
            for (int i = 0; i < m; i++) services[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(6)};
            check(services, rnd.nextInt(n), rnd.nextInt(2), n, 6);
        }
    }
}
```

#### Solution: [Vary] Distance By State (Author exercise)
<!-- id: sp-distance-by-state -->

**Approach.** Run Dijkstra on 2n flat vertices, where vertex `v * 2 + k` means standing at `v` with the coupon in hand when `k` is 0 and spent when `k` is 1. A paid service stays inside its layer at the fare, a free ride moves from layer 0 to layer 1 at cost 0, and an entry is skipped when its fare is larger than the stored one. Entries still at the sentinel become -1 in the output. The oracle does not use a heap at all: it sweeps every service over both layers repeatedly until a full sweep changes nothing, which is Bellman-Ford to a fixpoint. Fares go up to 2,000,000,000, so the test also runs graphs whose totals pass `Integer.MAX_VALUE`, and the run asserts three Java claims: that the same sum in `int` overflows to a negative number, that an `int[]` pair is not found in a `HashSet`, and that `(int) (a - b)` compares 2^32 and 0 as equal where `Long.compare` does not.

**Complexity.** Each of the 2n vertices is settled once and each of the up to 2E edges is relaxed once, with heap operations costing a logarithm, so the time is O((n + E) log E) and the memory is O(n + E).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.Set;

public final class DistanceByStateSolution {
    static long[][] solve(int n, int[][] services, int source) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] s : services) out.get(s[0]).add(new int[] {s[1], s[2]});
        long[] fare = new long[2 * n];
        Arrays.fill(fare, Long.MAX_VALUE);
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        fare[source * 2] = 0;
        heap.add(new long[] {0, source * 2});
        while (!heap.isEmpty()) {
            long[] cur = heap.poll();
            int ix = (int) cur[1];
            if (cur[0] > fare[ix]) continue;
            int layer = ix % 2;
            for (int[] ride : out.get(ix / 2)) {
                int paid = ride[0] * 2 + layer;
                if (cur[0] + ride[1] < fare[paid]) {
                    fare[paid] = cur[0] + ride[1];
                    heap.add(new long[] {fare[paid], paid});
                }
                int free = ride[0] * 2 + 1;
                if (layer == 0 && cur[0] < fare[free]) {
                    fare[free] = cur[0];
                    heap.add(new long[] {fare[free], free});
                }
            }
        }
        long[][] best = new long[n][2];
        for (int v = 0; v < n; v++)
            for (int k = 0; k < 2; k++) best[v][k] = fare[v * 2 + k] == Long.MAX_VALUE ? -1 : fare[v * 2 + k];
        return best;
    }

    static long[][] oracle(int n, int[][] services, int source) {
        long inf = Long.MAX_VALUE / 4;
        long[][] d = new long[n][2];
        for (long[] row : d) Arrays.fill(row, inf);
        d[source][0] = 0;
        boolean changed = true;
        while (changed) {
            changed = false;
            for (int[] s : services) {
                for (int k = 0; k < 2; k++)
                    if (d[s[0]][k] < inf && d[s[0]][k] + s[2] < d[s[1]][k]) {
                        d[s[1]][k] = d[s[0]][k] + s[2];
                        changed = true;
                    }
                if (d[s[0]][0] < inf && d[s[0]][0] < d[s[1]][1]) {
                    d[s[1]][1] = d[s[0]][0];
                    changed = true;
                }
            }
        }
        for (long[] row : d) for (int k = 0; k < 2; k++) if (row[k] == inf) row[k] = -1;
        return d;
    }

    public static void main(String[] args) {
        int[][] one = {{0, 1, 6}, {1, 2, 2}, {0, 2, 15}, {2, 3, 4}};
        if (!Arrays.deepEquals(solve(4, one, 0), new long[][] {{0, -1}, {6, 0}, {8, 0}, {12, 4}}))
            throw new AssertionError("example 1");
        int[][] two = {{1, 0, 4}, {1, 2, 6}, {2, 0, 1}};
        if (!Arrays.deepEquals(solve(3, two, 1), new long[][] {{4, 0}, {0, -1}, {6, 0}}))
            throw new AssertionError("example 2");
        int big = 2_000_000_000;
        int wrapped = big + big;
        if (wrapped >= 0) throw new AssertionError("int sum must overflow");
        long[][] huge = solve(3, new int[][] {{0, 1, big}, {1, 2, big}}, 0);
        if (huge[2][0] != 4_000_000_000L || huge[2][1] != big) throw new AssertionError("long totals");
        Set<int[]> byIdentity = new HashSet<>();
        byIdentity.add(new int[] {2, 1});
        if (byIdentity.contains(new int[] {2, 1})) throw new AssertionError("arrays hash by identity");
        long a = 1L << 32, b = 0;
        if ((int) (a - b) != 0 || Long.compare(a, b) != 1) throw new AssertionError("truncated comparator");
        Random rnd = new Random(24302);
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(6), m = rnd.nextInt(14);
            int[][] services = new int[m][];
            boolean large = rnd.nextBoolean();
            for (int i = 0; i < m; i++)
                services[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), large ? 1_000_000_000 + rnd.nextInt(1_000_000_000) : 1 + rnd.nextInt(9)};
            int[][] copy = new int[m][];
            for (int i = 0; i < m; i++) copy[i] = services[i].clone();
            int source = rnd.nextInt(n);
            long[][] got = solve(n, services, source);
            if (!Arrays.deepEquals(got, oracle(n, services, source))) throw new AssertionError("random " + t);
            if (!Arrays.deepEquals(copy, services)) throw new AssertionError("input changed");
        }
    }
}
```

#### Solution: [Boundary] Same Node, Different Future (Author exercise)
<!-- id: sp-same-node-future -->

**Approach.** Compute two tables with the pair search: `fwd[v][k]`, the cheapest fare from the source into each pair, and `back[v][k]`, the cheapest fare from each pair to the target over reversed services, where a reversed free ride goes from layer 1 back to layer 0 at cost 0. The overall best is the smaller of the target's two forward values. A stop is kept when its spent arrival is finite and strictly cheaper than its unspent arrival, and when `fwd[v][0] + back[v][0]` equals the best, meaning an optimal route can pass through it with the coupon still in hand. The oracle enumerates every simple route from the source to the target, tries each ride as the free one, takes the minimum, and collects the stops at positions up to the free ride from every optimal choice, filtered by the same price comparison computed from the routes themselves. The run also builds the lesson's false friend, a search with one fare per stop, asserts it returns 13 where the true answer is 7 on a concrete network, and that it is never too small on random networks while being too large at least once.

**Complexity.** Two Dijkstra runs over 2n vertices cost O((n + E) log E) time and O(n + E) memory, while the route-enumerating oracle is exponential and used only for n of at most 7.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;
import java.util.Set;
import java.util.TreeSet;

public final class SameNodeFutureSolution {
    static final long INF = Long.MAX_VALUE / 4;

    static long[] pairSearch(int n, int[][] services, int start, boolean reversed) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] s : services) {
            if (reversed) out.get(s[1]).add(new int[] {s[0], s[2]});
            else out.get(s[0]).add(new int[] {s[1], s[2]});
        }
        long[] d = new long[2 * n];
        Arrays.fill(d, INF);
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        if (reversed) {
            d[start * 2] = 0;
            d[start * 2 + 1] = 0;
            heap.add(new long[] {0, start * 2});
            heap.add(new long[] {0, start * 2 + 1});
        } else {
            d[start * 2] = 0;
            heap.add(new long[] {0, start * 2});
        }
        while (!heap.isEmpty()) {
            long[] cur = heap.poll();
            int ix = (int) cur[1];
            if (cur[0] > d[ix]) continue;
            int layer = ix % 2;
            for (int[] r : out.get(ix / 2)) {
                int same = r[0] * 2 + layer;
                if (cur[0] + r[1] < d[same]) {
                    d[same] = cur[0] + r[1];
                    heap.add(new long[] {d[same], same});
                }
                // forward: layer 0 -> 1 free; reversed: standing in layer 1 after the ride came from layer 0
                if (!reversed && layer == 0 && cur[0] < d[r[0] * 2 + 1]) {
                    d[r[0] * 2 + 1] = cur[0];
                    heap.add(new long[] {cur[0], r[0] * 2 + 1});
                }
                if (reversed && layer == 1 && cur[0] < d[r[0] * 2]) {
                    d[r[0] * 2] = cur[0];
                    heap.add(new long[] {cur[0], r[0] * 2});
                }
            }
        }
        return d;
    }

    static List<Integer> solve(int n, int[][] services, int source, int target) {
        List<Integer> kept = new ArrayList<>();
        if (source == target) return kept;
        long[] fwd = pairSearch(n, services, source, false);
        long[] back = pairSearch(n, services, target, true);
        long best = Math.min(fwd[target * 2], fwd[target * 2 + 1]);
        if (best >= INF) return kept;
        for (int v = 0; v < n; v++) {
            long open = fwd[v * 2], spent = fwd[v * 2 + 1];
            if (spent >= INF || spent >= open) continue;
            if (back[v * 2] < INF && open + back[v * 2] == best) kept.add(v);
        }
        return kept;
    }

    static long nodeOnly(int n, int[][] services, int source, int target) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] s : services) out.get(s[0]).add(new int[] {s[1], s[2]});
        boolean[] done = new boolean[n];
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> {
            int c = Long.compare(a[0], b[0]);
            return c != 0 ? c : Long.compare(a[1], b[1]);
        });
        heap.add(new long[] {0, source, 0});
        while (!heap.isEmpty()) {
            long[] cur = heap.poll();
            int v = (int) cur[1];
            if (done[v]) continue;
            done[v] = true;
            if (v == target) return cur[0];
            for (int[] r : out.get(v)) {
                heap.add(new long[] {cur[0] + r[1], r[0], cur[2]});
                if (cur[2] == 0) heap.add(new long[] {cur[0], r[0], 1});
            }
        }
        return -1;
    }

    static void walk(int n, int[][] services, int at, int target, boolean[] on, List<Integer> path, List<Integer> fares,
                     List<List<Integer>> paths, List<List<Integer>> fareLists) {
        if (at == target) {
            paths.add(new ArrayList<>(path));
            fareLists.add(new ArrayList<>(fares));
            return;
        }
        for (int[] s : services) {
            if (s[0] != at || on[s[1]]) continue;
            on[s[1]] = true;
            path.add(s[1]);
            fares.add(s[2]);
            walk(n, services, s[1], target, on, path, fares, paths, fareLists);
            fares.remove(fares.size() - 1);
            path.remove(path.size() - 1);
            on[s[1]] = false;
        }
    }

    static List<Integer> oracle(int n, int[][] services, int source, int target) {
        if (source == target) return new ArrayList<>();
        List<List<Integer>> paths = new ArrayList<>(), fareLists = new ArrayList<>();
        boolean[] on = new boolean[n];
        on[source] = true;
        List<Integer> path = new ArrayList<>();
        path.add(source);
        walk(n, services, source, target, on, path, new ArrayList<>(), paths, fareLists);
        if (paths.isEmpty()) return new ArrayList<>();
        // cheapest arrival per stop, found by looking at every simple route prefix
        long[] open = new long[n], spent = new long[n];
        Arrays.fill(open, INF);
        Arrays.fill(spent, INF);
        open[source] = 0;
        boolean[] on2 = new boolean[n];
        List<List<Integer>> allP = new ArrayList<>(), allF = new ArrayList<>();
        for (int v = 0; v < n; v++) {
            if (v == source) continue;
            boolean[] on3 = new boolean[n];
            on3[source] = true;
            List<Integer> p = new ArrayList<>();
            p.add(source);
            walk(n, services, source, v, on3, p, new ArrayList<>(), allP, allF);
        }
        for (int i = 0; i < allP.size(); i++) {
            List<Integer> p = allP.get(i), f = allF.get(i);
            int v = p.get(p.size() - 1);
            long sum = 0, mx = 0;
            for (int x : f) {
                sum += x;
                mx = Math.max(mx, x);
            }
            open[v] = Math.min(open[v], sum);
            spent[v] = Math.min(spent[v], sum - mx);
        }
        long best = INF;
        for (int i = 0; i < paths.size(); i++) {
            long sum = 0, mx = 0;
            for (int x : fareLists.get(i)) {
                sum += x;
                mx = Math.max(mx, x);
            }
            best = Math.min(best, sum - mx);
        }
        Set<Integer> kept = new TreeSet<>();
        for (int i = 0; i < paths.size(); i++) {
            List<Integer> f = fareLists.get(i);
            long sum = 0;
            for (int x : f) sum += x;
            for (int j = 0; j < f.size(); j++) {
                if (sum - f.get(j) != best) continue;
                for (int pos = 0; pos <= j; pos++) {
                    int v = paths.get(i).get(pos);
                    if (spent[v] < INF && spent[v] < open[v]) kept.add(v);
                }
            }
        }
        return new ArrayList<>(kept);
    }

    public static void main(String[] args) {
        int[][] decoy = {{0, 1, 3}, {1, 2, 10}, {2, 3, 4}, {0, 4, 6}, {4, 2, 9}};
        if (!solve(5, decoy, 0, 3).equals(List.of(1))) throw new AssertionError("example 1");
        int[][] easy = {{0, 1, 2}, {1, 2, 2}, {0, 2, 9}};
        if (!solve(3, easy, 0, 2).isEmpty()) throw new AssertionError("example 2");
        if (!solve(5, decoy, 3, 3).isEmpty()) throw new AssertionError("same stop");
        if (!solve(5, decoy, 3, 0).isEmpty()) throw new AssertionError("unreachable target");
        if (nodeOnly(5, decoy, 0, 3) != 13) throw new AssertionError("false friend value");
        long truth = Math.min(pairSearch(5, decoy, 0, false)[6], pairSearch(5, decoy, 0, false)[7]);
        if (truth != 7) throw new AssertionError("pair search value " + truth);
        Random rnd = new Random(24303);
        boolean worse = false;
        for (int t = 0; t < 500; t++) {
            int n = 2 + rnd.nextInt(5), m = rnd.nextInt(13);
            int[][] services = new int[m][];
            for (int i = 0; i < m; i++) services[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(12)};
            int s = rnd.nextInt(n), g = rnd.nextInt(n);
            List<Integer> got = solve(n, services, s, g);
            if (!got.equals(oracle(n, services, s, g))) throw new AssertionError("random " + t + " " + got + " " + oracle(n, services, s, g));
            if (s != g) {
                long[] f = pairSearch(n, services, s, false);
                long real = Math.min(f[g * 2], f[g * 2 + 1]);
                long naive = nodeOnly(n, services, s, g);
                if (real >= INF) {
                    if (naive != -1) throw new AssertionError("reach mismatch");
                } else {
                    if (naive < real) throw new AssertionError("false friend below truth");
                    if (naive > real) worse = true;
                }
            }
        }
        if (!worse) throw new AssertionError("false friend never failed");
    }
}
```

#### Solution: [Recognize] Shortest Path with Alternating Colors (LeetCode 1129)
<!-- id: sp-alternating-colors -->

**Approach.** The vertex is not enough, because reaching vertex v by a red edge allows only blue exits and reaching it by a blue edge allows only red ones. So the search runs over pairs `(v, colour of the last edge)`, flattened as `v * 2 + colour`, and both colours are seeded at vertex 0 with distance 0, since the first edge may have either colour. From a pair with colour c, only edges of the other colour are followed, and a pair is queued the first time it is seen, which makes its distance the shortest. The answer for a vertex is the smaller of its two pair distances, or -1 if neither was reached. The oracle is a layered reachability table: it keeps the set of pairs reachable by exactly L alternating edges for L from 0 upward, and a vertex's answer is the first L at which either of its pairs appears. The run also asserts that a search with one seen flag per vertex returns -1 for vertex 4 in the first example where the real answer is 3.

**Complexity.** There are 2n pairs and each edge is scanned at most once per pair at its tail, so the time is O(n + R + B) for R red and B blue edges, and the extra memory is O(n + R + B) for the adjacency lists, distances and queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class AlternatingColorsSolution {
    static int[] solve(int n, int[][] redEdges, int[][] blueEdges) {
        List<List<Integer>> red = new ArrayList<>(), blue = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            red.add(new ArrayList<>());
            blue.add(new ArrayList<>());
        }
        for (int[] e : redEdges) red.get(e[0]).add(e[1]);
        for (int[] e : blueEdges) blue.get(e[0]).add(e[1]);
        int[] dist = new int[2 * n];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        dist[0] = 0;
        dist[1] = 0;
        queue.add(0);
        queue.add(1);
        while (!queue.isEmpty()) {
            int pair = queue.poll();
            int v = pair / 2, last = pair % 2;
            List<Integer> exits = last == 0 ? blue.get(v) : red.get(v);
            int nextColor = 1 - last;
            for (int w : exits) {
                int to = w * 2 + nextColor;
                if (dist[to] != -1) continue;
                dist[to] = dist[pair] + 1;
                queue.add(to);
            }
        }
        int[] answer = new int[n];
        for (int v = 0; v < n; v++) {
            int a = dist[v * 2], b = dist[v * 2 + 1];
            answer[v] = a == -1 ? b : b == -1 ? a : Math.min(a, b);
        }
        return answer;
    }

    static int[] vertexOnly(int n, int[][] redEdges, int[][] blueEdges) {
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        dist[0] = 0;
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        queue.add(new int[] {0, 0});
        queue.add(new int[] {0, 1});
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            int[][] edges = cur[1] == 0 ? blueEdges : redEdges;
            for (int[] e : edges) {
                if (e[0] != cur[0] || dist[e[1]] != -1) continue;
                dist[e[1]] = dist[cur[0]] + 1;
                queue.add(new int[] {e[1], 1 - cur[1]});
            }
        }
        return dist;
    }

    static int[] oracle(int n, int[][] redEdges, int[][] blueEdges) {
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        boolean[][] now = new boolean[n][2];
        now[0][0] = true;
        now[0][1] = true;
        answer[0] = 0;
        for (int len = 1; len <= 2 * n + 2; len++) {
            boolean[][] nxt = new boolean[n][2];
            for (int[] e : redEdges) if (now[e[0]][1]) nxt[e[1]][0] = true;
            for (int[] e : blueEdges) if (now[e[0]][0]) nxt[e[1]][1] = true;
            for (int v = 0; v < n; v++) if (answer[v] == -1 && (nxt[v][0] || nxt[v][1])) answer[v] = len;
            now = nxt;
        }
        return answer;
    }

    public static void main(String[] args) {
        int[][] red1 = {{0, 1}, {0, 3}, {1, 4}}, blue1 = {{3, 1}};
        if (!Arrays.equals(solve(5, red1, blue1), new int[] {0, 1, -1, 1, 3})) throw new AssertionError("example 1");
        int[][] red2 = {{0, 1}, {1, 1}, {2, 3}}, blue2 = {{0, 1}, {3, 2}};
        if (!Arrays.equals(solve(4, red2, blue2), new int[] {0, 1, -1, -1})) throw new AssertionError("example 2");
        if (!Arrays.equals(vertexOnly(5, red1, blue1), new int[] {0, 1, -1, 1, -1}))
            throw new AssertionError("false friend must miss vertex 4");
        if (!Arrays.equals(solve(1, new int[0][], new int[0][]), new int[] {0})) throw new AssertionError("single vertex");
        Random rnd = new Random(24304);
        boolean friendFailed = false;
        for (int t = 0; t < 700; t++) {
            int n = 1 + rnd.nextInt(7);
            int[][] red = new int[rnd.nextInt(10)][], blue = new int[rnd.nextInt(10)][];
            for (int i = 0; i < red.length; i++) red[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            for (int i = 0; i < blue.length; i++) blue[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n)};
            int[] got = solve(n, red, blue);
            if (!Arrays.equals(got, oracle(n, red, blue))) throw new AssertionError("random " + t);
            if (!Arrays.equals(got, vertexOnly(n, red, blue))) friendFailed = true;
        }
        if (!friendFailed) throw new AssertionError("false friend never failed");
    }
}
```
