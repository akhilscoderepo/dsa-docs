<!-- solutions-for: 06-randomized-partitioning -->
### Solutions For Randomized Partitioning

#### Solution: [Build] Uniform Pivot Index (Author exercise)
<!-- id: rp35-uniform-pivot-index -->

**Approach.**
An inclusive range from `lo` to `hi` holds `hi - lo + 1` positions, so the draw bound is that count and not `hi - lo`. The bound `hi - lo` would make the last position unreachable. The method checks `lo <= hi` first, calls `pick` once, validates that the offset is within 0 to `hi - lo`, and returns `lo + d`. Under the constraint `hi <= 10^9`, the count fits in an `int`. The invariant is that the returned position lies in `[lo, hi]` and every position has the same chance when `pick` is uniform.

The program runs every offset for random ranges and checks that every position in the range is returned exactly once. It also checks the error paths and that a call with a bad range never calls `pick`.

**Complexity.**
- **Time** is O(1).
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class UniformPivotIndexBuild {
    /**
     * Returns a pivot position drawn from the inclusive range [lo, hi].
     * Time: O(1). Space: O(1).
     * Invariant: the result lies in [lo, hi].
     */
    static int pivotIndex(int lo, int hi, IntUnaryOperator pick) {
        if (lo > hi) throw new IllegalArgumentException("empty range"); // checked before any draw
        int d = pick.applyAsInt(hi - lo + 1); // the range holds hi - lo + 1 positions
        if (d < 0 || d > hi - lo) throw new IllegalStateException("draw out of range");
        return lo + d; // offset from the left end
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        int[] bound = {0};
        if (pivotIndex(3, 7, b -> { bound[0] = b; return 4; }) != 7 || bound[0] != 5) throw new AssertionError("ex1");
        if (pivotIndex(5, 5, b -> { bound[0] = b; return 0; }) != 5 || bound[0] != 1) throw new AssertionError("ex2");
        // empty range: no draw happens
        boolean threw = false;
        try { pivotIndex(4, 3, b -> { throw new AssertionError("pick must not run"); }); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("empty range");
        // out-of-range draws are rejected
        threw = false;
        try { pivotIndex(2, 4, b -> 3); } catch (IllegalStateException e) { threw = true; }
        if (!threw) throw new AssertionError("bad draw");
        // every position of a random range is reachable exactly once
        Random rnd = new Random(71);
        for (int t = 0; t < 200; t++) {
            int lo = rnd.nextInt(50), hi = lo + rnd.nextInt(20);
            boolean[] seen = new boolean[hi - lo + 1];
            for (int d = 0; d <= hi - lo; d++) {
                final int dd = d;
                int p = pivotIndex(lo, hi, b -> dd);
                if (p < lo || p > hi || seen[p - lo]) throw new AssertionError("range or duplicate");
                seen[p - lo] = true;
            }
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Randomized Quickselect (Author exercise)
<!-- id: rp35-randomized-quickselect -->

**Approach.**
Each round draws the pivot position, swaps the pivot to the end of the active range and scans the rest of the range once. A value below the pivot goes to the next free slot at the front, and the pivot then swaps into the slot after the last smaller value. That slot, `store`, is the pivot's final index in sorted order. If `store` equals the wanted index `k - 1`, the loop returns. If the wanted index is smaller, the range shrinks to the part before `store`, and otherwise to the part after it. The part that is dropped never contains the wanted index, so the answer stays inside the active range. The invariant is that every value left of `lo` is no larger than every value in the range, and every value right of `hi` is no smaller.

The program compares the method with a sort on random arrays that include repeats. It also checks the lesson's claim about the last-element rule: on a sorted array the last-pivot version makes exactly `n(n - 1) / 2` comparisons, and the random version makes far fewer on the same input.

**Complexity.**
- **Time** is O(n) expected for any input order and O(n^2) in the worst case.
- **Space** is O(1), because the method works in place.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class RandomizedQuickselectVary {
    static long compares; // number of element comparisons in the last run

    /**
     * Returns the k-th smallest value, rearranging a.
     * Time: O(n) expected. Space: O(1).
     * Invariant: the wanted index stays inside [lo, hi].
     */
    static int kthSmallest(int[] a, int k, IntUnaryOperator pick) {
        int lo = 0, hi = a.length - 1, target = k - 1;
        while (true) {
            int p = lo + pick.applyAsInt(hi - lo + 1); // pivot position, inclusive range
            int pv = a[p];
            a[p] = a[hi]; a[hi] = pv; // park the pivot at the end of the range
            int store = lo;
            for (int j = lo; j < hi; j++) {
                compares++;
                if (a[j] < pv) { int t = a[store]; a[store] = a[j]; a[j] = t; store++; } // smaller values go to the front
            }
            int t = a[store]; a[store] = a[hi]; a[hi] = t; // the pivot reaches its final index
            if (store == target) return a[store];
            if (target < store) hi = store - 1; else lo = store + 1; // keep the side with the target
        }
    }

    static int lastPivot(int[] a, int k) {
        return kthSmallest(a, k, bound -> bound - 1); // offset bound - 1 is always the last position
    }

    static IntUnaryOperator script(int... d) {
        int[] at = {0};
        return b -> d[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (kthSmallest(new int[]{7, 2, 9, 4, 1}, 2, script(0, 1)) != 2) throw new AssertionError("ex1");
        if (kthSmallest(new int[]{9, 4, 7, 4, 1, 8}, 3, script(0, 1, 1)) != 4) throw new AssertionError("ex2");
        // random arrays with repeats agree with a sort
        Random rnd = new Random(72);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(30)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(12);
            int k = 1 + rnd.nextInt(a.length);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            if (kthSmallest(a.clone(), k, bound -> rnd.nextInt(bound)) != sorted[k - 1]) throw new AssertionError("random");
        }
        // sorted input: the last-element rule makes n(n-1)/2 comparisons for k = 1, the random rule far fewer
        for (int n : new int[]{8, 100, 2000}) {
            int[] sorted = new int[n];
            for (int i = 0; i < n; i++) sorted[i] = i;
            compares = 0;
            if (lastPivot(sorted.clone(), 1) != 0) throw new AssertionError("last pivot answer");
            if (compares != (long) n * (n - 1) / 2) throw new AssertionError("quadratic count " + compares);
            compares = 0;
            kthSmallest(sorted.clone(), 1, bound -> rnd.nextInt(bound));
            if (n == 2000 && compares > 20L * n) throw new AssertionError("random rule too slow: " + compares);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Equal Values (Author exercise)
<!-- id: rp35-equal-values -->

**Approach.**
The method keeps three indices over the active range. Positions from `lo` to `lt - 1` hold values below the pivot value, positions from `lt` to `i - 1` hold values equal to it, and positions from `gt + 1` to `hi` hold values above it. The scan examines position `i`. A smaller value swaps with the first equal position and both `lt` and `i` advance. A larger value swaps with the last unexamined position and only `gt` moves, so `i` stays to examine the swapped-in value. An equal value advances `i`. When `i` passes `gt`, the three bands cover the range. If the wanted index lies inside `[lt, gt]`, the pivot value is the answer. Otherwise the range shrinks to the below band or the above band, and the equal band leaves at once. An array of equal values forms a single equal band, so the first round returns. The invariant is that the three bands plus the unexamined part always cover `[lo, hi]` without overlap.

The program compares the method with a sort, checks the two examples, and checks that an array of 100000 equal values returns after one round. It also counts comparisons of the two-way rule from the previous exercise on equal values and confirms the `n(n - 1) / 2` growth that the lesson warns about.

**Complexity.**
- **Time** is O(n) expected, and an array of equal values costs O(n) in one round.
- **Space** is O(1).

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class EqualValuesBoundary {
    /**
     * Returns {value, rounds} for the k-th smallest value with a three-way partition.
     * Time: O(n) expected. Space: O(1).
     * Invariant: [lo, lt) is below pv, [lt, i) equals pv, (gt, hi] is above pv.
     */
    static int[] kthSmallestThreeWay(int[] a, int k, IntUnaryOperator pick) {
        int lo = 0, hi = a.length - 1, target = k - 1, rounds = 0;
        while (true) {
            rounds++;
            int pv = a[lo + pick.applyAsInt(hi - lo + 1)];
            int lt = lo, i = lo, gt = hi;
            while (i <= gt) { // each pass examines one position
                if (a[i] < pv) { int t = a[lt]; a[lt] = a[i]; a[i] = t; lt++; i++; } // grow the below band
                else if (a[i] > pv) { int t = a[i]; a[i] = a[gt]; a[gt] = t; gt--; } // the swapped-in value is still unexamined
                else i++; // grow the equal band
            }
            if (target < lt) hi = lt - 1; // continue in the below band
            else if (target > gt) lo = gt + 1; // continue in the above band
            else return new int[]{pv, rounds}; // the target is in the equal band
        }
    }

    static long twoWayCompares(int[] a, int k) {
        long compares = 0;
        int lo = 0, hi = a.length - 1, target = k - 1;
        while (true) {
            int pv = a[hi], store = lo; // last-element pivot with the two-way rule
            for (int j = lo; j < hi; j++) { compares++; if (a[j] < pv) { int t = a[store]; a[store] = a[j]; a[j] = t; store++; } }
            int t = a[store]; a[store] = a[hi]; a[hi] = t;
            if (store == target) return compares;
            if (target < store) hi = store - 1; else lo = store + 1;
        }
    }

    static IntUnaryOperator script(int... d) {
        int[] at = {0};
        return b -> d[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        int[] r1 = kthSmallestThreeWay(new int[]{3, 1, 3, 2, 3}, 4, script(1, 0));
        if (r1[0] != 3 || r1[1] != 2) throw new AssertionError("ex1");
        int[] r2 = kthSmallestThreeWay(new int[]{4, 4, 4, 4, 4}, 3, script(0));
        if (r2[0] != 4 || r2[1] != 1) throw new AssertionError("ex2");
        // random arrays with many repeats agree with a sort
        Random rnd = new Random(73);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(30)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(4);
            int k = 1 + rnd.nextInt(a.length);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            if (kthSmallestThreeWay(a, k, bound -> rnd.nextInt(bound))[0] != sorted[k - 1]) throw new AssertionError("random");
        }
        // 100000 equal values need one round
        int[] same = new int[100_000];
        Arrays.fill(same, 9);
        if (kthSmallestThreeWay(same, 50_000, bound -> rnd.nextInt(bound))[1] != 1) throw new AssertionError("one round");
        // the two-way rule makes n(n-1)/2 comparisons on equal values
        int[] equal = new int[1000];
        Arrays.fill(equal, 5);
        if (twoWayCompares(equal, 1000) != 1000L * 999 / 2) throw new AssertionError("two-way growth");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Kth Largest Element In An Array (LeetCode 215)
<!-- id: rp35-kth-largest -->

**Approach.**
The k-th largest value of `n` numbers has the 0-based index `n - k` in ascending order, so the problem is a selection of ascending rank `n - k`. The method uses the three-way randomized loop from the previous exercise with that target. Expected time is O(n) because each draw is good with probability one half whatever the input order is, and a good draw leaves at most three quarters of the range. The worst case is O(n^2), reached only when most draws are extreme, and its probability falls quickly with `n`. Equal values leave the loop at once, because they form the equal band. The invariant is that the target index stays inside the active range after every round.

The program compares the method with a sort on random arrays and checks both examples. It also measures the work on a sorted array of 20000 values and on its reverse, with a seeded generator, and confirms that the number of pivot-scan comparisons stays below 12 times the length, so input order does not matter.

**Complexity.**
- **Time** is O(n) expected and O(n^2) in the worst case.
- **Space** is O(1) beyond the rearranged input.

```java run
import java.util.Arrays;
import java.util.Random;
import java.util.function.IntUnaryOperator;

public final class KthLargestRecognize {
    static long scans; // number of positions examined in all rounds

    /**
     * Returns the k-th largest value, rearranging nums.
     * Time: O(n) expected, O(n^2) worst case. Space: O(1).
     * Invariant: the target index n - k stays inside [lo, hi].
     */
    static int findKthLargest(int[] nums, int k, IntUnaryOperator pick) {
        int lo = 0, hi = nums.length - 1, target = nums.length - k; // ascending index of the k-th largest
        while (true) {
            int pv = nums[lo + pick.applyAsInt(hi - lo + 1)];
            int lt = lo, i = lo, gt = hi;
            while (i <= gt) { // three-way scan
                scans++;
                if (nums[i] < pv) { int t = nums[lt]; nums[lt] = nums[i]; nums[i] = t; lt++; i++; }
                else if (nums[i] > pv) { int t = nums[i]; nums[i] = nums[gt]; nums[gt] = t; gt--; }
                else i++;
            }
            if (target < lt) hi = lt - 1; else if (target > gt) lo = gt + 1; else return pv;
        }
    }

    static IntUnaryOperator script(int... d) {
        int[] at = {0};
        return b -> d[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (findKthLargest(new int[]{9, 4, 7, 4, 1, 8}, 3, script(0, 1)) != 7) throw new AssertionError("ex1");
        if (findKthLargest(new int[]{6, 6, 2, 6, 3}, 2, script(2, 0)) != 6) throw new AssertionError("ex2");
        // random arrays with repeats and negative values agree with a sort
        Random rnd = new Random(74);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(30)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(15) - 7;
            int k = 1 + rnd.nextInt(a.length);
            int[] sorted = a.clone();
            Arrays.sort(sorted);
            if (findKthLargest(a, k, bound -> rnd.nextInt(bound)) != sorted[sorted.length - k]) throw new AssertionError("random");
        }
        // sorted and reversed input do the same expected work
        int n = 20_000;
        int[] up = new int[n], down = new int[n];
        for (int i = 0; i < n; i++) { up[i] = i; down[i] = n - i; }
        scans = 0;
        findKthLargest(up, n / 2, bound -> rnd.nextInt(bound));
        long upScans = scans;
        scans = 0;
        findKthLargest(down, n / 2, bound -> rnd.nextInt(bound));
        long downScans = scans;
        if (upScans > 12L * n || downScans > 12L * n) throw new AssertionError("too many scans " + upScans + " " + downScans);
        System.out.println("ok");
    }
}
```
