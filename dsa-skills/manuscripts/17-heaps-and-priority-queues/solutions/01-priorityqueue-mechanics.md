<!-- solutions-for: 01-priorityqueue-mechanics -->
### PriorityQueue Mechanics

#### Solution: [Build] Repeated Minimum (Author exercise)
<!-- id: hp-repeated-minimum -->

**Approach.** Offer every value, then poll until `isEmpty()`. Because `poll` always removes the root, which is the smallest value under the natural order, the polls come out in nondecreasing order whatever the order of the offers, and equal values are kept as separate items. The assertions check both examples against `Arrays.sort` on random arrays with many duplicates, and they also show the false friend of the lesson: after offering 7, 3, 9, 1, 5, 2 the queue's own iteration order is the array `[1, 3, 2, 7, 5, 9]`, which is a valid heap and is not sorted.

**Complexity.** Sorting through the queue takes O(n log n) time, spent as n offers and n polls of logarithmic cost each, with O(n) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Random;

public final class RepeatedMinimum {
    static int[] drain(int[] values) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        for (int v : values) queue.offer(v);
        int[] out = new int[values.length];
        int i = 0;
        while (!queue.isEmpty()) out[i++] = queue.poll();
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(drain(new int[]{9, 4, 7, 4, 1}), new int[]{1, 4, 4, 7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(drain(new int[]{-3, 8, -3, 0}), new int[]{-3, -3, 0, 8})) throw new AssertionError("example 2");
        if (drain(new int[0]).length != 0) throw new AssertionError("empty input");
        PriorityQueue<Integer> q = new PriorityQueue<>();
        for (int v : new int[]{7, 3, 9, 1, 5, 2}) q.offer(v);
        List<Integer> arrangement = new ArrayList<>(q);
        if (!arrangement.equals(Arrays.asList(1, 3, 2, 7, 5, 9))) throw new AssertionError("array order of the heap was " + arrangement);
        List<Integer> sorted = new ArrayList<>(arrangement);
        java.util.Collections.sort(sorted);
        if (arrangement.equals(sorted)) throw new AssertionError("iteration order must not be sorted here");
        if (q.peek() != 1) throw new AssertionError("the root is still the minimum");
        Random rnd = new Random(1701);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5;
            int[] expected = a.clone();
            Arrays.sort(expected);
            if (!Arrays.equals(drain(a), expected)) throw new AssertionError("disagrees with sort on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Last Stone Weight (LeetCode 1046)
<!-- id: hp-last-stone-weight -->

**Approach.** Use a queue ordered by `Collections.reverseOrder()`, so that the root is the heaviest stone. While two stones remain, poll both, and if they differ offer the difference. The first poll is the heaviest and the second the next heaviest, so the difference is never negative. The answer is the single remaining stone, or 0 for an empty queue. The assertions check both examples, compare with a slow version that sorts a list after every round, and confirm that the default queue would hand out the lightest stone first, which is why the reversed order is needed.

**Complexity.** There are at most n rounds and each does three queue operations, so the time is O(n log n) and the memory is O(n).

```java run
import java.util.ArrayList;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class LastStoneWeight {
    static int lastStone(int[] stones) {
        PriorityQueue<Integer> heaviest = new PriorityQueue<>(Collections.reverseOrder());
        for (int s : stones) heaviest.offer(s);
        while (heaviest.size() >= 2) {
            int a = heaviest.poll();
            int b = heaviest.poll();
            if (a != b) heaviest.offer(a - b);
        }
        return heaviest.isEmpty() ? 0 : heaviest.peek();
    }

    static int slow(int[] stones) {
        ArrayList<Integer> list = new ArrayList<>();
        for (int s : stones) list.add(s);
        while (list.size() >= 2) {
            Collections.sort(list);
            int a = list.remove(list.size() - 1);
            int b = list.remove(list.size() - 1);
            if (a != b) list.add(a - b);
        }
        return list.isEmpty() ? 0 : list.get(0);
    }

    public static void main(String[] args) {
        if (lastStone(new int[]{9, 3, 6, 6, 2}) != 2) throw new AssertionError("example 1");
        if (lastStone(new int[]{5, 5}) != 0) throw new AssertionError("example 2");
        if (lastStone(new int[]{4}) != 4) throw new AssertionError("single stone");
        PriorityQueue<Integer> natural = new PriorityQueue<>();
        for (int v : new int[]{9, 3, 6}) natural.offer(v);
        if (natural.peek() != 3) throw new AssertionError("the default queue is a min-heap");
        PriorityQueue<Integer> reversed = new PriorityQueue<>(Collections.reverseOrder());
        for (int v : new int[]{9, 3, 6}) reversed.offer(v);
        if (reversed.peek() != 9) throw new AssertionError("the reversed queue is a max-heap");
        Random rnd = new Random(1702);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(20);
            if (lastStone(a) != slow(a)) throw new AssertionError("disagrees with the sorting version on " + java.util.Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Empty And Singleton Heap (Author exercise)
<!-- id: hp-empty-and-singleton -->

**Approach.** `peek` and `poll` are the two reads that return `null` on an empty queue, and the code maps that `null` to 0 before it reaches an unboxing assignment. `element` and `remove` throw `NoSuchElementException` in the same situation and are not used by the method. With a single item the root is the whole queue, so a peek and the following poll return the same value and leave size 0. The assertions check both examples, the four empty-queue behaviours directly, the rejection of `null`, the failure to compare a non-comparable element, and a random comparison with a list that scans for the minimum.

**Complexity.** Each operation costs O(log n) or less, so a run of m operations takes O(m log m) time with O(m) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.NoSuchElementException;
import java.util.PriorityQueue;
import java.util.Random;

public final class EmptyAndSingleton {
    static int[] run(int[] ops) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        ArrayList<Integer> out = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) queue.offer(op);
            else if (op == 0) { Integer x = queue.poll(); out.add(x == null ? 0 : x); }
            else { Integer x = queue.peek(); out.add(x == null ? 0 : x); }
        }
        out.add(queue.size());
        int[] result = new int[out.size()];
        for (int i = 0; i < result.length; i++) result[i] = out.get(i);
        return result;
    }

    static int[] slow(int[] ops) {
        ArrayList<Integer> bag = new ArrayList<>();
        ArrayList<Integer> out = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) bag.add(op);
            else {
                int best = -1;
                for (int i = 0; i < bag.size(); i++) if (best < 0 || bag.get(i) < bag.get(best)) best = i;
                out.add(best < 0 ? 0 : bag.get(best));
                if (op == 0 && best >= 0) bag.remove(best);
            }
        }
        out.add(bag.size());
        int[] result = new int[out.size()];
        for (int i = 0; i < result.length; i++) result[i] = out.get(i);
        return result;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[]{0, -1, 5, -1, 0, 0}), new int[]{0, 0, 5, 5, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[]{4, 4, 0, -1}), new int[]{4, 4, 1})) throw new AssertionError("example 2");

        PriorityQueue<Integer> empty = new PriorityQueue<>();
        if (empty.peek() != null) throw new AssertionError("peek on empty returns null");
        if (empty.poll() != null) throw new AssertionError("poll on empty returns null");
        try { empty.element(); throw new AssertionError("element must throw"); } catch (NoSuchElementException expected) { }
        try { empty.remove(); throw new AssertionError("remove must throw"); } catch (NoSuchElementException expected) { }
        PriorityQueue<Integer> one = new PriorityQueue<>();
        one.offer(8);
        if (one.peek() != 8 || one.size() != 1) throw new AssertionError("peek leaves the item");
        if (one.poll() != 8 || !one.isEmpty()) throw new AssertionError("the singleton poll empties the queue");
        try { one.offer(null); throw new AssertionError("null must be rejected"); } catch (NullPointerException expected) { }
        try {
            PriorityQueue<Object> raw = new PriorityQueue<>();
            raw.offer(new Object());
            raw.offer(new Object());
            throw new AssertionError("objects without an order must fail to compare");
        } catch (ClassCastException expected) { }

        Random rnd = new Random(1703);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] ops = new int[n];
            for (int i = 0; i < n; i++) {
                int r = rnd.nextInt(5);
                ops[i] = r == 0 ? -1 : r <= 2 ? 0 : 1 + rnd.nextInt(6);
            }
            if (!Arrays.equals(run(ops), slow(ops))) throw new AssertionError("disagrees with the scanning bag on " + Arrays.toString(ops));
        }
    }
}
```

#### Solution: [Recognize] Kth Largest Element in a Stream (LeetCode 703)
<!-- id: hp-kth-largest-stream -->

**Approach.** Keep a natural-order queue that never holds more than the `k` largest values seen. Its root is the smallest of those `k`, which is exactly the k-th largest overall. For each new value, offer it, and if the size is now `k + 1` poll once, which removes the weakest of the `k + 1` candidates. The answer after the addition is the root. The initial values go through the same step, without a report. Both examples are asserted, and a slower version that re-sorts all values after every addition serves as the oracle on random streams.

**Complexity.** Every value costs O(log k) to process, so the time is O((m + n) log k) for m initial values and n additions, and the queue holds at most k + 1 items.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class KthLargestStream {
    static int[] kthAfterEach(int k, int[] initial, int[] adds) {
        PriorityQueue<Integer> best = new PriorityQueue<>();
        for (int v : initial) {
            best.offer(v);
            if (best.size() > k) best.poll();
        }
        int[] out = new int[adds.length];
        for (int i = 0; i < adds.length; i++) {
            best.offer(adds[i]);
            if (best.size() > k) best.poll();
            out[i] = best.peek();
        }
        return out;
    }

    static int[] slow(int k, int[] initial, int[] adds) {
        ArrayList<Integer> all = new ArrayList<>();
        for (int v : initial) all.add(v);
        int[] out = new int[adds.length];
        for (int i = 0; i < adds.length; i++) {
            all.add(adds[i]);
            ArrayList<Integer> copy = new ArrayList<>(all);
            copy.sort(Collections.reverseOrder());
            out[i] = copy.get(k - 1);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(kthAfterEach(2, new int[]{6, 1, 9}, new int[]{4, 10, 7, 2}), new int[]{6, 9, 9, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(kthAfterEach(1, new int[]{}, new int[]{3, 1, 5}), new int[]{3, 3, 5})) throw new AssertionError("example 2");
        Random rnd = new Random(1704);
        for (int t = 0; t < 4000; t++) {
            int k = 1 + rnd.nextInt(5);
            int m = rnd.nextInt(8);
            int n = 1 + rnd.nextInt(10);
            if (m + 1 < k) m = k - 1;
            int[] initial = new int[m];
            int[] adds = new int[n];
            for (int i = 0; i < m; i++) initial[i] = rnd.nextInt(9) - 4;
            for (int i = 0; i < n; i++) adds[i] = rnd.nextInt(9) - 4;
            if (!Arrays.equals(kthAfterEach(k, initial, adds), slow(k, initial, adds))) throw new AssertionError("disagrees with the sorting version, k=" + k + " " + Arrays.toString(initial) + " " + Arrays.toString(adds));
        }
    }
}
```
