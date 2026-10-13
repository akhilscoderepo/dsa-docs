<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Stock States

#### Solution: [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ss-one-trade-states -->

**Approach.**
The loop keeps `hold`, the best profit of plans that own a share, and `cash`, the best profit of plans that own none. For one trade, a buy always starts from profit 0, so the buy value on a day with price `p` is `-p`. The sell value is the old `hold` plus `p`. The loop computes both new values from the old pair before it stores either.

The invariant is that after day `i`, `cash` is the largest profit of at most one completed trade within days 0 to `i`. The method stores `cash` into `best[i]` at the end of each iteration. Because the start value of `hold` is half of the smallest `int`, adding a price to it cannot overflow.

**Complexity.**
- **Time** is O(n), because each day does a constant number of comparisons.
- **Space** is O(n) for the returned array, and the working values use O(1) extra memory.

```java run
import java.util.*;

public final class SsOneTradeStates {
    /**
     * Returns, for each day, the best profit of at most one completed trade so far.
     * Time: O(n). Space: O(n) for the result, O(1) for the working values.
     * Invariant: after day i, cash is the best profit of at most one trade within days 0..i.
     */
    static int[] bestByDay(int[] prices) {
        // The result has one entry per day.
        int[] best = new int[prices.length];
        // hold is impossible before any buy; half of MIN_VALUE leaves room for additions.
        int hold = Integer.MIN_VALUE / 2;
        // cash starts at 0 because doing nothing is a legal plan.
        int cash = 0;
        // One pass visits every day once, which costs O(n).
        for (int i = 0; i < prices.length; i++) {
            // Buying starts the only trade, so its value is the negated price.
            int nextHold = Math.max(hold, -prices[i]);
            // Selling adds today's price to the best owning plan.
            int nextCash = Math.max(cash, hold + prices[i]);
            // Both new values came from old values, so the order of these stores does not matter.
            hold = nextHold;
            cash = nextCash;
            // The day's cash is the answer for the prefix ending today.
            best[i] = cash;
        }
        // The caller receives a fresh array and the input stays unchanged.
        return best;
    }

    /** Oracle: tries every buy day and later sell day for each prefix. */
    static int[] oracle(int[] prices) {
        int[] best = new int[prices.length];
        for (int i = 0; i < prices.length; i++) {
            int b = 0;
            for (int a = 0; a < i; a++) {
                for (int s = a + 1; s <= i; s++) {
                    b = Math.max(b, prices[s] - prices[a]);
                }
            }
            best[i] = b;
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bestByDay(new int[] {7, 1, 5, 3, 6, 4}), new int[] {0, 0, 4, 4, 5, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(bestByDay(new int[] {5, 4, 3}), new int[] {0, 0, 0})) throw new AssertionError("ex2");
        // An empty input returns an empty array.
        if (bestByDay(new int[] {}).length != 0) throw new AssertionError("empty");
        // The sentinel plus a price does not overflow, while the smallest int minus one wraps to the largest.
        if (Integer.MIN_VALUE / 2 + 10000 >= 0) throw new AssertionError("sentinel");
        if (Integer.MIN_VALUE - 1 != Integer.MAX_VALUE) throw new AssertionError("wrap");
        // The input stays unchanged.
        int[] p = {3, 1, 2};
        bestByDay(p);
        if (!Arrays.equals(p, new int[] {3, 1, 2})) throw new AssertionError("mutated");
        // Random inputs against the pair oracle.
        Random rnd = new Random(2801);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(20);
            if (!Arrays.equals(bestByDay(a), oracle(a))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ss-many-trades -->

**Approach.**
Each situation keeps a pair: the best profit and, among plans with that profit, the fewest buys. A buy moves from cash to hold, subtracts the price and adds one to the buy count. A sell moves from hold to cash, adds the price and keeps the count. Doing nothing keeps the pair. The loop compares two candidate pairs by larger profit first, then by smaller count.

The invariant is that after each day, each pair describes the best plan for its exact situation under that order. Impossible plans carry the sentinel profit, and the first buy replaces it. The answer is the pair of `cash`. Fixing the count at the buy keeps the comparison correct, because a plan that is still owning a share has already paid for its trade.

**Complexity.**
- **Time** is O(n), because each day compares a constant number of pairs.
- **Space** is O(1) extra, since four integers carry the whole state.

```java run
import java.util.*;

public final class SsManyTrades {
    static final int NONE = Integer.MIN_VALUE / 2;

    /** Reports whether the pair (p1, t1) beats the pair (p2, t2): larger profit first, then fewer trades. */
    static boolean better(int p1, int t1, int p2, int t2) {
        return p1 > p2 || (p1 == p2 && t1 < t2);
    }

    /**
     * Returns {largest profit, fewest buys that reach it} for any number of trades.
     * Time: O(n). Space: O(1).
     * Invariant: each situation holds the best pair over the processed days, ordered by profit then trades.
     */
    static int[] profitAndTrades(int[] prices) {
        // hold is impossible at the start; cash is the empty plan with no buys.
        int holdP = NONE, holdT = 0, cashP = 0, cashT = 0;
        // One pass over the days costs O(n).
        for (int price : prices) {
            // Staying in hold is the first candidate for the new hold pair.
            int nhP = holdP, nhT = holdT;
            // Buying pays the price and adds one buy; it wins only when it is better.
            if (better(cashP - price, cashT + 1, nhP, nhT)) {
                nhP = cashP - price;
                nhT = cashT + 1;
            }
            // Staying in cash is the first candidate for the new cash pair.
            int ncP = cashP, ncT = cashT;
            // Selling earns the price and keeps the buy count; it wins only when it is better.
            if (better(holdP + price, holdT, ncP, ncT)) {
                ncP = holdP + price;
                ncT = holdT;
            }
            // Both new pairs were computed from the old pairs, so now the stores are safe.
            holdP = nhP;
            holdT = nhT;
            cashP = ncP;
            cashT = ncT;
        }
        // The answer is the cash pair, because a plan must end without a share.
        return new int[] {cashP, cashT};
    }

    /** Oracle: tries every sequence of Buy, Sell and Rest and keeps the best legal pair. */
    static int[] oracle(int[] prices) {
        int n = prices.length;
        int total = 1;
        for (int i = 0; i < n; i++) total *= 3;
        int bestP = 0, bestT = 0;
        for (int code = 0; code < total; code++) {
            int c = code;
            boolean own = false, ok = true;
            int profit = 0, trades = 0;
            for (int d = 0; d < n && ok; d++) {
                int a = c % 3;
                c /= 3;
                if (a == 0) {
                    if (own) ok = false;
                    else { own = true; profit -= prices[d]; trades++; }
                } else if (a == 1) {
                    if (!own) ok = false;
                    else { own = false; profit += prices[d]; }
                }
            }
            if (ok && !own && better(profit, trades, bestP, bestT)) {
                bestP = profit;
                bestT = trades;
            }
        }
        return new int[] {bestP, bestT};
    }

    static int calls;

    /** The recursion from the lesson, instrumented to count its calls. */
    static int explore(int[] prices, int day, boolean owns) {
        calls++;
        if (day == prices.length) return owns ? -1_000_000 : 0;
        int rest = explore(prices, day + 1, owns);
        if (owns) return Math.max(rest, prices[day] + explore(prices, day + 1, false));
        return Math.max(rest, -prices[day] + explore(prices, day + 1, true));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(profitAndTrades(new int[] {3, 1, 4, 1, 5}), new int[] {7, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(profitAndTrades(new int[] {2, 2, 2}), new int[] {0, 0})) throw new AssertionError("ex2");
        // An empty input returns {0, 0}.
        if (!Arrays.equals(profitAndTrades(new int[] {}), new int[] {0, 0})) throw new AssertionError("empty");
        // The lesson's recursion makes 15 calls on 3 days, 2^(n+1) - 1 in general, and returns the same profit.
        calls = 0;
        int[] three = {1, 2, 3};
        if (explore(three, 0, false) != profitAndTrades(three)[0] || calls != 15) throw new AssertionError("calls");
        calls = 0;
        explore(new int[10], 0, false);
        if (calls != (1 << 11) - 1) throw new AssertionError("calls10");
        // The input stays unchanged.
        int[] p = {3, 1, 2};
        profitAndTrades(p);
        if (!Arrays.equals(p, new int[] {3, 1, 2})) throw new AssertionError("mutated");
        // Random inputs against the sequence oracle, with a small price range to force ties.
        Random rnd = new Random(2802);
        for (int t = 0; t < 1500; t++) {
            int[] a = new int[rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(7);
            if (!Arrays.equals(profitAndTrades(a), oracle(a))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] One Day And Falling Prices (Author exercise)
<!-- id: ss-falling-prices -->

**Approach.**
The method runs the one-trade loop with `hold` and `cash` and then reads the final `cash`. The value of `cash` starts at 0, so it equals 0 whenever no trade earned more than 0. A trade with profit 0 gives the same `cash` as no trade, and the contract treats both as unprofitable. The method therefore returns -1 for a final `cash` of 0 and returns `cash` otherwise.

The invariant is that `cash` is the largest profit of at most one trade over the processed prefix, so it is never negative. A one-day array never reaches the sell move with a real `hold`, a strictly falling array never beats the start value, and a flat array only ties it. All three end at 0 and return -1.

**Complexity.**
- **Time** is O(n), because the loop visits each day once.
- **Space** is O(1), since only `hold` and `cash` are stored.

```java run
import java.util.*;

public final class SsFallingPrices {
    /**
     * Returns the largest positive profit of one trade, or -1 when no trade earns more than 0.
     * Time: O(n). Space: O(1).
     * Invariant: cash is the best profit of at most one trade in the processed prefix and never drops below 0.
     */
    static int positiveProfitOrMinusOne(int[] prices) {
        // hold is impossible until the first buy.
        int hold = Integer.MIN_VALUE / 2;
        // cash 0 stands for no profitable trade yet.
        int cash = 0;
        // One pass over the days costs O(n).
        for (int p : prices) {
            // The one trade buys at the lowest price seen, so the buy value is -p.
            int nextHold = Math.max(hold, -p);
            // Selling adds today's price to the best owning plan.
            int nextCash = Math.max(cash, hold + p);
            // Stores happen after both values are computed.
            hold = nextHold;
            cash = nextCash;
        }
        // A final cash of 0 means no trade beat the start, so the contract returns -1.
        return cash == 0 ? -1 : cash;
    }

    /** Oracle: tries every buy day and later sell day. */
    static int oracle(int[] prices) {
        int best = -1;
        for (int a = 0; a < prices.length; a++) {
            for (int s = a + 1; s < prices.length; s++) {
                if (prices[s] - prices[a] > best && prices[s] - prices[a] > 0) best = prices[s] - prices[a];
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (positiveProfitOrMinusOne(new int[] {9}) != -1) throw new AssertionError("ex1");
        if (positiveProfitOrMinusOne(new int[] {4, 4, 2, 1, 4}) != 3) throw new AssertionError("ex2");
        // Falling and flat arrays return -1.
        if (positiveProfitOrMinusOne(new int[] {5, 4, 3, 2}) != -1) throw new AssertionError("falling");
        if (positiveProfitOrMinusOne(new int[] {6, 6, 6}) != -1) throw new AssertionError("flat");
        // A rise after a fall is found, and the largest price may come before the smallest.
        if (positiveProfitOrMinusOne(new int[] {6, 9, 1, 3}) != 3) throw new AssertionError("order");
        // The input stays unchanged.
        int[] p = {3, 1, 2};
        positiveProfitOrMinusOne(p);
        if (!Arrays.equals(p, new int[] {3, 1, 2})) throw new AssertionError("mutated");
        // Random inputs against the pair oracle, including many falling arrays.
        Random rnd = new Random(2803);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            int base = 5 + rnd.nextInt(10);
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3) == 0 ? rnd.nextInt(base) : Math.max(0, base - i - rnd.nextInt(2));
            if (positiveProfitOrMinusOne(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] State Diagram (Author exercise)
<!-- id: ss-state-diagram -->

**Approach.**
The state diagram has two situations, cash and hold, and each day draws four lines. Rest keeps cash, rest keeps hold, Buy goes from cash to hold, and Sell goes from hold to cash. Each line is one action, so counting action sequences means counting paths through this diagram. The method derives these lines first and then keeps, for each situation, the best profit and the number of paths that reach it.

When two lines enter the same situation on a day, the larger profit wins and keeps its count. When the profits tie, the counts add. An impossible situation has count 0, so it never contributes to a sum. The invariant is that each pair holds the best profit over the processed days and the exact number of legal prefixes that reach it. The answer is the cash pair.

**Complexity.**
- **Time** is O(n), because each day combines a constant number of lines.
- **Space** is O(1) extra, since two profits and two counts carry the state.

```java run
import java.util.*;

public final class SsStateDiagram {
    static final int NONE = Integer.MIN_VALUE / 2;

    /**
     * Returns {largest profit, number of legal Buy/Sell/Rest sequences that earn it}.
     * Time: O(n). Space: O(1).
     * Invariant: each situation stores its best profit and the number of legal prefixes that reach it.
     */
    static int[] bestAndWays(int[] prices) {
        // Cash has the empty prefix as one way; hold has no way yet.
        int cashP = 0, cashW = 1, holdP = NONE, holdW = 0;
        // One pass over the days costs O(n).
        for (int price : prices) {
            // Two lines enter cash: Rest from cash and Sell from hold.
            int sellP = holdP + price;
            int ncP = Math.max(cashP, sellP);
            // Equal profits add their ways; a line with a smaller profit adds nothing.
            int ncW = (cashP == ncP ? cashW : 0) + (sellP == ncP ? holdW : 0);
            // Two lines enter hold: Rest from hold and Buy from cash.
            int buyP = cashP - price;
            int nhP = Math.max(holdP, buyP);
            int nhW = (holdP == nhP ? holdW : 0) + (buyP == nhP ? cashW : 0);
            // The stores wait until both pairs are ready, because each reads the old pair of the other.
            cashP = ncP;
            cashW = ncW;
            holdP = nhP;
            holdW = nhW;
        }
        // The sequence must end without a share, so the cash pair is the answer.
        return new int[] {cashP, cashW};
    }

    /** Oracle: enumerates all 3^n action strings and filters the legal ones. */
    static int[] oracle(int[] prices) {
        int n = prices.length;
        int total = 1;
        for (int i = 0; i < n; i++) total *= 3;
        int best = Integer.MIN_VALUE, ways = 0;
        for (int code = 0; code < total; code++) {
            int c = code;
            boolean own = false, ok = true;
            int profit = 0;
            for (int d = 0; d < n && ok; d++) {
                int a = c % 3;
                c /= 3;
                if (a == 0) {
                    if (own) ok = false;
                    else { own = true; profit -= prices[d]; }
                } else if (a == 1) {
                    if (!own) ok = false;
                    else { own = false; profit += prices[d]; }
                }
            }
            if (!ok || own) continue;
            if (profit > best) { best = profit; ways = 1; }
            else if (profit == best) ways++;
        }
        return new int[] {best, ways};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bestAndWays(new int[] {1, 2, 3}), new int[] {2, 1})) throw new AssertionError("ex1");
        if (!Arrays.equals(bestAndWays(new int[] {2, 2, 2}), new int[] {0, 4})) throw new AssertionError("ex2");
        // The empty array has exactly one legal sequence, the empty one.
        if (!Arrays.equals(bestAndWays(new int[] {}), new int[] {0, 1})) throw new AssertionError("empty");
        // The input stays unchanged.
        int[] p = {3, 1, 2};
        bestAndWays(p);
        if (!Arrays.equals(p, new int[] {3, 1, 2})) throw new AssertionError("mutated");
        // Random inputs against the enumeration oracle, with a small price range to force ties.
        Random rnd = new Random(2804);
        for (int t = 0; t < 1500; t++) {
            int[] a = new int[rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(5);
            if (!Arrays.equals(bestAndWays(a), oracle(a))) throw new AssertionError("random " + t);
        }
    }
}
```
