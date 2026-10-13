<!-- solutions-for: 01-quickselect -->
### Solutions For Quickselect

#### Solution: [Build] Select Kth Smallest (Author exercise)
<!-- id: sel-select-kth-smallest -->

**Approach.** The method keeps the bounds `lo` and `hi` of the range that still holds index `r`. Each round partitions `a[lo..hi]` around its middle element and gets the pivot's final rank `p`.

The pivot's final rank is exact, because the partition leaves exactly `p - lo` smaller values in front of it and the range holds the values that belong at positions `lo` to `hi`. If `p` equals `r`, the pivot is the answer. If `r` is smaller, only the left group can hold index `r`, so `hi` becomes `p - 1`. Otherwise `lo` becomes `p + 1`. The invariant is that `r` stays inside `lo..hi` and the range holds exactly the values of sorted positions `lo` to `hi`. The method passes bounds and never copies a subarray. The test also shows that the form `(lo + hi) / 2` overflows, which is why the code uses `lo + (hi - lo) / 2`.

**Complexity.**

- **Time** is expected O(n) for distinct values, because each partition scans the current range once and the range shrinks geometrically for typical pivots. A bad pivot sequence costs O(n^2). Many equal values also cost O(n^2) with this two-way partition, which the next lesson fixes with a three-way split.
- **Space** is O(1), because the method swaps inside the input and keeps three integers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class SelectKth {
    /**
     * Returns the value at sorted index k, reordering a in place.
     * Time: expected O(n), worst case O(n^2).
     * Space: O(1) extra.
     * Invariant: k lies in lo..hi and a[lo..hi] holds the values of sorted positions lo..hi.
     */
    static int select(int[] a, int k) {
        // The range starts as the whole array, which trivially holds index k.
        int lo = 0, hi = a.length - 1;
        // One element left means the range holds only index k.
        while (lo < hi) {
            // The partition fixes the pivot at its final rank p.
            int p = partition(a, lo, hi);
            // A pivot at index k is the answer.
            if (p == k) return a[p];
            // The target lies left of the pivot, so the right group is discarded.
            if (k < p) hi = p - 1;
            // The target lies right of the pivot, so the left group is discarded.
            else lo = p + 1;
        }
        // The last remaining element sits at index k.
        return a[lo];
    }

    /** Places the middle element at its final rank inside lo..hi and returns that rank. */
    static int partition(int[] a, int lo, int hi) {
        // The overflow-safe midpoint stays inside lo..hi.
        int mid = lo + (hi - lo) / 2;
        // Park the pivot at hi so the scan can ignore it.
        swap(a, mid, hi);
        int pivot = a[hi];
        // The boundary store is defined before any swap: a[lo..store-1] is below the pivot.
        int store = lo;
        // One scan costs O(hi - lo).
        for (int i = lo; i < hi; i++) {
            // Only values below the pivot cross the boundary.
            if (a[i] < pivot) {
                swap(a, i, store);
                store++;
            }
        }
        // The pivot moves to the boundary, which is its final rank.
        swap(a, store, hi);
        return store;
    }

    static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (select(new int[]{9, 4, 7, 1, 8, 2}, 2) != 4) throw new AssertionError("example 1");
        if (select(new int[]{5}, 0) != 5) throw new AssertionError("example 2");
        // Checks the claim that (lo + hi) / 2 overflows while lo + (hi - lo) / 2 does not.
        int lo = 2_000_000_000, hi = 2_100_000_000;
        if ((lo + hi) / 2 >= 0) throw new AssertionError("naive midpoint should overflow");
        if (lo + (hi - lo) / 2 != 2_050_000_000) throw new AssertionError("safe midpoint");
        // Checks every rank against a sorted copy on random arrays, including many ties.
        Random rnd = new Random(32);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(30);
            int bound = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2 * bound + 1) - bound;
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            for (int r = 0; r < n; r++) {
                if (select(a.clone(), r) != sorted[r]) throw new AssertionError("rank " + r + " of " + Arrays.toString(a));
            }
            // Checks the partition postcondition: the pivot sits at the count of smaller values.
            int[] b = a.clone();
            int p = partition(b, 0, n - 1);
            int smaller = 0;
            for (int v : a) if (v < b[p]) smaller++;
            if (p != smaller) throw new AssertionError("final rank");
            for (int i = 0; i < p; i++) if (b[i] >= b[p]) throw new AssertionError("left side");
            for (int i = p + 1; i < n; i++) if (b[i] < b[p]) throw new AssertionError("right side");
        }
    }
}
```

#### Solution: [Vary] Kth Largest Element (LeetCode 215)
<!-- id: sel-kth-largest -->

**Approach.** The `k`-th largest value is the value at ascending index `n - k`, because `k - 1` values are larger than it and `n - k` values come before it. The method converts `k` to that index once and then runs the same bounded partition loop.

The invariant stays the same: the range `lo..hi` holds the values of sorted positions `lo` to `hi` and contains the target index `n - k`. Equal values count separately, so a repeated value occupies several ranks. The test also asserts two Java facts that the lesson states. The call `Arrays.copyOfRange` returns an independent array, so writes to it never reach the original. The subtraction `a - b` overflows for values of opposite signs.

**Complexity.**

- **Time** is expected O(n) for distinct values, because each round scans only the surviving range. Many equal values degrade it to O(n^2) with this two-way partition.
- **Space** is O(1), because the partition swaps inside the input array.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KthLargest {
    /**
     * Returns the k-th largest element, where k = 1 is the maximum.
     * Time: expected O(n), worst case O(n^2).
     * Space: O(1) extra.
     * Invariant: n - k lies in lo..hi and a[lo..hi] holds the values of those sorted positions.
     */
    static int findKthLargest(int[] nums, int k) {
        // The k-th largest has n - k elements before it in ascending order.
        int target = nums.length - k;
        int lo = 0, hi = nums.length - 1;
        // Each round discards one side of the pivot.
        while (lo < hi) {
            int p = partition(nums, lo, hi);
            // The pivot at the target index is the answer.
            if (p == target) return nums[p];
            // Keep the side that contains the target.
            if (target < p) hi = p - 1;
            else lo = p + 1;
        }
        // One element left holds the target index.
        return nums[lo];
    }

    /** Places the middle element at its final rank in lo..hi and returns the rank. */
    static int partition(int[] a, int lo, int hi) {
        // Overflow-safe midpoint.
        int mid = lo + (hi - lo) / 2;
        int t = a[mid]; a[mid] = a[hi]; a[hi] = t;
        int pivot = a[hi];
        // Boundary of the smaller group, defined before the scan swaps anything.
        int store = lo;
        for (int i = lo; i < hi; i++) {
            if (a[i] < pivot) {
                int u = a[i]; a[i] = a[store]; a[store] = u;
                store++;
            }
        }
        // The pivot lands at the boundary.
        t = a[store]; a[store] = a[hi]; a[hi] = t;
        return store;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (findKthLargest(new int[]{3, 2, 1, 5, 6, 4}, 2) != 5) throw new AssertionError("example 1");
        if (findKthLargest(new int[]{4, 4, 1, 9, 9, 2, 7}, 3) != 7) throw new AssertionError("example 2");
        // Checks that copyOfRange gives an independent array, so a subarray copy is real extra work.
        int[] src = {1, 2, 3, 4};
        int[] copy = Arrays.copyOfRange(src, 1, 3);
        copy[0] = 99;
        if (src[1] != 2) throw new AssertionError("copy must be independent");
        // Checks that a - b overflows for values of opposite signs.
        int big = Integer.MAX_VALUE, neg = -1;
        if (big - neg >= 0) throw new AssertionError("difference should overflow");
        if (Integer.compare(big, neg) <= 0) throw new AssertionError("compare must stay correct");
        // Checks every k against a descending sort on random arrays with extreme values.
        Random rnd = new Random(215);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(25);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int pick = rnd.nextInt(6);
                a[i] = pick == 0 ? Integer.MAX_VALUE : pick == 1 ? Integer.MIN_VALUE : rnd.nextInt(9) - 4;
            }
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            for (int k = 1; k <= n; k++) {
                if (findKthLargest(a.clone(), k) != sorted[n - k]) throw new AssertionError("k=" + k + " " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Boundary] Duplicates And Extreme K (Author exercise)
<!-- id: sel-duplicates-extreme -->

**Approach.** A partition that keeps only strictly smaller values on the left and puts every other value on the right removes just the pivot from an array of equal values. Each round then shrinks the range by one, and the total cost is O(n^2). The fix is a three-way partition.

The three-way partition splits `a[lo..hi]` into three groups with boundaries `lt` and `gt`. Values below the pivot occupy `lo..lt-1`, values equal to it occupy `lt..gt`, and values above it occupy `gt+1..hi`. The scan index `i` separates the settled groups from the unread values `i..gt`. The method defines `lt`, `i` and `gt` before it swaps anything. After the scan, every index in `lt..gt` has the final value of the pivot, so a target inside that block is answered at once. Otherwise the range keeps the left or the right group. The invariant is that the range holds the values of sorted positions `lo..hi` and contains the target. With all equal values, one round settles the whole range, and the test counts the rounds to confirm it. Extreme ranks 0 and `n - 1` need no special case.

**Complexity.**

- **Time** is expected O(n), because each round scans the range once and an equal run leaves the range in one step.
- **Space** is O(1), because the method swaps inside the input and keeps five integers.

```java run
import java.util.Arrays;
import java.util.Random;

public final class DuplicatesSelect {
    static int rounds;   // counts partition rounds so the test can check the equal-values claim

    /**
     * Returns the value at sorted index r using a three-way partition.
     * Time: expected O(n), and one round when all values are equal.
     * Space: O(1) extra.
     * Invariant: r lies in lo..hi and a[lo..hi] holds the values of sorted positions lo..hi.
     */
    static int select(int[] a, int r) {
        int lo = 0, hi = a.length - 1;
        // The range always contains r, so the loop stops when the equal block covers r.
        while (lo <= hi) {
            rounds++;
            // Overflow-safe middle value as the pivot.
            int pivot = a[lo + (hi - lo) / 2];
            // Boundaries are defined before any swap: a[lo..lt-1] < pivot, a[gt+1..hi] > pivot.
            int lt = lo, i = lo, gt = hi;
            // Scan the unread values i..gt exactly once.
            while (i <= gt) {
                if (a[i] < pivot) {
                    swap(a, lt++, i++);       // smaller value joins the left group
                } else if (a[i] > pivot) {
                    swap(a, i, gt--);         // larger value joins the right group; i stays to re-read the swapped value
                } else {
                    i++;                      // equal value stays in the middle block
                }
            }
            // A target inside lt..gt already holds the pivot value.
            if (r < lt) hi = lt - 1;
            else if (r > gt) lo = gt + 1;
            else return pivot;
        }
        // Unreachable, because the range always contains r.
        throw new AssertionError("range lost the target");
    }

    static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (select(new int[]{6, 6, 6, 6, 6}, 3) != 6) throw new AssertionError("example 1");
        if (select(new int[]{2, 9, 2, 2, 5, 2, 9}, 4) != 5) throw new AssertionError("example 2");
        // Checks that an array of equal values needs a single round, even for large n.
        int[] same = new int[100_000];
        Arrays.fill(same, 7);
        rounds = 0;
        if (select(same, 99_999) != 7) throw new AssertionError("all equal");
        if (rounds != 1) throw new AssertionError("rounds " + rounds);
        // Checks all ranks against a sorted copy on random arrays with few distinct values.
        Random rnd = new Random(322);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(30);
            int distinct = 1 + rnd.nextInt(4);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(distinct) * 3 - 3;
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            for (int r = 0; r < n; r++) {
                if (select(a.clone(), r) != sorted[r]) throw new AssertionError("rank " + r + " of " + Arrays.toString(a));
            }
        }
    }
}
```

#### Solution: [Recognize] K Closest Points To Origin (LeetCode 973)
<!-- id: sel-k-closest-points -->

**Approach.** The `k` closest points are the points with the `k` smallest squared distances, and the square root is not needed because it preserves order. The method selects index `k - 1` by quickselect on the squared distance, and then the first `k` entries of the array are the answer.

A squared distance `x*x + y*y` reaches 2 * 10^18 for coordinates of 10^9, which exceeds the `int` range but fits in `long`. The key function therefore widens each coordinate to `long` before multiplying. The invariant is the same as before: after the partition loop for target index `k - 1`, every entry in `0..k-1` has a key not larger than every entry in `k..n-1`. The method swaps whole point references and passes bounds, so it copies no coordinates during the search.

**Complexity.**

- **Time** is expected O(n) when distances are mostly distinct, and O(n^2) when many points tie under this two-way partition, because each round scans the surviving range and computes two `long` products per point.
- **Space** is O(1) extra beyond the returned array of `k` references.

```java run
import java.util.Arrays;
import java.util.Random;

public final class KClosest {
    /** Returns the squared distance to the origin as a long, so the sum cannot overflow. */
    static long key(int[] pt) {
        // Widening before the multiplication prevents int overflow.
        return (long) pt[0] * pt[0] + (long) pt[1] * pt[1];
    }

    /**
     * Returns the k points with the smallest squared distance, in any order.
     * Time: expected O(n).
     * Space: O(k) for the result, O(1) extra otherwise.
     * Invariant: k - 1 lies in lo..hi and points[lo..hi] holds the keys of sorted positions lo..hi.
     */
    static int[][] kClosest(int[][] points, int k) {
        int target = k - 1;
        int lo = 0, hi = points.length - 1;
        // Each round discards the side that cannot hold the cutoff index.
        while (lo < hi) {
            int p = partition(points, lo, hi);
            if (p == target) break;
            if (target < p) hi = p - 1;
            else lo = p + 1;
        }
        // Entries 0..k-1 now hold the k smallest keys.
        return Arrays.copyOfRange(points, 0, k);
    }

    /** Places the middle point at its final rank by key and returns that rank. */
    static int partition(int[][] a, int lo, int hi) {
        int mid = lo + (hi - lo) / 2;
        swap(a, mid, hi);
        long pivot = key(a[hi]);
        // Boundary of the smaller group, defined before the scan swaps anything.
        int store = lo;
        for (int i = lo; i < hi; i++) {
            if (key(a[i]) < pivot) {
                swap(a, i, store);
                store++;
            }
        }
        swap(a, store, hi);
        return store;
    }

    static void swap(int[][] a, int i, int j) {
        int[] t = a[i]; a[i] = a[j]; a[j] = t;
    }

    static long[] sortedKeys(int[][] pts) {
        long[] keys = new long[pts.length];
        for (int i = 0; i < pts.length; i++) keys[i] = key(pts[i]);
        Arrays.sort(keys);
        return keys;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        int[][] r1 = kClosest(new int[][]{{3, 3}, {5, -1}, {-2, 4}}, 2);
        if (!Arrays.equals(sortedKeys(r1), new long[]{18, 20})) throw new AssertionError("example 1");
        int[][] r2 = kClosest(new int[][]{{1_000_000_000, 1_000_000_000}, {1, 1}, {-1, 2}}, 2);
        if (!Arrays.equals(sortedKeys(r2), new long[]{2, 5})) throw new AssertionError("example 2");
        // Checks that int arithmetic would overflow while the long key is exact.
        int x = 1_000_000_000;
        if ((long) (x * x) == (long) x * x) throw new AssertionError("int product should overflow");
        if (key(new int[]{x, x}) != 2_000_000_000_000_000_000L) throw new AssertionError("long key");
        // Checks the selected keys against a full sort on random points, including ties and large values.
        Random rnd = new Random(973);
        for (int round = 0; round < 500; round++) {
            int n = 1 + rnd.nextInt(25);
            int[][] pts = new int[n][2];
            for (int i = 0; i < n; i++) {
                boolean large = rnd.nextInt(5) == 0;
                pts[i][0] = large ? (rnd.nextInt(3) - 1) * 1_000_000_000 : rnd.nextInt(11) - 5;
                pts[i][1] = large ? (rnd.nextInt(3) - 1) * 1_000_000_000 : rnd.nextInt(11) - 5;
            }
            int k = 1 + rnd.nextInt(n);
            long[] expected = Arrays.copyOf(sortedKeys(pts), k);
            int[][] got = kClosest(pts.clone(), k);
            if (got.length != k) throw new AssertionError("length");
            if (!Arrays.equals(sortedKeys(got), expected)) throw new AssertionError("keys differ, k=" + k);
        }
    }
}
```
