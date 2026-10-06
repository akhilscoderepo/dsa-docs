<!-- solutions-for: 08-shortest-subarray-deque-state -->
### Solutions For The Shortest Subarray Exercises

#### Solution: [Build] Prefix-Pair Difference (Author exercise)
<!-- id: dq-prefix-pair -->

**Approach.**

The method builds the prefix array once, with `long` entries, so that each total fits. A query `(a, b)` then reads two entries and subtracts them. The invariant is that `P[i]` holds the sum of the first `i` values. The assertions compare each answer with a direct sum of the values from `a` to `b - 1`, and they cover totals above the `int` range.

**Complexity.**

- **Time** is O(n + q) for n values and q queries, because the prefix array costs n steps and each query costs one subtraction.
- **Space** is O(n) for the prefix array, plus the q answers.

```java run
import java.util.*;

public final class PrefixPair {
    /**
     * Returns the total of nums[a..b-1] for every query (a, b).
     * Time: O(n + q). Space: O(n + q). Invariant: P[i] is the sum of the first i values.
     */
    static long[] totals(int[] nums, int[][] queries) {
        long[] p = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];   // long, so the sum cannot overflow
        long[] out = new long[queries.length];
        for (int q = 0; q < queries.length; q++) out[q] = p[queries[q][1]] - p[queries[q][0]];
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(totals(new int[]{3, -2, 4, -1, 5}, new int[][]{{0, 3}, {1, 5}}), new long[]{5, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(totals(new int[]{1_000_000_000, 1_000_000_000, 1_000_000_000}, new int[][]{{0, 3}}), new long[]{3_000_000_000L})) throw new AssertionError("example 2");
        // No queries gives an empty result, and an int sum would overflow.
        if (totals(new int[]{1}, new int[0][]).length != 0) throw new AssertionError("empty queries");
        int wrapped = 1_000_000_000 + 1_000_000_000 + 1_000_000_000;
        if (wrapped == 3_000_000_000L) throw new AssertionError("the int sum wraps around");
        // Random arrays agree with a direct sum.
        Random rnd = new Random(25);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(15);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2_000_000_001) - 1_000_000_000;
            int lo = rnd.nextInt(n), hi = lo + 1 + rnd.nextInt(n - lo);
            long want = 0;
            for (int i = lo; i < hi; i++) want += a[i];
            if (totals(a, new int[][]{{lo, hi}})[0] != want) throw new AssertionError("direct sum");
        }
    }
}
```

#### Solution: [Vary] Remove Dominated Prefixes (Author exercise)
<!-- id: dq-dominated-prefixes -->

**Approach.**

A later position with a prefix sum that is not larger beats every earlier position with a larger or equal sum. Such a start gives a run that is at least as large and shorter for every end. The method pops from the back while the back sum is greater than or equal to the new sum, then appends the new position. The invariant is that the stored prefix sums strictly increase from the front to the back. The assertions compare the result with a filter that keeps a position when every later prefix sum is larger.

**Complexity.**

- **Time** is O(n), because every position takes one append and at most one pop.
- **Space** is O(n), since a strictly increasing array keeps every position.

```java run
import java.util.*;

public final class DominatedPrefixes {
    /**
     * Returns the stored positions, front to back, after all prefix sums are processed.
     * Time: O(n). Space: O(n). Invariant: stored prefix sums strictly increase toward the back.
     */
    static int[] stored(long[] p) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int b = 0; b < p.length; b++) {                          // one step per position
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.pollLast();   // a not-larger newer sum wins
            d.addLast(b);
        }
        int[] out = new int[d.size()];
        int i = 0;
        for (int x : d) out[i++] = x;
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(stored(new long[]{0, 3, 1, 5, 4, 9}), new int[]{0, 2, 4, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(stored(new long[]{5, 5, 5}), new int[]{2})) throw new AssertionError("example 2");
        // A single position stays.
        if (!Arrays.equals(stored(new long[]{7}), new int[]{0})) throw new AssertionError("single");
        // Random arrays: keep a position when every later sum is strictly larger.
        Random rnd = new Random(26);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20);
            long[] p = new long[n];
            for (int i = 0; i < n; i++) p[i] = rnd.nextInt(7) - 3;
            List<Integer> want = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                boolean kept = true;
                for (int j = i + 1; j < n; j++) if (p[j] <= p[i]) kept = false;
                if (kept) want.add(i);
            }
            if (!Arrays.equals(stored(p), want.stream().mapToInt(Integer::intValue).toArray())) throw new AssertionError(Arrays.toString(p));
        }
    }
}
```

#### Solution: [Boundary] Negative Values And Long Sums (Author exercise)
<!-- id: dq-negative-long -->

**Approach.**

The method runs two procedures and compares their results. The shrinking procedure keeps a running total in a `long` and removes the leftmost value after each success. The true procedure is the deque method on prefix sums. The invariant of the second procedure is that the stored starts have strictly increasing prefix sums and none has reached the target. The assertions check the two worked examples and then compare the true procedure with a quadratic scan on random arrays, so the comparison rests on a verified answer.

**Complexity.**

- **Time** is O(n), because both procedures make a single pass, and no position is popped twice.
- **Space** is O(n), for the prefix array and for the deque.

```java run
import java.util.*;

public final class NegativeLong {
    /** Shrinking method: correct only when extending a run never lowers its total. Time O(n). Space O(1). */
    static int shrinking(int[] nums, long target) {
        long sum = 0;
        int left = 0, best = -1;
        for (int right = 0; right < nums.length; right++) {            // grow on the right
            sum += nums[right];
            while (sum >= target) {                                    // shrink while the total reaches the target
                int len = right - left + 1;
                if (best == -1 || len < best) best = len;
                sum -= nums[left++];
            }
        }
        return best;
    }

    /** True answer with the deque of prefix positions. Time O(n). Space O(n). */
    static int truth(int[] nums, long target) {
        int n = nums.length;
        long[] p = new long[n + 1];
        for (int i = 0; i < n; i++) p[i + 1] = p[i] + nums[i];
        int best = -1;
        Deque<Integer> d = new ArrayDeque<>();
        for (int b = 0; b <= n; b++) {
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= target) {
                int len = b - d.pollFirst();                           // the start is used up
                if (best == -1 || len < best) best = len;
            }
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.pollLast();
            d.addLast(b);
        }
        return best;
    }

    /**
     * Returns true when the shrinking method disagrees with the true answer.
     * Time: O(n). Space: O(n). Invariant: truth() keeps starts with increasing prefix sums.
     */
    static boolean differs(int[] nums, long target) {
        return shrinking(nums, target) != truth(nums, target);
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!differs(new int[]{5, -4, 3, 6, -2}, 7)) throw new AssertionError("example 1");
        if (shrinking(new int[]{5, -4, 3, 6, -2}, 7) != 4 || truth(new int[]{5, -4, 3, 6, -2}, 7) != 2) throw new AssertionError("example 1 values");
        if (differs(new int[]{1_000_000_000, 1_000_000_000, 1_000_000_000}, 3_000_000_000L)) throw new AssertionError("example 2");
        // The shrinking method finds nothing here, while a run of length 3 exists.
        if (shrinking(new int[]{4, -5, 6, -1, 7}, 12) != -1 || truth(new int[]{4, -5, 6, -1, 7}, 12) != 3) throw new AssertionError("missed run");
        // Non-negative arrays never differ.
        Random rnd = new Random(27);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6);
            long target = 1 + rnd.nextInt(15);
            if (differs(a, target)) throw new AssertionError("non-negative " + Arrays.toString(a));
        }
        // The true answer agrees with a quadratic scan on arrays with negatives.
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(15);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5;
            long target = 1 + rnd.nextInt(12);
            int want = -1;
            for (int s = 0; s < n; s++) {
                long sum = 0;
                for (int e = s; e < n; e++) {
                    sum += a[e];
                    if (sum >= target && (want == -1 || e - s + 1 < want)) want = e - s + 1;
                }
            }
            if (truth(a, target) != want) throw new AssertionError("scan " + Arrays.toString(a) + " target " + target);
        }
    }
}
```

#### Solution: [Recognize] LC 862 Shortest Subarray With Sum At Least K (LeetCode 862)
<!-- id: dq-lc862 -->

**Approach.**

The method turns each run into a pair of prefix positions and looks for the pair with `P[b] - P[a] >= k` and the smallest `b - a`. The deque holds start candidates with strictly increasing prefix sums. At each end position the front loop removes starts that reach the target and records their lengths, because a used start can only give longer runs later. The back loop removes starts that a not-larger new prefix sum beats. The invariant is that no stored start has reached the target and the stored sums strictly increase. The assertions compare the answer with a quadratic scan, and they cover a target that no run reaches.

**Complexity.**

- **Time** is O(n), because each position is appended once and popped at most once from either end.
- **Space** is O(n), for the prefix array and for a deque that may hold every position.

```java run
import java.util.*;

public final class Lc862 {
    /**
     * Returns the length of the shortest non-empty subarray with sum at least k, or -1.
     * Time: O(n). Space: O(n). Invariant: stored starts have strictly increasing prefix sums and none reached k.
     */
    static int shortestSubarray(int[] nums, int k) {
        int n = nums.length;
        long[] p = new long[n + 1];
        for (int i = 0; i < n; i++) p[i + 1] = p[i] + nums[i];            // long prefix sums
        int best = -1;
        Deque<Integer> d = new ArrayDeque<>();
        for (int b = 0; b <= n; b++) {                                    // one step per end position
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= k) {        // front start reaches the target
                int len = b - d.pollFirst();                              // the start is used up
                if (best == -1 || len < best) best = len;
            }
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.pollLast(); // dominated starts leave
            d.addLast(b);                                                 // the new start enters
        }
        return best;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (shortestSubarray(new int[]{1, -2, 6, -1, 3}, 7) != 3) throw new AssertionError("example 1");
        if (shortestSubarray(new int[]{3, -1, 1}, 5) != -1) throw new AssertionError("example 2");
        // A single value that reaches the target, and an all-negative array.
        if (shortestSubarray(new int[]{9}, 9) != 1) throw new AssertionError("single");
        if (shortestSubarray(new int[]{-1, -2, -3}, 1) != -1) throw new AssertionError("negatives");
        // Random arrays agree with a quadratic scan.
        Random rnd = new Random(28);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(18), k = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(13) - 6;
            int want = -1;
            for (int s = 0; s < n; s++) {
                long sum = 0;
                for (int e = s; e < n; e++) {
                    sum += a[e];
                    if (sum >= k && (want == -1 || e - s + 1 < want)) want = e - s + 1;
                }
            }
            if (shortestSubarray(a, k) != want) throw new AssertionError(Arrays.toString(a) + " k=" + k);
        }
    }
}
```
