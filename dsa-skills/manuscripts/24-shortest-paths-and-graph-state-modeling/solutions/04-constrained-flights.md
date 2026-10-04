<!-- solutions-for: 04-constrained-flights -->
### Constrained Flights

#### Solution: [Build] At Most Two Edges (Author exercise)
<!-- id: sp-two-edges -->

**Approach.** Price every airfield for zero flights, then run two passes, each one copying the previous array and offering `old[from] + fee` to the copy. Because the second pass reads only the array finished by the first, a route of two flights is never mistaken for one. The oracle never builds a table: it lists every single flight from `src` to `dst` and every pair of flights that join up at an airfield, then takes the cheapest. The assertions cover both examples, show that a version which updates one array in place returns 300 on Example 1 where the right answer is 600, and check three Java claims: `clone()` on a `long[]` is an independent copy, adding a fee to `Long.MAX_VALUE` wraps negative, and the input is left as it was.

**Complexity.** Two scans of the F flights plus two copies of n prices cost O(F + n) time, and two arrays of n longs are live, so memory is O(n).

```java run
import java.util.Arrays;
import java.util.Random;

public final class TwoEdgesSolution {
    static final long NONE = Long.MAX_VALUE / 4;

    static int solve(int n, int[][] flights, int src, int dst) {
        long[] zero = new long[n];
        Arrays.fill(zero, NONE);
        zero[src] = 0;
        long[] one = zero.clone();
        for (int[] f : flights) {
            if (zero[f[0]] < NONE) one[f[1]] = Math.min(one[f[1]], zero[f[0]] + f[2]);
        }
        long[] two = one.clone();
        for (int[] f : flights) {
            if (one[f[0]] < NONE) two[f[1]] = Math.min(two[f[1]], one[f[0]] + f[2]);
        }
        return two[dst] >= NONE ? -1 : (int) two[dst];
    }

    static int inPlace(int n, int[][] flights, int src, int dst) {
        long[] price = new long[n];
        Arrays.fill(price, NONE);
        price[src] = 0;
        for (int pass = 0; pass < 2; pass++) {
            for (int[] f : flights) {
                if (price[f[0]] < NONE) price[f[1]] = Math.min(price[f[1]], price[f[0]] + f[2]);
            }
        }
        return price[dst] >= NONE ? -1 : (int) price[dst];
    }

    static int oracle(int n, int[][] flights, int src, int dst) {
        long best = NONE;
        for (int[] a : flights) {
            if (a[0] != src) continue;
            if (a[1] == dst) best = Math.min(best, a[2]);
            for (int[] b : flights) {
                if (b[0] == a[1] && b[1] == dst) best = Math.min(best, (long) a[2] + b[2]);
            }
        }
        return best >= NONE ? -1 : (int) best;
    }

    static int[][] copy(int[][] a) {
        int[][] c = new int[a.length][];
        for (int i = 0; i < a.length; i++) c[i] = a[i].clone();
        return c;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 100}, {1, 2, 100}, {2, 3, 100}, {0, 2, 500}};
        if (solve(4, e1, 0, 3) != 600) throw new AssertionError("example 1");
        if (inPlace(4, e1, 0, 3) != 300) throw new AssertionError("in-place version must leak to 300");
        int[][] e2 = {{0, 1, 10}, {1, 2, 10}, {2, 3, 10}, {3, 4, 10}};
        if (solve(5, e2, 0, 4) != -1) throw new AssertionError("example 2");
        if (solve(2, new int[0][], 0, 1) != -1) throw new AssertionError("no flights");
        long[] a = {1, 2, 3};
        long[] b = a.clone();
        b[0] = 99;
        if (a[0] != 1) throw new AssertionError("clone is independent");
        if (Long.MAX_VALUE + 5 >= 0) throw new AssertionError("sum must wrap");
        Random rnd = new Random(24401);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(5);
            int m = rnd.nextInt(12);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(30)};
            int src = rnd.nextInt(n), dst = rnd.nextInt(n);
            if (src == dst) dst = (src + 1) % n;
            int[][] before = copy(fl);
            int got = solve(n, fl, src, dst);
            if (!Arrays.deepEquals(before, fl)) throw new AssertionError("input changed");
            if (got != oracle(n, fl, src, dst)) throw new AssertionError("random case " + t);
        }
    }
}
```

#### Solution: [Vary] Cost By Stops Used (Author exercise)
<!-- id: sp-cost-by-legs -->

**Approach.** Allocate a table with `maxLegs + 1` rows and n columns. Row 0 holds zero for `src` and the none marker elsewhere. Every later row starts as a copy of the row above it, since a route that needs j - 1 flights also fits within j, and is then improved by offering each flight's fee on top of the row above. Entry j of the answer is the value at `dst` in row j, or -1. The oracle is independent of the table: for each j it walks recursively through every sequence of at most j flights from `src` and keeps the cheapest that ends at `dst`. The assertions check both examples, that the answers never increase with j, and a Java claim made in the lesson: calling `clone()` on a `long[][]` shares the row arrays, so a table built from a shallow copy is damaged by writes to the copy.

**Complexity.** Each of the maxLegs rows costs one copy of n entries and one scan of F flights, giving O(maxLegs * (n + F)) time, and the table itself needs O(maxLegs * n) memory.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CostByLegsSolution {
    static final long NONE = Long.MAX_VALUE / 4;

    static int[] solve(int n, int[][] flights, int src, int dst, int maxLegs) {
        long[][] table = new long[maxLegs + 1][n];
        Arrays.fill(table[0], NONE);
        table[0][src] = 0;
        for (int j = 1; j <= maxLegs; j++) {
            table[j] = table[j - 1].clone();
            for (int[] f : flights) {
                long from = table[j - 1][f[0]];
                if (from < NONE && from + f[2] < table[j][f[1]]) table[j][f[1]] = from + f[2];
            }
        }
        int[] out = new int[maxLegs + 1];
        for (int j = 0; j <= maxLegs; j++) out[j] = table[j][dst] >= NONE ? -1 : (int) table[j][dst];
        return out;
    }

    static long walk(int at, int dst, int[][] flights, int left) {
        long best = at == dst ? 0 : NONE;
        if (left == 0) return best;
        for (int[] f : flights) {
            if (f[0] == at) best = Math.min(best, f[2] + walk(f[1], dst, flights, left - 1));
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 100}, {1, 2, 100}, {2, 3, 100}, {0, 2, 500}};
        if (!Arrays.equals(solve(4, e1, 0, 3, 3), new int[] {-1, -1, 600, 300})) throw new AssertionError("example 1");
        int[][] e2 = {{0, 1, 2}, {1, 2, 3}, {0, 2, 9}};
        if (!Arrays.equals(solve(3, e2, 0, 2, 2), new int[] {-1, 9, 5})) throw new AssertionError("example 2");
        if (!Arrays.equals(solve(2, new int[0][], 0, 1, 0), new int[] {-1})) throw new AssertionError("zero legs");
        long[][] shared = {{1, 2}, {3, 4}};
        long[][] shallow = shared.clone();
        shallow[0][0] = 77;
        if (shared[0][0] != 77 || shallow[0] != shared[0]) throw new AssertionError("shallow clone shares rows");
        Random rnd = new Random(24402);
        for (int t = 0; t < 1500; t++) {
            int n = 2 + rnd.nextInt(4);
            int m = rnd.nextInt(9);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(20)};
            int src = rnd.nextInt(n), dst = rnd.nextInt(n);
            if (src == dst) dst = (src + 1) % n;
            int maxLegs = rnd.nextInt(5);
            int[] got = solve(n, fl, src, dst, maxLegs);
            for (int j = 0; j <= maxLegs; j++) {
                long want = walk(src, dst, fl, j);
                if (got[j] != (want >= NONE ? -1 : (int) want)) throw new AssertionError("case " + t + " j " + j);
                if (j > 0 && got[j - 1] != -1 && (got[j] == -1 || got[j] > got[j - 1]))
                    throw new AssertionError("must not increase " + t);
            }
        }
    }
}
```

#### Solution: [Boundary] Direct Flight And K Zero (Author exercise)
<!-- id: sp-direct-k-zero -->

**Approach.** Build adjacency lists, price the start at zero before any pass, and run passes for `round` from 0 through `k`, which is k + 1 passes and so a single pass when k is 0. Each pass copies the current prices and offers fees from the old array only. Because the start is priced at zero up front, `src == dst` returns 0 with no special case, and parallel flights are handled by the minimum in each offer. A pass that changes nothing ends the loop early, which cannot change the answer because later passes would see the same array. The oracle is a recursion over every walk of at most k + 1 flights that reports the cheapest arrival at `dst`, with the empty walk allowed. The assertions check both examples, a k of 0 where a dearer direct flight must beat a cheaper two-flight route, and the Java claim that `Integer.MAX_VALUE + 1` wraps negative, which is why the loop bound is written `round <= k` and not computed from `k + 1` in an `int` for huge k.

**Complexity.** There are at most k + 1 passes, each touching every flight once through the adjacency lists and copying n prices, so the time is O((k + 1) * (n + F)); the lists and two price arrays use O(n + F) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DirectFlightKZeroSolution {
    static final long NONE = Long.MAX_VALUE / 4;

    static int solve(int n, int[][] flights, int src, int dst, int k) {
        List<List<int[]>> out = new ArrayList<>();
        for (int i = 0; i < n; i++) out.add(new ArrayList<>());
        for (int[] f : flights) out.get(f[0]).add(new int[] {f[1], f[2]});
        long[] price = new long[n];
        Arrays.fill(price, NONE);
        price[src] = 0;
        for (int round = 0; round <= k; round++) {
            long[] fresh = price.clone();
            boolean moved = false;
            for (int u = 0; u < n; u++) {
                if (price[u] >= NONE) continue;
                for (int[] e : out.get(u)) {
                    if (price[u] + e[1] < fresh[e[0]]) {
                        fresh[e[0]] = price[u] + e[1];
                        moved = true;
                    }
                }
            }
            price = fresh;
            if (!moved) break;
        }
        return price[dst] >= NONE ? -1 : (int) price[dst];
    }

    static long walk(int at, int dst, int[][] flights, int left) {
        long best = at == dst ? 0 : NONE;
        if (left == 0) return best;
        for (int[] f : flights) {
            if (f[0] == at) best = Math.min(best, f[2] + walk(f[1], dst, flights, left - 1));
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] e1 = {{0, 1, 80}, {0, 1, 60}, {1, 2, 10}, {0, 2, 200}};
        if (solve(3, e1, 0, 2, 0) != 200) throw new AssertionError("example 1");
        if (solve(3, e1, 0, 2, 1) != 70) throw new AssertionError("one stop is cheaper");
        if (solve(3, e1, 0, 1, 0) != 60) throw new AssertionError("cheapest parallel flight");
        int[][] e2 = {{1, 0, 5}, {0, 1, 5}};
        if (solve(2, e2, 1, 1, 2) != 0) throw new AssertionError("example 2");
        if (solve(2, e2, 1, 1, 0) != 0) throw new AssertionError("empty route with k zero");
        if (solve(2, new int[][] {{0, 1, 4}}, 1, 0, 5) != -1) throw new AssertionError("directed");
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("int must wrap");
        Random rnd = new Random(24403);
        for (int t = 0; t < 2500; t++) {
            int n = 1 + rnd.nextInt(5);
            int m = n == 0 ? 0 : rnd.nextInt(10);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(25)};
            int src = rnd.nextInt(n), dst = rnd.nextInt(n);
            int k = rnd.nextInt(5);
            int[][] before = new int[m][];
            for (int i = 0; i < m; i++) before[i] = fl[i].clone();
            long want = walk(src, dst, fl, k + 1);
            int got = solve(n, fl, src, dst, k);
            if (!Arrays.deepEquals(before, fl)) throw new AssertionError("input changed");
            if (got != (want >= NONE ? -1 : (int) want)) throw new AssertionError("case " + t);
        }
    }
}
```

#### Solution: [Recognize] Cheapest Flights Within K Stops (LeetCode 787)
<!-- id: sp-cheapest-k-stops -->

**Approach.** Convert k stops to k + 1 flights, then run that many passes of bounded Bellman-Ford. Each pass clones the price array, so every offer reads the frozen previous row and writes the new one. The answer is the price at `dst` after the last pass, or -1 if it is still the none marker. The code is checked against two independent oracles on random graphs: a recursion over every walk of at most k + 1 flights, and a table indexed by the exact number of flights used, from which the minimum over all counts up to k + 1 is taken. The false friend is built as a real function: Dijkstra with one `dist[city]` that skips a popped entry whose price differs from `dist` and refuses to expand after k + 1 flights. On the graph 0 to 1 at 10, 1 to 2 at 10, 2 to 3 at 10 and 0 to 2 at 50 with k = 1, it returns -1 while the true answer is 60, and the assertions require both facts. They also check that `Integer.MAX_VALUE + 10` wraps negative, the reason a `long` sentinel is used, and that the flights array is not modified.

**Complexity.** The method runs k + 1 passes of one array copy and one flight scan each, so time is O((k + 1) * (n + F)), which is below a million steps at the largest limits, and only two arrays of n prices are alive, giving O(n) extra space.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class CheapestKStopsSolution {
    static final long NONE = Long.MAX_VALUE / 4;

    static int solve(int n, int[][] flights, int src, int dst, int k) {
        long[] best = new long[n];
        Arrays.fill(best, NONE);
        best[src] = 0;
        for (int leg = 0; leg <= k; leg++) {
            long[] next = best.clone();
            for (int[] f : flights) {
                if (best[f[0]] == NONE) continue;
                long offer = best[f[0]] + f[2];
                if (offer < next[f[1]]) next[f[1]] = offer;
            }
            best = next;
        }
        return best[dst] == NONE ? -1 : (int) best[dst];
    }

    static int oneDistPerCity(int n, int[][] flights, int src, int dst, int k) {
        long[] dist = new long[n];
        Arrays.fill(dist, NONE);
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src, 0});
        while (!heap.isEmpty()) {
            long[] top = heap.poll();
            int u = (int) top[1];
            if (top[0] != dist[u]) continue;
            if (u == dst) return (int) top[0];
            if (top[2] == k + 1) continue;
            for (int[] f : flights) {
                if (f[0] != u || top[0] + f[2] >= dist[f[1]]) continue;
                dist[f[1]] = top[0] + f[2];
                heap.add(new long[] {dist[f[1]], f[1], top[2] + 1});
            }
        }
        return -1;
    }

    static long walk(int at, int dst, int[][] flights, int left) {
        if (at == dst) return 0;
        if (left == 0) return NONE;
        long best = NONE;
        for (int[] f : flights) {
            if (f[0] == at) best = Math.min(best, f[2] + walk(f[1], dst, flights, left - 1));
        }
        return best;
    }

    static int byExactCount(int n, int[][] flights, int src, int dst, int k) {
        long[] exact = new long[n];
        Arrays.fill(exact, NONE);
        exact[src] = 0;
        long best = NONE;
        for (int used = 1; used <= k + 1; used++) {
            long[] nxt = new long[n];
            Arrays.fill(nxt, NONE);
            for (int[] f : flights) {
                if (exact[f[0]] < NONE) nxt[f[1]] = Math.min(nxt[f[1]], exact[f[0]] + f[2]);
            }
            exact = nxt;
            best = Math.min(best, exact[dst]);
        }
        return best >= NONE ? -1 : (int) best;
    }

    public static void main(String[] args) {
        int[][] g = {{0, 1, 30}, {1, 2, 30}, {2, 3, 30}, {3, 4, 30}, {0, 2, 100}, {2, 4, 100}};
        if (solve(5, g, 0, 4, 1) != 200) throw new AssertionError("example 1");
        if (solve(5, g, 0, 4, 3) != 120) throw new AssertionError("example 2");
        if (solve(5, g, 0, 4, 2) != 160) throw new AssertionError("two stops");
        int[][] trap = {{0, 1, 10}, {1, 2, 10}, {2, 3, 10}, {0, 2, 50}};
        if (solve(4, trap, 0, 3, 1) != 60) throw new AssertionError("layered answer");
        if (oneDistPerCity(4, trap, 0, 3, 1) != -1) throw new AssertionError("false friend must fail here");
        if (oneDistPerCity(4, trap, 0, 3, 2) != 30) throw new AssertionError("false friend fine with room");
        if (Integer.MAX_VALUE + 10 >= 0) throw new AssertionError("int sentinel would wrap");
        Random rnd = new Random(24404);
        int falseFriendWrong = 0;
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(5);
            int m = 4 + rnd.nextInt(10);
            int[][] fl = new int[m][];
            for (int i = 0; i < m; i++) fl[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), 1 + rnd.nextInt(20)};
            int src = rnd.nextInt(n), dst = rnd.nextInt(n);
            if (src == dst) dst = (src + 1) % n;
            int k = rnd.nextInt(3);
            int[][] before = new int[m][];
            for (int i = 0; i < m; i++) before[i] = fl[i].clone();
            int got = solve(n, fl, src, dst, k);
            if (!Arrays.deepEquals(before, fl)) throw new AssertionError("input changed");
            long want = walk(src, dst, fl, k + 1);
            if (got != (want >= NONE ? -1 : (int) want)) throw new AssertionError("walk oracle " + t);
            if (got != byExactCount(n, fl, src, dst, k)) throw new AssertionError("count oracle " + t);
            if (oneDistPerCity(n, fl, src, dst, k) != got) falseFriendWrong++;
        }
        if (falseFriendWrong == 0) throw new AssertionError("false friend never failed on random inputs");
    }
}
```
