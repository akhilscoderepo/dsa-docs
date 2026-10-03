<!-- lesson-kind: standard -->
<!-- lesson-id: complexity-tradeoffs -->
## Complexity Tradeoffs

<!-- stage: context -->
### Two Engineers, One Loop Count

Two engineers review the same method during a code review. The method scans a list of orders once to find the largest, then scans it a second time to count how many orders match that largest value. One engineer says it has two loops, so it must be quadratic and should be rewritten. The other says it is obviously linear and fine as it is.

They are not arguing about taste, because one of them is simply wrong, and the way to tell is to count how many times the innermost line runs instead of counting the loops on the screen. The same dispute appears whenever someone compares two solutions that spend different resources, one using more memory to save time, another changing the input to save both. Choosing between them requires a shared way to say what each one costs.

<!-- stage: naive -->
### Count The Loops

The popular shortcut is to read the number of loops as the exponent. One loop is linear, two loops are quadratic, three loops are cubic. Here are two methods that a loop-counter would treat identically.

```java
static int twoScans(int[] orders) {
    int max = orders[0];
    for (int v : orders) max = Math.max(max, v);
    int count = 0;
    for (int v : orders) if (v == max) count++;
    return count;
}

static int pairCount(int[] orders) {
    int pairs = 0;
    for (int i = 0; i < orders.length; i++)
        for (int j = i + 1; j < orders.length; j++) pairs++;
    return pairs;
}
```

Both have two `for` keywords that touch the array. By the shortcut they would be classified the same way. They are not the same.

<!-- stage: bottleneck -->
### Loops Do Not Multiply Unless They Nest

Count how often the innermost statement runs. In `twoScans`, the first loop runs `n` times and the second loop runs `n` times afterward, so the total is `n + n = 2n`, which is O(n). In `pairCount` the outer loop runs `n` times and the inner loop runs a shrinking number of times, `n - 1`, then `n - 2`, down to 0. The total is `n * (n - 1) / 2`, which is O(n^2).

The cost of the wrong classification is real in both directions. Calling `twoScans` quadratic leads someone to rewrite correct, fast code and risk introducing a bug. Calling `pairCount` linear leads someone to accept a method that needs five billion steps at `n = 100,000`. A rule that cannot distinguish them is worse than no rule, because it produces confident wrong answers. The correct tool is to count executions of the dominant statement.

<!-- stage: insight -->
### Add, Multiply, Keep The Largest

Loops that run one after another add their costs. Loops placed inside one another multiply the cost of the inner body by the number of times it is reached. After counting, the final bound keeps only the part that grows fastest.

That fastest-growing part is the **dominant term**. In `2n + 5` it is `2n`, and a constant factor is dropped because it does not change how the cost scales, so the bound is O(n). In `n^2 / 2 - n / 2` the dominant term is `n^2 / 2`, so the bound is O(n^2). The smaller terms matter for tiny inputs and stop mattering as the input grows.

<!-- names: dominant term, worst legal input, tradeoff -->

A bound is meaningful only for a named input. The bound should describe the dominant work on the **worst legal input**, the input of the largest allowed size and the most unfavorable shape. A method that stops early on some inputs still has to be judged on the one where it does not.

A **tradeoff** exists when two correct solutions spend different resources: time, extra memory, a preprocessing step, or permission to change the input. Comparing them means writing each one's cost in the same units and stating what each one gives up. Sorting first costs O(n log n) and may reorder or copy the data, and it can replace an all-pairs search with a single pass. The honest comparison is that you pay a modest cost to buy a large one, and that you give up the original order.

<!-- stage: variables -->
### What Is Being Counted

Name three things before computing a bound. The first is the size variable, `n`, and any second dimension such as `rows` and `cols`, which must not be silently merged into one letter. The second is the exact operation you are counting, such as comparisons, array reads or element copies. The third is the shape of the loops, whether they are sequential, nested with a fixed inner bound, or nested with an inner bound that shrinks or depends on the outer index.

<!-- stage: trace -->
### Counting A Shrinking Inner Loop

Take `pairCount` with `n = 4`. The outer index `i` is 0 and the inner index `j` runs 1, 2 and 3, so the statement executes three times. With `i` equal to 1 the inner index runs 2 and 3, which adds two executions, and with `i` equal to 2 it runs only 3, which adds one. With `i` equal to 3 the inner loop has nothing left to run.

The total is 3 + 2 + 1 + 0, which is 6, and the formula `n * (n - 1) / 2` gives 4 * 3 / 2, which is 6 as well. The hardest step to see is the last one, where an iteration of the outer loop contributes nothing. It is the reason the answer is half of `n * n`, and it also shows why a shrinking inner loop does not make the method linear, because the pieces still add up to a quantity proportional to `n^2`. Doubling `n` to 8 would give 28 executions, nearly four times as many.

```trace
{"cells":[0,1,2,3],"pointers":["i","j"],"steps":[{"at":{"i":0,"j":1},"vars":{"executions":1},"note":"i = 0, j = 1: the inner statement runs for the 1st time."},{"at":{"i":0,"j":2},"vars":{"executions":2},"note":"i = 0, j = 2: the inner statement runs for the 2nd time."},{"at":{"i":0,"j":3},"vars":{"executions":3},"note":"i = 0, j = 3: the inner statement runs for the 3rd time."},{"at":{"i":1,"j":2},"vars":{"executions":4},"note":"i = 1, j = 2: the inner statement runs for the 4th time."},{"at":{"i":1,"j":3},"vars":{"executions":5},"note":"i = 1, j = 3: the inner statement runs for the 5th time."},{"at":{"i":2,"j":3},"vars":{"executions":6},"note":"i = 2, j = 3: the inner statement runs for the 6th time."},{"at":{"i":3,"j":4},"vars":{"executions":6},"note":"i = 3: the inner loop starts at 4 and has nothing to run, so this outer pass adds 0."},{"at":{"i":4,"j":4},"vars":{"executions":6,"formula":6},"note":"Done. 3 + 2 + 1 + 0 = 6, and n(n-1)/2 = 4*3/2 = 6."}]}
```

<!-- stage: code -->
### Counting Executions Directly

```java
static long countTwoScans(int n) {
    long steps = 0;
    for (int i = 0; i < n; i++) steps++;      // first scan
    for (int i = 0; i < n; i++) steps++;      // second scan
    return steps;
}

static long countTriangular(int n) {
    long steps = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) steps++;
    return steps;
}

static long countGrid(int rows, int cols) {
    long steps = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) steps++;
    return steps;
}
```

Each counter mirrors the loop structure of the method it models, and `steps++` stands for the dominant statement. The first returns `2n`, the second `n * (n - 1) / 2` and the third `rows * cols`. The counters are written with `long` because the triangular count for `n = 100,000` already exceeds what an `int` can hold. Their own running time equals the count they return, which is why they are only used on small inputs to check a formula before trusting it.

<!-- stage: applicability -->
### Stating A Bound Honestly

Count executions of the dominant statement whenever you claim a time or space bound, and say which input the bound describes. The invariant is that the stated bound describes the dominant work on the worst legal input, in units that the problem's variables can express. If there are two size variables, the bound uses both.

The false friend is the loop-counting shortcut. Two loops side by side add, and two loops nested over the same growing input usually multiply. The word usually matters, because a nested loop whose inner index only moves forward across the whole run can still total O(n), and later chapters on two pointers and sliding windows depend on exactly that argument. So the rule is to count executions, and the nesting depth alone does not decide it.

Java adds hidden costs that loop counting misses. A library call inside a loop, such as `list.remove(0)` or string concatenation, may itself cost O(n) per call. Lesson 8 of this chapter lists those, and any bound you state must include them.

<!-- stage: exercises -->
### Exercises

#### [Build] Consecutive Loops (Author exercise)
<!-- id: pc-consecutive-loops -->

**Prerequisites.** Counting loop executions as in this lesson.

**Problem.** Determine the time cost of scanning an `n`-element array twice in a row. Explain why `O(n) + O(n)` simplifies to `O(n)` and why the two scans do not multiply.

**Constraints.** `1 <= n <= 10^5`. The two scans are sequential, and neither is nested inside the other.

**Example 1.** Input `n = 10`, output 20 loop-body executions, which is O(n).

**Example 2.** Input `n = 1`, output 2 executions, so a constant factor of two persists even on the smallest input.

**Hint.** Do the executions of the second loop depend on how many times the first loop ran? What does a constant factor do to growth as `n` doubles?

**Changed decision.** First rung: separates adding sequential work from multiplying nested work.

#### [Vary] Triangular Work (Author exercise)
<!-- id: pc-triangular-work -->

**Prerequisites.** The consecutive-loops exercise above.

**Problem.** Count the iterations of `for (i = 0; i < n; i++) for (j = i + 1; j < n; j++)`. Derive the formula `n(n-1)/2` and classify the loop pair as O(n^2).

**Constraints.** `0 <= n <= 10^5`. The inner loop starts at `i + 1`, so it shrinks as `i` grows.

**Example 1.** Input `n = 5`, output 10 iterations.

**Example 2.** Input `n = 1`, output 0 iterations, because the inner loop never runs.

**Hint.** Add up how many inner iterations happen for `i = 0`, then for `i = 1`, and so on. What does `1 + 2 + ... + (n-1)` equal?

**Changed decision.** The inner bound now depends on the outer index, so the total is a sum and not a simple product.

#### [Boundary] Two Dimensions (Author exercise)
<!-- id: pc-two-dimensions -->

**Prerequisites.** The two exercises above.

**Problem.** A grid has `rows` and `cols`. State the traversal time as `O(rows * cols)` rather than silently calling both dimensions `n`, and show one input where calling it O(n^2) overstates the cost badly.

**Constraints.** `1 <= rows, cols <= 10^5`, with `rows * cols <= 10^6`. Visit every cell exactly once.

**Example 1.** Input `rows = 3, cols = 4`, output 12 visits.

**Example 2.** Input `rows = 1000, cols = 2`, output 2,000 visits, whereas treating the larger dimension as `n` and claiming O(n^2) would suggest 1,000,000.

**Hint.** If one dimension is tiny, what does the product look like? What would you write for a grid that is a single row?

**Changed decision.** A second size variable appears, and the bound must keep both instead of merging them.

#### [Recognize] Sort Then Scan (Author exercise)
<!-- id: pc-sort-then-scan -->

**Prerequisites.** All three exercises above.

**Problem.** To detect whether an array contains a duplicate, compare O(n^2) all-pairs work with O(n log n) sorting followed by one O(n) scan of neighbors. State the tradeoff in full: the lower time, the changed order, and the copy or mutation needed to keep the original intact.

**Constraints.** `1 <= n <= 10^5`. Sorting a copy costs O(n) extra space, while sorting in place destroys the original order.

**Example 1.** Input `[4,1,3,1]`, output true, because the sorted copy `[1,1,3,4]` has equal neighbors.

**Example 2.** Input `[4,1,3,2]`, output false, since the sorted neighbors are all different.

**Hint.** After sorting, where must two equal values be? What do you give up by sorting, and how could you avoid giving up the original order?

**Changed decision.** The algorithm swaps one resource for another: it spends time on ordering to remove an entire nested loop, and it pays with a changed or copied array.
