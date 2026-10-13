<!-- lesson-kind: standard -->
<!-- lesson-id: rejection-sampling -->
## Rejection Sampling

<!-- stage: context -->
### Pickups Pile Up In The Middle

A game drops a bonus item at a random spot inside a circular arena. The first version picks a random distance from the center and a random angle, and it places the item there. Players report that the bonus always seems to be near the middle of the arena. The designers plot 100000 drops and see a dense cluster in the center and a thin scatter near the wall. Each drop looks random, and the code uses a fair random number generator, yet the drops are not spread evenly over the floor.

The arena is a region with an area, and "even" means that two patches of equal area receive the same number of drops. The question of this lesson is how to produce points that are even over a circle when the only tool is a generator of even numbers between 0 and 1. It also asks what a program can do when a region has no simple formula for its own points.

<!-- stage: naive -->
### Random Distance And Random Angle

The direct design copies how a circle is described. It draws a distance `d` uniformly from 0 to the radius and an angle `a` uniformly from 0 to `2 * pi`, then converts to coordinates. The source of randomness is a `DoubleSupplier` named `rand`, whose method `getAsDouble()` returns a number from 0 (included) to 1 (excluded).

```java
final class PolarPicker {
    private final java.util.function.DoubleSupplier rand;

    PolarPicker(java.util.function.DoubleSupplier rand) { this.rand = rand; }

    double[] pointInUnitCircle() {
        double d = rand.getAsDouble();                   // distance from the center, 0 to 1
        double a = 2 * Math.PI * rand.getAsDouble();     // angle, 0 to 2 pi
        return new double[]{d * Math.cos(a), d * Math.sin(a)};
    }
}
```

The code is short and always returns a point inside the circle. It passes a visual check on a few points, which is why the bug survives review. The designers' plot is the real test.

```predict
Consider the inner disc with half the radius. What fraction of the circle's area does it cover? What fraction of the drops from PolarPicker land in that inner disc?

The inner disc has radius 1/2, so its area is pi * (1/2)^2 = pi / 4, which is one quarter of the area pi of the full circle. PolarPicker draws the distance uniformly, so half of the drops (distance below 1/2) land in the inner disc. That is twice the fair share. The method puts too many points near the center.
```

<!-- stage: bottleneck -->
### Equal Distances Are Not Equal Areas

#### Why The Polar Method Fails

The polar method costs O(1) time and O(1) space, and it is wrong. Its error is in what the uniform distance means. A ring between distance `d` and `d + e` has area about `2 * pi * d * e`, which grows with `d`. A uniform distance gives every ring of the same width the same number of points. The ring near the wall has far more area than the ring near the center, so its points are spread thin, and the center is crowded. Fair points need a distance whose chance of falling in a ring is proportional to the ring's area.

#### An Exact Repair For One Shape

There is an exact repair for the circle. Taking the square root of the uniform number gives a distance with the right chance for every ring. The repair works only because the area of a disc has a formula that can be inverted. For an arena shaped like a ring with a hole, a triangle, or a region given by a test function, no such formula is available. The method has to stay simple, exact, and independent of the shape.

#### A Method Without A Formula

A tool that needs no formula for the shape would be valuable. The only shape-specific operation it may use is a yes-or-no test: is this point inside the region? The tool needs a source of points that is uniform over some simpler region, where uniform points are easy to produce.

<!-- stage: insight -->
### Draw From A Square And Reject

<!-- names: bounding square, acceptance probability, expected trials -->

#### A Simple Region Around The Shape

The **bounding square** of the unit circle is the square with corners at `(-1, -1)` and `(1, 1)`. Uniform points in it are easy to produce, since the x-coordinate and the y-coordinate are independent. The program sets `x = 2u - 1` and `y = 2v - 1` for two numbers `u` and `v` from the generator. Every patch of the square receives points in proportion to its area.

#### Keep Only The Points That Pass The Test

The method draws a point from the square and tests `x^2 + y^2 <= 1`. If the point passes, the method returns it. If not, the method discards it and draws a new one. Why is the returned point uniform over the circle? Take any patch `A` inside the circle. A draw lands in `A` with probability `area(A) / 4`, and a draw is kept with probability `pi / 4`. The chance that the returned point lies in `A` is `(area(A) / 4) / (pi / 4) = area(A) / pi`, which is the patch's share of the circle's area. Rejection removes the part of the square outside the circle and leaves the density in the circle unchanged.

#### How Many Draws It Takes

The **acceptance probability** `p` is the area of the circle divided by the area of the bounding square, here `pi / 4`, about 0.785. The trials are independent, so the number of trials until the first acceptance follows a geometric law. The **expected trials** are `1 / p`, about 1.27 draws of a pair. The chance that more than `m` trials are needed is `(1 - p)^m`, which shrinks fast.

The invariant is that every draw is uniform over the bounding square, the test depends only on the point, and the point returned is therefore uniform over the shape.

<!-- stage: variables -->
### Draws, Coordinates And Trials

The loop keeps five names.

- **u** and **v** come from `rand`, and each lies from 0 (included) to 1 (excluded).
- **x** and **y** are `2u - 1` and `2v - 1`, so they lie from -1 (included) to 1 (excluded).
- **r2** is `x * x + y * y`, the squared distance from the center. Comparing squares avoids a square root.
- **trials** counts the pairs drawn so far. It starts at 0 and grows by one per pair.
- **accepted** is true when `r2 <= 1`. The loop ends when it becomes true.

The squared distance is compared to 1, which is the squared radius. The comparison uses `<=`, so a point exactly on the edge counts as inside.

<!-- stage: trace -->
### Tracing Two Rejection Loops

#### Points In A Circle

The first trace follows three trials of the circle sampler. The pointer `trial` marks the trial. The first pair of numbers is `0.1` and `0.9`, which gives the point `(-0.8, 0.8)`. The squared distance is `1.28`, above 1, so the point is rejected. The second pair is `0.9` and `0.1`, which gives `(0.8, -0.8)`, also at squared distance `1.28`, so it is rejected. The third pair is `0.6` and `0.3`, which gives `(0.2, -0.4)` with squared distance `0.2`, so the point is accepted and returned.

```trace
{"cells":["(-0.8, 0.8)","(0.8, -0.8)","(0.2, -0.4)"],"pointers":["trial"],"steps":[{"at":{"trial":0},"vars":{"u":0.1,"v":0.9,"x":-0.8,"y":0.8,"r2":1.28,"verdict":"reject"},"note":"Draws 0.1 and 0.9 give the point (-0.8, 0.8) with squared distance 1.28. It is above 1, so the point is rejected."},{"at":{"trial":1},"vars":{"u":0.9,"v":0.1,"x":0.8,"y":-0.8,"r2":1.28,"verdict":"reject"},"note":"Draws 0.9 and 0.1 give the point (0.8, -0.8) with squared distance 1.28. It is above 1, so the point is rejected."},{"at":{"trial":2},"vars":{"u":0.6,"v":0.3,"x":0.2,"y":-0.4,"r2":0.2,"verdict":"accept"},"note":"Draws 0.6 and 0.3 give the point (0.2, -0.4) with squared distance 0.2. It is at most 1, so the point is accepted and returned."}]}
```

#### Digits From Seven Faces

The second trace uses the same idea on integers. A die with seven faces numbered 1 to 7 must produce a fair number from 1 to 10. Two rolls `a` and `b` give the index `(a - 1) * 7 + b`, which is uniform over 1 to 49. Only the indexes 1 to 40 divide evenly into 10 groups of 4, so the loop rejects indexes 41 to 49. The first roll pair `6, 6` gives index 41 and is rejected. The pair `7, 3` gives index 45 and is rejected. The pair `2, 5` gives index 12, which is accepted, and the result is `1 + (12 - 1) % 10 = 2`.

```trace
{"cells":["6,6","7,3","2,5"],"pointers":["trial"],"steps":[{"at":{"trial":0},"vars":{"a":6,"b":6,"index":41,"verdict":"reject"},"note":"Rolls 6 and 6 give index 41. The index is above 40, so the pair is rejected."},{"at":{"trial":1},"vars":{"a":7,"b":3,"index":45,"verdict":"reject"},"note":"Rolls 7 and 3 give index 45. The index is above 40, so the pair is rejected."},{"at":{"trial":2},"vars":{"a":2,"b":5,"index":12,"verdict":"accept"},"note":"Rolls 2 and 5 give index 12. The index is at most 40, so it is accepted and the result is 2."}]}
```

<!-- stage: code -->
### Circle Sampler With A Loop

#### The Loop

The method draws pairs until one passes the test. It counts the pairs in a local variable so a test can read the trial count.

```java
final class CirclePicker {
    private final java.util.function.DoubleSupplier rand;
    int lastTrials;                                       // trials used by the last call

    CirclePicker(java.util.function.DoubleSupplier rand) { this.rand = rand; }

    double[] pointInUnitCircle() {
        int trials = 0;
        while (true) {
            trials++;
            double x = 2 * rand.getAsDouble() - 1;        // uniform in [-1, 1)
            double y = 2 * rand.getAsDouble() - 1;
            if (x * x + y * y <= 1) {                     // test against the squared radius
                lastTrials = trials;
                return new double[]{x, y};
            }
        }
    }
}
```

#### Cost

- **Time** is O(1) expected per point, with `4 / pi` pairs on average.
- **Worst case** has no fixed bound, because a long run of rejections is possible, though its chance falls geometrically.
- **Space** is O(1).

<!-- stage: applicability -->
### When Rejection Applies

#### Recognizing The Pattern

Use this method in three conditions. Uniform points are easy in a larger region. A yes-or-no test decides whether a point lies in the shape. The shape fills a good share of the larger region. The words "uniformly at random in a circle, triangle or range" are the cue. Before coding, compute the acceptance probability and decide whether boundary points count as inside. The invariant to keep is that every draw is uniform over the larger region and the test sees only the drawn point.

#### False Friends

The polar method with a uniform distance is a false friend: it looks uniform and is not. Clamping a rejected point to the circle edge is a second false friend, because every rejected point would pile onto the boundary. Reusing leftover randomness from rejected draws needs care and a proof, which is why the simple version discards them.

#### When The Method Does Not Apply

If the shape fills a tiny share of its bounding region, the acceptance probability is small and the expected trials `1 / p` grow. A thin ring inside a large square is an example, and an inverse formula or a mapped sampler is faster. If the loop must finish within a fixed number of draws, rejection has no guarantee, and a capped version needs a stated fallback.

<!-- stage: exercises -->
### Exercises

#### [Build] Point In Unit Circle (Author exercise)
<!-- id: rj35-point-unit-circle -->

**Prerequisites.** The bounding square and the squared-distance test from this lesson.

**Problem.** Write `double[] pointInUnitCircle(DoubleSupplier rand)`. Each trial calls `rand.getAsDouble()` twice, first for `u` and then for `v`, and forms `x = 2u - 1` and `y = 2v - 1`. If `x * x + y * y <= 1`, the method returns `{x, y}`. Otherwise it starts a new trial. The method never reuses a rejected number.

**Constraints.** The limits are:
- **Draws** are doubles from 0 (included) to 1 (excluded), possibly scripted.
- **Order** of calls is `u` then `v` in every trial.
- **Boundary** points with `x * x + y * y == 1` count as inside.
- **Memory** is O(1).

**Example 1.** Input draws `0.9, 0.9, 0.25, 0.75`, output `[-0.5, 0.5]`.

**Example 2.** Input draws `0.5, 0.5`, output `[0.0, 0.0]`.

**Hint.** Which two numbers belong to one trial, and what happens to them when the test fails?

**Changed decision.** Basic case: a loop around one test, with the unit circle fixed.

#### [Vary] Generate Random Point In A Circle (LeetCode 478)
<!-- id: rj35-random-point-circle -->

**Prerequisites.** The Point In Unit Circle exercise above. This exercise adds a radius and a center.

**Problem.** Design the class `ArenaPicker` with a constructor that receives `double radius`, `double xCenter`, `double yCenter` and a `DoubleSupplier rand`. The method `randPoint()` samples a point `(ux, uy)` in the unit circle as in the previous exercise, then returns `{xCenter + radius * ux, yCenter + radius * uy}`.

**Constraints.** The limits are:
- **Radius** is a positive double up to 10^8.
- **Center** coordinates are doubles from -10^7 to 10^7.
- **Test** is applied in unit coordinates, before scaling.
- **Calls** number at most 3 * 10^4 per object.

**Example 1.** Input `radius = 2`, center `(1, -1)`, draws `0.25, 0.75`, output `[0.0, 0.0]`.

**Example 2.** Input `radius = 10`, center `(0, 0)`, draws `0.9, 0.9, 0.5, 0.75`, output `[0.0, 5.0]`.

**Hint.** Why is the rejection test run before the point is scaled and shifted?

**Changed decision.** The sampler stays in the unit circle, and a scale and a shift map the accepted point to the arena.

#### [Boundary] Boundary And Expected Trials (Author exercise)
<!-- id: rj35-boundary-expected-trials -->

**Prerequisites.** The Generate Random Point In A Circle exercise above. This exercise changes the inclusion policy and bounds the trials.

**Problem.** Write `double[] boundedPoint(DoubleSupplier rand, int maxTrials)`. Use the open unit disc: a point is accepted only when `x * x + y * y < 1`, so points on the edge are rejected. Run at most `maxTrials` trials with two draws each. Return the first accepted point, or `null` if every trial is rejected.

**Constraints.** The limits are:
- **maxTrials** is from 1 to 10^6.
- **Draws** are doubles from 0 (included) to 1 (excluded).
- **Policy** is strict: a point exactly on the edge is rejected.
- **Calls** to `rand` number at most `2 * maxTrials`.

**Example 1.** Input draws `0.0, 0.5, 0.75, 0.5`, `maxTrials = 2`, output `[0.5, 0.0]`, because the first point `(-1, 0)` lies on the edge.

**Example 2.** Input draws `0.0, 0.0`, `maxTrials = 1`, output `null`.

**Hint.** The chance that a single trial is rejected is `1 - pi / 4`. How does it combine over `m` independent trials?

**Changed decision.** The edge is excluded and the loop has a cap, so the method can return no point.

#### [Recognize] Implement Rand10 Using Rand7 (LeetCode 470)
<!-- id: rj35-rand10-from-rand7 -->

**Prerequisites.** The Boundary And Expected Trials exercise above. This exercise moves from points in a plane to integers.

**Problem.** Write `int rand10(IntSupplier rand7)`. Each call of `rand7.getAsInt()` returns a fair integer from 1 to 7. The method calls `rand7` twice to get `a` and `b`, forms `idx = (a - 1) * 7 + b`, and returns `1 + (idx - 1) % 10` when `idx <= 40`. When `idx > 40`, it rejects the pair and starts again. The result must be a fair integer from 1 to 10.

**Constraints.** The limits are:
- **rand7** returns an integer from 1 to 7 on every call.
- **Pairs** are drawn in the order `a` then `b`.
- **Rejected** pairs are discarded.
- **Calls** are unbounded in the worst case, with about 2.45 calls expected.

**Example 1.** Input `rand7` outputs `3, 4`, output `8`.

**Example 2.** Input `rand7` outputs `6, 6, 1, 1`, output `1`.

**Hint.** Which indexes can be split into groups of equal size, and what happens to the rest?

**Changed decision.** The bounding region is the range 1 to 49, and the accepted region is its largest multiple of 10.
