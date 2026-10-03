<!-- solutions-for: 06-event-sweep-ties -->
### Event Sweep Ties

#### Solution: [Build] Maximum Concurrent Half-Open Intervals (Author exercise)
<!-- id: iv-max-concurrent-half-open -->

**Approach.** Turn every interval into a plus-one entry at its start and a minus-one entry at its end. Sort by coordinate, and for equal coordinates put the minus-one first, which is the order that keeps touching half-open intervals apart. Walk the entries, add each delta to a counter, and track the largest counter value. The comparator uses `Integer.compare`, never subtraction. The assertions show that the opposite tie order overcounts on touching intervals, and compare the sweep with a direct count at every integer coordinate on random inputs.

**Complexity.** O(n log n) time for sorting 2n entries and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaxConcurrentHalfOpen {
    static int peak(int[][] intervals, boolean endsFirst) {
        int[][] entries = new int[intervals.length * 2][];
        for (int i = 0; i < intervals.length; i++) {
            entries[2 * i] = new int[] {intervals[i][0], 1};
            entries[2 * i + 1] = new int[] {intervals[i][1], -1};
        }
        Arrays.sort(entries, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0])
                : (endsFirst ? Integer.compare(a[1], b[1]) : Integer.compare(b[1], a[1])));
        int active = 0, best = 0;
        for (int[] e : entries) { active += e[1]; best = Math.max(best, active); }
        return best;
    }
    static int oracle(int[][] iv) {
        int best = 0;
        for (int x = -2; x < 40; x++) {
            int c = 0;
            for (int[] r : iv) if (r[0] <= x && x < r[1]) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        if (peak(new int[][] {{1, 4}, {2, 5}, {4, 7}, {5, 8}}, true) != 2) throw new AssertionError("example 1");
        if (peak(new int[][] {{1, 3}, {3, 5}, {5, 7}}, true) != 1) throw new AssertionError("example 2");
        if (peak(new int[][] {{1, 3}, {3, 5}, {5, 7}}, false) != 2) throw new AssertionError("starts first overcounts touching half-open intervals");
        if (peak(new int[0][], true) != 0) throw new AssertionError("empty input");
        Random rnd = new Random(10601);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(15); a[i][1] = a[i][0] + 1 + rnd.nextInt(6); }
            if (peak(a, true) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Vary] Maximum Concurrent Closed Intervals (Author exercise)
<!-- id: iv-max-concurrent-closed -->

**Approach.** The entries are the same, but the tie order flips: at one coordinate the plus-one entries are applied before the minus-one entries, because two closed intervals that meet at a value are both alive there. A zero-length interval `[s, s]` then raises the counter for an instant and lowers it again, so it is still counted. The assertions compare against a count at every integer coordinate with closed membership, and show that the half-open order undercounts both touching pairs and zero-length intervals.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaxConcurrentClosed {
    static int peak(int[][] intervals, boolean startsFirst) {
        int[][] entries = new int[intervals.length * 2][];
        for (int i = 0; i < intervals.length; i++) {
            entries[2 * i] = new int[] {intervals[i][0], 1};
            entries[2 * i + 1] = new int[] {intervals[i][1], -1};
        }
        Arrays.sort(entries, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0])
                : (startsFirst ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
        int active = 0, best = 0;
        for (int[] e : entries) { active += e[1]; best = Math.max(best, active); }
        return best;
    }
    static int oracle(int[][] iv) {
        int best = 0;
        for (int x = -2; x < 40; x++) {
            int c = 0;
            for (int[] r : iv) if (r[0] <= x && x <= r[1]) c++;
            best = Math.max(best, c);
        }
        return best;
    }

    public static void main(String[] args) {
        if (peak(new int[][] {{1, 4}, {2, 5}, {4, 7}, {5, 8}}, true) != 3) throw new AssertionError("example 1");
        if (peak(new int[][] {{1, 3}, {3, 5}, {5, 7}}, true) != 2) throw new AssertionError("example 2");
        if (peak(new int[][] {{4, 4}}, true) != 1) throw new AssertionError("a zero-length closed interval is one value");
        if (peak(new int[][] {{4, 4}}, false) != 0) throw new AssertionError("ends first erases the zero-length interval");
        if (peak(new int[][] {{1, 3}, {3, 5}}, false) != 1) throw new AssertionError("ends first undercounts a touching pair");
        Random rnd = new Random(10602);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(15); a[i][1] = a[i][0] + rnd.nextInt(6); }
            if (peak(a, true) != oracle(a)) throw new AssertionError("differs on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Many Events At One Coordinate (Author exercise)
<!-- id: iv-many-events-one-coordinate -->

**Approach.** Sort the entries by coordinate only, then process one coordinate group at a time: apply every delta in the group, and only after the whole group record the counter in the running maximum. The value inside a group depends on the order of its members, which the sort does not fix, so recording it would let the input order leak into the answer. Recording after the group removes that dependence. The assertions show that a naive per-entry maximum changes under a reordering of one group, and that the grouped answer is the same for many random shuffles and matches a map-based oracle that sums deltas per coordinate.

**Complexity.** O(n log n) time and O(n) space for the sorted copy.

```java run
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.TreeMap;
import java.util.ArrayList;

public final class ManyEventsOneCoordinate {
    static int grouped(int[][] entries) {
        int[][] sorted = new int[entries.length][];
        for (int i = 0; i < sorted.length; i++) sorted[i] = entries[i].clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        int active = 0, best = 0, i = 0;
        while (i < sorted.length) {
            int coordinate = sorted[i][0];
            while (i < sorted.length && sorted[i][0] == coordinate) { active += sorted[i][1]; i++; }
            best = Math.max(best, active);
        }
        return best;
    }
    static int perEntry(int[][] entries) {
        int active = 0, best = 0;
        for (int[] e : entries) { active += e[1]; best = Math.max(best, active); }
        return best;
    }
    static int oracle(int[][] entries) {
        TreeMap<Integer, Integer> sums = new TreeMap<>();
        for (int[] e : entries) sums.merge(e[0], e[1], Integer::sum);
        int active = 0, best = 0;
        for (int d : sums.values()) { active += d; best = Math.max(best, active); }
        return best;
    }

    public static void main(String[] args) {
        if (grouped(new int[][] {{5, -2}, {5, 3}, {1, 2}, {9, -3}}) != 3) throw new AssertionError("example 1");
        if (grouped(new int[][] {{2, 1}, {2, -1}, {2, 1}, {2, -1}}) != 0) throw new AssertionError("example 2");
        int[][] plusFirst = {{1, 2}, {5, 3}, {5, -2}, {9, -3}};
        int[][] minusFirst = {{1, 2}, {5, -2}, {5, 3}, {9, -3}};
        if (perEntry(plusFirst) == perEntry(minusFirst)) throw new AssertionError("the per-entry maximum depends on the order inside a group");
        if (grouped(plusFirst) != grouped(minusFirst)) throw new AssertionError("the grouped maximum must not");
        Random rnd = new Random(10603);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(10);
            List<int[]> list = new ArrayList<>();
            int balance = 0;
            for (int i = 0; i < n; i++) {
                int c = rnd.nextInt(6);
                int d = 1 + rnd.nextInt(4);
                list.add(new int[] {c, d});
                list.add(new int[] {c + 1 + rnd.nextInt(4), -d});
            }
            int[][] base = list.toArray(new int[0][]);
            int expected = oracle(base);
            for (int s = 0; s < 5; s++) {
                Collections.shuffle(list, rnd);
                int[][] shuffled = list.toArray(new int[0][]);
                if (grouped(shuffled) != expected) throw new AssertionError("changed under shuffling: " + Arrays.deepToString(shuffled));
            }
        }
    }
}
```

#### Solution: [Recognize] First Coordinate Reaching Capacity (Author exercise)
<!-- id: iv-first-coordinate-capacity -->

**Approach.** Build the plus-one and minus-one entries for the half-open intervals, sort them by coordinate with ends before starts, and walk coordinate groups. After the last entry of a group the counter equals the number of intervals active at that coordinate, so test it against `k` and return the coordinate on the first success. Testing inside a group could report a value that never describes a real coordinate. The assertions compare with a direct count at each integer coordinate in increasing order, and show that a per-entry test returns an earlier, wrong coordinate on a touching pair.

**Complexity.** O(n log n) time and O(n) space.

```java run
import java.util.Arrays;
import java.util.Random;

public final class FirstCoordinateCapacity {
    static int first(int[][] intervals, int k, boolean testInsideGroup) {
        int[][] entries = new int[intervals.length * 2][];
        for (int i = 0; i < intervals.length; i++) {
            entries[2 * i] = new int[] {intervals[i][0], 1};
            entries[2 * i + 1] = new int[] {intervals[i][1], -1};
        }
        Arrays.sort(entries, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0])
                : (testInsideGroup ? Integer.compare(b[1], a[1]) : Integer.compare(a[1], b[1])));
        int active = 0, i = 0;
        while (i < entries.length) {
            int coordinate = entries[i][0];
            while (i < entries.length && entries[i][0] == coordinate) {
                active += entries[i][1];
                i++;
                if (testInsideGroup && active >= k) return coordinate;
            }
            if (!testInsideGroup && active >= k) return coordinate;
        }
        return -1;
    }
    static int oracle(int[][] iv, int k) {
        for (int x = -2; x < 40; x++) {
            int c = 0;
            for (int[] r : iv) if (r[0] <= x && x < r[1]) c++;
            if (c >= k) return x;
        }
        return -1;
    }

    public static void main(String[] args) {
        if (first(new int[][] {{1, 5}, {2, 6}, {3, 4}}, 3, false) != 3) throw new AssertionError("example 1");
        if (first(new int[][] {{1, 3}, {3, 5}}, 2, false) != -1) throw new AssertionError("example 2");
        if (first(new int[][] {{1, 3}, {3, 5}}, 2, true) != 3) throw new AssertionError("a test inside the group reports a coordinate that never has two active");
        if (first(new int[0][], 1, false) != -1) throw new AssertionError("empty input");
        Random rnd = new Random(10604);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(15); a[i][1] = a[i][0] + 1 + rnd.nextInt(6); }
            int k = 1 + rnd.nextInt(4);
            if (first(a, k, false) != oracle(a, k)) throw new AssertionError("differs on " + Arrays.deepToString(a) + " k=" + k);
        }
    }
}
```
