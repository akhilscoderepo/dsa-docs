<!-- lesson-kind: standard -->
<!-- lesson-id: constraint-signals -->
## Constraint Signals

<!-- stage: context -->
### The Solution That Passed Every Sample

A teammate posts a pair-finding method for review. The task is to find two readings in a list whose sum equals a target, and the method passes all three sample inputs on the first run. She submits it to the grader and gets a time-limit failure on the fourth test. Nothing is wrong with the logic, which is the unsettling part. The method simply was never going to finish on the largest allowed input, and a glance at the last two lines of the problem statement would have told her so before she typed anything.

Those lines are the constraints, and most people read them last, if at all. This lesson is about reading them first. A constraint is a promise about how big the input can get, and every promise rules some approaches in and others out before any code exists.

<!-- stage: naive -->
### Write What Matches The Sample

The habit that produced the failure is to translate the sample directly into code and trust it. For the pair task, the direct translation checks every pair of positions.

```java
static boolean hasPairBrute(int[] nums, int target) {
    for (int i = 0; i < nums.length; i++) {
        for (int j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] == target) return true;
        }
    }
    return false;
}
```

On a sample with five readings it does ten comparisons and returns instantly. It is a correct method and a reasonable first draft.

<!-- stage: bottleneck -->
### Ten Comparisons Become Five Billion

Count the comparisons instead of timing the sample. For `n` readings there are `n * (n - 1) / 2` pairs, so the work grows as O(n^2). With `n = 5` that is 10 comparisons. With the stated maximum of `n = 100,000` it is 4,999,950,000, close to five billion, for a single call.

A judge or an interview machine performs very roughly one hundred million simple steps in the time we are normally given, and the exact figure varies by language and hardware. Five billion is fifty times over that, so the failure is not bad luck or a slow laptop. The sample could not reveal it because the sample is tiny, and the method's cost depends on the largest legal input, not the one on the page. The method needs O(1) extra space, which is fine, and the time is the entire problem.

<!-- stage: insight -->
### Read The Limits, Then Do The Arithmetic

Before choosing an approach, write down the largest legal input and compute how many steps each candidate would take on it. Compare that number to what the time limit allows. This takes ten seconds and eliminates whole families of solutions at once.

The number to compare against is the **operation budget**, the count of simple steps a solution may take on its worst legal input. A workable rule of thumb for interview-style limits is about 10^8 steps, and the rule is deliberately coarse, because the point is to separate "obviously fine" from "obviously impossible" and not to predict a stopwatch. The count for a candidate depends on its **growth class**, meaning how the step count changes as the input size changes. A single pass grows linearly, sorting grows a little faster than linearly, and all pairs grows with the square.

<!-- names: operation budget, growth class, constraint signal -->

Each limit in a statement is a **constraint signal**, a hint about which growth classes are allowed. The table lists the usual pairings. They are guides for a first filter, not laws.

| Largest input size | Growth classes that usually fit |
| --- | --- |
| about 20 | exponential search, trying every subset |
| about 500 | cubic loops, three nested scans |
| about 5,000 | quadratic loops, all pairs |
| about 100,000 | linear and n log n work |
| about 1,000,000 | linear work, small constants |

A second signal hides in the value range. If every value is tiny, a table indexed by value becomes affordable, and if values are huge, that table is impossible. A third signal is how many operations the problem asks for. The size of the data and the number of questions asked about it are two different quantities, and both belong in the arithmetic.

<!-- stage: variables -->
### Three Numbers And A Threshold

Write down the largest input size, the range of the values, and the number of operations the problem will ask you to perform. Add the budget as a fourth line, about 10^8. For each approach you are considering, compute its step count at the maximum and compare it with the budget. Use `long` for that arithmetic, because squaring 100,000 already overflows a 32-bit `int`, and an overflowed estimate can look comfortably small.

<!-- stage: trace -->
### Growing The Input Tenfold

Watch the pair method next to a sort-based method as the input grows. At `n = 10` the all-pairs count is 45 and a sort costs about 40 steps, so they look alike, and nobody learns anything from the sample. At `n = 1,000` all pairs reaches 499,500 against roughly 10,000 for sorting, and both are still instant. At `n = 100,000` the gap opens completely. All pairs needs 4,999,950,000 steps, which is far past the budget, while sorting needs about 1.7 million, which is a rounding error against it.

The lesson of the run is that the two methods are indistinguishable until the input is large, and the constraint line is the only place that tells you the input will be large. The hardest step to see is the middle one, where both methods still pass. A solution can pass every test you would think to write and still fail on the one the constraint announces.

```trace
{"cells":[10,1000,100000],"pointers":["n"],"steps":[{"at":{"n":0},"vars":{"scan":10,"sort":40,"allPairs":45,"allPairsVsBudget":"within"},"note":"n = 10: all pairs is 45 steps and sorting about 40, so the sample cannot tell the plans apart."},{"at":{"n":1},"vars":{"scan":1000,"sort":10000,"allPairs":499500,"allPairsVsBudget":"within"},"note":"n = 1,000: all pairs is 499,500 and sorting about 10,000. Both still finish instantly, which is the dangerous middle."},{"at":{"n":2},"vars":{"scan":100000,"sort":1700000,"allPairs":4999950000,"allPairsVsBudget":"over"},"note":"n = 100,000: all pairs is 4,999,950,000, fifty times the budget, while sorting is 1,700,000. The constraint line was the only warning."}]}
```

<!-- stage: code -->
### A Budget Calculator

```java
static final long BUDGET = 100_000_000L;

static long allPairs(long n) { return n * (n - 1) / 2; }

static long nLogN(long n) {
    long log = 64 - Long.numberOfLeadingZeros(Math.max(1, n - 1));   // ceiling of log2(n)
    return n * log;
}

static boolean plausible(long stepsAtMax) { return stepsAtMax <= BUDGET; }
```

All arithmetic is in `long`, and `n * (n - 1) / 2` multiplies before it divides, so the product `n * (n - 1)` is the thing that would overflow an `int`. The `nLogN` helper uses the bit length of `n - 1` as the ceiling of the base-2 logarithm, which is exact for powers of two. The helper is a thinking tool, so it stays coarse on purpose and ignores constants. Each call is O(1), and the method is only worth writing because the habit it builds, computing before coding, is worth having.

<!-- stage: applicability -->
### When Constraints Decide

Use this reading whenever a problem gives limits, which is nearly always. The invariant is that a proposed approach must stay within its operation budget and memory budget at the maximum legal input, not at the sample size. Before you commit to an idea, write one line such as "n up to 100,000, all pairs is 5 billion, too slow", and only then continue.

The false friend is the problem's difficulty label or its familiar noun. The word "array" does not select a method, and "easy" does not mean a brute force will pass. The contract selects the method. Another false friend is trusting the constant factor too much. When the count is within a factor of ten of the budget, the arithmetic is no longer decisive and you should look at what each step costs.

Java adds the overflow hazard already mentioned, plus the fact that boxed collections multiply memory use several times over compared with primitive arrays, which matters when the size limit is near a million. The exercises below ask you to make these calls without writing the algorithm, because the point here is choosing the family, and Chapter 01 onward supplies the algorithms.

<!-- stage: exercises -->
### Exercises

#### [Build] Budget Check (Author exercise)
<!-- id: pc-budget-check -->

**Prerequisites.** Reading Big-O notation for simple loops; this lesson.

**Problem.** A problem allows `1 <= n <= 100_000`. Classify each of three plans as plausible or implausible for an ordinary interview time limit: a single scan, a sort followed by a scan, and a comparison of every pair of elements. Support each answer with the step count at the maximum input.

**Constraints.** Use a budget of about 10^8 simple steps. Compute at `n = 100_000`, not at the sample size, and use `long` for any product.

**Example 1.** Input `n = 100000` with a single scan, output plausible, because the step count is about 10^5.

**Example 2.** Input `n = 100000` with all pairs, output implausible, because the count is 4,999,950,000, roughly fifty times the budget.

**Hint.** Do the estimate at the largest legal `n` and write the number out. Which two of the three plans land below 10^8, and which lands far above it?

**Changed decision.** First rung of the ladder: replaces a feeling about speed with a computed step count at the maximum input.

#### [Vary] Small Domain (Author exercise)
<!-- id: pc-small-domain -->

**Prerequisites.** The budget check above.

**Problem.** The limits are `1 <= n <= 100_000` and `0 <= nums[i] <= 100`. Explain why an auxiliary array of 101 counters is a reasonable plan here, and why the same plan is not reasonable when values can be any integer up to a billion. State the memory used in each case.

**Constraints.** Assume 4-byte `int` counters. Compare the 101-counter table against a table indexed directly by values up to 1,000,000,000.

**Example 1.** Input values limited to `0..100`, output a 101-slot table of about 404 bytes, which is trivial.

**Example 2.** Input values limited to `0..1_000_000_000`, output a table of about 4 gigabytes, which is not an acceptable plan.

**Hint.** The size of a value-indexed table is the size of the value range, not the number of elements. Which signal in the statement is doing the work here, the size limit or the value limit?

**Changed decision.** The signal changes from the input size to the value range, which decides whether a value-indexed table is affordable.

#### [Boundary] Hidden Overflow (Author exercise)
<!-- id: pc-hidden-overflow -->

**Prerequisites.** The two exercises above.

**Problem.** The limits are `n = 100_000` and `|nums[i]| <= 1_000_000_000`. Decide whether the sum of the whole array always fits in a Java `int`. Name the hostile input that decides the question, and say which type the accumulator should use.

**Constraints.** The largest `int` is 2,147,483,647. Consider the worst case, in which every element has the maximum legal magnitude.

**Example 1.** Input one hundred thousand copies of 1,000,000,000, output a sum of 100,000,000,000,000, which does not fit in an `int`.

**Example 2.** Input `[5, 7, 9]`, output a sum of 21, which fits easily, so a passing small test proves nothing about the limit.

**Hint.** Multiply the largest element by the largest count and compare the product with the `int` ceiling. Does the answer change if the values are mostly small but one hostile test uses the maximum?

**Changed decision.** The question moves from running time to numeric range, so the constraint signal now decides the accumulator type.

#### [Recognize] Query Pressure (Author exercise)
<!-- id: pc-query-pressure -->

**Prerequisites.** The budget check and the small-domain exercise.

**Problem.** A fixed array of 100,000 values is queried for range sums. Compare two situations: one query, and one hundred thousand queries over the same unchanged array. State which plans are acceptable in each, and explain why the number of operations, rather than the word "array", changes the design. Do not implement the faster plan, since the prefix-sum chapter owns it.

**Constraints.** `n = 100_000`, up to `q = 100_000` queries, each over an arbitrary range. Use the budget of about 10^8 steps.

**Example 1.** Input one query, output that a direct loop of at most 100,000 steps is acceptable.

**Example 2.** Input `q = 100000` queries, output that looping per query costs up to 10^10 steps in the worst case, so a smarter plan is required.

**Hint.** Multiply the cost of one query by the number of queries. At what query count does the plain loop leave the budget?

**Changed decision.** The signal changes from the size of the data to the number of operations asked about it.
