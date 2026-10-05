<!-- solutions-for: 06-binary-search -->
### Solutions For Whole Number Answers

#### Solution: [Build] Eating Speed For All Piles (LeetCode 875)
<!-- id: bs-int-eating-speed -->

**Approach.**
The hours needed at speed `k` never increase when `k` grows, so the check "all piles fit in `h` hours" is false up to a boundary and true after it. The largest pile always passes, because every pile then takes one hour and `h` is at least the pile count. The search keeps `hi` as a passing speed and `lo` as the lowest speed not yet excluded. A passing `mid` lowers `hi` to `mid`, and a failing `mid` raises `lo` to `mid + 1`. The check sums rounded-up hours in a `long`, so large piles cannot overflow. The loop ends when `lo == hi`.

**Complexity.**
- **Time** is O(n log m) for `n` piles and a largest pile `m`, since the loop makes about log2(m) checks and each reads `n` piles.
- **Space** is O(1), because only two bounds and one running total are stored.

```java run
import java.util.Random;

public final class EatingSpeed875 {
    /**
     * Returns the smallest speed that empties all piles within h hours.
     * Time: O(n log m). Space: O(1).
     * Invariant: hi passes the check and every speed below lo fails it.
     */
    static int minSpeed(int[] piles, int h) {
        int lo = 1, hi = 1;
        // The largest pile is a passing speed, since each pile then costs one hour.
        for (int p : piles) hi = Math.max(hi, p);
        // Each round halves the range [lo, hi], so about log2(m) rounds run.
        while (lo < hi) {
            // The midpoint stays below hi when lo < hi, and the form avoids int overflow.
            int mid = lo + (hi - lo) / 2;
            // A passing mid can be the answer, so hi keeps it.
            if (hours(piles, mid) <= h) hi = mid;
            // A failing mid cannot be the answer, so lo moves past it.
            else lo = mid + 1;
        }
        // lo == hi is the lowest passing speed.
        return lo;
    }

    /** Hours at speed k; Time O(n), Space O(1). A long total avoids overflow. */
    static long hours(int[] piles, int k) {
        long used = 0;
        // Each pile costs ceil(pile / k) hours, computed without floating point.
        for (int p : piles) used += (p + (long) k - 1) / k;
        return used;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (minSpeed(new int[]{5, 9, 14, 20}, 9) != 7) throw new AssertionError("example 1");
        if (minSpeed(new int[]{4, 4, 4}, 3) != 4) throw new AssertionError("example 2");
        // Large piles: the total of hours stays correct in long arithmetic.
        if (minSpeed(new int[]{1_000_000_000, 1_000_000_000}, 2) != 1_000_000_000) throw new AssertionError("large");
        // Random inputs against a scan over every speed.
        Random rnd = new Random(81);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(6);
            int[] p = new int[n];
            for (int i = 0; i < n; i++) p[i] = 1 + rnd.nextInt(30);
            int h = n + rnd.nextInt(25), expect = 1;
            while (hours(p, expect) > h) expect++;
            if (minSpeed(p, h) != expect) throw new AssertionError("random " + java.util.Arrays.toString(p) + " " + h);
        }
    }
}
```

#### Solution: [Vary] Capacity For Shipping In Order (LeetCode 1011)
<!-- id: bs-int-ship-capacity -->

**Approach.**
A capacity below the heaviest package cannot carry it, and the total weight carries everything in one day, so the answer lies in `[max, sum]`. A greedy pass loads packages in order and starts a new day when the next package does not fit. Greedy loading uses the fewest days for a given capacity, so the day count never grows when capacity grows, and the check is monotone. The search keeps `hi` as a passing capacity. A passing `mid` lowers `hi`, and a failing `mid` raises `lo`. Starting `lo` at the heaviest package prevents a capacity that skips a package.

**Complexity.**
- **Time** is O(n log S) for total weight `S`, because each check reads the packages once and the range has `S` values.
- **Space** is O(1), because the pass keeps a day counter and a running load.

```java run
import java.util.Random;

public final class ShipCapacity1011 {
    /**
     * Returns the smallest capacity that ships all packages in order within the given days.
     * Time: O(n log S). Space: O(1).
     * Invariant: hi ships within days and every capacity below lo does not.
     */
    static int minCapacity(int[] w, int days) {
        int lo = 0, hi = 0;
        // The range starts at the heaviest package and ends at the total weight.
        for (int x : w) { lo = Math.max(lo, x); hi += x; }
        // Each round halves the range, so about log2(S) rounds run.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A passing mid stays as the upper bound.
            if (daysNeeded(w, mid) <= days) hi = mid;
            // A failing mid is excluded.
            else lo = mid + 1;
        }
        return lo;
    }

    /** Days a greedy in-order loading needs; Time O(n), Space O(1). */
    static int daysNeeded(int[] w, int cap) {
        int d = 1, load = 0;
        for (int x : w) {
            // A package that does not fit starts the next day.
            if (load + x > cap) { d++; load = 0; }
            // The package joins the current day.
            load += x;
        }
        return d;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {4, 2, 7, 1, 5, 3};
        if (minCapacity(a, 3) != 8) throw new AssertionError("example 1");
        if (minCapacity(a, 1) != 22) throw new AssertionError("example 2");
        // One package per day forces the capacity to the heaviest package.
        if (minCapacity(a, 6) != 7) throw new AssertionError("max package");
        // Random inputs against a scan over every capacity.
        Random rnd = new Random(82);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] w = new int[n];
            for (int i = 0; i < n; i++) w[i] = 1 + rnd.nextInt(12);
            int days = 1 + rnd.nextInt(n), cap = 1;
            while (daysNeeded(w, cap) > days || cap < java.util.Arrays.stream(w).max().getAsInt()) cap++;
            if (minCapacity(w, days) != cap) throw new AssertionError("random " + java.util.Arrays.toString(w) + " " + days);
        }
    }
}
```

#### Solution: [Boundary] Days To Make Bouquets (LeetCode 1482)
<!-- id: bs-int-bouquets -->

**Approach.**
Making `m` bouquets needs `m * k` flowers, and the row has fewer when `m * k` exceeds its length, so no day works and the method returns `-1` before any search. The product is computed in `long`, because `m` and `k` can each be near 10^9. Otherwise the last bloom day is a passing day. The check counts runs of `k` adjacent flowers that have bloomed by a day `d`, and a larger `d` never lowers that count. The search then returns the lowest passing day within `[min, max]` of the bloom days.

**Complexity.**
- **Time** is O(n log D) for a day range of size `D`, because each check scans the row once.
- **Space** is O(1), because the scan keeps a run length and a bouquet count.

```java run
import java.util.Random;

public final class Bouquets1482 {
    /**
     * Returns the earliest day with m bouquets of k adjacent flowers, or -1.
     * Time: O(n log D). Space: O(1).
     * Invariant: hi allows m bouquets and every day below lo does not.
     */
    static int minDays(int[] bloom, int m, int k) {
        // Demand is compared in long, since m * k can pass the int range.
        if ((long) m * k > bloom.length) return -1;
        int lo = Integer.MAX_VALUE, hi = 0;
        for (int b : bloom) { lo = Math.min(lo, b); hi = Math.max(hi, b); }
        // Each round halves the day range.
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A passing day stays as the upper bound.
            if (bouquets(bloom, mid, k) >= m) hi = mid; else lo = mid + 1;
        }
        return lo;
    }

    /** Bouquets formed by day d; Time O(n), Space O(1). */
    static int bouquets(int[] bloom, int d, int k) {
        int made = 0, run = 0;
        for (int b : bloom) {
            // A bloomed flower extends the run, and a full run closes one bouquet.
            if (b <= d) { if (++run == k) { made++; run = 0; } }
            // An unbloomed flower breaks adjacency.
            else run = 0;
        }
        return made;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (minDays(new int[]{7, 3, 9, 3, 7, 8, 3}, 2, 3) != 9) throw new AssertionError("example 1");
        if (minDays(new int[]{7, 3, 9, 3, 7}, 2, 3) != -1) throw new AssertionError("example 2");
        // Demand beyond the int range must not wrap around to a small product.
        if (minDays(new int[]{1, 2, 3}, 1_000_000_000, 1_000_000_000) != -1) throw new AssertionError("overflow");
        // Random inputs against a scan over every day.
        Random rnd = new Random(83);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] b = new int[n];
            for (int i = 0; i < n; i++) b[i] = 1 + rnd.nextInt(10);
            int m = 1 + rnd.nextInt(3), k = 1 + rnd.nextInt(3), expect = -1;
            for (int d = 1; d <= 10 && expect < 0; d++) if (bouquets(b, d, k) >= m) expect = d;
            if (minDays(b, m, k) != expect) throw new AssertionError("random " + java.util.Arrays.toString(b) + " " + m + " " + k);
        }
    }
}
```

#### Solution: [Recognize] Split Into Smallest Largest Sum (LeetCode 410)
<!-- id: bs-int-split-array -->

**Approach.**
The candidate is a ceiling `c` on the sum of any part. A greedy pass adds elements to the current part until the next element would pass `c`, and then it opens a new part. This pass uses the fewest parts for the ceiling `c`. If it uses at most `k` parts, a split into exactly `k` parts also respects `c`, because a part with two or more elements can be cut without raising any sum. The check is monotone in `c`. The range runs from the largest element, which no part can avoid, to the total sum, which one part carries.

**Complexity.**
- **Time** is O(n log S) for total sum `S`, because each check reads the array once.
- **Space** is O(1), because the pass keeps a part count and a running sum.

```java run
import java.util.Random;

public final class SplitArray410 {
    /**
     * Returns the smallest possible largest part sum over splits into k non-empty parts.
     * Time: O(n log S). Space: O(1).
     * Invariant: hi allows at most k parts and every ceiling below lo needs more.
     */
    static int splitLargest(int[] nums, int k) {
        int lo = 0, hi = 0;
        // The range runs from the largest element to the total sum.
        for (int x : nums) { lo = Math.max(lo, x); hi += x; }
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            // A ceiling that needs at most k parts passes and stays as the upper bound.
            if (parts(nums, mid) <= k) hi = mid; else lo = mid + 1;
        }
        return lo;
    }

    /** Parts a greedy pass needs for ceiling c; Time O(n), Space O(1). */
    static int parts(int[] nums, int c) {
        int p = 1, sum = 0;
        for (int x : nums) {
            // An element that would pass the ceiling opens a new part.
            if (sum + x > c) { p++; sum = 0; }
            sum += x;
        }
        return p;
    }

    /** Brute force over every way to place k - 1 cuts. */
    static int brute(int[] a, int k, int from, int left) {
        if (left == 1) { int s = 0; for (int i = from; i < a.length; i++) s += a[i]; return s; }
        int best = Integer.MAX_VALUE, s = 0;
        // Each choice ends the current part at index i and leaves enough elements for the rest.
        for (int i = from; i <= a.length - left; i++) {
            s += a[i];
            best = Math.min(best, Math.max(s, brute(a, k, i + 1, left - 1)));
        }
        return best;
    }

    public static void main(String[] args) {
        // The statement examples.
        int[] a = {4, 9, 3, 8, 6};
        if (splitLargest(a, 3) != 13) throw new AssertionError("example 1");
        if (splitLargest(a, 5) != 9) throw new AssertionError("example 2");
        if (splitLargest(a, 1) != 30) throw new AssertionError("one part");
        // Random inputs against exhaustive cut placement.
        Random rnd = new Random(84);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(8);
            int[] x = new int[n];
            for (int i = 0; i < n; i++) x[i] = rnd.nextInt(15);
            int k = 1 + rnd.nextInt(n);
            if (splitLargest(x, k) != brute(x, k, 0, k)) throw new AssertionError("random " + java.util.Arrays.toString(x) + " " + k);
        }
    }
}
```
