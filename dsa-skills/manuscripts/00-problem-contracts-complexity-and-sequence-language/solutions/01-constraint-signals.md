<!-- solutions-for: 01-constraint-signals -->
### Constraint Signals

#### Solution: [Build] Budget Check (Author exercise)
<!-- id: pc-budget-check -->

**Approach.** At `n = 100_000` a single scan takes about 100,000 steps. A sort followed by a scan takes about `n * 17`, which is 1.7 million steps. All pairs takes `n * (n - 1) / 2`, which is 4,999,950,000 steps. Against a budget of 10^8, the first two plans are comfortably plausible. The third is about fifty times over. The code below states the budget and checks each claim, so the verdict is an assertion and not a feeling.

**Complexity.** The estimate itself is O(1). The three plans it judges run in O(n), O(n log n) and O(n^2) time respectively.

```java run
public final class BudgetCheck {
    static final long BUDGET = 100_000_000L;

    static long scan(long n) { return n; }
    static long sortThenScan(long n) { return n * (64 - Long.numberOfLeadingZeros(n - 1)) + n; }
    static long allPairs(long n) { return n * (n - 1) / 2; }

    public static void main(String[] args) {
        long n = 100_000;
        if (!(scan(n) <= BUDGET)) throw new AssertionError("scan should fit");
        if (!(sortThenScan(n) <= BUDGET)) throw new AssertionError("sort then scan should fit");
        if (allPairs(n) != 4_999_950_000L) throw new AssertionError("pair count");
        if (!(allPairs(n) > 49 * BUDGET)) throw new AssertionError("pairs should be about fifty times over budget");
        if (!(allPairs(5) == 10)) throw new AssertionError("the sample hides the problem");
    }
}
```

#### Solution: [Vary] Small Domain (Author exercise)
<!-- id: pc-small-domain -->

**Approach.** A value-indexed table has one slot per possible value, so its size equals the size of the value range and does not depend on `n`. Values in `0..100` need 101 four-byte counters, which is 404 bytes. Values in `0..1_000_000_000` need a billion and one counters, about four gigabytes. The size limit is identical in both cases. The value limit changes the decision.

**Complexity.** Building the counts takes O(n) time. The table takes O(V) space, where V is the number of distinct possible values. That means 101 slots in the first case and about 10^9 slots in the second.

```java run
public final class SmallDomain {
    static long tableBytes(long maxValue) { return (maxValue + 1) * 4L; }

    static int[] countSmall(int[] nums) {
        int[] counts = new int[101];
        for (int v : nums) counts[v]++;
        return counts;
    }

    public static void main(String[] args) {
        if (tableBytes(100) != 404) throw new AssertionError("small table size");
        if (!(tableBytes(1_000_000_000) > 3_900_000_000L)) throw new AssertionError("large table is about 4 GB");
        int[] c = countSmall(new int[] {5, 100, 5, 0});
        if (c[5] != 2 || c[100] != 1 || c[0] != 1 || c[7] != 0) throw new AssertionError("counts");
    }
}
```

#### Solution: [Boundary] Hidden Overflow (Author exercise)
<!-- id: pc-hidden-overflow -->

**Approach.** The largest possible sum is `100_000 * 1_000_000_000`, which is 10^14. The `int` ceiling is 2,147,483,647, so an `int` cannot hold the sum. The accumulator must be a `long`, which holds values up to about 9.2 * 10^18. The adversarial input is one hundred thousand copies of the largest legal value. A small sample like `[5, 7, 9]` passes either way, so you must read the limit and not rely on testing.

**Complexity.** O(n) time and O(1) extra space. Widening the accumulator costs nothing extra.

```java run
public final class HiddenOverflow {
    static int sumAsInt(int[] nums) { int s = 0; for (int v : nums) s += v; return s; }
    static long sumAsLong(int[] nums) { long s = 0; for (int v : nums) s += v; return s; }

    public static void main(String[] args) {
        int[] hostile = new int[100_000];
        java.util.Arrays.fill(hostile, 1_000_000_000);
        if (sumAsLong(hostile) != 100_000_000_000_000L) throw new AssertionError("true sum");
        if (sumAsInt(hostile) == 100_000_000_000_000L) throw new AssertionError("an int cannot hold it");
        if ((long) sumAsInt(hostile) == sumAsLong(hostile)) throw new AssertionError("int sum must be wrong here");
        int[] tiny = {5, 7, 9};
        if (sumAsInt(tiny) != 21 || sumAsLong(tiny) != 21) throw new AssertionError("tiny input hides the bug");
    }
}
```

#### Solution: [Recognize] Query Pressure (Author exercise)
<!-- id: pc-query-pressure -->

**Approach.** One range-sum query by a plain loop costs at most `n = 100_000` steps, far below the budget. One hundred thousand such queries cost up to `100_000 * 100_000 = 10^10` steps, a hundred times the budget. The array and its size stay the same. Only the operation count changes. Therefore the design must spend time up front to make each query cheap. The prefix-sum chapter provides that design. This exercise only decides that the design is needed.

**Complexity.** Looping per query is O(n) per query, so O(n * q) in total. The estimate itself is O(1).

```java run
public final class QueryPressure {
    static final long BUDGET = 100_000_000L;
    static long loopCost(long n, long queries) { return n * queries; }

    public static void main(String[] args) {
        if (!(loopCost(100_000, 1) <= BUDGET)) throw new AssertionError("one query is fine");
        if (loopCost(100_000, 100_000) != 10_000_000_000L) throw new AssertionError("total work");
        if (!(loopCost(100_000, 100_000) >= 100 * BUDGET)) throw new AssertionError("a hundred times over");
        if (!(loopCost(100_000, 1_000) <= BUDGET)) throw new AssertionError("the loop stays affordable up to 1,000 queries");
    }
}
```
