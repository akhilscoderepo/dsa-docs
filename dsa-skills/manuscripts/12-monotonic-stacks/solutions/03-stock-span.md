<!-- solutions-for: 03-stock-span -->
### Stock Span

#### Solution: [Build] Span From Previous-Greater Index (Author exercise)
<!-- id: ms-span-from-previous-greater -->

**Approach.** For each day, remove from the stack every day whose price is at most today's. What remains on top, if anything, is the nearest earlier day with a strictly higher price, which is the previous greater index `p`, and the span is `i - p`, with `p = -1` for an empty stack. The answer is read after the removals, not during them. The assertions check both examples, compare with the walk-back method on random arrays, and confirm that the stack's prices are strictly decreasing from bottom to top after every day.

**Complexity.** O(n) time, since each day is pushed once and removed at most once, and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class SpanFromPreviousGreater {
    static int[] spans(int[] prices) {
        int n = prices.length;
        int[] span = new int[n];
        ArrayDeque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && prices[stack.peekLast()] <= prices[i]) stack.removeLast();
            int previousGreater = stack.isEmpty() ? -1 : stack.peekLast();
            span[i] = i - previousGreater;
            stack.addLast(i);
            int prev = Integer.MAX_VALUE;
            for (int idx : stack) {
                if (prices[idx] >= prev) throw new AssertionError("stack prices must strictly decrease");
                prev = prices[idx];
            }
        }
        return span;
    }
    static int[] oracle(int[] prices) {
        int[] span = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int k = i;
            while (k >= 0 && prices[k] <= prices[i]) k--;
            span[i] = i - k;
        }
        return span;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(spans(new int[]{40, 30, 20, 35, 25, 38, 50}), new int[]{1, 1, 1, 3, 1, 5, 7})) throw new AssertionError("example 1");
        if (!Arrays.equals(spans(new int[]{9, 8, 7}), new int[]{1, 1, 1})) throw new AssertionError("example 2");
        if (spans(new int[]{10, 50, 20, 30})[3] != 2) throw new AssertionError("an unbroken run, not the count of lower days anywhere");
        Random rnd = new Random(1301);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(9);
            if (!Arrays.equals(spans(a), oracle(a))) throw new AssertionError("disagrees with the walk-back method on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Vary] Compressed Price-Span Pairs (Author exercise)
<!-- id: ms-compressed-price-span-pairs -->

**Approach.** Store a pair of a price and a span on the stack. A new price starts with span 1, removes each pair whose price is at most its own, and adds the removed spans. Then it pushes its own pair. A pair's span is exactly the number of days it covers, so no index and no input array is read after a price has been processed. The assertions check the examples, compare with the walk-back method, and check the tiling invariant from the lesson: after every day, the spans on the stack add up to the number of days seen so far.

**Complexity.** O(n) time in total and O(n) extra space in the worst case of falling prices.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class CompressedPairs {
    static int[] spans(int[] prices) {
        int[] out = new int[prices.length];
        ArrayDeque<int[]> pairs = new ArrayDeque<>();
        for (int i = 0; i < prices.length; i++) {
            int span = 1;
            while (!pairs.isEmpty() && pairs.peekLast()[0] <= prices[i]) span += pairs.removeLast()[1];
            pairs.addLast(new int[]{prices[i], span});
            out[i] = span;
            int total = 0;
            for (int[] pr : pairs) total += pr[1];
            if (total != i + 1) throw new AssertionError("stored spans must tile the days seen so far");
        }
        return out;
    }
    static int[] oracle(int[] prices) {
        int[] span = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int k = i;
            while (k >= 0 && prices[k] <= prices[i]) k--;
            span[i] = i - k;
        }
        return span;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(spans(new int[]{90, 80, 85, 85, 70, 95}), new int[]{1, 1, 2, 3, 1, 6})) throw new AssertionError("example 1");
        if (!Arrays.equals(spans(new int[]{20, 30, 40}), new int[]{1, 2, 3})) throw new AssertionError("example 2");
        Random rnd = new Random(1302);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(7);
            if (!Arrays.equals(spans(a), oracle(a))) throw new AssertionError("disagrees with the walk-back method on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Boundary] Equal Prices (Author exercise)
<!-- id: ms-equal-prices-span -->

**Approach.** Remove pairs whose price is less than or equal to today's, so a day with an equal price is absorbed into today's run. With a strict `<` instead, the equal earlier day would stay on the stack and would end the run, and the span would be too short. The assertions run both versions on the examples to show the difference, then check the correct version against the walk-back method on arrays drawn from two or three distinct values, and check that an all-equal array of length `n` gives spans `1..n`.

**Complexity.** O(n) time and O(n) extra space.

```java run
import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Random;

public final class EqualPricesSpan {
    static int[] spans(int[] prices, boolean absorbEqual) {
        int[] out = new int[prices.length];
        ArrayDeque<int[]> pairs = new ArrayDeque<>();
        for (int i = 0; i < prices.length; i++) {
            int span = 1;
            while (!pairs.isEmpty() && (absorbEqual ? pairs.peekLast()[0] <= prices[i] : pairs.peekLast()[0] < prices[i])) span += pairs.removeLast()[1];
            pairs.addLast(new int[]{prices[i], span});
            out[i] = span;
        }
        return out;
    }
    static int[] oracle(int[] prices) {
        int[] span = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int k = i;
            while (k >= 0 && prices[k] <= prices[i]) k--;
            span[i] = i - k;
        }
        return span;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(spans(new int[]{5, 5, 3, 5}, true), new int[]{1, 2, 1, 4})) throw new AssertionError("example 1");
        if (!Arrays.equals(spans(new int[]{7, 7, 7}, true), new int[]{1, 2, 3})) throw new AssertionError("example 2");
        if (!Arrays.equals(spans(new int[]{7, 7, 7}, false), new int[]{1, 1, 1})) throw new AssertionError("a strict removal test keeps equal days apart");
        int[] same = new int[9];
        Arrays.fill(same, 4);
        int[] expected = new int[9];
        for (int i = 0; i < 9; i++) expected[i] = i + 1;
        if (!Arrays.equals(spans(same, true), expected)) throw new AssertionError("an all-equal array has spans 1 to n");
        Random rnd = new Random(1303);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = 1 + rnd.nextInt(3);
            if (!Arrays.equals(spans(a, true), oracle(a))) throw new AssertionError("disagrees with the walk-back method on " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Online Stock Span (LeetCode 901)
<!-- id: ms-online-stock-span -->

**Approach.** Keep the stack of price and span pairs as a field of the class. Each call to `next` removes the pairs whose price is at most the new price, accumulates their spans, pushes the new pair and returns the accumulated span. Nothing about future prices is needed. The assertions replay both example call sequences, compare random call sequences with a method that keeps the full history and walks back, and count removals over a long sequence to confirm that the total number of removals never exceeds the number of calls, which is the amortized claim.

**Complexity.** Amortized O(1) per call and O(n) total space for `n` calls, although a single call can remove many pairs.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Random;

public final class OnlineStockSpan {
    static final class StockSpanner {
        private final ArrayDeque<int[]> pairs = new ArrayDeque<>();
        long removals;
        int next(int price) {
            int span = 1;
            while (!pairs.isEmpty() && pairs.peekLast()[0] <= price) { span += pairs.removeLast()[1]; removals++; }
            pairs.addLast(new int[]{price, span});
            return span;
        }
    }
    static final class Historian {
        private final ArrayList<Integer> history = new ArrayList<>();
        int next(int price) {
            history.add(price);
            int k = history.size() - 1;
            while (k >= 0 && history.get(k) <= price) k--;
            return history.size() - 1 - k;
        }
    }

    public static void main(String[] args) {
        int[] calls1 = {31, 28, 28, 29, 35, 26};
        int[] want1 = {1, 1, 2, 3, 5, 1};
        StockSpanner a = new StockSpanner();
        for (int i = 0; i < calls1.length; i++) if (a.next(calls1[i]) != want1[i]) throw new AssertionError("example 1 at call " + i);
        int[] calls2 = {12, 12, 9, 15, 15, 14};
        int[] want2 = {1, 2, 1, 4, 5, 1};
        StockSpanner b = new StockSpanner();
        for (int i = 0; i < calls2.length; i++) if (b.next(calls2[i]) != want2[i]) throw new AssertionError("example 2 at call " + i);
        Random rnd = new Random(1304);
        for (int t = 0; t < 1500; t++) {
            StockSpanner fast = new StockSpanner();
            Historian slow = new Historian();
            int n = 1 + rnd.nextInt(30);
            for (int i = 0; i < n; i++) {
                int price = 1 + rnd.nextInt(8);
                if (fast.next(price) != slow.next(price)) throw new AssertionError("disagrees with the historian at call " + i);
            }
            if (fast.removals > n) throw new AssertionError("removals can never exceed the number of calls");
        }
        StockSpanner big = new StockSpanner();
        for (int i = 1; i <= 100000; i++) big.next(i % 1000 + 1);
        if (big.removals > 100000) throw new AssertionError("amortized removals stay linear in the number of calls");
    }
}
```
