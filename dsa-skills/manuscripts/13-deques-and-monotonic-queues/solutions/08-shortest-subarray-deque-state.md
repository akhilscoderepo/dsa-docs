<!-- solutions-for: 08-shortest-subarray-deque-state -->
### Shortest-Subarray Deque State

#### Solution: [Build] Prefix-Pair Difference (Author exercise)
<!-- id: dq-prefix-pair-difference -->

**Approach.** Build a `long` array of cumulative sums with a leading zero, so that entry `j` is the sum of the first `j` numbers. A query `[l, r]` is then the entry at `r + 1` minus the entry at `l`, and each query costs one subtraction. The assertions compare with a direct loop over each query range, and show that summing in `int` wraps for values near the limit while the `long` array does not.

**Complexity.** O(n) to build the array and O(1) per query, with O(n) extra memory.

```java run
import java.util.Random;

public final class PrefixPairDifference {
    static long[] answer(int[] nums, int[][] queries) {
        long[] p = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];
        long[] out = new long[queries.length];
        for (int q = 0; q < queries.length; q++) out[q] = p[queries[q][1] + 1] - p[queries[q][0]];
        return out;
    }
    static long[] brute(int[] nums, int[][] queries) {
        long[] out = new long[queries.length];
        for (int q = 0; q < queries.length; q++)
            for (int i = queries[q][0]; i <= queries[q][1]; i++) out[q] += nums[i];
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(answer(new int[]{2, -1, 3, -4, 5}, new int[][]{{0, 2}, {1, 3}, {3, 4}}), new long[]{4, -2, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(answer(new int[]{7}, new int[][]{{0, 0}}), new long[]{7})) throw new AssertionError("example 2");
        int wrapped = Integer.MAX_VALUE + Integer.MAX_VALUE;
        if (wrapped != -2) throw new AssertionError("int addition wraps");
        if (answer(new int[]{Integer.MAX_VALUE, Integer.MAX_VALUE}, new int[][]{{0, 1}})[0] != 4294967294L) throw new AssertionError("long cumulative sums do not wrap");
        Random rnd = new Random(1311);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) == 0 ? Integer.MAX_VALUE : rnd.nextInt(21) - 10;
            int[][] qs = new int[5][2];
            for (int[] q : qs) { q[0] = rnd.nextInt(n); q[1] = q[0] + rnd.nextInt(n - q[0]); }
            if (!java.util.Arrays.equals(answer(a, qs), brute(a, qs))) throw new AssertionError("disagrees with direct sums");
        }
    }
}
```

#### Solution: [Vary] Remove Dominated Prefixes (Author exercise)
<!-- id: dq-remove-dominated-prefixes -->

**Approach.** Walk the indices in order, remove from the back every stored index whose value is not smaller than the new value, and then append the new index. Afterwards the stored values are strictly increasing, and equal values keep only the newest index. An older index with a value at least as large as a newer one is never the better start, since the newer start is closer to every later end and gives a difference that is no smaller. The assertions compare with a definition-based filter that keeps an index only if every later value is larger.

**Complexity.** Each index is stored once and removed at most once, so the time is linear.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RemoveDominatedPrefixes {
    static List<Integer> survivors(long[] p) {
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < p.length; i++) {
            while (!d.isEmpty() && p[d.peekLast()] >= p[i]) d.removeLast();
            d.addLast(i);
        }
        return new ArrayList<>(d);
    }
    static List<Integer> brute(long[] p) {
        List<Integer> out = new ArrayList<>();
        for (int i = 0; i < p.length; i++) {
            boolean keep = true;
            for (int j = i + 1; j < p.length; j++) if (p[j] <= p[i]) keep = false;
            if (keep) out.add(i);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!survivors(new long[]{0, 2, 1, 4, 4, 3}).equals(List.of(0, 2, 5))) throw new AssertionError("example 1");
        if (!survivors(new long[]{0, -1, -2}).equals(List.of(2))) throw new AssertionError("example 2");
        if (!survivors(new long[]{5, 5, 5}).equals(List.of(2))) throw new AssertionError("equal values keep the newest index only");
        Random rnd = new Random(1312);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            long[] p = new long[n];
            for (int i = 0; i < n; i++) p[i] = rnd.nextInt(7) - 3;
            List<Integer> got = survivors(p);
            if (!got.equals(brute(p))) throw new AssertionError("disagrees with the definition: " + java.util.Arrays.toString(p));
            for (int i = 1; i < got.size(); i++) if (p[got.get(i)] <= p[got.get(i - 1)]) throw new AssertionError("values must strictly increase");
        }
    }
}
```

#### Solution: [Boundary] Negative Values And Long Sums (Author exercise)
<!-- id: dq-negative-long-sums -->

**Approach.** Build `long` cumulative sums and run the two jobs at each cut point: remove from the front every start whose difference reaches the target, recording the run length and the start, and then trim the back and append. The candidate replaces the best only when it is strictly shorter, so among runs of equal length the one with the earlier end, and therefore the earlier start, is kept. Within one end the last removed front is the closest start, which gives the shortest run for that end. The assertions compare with all start and end pairs and use a target above the range of `int`.

**Complexity.** Linear time, since every cut point is added once and removed at most once, and O(n) memory.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class NegativeLongSums {
    static int[] shortest(int[] nums, long k) {
        long[] p = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int bestLen = Integer.MAX_VALUE, bestStart = -1;
        for (int b = 0; b < p.length; b++) {
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= k) {
                int s = d.removeFirst();
                if (b - s < bestLen) { bestLen = b - s; bestStart = s; }
            }
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.removeLast();
            d.addLast(b);
        }
        return bestLen == Integer.MAX_VALUE ? new int[]{-1, -1} : new int[]{bestLen, bestStart};
    }
    static int[] brute(int[] nums, long k) {
        int bestLen = Integer.MAX_VALUE, bestStart = -1;
        for (int s = 0; s < nums.length; s++) {
            long sum = 0;
            for (int e = s; e < nums.length; e++) {
                sum += nums[e];
                if (sum >= k && e - s + 1 < bestLen) { bestLen = e - s + 1; bestStart = s; }
            }
        }
        return bestLen == Integer.MAX_VALUE ? new int[]{-1, -1} : new int[]{bestLen, bestStart};
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(shortest(new int[]{4, -5, 6, -1, 7}, 12), new int[]{3, 2})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(shortest(new int[]{1000000000, 1000000000, 1000000000}, 3000000000L), new int[]{3, 0})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(shortest(new int[]{1, 2}, 4), new int[]{-1, -1})) throw new AssertionError("no qualifying run");
        Random rnd = new Random(1313);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5) == 0 ? 1000000000 : rnd.nextInt(15) - 7;
            long k = rnd.nextInt(4) == 0 ? 1000000000L + rnd.nextInt(10) : 1 + rnd.nextInt(12);
            if (!java.util.Arrays.equals(shortest(a, k), brute(a, k))) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Shortest Subarray with Sum at Least K (LeetCode 862)
<!-- id: dq-shortest-subarray-sum-k -->

**Approach.** Rewrite each run as a difference of two cumulative sums and keep candidate starts in a deque with strictly increasing cumulative values. At each cut point, remove from the front while the difference reaches `k`, taking the length each time, then remove from the back while the stored value is not smaller, and append. A window that shrinks from the left is wrong here, because removing a negative entry raises the sum. The assertions compare with every start and end pair, and a random search confirms that a shrinking window gives a wrong answer on some input with negative entries.

**Complexity.** O(n) time, because each cut point enters and leaves once, and O(n) memory for the sums.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class ShortestSubarraySumK {
    static int shortestSubarray(int[] nums, int k) {
        long[] p = new long[nums.length + 1];
        for (int i = 0; i < nums.length; i++) p[i + 1] = p[i] + nums[i];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        int best = Integer.MAX_VALUE;
        for (int b = 0; b < p.length; b++) {
            while (!d.isEmpty() && p[b] - p[d.peekFirst()] >= k) best = Math.min(best, b - d.removeFirst());
            while (!d.isEmpty() && p[d.peekLast()] >= p[b]) d.removeLast();
            d.addLast(b);
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }
    static int shrinkingWindow(int[] nums, int k) {
        int best = Integer.MAX_VALUE, left = 0;
        long sum = 0;
        for (int r = 0; r < nums.length; r++) {
            sum += nums[r];
            while (left <= r && sum >= k) { best = Math.min(best, r - left + 1); sum -= nums[left++]; }
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }
    static int brute(int[] nums, int k) {
        int best = Integer.MAX_VALUE;
        for (int s = 0; s < nums.length; s++) {
            long sum = 0;
            for (int e = s; e < nums.length; e++) {
                sum += nums[e];
                if (sum >= k) best = Math.min(best, e - s + 1);
            }
        }
        return best == Integer.MAX_VALUE ? -1 : best;
    }

    public static void main(String[] args) {
        if (shortestSubarray(new int[]{3, -2, 4, -1, 5}, 6) != 3) throw new AssertionError("example 1");
        if (shortestSubarray(new int[]{1, 2}, 4) != -1) throw new AssertionError("example 2");
        Random rnd = new Random(1314);
        boolean windowFailed = false;
        for (int t = 0; t < 6000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(13) - 6;
            int k = 1 + rnd.nextInt(10);
            int expected = brute(a, k);
            if (shortestSubarray(a, k) != expected) throw new AssertionError("disagrees with brute force on " + java.util.Arrays.toString(a) + " k=" + k);
            if (shrinkingWindow(a, k) != expected) windowFailed = true;
        }
        if (!windowFailed) throw new AssertionError("the shrinking window should fail on some input with negative entries");
    }
}
```
