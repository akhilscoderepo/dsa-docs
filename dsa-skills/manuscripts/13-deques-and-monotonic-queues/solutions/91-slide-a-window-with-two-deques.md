<!-- solutions-for: 91-slide-a-window-with-two-deques -->
### Solutions For The Two-Deque Window Exercises

#### Solution: [Build] Fixed-Window Maximum Trace (Author exercise)
<!-- id: dq-fixed-window-trace -->

**Approach.**

The method runs the fixed-window update and copies the deque after every append. The front pass removes positions that left the range, and the back pass removes strictly smaller values. A copy after the append shows the result of both passes together. The invariant is that every state holds positions in increasing order with values that never increase. The assertions check the two worked examples, then compare each state with a direct definition: the positions in the range that no later position in the range strictly beats.

**Complexity.**

- **Time** is O(n * k) for the copies, because each state holds up to `k` positions, while the deque updates alone cost O(n).
- **Space** is O(n * k) for the recorded states, plus O(k) for the deque.

```java run
import java.util.*;

public final class FixedWindowTrace {
    /**
     * Returns the deque contents after every position.
     * Time: O(n * k) because of the copies. Space: O(n * k). Invariant: values never increase toward the back.
     */
    static int[][] states(int[] a, int k) {
        int[][] out = new int[a.length][];
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {                    // one step per position
            while (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();      // front pass: expiry
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.pollLast();       // back pass: domination
            d.addLast(right);
            out[right] = d.stream().mapToInt(Integer::intValue).toArray();         // copy the state
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.deepEquals(states(new int[]{6, 1, 4, 4, 2}, 3), new int[][]{{0}, {0, 1}, {0, 2}, {2, 3}, {2, 3, 4}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(states(new int[]{3, 2, 1}, 1), new int[][]{{0}, {1}, {2}})) throw new AssertionError("example 2");
        // Random arrays agree with the direct definition of each state.
        Random rnd = new Random(29);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            int[][] got = states(a, k);
            for (int r = 0; r < n; r++) {
                List<Integer> want = new ArrayList<>();
                for (int i = Math.max(0, r - k + 1); i <= r; i++) {
                    boolean beaten = false;
                    for (int j = i + 1; j <= r; j++) if (a[j] > a[i]) beaten = true;
                    if (!beaten) want.add(i);
                }
                if (!Arrays.equals(got[r], want.stream().mapToInt(Integer::intValue).toArray())) throw new AssertionError("state " + r);
            }
        }
    }
}
```

#### Solution: [Vary] Smallest Window Maximum (Author exercise)
<!-- id: dq-smallest-window-max -->

**Approach.**

The deque method reads the maximum of each full range. The method keeps the smallest value it has read so far. Only the output contract changes from the window maximum of LC 239, since the deque update stays the same. The invariant is that, after each full range, the running minimum equals the smallest range maximum seen so far. The assertions compare the answer with a quadratic scan of every range.

**Complexity.**

- **Time** is O(n), because each position enters once and the two loops pop it at most once in total.
- **Space** is O(k), since the deque holds only positions from one range.

```java run
import java.util.*;

public final class SmallestWindowMax {
    /**
     * Returns the smallest of the maxima of all ranges of k consecutive values.
     * Time: O(n). Space: O(k). Invariant: best is the smallest range maximum read so far.
     */
    static int smallestMax(int[] a, int k) {
        Deque<Integer> d = new ArrayDeque<>();
        int best = Integer.MAX_VALUE;
        for (int right = 0; right < a.length; right++) {                    // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.pollLast();
            d.addLast(right);
            if (right >= k - 1) best = Math.min(best, a[d.peekFirst()]);    // read the range maximum
        }
        return best;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (smallestMax(new int[]{8, 2, 7, 3, 5, 1}, 2) != 5) throw new AssertionError("example 1");
        if (smallestMax(new int[]{4, 4, 4}, 3) != 4) throw new AssertionError("example 2");
        // Range length 1 gives the minimum of the array.
        if (smallestMax(new int[]{5, 2, 9}, 1) != 2) throw new AssertionError("k = 1");
        // Random arrays agree with a quadratic scan.
        Random rnd = new Random(30);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int want = Integer.MAX_VALUE;
            for (int s = 0; s + k <= n; s++) {
                int mx = Integer.MIN_VALUE;
                for (int j = s; j < s + k; j++) mx = Math.max(mx, a[j]);
                want = Math.min(want, mx);
            }
            if (smallestMax(a, k) != want) throw new AssertionError(Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Count Steady Stretches (Author exercise)
<!-- id: dq-count-steady -->

**Approach.**

Every subarray of a steady window is steady, because its largest value is not higher and its smallest value is not lower. For each right end, the method moves the left pointer until the window is steady, and it then adds `right - left + 1` to the total. The two deques supply the extremes in constant time. The invariant after the pointer settles is that the window is the longest steady stretch that ends at `right`. The assertions compare the total with a quadratic count, and they check a case whose count exceeds the `int` range.

**Complexity.**

- **Time** is O(n), as the two deques receive every position once and the left pointer never steps back.
- **Space** is O(n) in the worst case, which a steady sorted array reaches.

```java run
import java.util.*;

public final class CountSteady {
    /**
     * Returns the number of subarrays whose largest minus smallest value is at most limit.
     * Time: O(n). Space: O(n). Invariant: after settling, a[left..right] is the longest steady stretch ending at right.
     */
    static long count(int[] a, int limit) {
        Deque<Integer> hi = new ArrayDeque<>(), lo = new ArrayDeque<>();
        int left = 0;
        long total = 0;
        for (int right = 0; right < a.length; right++) {                    // one step per right end
            while (!hi.isEmpty() && a[hi.peekLast()] < a[right]) hi.pollLast();
            while (!lo.isEmpty() && a[lo.peekLast()] > a[right]) lo.pollLast();
            hi.addLast(right);
            lo.addLast(right);
            while (a[hi.peekFirst()] - a[lo.peekFirst()] > limit) {         // the spread is too large
                left++;
                if (hi.peekFirst() < left) hi.pollFirst();
                if (lo.peekFirst() < left) lo.pollFirst();
            }
            total += right - left + 1;                                      // every stretch ending here counts
        }
        return total;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (count(new int[]{1, 3, 2}, 1) != 4) throw new AssertionError("example 1");
        if (count(new int[]{5, 5, 5}, 0) != 6) throw new AssertionError("example 2");
        // A steady array of 100,000 values needs a long counter.
        int[] flat = new int[100_000];
        long want = 100_000L * 100_001L / 2;
        if (count(flat, 0) != want || want <= Integer.MAX_VALUE) throw new AssertionError("long count");
        // Random arrays agree with a quadratic count.
        Random rnd = new Random(31);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(18), limit = rnd.nextInt(5);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(10);
            long expected = 0;
            for (int s = 0; s < n; s++) {
                int mx = a[s], mn = a[s];
                for (int e = s; e < n; e++) {
                    mx = Math.max(mx, a[e]); mn = Math.min(mn, a[e]);
                    if (mx - mn <= limit) expected++;
                }
            }
            if (count(a, limit) != expected) throw new AssertionError(Arrays.toString(a) + " limit " + limit);
        }
    }
}
```

#### Solution: [Recognize] Shortest Subarray With Its Start (Author exercise)
<!-- id: dq-shortest-with-start -->

**Approach.**

The method uses prefix positions as the moving candidates, because the array holds negative values and a plain window cannot decide when to shrink. The front loop removes starts that reach the target and records the length and the start of the shortest run. The strict comparison keeps the earliest end for each length, so equal lengths keep the smallest start. The back loop removes starts that a not-larger prefix sum beats. The invariant is that stored starts have strictly increasing prefix sums and none has reached the target. The assertions compare the pair with a quadratic scan that scans starts in order.

**Complexity.**

- **Time** is O(n), because the two loops together pop each prefix position at most once.
- **Space** is O(n), for the prefix array and the deque.

```java run
import java.util.*;

public final class ShortestWithStart {
    /**
     * Returns {start, length} of the shortest subarray with sum at least k, smallest start on ties, or {-1, -1}.
     * Time: O(n). Space: O(n). Invariant: stored starts have increasing prefix sums and none reached k.
     */
    static int[] shortest(int[] nums, int k) {
        int n = nums.length;
        long[] p = new long[n + 1];
        for (int i = 0; i < n; i++) p[i + 1] = p[i] + nums[i];              // long prefix sums
        int bestLen = -1, bestStart = -1;
        Deque<Integer> d = new ArrayDeque<>();
        for (int b = 0; b <= n; b++) {                                      // one step per end position
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= k) {
                int start = d.pollFirst();                                  // the start is used up
                int len = b - start;
                if (bestLen == -1 || len < bestLen) { bestLen = len; bestStart = start; }
            }
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.pollLast();   // dominated starts leave
            d.addLast(b);
        }
        return new int[]{bestStart, bestLen};
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(shortest(new int[]{2, -3, 4, 1, -2, 5}, 6), new int[]{2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(shortest(new int[]{2, -2, 2}, 3), new int[]{-1, -1})) throw new AssertionError("example 2");
        // A single qualifying value.
        if (!Arrays.equals(shortest(new int[]{1, 9}, 9), new int[]{1, 1})) throw new AssertionError("single value");
        // Random arrays agree with a quadratic scan, including the tie rule.
        Random rnd = new Random(32);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16), k = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5;
            int wl = -1, ws = -1;
            for (int s = 0; s < n; s++) {
                long sum = 0;
                for (int e = s; e < n; e++) {
                    sum += a[e];
                    if (sum >= k && (wl == -1 || e - s + 1 < wl)) { wl = e - s + 1; ws = s; }
                }
            }
            if (!Arrays.equals(shortest(a, k), new int[]{ws, wl})) throw new AssertionError(Arrays.toString(a) + " k=" + k);
        }
    }
}
```
