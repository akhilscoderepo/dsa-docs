<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Submask Aggregation

#### Solution: [Build] Enumerate Submasks (Author exercise)
<!-- id: dp29-enumerate-submasks -->

**Approach.**
The loop starts at `mask`, which is its own largest submask. After each report it replaces `sub` by `(sub - 1) & mask`. Subtracting 1 clears the lowest set bit and sets the bits below it, and the AND keeps only the bits that belong to the mask. The result is the next smaller submask.

The invariant is that every submask smaller than the current `sub` is still ahead, and every larger one has been reported once. The loop condition `sub > 0` stops at the empty submask, which the problem excludes. The output length is known in advance as `2^k - 1`, with `k = Integer.bitCount(mask)`.

**Complexity.**
- **Time** is O(2^k) for k set bits, because each iteration reports one submask with constant work.
- **Space** is O(2^k) for the result array, and no other memory grows.

```java run
import java.util.*;

public final class Dp29EnumerateSubmasks {
    /**
     * Returns all nonempty submasks of mask in decreasing order.
     * Time: O(2^k) for k set bits. Space: O(2^k) for the result.
     * Invariant: every submask below sub is still ahead and none is repeated.
     */
    static int[] submasks(int mask) {
        // The count of nonempty submasks is 2^k - 1, so the array has the exact size.
        int[] out = new int[(1 << Integer.bitCount(mask)) - 1];
        int w = 0;
        // The loop starts at the largest submask and stops before the empty one.
        for (int sub = mask; sub > 0; sub = (sub - 1) & mask) {
            // Each iteration reports one submask, which costs constant time.
            out[w++] = sub;
        }
        return out;
    }

    /** Oracle: scans every integer up to mask and keeps those with all bits inside the mask. */
    static int[] oracle(int mask) {
        List<Integer> all = new ArrayList<>();
        for (int s = mask; s >= 1; s--) if ((s & mask) == s) all.add(s);
        int[] r = new int[all.size()];
        for (int i = 0; i < r.length; i++) r[i] = all.get(i);
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(submasks(13), new int[]{13, 12, 9, 8, 5, 4, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(submasks(6), new int[]{6, 4, 2})) throw new AssertionError("ex2");
        // A zero mask has no nonempty submask.
        if (submasks(0).length != 0) throw new AssertionError("zero");
        // The naive scan makes exactly mask iterations, which grows with the top bit and not with the bit count.
        int iterations = 0;
        int mask = (1 << 20) | 1;
        for (int s = 1; s <= mask; s++) iterations++;
        if (iterations != mask || submasks(mask).length != 3) throw new AssertionError("scan cost");
        // Subtracting 1 from 12 gives 1011, and the AND with 1101 gives 1001, which is 9.
        if (((12 - 1) & 13) != 9) throw new AssertionError("step");
        // Random masks against the scan oracle.
        Random rnd = new Random(2905);
        for (int t = 0; t < 2000; t++) {
            int m = rnd.nextInt(1 << 12);
            if (!Arrays.equals(submasks(m), oracle(m))) throw new AssertionError("random " + m);
        }
    }
}
```

#### Solution: [Vary] Partition A Mask (Author exercise)
<!-- id: dp29-partition-mask -->

**Approach.**
Entry `dp[mask]` is the smallest number of groups for the items named by `mask`. If the total weight of `mask` is at most `cap`, one group holds all of them, so the entry is 1. Otherwise some group in an optimal answer contains a proper part of the mask, and the rest forms the other part. The entry is the minimum of `dp[sub] + dp[mask ^ sub]` over every proper nonempty `sub`.

The invariant is that `sub` and `mask ^ sub` are both smaller than `mask` as numbers, so their entries are final when `mask` is processed in increasing order. The total weight of each mask comes from the mask without its lowest bit, which costs constant time per mask. Every weight is at most `cap`, so each single item fits and every entry is finite.

**Complexity.**
- **Time** is O(3^n), because the proper submasks of all masks together number at most 3^n.
- **Space** is O(2^n) for the two tables, and the input array stays unchanged.

```java run
import java.util.*;

public final class Dp29PartitionMask {
    /**
     * Returns the smallest number of groups whose weight sums stay within cap.
     * Time: O(3^n). Space: O(2^n).
     * Invariant: dp[sub] and dp[mask ^ sub] are final before dp[mask] reads them.
     */
    static int groups(int[] weight, int cap) {
        // n items give 2^n masks, one table entry for each.
        int n = weight.length;
        int[] sum = new int[1 << n];
        int[] dp = new int[1 << n];
        // Masks grow from 1, so every smaller mask is final when read.
        for (int mask = 1; mask < (1 << n); mask++) {
            // The mask without its lowest bit is smaller, so its sum is already known.
            int lowest = Integer.numberOfTrailingZeros(mask);
            sum[mask] = sum[mask & (mask - 1)] + weight[lowest];
            // A mask that fits the capacity needs one group; otherwise start from a large value.
            dp[mask] = sum[mask] <= cap ? 1 : Integer.MAX_VALUE / 2;
            // The proper submasks start below mask and stop before 0.
            for (int sub = (mask - 1) & mask; sub > 0; sub = (sub - 1) & mask) {
                // Combine the answer for sub with the answer for the remaining items.
                dp[mask] = Math.min(dp[mask], dp[sub] + dp[mask ^ sub]);
            }
        }
        // The full mask names every item.
        return dp[(1 << n) - 1];
    }

    /** Oracle: places each item into an existing group or a new group, trying every choice. */
    static int oracle(int[] w, int cap, int i, List<Integer> loads) {
        if (i == w.length) return loads.size();
        int best = Integer.MAX_VALUE;
        for (int g = 0; g < loads.size(); g++) {
            if (loads.get(g) + w[i] <= cap) {
                loads.set(g, loads.get(g) + w[i]);
                best = Math.min(best, oracle(w, cap, i + 1, loads));
                loads.set(g, loads.get(g) - w[i]);
            }
        }
        loads.add(w[i]);
        best = Math.min(best, oracle(w, cap, i + 1, loads));
        loads.remove(loads.size() - 1);
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (groups(new int[]{4, 3, 3, 2}, 6) != 2) throw new AssertionError("ex1");
        if (groups(new int[]{5, 5, 5}, 9) != 3) throw new AssertionError("ex2");
        // One item needs one group, and mask & (mask - 1) clears the lowest set bit.
        if (groups(new int[]{7}, 7) != 1) throw new AssertionError("single");
        if ((12 & 11) != 8 || Integer.numberOfTrailingZeros(12) != 2) throw new AssertionError("bit facts");
        // Random instances against the assignment oracle.
        Random rnd = new Random(2906);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(8);
            int cap = 1 + rnd.nextInt(12);
            int[] w = new int[n];
            for (int i = 0; i < n; i++) w[i] = 1 + rnd.nextInt(cap);
            int[] copy = w.clone();
            if (groups(w, cap) != oracle(w, cap, 0, new ArrayList<>())) throw new AssertionError("random " + t);
            if (!Arrays.equals(copy, w)) throw new AssertionError("mutation");
        }
    }
}
```

#### Solution: [Boundary] Include Empty Submask Deliberately (Author exercise)
<!-- id: dp29-include-empty -->

**Approach.**
The standard loop ends at 0 because `sub > 0` fails there. This exercise needs 0 in the output, so the loop reports `sub` first and then checks for 0. Java computes `0 - 1` as `-1`, whose bits are all set, so `(0 - 1) & mask` equals `mask`. A loop that moves on from 0 returns to the start and never ends. The explicit break prevents that.

The invariant is that every submask larger than the current one has been reported, and the current one is reported before the stop test. Mask 0 reports `[0]` and stops at once. The result has `2^k` entries.

**Complexity.**
- **Time** is O(2^k) for k set bits, because each submask costs constant work, including the final 0.
- **Space** is O(2^k) for the result array.

```java run
import java.util.*;

public final class Dp29IncludeEmpty {
    /**
     * Returns every submask of mask including 0, in decreasing order.
     * Time: O(2^k) for k set bits. Space: O(2^k).
     * Invariant: the current submask is reported before the stop test, so 0 appears last.
     */
    static int[] withEmpty(int mask) {
        // There are 2^k submasks including the empty one.
        int[] out = new int[1 << Integer.bitCount(mask)];
        int w = 0;
        int sub = mask;
        // The loop is open-ended on purpose, and the break below is the only exit.
        while (true) {
            // Report first, so that sub = 0 is also reported.
            out[w++] = sub;
            // Stop at 0, because the next step from 0 would return to mask.
            if (sub == 0) break;
            // Move to the next smaller submask.
            sub = (sub - 1) & mask;
        }
        return out;
    }

    /** Oracle: scans every integer from mask down to 0 and keeps the submasks. */
    static int[] oracle(int mask) {
        List<Integer> all = new ArrayList<>();
        for (int s = mask; s >= 0; s--) if ((s & mask) == s) all.add(s);
        int[] r = new int[all.size()];
        for (int i = 0; i < r.length; i++) r[i] = all.get(i);
        return r;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(withEmpty(5), new int[]{5, 4, 1, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(withEmpty(0), new int[]{0})) throw new AssertionError("ex2");
        // In Java, 0 - 1 is -1, and -1 & mask equals mask, so a loop that continues after 0 repeats.
        for (int mask : new int[]{1, 5, 13, 1000}) {
            if (((0 - 1) & mask) != mask) throw new AssertionError("wrap " + mask);
        }
        // The condition sub >= 0 on an int never fails, because the value returns to mask.
        int sub = 5, steps = 0;
        while (sub >= 0 && steps < 10) { sub = (sub - 1) & 5; steps++; }
        if (steps != 10) throw new AssertionError("no end");
        // Random masks against the scan oracle.
        Random rnd = new Random(2907);
        for (int t = 0; t < 2000; t++) {
            int m = rnd.nextInt(1 << 12);
            if (!Arrays.equals(withEmpty(m), oracle(m))) throw new AssertionError("random " + m);
        }
    }
}
```

#### Solution: [Recognize] SOS Subset Sums (Author exercise)
<!-- id: dp29-sos-subset-sums -->

**Approach.**
The array `f` starts as a copy of `a`. The method then processes the bits one at a time. In layer `bit`, every mask that has that bit set adds the current value of the mask with that bit cleared. After layer `bit`, `f[mask]` holds the sum of `a[sub]` over submasks that differ from `mask` only in bits 0 to `bit`.

The invariant is the sentence above, and it holds by induction on the layer. A submask that has the bit cleared is reached through the added entry, and a submask that keeps the bit is already in the old value. The layer reads an entry with the bit cleared, which the layer never changes, so the in-place update is safe. After the last layer every submask is counted once. Sums use `long`, since 2^16 values of 10^6 exceed the `int` range.

**Complexity.**
- **Time** is O(n * 2^n), because each of the n layers visits 2^n masks with constant work.
- **Space** is O(2^n) for the result, and the input array stays unchanged.

```java run
import java.util.*;

public final class Dp29SosSubsetSums {
    /**
     * Returns f where f[mask] is the sum of a[sub] over all submasks of mask.
     * Time: O(n * 2^n). Space: O(2^n).
     * Invariant: after layer b, f[mask] sums the submasks that differ from mask only in bits 0..b.
     */
    static long[] sums(int n, int[] a) {
        // The copy keeps the input unchanged and widens each value to long.
        long[] f = new long[1 << n];
        for (int i = 0; i < f.length; i++) f[i] = a[i];
        // Each layer handles one bit, so n layers run.
        for (int b = 0; b < n; b++) {
            // Every mask is visited once per layer, which costs 2^n.
            for (int mask = 0; mask < (1 << n); mask++) {
                // Only masks with bit b set receive a contribution.
                if ((mask & (1 << b)) != 0) {
                    // The partner has bit b cleared, so this layer does not change it.
                    f[mask] += f[mask ^ (1 << b)];
                }
            }
        }
        return f;
    }

    /** Oracle: enumerates the submasks of each mask, including 0. */
    static long[] oracle(int n, int[] a) {
        long[] f = new long[1 << n];
        for (int mask = 0; mask < (1 << n); mask++) {
            long s = 0;
            for (int sub = mask; ; sub = (sub - 1) & mask) {
                s += a[sub];
                if (sub == 0) break;
            }
            f[mask] = s;
        }
        return f;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(sums(2, new int[]{1, 2, 3, 4}), new long[]{1, 3, 4, 10})) throw new AssertionError("ex1");
        if (!Arrays.equals(sums(3, new int[]{3, 1, 4, 1, 5, 9, 2, 6}), new long[]{3, 4, 7, 9, 8, 18, 14, 31})) throw new AssertionError("ex2");
        // With n = 0 the table has one entry, which is a[0].
        if (!Arrays.equals(sums(0, new int[]{7}), new long[]{7})) throw new AssertionError("n zero");
        // The largest allowed sum exceeds the int range, so long is required.
        long big = (1L << 16) * 1_000_000L;
        if (big <= Integer.MAX_VALUE) throw new AssertionError("range");
        // Random arrays against the enumeration oracle, with a check that the input is unchanged.
        Random rnd = new Random(2908);
        for (int t = 0; t < 500; t++) {
            int n = rnd.nextInt(8);
            int[] a = new int[1 << n];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(1_000_001);
            int[] copy = a.clone();
            if (!Arrays.equals(sums(n, a), oracle(n, a))) throw new AssertionError("random " + t);
            if (!Arrays.equals(copy, a)) throw new AssertionError("mutation");
        }
        // The full table at n = 16 with maximal values stays exact.
        int[] full = new int[1 << 16];
        Arrays.fill(full, 1_000_000);
        if (sums(16, full)[(1 << 16) - 1] != big) throw new AssertionError("big");
    }
}
```
