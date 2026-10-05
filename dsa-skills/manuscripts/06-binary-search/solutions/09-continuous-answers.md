<!-- solutions-for: 06-binary-search -->
### Solutions For Real Number Answers

#### Solution: [Build] Square Root By Bisection (Author exercise)
<!-- id: bs-real-sqrt -->

**Approach.**
The test "mid squared is at least x" fails below the root and passes at and above it. The interval starts at `[0, max(1, x)]`, where `hi` passes, because for `x >= 1` the value `x` has a square at least `x`, and for `x < 1` the value 1 has a square of 1. Each round replaces one end by the midpoint, which halves the width. After 100 rounds the width is at most `max(1, x) / 2^100`, so `hi` is within the tolerance. The loop uses a round count and not a width comparison, so it always ends.

**Complexity.**
- **Time** is O(t) for a round count `t`, here 100, because each round does one multiplication and one comparison.
- **Space** is O(1), because the search keeps two doubles and a counter.

```java run
import java.util.Random;

public final class SqrtBisection {
    /**
     * Returns a value within 1e-6 of sqrt(x) for 0 <= x <= 1e9.
     * Time: O(t) for t = 100 rounds. Space: O(1).
     * Invariant: lo * lo < x <= hi * hi, or lo == 0 when x == 0.
     */
    static double root(double x) {
        double lo = 0, hi = Math.max(1, x);
        // A fixed count always ends, and 100 halvings shrink the width below any double spacing here.
        for (int round = 0; round < 100; round++) {
            double mid = lo + (hi - lo) / 2;
            // A passing midpoint is the new upper end.
            if (mid * mid >= x) hi = mid;
            // A failing midpoint is the new lower end, and it is never skipped past.
            else lo = mid;
        }
        return hi;
    }

    public static void main(String[] args) {
        // The statement examples as intervals.
        double r = root(2);
        if (r < 1.414212 || r > 1.414215) throw new AssertionError("example 1 " + r);
        r = root(0.25);
        if (r < 0.499999 || r > 0.500001) throw new AssertionError("example 2 " + r);
        // Zero returns a value within the tolerance of 0.
        if (Math.abs(root(0)) > 1e-6) throw new AssertionError("zero");
        // Random inputs against Math.sqrt as the oracle.
        Random rnd = new Random(91);
        for (int t = 0; t < 4000; t++) {
            double x = rnd.nextInt(4) == 0 ? rnd.nextDouble() : rnd.nextDouble() * 1e9;
            if (Math.abs(root(x) - Math.sqrt(x)) > 1e-6) throw new AssertionError("random " + x);
        }
    }
}
```

#### Solution: [Vary] Widest Gap Between Points (Author exercise)
<!-- id: bs-real-widest-gap -->

**Approach.**
For a gap `d`, a greedy pass places the first point at the start of the first interval and each next point as early as the gap and the interval allow. In an interval with first usable position `f`, the pass fits `floor((b - f) / d) + 1` points and records the last one. Placing points as early as possible never loses a point, so the pass counts the maximum number that fit. The count does not grow when `d` grows, so the check is monotone. The search keeps `lo` as a gap that fits `k` points and `hi` as a gap that does not. A fitting midpoint becomes `lo`, and a failing midpoint becomes `hi`, because the answer is the largest fitting gap.

**Complexity.**
- **Time** is O(n * t) for `n` intervals and `t` rounds, because each check reads every interval once and does constant work for it.
- **Space** is O(1), because the pass keeps the last position and a count.

```java run
import java.util.Random;

public final class WidestGap {
    /**
     * Returns the largest smallest distance among k points chosen inside the intervals.
     * Time: O(n * t). Space: O(1).
     * Invariant: gap lo fits k points and gap hi does not.
     */
    static double widest(int[][] iv, int k) {
        double lo = 0, hi = iv[iv.length - 1][1] - iv[0][0] + 1;
        // 100 rounds shrink the width far below the required error.
        for (int round = 0; round < 100; round++) {
            double mid = lo + (hi - lo) / 2;
            // A gap that fits k points is feasible and raises the lower end.
            if (count(iv, mid) >= k) lo = mid;
            // A gap that does not fit lowers the upper end.
            else hi = mid;
        }
        return lo;
    }

    /** Greedy count of points that fit with gap d; Time O(n), Space O(1). */
    static long count(int[][] iv, double d) {
        long total = 0;
        double last = Double.NEGATIVE_INFINITY;
        for (int[] seg : iv) {
            // The earliest allowed position is the segment start or the last point plus the gap.
            double first = Math.max(seg[0], last + d);
            // The segment holds no point when the earliest position is past its end.
            if (first > seg[1]) continue;
            long m = (long) Math.floor((seg[1] - first) / d);
            total += m + 1;
            last = first + m * d;
        }
        return total;
    }

    public static void main(String[] args) {
        int[][] a = {{0, 2}, {5, 6}, {9, 12}};
        // The statement examples.
        if (Math.abs(widest(a, 5) - 2.0) > 1e-6) throw new AssertionError("example 1");
        if (Math.abs(widest(a, 2) - 12.0) > 1e-6) throw new AssertionError("example 2");
        // One interval has the closed form (b - a) / (k - 1).
        if (Math.abs(widest(new int[][]{{0, 10}}, 4) - 10.0 / 3) > 1e-6) throw new AssertionError("single");
        // Random intervals: the gap fits just below the answer and not just above, and k = 2 spans the whole range.
        Random rnd = new Random(92);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(4), pos = 0;
            int[][] iv = new int[n][2];
            for (int i = 0; i < n; i++) {
                iv[i][0] = pos + (i == 0 ? 0 : 1 + rnd.nextInt(5));
                iv[i][1] = iv[i][0] + rnd.nextInt(8);
                pos = iv[i][1];
            }
            if (iv[n - 1][1] == iv[0][0]) continue;
            if (Math.abs(widest(iv, 2) - (iv[n - 1][1] - iv[0][0])) > 1e-6) throw new AssertionError("span");
            int k = 2 + rnd.nextInt(5);
            // The scan keeps the largest gap on a fine grid that still fits k points.
            double best = 0;
            for (double d = 0.001; d < 60; d += 0.001) if (count(iv, d) >= k) best = d;
            if (best == 0 && count(iv, 0.001) < k) continue;
            if (Math.abs(widest(iv, k) - best) > 2e-3) throw new AssertionError("grid " + k);
        }
    }
}
```

#### Solution: [Boundary] Relative Error For Tiny And Huge Roots (Author exercise)
<!-- id: bs-real-relative-error -->

**Approach.**
The root lies between 10^-6 and 10^6, so the worst case needs a width of at most 10^-15 when the answer is 10^-6. Starting from the interval `[0, max(1, x)]` of width at most 10^12, the width reaches 10^-15 after log2(10^27), about 90 rounds. A fixed count of 100 rounds covers every input with margin. The same count serves a root near 10^6, where the relative error is far below the limit. An absolute tolerance of 10^-6 would accept the answer 0 for the smallest input, which is why the count is derived from the relative tolerance.

**Complexity.**
- **Time** is O(t) for 100 rounds, because each round does one multiplication and one comparison.
- **Space** is O(1), because the search keeps two doubles.

```java run
import java.util.Random;

public final class RelativeRoot {
    /**
     * Returns r with |r - sqrt(x)| <= 1e-9 * sqrt(x) for 1e-12 <= x <= 1e12.
     * Time: O(t) for 100 rounds. Space: O(1).
     * Invariant: lo * lo < x <= hi * hi.
     */
    static double root(double x) {
        double lo = 0, hi = Math.max(1, x);
        // 100 halvings take a width of 1e12 below 1e-18, under the 1e-15 that the smallest root needs.
        for (int round = 0; round < 100; round++) {
            double mid = lo + (hi - lo) / 2;
            if (mid * mid >= x) hi = mid; else lo = mid;
        }
        return hi;
    }

    public static void main(String[] args) {
        // The statement examples as intervals.
        double a = root(1e-12);
        if (a < 0.000000999999999 || a > 0.000001000000001) throw new AssertionError("example 1 " + a);
        double b = root(1e12);
        if (b < 999999.999 || b > 1000000.001) throw new AssertionError("example 2 " + b);
        // An absolute tolerance of 1e-6 would accept 0 for the smallest input, but the relative limit does not.
        if (Math.abs(0 - Math.sqrt(1e-12)) <= 1e-9 * Math.sqrt(1e-12)) throw new AssertionError("zero is not accepted");
        // Random inputs spread over twenty-four orders of magnitude against Math.sqrt.
        Random rnd = new Random(93);
        for (int t = 0; t < 4000; t++) {
            double x = Math.pow(10, -12 + 24 * rnd.nextDouble());
            double s = Math.sqrt(x);
            if (Math.abs(root(x) - s) > 1e-9 * s) throw new AssertionError("random " + x);
        }
    }
}
```

#### Solution: [Recognize] Count The Bisection Rounds (Author exercise)
<!-- id: bs-real-round-count -->

**Approach.**
After `t` rounds the width is `w / 2^t`. The smallest `t` with `w / 2^t <= eps` is found by halving a copy of the width and counting the halvings. A division of a `double` by 2 changes only the exponent, so it is exact and the comparison with `eps` has no rounding error from the loop. The result is also the number of rounds a bisection needs for a start width `w`. A count of 100 is a policy, because a width that reaches the spacing of two neighboring `double` values makes the midpoint equal to an end, and further rounds change nothing.

**Complexity.**
- **Time** is O(t), where `t` is the returned count and is at most about 80 for the allowed limits.
- **Space** is O(1), because the loop keeps the copied width and the counter.

```java run
public final class RoundCount {
    /**
     * Returns the smallest t with w / 2^t <= eps.
     * Time: O(t). Space: O(1).
     * Invariant: width equals w / 2^t after t halvings.
     */
    static int rounds(double w, double eps) {
        int t = 0;
        double width = w;
        // Halving a double is exact, so the loop compares exact values.
        while (width > eps) { width /= 2; t++; }
        return t;
    }

    public static void main(String[] args) {
        // The statement examples.
        if (rounds(10, 1e-6) != 24) throw new AssertionError("example 1");
        if (rounds(1, 1e-3) != 10) throw new AssertionError("example 2");
        // The returned count meets the tolerance and one fewer does not.
        for (double w : new double[]{1, 7, 1e6, 1e12}) {
            for (double eps : new double[]{1e-12, 1e-6, 0.5}) {
                if (eps > w) continue;
                int t = rounds(w, eps);
                if (w / Math.pow(2, t) > eps) throw new AssertionError("too few " + w + " " + eps);
                if (t > 0 && w / Math.pow(2, t - 1) <= eps) throw new AssertionError("not smallest " + w + " " + eps);
            }
        }
        // The count of 100 is only a policy: once the width reaches the spacing of two doubles, the midpoint equals an end.
        double lo = 1, hi = 2;
        int shrinking = 0;
        for (int round = 0; round < 100; round++) {
            double mid = lo + (hi - lo) / 2;
            if (mid == lo || mid == hi) break;
            hi = mid;
            shrinking++;
        }
        if (shrinking != 52) throw new AssertionError("stops after 52 halvings: " + shrinking);
    }
}
```
