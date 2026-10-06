<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For The Largest Rectangle

#### Solution: [Build] Rectangle From Supplied Boundaries (Author exercise)
<!-- id: ms-rectangle-from-boundaries -->

**Approach.**
The widest banner at the height of bar `i` stretches over every bar strictly between its two boundaries. Those bars number `right[i] - left[i] - 1`, because the boundaries themselves are shorter and excluded. Every bar between them is at least as tall as bar `i`, so the banner of height `heights[i]` fits. The best rectangle has the height of some bar, so the maximum over all indices is the answer. The product is formed in `long`, because a height near 10^9 times a width near 10^5 passes the range of `int`.

**Complexity.**
- **Time** is O(n), because each index needs one subtraction and one product.
- **Space** is O(1) beyond the inputs.

```java run
import java.util.Random;

public final class RectangleFromBoundaries {
    /**
     * Returns the maximum of heights[i] * (right[i] - left[i] - 1).
     * Time: O(n). Space: O(1).
     * Invariant: every bar strictly between the boundaries is at least heights[i].
     */
    static long solve(int[] heights, int[] left, int[] right) {
        long best = 0;
        // One candidate banner per bar height.
        for (int i = 0; i < heights.length; i++) {
            // The width counts the bars strictly between the two boundaries.
            long width = right[i] - left[i] - 1;
            best = Math.max(best, heights[i] * width);
        }
        return best;
    }

    /** Reference: try every pair of end bars. */
    static long oracle(int[] h) {
        long best = 0;
        for (int l = 0; l < h.length; l++) {
            int low = Integer.MAX_VALUE;
            for (int r = l; r < h.length; r++) {
                low = Math.min(low, h[r]);
                best = Math.max(best, (long) low * (r - l + 1));
            }
        }
        return best;
    }

    /** Builds strictly smaller boundaries by walking outward. */
    static int[][] boundaries(int[] h) {
        int n = h.length;
        int[] left = new int[n];
        int[] right = new int[n];
        for (int i = 0; i < n; i++) {
            int j = i - 1;
            while (j >= 0 && h[j] >= h[i]) j--;
            left[i] = j;
            int k = i + 1;
            while (k < n && h[k] >= h[i]) k++;
            right[i] = k;
        }
        return new int[][] {left, right};
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {3, 1, 3, 2, 2}, new int[] {-1, -1, 1, 1, 1}, new int[] {1, 5, 3, 5, 5}) != 6) throw new AssertionError("example 1");
        if (solve(new int[] {2, 5, 6, 3, 0, 4, 4}, new int[] {-1, 0, 1, 0, -1, 4, 4}, new int[] {4, 3, 3, 4, 7, 7, 7}) != 10) throw new AssertionError("example 2");
        // Large heights keep the product exact in long.
        if (solve(new int[] {1_000_000_000, 1_000_000_000}, new int[] {-1, -1}, new int[] {2, 2}) != 2_000_000_000L) throw new AssertionError("long");
        // Random charts with correct boundaries must match the oracle.
        Random rnd = new Random(107);
        for (int t = 0; t < 3000; t++) {
            int[] h = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < h.length; i++) h[i] = rnd.nextInt(6);
            int[][] b = boundaries(h);
            if (solve(h, b[0], b[1]) != oracle(h)) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Resolve On A Shorter Bar (Author exercise)
<!-- id: ms-resolve-on-shorter-bar -->

**Approach.**
The stack holds bar indices whose heights never decrease from bottom to top. When the current bar is shorter than the top, the current index is the right boundary of the top, and the new top after the pop is its left boundary. The banner at the popped height spans the bars strictly between them, so its width is `i - top - 1`, or `i` when the stack is empty. The final entry of the input is `0`, so it pops every bar of positive height without a separate flush. When equal bars sit on the stack, the first one to pop may compute a smaller width, and the equal bar below it pops next and computes the full width, so the maximum is correct.

**Complexity.**
- **Time** is O(n), because every index enters the stack once and leaves it at most once.
- **Space** is O(n), because a non-decreasing chart keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Random;

public final class ResolveOnShorterBar {
    /**
     * Returns the largest rectangle area for a chart that ends with a zero height.
     * Time: O(n). Space: O(n).
     * Invariant: stack heights never decrease from bottom to top.
     */
    static long solve(int[] heights) {
        long best = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < heights.length; i++) {
            // A strictly shorter current bar closes the taller tops.
            while (!stack.isEmpty() && heights[stack.peek()] > heights[i]) {
                int height = heights[stack.pop()];
                // An empty stack means the banner reaches the left end.
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                best = Math.max(best, (long) height * width);
            }
            stack.push(i);
        }
        return best;
    }

    /** Reference: try every pair of end bars. */
    static long oracle(int[] h) {
        long best = 0;
        for (int l = 0; l < h.length; l++) {
            int low = Integer.MAX_VALUE;
            for (int r = l; r < h.length; r++) {
                low = Math.min(low, h[r]);
                best = Math.max(best, (long) low * (r - l + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {3, 1, 3, 2, 2, 0}) != 6) throw new AssertionError("example 1");
        if (solve(new int[] {2, 5, 6, 3, 0}) != 10) throw new AssertionError("example 2");
        // Random charts that end with zero, with many equal heights, must match the oracle.
        Random rnd = new Random(109);
        for (int t = 0; t < 3000; t++) {
            int[] h = new int[2 + rnd.nextInt(12)];
            for (int i = 0; i < h.length - 1; i++) h[i] = rnd.nextInt(5);
            h[h.length - 1] = 0;
            if (solve(h) != oracle(h)) throw new AssertionError("random");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Flush Increasing Heights (Author exercise)
<!-- id: ms-flush-increasing-heights -->

**Approach.**
A chart without a trailing zero can end while bars are still on the stack. A non-decreasing chart is the extreme case, because no bar is ever shorter than the one before it, and nothing pops during the scan. The loop therefore runs one step further, to `i = n`, and reads a virtual height of 0 there. That height is shorter than every positive bar, so the step pops everything that remains and computes its width against the end of the chart. Bars of height 0 stay on the stack and have area 0. The invariant is the same as in the previous solution.

**Complexity.**
- **Time** is O(n), because each bar is stacked once and removed at most once.
- **Space** is O(n), because a non-decreasing chart keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class FlushIncreasingHeights {
    /**
     * Returns the largest rectangle area, flushing the stack with a virtual zero bar.
     * Time: O(n). Space: O(n).
     * Invariant: stack heights never decrease from bottom to top.
     */
    static long solve(int[] heights, boolean flush) {
        int n = heights.length;
        long best = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        // The extra position n reads height 0 when the flush is on.
        int end = flush ? n : n - 1;
        for (int i = 0; i <= end; i++) {
            int current = i == n ? 0 : heights[i];
            while (!stack.isEmpty() && heights[stack.peek()] > current) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                best = Math.max(best, (long) height * width);
            }
            stack.push(i);
        }
        return best;
    }

    /** Reference: try every pair of end bars. */
    static long oracle(int[] h) {
        long best = 0;
        for (int l = 0; l < h.length; l++) {
            int low = Integer.MAX_VALUE;
            for (int r = l; r < h.length; r++) {
                low = Math.min(low, h[r]);
                best = Math.max(best, (long) low * (r - l + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (solve(new int[] {1, 2, 3, 4, 5}, true) != 9) throw new AssertionError("example 1");
        if (solve(new int[] {2, 2, 2}, true) != 6) throw new AssertionError("example 2");
        // Without the flush, a rising chart reports area 0, which shows why the flush is needed.
        if (solve(new int[] {1, 2, 3}, false) != 0) throw new AssertionError("no flush");
        // Random non-decreasing charts and random charts must match the oracle.
        Random rnd = new Random(113);
        for (int t = 0; t < 3000; t++) {
            int[] h = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < h.length; i++) h[i] = rnd.nextInt(6);
            if (solve(h, true) != oracle(h)) throw new AssertionError(Arrays.toString(h));
            Arrays.sort(h);
            if (solve(h, true) != oracle(h)) throw new AssertionError("sorted " + Arrays.toString(h));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Largest Rectangle in Histogram (LeetCode 84)
<!-- id: ms-largest-rectangle-histogram -->

**Approach.**
The best rectangle has the height of one bar, and for that height it is as wide as possible. The widest banner at bar `i` is bounded by the nearest shorter bar on each side. A stack of indices with non-decreasing heights produces both boundaries, because a pop supplies the right boundary and the bar below supplies the left boundary. A virtual bar of height 0 at position `n` flushes the rest of the stack. The area at the largest scale is `10^4 * 10^5 = 10^9`, which fits in `int`, so the method returns `int`.

**Complexity.**
- **Time** is O(n), because the stack sees each bar once and drops it at most once.
- **Space** is O(n), because a non-decreasing chart keeps every index on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class LargestRectangleHistogram {
    /**
     * Returns the area of the largest rectangle in the histogram.
     * Time: O(n). Space: O(n).
     * Invariant: stack heights never decrease from bottom to top.
     */
    static int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int best = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        // The loop includes position n, which reads height 0 and flushes the stack.
        for (int i = 0; i <= n; i++) {
            int current = i == n ? 0 : heights[i];
            // Every taller top is closed by the current bar.
            while (!stack.isEmpty() && heights[stack.peek()] > current) {
                int height = heights[stack.pop()];
                // The new top is the left boundary, and an empty stack means the left end.
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                best = Math.max(best, height * width);
            }
            stack.push(i);
        }
        return best;
    }

    /** Reference: try every pair of end bars. */
    static int oracle(int[] h) {
        int best = 0;
        for (int l = 0; l < h.length; l++) {
            int low = Integer.MAX_VALUE;
            for (int r = l; r < h.length; r++) {
                low = Math.min(low, h[r]);
                best = Math.max(best, low * (r - l + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (largestRectangleArea(new int[] {6, 2, 5, 4, 5, 1, 6}) != 12) throw new AssertionError("example 1");
        if (largestRectangleArea(new int[] {3, 3, 1, 3, 3, 3}) != 9) throw new AssertionError("example 2");
        // The largest allowed chart stays inside int.
        int[] big = new int[100000];
        Arrays.fill(big, 10000);
        if (largestRectangleArea(big) != 1_000_000_000) throw new AssertionError("big");
        // Random charts, including zeros, must match the oracle.
        Random rnd = new Random(127);
        for (int t = 0; t < 3000; t++) {
            int[] h = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < h.length; i++) h[i] = rnd.nextInt(6);
            if (largestRectangleArea(h) != oracle(h)) throw new AssertionError(Arrays.toString(h));
        }
        System.out.println("ok");
    }
}
```
