<!-- solutions-for: 08-stack-and-contribution-counting -->
### Stack And Contribution Counting

#### Solution: [Build] Next Greater By Position (LeetCode 496)
<!-- id: ms-combo-next-greater-by-position -->

**Approach.** Run the ordered stack over the whole array and write each resolved value into an array indexed by position, not into a map keyed by value. The queries then read `answer[p]`. A value-keyed map breaks when values repeat, because two positions with the same value can have different next greater values, and the later `put` overwrites the earlier one. The assertions show that failure on `[3, 5, 3, 2, 4]`, check the examples, and compare the positional answers with a forward walk on random arrays with many repeated values.

**Complexity.** O(n + q) time for `n` reference values and `q` queries, and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Random;

public final class NextGreaterByPosition {
    static int[] byPosition(int[] reference, int[] positions) {
        int n = reference.length;
        int[] answer = new int[n];
        Arrays.fill(answer, -1);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && reference[j] > reference[stack.peekLast()]) answer[stack.removeLast()] = reference[j];
            stack.addLast(j);
        }
        int[] out = new int[positions.length];
        for (int i = 0; i < positions.length; i++) out[i] = answer[positions[i]];
        return out;
    }
    static int[] valueKeyed(int[] reference, int[] positions) {
        HashMap<Integer, Integer> next = new HashMap<>();
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < reference.length; j++) {
            while (!stack.isEmpty() && reference[j] > reference[stack.peekLast()]) next.put(reference[stack.removeLast()], reference[j]);
            stack.addLast(j);
        }
        int[] out = new int[positions.length];
        for (int i = 0; i < positions.length; i++) out[i] = next.getOrDefault(reference[positions[i]], -1);
        return out;
    }
    static int[] oracle(int[] reference, int[] positions) {
        int[] out = new int[positions.length];
        for (int i = 0; i < positions.length; i++) {
            out[i] = -1;
            for (int j = positions[i] + 1; j < reference.length; j++) if (reference[j] > reference[positions[i]]) { out[i] = reference[j]; break; }
        }
        return out;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(byPosition(new int[]{3, 1, 3, 2, 4}, new int[]{1, 0, 3}), new int[]{3, 4, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(byPosition(new int[]{2, 2, 2}, new int[]{0, 2}), new int[]{-1, -1})) throw new AssertionError("example 2");
        int[] dup = {3, 5, 3, 2, 4};
        if (Arrays.equals(valueKeyed(dup, new int[]{0}), oracle(dup, new int[]{0}))) throw new AssertionError("a value-keyed map should fail on repeated values");
        if (!Arrays.equals(byPosition(dup, new int[]{0}), oracle(dup, new int[]{0}))) throw new AssertionError("the positional answer must be right");
        Random rnd = new Random(1801);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] ref = new int[n];
            for (int i = 0; i < n; i++) ref[i] = rnd.nextInt(5);
            int[] pos = new int[1 + rnd.nextInt(n)];
            for (int i = 0; i < pos.length; i++) pos[i] = rnd.nextInt(n);
            if (!Arrays.equals(byPosition(ref, pos), oracle(ref, pos))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(ref));
        }
    }
}
```

#### Solution: [Vary] Wait Totals From Resolving Positions (LeetCode 739)
<!-- id: ms-combo-wait-totals -->

**Approach.** When a reading removes a waiting day from the stack, the distance `j - top` is that day's wait, so fold it into a running sum and a running maximum right there, without storing the waits. Days that are never removed have wait 0 and add nothing to either aggregate. The sum is kept in `long` for safety. The assertions check the examples and compare the two aggregates with the waits computed by a forward walk on random readings.

**Complexity.** O(n) time and O(n) extra space for the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class WaitTotals {
    static long[] waitTotals(int[] temps) {
        long sum = 0, longest = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < temps.length; j++) {
            while (!stack.isEmpty() && temps[j] > temps[stack.peekLast()]) {
                int wait = j - stack.removeLast();
                sum += wait;
                longest = Math.max(longest, wait);
            }
            stack.addLast(j);
        }
        return new long[]{sum, longest};
    }
    static long[] oracle(int[] t) {
        long sum = 0, longest = 0;
        for (int i = 0; i < t.length; i++)
            for (int j = i + 1; j < t.length; j++)
                if (t[j] > t[i]) { sum += j - i; longest = Math.max(longest, j - i); break; }
        return new long[]{sum, longest};
    }

    public static void main(String[] args) {
        if (!Arrays.equals(waitTotals(new int[]{66, 70, 68, 68, 75, 64, 72}), new long[]{8, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(waitTotals(new int[]{80, 70, 60}), new long[]{0, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1802);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 30 + rnd.nextInt(7);
            if (!Arrays.equals(waitTotals(a), oracle(a))) throw new AssertionError("disagrees with the forward walk on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Best Rectangle With Its Span (LeetCode 84)
<!-- id: ms-combo-best-rectangle-span -->

**Approach.** Use the pop-time width and the closing zero. When bar `t` is removed at `j` with left wall `left`, it limits a rectangle that covers indices `left + 1` through `j - 1`, so the candidate is `[h[t] * (j - left - 1), left + 1, j - 1]`. The best candidate is updated when its area is larger, or when it is equal and its start is smaller, or equal start and smaller end. A zero-height bar is never a useful candidate, because the problem guarantees a positive bar. Two equal bars give two candidates, a narrower one for the later bar and a full one for the earlier bar, and the narrower one has a strictly smaller area, so it never wins a tie. The assertions check the examples and compare with a brute force that tries every run and applies the same tie rule.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class BestRectangleSpan {
    static long[] best(int[] h) {
        int n = h.length;
        long[] best = {0, -1, -1};
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            int current = (j == n) ? 0 : h[j];
            while (!stack.isEmpty() && h[stack.peekLast()] > current) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                long area = (long) h[t] * (j - left - 1);
                long start = left + 1, end = j - 1;
                boolean better = area > best[0]
                        || (area == best[0] && (start < best[1] || (start == best[1] && end < best[2])));
                if (better) { best[0] = area; best[1] = start; best[2] = end; }
            }
            if (j < n) stack.addLast(j);
        }
        return best;
    }
    static long[] oracle(int[] h) {
        long[] best = {0, -1, -1};
        for (int s = 0; s < h.length; s++) {
            int shortest = Integer.MAX_VALUE;
            for (int e = s; e < h.length; e++) {
                shortest = Math.min(shortest, h[e]);
                long area = (long) shortest * (e - s + 1);
                if (area > best[0] || (area == best[0] && (s < best[1] || (s == best[1] && e < best[2])))) { best[0] = area; best[1] = s; best[2] = e; }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(best(new int[]{2, 4, 4, 3, 1, 5, 5, 5}), new long[]{15, 5, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(best(new int[]{3, 0, 3}), new long[]{3, 0, 0})) throw new AssertionError("example 2");
        Random rnd = new Random(1803);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] h = new int[n];
            boolean positive = false;
            for (int i = 0; i < n; i++) { h[i] = rnd.nextInt(5); positive |= h[i] > 0; }
            if (!positive) h[rnd.nextInt(n)] = 1;
            if (!Arrays.equals(best(h), oracle(h))) throw new AssertionError("disagrees with the brute force on " + Arrays.toString(h));
        }
    }
}
```

#### Solution: [Recognize] Subarray Ranges From Two Ownership Passes (LeetCode 907)
<!-- id: ms-combo-subarray-ranges -->

**Approach.** The range of a subarray is its maximum minus its minimum, so the answer is the sum of maxima minus the sum of minima. For each role, one stack pass finds a strict left wall and a non-strict right wall, so each subarray has exactly one owner of its maximum and one owner of its minimum, with ties going to the last tied index. The counts of each role must add up to `n * (n + 1) / 2`, and the answer is the sum over indices of the value times the difference of the two counts. The assertions check the examples, compare with a brute force, verify both count totals, and show that using strict walls on both sides for the maximum role gives 10 instead of 4 on `[1, 3, 3]`.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SubarrayRanges {
    static long[] owned(int[] a, boolean forMaximum) {
        int n = a.length;
        int[] left = new int[n];
        int[] right = new int[n];
        Arrays.fill(right, n);
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < n; j++) {
            while (!stack.isEmpty() && beats(a[j], a[stack.peekLast()], forMaximum)) right[stack.removeLast()] = j;
            left[j] = stack.isEmpty() ? -1 : stack.peekLast();
            stack.addLast(j);
        }
        long[] count = new long[n];
        for (int i = 0; i < n; i++) count[i] = (long) (i - left[i]) * (right[i] - i);
        return count;
    }
    static boolean beats(int current, int top, boolean forMaximum) {
        return forMaximum ? current >= top : current <= top;
    }
    static long[] strictBothMaximum(int[] a) {
        int n = a.length;
        long[] count = new long[n];
        for (int i = 0; i < n; i++) {
            int l = i - 1;
            while (l >= 0 && !(a[l] > a[i])) l--;
            int r = i + 1;
            while (r < n && !(a[r] > a[i])) r++;
            count[i] = (long) (i - l) * (r - i);
        }
        return count;
    }
    static long sumOfRanges(int[] a, boolean strictMaxWalls) {
        long[] asMax = strictMaxWalls ? strictBothMaximum(a) : owned(a, true);
        long[] asMin = owned(a, false);
        long total = 0;
        for (int i = 0; i < a.length; i++) total += (long) a[i] * (asMax[i] - asMin[i]);
        return total;
    }
    static long oracle(int[] a) {
        long total = 0;
        for (int l = 0; l < a.length; l++) {
            int lo = a[l], hi = a[l];
            for (int r = l; r < a.length; r++) {
                lo = Math.min(lo, a[r]);
                hi = Math.max(hi, a[r]);
                total += (long) hi - lo;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        if (sumOfRanges(new int[]{1, 3, 3}, false) != 4) throw new AssertionError("example 1");
        if (sumOfRanges(new int[]{4, 4, 4}, false) != 0) throw new AssertionError("example 2");
        if (sumOfRanges(new int[]{1, 3, 3}, true) != 10) throw new AssertionError("strict walls on both sides over-count tied maxima");
        Random rnd = new Random(1804);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (sumOfRanges(a, false) != oracle(a)) throw new AssertionError("disagrees with the brute force on " + Arrays.toString(a));
            long all = (long) n * (n + 1) / 2;
            if (Arrays.stream(owned(a, true)).sum() != all || Arrays.stream(owned(a, false)).sum() != all)
                throw new AssertionError("each role must own every subarray exactly once");
        }
        int[] big = new int[100000];
        for (int i = 0; i < big.length; i++) big[i] = rnd.nextInt(20001) - 10000;
        int[] reversed = new int[big.length];
        for (int i = 0; i < big.length; i++) reversed[i] = big[big.length - 1 - i];
        long viaStack = sumOfRanges(big, false);
        if (viaStack < 0 || viaStack >= 1_000_000_000_000_000L) throw new AssertionError("the total must be non-negative and below 10^15");
        if (viaStack != sumOfRanges(reversed, false)) throw new AssertionError("reversing swaps the tie owners but not the total");
    }
}
```
