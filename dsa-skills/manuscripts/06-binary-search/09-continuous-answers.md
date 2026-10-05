<!-- lesson-kind: standard -->
<!-- lesson-id: continuous-answers -->
## Search Real Number Answers

<!-- stage: context -->
### A Square Root Without A Library Call

A small embedded controller must compute the length of a vector, which needs the square root of a sum of squares. Its firmware has multiplication, addition and comparison, and it has no square root routine. A sum such as 2 has a root of 1.41421356..., a number with no finite decimal form. No whole number answers the question.

The last lesson searched whole numbers, and every candidate was an integer that could be named. A real answer has no next candidate. The question for this lesson is how a search reaches a real answer, and when it may stop.

<!-- stage: naive -->
### Stepping Forward By A Small Amount

The direct method walks upward from 0 in small steps. It keeps the largest multiple of the step whose square does not exceed `x`.

```java
static double rootByStepping(double x, double step) {
    long i = 0;
    while (((i + 1) * step) * ((i + 1) * step) <= x) i++;
    return i * step;
}
```

For `x = 2` and `step = 0.000001`, the loop runs 1414213 times and returns 1.414213. The error is smaller than the step.

```predict
The caller now wants an error below 0.000000001 for x = 2, a step 1000 times smaller. How many loop passes does the method make, and what happens to the pass count for x = 10^12?

It makes about 1.4 billion passes for x = 2, since the count is root divided by step. For x = 10^12 the root is 10^6, so the count is 10^15 passes and the loop cannot finish.
```

<!-- stage: bottleneck -->
### The Pass Count Grows With Precision

The loop makes about `sqrt(x) / step` passes, which is O(sqrt(x) / step). Halving the step doubles the cost, so each extra digit of precision multiplies the work by 10.

The test `i * step squared <= x` has the same monotone shape as the whole number checks. Every value below the root passes the test and every value above it fails. The loop uses that fact only to decide when to stop, and it discards one step of the range per test. A search that discards half of the remaining range per test would need only a few dozen tests for the same precision.

<!-- stage: insight -->
### Halve The Interval Until Narrow Enough

A real interval can be halved exactly as an integer range is. Keep an interval `[lo, hi]` with a passing value at `hi` and a failing value at `lo`, and replace one end by the midpoint after each test.

<!-- names: bisection, tolerance, bisection count -->

#### Bisection On A Real Interval

**Bisection** is the repeated halving of an interval that brackets the answer. The interval keeps `lo` as a value that fails the test and `hi` as a value that passes it. A midpoint `mid = lo + (hi - lo) / 2` that passes becomes the new `hi`, and a midpoint that fails becomes the new `lo`. Unlike the integer search, `mid` is never skipped past, because a real interval has no neighbor to step to, so an end takes the value `mid` and not `mid + 1`.

#### Tolerance Sets The Stopping Point

A **tolerance** is the largest error that the caller accepts, either as an absolute amount such as 0.000001 or as a fraction of the answer. The search can stop once `hi - lo` is at most the tolerance, because the true answer lies somewhere inside the interval. Either end, or the midpoint, is then within the tolerance of the answer.

#### A Fixed Bisection Count

The width of the interval after `t` rounds is the starting width divided by 2^t. This gives a **bisection count** that depends only on the starting width and the tolerance, and not on the input values. A loop that runs a fixed number of rounds, such as 100, needs no comparison of widths. Each round costs one check, so the total cost is O(t) checks, and `t` grows with the logarithm of the starting width divided by the tolerance.

<!-- stage: variables -->
### The Interval And The Count

The loop keeps four values: two ends, a midpoint and a counter.

- **lo** is a value known to fail the check, or the lowest value of the range.
- **hi** is a value known to pass the check, or the highest value of the range.
- **mid** is `lo + (hi - lo) / 2`, a `double` that becomes one of the two ends.
- **round** counts the completed halvings and stops the loop at the chosen bisection count.

The check is a pure function of one `double`. It must be monotone, so every value below the answer fails and every value above it passes.

<!-- stage: trace -->
### Two Bisections On A Real Interval

#### The Root Of 10

The search looks for the root of 10 inside `[0, 10]`. Each round squares `mid` and compares the result with 10. Round 1 tests 5, whose square 25 is too large, so `hi` becomes 5. Round 2 tests 2.5, whose square 6.25 is too small, so `lo` becomes 2.5. Round 3 tests 3.75, round 4 tests 3.125, and each round halves the width from 10 down to 0.078125 after seven rounds. The true root is 3.16227766.

```trace
{"cells":["round 0","round 1","round 2","round 3","round 4","round 5","round 6","round 7"],"pointers":["round"],"steps":[{"at":{"round":0},"vars":{"lo":"0","hi":"10"},"note":"Start with the interval [0, 10]."},{"at":{"round":1},"vars":{"mid":"5","lo":"0","hi":"5"},"note":"The square of 5 is 25, which is at least 10, so hi becomes 5."},{"at":{"round":2},"vars":{"mid":"2.5","lo":"2.5","hi":"5"},"note":"The square of 2.5 is 6.25, which is below 10, so lo becomes 2.5."},{"at":{"round":3},"vars":{"mid":"3.75","lo":"2.5","hi":"3.75"},"note":"The square of 3.75 is 14.0625, which is at least 10, so hi becomes 3.75."},{"at":{"round":4},"vars":{"mid":"3.125","lo":"3.125","hi":"3.75"},"note":"The square of 3.125 is 9.76562, which is below 10, so lo becomes 3.125."},{"at":{"round":5},"vars":{"mid":"3.4375","lo":"3.125","hi":"3.4375"},"note":"The square of 3.4375 is 11.8164, which is at least 10, so hi becomes 3.4375."},{"at":{"round":6},"vars":{"mid":"3.28125","lo":"3.125","hi":"3.28125"},"note":"The square of 3.28125 is 10.7666, which is at least 10, so hi becomes 3.28125."},{"at":{"round":7},"vars":{"mid":"3.20312","lo":"3.125","hi":"3.20312"},"note":"The square of 3.20312 is 10.26, which is at least 10, so hi becomes 3.20312."}]}
```

#### Four Points On A Segment

The second search places 4 points on the segment `[0, 10]` and looks for the largest gap `d` between neighbors. A gap `d` works when the segment holds at least 4 points spaced `d` apart, which means `floor(10 / d) + 1 >= 4`. Larger gaps are harder, so the check succeeds for small `d` and fails for large `d`, and the answer is the largest successful value. The roles of the ends swap here. A successful midpoint becomes `lo`, and a failing midpoint becomes `hi`. After six rounds the interval is `[3.28125, 3.4375]`, and the true answer 3.3333... lies inside it.

```trace
{"cells":["round 0","round 1","round 2","round 3","round 4","round 5","round 6"],"pointers":["round"],"steps":[{"at":{"round":0},"vars":{"lo":"0","hi":"10"},"note":"Start with the gap range [0, 10]."},{"at":{"round":1},"vars":{"mid":"5","lo":"0","hi":"5"},"note":"A gap of 5 fits 3 points, which is fewer than 4, so hi becomes 5."},{"at":{"round":2},"vars":{"mid":"2.5","lo":"2.5","hi":"5"},"note":"A gap of 2.5 fits 5 points, which is at least 4, so lo becomes 2.5."},{"at":{"round":3},"vars":{"mid":"3.75","lo":"2.5","hi":"3.75"},"note":"A gap of 3.75 fits 3 points, which is fewer than 4, so hi becomes 3.75."},{"at":{"round":4},"vars":{"mid":"3.125","lo":"3.125","hi":"3.75"},"note":"A gap of 3.125 fits 4 points, which is at least 4, so lo becomes 3.125."},{"at":{"round":5},"vars":{"mid":"3.4375","lo":"3.125","hi":"3.4375"},"note":"A gap of 3.4375 fits 3 points, which is fewer than 4, so hi becomes 3.4375."},{"at":{"round":6},"vars":{"mid":"3.28125","lo":"3.28125","hi":"3.4375"},"note":"A gap of 3.28125 fits 4 points, which is at least 4, so lo becomes 3.28125."}]}
```

<!-- stage: code -->
### The Fixed Round Search In Java

```java
static double sqrtByBisection(double x) {
    double lo = 0, hi = Math.max(1, x);
    for (int round = 0; round < 100; round++) {
        double mid = lo + (hi - lo) / 2;
        if (mid * mid >= x) hi = mid;
        else lo = mid;
    }
    return hi;
}
```

The starting `hi` is `max(1, x)`, because the root of a number below 1 is larger than the number. After 100 rounds the width is at most `max(1, x) / 2^100`, far below the spacing of two neighboring `double` values for any ordinary input.

<!-- stage: applicability -->
### When To Search Real Values

#### The Invariant

The invariant is that the check fails at `lo` and passes at `hi`, so the answer lies in `[lo, hi]`. A passing midpoint keeps the property for the new `hi`, and a failing midpoint keeps it for the new `lo`. The width halves exactly in each round, until the width is too small for the `double` format to represent a midpoint.

#### The False Friend

A loop of the form `while (hi - lo > eps)` looks safer than a fixed count, and it can fail to stop. When `eps` is smaller than the gap between two neighboring `double` values at `hi`, the midpoint equals `lo` or `hi`, so the interval stops shrinking, and the loop runs forever. A fixed count always stops. A count of 100 is a policy for ordinary inputs and not a claim of the best possible precision.

#### Absolute And Relative Error

An absolute tolerance of 0.000001 is very strict for a root near 1000000 and meaningless for a root near 0.000001, where the answer 0 passes. A relative tolerance scales with the answer. Choose the kind of error before choosing the count, and derive the count from the starting width and that tolerance.

<!-- stage: exercises -->
### Exercises

#### [Build] Square Root (Author exercise)
<!-- id: bs-real-sqrt -->

**Prerequisites.** The previous lesson and the bisection of this lesson.

**Problem.** Given a non-negative real number `x`, return a number `r` with `|r - sqrt(x)| <= 0.000001`, using only multiplication, comparison and bisection. Do not call `Math.sqrt`.

**Constraints.** The limits are:
- **Input** satisfies `0 <= x <= 10^9`, given as a `double`.
- **Error** is absolute, at most `0.000001`.
- **Operations** exclude square root and power calls.
- **Zero** must return a value within the tolerance of 0.

**Example 1.** Input `x = 2`, output any value in `[1.414213, 1.414215]`.

**Example 2.** Input `x = 0.25`, output any value in `[0.499999, 0.500001]`.

**Hint.** The check is "mid squared is at least x". Which end of the interval takes `mid` when it passes?

**Changed decision.** Basic case: the answer is a real number, so the interval ends take the value `mid` and the loop uses a round count.

#### [Vary] Maximum Minimum Distance (Author exercise)
<!-- id: bs-real-widest-gap -->

**Prerequisites.** The previous exercise.

**Problem.** A sorted list of disjoint closed intervals `[a, b]` on a line is given, together with an integer `k`. Choose `k` points, each inside some interval, so that the smallest distance between two chosen points is as large as possible. Return that largest smallest distance with absolute error at most `0.000001`.

**Constraints.** The limits are:
- **Intervals** number `1 <= n <= 1000`, with integer ends `0 <= a <= b <= 10^6`.
- **Order** is strict, and each interval ends before the next one starts.
- **Points** satisfy `2 <= k`, and the intervals together hold at least `k` points.
- **Several points** may lie inside one interval.

**Example 1.** Input intervals `[0,2], [5,6], [9,12]` and `k = 5`, output 2.0.

**Example 2.** Input the same intervals and `k = 2`, output 12.0.

**Hint.** For a gap `d`, place the first point at the start of the first interval and each next point as early as the gap allows. How many points fit?

**Changed decision.** The check counts how many points fit for a gap `d`, and the search keeps the largest passing value, so a passing `mid` becomes `lo`.

#### [Boundary] Scale-Aware Error (Author exercise)
<!-- id: bs-real-relative-error -->

**Prerequisites.** Both exercises above.

**Problem.** Given a `double` `x` with `10^-12 <= x <= 10^12`, return a number `r` with `|r - sqrt(x)| <= 10^-9 * sqrt(x)`. A fixed absolute tolerance does not satisfy this for small `x`, so the round count must come from the relative tolerance.

**Constraints.** The limits are:
- **Input** satisfies `10^-12 <= x <= 10^12`.
- **Error** is relative to `sqrt(x)`, at most `10^-9`.
- **Rounds** are fixed in advance and the same for every input.
- **Operations** exclude square root and power calls.

**Example 1.** Input `x = 0.000000000001`, output any value in `[0.000000999999999, 0.000001000000001]`.

**Example 2.** Input `x = 1000000000000`, output any value in `[999999.999, 1000000.001]`.

**Hint.** The answer can be as small as 10^-6, so the final width must be at most 10^-15. How many halvings take a width of 10^12 down to that value?

**Changed decision.** The tolerance depends on the answer, so the round count is derived from the largest ratio of starting width to answer.

#### [Recognize] Fixed Iterations (Author exercise)
<!-- id: bs-real-round-count -->

**Prerequisites.** All exercises above.

**Problem.** Given a starting width `w` and a tolerance `eps`, return the smallest integer `t` such that `w / 2^t <= eps`, which is the number of bisection rounds that bring the interval within the tolerance.

**Constraints.** The limits are:
- **Width** satisfies `1 <= w <= 10^12` as a `double`.
- **Tolerance** satisfies `10^-12 <= eps <= w`.
- **Answer** is a non-negative `int`.
- **Method** uses an exact comparison, not a logarithm of a floating point quotient.

**Example 1.** Input `w = 10` and `eps = 0.000001`, output 24.

**Example 2.** Input `w = 1` and `eps = 0.001`, output 10.

**Hint.** Halve a copy of the width until it is at most the tolerance, and count the halvings. Halving a `double` by 2 is exact.

**Changed decision.** The task asks for the policy and not for the root, so the fixed count of 100 appears as one safe value and not as a theorem.
