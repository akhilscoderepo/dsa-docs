<!-- solutions-for: 25-advanced-graph-optimization -->
### Solutions For Floyd Warshall

#### Solution: [Build] Allow One Intermediate (Author exercise)
<!-- id: ga-fw-one-intermediate -->

**Approach.**
The method allocates a new table and fills each entry from the old table. For the pair (i, j), it first checks whether `dist[i][k]` and `dist[k][j]` are both finite. Only then does it form the sum, because adding to `Long.MAX_VALUE` wraps around to a negative number that looks like a bargain. It keeps the smaller of the sum and the stored entry.

The invariant is that every finite entry of the result is the cost of a real route. The sum is a known route to `k` followed by a known route from `k`, so it is a real route. Reading from the old table keeps one call from seeing its own updates, which is the exact meaning of allowing one more intermediate. The input table is never written.

**Complexity.**
- **Time** is O(n^2), because the method visits each of the n squared entries once and does constant work for each.
- **Space** is O(n^2) for the new table, and nothing else grows.

```java run
import java.math.BigInteger;
import java.util.*;

public final class FwOneIntermediate {
    /**
     * Returns a new table in which each pair may also use server k as a stop.
     * Time: O(n^2). Space: O(n^2).
     * Invariant: every finite entry is the cost of a real route.
     */
    static long[][] allowOne(long[][] dist, int k) {
        int n = dist.length;
        // The result is a separate table, so the input stays unchanged.
        long[][] out = new long[n][n];
        // Each row is visited once, which gives n rows of work.
        for (int i = 0; i < n; i++) {
            // Each column is visited once, which gives n squared entries in total.
            for (int j = 0; j < n; j++) {
                // Start from the direct or earlier route.
                out[i][j] = dist[i][j];
                // A missing part means the sum is not a route, and adding to the sentinel would wrap.
                if (dist[i][k] == Long.MAX_VALUE || dist[k][j] == Long.MAX_VALUE) continue;
                // Both parts are finite, so the long sum is exact.
                long through = dist[i][k] + dist[k][j];
                // Only a strictly cheaper route replaces the stored value.
                if (through < out[i][j]) out[i][j] = through;
            }
        }
        // Return the new table.
        return out;
    }

    /** Oracle: the same rule with unbounded integers and no guard tricks. */
    static long[][] oracle(long[][] dist, int k) {
        int n = dist.length;
        long[][] out = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                BigInteger inf = BigInteger.valueOf(Long.MAX_VALUE);
                BigInteger a = BigInteger.valueOf(dist[i][k]);
                BigInteger b = BigInteger.valueOf(dist[k][j]);
                BigInteger cur = BigInteger.valueOf(dist[i][j]);
                // Both parts below the sentinel means a real route exists.
                if (a.compareTo(inf) < 0 && b.compareTo(inf) < 0 && a.add(b).compareTo(cur) < 0) cur = a.add(b);
                out[i][j] = cur.longValueExact();
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        long M = Long.MAX_VALUE;
        long[][] t = {{0, 5, M}, {M, 0, 2}, {1, M, 0}};
        if (!Arrays.deepEquals(allowOne(t, 1), new long[][] {{0, 5, 7}, {M, 0, 2}, {1, M, 0}})) throw new AssertionError("ex1");
        if (!Arrays.deepEquals(allowOne(t, 0), new long[][] {{0, 5, M}, {M, 0, 2}, {1, 6, 0}})) throw new AssertionError("ex2");
        // Java fact: adding one to the sentinel wraps to a negative number.
        if (Long.MAX_VALUE + 1 >= 0) throw new AssertionError("wrap");
        // The input table is unchanged after a call.
        long[][] copy = {{0, 5, M}, {M, 0, 2}, {1, M, 0}};
        allowOne(copy, 1);
        if (!Arrays.deepEquals(copy, t)) throw new AssertionError("mutated");
        // Random tables against the oracle, with sentinels and large entries.
        Random rnd = new Random(2501);
        for (int c = 0; c < 2000; c++) {
            int n = 1 + rnd.nextInt(6);
            long[][] d = new long[n][n];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    d[i][j] = i == j ? 0 : (rnd.nextInt(3) == 0 ? M : (rnd.nextInt(4) == 0 ? 1_000_000_000_000L - rnd.nextInt(3) : rnd.nextInt(20)));
                }
            }
            int k = rnd.nextInt(n);
            if (!Arrays.deepEquals(allowOne(d, k), oracle(d, k))) throw new AssertionError("random " + c);
        }
    }
}
```

#### Solution: [Vary] All-Pairs Table (Author exercise)
<!-- id: ga-fw-prefix-table -->

**Approach.**
The method builds the table of direct edges with zeros on the diagonal, keeping the lowest weight for repeated edges. It then runs the round for server 0, then for server 1, and so on, and it stops after `m` rounds. The last step converts each remaining sentinel to minus one.

The invariant is that after the round for server `k`, each entry holds the lowest cost of a route whose intermediates all have an index of at most `k`. After `m` rounds, the intermediates are exactly the servers below `m`, which matches the contract. A route that stops at `k` splits into two parts that use only smaller intermediates, so one comparison per pair is enough. The conversion happens at the end, because minus one would break the comparisons.

**Complexity.**
- **Time** is O(m * n^2), because each of the m rounds visits every pair once.
- **Space** is O(n^2) for the table.

```java run
import java.util.*;

public final class FwPrefixTable {
    /**
     * Returns lowest route costs when only servers below m may act as stops.
     * Time: O(m * n^2). Space: O(n^2).
     * Invariant: after the round for k, intermediates are limited to 0..k.
     */
    static long[][] prefixTable(int n, int[][] edges, int m) {
        long[][] dist = new long[n][n];
        // Every pair starts with the sentinel, which means no known route.
        for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE);
        // A server reaches itself at cost zero.
        for (int v = 0; v < n; v++) dist[v][v] = 0;
        // Direct edges fill the table, and the lowest weight wins for repeats.
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
        // The outermost loop adds one allowed intermediate per round, and it stops at m.
        for (int k = 0; k < m; k++) {
            // The row index i is the first server of the pair.
            for (int i = 0; i < n; i++) {
                // Without a route to k, no sum for this row exists.
                if (dist[i][k] == Long.MAX_VALUE) continue;
                // The column index j is the last server of the pair.
                for (int j = 0; j < n; j++) {
                    // Without a route from k, the sum is not a route.
                    if (dist[k][j] == Long.MAX_VALUE) continue;
                    // Both parts are finite, so this long sum is exact.
                    long through = dist[i][k] + dist[k][j];
                    // Keep the cheaper route, which preserves the invariant.
                    if (through < dist[i][j]) dist[i][j] = through;
                }
            }
        }
        // The sentinel becomes minus one only after all comparisons are done.
        for (long[] row : dist) for (int j = 0; j < n; j++) if (row[j] == Long.MAX_VALUE) row[j] = -1;
        // Return the finished table.
        return dist;
    }

    /** Oracle: depth-first search over simple routes with stops restricted to indices below m. */
    static long[][] oracle(int n, int[][] edges, int m) {
        long[][] out = new long[n][n];
        for (int a = 0; a < n; a++) {
            for (int b = 0; b < n; b++) {
                boolean[] used = new boolean[n];
                used[a] = true;
                out[a][b] = a == b ? 0 : walk(n, edges, m, used, a, b, 0);
            }
        }
        return out;
    }

    static long walk(int n, int[][] edges, int m, boolean[] used, int at, int goal, long cost) {
        long best = -1;
        for (int[] e : edges) {
            if (e[0] != at || used[e[1]]) continue;
            long next = cost + e[2];
            if (e[1] == goal) {
                if (best == -1 || next < best) best = next;
                continue;
            }
            // A stop must have an index below m.
            if (e[1] >= m) continue;
            used[e[1]] = true;
            long sub = walk(n, edges, m, used, e[1], goal, next);
            used[e[1]] = false;
            if (sub != -1 && (best == -1 || sub < best)) best = sub;
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        int[][] g = {{0, 1, 1}, {1, 2, 1}, {2, 3, 1}, {0, 3, 9}};
        long[][] a = {{0, 1, 2, 9}, {-1, 0, 1, -1}, {-1, -1, 0, 1}, {-1, -1, -1, 0}};
        if (!Arrays.deepEquals(prefixTable(4, g, 2), a)) throw new AssertionError("ex1");
        long[][] b = {{0, 1, 2, 3}, {-1, 0, 1, 2}, {-1, -1, 0, 1}, {-1, -1, -1, 0}};
        if (!Arrays.deepEquals(prefixTable(4, g, 4), b)) throw new AssertionError("ex2");
        // With m equal to zero the table holds only direct edges.
        if (prefixTable(4, g, 0)[0][2] != -1) throw new AssertionError("m zero");
        // Random graphs with zero weights, repeats and self loops, for every limit m.
        Random rnd = new Random(2502);
        for (int c = 0; c < 1500; c++) {
            int n = 1 + rnd.nextInt(6);
            int cnt = rnd.nextInt(12);
            int[][] edges = new int[cnt][];
            for (int i = 0; i < cnt; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(5)};
            int m = rnd.nextInt(n + 1);
            if (!Arrays.deepEquals(prefixTable(n, edges, m), oracle(n, edges, m))) throw new AssertionError("random " + c);
        }
    }
}
```

#### Solution: [Boundary] Infinity Arithmetic (Author exercise)
<!-- id: ga-fw-infinity-arith -->

**Approach.**
The method runs the three loops of this lesson on a `long` table whose missing routes hold `Long.MAX_VALUE`. Before it forms any sum, it checks both parts against the sentinel, so the sentinel never takes part in arithmetic. After the loops finish, it scans each ordered pair of different servers. A finite entry updates the largest value, and a sentinel entry adds one to the count of missing routes.

The invariant is that every finite entry is the cost of a real route and the sentinel marks a pair with no route yet. The largest possible distance is below 100 times two billion, about 2 times 10 to the 11, so `long` holds it. A smaller type fails here: two weights of two billion already exceed the range of `int`, and a sentinel such as `Integer.MAX_VALUE` plus any weight wraps negative.

**Complexity.**
- **Time** is O(n^3) for the three nested loops, plus O(m) to read the m edges and O(n^2) for the final scan.
- **Space** is O(n^2) for the table.

```java run
import java.util.*;

public final class FwInfinityArith {
    /**
     * Returns the largest finite distance and the number of ordered pairs with no route.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: the sentinel never appears in a sum.
     */
    static long[] summary(int n, int[][] edges) {
        long[][] dist = new long[n][n];
        // Missing routes hold the sentinel, which is the largest long.
        for (long[] row : dist) Arrays.fill(row, Long.MAX_VALUE);
        // Each server reaches itself at cost zero.
        for (int v = 0; v < n; v++) dist[v][v] = 0;
        // Direct edges fill the table with the lowest weight for repeats.
        for (int[] e : edges) dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
        // Server k is the newest allowed intermediate in this round.
        for (int k = 0; k < n; k++) {
            // The first server of the pair.
            for (int i = 0; i < n; i++) {
                // A missing route to k makes every sum in this row invalid.
                if (dist[i][k] == Long.MAX_VALUE) continue;
                // The last server of the pair.
                for (int j = 0; j < n; j++) {
                    // A missing route from k makes the sum invalid.
                    if (dist[k][j] == Long.MAX_VALUE) continue;
                    // Both parts are finite, and the long sum cannot wrap here.
                    long through = dist[i][k] + dist[k][j];
                    // Keep the cheaper route.
                    if (through < dist[i][j]) dist[i][j] = through;
                }
            }
        }
        long largest = 0;
        long missing = 0;
        // Scan every ordered pair of different servers once.
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                // Pairs of one server with itself are not counted.
                if (i == j) continue;
                // A sentinel counts as a missing route, and a finite value can raise the maximum.
                if (dist[i][j] == Long.MAX_VALUE) missing++;
                else largest = Math.max(largest, dist[i][j]);
            }
        }
        // Return both values in the order of the contract.
        return new long[] {largest, missing};
    }

    /** Oracle: repeated passes over all edges from every source, until nothing improves. */
    static long[] oracle(int n, int[][] edges) {
        long largest = 0;
        long missing = 0;
        for (int s = 0; s < n; s++) {
            long[] d = new long[n];
            Arrays.fill(d, -1);
            d[s] = 0;
            boolean changed = true;
            while (changed) {
                changed = false;
                for (int[] e : edges) {
                    if (d[e[0]] >= 0 && (d[e[1]] == -1 || d[e[0]] + e[2] < d[e[1]])) {
                        d[e[1]] = d[e[0]] + e[2];
                        changed = true;
                    }
                }
            }
            for (int t = 0; t < n; t++) {
                if (t == s) continue;
                if (d[t] == -1) missing++;
                else largest = Math.max(largest, d[t]);
            }
        }
        return new long[] {largest, missing};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(summary(3, new int[][] {{0, 1, 2_000_000_000}, {1, 2, 2_000_000_000}}), new long[] {4_000_000_000L, 3})) throw new AssertionError("ex1");
        if (!Arrays.equals(summary(2, new int[][] {}), new long[] {0, 2})) throw new AssertionError("ex2");
        // Java facts: the sentinel plus one wraps, and an int sum of two large weights wraps.
        if (Long.MAX_VALUE + 1 >= 0) throw new AssertionError("long wrap");
        int wrapped = 2_000_000_000 + 2_000_000_000;
        if (wrapped >= 0) throw new AssertionError("int wrap");
        // A sentinel of Integer.MAX_VALUE plus a large weight also wraps negative in int arithmetic.
        int bad = Integer.MAX_VALUE + 2_000_000_000;
        if (bad >= 0) throw new AssertionError("int sentinel");
        // Random graphs with weights near the maximum and many missing routes.
        Random rnd = new Random(2503);
        for (int c = 0; c < 1500; c++) {
            int n = 1 + rnd.nextInt(7);
            int cnt = rnd.nextInt(12);
            int[][] edges = new int[cnt][];
            for (int i = 0; i < cnt; i++) edges[i] = new int[] {rnd.nextInt(n), rnd.nextInt(n), rnd.nextInt(2) == 0 ? 2_000_000_000 - rnd.nextInt(3) : rnd.nextInt(6)};
            if (!Arrays.equals(summary(n, edges), oracle(n, edges))) throw new AssertionError("random " + c);
        }
    }
}
```

#### Solution: [Recognize] Find the City With the Smallest Number of Neighbors at a Threshold Distance (LeetCode 1334)
<!-- id: ga-fw-city-threshold -->

**Approach.**
The cue is a question about distances between all pairs of cities on a graph with at most 100 cities. The method fills a distance table with the three loops of this lesson. Each undirected road writes the weight into both directions of the table, because one road serves both ways. After the loops, it counts for each city the other cities with a finite distance of at most the threshold. It keeps the city with the smallest count, and a strict comparison keeps the earlier, smaller index on a tie.

The invariant is that after the round for `k`, each entry is the lowest cost of a route with intermediates 0 to `k`. The usual statement lets a tie go to the greatest index. This contract sends it to the smallest index and also returns the count, so the scan runs in increasing city order with a strict less-than test. Distances stay below 100 times 10000, so `int` holds them. The method never adds the sentinel, because it tests both parts first.

**Complexity.**
- **Time** is O(n^3) for the table and O(n^2) for the counting scan.
- **Space** is O(n^2) for the table.

```java run
import java.util.*;

public final class FwCityThreshold {
    /**
     * Returns {city, neighbor count} with the fewest neighbors, and the smallest index on a tie.
     * Time: O(n^3). Space: O(n^2).
     * Invariant: after the round for k, intermediates are limited to 0..k.
     */
    static int[] pick(int n, int[][] edges, int threshold) {
        final int NONE = Integer.MAX_VALUE;
        int[][] dist = new int[n][n];
        // Every pair starts with no known route.
        for (int[] row : dist) Arrays.fill(row, NONE);
        // A city reaches itself at cost zero.
        for (int v = 0; v < n; v++) dist[v][v] = 0;
        // A road is two-way, so it fills both table entries.
        for (int[] e : edges) {
            dist[e[0]][e[1]] = Math.min(dist[e[0]][e[1]], e[2]);
            dist[e[1]][e[0]] = Math.min(dist[e[1]][e[0]], e[2]);
        }
        // The outermost loop adds one allowed intermediate city per round.
        for (int k = 0; k < n; k++) {
            // First city of the pair.
            for (int i = 0; i < n; i++) {
                // The sentinel is never added to anything.
                if (dist[i][k] == NONE) continue;
                // Last city of the pair.
                for (int j = 0; j < n; j++) {
                    if (dist[k][j] == NONE) continue;
                    // Both parts are finite, and the sum stays far below the int limit.
                    int through = dist[i][k] + dist[k][j];
                    // Keep the cheaper route.
                    if (through < dist[i][j]) dist[i][j] = through;
                }
            }
        }
        int bestCity = -1;
        int bestCount = Integer.MAX_VALUE;
        // Cities are scanned in increasing order, so a strict test keeps the smaller index on a tie.
        for (int c = 0; c < n; c++) {
            int count = 0;
            // Count other cities within the threshold, skipping the sentinel by the comparison itself.
            for (int j = 0; j < n; j++) if (j != c && dist[c][j] <= threshold) count++;
            // A strictly smaller count replaces the current best.
            if (count < bestCount) {
                bestCount = count;
                bestCity = c;
            }
        }
        // Return the city and its neighbor count.
        return new int[] {bestCity, bestCount};
    }

    /** Oracle: repeated passes over all roads from every source, then the same counting rule. */
    static int[] oracle(int n, int[][] edges, int threshold) {
        int bestCity = -1;
        int bestCount = Integer.MAX_VALUE;
        for (int s = 0; s < n; s++) {
            long[] d = new long[n];
            Arrays.fill(d, -1);
            d[s] = 0;
            boolean changed = true;
            while (changed) {
                changed = false;
                for (int[] e : edges) {
                    for (int dir = 0; dir < 2; dir++) {
                        int a = dir == 0 ? e[0] : e[1];
                        int b = dir == 0 ? e[1] : e[0];
                        if (d[a] >= 0 && (d[b] == -1 || d[a] + e[2] < d[b])) {
                            d[b] = d[a] + e[2];
                            changed = true;
                        }
                    }
                }
            }
            int count = 0;
            for (int t = 0; t < n; t++) if (t != s && d[t] != -1 && d[t] <= threshold) count++;
            if (count < bestCount) {
                bestCount = count;
                bestCity = s;
            }
        }
        return new int[] {bestCity, bestCount};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(pick(4, new int[][] {{0, 1, 3}, {1, 2, 1}, {1, 3, 4}, {2, 3, 1}}, 4), new int[] {0, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(pick(4, new int[][] {{0, 1, 1}, {2, 3, 1}}, 1), new int[] {0, 1})) throw new AssertionError("ex2");
        // Java fact: an int sentinel added to a positive weight would wrap, which the guard avoids.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("wrap");
        // Random connected-or-not graphs with distinct pairs, against the oracle.
        Random rnd = new Random(2504);
        for (int c = 0; c < 2000; c++) {
            int n = 2 + rnd.nextInt(6);
            List<int[]> list = new ArrayList<>();
            for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) if (rnd.nextInt(3) == 0) list.add(new int[] {a, b, 1 + rnd.nextInt(6)});
            // The contract needs at least one road.
            if (list.isEmpty()) list.add(new int[] {0, 1, 1 + rnd.nextInt(6)});
            int[][] edges = list.toArray(new int[0][]);
            int threshold = 1 + rnd.nextInt(10);
            if (!Arrays.equals(pick(n, edges, threshold), oracle(n, edges, threshold))) throw new AssertionError("random " + c);
        }
    }
}
```
