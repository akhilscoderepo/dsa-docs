<!-- lesson-kind: standard -->
<!-- lesson-id: hostile-dry-runs -->
## Hostile Dry Runs

<!-- stage: context -->
### Why Random Tests Miss This Bug

A developer writes a method that finds the longest climb in a list of daily step counts. A climb is the longest stretch where each day beats the one before. She tests it with the examples from the ticket. Then she tests it with a thousand random lists of a hundred days each, and everything passes. A week after release, a user with a single logged day sees "longest climb: 0 days" on their dashboard.

The random tests were not careless. They could not reach the failing case, because a random list of a hundred days almost never forms one unbroken climb and almost never has length one. A bug that hides behind a boundary appears only when you choose the boundary on purpose. This lesson shows how to design the smallest input that attacks one specific weakness. It also shows how to trace the variables by hand so the weakness becomes visible. The title uses the course's older word "hostile" for what the industry calls adversarial tests, and the lesson uses the industry term from here on.

<!-- stage: naive -->
### A Method That Passes Every Sample

The method below has a flaw that a reader does not see, because every line looks reasonable.

```java
static int longestClimb(int[] steps) {
    int best = 0, current = 1;
    for (int i = 1; i < steps.length; i++) {
        if (steps[i] > steps[i - 1]) {
            current++;
        } else {
            best = Math.max(best, current);
            current = 1;
        }
    }
    return best;
}
```

On `[1, 3, 2, 4, 5, 1]` it returns 3, which is correct. It passes the ticket's examples and, as the story shows, nearly every random list. Most people stop when the tests turn green.

<!-- stage: bottleneck -->
### Why Random Volume Misses Edge Cases

Count what random testing actually buys. A thousand lists of a hundred values cost about 100,000 element visits, which is O(n) work per list and trivial to run. Now draw values from a small range such as 0 to 9. A list of more than ten days can never be strictly increasing from start to end. The failing case is an unbroken climb that never triggers the `else` branch, so it is unreachable at that size. A million such lists would still test the same behaviors that a thousand did.

The failing inputs are tiny. A list of one day returns 0 instead of 1, because the loop never runs and `best` keeps its initial value. A list that climbs every day also returns 0. The method updates `best` only when a climb ends, and the last climb never ends inside the loop. Both failures sit at the edge of the loop, where the first and last iterations behave differently from the middle. A small deliberate input reaches them in seconds.

<!-- stage: insight -->
### Aim One Small Input At One Weakness

#### Think Like An Attacker

Choose test inputs the way an attacker would, one weakness at a time. Each plausible implementation depends on an unstated happy-path assumption. The adversarial input is the smallest one that makes that assumption false.

A **dry run** is a hand execution of the code on a chosen input. You write down the value of every variable after every state change. An **adversarial input** is a small input chosen to break one specific assumption. A **failure mode** is the category of assumption under attack. The usual categories are initialization, equality, boundaries, overflow and mutation order.

<!-- names: dry run, adversarial input, failure mode -->

#### Pick One Attacker Per Failure Mode

Each failure mode has a standard small attacker. For initialization, use the smallest legal input, often a single element. For equality, use all-equal values, so strict and non-strict comparisons give different answers. For boundaries, use inputs that fill or empty the structure exactly. For overflow, use extreme values in the type that accumulates. For mutation order, use an input where a write destroys a value that the code has not read yet.

#### Check What Each Variable Means

The invariant for a dry run is that after each state change you can say what every variable means. In the climb method, `current` is the length of the climb that ends at the index just examined. The variable `best` is the longest climb that has already ended. Written that way, the bug is obvious. A climb that is still open when the loop ends has not been recorded, so `best` is stale.

<!-- stage: variables -->
### Track Variables In A Table

For a dry run, keep a small table with one row per state change and one column per variable. Next to each variable, write its meaning in a few words. A sample output reproduces a result but does not show whether a meaning broke, so you check the meanings, not the outputs. Pick the input first. Say which failure mode it attacks. Predict the result before you execute anything. A prediction that disagrees with the code is the whole point of the exercise.

<!-- stage: trace -->
### Dry Run On An Unbroken Climb

Trace the method on `[1, 2, 3]`. The variables start at `best = 0` and `current = 1`. At index 1 the value 2 beats 1, so `current` becomes 2 and `best` stays 0. At index 2 the value 3 beats 2, so `current` becomes 3 and `best` is still 0.

The loop ends. The method returns `best`, which is 0, although the true answer is 3. The table shows the problem in the final row. The variable `current` holds 3, a climb that is still open, and no line of code moves it into `best`. For the one-element list the same table shows the bug sooner, since the loop body never runs and the result is the initial 0. The step that matters is the one that does not happen, the missing update after the loop. A sample that ends with a drop hides it, because the `else` branch performs the update at the right moment.

```trace
{"cells":[1,2,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"best":0,"current":1},"note":"Start: best = 0, current = 1. The loop begins at index 1."},{"at":{"i":1},"vars":{"best":0,"current":2},"note":"Index 1: 2 beats 1, so current becomes 2. best is untouched because no climb has ended."},{"at":{"i":2},"vars":{"best":0,"current":3},"note":"Index 2: 3 beats 2, so current becomes 3. best is untouched because no climb has ended."},{"at":{"i":3},"vars":{"best":0,"current":3},"note":"The loop ends and returns best = 0. current holds an open climb of 3 that nothing recorded. The true answer is 3."}]}
```

<!-- stage: code -->
### Fix The Method And Rerun Attackers

```java
static int longestClimb(int[] steps) {
    if (steps.length == 0) return 0;
    int best = 1, current = 1;
    for (int i = 1; i < steps.length; i++) {
        current = steps[i] > steps[i - 1] ? current + 1 : 1;
        best = Math.max(best, current);          // record after every step, not only when a climb ends
    }
    return best;
}
```

The repair has two parts. The method updates `best` after every step, so an unfinished climb is always counted. It also starts `best` at 1, because any non-empty list contains a climb of length one. The specification of this method allows the empty list, and the method returns 0 for it explicitly. The method runs in O(n) time and O(1) space. The attackers `[7]`, `[1, 2, 3]`, `[4, 4, 4]` and `[3, 2, 1]` now pass. Each one hits a different failure mode, from initialization to equality.

<!-- stage: applicability -->
### Choose The Smallest Adversarial Input

Before you trust a solution, write down which failure modes it could have. Pick one tiny input for each. The invariant is that a dry run records the meaning of every variable after every state change. Each adversarial input then targets one weakness. Make the prediction first, then run the code.

The false friend is the large random test. Random data catches surprises you did not think of, and the next chapters use it as a cross-check. It is a poor substitute for a deliberately chosen tiny case, because edge cases occupy a vanishing share of the random space.

Java supplies several ready-made attackers. `Integer.MAX_VALUE` and `Integer.MIN_VALUE` break accumulators and negation, since `Math.abs(Integer.MIN_VALUE)` is still negative. A freshly allocated `int[]` holds zeros, which can look like real data. Comparing boxed `Integer` objects with `==` works for small values and fails for larger ones.

<!-- stage: exercises -->
### Exercises

#### [Build] Singleton (Author exercise)
<!-- id: pc-singleton -->

**Prerequisites.** The variable table from this lesson.

**Problem.** Dry-run the corrected `longestClimb` loop over `[7]`. Verify the initialization, the number of loop iterations and the returned value. Then say what the original flawed version returns.

**Constraints.** The input has exactly one element. The method contract allows lengths from 0 to 10^5.

**Example 1.** Input `[7]`, output 1, with zero loop iterations.

**Example 2.** Input `[7]` to the flawed version that starts `best` at 0, output 0, which shows the initialization bug.

**Hint.** How many times does a loop that starts at index 1 run when the array has one element? Which line is responsible for the result in that case?

**Changed decision.** The smallest legal input attacks initialization, because no loop iteration exists to repair it.

#### [Vary] All Equal (Author exercise)
<!-- id: pc-all-equal -->

**Prerequisites.** The singleton exercise above.

**Problem.** Use `[4,4,4]` to test strict versus non-strict comparisons. Compute the longest strictly increasing run and the longest non-decreasing run. Then explain why this one input tells the two comparisons apart.

**Constraints.** The array holds three equal values. A strict comparison uses `>` and a non-strict one uses `>=`.

**Example 1.** Input `[4,4,4]` with a strict comparison, output 1.

**Example 2.** Input `[4,4,4]` with a non-strict comparison, output 3.

**Hint.** What does each comparison say about two equal neighbors? Which kind of input makes the two versions disagree?

**Changed decision.** The attacked failure mode changes from initialization to equality handling.

#### [Boundary] Numeric Extremes (Author exercise)
<!-- id: pc-numeric-extremes -->

**Prerequisites.** The two exercises above.

**Problem.** Use `[Integer.MAX_VALUE, Integer.MAX_VALUE]` against code that accumulates a sum into an `int`. Predict the overflow before you run anything. Then state the correct sum and the type that holds it.

**Constraints.** The largest `int` is 2,147,483,647 and wrap-around arithmetic applies on overflow. Use `long` for the corrected sum.

**Example 1.** Input `[2147483647, 2147483647]` summed in an `int`, output -2.

**Example 2.** Input the same array summed in a `long`, output 4294967294.

**Hint.** Add the two numbers on paper and compare with 2^31 - 1. What does two's-complement wrap-around do to a sum just above the maximum?

**Changed decision.** The attacked failure mode becomes overflow, and the adversarial input comes from the extreme of the type.

#### [Recognize] Mutation Order (Author exercise)
<!-- id: pc-mutation-order -->

**Prerequisites.** All three exercises above.

**Problem.** To insert a value at index 0 of `[1,2,3]`, the elements must shift right inside an array of length 4. Trace a left-to-right copy. Show exactly where it overwrites data that the loop has not read yet. Then justify copying right to left.

**Constraints.** The array has length 4 with three live values. Inserting 9 at index 0 should produce `[9,1,2,3]`.

**Example 1.** Input `[1,2,3,_]` shifted left to right, output `[1,1,1,1]` before the insert, so the data is lost.

**Example 2.** Input `[1,2,3,_]` shifted right to left, output `[1,1,2,3]` before the insert, and `[9,1,2,3]` after it.

**Hint.** When you copy `a[0]` into `a[1]`, what happens to the old `a[1]`, and have you read it yet? In which direction can a write never land on an unread slot?

**Changed decision.** The attacked failure mode is the order of writes, which decides whether a copy destroys its own input.
