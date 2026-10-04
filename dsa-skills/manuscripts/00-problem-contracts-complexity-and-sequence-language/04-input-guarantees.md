<!-- lesson-kind: standard -->
<!-- lesson-id: input-guarantees -->
## Input Guarantees

<!-- stage: context -->
### A Wrong Maximum On The Coldest Night

A weather station logs overnight temperatures in degrees below and above freezing. A small method reports the warmest reading of the night. For months it reports sensible values. Then a cold snap arrives and every reading is negative. The report says the warmest reading was 0 degrees, a night that never reached it.

A colleague proposes a fix: return 0 whenever something looks wrong. That fix also hides the night the logger was offline and sent an empty list. Both failures have the same cause. The method makes silent guesses about its input, and nobody wrote down what the caller promised. This lesson separates what the input is guaranteed to be from what the code merely hopes.

<!-- stage: naive -->
### Start From Zero And Guard Everything

The first version initializes the answer to zero, because zero feels neutral. It adds a guard for the empty case, because the code might crash.

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

The method never crashes, passes every sample with a positive reading, and looks careful. Habit added each defensive line, and no line ties to a rule in the problem.

<!-- stage: bottleneck -->
### Confident Wrong Answers

#### Wrong Results Without Errors

The method returns 0 for `[-8, -3, -6]`, where the true maximum is -3. It also returns 0 for an empty array, which has no maximum at all. The time is O(n) and the space is O(1), so every cost the earlier lessons taught us to check looks fine. The damage is to correctness, and it is silent. The method throws no exception and gives no warning. It returns a plausible number.

#### Guards That Claim Too Much

The defensive guard does a second kind of damage. It defines a behavior, "empty means 0", that the problem never requested. If the specification promises a non-empty array, the guard is dead code that suggests the opposite promise. If the specification allows empty input and expects an error, the guard hides that error. In both cases the code makes a claim about the problem that the author did not intend. Failures like this are expensive because they pass review, since each line reads as careful.

<!-- stage: insight -->
### Rely On The Promise, Never Invent One

Every problem makes a set of promises about its input, and a solution is correct only for inputs that keep them. Collect those promises before writing code. Keep them in a separate list from anything your solution adds on top.

#### Separate Guarantees From Assumptions

An **input guarantee** is a fact the caller has promised in the problem statement. Examples are a non-empty array, a range for the values, a rectangular grid, or sorted input. An **assumption** is anything your code depends on that the statement did not promise, even if it feels obvious. The rule is that code may rely on a documented guarantee and must never invent one. If your code needs an assumption, it must check the assumption at run time or write it into the specification you hand back.

<!-- names: input guarantee, assumption, sentinel -->

#### Initialize From Real Input

A guarantee also decides how to initialize. With a promised non-empty array, the maximum starts at the first element, because that element is a real member of the input. Starting from zero assumes that zero lies below every value. When the specification allows empty input, the method needs a documented way to say "there is no answer". One choice is a **sentinel**, a reserved value that cannot be a real answer. The alternatives are to throw an exception or to return an optional wrapper that makes absence part of the type. Whichever you pick, the method signature and the documentation must agree on it.

#### Draw Stronger Conclusions

A guarantee can also unlock a stronger conclusion. If the statement promises a sorted array, equal values sit side by side in runs. The code can use that structural fact without checking it.

<!-- stage: variables -->
### Five Questions About The Input

For any problem, keep five questions in view. Can the input be empty or null, and does the statement say so? What are the value and size ranges? Is there an ordering promise, such as sorted order? What is the shape, meaning whether a two-dimensional input is rectangular? What must the method return when no answer exists? Under each question, mark whether the statement promises the answer or your code assumes it. Anything in the second category needs a check or a note.

<!-- stage: trace -->
### Two Initializations Side By Side

#### Run The Zero-Start Version

Run both initializations on `[-8, -3, -6]`. The zero-start version holds 0 from the beginning. At -8 the comparison fails, because -8 is not larger than 0, so the best stays 0. At -3 and at -6 the same thing happens. The loop ends and reports 0, for a night in which no reading reached 0.

#### Run The First-Element Version

The first-element version starts from -8, because that is a real reading. At -3 the comparison succeeds, because -3 is larger than -8, so the best becomes -3. At -6 the comparison fails and the best stays -3. The loop reports -3, which is correct. The hardest step to notice is the very first one. The zero-start version never had a chance. Its starting value was already larger than everything it would see, and no later step could fix that.

#### Replay Both Versions Step By Step

```trace
{"cells":[-8,-3,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Start. The zero version holds 0 and the first-element version holds -8, a real reading."},{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Read -8. Zero version: not larger than 0, so it stays 0. First-element version holds -8."},{"at":{"i":1},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -3. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":2},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -6. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":3},"vars":{"zeroStart":0,"firstStart":-3},"note":"Loop ends. The zero version reports 0, a night that never reached 0. The first-element version reports -3."}]}
```

<!-- stage: code -->
### Guarantees Stated In The Signature

#### Write Both Methods

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

#### Compare Their Behavior

Both methods run in O(n) time with O(1) extra space. The first trusts its guarantee and says so in a comment, so a reader knows the missing guard is deliberate and not an oversight. The second spends one branch to make "no answer" explicit. Callers must handle it, because the type forces them to. Neither method invents a value. A third option for a specification that allows empty input is to throw `IllegalArgumentException` and document it. That option is also fine, as long as the specification says so.

<!-- stage: applicability -->
### Before Any Guard Or Initial Value

#### Run The Checklist First

Run the checklist before choosing initial values and before adding guards. The invariant to hold is that code relies only on what the statement guarantees and checks or documents everything else. Initial values come from real input whenever the specification allows. Choose a sentinel only when it cannot collide with a real answer.

#### Spot The False Friend

The false friend is defensive programming added from habit. Branches that handle cases the problem never allows obscure the actual algorithm. They can also define behavior nobody asked for. This is not an argument against validation in production services, where untrusted input needs checks. It is an argument about interview and contest problems, where the statement is the specification and an extra branch is a claim about it.

#### Watch For Java Traps

Java adds specific traps. `int[][] grid` may be ragged, so `grid[0].length` is not safe for every row unless the statement promises rectangularity. `Integer.MIN_VALUE` as a sentinel collides with a legal answer if inputs may reach that value, and negating it overflows. A `null` array differs from an empty array. A statement that mentions neither has promised neither.

<!-- stage: exercises -->
### Exercises

#### [Build] Non-Empty Maximum (Author exercise)
<!-- id: pc-non-empty-maximum -->

**Prerequisites.** The input checklist from this lesson.

**Problem.** The specification guarantees that the array `nums` has at least one element. Return the largest value in `nums` by starting from `nums[0]` and comparing the remaining elements. Then explain two facts. First, starting from the value 0 gives a wrong result for `nums = [-8,-3]`. Second, an empty-array check is unnecessary under this specification.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`, with `nums[i]` of type `int`. The result is one `int`. If the maximum appears more than once, the value is the same. `nums` does not change. Do not add branches for inputs the specification excludes.

**Example 1.** Input `nums = [-8,-3]`, output -3, whereas a zero-start version would return 0.

**Example 2.** Input `nums = [7]`, output 7, so a single element is already a valid maximum.

**Hint.** Which real element of the input is guaranteed to exist? What does a starting value of zero assume about the data?

**Changed decision.** First rung: the starting value comes from the input itself, because the specification guarantees it exists.

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

**Example 1.** Input `grid = {{1,2,3},{4},{5,6}}` under a ragged contract, output a cell count of 6.

**Example 2.** Input `grid = {{1,2},{3,4}}` under a rectangular contract, output a cell count of 4, and either loop form gives the same result.

**Hint.** What does `grid[0].length` measure, one row or all rows? What bound do you use if every row can differ?

**Changed decision.** The shape promise changes from rectangular to ragged, so the inner loop bound moves from one shared length to each row's own length.

#### [Recognize] Sorted Promise (Author exercise)
<!-- id: pc-sorted-promise -->

**Prerequisites.** All three exercises above.

**Problem.** The specification guarantees that `nums` is sorted in non-decreasing order, so `nums[i] <= nums[i + 1]` for every valid `i`. Show that this guarantee places equal values next to each other in runs. Use that fact to return the number of distinct values in `nums` with one pass over the array. Do not use binary search, two pointers or a set.

**Constraints.** `0 <= nums.length <= 10^5`, with `int` values. The sorted order is guaranteed, so the code does not check it. For an empty array, return 0. The result is one `int`. `nums` does not change.

**Example 1.** Input `nums = [1,1,2,2,2,5]`, output 3 distinct values.

**Example 2.** Input `nums = []`, output 0, since an empty sorted array has no values and no runs.

**Hint.** If equal values are always neighbors, how can you tell that a new value has started? What would break if the array were not sorted?

**Changed decision.** A single promise, sorted order, replaces a whole lookup structure with a comparison against the previous element.
