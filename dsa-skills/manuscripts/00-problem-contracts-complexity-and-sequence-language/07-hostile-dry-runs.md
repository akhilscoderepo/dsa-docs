<!-- lesson-kind: standard -->
<!-- lesson-id: hostile-dry-runs -->
## Writing Edge-Case Tests

<!-- stage: context -->
### Why Random Tests Miss Some Bugs

A developer writes a method that finds the longest climb in a list of daily step counts. A climb is the longest stretch where each day beats the one before. She tests it with the examples from the ticket. Then she tests it with a thousand random lists of a hundred days each, and everything passes. A week after release, a user with a single logged day sees "longest climb: 0 days" on their dashboard.

The random tests were not careless. They could not reach the failing case, because a random list of a hundred days almost never forms one unbroken climb and almost never has length one. A bug that hides behind a boundary appears only when you choose the boundary on purpose. This lesson shows how to design the smallest input that breaks one specific assumption in the code. It also shows how to trace the variables by hand so the broken assumption becomes visible.

<!-- stage: naive -->
### A Loop That Passes The Sample Tests

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

On `[1, 3, 2, 4, 5, 1]` it returns 3, which is correct. It passes the ticket's examples and nearly every random list. Most people stop when the tests turn green.

<!-- stage: bottleneck -->
### Why Random Lists Rarely Hit Edge Cases

```predict
Which step-count lists does the longest-climb method get wrong, and why do a thousand random lists not contain them?

The method returns 0 for a list of one day and for a list that climbs every day, because it updates `best` only when a climb ends. A random list almost never has length one or one unbroken climb, so the tests never reach those inputs.
```

Count the work that random testing performs. A thousand lists of a hundred values cost about 100,000 element visits, which is O(n) work per list and trivial to run. Now draw values from a small range such as 0 to 9. A list of more than ten days can never be strictly increasing from start to end. The failing case is an unbroken climb that never triggers the `else` branch, so it is unreachable at that size. A million such lists would still test the same behaviors that a thousand did.

The failing inputs are tiny. A list of one day returns 0 instead of 1, because the loop never runs and `best` keeps its initial value. A list that climbs every day also returns 0. The method updates `best` only when a climb ends, and the last climb never ends inside the loop. Both failures sit at the edge of the loop, where the first and last iterations behave differently from the middle. A small deliberate input reaches them in seconds.

<!-- stage: insight -->
### Choosing Test Inputs That Break One Assumption

#### Break One Assumption Per Test

Choose each test input to violate one assumption of the implementation. Each plausible implementation depends on an unstated assumption that the input is typical. The best test input is the smallest one that makes that assumption false.

A **dry run** is a hand execution of the code on a chosen input. You write down the value of every variable after every change. An **edge case** is a small input at the limit of what the code accepts, chosen to break one specific assumption, such as an empty list, a single element or the largest value. Each edge case targets one kind of bug. The usual kinds are initial values, equal values, boundaries, overflow and the order of writes.

<!-- names: dry run, edge case, invariant -->

#### Pick The Smallest Input Per Bug Type

Each kind of bug has a standard small edge case. For initial values, use the smallest legal input, often a single element. For equality, use all-equal values, so strict and non-strict comparisons give different answers. For boundaries, use inputs that fill or empty the structure exactly. For overflow, use extreme values in the type that accumulates. For the order of writes, use an input where a write destroys a value that the code has not read yet.

#### State What Every Variable Means

An **invariant** is a statement that stays true after every step. In a dry run, you keep one such statement: after each change you can say what every variable means. In the climb method, `current` is the length of the climb that ends at the index just examined. The variable `best` is the longest climb that has already ended. Written that way, the bug is obvious. A climb that is still open when the loop ends has not been recorded, so `best` is stale.

<!-- stage: variables -->
### Recording Variables During A Dry Run

A dry run uses a variable table with one row per state change and one column per variable. A sample output reproduces a result but does not show whether a variable lost its meaning. Check the meanings, not only the outputs. Follow this procedure.

You pick the input first, before you execute anything. Next you name the kind of bug, and the input targets it. Then you write the meaning of each variable beside its column in a few words.

After that, you write a prediction of the result before the code runs. A disagreement between prediction and code is the purpose of the exercise.

<!-- stage: trace -->
### Dry Run On A Strictly Increasing Array

Trace the flawed method on `[1, 2, 3]`.

The variable `best` starts at 0, and `current` starts at 1. Index 1 holds 2, which beats 1, so `current` becomes 2 and `best` stays 0. Index 2 holds 3, which beats 2, so `current` becomes 3 and `best` stays 0.

The loop then exits and returns `best`, which is 0, although the true answer is 3. The variable `current` holds 3 in the final row, an open climb that no line moves into `best`.

The remaining observations explain why the sample inputs miss the defect.

A one-element list runs no loop body, so the result is the initial 0. The missing update after the loop is the step that matters. A sample ending with a drop hides the defect, because the `else` branch updates `best` at the right moment.

```trace
{"cells":[1,2,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"best":0,"current":1},"note":"Start: best = 0, current = 1. The loop begins at index 1."},{"at":{"i":1},"vars":{"best":0,"current":2},"note":"Index 1: 2 beats 1, so current becomes 2. best is untouched because no climb has ended."},{"at":{"i":2},"vars":{"best":0,"current":3},"note":"Index 2: 3 beats 2, so current becomes 3. best is untouched because no climb has ended."},{"at":{"i":3},"vars":{"best":0,"current":3},"note":"The loop ends and returns best = 0. current holds an open climb of 3 that nothing recorded. The true answer is 3."}]}
```

<!-- stage: code -->
### Fixing The Method And Rerunning The Tests

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

The repair has three changes.

The update rule sets `best` after every step, so an unfinished climb is always counted. The initial value of `best` is 1, because any non-empty list contains a climb of length one. An empty list returns 0 explicitly, because the specification allows it.

- **Time** is O(n), because the loop makes one pass.
- **Space** is O(1), because two counters hold all the state.

The edge cases `[7]`, `[1, 2, 3]`, `[4, 4, 4]` and `[3, 2, 1]` now pass. Each one targets a different assumption, from the initial value to equal neighbors.

<!-- stage: applicability -->
### Edge Cases Versus Random Tests

Before you trust a solution, apply this checklist.

First, write down the kinds of bug that the solution could have. Next, choose one tiny edge-case input for each kind of bug. Then make a prediction first, and run the code after it. Throughout, the invariant of a dry run holds: you record the meaning of every variable after every change.

The large random test is a false friend. It looks like thorough verification, but it rarely reaches the boundary inputs, so it can pass while the failing precondition stays untested. Random data still catches surprises you did not predict, and the next chapters use it as a cross-check. It is a poor substitute for a deliberately chosen tiny case, because edge cases make up a tiny share of all random inputs.

Java supplies several ready-made edge cases.

`Integer.MAX_VALUE` and `Integer.MIN_VALUE` break accumulators and negation, since `Math.abs(Integer.MIN_VALUE)` is still negative. A freshly allocated `int[]` holds zeros, which can look like real data. A boxed `Integer` comparison with `==` works for small values and fails for larger ones.

<!-- stage: exercises -->
### Exercises

#### [Build] Singleton (Author exercise)
<!-- id: pc-singleton -->

**Prerequisites.** The variable table from this lesson.

**Problem.** The method `longestClimb(int[] a)` returns the length of the longest strictly increasing run in `a`. A run is a contiguous block of positions. A strictly increasing run has each value larger than the value before it. Execute the corrected loop by hand on the input `[7]`. State the initial value of `best`, the number of loop iterations and the returned value. Then state what the flawed version returns. The flawed version starts `best` at 0 and updates it only inside the loop.

**Constraints.** The limits are:
- **Length** is exactly 1, so `a.length == 1`, although the method accepts any length from 0 to 10^5.
- **Element** is an `int`.
- **Return value** is an `int` of at least 1 for any non-empty array.
- **Mutation** is none, so `a` is not modified.

**Example 1.** Input `[7]`, output 1, with zero loop iterations.

**Example 2.** Input `[7]` to the flawed version that starts `best` at 0, output 0, which shows the initialization bug.

**Hint.** How many times does a loop that starts at index 1 run when the array has one element? Which line is responsible for the result in that case?

**Changed decision.** The smallest legal input tests the initial value, because no loop iteration exists to repair it.

#### [Vary] All Equal (Author exercise)
<!-- id: pc-all-equal -->

**Prerequisites.** The singleton exercise above.

**Problem.** Take the array `[4,4,4]`. A strict comparison extends a run when `a[i] > a[i - 1]`. A non-strict comparison extends a run when `a[i] >= a[i - 1]`. Compute the length of the longest run under each comparison. Then explain why this one input gives different answers for the two comparisons.

**Constraints.** The limits are:
- **Array** has length 3, and every element is the `int` value 4.
- **Run** is a contiguous block of positions.
- **Equal neighbors** satisfy `a[i] == a[i - 1]`.
- **Return value** is an `int` of at least 1 for a non-empty array.
- **Mutation** is none for both methods.

**Example 1.** Input `[4,4,4]` with a strict comparison, output 1.

**Example 2.** Input `[4,4,4]` with a non-strict comparison, output 3.

**Hint.** What does each comparison say about two equal neighbors? Which kind of input makes the two versions disagree?

**Changed decision.** The bug under test changes from the initial value to equal values.

#### [Boundary] Numeric Extremes (Author exercise)
<!-- id: pc-numeric-extremes -->

**Prerequisites.** The two exercises above.

**Problem.** Take the array `[Integer.MAX_VALUE, Integer.MAX_VALUE]`. A method adds its elements into a variable of type `int`. Overflow occurs when the true sum lies outside the range of `int`. Predict the value this method returns before you run any code. Then state the true sum and name the type that holds it exactly. The corrected sum uses a `long` accumulator, which holds values up to 9,223,372,036,854,775,807.

**Constraints.** The limits are:
- **Array** has length 2.
- **Elements** are each the `int` value 2,147,483,647, which is the largest `int`.
- **Arithmetic** is 32-bit two's complement for `int` and wraps around on overflow without an exception.
- **Mutation** is none, so the array is not modified.

**Example 1.** Input `[2147483647, 2147483647]` summed in an `int`, output -2.

**Example 2.** Input the same array summed in a `long`, output 4294967294.

**Hint.** Add the two numbers on paper and compare with 2^31 - 1. What does two's-complement wrap-around do to a sum just above the maximum?

**Changed decision.** The bug under test becomes overflow, and the input comes from the extreme value of the type.

#### [Recognize] Mutation Order (Author exercise)
<!-- id: pc-mutation-order -->

**Prerequisites.** All three exercises above.

**Problem.** An array `a` of length 4 holds the three live values `[1,2,3]` in positions 0 to 2. Position 3 is free. To insert a value at index 0, every live value moves one position to the right. A left-to-right shift runs `a[i] = a[i - 1]` for `i = 1, 2, 3`. A right-to-left shift runs the same assignment for `i = 3, 2, 1`. Trace the left-to-right shift. Identify the first write that overwrites a value the loop has not yet read. Then explain why the right-to-left shift preserves every live value.

**Constraints.** The limits are:
- **Array** has length 4. Positions 0 to 2 hold live values.
- **Inserted value** is 9 at index 0.
- **Shift** writes positions 1 to 3 only.
- **Position 0** receives the inserted value after the shift completes.
- **Result** equals `[9,1,2,3]` after a correct shift and insert.
- **Values** are all `int`.

**Example 1.** Input `[1,2,3,_]` shifted left to right, output `[1,1,1,1]` before the insert, so the data is lost.

**Example 2.** Input `[1,2,3,_]` shifted right to left, output `[1,1,2,3]` before the insert, and `[9,1,2,3]` after it.

**Hint.** When you copy `a[0]` into `a[1]`, what happens to the old `a[1]`, and have you read it yet? In which direction can a write never land on an unread slot?

**Changed decision.** The bug under test is the order of writes, which decides whether a copy destroys its own input.
