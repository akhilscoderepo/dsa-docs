<!-- solutions-for: 04-input-guarantees -->
### Solutions For Input Preconditions

#### Solution: [Build] Non-Empty Maximum (Author exercise)
<!-- id: pc-non-empty-maximum -->

**Approach.**
The method starts `best` at `nums[0]`, a real member of the input, because the specification promises at least one element. Then the loop visits the remaining elements from index 1. At each step, `best` keeps the larger of itself and the current element. The invariant is that `best` equals the maximum of the elements read so far, so it is the maximum of the whole array when the loop ends.

A zero start assumes zero is below every value, and it fails on `[-8,-3]` with result 0 instead of -3. An empty-array guard is dead code under this specification, and it implies a precondition the problem never stated.

**Complexity.**
- **Time** is O(n), because the loop reads each of the `n` elements once.
- **Space** is O(1), because the method stores only `best` and the loop index.

```java run
public final class NonEmptyMaximum {
    /**
     * Returns the maximum of a non-empty array.
     * Time: O(n), because the loop reads each element once.
     * Space: O(1), because only best and i are stored.
     * Invariant: best is the maximum of nums[0..i-1] at the start of each iteration.
     * Precondition: nums.length >= 1, so nums[0] exists.
     */
    static int maxNonEmpty(int[] nums) {
        // Start from a real element, so the start can never beat the true maximum.
        int best = nums[0];
        // Index 0 is already in best, so the loop starts at 1 and runs n - 1 times.
        // Each element is compared once, which is the O(n) cost.
        for (int i = 1; i < nums.length; i++) best = Math.max(best, nums[i]);
        // The invariant now covers the whole array.
        return best;
    }
    /**
     * Buggy variant that starts from zero; it exists only to show the failure.
     * Time: O(n), because the loop reads each element once.
     * Space: O(1), because only best is stored.
     */
    static int maxZeroStart(int[] nums) {
        // Zero is not an element of the input, so this start can exceed every value.
        int best = 0;
        // Only a value above zero can replace best, so an all-negative array keeps 0.
        for (int v : nums) if (v > best) best = v;
        // Wrong for all-negative input.
        return best;
    }

    public static void main(String[] args) {
        // All-negative input: the correct method returns -3 and the zero-start method returns 0.
        if (maxNonEmpty(new int[] {-8, -3}) != -3) throw new AssertionError("negative maximum");
        if (maxZeroStart(new int[] {-8, -3}) != 0) throw new AssertionError("the zero-start bug is real");
        // A single element is its own maximum.
        if (maxNonEmpty(new int[] {7}) != 7) throw new AssertionError("single element");
        // The smallest int still works, because the start is an element and not a constant.
        if (maxNonEmpty(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("extreme values");
    }
}
```

#### Solution: [Vary] Possibly Empty (Author exercise)
<!-- id: pc-possibly-empty -->

**Approach.**
`OptionalInt` makes absence part of the return type, so a caller must handle the case where no answer exists. A sentinel is rejected, because a value such as `Integer.MIN_VALUE` collides with a legal answer. The range `-10^9..10^9` makes every integer a legal maximum, so no safe sentinel exists unless the range excludes one.

Empty input returns `OptionalInt.empty()` when `nums.length == 0`. Non-empty input starts `best` at `nums[0]`, keeps the larger value in a loop, and returns `OptionalInt.of(best)`. The documentation says "empty when the array is empty" and adds no other convention.

**Complexity.**
- **Time** is O(n), because the loop reads each of the `n` elements once.
- **Space** is O(1), because the method stores only `best`, and the returned optional is a constant-size object.

```java run
import java.util.OptionalInt;

public final class PossiblyEmpty {
    /**
     * Returns the maximum of nums, or an empty optional when nums is empty.
     * Time: O(n), because the loop reads each element once.
     * Space: O(1), because only best is stored and the optional has constant size.
     * Invariant: after each iteration, best is the maximum of the elements read so far.
     */
    static OptionalInt maxOrNone(int[] nums) {
        // Absence is part of the return type, so no int value is reserved as "no answer".
        if (nums.length == 0) return OptionalInt.empty();
        // The array is non-empty here, so nums[0] is a real element and a safe start.
        int best = nums[0];
        // Reading each element once gives the O(n) cost; index 0 is re-read, which does no harm.
        for (int v : nums) best = Math.max(best, v);
        // Wrap the result so a legal negative maximum stays distinct from "no answer".
        return OptionalInt.of(best);
    }

    public static void main(String[] args) {
        // Empty input must report absence.
        if (maxOrNone(new int[] {}).isPresent()) throw new AssertionError("empty input has no maximum");
        // A negative maximum is still an answer.
        if (maxOrNone(new int[] {-5}).getAsInt() != -5) throw new AssertionError("a negative answer stays an answer");
        // The smallest int is a legal maximum, which shows why a sentinel would collide.
        if (maxOrNone(new int[] {Integer.MIN_VALUE}).getAsInt() != Integer.MIN_VALUE) throw new AssertionError("no sentinel collision");
    }
}
```

#### Solution: [Boundary] Rectangular Or Ragged (Author exercise)
<!-- id: pc-rectangular-or-ragged -->

**Approach.**
The bound `grid[0].length` measures only the first row. A shorter row makes that bound overrun and throw `ArrayIndexOutOfBoundsException`. A longer row makes that bound skip the extra cells silently.

Therefore the inner bound is `c < grid[r].length`, which evaluates the length of the current row `r`. The variable `count` increases by one per inner iteration. The invariant is that `count` equals the number of cells in the rows and columns already visited. Rectangular grids also work with this form, so it is correct whatever the shape. Zero rows and zero-length rows make the matching loop body not run.

**Complexity.**
- **Time** is O(R + C), where R is the number of rows and C is the total number of cells, because the outer loop runs R times and the inner iterations add up to C.
- **Time** reduces to O(total cells) when rows are non-empty.
- **Space** is O(1), because the method stores only `count` and two indexes.

```java run
public final class RectangularOrRagged {
    /**
     * Counts the cells of a rectangular or ragged grid.
     * Time: O(R + C) for R rows and C cells, because each row and each cell is visited once.
     * Space: O(1), because only count and two indexes are stored.
     * Invariant: count is the number of cells in the rows and columns visited so far.
     */
    static int cellsSafe(int[][] grid) {
        int count = 0;
        // One pass over the rows; this loop runs R times and does nothing for zero rows.
        for (int r = 0; r < grid.length; r++)
            // The bound is this row's own length, so short, long and empty rows are all correct.
            for (int c = 0; c < grid[r].length; c++) { int cell = grid[r][c]; count++; }
        // count now holds every cell in the grid.
        return count;
    }
    /**
     * Buggy variant that trusts the first row's length for every row.
     * Time: O(R * grid[0].length), because every row is scanned to the first row's width.
     * Space: O(1), because only count and two indexes are stored.
     */
    static int cellsAssumingRectangular(int[][] grid) {
        int count = 0;
        // Visit every row, as the safe version does.
        for (int r = 0; r < grid.length; r++)
            // The shared bound grid[0].length is wrong when this row is shorter or longer than row 0.
            for (int c = 0; c < grid[0].length; c++) { int cell = grid[r][c]; count++; }   // reads each cell, so a short row fails
        return count;
    }

    public static void main(String[] args) {
        // A ragged grid has 3 + 1 + 2 = 6 cells.
        int[][] ragged = {{1, 2, 3}, {4}, {5, 6}};
        if (cellsSafe(ragged) != 6) throw new AssertionError("ragged count");
        // The rectangular assumption must throw on the short second row.
        boolean crashed = false;
        try { cellsAssumingRectangular(ragged); } catch (ArrayIndexOutOfBoundsException e) { crashed = true; }
        // On a rectangular grid both loop forms agree.
        if (cellsAssumingRectangular(new int[][] {{1, 2}, {3, 4}}) != 4 || cellsSafe(new int[][] {{1, 2}, {3, 4}}) != 4) throw new AssertionError("rectangular count");
        // Edge cases: no rows, and a row of length zero.
        if (cellsSafe(new int[][] {}) != 0) throw new AssertionError("no rows");
        if (cellsSafe(new int[][] {{}, {7}}) != 1) throw new AssertionError("a zero-length row");
        // Confirms the exception actually happened.
        if (!crashed) throw new AssertionError("the rectangular assumption must fail on ragged input");
    }
}
```

#### Solution: [Recognize] Sorted Promise (Author exercise)
<!-- id: pc-sorted-promise -->

**Approach.**
Sorted order places equal values next to each other, so a new value starts exactly when `nums[i]` differs from `nums[i - 1]`. An empty array has no values, so the method returns 0. Otherwise, `distinct` starts at 1, because the first element begins the first run.

Then the scan runs from index 1 and adds one at every position where `nums[i] != nums[i - 1]`. The invariant is that `distinct` equals the number of runs in `nums[0..i]`, which equals the number of distinct values because the array is sorted. An unsorted array breaks the precondition, so the same loop counts runs and `[1,2,1]` gives 3 instead of 2.

**Complexity.**
- **Time** is O(n), because the loop makes one comparison for each of the `n - 1` later elements.
- **Space** is O(1), because the method stores only `distinct` and the loop index, and no set is needed.

```java run
public final class SortedPromise {
    /**
     * Counts distinct values in a sorted array.
     * Time: O(n), because the loop compares each element with its predecessor once.
     * Space: O(1), because only distinct and i are stored.
     * Invariant: distinct is the number of runs in nums[0..i] at the end of iteration i.
     * Precondition: nums is sorted in non-decreasing order (not checked).
     */
    static int distinctInSorted(int[] nums) {
        // An empty array has no values and no runs; this also protects the nums[0] case below.
        if (nums.length == 0) return 0;
        // The first element always starts the first run.
        int distinct = 1;
        // Start at 1 because index 0 has no predecessor; the loop runs n - 1 times.
        // A change from the previous element marks the start of a new run, so add one.
        for (int i = 1; i < nums.length; i++) if (nums[i] != nums[i - 1]) distinct++;
        // For sorted input, runs and distinct values are the same count.
        return distinct;
    }

    public static void main(String[] args) {
        // Three runs: 1s, 2s and 5.
        if (distinctInSorted(new int[] {1, 1, 2, 2, 2, 5}) != 3) throw new AssertionError("three values");
        // Edge cases: empty and single element.
        if (distinctInSorted(new int[] {}) != 0) throw new AssertionError("empty");
        if (distinctInSorted(new int[] {4}) != 1) throw new AssertionError("single");
        // Unsorted input breaks the promise: runs are counted, so the result is 3 for two distinct values.
        if (distinctInSorted(new int[] {1, 2, 1}) != 3) throw new AssertionError("without the promise the loop counts runs, so this reports 3 for two values");
    }
}
```
