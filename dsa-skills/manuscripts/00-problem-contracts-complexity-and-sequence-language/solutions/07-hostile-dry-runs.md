<!-- solutions-for: 07-hostile-dry-runs -->
### Solutions For Edge-Case Tests

#### Solution: [Build] Singleton (Author exercise)
<!-- id: pc-singleton -->

**Approach.**

- **Loop header** `for (i = 1; i < 1; ...)` tests `1 < 1`, which is false, so the body never runs.
- **Result** comes entirely from the initialization, because no iteration can repair it.
- **Corrected method** starts `best` at 1, because any non-empty array holds a run of length one, so it returns 1.
- **Flawed method** starts `best` at 0 and raises it only inside the loop, so it returns 0.
- **Invariant** is that `best` holds the longest run seen so far, and an empty prefix must not count as a run of length one.
- **Dry-run table** has a single row, the initial one, and that row already shows the wrong value of `best`.

**Complexity.**

- **Time** is O(n), because the loop visits each index from 1 to `n - 1` once, and it runs zero times when `n = 1`.
- **Space** is O(1), because the method keeps only `best` and `cur`.

```java run
public final class Singleton {
    /**
     * Returns the length of the longest strictly increasing run in {@code a}.
     * Time: O(n), one pass over the array. Space: O(1), two counters.
     * Invariant: after step i, cur is the run length ending at i and best is the maximum so far.
     */
    static int fixed(int[] a) {
        // The empty array has no run, so the specification returns 0 before any indexing.
        if (a.length == 0) return 0;
        // Start at 1, because any non-empty array already holds a run of length one.
        int best = 1, cur = 1;
        // Loop from index 1 because each step compares a[i] with its left neighbor; n - 1 steps.
        // The ternary extends the run on a strict rise and restarts it at 1 otherwise.
        // The max keeps the longest run seen, so best never decreases.
        for (int i = 1; i < a.length; i++) { cur = a[i] > a[i - 1] ? cur + 1 : 1; best = Math.max(best, cur); }
        // Return the maximum; for one element the loop never ran, so this is the initial 1.
        return best;
    }
    /**
     * Flawed variant: best starts at 0 and changes only when a run ends inside the loop.
     * Time: O(n), one pass. Space: O(1), two counters.
     * Bug: the final run is never folded into best, and a one-element array runs no iteration.
     */
    static int flawed(int[] a) {
        // The initialization is the defect: 0 is below the true answer for non-empty input.
        int best = 0, cur = 1;
        // Same loop bounds as the fixed version, so the same O(n) cost.
        for (int i = 1; i < a.length; i++) {
            // A strict rise extends the current run without touching best.
            if (a[i] > a[i - 1]) cur++; else { best = Math.max(best, cur); cur = 1; }
        }
        // Returns best, which misses a run that is still open when the loop ends.
        return best;
    }
    // Counts how many times a loop from index 1 to length - 1 runs. Time: O(length). Space: O(1).
    static int iterations(int length) { int n = 0; for (int i = 1; i < length; i++) n++; return n; }

    public static void main(String[] args) {
        // A one-element array gives zero loop iterations.
        if (iterations(1) != 0) throw new AssertionError("no iterations for one element");
        // The corrected method returns 1 for [7].
        if (fixed(new int[] {7}) != 1) throw new AssertionError("fixed result");
        // The flawed method returns 0 for [7], which exposes the initialization bug.
        if (flawed(new int[] {7}) != 0) throw new AssertionError("flawed result is the initialization bug");
        // The empty array returns 0 by the specification.
        if (fixed(new int[] {}) != 0) throw new AssertionError("empty contract");
    }
}
```

#### Solution: [Vary] All Equal (Author exercise)
<!-- id: pc-all-equal -->

**Approach.**

- **Strict comparison** `a[i] > a[i - 1]` fails on two equal neighbors, so `cur` resets to 1 at both steps and `best` stays 1.
- **Non-strict comparison** `a[i] >= a[i - 1]` passes on equal neighbors, so `cur` grows to 2 and then 3, and `best` becomes 3.
- **Values** never differ between the two runs, so the comparison operator alone changes the answer.
- **Invariant** is that `cur` is the length of the run that ends at index `i` under the chosen comparison.
- **Distinct values** cannot separate the two versions, because they contain no equal neighbors.

**Complexity.**

- **Time** is O(n), because each version makes one pass and does constant work per index.
- **Space** is O(1), because each version stores only `best` and `cur`.

```java run
public final class AllEqual {
    /**
     * Returns the longest run in {@code a} under a strict or non-strict comparison.
     * Time: O(n), one pass. Space: O(1), two counters and one flag.
     * Invariant: cur is the length of the run ending at i; best is the maximum so far.
     */
    static int run(int[] a, boolean strict) {
        // The empty array has no run, so return 0 before any indexing.
        if (a.length == 0) return 0;
        // A non-empty array holds at least one run of length one.
        int best = 1, cur = 1;
        // Compare each element with its left neighbor, so n - 1 iterations, constant work each.
        for (int i = 1; i < a.length; i++) {
            // The flag selects the comparison; equal neighbors extend only the non-strict run.
            boolean extends_ = strict ? a[i] > a[i - 1] : a[i] >= a[i - 1];
            // Extend the run on success; otherwise restart at length one.
            cur = extends_ ? cur + 1 : 1;
            // Record the longest run seen so far.
            best = Math.max(best, cur);
        }
        // The answer is the maximum run length.
        return best;
    }

    public static void main(String[] args) {
        int[] equal = {4, 4, 4};
        // Strict comparison: equal neighbors never extend a run, so the answer is 1.
        if (run(equal, true) != 1) throw new AssertionError("strict");
        // Non-strict comparison: equal neighbors extend the run to the full length 3.
        if (run(equal, false) != 3) throw new AssertionError("non-strict");
        int[] distinct = {1, 2, 3};
        // Distinct increasing values give the same answer for both comparisons, so they cannot separate them.
        if (run(distinct, true) != run(distinct, false)) throw new AssertionError("distinct values do not separate the two comparisons");
    }
}
```

#### Solution: [Boundary] Numeric Extremes (Author exercise)
<!-- id: pc-numeric-extremes -->

**Approach.**

- **True sum** is 2 * 2,147,483,647 = 4,294,967,294, which exceeds the `int` maximum of 2,147,483,647.
- **Two's-complement wrap-around** keeps the sum modulo 2^32 in a 32-bit `int`, so the stored value is 4,294,967,294 - 2^32, which is -2.
- **Prediction** of -2 is made before the code runs, and the run confirms it.
- **Long accumulator** holds 4,294,967,294 exactly, and each `int` element widens to `long` before the addition.
- **Test input** sits at the extreme value of the type, where wrap-around is guaranteed.

**Complexity.**

- **Time** is O(n), because each method adds every element once.
- **Space** is O(1), because each method keeps one accumulator.

```java run
public final class NumericExtremes {
    /**
     * Sums the array in an int accumulator, which wraps around on overflow.
     * Time: O(n), one pass. Space: O(1), one accumulator.
     */
    static int sumInt(int[] a) { int s = 0; for (int v : a) s += v; return s; }
    /**
     * Sums the array in a long accumulator, which holds the exact sum for this input.
     * Time: O(n), one pass. Space: O(1), one accumulator.
     * Invariant: s equals the exact sum of the elements read so far.
     */
    static long sumLong(int[] a) { long s = 0; for (int v : a) s += v; return s; }

    public static void main(String[] args) {
        int[] hostile = {Integer.MAX_VALUE, Integer.MAX_VALUE};
        // The int sum wraps around to -2.
        if (sumInt(hostile) != -2) throw new AssertionError("wrap-around gives -2");
        // The long sum is exact.
        if (sumLong(hostile) != 4_294_967_294L) throw new AssertionError("the long sum");
        // A related extreme: the absolute value of Integer.MIN_VALUE stays negative.
        if (Math.abs(Integer.MIN_VALUE) >= 0) throw new AssertionError("abs of MIN_VALUE stays negative");
    }
}
```

#### Solution: [Recognize] Mutation Order (Author exercise)
<!-- id: pc-mutation-order -->

**Approach.**

- **Left-to-right step** `a[1] = a[0]` overwrites the old `a[1]`, which holds 2, before the loop reads it.
- **First bad write** is that step, because it overwrites unread data.
- **Next steps** `a[2] = a[1]` and `a[3] = a[2]` copy the value just written, so `a[2]` receives 1 instead of 2, and `a[3]` receives 1 again. Every slot ends up holding the first value.
- **Right-to-left steps** `a[3] = a[2]`, `a[2] = a[1]` and `a[1] = a[0]` each write a slot whose old value the loop has already moved.
- **Invariant** is that every slot to the left of the write position is still unread and unchanged.
- **Insert** writes 9 into slot 0 after the shift.
- **Rule** is to copy in the direction that keeps the destination behind the source.
- **`System.arraycopy`** handles overlapping ranges correctly, as its documentation states, so it is a safe alternative.

**Complexity.**

- **Time** is O(n), because the shift moves each live value once.
- **Space** is O(1), because the shift works in place and needs no second array.

```java run
import java.util.Arrays;

public final class MutationOrder {
    /**
     * Shifts the live values right by one, copying from the left (the buggy order).
     * Time: O(n), one write per live value. Space: O(1), in place.
     * Defect: a[i] is overwritten before the loop reads it as the source of the next step.
     */
    // The loop writes positions 1 to live; each write destroys the next unread source value.
    static void shiftLeftToRight(int[] a, int live) { for (int i = 1; i <= live; i++) a[i] = a[i - 1]; }
    /**
     * Shifts the live values right by one, copying from the right (the safe order).
     * Time: O(n), one write per live value. Space: O(1), in place.
     * Invariant: slots 0 to i - 1 are untouched when step i reads a[i - 1].
     */
    // The loop runs from the free slot down, so every write lands on a value already moved.
    static void shiftRightToLeft(int[] a, int live) { for (int i = live; i >= 1; i--) a[i] = a[i - 1]; }

    public static void main(String[] args) {
        int[] bad = {1, 2, 3, 0};
        shiftLeftToRight(bad, 3);
        // The left-to-right shift copies the first value everywhere and loses the data.
        if (!Arrays.equals(bad, new int[] {1, 1, 1, 1})) throw new AssertionError("left to right destroys data");
        int[] good = {1, 2, 3, 0};
        shiftRightToLeft(good, 3);
        // The right-to-left shift keeps every live value, shifted by one.
        if (!Arrays.equals(good, new int[] {1, 1, 2, 3})) throw new AssertionError("right to left keeps data");
        good[0] = 9;
        // The insert into slot 0 completes the result [9, 1, 2, 3].
        if (!Arrays.equals(good, new int[] {9, 1, 2, 3})) throw new AssertionError("after insert");
        int[] viaCopy = {1, 2, 3, 0};
        System.arraycopy(viaCopy, 0, viaCopy, 1, 3);
        // System.arraycopy gives the same safe result on overlapping ranges.
        if (!Arrays.equals(viaCopy, new int[] {1, 1, 2, 3})) throw new AssertionError("arraycopy handles overlap");
    }
}
```
