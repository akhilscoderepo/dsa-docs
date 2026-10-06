<!-- solutions-for: 06-lazy-deletion -->
### Solutions For Deleting Lazily

#### Solution: [Build] Versioned Priorities (Author exercise)
<!-- id: hp-versioned-priorities -->

**Approach.**
Each `set` call increments a global version counter, stores the new version in a map under the task id, and inserts a `{id, priority, version}` entry. The older entries of that task stay in the queue. The `poll` method first cleans the root. A root is live only when the map holds its version for its id. A stale root is polled and dropped, and the loop repeats. The first live root is polled, and the map entry of its id is removed, so every older entry of that task becomes stale. A global counter prevents a later `set` of the same id from reusing a version that an old entry still carries.

The invariant is that, after the cleaning loop, the root is live or the queue is empty.

**Complexity.**
- **Time** is O(log n) amortized per call, because each entry is inserted once and discarded or returned at most once.
- **Space** is O(m) for `m` calls, because stale entries stay in the queue until they reach the root.

```java run
import java.util.*;

public final class VersionedBoard {
    static final class TaskBoard {
        private final PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
            a[1] != b[1] ? Integer.compare(a[1], b[1]) : Integer.compare(a[0], b[0]));
        private final Map<Integer, Integer> latest = new HashMap<>();
        private int version = 0;

        /**
         * Inserts or replaces the priority of a task.
         * Time: O(log n). Space: O(1) extra per call.
         */
        void set(int id, int priority) {
            // A global counter never reuses a version, even after a task leaves.
            version++;
            latest.put(id, version);
            queue.offer(new int[] {id, priority, version});
        }

        /**
         * Removes and returns the id with the smallest priority, or -1.
         * Time: O(log n) amortized. Space: O(1).
         * Invariant: after cleaning, the root is live.
         */
        int poll() {
            // A stale root has no matching version in the map.
            while (!queue.isEmpty()) {
                int[] top = queue.peek();
                Integer v = latest.get(top[0]);
                if (v != null && v == top[2]) break;
                queue.poll();
            }
            if (queue.isEmpty()) return -1;
            int id = queue.poll()[0];
            // Removing the map entry makes every older entry of this id stale.
            latest.remove(id);
            return id;
        }
    }

    /** Oracle: a map of id to priority scanned in full at every poll. */
    static final class Oracle {
        private final Map<Integer, Integer> prio = new HashMap<>();
        void set(int id, int p) { prio.put(id, p); }
        int poll() {
            int best = -1;
            for (Map.Entry<Integer, Integer> e : prio.entrySet()) {
                if (best == -1 || e.getValue() < prio.get(best) || (e.getValue().equals(prio.get(best)) && e.getKey() < best)) best = e.getKey();
            }
            if (best != -1) prio.remove(best);
            return best;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        TaskBoard b = new TaskBoard();
        b.set(1, 5); b.set(2, 3); b.set(1, 1);
        if (b.poll() != 1 || b.poll() != 2 || b.poll() != -1) throw new AssertionError("ex1");
        // Example 2 from the exercise.
        TaskBoard c = new TaskBoard();
        c.set(7, 2); c.set(7, 9); c.set(8, 5);
        if (c.poll() != 8 || c.poll() != 7) throw new AssertionError("ex2");
        // A task that was polled and then set again must not revive its old entry.
        TaskBoard d = new TaskBoard();
        d.set(1, 1); d.poll(); d.set(1, 9); d.set(2, 5);
        if (d.poll() != 2 || d.poll() != 1 || d.poll() != -1) throw new AssertionError("reinsert");
        // Random operation streams must match the scan oracle.
        Random rnd = new Random(1761);
        for (int t = 0; t < 400; t++) {
            TaskBoard x = new TaskBoard();
            Oracle o = new Oracle();
            for (int step = 0; step < 40; step++) {
                if (rnd.nextInt(3) > 0) { int id = rnd.nextInt(5), p = rnd.nextInt(6); x.set(id, p); o.set(id, p); }
                else if (x.poll() != o.poll()) throw new AssertionError("random " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Delayed Removal Counts (Author exercise)
<!-- id: hp-delayed-removal-counts -->

**Approach.**
The `remove` method does not touch the queue. It adds one to the pending count of the value. The `min` method cleans the root first. While the root value has a positive pending count, the method polls the root and lowers the count by one. This discards exactly as many copies as were deleted, even when many copies of one value sit at the root together. The method then returns the root, which is the smallest live value. A separate counter tracks the live size, because the queue size also counts the pending copies.

The invariant is that, for each value, the number of copies in the queue minus its pending count equals the number of live copies.

**Complexity.**
- **Time** is O(log n) amortized per call, because every copy is inserted once and discarded at most once.
- **Space** is O(n), because pending copies stay in the queue until they reach the root.

```java run
import java.util.*;

public final class DelayedRemovalCounts {
    static final class ValueBag {
        private final PriorityQueue<Integer> queue = new PriorityQueue<>();
        private final Map<Integer, Integer> pending = new HashMap<>();
        private int live = 0;

        void add(int v) { queue.offer(v); live++; }

        // Only the count changes at remove time; the queue is untouched.
        void remove(int v) { pending.merge(v, 1, Integer::sum); live--; }

        /**
         * Returns the smallest live value, or null.
         * Time: O(log n) amortized. Space: O(1).
         * Invariant: copies in the queue minus pending count equals live copies for each value.
         */
        Integer min() {
            while (!queue.isEmpty()) {
                Integer c = pending.get(queue.peek());
                // No pending deletion means the root is live.
                if (c == null) break;
                int top = queue.poll();
                // One discarded copy settles one pending deletion.
                if (c == 1) pending.remove(top); else pending.put(top, c - 1);
            }
            return queue.peek();
        }

        int size() { return live; }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        ValueBag b = new ValueBag();
        b.add(4); b.add(2); b.add(4); b.remove(2);
        if (b.min() != 4) throw new AssertionError("ex1a");
        b.remove(4);
        if (b.min() != 4) throw new AssertionError("ex1b");
        b.remove(4);
        if (b.min() != null) throw new AssertionError("ex1c");
        // Example 2 from the exercise.
        ValueBag c = new ValueBag();
        c.add(3); c.add(1); c.remove(1);
        if (c.min() != 3) throw new AssertionError("ex2");
        // The live size stays at one value, and a pending copy never counts as live.
        if (c.size() != 1) throw new AssertionError("live size");
        // Documented hazard: removing an absent value corrupts the count and deletes a later copy.
        ValueBag bad = new ValueBag();
        bad.remove(5);
        bad.add(5);
        if (bad.min() != null) throw new AssertionError("absent removal eats a later copy");
        // Random streams must match a multiset kept as a list.
        Random rnd = new Random(1762);
        for (int t = 0; t < 400; t++) {
            ValueBag x = new ValueBag();
            List<Integer> model = new ArrayList<>();
            for (int step = 0; step < 40; step++) {
                int op = rnd.nextInt(3);
                if (op == 0) { int v = rnd.nextInt(5); x.add(v); model.add(v); }
                else if (op == 1 && !model.isEmpty()) { int v = model.get(rnd.nextInt(model.size())); x.remove(v); model.remove(Integer.valueOf(v)); }
                else {
                    Integer expect = model.isEmpty() ? null : Collections.min(model);
                    if (!Objects.equals(x.min(), expect)) throw new AssertionError("random " + t);
                }
                if (x.size() != model.size()) throw new AssertionError("size " + t);
            }
        }
    }
}
```

#### Solution: [Boundary] Several Stale Roots (Author exercise)
<!-- id: hp-several-stale-roots -->

**Approach.**
The method adds every value to a queue and records every removal as a pending count. The cleaning step is a `while` loop and not an `if`, because several entries at the root can be stale one after another. With `adds = [5,5,5,5,9]` and three removals of 5, the loop discards three copies of 5 in a row and stops at the fourth. With four removals of 5, the loop discards all four and stops at 9. A single `if` would stop after one discard and return a stale value.

The invariant is that, when the loop ends, the root has no pending deletion or the queue is empty.

**Complexity.**
- **Time** is O((n + r) log n), for `n` adds and `r` removals, because each added value is inserted once and discarded at most once.
- **Space** is O(n), because the queue and the count map hold at most the added values.

```java run
import java.util.*;

public final class SeveralStaleRoots {
    /**
     * Returns the smallest value that remains after all removals, or null.
     * Time: O((n + r) log n). Space: O(n).
     * Invariant: after the loop, the root has no pending deletion.
     */
    static Integer smallestAfter(int[] adds, int[] removes) {
        PriorityQueue<Integer> queue = new PriorityQueue<>();
        for (int v : adds) queue.offer(v);
        Map<Integer, Integer> pending = new HashMap<>();
        // Removals only record counts; the queue stays as it is.
        for (int v : removes) pending.merge(v, 1, Integer::sum);
        // A loop is needed because many stale entries can sit at the root in a row.
        while (!queue.isEmpty()) {
            Integer c = pending.get(queue.peek());
            if (c == null) break;
            int top = queue.poll();
            if (c == 1) pending.remove(top); else pending.put(top, c - 1);
        }
        return queue.peek();
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (smallestAfter(new int[] {5, 5, 5, 5, 9}, new int[] {5, 5, 5}) != 5) throw new AssertionError("ex1");
        if (smallestAfter(new int[] {2, 2, 2, 9}, new int[] {2, 2, 2}) != 9) throw new AssertionError("ex2");
        // Removing every copy empties the bag.
        if (smallestAfter(new int[] {1, 1}, new int[] {1, 1}) != null) throw new AssertionError("empty");
        if (smallestAfter(new int[0], new int[0]) != null) throw new AssertionError("no input");
        // Random valid inputs must match a multiset model.
        Random rnd = new Random(1763);
        for (int t = 0; t < 500; t++) {
            int[] adds = new int[rnd.nextInt(15)];
            for (int i = 0; i < adds.length; i++) adds[i] = rnd.nextInt(4);
            List<Integer> model = new ArrayList<>();
            for (int v : adds) model.add(v);
            int r = rnd.nextInt(adds.length + 1);
            int[] removes = new int[r];
            for (int i = 0; i < r; i++) {
                int v = model.get(rnd.nextInt(model.size()));
                removes[i] = v;
                model.remove(Integer.valueOf(v));
            }
            Integer expect = model.isEmpty() ? null : Collections.min(model);
            if (!Objects.equals(smallestAfter(adds, removes), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-sliding-window-median -->

**Approach.**
The queue stores `{value, index}` entries and puts the largest value at the root. For each index `i`, the method inserts its entry. The window that ends at `i` starts at `i - k + 1`. While the root index is below that start, the entry left the window, so the method polls it. The loop leaves a root that lies inside the window. No entry inside the window is larger than that root, so its value is the window maximum. Entries that expired and sit below the root cost nothing until they surface. The median version of this problem needs the two halves of the next lesson, and this exercise keeps only the delayed expiry.

The invariant is that, after the cleaning loop, the root is the largest value among the entries inside the window.

**Complexity.**
- **Time** is O(n log n), because each entry is inserted once and discarded at most once.
- **Space** is O(n), because expired entries can stay in the queue until they reach the root.

```java run
import java.util.*;

public final class SlidingWindowMax {
    /**
     * Returns the maximum of each window of k consecutive values.
     * Time: O(n log n). Space: O(n).
     * Invariant: after cleaning, the root is the largest value inside the window.
     */
    static int[] windowMax(int[] nums, int k) {
        // Largest value first; a larger index wins ties so that the freshest copy stays.
        PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) ->
            a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(b[1], a[1]));
        int[] out = new int[nums.length - k + 1];
        for (int i = 0; i < nums.length; i++) {
            queue.offer(new int[] {nums[i], i});
            // The window ending at i starts at i - k + 1; a smaller index has expired.
            while (queue.peek()[1] <= i - k) queue.poll();
            if (i >= k - 1) out[i - k + 1] = queue.peek()[0];
        }
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(windowMax(new int[] {4, 2, 12, 3, 8, 1}, 3), new int[] {12, 12, 12, 8})) throw new AssertionError("ex1");
        if (!Arrays.equals(windowMax(new int[] {5}, 1), new int[] {5})) throw new AssertionError("ex2");
        // Equal values and a window of one return the input itself.
        if (!Arrays.equals(windowMax(new int[] {3, 3, 3}, 2), new int[] {3, 3})) throw new AssertionError("equal");
        if (!Arrays.equals(windowMax(new int[] {2, 7, 1}, 1), new int[] {2, 7, 1})) throw new AssertionError("k one");
        // Random arrays must match a direct scan of every window.
        Random rnd = new Random(1764);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[1 + rnd.nextInt(20)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(9) - 4;
            int k = 1 + rnd.nextInt(a.length);
            int[] got = windowMax(a, k);
            for (int s = 0; s + k <= a.length; s++) {
                int best = Integer.MIN_VALUE;
                for (int j = s; j < s + k; j++) best = Math.max(best, a[j]);
                if (got[s] != best) throw new AssertionError("random " + t);
            }
        }
    }
}
```
