<!-- solutions-for: 20-greedy -->
### Greedy And Heap

#### Solution: [Build] Furthest Building You Can Reach (LeetCode 1642)
<!-- id: gc-furthest-building -->

**Approach.** Walk the buildings and, for each climb, add it to a min-heap of climbs that currently use a winch. If the heap holds more climbs than there are winches, remove the smallest and pay for it from the timber. If the timber becomes negative, the climb that was just attempted cannot be done and the current index is the answer. Whatever the full road looks like, the timber needed up to a point is the sum of all its climbs minus the largest few, and the heap holds exactly those. The timber is a `long`, since the sum of climbs can pass the `int` range. The assertions check both examples and compare random small roads with the exhaustive recursion that tries timber and a winch at each climb.

**Complexity.** Each climb enters and leaves the heap at most once, so the time is O(n log w) for w winches and the heap holds at most w + 1 entries.

```java run
import java.util.PriorityQueue;
import java.util.Random;

public final class FurthestBuilding {
    static int furthestBuilding(int[] h, long timber, int winches) {
        PriorityQueue<Integer> onWinches = new PriorityQueue<>();
        for (int i = 0; i + 1 < h.length; i++) {
            int climb = h[i + 1] - h[i];
            if (climb <= 0) continue;
            onWinches.add(climb);
            if (onWinches.size() > winches) timber -= onWinches.poll();
            if (timber < 0) return i;
        }
        return h.length - 1;
    }

    static int oracle(int[] h, int i, long timber, int winches) {
        if (i == h.length - 1) return i;
        int climb = h[i + 1] - h[i];
        if (climb <= 0) return oracle(h, i + 1, timber, winches);
        int best = i;
        if (timber >= climb) best = Math.max(best, oracle(h, i + 1, timber - climb, winches));
        if (winches > 0) best = Math.max(best, oracle(h, i + 1, timber, winches - 1));
        return best;
    }

    public static void main(String[] args) {
        if (furthestBuilding(new int[]{3, 9, 4, 6, 2, 12, 8}, 4, 1) != 4) throw new AssertionError("example 1");
        if (furthestBuilding(new int[]{1, 1000000000, 1, 1000000000}, 1999999998L, 0) != 3) throw new AssertionError("example 2");
        if (furthestBuilding(new int[]{5}, 0, 0) != 0) throw new AssertionError("a single building");
        if (furthestBuilding(new int[]{1, 5, 1, 2, 3, 4}, 0, 10) != 5) throw new AssertionError("plenty of winches");
        if (furthestBuilding(new int[]{1, 2}, 0, 0) != 0) throw new AssertionError("no supplies for the first climb");
        if (furthestBuilding(new int[]{9, 8, 7}, 0, 0) != 2) throw new AssertionError("descents are free");
        if (1000000000 + 1000000000 + 1000000000 >= 0) throw new AssertionError("three billions must wrap an int");

        Random rnd = new Random(2701);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] h = new int[n];
            for (int i = 0; i < n; i++) h[i] = 1 + rnd.nextInt(9);
            long timber = rnd.nextInt(12);
            int winches = rnd.nextInt(4);
            if (furthestBuilding(h, timber, winches) != oracle(h, 0, timber, winches)) throw new AssertionError("disagrees with the recursion");
        }
    }
}
```

#### Solution: [Vary] Minimum Number of Refueling Stops (LeetCode 871)
<!-- id: gc-refuel-stops -->

**Approach.** Treat the target as a final depot with no oil. Walk the depots in order. Before a depot or the target at a given position, drive on as long as the fuel allows; while the reach is short of that position, take the largest oil from the pool of depots already passed and count a stop, and answer -1 if the pool is empty. Then add the depot's oil to the pool. Using the largest depot is safe because any plan that reaches the same point with the same number of stops can swap in a larger passed depot. The oracle is a different method, a table of the farthest reach with exactly j stops. The assertions check both examples, the case where the start fuel already reaches the target, and random small instances.

**Complexity.** Each depot is pushed and popped at most once, so the time is O(n log n) and the pool holds at most n values; the oracle takes O(n²).

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class RefuelStops {
    static int refuelStops(long target, long startFuel, long[][] depots) {
        PriorityQueue<Long> pool = new PriorityQueue<>(Comparator.reverseOrder());
        long reach = startFuel;
        int stops = 0;
        for (int i = 0; i <= depots.length; i++) {
            long position = i < depots.length ? depots[i][0] : target;
            while (reach < position) {
                if (pool.isEmpty()) return -1;
                reach += pool.poll();
                stops++;
            }
            if (i < depots.length) pool.add(depots[i][1]);
        }
        return stops;
    }

    static int oracle(long target, long startFuel, long[][] depots) {
        int n = depots.length;
        long[] farthest = new long[n + 2];
        Arrays.fill(farthest, -1);
        farthest[0] = startFuel;
        for (int i = 0; i < n; i++) {
            for (int j = i; j >= 0; j--) {
                if (farthest[j] >= depots[i][0]) farthest[j + 1] = Math.max(farthest[j + 1], farthest[j] + depots[i][1]);
            }
        }
        for (int j = 0; j <= n; j++) if (farthest[j] >= target) return j;
        return -1;
    }

    public static void main(String[] args) {
        if (refuelStops(60, 10, new long[][]{{10, 30}, {20, 10}, {30, 25}, {50, 20}}) != 2) throw new AssertionError("example 1");
        if (refuelStops(100, 1, new long[][]{{10, 100}}) != -1) throw new AssertionError("example 2");
        if (refuelStops(50, 50, new long[0][]) != 0) throw new AssertionError("the start fuel is enough");
        if (refuelStops(50, 49, new long[0][]) != -1) throw new AssertionError("one unit short with no depots");
        if (refuelStops(2000000000L, 1000000000L, new long[][]{{1000000000L, 1000000000L}}) != 1) throw new AssertionError("sums above the int range");

        Random rnd = new Random(2702);
        for (int t = 0; t < 6000; t++) {
            int n = rnd.nextInt(7);
            long target = 5 + rnd.nextInt(40);
            long start = 1 + rnd.nextInt(12);
            long[][] depots = new long[n][];
            long pos = 0;
            for (int i = 0; i < n; i++) {
                pos += 1 + rnd.nextInt(7);
                if (pos >= target) { depots = Arrays.copyOf(depots, i); break; }
                depots[i] = new long[]{pos, 1 + rnd.nextInt(15)};
            }
            if (refuelStops(target, start, depots) != oracle(target, start, depots)) throw new AssertionError("disagrees with the stops table on target " + target + " start " + start + " " + Arrays.deepToString(depots));
        }
    }
}
```

#### Solution: [Boundary] Course Schedule III (LeetCode 630)
<!-- id: gc-course-plan-total -->

**Approach.** Sort a copy by last day and keep a max-heap of the durations of the retained courses together with their total. Add each course. If the total passes its last day, remove the longest duration in the heap, which may be the course just added. Both the count and the total are read from the final state. The count is the best possible, and the total is the smallest among all schedules of that count, because each removal replaces a longer course with a shorter one or drops the newcomer. The assertions check both examples, show that an `int` total of 4000000000 would wrap, and compare random inputs with an enumeration of every feasible subset, taking the largest size and then the smallest total.

**Complexity.** Sorting and heap operations give O(n log n) time with O(n) memory for the heap.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class CoursePlanTotal {
    static long[] bestPlan(int[][] courses) {
        int[][] order = courses.clone();
        Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
        PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());
        long time = 0;
        for (int[] c : order) {
            kept.add(c[0]);
            time += c[0];
            if (time > c[1]) time -= kept.poll();
        }
        return new long[]{kept.size(), time};
    }

    static long[] oracle(int[][] c) {
        int n = c.length;
        int bestCount = 0;
        long bestTotal = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int[][] chosen = new int[Integer.bitCount(mask)][];
            for (int i = 0, k = 0; i < n; i++) if ((mask >> i & 1) == 1) chosen[k++] = c[i];
            Arrays.sort(chosen, (a, b) -> Integer.compare(a[1], b[1]));
            long time = 0;
            boolean ok = true;
            for (int[] x : chosen) { time += x[0]; if (time > x[1]) { ok = false; break; } }
            if (!ok) continue;
            if (chosen.length > bestCount || (chosen.length == bestCount && time < bestTotal)) { bestCount = chosen.length; bestTotal = time; }
        }
        return new long[]{bestCount, bestTotal};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(bestPlan(new int[][]{{7, 7}, {3, 8}, {2, 9}, {4, 13}, {5, 13}}), new long[]{3, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(bestPlan(new int[][]{{2000000000, 2000000000}, {2000000000, 2147483647}}), new long[]{1, 2000000000})) throw new AssertionError("example 2");
        if (!Arrays.equals(bestPlan(new int[0][]), new long[]{0, 0})) throw new AssertionError("no courses");
        if (2000000000 + 2000000000 >= 0) throw new AssertionError("two billions must wrap an int");
        if (!Arrays.equals(bestPlan(new int[][]{{4, 3}}), new long[]{0, 0})) throw new AssertionError("a course longer than its last day");

        Random rnd = new Random(2703);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] c = new int[n][];
            for (int i = 0; i < n; i++) c[i] = new int[]{1 + rnd.nextInt(6), 1 + rnd.nextInt(14)};
            if (!Arrays.equals(bestPlan(c), oracle(c))) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(c));
        }
    }
}
```

#### Solution: [Recognize] IPO (LeetCode 502)
<!-- id: gc-ipo-capital -->

**Approach.** Sort the project indexes by required capital. In each of at most `k` rounds, move every project whose capital is at most the current capital into a max-heap of profits, then take the largest profit and add it to the capital. If the heap is empty, no project is affordable and the loop stops. Capital never decreases, so a project that became affordable stays affordable, which is why the pool only grows. The capital is held in a `long`. The assertions check both examples, then compare random small instances with an exhaustive search over every sequence of at most `k` affordable projects.

**Complexity.** The sort and the heap operations cost O((n + k) log n) time and the heap holds at most n profits.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class IpoCapital {
    static long ipo(int k, long w, int[] profit, int[] capital) {
        Integer[] byCapital = new Integer[profit.length];
        for (int i = 0; i < byCapital.length; i++) byCapital[i] = i;
        Arrays.sort(byCapital, (a, b) -> Integer.compare(capital[a], capital[b]));
        PriorityQueue<Integer> pool = new PriorityQueue<>(Comparator.reverseOrder());
        int next = 0;
        for (int round = 0; round < k; round++) {
            while (next < byCapital.length && capital[byCapital[next]] <= w) pool.add(profit[byCapital[next++]]);
            if (pool.isEmpty()) break;
            w += pool.poll();
        }
        return w;
    }

    static long oracle(int k, long w, int[] profit, int[] capital, boolean[] used) {
        long best = w;
        if (k == 0) return best;
        for (int i = 0; i < profit.length; i++) {
            if (!used[i] && capital[i] <= w) {
                used[i] = true;
                best = Math.max(best, oracle(k - 1, w + profit[i], profit, capital, used));
                used[i] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (ipo(3, 2, new int[]{5, 1, 4, 9, 2}, new int[]{3, 0, 2, 8, 2}) != 20) throw new AssertionError("example 1");
        if (ipo(2, 0, new int[]{7, 3}, new int[]{1, 1}) != 0) throw new AssertionError("example 2");
        if (ipo(0, 5, new int[]{9}, new int[]{0}) != 5) throw new AssertionError("no projects allowed");
        if (ipo(5, 1, new int[]{2}, new int[]{1}) != 3) throw new AssertionError("more rounds than projects");
        if (ipo(2, 1000000000, new int[]{1000000000, 1000000000}, new int[]{1000000000, 0}) != 3000000000L) throw new AssertionError("capital above the int range");

        Random rnd = new Random(2704);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(7);
            int[] profit = new int[n], capital = new int[n];
            for (int i = 0; i < n; i++) { profit[i] = rnd.nextInt(8); capital[i] = rnd.nextInt(10); }
            int k = rnd.nextInt(5);
            long w = rnd.nextInt(6);
            if (ipo(k, w, profit, capital) != oracle(k, w, profit, capital, new boolean[n])) throw new AssertionError("disagrees with the exhaustive search");
        }
    }
}
```
