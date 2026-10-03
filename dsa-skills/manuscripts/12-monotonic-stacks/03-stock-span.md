<!-- lesson-kind: standard -->
<!-- lesson-id: stock-span -->
## Stock Span

<!-- stage: context -->
### How Long Has Today Been The Best

A market clerk writes down the closing price of one share every evening in a ledger. At the end of each day a trader asks her a single question: counting today and going back one day at a time, for how many days in a row was the price no higher than today's? The count stops at the first earlier day whose price was higher, or at the first page of the ledger. That count is called the span of today.

The clerk answers each evening, and she cannot know tomorrow's price, so every answer must be ready before the next day begins. Looking back through the pages each evening would take longer as the ledger grows. She starts to keep a short list on a separate card that records, for a few chosen earlier days, a price and how many days that price stretches back over, and she hopes that the card stays short whatever the ledger holds.

<!-- stage: naive -->
### Walk Back Through The Ledger

The direct method answers each day by stepping back from that day until a higher price appears.

```java
static int[] spansByWalkingBack(int[] prices) {
    int n = prices.length;
    int[] span = new int[n];
    for (int i = 0; i < n; i++) {
        int k = i;
        while (k >= 0 && prices[k] <= prices[i]) k--;
        span[i] = i - k;
    }
    return span;
}
```

When the loop stops, `k` is the last day that was strictly higher, or -1, so `i - k` counts today and the days since. For `[40, 30, 35]` it gives `[1, 1, 2]`: the 35 is no lower than the 30 before it, and the walk stops at the 40.

<!-- stage: bottleneck -->
### Rising Prices Re-Walk The Ledger

In a ledger whose prices climb every day, today's price is at least as high as every earlier one, so the walk goes all the way back to the first page. Day `i` takes about `i` steps, and the total is about `n * n / 2`, which is O(n^2). Ten thousand rising days require about fifty million steps for a single pass, and the cost grows with the square of the ledger.

Yesterday's answer already contains the information that today's walk rebuilds. If yesterday's span was 6 and today's price is not lower than yesterday's price, then today's span covers all six of those days without looking at any of them, and the walk only needs to continue from the day just before them. The method steps over days one at a time that a single stored number could have jumped across. It also cannot answer in the order the days arrive without keeping the entire ledger.

<!-- stage: insight -->
### Jump Over Runs Already Counted

The span of day `i` equals `i - p`, where `p` is the **previous greater index**: the nearest earlier day whose price is strictly higher than today's, or -1 if there is none. Everything after `p` up to today is at most today's price, so those days form the run that the span counts. To find `p` quickly, keep a stack of the days that can still be the previous greater index of some future day: candidates whose prices strictly fall from bottom to top. When a new price arrives, every day on top with a price no higher than the new one is removed, because the new day is at least as high and is also later, so none of those days can ever again be the nearest higher day for anyone. The day left on top is `p`.

The stack can store a **span pair** in place of an index: the price of a candidate and the number of days that the candidate's price stretches back over. When the new price pops a pair, it adds that pair's span to its own, and the new pair's span is one plus the sum of the removed spans. Nothing but the pairs is needed, so the method works while prices arrive one at a time and needs no array of history.

Equality needs a decision. A day with an equal price belongs inside today's run, since the question counts days "no higher than today". The scan therefore applies an **equality pop**: it removes the top when the top's price is less than or equal to the new price, so the stack's prices are strictly decreasing and an equal earlier day is absorbed in the span.

<!-- names: previous greater index, span pair, equality pop -->

Each day goes onto the stack one time and comes off at most one time, so a whole stream of `n` prices costs O(n) in total, although a single price may remove many pairs. The cost of one call is amortized constant, not worst-case constant.

<!-- stage: variables -->
### Pairs On The Card

The stack holds pairs of a price and a span. The span of a pair is the number of consecutive days, ending at that pair's day, whose prices are no higher than the pair's price, and the pairs' spans together never overlap: from top to bottom they cover the ledger exactly once, in blocks. While a new price arrives, a running total `span` starts at 1 for today and gains the span of each pair that is popped. After the loop, the pair `(price, span)` is pushed and `span` is returned as the answer for today. In the offline version the same information is carried by an index: the stack holds days, the surviving top is `p`, and the answer is `i - p`, with -1 standing for the position before the first day.

<!-- stage: trace -->
### The Card Over A Week

Take the prices `40, 30, 20, 35, 25, 38, 50`. The first three days are pushed with span 1 each, because each is lower than the day before and nothing is removed. The price 35 on day 3 removes the pair for 20 and the pair for 30, which add 1 and 1 to the starting 1, so the span is 3, and the pair `(35, 3)` is pushed above `(40, 1)`. The price 25 removes nothing, since it is lower than 35, and has span 1. The price 38 removes `(25, 1)` and `(35, 3)`, and the span is 1 plus 1 plus 3, which is 5. The final price 50 removes `(38, 5)` and `(40, 1)` and the span is 7, the whole ledger.

Now take `5, 5, 3, 5`. The second 5 meets an equal price, which is removed by the equality pop, and the span is 2. The 3 is lower, so it has span 1. The last 5 removes the 3 and then the earlier `(5, 2)`, and gets 1 plus 1 plus 2, which is 4. The step to study is the first one, where an equal price is absorbed and not kept as a separate candidate.

```trace
{"cells":[40,30,20,35,25,38,50],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"span":1,"pairs":"[(40,1)]"},"note":"The price 40 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":1},"vars":{"span":1,"pairs":"[(40,1), (30,1)]"},"note":"The price 30 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":2},"vars":{"span":1,"pairs":"[(40,1), (30,1), (20,1)]"},"note":"The price 20 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":3},"vars":{"span":3,"pairs":"[(40,1), (35,3)]"},"note":"The price 35 removes (20,1), (30,1), so the span is 1 plus their spans, which is 3."},{"at":{"i":4},"vars":{"span":1,"pairs":"[(40,1), (35,3), (25,1)]"},"note":"The price 25 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":5},"vars":{"span":5,"pairs":"[(40,1), (38,5)]"},"note":"The price 38 removes (25,1), (35,3), so the span is 1 plus their spans, which is 5."},{"at":{"i":6},"vars":{"span":7,"pairs":"[(50,7)]"},"note":"The price 50 removes (38,5), (40,1), so the span is 1 plus their spans, which is 7."}]}
```

```trace
{"cells":[5,5,3,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"span":1,"pairs":"[(5,1)]"},"note":"The price 5 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":1},"vars":{"span":2,"pairs":"[(5,2)]"},"note":"The price 5 removes (5,1), so the span is 1 plus their spans, which is 2. An equal price is removed as well, because equal days are inside the run."},{"at":{"i":2},"vars":{"span":1,"pairs":"[(5,2), (3,1)]"},"note":"The price 3 is lower than the top, or the stack is empty, so nothing is removed and the span is 1."},{"at":{"i":3},"vars":{"span":4,"pairs":"[(5,4)]"},"note":"The price 5 removes (3,1), (5,2), so the span is 1 plus their spans, which is 4. An equal price is removed as well, because equal days are inside the run."}]}
```

<!-- stage: code -->
### Offline With Indices, Online With Pairs

```java
final class SpanCode {
    static int[] spans(int[] prices) {
        int n = prices.length;
        int[] span = new int[n];
        java.util.ArrayDeque<Integer> stack = new java.util.ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && prices[stack.peekLast()] <= prices[i]) stack.removeLast();
            int previousGreater = stack.isEmpty() ? -1 : stack.peekLast();
            span[i] = i - previousGreater;
            stack.addLast(i);
        }
        return span;
    }

    static final class SpanCard {
        private final java.util.ArrayDeque<int[]> pairs = new java.util.ArrayDeque<>();   // {price, span}

        int next(int price) {
            int span = 1;
            while (!pairs.isEmpty() && pairs.peekLast()[0] <= price) span += pairs.removeLast()[1];
            pairs.addLast(new int[]{price, span});
            return span;
        }
    }
}
```

Both versions remove with `<=`, so the stack's prices are strictly decreasing. The offline method keeps indices and uses the subtraction at the end. The online class keeps only pairs, which is enough because the span of a popped pair is exactly the number of days it covered. The time is O(n) over `n` calls and the space is O(n) in the worst case of falling prices.

<!-- stage: applicability -->
### When The Whole Dominated Run Counts

Use a span stack when each new value must report how long a run of earlier values that it dominates, going back without a gap, and the values arrive in order. The invariant is that the stack holds strictly decreasing candidates, each paired with the number of days it already summarizes, so that the stored spans tile the ledger. Decide the equality rule from the sentence of the problem: "no higher than" removes equal prices, and "strictly lower than" would keep them.

The false friend is the next-greater problem of the first lesson. That one looks forward and asks for the position of one later value, so the answer is read at the moment of a pop. The span looks backward and asks for the size of a whole run, so the answer is read after the pops, from the survivor or from the accumulated spans. A second false friend is counting the days with a lower price anywhere in the past, which ignores the requirement that the run be unbroken, and for `[10, 50, 20, 30]` the span of the last day is 2, although three days in the whole history, the 10, the 20 and the 30, had a price at most 30.

Do not use the pattern when the question concerns a fixed-length window of recent days, because a stack of dominated candidates has no way to forget the oldest day by age. That is the territory of a different structure in a later chapter. Keep the integer type in mind as well, since the span is at most the number of calls and fits in `int` for the stated limits.

<!-- stage: exercises -->
### Exercises

#### [Build] Span From Previous-Greater Index (Author exercise)
<!-- id: ms-span-from-previous-greater -->

**Prerequisites.** The two previous lessons in this chapter.

**Problem.** Given an array `prices` that is fully known in advance, return an array `span` where `span[i]` is `i - p`. Here `p` is the largest index `p < i` with `prices[p] > prices[i]`, and `p = -1` when no such index exists.

**Constraints.** 1 <= prices.length <= 10^5 and 1 <= prices[i] <= 10^9. Use one pass and keep indices on the stack.

**Example 1.** Input `prices = [40, 30, 20, 35, 25, 38, 50]`, output `[1, 1, 1, 3, 1, 5, 7]`.

**Example 2.** Input `prices = [9, 8, 7]`, output `[1, 1, 1]`, since every day is lower than the day before.

**Hint.** What does the surviving top of the stack mean after the removals? What value should the subtraction use when the stack becomes empty?

**Changed decision.** First rung: the answer is read after the pops, from the survivor, and not at the moment of a pop.

#### [Vary] Compressed Price-Span Pairs (Author exercise)
<!-- id: ms-compressed-price-span-pairs -->

**Prerequisites.** The Span From Previous-Greater Index exercise above.

**Problem.** Given the same kind of array of prices, return the array of spans again, but process each price exactly once in order, without looking back into the input array. Keep only pairs of a price and the number of days that price summarizes.

**Constraints.** 1 <= prices.length <= 10^5 and 1 <= prices[i] <= 10^9. The only state allowed between prices is the stack of pairs.

**Example 1.** Input `prices = [90, 80, 85, 85, 70, 95]`, output `[1, 1, 2, 3, 1, 6]`.

**Example 2.** Input `prices = [20, 30, 40]`, output `[1, 2, 3]`, so a rising ledger makes each pair swallow the one before it.

**Hint.** When a pair is removed, what number does it carry that the new day needs? Why is the stack still enough to answer the next day?

**Changed decision.** The stack stores spans in place of indices, so the method needs no history and works in streaming order.

#### [Boundary] Equal Prices (Author exercise)
<!-- id: ms-equal-prices-span -->

**Prerequisites.** The two exercises above.

**Problem.** Compute the spans for arrays that contain repeated prices, where the span of a day counts consecutive days, ending today, whose price is at most today's. Check that a run of equal prices counts every one of its days.

**Constraints.** 1 <= prices.length <= 10^5 and 1 <= prices[i] <= 10^9, with long runs of equal values allowed. Linear time.

**Example 1.** Input `prices = [5, 5, 3, 5]`, output `[1, 2, 1, 4]`.

**Example 2.** Input `prices = [7, 7, 7]`, output `[1, 2, 3]`.

**Hint.** What happens to the span of the third 7 if the removal condition uses `<` in place of `<=`? Which test in the examples would show it?

**Changed decision.** The removal test includes equality, so an equal earlier day is absorbed into today's run.

#### [Recognize] Online Stock Span (LeetCode 901)
<!-- id: ms-online-stock-span -->

**Prerequisites.** All three exercises above.

**Problem.** Design a class `StockSpanner` with a method `next(price)` that is called once per day with that day's price and returns the span of that day, meaning the number of consecutive days up to and including today whose price is less than or equal to today's price. Calls arrive in order and the future prices are not known.

**Constraints.** 1 <= price <= 10^5 and at most 10^5 calls. The total time for all calls should be linear.

**Example 1.** Input `calls = next(31), next(28), next(28), next(29), next(35), next(26)`, output `[1, 1, 2, 3, 5, 1]`.

**Example 2.** Input `calls = next(12), next(12), next(9), next(15), next(15), next(14)`, output `[1, 2, 1, 4, 5, 1]`.

**Hint.** What must survive between calls, and what can be thrown away once a day has been absorbed by a higher price?

**Changed decision.** The structure must live across calls, so the stack of pairs becomes a field and the amortized cost is the one that counts.
