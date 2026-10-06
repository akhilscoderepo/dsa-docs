<!-- solutions-for: 05-sliding-maximum -->
### Solutions For The Window Maximum Exercises

#### Solution: [Build] Maximum Of One Moving Window (Author exercise)
<!-- id: dq-one-window -->

**Approach.**

The method runs the three steps for every position and reads the front once, after the last position. The age test removes the front when it falls out of the final range. The back removes weaker values, and the append adds the newest position. The invariant is that the front always holds the position of the largest value among the last `k` processed positions. The assertions compare the result with a direct scan of the last `k` values on random arrays.

**Complexity.**

- **Time** is O(n), because the loop makes one append and at most one removal for each position.
- **Space** is O(k), since the deque holds only positions from the current range.

```java run
import java.util.*;

public final class OneWindow {
    /**
     * Returns the maximum of the last k values using the window deque.
     * Time: O(n). Space: O(k).
     * Invariant: the front is the position of the maximum among the last k processed positions.
     */
    static int lastWindowMax(int[] a, int k) {
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {              // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();   // the front left the range
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.pollLast(); // weaker values lose
            d.addLast(right);                                         // the newest position enters
        }
        return a[d.peekFirst()];                                      // read last, after the final append
    }

    public static void main(String[] args) {
        // Worked examples.
        if (lastWindowMax(new int[]{8, 3, 5, 9, 2, 7}, 3) != 9) throw new AssertionError("example 1");
        if (lastWindowMax(new int[]{4, 6}, 1) != 6) throw new AssertionError("example 2");
        // A range as long as the array.
        if (lastWindowMax(new int[]{3, 9, 1}, 3) != 9) throw new AssertionError("full range");
        // Random arrays agree with a direct scan.
        Random rnd = new Random(13);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            int best = Integer.MIN_VALUE;
            for (int i = n - k; i < n; i++) best = Math.max(best, a[i]);
            if (lastWindowMax(a, k) != best) throw new AssertionError("scan " + Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Return Maximum Indices (Author exercise)
<!-- id: dq-max-indices -->

**Approach.**

The deque already stores positions, so the answer for a range is the front itself, with no array read. Equal values stay in the deque, so the front is the oldest position that holds the maximum. The invariant is the same as for the value version. The assertions compare each returned position with the leftmost position of the maximum in a direct scan.

**Complexity.**

- **Time** is O(n), as each position goes in one time and comes out at most one time.
- **Space** is O(k) for the deque, plus the output array.

```java run
import java.util.*;

public final class MaxIndices {
    /**
     * Returns, for each full range, the leftmost position that holds the range maximum.
     * Time: O(n). Space: O(k) plus the output. Invariant: the front holds the leftmost maximum position.
     */
    static int[] maxPositions(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {              // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();   // expire the front
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) d.pollLast(); // strictly weaker values leave; equal values stay
            d.addLast(right);
            if (right >= k - 1) out[right - k + 1] = d.peekFirst();   // the stored position is the answer
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(maxPositions(new int[]{2, 9, 4, 4, 1, 6}, 2), new int[]{1, 1, 2, 3, 5})) throw new AssertionError("example 1");
        if (!Arrays.equals(maxPositions(new int[]{7, 7, 7}, 2), new int[]{0, 1})) throw new AssertionError("example 2");
        // Range length 1 returns every position.
        if (!Arrays.equals(maxPositions(new int[]{5, 1, 5}, 1), new int[]{0, 1, 2})) throw new AssertionError("k = 1");
        // Random arrays agree with a scan for the leftmost maximum.
        Random rnd = new Random(14);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            int[] got = maxPositions(a, k);
            for (int s = 0; s + k <= n; s++) {
                int best = s;
                for (int j = s; j < s + k; j++) if (a[j] > a[best]) best = j;
                if (got[s] != best) throw new AssertionError("start " + s);
            }
        }
    }
}
```

#### Solution: [Boundary] Increasing, Decreasing, And Equal Arrays (Author exercise)
<!-- id: dq-three-shapes -->

**Approach.**

The method runs the full update and counts the removals at each end. In an increasing array each new value removes everything at the back, so the back count is large and the front count is zero. In a decreasing array nothing leaves from the back, and the front loses one position per step after the range fills. Equal values stay under the strict rule, so an equal array behaves like a decreasing one. The invariant is that every removal is counted once. The assertions check the three shapes with exact counts and check that the two counts together never exceed the number of appends.

**Complexity.**

- **Time** is O(n), because every position is appended once and leaves at most once.
- **Space** is O(k), since the deque holds at most `k` positions.

```java run
import java.util.*;

public final class ThreeShapes {
    /**
     * Returns {back removals, front removals} for the whole run.
     * Time: O(n). Space: O(k). Invariant: each position is counted at most once, at the end that removes it.
     */
    static int[] removals(int[] a, int k) {
        int back = 0, front = 0;
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < a.length; right++) {                   // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) { d.pollFirst(); front++; }
            while (!d.isEmpty() && a[d.peekLast()] < a[right]) { d.pollLast(); back++; }
            d.addLast(right);
        }
        return new int[]{back, front};
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(removals(new int[]{1, 2, 3, 4}, 2), new int[]{3, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(removals(new int[]{4, 3, 2, 1}, 2), new int[]{0, 2})) throw new AssertionError("example 2");
        // Equal values behave like a decreasing array.
        if (!Arrays.equals(removals(new int[]{5, 5, 5, 5}, 2), new int[]{0, 2})) throw new AssertionError("equal");
        // Random arrays: removals never exceed appends.
        Random rnd = new Random(15);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(20), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            int[] r = removals(a, k);
            if (r[0] + r[1] > n) throw new AssertionError("more removals than appends");
        }
    }
}
```

#### Solution: [Recognize] LC 239 Sliding Window Maximum (LeetCode 239)
<!-- id: dq-lc239 -->

**Approach.**

Each range of length `k` needs its maximum, and the ranges shift by one position. The window deque holds the in-range positions that no later in-range position dominates. For each new position the method expires the front, removes weaker values from the back, appends and reads the front once a full range exists. The invariant is that the front is the range maximum at every read. The assertions compare the output with a direct scan on random arrays, and they cover a range of length 1, a range as long as the array and equal values.

**Complexity.**

- **Time** is O(n), since the number of removals cannot exceed the number of appends.
- **Space** is O(k) for the deque, plus O(n - k + 1) for the output.

```java run
import java.util.*;

public final class Lc239 {
    /**
     * Returns the maximum of every range of k consecutive values.
     * Time: O(n). Space: O(k) plus the output. Invariant: the front is the maximum of the current range.
     */
    static int[] maxSlidingWindow(int[] nums, int k) {
        int[] out = new int[nums.length - k + 1];
        Deque<Integer> d = new ArrayDeque<>();
        for (int right = 0; right < nums.length; right++) {            // one step per position
            if (!d.isEmpty() && d.peekFirst() <= right - k) d.pollFirst();     // step 1: age test
            while (!d.isEmpty() && nums[d.peekLast()] < nums[right]) d.pollLast(); // step 2: weaker values leave
            d.addLast(right);                                          // step 3: append
            if (right >= k - 1) out[right - k + 1] = nums[d.peekFirst()];      // read after the append
        }
        return out;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(maxSlidingWindow(new int[]{2, 9, 4, 4, 1, 6}, 2), new int[]{9, 9, 4, 4, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(maxSlidingWindow(new int[]{5, 1, 1, 1, 3}, 3), new int[]{5, 1, 3})) throw new AssertionError("example 2");
        // Hostile shapes: k = 1, k = n, equal values.
        if (!Arrays.equals(maxSlidingWindow(new int[]{3, 1, 2}, 1), new int[]{3, 1, 2})) throw new AssertionError("k = 1");
        if (!Arrays.equals(maxSlidingWindow(new int[]{3, 1, 2}, 3), new int[]{3})) throw new AssertionError("k = n");
        if (!Arrays.equals(maxSlidingWindow(new int[]{7, 7, 7, 2}, 2), new int[]{7, 7, 7})) throw new AssertionError("equal");
        // Random arrays agree with a direct scan.
        Random rnd = new Random(16);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(25), k = 1 + rnd.nextInt(n);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int[] got = maxSlidingWindow(a, k);
            for (int s = 0; s + k <= n; s++) {
                int best = Integer.MIN_VALUE;
                for (int j = s; j < s + k; j++) best = Math.max(best, a[j]);
                if (got[s] != best) throw new AssertionError("start " + s);
            }
        }
    }
}
```
