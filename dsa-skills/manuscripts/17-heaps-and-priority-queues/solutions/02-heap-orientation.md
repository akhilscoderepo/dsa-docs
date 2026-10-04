<!-- solutions-for: 02-heap-orientation -->
### Heap Orientation

#### Solution: [Build] Safe Max-Heap (Author exercise)
<!-- id: hp-safe-max-heap -->

**Approach.** Build the queue with `Comparator.reverseOrder()`, which compares through the elements' own `compareTo`, so no value is ever negated or subtracted. The polls then come out largest first. The assertions check both examples against a descending sort, and they demonstrate the two hazards from the lesson: negating `Integer.MIN_VALUE` returns the same number, which makes a negation-based max-heap hand out the smallest integer first, and the subtracting comparator wraps around and puts `Integer.MAX_VALUE` ahead of `-5` in a queue that is supposed to give the smaller number first.

**Complexity.** The method makes n offers and n polls of logarithmic cost, so it needs O(n log n) time and O(n) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class SafeMaxHeap {
    static int[] descending(int[] values) {
        PriorityQueue<Integer> queue = new PriorityQueue<>(Comparator.reverseOrder());
        for (int v : values) queue.offer(v);
        int[] out = new int[values.length];
        for (int i = 0; i < out.length; i++) out[i] = queue.poll();
        return out;
    }

    static int[] byNegation(int[] values) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        for (int v : values) queue.offer(-v);
        int[] out = new int[values.length];
        for (int i = 0; i < out.length; i++) out[i] = -queue.poll();
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(descending(new int[]{3, -7, 10, 3}), new int[]{10, 3, 3, -7})) throw new AssertionError("example 1");
        int min = Integer.MIN_VALUE, max = Integer.MAX_VALUE;
        if (!Arrays.equals(descending(new int[]{min, max, 0}), new int[]{max, 0, min})) throw new AssertionError("example 2");
        if (descending(new int[0]).length != 0) throw new AssertionError("empty input");

        if (-min != min) throw new AssertionError("negating the smallest int returns itself");
        int[] wrong = byNegation(new int[]{max, 0, min});
        if (wrong[0] != min) throw new AssertionError("negation hands out the smallest int first");
        PriorityQueue<Integer> subtracting = new PriorityQueue<>((a, b) -> a - b);
        subtracting.offer(-5);
        subtracting.offer(max);
        if (subtracting.peek() != max) throw new AssertionError("a - b wraps around and misorders max against -5");
        if (max - (-5) >= 0) throw new AssertionError("the difference must have wrapped to a negative number");

        Random rnd = new Random(1711);
        int[] pool = {min, max, 0, -1, 1, 7, -7};
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            ArrayList<Integer> boxed = new ArrayList<>();
            for (int v : a) boxed.add(v);
            boxed.sort(Collections.reverseOrder());
            int[] expected = new int[n];
            for (int i = 0; i < n; i++) expected[i] = boxed.get(i);
            if (!Arrays.equals(descending(a), expected)) throw new AssertionError("disagrees with the descending sort on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Pair Priority (Author exercise)
<!-- id: hp-pair-priority -->

**Approach.** Store `{duration, index}` pairs and rank them with `comparingInt` on the duration followed by `thenComparingInt` on the index. The index is unique, so the order is total and the polls are fully determined. The output is the index of each polled pair. The assertions check both examples and compare with a sort of the indices by the same tuple on random arrays with many equal durations. They also show that a comparator reading only the duration disagrees with the tuple order on some inputs, which is why the second field has to be part of the comparator.

**Complexity.** The sorting through the queue costs O(n log n) time, with O(n) memory for the pairs.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class PairPriority {
    static int[] order(int[] duration, boolean withTieBreak) {
        Comparator<int[]> cmp = Comparator.<int[]>comparingInt(t -> t[0]);
        if (withTieBreak) cmp = cmp.thenComparingInt(t -> t[1]);
        PriorityQueue<int[]> queue = new PriorityQueue<>(cmp);
        for (int i = 0; i < duration.length; i++) queue.offer(new int[]{duration[i], i});
        int[] out = new int[duration.length];
        for (int k = 0; k < out.length; k++) out[k] = queue.poll()[1];
        return out;
    }

    static int[] bySorting(int[] duration) {
        ArrayList<Integer> idx = new ArrayList<>();
        for (int i = 0; i < duration.length; i++) idx.add(i);
        idx.sort((x, y) -> duration[x] != duration[y] ? Integer.compare(duration[x], duration[y]) : Integer.compare(x, y));
        int[] out = new int[idx.size()];
        for (int i = 0; i < out.length; i++) out[i] = idx.get(i);
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(order(new int[]{4, 1, 4, 1, 3}, true), new int[]{1, 3, 4, 0, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[]{2, 2, 2}, true), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        Random rnd = new Random(1712);
        int differing = 0;
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] d = new int[n];
            for (int i = 0; i < n; i++) d[i] = 1 + rnd.nextInt(4);
            int[] expected = bySorting(d);
            if (!Arrays.equals(order(d, true), expected)) throw new AssertionError("disagrees with the tuple sort on " + Arrays.toString(d));
            if (!Arrays.equals(order(d, false), expected)) differing++;
        }
        if (differing == 0) throw new AssertionError("the duration-only comparator should break ties differently for some input");
    }
}
```

#### Solution: [Boundary] Equal Priorities And Extreme Integers (Author exercise)
<!-- id: hp-equal-priorities-extremes -->

**Approach.** The tuple is the priority in descending direction, then the index in ascending direction. The two fields run in opposite directions, so the comparator is written by hand with `Integer.compare(b, a)` on the priority and `Integer.compare(a, b)` on the index, and no subtraction appears. The assertions check both examples and compare with a sort that uses the same two rules on random arrays drawn from a pool that includes both extremes. They also show that reversing a whole chain with `.reversed()` flips the tie-break too, because on `[0, 0]` it yields the indices 1 then 0.

**Complexity.** The time is O(n log n) and the memory is O(n).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class EqualPrioritiesExtremes {
    static int[] order(int[] priority) {
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(a[1], b[1]));
        for (int i = 0; i < priority.length; i++) queue.offer(new int[]{priority[i], i});
        int[] out = new int[priority.length];
        for (int k = 0; k < out.length; k++) out[k] = queue.poll()[1];
        return out;
    }

    static int[] bySorting(int[] priority) {
        ArrayList<Integer> idx = new ArrayList<>();
        for (int i = 0; i < priority.length; i++) idx.add(i);
        idx.sort((x, y) -> priority[x] != priority[y] ? (priority[x] > priority[y] ? -1 : 1) : Integer.compare(x, y));
        int[] out = new int[idx.size()];
        for (int i = 0; i < out.length; i++) out[i] = idx.get(i);
        return out;
    }

    static int[] wholeChainReversed(int[] priority) {
        Comparator<int[]> cmp = Comparator.<int[]>comparingInt(t -> t[0]).thenComparingInt(t -> t[1]).reversed();
        PriorityQueue<int[]> queue = new PriorityQueue<>(cmp);
        for (int i = 0; i < priority.length; i++) queue.offer(new int[]{priority[i], i});
        int[] out = new int[priority.length];
        for (int k = 0; k < out.length; k++) out[k] = queue.poll()[1];
        return out;
    }

    public static void main(String[] args) {
        int min = Integer.MIN_VALUE, max = Integer.MAX_VALUE;
        if (!Arrays.equals(order(new int[]{5, max, 5, min, max}), new int[]{1, 4, 0, 2, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[]{0, 0}), new int[]{0, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(wholeChainReversed(new int[]{0, 0}), new int[]{1, 0})) throw new AssertionError("a reversed chain also reverses the tie-break");
        Random rnd = new Random(1713);
        int[] pool = {min, max, 0, 5, -5};
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] p = new int[n];
            for (int i = 0; i < n; i++) p[i] = pool[rnd.nextInt(pool.length)];
            if (!Arrays.equals(order(p), bySorting(p))) throw new AssertionError("disagrees with the sort on " + Arrays.toString(p));
        }
    }
}
```

#### Solution: [Recognize] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-single-threaded-cpu -->

**Approach.** Sort the task indices by enqueue time, then run a clock. If the queue is empty and the next task is not yet released, jump the clock to its enqueue time. Offer every task whose enqueue time is at most the clock, as a pair of processing time and index ranked by the tuple comparator, then poll one pair, add its processing time to the clock, and record the index. The clock is a `long`, because the sum of times can exceed the `int` range, and the assertions include an input where the clock ends at 4,000,000,000. They also check both examples and compare with a version that scans all unprocessed tasks for the best one at each step.

**Complexity.** The sort and the queue operations give O(n log n) time, and the queue and the sorted indices need O(n) memory.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.Random;

public final class SingleThreadedCpu {
    static long lastClock;

    static int[] order(int[][] tasks) {
        int n = tasks.length;
        Integer[] byRelease = new Integer[n];
        for (int i = 0; i < n; i++) byRelease[i] = i;
        Arrays.sort(byRelease, Comparator.<Integer>comparingInt(i -> tasks[i][0]).thenComparingInt(i -> i));
        PriorityQueue<long[]> ready = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Long.compare(a[0], b[0]) : Long.compare(a[1], b[1]));
        int[] out = new int[n];
        int done = 0, next = 0;
        long clock = 0;
        while (done < n) {
            if (ready.isEmpty() && tasks[byRelease[next]][0] > clock) clock = tasks[byRelease[next]][0];
            while (next < n && tasks[byRelease[next]][0] <= clock) {
                int i = byRelease[next++];
                ready.offer(new long[]{tasks[i][1], i});
            }
            long[] best = ready.poll();
            clock += best[0];
            out[done++] = (int) best[1];
        }
        lastClock = clock;
        return out;
    }

    static int[] slow(int[][] tasks) {
        int n = tasks.length;
        boolean[] used = new boolean[n];
        int[] out = new int[n];
        long clock = 0;
        for (int step = 0; step < n; step++) {
            int best = -1;
            for (int i = 0; i < n; i++) {
                if (used[i] || tasks[i][0] > clock) continue;
                if (best < 0 || tasks[i][1] < tasks[best][1]) best = i;
            }
            if (best < 0) {
                long soonest = Long.MAX_VALUE;
                for (int i = 0; i < n; i++) if (!used[i]) soonest = Math.min(soonest, tasks[i][0]);
                clock = soonest;
                step--;
                continue;
            }
            used[best] = true;
            clock += tasks[best][1];
            out[step] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(order(new int[][]{{2, 3}, {0, 6}, {3, 1}, {3, 1}, {20, 2}}), new int[]{1, 2, 3, 0, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(order(new int[][]{{1, 2}, {1, 2}, {1, 2}}), new int[]{0, 1, 2})) throw new AssertionError("example 2");
        order(new int[][]{{1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}, {1_000_000_000, 1_000_000_000}});
        if (lastClock != 4_000_000_000L) throw new AssertionError("the clock must reach 4e9 and needs a long, got " + lastClock);
        if (lastClock <= Integer.MAX_VALUE) throw new AssertionError("4e9 does not fit in an int");
        Random rnd = new Random(1714);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[][] tasks = new int[n][2];
            for (int i = 0; i < n; i++) { tasks[i][0] = 1 + rnd.nextInt(12); tasks[i][1] = 1 + rnd.nextInt(4); }
            if (!Arrays.equals(order(tasks), slow(tasks))) throw new AssertionError("disagrees with the scan on " + Arrays.deepToString(tasks));
        }
    }
}
```
