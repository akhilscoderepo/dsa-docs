<!-- solutions-for: 07-running-median -->
### Solutions For Tracking The Median

#### Solution: [Build] Rebalance Two Halves (Author exercise)
<!-- id: hp-rebalance-halves -->

**Approach.**
The method keeps a max-first queue for the lower half and a min-first queue for the upper half. A new value goes to the lower half when it is at most the lower root, and to the upper half otherwise. That placement keeps every lower value at most every upper value. The size rule may break by one, so the method then moves one root. A lower half that is two values ahead gives its root to the upper half. An upper half that is ahead gives its root to the lower half. A moved root stays on the correct side of the boundary, because it is the value nearest to that boundary. After each insertion, the method records the lower root.

The invariant has two parts. The lower half is never smaller than the upper half and never larger by more than one value. The lower root is at most the upper root.

**Complexity.**
- **Time** is O(n log n), because each of the n insertions makes at most three queue operations.
- **Space** is O(n), because both queues together hold every value.

```java run
import java.util.*;

public final class RebalanceHalves {
    /**
     * Returns the lower root after each insertion.
     * Time: O(n log n). Space: O(n).
     * Invariant: lower holds equal or one more values than upper, and lower root <= upper root.
     */
    static int[] lowerRoots(int[] values) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Comparator.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        int[] out = new int[values.length];
        for (int i = 0; i < values.length; i++) {
            int v = values[i];
            // The order rule picks the side; a value equal to the lower root stays in the lower half.
            if (lower.isEmpty() || v <= lower.peek()) lower.offer(v);
            else upper.offer(v);
            // The size rule is repaired by moving one root across the boundary.
            if (lower.size() > upper.size() + 1) upper.offer(lower.poll());
            else if (upper.size() > lower.size()) lower.offer(upper.poll());
            out[i] = lower.peek();
        }
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(lowerRoots(new int[] {5, 2, 8, 1}), new int[] {5, 2, 5, 2})) throw new AssertionError("ex1");
        if (lowerRoots(new int[0]).length != 0) throw new AssertionError("ex2");
        // Duplicates keep the rule: the lower root is the smaller middle value.
        if (!Arrays.equals(lowerRoots(new int[] {4, 4, 4}), new int[] {4, 4, 4})) throw new AssertionError("duplicates");
        // Random streams must match the sorted position ceil(i / 2).
        Random rnd = new Random(1771);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(25)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(9) - 4;
            int[] got = lowerRoots(a);
            for (int i = 1; i <= a.length; i++) {
                int[] prefix = Arrays.copyOf(a, i);
                Arrays.sort(prefix);
                // The position ceil(i / 2) counted from 1 is index (i + 1) / 2 - 1.
                if (got[i - 1] != prefix[(i + 1) / 2 - 1]) throw new AssertionError("random " + t + " prefix " + i);
            }
        }
    }
}
```

#### Solution: [Vary] Find Median from Data Stream (LeetCode 295)
<!-- id: hp-find-median-stream -->

**Approach.**
The class stores the two halves from the Build exercise. The method `findMedian` compares the two sizes. When the lower half is larger, the count is odd and the answer is the lower root. Otherwise the sizes are equal, the count is even, and the answer is the average of the two roots. The sum uses `long` so that extreme values cannot wrap. Each `addNum` call keeps both rules, so `findMedian` needs no work beyond reading the roots.

Both rules hold after every call. The size gap between the halves is 0 or 1 in favor of the lower half, and no lower value exceeds an upper value.

**Complexity.**
- **Time** is O(log n) per `addNum` and O(1) per `findMedian`, because insertion touches at most three queue operations and the median reads two roots.
- **Space** is O(n), because the two queues hold every value.

```java run
import java.util.*;

public final class FindMedianStream {
    static final class MedianFinder {
        private final PriorityQueue<Integer> lower = new PriorityQueue<>(Comparator.reverseOrder());
        private final PriorityQueue<Integer> upper = new PriorityQueue<>();

        /**
         * Adds one value and restores both rules.
         * Time: O(log n). Space: O(1) extra.
         */
        void addNum(int num) {
            if (lower.isEmpty() || num <= lower.peek()) lower.offer(num);
            else upper.offer(num);
            // Repair the size rule by moving one root.
            if (lower.size() > upper.size() + 1) upper.offer(lower.poll());
            else if (upper.size() > lower.size()) lower.offer(upper.poll());
        }

        /**
         * Returns the median of all added values.
         * Time: O(1). Space: O(1).
         */
        double findMedian() {
            // A larger lower half means an odd count, and its root is the median.
            if (lower.size() > upper.size()) return lower.peek();
            // Equal sizes mean an even count; the long cast prevents int wraparound.
            return ((long) lower.peek() + upper.peek()) / 2.0;
        }
    }

    public static void main(String[] args) {
        // Example 1 from the exercise.
        MedianFinder f = new MedianFinder();
        f.addNum(6);
        if (f.findMedian() != 6.0) throw new AssertionError("ex1a");
        f.addNum(10);
        if (f.findMedian() != 8.0) throw new AssertionError("ex1b");
        f.addNum(2);
        if (f.findMedian() != 6.0) throw new AssertionError("ex1c");
        // Example 2 from the exercise.
        MedianFinder g = new MedianFinder();
        g.addNum(3); g.addNum(3);
        if (g.findMedian() != 3.0) throw new AssertionError("ex2");
        // Random streams must match sorting every prefix.
        Random rnd = new Random(1772);
        for (int t = 0; t < 400; t++) {
            MedianFinder x = new MedianFinder();
            List<Integer> seen = new ArrayList<>();
            for (int step = 0; step < 25; step++) {
                int v = rnd.nextInt(21) - 10;
                x.addNum(v);
                seen.add(v);
                List<Integer> s = new ArrayList<>(seen);
                Collections.sort(s);
                int n = s.size();
                double expect = n % 2 == 1 ? s.get(n / 2) : ((long) s.get(n / 2 - 1) + s.get(n / 2)) / 2.0;
                if (x.findMedian() != expect) throw new AssertionError("random " + t);
            }
        }
    }
}
```

#### Solution: [Boundary] Overflow-Safe Even Median (Author exercise)
<!-- id: hp-overflow-safe-median -->

**Approach.**
The method builds the two halves from the Find Median exercise and reads the final median. For an even count, the two middle values can both be near `Integer.MAX_VALUE`. The `int` sum of such values wraps to a negative number, and halving the wrapped number gives a wrong median. The cast `(long) lower.peek()` widens the first operand before the addition, so the sum is exact in 64 bits. Division by `2.0` then produces an exact `double`, because the sum fits in 33 bits.

The invariant is that the sum is computed in `long`, so the average of two `int` values is exact.

**Complexity.**
- **Time** is O(n log n), because each of the n insertions costs O(log n) and the final read costs O(1).
- **Space** is O(n), because the queues hold every value.

```java run
import java.util.*;

public final class OverflowSafeMedian {
    /**
     * Returns the median of all values as an exact double.
     * Time: O(n log n). Space: O(n).
     * Invariant: the sum of the two middle values is computed in long.
     */
    static double median(int[] values) {
        PriorityQueue<Integer> lower = new PriorityQueue<>(Comparator.reverseOrder());
        PriorityQueue<Integer> upper = new PriorityQueue<>();
        for (int v : values) {
            if (lower.isEmpty() || v <= lower.peek()) lower.offer(v);
            else upper.offer(v);
            if (lower.size() > upper.size() + 1) upper.offer(lower.poll());
            else if (upper.size() > lower.size()) lower.offer(upper.poll());
        }
        // An odd count leaves the median at the lower root.
        if (lower.size() > upper.size()) return lower.peek();
        // The cast widens one operand before the addition, so the sum cannot wrap.
        return ((long) lower.peek() + upper.peek()) / 2.0;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (median(new int[] {2147483647, 2147483646}) != 2147483646.5) throw new AssertionError("ex1");
        if (median(new int[] {-2147483648, -2147483648}) != -2147483648.0) throw new AssertionError("ex2");
        // The int sum wraps, and the cast after the addition is too late.
        int a = Integer.MAX_VALUE, b = Integer.MAX_VALUE - 1;
        if (a + b >= 0) throw new AssertionError("the int sum wraps to a negative number");
        if ((long) (a + b) / 2.0 == 2147483646.5) throw new AssertionError("a late cast keeps the wrong value");
        // One extreme value and a single element.
        if (median(new int[] {Integer.MIN_VALUE}) != -2147483648.0) throw new AssertionError("single");
        // Random streams with extreme values must match a sorted array and exact long arithmetic.
        Random rnd = new Random(1773);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, 0, -1, 1, Integer.MAX_VALUE - 1};
        for (int t = 0; t < 400; t++) {
            int[] arr = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < arr.length; i++) arr[i] = pool[rnd.nextInt(pool.length)];
            int[] s = arr.clone();
            Arrays.sort(s);
            int n = s.length;
            double expect = n % 2 == 1 ? s[n / 2] : ((long) s[n / 2 - 1] + s[n / 2]) / 2.0;
            if (median(arr) != expect) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Sliding Window Median (LeetCode 480)
<!-- id: hp-window-median-full -->

**Approach.**
The method keeps two queues of `{value, index}` entries. The lower half has the largest value at its root, and the upper half has the smallest value at its root. Two arrays record which half holds each index and whether the entry has expired. Two counters, `lowLive` and `upLive`, count the live entries in each half. When index `i - k` leaves the window, the method marks it expired and lowers the counter of its half. It leaves the entry in the queue. Before any root is read, the method polls expired entries from the top of each queue. The rebalance loops use the live counters and not the queue sizes. After each step the method reads the roots, which are live, and builds the median from the live counters.

The invariant is that the live counters satisfy the size rule for the entries inside the window, and both roots are live whenever the method reads them.

**Complexity.**
- **Time** is O(n log n), because each entry is inserted once, moved between halves a bounded number of times, and discarded at most once.
- **Space** is O(n), because expired entries stay in the queues until they reach a root.

```java run
import java.util.*;

public final class SlidingWindowMedian {
    static int[] nums;
    static boolean[] dead, inLower;
    static int lowLive, upLive;
    static PriorityQueue<int[]> lower, upper;

    // Expired entries are removed only when they reach the root.
    static void prune(PriorityQueue<int[]> q) {
        while (!q.isEmpty() && dead[q.peek()[1]]) q.poll();
    }

    // Moves one live root across the boundary and updates the counters.
    static void move(boolean toUpper) {
        PriorityQueue<int[]> from = toUpper ? lower : upper;
        prune(from);
        int[] e = from.poll();
        if (toUpper) { upper.offer(e); inLower[e[1]] = false; lowLive--; upLive++; }
        else { lower.offer(e); inLower[e[1]] = true; upLive--; lowLive++; }
    }

    /**
     * Returns the median of each window of k values.
     * Time: O(n log n). Space: O(n).
     * Invariant: live counters follow the size rule, and both roots are live when read.
     */
    static double[] medians(int[] a, int k) {
        nums = a;
        int n = a.length;
        // Larger value first for the lower half, smaller value first for the upper half; ties by index.
        lower = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(y[0], x[0]) : Integer.compare(x[1], y[1]));
        upper = new PriorityQueue<>((x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
        dead = new boolean[n];
        inLower = new boolean[n];
        lowLive = 0;
        upLive = 0;
        double[] out = new double[n - k + 1];
        for (int i = 0; i < n; i++) {
            // The entry at index i - k has left the window: mark it and lower its half's counter.
            if (i >= k) {
                int old = i - k;
                dead[old] = true;
                if (inLower[old]) lowLive--; else upLive--;
            }
            // Roots must be live before the new value is compared with the lower root.
            prune(lower);
            prune(upper);
            if (lowLive == 0 || a[i] <= lower.peek()[0]) { lower.offer(new int[] {a[i], i}); inLower[i] = true; lowLive++; }
            else { upper.offer(new int[] {a[i], i}); inLower[i] = false; upLive++; }
            // The size rule uses live counters; a loop handles the expiry followed by an insertion.
            while (lowLive > upLive + 1) move(true);
            while (upLive > lowLive) move(false);
            prune(lower);
            prune(upper);
            if (i >= k - 1) {
                // An odd window keeps the extra value in the lower half; an even window averages two roots.
                out[i - k + 1] = lowLive > upLive ? lower.peek()[0] : ((long) lower.peek()[0] + upper.peek()[0]) / 2.0;
            }
        }
        return out;
    }

    public static void main(String[] args) {
        // Examples from the exercise.
        if (!Arrays.equals(medians(new int[] {4, 2, 12, 3, 8, 1}, 3), new double[] {4.0, 3.0, 8.0, 3.0})) throw new AssertionError("ex1");
        if (!Arrays.equals(medians(new int[] {1, 5, 2, 2}, 2), new double[] {3.0, 3.5, 2.0})) throw new AssertionError("ex2");
        // Extreme values need the long sum in an even window.
        if (!Arrays.equals(medians(new int[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, 2), new double[] {2147483647.0})) throw new AssertionError("extreme");
        // Window of one returns every value, and a window of the whole array returns one median.
        if (!Arrays.equals(medians(new int[] {7, -3, 7}, 1), new double[] {7.0, -3.0, 7.0})) throw new AssertionError("k one");
        if (!Arrays.equals(medians(new int[] {9, 1, 5}, 3), new double[] {5.0})) throw new AssertionError("k full");
        // Random arrays with many equal values must match sorting every window.
        Random rnd = new Random(1774);
        for (int t = 0; t < 500; t++) {
            int[] arr = new int[1 + rnd.nextInt(18)];
            for (int i = 0; i < arr.length; i++) arr[i] = rnd.nextInt(6) - 3;
            int k = 1 + rnd.nextInt(arr.length);
            double[] got = medians(arr, k);
            for (int s = 0; s + k <= arr.length; s++) {
                int[] w = Arrays.copyOfRange(arr, s, s + k);
                Arrays.sort(w);
                double expect = k % 2 == 1 ? w[k / 2] : ((long) w[k / 2 - 1] + w[k / 2]) / 2.0;
                if (got[s] != expect) throw new AssertionError("random " + t + " window " + s);
            }
        }
    }
}
```
