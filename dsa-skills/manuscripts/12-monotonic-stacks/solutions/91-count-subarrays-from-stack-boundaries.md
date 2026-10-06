<!-- solutions-for: 91-count-subarrays-from-stack-boundaries -->
### Solutions For The Stack Counting Exercises

#### Solution: [Build] Next Greater Element I Pairs (LeetCode 496)
<!-- id: ms-combo-pop-pairs -->

**Approach.**

The method scans the array once and keeps a stack of indices that still wait for a larger value. When index `j` arrives, it removes the top while the top value is strictly less than `a[j]`, and each removal records the pair of the removed index and `j`. The stack holds increasing indices, so the top is the newest waiting index, and the pairs for one `j` come out from the largest index downward. The invariant is that every index on the stack has no strictly larger value after it so far. Equal values never leave, because the comparison is strict. The assertions check both examples and then compare the output with a direct search for the first larger value on the right, sorted by arrival and then by descending index.

**Complexity.**

- **Time** is O(n + p), where `p` is the number of pairs, because each index is pushed once and removed at most once.
- **Space** is O(n) for the stack and the recorded pairs.

```java run
import java.util.*;

public final class PopPairs {
    /**
     * Returns [removed index, arriving index] in removal order.
     * Time: O(n). Space: O(n).
     * Invariant: an index waits on the stack only while no strictly larger value follows it.
     */
    static int[][] solve(int[] a) {
        List<int[]> out = new ArrayList<>();
        int[] stack = new int[a.length];
        int size = 0;                                           // number of waiting indices
        for (int j = 0; j < a.length; j++) {                    // one arrival per index
            while (size > 0 && a[stack[size - 1]] < a[j]) {     // strict: equal values keep waiting
                out.add(new int[]{stack[--size], j});           // the top is resolved by j
            }
            stack[size++] = j;                                  // j waits for its own larger value
        }
        return out.toArray(new int[0][]);
    }

    static int[][] oracle(int[] a) {
        List<int[]> out = new ArrayList<>();
        for (int j = 0; j < a.length; j++) {
            for (int t = j - 1; t >= 0; t--) {                  // descending index order within one arrival
                boolean first = a[t] < a[j];
                for (int k = t + 1; k < j; k++) if (a[k] > a[t]) first = false;   // an earlier larger value resolved t
                if (first) out.add(new int[]{t, j});
            }
        }
        return out.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.deepEquals(solve(new int[]{4, 1, 2, 5}), new int[][]{{1, 2}, {2, 3}, {0, 3}})) throw new AssertionError("example 1");
        if (solve(new int[]{3, 3, 3}).length != 0) throw new AssertionError("example 2");
        // Random arrays agree with the direct search.
        Random rnd = new Random(41);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(6) - 2;
            if (!Arrays.deepEquals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Daily Temperatures With The Longest Wait (LeetCode 739)
<!-- id: ms-combo-longest-wait -->

**Approach.**

The method keeps the same stack as the previous exercise. When day `j` removes day `t`, the wait of `t` is `j - t`, and the method compares that wait with the best wait so far. A larger wait replaces the best pair. An equal wait replaces it only when `t` is smaller than the stored start. Days that stay on the stack have no wait and never enter the comparison, so the result stays `[-1, -1]` when nothing leaves. The invariant is that the stored pair is the best among all days removed so far. The assertions compare the result with a quadratic search for each day's first warmer day.

**Complexity.**

- **Time** is O(n), because each day enters and leaves the stack once and each leaving costs a constant comparison.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class LongestWait {
    /**
     * Returns [start, wait] for the longest wait, with the smallest start on ties, or [-1, -1].
     * Time: O(n). Space: O(n).
     * Invariant: best holds the largest wait among the days removed so far.
     */
    static int[] solve(int[] temp) {
        int[] stack = new int[temp.length];
        int size = 0;
        int bestStart = -1, bestWait = 0;
        for (int j = 0; j < temp.length; j++) {                 // day j may resolve waiting days
            while (size > 0 && temp[stack[size - 1]] < temp[j]) {   // a warmer day ends the wait of the top
                int t = stack[--size];
                int wait = j - t;                               // distance from the waiting day to the warmer day
                if (wait > bestWait || (wait == bestWait && t < bestStart)) {   // larger wait, or earlier start on a tie
                    bestWait = wait;
                    bestStart = t;
                }
            }
            stack[size++] = j;                                  // day j waits for its own warmer day
        }
        return bestStart < 0 ? new int[]{-1, -1} : new int[]{bestStart, bestWait};
    }

    static int[] oracle(int[] temp) {
        int bs = -1, bw = 0;
        for (int i = 0; i < temp.length; i++) {
            for (int j = i + 1; j < temp.length; j++) {
                if (temp[j] > temp[i]) {                        // the first warmer day fixes the wait of day i
                    if (j - i > bw) { bw = j - i; bs = i; }     // scanning i upward keeps the smallest start on ties
                    break;
                }
            }
        }
        return bs < 0 ? new int[]{-1, -1} : new int[]{bs, bw};
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(solve(new int[]{73, 74, 75, 71, 69, 72, 76, 73}), new int[]{2, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[]{5, 4, 3}), new int[]{-1, -1})) throw new AssertionError("example 2");
        // Random arrays agree with the quadratic search, including ties.
        Random rnd = new Random(43);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Largest Rectangle With Its Left Index (LeetCode 84)
<!-- id: ms-combo-best-rectangle-left -->

**Approach.**

The method scans the heights with a stack whose heights never decrease from bottom to top. A bar leaves the stack when the arriving bar is not taller, and the arriving index is the right boundary. The new top is the left boundary, or `-1` for an empty stack. The leaving bar then spans the indices `left + 1` through `j - 1`, with area `height * (j - left - 1)`. The closing step uses height 0 at index `n`, which is below every real height, so it removes the bars that no shorter bar ever ended. In an increasing histogram such as Example 2, only this step reports rectangles. The pair `(area, left + 1)` replaces the best pair when the area is larger, or when it is equal and the left index is smaller. The invariant is that the best pair covers every bar that has left the stack. The assertions compare the result with a check of every range of bars.

**Complexity.**

- **Time** is O(n), as every bar enters the stack once and leaves it once.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class BestRectangle {
    /**
     * Returns [largest area, smallest left index among rectangles with that area].
     * Time: O(n). Space: O(n).
     * Invariant: the best pair covers every bar that has left the stack.
     */
    static int[] solve(int[] h) {
        int n = h.length;
        int[] stack = new int[n];
        int size = 0;
        int bestArea = 0, bestLeft = 0;
        for (int j = 0; j <= n; j++) {                          // j == n is the closing step with height 0
            int v = j == n ? 0 : h[j];
            while (size > 0 && h[stack[size - 1]] >= v) {       // the arriving bar is not taller, so the top ends here
                int t = stack[--size];
                int left = size == 0 ? -1 : stack[size - 1];    // the new top is the left boundary
                int area = h[t] * (j - left - 1);               // height times the bars strictly between the boundaries
                if (area > bestArea || (area == bestArea && left + 1 < bestLeft)) {   // larger area, or earlier start on a tie
                    bestArea = area;
                    bestLeft = left + 1;
                }
            }
            if (j < n) stack[size++] = j;                       // the arriving bar waits for a shorter bar
        }
        return new int[]{bestArea, bestLeft};
    }

    static int[] oracle(int[] h) {
        int bestArea = 0, bestLeft = 0;
        for (int l = 0; l < h.length; l++) {
            int low = Integer.MAX_VALUE;
            for (int r = l; r < h.length; r++) {
                low = Math.min(low, h[r]);                      // the shortest bar of the range sets the height
                int area = low * (r - l + 1);
                if (area > bestArea) { bestArea = area; bestLeft = l; }   // a larger l never beats an equal area found earlier
            }
        }
        return new int[]{bestArea, bestLeft};
    }

    public static void main(String[] args) {
        // Worked examples.
        if (!Arrays.equals(solve(new int[]{2, 1, 5, 6, 2, 3}), new int[]{10, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[]{1, 2, 3, 4}), new int[]{6, 1})) throw new AssertionError("example 2");
        // Equal heights, one bar and a flat histogram.
        if (!Arrays.equals(solve(new int[]{4, 4, 4}), new int[]{12, 0})) throw new AssertionError("flat");
        if (!Arrays.equals(solve(new int[]{7}), new int[]{7, 0})) throw new AssertionError("single");
        // Random histograms agree with the check of every range.
        Random rnd = new Random(47);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(5);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Sum Of Subarray Maximums (LeetCode 907)
<!-- id: ms-combo-sum-maximums -->

**Approach.**

The method gives each subarray to its rightmost maximum. A leaving index `t` has the right boundary `j`, which is the first value on its right that is greater than or equal to `a[t]`. Its left boundary is the new top of the stack, which is strictly greater than `a[t]`. A subarray owned by `t` picks a start from `t - left` indices and an end from `j - t` indices, so `t` owns `(t - left) * (j - t)` subarrays. The method adds `a[t]` times that count in `long`. A negative value needs no special case, because the product keeps its sign. The invariant is that each subarray is counted once, by its rightmost maximum. The assertions include a negative array and the all-equal array, where a wrong tie rule changes the total.

**Complexity.**

- **Time** is O(n), because a leaving index costs one multiplication and the loop never revisits an index after it leaves.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class SumOfMaximums {
    /**
     * Returns the sum of the maximum of every non-empty subarray.
     * Time: O(n). Space: O(n).
     * Invariant: every subarray is counted once, by its rightmost maximum.
     */
    static long solve(int[] a) {
        int n = a.length;
        int[] stack = new int[n];
        int size = 0;
        long total = 0;
        for (int j = 0; j <= n; j++) {                          // j == n removes the indices that no larger value followed
            while (size > 0 && (j == n || a[stack[size - 1]] <= a[j])) {   // equality removes, so the later maximum owns ties
                int t = stack[--size];
                int left = size == 0 ? -1 : stack[size - 1];    // the new top is strictly greater than a[t]
                total += (long) a[t] * (t - left) * (j - t);    // value times starts times ends, in long
            }
            if (j < n) stack[size++] = j;                       // the arriving index waits for a value at least as large
        }
        return total;
    }

    static long oracle(int[] a) {
        long total = 0;
        for (int l = 0; l < a.length; l++) {
            int hi = Integer.MIN_VALUE;
            for (int r = l; r < a.length; r++) {
                hi = Math.max(hi, a[r]);                        // running maximum of the range l..r
                total += hi;
            }
        }
        return total;
    }

    public static void main(String[] args) {
        // Worked examples.
        if (solve(new int[]{3, 1, 2}) != 14) throw new AssertionError("example 1");
        if (solve(new int[]{-2, -2, -2}) != -12) throw new AssertionError("example 2");
        // Largest allowed length with the largest value stays inside long.
        int[] big = new int[30000];
        Arrays.fill(big, 100000);
        if (solve(big) != 100000L * 30000L * 30001L / 2) throw new AssertionError("big");
        // Random arrays with negative values agree with the quadratic sum.
        Random rnd = new Random(53);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(7) - 3;
            if (solve(a) != oracle(a)) throw new AssertionError(Arrays.toString(a));
        }
    }
}
```
