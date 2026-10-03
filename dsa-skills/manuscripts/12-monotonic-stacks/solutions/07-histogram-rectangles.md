<!-- solutions-for: 07-histogram-rectangles -->
### Histogram Rectangles

#### Solution: [Build] Rectangle From Supplied Boundaries (Author exercise)
<!-- id: ms-rectangle-supplied-boundaries -->

**Approach.** For each bar, `right - left - 1` is the number of bars strictly between the two shorter bars, and every one of them is at least as tall as the bar, so a rectangle of that width and the bar's height fits. The answer is the largest such product, computed in `long`. The walls must be strictly shorter bars: an equal bar never limits a rectangle. The assertions check the examples, compute the walls by an outward walk on random arrays, and compare the best product with a method that tries every run and uses its shortest bar as the height.

**Complexity.** O(n) time and O(1) extra space once the walls are supplied.

```java run
import java.util.Random;

public final class RectangleSuppliedBoundaries {
    static long best(int[] h, int[] left, int[] right) {
        long best = 0;
        for (int i = 0; i < h.length; i++) best = Math.max(best, (long) h[i] * (right[i] - left[i] - 1));
        return best;
    }
    static long everyRun(int[] h) {
        long best = 0;
        for (int s = 0; s < h.length; s++) {
            int shortest = Integer.MAX_VALUE;
            for (int e = s; e < h.length; e++) {
                shortest = Math.min(shortest, h[e]);
                best = Math.max(best, (long) shortest * (e - s + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (best(new int[]{4, 1, 3, 5, 2, 2}, new int[]{-1, -1, 1, 2, 1, 1}, new int[]{1, 6, 4, 4, 6, 6}) != 8) throw new AssertionError("example 1");
        if (best(new int[]{7}, new int[]{-1}, new int[]{1}) != 7) throw new AssertionError("example 2");
        Random rnd = new Random(1701);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] h = new int[n];
            for (int i = 0; i < n; i++) h[i] = rnd.nextInt(6);
            int[] left = new int[n];
            int[] right = new int[n];
            for (int i = 0; i < n; i++) {
                int l = i - 1;
                while (l >= 0 && !(h[l] < h[i])) l--;
                int r = i + 1;
                while (r < n && !(h[r] < h[i])) r++;
                left[i] = l;
                right[i] = r;
            }
            if (best(h, left, right) != everyRun(h)) throw new AssertionError("disagrees with the every-run method on " + java.util.Arrays.toString(h));
        }
    }
}
```

#### Solution: [Vary] Resolve On A Shorter Bar (Author exercise)
<!-- id: ms-resolve-on-shorter-bar -->

**Approach.** Scan left to right with a stack of indices whose heights never decrease. When a strictly shorter bar arrives, remove each taller top, take the new top as its left wall and the current index as its right wall, and price it with width `j - left - 1`. Equal bars stay on the stack, so for two equal bars the later one is priced first with a narrower width and the earlier one is then priced with the full width. The final zero guarantees that every real bar is removed. The assertions record the priced areas for `[5, 5, 0]` to show the narrower and then the full pricing, check the examples, and compare with the every-run method on random arrays with an appended zero.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class ResolveOnShorterBar {
    static long largest(int[] h, List<Long> priced) {
        long best = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j < h.length; j++) {
            while (!stack.isEmpty() && h[stack.peekLast()] > h[j]) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                long area = (long) h[t] * (j - left - 1);
                if (priced != null) priced.add(area);
                best = Math.max(best, area);
            }
            stack.addLast(j);
        }
        return best;
    }
    static long everyRun(int[] h) {
        long best = 0;
        for (int s = 0; s < h.length; s++) {
            int shortest = Integer.MAX_VALUE;
            for (int e = s; e < h.length; e++) {
                shortest = Math.min(shortest, h[e]);
                best = Math.max(best, (long) shortest * (e - s + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (largest(new int[]{3, 6, 2, 5, 4, 5, 1, 0}, null) != 12) throw new AssertionError("example 1");
        if (largest(new int[]{5, 5, 5, 0}, null) != 15) throw new AssertionError("example 2");
        List<Long> priced = new ArrayList<>();
        largest(new int[]{5, 5, 0}, priced);
        if (!priced.equals(List.of(5L, 10L))) throw new AssertionError("the later equal bar is priced narrower, then the earlier one gets the full width: " + priced);
        Random rnd = new Random(1702);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] h = new int[n + 1];
            for (int i = 0; i < n; i++) h[i] = rnd.nextInt(6);
            h[n] = 0;
            if (largest(h, null) != everyRun(h)) throw new AssertionError("disagrees with the every-run method on " + java.util.Arrays.toString(h));
        }
    }
}
```

#### Solution: [Boundary] Flush Increasing Heights (Author exercise)
<!-- id: ms-flush-increasing-heights -->

**Approach.** Run the loop one step further, to `j = n`, and let `current` be 0 at that step, so the closing zero removes every bar still on the stack. For a strictly increasing row nothing is removed before the end, so without the closing step no bar would ever be priced. Each bar then receives the width from the new top to the end. The assertions show that a loop that stops at `n - 1` returns 0 for `[2, 4, 6]`, check the examples, and compare with the every-run method on increasing and random arrays.

**Complexity.** O(n) time and O(n) extra space, with no copy of the array.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class FlushIncreasingHeights {
    static long largest(int[] h, boolean closingZero) {
        int n = h.length;
        long best = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        int last = closingZero ? n : n - 1;
        for (int j = 0; j <= last; j++) {
            int current = (j == n) ? 0 : h[j];
            while (!stack.isEmpty() && h[stack.peekLast()] > current) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                best = Math.max(best, (long) h[t] * (j - left - 1));
            }
            if (j < n) stack.addLast(j);
        }
        return best;
    }
    static long everyRun(int[] h) {
        long best = 0;
        for (int s = 0; s < h.length; s++) {
            int shortest = Integer.MAX_VALUE;
            for (int e = s; e < h.length; e++) {
                shortest = Math.min(shortest, h[e]);
                best = Math.max(best, (long) shortest * (e - s + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (largest(new int[]{2, 4, 6}, true) != 8) throw new AssertionError("example 1");
        if (largest(new int[]{5}, true) != 5) throw new AssertionError("example 2");
        if (largest(new int[]{2, 4, 6}, false) != 0) throw new AssertionError("without the closing step nothing is priced");
        Random rnd = new Random(1703);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] h = new int[n];
            int value = rnd.nextInt(3);
            for (int i = 0; i < n; i++) { value += rnd.nextInt(3); h[i] = value; }
            if (largest(h, true) != everyRun(h)) throw new AssertionError("disagrees on increasing input " + java.util.Arrays.toString(h));
            for (int i = 0; i < n; i++) h[i] = rnd.nextInt(7);
            if (largest(h, true) != everyRun(h)) throw new AssertionError("disagrees on random input " + java.util.Arrays.toString(h));
        }
    }
}
```

#### Solution: [Recognize] Largest Rectangle in Histogram (LeetCode 84)
<!-- id: ms-largest-rectangle-histogram -->

**Approach.** Combine the two earlier rungs: a stack of indices with non-decreasing heights, pricing each bar with width `j - left - 1` when a strictly shorter bar arrives, and a closing zero at `j = n` that removes every remaining bar. The widest rectangle limited by each bar is considered exactly once, and the best of these is the answer, because any rectangle is limited by its shortest bar and is no wider than that bar's widest run. The assertions check the examples, compare with the every-run method on random arrays including zeros and ties, and run an array of 100,000 bars of height 10,000 to confirm the `long` area.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Random;

public final class LargestRectangleHistogram {
    static long largestRectangleArea(int[] heights) {
        int n = heights.length;
        long best = 0;
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int j = 0; j <= n; j++) {
            int current = (j == n) ? 0 : heights[j];
            while (!stack.isEmpty() && heights[stack.peekLast()] > current) {
                int t = stack.removeLast();
                int left = stack.isEmpty() ? -1 : stack.peekLast();
                best = Math.max(best, (long) heights[t] * (j - left - 1));
            }
            if (j < n) stack.addLast(j);
        }
        return best;
    }
    static long everyRun(int[] h) {
        long best = 0;
        for (int s = 0; s < h.length; s++) {
            int shortest = Integer.MAX_VALUE;
            for (int e = s; e < h.length; e++) {
                shortest = Math.min(shortest, h[e]);
                best = Math.max(best, (long) shortest * (e - s + 1));
            }
        }
        return best;
    }

    public static void main(String[] args) {
        if (largestRectangleArea(new int[]{6, 2, 5, 4, 5, 1, 6}) != 12) throw new AssertionError("example 1");
        if (largestRectangleArea(new int[]{3, 3, 1, 3}) != 6) throw new AssertionError("example 2");
        Random rnd = new Random(1704);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] h = new int[n];
            for (int i = 0; i < n; i++) h[i] = rnd.nextInt(6);
            if (largestRectangleArea(h) != everyRun(h)) throw new AssertionError("disagrees with the every-run method on " + java.util.Arrays.toString(h));
        }
        int[] big = new int[100000];
        java.util.Arrays.fill(big, 10000);
        if (largestRectangleArea(big) != 1_000_000_000L) throw new AssertionError("the area of a full flat histogram needs long");
    }
}
```
