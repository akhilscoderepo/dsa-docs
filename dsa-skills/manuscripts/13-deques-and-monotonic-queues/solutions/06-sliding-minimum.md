<!-- solutions-for: 06-sliding-minimum -->
### Sliding Minimum

#### Solution: [Build] Minimum Of Every K-Window (Author exercise)
<!-- id: dq-minimum-every-window -->

**Approach.** Keep indices in an `ArrayDeque` whose values never decrease from front to back. For each right edge, drop the front index if it has fallen out of the frame, drop back indices whose value is greater than the newcomer, append the newcomer, and read the front once the first frame is complete. Only the comparison in the back loop differs from the maximum version. The assertions show that the unchanged maximum comparison returns maxima on a hand-made case, and compare the minimum version with a brute-force scan of every frame.

**Complexity.** Every index enters and leaves the deque at most once, so the time is linear, and the deque never holds more than k entries.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class MinimumEveryWindow {
    static int[] slidingMinimum(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] > a[r]) d.removeLast();
            d.addLast(r);
            if (r >= k - 1) out[r - k + 1] = a[d.peekFirst()];
        }
        return out;
    }
    static int[] unflippedMaximum(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) d.removeLast();
            d.addLast(r);
            if (r >= k - 1) out[r - k + 1] = a[d.peekFirst()];
        }
        return out;
    }
    static int[] brute(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        for (int i = 0; i + k <= a.length; i++) {
            int m = Integer.MAX_VALUE;
            for (int j = i; j < i + k; j++) m = Math.min(m, a[j]);
            out[i] = m;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(slidingMinimum(new int[]{7, 4, 5, 2, 9, 4, 6}, 3), new int[]{4, 2, 2, 2, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(slidingMinimum(new int[]{4, 3, 2, 1}, 2), new int[]{3, 2, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(unflippedMaximum(new int[]{4, 1, 3, 5, 2}, 3), new int[]{4, 5, 5})) throw new AssertionError("the unchanged comparison returns maxima");
        if (!java.util.Arrays.equals(slidingMinimum(new int[]{4, 1, 3, 5, 2}, 3), new int[]{1, 1, 2})) throw new AssertionError("minimum on the hand-made case");
        Random rnd = new Random(1301);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(9) - 4;
            int k = 1 + rnd.nextInt(n);
            if (!java.util.Arrays.equals(slidingMinimum(a, k), brute(a, k))) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Window Range (Author exercise)
<!-- id: dq-window-range -->

**Approach.** Use two deques over the same indices, a non-increasing one for the largest value and a non-decreasing one for the smallest, and apply the same expiry bound to both fronts. After the newcomer is appended to both, the range of the frame is the difference of the two front values, computed after widening one operand to `long`. The assertions show that the `int` subtraction wraps for values at the ends of the `int` range, and compare the two-deque result with a brute-force scan.

**Complexity.** Each deque does amortised constant work per index, giving linear time and at most 2k stored indices.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class WindowRange {
    static long[] windowRanges(int[] a, int k) {
        long[] out = new long[a.length - k + 1];
        ArrayDeque<Integer> high = new ArrayDeque<>();
        ArrayDeque<Integer> low = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!high.isEmpty() && high.peekFirst() <= r - k) high.removeFirst();
            while (!low.isEmpty() && low.peekFirst() <= r - k) low.removeFirst();
            while (!high.isEmpty() && a[high.peekLast()] < a[r]) high.removeLast();
            while (!low.isEmpty() && a[low.peekLast()] > a[r]) low.removeLast();
            high.addLast(r);
            low.addLast(r);
            if (r >= k - 1) out[r - k + 1] = (long) a[high.peekFirst()] - a[low.peekFirst()];
        }
        return out;
    }
    static long[] brute(int[] a, int k) {
        long[] out = new long[a.length - k + 1];
        for (int i = 0; i + k <= a.length; i++) {
            long mx = Long.MIN_VALUE, mn = Long.MAX_VALUE;
            for (int j = i; j < i + k; j++) { mx = Math.max(mx, a[j]); mn = Math.min(mn, a[j]); }
            out[i] = mx - mn;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(windowRanges(new int[]{8, 2, 4, 7, 5, 3}, 3), new long[]{6, 5, 3, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(windowRanges(new int[]{5, 5, 5}, 2), new long[]{0, 0})) throw new AssertionError("example 2");
        int wrapped = Integer.MAX_VALUE - Integer.MIN_VALUE;
        if (wrapped != -1) throw new AssertionError("int subtraction wraps to " + wrapped);
        if (windowRanges(new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE}, 2)[0] != 4294967295L) throw new AssertionError("long subtraction keeps the true range");
        Random rnd = new Random(1302);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) == 0 ? (rnd.nextBoolean() ? Integer.MAX_VALUE : Integer.MIN_VALUE) : rnd.nextInt(21) - 10;
            int k = 1 + rnd.nextInt(n);
            if (!java.util.Arrays.equals(windowRanges(a, k), brute(a, k))) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Duplicate Minima Expire (Author exercise)
<!-- id: dq-duplicate-minima-expire -->

**Approach.** Keep equal values in the deque by removing from the back only values that are strictly greater than the newcomer. A second deque groups the stored indices by value, holding a pair of value and count, so equal minima form one group at the front. When an index expires, the front group loses one, and when a back index is dropped the last group loses one. The count of the front group is then the number of window positions that hold the minimum. The assertions compare the pair with a brute-force count and show that a strict comparison, which drops equal values, would report a count of one on a window of equal values.

**Complexity.** Both deques see each index once on the way in and at most once on the way out, so the work is linear.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DuplicateMinima {
    static int[][] minAndCount(int[] a, int k) {
        int[][] out = new int[a.length - k + 1][];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        ArrayDeque<int[]> groups = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) {
                d.removeFirst();
                int[] g = groups.peekFirst();
                if (--g[1] == 0) groups.removeFirst();
            }
            while (!d.isEmpty() && a[d.peekLast()] > a[r]) {
                d.removeLast();
                int[] g = groups.peekLast();
                if (--g[1] == 0) groups.removeLast();
            }
            d.addLast(r);
            if (!groups.isEmpty() && groups.peekLast()[0] == a[r]) groups.peekLast()[1]++;
            else groups.addLast(new int[]{a[r], 1});
            if (r >= k - 1) out[r - k + 1] = new int[]{a[d.peekFirst()], groups.peekFirst()[1]};
        }
        return out;
    }
    static int strictDequeSize(int[] a) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && a[d.peekLast()] >= a[r]) d.removeLast();
            d.addLast(r);
        }
        return d.size();
    }
    static int[][] brute(int[] a, int k) {
        int[][] out = new int[a.length - k + 1][];
        for (int i = 0; i + k <= a.length; i++) {
            int m = Integer.MAX_VALUE;
            for (int j = i; j < i + k; j++) m = Math.min(m, a[j]);
            int c = 0;
            for (int j = i; j < i + k; j++) if (a[j] == m) c++;
            out[i] = new int[]{m, c};
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.deepEquals(minAndCount(new int[]{3, 1, 1, 4, 1, 6}, 3), new int[][]{{1, 2}, {1, 2}, {1, 2}, {1, 1}})) throw new AssertionError("example 1");
        if (!java.util.Arrays.deepEquals(minAndCount(new int[]{5, 5, 5}, 2), new int[][]{{5, 2}, {5, 2}})) throw new AssertionError("example 2");
        if (strictDequeSize(new int[]{5, 5, 5}) != 1) throw new AssertionError("a strict comparison keeps only one equal value");
        Random rnd = new Random(1303);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(4);
            int k = 1 + rnd.nextInt(n);
            if (!java.util.Arrays.deepEquals(minAndCount(a, k), brute(a, k))) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Longest Continuous Subarray With Absolute Difference Less Than or Equal to Limit (LeetCode 1438)
<!-- id: dq-longest-limit-subarray -->

**Approach.** Every pair in a window differs by at most the limit exactly when the largest and the smallest do, so the test needs only the two extremes. Keep a maximum deque and a minimum deque, append each new index to both, and while the front values differ by more than the limit advance the left pointer by one and drop any front index that falls behind it. After the loop the window is valid, and its length is compared with the best so far. The assertions compare with a brute-force check of every subarray and with the second example, where a limit of zero forces runs of equal values.

**Complexity.** The left pointer and the right edge each move forward at most n times, so the total work is linear.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class LongestLimitSubarray {
    static int longestSubarray(int[] nums, int limit) {
        ArrayDeque<Integer> high = new ArrayDeque<>();
        ArrayDeque<Integer> low = new ArrayDeque<>();
        int left = 0, best = 0;
        for (int r = 0; r < nums.length; r++) {
            while (!high.isEmpty() && nums[high.peekLast()] < nums[r]) high.removeLast();
            while (!low.isEmpty() && nums[low.peekLast()] > nums[r]) low.removeLast();
            high.addLast(r);
            low.addLast(r);
            while ((long) nums[high.peekFirst()] - nums[low.peekFirst()] > limit) {
                left++;
                if (high.peekFirst() < left) high.removeFirst();
                if (low.peekFirst() < left) low.removeFirst();
            }
            best = Math.max(best, r - left + 1);
        }
        return best;
    }
    static int brute(int[] a, int limit) {
        int best = 0;
        for (int i = 0; i < a.length; i++) {
            int mx = a[i], mn = a[i];
            for (int j = i; j < a.length; j++) {
                mx = Math.max(mx, a[j]);
                mn = Math.min(mn, a[j]);
                if ((long) mx - mn <= limit) best = Math.max(best, j - i + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (longestSubarray(new int[]{5, 8, 6, 7, 2, 9, 4}, 3) != 4) throw new AssertionError("example 1");
        if (longestSubarray(new int[]{5, 5, 5, 6}, 0) != 3) throw new AssertionError("example 2");
        Random rnd = new Random(1304);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(9);
            int limit = rnd.nextInt(6);
            if (longestSubarray(a, limit) != brute(a, limit)) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " limit=" + limit);
        }
    }
}
```
