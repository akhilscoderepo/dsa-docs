<!-- lesson-kind: standard -->
<!-- lesson-id: input-guarantees -->
## Input Preconditions And Edge Cases

<!-- stage: context -->
### A Method That Guesses About Its Input

A weather station logs overnight temperatures in degrees below and above freezing. A small method reports the warmest reading of the night. For months it reports sensible values. Then a cold snap arrives and every reading is negative. The report says the warmest reading was 0 degrees, a night that never reached it.

A colleague proposes a fix: return 0 whenever something looks wrong. That fix also hides the night the logger was offline and sent an empty list. Both failures have the same cause. The method makes silent guesses about its input, and nobody wrote down what the caller promised. This lesson separates what the caller promises about the input from what the code assumes.

<!-- stage: naive -->
### Start At Zero And Guard Empty Input

The first version initializes the answer to zero, because zero seems a safe default. It adds a guard for the empty case, because the code might crash.

```java
static int warmest(int[] temps) {
    if (temps == null || temps.length == 0) return 0;
    int best = 0;
    for (int t : temps) {
        if (t > best) best = t;
    }
    return best;
}
```

The method never crashes, passes every sample with a positive reading, and looks careful. The author added each guard without a rule from the problem, and no guard ties to one.

<!-- stage: bottleneck -->
### Wrong Answers With Fine Time Complexity

#### Wrong Output With No Exception

The method returns 0 for `[-8, -3, -6]`, where the true maximum is -3. It also returns 0 for an empty array, which has no maximum at all. The time is O(n) and the space is O(1), so the time and space costs from the earlier lessons look fine. The damage is to correctness, and it is silent. The method throws no exception and gives no warning. It returns a plausible number.

#### A Guard Adds Behavior Nobody Asked For

The guard does a second kind of damage. It defines a behavior, "empty means 0", that the problem never requested. If the specification promises a non-empty array, the guard is dead code that suggests the opposite promise. If the specification allows empty input and expects an error, the guard hides that error. In both cases the code makes a claim about the problem that the author did not intend. Failures like this are expensive because they pass review, since each line reads as careful.

<!-- stage: insight -->
### Preconditions Versus Assumptions

Every problem states facts about its input, and a solution is correct only for inputs that satisfy them. List those facts before writing code, and keep them apart from anything your solution adds on top.

#### Define Precondition And Assumption

A **precondition** is a fact the caller promises in the problem statement, so the method may rely on it. Examples are a non-empty array, a range for the values, a rectangular grid, or sorted input. An **assumption** is anything your code depends on that the statement did not promise, even if it feels obvious. The rule is that code may rely on a documented precondition and must never invent one. If your code needs an assumption, it must check the assumption at run time or write it into the specification you hand back.

<!-- names: precondition, assumption, sentinel -->

#### Start From A Real Element

A precondition also decides the starting value. With a promised non-empty array, the maximum starts at the first element, because that element is a real member of the input. Starting from zero assumes that zero lies below every value. When the specification allows empty input, the method needs a documented way to say "there is no answer". One choice is a **sentinel**, a reserved value that cannot be a real answer. The alternatives are to throw an exception or to return an optional wrapper that makes absence part of the type. Whichever you pick, the method signature and the documentation must agree on it.

#### Use A Precondition Without Rechecking

A precondition can also support a stronger conclusion. If the statement promises a sorted array, equal values sit side by side in runs. The code can use that fact without checking it.

<!-- stage: variables -->
### Five Questions To Ask About Input

Check five input properties for every problem.

- **Emptiness** asks whether the input can be empty or null, and whether the statement says so.
- **Value and size ranges** ask for the limits on each element and on the length.
- **Ordering** asks whether the statement guarantees sorted order.
- **Shape** asks whether a two-dimensional input is rectangular.
- **No-answer result** asks what the method returns when no answer exists.

Mark each answer as a precondition from the statement or an assumption of your code. Every assumption needs a check or a note.

<!-- stage: trace -->
### Trace Two Starting Values On Negative Input

#### Run The Zero-Start Version

Run both initializations on `[-8, -3, -6]`.

- **best** starts at 0 in the zero-start version.
- **-8** fails the comparison, because -8 is not larger than 0, so best stays 0.
- **-3 and -6** fail the same comparison.
- **Result** is 0, although no reading reached 0.

#### Run The First-Element Version

- **best** starts at -8, a real reading.
- **-3** passes the comparison, because -3 is larger than -8, so best becomes -3.
- **-6** fails the comparison, so best stays -3.
- **Result** is -3, which is correct.

The starting value is the step most often overlooked. The zero-start version starts above every value in the array, so no later comparison can correct it.

#### Watch Both Versions Side By Side

```trace
{"cells":[-8,-3,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Start. The zero version holds 0 and the first-element version holds -8, a real reading."},{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Read -8. Zero version: not larger than 0, so it stays 0. First-element version holds -8."},{"at":{"i":1},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -3. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":2},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -6. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":3},"vars":{"zeroStart":0,"firstStart":-3},"note":"Loop ends. The zero version reports 0, a night that never reached 0. The first-element version reports -3."}]}
```

<!-- stage: code -->
### Write Methods With Stated Preconditions

#### Two Ways To Handle Empty Input

```java
// Contract: temps is non-empty. No guard, because the guarantee already covers it.
static int warmestNonEmpty(int[] temps) {
    int best = temps[0];
    for (int i = 1; i < temps.length; i++) best = Math.max(best, temps[i]);
    return best;
}

// Contract: temps may be empty. Absence is part of the return type.
static java.util.OptionalInt warmestOrNone(int[] temps) {
    if (temps.length == 0) return java.util.OptionalInt.empty();
    return java.util.OptionalInt.of(warmestNonEmpty(temps));
}
```

#### Compare Cost And Empty-Input Behavior

- **warmestNonEmpty** runs in O(n) time and O(1) extra space, and relies on its documented precondition.
- **Comment on the precondition** shows the missing guard is deliberate and not an oversight.
- **warmestOrNone** has the same cost and adds one branch that makes "no answer" explicit in the return type.
- **Optional return type** forces callers to handle the empty case.
- **IllegalArgumentException** is a third option for a specification that allows empty input, valid when the documentation states it.

Neither method invents a value.

<!-- stage: applicability -->
### Choose Guards And Starting Values Carefully

#### Run The Checklist First

Run the checklist before choosing initial values and before adding guards.

- **Invariant** is that code relies only on what the statement promises, and checks or documents everything else.
- **Starting values** come from real input whenever the specification allows.
- **Sentinel** is chosen only when it cannot collide with a real answer.

#### Skip Guards The Problem Never Asked For

A false friend in input handling is a guard that looks like robustness but contradicts the stated precondition. Here it is a guard added without a specification rule. Branches that handle cases the problem never allows obscure the actual algorithm. They can also define behavior nobody asked for. This is not an argument against validation in production services, where untrusted input needs checks. It is an argument about interview and contest problems, where the statement is the specification and an extra branch is a claim about it.

#### Watch For Java Input Traps

Java adds specific traps.

- **int[][] grid** may be ragged, so `grid[0].length` is unsafe for every row unless the statement guarantees rectangularity.
- **Integer.MIN_VALUE** as a sentinel collides with a legal answer if inputs may reach that value, and negating it overflows.
- **null array** differs from an empty array.
- **Unmentioned cases** are not promised, so a statement that mentions neither null nor empty input promises neither.

<!-- stage: exercises -->
### Exercises

#### [Build] Non-Empty Maximum (Author exercise)
<!-- id: pc-non-empty-maximum -->

**Prerequisites.** The input checklist from this lesson.

**Problem.** The precondition states that the array `nums` has at least one element. Return the largest value in `nums` by starting from `nums[0]` and comparing the remaining elements. Then explain two facts. First, starting from the value 0 gives a wrong result for `nums = [-8,-3]`. Second, an empty-array check is unnecessary under this specification.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`, with `nums[i]` of type `int`. The result is one `int`. If the maximum appears more than once, the value is the same. `nums` does not change. Do not add branches for inputs the specification excludes.

**Example 1.** Input `nums = [-8,-3]`, output -3, whereas a zero-start version would return 0.

**Example 2.** Input `nums = [7]`, output 7, so a single element is already a valid maximum.

**Hint.** Which real element of the input is promised to exist? What does a starting value of zero assume about the data?

**Changed decision.** Basic case: the starting value comes from the input itself, because the precondition promises it exists.

#### [Vary] Possibly Empty (Author exercise)
<!-- id: pc-possibly-empty -->

**Prerequisites.** The non-empty maximum exercise above.

**Problem.** Change the specification of the previous exercise so that `nums` may be empty. Then define the result for the empty case by choosing exactly one of three responses. A sentinel is a reserved `int` value that means "no answer". An exception is a thrown error. An optional result is a return type that either holds a value or is empty. Document the choice, and make the method signature match it. For a non-empty array, return the largest value.

**Constraints.** `0 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`, with `nums[i]` of type `int`. The response for the empty case must not equal any legal maximum. `nums` does not change.

**Example 1.** Input `nums = []` under an optional-result specification, output an empty optional.

**Example 2.** Input `nums = [-5]` under the same specification, output an optional holding -5, so a legal negative answer is never confused with "no answer".

**Hint.** Is there any `int` value that can never be a legal maximum for this range? If not, what should carry the "no answer" signal instead?

**Changed decision.** The specification now permits an empty input, so absence has to become part of the interface.

#### [Boundary] Rectangular Or Ragged (Author exercise)
<!-- id: pc-rectangular-or-ragged -->

**Prerequisites.** The two exercises above.

**Problem.** A two-dimensional array `int[][] grid` is rectangular if every row has the same length. It is ragged if rows may have different lengths, including length 0. A cell is one element `grid[r][c]`. Return the number of cells in `grid`. Explain why using `grid[0].length` as the column bound for every row is unsafe when ragged input is legal. Write a loop that is correct for both shapes.

**Constraints.** `0 <= grid.length <= 100`, so `grid` may have no rows. Under the ragged specification each row has a length of at least 0, and rows may differ. Every row is non-null. The result is one `int`. `grid` does not change.

**Example 1.** Input `grid = {{1,2,3},{4},{5,6}}` under a ragged specification, output a cell count of 6.

**Example 2.** Input `grid = {{1,2},{3,4}}` under a rectangular specification, output a cell count of 4, and either loop form gives the same result.

**Hint.** What does `grid[0].length` measure, one row or all rows? What bound do you use if every row can differ?

**Changed decision.** The shape promise changes from rectangular to ragged, so the inner loop bound moves from one shared length to each row's own length.

#### [Recognize] Sorted Promise (Author exercise)
<!-- id: pc-sorted-promise -->

**Prerequisites.** All three exercises above.

**Problem.** The precondition is that `nums` is sorted in non-decreasing order, so `nums[i] <= nums[i + 1]` for every valid `i`. Show that this precondition places equal values next to each other in runs. Use that fact to return the number of distinct values in `nums` with one pass over the array. Do not use binary search, two pointers or a set.

**Constraints.** `0 <= nums.length <= 10^5`, with `int` values. The sorted order is a precondition, so the code does not check it. For an empty array, return 0. The result is one `int`. `nums` does not change.

**Example 1.** Input `nums = [1,1,2,2,2,5]`, output 3 distinct values.

**Example 2.** Input `nums = []`, output 0, since an empty sorted array has no values and no runs.

**Hint.** If equal values are always neighbors, how can you tell that a new value has started? What would break if the array were not sorted?

**Changed decision.** A single promise, sorted order, replaces a whole lookup structure with a comparison against the previous element.
