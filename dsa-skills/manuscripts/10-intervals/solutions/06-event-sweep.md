<!-- solutions-for: 10-intervals -->
### Solutions For Counting Active Intervals

#### Solution: [Build] Maximum Concurrent Half-Open Intervals (Author exercise)
<!-- id: iv-peak-half-open -->

**Approach.**
Each session `[start, end)` produces a start event with change +1 at `start` and an end event with change -1 at `end`. The method sorts the events by coordinate, and by change ascending when coordinates tie, so an end runs before a start at the same coordinate. A half-open session no longer holds its end coordinate, so this order frees the place before the next session takes it. One pass adds each change to `active` and records the largest value. The opening log `[1,4)` and `[4,6)` then gives a peak of 1, while the reverse tie order would report 2. The invariant is that `active` equals the number of sessions holding the coordinate of the last processed event, once all earlier events at that coordinate have run.

**Complexity.**
- **Time** is O(n log n), because sorting the `2n` events dominates and the pass adds O(n).
- **Space** is O(n), because the event array holds `2n` pairs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PeakHalfOpen {
    /**
     * Returns the largest number of half-open sessions that hold one integer time.
     * Time: O(n log n), the sort of 2n events plus one pass.
     * Space: O(n), for the event array.
     * Invariant: active counts the sessions holding the coordinate of the last event, after earlier ties ran.
     */
    static int peak(int[][] sessions, boolean endFirst) {
        // Two events per session: a start (+1) and an end (-1).
        int[][] events = new int[2 * sessions.length][];
        for (int i = 0; i < sessions.length; i++) {
            events[2 * i] = new int[] {sessions[i][0], +1};
            events[2 * i + 1] = new int[] {sessions[i][1], -1};
        }
        // Sort by coordinate; on a tie, minus 1 first for half-open sessions (endFirst), plus 1 first otherwise.
        Arrays.sort(events, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0])
                : (endFirst ? Integer.compare(a[1], b[1]) : Integer.compare(b[1], a[1])));
        int active = 0, best = 0;
        // One pass applies each change and tracks the largest count.
        for (int[] e : events) {
            active += e[1];
            best = Math.max(best, active);
        }
        return best;
    }

    /** Reference: count the sessions that hold each integer time in a small window. */
    static int brute(int[][] in) {
        int best = 0;
        for (int t = -2; t <= 40; t++) {
            int c = 0;
            for (int[] s : in) if (s[0] <= t && t < s[1]) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: at most two sessions share a time.
        if (peak(new int[][] {{1, 4}, {4, 6}, {2, 5}, {5, 7}}, true) != 2) throw new AssertionError("example 1");
        // Example 2: touching sessions never overlap.
        if (peak(new int[][] {{3, 5}, {5, 8}, {8, 9}}, true) != 1) throw new AssertionError("example 2");
        // The opening log: the wrong tie order reports 2, the right one reports 1.
        int[][] log = {{1, 4}, {4, 6}};
        if (peak(log, false) != 2) throw new AssertionError("start-first order reports 2");
        if (peak(log, true) != 1) throw new AssertionError("end-first order reports 1");
        // The direct counting method from the lesson agrees on the log.
        if (brute(log) != 1) throw new AssertionError("brute on log");
        // Empty input.
        if (peak(new int[0][], true) != 0) throw new AssertionError("empty");
        // Random inputs agree with counting each time.
        Random rnd = new Random(50);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); in[i] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            if (peak(in, true) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Vary] Maximum Concurrent Closed Intervals (Author exercise)
<!-- id: iv-peak-closed -->

**Approach.**
A closed session `[start, end]` still holds `end`, so at a shared coordinate the starting session meets the ending one. The method keeps the same events and reverses the tie order, so a start event runs before an end event at the same coordinate. At coordinate 4 in the first example the start of `[4,6]` raises the count to 3 before the end of `[1,4]` lowers it, and coordinate 4 truly lies in three sessions. The invariant is that `active` after the last start at a coordinate counts every session holding that coordinate.

**Complexity.**
- **Time** is O(n log n), because sorting the `2n` events dominates and the pass adds O(n).
- **Space** is O(n), because the event array holds `2n` pairs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class PeakClosed {
    /**
     * Returns the largest number of closed sessions that hold one integer time.
     * Time: O(n log n), the sort of 2n events plus one pass.
     * Space: O(n), for the event array.
     * Invariant: after the last start at a coordinate, active counts every session holding it.
     */
    static int peak(int[][] sessions) {
        int[][] events = new int[2 * sessions.length][];
        for (int i = 0; i < sessions.length; i++) {
            events[2 * i] = new int[] {sessions[i][0], +1};
            events[2 * i + 1] = new int[] {sessions[i][1], -1};
        }
        // Sort by coordinate; plus 1 first on a tie, because a closed interval still holds its end.
        Arrays.sort(events, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(b[1], a[1]));
        int active = 0, best = 0;
        for (int[] e : events) {
            active += e[1];
            best = Math.max(best, active);
        }
        return best;
    }

    /** Reference: count the sessions that hold each integer time in a small window. */
    static int brute(int[][] in) {
        int best = 0;
        for (int t = -2; t <= 40; t++) {
            int c = 0;
            for (int[] s : in) if (s[0] <= t && t <= s[1]) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: coordinate 4 lies in three closed sessions.
        if (peak(new int[][] {{1, 4}, {4, 6}, {2, 5}, {5, 7}}) != 3) throw new AssertionError("example 1");
        // Example 2: neighbours share a coordinate, so two sessions hold it.
        if (peak(new int[][] {{3, 5}, {5, 8}, {8, 9}}) != 2) throw new AssertionError("example 2");
        // Empty input.
        if (peak(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs, including single-coordinate sessions, agree with counting each time.
        Random rnd = new Random(51);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(12); in[i] = new int[] {s, s + rnd.nextInt(6)}; }
            if (peak(in) != brute(in)) throw new AssertionError("random " + Arrays.deepToString(in));
        }
    }
}
```

#### Solution: [Boundary] Many Events At One Coordinate (Author exercise)
<!-- id: iv-events-one-coordinate -->

**Approach.**
The method skips every interval with `start == end`, because a half-open interval of length zero holds no time, and its end event would run before its start event and push the count below zero. It builds the events of the remaining intervals and sorts them by coordinate, with ends before starts on a tie. The scan then handles one coordinate at a time. It applies every event that shares the coordinate and only then writes the pair `[coordinate, active]`. Because the pair is written after the whole group, the result cannot depend on the input order or on the order inside the group. The invariant is that `active` is never negative and equals the number of intervals holding the coordinate after each group.

**Complexity.**
- **Time** is O(n log n), because sorting the events dominates and the grouped pass adds O(n).
- **Space** is O(n), because the events and the output each hold up to `2n` entries.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class GroupedSweep {
    /**
     * Returns [coordinate, active] for every coordinate carrying an event of a non-empty interval.
     * Time: O(n log n), the sort plus one grouped pass.
     * Space: O(n), for the events and the output.
     * Invariant: active is never negative and counts the intervals holding the coordinate after each group.
     */
    static int[][] activeAtEvents(int[][] sessions) {
        List<int[]> events = new ArrayList<>();
        for (int[] s : sessions) {
            // An empty half-open interval holds no time; skipping it keeps the count from dipping below zero.
            if (s[0] == s[1]) continue;
            events.add(new int[] {s[0], +1});
            events.add(new int[] {s[1], -1});
        }
        // Sort by coordinate, with ends first so the order of ties is fixed by the contract.
        events.sort((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        List<int[]> out = new ArrayList<>();
        int active = 0, i = 0;
        // Each outer iteration consumes one whole group of events at a coordinate.
        while (i < events.size()) {
            int c = events.get(i)[0];
            // Apply every event at this coordinate before reading the count.
            while (i < events.size() && events.get(i)[0] == c) active += events.get(i++)[1];
            out.add(new int[] {c, active});
        }
        return out.toArray(new int[out.size()][]);
    }

    /** Reference: count the intervals that hold each event coordinate. */
    static int[][] brute(int[][] in) {
        List<Integer> coords = new ArrayList<>();
        for (int[] s : in) if (s[0] != s[1]) { if (!coords.contains(s[0])) coords.add(s[0]); if (!coords.contains(s[1])) coords.add(s[1]); }
        Collections.sort(coords);
        int[][] out = new int[coords.size()][];
        for (int k = 0; k < out.length; k++) {
            int c = coords.get(k), count = 0;
            for (int[] s : in) if (s[0] <= c && c < s[1]) count++;
            out[k] = new int[] {c, count};
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: three events at coordinate 4 give an active count of 2.
        if (!Arrays.deepEquals(activeAtEvents(new int[][] {{1, 4}, {4, 6}, {4, 9}}), new int[][] {{1, 1}, {4, 2}, {6, 1}, {9, 0}})) throw new AssertionError("example 1");
        // Example 2: the empty interval [5,5) is skipped.
        if (!Arrays.deepEquals(activeAtEvents(new int[][] {{5, 5}, {5, 8}}), new int[][] {{5, 1}, {8, 0}})) throw new AssertionError("example 2");
        // Only empty intervals give an empty result.
        if (activeAtEvents(new int[][] {{3, 3}}).length != 0) throw new AssertionError("only empty");
        // Many events at one coordinate give one pair, whatever the input order.
        int[][] many = new int[1000][];
        for (int i = 0; i < many.length; i++) many[i] = i % 2 == 0 ? new int[] {0, 7} : new int[] {7, 9};
        if (!Arrays.deepEquals(activeAtEvents(many), new int[][] {{0, 500}, {7, 500}, {9, 0}})) throw new AssertionError("many");
        // Random inputs agree with counting at each coordinate, and shuffling the input does not change the result.
        Random rnd = new Random(52);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(8); in[i] = new int[] {s, s + rnd.nextInt(5)}; }
            int[][] got = activeAtEvents(in);
            if (!Arrays.deepEquals(got, brute(in))) throw new AssertionError("random " + Arrays.deepToString(in));
            List<int[]> shuffled = new ArrayList<>(Arrays.asList(in));
            Collections.shuffle(shuffled, rnd);
            if (!Arrays.deepEquals(got, activeAtEvents(shuffled.toArray(new int[0][])))) throw new AssertionError("order dependence");
        }
    }
}
```

#### Solution: [Recognize] First Coordinate Reaching Capacity (Author exercise)
<!-- id: iv-first-capacity -->

**Approach.**
The method builds the same events and sorts them with ends before starts at a shared coordinate. It applies the events in order and stops at the first start event after which `active` is at least `k`, returning that event's coordinate. The count can only rise at a start, so the first time it reaches `k` is right after a start. Because ends at the coordinate already ran, `active` at that moment is a lower bound of the true count at the coordinate, and it is already at least `k`, so the coordinate holds `k` sessions. The earliest such start event has the smallest coordinate, so the sweep needs no stored peak. When no event reaches `k`, the method returns -1. The invariant is that no earlier coordinate had `k` active sessions.

**Complexity.**
- **Time** is O(n log n), because sorting the `2n` events dominates and the pass adds O(n).
- **Space** is O(n), because the event array holds `2n` pairs.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstCapacity {
    /**
     * Returns the smallest integer time at which at least k half-open sessions hold it, or -1.
     * Time: O(n log n), the sort plus one pass.
     * Space: O(n), for the event array.
     * Invariant: no coordinate before the current event had k active sessions.
     */
    static int firstAtCapacity(int[][] sessions, int k) {
        int[][] events = new int[2 * sessions.length][];
        for (int i = 0; i < sessions.length; i++) {
            events[2 * i] = new int[] {sessions[i][0], +1};
            events[2 * i + 1] = new int[] {sessions[i][1], -1};
        }
        // Ends first on a tie, so touching sessions never count together.
        Arrays.sort(events, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int active = 0;
        // Apply events in order and stop at the first start that reaches the capacity.
        for (int[] e : events) {
            active += e[1];
            if (e[1] > 0 && active >= k) return e[0];
        }
        return -1;
    }

    /** Reference: test each integer time in order. */
    static int brute(int[][] in, int k) {
        for (int t = 0; t <= 40; t++) {
            int c = 0;
            for (int[] s : in) if (s[0] <= t && t < s[1]) c++;
            if (c >= k) return t;
        }
        return -1;
    }

    public static void main(String[] args) {
        // Example 1: three sessions hold time 4.
        if (firstAtCapacity(new int[][] {{1, 5}, {2, 6}, {4, 8}}, 3) != 4) throw new AssertionError("example 1");
        // Example 2: touching sessions never reach 2.
        if (firstAtCapacity(new int[][] {{1, 3}, {3, 5}}, 2) != -1) throw new AssertionError("example 2");
        // Empty input.
        if (firstAtCapacity(new int[0][], 1) != -1) throw new AssertionError("empty");
        // Random inputs agree with testing each time in order.
        Random rnd = new Random(53);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] in = new int[n][];
            for (int i = 0; i < n; i++) { int s = rnd.nextInt(15); in[i] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            int k = 1 + rnd.nextInt(4);
            if (firstAtCapacity(in, k) != brute(in, k)) throw new AssertionError("random " + Arrays.deepToString(in) + k);
        }
    }
}
```
