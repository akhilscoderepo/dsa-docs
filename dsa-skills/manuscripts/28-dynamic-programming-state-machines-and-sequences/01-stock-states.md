<!-- lesson-kind: standard -->
<!-- lesson-id: stock-states -->
## Stock States

<!-- stage: context -->
### A Profit Report That Sells Before Buying

#### The Wrong Subtraction

A reporting script receives the daily closing prices of one stock: 6, 9, 1, 3. The author reasons that the best profit is the largest price minus the smallest price. The script prints 9 - 1 = 8. No real trade earns 8, because the largest price (9) occurs on day 1 and the smallest price (1) occurs on day 2. A trade buys first and sells later, so buying at 6 and selling at 9 earns 3, and buying at 1 and selling at 3 earns 2. The correct answer for a single trade is 3.

The error comes from ignoring order. At the end of each day, the trader is in one of two situations: the trader owns a share or does not own one. What the trader may do next depends only on that situation and the next price.

#### The Exact Task

Formally, the input is an array `prices`, where `prices[i]` is the price on day `i`. A trade buys one share on a day and sells it on a later day, and the profit of a trade is the sell price minus the buy price. This lesson computes the best total profit while the trader owns at most one share at a time.

The lesson asks how to record the two situations so that every day updates them with a constant amount of work.

<!-- stage: naive -->
### Trying Every Choice On Every Day

The direct idea is a recursion over the days. On each day, the trader rests, buys when no share is owned, or sells when a share is owned. The method `explore(prices, day, owns)` returns the best profit obtainable from `day` to the end of the array. The flag `owns` records whether the trader owns a share before that day. A share still owned after the last day never gets sold, so that ending is invalid and receives a very negative value.

```java
static int explore(int[] prices, int day, boolean owns) {
    if (day == prices.length) return owns ? -1_000_000 : 0;
    int rest = explore(prices, day + 1, owns);
    if (owns) {
        return Math.max(rest, prices[day] + explore(prices, day + 1, false));
    }
    return Math.max(rest, -prices[day] + explore(prices, day + 1, true));
}
```

The call `explore(prices, 0, false)` returns the best profit for any number of trades. Every day offers two choices, so the recursion tree has one leaf for each combination of choices.

```predict
How many calls does explore make for a prices array of length 3, counting the first call? Then estimate the number for length 30.

It makes 15 calls for length 3, because the tree has 1 + 2 + 4 + 8 calls on its four levels. For length 30 the tree has 2^31 - 1 calls, which is more than two billion. The method returns the right answer but takes exponential time.
```

<!-- stage: bottleneck -->
### The Same Day Is Solved Many Times

The recursion has O(2^n) running time for n days, and n = 40 already needs about 2 * 10^12 calls. Most of that work repeats. Two different histories can reach day 5 with no share owned, for example after selling on day 2 or after never buying. The call `explore(prices, 5, false)` is identical in both histories and returns the same number.

A call depends on only two inputs: the day and the ownership flag. A prices array of length n has n + 1 values of `day` and 2 values of `owns`, so the recursion has at most 2n + 2 distinct calls. The exponential cost comes entirely from computing each distinct call again and again. A table with two entries per day removes the repetition, and a loop over the days fills it in O(n) time.

<!-- stage: insight -->
### Two Best Values Per Day

The profit before a day does not depend on the order of earlier trades, only on the ownership situation at the end of the day. So it is enough to remember the best profit for each situation.

<!-- names: hold, cash, transition -->

#### Two Values For Two Situations

Let `hold` be the best profit over the processed days among all plans that end the last processed day while owning a share. The profit of such a plan already includes the price paid for that share, so `hold` is often negative. Let `cash` be the best profit among all plans that end the last processed day without owning a share. Before day 0, `cash` is 0, because doing nothing is a legal plan. The value of `hold` is impossible, because no share exists yet, so it starts at a very negative number.

#### Each Day Has Four Moves

On a new day with price `p`, exactly two moves reach each situation. Each move is a **transition** between the situation before the day and the situation after it.

Staying in cash means doing nothing, and the value is the old `cash`. Selling moves from hold to cash and earns the price, so the value is the old `hold` plus `p`. Staying in hold means doing nothing, and the value is the old `hold`. Buying moves from cash to hold and pays the price, so the value is the old `cash` minus `p`.

The new `cash` is the larger of the first two values, and the new `hold` is the larger of the last two. Both new values use only old values, so the day computes them from a snapshot of the previous day.

#### Why The Answer Is Cash

The best plan over all days must end without a share, since an owned share at the end earns nothing. The final `cash` therefore covers all plans, and the answer is the final `cash`. For a single allowed trade, the buy value changes to `-p`, because the one trade has no earlier profit to add to the price paid.

<!-- stage: variables -->
### The Two Running Values

The method reads the array without changing it and keeps these values.

- **hold** is the best profit so far among plans that own a share, started at `Integer.MIN_VALUE / 2`.
- **cash** is the best profit so far among plans that own no share, started at 0.
- **p** is the price of the current day.
- **nextHold** is the new value of `hold` computed from the old `hold` and old `cash`.
- **nextCash** is the new value of `cash` computed from the old `hold` and old `cash`.

The start value of `hold` is half of the smallest `int`. Adding a price of at most 10^4 to it cannot overflow, and the half value leaves a wide margin before the smallest `int`. The loop computes both next values before it overwrites either old value, so the second computation never reads an updated value.

<!-- stage: trace -->
### Two Runs Day By Day

#### Many Trades On Five Prices

The first run uses prices 3, 1, 4, 1, 5 with any number of trades. Each cell is a price, the pointer `i` marks the day, and the variables show `hold` and `cash` after that day. The impossible `hold` before the first day appears as -1073741824, which is half of the smallest `int`.

On day 0 the only useful move is a buy, so `hold` becomes -3. On day 1 a lower price improves `hold` to -1. Day 2 sells at 4, so `cash` becomes 3. Day 3 buys again with `cash - 1`, and `hold` becomes 2. Day 4 sells at 5 and `cash` becomes 7. Two trades each earn their own rise, 3 and 4.

```trace
{"cells":[3,1,4,1,5],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"hold":-1073741824,"cash":0},"note":"Before day 0, cash is 0 because doing nothing is legal, and hold is impossible."},{"at":{"i":0},"vars":{"hold":-3,"cash":0},"note":"Day 0, price 3. Buying gives -3, so hold becomes -3. No share exists to sell, so cash stays 0."},{"at":{"i":1},"vars":{"hold":-1,"cash":0},"note":"Day 1, price 1. Buying gives -1, so hold becomes -1. Selling does not improve cash, which stays 0."},{"at":{"i":2},"vars":{"hold":-1,"cash":3},"note":"Day 2, price 4. Buying gives -4, which does not beat -1, so hold stays. Selling gives 3, so cash becomes 3."},{"at":{"i":3},"vars":{"hold":2,"cash":3},"note":"Day 3, price 1. Buying gives 2, so hold becomes 2. Selling does not improve cash, which stays 3."},{"at":{"i":4},"vars":{"hold":2,"cash":7},"note":"Day 4, price 5. Buying gives -2, which does not beat 2, so hold stays. Selling gives 7, so cash becomes 7."}]}
```

#### One Trade On Six Prices

The second run uses prices 7, 1, 5, 3, 6, 4 and allows one trade. The buy move is `-p`, so `hold` always holds the negated lowest price seen so far. It reaches -1 on day 1 and stays there. The value of `cash` grows from 0 to 4 on day 2 and to 5 on day 4. Day 5 does not improve it, so the answer is 5, the profit of buying at 1 and selling at 6.

```trace
{"cells":[7,1,5,3,6,4],"pointers":["i"],"steps":[{"at":{"i":-1},"vars":{"hold":-1073741824,"cash":0},"note":"Before day 0, cash is 0 because doing nothing is legal, and hold is impossible."},{"at":{"i":0},"vars":{"hold":-7,"cash":0},"note":"Day 0, price 7. Buying gives -7, so hold becomes -7. No share exists to sell, so cash stays 0."},{"at":{"i":1},"vars":{"hold":-1,"cash":0},"note":"Day 1, price 1. Buying gives -1, so hold becomes -1. Selling does not improve cash, which stays 0."},{"at":{"i":2},"vars":{"hold":-1,"cash":4},"note":"Day 2, price 5. Buying gives -5, which does not beat -1, so hold stays. Selling gives 4, so cash becomes 4."},{"at":{"i":3},"vars":{"hold":-1,"cash":4},"note":"Day 3, price 3. Buying gives -3, which does not beat -1, so hold stays. Selling does not improve cash, which stays 4."},{"at":{"i":4},"vars":{"hold":-1,"cash":5},"note":"Day 4, price 6. Buying gives -6, which does not beat -1, so hold stays. Selling gives 5, so cash becomes 5."},{"at":{"i":5},"vars":{"hold":-1,"cash":5},"note":"Day 5, price 4. Buying gives -4, which does not beat -1, so hold stays. Selling does not improve cash, which stays 5."}]}
```

<!-- stage: code -->
### Two Loops With Two Values

Both methods scan the array once and return `cash`. The first allows any number of trades. The second allows one trade, and only its buy line differs.

```java
static int manyTrades(int[] prices) {
    int hold = Integer.MIN_VALUE / 2;
    int cash = 0;
    for (int p : prices) {
        int nextHold = Math.max(hold, cash - p);
        int nextCash = Math.max(cash, hold + p);
        hold = nextHold;
        cash = nextCash;
    }
    return cash;
}

static int oneTrade(int[] prices) {
    int hold = Integer.MIN_VALUE / 2;
    int cash = 0;
    for (int p : prices) {
        int nextHold = Math.max(hold, -p);
        int nextCash = Math.max(cash, hold + p);
        hold = nextHold;
        cash = nextCash;
    }
    return cash;
}
```

Each method runs in O(n) time and O(1) extra memory. An empty array returns 0, and a strictly falling array also returns 0, because `cash` never rises above its start value.

<!-- stage: applicability -->
### Recognizing Daily Ownership Modes

#### Reading The Cue

Use this method when every step ends in one of a few named modes and the next step depends only on the current mode and the new input. Stock questions, on and off switches and borrow and return sequences all have this shape. Draw the modes as boxes and the legal moves as lines before writing any variable.

#### Checking The Invariant

The invariant says that after each day, `hold` and `cash` are the best profits over the processed prefix for their exact ownership situations. Check it on a one-day array, where `cash` must stay 0 and `hold` must equal the negated price. Check a strictly falling array, where `cash` must stay 0, and a flat array, where a trade earns nothing and `cash` also stays 0.

#### Avoiding The False Friend

The false friend is the largest price minus the smallest price from the opening, which ignores order. A second false friend is the sum of all positive day-to-day rises. That sum equals the many-trades answer. It has no ownership modes to extend, so it fails once a rule such as a waiting day after a sale or a fee appears.

#### Knowing When Two Values Are Not Enough

Do not use two scalars when a rule needs history beyond the current mode. A cooldown after a sale needs to know whether the last action was a sale. A limit on the number of trades needs a trade count. Each such fact adds a dimension to the state, and the next lesson adds them.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ss-one-trade-states -->

**Prerequisites.** The two best values `hold` and `cash` from this lesson.

**Problem.** Given an integer array `prices`, where `prices[i]` is the price on day `i`, a trader completes at most one trade. A trade buys on one day and sells on a strictly later day. Return an array `best` of the same length, where `best[i]` is the largest profit of at most one trade that is complete by the end of day `i`. A profit of 0 means no trade.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 1000`, and empty input returns an empty array.
- **Price** satisfies `0 <= prices[i] <= 10000`.
- **Result** is a new `int[]` of the same length as `prices`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [7,1,5,3,6,4]`, output `[0,0,4,4,5,5]`.

**Example 2.** Input `prices = [5,4,3]`, output `[0,0,0]`.

**Hint.** The value of `cash` after day `i` is exactly `best[i]`. Which line of the loop gives it, and when do you store it?

**Changed decision.** The method records `cash` after every day, not only after the last day. The buy move is `-p`, because only one trade is allowed.

#### [Vary] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ss-many-trades -->

**Prerequisites.** The previous exercise and the buy and sell moves from this lesson.

**Problem.** Given an integer array `prices`, a trader may buy and sell any number of times while owning at most one share. Each day allows at most one action, and a buy and a sell cannot share a day. Return an array `{profit, trades}` where `profit` is the largest total profit and `trades` is the smallest number of buys that achieves that profit.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 1000`.
- **Price** satisfies `0 <= prices[i] <= 10000`.
- **Result** is an `int[]` of length 2, and `{0,0}` means no trade helps.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [3,1,4,1,5]`, output `[7,2]`.

**Example 2.** Input `prices = [2,2,2]`, output `[0,0]`.

**Hint.** Store a pair for each situation and compare pairs by larger profit first, then by fewer trades. Where is a trade counted?

**Changed decision.** Each situation keeps a profit and a trade count instead of one number, and equal profits keep the smaller count.

#### [Boundary] One Day And Falling Prices (Author exercise)
<!-- id: ss-falling-prices -->

**Prerequisites.** The two exercises above.

**Problem.** Given an integer array `prices`, a trader completes at most one trade, which pairs a buy day with a later sell day. Return the largest profit of a trade, or -1 if no trade earns a profit greater than 0.

**Constraints.** The limits are:
- **Length** satisfies `1 <= prices.length <= 1000`.
- **Price** satisfies `0 <= prices[i] <= 10000`.
- **Result** is an `int`, and -1 is the only negative result.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [9]`, output `-1`.

**Example 2.** Input `prices = [4,4,2,1,4]`, output `3`.

**Hint.** What does `cash` equal when no trade ever earned more than 0, and which value of `cash` means that no trade happened?

**Changed decision.** The method converts a final `cash` of 0 to the result -1, because a trade with zero profit does not count as a profitable trade.

#### [Recognize] State Diagram (Author exercise)
<!-- id: ss-state-diagram -->

**Prerequisites.** All three exercises above.

**Problem.** Given an integer array `prices`, each day the trader performs exactly one action: Buy, Sell or Rest. Buy requires that the trader owns no share, and Sell requires that the trader owns one. The trader owns no share before the first day and after the last day. Return `{profit, ways}`, where `profit` is the largest total profit and `ways` is the number of legal action sequences that earn it.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 12`.
- **Price** satisfies `0 <= prices[i] <= 100`.
- **Result** is an `int[]` of length 2, and the empty array returns `{0,1}`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [1,2,3]`, output `[2,1]`.

**Example 2.** Input `prices = [2,2,2]`, output `[0,4]`.

**Hint.** Draw the two situations and the actions on each line first. How many ways reach each situation, and what happens to the counts when two actions tie?

**Changed decision.** Each situation keeps a best profit and a count of sequences that reach it, and equal profits add their counts.
