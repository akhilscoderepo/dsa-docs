<!-- solutions-for: 07-index-expiry -->
### Index Expiry

#### Solution: [Build] Best Of Last K Scores (Author exercise)
<!-- id: dq-best-of-last-k -->

**Approach.** Keep positions in a deque whose scores fall from front to back. At each position, first remove front positions below `i - k`, then read the front as the answer, since the current position may not answer for itself, and only then remove weaker positions from the back and append the current one. An empty deque gives -1. The assertions compare with a rescan of the previous `k` positions on random arrays that contain many ties, and show that appending before reading would let a position see its own score.

**Complexity.** Each position is appended once and removed at most once, so the run is linear and the deque holds at most k positions.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class BestOfLastK {
    static int[] bonus(int[] score, int k) {
        int[] out = new int[score.length];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < score.length; i++) {
            while (!d.isEmpty() && d.peekFirst() < i - k) d.removeFirst();
            out[i] = d.isEmpty() ? -1 : score[d.peekFirst()];
            while (!d.isEmpty() && score[d.peekLast()] < score[i]) d.removeLast();
            d.addLast(i);
        }
        return out;
    }
    static int[] appendFirst(int[] score, int k) {
        int[] out = new int[score.length];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < score.length; i++) {
            while (!d.isEmpty() && score[d.peekLast()] < score[i]) d.removeLast();
            d.addLast(i);
            while (!d.isEmpty() && d.peekFirst() < i - k) d.removeFirst();
            out[i] = score[d.peekFirst()];
        }
        return out;
    }
    static int[] brute(int[] score, int k) {
        int[] out = new int[score.length];
        for (int i = 0; i < score.length; i++) {
            int best = -1;
            for (int j = Math.max(0, i - k); j < i; j++) best = Math.max(best, score[j]);
            out[i] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(bonus(new int[]{5, 3, 6, 2, 4, 1, 7}, 3), new int[]{-1, 5, 5, 6, 6, 6, 4})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(bonus(new int[]{2, 2, 2}, 1), new int[]{-1, 2, 2})) throw new AssertionError("example 2");
        if (appendFirst(new int[]{1, 9}, 1)[1] != 9) throw new AssertionError("appending first lets a position see itself");
        Random rnd = new Random(1307);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            int k = 1 + rnd.nextInt(n);
            if (!java.util.Arrays.equals(bonus(a, k), brute(a, k))) throw new AssertionError("disagrees with rescan on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Variable Legal Left Bound (Author exercise)
<!-- id: dq-variable-left-bound -->

**Approach.** Replace the constant lookback by the entry of `low` for the current position. The current position is part of its own window here, so it is appended first, and the front is then removed while it lies below `low[i]`. Because `low[i] <= i` the just-appended position is never removed, so the deque is never empty at the read. The assertions compare with a scan over positions `low[i]` through `i`, and show that a boundary array that moves left can bring back a position that was already discarded.

**Complexity.** Positions enter once and leave once, so the time is linear, and the deque is bounded by the largest window.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class VariableLeftBound {
    static int[] boundedMax(int[] a, int[] low) {
        int[] out = new int[a.length];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int i = 0; i < a.length; i++) {
            while (!d.isEmpty() && a[d.peekLast()] < a[i]) d.removeLast();
            d.addLast(i);
            while (d.peekFirst() < low[i]) d.removeFirst();
            out[i] = a[d.peekFirst()];
        }
        return out;
    }
    static int[] brute(int[] a, int[] low) {
        int[] out = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            int best = Integer.MIN_VALUE;
            for (int j = low[i]; j <= i; j++) best = Math.max(best, a[j]);
            out[i] = best;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(boundedMax(new int[]{6, 2, 8, 3, 5, 4}, new int[]{0, 0, 1, 2, 2, 4}), new int[]{6, 6, 8, 8, 8, 5})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(boundedMax(new int[]{7, 7, 7}, new int[]{0, 1, 2}), new int[]{7, 7, 7})) throw new AssertionError("example 2");
        int[] movesLeft = boundedMax(new int[]{9, 1, 2}, new int[]{0, 1, 0});
        if (movesLeft[2] == 9) throw new AssertionError("a discarded position should not return in this implementation");
        if (brute(new int[]{9, 1, 2}, new int[]{0, 1, 0})[2] != 9) throw new AssertionError("the true answer for a left-moving bound is 9");
        Random rnd = new Random(1308);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            int[] low = new int[n];
            int cur = 0;
            for (int i = 0; i < n; i++) {
                a[i] = rnd.nextInt(11) - 5;
                cur = Math.min(i, cur + (rnd.nextInt(3) == 0 ? rnd.nextInt(3) : 0));
                low[i] = cur;
            }
            if (!java.util.Arrays.equals(boundedMax(a, low), brute(a, low))) throw new AssertionError("disagrees with scan on " + java.util.Arrays.toString(a) + " low=" + java.util.Arrays.toString(low));
        }
    }
}
```

#### Solution: [Boundary] Duplicate Values, Different Ages (Author exercise)
<!-- id: dq-duplicate-ages -->

**Approach.** Remove from the back only values that are strictly smaller than the newcomer, so equal values stay behind each other in age order. Expire the front by position with the test `front <= right - k`. The front is then the oldest position holding the largest value in the window, and that is what the contract asks for. The assertions compare with a scan that picks the first maximum, and show that a non-strict back removal returns the newest tied position instead.

**Complexity.** Every position enters and leaves once, so the time is linear and the extra memory is at most k positions.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class DuplicateAges {
    static int[] oldestMaxPositions(int[] a, int k, boolean strict) {
        int[] out = new int[a.length - k + 1];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        for (int r = 0; r < a.length; r++) {
            while (!d.isEmpty() && d.peekFirst() <= r - k) d.removeFirst();
            while (!d.isEmpty() && (strict ? a[d.peekLast()] < a[r] : a[d.peekLast()] <= a[r])) d.removeLast();
            d.addLast(r);
            if (r >= k - 1) out[r - k + 1] = d.peekFirst();
        }
        return out;
    }
    static int[] brute(int[] a, int k) {
        int[] out = new int[a.length - k + 1];
        for (int i = 0; i + k <= a.length; i++) {
            int pos = i;
            for (int j = i; j < i + k; j++) if (a[j] > a[pos]) pos = j;
            out[i] = pos;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!java.util.Arrays.equals(oldestMaxPositions(new int[]{4, 4, 2, 4}, 2, true), new int[]{0, 1, 3})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(oldestMaxPositions(new int[]{3, 3, 3}, 2, true), new int[]{0, 1})) throw new AssertionError("example 2");
        if (!java.util.Arrays.equals(oldestMaxPositions(new int[]{3, 3, 3}, 2, false), new int[]{1, 2})) throw new AssertionError("non-strict removal reports the newest tied position");
        Random rnd = new Random(1309);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(3);
            int k = 1 + rnd.nextInt(n);
            if (!java.util.Arrays.equals(oldestMaxPositions(a, k, true), brute(a, k))) throw new AssertionError("disagrees with scan on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Jump Game VI (LeetCode 1696)
<!-- id: dq-jump-game-six -->

**Approach.** The best score at index `i` is `nums[i]` plus the best score among indices `i-k` through `i-1`, which is a lookback maximum over computed values. Keep a deque of indices ordered by their computed scores, expire the front below `i - k`, use the front score, then remove back indices whose score is not larger and append `i`. The assertions compare with the quadratic recurrence on random arrays, including all-negative ones where the best path takes few jumps.

**Complexity.** Linear time, because each index is added once and removed at most once, and O(n) memory for the scores.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class JumpGameSix {
    static long best(int[] nums, int k) {
        long[] score = new long[nums.length];
        ArrayDeque<Integer> d = new ArrayDeque<>();
        score[0] = nums[0];
        d.addLast(0);
        for (int i = 1; i < nums.length; i++) {
            while (d.peekFirst() < i - k) d.removeFirst();
            score[i] = nums[i] + score[d.peekFirst()];
            while (!d.isEmpty() && score[d.peekLast()] <= score[i]) d.removeLast();
            d.addLast(i);
        }
        return score[nums.length - 1];
    }
    static long brute(int[] nums, int k) {
        long[] dp = new long[nums.length];
        dp[0] = nums[0];
        for (int i = 1; i < nums.length; i++) {
            long m = Long.MIN_VALUE;
            for (int j = Math.max(0, i - k); j < i; j++) m = Math.max(m, dp[j]);
            dp[i] = nums[i] + m;
        }
        return dp[nums.length - 1];
    }

    public static void main(String[] args) {
        if (best(new int[]{3, -2, 4, -1, 2, -5, 6}, 3) != 15) throw new AssertionError("example 1");
        if (best(new int[]{-4, -3, -5}, 1) != -12) throw new AssertionError("example 2");
        Random rnd = new Random(1310);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            int bias = rnd.nextInt(3);
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(11) - 5 - (bias == 0 ? 6 : 0);
            int k = 1 + rnd.nextInt(n);
            if (best(a, k) != brute(a, k)) throw new AssertionError("disagrees with the recurrence on " + java.util.Arrays.toString(a) + " k=" + k);
        }
    }
}
```
