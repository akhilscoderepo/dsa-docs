<!-- solutions-for: 12-monotonic-stacks -->
### Solutions For The Stock Span

#### Solution: [Build] Span From Previous-Greater Index (Author exercise)
<!-- id: ms-span-from-previous-greater -->

**Approach.**
The span of day `i` equals `i - p`, where `p` is the nearest earlier day with a strictly higher price. The stack holds the days that can still be such a boundary, and their prices strictly decrease from bottom to top. A new price pops every top that is lower, because those days can never be a boundary for it or for any later day. The top that remains is `p`, and an empty stack means `p = -1`. The prices are distinct, so the comparison never meets a tie.

**Complexity.**
- **Time** is O(n), because the loop pushes each day once and pops it at most once.
- **Space** is O(n), because a decreasing feed keeps every day on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

public final class SpanFromBoundary {
    /**
     * Returns i minus the previous greater index for every day.
     * Time: O(n). Space: O(n).
     * Invariant: stack prices strictly decrease from bottom to top.
     */
    static int[] solve(int[] prices) {
        int[] span = new int[prices.length];
        Deque<Integer> stack = new ArrayDeque<>();
        // One left-to-right pass handles each day once.
        for (int i = 0; i < prices.length; i++) {
            // Lower tops can never be the boundary again, so they leave.
            while (!stack.isEmpty() && prices[stack.peek()] < prices[i]) stack.pop();
            // The surviving top is the previous greater index, or -1 when empty.
            int boundary = stack.isEmpty() ? -1 : stack.peek();
            span[i] = i - boundary;
            // The current day can be the boundary of later days.
            stack.push(i);
        }
        return span;
    }

    /** Reference: walk left from every day until a greater price appears. */
    static int[] oracle(int[] prices) {
        int[] r = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int p = i - 1;
            while (p >= 0 && prices[p] < prices[i]) p--;
            r[i] = i - p;
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {30, 25, 20, 22, 28, 40, 10}), new int[] {1, 1, 1, 2, 4, 6, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {1, 2, 3, 4}), new int[] {1, 2, 3, 4})) throw new AssertionError("example 2");
        // Random arrays of distinct values must match the oracle.
        Random rnd = new Random(37);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            Set<Integer> seen = new HashSet<>();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                int v;
                do { v = rnd.nextInt(40); } while (!seen.add(v));
                a[i] = v;
            }
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Compressed Price-Span Pairs (Author exercise)
<!-- id: ms-compressed-price-span-pairs -->

**Approach.**
Each stack entry is a pair of a price and the number of consecutive days it summarizes, ending at the day that created it. A new price starts with a span of 1 and pops every pair whose price is at most the new price. Each popped pair covers days whose prices are at most the popped price, so they are at most the new price too. The new span adds the popped spans. The pair with the new price and the new span goes on top. The prices strictly decrease from bottom to top, and the spans on the stack always add up to the number of days read.

**Complexity.**
- **Time** is O(n), because the loop pushes each pair once and pops it at most once.
- **Space** is O(n), because a strictly decreasing input keeps a pair for every day.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class CompressedPairs {
    /**
     * Returns the stack of {price, span} pairs after all prices, bottom to top.
     * Time: O(n). Space: O(n).
     * Invariant: prices strictly decrease upward, and the spans sum to the days read.
     */
    static int[][] solve(int[] prices) {
        Deque<int[]> pairs = new ArrayDeque<>();
        // Each price arrives once, as in an online feed.
        for (int price : prices) {
            int span = 1;
            // Pairs at most the new price merge into the new span.
            while (!pairs.isEmpty() && pairs.peek()[0] <= price) span += pairs.pop()[1];
            pairs.push(new int[] {price, span});
        }
        // The deque iterates from top to bottom, so the copy fills from the end.
        int[][] out = new int[pairs.size()][];
        int k = out.length - 1;
        for (int[] p : pairs) out[k--] = p;
        return out;
    }

    /** Reference: compute the span of each day by walking left, then group days by boundary. */
    static int[][] oracle(int[] prices) {
        int n = prices.length;
        // A day stays on the stack when no later day has a price at least as high.
        java.util.List<int[]> kept = new java.util.ArrayList<>();
        for (int i = n - 1; i >= 0; i--) {
            boolean beaten = false;
            for (int j = i + 1; j < n; j++) if (prices[j] >= prices[i]) beaten = true;
            if (beaten) continue;
            int p = i - 1;
            while (p >= 0 && prices[p] <= prices[i]) p--;
            kept.add(0, new int[] {prices[i], i - p});
        }
        return kept.toArray(new int[0][]);
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.deepEquals(solve(new int[] {4, 9, 7, 7, 2, 2}), new int[][] {{9, 2}, {7, 2}, {2, 2}})) throw new AssertionError("example 1");
        if (!Arrays.deepEquals(solve(new int[] {5, 3, 4, 4, 2, 6}), new int[][] {{6, 6}})) throw new AssertionError("example 2");
        // Random arrays must match the oracle, and the spans must sum to n.
        Random rnd = new Random(41);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            int[][] got = solve(a);
            if (!Arrays.deepEquals(got, oracle(a))) throw new AssertionError(Arrays.toString(a));
            int sum = 0;
            for (int[] p : got) sum += p[1];
            if (sum != a.length) throw new AssertionError("span sum");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Equal Prices (Author exercise)
<!-- id: ms-equal-prices -->

**Approach.**
The span counts earlier days whose price is at most today's price, so an equal earlier price belongs inside the span. The stack therefore pops with the non-strict comparison `<=`, and the surviving top is the nearest earlier day with a strictly higher price. With a strict pop, an equal earlier day would stay on the stack and cut the span short. After the pops, the span is `i` minus the surviving top, or `i + 1` for an empty stack. An all-equal array pops the previous day each time, so the stack never holds more than one entry and the spans grow by one.

**Complexity.**
- **Time** is O(n), because the loop pushes each day once and pops it at most once.
- **Space** is O(n), because a strictly decreasing array keeps every day on the stack.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class EqualPriceSpan {
    /**
     * Returns the span with ties inside it for every day.
     * Time: O(n). Space: O(n).
     * Invariant: stack prices strictly decrease from bottom to top.
     */
    static int[] solve(int[] prices) {
        int[] span = new int[prices.length];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < prices.length; i++) {
            // The non-strict comparison pops equal earlier days into the span.
            while (!stack.isEmpty() && prices[stack.peek()] <= prices[i]) stack.pop();
            // An empty stack means every earlier day is inside the span.
            span[i] = stack.isEmpty() ? i + 1 : i - stack.peek();
            stack.push(i);
        }
        return span;
    }

    /** Reference: walk left while the earlier price is at most the current one. */
    static int[] oracle(int[] prices) {
        int[] r = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int c = 1;
            for (int j = i - 1; j >= 0 && prices[j] <= prices[i]; j--) c++;
            r[i] = c;
        }
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(solve(new int[] {7, 7, 7, 7}), new int[] {1, 2, 3, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(solve(new int[] {5, 3, 4, 4, 2, 6}), new int[] {1, 1, 2, 3, 1, 6})) throw new AssertionError("example 2");
        // Random arrays with heavy repetition must match the oracle.
        Random rnd = new Random(43);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3);
            if (!Arrays.equals(solve(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Online Stock Span (LeetCode 901)
<!-- id: ms-online-stock-span -->

**Approach.**
The class never sees later prices and keeps no price array, so each stack entry must carry its own run length. The entry is a pair of a price and a span. A call to `next` starts the span at 1, pops every pair with a price at most the new price, and adds each popped span. It pushes the new pair and returns the span. The prices on the stack strictly decrease from bottom to top, so the pops stop at the first pair with a higher price.

**Complexity.**
- **Time** is O(1) amortized per call, because all calls together push each pair once and pop it at most once.
- **Space** is O(n) for n calls, reached when the prices strictly decrease.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Deque;
import java.util.Random;

public final class OnlineStockSpan {
    /** Online span tracker. Time: O(1) amortized per call. Space: O(n). */
    static final class StockSpanner {
        // Each pair is {price, span}, and prices strictly decrease upward.
        private final Deque<int[]> pairs = new ArrayDeque<>();

        int next(int price) {
            int span = 1;
            // Pairs at most the new price merge into the new span.
            while (!pairs.isEmpty() && pairs.peek()[0] <= price) span += pairs.pop()[1];
            pairs.push(new int[] {price, span});
            return span;
        }
    }

    /** Reference: keep every price and walk left on each call. */
    static int[] oracle(int[] prices) {
        int[] r = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int c = 1;
            for (int j = i - 1; j >= 0 && prices[j] <= prices[i]; j--) c++;
            r[i] = c;
        }
        return r;
    }

    static int[] feed(int[] prices) {
        StockSpanner s = new StockSpanner();
        int[] r = new int[prices.length];
        for (int i = 0; i < prices.length; i++) r[i] = s.next(prices[i]);
        return r;
    }

    public static void main(String[] args) {
        // Example 1 and Example 2 from the exercise text.
        if (!Arrays.equals(feed(new int[] {31, 41, 41, 59, 26, 53}), new int[] {1, 2, 3, 4, 1, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(feed(new int[] {9, 9, 10, 8, 8, 8}), new int[] {1, 2, 3, 1, 2, 3})) throw new AssertionError("example 2");
        // Random call sequences must match the oracle.
        Random rnd = new Random(47);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(14)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(6);
            if (!Arrays.equals(feed(a), oracle(a))) throw new AssertionError(Arrays.toString(a));
        }
        System.out.println("ok");
    }
}
```
