<!-- solutions-for: 05-task-selection -->
### Solutions For Task Selection

#### Solution: [Build] Maximum Units on a Truck (LeetCode 1710)
<!-- id: gr-maximum-units-truck -->

**Approach.**
The method sorts the box types by units per box in decreasing order and loads whole types while room remains. For the last type that does not fit completely, it loads as many boxes as the remaining room allows and stops. The swap argument is direct: in any full truck, replacing a box that carries fewer units with an unused box that carries more raises the total and keeps the box count, so a truck that skips a better box while holding a worse one is not best.

After each type, the truck holds the best total for the boxes loaded so far, and `room` is the space left.

**Complexity.**
- **Time** is O(t log t) for `t` box types, because the sort dominates the scan.
- **Space** is O(1) extra beyond the sort.

```java run
import java.util.*;

public final class MaximumUnitsTruck {
    /**
     * Returns the largest total units for a truck of the given box capacity.
     * Time: O(t log t). Space: O(1) extra.
     * Invariant: the loaded boxes are the best possible for the room already used.
     */
    static int maximumUnits(int[][] boxTypes, int truckSize) {
        Arrays.sort(boxTypes, (a, b) -> Integer.compare(b[1], a[1]));   // most units per box first
        int room = truckSize, units = 0;
        for (int[] t : boxTypes) {                                      // one type per step
            if (room == 0) break;                                       // the truck is full
            int take = Math.min(room, t[0]);                            // all of the type or what fits
            units += take * t[1];
            room -= take;
        }
        return units;
    }

    static int brute(int[][] types, int size) {
        List<Integer> all = new ArrayList<>();
        for (int[] t : types) for (int k = 0; k < t[0]; k++) all.add(t[1]);
        int best = 0;
        for (int mask = 0; mask < (1 << all.size()); mask++) {          // every set of boxes
            if (Integer.bitCount(mask) > size) continue;
            int sum = 0;
            for (int k = 0; k < all.size(); k++) if ((mask >> k & 1) != 0) sum += all.get(k);
            best = Math.max(best, sum);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (maximumUnits(new int[][] {{1, 3}, {2, 2}, {3, 1}}, 4) != 8) throw new AssertionError("ex1");
        if (maximumUnits(new int[][] {{2, 4}, {3, 6}, {1, 9}}, 5) != 31) throw new AssertionError("ex2");
        // Random small inputs must match exhaustive choice of boxes.
        Random rnd = new Random(2051);
        for (int t = 0; t < 400; t++) {
            int[][] types = new int[1 + rnd.nextInt(3)][];
            for (int k = 0; k < types.length; k++) types[k] = new int[] {1 + rnd.nextInt(3), 1 + rnd.nextInt(9)};
            int size = 1 + rnd.nextInt(8);
            int expect = brute(types, size);
            if (maximumUnits(types.clone(), size) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Deadline-Compatible Unit Tasks (Author exercise)
<!-- id: gr-deadline-unit-tasks -->

**Approach.**
The method sorts the deadlines in increasing order and counts the accepted tasks. A task with deadline `d` is accepted when fewer than `d` tasks are already accepted, which means slot `count + 1` is at most `d`. Since every duration is one, the retained set never has to drop a task, because a task that does not fit cannot be repaired by removing an equal-length task. Skipping a task that fails the test loses nothing, as all later deadlines are at least as large and use the same free slots.

After each deadline, `count` is the largest feasible number among the tasks read so far.

**Complexity.**
- **Time** is O(n log n), since the sort costs more than the one-pass scan that follows.
- **Space** is O(1) extra beyond the sort.

```java run
import java.util.*;

public final class DeadlineUnitTasks {
    /**
     * Returns the largest number of unit tasks that meet their deadlines.
     * Time: O(n log n). Space: O(1) extra.
     * Invariant: count tasks occupy slots 1..count, and count is the best for the deadlines read.
     */
    static int schedule(int[] deadlines) {
        Arrays.sort(deadlines);                                        // earliest deadline first
        int count = 0;
        for (int d : deadlines) {                                      // one test per task
            if (count < d) count++;                                    // slot count + 1 is at most d
        }
        return count;
    }

    static int brute(int[] d) {
        int best = 0;
        for (int mask = 0; mask < (1 << d.length); mask++) {           // every subset of tasks
            int[] chosen = new int[Integer.bitCount(mask)];
            int n = 0;
            for (int k = 0; k < d.length; k++) if ((mask >> k & 1) != 0) chosen[n++] = d[k];
            Arrays.sort(chosen);
            boolean ok = true;
            for (int k = 0; k < n; k++) if (chosen[k] < k + 1) ok = false; // k-th task runs in slot k + 1
            if (ok) best = Math.max(best, n);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (schedule(new int[] {2, 1, 2}) != 2) throw new AssertionError("ex1");
        if (schedule(new int[] {1, 1, 1}) != 1) throw new AssertionError("ex2");
        // Empty input and one huge deadline.
        if (schedule(new int[0]) != 0 || schedule(new int[] {1_000_000_000}) != 1) throw new AssertionError("edge");
        // Random inputs must match exhaustive subsets.
        Random rnd = new Random(2052);
        for (int t = 0; t < 500; t++) {
            int[] d = new int[rnd.nextInt(8)];
            for (int k = 0; k < d.length; k++) d[k] = 1 + rnd.nextInt(5);
            int expect = brute(d);
            if (schedule(d.clone()) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Equal Reward And Capacity Limit (Author exercise)
<!-- id: gr-equal-reward-capacity -->

**Approach.**
The method sorts the type indices by reward in decreasing order and breaks ties by the smaller index. It then takes units from each type in that order until the capacity is spent. The tie rule decides the returned amounts only, because equal rewards give the same total. Every product `taken * reward` uses `long`, since two values of 10^9 multiply to 10^18, which overflows `int`. A capacity larger than the total number of units simply takes every unit.

After each type, `room` is the unused capacity, and `total` is the reward of the units taken so far.

**Complexity.**
- **Time** is O(n log n), because the sort of the indices dominates.
- **Space** is O(n) for the index array and the output.

```java run
import java.util.*;

public final class EqualRewardCapacity {
    /**
     * Returns taken units per type, followed by the total reward.
     * Time: O(n log n). Space: O(n).
     * Invariant: room units remain, and total is the reward of the taken units.
     */
    static long[] fill(int[] counts, int[] rewards, int capacity) {
        int n = counts.length;
        Integer[] order = new Integer[n];
        for (int i = 0; i < n; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> rewards[a] != rewards[b] ? Integer.compare(rewards[b], rewards[a]) : Integer.compare(a, b)); // reward desc, index asc
        long[] out = new long[n + 1];
        long room = capacity, total = 0;                                // long avoids overflow
        for (int i : order) {                                           // one type per step
            long take = Math.min(room, counts[i]);                      // what fits of this type
            out[i] = take;
            total += take * rewards[i];                                 // up to 10^9 * 10^9
            room -= take;
        }
        out[n] = total;
        return out;
    }

    static long[] brute(int[] c, int[] r, int cap) {
        int n = c.length;
        long[] out = new long[n + 1];
        long room = cap;
        while (room > 0) {                                              // take one unit at a time from the best type
            int best = -1;
            for (int i = 0; i < n; i++) if (out[i] < c[i] && (best < 0 || r[i] > r[best])) best = i;
            if (best < 0) break;
            out[best]++; room--; out[n] += r[best];
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(fill(new int[] {3, 2}, new int[] {5, 5}, 4), new long[] {3, 1, 20})) throw new AssertionError("ex1");
        if (!Arrays.equals(fill(new int[] {1_000_000_000}, new int[] {1_000_000_000}, 1_000_000_000), new long[] {1_000_000_000L, 1_000_000_000_000_000_000L})) throw new AssertionError("ex2");
        // A capacity above the total units takes everything.
        if (!Arrays.equals(fill(new int[] {1, 1}, new int[] {2, 3}, 10), new long[] {1, 1, 5})) throw new AssertionError("large capacity");
        // Random small inputs must match a unit-by-unit simulation with the same tie rule.
        Random rnd = new Random(2053);
        for (int t = 0; t < 500; t++) {
            int n = 1 + rnd.nextInt(5);
            int[] c = new int[n], r = new int[n];
            for (int k = 0; k < n; k++) { c[k] = 1 + rnd.nextInt(4); r[k] = 1 + rnd.nextInt(3); }
            int cap = 1 + rnd.nextInt(12);
            if (!Arrays.equals(fill(c, r, cap), brute(c, r, cap))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Course Schedule III (LeetCode 630)
<!-- id: gr-course-schedule-iii -->

**Approach.**
The method sorts the courses by last day and processes them in that order, which makes the new course the one with the latest last day. It adds the new duration to the retained set and to the running total. When the total passes the new last day, it removes the longest retained duration, which may be the new course itself. The removal lowers the total by the most possible amount and drops exactly one course. A feasible set of the first `k` courses with the most members and the smallest total is the one kept, so any later course sees the most room.

After each course, the heap holds the durations of a largest feasible set of the processed courses with the smallest total.

**Complexity.**
- **Time** is O(n log n), because the sort and the heap operations dominate.
- **Space** is O(n) for the heap and the sorted copy.

```java run
import java.util.*;

public final class CourseScheduleIII {
    /**
     * Returns the largest number of courses that finish on time.
     * Time: O(n log n). Space: O(n).
     * Invariant: the heap holds a largest feasible set of the processed courses with the smallest total.
     */
    static int scheduleCourse(int[][] courses) {
        int[][] order = courses.clone();                                // keep the caller's order
        Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));      // earliest last day first
        PriorityQueue<Integer> kept = new PriorityQueue<>(Collections.reverseOrder());
        long total = 0;
        for (int[] c : order) {                                         // one course per step
            kept.add(c[0]);                                             // the new course joins the set
            total += c[0];
            if (total > c[1]) total -= kept.poll();                     // drop the longest retained duration
        }
        return kept.size();
    }

    static int brute(int[][] c) {
        int best = 0;
        for (int mask = 0; mask < (1 << c.length); mask++) {            // every subset
            List<int[]> pick = new ArrayList<>();
            for (int k = 0; k < c.length; k++) if ((mask >> k & 1) != 0) pick.add(c[k]);
            pick.sort((a, b) -> Integer.compare(a[1], b[1]));           // deadline order is optimal for a fixed subset
            long t = 0;
            boolean ok = true;
            for (int[] p : pick) { t += p[0]; if (t > p[1]) ok = false; }
            if (ok) best = Math.max(best, pick.size());
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (scheduleCourse(new int[][] {{3, 6}, {4, 8}, {2, 5}, {7, 20}}) != 3) throw new AssertionError("ex1");
        if (scheduleCourse(new int[][] {{5, 5}, {2, 6}, {2, 6}}) != 2) throw new AssertionError("ex2");
        if (scheduleCourse(new int[0][]) != 0) throw new AssertionError("empty");
        // Random inputs must match exhaustive subsets.
        Random rnd = new Random(2054);
        for (int t = 0; t < 500; t++) {
            int[][] c = new int[rnd.nextInt(8)][];
            for (int k = 0; k < c.length; k++) c[k] = new int[] {1 + rnd.nextInt(5), 1 + rnd.nextInt(12)};
            if (scheduleCourse(c) != brute(c)) throw new AssertionError("random " + t);
        }
    }
}
```
