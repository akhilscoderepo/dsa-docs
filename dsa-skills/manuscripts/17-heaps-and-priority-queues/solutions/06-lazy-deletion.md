<!-- solutions-for: 06-lazy-deletion -->
### Lazy Deletion

#### Solution: [Build] Versioned Priorities (Author exercise)
<!-- id: hp-versioned-priorities -->

**Approach.** Keep a map `current` from id to its live version and a map `counter` that hands out new version numbers per id. A set operation increments the id's counter, records it in `current`, and offers `{priority, id, version}` without looking for the old entry. A pop first cleans the root: while the root's version differs from `current.get(id)`, which also covers an id that is absent because it was popped, discard it. Then it polls the live root, removes the id from `current`, and records the id. The harness asserts both examples, and a scan over a plain map of id to priority is the oracle on random operation streams. It also shows why `remove(Object)` is no substitute: on array entries it compares by identity, so an equal-looking copy is not found, while the very same array object is found.

**Complexity.** Each operation inserts at most one entry and each entry leaves once, so the total time is O(m log m) for m operations, with O(m) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class VersionedPriorities {
    static int[] run(int[][] ops) {
        PriorityQueue<int[]> heap = new PriorityQueue<>((x, y) -> {
            if (x[0] != y[0]) return Integer.compare(x[0], y[0]);
            return Integer.compare(x[1], y[1]);
        });
        HashMap<Integer, Integer> current = new HashMap<>();
        HashMap<Integer, Integer> counter = new HashMap<>();
        ArrayList<Integer> out = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) {
                int version = counter.merge(op[1], 1, Integer::sum);
                current.put(op[1], version);
                heap.offer(new int[]{op[2], op[1], version});
            } else {
                while (!heap.isEmpty()) {
                    int[] top = heap.peek();
                    Integer live = current.get(top[1]);
                    if (live != null && live == top[2]) break;
                    heap.poll();
                }
                if (heap.isEmpty()) out.add(-1);
                else {
                    int[] top = heap.poll();
                    current.remove(top[1]);
                    out.add(top[1]);
                }
            }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    static int[] scan(int[][] ops) {
        HashMap<Integer, Integer> priority = new HashMap<>();
        ArrayList<Integer> out = new ArrayList<>();
        for (int[] op : ops) {
            if (op[0] == 0) priority.put(op[1], op[2]);
            else {
                int best = -1;
                for (int id : priority.keySet()) {
                    if (best < 0 || priority.get(id) < priority.get(best) || (priority.get(id).equals(priority.get(best)) && id < best)) best = id;
                }
                out.add(best);
                if (best >= 0) priority.remove(best);
            }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(run(new int[][]{{0, 1, 5}, {0, 2, 3}, {0, 1, 1}, {1}, {1}, {1}}), new int[]{1, 2, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(run(new int[][]{{0, 7, 4}, {0, 7, 9}, {0, 3, 6}, {1}, {1}}), new int[]{3, 7})) throw new AssertionError("example 2");

        PriorityQueue<int[]> arrays = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
        int[] card = {4, 1};
        arrays.offer(card);
        if (arrays.contains(new int[]{4, 1})) throw new AssertionError("an equal-looking array is a different object");
        if (arrays.remove(new int[]{4, 1})) throw new AssertionError("remove(Object) must not find the copy");
        if (!arrays.contains(card) || !arrays.remove(card)) throw new AssertionError("the same object is found");

        Random rnd = new Random(1761);
        for (int t = 0; t < 4000; t++) {
            int m = 1 + rnd.nextInt(20);
            int[][] ops = new int[m][];
            for (int i = 0; i < m; i++) ops[i] = rnd.nextInt(3) == 0 ? new int[]{1} : new int[]{0, rnd.nextInt(4), 1 + rnd.nextInt(5)};
            if (!Arrays.equals(run(ops), scan(ops))) throw new AssertionError("differs from the scan on " + Arrays.deepToString(ops));
        }
    }
}
```

#### Solution: [Vary] Delayed Removal Counts (Author exercise)
<!-- id: hp-delayed-removal-counts -->

**Approach.** There are no ids here, so the companion state is a map from a value to the number of its copies that have been removed logically. A removal increments that count and does nothing else. A query runs the cleanup loop: while the root has a positive pending count, decrement the count, delete the entry when it reaches zero, and poll the root. After the loop the root, if any, is live, and it is the answer. Both examples are asserted, and a multiset kept as a list with real deletions is the oracle on random streams that contain many equal values. The class from the lesson is used as it is written there, so its `size()` is also compared with the oracle's size.

**Complexity.** Every add is paid for once by its later discard, so m operations take O(m log m) time and O(m) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class DelayedRemovalCounts {
    static final class LazyMinBag {
        private final PriorityQueue<Integer> heap = new PriorityQueue<>();
        private final HashMap<Integer, Integer> pending = new HashMap<>();
        private int live;

        void add(int v) { heap.offer(v); live++; }
        void remove(int v) { pending.merge(v, 1, Integer::sum); live--; }
        int size() { return live; }
        Integer min() { cleanRoot(); return heap.peek(); }
        int physical() { return heap.size(); }

        private void cleanRoot() {
            while (!heap.isEmpty()) {
                Integer top = heap.peek();
                Integer count = pending.get(top);
                if (count == null) return;
                if (count == 1) pending.remove(top); else pending.put(top, count - 1);
                heap.poll();
            }
        }
    }

    static int[] answers(int[] ops) {
        LazyMinBag bag = new LazyMinBag();
        ArrayList<Integer> out = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) bag.add(op);
            else if (op < 0) bag.remove(-op);
            else { Integer m = bag.min(); out.add(m == null ? -1 : m); }
        }
        int[] r = new int[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(answers(new int[]{5, 3, 8, -3, 0, -5, 0, 0}), new int[]{5, 8, 8})) throw new AssertionError("example 1");
        if (!Arrays.equals(answers(new int[]{2, -2, 0}), new int[]{-1})) throw new AssertionError("example 2");
        LazyMinBag probe = new LazyMinBag();
        probe.add(1); probe.add(2); probe.add(3);
        probe.remove(2);
        if (probe.size() != 2 || probe.physical() != 3) throw new AssertionError("logical size and heap size differ until cleanup");
        Random rnd = new Random(1762);
        for (int t = 0; t < 4000; t++) {
            int m = 1 + rnd.nextInt(24);
            ArrayList<Integer> bag = new ArrayList<>();
            int[] ops = new int[m];
            LazyMinBag bag2 = new LazyMinBag();
            ArrayList<Integer> expected = new ArrayList<>();
            ArrayList<Integer> got = new ArrayList<>();
            for (int i = 0; i < m; i++) {
                int r = rnd.nextInt(4);
                if (r == 0 && !bag.isEmpty()) {
                    int v = bag.remove(rnd.nextInt(bag.size()));
                    ops[i] = -v;
                    bag2.remove(v);
                } else if (r == 1) {
                    ops[i] = 0;
                    expected.add(bag.isEmpty() ? -1 : java.util.Collections.min(bag));
                    Integer x = bag2.min();
                    got.add(x == null ? -1 : x);
                } else {
                    int v = 1 + rnd.nextInt(4);
                    ops[i] = v;
                    bag.add(v);
                    bag2.add(v);
                }
                if (bag2.size() != bag.size()) throw new AssertionError("logical size differs");
            }
            if (!expected.equals(got)) throw new AssertionError("queries differ on " + Arrays.toString(ops));
            int[] viaMethod = answers(ops);
            for (int i = 0; i < viaMethod.length; i++) if (viaMethod[i] != expected.get(i)) throw new AssertionError("answers() differs on " + Arrays.toString(ops));
        }
    }
}
```

#### Solution: [Boundary] Several Stale Roots (Author exercise)
<!-- id: hp-several-stale-roots -->

**Approach.** The cleanup must be a loop, since removing equal values can leave several stale entries at the top together, and each pass consumes one pending count. The method counts every entry the cleanup discards, reads the heap's physical size at the end, and takes the live size from the logical counter. Entries below a live root are never visited, so they stay in the heap, which is why the second example reports three physical entries for one live value. Both examples are asserted. The oracle models the physical contents as a sorted list with the same pending map, so a mistake in the heap handling would show up as a different count, and the invariant `physical = adds - discarded` is asserted on every random stream.

**Complexity.** The cost is O(m log m) time for m operations and O(m) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class SeveralStaleRoots {
    static int[] report(int[] ops) {
        PriorityQueue<Integer> heap = new PriorityQueue<>();
        HashMap<Integer, Integer> pending = new HashMap<>();
        int live = 0, discarded = 0;
        for (int op : ops) {
            if (op > 0) { heap.offer(op); live++; }
            else if (op < 0) { pending.merge(-op, 1, Integer::sum); live--; }
            else {
                while (!heap.isEmpty() && pending.getOrDefault(heap.peek(), 0) > 0) {
                    int top = heap.poll();
                    pending.merge(top, -1, Integer::sum);
                    discarded++;
                }
            }
        }
        return new int[]{discarded, heap.size(), live};
    }

    static int[] model(int[] ops) {
        ArrayList<Integer> physical = new ArrayList<>();
        HashMap<Integer, Integer> pending = new HashMap<>();
        int live = 0, discarded = 0;
        for (int op : ops) {
            if (op > 0) { physical.add(op); Collections.sort(physical); live++; }
            else if (op < 0) { pending.merge(-op, 1, Integer::sum); live--; }
            else {
                while (!physical.isEmpty() && pending.getOrDefault(physical.get(0), 0) > 0) {
                    int top = physical.remove(0);
                    pending.merge(top, -1, Integer::sum);
                    discarded++;
                }
            }
        }
        return new int[]{discarded, physical.size(), live};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(report(new int[]{4, 4, 4, -4, -4, 0}), new int[]{2, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(report(new int[]{1, 2, 3, -2, -3, 0, 0}), new int[]{0, 3, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(1763);
        for (int t = 0; t < 5000; t++) {
            int m = 1 + rnd.nextInt(26);
            ArrayList<Integer> bag = new ArrayList<>();
            int[] ops = new int[m];
            int adds = 0;
            for (int i = 0; i < m; i++) {
                int r = rnd.nextInt(4);
                if (r == 0 && !bag.isEmpty()) {
                    int v = bag.remove(rnd.nextInt(bag.size()));
                    ops[i] = -v;
                } else if (r == 1) ops[i] = 0;
                else {
                    int v = 1 + rnd.nextInt(3);
                    ops[i] = v;
                    bag.add(v);
                    adds++;
                }
            }
            int[] got = report(ops);
            if (!Arrays.equals(got, model(ops))) throw new AssertionError("report differs on " + Arrays.toString(ops));
            if (got[1] != adds - got[0]) throw new AssertionError("physical size must be adds minus discards");
            if (got[2] != bag.size()) throw new AssertionError("live size must match the real contents");
        }
    }
}
```

#### Solution: [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-sliding-window-median -->

**Approach.** Keep the smaller half in a max-heap `lo` and the larger half in a min-heap `hi`, with logical sizes `loSize` and `hiSize`. A new value goes to `lo` if it is at most the root of `lo`, and otherwise to `hi`. When the oldest value leaves the window, a pending count is recorded for it, the half that owned it is the one whose root bounds it, and that half's logical size drops. Both roots are then cleaned of stale entries, and one root is moved across if the logical sizes differ by more than allowed, with a cleanup of the heap that gave up its root. For odd `k` the median is the root of `lo`, and for even `k` it is the average of the two roots, taken after widening to `double`, because the sum of two `int` values can overflow. Both examples are asserted, the overflowing sum is shown on two copies of the largest `int`, and a brute-force sort of each window is the oracle on random arrays with many duplicates and the two extreme values.

**Complexity.** Each value enters a heap once and leaves once, so the time is O(n log n), and the heaps and the pending map hold O(n) entries in the worst case.

```java run
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.Random;

public final class SlidingWindowMedian {
    static void prune(PriorityQueue<Integer> heap, HashMap<Integer, Integer> pending) {
        while (!heap.isEmpty()) {
            Integer top = heap.peek();
            Integer count = pending.get(top);
            if (count == null) return;
            if (count == 1) pending.remove(top); else pending.put(top, count - 1);
            heap.poll();
        }
    }

    static double[] medians(int[] nums, int k) {
        PriorityQueue<Integer> lo = new PriorityQueue<>(Comparator.reverseOrder());
        PriorityQueue<Integer> hi = new PriorityQueue<>();
        HashMap<Integer, Integer> pending = new HashMap<>();
        int loSize = 0, hiSize = 0;
        double[] out = new double[nums.length - k + 1];
        for (int i = 0; i < nums.length; i++) {
            if (lo.isEmpty() || nums[i] <= lo.peek()) { lo.offer(nums[i]); loSize++; }
            else { hi.offer(nums[i]); hiSize++; }
            if (i >= k) {
                int gone = nums[i - k];
                pending.merge(gone, 1, Integer::sum);
                if (gone <= lo.peek()) loSize--; else hiSize--;
                prune(lo, pending);
                prune(hi, pending);
            }
            if (loSize > hiSize + 1) { hi.offer(lo.poll()); loSize--; hiSize++; prune(lo, pending); }
            else if (loSize < hiSize) { lo.offer(hi.poll()); hiSize--; loSize++; prune(hi, pending); }
            if (i >= k - 1) out[i - k + 1] = (k % 2 == 1) ? lo.peek() : ((double) lo.peek() + hi.peek()) / 2;
        }
        return out;
    }

    static double[] byFullSort(int[] nums, int k) {
        double[] out = new double[nums.length - k + 1];
        for (int s = 0; s + k <= nums.length; s++) {
            int[] w = Arrays.copyOfRange(nums, s, s + k);
            Arrays.sort(w);
            out[s] = (k % 2 == 1) ? w[k / 2] : ((double) w[k / 2 - 1] + w[k / 2]) / 2;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(medians(new int[]{3, 9, 1, 7, 5, 2}, 3), new double[]{3.0, 7.0, 5.0, 5.0})) throw new AssertionError("example 1");
        if (!Arrays.equals(medians(new int[]{4, 6, 2, 8}, 2), new double[]{5.0, 4.0, 5.0})) throw new AssertionError("example 2");
        int max = Integer.MAX_VALUE;
        if ((max + max) / 2.0 >= 0) throw new AssertionError("the int sum must overflow to a negative number");
        if (medians(new int[]{max, max}, 2)[0] != (double) max) throw new AssertionError("widened average of two maxima");
        Random rnd = new Random(1764);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 1, -1, 5, 5, 5};
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(18);
            int[] a = new int[n];
            boolean small = rnd.nextBoolean();
            for (int i = 0; i < n; i++) a[i] = small ? rnd.nextInt(5) - 2 : pool[rnd.nextInt(pool.length)];
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(medians(a, k), byFullSort(a, k))) throw new AssertionError("differs on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```
