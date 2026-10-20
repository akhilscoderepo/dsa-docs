<!-- lesson-kind: combination -->
<!-- lesson-id: dp-state-machines -->
## DP State Machines

<!-- stage: context -->
### A Backtest That Breaks The Settlement Rule

A brokerage backtester replays a price list such as 2, 6, 3, 7 and reports the best profit a strategy could have made. The venue enforces a settlement rule: after a sale on one day, the account cannot buy on the next day. The backtester reports 8, and the compliance team confirms that no legal plan on those four days earns more than 5.

The report is not random noise. It reports the largest profit with the rule ignored. Every printed number is too high whenever the rule binds. Traders who trust the report size their positions on profit that no account can collect.

This lesson asks how a table over days can respect rules about what the account holds and when it may act, and how to extend the same table with a trade limit or a fee.

<!-- stage: contributions -->
### What Two Earlier Skills Add

#### What Dynamic Programming Supplies

In the foundations chapter every table entry received a one-sentence meaning and a combine rule. Each entry reads smaller entries that are already final, so the loop order follows the dependencies. A day-indexed table answers how well the first `d` days can go. The final entry is the answer, and a base entry covers the empty prefix.

#### What State Modeling Supplies

The shortest-path chapters modeled a search over nodes that carry more than a position. A node holds a position plus a small piece of extra information, and the edges list the moves that the rules allow from that node. The extra information is exactly what separates a legal future from an illegal one. Listing the edges first also exposes every rule before any code exists.

#### What Both Add Together

A table over days alone gives each day one number. That number cannot say whether the account holds a share or may buy. A graph of situations alone has no order to evaluate. Together they give a table with one entry per day and per situation, where each entry takes the best of the entries that the legal edges lead from. The tables of days stay small, because the situations are few.

<!-- stage: naive -->
### Adding Every Daily Rise

The quick idea keeps a single prefix table. Entry `best[d]` holds the profit for the first `d + 1` days, and each day adds its price rise over the previous day when that rise is positive. The routine below does exactly that and ignores the settlement rule.

```java
static int risesOnly(int[] prices) {
    int[] best = new int[prices.length];
    for (int d = 1; d < prices.length; d++) {
        best[d] = best[d - 1] + Math.max(0, prices[d] - prices[d - 1]);
    }
    return prices.length == 0 ? 0 : best[prices.length - 1];
}
```

For n prices the routine needs O(n) time and O(n) memory. It is a correct answer when the account may trade freely, because it collects every upward step. The open question is what it returns when a sale blocks the next day's purchase.

```predict
Run risesOnly on the prices [2, 6, 3, 7]. What does it return, and why can the settlement rule keep an account from earning that amount?

It returns 8, from the rise 4 on day 1 and the rise 4 on day 3. Collecting both needs a sale on day 1 and a purchase on day 2, and the rule forbids that purchase. The best legal plan buys on day 0 and sells on day 3 for 5.
```

<!-- stage: bottleneck -->
### One Number Per Day Hides The Account

The routine is fast, and the defect lies in what one number per day can express. After day 1, a plan that sold the share and a plan that still holds it differ in what they may do on day 2. The prefix entry stores a single profit and drops that difference, so the next day cannot tell which actions are legal.

Patching the routine with special cases does not scale. A cooldown needs to know whether yesterday was a sale. A trade limit needs to know how many purchases happened, and a fee only changes the value of one move. Each rule adds a new fact to remember, and checking all plans one by one costs O(2^n) time for n days, because every day offers several actions.

A reliable method must keep the facts that the rules read, and keep nothing else. The next section states how to name those facts and how to list the actions that each one allows.

<!-- stage: insight -->
### One Entry For Every Situation

A prefix table answers "what is the best value after the first `d` days". A state machine table answers "what is the best value after `d` days, given that the account is in this exact situation". The second question matters because the legal future depends on the situation and not only on the value earned so far.

<!-- names: state label, legal move, trade count -->

#### Name The Situations

A **state label** is a short name for one situation that the rules distinguish. The stock rules need three labels. `free` means the account holds no share and may buy. `hold` means the account holds one share. `rest` means the account sold a share today, so it cannot buy tomorrow. The second lesson names the no-share state `rest` and the sold-today state `sold`; this lesson uses `free` and `rest` for those same two situations. A trade limit adds the **trade count**, the number of purchases made so far, and the table then keeps one entry per pair of count and label.

#### List The Legal Moves

A **legal move** is one action from one label that the rules permit. The table below lists every move. The cost of a move is the change in cash. The column "To" shows where the entry for the next day takes its value, so each new entry is the best over all moves that end in it.

| From | Move | To | Cash change |
| --- | --- | --- | --- |
| free, count c | wait | free, count c | 0 |
| rest, count c | wait | free, count c | 0 |
| free, count c-1 | buy | hold, count c | minus price, minus fee |
| hold, count c | wait | hold, count c | 0 |
| hold, count c | sell | rest, count c | plus price |

A purchase starts only from `free`, and that restriction enforces the cooldown. The same row sets the trade count and charges the fee exactly once. When the rule has no cooldown, the sell move ends in `free` instead of `rest`.

#### Why A Prefix Table Is Not Enough

A prefix table merges all plans that end on the same day into one number. A state machine table merges only plans that end on the same day in the same situation. Two plans in different situations never merge, because their futures differ. The invariant is that each entry equals the best cash over all legal plans that end the day in exactly its label and count. Day `d` reads only entries of day `d - 1`, so the table needs the previous day only.

<!-- stage: variables -->
### Tables For Each Label And Count

The routine reads the price array and the rule values, and it never changes the array. It keeps these values.

- **prices** is an `int[]` of daily prices, possibly empty.
- **maxTrades** is the largest number of purchases allowed, which sets the size of each table to `maxTrades + 1`.
- **cooldown** is a `boolean` that is true when a sale blocks the next day's purchase.
- **fee** is an `int` charged once at each purchase.
- **free**, **hold** and **rest** are `long[]` tables where entry `c` is the best cash with `c` purchases made.
- **NEG** is a large negative `long` that marks a situation no legal plan reaches yet.

The method writes the new tables for a day into separate arrays, because a move reads yesterday's entries only. The first day starts with `free[0] = 0` and every other entry at `NEG`.

<!-- stage: trace -->
### Two Runs Over Six Days

#### Cooldown Without A Trade Limit

The first run uses the prices 3, 2, 6, 5, 0, 3 with the cooldown rule and no limit on purchases. The cells are the prices, and the pointer `d` marks the day. The variables show the three tables after the day, and the value -99 marks a situation no plan reaches. The cash after the final day is the larger of `free` and `rest`.

The share bought at price 2 on day 1 sells at 6 on day 2, which moves cash into `rest` on day 2. Day 3 turns `rest` into `free`, so the account could buy again, but the price 5 is no bargain. The price 0 on day 4 is the next purchase, and the sale at 3 on day 5 lands in `rest`. The final answer is 7.

```trace
{"cells":[3,2,6,5,0,3],"pointers":["d"],"steps":[{"at":{"d":0},"vars":{"price":3,"free":0,"hold":-3,"rest":-99},"note":"After day 0 at price 3, the best cash is 0 when free, -3 when holding and -99 when resting."},{"at":{"d":1},"vars":{"price":2,"free":0,"hold":-2,"rest":-1},"note":"After day 1 at price 2, the best cash is 0 when free, -2 when holding and -1 when resting."},{"at":{"d":2},"vars":{"price":6,"free":0,"hold":-2,"rest":4},"note":"After day 2 at price 6, the best cash is 0 when free, -2 when holding and 4 when resting."},{"at":{"d":3},"vars":{"price":5,"free":4,"hold":-2,"rest":3},"note":"After day 3 at price 5, the best cash is 4 when free, -2 when holding and 3 when resting."},{"at":{"d":4},"vars":{"price":0,"free":4,"hold":4,"rest":-2},"note":"After day 4 at price 0, the best cash is 4 when free, 4 when holding and -2 when resting."},{"at":{"d":5},"vars":{"price":3,"free":4,"hold":4,"rest":7},"note":"After day 5 at price 3, the best cash is 4 when free, 4 when holding and 7 when resting."}]}
```

#### Two Purchases At Most

The second run drops the cooldown and allows two purchases on the prices 3, 8, 1, 6, 2, 9. The variables `f1` and `f2` are the best cash with `free` after one and two purchases, and `h1` and `h2` are the best cash with `hold`. The entry for no purchases stays at 0. Each step shows the tables after the day.

The first purchase at 3 and its sale at 8 gives `f1` a value of 5 on day 1. The later purchase at 1 on day 2 moves from `f1` into `h2`, because it is the second purchase. The final sale at 9 on day 5 gives `f2` the value 13, which matches the best pair of trades.

```trace
{"cells":[3,8,1,6,2,9],"pointers":["d"],"steps":[{"at":{"d":0},"vars":{"price":3,"f1":-99,"f2":-99,"h1":-3,"h2":-99},"note":"After day 0 at price 3, free with one purchase holds -99, free with two holds -99, holding after one holds -3 and holding after two holds -99."},{"at":{"d":1},"vars":{"price":8,"f1":5,"f2":-99,"h1":-3,"h2":-99},"note":"After day 1 at price 8, free with one purchase holds 5, free with two holds -99, holding after one holds -3 and holding after two holds -99."},{"at":{"d":2},"vars":{"price":1,"f1":5,"f2":-99,"h1":-1,"h2":4},"note":"After day 2 at price 1, free with one purchase holds 5, free with two holds -99, holding after one holds -1 and holding after two holds 4."},{"at":{"d":3},"vars":{"price":6,"f1":5,"f2":10,"h1":-1,"h2":4},"note":"After day 3 at price 6, free with one purchase holds 5, free with two holds 10, holding after one holds -1 and holding after two holds 4."},{"at":{"d":4},"vars":{"price":2,"f1":5,"f2":10,"h1":-1,"h2":4},"note":"After day 4 at price 2, free with one purchase holds 5, free with two holds 10, holding after one holds -1 and holding after two holds 4."},{"at":{"d":5},"vars":{"price":9,"f1":8,"f2":13,"h1":-1,"h2":4},"note":"After day 5 at price 9, free with one purchase holds 8, free with two holds 13, holding after one holds -1 and holding after two holds 4."}]}
```

<!-- stage: code -->
### One Table Per Label And Count

The method builds the new tables from the old ones each day, using the moves of the table above. It switches the sale target by the cooldown flag.

```java
static long bestCash(int[] prices, int maxTrades, boolean cooldown, int fee) {
    final long NEG = Long.MIN_VALUE / 4;
    long[] free = new long[maxTrades + 1], hold = new long[maxTrades + 1], rest = new long[maxTrades + 1];
    java.util.Arrays.fill(free, NEG);
    java.util.Arrays.fill(hold, NEG);
    java.util.Arrays.fill(rest, NEG);
    free[0] = 0;
    for (int price : prices) {
        long[] nFree = new long[maxTrades + 1], nHold = new long[maxTrades + 1], nRest = new long[maxTrades + 1];
        for (int c = 0; c <= maxTrades; c++) {
            nFree[c] = Math.max(free[c], rest[c]);
            if (!cooldown) nFree[c] = Math.max(nFree[c], hold[c] + price);
            nHold[c] = Math.max(hold[c], c > 0 ? free[c - 1] - price - fee : NEG);
            nRest[c] = cooldown ? hold[c] + price : NEG;
        }
        free = nFree; hold = nHold; rest = nRest;
    }
    long answer = 0;
    for (int c = 0; c <= maxTrades; c++) answer = Math.max(answer, Math.max(free[c], rest[c]));
    return answer;
}
```

The method runs in O(n * maxTrades) time and uses O(maxTrades) memory, since only the previous day's tables stay alive. The prices 3, 2, 6, 5, 0, 3 with a cooldown and a large limit return 7. The prices 3, 8, 1, 6, 2, 9 with limit 2 and no cooldown return 13.

<!-- stage: applicability -->
### Choosing The Situations

#### Reading The Cue

Use this lesson when each step offers several actions and a rule restricts an action based on earlier actions. Phrases such as "cannot act the next day", "at most k times", "pay once per" and "holding at most one" name the facts to remember. Count the distinct facts the rules read, and give each combination its own label.

#### Checking The Invariant

The invariant says that every entry equals the best value over all legal plans that end the day in its exact label and count. Test it on an empty array, which must return 0. Test falling prices, which must return 0 without a purchase. Compare against a brute force that tries every action sequence on arrays of up to ten days.

#### Avoiding The False Friend

The false friend is a prefix table that adds the best gains day by day and looks like a state machine without labels. It returns a plausible profit that breaks a rule. A second false friend is updating `hold` and `free` in place on one day, which lets a purchase read the same day's sale. A third is charging the fee at both ends of a trade, which doubles the cost.

<!-- stage: exercises -->
### Exercises

#### [Build] Best Time To Buy And Sell Stock (LeetCode 121)
<!-- id: sm-best-trade-days -->

**Prerequisites.** The labels `free` and `hold` from this lesson and a running minimum from the prefix lessons.

**Problem.** An array `prices` of daily prices is given. A trade buys on day `b` and sells on a later day `s` with `b < s`, and its profit is `prices[s] - prices[b]`. Return the array `{b, s}` of the trade with the largest profit, provided that profit is greater than 0. Among trades with equal profit, the smaller `s` wins, and then the smaller `b`. When no trade has positive profit, return `{-1, -1}`.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 100000`, and an empty array returns `{-1, -1}`.
- **Price** satisfies `0 <= prices[i] <= 10000`.
- **Result** is an `int[]` of length 2 holding day indexes.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [6,2,8,2,8,1]`, output `[1,2]`.

**Example 2.** Input `prices = [7,5,4]`, output `[-1,-1]`.

**Hint.** The `hold` label keeps its best entry value and also the day that entry bought on. When does a later equal price replace that day?

**Changed decision.** The label stores the buy day next to its value. A strict comparison keeps the earliest day, which implements the tie rule.

#### [Vary] Best Time To Buy And Sell Stock With Cooldown (LeetCode 309)
<!-- id: sm-cooldown-days -->

**Prerequisites.** The exercise above and the table of legal moves from this lesson.

**Problem.** An array `prices` is given, and any number of trades may be made, holding at most one share. After a sale on day `i`, the account cannot buy on day `i + 1`. A plan ends with no share held. The profit is the total of sale prices minus purchase prices. A cooldown day is a day `i + 1 < n` that follows a sale on day `i`. Return `{profit, cooldownDays}` for the plan with the largest profit and, among those, the fewest cooldown days.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 1000`, and an empty array returns `{0, 0}`.
- **Price** satisfies `0 <= prices[i] <= 1000`.
- **Result** is a `long[]` of length 2.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [1,4,2,5]`, output `[4,0]`.

**Example 2.** Input `prices = [2,9,1,9,1,9]`, output `[15,1]`.

**Hint.** Both goals fit one comparison if the table stores profit times 1000 minus the cooldown days. Which move adds one cooldown day?

**Changed decision.** The `rest` label gains a penalty of one unit when the sale is not on the last day. The entry now orders plans by profit first and cooldown days second.

#### [Boundary] Best Time To Buy And Sell Stock With Transaction Fee (LeetCode 714)
<!-- id: sm-fee-min-profit -->

**Prerequisites.** The two exercises above and the update-order warning from this lesson.

**Problem.** An array `prices`, an integer `fee` and an integer `minProfit` are given. Any number of trades may be made, holding at most one share. Each purchase costs its price plus `fee`. A plan ends with no share held. Return the largest profit among all plans if it is at least `minProfit`; otherwise return 0.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 50000`, and an empty array returns 0.
- **Price** satisfies `0 <= prices[i] <= 50000`.
- **Fee** satisfies `0 <= fee <= 50000`, and fee 0 is allowed.
- **Minimum** satisfies `0 <= minProfit <= 1000000`, and the result is a `long`.

**Example 1.** Input `prices = [2,8,4,9]`, `fee = 2`, `minProfit = 5`, output `7`.

**Example 2.** Input `prices = [2,8,4,9]`, `fee = 2`, `minProfit = 9`, output `0`.

**Hint.** Where does the fee enter the move table? Which day's `free` entry must a purchase read?

**Changed decision.** The fee is charged on the purchase, as in this lesson's move table, and the final answer passes through a threshold test. The update order stays the same as in the lesson.

#### [Recognize] Best Time To Buy And Sell Stock III (LeetCode 123)
<!-- id: sm-k-trades -->

**Prerequisites.** All three exercises above.

**Problem.** An array `prices` and an integer `k` are given. A plan makes at most `k` purchases, holds at most one share, and ends with no share held. Each purchase and its later sale form one trade, and the profit is the total of sale prices minus purchase prices. Return `{profit, trades}` for the plan with the largest profit and, among those, the fewest trades.

**Constraints.** The limits are:
- **Length** satisfies `0 <= prices.length <= 1000`, and an empty array returns `{0, 0}`.
- **Price** satisfies `0 <= prices[i] <= 1000`.
- **Limit** satisfies `0 <= k <= 100`, and `k = 0` returns `{0, 0}`.
- **Result** is a `long[]` of length 2.

**Example 1.** Input `prices = [3,8,1,6,2,9]`, `k = 2`, output `[13,2]`.

**Example 2.** Input `prices = [1,5,2,6,1,5]`, `k = 3`, output `[12,3]`.

**Hint.** Besides the share, which second fact must each entry remember? How many entries does a day need?

**Changed decision.** The tables get a second axis for the purchase count, and each entry packs profit and trade count into one comparison. The moves stay those of the lesson.
