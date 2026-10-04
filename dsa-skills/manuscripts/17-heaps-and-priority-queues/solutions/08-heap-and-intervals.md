<!-- solutions-for: 08-heap-and-intervals -->
### Heap And Intervals

#### Solution: [Build] Meeting Rooms (LeetCode 252)
<!-- id: hi-meeting-rooms -->

**Approach.** Sort the intervals by start. After sorting, a conflict can only appear between neighbours, because if some earlier interval reached past the start of an interval, it would also reach past the start of every interval between them, so the previous interval in order is the first to be tested. Interval `i` conflicts with its predecessor exactly when the predecessor's end is greater than `i`'s start, and an equal value is allowed because the intervals are half-open. The run covers both examples, and a pairwise test of every two meetings is the reference on random schedules built with many touching endpoints. One run also shows that a strict comparison in the wrong direction rejects a schedule that only touches.

**Complexity.** The sort dominates at O(n log n) time, the scan is O(n), and the extra memory is O(1) beyond the sorted copy.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MeetingRooms {
    static boolean canAttendAll(int[][] intervals, boolean touchingConflicts) {
        int[][] byStart = intervals.clone();
        Arrays.sort(byStart, (x, y) -> Integer.compare(x[0], y[0]));
        for (int i = 1; i < byStart.length; i++) {
            int previousEnd = byStart[i - 1][1];
            boolean conflict = touchingConflicts ? previousEnd >= byStart[i][0] : previousEnd > byStart[i][0];
            if (conflict) return false;
        }
        return true;
    }

    static boolean byPairs(int[][] intervals) {
        for (int i = 0; i < intervals.length; i++)
            for (int j = i + 1; j < intervals.length; j++)
                if (intervals[i][0] < intervals[j][1] && intervals[j][0] < intervals[i][1]) return false;
        return true;
    }

    public static void main(String[] args) {
        if (!canAttendAll(new int[][]{{0, 5}, {5, 9}, {12, 14}}, false)) throw new AssertionError("example 1");
        if (canAttendAll(new int[][]{{1, 6}, {5, 8}}, false)) throw new AssertionError("example 2");
        if (!canAttendAll(new int[][]{}, false)) throw new AssertionError("no meetings");
        if (canAttendAll(new int[][]{{0, 5}, {5, 9}}, true)) throw new AssertionError("a closed-style comparison rejects touching meetings");
        Random rnd = new Random(1781);
        for (int t = 0; t < 5000; t++) {
            int n = rnd.nextInt(6);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(12); a[i][1] = a[i][0] + 1 + rnd.nextInt(4); }
            if (canAttendAll(a, false) != byPairs(a)) throw new AssertionError("disagrees with the pair test on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Vary] Meeting Rooms II (LeetCode 253)
<!-- id: hi-meeting-rooms-two -->

**Approach.** Sort by start and keep a min-heap of the end times of the rooms in use. For each meeting, if the earliest end is at most the new start, poll it, since that room is free, and in every case offer the new end. The heap's final size is the number of rooms. The heap neither shrinks when a room is reused nor loses a room that is still busy, which is why its size is also the largest number of simultaneous meetings. Both examples are asserted. The reference counts, for every integer minute, how many meetings contain it, and takes the maximum, which is an independent way to get the same number.

**Complexity.** The time is O(n log n) for the sort and the heap work, and the heap holds at most one entry per room.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class MeetingRoomsTwo {
    static int minRooms(int[][] intervals) {
        int[][] byStart = intervals.clone();
        Arrays.sort(byStart, (x, y) -> Integer.compare(x[0], y[0]));
        PriorityQueue<Integer> ends = new PriorityQueue<>();
        for (int[] m : byStart) {
            if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();
            ends.offer(m[1]);
        }
        return ends.size();
    }

    static int deepestOverlap(int[][] intervals) {
        int best = 0;
        for (int minute = 0; minute <= 40; minute++) {
            int open = 0;
            for (int[] m : intervals) if (m[0] <= minute && minute < m[1]) open++;
            best = Math.max(best, open);
        }
        return best;
    }

    public static void main(String[] args) {
        if (minRooms(new int[][]{{2, 7}, {7, 9}, {3, 8}, {9, 12}}) != 2) throw new AssertionError("example 1");
        if (minRooms(new int[][]{{1, 2}}) != 1) throw new AssertionError("example 2");
        if (minRooms(new int[][]{{1, 4}, {2, 6}, {4, 7}, {5, 9}, {8, 10}}) != 3) throw new AssertionError("the traced programme needs three");
        Random rnd = new Random(1782);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = rnd.nextInt(15); a[i][1] = a[i][0] + 1 + rnd.nextInt(6); }
            if (minRooms(a) != deepestOverlap(a)) throw new AssertionError("rooms differ from the deepest overlap on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Boundary] Divide Intervals Into Minimum Number of Groups (LeetCode 2406)
<!-- id: hi-min-groups-closed -->

**Approach.** The loop is the same as for the previous rung, with the reuse test made strict: a group's last right endpoint must be smaller than the new left endpoint, because closed intervals that share a point intersect. A one-point interval `[x, x]` therefore conflicts with another copy of itself. The assertions show the effect of the tie rule on the first example, where the half-open comparison would report one group and the closed one reports two. Both examples are asserted, and the reference takes the largest number of intervals that contain a single integer point, since closed intervals conflict exactly when they share a point.

**Complexity.** The time is O(n log n) and the heap holds one entry per group, which is O(n) in the worst case.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class MinGroupsClosed {
    static int minGroups(int[][] intervals, boolean closed) {
        int[][] byLeft = intervals.clone();
        Arrays.sort(byLeft, (x, y) -> Integer.compare(x[0], y[0]));
        PriorityQueue<Integer> lastRight = new PriorityQueue<>();
        for (int[] iv : byLeft) {
            boolean reusable = !lastRight.isEmpty() && (closed ? lastRight.peek() < iv[0] : lastRight.peek() <= iv[0]);
            if (reusable) lastRight.poll();
            lastRight.offer(iv[1]);
        }
        return lastRight.size();
    }

    static int mostSharingAPoint(int[][] intervals) {
        int best = 0;
        for (int p = 0; p <= 30; p++) {
            int count = 0;
            for (int[] iv : intervals) if (iv[0] <= p && p <= iv[1]) count++;
            best = Math.max(best, count);
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] first = {{2, 5}, {5, 8}, {1, 2}, {8, 9}};
        if (minGroups(first, true) != 2) throw new AssertionError("example 1");
        if (minGroups(first, false) != 1) throw new AssertionError("the half-open rule would merge touching intervals into one group");
        if (minGroups(new int[][]{{1, 1}, {1, 1}}, true) != 2) throw new AssertionError("example 2");
        Random rnd = new Random(1783);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[][] a = new int[n][2];
            for (int i = 0; i < n; i++) { a[i][0] = 1 + rnd.nextInt(14); a[i][1] = a[i][0] + rnd.nextInt(5); }
            if (minGroups(a, true) != mostSharingAPoint(a)) throw new AssertionError("groups differ from the deepest point on " + Arrays.deepToString(a));
        }
    }
}
```

#### Solution: [Recognize] Minimum Interval to Include Each Query (LeetCode 1851)
<!-- id: hi-min-interval-queries -->

**Approach.** Sort the intervals by left end, and process the queries in increasing order while remembering each query's original position. For a query `q`, offer every interval whose left end is at most `q` into a heap ordered by size and then by right end. Then discard roots whose right end is below `q`: such an interval can never contain this query or any later one, because later queries are larger. The root after the cleanup, if there is one, is the smallest interval containing `q`, and otherwise the answer is -1. The expiry is lazy, so an expired interval that is not at the root simply waits until it surfaces. Both examples are asserted, and a scan of every interval for every query is the reference on random inputs, including queries equal to interval endpoints.

**Complexity.** Sorting costs O((n + m) log(n + m)), and every interval is offered once and polled at most once, so the total time is O((n + m) log(n + m)) with O(n + m) memory.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class MinIntervalQueries {
    static int[] smallest(int[][] intervals, int[] queries) {
        int n = intervals.length, m = queries.length;
        int[][] byLeft = intervals.clone();
        Arrays.sort(byLeft, (x, y) -> Integer.compare(x[0], y[0]));
        Integer[] order = new Integer[m];
        for (int i = 0; i < m; i++) order[i] = i;
        Arrays.sort(order, (x, y) -> Integer.compare(queries[x], queries[y]));
        PriorityQueue<int[]> heap = new PriorityQueue<>(
            (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
        int[] answer = new int[m];
        int next = 0;
        for (int idx : order) {
            int q = queries[idx];
            while (next < n && byLeft[next][0] <= q) {
                heap.offer(new int[]{byLeft[next][1] - byLeft[next][0] + 1, byLeft[next][1]});
                next++;
            }
            while (!heap.isEmpty() && heap.peek()[1] < q) heap.poll();
            answer[idx] = heap.isEmpty() ? -1 : heap.peek()[0];
        }
        return answer;
    }

    static int[] byScan(int[][] intervals, int[] queries) {
        int[] answer = new int[queries.length];
        for (int j = 0; j < queries.length; j++) {
            int best = -1;
            for (int[] iv : intervals) {
                if (iv[0] <= queries[j] && queries[j] <= iv[1]) {
                    int size = iv[1] - iv[0] + 1;
                    if (best < 0 || size < best) best = size;
                }
            }
            answer[j] = best;
        }
        return answer;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(smallest(new int[][]{{2, 5}, {1, 3}, {6, 9}, {3, 3}}, new int[]{3, 1, 6, 10, 4}), new int[]{1, 3, 4, -1, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(smallest(new int[][]{{4, 4}}, new int[]{4, 5}), new int[]{1, -1})) throw new AssertionError("example 2");
        Random rnd = new Random(1784);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(7), m = 1 + rnd.nextInt(7);
            int[][] iv = new int[n][2];
            for (int i = 0; i < n; i++) { iv[i][0] = 1 + rnd.nextInt(12); iv[i][1] = iv[i][0] + rnd.nextInt(6); }
            int[] q = new int[m];
            for (int j = 0; j < m; j++) q[j] = 1 + rnd.nextInt(18);
            if (!Arrays.equals(smallest(iv, q), byScan(iv, q))) throw new AssertionError("differs on " + Arrays.deepToString(iv) + " " + Arrays.toString(q));
        }
    }
}
```
