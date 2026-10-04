<!-- solutions-for: 07-running-median -->
### Running Median

#### Solution: [Build] Rebalance Two Halves (Author exercise)
<!-- id: hp-rebalance-two-halves -->

**Approach.** Every value takes the same three steps: offer it to the lower max-heap, move that heap's root to the upper min-heap, and if the upper heap is now larger, move its root back. The crossing guarantees that the order between the halves survives, because the value that crosses is the largest of the lower side. After n insertions the sizes are `(n + 1) / 2` and `n / 2`, and the roots are the two middle elements of the sorted array, which is how the random test judges the result. The harness also runs a flawed variant that alternates insertions between the halves without crossing, and it shows that this variant ends with a lower root larger than the upper root on the input `[15, 5]`.

**Complexity.** Each insertion makes a constant number of heap operations, so n insertions take O(n log n) time with O(n) memory.

```java run
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class RebalanceTwoHalves {
    static int[] state(int[] values) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Collections.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        for (int v : values) {
            lower.offer(v);
            upper.offer(lower.poll());
            if (upper.size() > lower.size()) lower.offer(upper.poll());
        }
        return new int[]{lower.size(), upper.size(), lower.peek(), upper.isEmpty() ? 0 : upper.peek()};
    }

    static boolean alternatingBreaksOrder(int[] values) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Collections.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        for (int i = 0; i < values.length; i++) {
            if (i % 2 == 0) lower.offer(values[i]); else upper.offer(values[i]);
        }
        return !upper.isEmpty() && lower.peek() > upper.peek();
    }

    public static void main(String[] args) {
        if (!Arrays.equals(state(new int[]{5, 15, 1}), new int[]{2, 1, 5, 15})) throw new AssertionError("example 1");
        if (!Arrays.equals(state(new int[]{4}), new int[]{1, 0, 4, 0})) throw new AssertionError("example 2");
        if (!alternatingBreaksOrder(new int[]{15, 5})) throw new AssertionError("inserting by turns without crossing breaks the order between halves");
        Random rnd = new Random(1771);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(20);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(8);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            int lowSize = (n + 1) / 2;
            int[] expected = {lowSize, n - lowSize, sorted[lowSize - 1], n - lowSize > 0 ? sorted[lowSize] : 0};
            if (!Arrays.equals(state(a), expected)) throw new AssertionError("state differs on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Find Median from Data Stream (LeetCode 295)
<!-- id: hp-find-median-stream -->

**Approach.** Use the two heaps with the size rule that the lower heap is equal to the upper heap or one larger. A query returns the lower root when the lower heap is larger, which happens exactly for an odd count, and otherwise the average of the two roots. The method wraps the roots in `double` before the division. Both examples are asserted, and the sorted-list method from the naive stage is the oracle on random operation streams, with the median read after every query.

**Complexity.** An add costs O(log n), a query costs O(1), and the memory is O(n).

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class FindMedianStream {
    static double[] answers(int[] ops) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Collections.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        ArrayList<Double> out = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) {
                lower.offer(op);
                upper.offer(lower.poll());
                if (upper.size() > lower.size()) lower.offer(upper.poll());
            } else {
                out.add(lower.size() > upper.size() ? (double) lower.peek() : ((double) lower.peek() + upper.peek()) / 2);
            }
        }
        double[] r = new double[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    static double[] byInsertion(int[] ops) {
        ArrayList<Integer> sorted = new ArrayList<>();
        ArrayList<Double> out = new ArrayList<>();
        for (int op : ops) {
            if (op > 0) {
                int pos = Collections.binarySearch(sorted, op);
                if (pos < 0) pos = -pos - 1;
                sorted.add(pos, op);
            } else {
                int n = sorted.size();
                out.add(n % 2 == 1 ? (double) sorted.get(n / 2) : ((double) sorted.get(n / 2 - 1) + sorted.get(n / 2)) / 2);
            }
        }
        double[] r = new double[out.size()];
        for (int i = 0; i < r.length; i++) r[i] = out.get(i);
        return r;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(answers(new int[]{5, 15, 0, 1, 0, 3, 0}), new double[]{10.0, 5.0, 4.0})) throw new AssertionError("example 1");
        if (!Arrays.equals(answers(new int[]{2, 0}), new double[]{2.0})) throw new AssertionError("example 2");
        Random rnd = new Random(1772);
        for (int t = 0; t < 4000; t++) {
            int m = 2 + rnd.nextInt(24);
            int[] ops = new int[m];
            boolean any = false;
            for (int i = 0; i < m; i++) {
                if (any && rnd.nextInt(3) == 0) ops[i] = 0;
                else { ops[i] = 1 + rnd.nextInt(9); any = true; }
            }
            if (!Arrays.equals(answers(ops), byInsertion(ops))) throw new AssertionError("medians differ on " + Arrays.toString(ops));
        }
    }
}
```

#### Solution: [Boundary] Overflow-Safe Even Median (Author exercise)
<!-- id: hp-overflow-safe-median -->

**Approach.** The structure is unchanged, and only the average of the two roots needs care. Casting the first root to `double` before the addition forces the sum to be computed in floating point, where two `int` values always fit exactly. An expression such as `(a + b) / 2.0` adds in `int` first and wraps around for large operands. The harness asserts both examples and shows that the careless form gives 0.0 for two copies of the smallest `int`, and a negative number for two copies of the largest. Random prefixes drawn from a pool of extreme values are checked against a sorted copy whose average is formed through `long`.

**Complexity.** The time is O(n log n) and the memory is O(n).

```java run
import java.util.Arrays;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Random;

public final class OverflowSafeMedian {
    static double[] prefixMedians(int[] values, boolean widen) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Collections.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        double[] out = new double[values.length];
        for (int i = 0; i < values.length; i++) {
            lower.offer(values[i]);
            upper.offer(lower.poll());
            if (upper.size() > lower.size()) lower.offer(upper.poll());
            if (lower.size() > upper.size()) out[i] = lower.peek();
            else if (widen) out[i] = ((double) lower.peek() + upper.peek()) / 2;
            else out[i] = (lower.peek() + upper.peek()) / 2.0;
        }
        return out;
    }

    static double[] byRescanning(int[] values) {
        double[] out = new double[values.length];
        for (int i = 0; i < values.length; i++) {
            int[] w = Arrays.copyOf(values, i + 1);
            Arrays.sort(w);
            int n = w.length;
            out[i] = n % 2 == 1 ? w[n / 2] : ((long) w[n / 2 - 1] + (long) w[n / 2]) / 2.0;
        }
        return out;
    }

    public static void main(String[] args) {
        int min = Integer.MIN_VALUE, max = Integer.MAX_VALUE;
        if (!Arrays.equals(prefixMedians(new int[]{max, max}, true), new double[]{max, max})) throw new AssertionError("example 1");
        if (!Arrays.equals(prefixMedians(new int[]{min, min}, true), new double[]{min, min})) throw new AssertionError("example 2");
        if (prefixMedians(new int[]{min, min}, false)[1] != 0.0) throw new AssertionError("the int sum of two minima wraps to zero");
        if (prefixMedians(new int[]{max, max}, false)[1] >= 0) throw new AssertionError("the int sum of two maxima wraps to a negative number");
        if (prefixMedians(new int[]{min, max}, true)[1] != -0.5) throw new AssertionError("the extremes average to -0.5");
        Random rnd = new Random(1773);
        int[] pool = {min, max, 0, -1, 1, min + 1, max - 1};
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = pool[rnd.nextInt(pool.length)];
            if (!Arrays.equals(prefixMedians(a, true), byRescanning(a))) throw new AssertionError("medians differ on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-window-lower-median-report -->

**Approach.** Entries in both heaps are `{value, index}` pairs, and an entry is stale as soon as its index is at most `i - k`, so the age test needs no map. A boolean array records which half currently owns each index, and the logical sizes change at insertion, at expiry and at every move. The order of work for each index is to insert the new value into the half its value belongs to, while the departing value still takes part in that comparison, apply the expiry to the owner's logical size, clean the roots, and then restore the size rule with moves that always take a live root. Once the window is full, the lower median is the root of the lower heap, since the lower half is the larger one when `k` is odd and equal otherwise. Both examples are asserted, and a brute-force sort of every window is the oracle for the sum and the change count on random arrays with duplicates and extreme values. The sum is a `long`.

**Complexity.** Every index enters one heap, may move a bounded number of times, and leaves once, so the time is O(n log n) and the memory is O(n).

```java run
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Random;

public final class WindowLowerMedianReport {
    static void clean(PriorityQueue<int[]> heap, int oldestExpired) {
        while (!heap.isEmpty() && heap.peek()[1] <= oldestExpired) heap.poll();
    }

    static long[] report(int[] nums, int k) {
        int n = nums.length;
        PriorityQueue<int[]> lo = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        PriorityQueue<int[]> hi = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        boolean[] inLo = new boolean[n];
        int loSize = 0, hiSize = 0;
        long sum = 0, changes = 0;
        int previous = 0;
        boolean first = true;
        for (int i = 0; i < n; i++) {
            int expired = i - k;      // this index leaves the window now, but still takes part in the placement
            if (lo.isEmpty() || nums[i] <= lo.peek()[0]) { lo.offer(new int[]{nums[i], i}); inLo[i] = true; loSize++; }
            else { hi.offer(new int[]{nums[i], i}); hiSize++; }
            if (expired >= 0) { if (inLo[expired]) loSize--; else hiSize--; }
            clean(lo, expired);
            clean(hi, expired);
            while (loSize > hiSize + 1) {
                int[] e = lo.poll();
                inLo[e[1]] = false;
                hi.offer(e);
                loSize--; hiSize++;
                clean(lo, expired);
            }
            while (loSize < hiSize) {
                int[] e = hi.poll();
                inLo[e[1]] = true;
                lo.offer(e);
                hiSize--; loSize++;
                clean(hi, expired);
            }
            if (i >= k - 1) {
                int median = lo.peek()[0];
                sum += median;
                if (!first && median != previous) changes++;
                previous = median;
                first = false;
            }
        }
        return new long[]{sum, changes};
    }

    static long[] byFullSort(int[] nums, int k) {
        long sum = 0, changes = 0;
        int previous = 0;
        boolean first = true;
        for (int s = 0; s + k <= nums.length; s++) {
            int[] w = Arrays.copyOfRange(nums, s, s + k);
            Arrays.sort(w);
            int median = w[(k - 1) / 2];
            sum += median;
            if (!first && median != previous) changes++;
            previous = median;
            first = false;
        }
        return new long[]{sum, changes};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(report(new int[]{5, 1, 9, 7, 7, 2, 8}, 4), new long[]{26, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(report(new int[]{Integer.MIN_VALUE, Integer.MIN_VALUE, Integer.MAX_VALUE}, 2), new long[]{-4294967296L, 0})) throw new AssertionError("example 2");
        if (-4294967296L >= Integer.MIN_VALUE) throw new AssertionError("the sum is below the int range and needs a long");
        Random rnd = new Random(1774);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, 3, 3, -3};
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(18);
            int[] a = new int[n];
            boolean small = rnd.nextBoolean();
            for (int i = 0; i < n; i++) a[i] = small ? rnd.nextInt(5) - 2 : pool[rnd.nextInt(pool.length)];
            int k = 1 + rnd.nextInt(n);
            if (!Arrays.equals(report(a, k), byFullSort(a, k))) throw new AssertionError("report differs on " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```
