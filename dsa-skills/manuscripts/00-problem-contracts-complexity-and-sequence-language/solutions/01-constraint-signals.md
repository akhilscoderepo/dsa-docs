<!-- solutions-for: 01-constraint-signals -->
### Solutions For The Input Limit Exercises

#### Solution: [Build] Budget Check (Author exercise)
<!-- id: pc-budget-check -->

**Approach.**

- **Maximum input** is `n = 100_000`, with a time limit of 10^8 steps.
- **Single scan** takes about 100,000 steps.
- **Sort then scan** takes about `n * 17`, which is 1.7 million steps, because `log2(100_000)` rounds up to 17.
- **All pairs** takes `n * (n - 1) / 2`, which is 4,999,950,000 steps.
- **Verdict for the first two plans** is "plausible", because they stay far below the limit.
- **Verdict for all pairs** is "implausible", because it is about fifty times over the limit.
- **long** holds every count, because the pair count exceeds the `int` maximum.
- **Assertions** in the code state each claim, so the verdict is a checked fact.

**Complexity.**

- **Time** is O(1), because the estimate evaluates three closed-form expressions and runs no loop. The plans it judges run in O(n), O(n log n) and O(n^2) time.
- **Space** is O(1), because the estimate stores a few `long` values.

```java run
public final class BudgetCheck {
    // Budget of simple steps that fits an ordinary interview time limit.
    static final long BUDGET = 100_000_000L;

    /**
     * Step count of one scan. Time: O(1), a closed-form expression. Space: O(1), no storage.
     */
    static long scan(long n) { return n; }

    /**
     * Step count of a sort plus one scan: n * ceil(log2 n) comparisons, then n reads.
     * Time: O(1), a closed-form expression. Space: O(1), no storage.
     */
    static long sortThenScan(long n) { return n * (64 - Long.numberOfLeadingZeros(n - 1)) + n; }

    /**
     * Step count of comparing every pair: n * (n - 1) / 2.
     * Time: O(1), a closed-form expression. Space: O(1), no storage.
     * The product needs long, because n * n overflows int at n = 100_000.
     */
    static long allPairs(long n) { return n * (n - 1) / 2; }

    public static void main(String[] args) {
        // Evaluate at the maximum legal n, because the sample size hides the cost.
        long n = 100_000;
        // The single scan and the sort-plus-scan stay within the budget.
        if (!(scan(n) <= BUDGET)) throw new AssertionError("scan should fit");
        if (!(sortThenScan(n) <= BUDGET)) throw new AssertionError("sort then scan should fit");
        // The pair count is exact and lands about fifty times above the budget.
        if (allPairs(n) != 4_999_950_000L) throw new AssertionError("pair count");
        if (!(allPairs(n) > 49 * BUDGET)) throw new AssertionError("pairs should be about fifty times over budget");
        // A tiny input makes the quadratic plan look harmless.
        if (!(allPairs(5) == 10)) throw new AssertionError("the sample hides the problem");
    }
}
```

#### Solution: [Vary] Small Domain (Author exercise)
<!-- id: pc-small-domain -->

**Approach.**

- **Value-indexed table** has one slot per possible value, so its size equals the value range and does not depend on `n`.
- **Memory** is the slot count times 4 bytes.
- **Values in 0..100** need 101 counters, which is 404 bytes.
- **Values in 0..1_000_000_000** need 1,000,000,001 counters, about four gigabytes.
- **Size limit** `n <= 100_000` is identical in both cases.
- **Value limit** is the input constraint that changes the decision.
- **Counting loop** increments `counts[v]` for each element `v`, in one pass.

**Complexity.**

- **Time** is O(n), because the counting loop reads each element once and does O(1) work for it.
- **Space** is O(V), where V is the number of possible values, because the table has one slot per value. That means 101 slots in the first case and about 10^9 slots in the second.

```java run
public final class SmallDomain {
    /**
     * Memory of a value-indexed table of 4-byte counters for values 0..maxValue.
     * Time: O(1), one multiplication. Space: O(1), no allocation.
     * The table has maxValue + 1 slots, so memory depends on the value range, not on n.
     */
    static long tableBytes(long maxValue) { return (maxValue + 1) * 4L; }

    /**
     * Counts how often each value 0..100 occurs in nums.
     * Time: O(n), because the loop visits each element once. Space: O(V) with V = 101,
     * because the counter table has one slot per possible value.
     * Precondition: 0 <= nums[i] <= 100, so every index is in bounds.
     */
    static int[] countSmall(int[] nums) {
        // One slot per possible value; this table is the only extra memory.
        int[] counts = new int[101];
        // Visit each element once; the value itself is the index, so no search is needed.
        for (int v : nums) counts[v]++;
        // Return the table; the counts are the answer.
        return counts;
    }

    public static void main(String[] args) {
        // The table size follows the value range: 404 bytes versus about 4 GB.
        if (tableBytes(100) != 404) throw new AssertionError("small table size");
        if (!(tableBytes(1_000_000_000) > 3_900_000_000L)) throw new AssertionError("large table is about 4 GB");
        // The small table counts a mixed sample correctly, including the boundary values 0 and 100.
        int[] c = countSmall(new int[] {5, 100, 5, 0});
        if (c[5] != 2 || c[100] != 1 || c[0] != 1 || c[7] != 0) throw new AssertionError("counts");
    }
}
```

#### Solution: [Boundary] Hidden Overflow (Author exercise)
<!-- id: pc-hidden-overflow -->

**Approach.**

- **Largest sum** is `100_000 * 1_000_000_000`, which is 10^14.
- **int ceiling** is 2,147,483,647, far below that bound, so an `int` cannot always hold the sum and the answer is "no".
- **Accumulator** must be a `long`, which holds values up to about 9.2 * 10^18.
- **Adversarial input** is one hundred thousand copies of the largest legal value.
- **Small sample** such as `[5, 7, 9]` passes with either type, so small tests cannot replace reading the limit.
- **int accumulator** wraps around silently, so the program gives a wrong answer and no error.

**Complexity.**

- **Time** is O(n), because the loop adds each element once.
- **Space** is O(1), because the method keeps one accumulator. Widening the accumulator from `int` to `long` adds no asymptotic cost.

```java run
public final class HiddenOverflow {
    /**
     * Sums nums in an int accumulator. This version overflows on the adversarial input.
     * Time: O(n), one addition per element. Space: O(1), one accumulator.
     */
    static int sumAsInt(int[] nums) { int s = 0; for (int v : nums) s += v; return s; }

    /**
     * Sums nums in a long accumulator, which cannot overflow for n <= 100_000 and |v| <= 10^9.
     * Time: O(n), one addition per element. Space: O(1), one accumulator.
     */
    static long sumAsLong(int[] nums) { long s = 0; for (int v : nums) s += v; return s; }

    public static void main(String[] args) {
        // Build the adversarial input: every element has the maximum legal value.
        int[] hostile = new int[100_000];
        java.util.Arrays.fill(hostile, 1_000_000_000);
        // The long sum equals the true total of 10^14.
        if (sumAsLong(hostile) != 100_000_000_000_000L) throw new AssertionError("true sum");
        // The int sum cannot match the true total, because 10^14 exceeds the int range.
        if (sumAsInt(hostile) == 100_000_000_000_000L) throw new AssertionError("an int cannot hold it");
        if ((long) sumAsInt(hostile) == sumAsLong(hostile)) throw new AssertionError("int sum must be wrong here");
        // A tiny input gives the same result with both types, so it hides the bug.
        int[] tiny = {5, 7, 9};
        if (sumAsInt(tiny) != 21 || sumAsLong(tiny) != 21) throw new AssertionError("tiny input hides the bug");
    }
}
```

#### Solution: [Recognize] Query Pressure (Author exercise)
<!-- id: pc-query-pressure -->

**Approach.**

- **One query** reads at most `n = 100_000` elements, far below the time limit of 10^8.
- **q queries** cost up to `100_000 * 100_000 = 10^10` steps, a hundred times the limit.
- **Array size** stays the same across both workloads, and only the operation count changes.
- **Design** must therefore spend time up front to make each query cheap.
- **Prefix-sum chapter** provides that design, and this exercise only decides that it is needed.
- **Break-even point** is 1,000 queries, because `100_000 * 1_000` equals the limit.

**Complexity.**

- **Time** is O(n * q) for the plain-loop plan, because each of the q queries scans up to n elements. The estimate itself takes O(1) time, because it multiplies two numbers.
- **Space** is O(1), because the plan stores no extra structure and the estimate stores one `long`.

```java run
public final class QueryPressure {
    // Budget of simple steps that fits an ordinary interview time limit.
    static final long BUDGET = 100_000_000L;

    /**
     * Worst-case step count of answering every query with a plain loop over the whole array.
     * Time: O(1), one multiplication. Space: O(1), no storage.
     * Each query costs up to n steps, so q queries cost n * q; long avoids int overflow.
     */
    static long loopCost(long n, long queries) { return n * queries; }

    public static void main(String[] args) {
        // One query costs at most n steps, which fits the budget.
        if (!(loopCost(100_000, 1) <= BUDGET)) throw new AssertionError("one query is fine");
        // With 100,000 queries the total is 10^10, a hundred times the budget.
        if (loopCost(100_000, 100_000) != 10_000_000_000L) throw new AssertionError("total work");
        if (!(loopCost(100_000, 100_000) >= 100 * BUDGET)) throw new AssertionError("a hundred times over");
        // The break-even point: 1,000 queries still fit, so the query count decides.
        if (!(loopCost(100_000, 1_000) <= BUDGET)) throw new AssertionError("the loop stays affordable up to 1,000 queries");
    }
}
```
