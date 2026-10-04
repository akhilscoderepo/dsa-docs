<!-- solutions-for: 03-top-k -->
### Top K

#### Solution: [Build] K Largest Values (Author exercise)
<!-- id: hp-k-largest-values -->

**Approach.** Keep a natural-order queue that never exceeds `k` items. While it is below the limit, offer the value. Once it is full, the root is the weakest retained value, and a strictly larger newcomer replaces it by a poll followed by an offer. At the end the polls arrive weakest first, so they are written into the result from the back. The assertions check both examples, the case `k = 0`, a recorded peak size that never passes `k`, and a comparison with the first `k` values of a descending sort on random arrays with many duplicates.

**Complexity.** Each value costs at most two operations on a heap of size k, giving O(n log k) time, and the heap uses O(k) memory.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class KLargestValues {
    static int peak;

    static int[] kLargest(int[] values, int k) {
        PriorityQueue<Integer> best = new PriorityQueue<>();
        peak = 0;
        for (int v : values) {
            if (best.size() < k) best.offer(v);
            else if (k > 0 && v > best.peek()) {
                best.poll();
                best.offer(v);
            }
            peak = Math.max(peak, best.size());
        }
        int[] out = new int[best.size()];
        for (int i = out.length - 1; i >= 0; i--) out[i] = best.poll();
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(kLargest(new int[]{4, 9, 1, 7, 3, 8}, 3), new int[]{9, 8, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(kLargest(new int[]{5, 5, 2}, 2), new int[]{5, 5})) throw new AssertionError("example 2");
        if (kLargest(new int[]{1, 2, 3}, 0).length != 0) throw new AssertionError("k = 0 returns nothing");
        Random rnd = new Random(1731);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            int k = rnd.nextInt(n + 1);
            ArrayList<Integer> boxed = new ArrayList<>();
            for (int v : a) boxed.add(v);
            boxed.sort(Collections.reverseOrder());
            int[] expected = new int[k];
            for (int i = 0; i < k; i++) expected[i] = boxed.get(i);
            int[] got = kLargest(a, k);
            if (!Arrays.equals(got, expected)) throw new AssertionError("disagrees with the sort on " + Arrays.toString(a) + " k=" + k);
            if (peak > k) throw new AssertionError("the heap grew past k: " + peak + " > " + k);
        }
    }
}
```

#### Solution: [Vary] Kth Largest Element in an Array (LeetCode 215)
<!-- id: hp-kth-largest-element -->

**Approach.** Run the same bounded heap and return `peek()` after the scan. The heap holds the `k` largest values, and its root is the smallest of them, which is the k-th largest of the whole array when duplicates are counted separately. The contents never need to be sorted. Both examples are asserted, and the element at position `k - 1` of a descending sort is the oracle on random arrays, including arrays where all values are equal.

**Complexity.** The scan takes O(n log k) time with O(k) memory, which is the same bound as the previous rung, and the final read is constant.

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class KthLargestElement {
    static int kthLargest(int[] nums, int k) {
        PriorityQueue<Integer> best = new PriorityQueue<>();
        for (int v : nums) {
            if (best.size() < k) best.offer(v);
            else if (v > best.peek()) {
                best.poll();
                best.offer(v);
            }
        }
        return best.peek();
    }

    public static void main(String[] args) {
        if (kthLargest(new int[]{8, 2, 9, 4, 9, 1}, 2) != 9) throw new AssertionError("example 1");
        if (kthLargest(new int[]{-1, -4, -2}, 3) != -4) throw new AssertionError("example 2");
        if (kthLargest(new int[]{6, 6, 6}, 2) != 6) throw new AssertionError("equal values count separately");
        Random rnd = new Random(1732);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            int k = 1 + rnd.nextInt(n);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            int expected = sorted[n - k];
            if (kthLargest(a, k) != expected) throw new AssertionError("disagrees with the sort on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] K Equals One Or N (Author exercise)
<!-- id: hp-k-one-or-n -->

**Approach.** The same rule serves both limits. With `k = 1` the heap is full after the first value, so the root is a running maximum and every strictly larger value is a replacement, while an equal value is not. With `k = n` the heap fills exactly at the last value and is never full beforehand, so no replacement can occur and the root is the overall minimum. The method returns the root and the replacement count. The assertions check both examples, check that the root equals the k-th largest by sorting, and check the replacement count against a separate simulation that keeps a sorted list of the retained values.

**Complexity.** The time is O(n log k) and the memory is O(k).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class KEqualsOneOrN {
    static int[] rootAndReplacements(int[] values, int k) {
        PriorityQueue<Integer> best = new PriorityQueue<>();
        int replacements = 0;
        for (int v : values) {
            if (best.size() < k) best.offer(v);
            else if (v > best.peek()) {
                best.poll();
                best.offer(v);
                replacements++;
            }
        }
        return new int[]{best.peek(), replacements};
    }

    static int[] withSortedList(int[] values, int k) {
        ArrayList<Integer> kept = new ArrayList<>();
        int replacements = 0;
        for (int v : values) {
            if (kept.size() < k) kept.add(v);
            else if (v > kept.get(0)) {
                kept.set(0, v);
                replacements++;
            }
            java.util.Collections.sort(kept);
        }
        return new int[]{kept.get(0), replacements};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(rootAndReplacements(new int[]{3, 1, 4, 1, 5, 9, 2, 6}, 1), new int[]{9, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(rootAndReplacements(new int[]{2, 7, 1}, 3), new int[]{1, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(rootAndReplacements(new int[]{4, 4, 4}, 1), new int[]{4, 0})) throw new AssertionError("equal values never replace");
        Random rnd = new Random(1733);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(8) - 3;
            int k = rnd.nextInt(3) == 0 ? 1 : rnd.nextInt(3) == 0 ? n : 1 + rnd.nextInt(n);
            int[] got = rootAndReplacements(a, k);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            if (got[0] != sorted[n - k]) throw new AssertionError("root is not the k-th largest on " + Arrays.toString(a) + " k=" + k);
            if (!Arrays.equals(got, withSortedList(a, k))) throw new AssertionError("replacement count disagrees on " + Arrays.toString(a) + " k=" + k);
            if (k == n && got[1] != 0) throw new AssertionError("k = n never replaces");
        }
    }
}
```

#### Solution: [Recognize] Top K Frequent Elements (LeetCode 347)
<!-- id: hp-top-k-frequent -->

**Approach.** Count occurrences in a `HashMap`, then run the bounded heap over the distinct values, ranking each entry `{count, value}` by count with the value as a final tie-break so that the order is total. Offer each entry, and poll once whenever the heap holds more than `k` entries, which removes the least frequent of the candidates. The remaining entries are the answer, and the method sorts their values ascending as the contract requires. The assertions check both examples, check that the heap never holds more than `k + 1` entries, and compare with sorting all distinct values by count on random arrays whose `k`-th and `(k+1)`-th counts differ, since the problem guarantees a unique answer.

**Complexity.** Counting costs O(n), and the heap over d distinct values costs O(d log k), so the total is O(n + d log k) with O(d) memory for the map.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;
import java.util.Random;

public final class TopKFrequent {
    static int peakSize;

    static int[] topK(int[] nums, int k) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        PriorityQueue<int[]> heap = new PriorityQueue<>(
            Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]));
        peakSize = 0;
        for (Map.Entry<Integer, Integer> e : count.entrySet()) {
            heap.offer(new int[]{e.getValue(), e.getKey()});
            if (heap.size() > k) heap.poll();
            peakSize = Math.max(peakSize, heap.size());
        }
        int[] out = new int[heap.size()];
        int i = 0;
        for (int[] e : heap) out[i++] = e[1];
        Arrays.sort(out);
        return out;
    }

    static int[] bySorting(int[] nums, int k) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        ArrayList<Integer> keys = new ArrayList<>(count.keySet());
        keys.sort((x, y) -> count.get(x) != count.get(y).intValue() ? Integer.compare(count.get(y), count.get(x)) : Integer.compare(x, y));
        int[] out = new int[k];
        for (int i = 0; i < k; i++) out[i] = keys.get(i);
        Arrays.sort(out);
        return out;
    }

    static boolean uniqueTop(int[] nums, int k) {
        HashMap<Integer, Integer> count = new HashMap<>();
        for (int v : nums) count.merge(v, 1, Integer::sum);
        ArrayList<Integer> freqs = new ArrayList<>(count.values());
        freqs.sort(java.util.Collections.reverseOrder());
        return k == freqs.size() || !freqs.get(k - 1).equals(freqs.get(k));
    }

    public static void main(String[] args) {
        if (!Arrays.equals(topK(new int[]{7, 7, 7, 3, 3, 9, 9, 9, 9, 1}, 2), new int[]{7, 9})) throw new AssertionError("example 1");
        if (!Arrays.equals(topK(new int[]{5}, 1), new int[]{5})) throw new AssertionError("example 2");
        Random rnd = new Random(1734);
        int checked = 0;
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            int distinct = (int) Arrays.stream(a).distinct().count();
            int k = 1 + rnd.nextInt(distinct);
            if (!uniqueTop(a, k)) continue;
            checked++;
            if (!Arrays.equals(topK(a, k), bySorting(a, k))) throw new AssertionError("disagrees with the sort on " + Arrays.toString(a) + " k=" + k);
            if (peakSize > k + 1) throw new AssertionError("heap exceeded k + 1 entries");
        }
        if (checked < 500) throw new AssertionError("too few valid random cases: " + checked);
    }
}
```
