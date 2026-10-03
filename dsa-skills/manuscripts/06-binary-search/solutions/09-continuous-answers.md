<!-- solutions-for: 06-continuous-answers -->
### Continuous Answers

#### Solution: [Build] Square Root (Author exercise)
<!-- id: bs-square-root -->

**Approach.** The square of a non-negative number grows with it, so a midpoint whose square is at most `x` is too small or exact, and the root is at or above it. Start with `lo = 0` and `hi = max(1, x)`, which contains the root since the root of a number below one is at most one and the root of a larger number is below the number. Each round sets `lo = mid` or `hi = mid`. After 100 rounds the width is the starting width divided by `2^100`, which is far below one millionth for any `x` up to a trillion. The program compares with `Math.sqrt` as an oracle on fixed and random inputs.

**Complexity.** O(rounds) time, which is constant for a fixed round count, and O(1) extra space.

```java run
import java.util.Random;

public final class SquareRoot {
    static double sqrtApprox(double x) {
        double lo = 0, hi = Math.max(1, x);
        for (int round = 0; round < 100; round++) {
            double mid = (lo + hi) / 2;
            if (mid * mid <= x) lo = mid;
            else hi = mid;
        }
        return lo;
    }

    public static void main(String[] args) {
        if (Math.abs(sqrtApprox(2) - 1.4142135623730951) > 1e-6) throw new AssertionError("example 1");
        if (Math.abs(sqrtApprox(0.25) - 0.5) > 1e-6) throw new AssertionError("example 2");
        if (sqrtApprox(0) != 0) throw new AssertionError("zero");
        if (Math.abs(sqrtApprox(1e12) - 1e6) > 1e-6) throw new AssertionError("largest input");
        Random rnd = new Random(691);
        for (int t = 0; t < 5000; t++) {
            double x = rnd.nextDouble() * Math.pow(10, rnd.nextInt(13));
            if (Math.abs(sqrtApprox(x) - Math.sqrt(x)) > 1e-6) throw new AssertionError("differs for x=" + x);
        }
    }
}
```

#### Solution: [Vary] Maximum Minimum Distance (Author exercise)
<!-- id: bs-max-min-distance -->

**Approach.** If a gap is feasible, any smaller gap is feasible too, because the same chosen sites still keep that distance. The greedy placement takes the first site and then each site at least the gap from the last chosen one, and it finds the most sites possible for that gap. The feasible side is the low side, so a hit sets `lo = mid`. The search runs between zero and the distance from the first site to the last. The oracle takes every difference between two sites as a candidate answer, since the exact answer is one of them, and keeps the largest feasible one.

**Complexity.** O(rounds times n) time for n sites, and O(1) extra space, not counting the sorted order the input already has.

```java run
import java.util.Arrays;
import java.util.Random;

public final class MaxMinDistance {
    static boolean canPlace(double[] sites, int k, double gap) {
        int placed = 1;
        double last = sites[0];
        for (int i = 1; i < sites.length; i++) {
            if (sites[i] - last >= gap) {
                placed++;
                last = sites[i];
            }
        }
        return placed >= k;
    }
    static double maxMinGap(double[] sites, int k) {
        double lo = 0, hi = sites[sites.length - 1] - sites[0];
        for (int round = 0; round < 100; round++) {
            double mid = (lo + hi) / 2;
            if (canPlace(sites, k, mid)) lo = mid;
            else hi = mid;
        }
        return lo;
    }
    static double oracle(double[] sites, int k) {
        double best = 0;
        for (int i = 0; i < sites.length; i++)
            for (int j = i + 1; j < sites.length; j++) {
                double d = sites[j] - sites[i];
                if (d > best && canPlace(sites, k, d)) best = d;
            }
        return best;
    }

    public static void main(String[] args) {
        if (Math.abs(maxMinGap(new double[] {1, 2, 4, 8, 9}, 3) - 3) > 1e-9) throw new AssertionError("example 1");
        if (Math.abs(maxMinGap(new double[] {0, 10}, 2) - 10) > 1e-9) throw new AssertionError("example 2");
        Random rnd = new Random(692);
        for (int t = 0; t < 3000; t++) {
            int n = 2 + rnd.nextInt(8);
            double[] sites = new double[n];
            for (int i = 0; i < n; i++) sites[i] = rnd.nextDouble() * 100;
            Arrays.sort(sites);
            int k = 2 + rnd.nextInt(n - 1);
            if (Math.abs(maxMinGap(sites, k) - oracle(sites, k)) > 1e-9) throw new AssertionError("differs for k=" + k);
        }
    }
}
```

#### Solution: [Boundary] Scale-Aware Error (Author exercise)
<!-- id: bs-scale-aware-error -->

**Approach.** The cube is increasing for non-negative numbers, so a midpoint whose cube is at most `x` is too small or exact. The smallest allowed input has a root of one ten-thousandth, and a relative error of one billionth of that is about 1e-13, so the final width must be below that. With the upper edge starting at `max(1, x)`, which is at most a trillion, a width of a trillion divided by `2^100` is about 8e-19, far below every answer in range. The program checks the relative error against `Math.cbrt` on log-spread inputs, then runs a variant that stops at an absolute width of one millionth and asserts that it breaks the relative contract on the smallest input and keeps it on the largest.

**Complexity.** O(rounds) time, constant for a fixed count, and O(1) extra space.

```java run
import java.util.Random;

public final class ScaleAwareError {
    static double cubeRoot(double x) {
        double lo = 0, hi = Math.max(1, x);
        for (int round = 0; round < 100; round++) {
            double mid = (lo + hi) / 2;
            if (mid * mid * mid <= x) lo = mid;
            else hi = mid;
        }
        return lo;
    }
    static double cubeRootAbsoluteStop(double x) {
        double lo = 0, hi = Math.max(1, x);
        while (hi - lo > 1e-6) {
            double mid = (lo + hi) / 2;
            if (mid * mid * mid <= x) lo = mid;
            else hi = mid;
        }
        return lo;
    }
    static double relative(double got, double truth) { return Math.abs(got - truth) / truth; }

    public static void main(String[] args) {
        if (relative(cubeRoot(27), 3) > 1e-9) throw new AssertionError("example 1");
        if (relative(cubeRoot(1e-12), 1e-4) > 1e-9) throw new AssertionError("example 2");
        Random rnd = new Random(693);
        for (int t = 0; t < 5000; t++) {
            double x = Math.pow(10, -12 + 24 * rnd.nextDouble());
            if (relative(cubeRoot(x), Math.cbrt(x)) > 1e-9) throw new AssertionError("relative error too large for x=" + x);
        }
        if (relative(cubeRootAbsoluteStop(1e-12), 1e-4) <= 1e-9) throw new AssertionError("the absolute stop should fail for the smallest input");
        if (relative(cubeRootAbsoluteStop(1e12), 1e4) > 1e-9) throw new AssertionError("the absolute stop should pass for the largest input");
    }
}
```

#### Solution: [Recognize] Fixed Iterations (Author exercise)
<!-- id: bs-fixed-iterations -->

**Approach.** After `t` halvings the width is the starting width divided by `2^t`, so 80 halvings guarantee an absolute error below one millionth only when the starting width is below about 1.2e18. They say nothing about relative error: a unit range after 80 halvings has a width near 8e-25, and an answer of 1e-20 can still be wrong in its fifth digit. A loop that waits for the width to pass a threshold smaller than the spacing of `double` values near the answer never exits, since once the edges are neighbours the midpoint equals an edge and the width stays constant. A stopping rule that always ends is to halt when the midpoint equals an edge, and that takes at most about a thousand rounds. The program shows the widths, the large relative error, the loop that does not end under a cap, and the neighbour-stopping rule.

**Complexity.** O(rounds) time for any of the fixed-count versions, and O(1) extra space.

```java run
public final class FixedIterations {
    static double sqrtRounds(double x, int rounds) {
        double lo = 0, hi = Math.max(1, x);
        for (int round = 0; round < rounds; round++) {
            double mid = (lo + hi) / 2;
            if (mid * mid <= x) lo = mid;
            else hi = mid;
        }
        return lo;
    }
    static int roundsUntilNeighbours(double x) {
        double lo = 0, hi = Math.max(1, x);
        int rounds = 0;
        while (true) {
            double mid = (lo + hi) / 2;
            if (mid <= lo || mid >= hi) return rounds;
            if (mid * mid <= x) lo = mid;
            else hi = mid;
            rounds++;
        }
    }

    public static void main(String[] args) {
        double wide = 1e12 / Math.pow(2, 80);
        if (wide >= 1e-6) throw new AssertionError("example 1");
        double unit = 1.0 / Math.pow(2, 80);
        if (unit >= 1e-24 || unit <= 1e-25) throw new AssertionError("unit width");
        double tiny = sqrtRounds(1e-40, 80);
        double relative = Math.abs(tiny - 1e-20) / 1e-20;
        if (relative <= 1e-9) throw new AssertionError("example 2");

        double x = 1e18, lo = 0, hi = 1e18;
        int rounds = 0;
        while (hi - lo > 1e-12 && rounds < 10000) {
            double mid = (lo + hi) / 2;
            if (mid * mid <= x) lo = mid;
            else hi = mid;
            rounds++;
        }
        if (rounds != 10000) throw new AssertionError("the threshold loop should not have ended");
        double mid = (lo + hi) / 2;
        if (mid != lo && mid != hi) throw new AssertionError("the edges should be neighbours");

        int needed = roundsUntilNeighbours(2);
        if (needed < 50 || needed > 1100) throw new AssertionError("neighbour rule rounds " + needed);
        if (roundsUntilNeighbours(1e12) > 1100) throw new AssertionError("large input");
    }
}
```
