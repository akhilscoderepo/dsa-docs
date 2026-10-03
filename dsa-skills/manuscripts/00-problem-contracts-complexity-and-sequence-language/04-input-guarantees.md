<!-- lesson-kind: standard -->
<!-- lesson-id: input-guarantees -->
## Input Guarantees

<!-- stage: context -->
### The Coldest Night Of The Year

A weather station logs overnight temperatures in degrees below and above freezing. A small method reports the warmest reading of the night, and for months it has reported sensible values. Then a cold snap arrives and every reading is negative. The report says the warmest reading was 0 degrees, a night that never reached it.

A colleague proposes a fix, which is to return 0 whenever something looks wrong. That fix would also hide the night the logger was offline and sent an empty list. Both failures come from the same place. The method makes silent guesses about its input, and nobody wrote down what the caller had actually promised. This lesson separates what the input is guaranteed to be from what the code merely hopes.

<!-- stage: naive -->
### Start From Zero, Guard Everything

The first version initializes the answer to zero because zero feels neutral, and it adds a guard for the empty case because the code might crash.

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

It never crashes, it passes every sample with a positive reading, and it looks careful. Each defensive line was added from habit, and no line is tied to a rule in the problem.

<!-- stage: bottleneck -->
### Confident Wrong Answers

The method returns 0 for `[-8, -3, -6]` when the true maximum is -3, and returns 0 for an empty array, which is not a maximum of anything. The time is O(n) and the space is O(1), so every cost the earlier lessons taught us to check looks fine. The damage is to correctness, and it is silent: no exception, no warning, just a plausible number.

The defensive guard is a second kind of damage. It defines a behavior, "empty means 0", that the problem never requested. If the contract promises a non-empty array, the guard is dead code that suggests the opposite promise. If the contract allows empty input and expects an error, the guard hides it. In both cases the code now makes a claim about the problem that the author did not intend. Failures like this are expensive precisely because they pass review, since each line reads as careful.

<!-- stage: insight -->
### Rely On The Promise, Never Invent One

Every problem makes a set of promises about its input, and a solution is correct only for inputs that keep them. Collect those promises before writing code, and keep them in a separate list from anything your solution adds on top.

An **input guarantee** is a fact the caller has promised, stated in the problem: the array is non-empty, the values lie in a given range, the grid is rectangular, the input is sorted. An **assumption** is anything your code depends on that the statement did not promise, even if it feels obvious. The rule is that code may rely on a documented guarantee and must never invent one. If an assumption is needed, it must either be checked at run time or be written into the contract you hand back.

<!-- names: input guarantee, assumption, sentinel -->

A guarantee also decides how to initialize. With a promised non-empty array, the maximum should start at the first element, since that is a real member of the input. Starting from zero is an assumption that zero lies below every value. When the contract does allow empty input, the method needs a documented way to say "there is no answer". One choice is a **sentinel**, a reserved value that cannot be a real answer. The alternatives are to throw an exception or to return an optional wrapper that makes absence part of the type. Whichever you pick, the method signature and the documentation must agree on it.

A guarantee can also unlock a stronger conclusion. If an array is promised sorted, equal values must sit side by side in runs, which is a structural fact the code can use without checking.

<!-- stage: variables -->
### A Short Contract Sheet

For any problem, keep five lines in view. Is the input possibly empty or null, and does the statement say so. What are the value and size ranges. Is there an ordering promise such as sorted order. What is the shape, meaning whether a two-dimensional input is rectangular. And what must the method return when no answer exists. Under each line, mark whether the statement promises it or your code assumes it. Anything in the second category needs a check or a note.

<!-- stage: trace -->
### Two Initializations Side By Side

Run both initializations on `[-8, -3, -6]`. The zero-start version holds 0 from the beginning. At -8 the comparison fails because -8 is not larger than 0, so it stays 0. At -3 and at -6 the same thing happens. The loop ends, and it reports 0 for a night in which no reading reached 0.

The first-element version starts from -8, since that is a real reading. At -3 the comparison succeeds, because -3 is larger than -8, and the best becomes -3. At -6 the comparison fails and the best stays -3. The loop reports -3, which is correct. The hardest step to notice is the very first one. The zero-start version never had a chance, because its starting value was already larger than everything it would see, and no later step could fix that.

```trace
{"cells":[-8,-3,-6],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Start. The zero version holds 0 and the first-element version holds -8, a real reading."},{"at":{"i":0},"vars":{"zeroStart":0,"firstStart":-8},"note":"Read -8. Zero version: not larger than 0, so it stays 0. First-element version holds -8."},{"at":{"i":1},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -3. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":2},"vars":{"zeroStart":0,"firstStart":-3},"note":"Read -6. Zero version: not larger than 0, so it stays 0. First-element version holds -3."},{"at":{"i":3},"vars":{"zeroStart":0,"firstStart":-3},"note":"Loop ends. The zero version reports 0, a night that never reached 0. The first-element version reports -3."}]}
```

<!-- stage: code -->
### Contracts In The Signature

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

Both methods run in O(n) time with O(1) extra space. The first trusts its guarantee and says so in a comment, so a reader knows the missing guard is deliberate and not an oversight. The second spends one branch to make "no answer" explicit, and callers must handle it because the type forces them to. Neither one invents a value. A third option for a contract that allows empty input is to throw `IllegalArgumentException` and document it, which is also fine as long as the contract says so.

<!-- stage: applicability -->
### Before Any Guard Or Initial Value

Run the contract sheet before choosing initial values and before adding guards. The invariant to hold is that code relies only on what the statement guarantees and checks or documents everything else. Initial values come from real input whenever the contract allows, and sentinels are chosen only when they cannot collide with a real answer.

The false friend is defensive programming added from habit. Branches that handle cases the problem never allows obscure the actual algorithm, and they can quietly define behavior nobody asked for. This is not an argument against validation in production services, where untrusted input does need checks. It is an argument about interview and contest problems, where the statement is the contract, and an extra branch is a claim about it.

Java adds specific traps. `int[][] grid` may be ragged, so `grid[0].length` is not safe for every row unless rectangularity is promised. Using `Integer.MIN_VALUE` as a sentinel collides with a legal answer if inputs may reach that value, and negating it overflows. A `null` array is a different case from an empty array, and a statement that mentions neither has promised neither.

<!-- stage: exercises -->
### Exercises

#### [Build] Non-Empty Maximum (Author exercise)
<!-- id: pc-non-empty-maximum -->

**Prerequisites.** The contract sheet from this lesson.

**Problem.** Under a contract that promises a non-empty array, return its maximum by initializing from `nums[0]`. Explain why initializing from zero fails for `[-8,-3]`, and why an empty-array guard is unnecessary under this exact contract.

**Constraints.** `1 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`. Do not add branches for inputs the contract excludes.

**Example 1.** Input `nums = [-8,-3]`, output -3, whereas a zero-start version would return 0.

**Example 2.** Input `nums = [7]`, output 7, so a single element is already a valid maximum.

**Hint.** Which real element of the input is guaranteed to exist? What does a starting value of zero assume about the data?

**Changed decision.** First rung: the starting value comes from the input itself because the contract guarantees it exists.

#### [Vary] Possibly Empty (Author exercise)
<!-- id: pc-possibly-empty -->

**Prerequisites.** The non-empty maximum exercise above.

**Problem.** Change the contract so the array may be empty. Choose and document exactly one response for the empty case, either a sentinel, an exception or an optional result, and make the method signature agree with that choice.

**Constraints.** `0 <= nums.length <= 10^5` and `-10^9 <= nums[i] <= 10^9`. The chosen response must not collide with any legal maximum.

**Example 1.** Input `nums = []` under an optional-result contract, output an empty optional.

**Example 2.** Input `nums = [-5]` under the same contract, output an optional holding -5, so a legal negative answer is never confused with "no answer".

**Hint.** Is there any `int` value that can never be a legal maximum for this range? If not, what should carry the "no answer" signal instead?

**Changed decision.** The contract now permits an empty input, so absence has to become part of the interface.

#### [Boundary] Rectangular Or Ragged (Author exercise)
<!-- id: pc-rectangular-or-ragged -->

**Prerequisites.** The two exercises above.

**Problem.** For `int[][] grid`, distinguish a rectangular guarantee from a ragged array. Explain why `grid[0].length` is unsafe as the column bound for every row when ragged input is legal, and write the loop that is safe in both cases.

**Constraints.** `0 <= grid.length <= 100`. Under the ragged contract each row may have a different length, including zero.

**Example 1.** Input `grid = {{1,2,3},{4},{5,6}}` under a ragged contract, output a cell count of 6.

**Example 2.** Input `grid = {{1,2},{3,4}}` under a rectangular contract, output a cell count of 4, and either loop form gives the same result.

**Hint.** What does `grid[0].length` measure, one row or all rows? What bound do you use if every row can differ?

**Changed decision.** The shape promise changes from rectangular to ragged, so the inner loop bound moves from one shared length to each row's own length.

#### [Recognize] Sorted Promise (Author exercise)
<!-- id: pc-sorted-promise -->

**Prerequisites.** All three exercises above.

**Problem.** An array is promised sorted in non-decreasing order. Show which conclusion this promise makes valid, namely that equal values form adjacent runs, and use it to count the distinct values in one pass. Do not introduce binary search or two pointers.

**Constraints.** `0 <= nums.length <= 10^5`. The sorted order is a guarantee and need not be checked.

**Example 1.** Input `nums = [1,1,2,2,2,5]`, output 3 distinct values.

**Example 2.** Input `nums = []`, output 0, since an empty sorted array has no values and no runs.

**Hint.** If equal values are always neighbors, how can you tell that a new value has started? What would break if the array were not sorted?

**Changed decision.** A single promise, sorted order, replaces a whole lookup structure with a comparison against the previous element.
