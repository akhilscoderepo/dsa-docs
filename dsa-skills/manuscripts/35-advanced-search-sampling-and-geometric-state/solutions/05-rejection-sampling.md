<!-- solutions-for: 05-rejection-sampling -->
### Solutions For Rejection Sampling

#### Solution: [Build] Point In Unit Circle (Author exercise)
<!-- id: rj35-point-unit-circle -->

**Approach.**
Each trial draws a pair `(u, v)` and maps it to `x = 2u - 1` and `y = 2v - 1`, a uniform point in the square from -1 to 1. The test compares `x * x + y * y` with 1, the squared radius, so no square root runs. A passing point is returned at once. A failing pair is discarded and the next trial draws two new numbers. For a patch `A` of the circle, a trial lands in `A` with probability `area(A) / 4` and passes with probability `pi / 4`, so the returned point lands in `A` with probability `area(A) / pi`. The invariant is that every draw is uniform over the square and the test sees only the drawn point.

The program checks the examples and the edge point `(-1, 0)`, which the inclusive test accepts. It then runs 200000 samples with a seeded generator and checks the fraction that falls inside the disc of radius one half. A fair sampler gives 1/4, and the polar method from the lesson gives 1/2.

**Complexity.**
- **Time** is O(1) expected, with 4/pi pairs per point.
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.DoubleSupplier;

public final class PointUnitCircleBuild {
    /**
     * Returns a uniform point in the closed unit disc.
     * Time: O(1) expected. Space: O(1).
     * Invariant: every draw is uniform in the square [-1, 1)^2 and the test depends on the point only.
     */
    static double[] pointInUnitCircle(DoubleSupplier rand) {
        while (true) { // each pass is one independent trial
            double x = 2 * rand.getAsDouble() - 1; // uniform in [-1, 1)
            double y = 2 * rand.getAsDouble() - 1;
            if (x * x + y * y <= 1) return new double[]{x, y}; // inside: accept, edge included
        }
    }

    static double[] polar(DoubleSupplier rand) {
        double d = rand.getAsDouble(), a = 2 * Math.PI * rand.getAsDouble();
        return new double[]{d * Math.cos(a), d * Math.sin(a)};
    }

    static DoubleSupplier script(double... v) {
        int[] at = {0};
        return () -> v[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        double[] p1 = pointInUnitCircle(script(0.9, 0.9, 0.25, 0.75));
        if (p1[0] != -0.5 || p1[1] != 0.5) throw new AssertionError("ex1");
        double[] p2 = pointInUnitCircle(script(0.5, 0.5));
        if (p2[0] != 0.0 || p2[1] != 0.0) throw new AssertionError("ex2");
        // the edge point (-1, 0) is accepted under the inclusive test
        double[] edge = pointInUnitCircle(script(0.0, 0.5));
        if (edge[0] != -1.0 || edge[1] != 0.0) throw new AssertionError("edge");
        // the fraction inside the half-radius disc is about 1/4 for rejection and about 1/2 for the polar method
        Random rnd = new Random(61);
        DoubleSupplier src = rnd::nextDouble;
        int n = 200_000, inner = 0, innerPolar = 0;
        for (int i = 0; i < n; i++) {
            double[] a = pointInUnitCircle(src);
            if (a[0] * a[0] + a[1] * a[1] <= 0.25) inner++;
            double[] b = polar(src);
            if (b[0] * b[0] + b[1] * b[1] <= 0.25) innerPolar++;
        }
        double fr = inner / (double) n, fp = innerPolar / (double) n;
        if (Math.abs(fr - 0.25) > 0.01) throw new AssertionError("rejection fraction " + fr);
        if (Math.abs(fp - 0.50) > 0.01) throw new AssertionError("polar fraction " + fp);
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Generate Random Point In A Circle (LeetCode 478)
<!-- id: rj35-random-point-circle -->

**Approach.**
The class keeps the radius, the center and the generator. A call samples a point in the unit circle by rejection and then scales it by the radius and adds the center. The test runs on unit coordinates, so it never depends on the size of the arena and never loses precision for a radius near 10^8. A uniform map that scales every length by the same factor and shifts the result keeps the density constant, so the output is uniform over the arena. The invariant is that the unit point is uniform over the unit circle and the affine map preserves uniformity.

The program checks the examples and then runs 100000 samples for a shifted, scaled arena. Every point must lie within `radius` of the center, and the fraction within half the radius must be near 1/4.

**Complexity.**
- **Time** is O(1) expected per call.
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.DoubleSupplier;

public final class RandomPointCircleVary {
    static final class ArenaPicker {
        private final double radius, xCenter, yCenter;
        private final DoubleSupplier rand;

        ArenaPicker(double radius, double xCenter, double yCenter, DoubleSupplier rand) {
            this.radius = radius; this.xCenter = xCenter; this.yCenter = yCenter; this.rand = rand;
        }

        /**
         * Returns a uniform point in the disc.
         * Time: O(1) expected. Space: O(1).
         * Invariant: the unit point is uniform over the unit disc, and scaling plus shifting keeps uniformity.
         */
        double[] randPoint() {
            while (true) {
                double ux = 2 * rand.getAsDouble() - 1; // unit coordinates
                double uy = 2 * rand.getAsDouble() - 1;
                if (ux * ux + uy * uy <= 1) // the test runs before scaling
                    return new double[]{xCenter + radius * ux, yCenter + radius * uy};
            }
        }
    }

    static DoubleSupplier script(double... v) {
        int[] at = {0};
        return () -> v[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        double[] a = new ArenaPicker(2, 1, -1, script(0.25, 0.75)).randPoint();
        if (a[0] != 0.0 || a[1] != 0.0) throw new AssertionError("ex1");
        double[] b = new ArenaPicker(10, 0, 0, script(0.9, 0.9, 0.5, 0.75)).randPoint();
        if (b[0] != 0.0 || b[1] != 5.0) throw new AssertionError("ex2");
        // statistics for a shifted and scaled arena
        Random rnd = new Random(62);
        ArenaPicker p = new ArenaPicker(50, 1000, -300, rnd::nextDouble);
        int n = 100_000, inner = 0;
        for (int i = 0; i < n; i++) {
            double[] q = p.randPoint();
            double dx = q[0] - 1000, dy = q[1] + 300;
            double r2 = dx * dx + dy * dy;
            if (r2 > 50.0 * 50.0 * (1 + 1e-12)) throw new AssertionError("outside the arena");
            if (r2 <= 25.0 * 25.0) inner++; // the half-radius disc holds a quarter of the area
        }
        if (Math.abs(inner / (double) n - 0.25) > 0.01) throw new AssertionError("not uniform");
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Boundary And Expected Trials (Author exercise)
<!-- id: rj35-boundary-expected-trials -->

**Approach.**
The method draws at most `maxTrials` pairs. For each pair it forms `x` and `y` and accepts only if `x * x + y * y < 1`, so a point on the edge is rejected. The edge has zero area, so excluding it does not change the probabilities of the sampler, but it changes which scripted draws are accepted, so the policy has to be stated. The acceptance probability is `p = pi / 4`, about 0.7854. The number of trials until success is geometric with mean `1 / p`, about 1.2732. The chance that all `m` trials fail is `(1 - p)^m`, which is about 0.2146 for one trial, 0.0461 for two trials and 0.0099 for three trials. The method returns `null` when the cap is reached. The invariant is that trial `k` runs only if the first `k - 1` trials were all rejected.

The program checks the examples and the edge policy. It then runs 200000 uncapped samples with a seeded generator and checks that the mean trial count is near 1.2732. It runs capped samples with `maxTrials = 3` and checks that the failure fraction is near 0.0099.

**Complexity.**
- **Time** is O(maxTrials) in the worst case and O(1) expected.
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.DoubleSupplier;

public final class BoundaryExpectedTrialsBoundary {
    static int lastTrials; // trials used by the last call, kept for the statistics below

    /**
     * Returns the first point in the open unit disc within maxTrials trials, or null.
     * Time: O(maxTrials). Space: O(1).
     * Invariant: trial k runs only when the first k - 1 trials were rejected.
     */
    static double[] boundedPoint(DoubleSupplier rand, int maxTrials) {
        for (int t = 1; t <= maxTrials; t++) { // the cap bounds the worst case
            lastTrials = t;
            double x = 2 * rand.getAsDouble() - 1;
            double y = 2 * rand.getAsDouble() - 1;
            if (x * x + y * y < 1) return new double[]{x, y}; // strict: the edge is rejected
        }
        return null; // every trial was rejected
    }

    static DoubleSupplier script(double... v) {
        int[] at = {0};
        return () -> v[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        double[] a = boundedPoint(script(0.0, 0.5, 0.75, 0.5), 2);
        if (a == null || a[0] != 0.5 || a[1] != 0.0) throw new AssertionError("ex1");
        if (boundedPoint(script(0.0, 0.0), 1) != null) throw new AssertionError("ex2");
        // a point exactly on the edge is rejected by the strict test
        if (boundedPoint(script(0.0, 0.5), 1) != null) throw new AssertionError("edge accepted");
        // the mean number of trials is near 4/pi
        Random rnd = new Random(63);
        DoubleSupplier src = rnd::nextDouble;
        int n = 200_000;
        long sum = 0;
        for (int i = 0; i < n; i++) { boundedPoint(src, 1000); sum += lastTrials; }
        double mean = sum / (double) n;
        if (Math.abs(mean - 4 / Math.PI) > 0.01) throw new AssertionError("mean trials " + mean);
        // the chance that three trials all fail is (1 - pi/4)^3
        int fails = 0;
        for (int i = 0; i < n; i++) if (boundedPoint(src, 3) == null) fails++;
        double expected = Math.pow(1 - Math.PI / 4, 3);
        if (Math.abs(fails / (double) n - expected) > 0.003) throw new AssertionError("failure rate");
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Implement Rand10 Using Rand7 (LeetCode 470)
<!-- id: rj35-rand10-from-rand7 -->

**Approach.**
Two calls to `rand7` give the pair `(a, b)` and the index `(a - 1) * 7 + b`, which takes each value from 1 to 49 with probability 1/49. The forty indexes 1 to 40 split into ten groups of four, so `1 + (idx - 1) % 10` gives each result from 1 to 10 exactly four times. The nine indexes 41 to 49 would favor the results 1 to 9 over 10, so the method rejects them and draws a new pair. The accepted index is uniform over 1 to 40, and the result is therefore uniform over 1 to 10. The acceptance probability is 40/49, so the expected number of pairs is 49/40 and the expected number of `rand7` calls is 2.45. The invariant is that every accepted index is uniform over 1 to 40.

The program enumerates all 49 pairs and counts how often each result occurs. Each of the ten results must appear exactly four times, and nine pairs must be rejected. It also runs the examples and checks the mean call count against 2.45 with a seeded generator.

**Complexity.**
- **Time** is O(1) expected, with 2.45 calls of `rand7` on average.
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.IntSupplier;

public final class Rand10Recognize {
    static int calls; // number of rand7 calls in the last run, used by the statistics below

    /**
     * Returns a fair integer from 1 to 10.
     * Time: O(1) expected. Space: O(1).
     * Invariant: every accepted index is uniform over 1..40.
     */
    static int rand10(IntSupplier rand7) {
        while (true) {
            int a = rand7.getAsInt(), b = rand7.getAsInt(); // two rolls
            calls += 2;
            int idx = (a - 1) * 7 + b; // uniform over 1..49
            if (idx <= 40) return 1 + (idx - 1) % 10; // 40 indexes form ten groups of four
            // idx in 41..49 would favor the results 1..9, so the pair is rejected
        }
    }

    static IntSupplier script(int... v) {
        int[] at = {0};
        return () -> v[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (rand10(script(3, 4)) != 8) throw new AssertionError("ex1");
        if (rand10(script(6, 6, 1, 1)) != 1) throw new AssertionError("ex2");
        // exact enumeration of the 49 pairs: each result appears four times and nine pairs are rejected
        int[] counts = new int[11];
        int rejected = 0;
        for (int a = 1; a <= 7; a++) for (int b = 1; b <= 7; b++) {
            int idx = (a - 1) * 7 + b;
            if (idx > 40) { rejected++; continue; }
            counts[1 + (idx - 1) % 10]++;
        }
        if (rejected != 9) throw new AssertionError("rejected count");
        for (int r = 1; r <= 10; r++) if (counts[r] != 4) throw new AssertionError("group size for " + r);
        // the mean number of rand7 calls is near 2 * 49 / 40 = 2.45
        Random rnd = new Random(64);
        IntSupplier die = () -> 1 + rnd.nextInt(7);
        int n = 200_000;
        calls = 0;
        for (int i = 0; i < n; i++) rand10(die);
        if (Math.abs(calls / (double) n - 2.45) > 0.02) throw new AssertionError("mean calls");
        System.out.println("ok");
    }
}
```
