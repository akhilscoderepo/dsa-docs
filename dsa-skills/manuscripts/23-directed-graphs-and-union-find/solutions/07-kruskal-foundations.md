<!-- solutions-for: 07-kruskal-foundations -->
### Kruskal Foundations

#### Solution: [Build] Cheapest Safe Edge (Author exercise)
<!-- id: ug-cheapest-safe-edge -->

**Approach.** Sort an array of route indices by price, which keeps equal prices in input order, then sweep once with a size-linked disjoint set. A route is accepted when the leaders of its ends differ, and the accepted row is copied into the result so the caller's rows are never shared. The oracle has no disjoint set at all. It keeps one label per village and, on an acceptance, rewrites every village of one label to the other, so a wrong tie order or a missed loop changes the list. On connected random graphs the oracle also tries every selection of n - 1 routes and checks that the accepted prices add up to the least total of any spanning selection, which is the minimality claim the cut property makes. The asserts confirm the Java claims of the lesson: the sort of objects is stable, `clone()` of an `int[][]` shares its rows, and the false friend fails, because the cheapest n - 1 routes without loop tests leave a village out on a fixed triangle graph.

**Complexity.** Sorting m routes is O(m log m) and the sweep adds O(m) leader walks of at most log n steps each, so the total is O(m log m) time with O(m + n) extra memory for the index array and the sets.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CheapestSafeEdgeSolution {
    static int leader(int[] parent, int v) {
        while (parent[v] != v) v = parent[v];
        return v;
    }

    static int[][] solve(int n, int[][] routes) {
        Integer[] idx = new Integer[routes.length];
        for (int i = 0; i < idx.length; i++) idx[i] = i;
        Arrays.sort(idx, (x, y) -> Integer.compare(routes[x][2], routes[y][2]));
        int[] parent = new int[n];
        int[] size = new int[n];
        for (int v = 0; v < n; v++) {
            parent[v] = v;
            size[v] = 1;
        }
        List<int[]> out = new ArrayList<>();
        for (int k : idx) {
            int ra = leader(parent, routes[k][0]), rb = leader(parent, routes[k][1]);
            if (ra == rb) continue;
            if (size[ra] < size[rb]) {
                int t = ra;
                ra = rb;
                rb = t;
            }
            parent[rb] = ra;
            size[ra] += size[rb];
            out.add(routes[k].clone());
        }
        return out.toArray(new int[0][]);
    }

    static List<int[]> labelOracle(int n, int[][] routes) {
        List<int[]> order = new ArrayList<>();
        for (int[] r : routes) order.add(r);
        for (int i = 1; i < order.size(); i++) {
            int[] key = order.get(i);
            int j = i - 1;
            while (j >= 0 && order.get(j)[2] > key[2]) {
                order.set(j + 1, order.get(j));
                j--;
            }
            order.set(j + 1, key);
        }
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        List<int[]> out = new ArrayList<>();
        for (int[] r : order) {
            if (label[r[0]] == label[r[1]]) continue;
            int from = label[r[1]], to = label[r[0]];
            for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
            out.add(r);
        }
        return out;
    }

    static boolean spans(int n, int[][] routes, int mask) {
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        for (int i = 0; i < routes.length; i++) {
            if ((mask >> i & 1) == 0) continue;
            int from = label[routes[i][1]], to = label[routes[i][0]];
            for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
        }
        for (int v = 0; v < n; v++) if (label[v] != label[0]) return false;
        return true;
    }

    static long bestBySelection(int n, int[][] routes) {
        long best = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << routes.length); mask++) {
            if (Integer.bitCount(mask) != n - 1 || !spans(n, routes, mask)) continue;
            long cost = 0;
            for (int i = 0; i < routes.length; i++) if ((mask >> i & 1) == 1) cost += routes[i][2];
            best = Math.min(best, cost);
        }
        return best;
    }

    static boolean sameRows(int[][] got, List<int[]> want) {
        if (got.length != want.size()) return false;
        for (int i = 0; i < got.length; i++) if (!Arrays.equals(got[i], want.get(i))) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!Arrays.deepEquals(solve(4, new int[][]{{0, 1, 5}, {1, 2, 3}, {0, 2, 4}, {2, 3, 6}}),
                new int[][]{{1, 2, 3}, {0, 2, 4}, {2, 3, 6}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(5, new int[][]{{0, 1, 2}, {2, 3, 2}, {1, 2, 2}, {3, 4, 1}, {0, 4, 2}, {1, 3, 9}}),
                new int[][]{{3, 4, 1}, {0, 1, 2}, {2, 3, 2}, {1, 2, 2}})) throw new AssertionError("example 2");
        if (solve(1, new int[][]{}).length != 0) throw new AssertionError("one village");
        if (solve(3, new int[][]{{1, 1, 0}, {0, 1, 4}, {1, 0, 4}}).length != 1) throw new AssertionError("loops and repeats");

        Integer[] ties = {0, 1, 2, 3, 4, 5};
        int[] key = {1, 0, 1, 0, 1, 0};
        Arrays.sort(ties, (x, y) -> Integer.compare(key[x], key[y]));
        if (!Arrays.equals(ties, new Integer[]{1, 3, 5, 0, 2, 4})) throw new AssertionError("object sort is stable");
        int[][] grid = {{1, 2}, {3, 4}};
        int[][] shallow = grid.clone();
        if (shallow == grid || shallow[0] != grid[0]) throw new AssertionError("clone shares rows");

        int[][] triangle = {{0, 1, 1}, {1, 2, 1}, {0, 2, 1}, {2, 3, 7}};
        int[][] blind = Arrays.copyOf(triangle, 3);
        if (spans(4, blind, 0b111)) throw new AssertionError("cheapest n-1 without loop test must fail");
        if (solve(4, triangle).length != 3) throw new AssertionError("sweep must still reach village 3");

        Random rnd = new Random(23701);
        int blindFailures = 0;
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(10);
            int[][] routes = new int[m][];
            for (int i = 0; i < m; i++) routes[i] = new int[]{rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(5)};
            int[][] snapshot = new int[m][];
            for (int i = 0; i < m; i++) snapshot[i] = routes[i].clone();
            int[][] got = solve(n, routes);
            for (int i = 0; i < m; i++) if (!Arrays.equals(routes[i], snapshot[i])) throw new AssertionError("input changed");
            if (!sameRows(got, labelOracle(n, routes))) throw new AssertionError("sweep differs from oracle");
            for (int[] r : got) for (int[] orig : routes) if (r == orig) throw new AssertionError("row shared");
            long total = 0;
            for (int[] r : got) total += r[2];
            boolean connected = got.length == n - 1;
            if (connected && total != bestBySelection(n, routes)) throw new AssertionError("not minimal");
            if (m >= n - 1 && connected) {
                Integer[] byPrice = new Integer[m];
                for (int i = 0; i < m; i++) byPrice[i] = i;
                Arrays.sort(byPrice, (x, y) -> Integer.compare(routes[x][2], routes[y][2]));
                int mask = 0;
                for (int i = 0; i < n - 1; i++) mask |= 1 << byPrice[i];
                if (!spans(n, routes, mask)) blindFailures++;
            }
        }
        if (blindFailures == 0) throw new AssertionError("false friend never failed");
    }
}
```

#### Solution: [Vary] Stop After V Minus One (Author exercise)
<!-- id: ug-stop-after-v-minus-one -->

**Approach.** The sweep is the same, with two changes: a counter of examined routes goes up for each route read, and the loop is left right after the acceptance that makes the count of accepted routes equal to `n - 1`. For one village the loop never starts, so the answer is `[0, 0]` with no special case. Sorting uses a copy of the outer array, and the stable sort keeps input order among equal prices. The oracle walks the same price order but merges villages by relabelling, then reads off the total and the position of the last accepted route. It also compares the total with the best of all selections of n - 1 routes. The asserts further check that an examined count below the number of routes is reached on at least some graphs, which shows the early exit really skips routes, and that the version without the early exit reports the larger count.

**Complexity.** The sort is O(m log m) and the loop reads at most m routes, each with two near-constant leader steps, giving O(m log m) time and O(n) memory beyond the sorted copy. The early exit saves only the tail of the scan, not the sort.

```java run
import java.util.Arrays;
import java.util.Random;

public final class StopAfterVMinusOneSolution {
    static int top(int[] link, int v) {
        while (link[v] != v) {
            link[v] = link[link[v]];
            v = link[v];
        }
        return v;
    }

    static long[] solve(int n, int[][] routes, boolean earlyExit) {
        int[][] sorted = routes.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[2], b[2]));
        int[] link = new int[n];
        for (int v = 0; v < n; v++) link[v] = v;
        long total = 0, examined = 0;
        int accepted = 0;
        for (int[] r : sorted) {
            if (earlyExit && accepted == n - 1) break;
            examined++;
            int ra = top(link, r[0]), rb = top(link, r[1]);
            if (ra == rb) continue;
            link[ra] = rb;
            total += r[2];
            accepted++;
        }
        return new long[]{total, examined};
    }

    static long[] oracle(int n, int[][] routes) {
        int m = routes.length;
        Integer[] order = new Integer[m];
        for (int i = 0; i < m; i++) order[i] = i;
        for (int i = 1; i < m; i++) {
            Integer key = order[i];
            int j = i - 1;
            while (j >= 0 && routes[order[j]][2] > routes[key][2]) {
                order[j + 1] = order[j];
                j--;
            }
            order[j + 1] = key;
        }
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        long total = 0;
        int accepted = 0, lastAt = 0;
        for (int pos = 0; pos < m && accepted < n - 1; pos++) {
            int[] r = routes[order[pos]];
            if (label[r[0]] == label[r[1]]) continue;
            int from = label[r[1]], to = label[r[0]];
            for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
            total += r[2];
            accepted++;
            lastAt = pos + 1;
        }
        return new long[]{total, lastAt};
    }

    static long bestBySelection(int n, int[][] routes) {
        long best = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << routes.length); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] label = new int[n];
            for (int v = 0; v < n; v++) label[v] = v;
            long cost = 0;
            for (int i = 0; i < routes.length; i++) {
                if ((mask >> i & 1) == 0) continue;
                int from = label[routes[i][1]], to = label[routes[i][0]];
                for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
                cost += routes[i][2];
            }
            boolean all = true;
            for (int v = 0; v < n; v++) if (label[v] != label[0]) all = false;
            if (all) best = Math.min(best, cost);
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(solve(4, new int[][]{{0, 1, 1}, {1, 2, 2}, {2, 3, 3}, {0, 3, 4}, {0, 2, 5}}, true), new long[]{6, 3}))
            throw new AssertionError("example 1");
        if (!Arrays.equals(solve(5, new int[][]{{0, 1, 1}, {1, 2, 2}, {0, 2, 3}, {3, 4, 4}, {2, 3, 6}, {1, 4, 8}}, true), new long[]{13, 5}))
            throw new AssertionError("example 2");
        if (!Arrays.equals(solve(1, new int[][]{}, true), new long[]{0, 0})) throw new AssertionError("one village");
        if (!Arrays.equals(solve(1, new int[][]{{0, 0, 3}}, true), new long[]{0, 0})) throw new AssertionError("one village with a loop");

        Random rnd = new Random(23702);
        int skipped = 0;
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(6);
            int extra = rnd.nextInt(5);
            int m = n - 1 + extra;
            int[][] routes = new int[m][];
            for (int v = 1; v < n; v++) routes[v - 1] = new int[]{rnd.nextInt(v), v, rnd.nextInt(6)};
            for (int i = n - 1; i < m; i++) routes[i] = new int[]{rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(6)};
            for (int i = m - 1; i > 0; i--) {
                int j = rnd.nextInt(i + 1);
                int[] tmp = routes[i];
                routes[i] = routes[j];
                routes[j] = tmp;
            }
            int[][] outer = routes.clone();
            int[][] before = new int[m][];
            for (int i = 0; i < m; i++) before[i] = routes[i].clone();
            long[] got = solve(n, routes, true);
            for (int i = 0; i < m; i++) {
                if (routes[i] != outer[i] || !Arrays.equals(routes[i], before[i])) throw new AssertionError("input changed");
            }
            if (!Arrays.equals(got, oracle(n, routes))) throw new AssertionError("sweep differs from oracle");
            if (got[0] != bestBySelection(n, routes)) throw new AssertionError("total is not minimal");
            long[] full = solve(n, routes, false);
            if (full[0] != got[0] || full[1] != m) throw new AssertionError("full scan reads every route");
            if (got[1] < m) skipped++;
        }
        if (skipped == 0) throw new AssertionError("early exit never skipped a route");
    }
}
```

#### Solution: [Boundary] Disconnected Weighted Graph (Author exercise)
<!-- id: ug-disconnected-weighted -->

**Approach.** Run the sweep and count acceptances, and return the total only if the count is exactly `n - 1`; otherwise return -1. The total lives in a `long` from the start, because four prices of two billion add up past the range of an `int`. The independent oracle is Prim's method on a matrix of cheapest parallel prices: start from village 0, repeatedly take the cheapest price from the reached set to an unreached village, and report -1 if every remaining price is missing. It uses no disjoint set. A selection-by-selection check on the smallest graphs gives a third opinion. Extra asserts confirm the Java claims: an int sum of two prices of two billion wraps to a negative number, a comparator that subtracts mis-orders values of opposite sign, and the true totals above `Integer.MAX_VALUE` come out right as a `long`.

**Complexity.** Sorting m routes costs O(m log m) and the sweep is O(m) near-constant steps, so the time is O(m log m) and memory is O(n) apart from the sorted copy, regardless of whether the answer is -1.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DisconnectedWeightedSolution {
    static int rootOf(int[] up, int v) {
        while (up[v] != v) {
            up[v] = up[up[v]];
            v = up[v];
        }
        return v;
    }

    static long solve(int n, int[][] routes) {
        int[][] byPrice = routes.clone();
        Arrays.sort(byPrice, (a, b) -> Integer.compare(a[2], b[2]));
        int[] up = new int[n];
        for (int v = 0; v < n; v++) up[v] = v;
        long total = 0;
        int taken = 0;
        for (int[] r : byPrice) {
            if (taken == n - 1) break;
            int ra = rootOf(up, r[0]), rb = rootOf(up, r[1]);
            if (ra == rb) continue;
            up[ra] = rb;
            total += r[2];
            taken++;
        }
        return taken == n - 1 ? total : -1;
    }

    static long prim(int n, int[][] routes) {
        long none = Long.MAX_VALUE;
        long[][] price = new long[n][n];
        for (long[] row : price) Arrays.fill(row, none);
        for (int[] r : routes) {
            if (r[0] == r[1]) continue;
            price[r[0]][r[1]] = Math.min(price[r[0]][r[1]], r[2]);
            price[r[1]][r[0]] = Math.min(price[r[1]][r[0]], r[2]);
        }
        boolean[] in = new boolean[n];
        long[] reach = new long[n];
        Arrays.fill(reach, none);
        reach[0] = 0;
        long total = 0;
        for (int round = 0; round < n; round++) {
            int pick = -1;
            for (int v = 0; v < n; v++) if (!in[v] && reach[v] != none && (pick < 0 || reach[v] < reach[pick])) pick = v;
            if (pick < 0) return -1;
            in[pick] = true;
            total += reach[pick];
            for (int v = 0; v < n; v++) if (!in[v] && price[pick][v] < reach[v]) reach[v] = price[pick][v];
        }
        return total;
    }

    static long bestBySelection(int n, int[][] routes) {
        long best = -1;
        for (int mask = 0; mask < (1 << routes.length); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] label = new int[n];
            for (int v = 0; v < n; v++) label[v] = v;
            long cost = 0;
            for (int i = 0; i < routes.length; i++) {
                if ((mask >> i & 1) == 0) continue;
                int from = label[routes[i][1]], to = label[routes[i][0]];
                for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
                cost += routes[i][2];
            }
            boolean all = true;
            for (int v = 0; v < n; v++) if (label[v] != label[0]) all = false;
            if (all && (best < 0 || cost < best)) best = cost;
        }
        return best;
    }

    public static void main(String[] args) {
        if (solve(4, new int[][]{{0, 1, 2}, {1, 2, 3}, {0, 2, 1}}) != -1) throw new AssertionError("example 1");
        int big = 2_000_000_000;
        if (solve(5, new int[][]{{0, 1, big}, {1, 2, big}, {2, 3, big}, {3, 4, big}}) != 8_000_000_000L)
            throw new AssertionError("example 2");
        if (solve(1, new int[][]{}) != 0) throw new AssertionError("one village");
        if (solve(2, new int[][]{}) != -1) throw new AssertionError("two villages, no route");
        if (solve(2, new int[][]{{0, 0, 1}, {1, 1, 1}}) != -1) throw new AssertionError("only loops");
        if (solve(2, new int[][]{{0, 1, 0}}) != 0) throw new AssertionError("free pipe is still a connection");

        int wrapped = big + big;
        if (wrapped >= 0 || wrapped != -294_967_296) throw new AssertionError("int sum wraps");
        Integer[] vals = {Integer.MAX_VALUE, -5, 3};
        Arrays.sort(vals, (a, b) -> a - b);
        if (Arrays.equals(vals, new Integer[]{-5, 3, Integer.MAX_VALUE})) throw new AssertionError("subtraction comparator overflows");
        Arrays.sort(vals, (a, b) -> Integer.compare(a, b));
        if (!Arrays.equals(vals, new Integer[]{-5, 3, Integer.MAX_VALUE})) throw new AssertionError("compare is safe");

        Random rnd = new Random(23703);
        int cut = 0;
        for (int t = 0; t < 600; t++) {
            int n = 1 + rnd.nextInt(6);
            int m = rnd.nextInt(9);
            int[][] routes = new int[m][];
            boolean huge = rnd.nextBoolean();
            for (int i = 0; i < m; i++) {
                int price = huge ? big - rnd.nextInt(4) : rnd.nextInt(6);
                routes[i] = new int[]{rnd.nextInt(n), rnd.nextInt(n), price};
            }
            int[][] outer = routes.clone();
            int[][] before = new int[m][];
            for (int i = 0; i < m; i++) before[i] = routes[i].clone();
            long got = solve(n, routes);
            for (int i = 0; i < m; i++) {
                if (routes[i] != outer[i] || !Arrays.equals(routes[i], before[i])) throw new AssertionError("input changed");
            }
            if (got != prim(n, routes)) throw new AssertionError("sweep differs from Prim");
            if (got != bestBySelection(n, routes)) throw new AssertionError("sweep differs from selection");
            if (got == -1) cut++;
            if (huge && got > Integer.MAX_VALUE) {
                if ((int) got == got) throw new AssertionError("a long total must not fit an int");
            }
        }
        if (cut == 0) throw new AssertionError("no disconnected case generated");
    }
}
```

#### Solution: [Recognize] Min Cost To Connect All Points (LeetCode 1584)
<!-- id: ug-min-cost-connect-points -->

**Approach.** Every pair of points is a route priced by Manhattan distance, so the problem is the sweep from the earlier rungs on a complete graph of n(n-1)/2 routes. Each route is packed into one `long` as distance, then the pair of indices, so a plain primitive sort orders them without a comparator or any boxing. The sweep then reads the packed value apart and links the two points when their leaders differ, finishing after n - 1 links. The oracle is Prim's method on a distance matrix, which uses no disjoint set, and a selection-by-selection check covers the smallest inputs. The asserts also confirm the Java claims: the packed distance never spills into the index bits for the largest allowed coordinates, the answer fits an `int` for a full-size input, and the false friend fails, since the n - 1 cheapest pair distances without loop tests leave a far point unreached on a fixed example.

**Complexity.** For n points there are about n^2/2 routes, so sorting costs O(n^2 log n) and the sweep adds O(n^2) leader steps, with O(n^2) memory for the packed array. For 1000 points that is roughly half a million routes, which a primitive `long[]` sort handles easily.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MinCostConnectPointsSolution {
    static int head(int[] chain, int v) {
        while (chain[v] != v) {
            chain[v] = chain[chain[v]];
            v = chain[v];
        }
        return v;
    }

    static int solve(int[][] points) {
        int n = points.length;
        long[] packed = new long[n * (n - 1) / 2];
        int k = 0;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                long dist = Math.abs(points[i][0] - points[j][0]) + Math.abs(points[i][1] - points[j][1]);
                packed[k++] = dist << 20 | (long) i << 10 | j;
            }
        }
        Arrays.sort(packed);
        int[] chain = new int[n];
        for (int v = 0; v < n; v++) chain[v] = v;
        long total = 0;
        int linked = 0;
        for (long p : packed) {
            if (linked == n - 1) break;
            int i = (int) (p >> 10 & 1023), j = (int) (p & 1023);
            int ri = head(chain, i), rj = head(chain, j);
            if (ri == rj) continue;
            chain[ri] = rj;
            total += p >> 20;
            linked++;
        }
        return (int) total;
    }

    static long prim(int[][] pts) {
        int n = pts.length;
        boolean[] in = new boolean[n];
        long[] best = new long[n];
        Arrays.fill(best, Long.MAX_VALUE);
        best[0] = 0;
        long total = 0;
        for (int round = 0; round < n; round++) {
            int pick = -1;
            for (int v = 0; v < n; v++) if (!in[v] && (pick < 0 || best[v] < best[pick])) pick = v;
            in[pick] = true;
            total += best[pick];
            for (int v = 0; v < n; v++) {
                if (in[v]) continue;
                long d = Math.abs(pts[pick][0] - pts[v][0]) + Math.abs(pts[pick][1] - pts[v][1]);
                if (d < best[v]) best[v] = d;
            }
        }
        return total;
    }

    static long bestBySelection(int[][] pts) {
        int n = pts.length;
        int m = n * (n - 1) / 2;
        int[][] routes = new int[m][];
        int k = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                routes[k++] = new int[]{i, j, Math.abs(pts[i][0] - pts[j][0]) + Math.abs(pts[i][1] - pts[j][1])};
        long best = Long.MAX_VALUE;
        for (int mask = 0; mask < (1 << m); mask++) {
            if (Integer.bitCount(mask) != n - 1) continue;
            int[] label = new int[n];
            for (int v = 0; v < n; v++) label[v] = v;
            long cost = 0;
            for (int i = 0; i < m; i++) {
                if ((mask >> i & 1) == 0) continue;
                int from = label[routes[i][1]], to = label[routes[i][0]];
                for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
                cost += routes[i][2];
            }
            boolean all = true;
            for (int v = 0; v < n; v++) if (label[v] != label[0]) all = false;
            if (all) best = Math.min(best, cost);
        }
        return best;
    }

    static boolean cheapestWithoutLoopTest(int[][] pts) {
        int n = pts.length;
        long[] packed = new long[n * (n - 1) / 2];
        int k = 0;
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                packed[k++] = (long) (Math.abs(pts[i][0] - pts[j][0]) + Math.abs(pts[i][1] - pts[j][1])) << 20 | (long) i << 10 | j;
        Arrays.sort(packed);
        int[] label = new int[n];
        for (int v = 0; v < n; v++) label[v] = v;
        for (int e = 0; e < n - 1; e++) {
            int i = (int) (packed[e] >> 10 & 1023), j = (int) (packed[e] & 1023);
            int from = label[j], to = label[i];
            for (int v = 0; v < n; v++) if (label[v] == from) label[v] = to;
        }
        for (int v = 0; v < n; v++) if (label[v] != label[0]) return false;
        return true;
    }

    public static void main(String[] args) {
        if (solve(new int[][]{{0, 0}, {1, 1}, {1, 0}, {-1, 1}}) != 4) throw new AssertionError("example 1");
        if (solve(new int[][]{{3, 12}, {-2, 5}, {-4, 1}}) != 18) throw new AssertionError("example 2");
        if (solve(new int[][]{{5, 5}}) != 0) throw new AssertionError("one point");
        if (solve(new int[][]{{0, 0}, {1000000, 1000000}}) != 2_000_000) throw new AssertionError("two points");

        int[][] square = {{0, 0}, {0, 1}, {1, 0}, {1, 1}, {10, 10}};
        if (cheapestWithoutLoopTest(square)) throw new AssertionError("blind cheapest must leave the far point out");
        if (solve(square) != 3 + 18) throw new AssertionError("sweep reaches the far point");

        long worst = 4_000_000L;
        if ((worst << 20 | 999L << 10 | 999L) >> 20 != worst) throw new AssertionError("distance bits are intact");
        if ((worst << 20) < 0) throw new AssertionError("packed value stays positive");

        Random rnd = new Random(23704);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(5);
            int[][] pts = new int[n][];
            for (int i = 0; i < n; i++) {
                int[] p;
                boolean dup;
                do {
                    p = new int[]{rnd.nextInt(9) - 4, rnd.nextInt(9) - 4};
                    dup = false;
                    for (int j = 0; j < i; j++) if (pts[j][0] == p[0] && pts[j][1] == p[1]) dup = true;
                } while (dup);
                pts[i] = p;
            }
            int[][] copy = new int[n][];
            for (int i = 0; i < n; i++) copy[i] = pts[i].clone();
            int got = solve(pts);
            if (!Arrays.deepEquals(pts, copy)) throw new AssertionError("input changed");
            if (got != prim(pts)) throw new AssertionError("differs from Prim");
            if (got != bestBySelection(pts)) throw new AssertionError("differs from selection");
        }
        for (int t = 0; t < 6; t++) {
            int n = 40 + rnd.nextInt(200);
            int[][] pts = new int[n][];
            java.util.Set<Long> used = new java.util.HashSet<>();
            for (int i = 0; i < n; i++) {
                int x, y;
                do {
                    x = rnd.nextInt(2_000_001) - 1_000_000;
                    y = rnd.nextInt(2_000_001) - 1_000_000;
                } while (!used.add((long) x * 4_000_000L + y));
                pts[i] = new int[]{x, y};
            }
            long want = prim(pts);
            if (want > Integer.MAX_VALUE || solve(pts) != want) throw new AssertionError("large case");
        }
    }
}
```
