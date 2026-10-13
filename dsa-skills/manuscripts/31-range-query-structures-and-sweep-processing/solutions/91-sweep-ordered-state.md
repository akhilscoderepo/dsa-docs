<!-- solutions-for: 91-sweep-ordered-state -->
### Solutions For Sweep And Ordered State

#### Solution: [Build] First Overloaded Stop (LeetCode 1094)
<!-- id: rq31-first-overload-stop -->

**Approach.** The solution stores one net change per coordinate in a sorted map and reads the map in key order.

Each trip adds `+passengers` at `from` and `-passengers` at `to`. The map merges every change at one coordinate into a single value, so equal coordinates are already grouped. The sweep then adds the values in increasing key order. After adding the value for key `x`, the running load equals the load on the span that starts at `x`. The first key whose running load exceeds the capacity is the answer, because the load cannot change between two keys. A trip that ends at `x` and a trip that starts at `x` cancel inside one merged value, which implements the half-open rule. The sum uses `long`, so the totals stay safe even when the limits grow.

**Complexity.**

- **Time** is O(n log n), because the map performs 2n merges at O(log n) each and the sweep visits at most 2n keys.
- **Space** is O(n), because the map holds at most one entry per distinct coordinate, which is at most 2n.

```java run
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class FirstOverloadStop {
    /**
     * Returns the smallest coordinate whose load exceeds the capacity, or -1.
     * Time: O(n log n), because each of the 2n merges costs O(log n) and the sweep reads 2n keys.
     * Space: O(n), because the map keeps one net change per distinct coordinate.
     * Invariant: after key x is applied, load equals the passengers seated on the span starting at x.
     */
    static int firstOverload(int[][] trips, int capacity) {
        // The map keeps coordinates sorted and merges equal coordinates into one net change.
        TreeMap<Integer, Long> change = new TreeMap<>();
        // One pass over the trips costs O(n) iterations.
        for (int[] t : trips) {
            // Boarding raises the load at the start coordinate; merge costs O(log n).
            change.merge(t[1], (long) t[0], Long::sum);
            // Leaving lowers the load at the end coordinate, so the seat is free from that coordinate on.
            change.merge(t[2], -(long) t[0], Long::sum);
        }
        // The running load is a long so that large passenger counts cannot overflow it.
        long load = 0;
        // Entries arrive in increasing coordinate order, which is the sweep order.
        for (Map.Entry<Integer, Long> e : change.entrySet()) {
            // Apply the whole merged change for this coordinate before looking at the load.
            load += e.getValue();
            // The load is constant until the next key, so the first key above capacity is the first bad coordinate.
            if (load > capacity) return e.getKey();
        }
        // No span exceeded the capacity.
        return -1;
    }

    /** Brute-force oracle that evaluates every integer coordinate in range. */
    static int oracle(int[][] trips, int capacity) {
        // Scan each integer coordinate from 0 to the largest end.
        for (int x = 0; x <= 60; x++) {
            // Recompute the load at x from scratch.
            long load = 0;
            // A trip occupies x when from <= x < to.
            for (int[] t : trips) if (t[1] <= x && x < t[2]) load += t[0];
            // The first exceeding coordinate is the answer.
            if (load > capacity) return x;
        }
        // Nothing exceeded the capacity.
        return -1;
    }

    public static void main(String[] args) {
        // Checks Example 1: the load reaches 5 at coordinate 3.
        if (firstOverload(new int[][]{{2, 1, 5}, {3, 3, 7}, {4, 5, 9}}, 4) != 3) throw new AssertionError("example 1");
        // Checks Example 2: a trip that ends at 4 frees its seats for the trip that starts at 4.
        if (firstOverload(new int[][]{{3, 1, 4}, {3, 4, 7}}, 3) != -1) throw new AssertionError("example 2");
        // Checks the lesson trace input: the net change at coordinate 4 is zero and the overload starts at 6.
        if (firstOverload(new int[][]{{2, 1, 4}, {1, 2, 6}, {2, 4, 8}, {3, 6, 9}}, 4) != 6) throw new AssertionError("trace input");
        // Checks 2000 random inputs against the oracle with a fixed seed.
        Random rnd = new Random(9101L);
        for (int iter = 0; iter < 2000; iter++) {
            // Build a random trip list with 1 to 6 trips on small coordinates.
            int n = 1 + rnd.nextInt(6);
            int[][] trips = new int[n][];
            for (int i = 0; i < n; i++) {
                int from = rnd.nextInt(40), to = from + 1 + rnd.nextInt(15);
                trips[i] = new int[]{1 + rnd.nextInt(5), from, to};
            }
            int cap = 1 + rnd.nextInt(10);
            if (firstOverload(trips, cap) != oracle(trips, cap)) throw new AssertionError("random mismatch at " + iter);
        }
    }
}
```

#### Solution: [Vary] Tallest Stretch Of A Skyline (LeetCode 218)
<!-- id: rq31-skyline-tallest -->

**Approach.** The sweep keeps the heights of active buildings in a sorted map from height to count.

Events are grouped by coordinate. At each coordinate the sweep first applies every start and every end, and only then reads the greatest key of the map. That tie policy matters for two touching buildings, because the end of one and the start of the next must not produce a false drop. Removal decrements the count and deletes the key when the count reaches zero, so equal heights are not lost when only one of them ends.

After each coordinate the current height is the greatest key, or 0 when the map is empty. A height above the best so far starts a new best stretch at that coordinate and marks it open. The first later coordinate whose height is below the best closes the stretch. Because all heights are positive and the last end empties the map, the stretch always closes.

**Complexity.**

- **Time** is O(n log n), because sorting the coordinates and the map updates cost O(log n) per event over 2n events.
- **Space** is O(n), because the event table and the height map hold at most 2n and n entries.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;

public final class SkylineTallest {
    /**
     * Returns {greatest height, leftmost coordinate with it, first coordinate where it ends}.
     * Time: O(n log n), because there are 2n events and each map update costs O(log n).
     * Space: O(n), because events and active heights are stored.
     * Invariant: after all events at x are applied, the greatest key is the skyline height on [x, next event).
     */
    static int[] tallest(int[][] buildings) {
        // Events are grouped by coordinate; each value lists {height, +1 for start or -1 for end}.
        TreeMap<Integer, List<int[]>> events = new TreeMap<>();
        // One pass over the buildings costs O(n) iterations.
        for (int[] b : buildings) {
            // The start event adds the height to the active set at the left coordinate.
            events.computeIfAbsent(b[0], k -> new ArrayList<>()).add(new int[]{b[2], 1});
            // The end event removes it at the right coordinate, so the building covers [left, right).
            events.computeIfAbsent(b[1], k -> new ArrayList<>()).add(new int[]{b[2], -1});
        }
        // Active heights map to the number of active buildings with that height.
        TreeMap<Integer, Integer> active = new TreeMap<>();
        // The best stretch starts empty; endX stays -1 while the stretch is open.
        int bestH = 0, bestX = -1, endX = -1;
        // A flag that says the best stretch has not yet closed.
        boolean open = false;
        // Visit coordinates in increasing order, which is the sweep order.
        for (var entry : events.entrySet()) {
            // Apply every event at this coordinate before reading the height, so ties cannot create a false drop.
            for (int[] ev : entry.getValue()) {
                if (ev[1] == 1) {
                    // A start increments the count for its height.
                    active.merge(ev[0], 1, Integer::sum);
                } else {
                    // An end decrements the count; the key goes away only when the count reaches zero.
                    int left = active.get(ev[0]) - 1;
                    if (left == 0) active.remove(ev[0]); else active.put(ev[0], left);
                }
            }
            // The skyline height is the greatest active height, or 0 when nothing is active.
            int h = active.isEmpty() ? 0 : active.lastKey();
            // A strictly greater height starts a new best stretch at this coordinate.
            if (h > bestH) { bestH = h; bestX = entry.getKey(); endX = -1; open = true; }
            // The first lower height after the best stretch began closes it.
            else if (open && h < bestH) { endX = entry.getKey(); open = false; }
        }
        // Return the three values the contract asks for.
        return new int[]{bestH, bestX, endX};
    }

    /** Brute-force oracle that computes the height at every integer coordinate. */
    static int[] oracle(int[][] buildings) {
        // Heights for coordinates 0..59 are enough for the random inputs.
        int[] h = new int[60];
        // Each coordinate takes the maximum height of the buildings covering it.
        for (int x = 0; x < 60; x++) for (int[] b : buildings) if (b[0] <= x && x < b[1]) h[x] = Math.max(h[x], b[2]);
        // Find the greatest height.
        int m = 0;
        for (int v : h) m = Math.max(m, v);
        // The leftmost coordinate with that height starts the stretch.
        int s = 0;
        while (h[s] != m) s++;
        // The stretch ends at the first later coordinate below the greatest height.
        int e = s;
        while (h[e] == m) e++;
        // Return the same triple as the sweep.
        return new int[]{m, s, e};
    }

    public static void main(String[] args) {
        // Checks Example 1: height 15 starts at coordinate 3 and ends at 7.
        int[][] ex1 = {{2, 9, 10}, {3, 7, 15}, {5, 12, 12}, {15, 20, 10}, {19, 24, 8}};
        if (!java.util.Arrays.equals(tallest(ex1), new int[]{15, 3, 7})) throw new AssertionError("example 1");
        // Checks Example 2: two buildings of equal height keep the stretch alive when one of them ends.
        if (!java.util.Arrays.equals(tallest(new int[][]{{1, 4, 6}, {2, 3, 6}}), new int[]{6, 1, 4})) throw new AssertionError("example 2");
        // Checks the touching case: the end at 3 and the start at 3 give one stretch from 1 to 5.
        if (!java.util.Arrays.equals(tallest(new int[][]{{1, 3, 4}, {3, 5, 4}}), new int[]{4, 1, 5})) throw new AssertionError("touching");
        // Checks the lesson trace input.
        if (!java.util.Arrays.equals(tallest(new int[][]{{1, 6, 3}, {4, 9, 5}, {6, 8, 2}, {8, 11, 5}}), new int[]{5, 4, 11})) throw new AssertionError("trace input");
        // Checks 2000 random inputs against the oracle with a fixed seed.
        Random rnd = new Random(9102L);
        for (int iter = 0; iter < 2000; iter++) {
            int n = 1 + rnd.nextInt(6);
            int[][] bs = new int[n][];
            for (int i = 0; i < n; i++) {
                int l = rnd.nextInt(40);
                bs[i] = new int[]{l, l + 1 + rnd.nextInt(15), 1 + rnd.nextInt(6)};
            }
            if (!java.util.Arrays.equals(tallest(bs), oracle(bs))) throw new AssertionError("random mismatch at " + iter);
        }
    }
}
```

#### Solution: [Boundary] Equal-Coordinate Events (Author exercise)
<!-- id: rq31-equal-coordinate-events -->

**Approach.** The solution turns each interval into two events and sorts them with a tie rule that depends on the interval kind.

For half-open intervals, an end at coordinate `x` must come before a start at `x`, because the ended interval no longer contains `x`. For closed intervals, a start at `x` must come before an end at `x`, because the ending interval still contains `x`. The comparator sorts by coordinate first and by the delta sign second, with the sign order reversed between the two kinds. The sweep adds each delta and records the largest running load after every event. An empty half-open interval, where `start == end`, contains no coordinate, so the solution skips it.

The invariant is that the running load after any prefix of events never exceeds the true overlap at the coordinate being processed, and it equals the true overlap after the last event at that coordinate. The tie rule makes the first part hold.

**Complexity.**

- **Time** is O(n log n), because sorting 2n events dominates and the sweep is linear.
- **Space** is O(n), because the event table holds 2n pairs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class EqualCoordinateEvents {
    /**
     * Returns the largest number of intervals that contain one common integer coordinate.
     * Time: O(n log n), because sorting 2n events dominates the linear sweep.
     * Space: O(n), because the event table holds two entries per interval.
     * Invariant: with the tie rule applied, the running load equals the overlap after each event.
     */
    static int maxOverlap(int[][] intervals, boolean closed) {
        // Events are {coordinate, delta}; two per interval.
        int[][] ev = new int[intervals.length * 2][];
        // Count of events actually created, because empty half-open intervals add none.
        int m = 0;
        // One pass over the intervals costs O(n) iterations.
        for (int[] iv : intervals) {
            // An empty half-open interval contains no coordinate, so it creates no events.
            if (!closed && iv[0] == iv[1]) continue;
            // The start raises the load by one.
            ev[m++] = new int[]{iv[0], 1};
            // The end lowers the load by one.
            ev[m++] = new int[]{iv[1], -1};
        }
        // Sort by coordinate, then by delta sign according to the interval kind; this is the O(n log n) step.
        Arrays.sort(ev, 0, m, (a, b) -> {
            // Different coordinates sort by coordinate alone.
            if (a[0] != b[0]) return Integer.compare(a[0], b[0]);
            // Closed intervals put starts (+1) first; half-open intervals put ends (-1) first.
            return closed ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1]);
        });
        // The running load and the best load seen so far.
        int load = 0, best = 0;
        // Apply events in sorted order, which is the sweep order.
        for (int i = 0; i < m; i++) {
            // Each event changes the load by its delta.
            load += ev[i][1];
            // Track the largest load after any event.
            best = Math.max(best, load);
        }
        // Return the largest overlap.
        return best;
    }

    /** Brute-force oracle that counts containing intervals at every integer coordinate. */
    static int oracle(int[][] intervals, boolean closed) {
        // The best count over all coordinates.
        int best = 0;
        // Coordinates 0..59 cover the random inputs.
        for (int x = 0; x < 60; x++) {
            // Count the intervals that contain x under the chosen kind.
            int c = 0;
            for (int[] iv : intervals) if (closed ? (iv[0] <= x && x <= iv[1]) : (iv[0] <= x && x < iv[1])) c++;
            best = Math.max(best, c);
        }
        // Return the best count.
        return best;
    }

    public static void main(String[] args) {
        // Checks Example 1: touching intervals overlap only when the ends are included.
        int[][] touching = {{1, 3}, {3, 5}};
        if (maxOverlap(touching, false) != 1) throw new AssertionError("half-open touching");
        if (maxOverlap(touching, true) != 2) throw new AssertionError("closed touching");
        // Checks Example 2: the zero-length interval counts only when the ends are included.
        int[][] mixed = {{2, 6}, {6, 9}, {4, 6}, {6, 6}};
        if (maxOverlap(mixed, false) != 2) throw new AssertionError("half-open mixed");
        if (maxOverlap(mixed, true) != 4) throw new AssertionError("closed mixed");
        // Checks 3000 random inputs for both kinds against the oracle with a fixed seed.
        Random rnd = new Random(9103L);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(7);
            int[][] iv = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(30);
                iv[i] = new int[]{s, s + rnd.nextInt(10)};
            }
            if (maxOverlap(iv, false) != oracle(iv, false)) throw new AssertionError("half-open mismatch at " + iter);
            if (maxOverlap(iv, true) != oracle(iv, true)) throw new AssertionError("closed mismatch at " + iter);
        }
    }
}
```

#### Solution: [Recognize] Busiest Moment After Each Booking (LeetCode 732)
<!-- id: rq31-calendar-busiest -->

**Approach.** The class keeps one sorted map of net changes and rescans it after every booking.

A booking `[start, end)` adds `+1` at `start` and `-1` at `end`. Equal coordinates merge into one value, so a booking that ends where another begins does not overlap it. After the update, a sweep over the map adds the values in key order. The running sum equals the number of bookings active on the span that starts at each key. The sweep keeps the largest sum and the first key where that sum is reached. A strict comparison keeps the leftmost key.

The rescan visits every key, so each booking costs time linear in the number of bookings so far. A segment tree with lazy updates would lower that cost, but it needs the compressed coordinate set in advance.

**Complexity.**

- **Time** is O(n) per booking and O(n^2) for n bookings, because each booking performs two O(log n) merges and one pass over up to 2n keys.
- **Space** is O(n), because the map holds one entry per distinct boundary.

```java run
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;

public final class CalendarBusiest {
    /** Net change in the number of active bookings, keyed by coordinate. */
    private final TreeMap<Integer, Integer> change = new TreeMap<>();

    /**
     * Adds the booking [start, end) and returns {largest overlap, leftmost coordinate reaching it}.
     * Time: O(n) per call, because two merges cost O(log n) and the rescan visits up to 2n keys.
     * Space: O(1) extra per call, because only counters are kept besides the map.
     * Invariant: the prefix sum of the map up to key x equals the bookings active on [x, next key).
     */
    int[] book(int start, int end) {
        // The booking becomes active at start.
        change.merge(start, 1, Integer::sum);
        // The booking stops being active at end, so the interval is half-open.
        change.merge(end, -1, Integer::sum);
        // Running overlap, the best overlap and the coordinate where the best first appears.
        int run = 0, best = 0, at = start;
        // Visit keys in increasing order; the cost is linear in the number of keys.
        for (Map.Entry<Integer, Integer> e : change.entrySet()) {
            // Add the merged change for this coordinate.
            run += e.getValue();
            // A strictly greater overlap records the key, so ties keep the leftmost key.
            if (run > best) { best = run; at = e.getKey(); }
        }
        // Return the pair the contract asks for.
        return new int[]{best, at};
    }

    /** Brute-force oracle that rescans every integer coordinate over a list of bookings. */
    static int[] oracleAfter(List<int[]> bookings) {
        // Best overlap and the leftmost coordinate that reaches it.
        int best = 0, at = 0;
        // Coordinates 0..59 cover the random inputs.
        for (int x = 0; x < 60; x++) {
            // Count bookings containing x.
            int c = 0;
            for (int[] b : bookings) if (b[0] <= x && x < b[1]) c++;
            // Strict comparison keeps the leftmost coordinate.
            if (c > best) { best = c; at = x; }
        }
        // Return the pair.
        return new int[]{best, at};
    }

    public static void main(String[] args) {
        // Checks Example 1: results after each of four bookings.
        CalendarBusiest c1 = new CalendarBusiest();
        int[][] in1 = {{4, 8}, {8, 12}, {6, 10}, {1, 5}};
        int[][] out1 = {{1, 4}, {1, 4}, {2, 6}, {2, 4}};
        for (int i = 0; i < in1.length; i++) {
            if (!Arrays.equals(c1.book(in1[i][0], in1[i][1]), out1[i])) throw new AssertionError("example 1 step " + i);
        }
        // Checks Example 2: a booking that touches another at coordinate 9 or 3 adds no overlap.
        CalendarBusiest c2 = new CalendarBusiest();
        int[][] in2 = {{3, 9}, {9, 14}, {1, 3}};
        int[][] out2 = {{1, 3}, {1, 3}, {1, 1}};
        for (int i = 0; i < in2.length; i++) {
            if (!Arrays.equals(c2.book(in2[i][0], in2[i][1]), out2[i])) throw new AssertionError("example 2 step " + i);
        }
        // Checks 1000 random booking sequences against the oracle with a fixed seed.
        Random rnd = new Random(9104L);
        for (int iter = 0; iter < 1000; iter++) {
            CalendarBusiest cal = new CalendarBusiest();
            List<int[]> seen = new ArrayList<>();
            for (int k = 0; k < 8; k++) {
                int s = rnd.nextInt(40);
                int[] b = {s, s + 1 + rnd.nextInt(15)};
                seen.add(b);
                if (!Arrays.equals(cal.book(b[0], b[1]), oracleAfter(seen))) throw new AssertionError("random mismatch at " + iter + "," + k);
            }
        }
    }
}
```
