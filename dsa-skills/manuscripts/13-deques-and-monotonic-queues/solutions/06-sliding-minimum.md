<!-- solutions-for: 06-sliding-minimum -->
### Solutions For The Window Minimum Exercises

#### Solution: [Build] Minimum Of Every K-Window (Author exercise)
<!-- id: dq-min-windows -->

**Approach.**

The method keeps positions whose values never decrease from the front to the back, so the front is the minimum. For each new position it expires the front, removes strictly larger values from the back and appends the position. It reads the front once a full range exists. The invariant is that the front holds the range minimum at each read. The assertions compare the output with a direct scan on random arrays, and they include a strictly increasing array, which never removes from the back.

**Complexity.**

- **Time** is O(n), as each position takes part in one append and at most one removal.
- **Space** is O(k) for the deque, and the output holds n - k + 1 entries.

```java run
import java.util.*;

public final class MinWindows {
    /**
     * Returns the minimum of every range of k consecutive values.
     * Time: O(n). Space: O(k) plus the output. Invariant: the front holds the range minimum.
     */
    static int[] minWindows(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {                  // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();       // age test
            while (!d.isEmpty() && a[d.peekLast()] > a[right]) d.pollLast();     // larger values lose
            d.addLast(right);
            if (right >= k - 1) out[right - k + 1] = a[d.peekFirst()];           // read after the append
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(minWindows(new int[]{7, 4, 5, 2, 9}, 3), new int[]{4, 2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(minWindows(new int[]{9, 7, 5, 3}, 2), new int[]{7, 5, 3})) throw new AssertionError("example 2");
        // Increasing array and a range as long as the array.
        if (!Arrays.equals(minWindows(new int[]{1, 2, 3, 4}, 2), new int[]{1, 2, 3})) throw new AssertionError("increasing");
        if (!Arrays.equals(minWindows(new int[]{4, 1, 3}, 3), new int[]{1})) throw new AssertionError("k = n");
        // Random arrays agree with a direct scan.
        Random rnd = new Random(17);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(15) - 7;
            int[] got = minWindows(a, k);
            for (int s = 0; s + k <= n; s++) {
                int best = Integer.MAX_VALUE;
                for (int j = s; j < s + k; j++) best = Math.min(best, a[j]);
                if (got[s] != best) throw new AssertionError("start " + s);
            }
        }
    }
}
```

#### Solution: [Vary] Window Range (Author exercise)
<!-- id: dq-window-range -->

**Approach.**

The maximum candidates and the minimum candidates are different positions, so the method keeps two deques. Both apply the same age test, and each uses its own back comparison. The answer for a range is the front value of the maximum deque minus the front value of the minimum deque. The invariant holds for each deque separately. The assertions compare the output with a direct scan, and they check that no entry is negative.

**Complexity.**

- **Time** is O(n), because both deques receive each position one time and release it at most one time.
- **Space** is O(k) for the two deques, plus n - k + 1 output entries.

```java run
import java.util.*;

public final class WindowRange {
    /**
     * Returns max minus min for every range of k consecutive values.
     * Time: O(n). Space: O(k) plus the output. Invariant: each front holds its range extreme.
     */
    static int[] ranges(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        Deque<Integer> hi = new ArrayDeque<>(), lo = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {                  // one step per position
            if (!hi.isEmpty() && hi.peekFirst() <= right - k) hi.pollFirst();    // same age test for both
            if (!lo.isEmpty() && lo.peekFirst() <= right - k) lo.pollFirst();
            while (!hi.isEmpty() && a[hi.peekLast()] < a[right]) hi.pollLast();  // maximum candidates
            while (!lo.isEmpty() && a[lo.peekLast()] > a[right]) lo.pollLast();  // minimum candidates
            hi.addLast(right);
            lo.addLast(right);
            if (right >= k - 1) out[right - k + 1] = a[hi.peekFirst()] - a[lo.peekFirst()];
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(ranges(new int[]{7, 4, 5, 2, 9}, 3), new int[]{3, 3, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(ranges(new int[]{4, 4, 4}, 2), new int[]{0, 0})) throw new AssertionError("example 2");
        // Range length 1 gives zero everywhere.
        if (!Arrays.equals(ranges(new int[]{5, 1, 9}, 1), new int[]{0, 0, 0})) throw new AssertionError("k = 1");
        // Random arrays agree with a direct scan.
        Random rnd = new Random(18);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int[] got = ranges(a, k);
            for (int s = 0; s + k <= n; s++) {
                int mx = Integer.MIN_VALUE, mn = Integer.MAX_VALUE;
                for (int j = s; j < s + k; j++) { mx = Math.max(mx, a[j]); mn = Math.min(mn, a[j]); }
                if (got[s] != mx - mn || got[s] < 0) throw new AssertionError("start " + s);
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicate Minima Expire (Author exercise)
<!-- id: dq-duplicate-minima -->

**Approach.**

Under the replace rule, a new value equal to the back removes the older equal position. The newest copy of the minimum is then the only copy stored, and it outlasts the older copy. When the older copy would have expired, the newer copy is already in place at the front. The invariant is that the front holds the largest position among equal minima. The assertions compare the output with a scan that picks the rightmost minimum, and they include arrays with many ties.

**Complexity.**

- **Time** is O(n), because every position enters once and leaves at most one time.
- **Space** is O(k) for the deque, because the age test keeps only positions inside one range, and the output adds n - k + 1 entries.

```java run
import java.util.*;

public final class DuplicateMinima {
    /**
     * Returns the largest position that holds the minimum of each range.
     * Time: O(n). Space: O(k) plus the output.
     * Invariant: equal values keep only their newest position, so the front is the rightmost minimum.
     */
    static int[] rightmostMinima(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {                  // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();       // age test
            while (!d.isEmpty() && a[d.peekLast()] >= a[right]) d.pollLast();    // equal values are replaced too
            d.addLast(right);
            if (right >= k - 1) out[right - k + 1] = d.peekFirst();
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(rightmostMinima(new int[]{3, 1, 1, 4}, 2), new int[]{1, 2, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(rightmostMinima(new int[]{2, 2, 2}, 2), new int[]{1, 2})) throw new AssertionError("example 2");
        // A range of length 1 returns each position.
        if (!Arrays.equals(rightmostMinima(new int[]{4, 4}, 1), new int[]{0, 1})) throw new AssertionError("k = 1");
        // Random arrays with many ties agree with a scan for the rightmost minimum.
        Random rnd = new Random(19);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int[] got = rightmostMinima(a, k);
            for (int s = 0; s + k <= n; s++) {
                int best = s;
                for (int j = s; j < s + k; j++) if (a[j] <= a[best]) best = j;
                if (got[s] != best) throw new AssertionError("start " + s);
            }
        }
    }
}
```

#### Solution: [Recognize] LC 1438 Longest Continuous Subarray With Absolute Difference Less Than Or Equal To Limit (LeetCode 1438)
<!-- id: dq-lc1438 -->

**Approach.**

The range grows by one position on the right and shrinks from the left while its spread exceeds the limit. A decreasing deque supplies the maximum and an increasing deque supplies the minimum. When the spread is too large, the left pointer moves forward by one, and each deque drops its front if that position fell behind the pointer. The invariant is that after the shrinking loop the range from `left` to `right` has a spread within the limit, and the fronts are its extremes. The assertions compare the length with a quadratic scan of every range, and they cover a limit of zero.

**Complexity.**

- **Time** is O(n), because each position enters each deque once and the left pointer moves forward at most n times.
- **Space** reaches O(n) on a sorted array, because one deque then keeps every position.

```java run
import java.util.*;

public final class Lc1438 {
    /**
     * Returns the length of the longest range whose largest and smallest values differ by at most limit.
     * Time: O(n). Space: O(n). Invariant: after shrinking, spread(left..right) <= limit.
     */
    static int longestSubarray(int[] nums, int limit) {
        Deque<Integer> hi = new ArrayDeque<>(), lo = new ArrayDeque<>();
        int left = 0, best = 0;
        for (int right = 0; right < nums.length; right++) {               // grow the range on the right
            while (!hi.isEmpty() && nums[hi.peekLast()] < nums[right]) hi.pollLast();
            while (!lo.isEmpty() && nums[lo.peekLast()] > nums[right]) lo.pollLast();
            hi.addLast(right);
            lo.addLast(right);
            while (nums[hi.peekFirst()] - nums[lo.peekFirst()] > limit) {        // shrink from the left
                left++;
                if (hi.peekFirst() < left) hi.pollFirst();                // the fronts that fell behind leave
                if (lo.peekFirst() < left) lo.pollFirst();
            }
            best = Math.max(best, right - left + 1);                      // record the range length
        }
        return best;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (longestSubarray(new int[]{3, 9, 4, 5, 6, 1}, 2) != 3) throw new AssertionError("example 1");
        if (longestSubarray(new int[]{1, 5, 9}, 0) != 1) throw new AssertionError("example 2");
        // Limit zero with equal values, and a limit above every spread.
        if (longestSubarray(new int[]{8, 8, 8, 2}, 0) != 3) throw new AssertionError("equal run");
        if (longestSubarray(new int[]{1, 100, 50}, 1000) != 3) throw new AssertionError("large limit");
        // Random arrays agree with a quadratic scan.
        Random rnd = new Random(20);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(18), limit = rnd.nextInt(6);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(12);
            int want = 0;
            for (int s = 0; s < n; s++) {
                int mx = a[s], mn = a[s];
                for (int e = s; e < n; e++) {
                    mx = Math.max(mx, a[e]); mn = Math.min(mn, a[e]);
                    if (mx - mn <= limit) want = Math.max(want, e - s + 1);
                }
            }
            if (longestSubarray(a, limit) != want) throw new AssertionError(Arrays.toString(a) + " limit " + limit);
        }
    }
}
```
