<!-- lesson-kind: standard -->
<!-- lesson-id: complexity-tradeoffs -->
## Complexity Tradeoffs

<!-- stage: context -->
### Why Two Engineers Disagree About Loops

Two engineers review the same method in a code review. The method scans a list of orders once to find the largest. It then scans the list a second time to count how many orders match that largest value. One engineer says the method has two loops, so it is quadratic and needs a rewrite. The other says it is obviously linear and fine as it is.

They are not arguing about taste, because one of them is simply wrong. To find out which, count how many times the innermost line runs. Do not count the loops on the screen. The same dispute appears whenever someone compares two solutions that spend different resources. One solution uses more memory to save time. Another changes the input to save both. To choose between them, you need a shared way to say what each one costs.

<!-- stage: naive -->
### Count The Loops

The popular shortcut reads the number of loops as the exponent. One loop is linear, two loops are quadratic, and three loops are cubic. Here are two methods that a loop-counter treats identically.

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

Both methods have two `for` keywords that touch the array. The shortcut classifies them the same way. They are not the same.

<!-- stage: bottleneck -->
### Loops Do Not Multiply Unless They Nest

Count how often the innermost statement runs. In `twoScans`, the first loop runs `n` times and the second loop runs `n` times afterward. The total is `n + n = 2n`, which is O(n). In `pairCount` the outer loop runs `n` times. The inner loop runs a shrinking number of times: `n - 1`, then `n - 2`, down to 0. The total is `n * (n - 1) / 2`, which is O(n^2).

A wrong classification costs real effort in both directions. If someone calls `twoScans` quadratic, a team rewrites correct, fast code and risks introducing a bug. If someone calls `pairCount` linear, a team accepts a method that needs five billion steps at `n = 100,000`. A rule that cannot tell them apart is worse than no rule, because it produces confident wrong answers. The correct tool is to count executions of the dominant statement.

<!-- stage: insight -->
### Add, Multiply, Keep The Largest

#### Add And Multiply Loop Costs

Loops that run one after another add their costs. A loop nested inside another multiplies the cost of its body by the number of times the outer loop reaches it. After counting, the final bound keeps only the part that grows fastest.

#### Keep The Dominant Term

That fastest-growing part is the **dominant term**. In `2n + 5` it is `2n`. The bound drops the constant factor because it does not change how the cost scales, so the bound is O(n). In `n^2 / 2 - n / 2` the dominant term is `n^2 / 2`, so the bound is O(n^2). The smaller terms matter for tiny inputs and stop mattering as the input grows.

<!-- names: dominant term, worst legal input, tradeoff -->

#### Name The Worst Legal Input

A bound is meaningful only for a named input. The bound describes the dominant work on the **worst legal input**: the input of the largest allowed size and the most unfavorable shape. A method that stops early on some inputs still needs a judgment on the input where it does not stop early.

#### Compare Costs As A Tradeoff

A **tradeoff** exists when two correct solutions spend different resources. The resources include time, extra memory, a preprocessing step, or permission to change the input. To compare the solutions, write each cost in the same units and state what each solution gives up. Sorting first costs O(n log n) and may reorder or copy the data. In return, it can replace an all-pairs search with a single pass. The honest comparison is that you pay a modest cost to avoid a large one, and you give up the original order.

<!-- stage: variables -->
### What Is Being Counted

Name three things before you compute a bound. The first is the size variable `n`, plus any second dimension such as `rows` and `cols`. Never merge two dimensions silently into one letter. The second is the exact operation you count, such as comparisons, array reads or element copies. The third is the shape of the loops. The loops are sequential, nested with a fixed inner bound, or nested with an inner bound that shrinks or depends on the outer index.

<!-- stage: trace -->
### Counting A Shrinking Inner Loop

Take `pairCount` with `n = 4`. When `i` is 0, `j` runs 1, 2 and 3, so the statement executes three times. When `i` is 1, `j` runs 2 and 3, which adds two executions. When `i` is 2, `j` runs only 3, which adds one. When `i` is 3, the inner loop has nothing left to run.

The total is 3 + 2 + 1 + 0, which is 6. The formula `n * (n - 1) / 2` gives 4 * 3 / 2, which is 6 as well. The hardest step to see is the last one, where an outer iteration contributes nothing. That step is why the answer is half of `n * n`. It also shows why a shrinking inner loop does not make the method linear, because the pieces still add up to a quantity proportional to `n^2`. Doubling `n` to 8 gives 28 executions, nearly four times as many.

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

Each counter mirrors the loop structure of the method it models, and `steps++` stands for the dominant statement. The first returns `2n`, the second `n * (n - 1) / 2` and the third `rows * cols`. The counters use `long` because the triangular count for `n = 100,000` already exceeds what an `int` can hold. Their own running time equals the count they return. For that reason, use them only on small inputs to check a formula before you trust it.

<!-- stage: applicability -->
### Stating A Bound Honestly

#### State The Bound And Its Input

Count executions of the dominant statement whenever you claim a time or space bound, and say which input the bound describes. The invariant is that the stated bound describes the dominant work on the worst legal input, in units that the problem's variables can express. If the problem has two size variables, the bound uses both.

#### Beware The Loop-Counting Shortcut

The false friend is the loop-counting shortcut. Two loops side by side add, and two loops nested over the same growing input usually multiply. The word usually matters. A nested loop whose inner index only moves forward across the whole run can still total O(n). Later chapters on two pointers and sliding windows depend on exactly that argument. So count executions, because nesting depth alone does not decide the bound.

#### Include Hidden Java Costs

Java adds hidden costs that loop counting misses. A library call inside a loop, such as `list.remove(0)` or string concatenation, may itself cost O(n) per call. Lesson 8 of this chapter lists those calls. Any bound you state must include them.

<!-- stage: exercises -->
### Exercises

#### [Build] Consecutive Loops (Author exercise)
<!-- id: pc-consecutive-loops -->

**Prerequisites.** Counting loop executions as in this lesson.

**Problem.** A program runs two loops one after the other. Each loop executes its body exactly once for every index from `0` to `n - 1`. A loop-body execution is one pass through the body of a loop. Return the total number of loop-body executions for a given `n`. Then classify that count with big-O notation, and explain why the two loops add their costs and do not multiply them.

**Constraints.** `n` is an `int` with `1 <= n <= 10^5`. The first loop finishes before the second loop starts, and neither loop is nested inside the other. The return value is a `long`. Each loop body costs one unit, and no other work is counted. The count is deterministic and does not depend on the array contents. The program does not modify any input.

**Example 1.** Input `n = 10`, output 20 loop-body executions, which is O(n).

**Example 2.** Input `n = 1`, output 2 executions, so a constant factor of two persists even on the smallest input.

**Hint.** Do the executions of the second loop depend on how many times the first loop ran? What does a constant factor do to growth as `n` doubles?

**Changed decision.** First rung: separates adding sequential work from multiplying nested work.

#### [Vary] Triangular Work (Author exercise)
<!-- id: pc-triangular-work -->

**Prerequisites.** The consecutive-loops exercise above.

**Problem.** Consider the loop pair `for (i = 0; i < n; i++) for (j = i + 1; j < n; j++)`. Return the number of times the inner loop body executes, for a given `n`. Derive a closed formula for that count, and classify the count with big-O notation. The expected formula is `n(n-1)/2`, and the expected class is O(n^2).

**Constraints.** `n` is an `int` with `0 <= n <= 10^5`. When `n = 0`, neither loop runs and the count is 0. The inner loop starts at `i + 1`, so it runs `n - 1 - i` times for each `i`, and it shrinks as `i` grows. The return value is a `long`, because the count reaches about `5 * 10^9` and overflows `int`. Only inner-loop-body executions are counted.

**Example 1.** Input `n = 5`, output 10 iterations.

**Example 2.** Input `n = 1`, output 0 iterations, because the inner loop never runs.

**Hint.** Add up how many inner iterations happen for `i = 0`, then for `i = 1`, and so on. What does `1 + 2 + ... + (n-1)` equal?

**Changed decision.** The inner bound now depends on the outer index, so the total is a sum and not a simple product.

#### [Boundary] Two Dimensions (Author exercise)
<!-- id: pc-two-dimensions -->

**Prerequisites.** The two exercises above.

**Problem.** A grid has `rows` rows and `cols` columns, so it has `rows * cols` cells. A traversal visits every cell exactly once. Return the number of cell visits. State the traversal time as `O(rows * cols)`, which keeps both dimensions. Then give one input where replacing both dimensions by a single `n` and claiming O(n^2) overstates the cost by a large factor.

**Constraints.** `rows` and `cols` are `int` values with `1 <= rows, cols <= 10^5` and `rows * cols <= 10^6`. The two dimensions are independent, so neither is assumed to be the larger one. Each cell is visited exactly once, and no cell is skipped. The return value is a `long`. One visit costs one unit. The traversal does not modify the grid.

**Example 1.** Input `rows = 3, cols = 4`, output 12 visits.

**Example 2.** Input `rows = 1000, cols = 2`, output 2,000 visits, whereas treating the larger dimension as `n` and claiming O(n^2) would suggest 1,000,000.

**Hint.** If one dimension is tiny, what does the product look like? What would you write for a grid that is a single row?

**Changed decision.** A second size variable appears, and the bound must keep both instead of merging them.

#### [Recognize] Sort Then Scan (Author exercise)
<!-- id: pc-sort-then-scan -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `nums`, return `true` if some value appears at positions `i` and `j` with `i != j`, and return `false` if all values are distinct. Compare two methods. The all-pairs method compares every pair of positions and takes O(n^2) time. The sort-then-scan method sorts the values and then compares each element with its predecessor in one O(n) pass, so it takes O(n log n) time. State the tradeoff in full: the lower time, the changed order, and the copy or in-place mutation that decides what happens to the original array.

**Constraints.** `nums` is an `int[]` with `1 <= n <= 10^5` elements, where `n = nums.length`. Values may repeat, and every `int` value is allowed. Sorting a copy costs O(n) extra space and leaves `nums` unchanged. Sorting `nums` in place uses O(1) extra space beyond the sort itself, but it destroys the original order. The all-pairs method uses O(1) extra space and does not modify `nums`.

**Example 1.** Input `[4,1,3,1]`, output true, because the sorted copy `[1,1,3,4]` has equal neighbors.

**Example 2.** Input `[4,1,3,2]`, output false, since the sorted neighbors are all different.

**Hint.** After sorting, where must two equal values be? What do you give up by sorting, and how could you avoid giving up the original order?

**Changed decision.** The algorithm swaps one resource for another: it spends time on ordering to remove an entire nested loop, and it pays with a changed or copied array.
