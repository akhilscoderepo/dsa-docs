<!-- solutions-for: 02-interval-scheduling -->
### Solutions For Interval Scheduling

#### Solution: [Build] Choose Compatible Meetings (Author exercise)
<!-- id: gr-choose-compatible-meetings -->

**Approach.**
The method sorts the meetings by end time and scans them once. It accepts a meeting when its start is at least the end of the last accepted meeting, and then moves `lastEnd` forward. The swap argument of the lesson shows that the meeting with the earliest end begins some largest schedule, and the same argument applies to what remains after it.

After each step, `lastEnd` is the smallest end time that any schedule of the scanned meetings of that size can reach.

**Complexity.**
- **Time** is O(n log n), because the sort costs that much and the scan adds O(n).
- **Space** is O(n) for the sorted copy of the references.

```java run
import java.util.*;

public final class ChooseCompatibleMeetings {
    /**
     * Returns the largest number of pairwise non-overlapping half-open intervals.
     * Time: O(n log n). Space: O(n).
     * Invariant: lastEnd is the earliest end time reachable by a schedule of the accepted size.
     */
    static int maxMeetings(int[][] meetings) {
        int[][] byEnd = meetings.clone();                             // keep the caller's order
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));   // earliest end first, no overflow
        int accepted = 0;
        long lastEnd = Long.MIN_VALUE;                                // below every start
        for (int[] m : byEnd) {                                       // one test per meeting
            if (m[0] >= lastEnd) {                                    // half-open: touching is allowed
                accepted++;
                lastEnd = m[1];                                       // free time now starts at this end
            }
        }
        return accepted;
    }

    static int brute(int[][] m) {
        int best = 0;
        for (int mask = 0; mask < (1 << m.length); mask++) {          // every subset
            boolean ok = true;
            for (int a = 0; a < m.length && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < m.length; b++) {
                    if ((mask >> b & 1) != 0 && m[a][0] < m[b][1] && m[b][0] < m[a][1]) { ok = false; break; }
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maxMeetings(new int[][] {{1, 3}, {2, 4}, {3, 6}, {5, 7}, {6, 8}}) != 3) throw new AssertionError("ex1");
        if (maxMeetings(new int[][] {{0, 10}, {1, 2}, {3, 4}, {5, 6}}) != 3) throw new AssertionError("ex2");
        // The start-order plan would return 1 on the second example; the empty input returns 0.
        if (maxMeetings(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs must match an exhaustive search over subsets.
        Random rnd = new Random(2011);
        for (int t = 0; t < 500; t++) {
            int[][] m = new int[rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(10); m[k] = new int[] {s, s + 1 + rnd.nextInt(5)}; }
            if (maxMeetings(m) != brute(m)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Non-overlapping Intervals (LeetCode 435)
<!-- id: gr-non-overlapping-intervals -->

**Approach.**
The method sorts the positions `0..n-1` by end time and breaks ties by position. It scans that order, keeps an interval when its start is at least the last kept end, and records the position of every other interval as removed. Sorting positions keeps the original index of each interval. The tie rule makes the output deterministic. The kept intervals form a largest schedule by the same swap argument as before, so the removed positions are as few as possible.

After each step, the kept positions form a largest schedule of the scanned prefix, and `removed` holds the rest of that prefix.

**Complexity.**
- **Time** is O(n log n) for the sort of positions, and the scan adds O(n).
- **Space** is O(n) for the position array and the removed list.

```java run
import java.util.*;

public final class NonOverlappingIntervals {
    /**
     * Returns the removed positions in increasing order.
     * Time: O(n log n). Space: O(n).
     * Invariant: the kept intervals form a largest schedule of the scanned prefix.
     */
    static int[] removed(int[][] iv) {
        Integer[] order = new Integer[iv.length];
        for (int i = 0; i < order.length; i++) order[i] = i;          // positions to sort
        Arrays.sort(order, (a, b) -> iv[a][1] != iv[b][1] ? Integer.compare(iv[a][1], iv[b][1]) : Integer.compare(a, b)); // end, then position
        boolean[] kept = new boolean[iv.length];
        long lastEnd = Long.MIN_VALUE;
        for (int p : order) {                                         // one test per interval
            if (iv[p][0] >= lastEnd) { kept[p] = true; lastEnd = iv[p][1]; } // keep when the model allows touching
        }
        int[] out = new int[iv.length];
        int n = 0;
        for (int i = 0; i < iv.length; i++) if (!kept[i]) out[n++] = i; // increasing positions
        return Arrays.copyOf(out, n);
    }

    static int brute(int[][] m) {
        int best = 0;
        for (int mask = 0; mask < (1 << m.length); mask++) {
            boolean ok = true;
            for (int a = 0; a < m.length && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < m.length; b++) {
                    if ((mask >> b & 1) != 0 && m[a][0] < m[b][1] && m[b][0] < m[a][1]) { ok = false; break; }
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(removed(new int[][] {{1, 2}, {2, 3}, {3, 4}, {1, 3}}), new int[] {3})) throw new AssertionError("ex1");
        if (!Arrays.equals(removed(new int[][] {{1, 2}, {1, 2}, {1, 2}}), new int[] {1, 2})) throw new AssertionError("ex2");
        if (removed(new int[0][]).length != 0) throw new AssertionError("empty");
        // Random inputs: the kept set must be valid, and its size must be the optimum.
        Random rnd = new Random(2012);
        for (int t = 0; t < 500; t++) {
            int[][] m = new int[rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(8) - 4; m[k] = new int[] {s, s + 1 + rnd.nextInt(4)}; }
            int[] r = removed(m);
            if (m.length - r.length != brute(m)) throw new AssertionError("size " + t);
            boolean[] gone = new boolean[m.length];
            for (int k = 0; k < r.length; k++) { gone[r[k]] = true; if (k > 0 && r[k - 1] >= r[k]) throw new AssertionError("order " + t); }
            for (int a = 0; a < m.length; a++) for (int b = a + 1; b < m.length; b++)
                if (!gone[a] && !gone[b] && m[a][0] < m[b][1] && m[b][0] < m[a][1]) throw new AssertionError("overlap " + t);
        }
    }
}
```

#### Solution: [Boundary] Touching Endpoint Contract (Author exercise)
<!-- id: gr-touching-endpoint-contract -->

**Approach.**
The method uses the end-order scan and changes only the compatibility test. A closed interval includes both ends, so the next start must be strictly greater than `lastEnd`. A half-open interval excludes its end, so the next start may equal `lastEnd`. The constraints rule out empty half-open intervals, because an empty interval could sit before an equal end in the sort and block a neighbor that it does not truly overlap. The boundary case is equal endpoints, and the flag decides it in one comparison.

After each step, `lastEnd` is the end of the last accepted interval, and the test uses the operator of the chosen model.

**Complexity.**
- **Time** is O(n log n) for the sort, and the scan adds O(n).
- **Space** is O(n) for the sorted copy.

```java run
import java.util.*;

public final class TouchingEndpointContract {
    /**
     * Returns the largest set of intervals that no two overlap in the chosen model.
     * Time: O(n log n). Space: O(n).
     * Invariant: lastEnd is the earliest end reachable by a schedule of the accepted size.
     */
    static int maxSet(int[][] intervals, boolean closed) {
        int[][] byEnd = intervals.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));   // earliest end first
        int accepted = 0;
        long lastEnd = Long.MIN_VALUE;
        for (int[] m : byEnd) {                                       // one test per interval
            boolean ok = closed ? m[0] > lastEnd : m[0] >= lastEnd;   // closed: sharing an endpoint overlaps
            if (ok) { accepted++; lastEnd = m[1]; }
        }
        return accepted;
    }

    static int brute(int[][] m, boolean closed) {
        int best = 0;
        for (int mask = 0; mask < (1 << m.length); mask++) {
            boolean ok = true;
            for (int a = 0; a < m.length && ok; a++) {
                if ((mask >> a & 1) == 0) continue;
                for (int b = a + 1; b < m.length; b++) {
                    if ((mask >> b & 1) == 0) continue;
                    boolean clash = closed ? m[a][0] <= m[b][1] && m[b][0] <= m[a][1] : m[a][0] < m[b][1] && m[b][0] < m[a][1];
                    if (clash) { ok = false; break; }
                }
            }
            if (ok) best = Math.max(best, Integer.bitCount(mask));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maxSet(new int[][] {{1, 2}, {2, 3}}, true) != 1) throw new AssertionError("ex1");
        if (maxSet(new int[][] {{1, 2}, {2, 3}}, false) != 2) throw new AssertionError("ex2");
        // A closed point interval conflicts with a closed neighbor that shares its coordinate.
        if (maxSet(new int[][] {{3, 3}, {1, 3}}, true) != 1 || maxSet(new int[0][], false) != 0) throw new AssertionError("point");
        // Random inputs in both models must match exhaustive search.
        Random rnd = new Random(2013);
        for (int t = 0; t < 600; t++) {
            boolean closed = rnd.nextBoolean();
            int[][] m = new int[rnd.nextInt(8)][];
            for (int k = 0; k < m.length; k++) { int s = rnd.nextInt(8); m[k] = new int[] {s, s + (closed ? rnd.nextInt(4) : 1 + rnd.nextInt(4))}; }
            if (maxSet(m, closed) != brute(m, closed)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Number of Arrows to Burst Balloons (LeetCode 452)
<!-- id: gr-balloon-group-sizes -->

**Approach.**
The method sorts the balloons by end. The first balloon in that order has the smallest end, so the first arrow goes at that end and bursts every balloon whose start is at most that end. The scan counts those balloons, and the next balloon that starts beyond the arrow begins a new group with a new arrow. An arrow at the smallest end reaches every balloon that any arrow at an earlier coordinate could reach, so no arrow is wasted. The group sizes sum to the number of balloons.

After each step, `arrowAt` is the coordinate of the current arrow, and `size` counts the balloons it has burst so far.

**Complexity.**
- **Time** is O(n log n) for the sort, and the scan adds O(n).
- **Space** is O(n) for the sorted copy and the output list.

```java run
import java.util.*;

public final class BalloonGroupSizes {
    /**
     * Returns the number of balloons burst by each arrow, placed at the smallest unburst end.
     * Time: O(n log n). Space: O(n).
     * Invariant: arrowAt is the smallest end of the current group, and size counts balloons with start <= arrowAt.
     */
    static int[] groups(int[][] points) {
        int[][] byEnd = points.clone();
        Arrays.sort(byEnd, (a, b) -> Integer.compare(a[1], b[1]));   // smallest end first, no overflow
        List<Integer> sizes = new ArrayList<>();
        long arrowAt = 0;
        int size = 0;
        for (int[] p : byEnd) {                                       // one test per balloon
            if (size > 0 && p[0] <= arrowAt) size++;                  // closed model: touching still bursts
            else {
                if (size > 0) sizes.add(size);                        // close the previous group
                arrowAt = p[1];                                       // new arrow at this smallest end
                size = 1;
            }
        }
        if (size > 0) sizes.add(size);                                // close the last group
        int[] out = new int[sizes.size()];
        for (int i = 0; i < out.length; i++) out[i] = sizes.get(i);
        return out;
    }

    static int bruteArrows(int[][] p) {
        TreeSet<Long> cand = new TreeSet<>();
        for (int[] b : p) cand.add((long) b[1]);                      // an optimal arrow can sit at some end
        List<Long> c = new ArrayList<>(cand);
        int best = Integer.MAX_VALUE;
        for (int mask = 0; mask < (1 << c.size()); mask++) {
            boolean all = true;
            for (int[] b : p) {
                boolean hit = false;
                for (int k = 0; k < c.size(); k++) if ((mask >> k & 1) != 0 && b[0] <= c.get(k) && c.get(k) <= b[1]) hit = true;
                if (!hit) { all = false; break; }
            }
            if (all) best = Math.min(best, Integer.bitCount(mask));
        }
        return p.length == 0 ? 0 : best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(groups(new int[][] {{10, 16}, {2, 8}, {1, 6}, {7, 12}}), new int[] {2, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(groups(new int[][] {{1, 2}, {3, 4}, {5, 6}}), new int[] {1, 1, 1})) throw new AssertionError("ex2");
        // Extreme coordinates sort without overflow, and the empty input gives an empty array.
        if (!Arrays.equals(groups(new int[][] {{Integer.MIN_VALUE, Integer.MAX_VALUE}, {Integer.MAX_VALUE, Integer.MAX_VALUE}}), new int[] {2})) throw new AssertionError("extreme");
        if (groups(new int[0][]).length != 0) throw new AssertionError("empty");
        // Random inputs: the group count must equal the smallest arrow count, and the sizes must sum to n.
        Random rnd = new Random(2014);
        for (int t = 0; t < 500; t++) {
            int[][] p = new int[rnd.nextInt(7)][];
            for (int k = 0; k < p.length; k++) { int s = rnd.nextInt(10); p[k] = new int[] {s, s + rnd.nextInt(5)}; }
            int[] g = groups(p);
            int sum = 0;
            for (int x : g) sum += x;
            if (g.length != bruteArrows(p) || sum != p.length) throw new AssertionError("random " + t);
        }
    }
}
```
