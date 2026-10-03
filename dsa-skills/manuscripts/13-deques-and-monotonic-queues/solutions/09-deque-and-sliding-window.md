<!-- solutions-for: 09-deque-and-sliding-window -->
### Deque And Sliding Window

#### Solution: [Build] Fixed-Window Maximum Trace (Author exercise)
<!-- id: dqw-fixed-window-trace -->

**Approach.** Run the fixed-window deque and count the removals of each pass at every edge. The expiry pass runs first and removes from the front while the front is at most `right - k`. The domination pass then removes from the back while the stored value is strictly smaller than the newcomer. The two counts are recorded separately. The assertions compare the counts with a simulation that uses a plain list and linear searches, and check that the totals are consistent: removals plus the final deque size equal the number of appends.

**Complexity.** Each position is appended once and removed at most once, so the time is linear and the deque holds at most k positions.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class FixedWindowTrace {
    static int[][] counts(int[] a, int k, int[] finalSize) {
        int[][] out = new int[a.length][2];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) { d.removeFirst(); out[r][0]++; }
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) { d.removeLast(); out[r][1]++; }
            d.addLast(r);
        }
        finalSize[0] = d.size();
        return out;
    }
    static int[][] brute(int[] a, int k) {
        int[][] out = new int[a.length][2];
        List<Integer> alive = new ArrayList<>();
        for (int r = 0; r < a.length; r++) {
            List<Integer> next = new ArrayList<>();
            for (int i : alive) {
                if (i <= r - k) out[r][0]++;
                else next.add(i);
            }
            List<Integer> kept = new ArrayList<>(next);
            int removed = 0;
            while (!kept.isEmpty() && a[kept.get(kept.size() - 1)] < a[r]) { kept.remove(kept.size() - 1); removed++; }
            out[r][1] = removed;
            kept.add(r);
            alive = kept;
        }
        return out;
    }

    public static void main(String[] args) {
        int[] size = new int[1];
        if (!java.util.Arrays.deepEquals(counts(new int[]{2, 5, 1, 1, 4}, 2, size), new int[][]{{0, 0}, {0, 1}, {0, 0}, {1, 0}, {1, 1}})) throw new AssertionError("example 1");
        if (!java.util.Arrays.deepEquals(counts(new int[]{3, 2, 1}, 3, size), new int[][]{{0, 0}, {0, 0}, {0, 0}})) throw new AssertionError("example 2");
        Random rnd = new Random(1315);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            int k = 1 + rnd.nextInt(n);
            int[][] got = counts(a, k, size);
            if (!java.util.Arrays.deepEquals(got, brute(a, k))) throw new AssertionError("disagrees with list simulation on " + java.util.Arrays.toString(a) + " k=" + k);
            int removed = 0;
            for (int[] g : got) removed += g[0] + g[1];
            if (removed + size[0] != n) throw new AssertionError("appends must equal removals plus survivors");
        }
    }
}
```

#### Solution: [Vary] Sliding Window Maximum (LeetCode 239)
<!-- id: dqw-sum-of-maxima -->

**Approach.** Use the same deque and add the front value to a `long` total whenever a window is complete. Nothing is stored per window, so the output array disappears. The total can pass the range of `int` since up to 10^5 windows each hold values near 10^9, so the accumulator must be `long`. The assertions compare with a direct sum of maxima and show that an `int` accumulator wraps on a large input.

**Complexity.** Linear time and O(k) memory.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class SumOfMaxima {
    static long sum(int[] a, int k) {
        long total = 0;
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) d.removeLast();
            d.addLast(r);
            if (r >= k - 1) total += a[d.peekFirst()];
        }
        return total;
    }
    static int sumInt(int[] a, int k) {
        int total = 0;
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && a[d.peekLast()] < a[r]) d.removeLast();
            d.addLast(r);
            if (r >= k - 1) total += a[d.peekFirst()];
        }
        return total;
    }
    static long brute(int[] a, int k) {
        long total = 0;
        for (int i = 0; i + k <= a.length; i++) {
            int m = Integer.MIN_VALUE;
            for (int j = i; j < i + k; j++) m = Math.max(m, a[j]);
            total += m;
        }
        return total;
    }

    public static void main(String[] args) {
        if (sum(new int[]{4, 2, 12, 3, 8, 1}, 3) != 44) throw new AssertionError("example 1");
        if (sum(new int[]{-5, -6}, 1) != -11) throw new AssertionError("example 2");
        int[] big = new int[10];
        java.util.Arrays.fill(big, 1000000000);
        if (sum(big, 2) != 9000000000L) throw new AssertionError("long total");
        if (sumInt(big, 2) == 9000000000L) throw new AssertionError("an int total should have wrapped");
        Random rnd = new Random(1316);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(21) - 10;
            int k = 1 + rnd.nextInt(n);
            if (sum(a, k) != brute(a, k)) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Count Of Calm Subarrays (LeetCode 1438)
<!-- id: dqw-count-calm-subarrays -->

**Approach.** Keep a maximum deque and a minimum deque and a left pointer. After the newcomer joins both deques, move the left pointer forward while the front values differ by more than the limit, and expire any front that falls behind it. Then every start from `left` to `right` gives a calm subarray ending at `right`, so add `right - left + 1`. The left pointer never moves backward, because a subarray that is too wide for one right edge stays too wide for every later one with the same start. The difference is taken in `long`, since the limit may reach two billion. The assertions compare with a count over all pairs.

**Complexity.** Linear time, because the right edge and the left pointer each advance at most n times, and O(n) memory in the worst case.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class CountCalm {
    static long count(int[] a, long limit) {
        ArrayDeque<Integer> high = new ArrayDeque<>();
        ArrayDeque<Integer> low = new ArrayDeque<>();
        long total = 0;
        int left = 0;
        for (int r = 0; r < a.length; r++) {
            while (!high.isEmpty() && a[high.peekLast()] < a[r]) high.removeLast();
            while (!low.isEmpty() && a[low.peekLast()] > a[r]) low.removeLast();
            high.addLast(r);
            low.addLast(r);
            while ((long) a[high.peekFirst()] - a[low.peekFirst()] > limit) {
                left++;
                if (high.peekFirst() < left) high.removeFirst();
                if (low.peekFirst() < left) low.removeFirst();
            }
            total += r - left + 1;
        }
        return total;
    }
    static long brute(int[] a, long limit) {
        long c = 0;
        for (int i = 0; i < a.length; i++) {
            long mx = a[i], mn = a[i];
            for (int j = i; j < a.length; j++) {
                mx = Math.max(mx, a[j]);
                mn = Math.min(mn, a[j]);
                if (mx - mn <= limit) c++;
            }
        }
        return c;
    }

    public static void main(String[] args) {
        if (count(new int[]{2, 4, 3, 7, 5}, 2) != 9) throw new AssertionError("example 1");
        if (count(new int[]{5, 5, 5}, 0) != 6) throw new AssertionError("example 2");
        if (count(new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE}, 2000000000L) != 2) throw new AssertionError("a wide pair is not calm for a limit below its spread");
        if (count(new int[]{Integer.MIN_VALUE, Integer.MAX_VALUE}, 4294967295L) != 3) throw new AssertionError("a limit equal to the spread accepts the pair");
        Random rnd = new Random(1317);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) == 0 ? (rnd.nextBoolean() ? Integer.MAX_VALUE : Integer.MIN_VALUE) : rnd.nextInt(15) - 7;
            long limit = rnd.nextInt(6) == 0 ? 4294967295L : rnd.nextInt(8);
            if (count(a, limit) != brute(a, limit)) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " limit=" + limit);
        }
    }
}
```

#### Solution: [Recognize] Shortest Subarray with Sum at Least K (LeetCode 862)
<!-- id: dqw-shortest-within-cap -->

**Approach.** Work on cumulative sums, so that a subarray is a difference of two cut points, and keep candidate starts in a deque with strictly increasing cumulative values. At each cut point, first remove from the front every start that is more than `m` positions back, since it is too old for any end from here on. Then remove starts from the front while the difference reaches `k`, taking the length each time. Then trim the back of dominated starts and append. Trimming the back is still correct under a cap, because a newer start with a value that is no larger is closer to every later end and gives a difference that is no smaller. The assertions compare with a scan limited to length `m`.

**Complexity.** Linear time, since every cut point is added once and removed at most once, and O(n) memory.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ShortestWithinCap {
    static int shortest(int[] nums, long k, int m) {
        long[] p = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int best = Integer.MAX_VALUE;
        for (int b = 0; b < p.length; b++) {
            while (!d.isEmpty() && b - d.peekFirst() > m) d.removeFirst();
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= k) best = Math.min(best, b - d.removeFirst());
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.removeLast();
            d.addLast(b);
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }
    static int brute(int[] nums, long k, int m) {
        int best = Integer.MAX_VALUE;
        for (int s = 0; s < nums.length; s++) {
            long sum = 0;
            for (int e = s; e < nums.length && e - s + 1 <= m; e++) {
                sum += nums[e];
                if (sum >= k) best = Math.min(best, e - s + 1);
            }
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    public static void main(String[] args) {
        if (shortest(new int[]{4, -3, 2, -1, 5}, 7, 5) != 5) throw new AssertionError("example 1");
        if (shortest(new int[]{4, -3, 2, -1, 5}, 7, 4) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(1318);
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(13) - 6;
            long k = 1 + rnd.nextInt(10);
            int m = 1 + rnd.nextInt(n);
            if (shortest(a, k, m) != brute(a, k, m)) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k + " m=" + m);
        }
    }
}
```
