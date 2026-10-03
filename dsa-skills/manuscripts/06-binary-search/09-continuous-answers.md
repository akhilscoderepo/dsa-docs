<!-- lesson-kind: standard -->
<!-- lesson-id: continuous-answers -->
## Continuous Answers

<!-- stage: context -->
### A Tile Maker With A Ruler

A tile maker is asked for a square tile with an area of exactly 10 square units, and she needs the side length. She has no tool that gives it directly. She can, however, take any proposed side, multiply it by itself, and see whether the area comes out too small or too big. A side of 3 gives an area of 9, which is too small. A side of 4 gives 16, which is too big. The side she wants is somewhere between them, and it is not a whole number, so no amount of trying 3 and 4 will find it.

Her customer does not need the exact value, since no saw cuts exactly anyway. The order says the side may be off by at most one millionth of a unit. The question is how to home in on a number that is not an integer, and how to know when to stop.

<!-- stage: naive -->
### Step Along The Ruler

The direct approach is to walk along the ruler in tiny steps, starting at zero, until the area first reaches 10.

```java
static double sideByStepping(double area) {
    double step = 0.000001;
    double side = 0;
    while (side * side < area) side += step;
    return side;
}
```

The result lands within one step of the true side, so it meets the order. For an area of 10 the loop runs about three million times.

<!-- stage: bottleneck -->
### Millions Of Steps For One Number

The number of steps is the length of the range divided by the step size. For an area of ten billion the side is about a hundred thousand, and the loop makes a hundred billion steps, so the cost is O(W / e) for a range of width W and a step e. Asking for ten times more precision makes the loop ten times longer. There is a second problem: adding a tiny step to a large number again and again loses the step in rounding, because a `double` near a hundred thousand cannot represent a change that small, and the loop may stop moving.

Each test says a lot more than the loop uses. If a side of 3 is too small, every side below 3 is too small as well, since a smaller side has a smaller area. If a side of 4 is too big, every side above 4 is too big. That is the same shape as the earlier searches: a stretch of failures, then a stretch of successes, with one boundary. Cutting the range in half at each test needs O(log(W / e)) tests for a range of width W and an allowed error e, here a few dozen, instead of W / e steps.

<!-- stage: insight -->
### Halve A Real Interval

The thing being searched is a **real interval**, a pair of edges `lo` and `hi` that are `double` values, with the answer known to lie between them. There is no list of candidates to index. At each step, test the midpoint. If the midpoint is too small, the answer is above it and `lo` moves up to it. If the midpoint is too big, `hi` moves down to it. In both cases the interval keeps half of its width, and the answer stays inside. Unlike the integer searches, the edges never cross or meet, so there is no `lo + 1`: the edge is set to `mid` itself.

Because the interval never becomes a single point, the search needs a rule for when to stop, which this lesson calls the **convergence policy**. The reasoning behind the most reliable policy is arithmetic. After `t` halvings the width is the starting width divided by `2` to the power `t`. The answer is within that width of either edge, so the error is at most that width. The **absolute error** is the plain distance between the returned number and the true answer. To guarantee an absolute error of one millionth for a range of width W, pick `t` large enough that W divided by `2^t` is below one millionth. A fixed count such as 100 rounds is such a choice for any range a `double` can sensibly describe.

<!-- names: real interval, convergence policy, absolute error -->

Stopping when the width drops below a small number looks equivalent and is riskier. A `double` has a limited number of digits, so when the edges are neighbours in the representation, the midpoint equals one of them, the width never shrinks, and a loop waiting for it to pass a threshold smaller than that spacing never ends. A fixed count always ends, and it is the policy this chapter uses.

<!-- stage: variables -->
### Two Edges And A Round Count

`lo` and `hi` are the edges of the interval. The invariant is that the answer lies between them, which for a minimum or a boundary means that `lo` is on the too-small side and `hi` is on the too-big side. `mid` is the point under test, and `rounds` is the fixed number of halvings. The starting edges come from the problem: zero and the larger of one and the input for a square root, since a square root is never above its input when the input is at least one, and never above one when the input is below one. What the function returns is a policy choice: either edge is within the final width of the answer.

<!-- stage: trace -->
### Halving Until The Edges Are Close

The first trace finds the side of a square with area 10. The row of cells is the whole numbers from zero to ten, and each pointer sits in the whole-number cell nearest to its edge, while the true values are given in the step data. The step to study is the second: the midpoint 2.5 has an area of 6.25, which is too small, so the lower edge moves up to 2.5 and the interval keeps its upper half.

```trace
{"cells":["0","1","2","3","4","5","6","7","8","9","10"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":10,"mid":5},"vars":{"mid":5.0,"area":25.0},"note":"Try 5. Its area is 25, which is too big, so hi moves down to 5 and the interval keeps its lower half."},{"at":{"lo":0,"hi":5,"mid":3},"vars":{"mid":2.5,"area":6.25},"note":"Try 2.5. Its area is 6.25, which is too small, so lo moves up to 2.5 and the interval keeps its upper half."},{"at":{"lo":3,"hi":5,"mid":4},"vars":{"mid":3.75,"area":14.0625},"note":"Try 3.75. Its area is 14.06, which is too big, so hi moves down to 3.75 and the interval keeps its lower half."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"mid":3.125,"area":9.7656},"note":"Try 3.125. Its area is 9.766, which is too small, so lo moves up to 3.125 and the interval keeps its upper half."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"mid":3.4375,"area":11.8164},"note":"Try 3.4375. Its area is 11.82, which is too big, so hi moves down to 3.4375 and the interval keeps its lower half."},{"at":{"lo":3,"hi":3,"mid":3},"vars":{"mid":3.28125,"area":10.7666},"note":"Try 3.28125. Its area is 10.77, which is too big, so hi moves down to 3.28125 and the interval keeps its lower half."},{"at":{"lo":3,"hi":3,"mid":3},"vars":{"mid":3.203125,"area":10.26},"note":"Try 3.20312. Its area is 10.26, which is too big, so hi moves down to 3.20312 and the interval keeps its lower half."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"lo":3.125,"hi":3.2031,"width":0.0781},"note":"After 7 halvings the width is 0.07812, the answer is between 3.125 and 3.203, and about 20 more halvings would pass one millionth."}]}
```

The second trace places three points among sites at 1, 2, 4, 8 and 9 so that the closest pair of chosen points is as far apart as possible. The row of cells is the distances from zero to eight, with each pointer at the nearest whole number. A distance is feasible when greedy placement, which takes each site at least that far from the last chosen one, finds three points. The step to study is the third: a distance of exactly 3 is feasible because the check allows a gap of exactly 3, so the lower edge moves to 3, and every later test above 3 fails.

```trace
{"cells":["0","1","2","3","4","5","6","7","8"],"pointers":["lo","hi","mid"],"steps":[{"at":{"lo":0,"hi":8,"mid":4},"vars":{"gap":4.0,"sites":2},"note":"Try a gap of 4. Greedy placement finds 2 sites, fewer than 3, so hi moves down to 4."},{"at":{"lo":0,"hi":4,"mid":2},"vars":{"gap":2.0,"sites":3},"note":"Try a gap of 2. Greedy placement finds 3 sites, enough, so lo moves up to 2."},{"at":{"lo":2,"hi":4,"mid":3},"vars":{"gap":3.0,"sites":3},"note":"Try a gap of 3. Greedy placement finds 3 sites, enough, so lo moves up to 3."},{"at":{"lo":3,"hi":4,"mid":4},"vars":{"gap":3.5,"sites":2},"note":"Try a gap of 3.5. Greedy placement finds 2 sites, fewer than 3, so hi moves down to 3.5."},{"at":{"lo":3,"hi":4,"mid":3},"vars":{"gap":3.25,"sites":2},"note":"Try a gap of 3.25. Greedy placement finds 2 sites, fewer than 3, so hi moves down to 3.25."},{"at":{"lo":3,"hi":3,"mid":3},"vars":{"gap":3.125,"sites":2},"note":"Try a gap of 3.125. Greedy placement finds 2 sites, fewer than 3, so hi moves down to 3.125."},{"at":{"lo":3,"hi":3,"mid":-1},"vars":{"lo":3.0,"hi":3.125},"note":"The answer is between 3 and 3.125, and more halvings close in on 3."}]}
```

<!-- stage: code -->
### Fixed Rounds Over A Real Range

```java
static double sqrtApprox(double x) {
    double lo = 0, hi = Math.max(1, x);
    for (int round = 0; round < 100; round++) {
        double mid = (lo + hi) / 2;
        if (mid * mid <= x) lo = mid;
        else hi = mid;
    }
    return lo;
}

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
```

Each search runs a fixed number of rounds, so the time is O(rounds) tests, and each test costs one pass for the placement and constant time for the square root, with O(1) extra space. The sites array must be sorted before the placement check, which is the cost of an earlier lesson and not part of the rounds.

<!-- stage: applicability -->
### When Real Answers Can Be Bisected

Use bisection over real values when the answer is a number that need not be whole, a candidate can be tested in constant or linear time, and feasibility is monotone: the test says too small below the answer and too big above it. State the allowed error before writing the loop, because the number of rounds comes from it. The invariant is that the answer lies between `lo` and `hi`, and each round keeps one half.

A false friend is a loop that stops when `hi - lo` is below a tolerance, with a tolerance smaller than the spacing of `double` values near the answer. The loop then never exits. Another false friend is a tolerance that is right for large answers and wrong for tiny ones, since a fixed absolute error of one millionth makes no sense for an answer of one billionth; a stated relative error needs a different choice of rounds. A third is a test that is not monotone, such as one that depends on rounding in its own arithmetic.

In Java, compare with `<=` so that exact hits count as feasible, keep both edges as `double`, and avoid `(lo + hi) / 2` only when the edges can be near the largest `double`, which does not happen for the ranges here. Prefer a fixed round count, and write down what the count guarantees and what it does not.

<!-- stage: exercises -->
### Exercises

#### [Build] Square Root (Author exercise)
<!-- id: bs-square-root -->

**Prerequisites.** The integer answers lesson and the idea of a real interval.

**Problem.** Given a non-negative `double x`, return a value within an absolute error of one millionth of the square root of `x`, without calling a library root function. Search the interval from zero to the larger of one and `x`.

**Constraints.** 0 <= x <= 1000000000000. The returned value must be within 0.000001 of the true root.

**Example 1.** Input `x = 2`, output about 1.414214.

**Example 2.** Input `x = 0.25`, output about 0.5.

**Hint.** If the midpoint squared is at most `x`, which edge moves? Why must the upper edge start at least at one?

**Changed decision.** First rung: the searched space is a real interval, so the edge is set to `mid` and a round count decides when to stop.

#### [Vary] Maximum Minimum Distance (Author exercise)
<!-- id: bs-max-min-distance -->

**Prerequisites.** The Square Root exercise above.

**Problem.** Given the sorted positions of sites on a line and a count `k`, choose `k` of the sites so that the smallest gap between two chosen neighbours is as large as possible, and return that gap. A gap is feasible when a greedy placement that takes each site at least that far from the last chosen one finds `k` sites. Search the real gap.

**Constraints.** 2 <= k <= sites.length <= 1000, sorted positions between 0 and 1000, and an answer within 0.000000001 is accepted.

**Example 1.** Input `sites = [1, 2, 4, 8, 9], k = 3`, output about 3.

**Example 2.** Input `sites = [0, 10], k = 2`, output about 10.

**Hint.** If a gap is feasible, what about a smaller gap? What are the smallest and largest gaps worth trying?

**Changed decision.** The test changes from a square to a greedy placement, and the feasible side is now the lower one, so `lo = mid` on a hit.

#### [Boundary] Scale-Aware Error (Author exercise)
<!-- id: bs-scale-aware-error -->

**Prerequisites.** The two exercises above.

**Problem.** Write a cube root by bisection that is correct to a relative error of one billionth, meaning the error divided by the answer, for inputs between a trillionth and a trillion. Then show that stopping at an absolute error of one millionth fails the relative contract for the smallest inputs and passes it for the largest.

**Constraints.** 0.000000000001 <= x <= 1000000000000. The relative error of the result must be at most 0.000000001.

**Example 1.** Input `x = 27`, output about 3.

**Example 2.** Input `x = 0.000000000001`, output about 0.0001, where an absolute error of one millionth is a relative error of one hundredth.

**Hint.** What is the true answer for the smallest input? How wide may the final interval be when the answer is that small?

**Changed decision.** The allowed error is tied to the size of the answer, so the number of rounds is chosen for the smallest answer, not for the range.

#### [Recognize] Fixed Iterations (Author exercise)
<!-- id: bs-fixed-iterations -->

**Prerequisites.** All three exercises above.

**Problem.** Explain why 80 bisections are a convergence policy and not a claim of maximal precision. Show the width after 80 halvings of a wide range and of a unit range, show a tiny answer whose relative error is still large, and show that a loop which waits for the width to drop below a threshold can fail to end.

**Constraints.** Use `double` arithmetic only. Cap any loop that might not end.

**Example 1.** Input a starting width of one trillion, output a width after 80 halvings that is below one millionth.

**Example 2.** Input the square root of 1e-40 searched from the unit range, output a relative error far above one billionth after 80 halvings.

**Hint.** What is the width after `t` halvings? What is the spacing of `double` values near the answer, and what happens when the midpoint equals an edge?

**Changed decision.** The task changes from writing the search to judging what its stopping rule does and does not promise.
