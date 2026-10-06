<!-- solutions-for: 01-priorityqueue-mechanics -->
### Solutions For Taking The Smallest Item

#### Solution: [Build] Repeated Minimum (Author exercise)
<!-- id: hp-repeated-minimum -->

**Approach.**
The method adds every value to a `PriorityQueue<Integer>` and then polls the queue once per value. Each poll returns the smallest value still stored, because heap order keeps that value at the root. The sequence of returned values therefore never decreases, and duplicates leave the queue one copy per poll. The input array stays untouched, because the method writes into a new array.

The invariant is that every value returned so far is less than or equal to every value still in the queue.

**Complexity.**
- **Time** is O(n log n), because each of the `n` offers and `n` polls moves an item through at most log2(n) levels.
- **Space** is O(n), because the queue holds all values at once.

```java run
import java.util.*;

public final class RepeatedMinimum {
    /**
     * Returns the values in nondecreasing order using offer and poll only.
     * Time: O(n log n). Space: O(n).
     * Invariant: each returned value is at most every value still queued.
     */
    static int[] sorted(int[] values) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        // Each offer sifts up at most log2(n) levels.
        for (int v : values) queue.offer(v);
        int[] out = new int[values.length];
        // Each poll sifts down at most log2(n) levels and returns the current root.
        for (int i = 0; i < out.length; i++) out[i] = queue.poll();
        return out;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise.
        if (!Arrays.equals(sorted(new int[] {7, 2, 9, 2}), new int[] {2, 2, 7, 9})) throw new AssertionError("ex1");
        if (sorted(new int[0]).length != 0) throw new AssertionError("ex2");
        // The input array must keep its order.
        int[] in = {3, 1, 2};
        sorted(in);
        if (!Arrays.equals(in, new int[] {3, 1, 2})) throw new AssertionError("mutation");
        // Iterating a queue does not give sorted order: the array layout after 5,3,8,1,4 is [1,3,8,5,4].
        PriorityQueue<Integer> q = new PriorityQueue<>();
        for (int v : new int[] {5, 3, 8, 1, 4}) q.offer(v);
        if (!q.toString().equals("[1, 3, 8, 5, 4]")) throw new AssertionError("layout");
        // Random arrays must match Arrays.sort, including extreme values.
        Random rnd = new Random(1701);
        for (int t = 0; t < 300; t++) {
            int[] a = new int[rnd.nextInt(30)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(12) - 6;
            if (t == 0 && a.length > 1) { a[0] = Integer.MIN_VALUE; a[1] = Integer.MAX_VALUE; }
            int[] expect = a.clone();
            Arrays.sort(expect);
            if (!Arrays.equals(sorted(a), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Last Stone Weight (LeetCode 1046)
<!-- id: hp-last-stone -->

**Approach.**
The queue uses `Collections.reverseOrder()`, so `poll` returns the heaviest stone. Each round polls two stones `y >= x`. The round inserts `y - x` only when that difference is positive, because equal stones destroy each other. Every round removes two items and adds at most one, so the queue shrinks by at least one item per round and the loop ends. The answer is the single stone left, or 0 when the queue is empty.

The invariant is that the queue always holds exactly the stones that remain after the completed rounds.

**Complexity.**
- **Time** is O(n log n), because at most n - 1 rounds run and each round does two polls and at most one offer.
- **Space** is O(n), because the queue stores the stones.

```java run
import java.util.*;

public final class LastStone {
    /**
     * Returns the weight of the last stone, or 0 when none remains.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds exactly the stones left after the finished rounds.
     */
    static int lastStone(int[] stones) {
        PriorityQueue<Integer> queue = new PriorityQueue<>(Collections.reverseOrder());
        for (int s : stones) queue.offer(s);
        // Two stones are needed for a round; each round removes two and adds at most one.
        while (queue.size() >= 2) {
            int y = queue.poll();
            int x = queue.poll();
            // Equal stones vanish; otherwise the remainder returns to the queue.
            if (y != x) queue.offer(y - x);
        }
        return queue.isEmpty() ? 0 : queue.peek();
    }

    /** Oracle: sort a list and take the two largest by scan. */
    static int oracle(int[] stones) {
        List<Integer> list = new ArrayList<>();
        for (int s : stones) list.add(s);
        while (list.size() >= 2) {
            Collections.sort(list);
            int y = list.remove(list.size() - 1);
            int x = list.remove(list.size() - 1);
            if (y != x) list.add(y - x);
        }
        return list.isEmpty() ? 0 : list.get(0);
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (lastStone(new int[] {9, 4, 6, 2}) != 1) throw new AssertionError("ex1");
        if (lastStone(new int[] {5, 5}) != 0) throw new AssertionError("ex2");
        // One stone stays as it is.
        if (lastStone(new int[] {7}) != 7) throw new AssertionError("single");
        // Random inputs must match the sorting oracle.
        Random rnd = new Random(1702);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(20);
            if (lastStone(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And Singleton Queue (Author exercise)
<!-- id: hp-empty-singleton -->

**Approach.**
The loop runs while two conditions hold. The count of finished polls is below `m`, and the queue is not empty. The second condition keeps `poll` legal, although `poll` returns `null` on an empty queue and would not throw. The method then returns `peek`, which reads the root without removing it and returns `null` on an empty queue. The return type is `Integer`, so the answer `null` stays distinct from every `int` value.

The invariant is that the queue holds the original values minus the smallest `done` values, where `done` counts completed polls.

**Complexity.**
- **Time** is O(n + m' log n), where `m'` is the smaller of `m` and `n`, because building costs n offers of O(log n) each and the polls cost O(log n) each. The bound simplifies to O(n log n).
- **Space** is O(n), because the queue holds all values at first.

```java run
import java.util.*;

public final class EmptySingleton {
    /**
     * Removes up to m smallest values and returns the smallest remaining value, or null.
     * Time: O(n log n). Space: O(n).
     * Invariant: the queue holds all values except the done smallest ones.
     */
    static Integer afterRemoving(int[] values, int m) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        for (int v : values) queue.offer(v);
        // The emptiness test makes a count above the size harmless.
        for (int done = 0; done < m && !queue.isEmpty(); done++) queue.poll();
        // peek returns null for an empty queue and leaves a non-empty queue unchanged.
        return queue.peek();
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (afterRemoving(new int[] {4, 1, 3}, 2) != 4) throw new AssertionError("ex1");
        if (afterRemoving(new int[] {4}, 1) != null) throw new AssertionError("ex2");
        // One item with no removal stays visible, and a huge count empties the queue.
        if (afterRemoving(new int[] {4}, 0) != 4) throw new AssertionError("m zero");
        if (afterRemoving(new int[] {4, 5}, 1_000_000) != null) throw new AssertionError("m large");
        // Java behaviour claimed in the lesson: peek and poll return null, element and remove throw.
        PriorityQueue<Integer> empty = new PriorityQueue<>();
        if (empty.peek() != null || empty.poll() != null) throw new AssertionError("null returns");
        try { empty.element(); throw new AssertionError("element must throw"); } catch (NoSuchElementException expected) { }
        try { empty.remove(); throw new AssertionError("remove must throw"); } catch (NoSuchElementException expected) { }
        // An int that equals the usual sentinel value is still a valid answer.
        if (afterRemoving(new int[] {-1, 0}, 1) != 0 || afterRemoving(new int[] {-1}, 0) != -1) throw new AssertionError("minus one");
        // Random inputs must match a sort-and-index oracle.
        Random rnd = new Random(1703);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(8)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(10) - 5;
            int m = rnd.nextInt(12);
            int[] s = a.clone();
            Arrays.sort(s);
            Integer expect = m < s.length ? s[m] : null;
            Integer got = afterRemoving(a, m);
            if (!Objects.equals(expect, got)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Kth Largest Element in a Stream (LeetCode 703)
<!-- id: hp-kth-largest-stream -->

**Approach.**
A value that is not among the `k` largest seen so far never becomes the kth largest again, because later values only push it further down. The class therefore keeps a min-oriented queue of at most `k` values. The root of that queue is the smallest of the `k` largest values, and that value is the kth largest overall. `add` offers the new value, then polls the root when the size reaches `k + 1`. The constructor calls `add` for each initial value, so one code path serves both.

The invariant is that the queue holds the `min(k, count)` largest values seen so far.

**Complexity.**
- **Time** is O(log k) per `add`, because the queue never holds more than `k + 1` items.
- **Space** is O(k), because the queue stores at most `k` values after each call.

```java run
import java.util.*;

public final class KthLargestStream {
    static final class KthLargest {
        private final int k;
        private final PriorityQueue<Integer> queue = new PriorityQueue<>();

        KthLargest(int k, int[] nums) {
            this.k = k;
            // The same path as add keeps the invariant from the first value.
            for (int v : nums) add(v);
        }

        /**
         * Inserts val and returns the kth largest value seen so far.
         * Time: O(log k). Space: O(k).
         * Invariant: the queue holds the min(k, count) largest values.
         */
        int add(int val) {
            queue.offer(val);
            // A size of k + 1 means the smallest kept value is no longer among the k largest.
            if (queue.size() > k) queue.poll();
            return queue.peek();
        }
    }

    public static void main(String[] args) {
        // Example 1: k = 2.
        KthLargest a = new KthLargest(2, new int[] {6, 1, 9});
        if (a.add(4) != 6 || a.add(10) != 9 || a.add(2) != 9) throw new AssertionError("ex1");
        // Example 2: k = 1 starting empty.
        KthLargest b = new KthLargest(1, new int[0]);
        if (b.add(3) != 3 || b.add(-2) != 3) throw new AssertionError("ex2");
        // Random streams must match sorting every prefix.
        Random rnd = new Random(1704);
        for (int t = 0; t < 300; t++) {
            int k = 1 + rnd.nextInt(5);
            int init = rnd.nextInt(6);
            List<Integer> seen = new ArrayList<>();
            int[] nums = new int[init];
            for (int i = 0; i < init; i++) { nums[i] = rnd.nextInt(15) - 7; seen.add(nums[i]); }
            KthLargest kl = new KthLargest(k, nums);
            for (int step = 0; step < 15; step++) {
                int v = rnd.nextInt(15) - 7;
                seen.add(v);
                int got = kl.add(v);
                // The exercise guarantees at least k values after each add, so shorter prefixes are not compared.
                if (seen.size() < k) continue;
                List<Integer> sorted = new ArrayList<>(seen);
                sorted.sort(Collections.reverseOrder());
                if (got != sorted.get(k - 1)) throw new AssertionError("random " + t);
            }
        }
    }
}
```
