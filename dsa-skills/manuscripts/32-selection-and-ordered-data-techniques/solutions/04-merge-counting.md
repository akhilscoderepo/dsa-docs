<!-- solutions-for: 04-merge-counting -->
### Solutions For Merge Counting

#### Solution: [Build] Count Inversions (Author exercise)
<!-- id: mrg-count-inversions -->

**Approach.** Split the range, count inside each half by recursion, then count the pairs between the halves while merging.

Both halves are sorted when the merge starts. When the merge takes a right value `a[j]` while the left value `a[i]` is larger, the sorted left half guarantees that all `mid - i` unread left values are larger too. The merge adds that number at once. A left value that is less than or equal to the right value moves first, so equal values are never counted. The invariant is that `count` equals the number of pairs in the range whose right value is already written. The program works on a clone, so the caller's array stays unchanged. The midpoint uses `lo + (hi - lo) / 2`, because `(lo + hi) / 2` overflows an `int` for bounds near two billion.

**Complexity.**

- **Time** is O(n log n), because the recursion has about log2(n) levels and each level merges n values in total.
- **Space** is O(n), for the clone, the shared buffer and the recursion stack of depth O(log n).

```java run
import java.util.Arrays;
import java.util.Random;

public final class InversionCount {
    /**
     * Counts pairs i < j with a[i] > a[j] without changing the input.
     * Time: O(n log n), about log2(n) levels of linear merges.
     * Space: O(n), one clone and one shared buffer.
     * Invariant: after a call on [lo, hi), the range is sorted and the return value counts its inversions.
     */
    static long count(int[] input) {
        // The clone keeps the caller's array unchanged.
        int[] work = input.clone();
        // One buffer is shared by every call, so no level allocates.
        return sortCount(work, 0, work.length, new int[work.length]);
    }

    private static long sortCount(int[] a, int lo, int hi, int[] buf) {
        // A range of zero or one value holds no pair.
        if (hi - lo < 2) return 0;
        // The offset form cannot overflow when lo and hi are large.
        int mid = lo + (hi - lo) / 2;
        // Pairs inside each half come from the recursion.
        long total = sortCount(a, lo, mid, buf) + sortCount(a, mid, hi, buf);
        int i = lo, j = mid, k = lo;
        // The loop runs once per value in the range, so each level costs O(n).
        while (i < mid || j < hi) {
            // A tie takes the left value first, so equal values do not count.
            if (j == hi || (i < mid && a[i] <= a[j])) {
                buf[k++] = a[i++];
            } else {
                // Every unread left value is larger than a[j] because the left half is sorted.
                total += mid - i;
                buf[k++] = a[j++];
            }
        }
        // Copy the merged range back so the parent sees sorted halves.
        System.arraycopy(buf, lo, a, lo, hi - lo);
        return total;
    }

    /** Counts inversions with the double loop. */
    static long brute(int[] a) {
        long c = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                if (a[i] > a[j]) c++;
        return c;
    }

    public static void main(String[] args) {
        // Checks Example 1 and the empty and single-value cases.
        if (count(new int[]{2, 4, 1, 3, 5}) != 3) throw new AssertionError("example 1");
        if (count(new int[]{}) != 0 || count(new int[]{9}) != 0) throw new AssertionError("tiny");
        // Checks Example 2: the total exceeds the int range, so the counter must be a long.
        int n = 100_000;
        int[] down = new int[n];
        for (int i = 0; i < n; i++) down[i] = n - i;
        long big = count(down);
        if (big != 4_999_950_000L) throw new AssertionError("example 2");
        if (big <= Integer.MAX_VALUE) throw new AssertionError("long needed");
        if ((int) big == big) throw new AssertionError("an int cast would lose the value");
        // Checks the claim that (lo + hi) / 2 overflows while the offset form does not.
        int lo = 1_500_000_000, hi = 2_000_000_000;
        if ((lo + hi) / 2 >= 0) throw new AssertionError("sum should overflow");
        if (lo + (hi - lo) / 2 != 1_750_000_000) throw new AssertionError("offset midpoint");
        // Checks against the brute force on random arrays, with many ties and with a wide range.
        Random rnd = new Random(3204);
        for (int round = 0; round < 600; round++) {
            int len = rnd.nextInt(60);
            int bound = round % 2 == 0 ? 6 : Integer.MAX_VALUE;
            int[] a = new int[len];
            for (int i = 0; i < len; i++) a[i] = rnd.nextInt(bound) - (bound / 2);
            int[] copy = a.clone();
            if (count(a) != brute(a)) throw new AssertionError("round " + round);
            // The input array is unchanged by the call.
            if (!Arrays.equals(a, copy)) throw new AssertionError("mutated " + round);
        }
    }
}
```

#### Solution: [Vary] Count Of Greater Values Before Each Position (LeetCode 315)
<!-- id: mrg-greater-before -->

**Approach.** Sort an array of positions instead of values, and add to the entry of the right value when it is taken.

The array `order` holds original positions, and the merge compares `a[order[i]]` with `a[order[j]]`. Merging moves positions around, but the array `a` and the meaning of each position never change. When the right position `order[j]` is taken while the left value is larger, all `mid - i` unread left positions hold larger values that sit before it in the original array. The merge adds `mid - i` to `result[order[j]]`. Each right position is taken once per level, and its earlier larger values are split across levels without overlap, so the additions over all levels sum to the full count. A left value that is less than or equal to the right value goes first, so equal values do not count. The sums are at most `n - 1`, so an `int` is enough here.

**Complexity.**

- **Time** is O(n log n), because each level merges n positions and does one addition per right position.
- **Space** is O(n), for the position array, the shared buffer and the result.

```java run
import java.util.Arrays;
import java.util.Random;

public final class GreaterBefore {
    /**
     * Returns, for each position j, the number of positions i < j with a[i] > a[j].
     * Time: O(n log n), one merge pass per level over the position array.
     * Space: O(n), for order, the buffer and the result.
     * Invariant: after a call on [lo, hi), order[lo..hi) lists those positions by ascending value,
     * and result holds the larger values found among positions of the same range.
     */
    static int[] countBefore(int[] a) {
        int n = a.length;
        // The position array starts as the identity order.
        int[] order = new int[n];
        for (int i = 0; i < n; i++) order[i] = i;
        int[] result = new int[n];
        sort(a, order, 0, n, new int[n], result);
        return result;
    }

    private static void sort(int[] a, int[] order, int lo, int hi, int[] buf, int[] result) {
        // A range of zero or one position needs no work.
        if (hi - lo < 2) return;
        int mid = lo + (hi - lo) / 2;
        sort(a, order, lo, mid, buf, result);
        sort(a, order, mid, hi, buf, result);
        int i = lo, j = mid, k = lo;
        while (i < mid || j < hi) {
            // Compare values through the positions; ties go left so equal values are not counted.
            if (j == hi || (i < mid && a[order[i]] <= a[order[j]])) {
                buf[k++] = order[i++];
            } else {
                // The right value gains one per unread left position, all with larger values.
                result[order[j]] += mid - i;
                buf[k++] = order[j++];
            }
        }
        // Copy the merged positions back for the parent level.
        System.arraycopy(buf, lo, order, lo, hi - lo);
    }

    /** Counts earlier larger values with the double loop. */
    static int[] brute(int[] a) {
        int[] r = new int[a.length];
        for (int j = 0; j < a.length; j++)
            for (int i = 0; i < j; i++)
                if (a[i] > a[j]) r[j]++;
        return r;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (!Arrays.equals(countBefore(new int[]{5, 2, 6, 1}), new int[]{0, 1, 0, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(countBefore(new int[]{4, 4, 4}), new int[]{0, 0, 0})) throw new AssertionError("example 2");
        if (countBefore(new int[]{}).length != 0) throw new AssertionError("empty");
        // Checks the claim that the call leaves the input unchanged and that the sums fit in an int.
        int n = 50_000;
        int[] down = new int[n];
        for (int i = 0; i < n; i++) down[i] = n - i;
        int[] copy = down.clone();
        int[] r = countBefore(down);
        if (!Arrays.equals(down, copy)) throw new AssertionError("mutated");
        if (r[n - 1] != n - 1) throw new AssertionError("last entry");
        // Checks the per-position results against the brute force, with ties and with a wide value range.
        Random rnd = new Random(3205);
        for (int round = 0; round < 600; round++) {
            int len = rnd.nextInt(60);
            int bound = round % 2 == 0 ? 6 : Integer.MAX_VALUE;
            int[] a = new int[len];
            for (int i = 0; i < len; i++) a[i] = rnd.nextInt(bound) - (bound / 2);
            if (!Arrays.equals(countBefore(a), brute(a))) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Boundary] Equal Values (Author exercise)
<!-- id: mrg-equal-values -->

**Approach.** Flip the tie rule so that an equal left value is counted against the right value.

The relation is now `a[i] >= a[j]`. The merge takes a left value first only when it is strictly smaller than the right value. On a tie the right value is taken and the program adds `mid - i`. That is correct because the left half is sorted, so the equal left value and every later left value are at least as large as `a[j]`. The invariant is that the unread left values are all at least `a[j]` whenever the right value is taken. Keeping the strict rule from the earlier exercise would count only strictly larger left values and would return 0 for four equal values, so the two contracts need different tie rules.

**Complexity.**

- **Time** is O(n log n), since the tie rule changes one comparison and not the number of merge steps.
- **Space** is O(n), because the clone, the shared buffer and the call stack are the only extra storage.

```java run
import java.util.Random;

public final class EqualPairs {
    /**
     * Counts pairs i < j with a[i] >= a[j].
     * Time: O(n log n), the same merge shape as the strict count.
     * Space: O(n), one clone and one buffer.
     * Invariant: when a right value is taken, every unread left value is at least that right value.
     */
    static long countAtLeast(int[] input) {
        int[] work = input.clone();
        return run(work, 0, work.length, new int[work.length], false);
    }

    /** Counts strict pairs; the flag chooses the tie rule so the two contracts can be compared. */
    static long countStrict(int[] input) {
        int[] work = input.clone();
        return run(work, 0, work.length, new int[work.length], true);
    }

    private static long run(int[] a, int lo, int hi, int[] buf, boolean strict) {
        if (hi - lo < 2) return 0;
        int mid = lo + (hi - lo) / 2;
        long total = run(a, lo, mid, buf, strict) + run(a, mid, hi, buf, strict);
        int i = lo, j = mid, k = lo;
        while (i < mid || j < hi) {
            // Strict: a tie moves left. Non-strict: a tie moves right, which counts the left value.
            boolean leftFirst = j == hi || (i < mid && (strict ? a[i] <= a[j] : a[i] < a[j]));
            if (leftFirst) {
                buf[k++] = a[i++];
            } else {
                // All unread left values satisfy the relation with a[j].
                total += mid - i;
                buf[k++] = a[j++];
            }
        }
        System.arraycopy(buf, lo, a, lo, hi - lo);
        return total;
    }

    /** Counts pairs with the double loop. */
    static long brute(int[] a, boolean strict) {
        long c = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                if (strict ? a[i] > a[j] : a[i] >= a[j]) c++;
        return c;
    }

    public static void main(String[] args) {
        // Checks both examples, and the claim that the strict rule returns 0 on equal values.
        if (countAtLeast(new int[]{1, 2, 2, 1}) != 4) throw new AssertionError("example 1");
        if (countAtLeast(new int[]{7, 7, 7, 7}) != 6) throw new AssertionError("example 2");
        if (countStrict(new int[]{7, 7, 7, 7}) != 0) throw new AssertionError("strict on ties");
        if (countAtLeast(new int[]{}) != 0 || countAtLeast(new int[]{3}) != 0) throw new AssertionError("tiny");
        // Checks a large all-equal array: n(n-1)/2 pairs need a long.
        int n = 100_000;
        int[] same = new int[n];
        if (countAtLeast(same) != 4_999_950_000L) throw new AssertionError("all equal");
        // Checks both tie rules against the brute force on random arrays with heavy repetition.
        Random rnd = new Random(3206);
        for (int round = 0; round < 600; round++) {
            int len = rnd.nextInt(60);
            int bound = round % 3 == 0 ? 3 : 8;
            int[] a = new int[len];
            for (int i = 0; i < len; i++) a[i] = rnd.nextInt(bound);
            if (countAtLeast(a) != brute(a, false)) throw new AssertionError("non-strict " + round);
            if (countStrict(a) != brute(a, true)) throw new AssertionError("strict " + round);
        }
    }
}
```

#### Solution: [Recognize] Reverse Pairs (LeetCode 493)
<!-- id: mrg-large-drop -->

**Approach.** Count the cross pairs in a separate pass over the two sorted halves, then merge.

The condition `a[i] - a[j] > d` is the same as `a[i] > a[j] + d`. The right half is sorted, so `a[j] + d` grows as `j` grows. The count of left values above that threshold can only shrink, so one left pointer `p` moves forward and never back. For each right value, the pointer skips the left values with `a[p] - a[j] <= d`, and the remaining `mid - p` left values all satisfy the relation. The counting pass finishes before the merge, because the merge order compares plain values and the counting order compares shifted values. The difference of two `int` values can reach about four billion, so the subtraction is done in `long`. The invariant is that, for the right value being processed, the left values before `p` do not satisfy the relation and those from `p` on all do.

**Complexity.**

- **Time** is O(n log n), because each level makes one linear counting pass and one linear merge.
- **Space** is O(n), for the clone, the shared buffer and the recursion stack.

```java run
import java.util.Random;

public final class LargeDrop {
    /**
     * Counts pairs i < j with a[i] - a[j] > d, using long arithmetic.
     * Time: O(n log n), a counting pass and a merge per level.
     * Space: O(n), one clone and one buffer.
     * Invariant: for the current right value, left values before p fail the test and the rest pass.
     */
    static long countDrops(int[] input, long d) {
        int[] work = input.clone();
        return run(work, 0, work.length, new int[work.length], d);
    }

    private static long run(int[] a, int lo, int hi, int[] buf, long d) {
        if (hi - lo < 2) return 0;
        int mid = lo + (hi - lo) / 2;
        long total = run(a, lo, mid, buf, d) + run(a, mid, hi, buf, d);
        // Counting pass: p only moves forward because a[j] + d grows with j.
        int p = lo;
        for (int j = mid; j < hi; j++) {
            // The cast to long happens before the subtraction, so the difference cannot overflow.
            while (p < mid && (long) a[p] - a[j] <= d) p++;
            // Every left value from p on has a difference above d.
            total += mid - p;
        }
        // Merge pass: an ordinary merge of two sorted halves.
        int i = lo, j = mid, k = lo;
        while (i < mid || j < hi) {
            if (j == hi || (i < mid && a[i] <= a[j])) buf[k++] = a[i++];
            else buf[k++] = a[j++];
        }
        System.arraycopy(buf, lo, a, lo, hi - lo);
        return total;
    }

    /** Counts pairs with the double loop in long arithmetic. */
    static long brute(int[] a, long d) {
        long c = 0;
        for (int i = 0; i < a.length; i++)
            for (int j = i + 1; j < a.length; j++)
                if ((long) a[i] - a[j] > d) c++;
        return c;
    }

    public static void main(String[] args) {
        // Checks Example 1 and the empty input.
        if (countDrops(new int[]{7, 1, 5, 2}, 3) != 2) throw new AssertionError("example 1");
        if (countDrops(new int[]{}, 0) != 0) throw new AssertionError("empty");
        // Checks Example 2, and the claim that the difference overflows an int.
        int bad = 2_000_000_000 - (-2_000_000_000);
        if (bad >= 0) throw new AssertionError("int difference should wrap to a negative value");
        if (countDrops(new int[]{2_000_000_000, -2_000_000_000}, 3_999_999_999L) != 1) throw new AssertionError("example 2");
        if (countDrops(new int[]{2_000_000_000, -2_000_000_000}, 4_000_000_000L) != 0) throw new AssertionError("threshold equal");
        // Checks d = 0 against the plain inversion count and a large decreasing array for the long total.
        int n = 100_000;
        int[] down = new int[n];
        for (int i = 0; i < n; i++) down[i] = n - i;
        if (countDrops(down, 0) != 4_999_950_000L) throw new AssertionError("d = 0");
        // Checks random arrays with small and with extreme values against the brute force.
        Random rnd = new Random(3207);
        for (int round = 0; round < 600; round++) {
            int len = rnd.nextInt(60);
            boolean wide = round % 2 == 1;
            int[] a = new int[len];
            for (int i = 0; i < len; i++) a[i] = wide ? rnd.nextInt() : rnd.nextInt(21) - 10;
            long d = wide ? (long) (rnd.nextDouble() * 4e9) : rnd.nextInt(8);
            if (countDrops(a, d) != brute(a, d)) throw new AssertionError("round " + round);
        }
    }
}
```
