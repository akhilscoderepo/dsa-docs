<!-- solutions-for: 04-input-guarantees -->
### Input Guarantees

#### Solution: [Build] Non-Empty Maximum (Author exercise)
<!-- id: pc-non-empty-maximum -->

**Approach.** The contract promises at least one element, so `nums[0]` is a real member of the input and a safe starting point. Starting from zero assumes zero is below every value, which fails on `[-8,-3]`, where it returns 0 instead of -3. An empty-array guard would be dead code under this contract, and its presence would suggest a promise that the problem never made.

**Complexity.** O(n) time, O(1) extra space.

```java run
public final class NonEmptyMaximum {
    static int maxNonEmpty(int[] nums) {
        int best = nums[0];
        for (int i = 1; i < nums.length; i++) best = Math.max(best, nums[i]);
        return best;
    }
    static int maxZeroStart(int[] nums) {
        int best = 0;
        for (int v : nums) if (v > best) best = v;
        return best;
    }

    public static void main(String[] args) {
        if (maxNonEmpty(new int[] {-8, -3}) != -3) throw new AssertionError("negative maximum");
        if (maxZeroStart(new int[] {-8, -3}) != 0) throw new AssertionError("the zero-start bug is real");
        if (maxNonEmpty(new int[] {7}) != 7) throw new AssertionError("single element");
        if (maxNonEmpty(new int[] {Integer.MIN_VALUE, Integer.MIN_VALUE}) != Integer.MIN_VALUE) throw new AssertionError("extreme values");
    }
}
```

#### Solution: [Vary] Possibly Empty (Author exercise)
<!-- id: pc-possibly-empty -->

**Approach.** Pick the optional-result design. `OptionalInt` makes absence part of the type, so a caller must decide what to do with it. A sentinel such as `Integer.MIN_VALUE` would collide with a legal answer when the range may contain that value, and any integer in `-10^9..10^9` can be a legal maximum, so no safe sentinel exists unless the range excludes one. The signature returns the optional, the documentation says "empty when the array is empty", and nothing else is invented.

**Complexity.** O(n) time, O(1) extra space.

```java run
import java.util.OptionalInt;

public final class PossiblyEmpty {
    static OptionalInt maxOrNone(int[] nums) {
        if (nums.length == 0) return OptionalInt.empty();
        int best = nums[0];
        for (int v : nums) best = Math.max(best, v);
        return OptionalInt.of(best);
    }

    public static void main(String[] args) {
        if (maxOrNone(new int[] {}).isPresent()) throw new AssertionError("empty input has no maximum");
        if (maxOrNone(new int[] {-5}).getAsInt() != -5) throw new AssertionError("a negative answer stays an answer");
        if (maxOrNone(new int[] {Integer.MIN_VALUE}).getAsInt() != Integer.MIN_VALUE) throw new AssertionError("no sentinel collision");
    }
}
```

#### Solution: [Boundary] Rectangular Or Ragged (Author exercise)
<!-- id: pc-rectangular-or-ragged -->

**Approach.** `grid[0].length` measures only the first row. When rows can differ it overruns a shorter row with an `ArrayIndexOutOfBoundsException`, or it silently skips cells in a longer one. The safe bound is each row's own length, `grid[r].length`, evaluated inside the outer loop. That form is correct for rectangular grids too, so it costs nothing to use when the shape is unclear.

**Complexity.** O(total cells) time and O(1) extra space.

```java run
public final class RectangularOrRagged {
    static int cellsSafe(int[][] grid) {
        int count = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[r].length; c++) { int cell = grid[r][c]; count++; }
        return count;
    }
    static int cellsAssumingRectangular(int[][] grid) {
        int count = 0;
        for (int r = 0; r < grid.length; r++)
            for (int c = 0; c < grid[0].length; c++) { int cell = grid[r][c]; count++; }   // reads each cell, so a short row fails
        return count;
    }

    public static void main(String[] args) {
        int[][] ragged = {{1, 2, 3}, {4}, {5, 6}};
        if (cellsSafe(ragged) != 6) throw new AssertionError("ragged count");
        boolean crashed = false;
        try { cellsAssumingRectangular(ragged); } catch (ArrayIndexOutOfBoundsException e) { crashed = true; }
        if (cellsAssumingRectangular(new int[][] {{1, 2}, {3, 4}}) != 4 || cellsSafe(new int[][] {{1, 2}, {3, 4}}) != 4) throw new AssertionError("rectangular count");
        if (cellsSafe(new int[][] {}) != 0) throw new AssertionError("no rows");
        if (cellsSafe(new int[][] {{}, {7}}) != 1) throw new AssertionError("a zero-length row");
        if (!crashed) throw new AssertionError("the rectangular assumption must fail on ragged input");
    }
}
```

#### Solution: [Recognize] Sorted Promise (Author exercise)
<!-- id: pc-sorted-promise -->

**Approach.** Sorted order means equal values are neighbors, so a new value has started exactly when the current element differs from the previous one. Count 1 for the first element and then one more at every position where `nums[i] != nums[i - 1]`. This relies on the sorted guarantee and never checks it. On an unsorted array the same loop would count runs, not distinct values, and `[1,2,1]` would be wrong.

**Complexity.** O(n) time, O(1) extra space.

```java run
public final class SortedPromise {
    static int distinctInSorted(int[] nums) {
        if (nums.length == 0) return 0;
        int distinct = 1;
        for (int i = 1; i < nums.length; i++) if (nums[i] != nums[i - 1]) distinct++;
        return distinct;
    }

    public static void main(String[] args) {
        if (distinctInSorted(new int[] {1, 1, 2, 2, 2, 5}) != 3) throw new AssertionError("three values");
        if (distinctInSorted(new int[] {}) != 0) throw new AssertionError("empty");
        if (distinctInSorted(new int[] {4}) != 1) throw new AssertionError("single");
        if (distinctInSorted(new int[] {1, 2, 1}) != 3) throw new AssertionError("without the promise the loop counts runs, so this reports 3 for two values");
    }
}
```
