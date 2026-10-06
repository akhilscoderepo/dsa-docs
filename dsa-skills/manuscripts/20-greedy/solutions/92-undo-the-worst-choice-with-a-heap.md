<!-- solutions-for: 92-undo-the-worst-choice-with-a-heap -->
### Solutions For Undoing With A Heap

#### Solution: [Build] Furthest Building You Can Reach (LeetCode 1642)
<!-- id: gr-furthest-building -->

**Approach.**
The method walks the heights and handles each positive climb. It adds the climb to a min-heap that holds the climbs covered by a ladder. When the heap holds more climbs than there are ladders, the method pops the smallest climb and pays it with bricks, because the smallest climb saves the fewest bricks when it holds a ladder. If the bricks go below zero, the method stops before the current building. Swapping a ladder from a larger climb to a smaller one never saves bricks, so the heap always holds the largest climbs.

After each building, the heap holds the largest climbs so far, up to the number of ladders, and the bricks pay for all other climbs.

**Complexity.**
- **Time** is O(n log L) for `L` ladders, because each climb costs one push and at most one pop.
- **Space** is O(L) for the heap.

```java run
import java.util.*;

public final class FurthestBuilding {
    /**
     * Returns the largest reachable index.
     * Time: O(n log L). Space: O(L).
     * Invariant: the heap holds the largest climbs so far, at most L of them, and bricks pay for the rest.
     */
    static int furthest(int[] heights, int bricks, int ladders) {
        PriorityQueue<Integer> ladderClimbs = new PriorityQueue<>();   // min-heap of climbs under ladders
        long left = bricks;                                             // bricks as long
        for (int i = 1; i < heights.length; i++) {                      // one building per step
            int climb = heights[i] - heights[i - 1];
            if (climb <= 0) continue;                                   // free move
            ladderClimbs.add(climb);                                    // tentatively use a ladder
            if (ladderClimbs.size() > ladders) left -= ladderClimbs.poll(); // pay for the smallest climb
            if (left < 0) return i - 1;                                 // cannot afford building i
        }
        return heights.length - 1;
    }

    static int brute(int[] h, int bricks, int ladders) {
        int best = 0;
        for (int mask = 0; mask < (1 << Math.max(0, h.length - 1)); mask++) { // each bit: a ladder on climb i
            for (int reach = 0; reach < h.length; reach++) {
                int used = 0;
                long cost = 0;
                boolean ok = true;
                for (int i = 1; i <= reach; i++) {
                    int c = h[i] - h[i - 1];
                    if (c <= 0) continue;
                    if ((mask >> (i - 1) & 1) != 0) used++; else cost += c;
                }
                if (used > ladders || cost > bricks) ok = false;
                if (ok) best = Math.max(best, reach);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (furthest(new int[] {4, 5, 13, 14}, 2, 1) != 3) throw new AssertionError("ex1");
        if (furthest(new int[] {1, 5, 1, 9, 2}, 3, 1) != 2) throw new AssertionError("ex2");
        // One building needs no move, and a large brick count does not overflow.
        if (furthest(new int[] {7}, 0, 0) != 0 || furthest(new int[] {1, 1_000_000}, 1_000_000_000, 0) != 1) throw new AssertionError("edge");
        // Random inputs must match an exhaustive assignment of ladders to climbs.
        Random rnd = new Random(2092);
        for (int t = 0; t < 400; t++) {
            int[] h = new int[1 + rnd.nextInt(7)];
            for (int k = 0; k < h.length; k++) h[k] = 1 + rnd.nextInt(12);
            int bricks = rnd.nextInt(12), ladders = rnd.nextInt(3);
            if (furthest(h, bricks, ladders) != brute(h, bricks, ladders)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Minimum Number of Refueling Stops (LeetCode 871)
<!-- id: gr-refueling-stops -->

**Approach.**
The method treats the target as a final station of no fuel. It keeps a max-heap of the fuel of the stations that the vehicle has passed. When the fuel in the tank does not reach the next position, the method takes the largest passed station and counts a stop. It repeats until the tank reaches the position or the heap is empty, and it returns -1 in the second case. Taking the largest passed amount first reaches farthest with the fewest stops, because any set of stops that reaches a position can swap in a larger passed station and still reach it. The fuel total uses `long`, because the sum of many fuel values passes the `int` range.

After each position, the tank holds the start fuel plus the fuel of the stops taken, and the heap holds the other passed stations.

**Complexity.**
- **Time** is O(n log n), because each station enters and leaves the heap once.
- **Space** is O(n) for the heap.

```java run
import java.util.*;

public final class RefuelingStops {
    /**
     * Returns the fewest stops to reach the target, or -1.
     * Time: O(n log n). Space: O(n).
     * Invariant: tank is the farthest position reached with the stops taken, and the heap holds passed unused fuel.
     */
    static int minStops(int target, int startFuel, int[][] stations) {
        PriorityQueue<Integer> passed = new PriorityQueue<>(Collections.reverseOrder()); // largest first
        long tank = startFuel;                                          // long: sums can pass int
        int stops = 0;
        for (int i = 0; i <= stations.length; i++) {                    // the target is the last position
            long pos = i < stations.length ? stations[i][0] : target;
            while (tank < pos) {                                        // the next position is out of reach
                if (passed.isEmpty()) return -1;
                tank += passed.poll();                                  // take the largest passed station
                stops++;
            }
            if (i < stations.length) passed.add(stations[i][1]);        // this station is now passed
        }
        return stops;
    }

    static int brute(int target, int start, int[][] st) {
        int best = -1;
        for (int mask = 0; mask < (1 << st.length); mask++) {           // every set of stops
            long tank = start;
            boolean ok = true;
            for (int i = 0; i < st.length && ok; i++) {
                if ((mask >> i & 1) != 0) { if (tank < st[i][0]) ok = false; else tank += st[i][1]; }
            }
            if (ok && tank >= target) { int c = Integer.bitCount(mask); if (best < 0 || c < best) best = c; }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minStops(25, 10, new int[][] {{5, 2}, {11, 10}, {20, 5}}) != 3) throw new AssertionError("ex1");
        if (minStops(15, 3, new int[][] {{2, 4}}) != -1) throw new AssertionError("ex2");
        // No stops needed, and large fuel does not overflow.
        if (minStops(5, 5, new int[0][]) != 0 || minStops(2_000_000_000, 1_000_000_000, new int[][] {{1, 1_000_000_000}}) != 1) throw new AssertionError("edge");
        // Random inputs must match exhaustive subsets of stops.
        Random rnd = new Random(2093);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(6);
            int[][] st = new int[n][];
            int p = 0;
            for (int k = 0; k < n; k++) { p += 1 + rnd.nextInt(4); st[k] = new int[] {p, 1 + rnd.nextInt(8)}; }
            int target = p + 1 + rnd.nextInt(6), start = 1 + rnd.nextInt(8);
            if (minStops(target, start, st) != brute(target, start, st)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Course Schedule III (LeetCode 630)
<!-- id: gr-courses-count-and-total -->

**Approach.**
The method uses the scan of lesson 05 and adds the running total to the result. It sorts the courses by last day, adds each duration to a max-heap and to the total, and removes the longest retained duration whenever the total passes the last day. Each removal takes out the largest possible duration, so after every course the total is the smallest total of any largest feasible set of the courses read. The total is a `long`, because durations up to 10^9 add up past the `int` range. The method returns the heap size and the total together.

After each course, the heap holds a largest feasible set with the smallest total, and `total` equals the sum of the heap.

**Complexity.**
- **Time** is O(n log n), because the sort and the heap operations dominate.
- **Space** is O(n) for the heap and the sorted copy.

```java run
import java.util.*;

public final class CoursesCountAndTotal {
    /**
     * Returns {count, total} for the largest feasible set with the smallest total.
     * Time: O(n log n). Space: O(n).
     * Invariant: the heap holds a largest feasible set of the processed courses, and total is its sum.
     */
    static long[] schedule(int[][] courses) {
        int[][] order = courses.clone();
        Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));      // last day first
        PriorityQueue<Integer> kept = new PriorityQueue<>(Collections.reverseOrder());
        long total = 0;
        for (int[] c : order) {                                         // one course per step
            kept.add(c[0]);
            total += c[0];
            if (total > c[1]) total -= kept.poll();                     // remove the longest retained duration
        }
        return new long[] {kept.size(), total};
    }

    static long[] brute(int[][] c) {
        long bestCount = 0, bestTotal = 0;
        for (int mask = 0; mask < (1 << c.length); mask++) {
            List<int[]> pick = new ArrayList<>();
            for (int k = 0; k < c.length; k++) if ((mask >> k & 1) != 0) pick.add(c[k]);
            pick.sort((a, b) -> Integer.compare(a[1], b[1]));
            long t = 0;
            boolean ok = true;
            for (int[] p : pick) { t += p[0]; if (t > p[1]) ok = false; }
            if (!ok) continue;
            if (pick.size() > bestCount || (pick.size() == bestCount && t < bestTotal)) { bestCount = pick.size(); bestTotal = t; }
        }
        return new long[] {bestCount, bestTotal};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(schedule(new int[][] {{5, 5}, {2, 6}, {2, 6}}), new long[] {2, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(schedule(new int[][] {{3, 3}, {4, 3}}), new long[] {1, 3})) throw new AssertionError("ex2");
        // Empty input, and durations near 10^9 sum without overflow.
        if (!Arrays.equals(schedule(new int[0][]), new long[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(schedule(new int[][] {{1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}}), new long[] {1, 1_000_000_000L})) throw new AssertionError("big");
        // Random inputs must match exhaustive subsets, with the smallest total among the largest sets.
        Random rnd = new Random(2094);
        for (int t = 0; t < 500; t++) {
            int[][] c = new int[rnd.nextInt(8)][];
            for (int k = 0; k < c.length; k++) c[k] = new int[] {1 + rnd.nextInt(5), 1 + rnd.nextInt(12)};
            if (!Arrays.equals(schedule(c), brute(c))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] IPO (LeetCode 502)
<!-- id: gr-project-capital -->

**Approach.**
The method sorts the project indices by required capital and keeps a pointer into that order. For each of up to `k` rounds, it pushes every project that the current capital unlocks into a max-heap of profits. It then takes the largest profit from the heap and adds it to the capital. If the heap is empty, no project is available, and the method stops. Taking the largest unlocked profit is safe, because capital only grows, so the project does not hurt later rounds and a larger profit unlocks at least as many projects. The method keeps capital as a `long`.

After each round, the capital is the largest reachable capital after that many projects, and the heap holds the unlocked projects not taken.

**Complexity.**
- **Time** is O(n log n + k log n), because the sort and the heap operations dominate.
- **Space** is O(n) for the index array and the heap.

```java run
import java.util.*;

public final class ProjectCapital {
    /**
     * Returns the largest final capital after at most k projects.
     * Time: O(n log n + k log n). Space: O(n).
     * Invariant: capital is the best after the rounds done, and the heap holds unlocked untaken profits.
     */
    static long maximize(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;
        Integer[] byCapital = new Integer[n];
        for (int i = 0; i < n; i++) byCapital[i] = i;
        Arrays.sort(byCapital, (a, b) -> Integer.compare(capital[a], capital[b])); // cheapest to start first
        PriorityQueue<Integer> unlocked = new PriorityQueue<>(Collections.reverseOrder());
        long cap = w;
        int next = 0;
        for (int round = 0; round < k; round++) {                       // at most k projects
            while (next < n && capital[byCapital[next]] <= cap) unlocked.add(profits[byCapital[next++]]); // unlock by capital
            if (unlocked.isEmpty()) break;                              // nothing can start
            cap += unlocked.poll();                                     // take the largest profit
        }
        return cap;
    }

    static long brute(int k, int w, int[] p, int[] c, boolean[] done) {
        if (k == 0) return w;
        long best = w;
        for (int i = 0; i < p.length; i++) {
            if (!done[i] && c[i] <= w) {
                done[i] = true;
                best = Math.max(best, brute(k - 1, w + p[i], p, c, done));
                done[i] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maximize(2, 0, new int[] {1, 2, 3}, new int[] {0, 1, 1}) != 4) throw new AssertionError("ex1");
        if (maximize(3, 5, new int[] {4, 1}, new int[] {9, 0}) != 6) throw new AssertionError("ex2");
        // No projects, k = 0, and a sum above the int range.
        if (maximize(0, 3, new int[] {5}, new int[] {0}) != 3 || maximize(2, 0, new int[0], new int[0]) != 0) throw new AssertionError("edge");
        if (maximize(2, 0, new int[] {1_000_000_000, 1_000_000_000}, new int[] {0, 0}) != 2_000_000_000L) throw new AssertionError("big");
        // Random inputs must match exhaustive search over project orders.
        Random rnd = new Random(2095);
        for (int t = 0; t < 400; t++) {
            int n = rnd.nextInt(6);
            int[] p = new int[n], c = new int[n];
            for (int i = 0; i < n; i++) { p[i] = rnd.nextInt(6); c[i] = rnd.nextInt(8); }
            int k = rnd.nextInt(4), w = rnd.nextInt(5);
            if (maximize(k, w, p, c) != brute(k, w, p, c, new boolean[n])) throw new AssertionError("random " + t);
        }
    }
}
```
