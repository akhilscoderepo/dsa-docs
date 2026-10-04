<!-- solutions-for: 20-greedy -->
### Task Selection

#### Solution: [Build] Maximum Units on a Truck (LeetCode 1710)
<!-- id: gr-maximum-units -->

**Approach.** Sort a copy of the kinds by units per box, highest first. Walk the sorted kinds and take as many boxes of each as the remaining places allow, adding `take * unitsPerBox` to a `long` total. A better box can always replace a worse one on the truck without changing the number of boxes, so the fill never needs to be reconsidered. The assertions check both examples and a truck larger than the supply, and compare random small instances with a recursion that tries every number of boxes from every kind.

**Complexity.** Sorting gives O(k log k) for k kinds, after which the fill is a single pass of at most k steps.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaximumUnits {
    static long maxUnits(long[][] types, long truck) {
        long[][] order = types.clone();
        Arrays.sort(order, (a, b) -> Long.compare(b[1], a[1]));
        long units = 0;
        for (long[] t : order) {
            if (truck == 0) break;
            long take = Math.min(t[0], truck);
            units += take * t[1];
            truck -= take;
        }
        return units;
    }

    static long oracle(long[][] types, int idx, long truck) {
        if (idx == types.length) return 0;
        long best = 0;
        for (long take = 0; take <= Math.min(types[idx][0], truck); take++) {
            best = Math.max(best, take * types[idx][1] + oracle(types, idx + 1, truck - take));
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxUnits(new long[][]{{3, 7}, {5, 2}, {2, 9}, {4, 4}}, 8) != 51) throw new AssertionError("example 1");
        if (maxUnits(new long[][]{{1, 5}, {2, 3}}, 100) != 11) throw new AssertionError("example 2");
        if (maxUnits(new long[0][], 5) != 0) throw new AssertionError("no boxes");
        if (maxUnits(new long[][]{{4, 9}}, 0) != 0) throw new AssertionError("no room");
        long[][] before = {{1, 1}, {1, 9}};
        maxUnits(before, 1);
        if (before[0][1] != 1 || before[1][1] != 9) throw new AssertionError("input order was changed");

        Random rnd = new Random(2501);
        for (int t = 0; t < 4000; t++) {
            int k = rnd.nextInt(5);
            long[][] types = new long[k][];
            for (int i = 0; i < k; i++) types[i] = new long[]{rnd.nextInt(5), rnd.nextInt(7)};
            long truck = rnd.nextInt(10);
            if (maxUnits(types, truck) != oracle(types, 0, truck)) throw new AssertionError("disagrees with the exhaustive fill");
        }
    }
}
```

#### Solution: [Vary] Deadline-Compatible Unit Tasks (Author exercise)
<!-- id: gr-unit-tasks-deadlines -->

**Approach.** Sort a copy of the deadlines. Keep a count `done` of tasks already placed in slots 1 to `done`. A task with deadline `x` can still be placed when `done < x`, because slot `done + 1` is free and lies within its deadline. Each task takes one slot, so no earlier acceptance ever needs to be undone. A deadline of 0 never passes the test. The oracle tries every subset and decides whether it can be scheduled by bipartite matching of tasks to slots, using augmenting paths, which does not rely on the sorted-order argument. The assertions also cover both examples.

**Complexity.** The sort dominates at O(n log n), followed by a single pass; the oracle is exponential in n.

```java run
import java.util.Arrays;
import java.util.Random;

public final class UnitTasksDeadlines {
    static int most(int[] deadlines) {
        int[] d = deadlines.clone();
        Arrays.sort(d);
        int done = 0;
        for (int x : d) if (done < x) done++;
        return done;
    }

    static boolean augment(int task, int[] d, int[] slotOwner, boolean[] seen) {
        for (int slot = 1; slot <= d[task]; slot++) {
            if (seen[slot]) continue;
            seen[slot] = true;
            if (slotOwner[slot] == -1 || augment(slotOwner[slot], d, slotOwner, seen)) { slotOwner[slot] = task; return true; }
        }
        return false;
    }

    static boolean schedulable(int[] chosen) {
        int maxD = 0;
        for (int x : chosen) maxD = Math.max(maxD, x);
        int[] owner = new int[maxD + 2];
        Arrays.fill(owner, -1);
        for (int t = 0; t < chosen.length; t++) {
            if (!augment(t, chosen, owner, new boolean[maxD + 2])) return false;
        }
        return true;
    }

    static int oracle(int[] d) {
        int n = d.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int[] chosen = new int[Integer.bitCount(mask)];
            for (int i = 0, k = 0; i < n; i++) if ((mask >> i & 1) == 1) chosen[k++] = d[i];
            if (chosen.length > best && schedulable(chosen)) best = chosen.length;
        }
        return best;
    }

    public static void main(String[] args) {
        if (most(new int[]{3, 1, 1, 4, 3}) != 4) throw new AssertionError("example 1");
        if (most(new int[]{0, 5}) != 1) throw new AssertionError("example 2");
        if (most(new int[0]) != 0) throw new AssertionError("no tasks");
        if (most(new int[]{2, 2, 2, 2}) != 2) throw new AssertionError("equal deadlines share the same slots");
        if (most(new int[]{1000000000, 1000000000}) != 2) throw new AssertionError("far deadlines");

        Random rnd = new Random(2502);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(9);
            int[] d = new int[n];
            for (int i = 0; i < n; i++) d[i] = rnd.nextInt(6);
            if (most(d) != oracle(d)) throw new AssertionError("disagrees with the matching oracle on " + Arrays.toString(d));
        }
    }
}
```

#### Solution: [Boundary] Equal Reward And Capacity Limit (Author exercise)
<!-- id: gr-equal-reward-capacity -->

**Approach.** Sort the kinds by units per box in descending order, breaking ties by the lower input index. To make that tie rule explicit the sort works on index positions rather than on rows. Walk the order and take `min(boxes, places left)` from each kind, adding the product in `long` and counting the kind when the take is positive. The assertions show that the product in the second example is wrong in 32-bit arithmetic and right in `long`. Random small inputs are compared with a brute-force loader that expands every box into its own entry, orders the entries by value and then kind index, and takes the first `truck` of them.

**Complexity.** The sort costs O(k log k) and the fill is one pass over k kinds.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public final class EqualRewardCapacity {
    static long[] load(long[][] types, long truck) {
        Integer[] order = new Integer[types.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> types[a][1] != types[b][1] ? Long.compare(types[b][1], types[a][1]) : Integer.compare(a, b));
        long units = 0, kinds = 0;
        for (int idx : order) {
            if (truck == 0) break;
            long take = Math.min(types[idx][0], truck);
            if (take > 0) { units += take * types[idx][1]; kinds++; truck -= take; }
        }
        return new long[]{units, kinds};
    }

    static long[] brute(long[][] types, long truck) {
        java.util.List<long[]> boxes = new java.util.ArrayList<>();
        for (int i = 0; i < types.length; i++) for (long b = 0; b < types[i][0]; b++) boxes.add(new long[]{types[i][1], i});
        boxes.sort((x, y) -> x[0] != y[0] ? Long.compare(y[0], x[0]) : Long.compare(x[1], y[1]));
        long units = 0;
        TreeSet<Long> kinds = new TreeSet<>();
        for (int i = 0; i < Math.min(truck, boxes.size()); i++) { units += boxes.get(i)[0]; kinds.add(boxes.get(i)[1]); }
        return new long[]{units, kinds.size()};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(load(new long[][]{{2, 5}, {3, 5}, {1, 5}}, 4), new long[]{20, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(load(new long[][]{{2000000000L, 2147483647L}}, 2000000000L), new long[]{4294967294000000000L, 1})) throw new AssertionError("example 2");
        int wrapped = 2000000000 * 2147483647;
        if ((long) wrapped == 4294967294000000000L) throw new AssertionError("the int product must not equal the true product");
        if (!Arrays.equals(load(new long[0][], 7), new long[]{0, 0})) throw new AssertionError("no kinds");
        if (!Arrays.equals(load(new long[][]{{5, 3}}, 0), new long[]{0, 0})) throw new AssertionError("empty truck");
        if (!Arrays.equals(load(new long[][]{{0, 9}, {2, 1}}, 5), new long[]{2, 1})) throw new AssertionError("a kind with no boxes is not counted");

        Random rnd = new Random(2503);
        for (int t = 0; t < 5000; t++) {
            int k = rnd.nextInt(6);
            long[][] types = new long[k][];
            for (int i = 0; i < k; i++) types[i] = new long[]{rnd.nextInt(5), rnd.nextInt(4)};
            long truck = rnd.nextInt(12);
            if (!Arrays.equals(load(types, truck), brute(types, truck))) throw new AssertionError("disagrees with the box-by-box loader on " + Arrays.deepToString(types) + " truck " + truck);
        }
    }
}
```

#### Solution: [Recognize] Course Schedule III (LeetCode 630)
<!-- id: gr-course-schedule-three -->

**Approach.** Sort a copy by last day. Add each course to the running total and to a max-heap of durations. If the total now passes that course's last day, remove the longest duration in the heap and subtract it, which drops the newcomer itself when it is the longest. The heap size at the end is the answer. The total is a `long`, since three durations of one billion exceed the `int` range. The assertions check both examples, show that accepting whatever fits without removal returns 1 on the first example while the answer is 2, and compare random small inputs with an enumeration of every subset, each simulated in deadline order.

**Complexity.** The sort and the heap operations together give O(n log n) time, with O(n) memory for the heap.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class CourseScheduleThree {
    static int mostCourses(int[][] courses) {
        int[][] order = courses.clone();
        Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
        PriorityQueue<Integer> kept = new PriorityQueue<>(Comparator.reverseOrder());
        long time = 0;
        for (int[] c : order) {
            kept.add(c[0]);
            time += c[0];
            if (time > c[1]) time -= kept.poll();
        }
        return kept.size();
    }

    static int acceptIfFits(int[][] courses) {
        int[][] order = courses.clone();
        Arrays.sort(order, (a, b) -> Integer.compare(a[1], b[1]));
        long time = 0;
        int taken = 0;
        for (int[] c : order) if (time + c[0] <= c[1]) { time += c[0]; taken++; }
        return taken;
    }

    static int oracle(int[][] courses) {
        int n = courses.length, best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int[][] chosen = new int[Integer.bitCount(mask)][];
            for (int i = 0, k = 0; i < n; i++) if ((mask >> i & 1) == 1) chosen[k++] = courses[i];
            Arrays.sort(chosen, (a, b) -> Integer.compare(a[1], b[1]));
            long time = 0;
            boolean ok = true;
            for (int[] c : chosen) { time += c[0]; if (time > c[1]) { ok = false; break; } }
            if (ok) best = Math.max(best, chosen.length);
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] ex1 = {{5, 5}, {4, 6}, {2, 6}};
        if (mostCourses(ex1) != 2) throw new AssertionError("example 1");
        if (acceptIfFits(ex1) != 1) throw new AssertionError("accept-if-fits should fail on example 1");
        int big = 1000000000;
        if (mostCourses(new int[][]{{big, big}, {big, 2 * big}, {big, 2 * big}}) != 2) throw new AssertionError("example 2");
        int wrapped = big + big + big;
        if (wrapped >= 0) throw new AssertionError("an int total of three billions must wrap negative");
        if (mostCourses(new int[0][]) != 0) throw new AssertionError("no courses");
        if (mostCourses(new int[][]{{7, 3}, {1, 1}}) != 1) throw new AssertionError("a course longer than its own last day is never kept");
        if (mostCourses(new int[][]{{2, 3}, {2, 3}, {2, 3}}) != 1) throw new AssertionError("equal courses compete for one slot");

        Random rnd = new Random(2504);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(9);
            int[][] c = new int[n][];
            for (int i = 0; i < n; i++) c[i] = new int[]{1 + rnd.nextInt(6), 1 + rnd.nextInt(14)};
            if (mostCourses(c) != oracle(c)) throw new AssertionError("disagrees with the subset search on " + Arrays.deepToString(c));
        }
    }
}
```
