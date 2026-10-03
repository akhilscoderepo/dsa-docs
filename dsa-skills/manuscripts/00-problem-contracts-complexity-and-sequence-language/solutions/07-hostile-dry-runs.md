<!-- solutions-for: 07-hostile-dry-runs -->
### Hostile Dry Runs

#### Solution: [Build] Singleton (Author exercise)
<!-- id: pc-singleton -->

**Approach.** With one element the loop `for (i = 1; i < 1; ...)` never executes, so the result comes entirely from the initialization. The corrected method starts `best` at 1, because any non-empty list holds a climb of length one, and returns 1. The flawed version starts `best` at 0 and only updates it inside the loop, so it returns 0. The dry-run ledger therefore has a single row, the initial one, and that row already shows the wrong meaning for `best`.

**Complexity.** O(n) time, O(1) space, and zero loop iterations for a single element.

```java run
public final class Singleton {
    static int fixed(int[] a) {
        if (a.length == 0) return 0;
        int best = 1, cur = 1;
        for (int i = 1; i < a.length; i++) { cur = a[i] > a[i - 1] ? cur + 1 : 1; best = Math.max(best, cur); }
        return best;
    }
    static int flawed(int[] a) {
        int best = 0, cur = 1;
        for (int i = 1; i < a.length; i++) {
            if (a[i] > a[i - 1]) cur++; else { best = Math.max(best, cur); cur = 1; }
        }
        return best;
    }
    static int iterations(int length) { int n = 0; for (int i = 1; i < length; i++) n++; return n; }

    public static void main(String[] args) {
        if (iterations(1) != 0) throw new AssertionError("no iterations for one element");
        if (fixed(new int[] {7}) != 1) throw new AssertionError("fixed result");
        if (flawed(new int[] {7}) != 0) throw new AssertionError("flawed result is the initialization bug");
        if (fixed(new int[] {}) != 0) throw new AssertionError("empty contract");
    }
}
```

#### Solution: [Vary] All Equal (Author exercise)
<!-- id: pc-all-equal -->

**Approach.** With a strict comparison, two equal neighbors do not extend a climb, so every day restarts at length 1 and the answer is 1. With a non-strict comparison, equal neighbors do extend the run, so the answer is 3. The values never differ, so this one input separates the two comparisons completely, and no input with distinct values could do so.

**Complexity.** O(n) time and O(1) space for each version.

```java run
public final class AllEqual {
    static int run(int[] a, boolean strict) {
        if (a.length == 0) return 0;
        int best = 1, cur = 1;
        for (int i = 1; i < a.length; i++) {
            boolean extends_ = strict ? a[i] > a[i - 1] : a[i] >= a[i - 1];
            cur = extends_ ? cur + 1 : 1;
            best = Math.max(best, cur);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] equal = {4, 4, 4};
        if (run(equal, true) != 1) throw new AssertionError("strict");
        if (run(equal, false) != 3) throw new AssertionError("non-strict");
        int[] distinct = {1, 2, 3};
        if (run(distinct, true) != run(distinct, false)) throw new AssertionError("distinct values do not separate the two comparisons");
    }
}
```

#### Solution: [Boundary] Numeric Extremes (Author exercise)
<!-- id: pc-numeric-extremes -->

**Approach.** The true sum is 2 * 2,147,483,647 = 4,294,967,294, which is above the `int` maximum. In two's-complement arithmetic the result wraps around to 4,294,967,294 - 2^32, which is -2. Predict that before running, then confirm it. The fix is a `long` accumulator, which holds 4,294,967,294 exactly. The attacker works because it sits at the extreme of the type, where the wrap-around is guaranteed.

**Complexity.** O(n) time, O(1) space.

```java run
public final class NumericExtremes {
    static int sumInt(int[] a) { int s = 0; for (int v : a) s += v; return s; }
    static long sumLong(int[] a) { long s = 0; for (int v : a) s += v; return s; }

    public static void main(String[] args) {
        int[] hostile = {Integer.MAX_VALUE, Integer.MAX_VALUE};
        if (sumInt(hostile) != -2) throw new AssertionError("wrap-around gives -2");
        if (sumLong(hostile) != 4_294_967_294L) throw new AssertionError("the long sum");
        if (Math.abs(Integer.MIN_VALUE) >= 0) throw new AssertionError("abs of MIN_VALUE stays negative");
    }
}
```

#### Solution: [Recognize] Mutation Order (Author exercise)
<!-- id: pc-mutation-order -->

**Approach.** Copying left to right does `a[1] = a[0]`, which overwrites the old `a[1]` before it was read, then `a[2] = a[1]`, which copies the already overwritten value, and so on, so every slot ends up holding the first value. Copying right to left does `a[3] = a[2]`, `a[2] = a[1]`, `a[1] = a[0]`, and each write lands on a slot whose old value has already been moved. After the shift the insert writes 9 into slot 0. The general rule is to copy in the direction that keeps the destination behind the source. `System.arraycopy` handles overlapping ranges correctly, as its documentation states, so it is a safe shortcut.

**Complexity.** O(n) time for the shift, O(1) extra space.

```java run
import java.util.Arrays;

public final class MutationOrder {
    static void shiftLeftToRight(int[] a, int live) { for (int i = 1; i <= live; i++) a[i] = a[i - 1]; }
    static void shiftRightToLeft(int[] a, int live) { for (int i = live; i >= 1; i--) a[i] = a[i - 1]; }

    public static void main(String[] args) {
        int[] bad = {1, 2, 3, 0};
        shiftLeftToRight(bad, 3);
        if (!Arrays.equals(bad, new int[] {1, 1, 1, 1})) throw new AssertionError("left to right destroys data");
        int[] good = {1, 2, 3, 0};
        shiftRightToLeft(good, 3);
        if (!Arrays.equals(good, new int[] {1, 1, 2, 3})) throw new AssertionError("right to left keeps data");
        good[0] = 9;
        if (!Arrays.equals(good, new int[] {9, 1, 2, 3})) throw new AssertionError("after insert");
        int[] viaCopy = {1, 2, 3, 0};
        System.arraycopy(viaCopy, 0, viaCopy, 1, 3);
        if (!Arrays.equals(viaCopy, new int[] {1, 1, 2, 3})) throw new AssertionError("arraycopy handles overlap");
    }
}
```
