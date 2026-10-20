<!-- solutions-for: 02-partition-invariants -->
### Solutions For Partition Invariants

#### Solution: [Build] Lomuto Partition (Author exercise)
<!-- id: par-lomuto-partition -->

**Approach.** The scan keeps four regions inside `a[lo..hi]`, and each step shrinks the unresolved one.

The pivot value is read from `a[hi]` before any swap. The pointer `i` starts at `lo`, so the range of smaller values is empty. For each `j` from `lo` to `hi - 1`, a value below the pivot swaps with `a[i]` and `i` moves right. The invariant is that `a[lo..i-1]` is below the pivot, `a[i..j-1]` is at least the pivot, and `a[j..hi-1]` is unresolved. A value that is not below the pivot needs no move, because it already lies in the second range. When `i` equals `j` the swap is a slot with itself, which leaves the array unchanged. The final swap puts the pivot at `i`. Slots outside `lo..hi` are never read or written.

**Complexity.**

- **Time** is O(hi - lo + 1), since the scan visits each slot of the range once and does constant work per slot.
- **Space** is O(1), as the method holds two indexes and the pivot value.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LomutoPartition {
    /**
     * Partitions a[lo..hi] around a[hi] and returns the final pivot index.
     * Time: O(hi - lo + 1), one visit per slot.
     * Space: O(1), two indexes and the pivot value.
     * Invariant: a[lo..i-1] below pivot, a[i..j-1] at least pivot, a[j..hi-1] unresolved.
     */
    static int lomuto(int[] a, int lo, int hi) {
        // Read the pivot before any swap can change a[hi].
        int pivot = a[hi];
        // The small range starts empty at lo.
        int i = lo;
        // The scan visits each unresolved slot once.
        for (int j = lo; j < hi; j++) {
            // Only a strictly smaller value joins the small range.
            if (a[j] < pivot) {
                // The swap keeps the large range contiguous.
                int t = a[i]; a[i] = a[j]; a[j] = t;
                // The small range grows by one slot.
                i++;
            }
        }
        // The pivot lands between the two ranges.
        int t = a[i]; a[i] = a[hi]; a[hi] = t;
        // This index is the pivot's final sorted position within the range.
        return i;
    }

    public static void main(String[] args) {
        // Checks Example 1.
        int[] e1 = {6, 3, 9, 2, 7, 4};
        if (lomuto(e1, 0, 5) != 2 || !Arrays.equals(e1, new int[]{3, 2, 4, 6, 7, 9})) throw new AssertionError("example 1");
        // Checks Example 2, where the bounds leave the outer slots alone.
        int[] e2 = {5, 1, 5, 5, 2};
        if (lomuto(e2, 1, 3) != 2 || !Arrays.equals(e2, new int[]{5, 1, 5, 5, 2})) throw new AssertionError("example 2");
        // Checks a single-slot range, where the pivot index is lo.
        int[] one = {9};
        if (lomuto(one, 0, 0) != 0) throw new AssertionError("single slot");
        // Checks the claim that equal values count as large: all equal puts the pivot at lo.
        int[] same = {4, 4, 4, 4};
        if (lomuto(same, 0, 3) != 0) throw new AssertionError("all equal pivot index");
        // Checks the postcondition on random inputs against a counting oracle.
        Random rnd = new Random(32);
        for (int round = 0; round < 2000; round++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int x = 0; x < n; x++) a[x] = rnd.nextInt(6);
            int lo = rnd.nextInt(n), hi = lo + rnd.nextInt(n - lo);
            int[] before = a.clone();
            int pivot = a[hi];
            int less = 0;
            for (int x = lo; x <= hi; x++) if (before[x] < pivot) less++;
            int idx = lomuto(a, lo, hi);
            if (idx != lo + less) throw new AssertionError("index round " + round);
            if (a[idx] != pivot) throw new AssertionError("pivot round " + round);
            for (int x = lo; x < idx; x++) if (a[x] >= pivot) throw new AssertionError("left round " + round);
            for (int x = idx + 1; x <= hi; x++) if (a[x] < pivot) throw new AssertionError("right round " + round);
            for (int x = 0; x < n; x++) if ((x < lo || x > hi) && a[x] != before[x]) throw new AssertionError("outside round " + round);
            int[] s1 = Arrays.copyOfRange(a, lo, hi + 1), s2 = Arrays.copyOfRange(before, lo, hi + 1);
            Arrays.sort(s1); Arrays.sort(s2);
            if (!Arrays.equals(s1, s2)) throw new AssertionError("multiset round " + round);
        }
    }
}
```

#### Solution: [Vary] Three-Way Partition (Author exercise)
<!-- id: par-three-way-partition -->

**Approach.** Three pointers split the array into below, equal, unresolved and above ranges.

The pointers start at `lt = 0`, `i = 0` and `gt = n - 1`, so only the unresolved range `a[i..gt]` is non-empty. The invariant is that `a[0..lt-1]` is below `p`, `a[lt..i-1]` equals `p`, `a[i..gt]` is unresolved and `a[gt+1..n-1]` is above `p`. A smaller value swaps with `a[lt]`. The value that arrives at `i` came from the equal range, so both `lt` and `i` advance. A larger value swaps with `a[gt]`. The value that arrives at `i` has not been compared, so `i` stays and only `gt` moves. An equal value advances `i`. The loop ends when `i > gt`, and the pair `{lt, gt}` bounds the equal range. If no value equals `p`, the result is `gt = lt - 1`.

**Complexity.**

- **Time** is O(n), because each step either advances `i` or lowers `gt`, so the unresolved range loses one slot per step.
- **Space** is O(1), as the method holds three indexes.

```java run
import java.util.Arrays;
import java.util.Random;

public final class ThreeWayPartition {
    /**
     * Rearranges a into below, equal and above ranges around p and returns {lt, gt}.
     * Time: O(n), the unresolved range loses one slot per step.
     * Space: O(1), three indexes.
     * Invariant: a[0..lt-1] < p, a[lt..i-1] == p, a[i..gt] unresolved, a[gt+1..n-1] > p.
     */
    static int[] threeWay(int[] a, int p) {
        // All slots start unresolved.
        int lt = 0, i = 0, gt = a.length - 1;
        // The loop runs while the unresolved range is non-empty.
        while (i <= gt) {
            if (a[i] < p) {
                // The value at lt is equal, so it moves to i and both pointers advance.
                int t = a[lt]; a[lt] = a[i]; a[i] = t;
                lt++; i++;
            } else if (a[i] > p) {
                // The arrival from gt is unexamined, so i stays.
                int t = a[i]; a[i] = a[gt]; a[gt] = t;
                gt--;
            } else {
                // An equal value is already in the equal range.
                i++;
            }
        }
        // The two bounds describe the equal range.
        return new int[]{lt, gt};
    }

    /** A faulty variant that advances i after the swap with gt, used to show why i must stay. */
    static void faulty(int[] a, int p) {
        int lt = 0, i = 0, gt = a.length - 1;
        while (i <= gt) {
            if (a[i] < p) { int t = a[lt]; a[lt] = a[i]; a[i] = t; lt++; i++; }
            else if (a[i] > p) { int t = a[i]; a[i] = a[gt]; a[gt] = t; gt--; i++; }
            else i++;
        }
    }

    static boolean valid(int[] a, int p, int lt, int gt) {
        for (int x = 0; x < a.length; x++) {
            if (x < lt && a[x] >= p) return false;
            if (x >= lt && x <= gt && a[x] != p) return false;
            if (x > gt && a[x] <= p) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1.
        int[] e1 = {4, 7, 1, 4, 9, 2, 4, 0};
        if (!Arrays.equals(threeWay(e1, 4), new int[]{3, 5}) || !valid(e1, 4, 3, 5)) throw new AssertionError("example 1");
        // Checks Example 2, where the pivot value is absent.
        int[] e2 = {8, 9, 6};
        if (!Arrays.equals(threeWay(e2, 5), new int[]{0, -1})) throw new AssertionError("example 2");
        // Checks the empty array.
        if (!Arrays.equals(threeWay(new int[0], 3), new int[]{0, -1})) throw new AssertionError("empty");
        // Shows that advancing i after the swap with gt leaves a smaller value in the equal range.
        int[] bad = {1, 2, 0};
        faulty(bad, 1);
        if (valid(bad, 1, 0, 1) && valid(bad, 1, 1, 1)) throw new AssertionError("faulty variant should break");
        int[] good = {1, 2, 0};
        int[] r = threeWay(good, 1);
        if (!Arrays.equals(good, new int[]{0, 1, 2}) || r[0] != 1 || r[1] != 1) throw new AssertionError("good variant");
        // Checks random arrays against counting.
        Random rnd = new Random(33);
        for (int round = 0; round < 3000; round++) {
            int n = rnd.nextInt(14);
            int[] a = new int[n];
            for (int x = 0; x < n; x++) a[x] = rnd.nextInt(7) - 3;
            int p = rnd.nextInt(9) - 4;
            int less = 0, eq = 0;
            for (int v : a) { if (v < p) less++; else if (v == p) eq++; }
            int[] copy = a.clone();
            int[] res = threeWay(a, p);
            if (res[0] != less || res[1] != less + eq - 1) throw new AssertionError("bounds round " + round);
            if (!valid(a, p, res[0], res[1])) throw new AssertionError("valid round " + round);
            Arrays.sort(a); Arrays.sort(copy);
            if (!Arrays.equals(a, copy)) throw new AssertionError("multiset round " + round);
        }
    }
}
```

#### Solution: [Boundary] All Equal Values (Author exercise)
<!-- id: par-all-equal-values -->

**Approach.** One three-way pass either finds that rank `k` is in the equal range or names the side that holds it.

The pivot value is read from `a[hi]` first. The three pointers start at `lt = lo`, `i = lo` and `gt = hi`, and the loop follows the same invariant as the three-way partition, restricted to `a[lo..hi]`. When every value equals the pivot, each step only advances `i`, `lt` stays at `lo` and `gt` stays at `hi`. The loop therefore ends after `hi - lo + 1` steps, and the equal range is the whole range. Then `k` lies in `lt..gt`, so the method returns `{-1, -1}`. If `k < lt` the answer lies below, so the method returns `{lo, lt - 1}`. If `k > gt` it returns `{gt + 1, hi}`. A two-way split on the same input would leave `n - 1` values still to examine.

**Complexity.**

- **Time** is O(hi - lo + 1), because each step shrinks the unresolved range by one slot.
- **Space** is O(1), since the method keeps three indexes and the pivot.

```java run
import java.util.Arrays;
import java.util.Random;

public final class AllEqualValues {
    /**
     * One three-way pass over a[lo..hi] that returns the range still holding position k.
     * Time: O(hi - lo + 1), one slot resolved per step.
     * Space: O(1), three indexes and the pivot.
     * Invariant: a[lo..lt-1] < pivot, a[lt..i-1] == pivot, a[i..gt] unresolved, a[gt+1..hi] > pivot.
     */
    static int[] step(int[] a, int lo, int hi, int k) {
        // Read the pivot before any swap.
        int pivot = a[hi];
        // The bounds are fixed, so the pointers start at them.
        int lt = lo, i = lo, gt = hi;
        // The loop ends when the unresolved range is empty.
        while (i <= gt) {
            if (a[i] < pivot) {
                int t = a[lt]; a[lt] = a[i]; a[i] = t;
                lt++; i++;
            } else if (a[i] > pivot) {
                int t = a[i]; a[i] = a[gt]; a[gt] = t;
                gt--;
            } else {
                i++;
            }
        }
        // Position k in the equal range is already final.
        if (k >= lt && k <= gt) return new int[]{-1, -1};
        // A smaller k keeps only the range below the equal block.
        if (k < lt) return new int[]{lo, lt - 1};
        // A larger k keeps only the range above the equal block.
        return new int[]{gt + 1, hi};
    }

    /** Counting oracle for the same contract. */
    static int[] oracle(int[] a, int lo, int hi, int k) {
        int p = a[hi], less = 0, eq = 0;
        for (int x = lo; x <= hi; x++) { if (a[x] < p) less++; else if (a[x] == p) eq++; }
        int lt = lo + less, gt = lt + eq - 1;
        if (k >= lt && k <= gt) return new int[]{-1, -1};
        if (k < lt) return new int[]{lo, lt - 1};
        return new int[]{gt + 1, hi};
    }

    public static void main(String[] args) {
        // Checks Example 1.
        int[] e1 = {3, 8, 3, 1, 3, 9, 3};
        if (!Arrays.equals(step(e1, 0, 6, 5), new int[]{5, 6})) throw new AssertionError("example 1");
        // Checks Example 2, where all values are equal.
        int[] e2 = {5, 5, 5, 5, 5};
        if (!Arrays.equals(step(e2, 0, 4, 2), new int[]{-1, -1})) throw new AssertionError("example 2");
        // Checks that the all-equal array is not changed by the pass.
        if (!Arrays.equals(e2, new int[]{5, 5, 5, 5, 5})) throw new AssertionError("all equal unchanged");
        // Checks the lower side of Example 1.
        int[] e3 = {3, 8, 3, 1, 3, 9, 3};
        if (!Arrays.equals(step(e3, 0, 6, 0), new int[]{0, 0})) throw new AssertionError("lower side");
        // Checks random sub-ranges against the counting oracle.
        Random rnd = new Random(34);
        for (int round = 0; round < 3000; round++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            int spread = 1 + rnd.nextInt(4);
            for (int x = 0; x < n; x++) a[x] = rnd.nextInt(spread);
            int lo = rnd.nextInt(n), hi = lo + rnd.nextInt(n - lo), k = lo + rnd.nextInt(hi - lo + 1);
            int[] expected = oracle(a, lo, hi, k);
            int[] got = step(a, lo, hi, k);
            if (!Arrays.equals(expected, got)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Recognize] Kth Largest Element In An Array (LeetCode 215)
<!-- id: par-kth-largest-unchanged -->

**Approach.** The `k`-th largest value sits at ascending index `n - k`, and a three-way partition on a working copy narrows the bounds until that index falls in an equal range.

The method copies `nums` once, so the caller's array stays unchanged. It sets `lo = 0`, `hi = n - 1` and `target = n - k`. Each round computes the middle index as `lo + (hi - lo) / 2`, which cannot overflow, and reads that value as the pivot. The three-way partition then splits `copy[lo..hi]` into below, equal and above ranges. If `target` is below the equal range, the search continues in the below range with `hi = lt - 1`. If `target` is above it, the search continues with `lo = gt + 1`. Otherwise the pivot is the answer. The invariant is that the element of ascending rank `target` always lies in `copy[lo..hi]`. Duplicates are counted separately, because the equal range occupies all its ranks. The bounds are passed as indexes, so no round copies a subarray.

**Complexity.**

- **Time** is O(n) on average, since each round discards the equal range and one side, and O(n^2) in the worst case with a fixed middle pivot.
- **Space** is O(n), for the single working copy, and O(1) beyond it.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KthLargestUnchanged {
    /**
     * Returns the k-th largest value of nums without modifying nums.
     * Time: O(n) on average, O(n^2) worst case with a fixed middle pivot.
     * Space: O(n) for the working copy, O(1) beyond it.
     * Invariant: the value of ascending rank target lies in copy[lo..hi].
     */
    static int kthLargest(int[] nums, int k) {
        // One copy protects the caller's array.
        int[] copy = nums.clone();
        // The k-th largest has ascending index n - k.
        int target = copy.length - k;
        // The search range starts as the whole copy.
        int lo = 0, hi = copy.length - 1;
        // Each round removes at least the pivot's equal range.
        while (lo <= hi) {
            // This midpoint form cannot overflow.
            int pivot = copy[lo + (hi - lo) / 2];
            // The three pointers describe the regions of copy[lo..hi].
            int lt = lo, i = lo, gt = hi;
            // The loop resolves one slot per step.
            while (i <= gt) {
                if (copy[i] < pivot) {
                    int t = copy[lt]; copy[lt] = copy[i]; copy[i] = t;
                    lt++; i++;
                } else if (copy[i] > pivot) {
                    int t = copy[i]; copy[i] = copy[gt]; copy[gt] = t;
                    gt--;
                } else {
                    i++;
                }
            }
            // The target rank is below the equal range, so drop it and everything above.
            if (target < lt) hi = lt - 1;
            // The target rank is above the equal range, so drop it and everything below.
            else if (target > gt) lo = gt + 1;
            // The target rank lies in the equal range, so the pivot is the answer.
            else return pivot;
        }
        // The invariant guarantees a return above for valid k.
        throw new IllegalArgumentException("k out of range");
    }

    public static void main(String[] args) {
        // Checks Example 1, where duplicates count separately.
        int[] e1 = {4, 9, 2, 9, 7, 1};
        int[] e1copy = e1.clone();
        if (kthLargest(e1, 3) != 7) throw new AssertionError("example 1");
        if (kthLargest(e1, 2) != 9) throw new AssertionError("duplicate count");
        // Checks that the input array is unchanged.
        if (!Arrays.equals(e1, e1copy)) throw new AssertionError("input changed");
        // Checks Example 2, where all values are equal.
        if (kthLargest(new int[]{5, 5, 5, 5}, 4) != 5) throw new AssertionError("example 2");
        // Checks that a copy of a subarray does not change the source, which is why bounds are passed instead.
        int[] src = {3, 1, 2};
        int[] part = Arrays.copyOfRange(src, 0, 3);
        part[0] = 99;
        if (src[0] != 3) throw new AssertionError("copy independent");
        // Checks that the sum of two large indexes overflows int while the safe midpoint does not.
        int lo = 1_500_000_000, hi = 2_000_000_000;
        if ((lo + hi) / 2 >= 0) throw new AssertionError("overflow expected");
        if (lo + (hi - lo) / 2 != 1_750_000_000) throw new AssertionError("safe midpoint");
        // Checks random arrays against sorting.
        Random rnd = new Random(35);
        for (int round = 0; round < 3000; round++) {
            int n = 1 + rnd.nextInt(15);
            int[] a = new int[n];
            for (int x = 0; x < n; x++) a[x] = rnd.nextInt(9) - 4;
            int k = 1 + rnd.nextInt(n);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            if (kthLargest(a, k) != sorted[n - k]) throw new AssertionError("round " + round);
        }
    }
}
```
