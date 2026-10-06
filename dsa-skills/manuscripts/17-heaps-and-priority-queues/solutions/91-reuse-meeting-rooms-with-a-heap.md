<!-- solutions-for: 91-reuse-meeting-rooms-with-a-heap -->
### Solutions For Reusing Meeting Rooms

#### Solution: [Build] Meeting Rooms (LeetCode 252)
<!-- id: hp-meeting-rooms -->

**Approach.**
The method sorts a copy of the intervals by start time. After the sort, a conflict can only appear between neighbors. Suppose a meeting overlaps a later one. Its end then lies beyond the start of the next meeting in sorted order, because that next start is no larger than the later start. The loop therefore compares the end of each meeting with the start of the next. An end that is larger than the next start is a conflict. An end equal to the next start is allowed, because the intervals are half-open.

The invariant is that every meeting before the current position ends at or before the start of the current meeting.

**Complexity.**
- **Time** is O(n log n), because the sort dominates and the neighbor loop costs O(n).
- **Space** is O(n), because the method sorts a copy and keeps the input unchanged.

```java run
import java.util.*;

public final class MeetingRooms {
    /**
     * Returns true when no two half-open meetings share a point.
     * Time: O(n log n). Space: O(n).
     * Invariant: every earlier meeting ends at or before the current start.
     */
    static boolean canAttendAll(int[][] intervals) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        // Only sorted neighbors can conflict, and a shared endpoint is allowed.
        for (int i = 1; i < sorted.length; i++) {
            if (sorted[i - 1][1] > sorted[i][0]) return false;
        }
        return true;
    }

    /** Oracle: compare every pair of meetings. */
    static boolean oracle(int[][] iv) {
        for (int i = 0; i < iv.length; i++) {
            for (int j = i + 1; j < iv.length; j++) {
                // Half-open meetings share a point when each starts before the other ends.
                if (iv[i][0] < iv[j][1] && iv[j][0] < iv[i][1]) return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!canAttendAll(new int[][] {{8, 10}, {2, 4}, {4, 8}})) throw new AssertionError("ex1");
        if (canAttendAll(new int[][] {{1, 5}, {4, 6}})) throw new AssertionError("ex2");
        if (!canAttendAll(new int[0][])) throw new AssertionError("empty");
        // The input keeps its order.
        int[][] in = {{5, 6}, {1, 2}};
        canAttendAll(in);
        if (in[0][0] != 5) throw new AssertionError("mutation");
        // Random meetings must match the pairwise oracle.
        Random rnd = new Random(1781);
        for (int t = 0; t < 500; t++) {
            int[][] a = new int[rnd.nextInt(6)][];
            for (int i = 0; i < a.length; i++) { int s = rnd.nextInt(12); a[i] = new int[] {s, s + 1 + rnd.nextInt(4)}; }
            if (canAttendAll(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Meeting Rooms II (LeetCode 253)
<!-- id: hp-meeting-rooms-two -->

**Approach.**
The method sorts the meetings by start time and keeps a queue of end times, one for each room in use. For each meeting, the root of the queue is the earliest finish. If the earliest finish is at most the new start, the meeting takes over that room, and the method removes the old end time. The method then offers the new end time in both cases. A reuse removes one entry and adds one, so the size does not change. A new room only adds an entry. The final size is the number of rooms.

Each room used so far owns one end time in the queue, the end of its last meeting. The size equals the largest number of meetings that shared a point.

**Complexity.**
- **Time** is O(n log n), because the sort costs O(n log n) and each meeting makes at most one poll and one offer.
- **Space** is O(n), because the queue holds one end time per room.

```java run
import java.util.*;

public final class MeetingRoomsTwo {
    /**
     * Returns the minimum number of rooms for half-open meetings.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds one end time per room in use.
     */
    static int minRooms(int[][] intervals) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        PriorityQueue<Integer> ends = new PriorityQueue<>();
        for (int[] m : sorted) {
            // The earliest finish at most the start means that room is free.
            if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();
            // The meeting holds its room until its own end time.
            ends.offer(m[1]);
        }
        return ends.size();
    }

    /** Oracle: the largest number of meetings active at one integer time. */
    static int oracle(int[][] iv) {
        int best = 0;
        for (int t = 0; t <= 40; t++) {
            int active = 0;
            for (int[] m : iv) if (m[0] <= t && t < m[1]) active++;
            best = Math.max(best, active);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (minRooms(new int[][] {{1, 4}, {2, 5}, {4, 6}, {5, 7}}) != 2) throw new AssertionError("ex1");
        if (minRooms(new int[][] {{3, 9}}) != 1) throw new AssertionError("ex2");
        if (minRooms(new int[0][]) != 0) throw new AssertionError("empty");
        // Half-open meetings that touch at one endpoint share a room.
        if (minRooms(new int[][] {{1, 3}, {3, 5}}) != 1) throw new AssertionError("touching");
        // The opening example: pairwise overlaps count three, yet two rooms are enough.
        if (minRooms(new int[][] {{1, 10}, {2, 3}, {4, 5}}) != 2) throw new AssertionError("pairs");
        // Random meetings must match the active-count oracle.
        Random rnd = new Random(1782);
        for (int t = 0; t < 600; t++) {
            int[][] a = new int[rnd.nextInt(9)][];
            for (int i = 0; i < a.length; i++) { int s = rnd.nextInt(15); a[i] = new int[] {s, s + 1 + rnd.nextInt(6)}; }
            if (minRooms(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Divide Intervals Into Minimum Number of Groups (LeetCode 2406)
<!-- id: hp-divide-intervals-groups -->

**Approach.**
The method is the room planner with a strict test. A closed interval `[left, right]` contains both endpoints, so an interval that starts at 3 shares a point with an interval that ends at 3. The earliest finish frees a group only when it is smaller than the new left end. With the test `<=`, the method would place `[1,3]` and `[3,5]` in one group and report one group too few for the example. The rest of the method is unchanged: sort by left end, reuse or open a group, and offer the right end.

Each group owns one right end in the queue, the right end of its last interval, and the intervals of one group share no point.

**Complexity.**
- **Time** is O(n log n), because the sort and the queue operations each cost O(n log n) in total.
- **Space** is O(n), because the queue holds one right end per group.

```java run
import java.util.*;

public final class DivideIntoGroups {
    /**
     * Returns the minimum number of groups of pairwise disjoint closed intervals.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds the last right end of each group.
     */
    static int minGroups(int[][] intervals) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        PriorityQueue<Integer> ends = new PriorityQueue<>();
        for (int[] iv : sorted) {
            // Closed intervals: a shared endpoint is a shared point, so the test is strict.
            if (!ends.isEmpty() && ends.peek() < iv[0]) ends.poll();
            ends.offer(iv[1]);
        }
        return ends.size();
    }

    /** Oracle: the largest number of intervals that contain one integer point. */
    static int oracle(int[][] iv) {
        int best = 0;
        for (int t = 0; t <= 40; t++) {
            int cover = 0;
            for (int[] x : iv) if (x[0] <= t && t <= x[1]) cover++;
            best = Math.max(best, cover);
        }
        return best;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (minGroups(new int[][] {{1, 3}, {3, 5}, {6, 8}}) != 2) throw new AssertionError("ex1");
        if (minGroups(new int[][] {{2, 2}}) != 1) throw new AssertionError("ex2");
        // Touching closed intervals share a point, so they need two groups.
        if (minGroups(new int[][] {{1, 3}, {3, 5}}) != 2) throw new AssertionError("touching");
        // Random closed intervals, including single points, must match the point-cover oracle.
        Random rnd = new Random(1783);
        for (int t = 0; t < 600; t++) {
            int[][] a = new int[1 + rnd.nextInt(9)][];
            for (int i = 0; i < a.length; i++) { int l = rnd.nextInt(15); a[i] = new int[] {l, l + rnd.nextInt(6)}; }
            if (minGroups(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Minimum Interval to Include Each Query (LeetCode 1851)
<!-- id: hp-minimum-interval-query -->

**Approach.**
The method sorts the intervals by left end and the queries by value, and it answers the queries in increasing order. For the current query `q`, it adds every interval with left end at most `q` to a queue ordered by size and then right end. An interval whose right end is below `q` cannot contain `q` or any later query, so it is stale. The method polls stale intervals from the root, because stale entries below the root do no harm until they surface. The root is then the smallest interval that contains `q`. If the queue is empty, no interval contains `q`, and the answer is -1. The method writes each answer at the original position of its query.

The invariant is that, after cleaning, the root is the smallest interval among those with left end at most `q` and right end at least `q`.

**Complexity.**
- **Time** is O((n + m) log(n + m)), for `n` intervals and `m` queries, because both sorts and the queue operations cost logarithmic time per item.
- **Space** is O(n + m), because the queue, the sorted copies and the result hold up to that many entries.

```java run
import java.util.*;

public final class MinimumIntervalQuery {
    /**
     * Returns, for each query, the size of the smallest interval that contains it, or -1.
     * Time: O((n + m) log(n + m)). Space: O(n + m).
     * Invariant: after cleaning, the root is the smallest interval that contains the query.
     */
    static int[] minInterval(int[][] intervals, int[] queries) {
        int[][] sorted = intervals.clone();
        Arrays.sort(sorted, (a, b) -> Integer.compare(a[0], b[0]));
        Integer[] order = new Integer[queries.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> Integer.compare(queries[a], queries[b]));
        // Entries are {size, right end}; the smallest size is the root.
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int[] answer = new int[queries.length];
        int next = 0;
        for (int idx : order) {
            int q = queries[idx];
            // Add every interval that has started by q.
            while (next < sorted.length && sorted[next][0] <= q) {
                queue.offer(new int[] {sorted[next][1] - sorted[next][0] + 1, sorted[next][1]});
                next++;
            }
            // A right end below q means the interval cannot contain q or any later query.
            while (!queue.isEmpty() && queue.peek()[1] < q) queue.poll();
            answer[idx] = queue.isEmpty() ? -1 : queue.peek()[0];
        }
        return answer;
    }

    /** Oracle: scan every interval for every query. */
    static int[] oracle(int[][] iv, int[] qs) {
        int[] out = new int[qs.length];
        for (int j = 0; j < qs.length; j++) {
            int best = -1;
            for (int[] x : iv) {
                if (x[0] <= qs[j] && qs[j] <= x[1]) {
                    int size = x[1] - x[0] + 1;
                    if (best == -1 || size < best) best = size;
                }
            }
            out[j] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(minInterval(new int[][] {{2, 5}, {3, 4}, {7, 9}}, new int[] {3, 5, 8, 10}), new int[] {2, 4, 3, -1})) throw new AssertionError("ex1");
        if (!Arrays.equals(minInterval(new int[][] {{1, 1}}, new int[] {1, 2}), new int[] {1, -1})) throw new AssertionError("ex2");
        // Queries in descending order still answer in their original positions.
        if (!Arrays.equals(minInterval(new int[][] {{2, 5}, {3, 4}}, new int[] {5, 3}), new int[] {4, 2})) throw new AssertionError("order");
        // Random inputs must match the scan oracle.
        Random rnd = new Random(1784);
        for (int t = 0; t < 600; t++) {
            int[][] iv = new int[1 + rnd.nextInt(6)][];
            for (int i = 0; i < iv.length; i++) { int l = 1 + rnd.nextInt(12); iv[i] = new int[] {l, l + rnd.nextInt(6)}; }
            int[] qs = new int[1 + rnd.nextInt(8)];
            for (int i = 0; i < qs.length; i++) qs[i] = 1 + rnd.nextInt(20);
            if (!Arrays.equals(minInterval(iv, qs), oracle(iv, qs))) throw new AssertionError("random " + t);
        }
    }
}
```
