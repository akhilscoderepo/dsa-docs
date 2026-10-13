<!-- lesson-kind: standard -->
<!-- lesson-id: transaction-variants -->
## Transaction Variants

<!-- stage: context -->
### A Profit Calculator That Ignores A Rule

A brokerage tool receives daily prices `[2, 3, 4, 1, 3]` and reports the largest profit from buying and selling one share at a time. The tool uses the hold and cash states from the previous lesson and prints 4. It buys at 2 and sells at 4, then buys at 1 and sells at 3. The exchange rejects the second purchase, because its rules forbid buying on the day after a sale. The achievable profit is 3.

The same calculator also misleads when every sale carries a flat fee, and when only two sales are allowed. In each case the two-state code accepts a sequence of actions that the rules forbid, or it prices the sequence wrongly.

Formally, `prices[i]` is the price on day `i`, and the trader holds at most one share. A transaction is one purchase followed by one later sale. The cooldown rule forbids a purchase on the day right after a sale. The task is to return the largest total profit that obeys the rule. The method never changes `prices`.

This lesson asks how the table can remember a rule that depends on what happened yesterday.

<!-- stage: naive -->
### Reusing The Two-State Update

The quick idea is to run the hold and cash update from the previous lesson unchanged. Each day it keeps the better of two values for holding a share and for holding none.

```java
static int twoStates(int[] prices) {
    int hold = -prices[0];
    int cash = 0;
    for (int i = 1; i < prices.length; i++) {
        int nextHold = Math.max(hold, cash - prices[i]);
        int nextCash = Math.max(cash, hold + prices[i]);
        hold = nextHold;
        cash = nextCash;
    }
    return cash;
}
```

The method runs in O(n) time and O(1) memory for n days. The open question is whether the value `cash` can tell a purchase that follows a sale from a purchase that follows a quiet day.

```predict
Run twoStates on prices [2, 3, 4, 1, 3]. What does it return, and what is the largest profit when a purchase on the day after a sale is forbidden?

It returns 4. On day 3 the update reads cash, which already contains the sale made on day 2, and buys at price 1. The rule forbids that purchase, so the true largest profit is 3.
```

<!-- stage: bottleneck -->
### One Cash Value Hides Yesterday

The variable `cash` stores a profit only. Two histories can give the same profit while one of them sold yesterday and the other did not. The next action is legal in the second history and illegal in the first, so a single value cannot decide the transition.

A correct but slow method tries every legal action for each day: skip, buy or sell. Each day offers at most two actions, so the search visits up to 2^n action sequences, which is O(2^n) time. For n = 40 days that is more than 10^12 sequences.

Another repair stores the day of the last sale next to each profit. Day `i` then keeps up to `i` pairs, and the whole scan costs O(n^2) time. That is better, but the extra information is wasteful. The next action depends only on whether the last sale happened yesterday, which is one yes-or-no fact. A table that keeps that fact as part of its state needs a constant number of values per day.

<!-- stage: insight -->
### Make The Rule Part Of The State

Each state must answer two questions at once: does the trader own a share, and which actions the rule allows next. Then the transition table is a small graph, and the best profit for each state follows from the best profits of the previous day.

<!-- names: sold state, rest state, old values -->

#### Three States For A Cooldown

The cooldown splits the cash condition in two. The **sold state** means the trader sold today, so a purchase tomorrow is illegal. The **rest state** means the trader holds no share and may buy tomorrow. The hold state keeps its meaning. Each state stores the best profit of any history that ends the day in it.

Five transitions are legal. Hold stays hold, or comes from the rest state by paying today's price. The sold state comes only from hold by receiving today's price. The rest state comes from the rest state or from the sold state of the day before. A purchase never reads the sold state, so the rule holds by construction.

#### One Fee On One Transition

A fee changes the value of a transition and leaves the states alone. The two states hold and cash still describe the rule completely. Subtract the fee on exactly one transition of each transaction, here the sale. Charging it on both the purchase and the sale would count it twice.

#### A Count Becomes A State

A limit of two sales needs the number of completed sales in the state. Hold after zero sales, cash after one sale, hold after one sale and cash after two sales are four states, and cash after zero sales is the constant 0, which the table does not store. A purchase moves from a cash state to the next hold state, and a sale moves from a hold state to the next cash state.

#### Reading Only The Old Values

All new values of day `i` come from the **old values** of day `i - 1`. If the code overwrites one variable and then reads it for another state, the second state sees a mix of two days. The invariant is that after day `i`, each state holds the best profit of histories that end day `i` in that state. Compute every new value into a temporary before any assignment.

<!-- stage: variables -->
### The Three Profit Values

The cooldown method leaves `prices` alone and keeps these working values.

- **hold** is the best profit of a history that owns a share at the end of the day.
- **sold** is the best profit of a history that sold a share today.
- **rest** is the best profit of a history that owns no share and sold nothing today.
- **i** is the current day, from 1 to `n - 1`.
- **nextHold**, **nextSold** and **nextRest** are the values for day `i`, computed before any assignment.

Day 0 starts with `hold = -prices[0]`, `sold = 0` and `rest = 0`. The value `sold = 0` is a placeholder that no purchase reads, because a purchase reads only `rest`. The answer is the larger of `sold` and `rest` after the last day, because a history that still owns a share has not realized its profit.

<!-- stage: trace -->
### Two Runs Over Short Price Lists

#### The Rule Blocks A Purchase

The first run uses prices `[2, 3, 4, 1, 3]` and the correct update. Each cell is a price, and the pointer `i` marks the current day. The variables `hold`, `sold` and `rest` show the three states after the day.

On day 1 the sale at 3 gives `sold = 1`. On day 2 that profit moves into `rest`, so a purchase becomes legal only on day 3. On day 3 the hold value rises to 0, which means the trader sold at 3 on day 1, skipped day 2 and bought at 1. On day 4 the sale at 3 gives `sold = 3`, which is the answer.

```trace
{"cells":[2,3,4,1,3],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"hold":-2,"sold":0,"rest":0},"note":"Day 0 at price 2. The only possible action is a purchase, so hold is -2, and sold and rest stay at 0."},{"at":{"i":1},"vars":{"hold":-2,"sold":1,"rest":0},"note":"Day 1 at price 3. Hold keeps -2 or buys from rest for -3. Sold is the old hold plus the price. Rest takes the larger of the old rest 0 and the old sold 0, so a sale made today cannot fund a purchase tomorrow. The values become hold -2, sold 1 and rest 0."},{"at":{"i":2},"vars":{"hold":-2,"sold":2,"rest":1},"note":"Day 2 at price 4. Hold keeps -2 or buys from rest for -4. Sold is the old hold plus the price. Rest takes the larger of the old rest 0 and the old sold 1, so a sale made today cannot fund a purchase tomorrow. The values become hold -2, sold 2 and rest 1."},{"at":{"i":3},"vars":{"hold":0,"sold":-1,"rest":2},"note":"Day 3 at price 1. Hold keeps -2 or buys from rest for 0. Sold is the old hold plus the price. Rest takes the larger of the old rest 1 and the old sold 2, so a sale made today cannot fund a purchase tomorrow. The values become hold 0, sold -1 and rest 2."},{"at":{"i":4},"vars":{"hold":0,"sold":3,"rest":2},"note":"Day 4 at price 3. Hold keeps 0 or buys from rest for -1. Sold is the old hold plus the price. Rest takes the larger of the old rest 2 and the old sold -1, so a sale made today cannot fund a purchase tomorrow. The values become hold 0, sold 3 and rest 2."}]}
```

#### The Update That Reads A Fresh Value

The second run uses prices `[2, 5, 1, 4]` and an update in the wrong order. It computes `sold` first and then lets `rest` read that new `sold` in the same day. The correct answer is 3, because the sale at 5 on day 1 blocks the purchase at 1 on day 2.

The faulty `rest` already contains the sale of day 1, so `hold` buys at 1 on day 2 and the final sale at 4 reports 6. The profit of 6 comes from a history that the rule forbids.

```trace
{"cells":[2,5,1,4],"pointers":["i"],"steps":[{"at":{"i":0},"vars":{"hold":-2,"sold":0,"rest":0},"note":"Day 0 at price 2. The only possible action is a purchase, so hold is -2, and sold and rest stay at 0."},{"at":{"i":1},"vars":{"hold":-2,"sold":3,"rest":3},"note":"Day 1 at price 5. Sold is the old hold plus the price, 3. The faulty rest reads that new sold at once and becomes 3, so it carries every sale up to today. Hold buys from that rest, so a purchase can directly follow a sale. The values become hold -2, sold 3 and rest 3."},{"at":{"i":2},"vars":{"hold":2,"sold":-1,"rest":3},"note":"Day 2 at price 1. Sold is the old hold plus the price, -1. The faulty rest reads that new sold at once and becomes 3, so it carries every sale up to today. Hold buys from that rest, so a purchase can directly follow a sale. The values become hold 2, sold -1 and rest 3."},{"at":{"i":3},"vars":{"hold":2,"sold":6,"rest":6},"note":"Day 3 at price 4. Sold is the old hold plus the price, 6. The faulty rest reads that new sold at once and becomes 6, so it carries every sale up to today. Hold buys from that rest, so a purchase can directly follow a sale. The values become hold 2, sold 6 and rest 6."}]}
```

<!-- stage: code -->
### The Three-State Loop

The method returns the largest profit under the cooldown rule. It computes the three new values from the three old ones and then assigns them together.

```java
static int cooldownProfit(int[] prices) {
    int hold = -prices[0];
    int sold = 0;
    int rest = 0;
    for (int i = 1; i < prices.length; i++) {
        int nextHold = Math.max(hold, rest - prices[i]);
        int nextSold = hold + prices[i];
        int nextRest = Math.max(rest, sold);
        hold = nextHold;
        sold = nextSold;
        rest = nextRest;
    }
    return Math.max(sold, rest);
}
```

The cost is O(n) time and O(1) memory. The fee version keeps two variables and subtracts the fee in the line that computes `nextCash`. The two-sale version keeps four variables and follows the same pattern of temporaries.

<!-- stage: applicability -->
### Recognizing A Rule That Needs State

#### Reading The Cue

Use this method when a rule restricts which action may follow which, or when the number of completed actions has a limit. Phrases such as "after a sale you must wait", "each transaction costs", and "at most k transactions" point here. A flat cost or reward changes a transition value, a waiting rule adds a state, and a count limit multiplies the states.

#### Checking The Invariant

The invariant says that each state stores the best profit of histories that end the day in exactly that situation. Check it by listing the legal transitions and confirming that no transition leaves a state the rule forbids. Test a falling price list, where the answer is 0. Test a single day. Test a list where a sale on day `i` makes day `i + 1` attractive, because only that case exposes a wrong update order.

#### Avoiding The False Friend

The first false friend is the two-state update, which passes every list in which the rule never binds. The second is a greedy rule that sells at every peak, which ignores both the fee and the waiting day. The third is an in-place update that overwrites a variable before another state reads it.

The method does not fit when legality depends on a history that no small label summarizes. A cooldown of `n / 2` days needs about `n / 2` states. A rule that compares the next purchase price with an earlier purchase price needs that price in the state. In those cases a table indexed by day and a larger parameter fits better.

<!-- stage: exercises -->
### Exercises

#### [Build] Stock With Cooldown (LeetCode 309)
<!-- id: tv-cooldown-profit -->

**Prerequisites.** The hold and cash states of the previous lesson and the three states of this lesson.

**Problem.** An array `prices` gives the price of one share on each day. A trader holds at most one share. A purchase is illegal on the day right after a sale. Return the largest total profit from any legal sequence of purchases and sales, where profit is total sale prices minus total purchase prices.

**Constraints.** The limits are:
- **Length** satisfies `1 <= prices.length <= 5000`.
- **Price** satisfies `0 <= prices[i] <= 1000`.
- **Ending** allows no open position to count, because an owned share has no profit.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [6,1,3,2,4,7]`, output `6`.

**Example 2.** Input `prices = [5,4,3]`, output `0`.

**Hint.** Which of the three states may a purchase read, and which state does a sale write?

**Changed decision.** The previous lesson used two states and allowed a purchase from any cash value. Here a purchase reads only the rest state, and the sold state delays its profit by one day.

#### [Vary] Stock With Transaction Fee (LeetCode 714)
<!-- id: tv-fee-profit -->

**Prerequisites.** The exercise above.

**Problem.** An array `prices` gives the price of one share on each day, and an integer `fee` applies to each transaction. A trader holds at most one share and can trade on any day. Return the largest profit, where each completed sale pays `fee` once.

**Constraints.** The limits are:
- **Length** satisfies `1 <= prices.length <= 10000`.
- **Price** satisfies `0 <= prices[i] <= 10000`.
- **Fee** satisfies `0 <= fee <= 10000`.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [3,8,5,10,4,9]`, `fee = 2`, output `9`.

**Example 2.** Input `prices = [4,5,6]`, `fee = 5`, output `0`.

**Hint.** If the sale pays the fee, which of the two transitions changes and which stays the same?

**Changed decision.** The state set stays at two values, and only the sale transition changes. Subtracting the fee on both the purchase and the sale would charge twice.

#### [Boundary] Update Aliasing (Author exercise)
<!-- id: tv-update-aliasing -->

**Prerequisites.** The exercises above.

**Problem.** Run two cooldown updates over `prices`. The correct update uses the three-state recurrence with all new values computed from the previous day. The faulty update runs `sold = hold + p`, then `rest = max(rest, sold)`, then `hold = max(hold, rest - p)` in place, for price `p`. Both start with `hold = -prices[0]`, `sold = 0` and `rest = 0`. After each day `i` from 1, the profit is `max(sold, rest)`. Return the smallest `i` where the two profits differ, or -1 if they never differ.

**Constraints.** The limits are:
- **Length** satisfies `1 <= prices.length <= 2000`.
- **Price** satisfies `0 <= prices[i] <= 1000`.
- **Result** is -1 for a list of length 1.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [2,5,1,4]`, output `3`.

**Example 2.** Input `prices = [3,3,3]`, output `-1`.

**Hint.** A wrong value first shows in the profit only after a purchase that the rule forbids can pay off. On which day does that profit appear?

**Changed decision.** The task compares two update orders on the same input. The correct one reads only values from the previous day, and the faulty one reads values that it has just written.

#### [Recognize] Stock III At Most Two Transactions (LeetCode 123)
<!-- id: tv-two-transactions -->

**Prerequisites.** All three exercises above.

**Problem.** The array `prices` lists one share price per day. A trader owns at most one share and sells it before the next purchase. Return the largest profit from at most two transactions, where a transaction is one purchase followed by one later sale.

**Constraints.** The limits are:
- **Length** satisfies `1 <= prices.length <= 100000`.
- **Price** satisfies `0 <= prices[i] <= 100000`.
- **Count** allows 0, 1 or 2 transactions.
- **Mutation** is not allowed, because the input array stays unchanged.

**Example 1.** Input `prices = [4,2,6,1,5,3,8]`, output `11`.

**Example 2.** Input `prices = [9,7,5]`, output `0`.

**Hint.** How many completed sales does a history have so far, and does it own a share right now?

**Changed decision.** The state carries a count of completed sales together with the possession flag. This gives four values, and each reads the four values of the previous day.
