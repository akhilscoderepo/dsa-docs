<!-- solutions-for: 02-heap-orientation -->
### Solutions For Choosing The Order

#### Solution: [Build] Safe Max-Heap (Author exercise)
<!-- id: hp-safe-max-heap -->

**Approach.**
The queue receives the comparator `(a, b) -> Integer.compare(b, a)`. The comparator swaps its arguments, so the larger value counts as smaller and sits at the root. The code stores every value unchanged, which removes the overflow that negation causes at `Integer.MIN_VALUE`. Polling `n` times returns the values from largest to smallest. Equal values leave in any order, which is harmless because equal `int` values look identical.

The invariant is that the root is the largest value among those still stored.

**Complexity.**
- **Time** is O(n log n), because n offers and n polls each cost O(log n) and every comparison takes constant time.
- **Space** is O(n), because the queue holds every value before the first poll.

```java run
import java.util.*;

public final class SafeMaxHeap {
    /**
     * Returns the values in nonincreasing order using a swapped-argument comparator.
     * Time: O(n log n). Space: O(n).
     * Invariant: the root is the largest stored value.
     */
    static int[] nonincreasing(int[] values) {
        // Swapping the arguments reverses the direction without touching the stored values.
        PriorityQueue<Integer> queue = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
        for (int v : values) queue.offer(v);
        int[] out = new int[values.length];
        // Each poll returns the largest value that remains.
        for (int i = 0; i < out.length; i++) out[i] = queue.poll();
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise, including both extreme int values.
        if (!Arrays.equals(nonincreasing(new int[] {4, -9, 4, 0}), new int[] {4, 4, 0, -9})) throw new AssertionError("ex1");
        int[] ext = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0};
        if (!Arrays.equals(nonincreasing(ext), new int[] {Integer.MAX_VALUE, 0, Integer.MIN_VALUE})) throw new AssertionError("ex2");
        // Claims from the lesson: negation wraps at the minimum, and subtraction wraps for a large gap.
        if (-Integer.MIN_VALUE != Integer.MIN_VALUE) throw new AssertionError("negation wraps");
        if (Integer.MAX_VALUE - (-1) >= 0) throw new AssertionError("subtraction wraps");
        if (Integer.compare(Integer.MAX_VALUE, -1) != 1) throw new AssertionError("compare is exact");
        // The negation plan puts MIN_VALUE first, which is the failure the lesson describes.
        PriorityQueue<Integer> negated = new PriorityQueue<>();
        negated.offer(-Integer.MIN_VALUE);
        negated.offer(-5);
        if (-negated.poll() != Integer.MIN_VALUE) throw new AssertionError("negation puts the minimum first");
        // Random arrays with extremes must match a descending sort.
        Random rnd = new Random(1711);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, -1, 0, 1, 7};
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(20)];
            for (int i = 0; i < a.length; i++) a[i] = pool[rnd.nextInt(pool.length)];
            int[] expect = a.clone();
            Arrays.sort(expect);
            for (int i = 0; i < expect.length / 2; i++) { int x = expect[i]; expect[i] = expect[expect.length - 1 - i]; expect[expect.length - 1 - i] = x; }
            if (!Arrays.equals(nonincreasing(a), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Pair Priority (Author exercise)
<!-- id: hp-pair-priority -->

**Approach.**
The queue stores one `int[]` pair of duration and index for each task. The comparator compares durations first with `Integer.compare`. Only when the durations are equal does it compare indexes. Indexes are unique, so the comparator never returns zero for two different tasks, and the removal order is fully determined by the input. Polling `n` times and recording the index of each pair gives the answer.

The invariant is that the root is the pair with the smallest duration, and the smallest index among those with that duration.

**Complexity.**
- **Time** is O(n log n), because each of the n offers and n polls costs O(log n).
- **Space** is O(n), because the queue stores one pair per task.

```java run
import java.util.*;

public final class PairPriority {
    /**
     * Returns task indexes in removal order: smaller duration first, then smaller index.
     * Time: O(n log n). Space: O(n).
     * Invariant: the root is the smallest (duration, index) pair still stored.
     */
    static int[] removalOrder(int[] durations) {
        PriorityQueue<int[]> queue = new PriorityQueue<>((p, q) -> {
            // The first field decides; Integer.compare cannot overflow.
            int byDuration = Integer.compare(p[0], q[0]);
            // A tie falls to the index, which is unique, so the order is total.
            return byDuration != 0 ? byDuration : Integer.compare(p[1], q[1]);
        });
        for (int i = 0; i < durations.length; i++) queue.offer(new int[] {durations[i], i});
        int[] order = new int[durations.length];
        // Each poll returns the index of the pair at the root.
        for (int k = 0; k < order.length; k++) order[k] = queue.poll()[1];
        return order;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(removalOrder(new int[] {3, 1, 3, 1}), new int[] {1, 3, 0, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(removalOrder(new int[] {5, 5, 5}), new int[] {0, 1, 2})) throw new AssertionError("ex2");
        if (removalOrder(new int[0]).length != 0) throw new AssertionError("empty");
        // Random inputs with many ties must match a sort of index objects by the same rule.
        Random rnd = new Random(1712);
        for (int t = 0; t < 300; t++) {
            int[] d = new int[rnd.nextInt(25)];
            for (int i = 0; i < d.length; i++) d[i] = 1 + rnd.nextInt(5);
            Integer[] idx = new Integer[d.length];
            for (int i = 0; i < idx.length; i++) idx[i] = i;
            Arrays.sort(idx, (x, y) -> d[x] != d[y] ? Integer.compare(d[x], d[y]) : Integer.compare(x, y));
            int[] got = removalOrder(d);
            for (int i = 0; i < got.length; i++) if (got[i] != idx[i]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Equal Priorities And Extreme Integers (Author exercise)
<!-- id: hp-equal-extreme -->

**Approach.**
The comparator compares priorities with the arguments swapped, so the larger priority leaves first, and it breaks ties by the smaller index. Both comparisons use `Integer.compare`, so no difference can wrap around, even for the pair `Integer.MAX_VALUE` and `Integer.MIN_VALUE`. The tie-break on the unique index makes the order identical across runs. The code also shows the mutable-key hazard from the lesson. A key changed after `offer` does not move the item, so the root can be wrong.

The invariant is that the root has the largest priority, and the smallest index among equal priorities.

**Complexity.**
- **Time** is O(n log n), because each of the n offers and n polls costs O(log n).
- **Space** is O(n), because the queue stores one entry per job.

```java run
import java.util.*;

public final class EqualExtreme {
    /**
     * Returns job indexes: larger priority first, then smaller index.
     * Time: O(n log n). Space: O(n).
     * Invariant: the root is the best remaining (priority, index) pair under the rule.
     */
    static int[] removalOrder(int[] priorities) {
        PriorityQueue<int[]> queue = new PriorityQueue<>((p, q) -> {
            // Swapped arguments put the larger priority first.
            int byPriority = Integer.compare(q[0], p[0]);
            // Equal priorities fall to the smaller index.
            return byPriority != 0 ? byPriority : Integer.compare(p[1], q[1]);
        });
        for (int i = 0; i < priorities.length; i++) queue.offer(new int[] {priorities[i], i});
        int[] order = new int[priorities.length];
        for (int k = 0; k < order.length; k++) order[k] = queue.poll()[1];
        return order;
    }

    public static void main(String[] args) {
        int lo = Integer.MIN_VALUE, hi = Integer.MAX_VALUE;
        // Examples from the exercise.
        if (!Arrays.equals(removalOrder(new int[] {lo, hi, lo, 0}), new int[] {1, 3, 0, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(removalOrder(new int[] {7, 7, 7}), new int[] {0, 1, 2})) throw new AssertionError("ex2");
        // A subtraction comparator gives the wrong sign for this pair, so the lesson avoids it.
        if (lo - hi <= 0) throw new AssertionError("MIN - MAX wraps to a positive number");
        // Mutable-key hazard: changing a key after offer does not move the item.
        int[] a = {5}, b = {3};
        PriorityQueue<int[]> byFirst = new PriorityQueue<>((p, q) -> Integer.compare(p[0], q[0]));
        byFirst.offer(a);
        byFirst.offer(b);
        a[0] = 1;
        if (byFirst.peek() != b) throw new AssertionError("the queue does not re-sift after a key changes");
        // Random inputs with extremes and ties must match a sort by the same rule.
        Random rnd = new Random(1713);
        int[] pool = {lo, hi, 0, -1, 1};
        for (int t = 0; t < 300; t++) {
            int[] p = new int[rnd.nextInt(20)];
            for (int i = 0; i < p.length; i++) p[i] = pool[rnd.nextInt(pool.length)];
            Integer[] idx = new Integer[p.length];
            for (int i = 0; i < idx.length; i++) idx[i] = i;
            Arrays.sort(idx, (x, y) -> p[x] != p[y] ? Integer.compare(p[y], p[x]) : Integer.compare(x, y));
            int[] got = removalOrder(p);
            for (int i = 0; i < got.length; i++) if (got[i] != idx[i]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Single-Threaded CPU (LeetCode 1834)
<!-- id: hp-single-threaded-cpu -->

**Approach.**
Every task is available at time 0, so the clock never changes which tasks are eligible. The next task is always the one with the smallest processing time and, for equal times, the smallest index. That is the same tuple rule as the Vary exercise, so the answer is the removal order of one queue ordered by the pair `(processing, index)`. The clock starts to matter when release times differ, and a later lesson of this chapter covers that case.

The invariant is that the queue holds exactly the tasks that have not run yet.

**Complexity.**
- **Time** is O(n log n), because each of the n offers and n polls costs O(log n).
- **Space** is O(n), because the queue stores every task before the first poll.

```java run
import java.util.*;

public final class SingleThreadedCpu {
    /**
     * Returns the execution order when all tasks are released at time 0.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds exactly the tasks that have not run.
     */
    static int[] executionOrder(int[] processing) {
        // The tuple (processing, index) decides which task runs next.
        PriorityQueue<long[]> queue = new PriorityQueue<>(
            Comparator.<long[]>comparingLong(t -> t[0]).thenComparingLong(t -> t[1]));
        for (int i = 0; i < processing.length; i++) queue.offer(new long[] {processing[i], i});
        int[] order = new int[processing.length];
        // Each poll starts the next task; the clock needs no tracking because all are released.
        for (int k = 0; k < order.length; k++) order[k] = (int) queue.poll()[1];
        return order;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(executionOrder(new int[] {4, 2, 4, 1}), new int[] {3, 1, 0, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(executionOrder(new int[] {6}), new int[] {0})) throw new AssertionError("ex2");
        if (executionOrder(new int[0]).length != 0) throw new AssertionError("empty");
        // Random inputs must match a stable sort of indexes by processing time.
        Random rnd = new Random(1714);
        for (int t = 0; t < 300; t++) {
            int[] p = new int[rnd.nextInt(25)];
            for (int i = 0; i < p.length; i++) p[i] = 1 + rnd.nextInt(6);
            Integer[] idx = new Integer[p.length];
            for (int i = 0; i < idx.length; i++) idx[i] = i;
            // Arrays.sort on objects is stable, so equal times keep index order.
            Arrays.sort(idx, (x, y) -> Integer.compare(p[x], p[y]));
            int[] got = executionOrder(p);
            for (int i = 0; i < got.length; i++) if (got[i] != idx[i]) throw new AssertionError("random " + t);
        }
    }
}
```
