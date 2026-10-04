<!-- lesson-kind: standard -->
<!-- lesson-id: constraint-signals -->
## Reading Input Limits Before Choosing An Algorithm

<!-- stage: context -->
### Why Correct Code Fails On Large Input

A developer posts a pair-finding method for code review. The task is to find two readings in a list whose sum equals a target. The method passes all three sample inputs on the first run. She submits it to the grader, and the fourth test fails because the method runs too slowly. The logic is correct. The method cannot finish on the largest allowed input. The last two lines of the problem statement show this before any code exists.

Those lines are the constraints, and most readers check them last, if at all. This lesson teaches you to read them first. A constraint states how large the input can get. Each constraint rules some approaches in and others out before you write code.

<!-- stage: naive -->
### Checking Every Pair Directly

The common error is to turn the sample straight into code and trust it. For the pair task, the direct translation checks every pair of positions.

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
### Counting Comparisons At The Largest Input

Count the comparisons instead of timing the sample. For `n` readings there are `n * (n - 1) / 2` pairs, so the work grows as O(n^2). With `n = 5` that is 10 comparisons. With the stated maximum of `n = 100,000` it is 4,999,950,000, close to five billion, for a single call.

A judge or an interview machine performs very roughly one hundred million simple steps in the time we normally get. The exact figure varies by language and hardware. Five billion is fifty times over that figure. The failure is not bad luck or a slow laptop. The sample cannot reveal it, because the sample is tiny. The cost of the method depends on the largest legal input, not the one on the page. The method needs O(1) extra space, which is fine, so time is the entire problem.

<!-- stage: insight -->
### Estimating Steps From The Input Limits

#### Counting Steps At The Largest Input

Before choosing an approach, write down the largest legal input. Then compute how many steps each candidate takes on it. Compare that number with what the time limit allows. This takes ten seconds and eliminates whole families of solutions at once.

#### What A Time Limit Allows

The **time limit** is how long a judge lets a solution run on its worst legal input. A rule of thumb for interview-style problems is that about 10^8 simple steps fit in that time. The rule is coarse. It separates clearly feasible from clearly infeasible and does not predict a stopwatch. The step count of a candidate depends on its **time complexity**. The time complexity states how the number of steps grows with the input size. A single pass is O(n). Sorting is O(n log n). Comparing all pairs is O(n^2).

<!-- names: time limit, time complexity, input constraint -->

#### Choosing Algorithms From Input Size

Each limit in a problem statement is an **input constraint**. It restricts which time complexities are feasible. The table lists the usual pairings. They give a first filter and are not laws.

| Largest input size | Growth classes that usually fit |
| --- | --- |
| about 20 | exponential search, trying every subset |
| about 500 | cubic loops, three nested scans |
| about 5,000 | quadratic loops, all pairs |
| about 100,000 | linear and n log n work |
| about 1,000,000 | linear work, small constants |

A second input constraint is the value range. If every value is small, a table indexed by value fits in memory. If values are huge, that table is impossible. A third input constraint is the number of queries or updates the problem requests. The size of the data and the number of queries are different quantities. Both belong in the arithmetic.

<!-- stage: variables -->
### Numbers To Write Down First

Write down four parameters. Then compute the step count of each candidate approach.

- **n** is the largest legal input size.
- **Value range** is the minimum and maximum allowed element value.
- **q** is the number of queries or updates the problem requests.
- **Time limit** is about 10^8 simple steps.
- **Step count** is the number of steps one approach takes at the maximum, compared with the time limit.
- **long** holds every estimate, because squaring 100,000 overflows a 32-bit `int`.

An overflowed estimate can look comfortably small, so it hides the problem.

<!-- stage: trace -->
### Comparing Step Counts As n Grows

#### Comparing Both Methods At Three Sizes

Compare the pair method with a sort-based method as the input grows.

- **n = 10** gives 45 all-pairs steps against about 40 for sorting, so the sample cannot separate the methods.
- **n = 1,000** gives 499,500 all-pairs steps against roughly 10,000 for sorting, and both finish instantly.
- **n = 100,000** gives 4,999,950,000 all-pairs steps, far past the time limit.
- **Sorting** needs about 1.7 million steps at `n = 100,000`, a rounding error against that count.

#### Reading The Result

The two methods look the same until the input is large. The middle row is the hardest to see, because both methods still pass.

- **Constraint line** is the only part of the statement that says the input is large.
- **Passing tests** do not prove feasibility, because a solution can pass every test you write and still fail on the maximum.

```trace
{"cells":[10,1000,100000],"pointers":["n"],"steps":[{"at":{"n":0},"vars":{"scan":10,"sort":40,"allPairs":45,"allPairsVsBudget":"within"},"note":"n = 10: all pairs is 45 steps and sorting about 40, so the sample cannot tell the plans apart."},{"at":{"n":1},"vars":{"scan":1000,"sort":10000,"allPairs":499500,"allPairsVsBudget":"within"},"note":"n = 1,000: all pairs is 499,500 and sorting about 10,000. Both still finish instantly, which is the dangerous middle."},{"at":{"n":2},"vars":{"scan":100000,"sort":1700000,"allPairs":4999950000,"allPairsVsBudget":"over"},"note":"n = 100,000: all pairs is 4,999,950,000, fifty times the budget, while sorting is 1,700,000. The constraint line was the only warning."}]}
```

<!-- stage: code -->
### Computing Step Counts In Code

```java
static final long BUDGET = 100_000_000L;

static long allPairs(long n) { return n * (n - 1) / 2; }

static long nLogN(long n) {
    long log = 64 - Long.numberOfLeadingZeros(Math.max(1, n - 1));   // ceiling of log2(n)
    return n * log;
}

static boolean plausible(long stepsAtMax) { return stepsAtMax <= BUDGET; }
```

The helpers compute step counts only.

- **long** holds all arithmetic in the helpers.
- **n * (n - 1) / 2** multiplies before it divides, so the product is the value that would overflow an `int`.
- **nLogN** takes the bit length of `n - 1` as the ceiling of the base-2 logarithm, which is exact for powers of two.
- **Precision** stays coarse on purpose, because the helpers ignore constants.
- **Time** is O(1) per call, because each helper evaluates one expression.
- **Space** is O(1) per call, because each helper stores a few `long` values.

Write the helpers to compute the step count before you write the algorithm.

<!-- stage: applicability -->
### Checking The Limits Before Coding

#### Applying The Invariant

Use this check whenever a problem gives limits, which is nearly always. Before you commit to an approach, write one line such as "n up to 100,000, all pairs is 5 billion, too slow". Then continue.

- **Invariant** is that the chosen approach stays within the time limit and the memory limit at the maximum legal input.
- **Sample size** never replaces the maximum legal input in this check.

#### Finding Cases That Break The Precondition

The precondition of this check is that the step count at the maximum input decides feasibility. The check has false friends, cases that match the pattern on the surface but break the precondition that the step count decides feasibility. Two cases qualify.

- **Difficulty label** misleads, because a label such as "easy" or a familiar noun such as "array" does not select a method.
- **Constant factor** misleads near the limit, because a count within a factor of ten of the limit is not decisive.
- **Step cost** decides the near-limit case, so compare what each step costs.

#### Avoiding Java Memory And Overflow Problems

- **int overflow** wraps silently, as the lesson showed earlier.
- **Boxed collections** use several times more memory than primitive arrays.
- **Size near 1,000,000** makes that memory difference matter.

The exercises below ask you to make these decisions without writing the algorithm. This lesson chooses the family of approaches. Chapter 01 onward supplies the algorithms.

<!-- stage: exercises -->
### Exercises

#### [Build] Budget Check (Author exercise)
<!-- id: pc-budget-check -->

**Prerequisites.** Reading Big-O notation for simple loops; this lesson.

**Problem.** A problem statement guarantees that the input size `n` satisfies `1 <= n <= 100_000`. A step is one basic operation, such as one comparison or one addition. Consider three plans. Plan A scans the array once. Plan B sorts the array and then scans it once. Plan C compares every unordered pair of distinct elements. For each plan, compute the number of steps at the largest legal `n`. Then return "plausible" if that number is at most the time limit, and "implausible" if it is larger. Show the step count that supports each answer.

**Constraints.** The time limit is 10^8 (100,000,000) steps. Compute every count at `n = 100_000`, not at the size of a sample input. Use `long` for every product, because `n * n` exceeds the `int` maximum. Plan A costs `n` steps. Plan B costs about `n * log2(n)` steps for the sort plus `n` steps for the scan. Plan C costs `n * (n - 1) / 2` steps. Ties go to "plausible": a count equal to the budget is plausible. The exercise has no mutable input.

**Example 1.** Input `n = 100000` with a single scan, output plausible, because the step count is about 10^5.

**Example 2.** Input `n = 100000` with all pairs, output implausible, because the count is 4,999,950,000, roughly fifty times the budget.

**Hint.** Do the estimate at the largest legal `n` and write the number out. Which two of the three plans land below 10^8, and which lands far above it?

**Changed decision.** First exercise in the sequence: replaces a feeling about speed with a computed step count at the maximum input.

#### [Vary] Small Domain (Author exercise)
<!-- id: pc-small-domain -->

**Prerequisites.** The budget check above.

**Problem.** A value-indexed table is an array in which slot `v` stores data about the value `v`. Such a table needs one slot for every value that can occur, so its size equals the size of the value range. Consider an input array `nums` of `n` integers, where `1 <= n <= 100_000` and `0 <= nums[i] <= 100`. Compute the memory in bytes of a table with one `int` counter per possible value. Then compute the memory of the same kind of table when `0 <= nums[i] <= 1_000_000_000`. State for each case whether the table is an acceptable plan, and name the limit in the statement that decides the answer.

**Constraints.** Each counter is a 4-byte `int`. The first table has exactly 101 slots, for the values `0` through `100`. The second table has exactly 1,000,000,001 slots, for the values `0` through `1_000_000_000`. The memory is `slots * 4` bytes, computed in `long`. The size `n` does not change the table size. The exercise has no mutable input and no empty input.

**Example 1.** Input values limited to `0..100`, output a 101-slot table of about 404 bytes, which is trivial.

**Example 2.** Input values limited to `0..1_000_000_000`, output a table of about 4 gigabytes, which is not an acceptable plan.

**Hint.** The size of a value-indexed table is the size of the value range, not the number of elements. Which input constraint in the statement decides the answer here, the size limit or the value limit?

**Changed decision.** The deciding input constraint changes from the input size to the value range, which decides whether a value-indexed table is affordable.

#### [Boundary] Hidden Overflow (Author exercise)
<!-- id: pc-hidden-overflow -->

**Prerequisites.** The two exercises above.

**Problem.** An input array `nums` has `n` elements, where `n = 100_000` and `-1_000_000_000 <= nums[i] <= 1_000_000_000`. The sum of the array is the total of all its elements. Decide whether the sum always fits in a Java `int`, that is, whether it always lies between -2,147,483,648 and 2,147,483,647. Return "yes" or "no". If the answer is "no", give one input array whose sum does not fit. Name the type that the accumulator variable must have.

**Constraints.** The largest `int` is 2,147,483,647. The largest `long` is 9,223,372,036,854,775,807. The worst case sets every element to the largest legal magnitude, which is 1_000_000_000. Elements are `int` values. The array has at least one element. An `int` accumulator wraps around silently on overflow and raises no error. The method does not modify `nums`.

**Example 1.** Input one hundred thousand copies of 1,000,000,000, output a sum of 100,000,000,000,000, which does not fit in an `int`.

**Example 2.** Input `[5, 7, 9]`, output a sum of 21, which fits easily, so a passing small test proves nothing about the limit.

**Hint.** Multiply the largest element by the largest count and compare the product with the `int` ceiling. Does the answer change if the values are mostly small but one adversarial test uses the maximum?

**Changed decision.** The question moves from running time to numeric range, so the input constraint now decides the accumulator type.

#### [Recognize] Query Pressure (Author exercise)
<!-- id: pc-query-pressure -->

**Prerequisites.** The budget check and the small-domain exercise.

**Problem.** An array of `n = 100_000` integers does not change. A range-sum query gives two positions `l` and `r` and asks for the sum of the elements from position `l` through position `r`. Compare two workloads on the same array: workload one has a single query, and workload two has `q = 100_000` queries. For each workload, compute the total step count of answering every query with a plain loop over the range. Return whether that plan stays within the time limit. Explain that the number of queries, not the type of the data, decides whether the plan is acceptable. Do not implement a faster plan.

**Constraints.** `n = 100_000` and `1 <= q <= 100_000`. Each query range may cover the whole array, so one query costs up to `n` steps. The time limit is 10^8 steps. Compute the total as `n * q` in `long`, because `10^10` exceeds the `int` maximum. A total equal to the time limit is within the limit. The array is never modified between queries.

**Example 1.** Input one query, output that a direct loop of at most 100,000 steps is acceptable.

**Example 2.** Input `q = 100000` queries, output that looping per query costs up to 10^10 steps in the worst case, so a smarter plan is required.

**Hint.** Multiply the cost of one query by the number of queries. At what query count does the plain loop exceed the time limit?

**Changed decision.** The deciding input constraint changes from the size of the data to the number of operations asked about it.
