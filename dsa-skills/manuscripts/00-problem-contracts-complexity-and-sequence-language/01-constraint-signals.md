<!-- lesson-kind: standard -->
<!-- lesson-id: constraint-signals -->
## Constraint Signals

<!-- stage: context -->
### Why A Correct Solution Still Failed

A teammate posts a pair-finding method for review. The task is to find two readings in a list whose sum equals a target. The method passes all three sample inputs on the first run. She submits it to the grader and gets a time-limit failure on the fourth test. The logic is correct, which is the unsettling part. The method never could finish on the largest allowed input. The last two lines of the problem statement would have told her so before she typed anything.

Those lines are the constraints, and most people read them last, if at all. This lesson teaches you to read them first. A constraint promises how big the input can get. Each promise rules some approaches in and others out before any code exists.

<!-- stage: naive -->
### Translate The Sample Directly Into Code

The habit behind the failure is to turn the sample straight into code and trust it. For the pair task, the direct translation checks every pair of positions.

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

On a sample with five readings it makes ten comparisons and returns instantly. The method is correct, and it is a reasonable first draft.

<!-- stage: bottleneck -->
### Count The Comparisons At Maximum Input

Count the comparisons instead of timing the sample. For `n` readings there are `n * (n - 1) / 2` pairs, so the work grows as O(n^2). With `n = 5` that is 10 comparisons. With the stated maximum of `n = 100,000` it is 4,999,950,000, close to five billion, for a single call.

A judge or an interview machine performs very roughly one hundred million simple steps in the time we normally get. The exact figure varies by language and hardware. Five billion is fifty times over that, so the failure is not bad luck or a slow laptop. The sample cannot reveal it because the sample is tiny. The method's cost depends on the largest legal input, not the one on the page. The method needs O(1) extra space, which is fine, so the time is the entire problem.

<!-- stage: insight -->
### Read The Limits, Then Do The Arithmetic

#### Compute Steps At The Maximum

Before choosing an approach, write down the largest legal input. Then compute how many steps each candidate takes on it. Compare that number to what the time limit allows. This takes ten seconds and eliminates whole families of solutions at once.

#### Define Budget And Growth Class

The number to compare against is the **operation budget**, the count of simple steps a solution may take on its worst legal input. A workable rule of thumb for interview-style limits is about 10^8 steps. The rule is deliberately coarse. It separates "obviously fine" from "obviously impossible" and does not predict a stopwatch. The count for a candidate depends on its **growth class**, meaning how the step count changes as the input size changes. A single pass grows linearly, sorting grows a little faster than linearly, and all pairs grows with the square.

<!-- names: operation budget, growth class, constraint signal -->

#### Match Each Limit To A Signal

Each limit in a statement is a **constraint signal**, a hint about which growth classes are allowed. The table lists the usual pairings. They guide a first filter and are not laws.

| Largest input size | Growth classes that usually fit |
| --- | --- |
| about 20 | exponential search, trying every subset |
| about 500 | cubic loops, three nested scans |
| about 5,000 | quadratic loops, all pairs |
| about 100,000 | linear and n log n work |
| about 1,000,000 | linear work, small constants |

A second signal hides in the value range. If every value is tiny, a table indexed by value is affordable. If values are huge, that table is impossible. A third signal is how many operations the problem asks for. The size of the data and the number of questions about it are two different quantities. Both belong in the arithmetic.

<!-- stage: variables -->
### Write Down Three Numbers And A Budget

Write down the largest input size, the range of the values, and the number of operations the problem asks you to perform. Add the budget as a fourth line, about 10^8. For each approach you consider, compute its step count at the maximum and compare it with the budget. Use `long` for that arithmetic. Squaring 100,000 already overflows a 32-bit `int`, and an overflowed estimate can look comfortably small.

<!-- stage: trace -->
### Compare Two Methods As n Grows

#### Watch The Gap Open

Watch the pair method next to a sort-based method as the input grows. At `n = 10` the all-pairs count is 45 and a sort costs about 40 steps. The two look alike, so the sample teaches nothing. At `n = 1,000` all pairs reaches 499,500 against roughly 10,000 for sorting, and both are still instant. At `n = 100,000` the gap opens completely. All pairs needs 4,999,950,000 steps, far past the budget. Sorting needs about 1.7 million, a rounding error against it.

#### Read The Lesson Of The Run

The two methods look the same until the input is large. The constraint line is the only place that says the input is large. The hardest step to see is the middle one, where both methods still pass. A solution can pass every test you think to write and still fail on the one the constraint announces.

```trace
{"cells":[10,1000,100000],"pointers":["n"],"steps":[{"at":{"n":0},"vars":{"scan":10,"sort":40,"allPairs":45,"allPairsVsBudget":"within"},"note":"n = 10: all pairs is 45 steps and sorting about 40, so the sample cannot tell the plans apart."},{"at":{"n":1},"vars":{"scan":1000,"sort":10000,"allPairs":499500,"allPairsVsBudget":"within"},"note":"n = 1,000: all pairs is 499,500 and sorting about 10,000. Both still finish instantly, which is the dangerous middle."},{"at":{"n":2},"vars":{"scan":100000,"sort":1700000,"allPairs":4999950000,"allPairsVsBudget":"over"},"note":"n = 100,000: all pairs is 4,999,950,000, fifty times the budget, while sorting is 1,700,000. The constraint line was the only warning."}]}
```

<!-- stage: code -->
### Compute Step Counts In Code

```java
static final long BUDGET = 100_000_000L;

static long allPairs(long n) { return n * (n - 1) / 2; }

static long nLogN(long n) {
    long log = 64 - Long.numberOfLeadingZeros(Math.max(1, n - 1));   // ceiling of log2(n)
    return n * log;
}

static boolean plausible(long stepsAtMax) { return stepsAtMax <= BUDGET; }
```

All arithmetic uses `long`. The expression `n * (n - 1) / 2` multiplies before it divides, so the product `n * (n - 1)` is the value that would overflow an `int`. The `nLogN` helper takes the bit length of `n - 1` as the ceiling of the base-2 logarithm, which is exact for powers of two. The helper is a thinking tool, so it stays coarse on purpose and ignores constants. Each call is O(1). The code is worth writing because it builds a good habit, computing before coding.

<!-- stage: applicability -->
### When Constraints Decide

#### Apply The Invariant

Use this reading whenever a problem gives limits, which is nearly always. The invariant is that a proposed approach stays within its operation budget and memory budget at the maximum legal input, not at the sample size. Before you commit to an idea, write one line such as "n up to 100,000, all pairs is 5 billion, too slow". Then continue.

#### Avoid The False Friends

The first false friend is the problem's difficulty label or its familiar noun. The word "array" does not select a method, and "easy" does not mean a brute force passes. The constraints select the method. Another false friend is trusting the constant factor too much. When the count is within a factor of ten of the budget, the arithmetic is no longer decisive, so look at what each step costs.

#### Watch Java Memory And Overflow

Java adds the overflow hazard already mentioned. Boxed collections also use several times more memory than primitive arrays, which matters when the size limit is near a million. The exercises below ask you to make these calls without writing the algorithm. This lesson chooses the family, and Chapter 01 onward supplies the algorithms.

<!-- stage: exercises -->
### Exercises

#### [Build] Budget Check (Author exercise)
<!-- id: pc-budget-check -->

**Prerequisites.** Reading Big-O notation for simple loops; this lesson.

**Problem.** A problem statement guarantees that the input size `n` satisfies `1 <= n <= 100_000`. A step is one basic operation, such as one comparison or one addition. Consider three plans. Plan A scans the array once. Plan B sorts the array and then scans it once. Plan C compares every unordered pair of distinct elements. For each plan, compute the number of steps at the largest legal `n`. Then return "plausible" if that number is at most the step budget, and "implausible" if it is larger. Show the step count that supports each answer.

**Constraints.** The step budget is 10^8 (100,000,000) steps. Compute every count at `n = 100_000`, not at the size of a sample input. Use `long` for every product, because `n * n` exceeds the `int` maximum. Plan A costs `n` steps. Plan B costs about `n * log2(n)` steps for the sort plus `n` steps for the scan. Plan C costs `n * (n - 1) / 2` steps. Ties go to "plausible": a count equal to the budget is plausible. The exercise has no mutable input.

**Example 1.** Input `n = 100000` with a single scan, output plausible, because the step count is about 10^5.

**Example 2.** Input `n = 100000` with all pairs, output implausible, because the count is 4,999,950,000, roughly fifty times the budget.

**Hint.** Do the estimate at the largest legal `n` and write the number out. Which two of the three plans land below 10^8, and which lands far above it?

**Changed decision.** First rung of the ladder: replaces a feeling about speed with a computed step count at the maximum input.

#### [Vary] Small Domain (Author exercise)
<!-- id: pc-small-domain -->

**Prerequisites.** The budget check above.

**Problem.** A value-indexed table is an array in which slot `v` stores data about the value `v`. Such a table needs one slot for every value that can occur, so its size equals the size of the value range. Consider an input array `nums` of `n` integers, where `1 <= n <= 100_000` and `0 <= nums[i] <= 100`. Compute the memory in bytes of a table with one `int` counter per possible value. Then compute the memory of the same kind of table when `0 <= nums[i] <= 1_000_000_000`. State for each case whether the table is an acceptable plan, and name the limit in the statement that decides the answer.

**Constraints.** Each counter is a 4-byte `int`. The first table has exactly 101 slots, for the values `0` through `100`. The second table has exactly 1,000,000,001 slots, for the values `0` through `1_000_000_000`. The memory is `slots * 4` bytes, computed in `long`. The size `n` does not change the table size. The exercise has no mutable input and no empty input.

**Example 1.** Input values limited to `0..100`, output a 101-slot table of about 404 bytes, which is trivial.

**Example 2.** Input values limited to `0..1_000_000_000`, output a table of about 4 gigabytes, which is not an acceptable plan.

**Hint.** The size of a value-indexed table is the size of the value range, not the number of elements. Which signal in the statement is doing the work here, the size limit or the value limit?

**Changed decision.** The signal changes from the input size to the value range, which decides whether a value-indexed table is affordable.

#### [Boundary] Hidden Overflow (Author exercise)
<!-- id: pc-hidden-overflow -->

**Prerequisites.** The two exercises above.

**Problem.** An input array `nums` has `n` elements, where `n = 100_000` and `-1_000_000_000 <= nums[i] <= 1_000_000_000`. The sum of the array is the total of all its elements. Decide whether the sum always fits in a Java `int`, that is, whether it always lies between -2,147,483,648 and 2,147,483,647. Return "yes" or "no". If the answer is "no", give one input array whose sum does not fit. Name the type that the accumulator variable must have.

**Constraints.** The largest `int` is 2,147,483,647. The largest `long` is 9,223,372,036,854,775,807. The worst case sets every element to the largest legal magnitude, which is 1_000_000_000. Elements are `int` values. The array has at least one element. An `int` accumulator wraps around silently on overflow and raises no error. The method does not modify `nums`.

**Example 1.** Input one hundred thousand copies of 1,000,000,000, output a sum of 100,000,000,000,000, which does not fit in an `int`.

**Example 2.** Input `[5, 7, 9]`, output a sum of 21, which fits easily, so a passing small test proves nothing about the limit.

**Hint.** Multiply the largest element by the largest count and compare the product with the `int` ceiling. Does the answer change if the values are mostly small but one adversarial test uses the maximum?

**Changed decision.** The question moves from running time to numeric range, so the constraint signal now decides the accumulator type.

#### [Recognize] Query Pressure (Author exercise)
<!-- id: pc-query-pressure -->

**Prerequisites.** The budget check and the small-domain exercise.

**Problem.** An array of `n = 100_000` integers does not change. A range-sum query gives two positions `l` and `r` and asks for the sum of the elements from position `l` through position `r`. Compare two workloads on the same array: workload one has a single query, and workload two has `q = 100_000` queries. For each workload, compute the total step count of answering every query with a plain loop over the range. Return whether that plan stays within the step budget. Explain that the number of queries, not the type of the data, decides whether the plan is acceptable. Do not implement a faster plan.

**Constraints.** `n = 100_000` and `1 <= q <= 100_000`. Each query range may cover the whole array, so one query costs up to `n` steps. The step budget is 10^8 steps. Compute the total as `n * q` in `long`, because `10^10` exceeds the `int` maximum. A total equal to the budget is within budget. The array is never modified between queries.

**Example 1.** Input one query, output that a direct loop of at most 100,000 steps is acceptable.

**Example 2.** Input `q = 100000` queries, output that looping per query costs up to 10^10 steps in the worst case, so a smarter plan is required.

**Hint.** Multiply the cost of one query by the number of queries. At what query count does the plain loop leave the budget?

**Changed decision.** The signal changes from the size of the data to the number of operations asked about it.
