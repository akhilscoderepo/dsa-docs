<!-- lesson-kind: standard -->
<!-- lesson-id: running-extremum-and-best-gain -->
## Running Extremum And Best Gain

<!-- stage: context -->
### The Collector's Best Flip

A collector watches the daily asking price of a rare trading card for a month, written down as a list. In hindsight she wants to know the largest profit she could have made by buying on one day and selling on a later day. Selling before buying is not allowed, and she may also decide to skip trading entirely if prices only fell.

The tempting shortcut is to find the highest price and the lowest price and subtract. That works only if the low came first. On a list that peaks early and bottoms out later it reports a profit that nobody could have collected, because the sale would have to happen before the purchase.

<!-- stage: naive -->
### Try Every Buy And Sell Pair

The unambiguous approach is to consider each buying day and each later selling day and keep the best difference.

```java
static int bestFlipBruteForce(int[] prices) {
    int best = 0;
    for (int buy = 0; buy < prices.length; buy++) {
        for (int sell = buy + 1; sell < prices.length; sell++) {
            best = Math.max(best, prices[sell] - prices[buy]);
        }
    }
    return best;
}
```

It respects the order, since the sale index always follows the purchase index. It starts the best at 0, which encodes the permission to skip trading.

<!-- stage: bottleneck -->
### Re-Deriving The Best Buy Day

For `n` prices the pair loops perform `n * (n - 1) / 2` comparisons, which is O(n^2). With `n = 100,000` that is nearly five billion subtractions, far beyond a budget of roughly 10^8. The extra memory is O(1), so time is the entire cost.

Look at what the inner loop does for a fixed selling day. It examines every earlier day to find the cheapest purchase, and the next selling day repeats most of that search over almost the same set of earlier days. The cheapest price among the days before day 40 is the cheapest among days before day 39, or the price of day 39 itself. Nothing about day 39's search has to be redone, and the quadratic work is just that one fact being recomputed on every selling day.

<!-- stage: insight -->
### Remember The Cheapest Day So Far

For any fixed selling day, the best buying day is simply the cheapest price among the days before it. So the whole answer reduces to one number carried along the scan, plus a second number recording the best result found.

The first number is the **running minimum**, the smallest value among the positions already read. The second is the **best gain**, the largest value of `price - runningMinimum` seen at any position. The invariant is that before reading `prices[i]`, the running minimum equals the minimum of `prices[0..i-1]`. Reading a new price does two things. It forms a candidate gain by subtracting that minimum, and it then lowers the minimum if the new price is cheaper.

<!-- names: running minimum, best gain, transaction contract -->

The **transaction contract** is the statement of what trades are allowed. Here it says one purchase followed by one later sale, with trading optional. Optional trading is why the best gain starts at 0. If a trade were mandatory, an all-falling list would have to report its least bad loss, and the starting value would have to change. Naming the contract before writing the initial value avoids that mistake.

This is a different state from the one in the previous lesson. It still reads one element at a time, but it keeps a minimum and a result together, and the result is formed by combining the new element with the minimum, not by folding the new element into a single total. It is also different from maximum subarray, which the later Kadane lesson teaches. A best gain picks two positions and ignores everything between them, while a subarray sum depends on every element in its block.

<!-- stage: variables -->
### Two Numbers And An Order

Keep `lowest`, the smallest price in the prefix, and `best`, the largest gain so far. The loop index decides the order. A candidate gain at index `i` may only subtract a minimum taken from earlier indices, which is why the minimum is read before it is updated with the current price, or updated first at the harmless cost of a zero gain on the same day. Starting `lowest` from the first price and `best` at 0 matches the contract that allows skipping the trade.

<!-- stage: trace -->
### Prices That Peak Early

Take the prices `[9, 3, 6, 2, 8, 5]`. The highest price is 9 on the first day and the lowest is 2 on the fourth, so the careless subtraction says 7, which cannot be achieved because 9 comes before 2. The scan finds the true answer instead.

Day 0 sets the running minimum to 9 and the best gain to 0. Day 1 has price 3, which is below the minimum, so the minimum drops to 3 and no gain is formed. Day 2 has price 6, which gives a gain of 3 and a new best of 3. Day 3 has price 2, which becomes the new minimum. Day 4 has price 8, which gives a gain of 6 over the minimum of 2 and a new best of 6. Day 5 has price 5, a gain of 3, which does not beat 6. The answer is 6, not 7. The step to watch is day 3, where the minimum drops to 2 but only days after it can use that bargain, which is exactly what the order rule enforces.

```trace
{"cells":[9,3,6,2,8,5],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"lowest":9,"best":0},"note":"Day 0: price 9. The running minimum is 9 and no sale is possible yet, so the best gain is 0."},{"at":{"i":1},"vars":{"lowest":3,"best":0},"note":"Day 1: price 3 is below the minimum, so the minimum drops to 3. The gain 3 - 9 is negative and is ignored."},{"at":{"i":2},"vars":{"lowest":3,"best":3},"note":"Day 2: price 6 sells at a gain of 3 over the minimum 3. The best gain becomes 3."},{"at":{"i":3},"vars":{"lowest":2,"best":3},"note":"Day 3: price 2 gives no gain over 3 and becomes the new minimum. Only later days can use this bargain."},{"at":{"i":4},"vars":{"lowest":2,"best":6},"note":"Day 4: price 8 sells at a gain of 6 over the minimum 2. The best gain becomes 6."},{"at":{"i":5},"vars":{"lowest":2,"best":6},"note":"Day 5: price 5 gives a gain of 3 over 2, which does not beat 6. The answer is 6, not the careless 9 - 2 = 7."}]}
```

<!-- stage: code -->
### The Two-Number Scan

```java
static int bestFlip(int[] prices) {
    if (prices.length == 0) return 0;
    int lowest = prices[0];                       // minimum of the prefix read so far
    int best = 0;                                 // trading is optional, so 0 is always achievable
    for (int i = 1; i < prices.length; i++) {
        best = Math.max(best, prices[i] - lowest);   // sell today, bought at the cheapest earlier day
        lowest = Math.min(lowest, prices[i]);        // then let today be a future buying option
    }
    return best;
}

static int largestDrop(int[] values) {
    if (values.length == 0) return 0;
    int highest = values[0];
    int drop = 0;
    for (int i = 1; i < values.length; i++) {
        drop = Math.max(drop, highest - values[i]);
        highest = Math.max(highest, values[i]);
    }
    return drop;
}
```

Both methods make one pass, so they run in O(n) time and O(1) space. The order of the two statements in the loop is what enforces the rule that the purchase comes earlier. The candidate uses the minimum from before today, and only afterward is today's price allowed to lower it. `largestDrop` mirrors the structure with a maximum, which is the same pattern with the comparison reversed.

<!-- stage: applicability -->
### When The Pair Must Respect Order

Use a running extremum when the answer is the best difference between two positions, the earlier one must come first, and the positions need not be adjacent. The invariant to state is that before reading `nums[i]`, the running extremum equals the extremum of `nums[0..i-1]`. Say the transaction contract aloud before choosing the initial result.

The false friend is the plain maximum minus the plain minimum, which ignores order and can report an impossible profit. Another false friend is Kadane's maximum subarray, which looks similar because both scan once and both track a best value. They answer different questions. The subarray version sums a contiguous block, and this one pairs two positions. Even within stock problems the family splits. When unlimited trades are allowed, the best result comes from adding every positive day-to-day rise, a different state with no running minimum at all, and the last exercise of this lesson uses that contrast.

Java hazards are small here. Subtracting two `int` values can overflow only for extreme inputs, so check the limits. A starting result of 0 is a decision, and for a mandatory trade the starting result must be something like `Integer.MIN_VALUE` together with a guard that at least two prices exist.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ar-best-time-single -->

**Prerequisites.** The running-minimum scan in this lesson; the aggregation lesson.

**Problem.** Given daily prices, choose one day to buy and a later day to sell, and return the largest profit possible. If no profitable trade exists, return 0.

**Constraints.** 1 <= prices.length <= 10^5 and 0 <= prices[i] <= 10^4. Aim for one pass and two scalars.

**Example 1.** Input `prices = [9, 3, 6, 2, 8, 5]`, output 6, from buying at 2 and selling at 8.

**Example 2.** Input `prices = [5, 4, 3, 2]`, output 0, since every later price is lower and the best choice is not to trade.

**Hint.** For a fixed selling day, which earlier price is the best to have paid? What single number lets you answer that without looking back?

**Changed decision.** First rung: a running minimum and a best gain replace a search over all earlier days.

#### [Vary] Largest Drop (Author exercise)
<!-- id: ar-largest-drop -->

**Prerequisites.** The best-flip exercise above.

**Problem.** Given an array of values, return the largest `earlier - later` over all pairs in which the earlier value comes first. If no pair has an earlier value larger than the later one, return 0.

**Constraints.** 0 <= values.length <= 10^5 and -10^9 <= values[i] <= 10^9. Use `long` for the difference if overflow is possible.

**Example 1.** Input `values = [4, 9, 2, 7, 1]`, output 8, from 9 followed by 1.

**Example 2.** Input `values = [1, 2, 3]`, output 0, because the values only rise.

**Hint.** If the running extremum was a minimum before, what should it be now? Which comparison flips?

**Changed decision.** The running extremum becomes a maximum and the difference reverses direction.

#### [Boundary] No Profitable Pair (Author exercise)
<!-- id: ar-no-profitable-pair -->

**Prerequisites.** The two exercises above.

**Problem.** For strictly decreasing prices the contract answer is 0, not a negative number and not -1. Write the method so that a one-price list and a falling list both return 0, and then state what the result would be if a trade were mandatory.

**Constraints.** 1 <= prices.length <= 10^5 and 0 <= prices[i] <= 10^4. The mandatory-trade variant needs at least two prices.

**Example 1.** Input `prices = [8, 6, 5, 1]`, output 0 under the optional-trade contract.

**Example 2.** Input `prices = [8, 6, 5, 1]` under a mandatory-trade contract, output -1, the least bad loss, from buying at 6 and selling at 5.

**Hint.** What is the profit of doing nothing? Which starting value of the best gain encodes that permission?

**Changed decision.** The initial result is chosen from the contract, and changing the contract changes that single starting value.

#### [Recognize] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ar-best-time-multiple -->

**Prerequisites.** All three exercises above.

**Problem.** Now any number of trades is allowed, but you hold at most one share at a time, so you must sell before buying again. Return the maximum total profit. State the new transaction contract first, then notice that the running minimum from this lesson is no longer the right state.

**Constraints.** 1 <= prices.length <= 3 * 10^4 and 0 <= prices[i] <= 10^4. Target O(n) time and O(1) extra space.

**Example 1.** Input `prices = [1, 5, 2, 6, 3]`, output 8, from gains of 4 and 4.

**Example 2.** Input `prices = [4, 3, 2]`, output 0, since no rise ever occurs.

**Hint.** If you can trade every day, what does each rise from one day to the next contribute? Is there any reason to skip a rise?

**Changed decision.** The state moves from a running minimum to day-to-day differences, so this lesson's own pattern becomes a false friend.
