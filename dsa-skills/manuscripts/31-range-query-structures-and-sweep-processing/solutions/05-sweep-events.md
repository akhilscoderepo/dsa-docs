<!-- solutions-for: 05-sweep-events -->
### Solutions For Sweep Events

#### Solution: [Build] Car Pooling (LeetCode 1094)
<!-- id: rq31-car-pooling -->

**Approach.** Each trip becomes two events, and a sorted pass keeps the load.

A trip adds its passengers at `from` and removes them at `to`. Sorting the pairs by coordinate and then by delta places a drop-off before a pickup at the same coordinate, which matches the half-open range. The pass adds each delta to a running load and returns `false` as soon as the load exceeds the capacity.

The invariant is that the load after each event equals the passengers on board from that coordinate to the next one. The load can only reach a new maximum right after a pickup, so checking after every event covers every position. The size of the coordinates never enters the cost.

**Complexity.**

- **Time** is O(n log n), because sorting the 2n events dominates the single linear pass over them.
- **Space** is O(n), because the event array holds two entries for each trip.

```java run
import java.util.Arrays;
import java.util.Random;

public final class CarPoolingSweep {
    /**
     * Reports whether the seat count is never exceeded.
     * Time: O(n log n) for sorting 2n events. Space: O(n) for the event array.
     * Invariant: load equals the passengers on board between the last applied coordinate and the next one.
     */
    static boolean carPooling(int[][] trips, int capacity) {
        // Two events per trip, so the array has 2n entries and costs O(n) memory.
        int[][] events = new int[trips.length * 2][];
        // k is the next free slot in the event array.
        int k = 0;
        // One iteration per trip creates its pickup and drop-off events in O(n) total.
        for (int[] t : trips) {
            // The pickup adds passengers at the first occupied position.
            events[k++] = new int[]{t[1], t[0]};
            // The drop-off removes them at the exclusive end of the range.
            events[k++] = new int[]{t[2], -t[0]};
        }
        // Sort by coordinate, then by delta, so a decrease runs before an increase at one coordinate; this is the O(n log n) step.
        Arrays.sort(events, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0]) : Integer.compare(p[1], q[1]));
        // The load is a long so that large inputs cannot overflow the sum.
        long load = 0;
        // One pass over the sorted events costs O(n).
        for (int[] e : events) {
            // Apply one delta; the load now describes the span up to the next coordinate.
            load += e[1];
            // A load above capacity at any span makes the whole batch infeasible.
            if (load > capacity) return false;
        }
        // Every span stayed within capacity.
        return true;
    }

    /** Reference answer that adds each trip to every position; usable only for small coordinates. */
    static boolean brute(int[][] trips, int capacity) {
        // One counter per position from 0 to 20 is enough for the test coordinates.
        int[] load = new int[21];
        // Add each trip to every position it occupies.
        for (int[] t : trips) {
            for (int x = t[1]; x < t[2]; x++) {
                load[x] += t[0];
                if (load[x] > capacity) return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1: the overlap at positions 3 and 4 carries 5 passengers.
        if (carPooling(new int[][]{{2, 1, 5}, {3, 3, 7}}, 4)) throw new AssertionError("example 1");
        // Checks Example 2: the drop-off at 5 runs before the pickup at 5.
        if (!carPooling(new int[][]{{2, 1, 5}, {3, 5, 7}}, 3)) throw new AssertionError("example 2");
        // Checks a trip near one billion, which the position array could not store.
        if (!carPooling(new int[][]{{5, 0, 1_000_000_000}, {5, 1_000_000_000 - 1, 1_000_000_000}}, 10)) throw new AssertionError("large coordinates");
        // Compares the sweep with the brute force on random small inputs with a fixed seed.
        Random rnd = new Random(3105);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(6);
            int[][] trips = new int[n][];
            for (int i = 0; i < n; i++) {
                int a = rnd.nextInt(10);
                int b = a + 1 + rnd.nextInt(10 - a);
                trips[i] = new int[]{1 + rnd.nextInt(4), a, b};
            }
            int cap = 1 + rnd.nextInt(9);
            if (carPooling(trips, cap) != brute(trips, cap)) throw new AssertionError("random case " + iter);
        }
    }
}
```

#### Solution: [Vary] Group Equal Coordinates (Author exercise)
<!-- id: rq31-group-equal-coordinates -->

**Approach.** A coverage count is read once per distinct coordinate, after all deltas there are applied.

Each interval adds one event at `start` and subtracts one at `end`. After sorting, the pass walks groups of equal coordinates. It applies every delta in a group and only then compares the count before and after the group. A change from zero to positive opens a span at this coordinate, and a change from positive to zero closes it.

Reading the count after each single delta would split `[1,3)` and `[3,5)`, because the count would touch zero between the drop-off and the pickup. Grouping removes that false gap. The invariant is that the count describes the positions from the current coordinate to the next distinct one.

**Complexity.**

- **Time** is O(n log n), because sorting 2n events dominates the linear grouped pass.
- **Space** is O(n), because the events and the output spans take linear memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MergeSpansSweep {
    /**
     * Returns the maximal covered spans of half-open intervals.
     * Time: O(n log n) for sorting. Space: O(n) for events and output.
     * Invariant: count equals the number of intervals covering the positions from the current coordinate onward.
     */
    static List<int[]> spans(int[][] intervals) {
        // Two events per interval, so memory is O(n).
        int[][] events = new int[intervals.length * 2][];
        int k = 0;
        // One iteration per interval creates its start and end events.
        for (int[] iv : intervals) {
            // The start raises coverage at the first covered position.
            events[k++] = new int[]{iv[0], 1};
            // The end lowers coverage at the first uncovered position.
            events[k++] = new int[]{iv[1], -1};
        }
        // Only the coordinate matters for the order, because groups are applied together.
        Arrays.sort(events, (p, q) -> Integer.compare(p[0], q[0]));
        List<int[]> out = new ArrayList<>();
        // count is the current coverage and open is the start of the span being tracked.
        int count = 0, open = 0, i = 0;
        // The outer loop visits each group of equal coordinates once, so the pass costs O(n).
        while (i < events.length) {
            // The group coordinate is read before any delta changes the count.
            int x = events[i][0];
            // Remember coverage before the group to detect a transition.
            int before = count;
            // Apply every delta that shares this coordinate before reading the count.
            while (i < events.length && events[i][0] == x) count += events[i++][1];
            // Coverage rising from zero opens a span at this coordinate.
            if (before == 0 && count > 0) open = x;
            // Coverage falling to zero closes the span at this coordinate.
            else if (before > 0 && count == 0) out.add(new int[]{open, x});
        }
        // The list holds the maximal spans in ascending order.
        return out;
    }

    /** Reference answer that marks every covered integer position and joins adjacent ones. */
    static List<int[]> brute(int[][] intervals) {
        // Positions range from -5 to 9 in the tests; the offset of 5 maps them to indexes.
        boolean[] cov = new boolean[16];
        for (int[] iv : intervals) for (int x = iv[0]; x < iv[1]; x++) cov[x + 5] = true;
        List<int[]> out = new ArrayList<>();
        // Scan once and join consecutive covered positions into one span.
        for (int x = 0; x < 16; x++) {
            if (!cov[x]) continue;
            int y = x;
            while (y < 16 && cov[y]) y++;
            out.add(new int[]{x - 5, y - 5});
            x = y;
        }
        return out;
    }

    static boolean same(List<int[]> a, List<int[]> b) {
        // Two span lists agree when they have the same length and equal pairs.
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); i++) if (!Arrays.equals(a.get(i), b.get(i))) return false;
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1: touching intervals merge and the gap keeps spans apart.
        if (!same(spans(new int[][]{{1, 3}, {3, 5}, {7, 9}}), List.of(new int[]{1, 5}, new int[]{7, 9}))) throw new AssertionError("example 1");
        // Checks Example 2: unsorted input with one uncovered position.
        if (!same(spans(new int[][]{{4, 6}, {1, 2}, {3, 4}}), List.of(new int[]{1, 2}, new int[]{3, 6}))) throw new AssertionError("example 2");
        // Checks the empty input.
        if (!spans(new int[0][]).isEmpty()) throw new AssertionError("empty");
        // Compares with the brute force on random inputs with a fixed seed.
        Random rnd = new Random(3105);
        for (int iter = 0; iter < 3000; iter++) {
            int n = rnd.nextInt(7);
            int[][] iv = new int[n][];
            for (int i = 0; i < n; i++) {
                int a = -5 + rnd.nextInt(13);
                iv[i] = new int[]{a, a + 1 + rnd.nextInt(10 - a)};
            }
            if (!same(spans(iv), brute(iv))) throw new AssertionError("random case " + iter);
        }
    }
}
```

#### Solution: [Boundary] Start-End Tie (Author exercise)
<!-- id: rq31-start-end-tie -->

**Approach.** The endpoint convention decides which event runs first at an equal coordinate.

Every interval produces a `+1` event at `start` and a `-1` event at `end`. For half-open intervals, an interval ending at `x` no longer contains `x`, so the decrease must run before the increase. For closed intervals, the interval still contains `x`, so the increase must run first. The sort key is the coordinate, then the delta ascending for half-open and descending for closed.

The pass keeps the running count and the largest value it reaches after any event. With the correct order, each value after an event is the true number of active intervals at some integer position. The wrong order creates a peak that no position has, or hides one that a position has.

**Complexity.**

- **Time** is O(n log n), because the sort of 2n events dominates the linear scan.
- **Space** is O(n), because the event array holds two entries for each interval.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaxActiveTie {
    /**
     * Returns the largest number of intervals active at one integer position.
     * Time: O(n log n) for sorting. Space: O(n) for events.
     * Invariant: current equals the intervals active at the coordinate of the last applied event under the chosen convention.
     */
    static int maxActive(int[][] intervals, boolean closed) {
        // Two events per interval, so memory is O(n).
        int[][] events = new int[intervals.length * 2][];
        int k = 0;
        // One iteration per interval creates its two events.
        for (int[] iv : intervals) {
            events[k++] = new int[]{iv[0], 1};
            events[k++] = new int[]{iv[1], -1};
        }
        // The tie policy: closed ranges put increases first, half-open ranges put decreases first.
        Arrays.sort(events, (p, q) -> p[0] != q[0] ? Integer.compare(p[0], q[0])
                : closed ? Integer.compare(q[1], p[1]) : Integer.compare(p[1], q[1]));
        // current is the running count and best is the largest count seen after any event.
        int current = 0, best = 0;
        // One linear pass over the sorted events.
        for (int[] e : events) {
            // Apply one delta under the tie policy.
            current += e[1];
            // The maximum can only change right after an increase, and taking it every time is still correct.
            best = Math.max(best, current);
        }
        // The best count is the answer for the chosen convention.
        return best;
    }

    /** Reference answer that counts the active intervals at every integer position. */
    static int brute(int[][] intervals, boolean closed) {
        int best = 0;
        // Positions in the tests lie between 0 and 12.
        for (int x = 0; x <= 12; x++) {
            int c = 0;
            // Count intervals that contain x under the convention.
            for (int[] iv : intervals) if (iv[0] <= x && (closed ? x <= iv[1] : x < iv[1])) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        // Checks Example 1 under both conventions.
        int[][] a = {{1, 3}, {3, 5}};
        if (maxActive(a, true) != 2 || maxActive(a, false) != 1) throw new AssertionError("example 1");
        // Checks Example 2 under both conventions.
        int[][] b = {{1, 4}, {2, 6}, {4, 8}};
        if (maxActive(b, true) != 3 || maxActive(b, false) != 2) throw new AssertionError("example 2");
        // Checks the Java claim that comparing by subtraction overflows for large coordinates of opposite sign.
        int big = 1_500_000_000;
        if (!(big - (-big) < 0)) throw new AssertionError("subtraction overflows");
        // Checks that the sweep still orders such coordinates correctly through Integer.compare.
        if (maxActive(new int[][]{{-big, big}, {-big, 0}}, false) != 2) throw new AssertionError("large coordinates");
        // Compares with the brute force on random inputs with a fixed seed.
        Random rnd = new Random(3105);
        for (int iter = 0; iter < 3000; iter++) {
            int n = 1 + rnd.nextInt(6);
            int[][] iv = new int[n][];
            for (int i = 0; i < n; i++) {
                int s = rnd.nextInt(10);
                iv[i] = new int[]{s, s + 1 + rnd.nextInt(12 - s)};
            }
            for (boolean closed : new boolean[]{true, false})
                if (maxActive(iv, closed) != brute(iv, closed)) throw new AssertionError("random case " + iter + " closed=" + closed);
        }
    }
}
```

#### Solution: [Recognize] The Skyline Problem (LeetCode 218)
<!-- id: rq31-skyline -->

**Approach.** A max-heap holds the active heights, and lazy deletion removes ended ones.

Each building gives a start event with its positive height and an end event with its negative height. The pass applies all events at one coordinate and then reads the maximum height. A key point is emitted only when that maximum differs from the previous one. The invariant is that the heap top, after cleanup, is the largest height over the positions from this coordinate to the next.

A `PriorityQueue` cannot cheaply remove an arbitrary height. The code instead counts each ended height in a map and leaves it in the heap. Before reading the top, the code pops the top while its pending count is positive. The count handles duplicate heights, so two buildings of equal height end independently. Ground height 0 stays in the heap, so the heap is never empty.

**Complexity.**

- **Time** is O(n log n), because sorting and the heap operations each handle at most 2n values at O(log n) apiece.
- **Space** is O(n), because the heap, the pending map and the events hold at most one entry per building end.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Random;

public final class SkylineSweep {
    /**
     * Returns the key points of the outline of half-open buildings.
     * Time: O(n log n) for sorting and heap work. Space: O(n) for events, heap and pending counts.
     * Invariant: after cleanup, the heap top is the maximum height active from the current coordinate to the next.
     */
    static List<int[]> skyline(int[][] buildings) {
        // Two events per building, so memory is O(n).
        int[][] events = new int[buildings.length * 2][];
        int k = 0;
        // One iteration per building creates its start and end events.
        for (int[] b : buildings) {
            // A positive height marks the start of a building.
            events[k++] = new int[]{b[0], b[2]};
            // A negative height marks its end at the exclusive right edge.
            events[k++] = new int[]{b[1], -b[2]};
        }
        // Only the coordinate matters, because all events at one coordinate are applied together.
        Arrays.sort(events, (p, q) -> Integer.compare(p[0], q[0]));
        // The max-heap yields the largest active height at its top.
        PriorityQueue<Integer> heap = new PriorityQueue<>(Comparator.reverseOrder());
        // pending counts ended heights that still sit inside the heap.
        Map<Integer, Integer> pending = new HashMap<>();
        // Ground level stays in the heap, so peek never returns null.
        heap.add(0);
        List<int[]> outline = new ArrayList<>();
        // previous is the last emitted height and i is the next unapplied event.
        int previous = 0, i = 0;
        // Each pass of this loop handles one distinct coordinate, so the loop touches each event once.
        while (i < events.length) {
            // The group coordinate is fixed before the inner loop moves i.
            int x = events[i][0];
            // Apply every event at this coordinate before reading the maximum.
            while (i < events.length && events[i][0] == x) {
                int h = events[i++][1];
                // A start pushes its height in O(log n).
                if (h > 0) heap.add(h);
                // An end only increments a counter in O(1), which is the lazy deletion.
                else pending.merge(-h, 1, Integer::sum);
            }
            // Discard ended heights that reached the top; each height is popped at most once overall.
            while (pending.getOrDefault(heap.peek(), 0) > 0)
                pending.merge(heap.poll(), -1, Integer::sum);
            // The cleaned top is the current maximum height.
            int top = heap.peek();
            // Emit a key point only where the maximum changes.
            if (top != previous) {
                outline.add(new int[]{x, top});
                previous = top;
            }
        }
        // The last key point has height 0 once every building has ended.
        return outline;
    }

    /** Reference answer that finds the height at every integer position in 0..10. */
    static List<int[]> brute(int[][] buildings) {
        List<int[]> out = new ArrayList<>();
        int prev = 0;
        // Positions in the tests lie between 0 and 10.
        for (int x = 0; x <= 10; x++) {
            int h = 0;
            // The height at x is the maximum over buildings that contain x.
            for (int[] b : buildings) if (b[0] <= x && x < b[1]) h = Math.max(h, b[2]);
            // A key point appears where the height differs from the previous position.
            if (h != prev) { out.add(new int[]{x, h}); prev = h; }
        }
        return out;
    }

    static boolean same(List<int[]> a, List<int[]> b) {
        // Two outlines agree when they have equal length and equal pairs.
        if (a.size() != b.size()) return false;
        for (int i = 0; i < a.size(); i++) if (!Arrays.equals(a.get(i), b.get(i))) return false;
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1: the shared edge at 6 drops the maximum from 5 to 2.
        if (!same(skyline(new int[][]{{2, 6, 3}, {4, 6, 5}, {6, 9, 2}}),
                List.of(new int[]{2, 3}, new int[]{4, 5}, new int[]{6, 2}, new int[]{9, 0}))) throw new AssertionError("example 1");
        // Checks Example 2: equal heights that overlap produce no key point at 3.
        if (!same(skyline(new int[][]{{0, 3, 4}, {2, 5, 4}}), List.of(new int[]{0, 4}, new int[]{5, 0}))) throw new AssertionError("example 2");
        // Checks the empty input.
        if (!skyline(new int[0][]).isEmpty()) throw new AssertionError("empty");
        // Compares with the brute force on random inputs with a fixed seed.
        Random rnd = new Random(3105);
        for (int iter = 0; iter < 3000; iter++) {
            int n = rnd.nextInt(7);
            int[][] bs = new int[n][];
            for (int i = 0; i < n; i++) {
                int l = rnd.nextInt(10);
                bs[i] = new int[]{l, l + 1 + rnd.nextInt(10 - l), 1 + rnd.nextInt(5)};
            }
            if (!same(skyline(bs), brute(bs))) throw new AssertionError("random case " + iter);
        }
    }
}
```
