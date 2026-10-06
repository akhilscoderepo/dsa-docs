<!-- solutions-for: 03-top-k -->
### Solutions For Keeping The Best K

#### Solution: [Build] K Largest Values (Author exercise)
<!-- id: hp-k-largest-values -->

**Approach.**
The method keeps a natural-order queue of at most `k` values. The first `k` values enter without a test. Each later value is compared once with the root. A value that is not larger than the root is discarded, because `k` kept values are already at least as large. A larger value removes the root and takes its place. At the end the queue holds the `k` largest values. Polling returns them in ascending order, so the method fills the result array from the back.

Among the values seen, the queue always keeps the `min(k, seen)` largest.

**Complexity.**
- **Time** is O(n log k), because each value costs one root comparison and at most one removal and one insertion in a queue of size `k`.
- **Space** is O(k), because the queue never holds more than `k` values.

```java run
import java.util.*;

public final class KLargestValues {
    /**
     * Returns the k largest values in nonincreasing order.
     * Time: O(n log k). Space: O(k).
     * Invariant: the queue holds the min(k, seen) largest values seen so far.
     */
    static int[] kLargest(int[] values, int k) {
        PriorityQueue<Integer> kept = new PriorityQueue<>();
        for (int v : values) {
            // The first k values always stay.
            if (kept.size() < k) kept.offer(v);
            // A larger candidate replaces the root, the retention boundary.
            else if (k > 0 && v > kept.peek()) { kept.poll(); kept.offer(v); }
        }
        int[] best = new int[kept.size()];
        // Each poll returns the smallest kept value, so fill from the back.
        for (int i = best.length - 1; i >= 0; i--) best[i] = kept.poll();
        return best;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(kLargest(new int[] {5, 1, 9, 3, 7}, 3), new int[] {9, 7, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(kLargest(new int[] {2, 2, 2, 1}, 2), new int[] {2, 2})) throw new AssertionError("ex2");
        // The edges k = 0 and an empty array return empty results.
        if (kLargest(new int[] {3, 4}, 0).length != 0 || kLargest(new int[0], 0).length != 0) throw new AssertionError("empty");
        // A max-oriented queue trimmed to k values keeps the smallest values instead.
        PriorityQueue<Integer> wrong = new PriorityQueue<>(Collections.reverseOrder());
        for (int v : new int[] {5, 1, 9, 3, 7}) { wrong.offer(v); if (wrong.size() > 2) wrong.poll(); }
        if (wrong.contains(9)) throw new AssertionError("wrong direction keeps the smallest");
        // Random arrays must match sort-and-take.
        Random rnd = new Random(1721);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(25)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(9) - 4;
            int k = a.length == 0 ? 0 : rnd.nextInt(a.length + 1);
            int[] s = a.clone();
            Arrays.sort(s);
            int[] expect = new int[k];
            for (int i = 0; i < k; i++) expect[i] = s[s.length - 1 - i];
            if (!Arrays.equals(kLargest(a, k), expect)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Kth Largest Element in an Array (LeetCode 215)
<!-- id: hp-kth-largest-array -->

**Approach.**
The scan is the same as in the Build exercise, and the method returns the root after the last value. The root is the smallest of the `k` largest values, so it is the kth largest of the whole array. Exactly `k - 1` kept values are at least as large, and every discarded value is at most as large. Duplicates count separately, so two equal values both occupy a slot.

The invariant is that the root equals the kth largest of the values seen, once `k` values have been seen.

**Complexity.**
- **Time** is O(n log k), because each value costs one comparison and at most one removal and one insertion.
- **Space** is O(k), because the queue stores at most `k` values.

```java run
import java.util.*;

public final class KthLargestArray {
    /**
     * Returns the kth largest value of the array, counting duplicates.
     * Time: O(n log k). Space: O(k).
     * Invariant: the root is the kth largest value seen once k values have been seen.
     */
    static int kthLargest(int[] values, int k) {
        PriorityQueue<Integer> kept = new PriorityQueue<>();
        for (int v : values) {
            // Fill first; after that only a larger candidate changes the queue.
            if (kept.size() < k) kept.offer(v);
            else if (v > kept.peek()) { kept.poll(); kept.offer(v); }
        }
        // The root is the smallest of the k largest values.
        return kept.peek();
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (kthLargest(new int[] {8, 3, 8, 1, 6, 6}, 3) != 6) throw new AssertionError("ex1");
        if (kthLargest(new int[] {4}, 1) != 4) throw new AssertionError("ex2");
        // Duplicates count separately: the 2nd largest of [9, 9, 1] is 9.
        if (kthLargest(new int[] {9, 9, 1}, 2) != 9) throw new AssertionError("duplicates");
        // Random arrays must match the sorted array read from the end.
        Random rnd = new Random(1722);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[1 + rnd.nextInt(25)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(8) - 4;
            int k = 1 + rnd.nextInt(a.length);
            int[] s = a.clone();
            Arrays.sort(s);
            if (kthLargest(a, k) != s[s.length - k]) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] K Equals One Or N (Author exercise)
<!-- id: hp-k-one-or-n -->

**Approach.**
The scan keeps the same size-`k` queue and adds the kept values at the end in a `long` accumulator. At `k = 1` the queue holds one value, and each candidate either beats it or not, so the scan finds the maximum. At `k = n` the queue never evicts, because the queue fills exactly when the input ends, and the sum covers every value. The `int` sum of two large values wraps, so the accumulator has the type `long`.

The queue always holds the `k` largest values seen, so the final sum covers exactly those values.

**Complexity.**
- **Time** is O(n log k), because each value costs one comparison and at most one removal and one insertion.
- **Space** is O(k), because the queue stores at most `k` values.

```java run
import java.util.*;

public final class KOneOrN {
    /**
     * Returns the sum of the k largest values as a long.
     * Time: O(n log k). Space: O(k).
     * Invariant: the queue holds the k largest values seen so far.
     */
    static long sumOfKLargest(int[] values, int k) {
        PriorityQueue<Integer> kept = new PriorityQueue<>();
        for (int v : values) {
            // At k = n the first branch always runs, so nothing is evicted.
            if (kept.size() < k) kept.offer(v);
            // At k = 1 the queue holds one value and each candidate either beats it or not.
            else if (v > kept.peek()) { kept.poll(); kept.offer(v); }
        }
        long sum = 0;
        // A long accumulator avoids int wraparound for large values.
        for (int v : kept) sum += v;
        return sum;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (sumOfKLargest(new int[] {4, 9, 2}, 1) != 9) throw new AssertionError("ex1");
        if (sumOfKLargest(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, 2) != 4294967294L) throw new AssertionError("ex2");
        // The int sum of the same two values wraps to -2, which is the bug the exercise guards against.
        if (Integer.MAX_VALUE + Integer.MAX_VALUE != -2) throw new AssertionError("int wraps");
        // Random arrays must match sorting, at k = 1, k = n and a middle k.
        Random rnd = new Random(1723);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[1 + rnd.nextInt(20)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextBoolean() ? Integer.MAX_VALUE - rnd.nextInt(3) : rnd.nextInt(7) - 3;
            int[] ks = {1, a.length, 1 + rnd.nextInt(a.length)};
            int[] s = a.clone();
            Arrays.sort(s);
            for (int k : ks) {
                long expect = 0;
                for (int i = 0; i < k; i++) expect += s[s.length - 1 - i];
                if (sumOfKLargest(a, k) != expect) throw new AssertionError("random " + t + " k " + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Top K Frequent Elements (LeetCode 347)
<!-- id: hp-top-k-frequent -->

**Approach.**
A hash map counts how often each value occurs. The method then scans the distinct values with a size-`k` queue ordered by frequency, smallest at the root. This is the same retention rule as before, with frequency as the key. A value enters while the queue holds fewer than `k` entries, and later it replaces the root only when its frequency is larger. After the scan, the queue holds the `k` most frequent values. The uniqueness guarantee means no tie at the boundary can change the answer set.

Among the distinct values seen, the queue always keeps the `min(k, seen)` most frequent ones.

**Complexity.**
- **Time** is O(n + d log k), where `d` is the number of distinct values, because counting costs O(n) and each distinct value costs O(log k).
- **Space** is O(d), because the map stores one entry per distinct value, and the queue adds O(k).

```java run
import java.util.*;

public final class TopKFrequent {
    /**
     * Returns the k most frequent values in any order.
     * Time: O(n + d log k). Space: O(d).
     * Invariant: the queue holds the min(k, seen) most frequent distinct values seen.
     */
    static int[] topK(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        // One pass counts each value.
        for (int v : nums) count.merge(v, 1, Integer::sum);
        // The queue orders entries by frequency, so the root is the least frequent kept value.
        PriorityQueue<int[]> kept = new PriorityQueue<>((p, q) -> Integer.compare(p[1], q[1]));
        for (Map.Entry<Integer, Integer> e : count.entrySet()) {
            int[] entry = {e.getKey(), e.getValue()};
            if (kept.size() < k) kept.offer(entry);
            // A strictly more frequent value replaces the root.
            else if (entry[1] > kept.peek()[1]) { kept.poll(); kept.offer(entry); }
        }
        int[] out = new int[kept.size()];
        for (int i = 0; i < out.length; i++) out[i] = kept.poll()[0];
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise; the output order is free, so compare sorted copies.
        int[] r1 = topK(new int[] {4, 1, 1, 2, 2, 2, 4, 4, 4}, 2);
        Arrays.sort(r1);
        if (!Arrays.equals(r1, new int[] {2, 4})) throw new AssertionError("ex1");
        if (!Arrays.equals(topK(new int[] {9}, 1), new int[] {9})) throw new AssertionError("ex2");
        // Random arrays whose answer is unique must match a sort by frequency.
        Random rnd = new Random(1724);
        int checked = 0;
        for (int t = 0; t < 600; t++) {
            int[] a = new int[1 + rnd.nextInt(30)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(6);
            Map<Integer, Integer> c = new HashMap<>();
            for (int v : a) c.merge(v, 1, Integer::sum);
            List<Map.Entry<Integer, Integer>> es = new ArrayList<>(c.entrySet());
            es.sort((x, y) -> Integer.compare(y.getValue(), x.getValue()));
            int k = 1 + rnd.nextInt(es.size());
            // The exercise guarantees a unique answer, so skip inputs that tie at the boundary.
            if (k < es.size() && es.get(k - 1).getValue().equals(es.get(k).getValue())) continue;
            int[] expect = new int[k];
            for (int i = 0; i < k; i++) expect[i] = es.get(i).getKey();
            int[] got = topK(a, k);
            Arrays.sort(expect);
            Arrays.sort(got);
            if (!Arrays.equals(got, expect)) throw new AssertionError("random " + t);
            checked++;
        }
        if (checked < 50) throw new AssertionError("too few unique cases");
    }
}
```
