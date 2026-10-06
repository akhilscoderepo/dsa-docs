<!-- lesson-kind: standard -->
<!-- lesson-id: stock-span -->
## Compute The Stock Span

<!-- stage: context -->
### Each New Price Needs A Span

A trading dashboard receives one closing price per day. Beside each price it shows the span of that day. The **span** is the number of consecutive days, counting today and moving backward, whose price is at most today's price. If the last three prices are 22, 22 and 28, the span of the 28 includes both 22 days and any earlier days that stay at or below 28.

The dashboard recomputes the span for every new price, and the feed holds 100000 days. The lesson answers one question. How can each new price get its span without reading the whole past again?

<!-- stage: naive -->
### Walk Back While Prices Stay Low

The direct approach starts at day `i` and walks backward while the earlier price is at most the price of day `i`. The span is the number of days that the walk covers, including day `i` itself.

```java
static int[] spansByWalking(int[] prices) {
    int[] span = new int[prices.length];
    for (int i = 0; i < prices.length; i++) {
        int count = 1;
        for (int j = i - 1; j >= 0 && prices[j] <= prices[i]; j--) {
            count++;
        }
        span[i] = count;
    }
    return span;
}
```

For the prices 30, 25, 20, 22, the walk for the 22 covers the 20 and stops at the 25, so the span is 2. The method is correct for a day with a nearby larger price.

<!-- stage: bottleneck -->
### A Rising Feed Rereads Everything

```predict
The prices rise every day, such as 1, 2, 3 and so on up to 100000. About how many earlier days do all the walks read in total?

About 5 x 10^9. The walk for day i never meets a larger price, so it reads all i earlier days. The sum of i over 100000 days is about 100000 x 99999 / 2.
```

The worst case is O(n^2) for `n` days. A rising feed makes every walk run to day 0. The reads also repeat. The walk for day 10 passes over days that the walk for day 9 already crossed, and it learns again that they are low.

The earlier walks already know something useful. Suppose day 9 covers a run of 6 days, and day 10 is at least as high as day 9. Then the walk for day 10 can skip that whole run in one step. The next section shows what the program must remember to make that jump.

<!-- stage: insight -->
### Skip A Whole Run In One Step

The span stops at the nearest earlier day with a strictly higher price. If the program finds that day directly, it does not need to read the days between.

<!-- names: previous greater index, price-span pair -->

#### The Span Is A Distance To A Boundary

The **previous greater index** of day `i` is the largest index `j < i` with `prices[j] > prices[i]`, or `-1` when no such day exists. Every day between `j` and `i` has a price at most `prices[i]`, so the span equals `i - j`. The task reduces to finding the previous greater index of every day.

A stack of indices finds it from left to right. The stack holds the days that can still be the previous greater index of a future day. When a new price arrives, every top with a price at most the new price can never be a boundary again. The new day is at least as high and sits closer to the future. The scan pops those tops. The top that survives has a strictly greater price, and it is the previous greater index. The prices on the stack strictly decrease from bottom to top. The comparison pops equal prices, because an equal earlier day belongs to the span.

#### A Pair Stores A Summarized Run

Some interfaces give the program only the price and never an index. A **price-span pair** stores a price together with the span that the entry already summarizes. When a new price pops a pair, the days in that pair's run are all at most the pair's price, so they are at most the new price too. The new span is therefore one plus the sum of the popped spans. Each pair stands for a run of days, so a pop can skip many days at once.

<!-- stage: variables -->
### What The Scan Remembers

The scan tracks four pieces of state.

- **prices** is the input sequence, and each new price arrives once.
- **stack** holds candidate boundary days, with prices that strictly decrease from bottom to top.
- **span** is the answer for the current day, counting the day itself.
- **pair** is one stack entry in the online version, holding a price and the days it summarizes.

In the index version, `span` equals `i` minus the index left on top. In the pair version, `span` equals one plus the spans of the popped pairs.

<!-- stage: trace -->
### Following Two Versions Of The Stack

#### Boundaries By Index

The first trace reads 30, 25, 20, 22, 22, 28, 40, 10. The stack lists day indices. A price pops every earlier day with a price at most its own. The span is the current index minus the top that survives, or `i + 1` when the stack becomes empty.

The 22 at index 3 pops the 20 and stops at the 25, so its span is 2. The next 22 pops the equal 22 at index 3 and stops at the 25, so its span is 3. The 28 pops both 22 days and the 25, then stops at the 30, so its span is 5.

```trace
{"cells":[30,25,20,22,22,28,40,10],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"stack":"[0]","span":1},"note":"The boundary is -1, so the span is 0 - (-1) = 1, and index 0 goes on the stack."},{"at":{"i":1},"vars":{"stack":"[0, 1]","span":1},"note":"The boundary is 0, so the span is 1 - (0) = 1, and index 1 goes on the stack."},{"at":{"i":2},"vars":{"stack":"[0, 1, 2]","span":1},"note":"The boundary is 1, so the span is 2 - (1) = 1, and index 2 goes on the stack."},{"at":{"i":3},"vars":{"stack":"[0, 1]","span":"-"},"note":"Price 22 is at least prices[2] = 20, so index 2 leaves the stack."},{"at":{"i":3},"vars":{"stack":"[0, 1, 3]","span":2},"note":"The boundary is 1, so the span is 3 - (1) = 2, and index 3 goes on the stack."},{"at":{"i":4},"vars":{"stack":"[0, 1]","span":"-"},"note":"Price 22 is at least prices[3] = 22, so index 3 leaves the stack."},{"at":{"i":4},"vars":{"stack":"[0, 1, 4]","span":3},"note":"The boundary is 1, so the span is 4 - (1) = 3, and index 4 goes on the stack."},{"at":{"i":5},"vars":{"stack":"[0, 1]","span":"-"},"note":"Price 28 is at least prices[4] = 22, so index 4 leaves the stack."},{"at":{"i":5},"vars":{"stack":"[0]","span":"-"},"note":"Price 28 is at least prices[1] = 25, so index 1 leaves the stack."},{"at":{"i":5},"vars":{"stack":"[0, 5]","span":5},"note":"The boundary is 0, so the span is 5 - (0) = 5, and index 5 goes on the stack."},{"at":{"i":6},"vars":{"stack":"[0]","span":"-"},"note":"Price 40 is at least prices[5] = 28, so index 5 leaves the stack."},{"at":{"i":6},"vars":{"stack":"[]","span":"-"},"note":"Price 40 is at least prices[0] = 30, so index 0 leaves the stack."},{"at":{"i":6},"vars":{"stack":"[6]","span":7},"note":"The boundary is -1, so the span is 6 - (-1) = 7, and index 6 goes on the stack."},{"at":{"i":7},"vars":{"stack":"[6, 7]","span":1},"note":"The boundary is 6, so the span is 7 - (6) = 1, and index 7 goes on the stack."}]}
```

#### Pairs Of Price And Span

The second trace reads 8, 6, 5, 6, 6, 9, 3 and stores pairs written as price/span. The 6 at index 3 pops the pair 5/1 and the pair 6/1, so its span is 1 + 1 + 1 = 3. The next 6 pops the pair 6/3, so its span is 1 + 3 = 4. The 9 pops 6/4 and 8/1, and its span is 6.

```trace
{"cells":[8,6,5,6,6,9,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"pairs":"[8/1]","span":1},"note":"The span of price 8 is 1, and the pair 8/1 goes on the stack."},{"at":{"i":1},"vars":{"pairs":"[8/1, 6/1]","span":1},"note":"The span of price 6 is 1, and the pair 6/1 goes on the stack."},{"at":{"i":2},"vars":{"pairs":"[8/1, 6/1, 5/1]","span":1},"note":"The span of price 5 is 1, and the pair 5/1 goes on the stack."},{"at":{"i":3},"vars":{"pairs":"[8/1, 6/1]","span":2},"note":"Price 6 is at least 5, so the pair 5/1 leaves and its 1 day join the span."},{"at":{"i":3},"vars":{"pairs":"[8/1]","span":3},"note":"Price 6 is at least 6, so the pair 6/1 leaves and its 1 day join the span."},{"at":{"i":3},"vars":{"pairs":"[8/1, 6/3]","span":3},"note":"The span of price 6 is 3, and the pair 6/3 goes on the stack."},{"at":{"i":4},"vars":{"pairs":"[8/1]","span":4},"note":"Price 6 is at least 6, so the pair 6/3 leaves and its 3 days join the span."},{"at":{"i":4},"vars":{"pairs":"[8/1, 6/4]","span":4},"note":"The span of price 6 is 4, and the pair 6/4 goes on the stack."},{"at":{"i":5},"vars":{"pairs":"[8/1]","span":5},"note":"Price 9 is at least 6, so the pair 6/4 leaves and its 4 days join the span."},{"at":{"i":5},"vars":{"pairs":"[]","span":6},"note":"Price 9 is at least 8, so the pair 8/1 leaves and its 1 day join the span."},{"at":{"i":5},"vars":{"pairs":"[9/6]","span":6},"note":"The span of price 9 is 6, and the pair 9/6 goes on the stack."},{"at":{"i":6},"vars":{"pairs":"[9/6, 3/1]","span":1},"note":"The span of price 3 is 1, and the pair 3/1 goes on the stack."}]}
```

<!-- stage: code -->
### The Stack In Two Java Shapes

#### One Pass Over An Array

The first method keeps indices on a stack and subtracts the surviving top. An empty stack means no greater earlier day exists, so the boundary is `-1`.

```java
static int[] spans(int[] prices) {
    int[] span = new int[prices.length];
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < prices.length; i++) {
        while (!stack.isEmpty() && prices[stack.peek()] <= prices[i]) {
            stack.pop();
        }
        int boundary = stack.isEmpty() ? -1 : stack.peek();
        span[i] = i - boundary;
        stack.push(i);
    }
    return span;
}
```

#### One Call Per Price

The second class receives one price at a time. Each stack entry is an `int[]` pair with the price at position 0 and the span at position 1.

```java
final class SpanTracker {
    private final Deque<int[]> pairs = new ArrayDeque<>();

    int next(int price) {
        int span = 1;
        while (!pairs.isEmpty() && pairs.peek()[0] <= price) {
            span += pairs.pop()[1];
        }
        pairs.push(new int[] {price, span});
        return span;
    }
}
```

Both versions run in O(n) total time. The scan pushes each day or pair once and pops it at most once. A single call can cost O(n), so the bound is amortized across all calls. The extra space is O(n) in the worst case, which a strictly decreasing feed reaches.

<!-- stage: applicability -->
### When Spans Replace Walks

#### The Cue For A Span

The cue is a count of consecutive earlier items that stay at or below the current one. The invariant is that the stack holds the days that can still be a boundary, and their prices strictly decrease from bottom to top. A popped day can never be a boundary again, because the current day is at least as high and closer. The scan covers one direction only, and a stream that delivers one price at a time fits it.

#### Two False Friends

Counting the pops is the first false friend. A pair can summarize many days, so the span equals one plus the sum of the popped spans, and the number of pops would undercount. On the feed 8, 6, 5, 6, 6, the last price pops one pair and has a span of 4.

The strict comparison from the previous lesson is the second false friend. There a tie stayed on the stack. Here a tie pops, because a day with an equal price still counts inside the span.

#### When It Does Not Apply

A span that must also look forward in time needs the boundary on both sides, and one left-to-right pass reveals only the left side. A later lesson shows how both sides combine. A span over a sliding window of fixed length also needs removal from the old end, which a plain stack cannot do.

<!-- stage: exercises -->
### Exercises

#### [Build] Span From Previous-Greater Index (Author exercise)
<!-- id: ms-span-from-previous-greater -->

**Prerequisites.** The index version in this lesson.

**Problem.** Let `prices` be an array of distinct integers. For each index `i`, let `p` be the largest index `p < i` with `prices[p] > prices[i]`, or `-1` when none exists. Return an array whose entry `i` equals `i - p`.

**Constraints.** The limits are:
- **Length** is `1 <= prices.length <= 10^5`.
- **Values** are distinct `int` values, so no two days have an equal price.
- **Boundary** `-1` means that every earlier day is lower.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[30,25,20,22,28,40,10]`, output `[1,1,1,2,4,6,1]`.

**Example 2.** Input `[1,2,3,4]`, output `[1,2,3,4]`.

**Hint.** Pop while the top price is lower than the new price. Which index remains on top after the pops?

**Changed decision.** The answer is a distance to a boundary index, not a value.

#### [Vary] Compressed Price-Span Pairs (Author exercise)
<!-- id: ms-compressed-price-span-pairs -->

**Prerequisites.** The exercise above and the pair version in this lesson.

**Problem.** Process the prices in order with a stack of price-span pairs. For each price, pop every pair whose price is at most the new price, and add the popped spans to a span that starts at 1. Push the new pair. After the last price, return the stack from bottom to top as an array of `{price, span}` pairs.

**Constraints.** The limits are:
- **Length** is `1 <= prices.length <= 10^5`.
- **Values** are `int` values, and equal prices pop each other.
- **Spans** in the returned pairs add up to `prices.length`.
- **Return** is an `int[][]` with one pair per remaining stack entry.

**Example 1.** Input `[4,9,7,7,2,2]`, output `[[9,2],[7,2],[2,2]]`.

**Example 2.** Input `[5,3,4,4,2,6]`, output `[[6,6]]`.

**Hint.** A popped pair gives its whole span to the new pair. Which prices stay on the stack at the end?

**Changed decision.** The stack stores summarized runs and keeps no index.

#### [Boundary] Equal Prices (Author exercise)
<!-- id: ms-equal-prices -->

**Prerequisites.** The two exercises above.

**Problem.** Let `prices` be an array of integers where equal prices can occur. For each day `i`, the span is the number of consecutive days ending at `i` with a price at most `prices[i]`, counting day `i`. Return the span of every day.

**Constraints.** The limits are:
- **Length** is `1 <= prices.length <= 10^5`.
- **Values** are `int` values, and every value can repeat.
- **Ties** count inside the span, because the condition is at most.
- **Return** is an `int[]` of the same length.

**Example 1.** Input `[7,7,7,7]`, output `[1,2,3,4]`.

**Example 2.** Input `[5,3,4,4,2,6]`, output `[1,1,2,3,1,6]`.

**Hint.** Compare an equal earlier price with the new one. Should it pop, or should it stay?

**Changed decision.** The pop condition includes equality, which is the opposite of the next greater scan.

#### [Recognize] Online Stock Span (LeetCode 901)
<!-- id: ms-online-stock-span -->

**Prerequisites.** The three exercises above.

**Problem.** Design a class `StockSpanner` with a method `next(int price)`. Each call receives the price of the next day and returns that day's span. The span is the maximum number of consecutive days, starting from that day and going backward, for which the price is less than or equal to that day's price.

**Constraints.** The limits are:
- **Calls** total at most `10^4`.
- **Values** are integers with `1 <= price <= 10^5`.
- **Order** is the call order, and the class never sees later prices.
- **Cost** per call is O(1) amortized, and the class cannot rescan old days.

**Example 1.** Input calls `next(31)`, `next(41)`, `next(41)`, `next(59)`, `next(26)`, `next(53)`, output `[1,2,3,4,1,2]`.

**Example 2.** Input calls `next(9)`, `next(9)`, `next(10)`, `next(8)`, `next(8)`, `next(8)`, output `[1,2,3,1,2,3]`.

**Hint.** The class has no array of past prices to index. What does each stack entry have to carry?

**Changed decision.** The data arrives one price at a time, so each entry summarizes its run itself.
