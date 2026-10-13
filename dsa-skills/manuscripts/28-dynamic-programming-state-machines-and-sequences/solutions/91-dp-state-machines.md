<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For DP State Machines

#### Solution: [Build] Best Time To Buy And Sell Stock (LeetCode 121)
<!-- id: sm-best-trade-days -->

**Approach.**
The `free` label before day `j` is the cheapest price seen on days `0..j-1`, and the `hold` label keeps the day of that price next to it. Each day `j` first tests a sale against that held day and only then considers replacing the held day. The sale test uses a strict comparison, so the first day that reaches the largest profit wins, which is the smallest sale day. The held-day replacement uses a strict comparison too, so the earliest day among equal minimum prices stays, which is the smallest buy day.

The invariant is that at the start of day `j`, the held day is the earliest day with the minimum price among earlier days, and the best trade so far is the first one with the largest positive profit. A profit of 0 never replaces the sentinel `{-1,-1}`.

**Complexity.**
- **Time** is O(n) for n prices, because each day makes one comparison against the held day.
- **Space** is O(1), since the method keeps three integers and the result pair.

```java run
import java.util.*;

public final class SmBestTradeDays {
    /**
     * Returns {buyDay, sellDay} of the largest positive-profit trade, or {-1,-1}.
     * Time: O(n). Space: O(1).
     * Invariant: heldDay is the earliest minimum-price day before the current day.
     */
    static int[] bestTrade(int[] prices) {
        int heldDay = 0, bestProfit = 0, buy = -1, sell = -1;
        // Day 0 can only buy, so the scan starts at day 1.
        for (int j = 1; j < prices.length; j++) {
            // A strictly larger profit replaces the trade, which keeps the smallest sell day on ties.
            if (prices[j] - prices[heldDay] > bestProfit) {
                bestProfit = prices[j] - prices[heldDay];
                buy = heldDay;
                sell = j;
            }
            // A strictly smaller price replaces the held day, which keeps the earliest day on ties.
            if (prices[j] < prices[heldDay]) heldDay = j;
        }
        return new int[] {buy, sell};
    }

    /** Oracle: tries every pair of days and applies the tie rule directly. */
    static int[] oracle(int[] p) {
        long bestKey = Long.MIN_VALUE;
        int[] res = {-1, -1};
        for (int s = 0; s < p.length; s++) {
            for (int b = 0; b < s; b++) {
                long gain = p[s] - p[b];
                // The key orders by profit, then by smaller sell day, then by smaller buy day.
                long key = gain * 1_000_000L - s * 1000L - b;
                if (gain > 0 && key > bestKey) { bestKey = key; res = new int[] {b, s}; }
            }
        }
        return res;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bestTrade(new int[] {6, 2, 8, 2, 8, 1}), new int[] {1, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(bestTrade(new int[] {7, 5, 4}), new int[] {-1, -1})) throw new AssertionError("ex2");
        // Empty input, a single day and equal prices return the sentinel.
        if (!Arrays.equals(bestTrade(new int[] {}), new int[] {-1, -1})) throw new AssertionError("empty");
        if (!Arrays.equals(bestTrade(new int[] {5}), new int[] {-1, -1})) throw new AssertionError("single");
        if (!Arrays.equals(bestTrade(new int[] {3, 3, 3}), new int[] {-1, -1})) throw new AssertionError("flat");
        // The input array stays unchanged.
        int[] in = {4, 9, 4, 9};
        int[] copy = in.clone();
        bestTrade(in);
        if (!Arrays.equals(in, copy)) throw new AssertionError("mutated");
        // Random inputs against the pair-enumeration oracle.
        Random rnd = new Random(2801);
        for (int t = 0; t < 5000; t++) {
            int[] p = new int[rnd.nextInt(10)];
            for (int i = 0; i < p.length; i++) p[i] = rnd.nextInt(8);
            if (!Arrays.equals(bestTrade(p), oracle(p))) throw new AssertionError("random " + Arrays.toString(p));
        }
    }
}
```

#### Solution: [Vary] Best Time To Buy And Sell Stock With Cooldown (LeetCode 309)
<!-- id: sm-cooldown-days -->

**Approach.**
The three labels `free`, `hold` and `rest` keep one score each. The score is the profit times 1000 minus the cooldown days, so a larger score means a larger profit and, on equal profit, fewer cooldown days. A purchase subtracts the price times 1000 and reads yesterday's `free` only, which enforces the cooldown. A sale adds the price times 1000 and subtracts 1 when a following day exists. The new `rest` value comes from yesterday's `hold`, and the new `free` value takes the larger of yesterday's `free` and `rest`.

The invariant is that each score is the best over all legal plans that end the day in that label. The final score is the larger of `free` and `rest`. Decoding takes the profit as the score divided by 1000 rounded up, and the cooldown days are what remains.

**Complexity.**
- **Time** is O(n), because each day updates three scores.
- **Space** is O(1), because the new scores are computed from the three old ones.

```java run
import java.util.*;

public final class SmCooldownDays {
    /**
     * Returns {profit, cooldownDays} of the best plan under the cooldown rule.
     * Time: O(n). Space: O(1).
     * Invariant: each score is the best packed score of the legal plans ending in its label.
     */
    static long[] cooldownPlan(int[] prices) {
        final long NEG = Long.MIN_VALUE / 4;
        long free = 0, hold = NEG, rest = NEG;
        // Each day builds all three new scores from yesterday's scores.
        for (int d = 0; d < prices.length; d++) {
            long price = prices[d] * 1000L;
            long nFree = Math.max(free, rest);
            // Buying reads yesterday's free score only, so a day after a sale cannot buy.
            long nHold = Math.max(hold, free - price);
            // A sale on a day with a following day costs one cooldown unit.
            long nRest = hold + price - (d < prices.length - 1 ? 1 : 0);
            free = nFree; hold = nHold; rest = nRest;
        }
        long score = Math.max(free, rest);
        // The score is profit * 1000 - cooldownDays, so rounding up recovers the profit.
        long profit = Math.floorDiv(score + 999, 1000);
        return new long[] {profit, profit * 1000 - score};
    }

    static long bestProfit, bestCool;

    /** Oracle: enumerates every action sequence and keeps the best pair. */
    static long[] oracle(int[] p) {
        bestProfit = Long.MIN_VALUE; bestCool = 0;
        walk(p, 0, false, false, 0, 0);
        return new long[] {bestProfit, bestCool};
    }

    static void walk(int[] p, int d, boolean holding, boolean blocked, long profit, long cool) {
        if (d == p.length) {
            // A plan counts only when it holds no share at the end.
            if (!holding && (profit > bestProfit || (profit == bestProfit && cool < bestCool))) { bestProfit = profit; bestCool = cool; }
            return;
        }
        walk(p, d + 1, holding, false, profit, cool);
        if (holding) walk(p, d + 1, false, true, profit + p[d], cool + (d < p.length - 1 ? 1 : 0));
        else if (!blocked) walk(p, d + 1, true, false, profit - p[d], cool);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(cooldownPlan(new int[] {1, 4, 2, 5}), new long[] {4, 0})) throw new AssertionError("ex1");
        if (!Arrays.equals(cooldownPlan(new int[] {2, 9, 1, 9, 1, 9}), new long[] {15, 1})) throw new AssertionError("ex2");
        // Empty and single-day inputs return zeros.
        if (!Arrays.equals(cooldownPlan(new int[] {}), new long[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(cooldownPlan(new int[] {5}), new long[] {0, 0})) throw new AssertionError("single");
        // The input array stays unchanged.
        int[] in = {3, 2, 6, 5, 0, 3};
        int[] copy = in.clone();
        cooldownPlan(in);
        if (!Arrays.equals(in, copy)) throw new AssertionError("mutated");
        // Random inputs against the enumeration oracle.
        Random rnd = new Random(2802);
        for (int t = 0; t < 3000; t++) {
            int[] p = new int[rnd.nextInt(10)];
            for (int i = 0; i < p.length; i++) p[i] = rnd.nextInt(9);
            if (!Arrays.equals(cooldownPlan(p), oracle(p))) throw new AssertionError("random " + Arrays.toString(p));
        }
    }
}
```

#### Solution: [Boundary] Best Time To Buy And Sell Stock With Transaction Fee (LeetCode 714)
<!-- id: sm-fee-min-profit -->

**Approach.**
Two labels suffice, `free` and `hold`, both holding the best cash. The purchase move subtracts the price and the fee once, so a trade pays the fee at its start only. The sale move adds the price. Both new values are computed from the old pair, so a purchase on day `d` never reads a sale of day `d`. A purchase and a sale on one day would otherwise cost the fee for no gain, and a fee of 0 would hide the error in tests.

The invariant is that `free` is the best cash with no share and `hold` is the best cash with one share, over all legal plans of the days so far. The method returns `free` after the last day when it reaches `minProfit`, and 0 otherwise.

**Complexity.**
- **Time** is O(n) for n prices, because each day updates two values.
- **Space** is O(1), since only the two values are kept.

```java run
import java.util.*;

public final class SmFeeMinProfit {
    /**
     * Returns the best profit with the fee charged on each purchase, or 0 below minProfit.
     * Time: O(n). Space: O(1).
     * Invariant: free and hold are the best cash in their label after the processed days.
     */
    static long feePlan(int[] prices, int fee, int minProfit) {
        final long NEG = Long.MIN_VALUE / 4;
        long free = 0, hold = NEG;
        for (int price : prices) {
            // Both new values read the old pair, so the day's sale cannot fund the day's purchase.
            long nHold = Math.max(hold, free - price - fee);
            long nFree = Math.max(free, hold + price);
            hold = nHold; free = nFree;
        }
        // The threshold is tested once, on the final cash with no share.
        return free >= minProfit ? free : 0;
    }

    static long best;

    /** Oracle: enumerates every action sequence. */
    static long oracle(int[] p, int fee, int minProfit) {
        best = 0;
        walk(p, 0, false, 0, fee);
        return best >= minProfit ? best : 0;
    }

    static void walk(int[] p, int d, boolean holding, long cash, int fee) {
        if (d == p.length) { if (!holding) best = Math.max(best, cash); return; }
        walk(p, d + 1, holding, cash, fee);
        if (holding) walk(p, d + 1, false, cash + p[d], fee);
        else walk(p, d + 1, true, cash - p[d] - fee, fee);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (feePlan(new int[] {2, 8, 4, 9}, 2, 5) != 7) throw new AssertionError("ex1");
        if (feePlan(new int[] {2, 8, 4, 9}, 2, 9) != 0) throw new AssertionError("ex2");
        // Empty input, fee 0 and flat prices.
        if (feePlan(new int[] {}, 1, 0) != 0) throw new AssertionError("empty");
        if (feePlan(new int[] {1, 3}, 0, 0) != 2) throw new AssertionError("fee zero");
        if (feePlan(new int[] {3, 3, 3}, 0, 1) != 0) throw new AssertionError("flat");
        // A threshold of 0 returns the plain best profit.
        if (feePlan(new int[] {5, 1}, 3, 0) != 0) throw new AssertionError("falling");
        // Random inputs against the enumeration oracle.
        Random rnd = new Random(2803);
        for (int t = 0; t < 4000; t++) {
            int[] p = new int[rnd.nextInt(10)];
            for (int i = 0; i < p.length; i++) p[i] = rnd.nextInt(9);
            int fee = rnd.nextInt(5), min = rnd.nextInt(8);
            if (feePlan(p, fee, min) != oracle(p, fee, min)) throw new AssertionError("random " + Arrays.toString(p));
        }
    }
}
```

#### Solution: [Recognize] Best Time To Buy And Sell Stock III (LeetCode 123)
<!-- id: sm-k-trades -->

**Approach.**
The table has one `free` entry and one `hold` entry for each purchase count `c` from 0 to `k`. A purchase moves from `free` at count `c - 1` to `hold` at count `c` and adds one trade unit to the penalty. A sale moves from `hold` to `free` at the same count. The score packs profit times 1000 minus the number of purchases, so equal profit prefers fewer trades. The new tables are built from the old ones, which keeps a purchase from reading the same day's sale.

The invariant is that each entry is the best packed score over legal plans that end the day in its label and count. The answer is the largest `free` entry after the last day. The method runs fewer count levels than `k` when `k` exceeds the days, because a trade needs two days.

**Complexity.**
- **Time** is O(n * k) for n prices, because each day updates 2(k + 1) entries.
- **Space** is O(k) for the two tables, since only yesterday's entries stay alive.

```java run
import java.util.*;

public final class SmKTrades {
    /**
     * Returns {profit, trades} for the best plan with at most k purchases.
     * Time: O(n * k). Space: O(k).
     * Invariant: free[c] and hold[c] are the best packed scores with c purchases made.
     */
    static long[] limited(int[] prices, int k) {
        final long NEG = Long.MIN_VALUE / 4;
        // More purchases than half the days cannot be used, which bounds the table.
        int cap = Math.min(k, prices.length / 2);
        long[] free = new long[cap + 1], hold = new long[cap + 1];
        Arrays.fill(free, NEG);
        Arrays.fill(hold, NEG);
        free[0] = 0;
        for (int price : prices) {
            long[] nFree = new long[cap + 1], nHold = new long[cap + 1];
            for (int c = 0; c <= cap; c++) {
                // A sale returns to free at the same count; waiting keeps the old value.
                nFree[c] = Math.max(free[c], hold[c] + price * 1000L);
                // A purchase reads yesterday's free at the previous count and costs one trade unit.
                long buy = c > 0 ? free[c - 1] - price * 1000L - 1 : NEG;
                nHold[c] = Math.max(hold[c], buy);
            }
            free = nFree; hold = nHold;
        }
        long score = NEG;
        // The best final score over all counts, with no share held.
        for (long v : free) score = Math.max(score, v);
        long profit = Math.floorDiv(score + 999, 1000);
        return new long[] {profit, profit * 1000 - score};
    }

    static long bestProfit, bestTrades;

    /** Oracle: enumerates every action sequence. */
    static long[] oracle(int[] p, int k) {
        bestProfit = Long.MIN_VALUE; bestTrades = 0;
        walk(p, k, 0, false, 0, 0);
        return new long[] {bestProfit, bestTrades};
    }

    static void walk(int[] p, int k, int d, boolean holding, int used, long profit) {
        if (d == p.length) {
            if (!holding && (profit > bestProfit || (profit == bestProfit && used < bestTrades))) { bestProfit = profit; bestTrades = used; }
            return;
        }
        walk(p, k, d + 1, holding, used, profit);
        if (holding) walk(p, k, d + 1, false, used, profit + p[d]);
        else if (used < k) walk(p, k, d + 1, true, used + 1, profit - p[d]);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(limited(new int[] {3, 8, 1, 6, 2, 9}, 2), new long[] {13, 2})) throw new AssertionError("ex1");
        if (!Arrays.equals(limited(new int[] {1, 5, 2, 6, 1, 5}, 3), new long[] {12, 3})) throw new AssertionError("ex2");
        // Limit 0, empty input and falling prices return zeros.
        if (!Arrays.equals(limited(new int[] {1, 5}, 0), new long[] {0, 0})) throw new AssertionError("k zero");
        if (!Arrays.equals(limited(new int[] {}, 5), new long[] {0, 0})) throw new AssertionError("empty");
        if (!Arrays.equals(limited(new int[] {5, 4, 3}, 3), new long[] {0, 0})) throw new AssertionError("falling");
        // Random inputs, including limits above the day count, against the oracle.
        Random rnd = new Random(2804);
        for (int t = 0; t < 3000; t++) {
            int[] p = new int[rnd.nextInt(10)];
            for (int i = 0; i < p.length; i++) p[i] = rnd.nextInt(9);
            int k = rnd.nextInt(7);
            if (!Arrays.equals(limited(p, k), oracle(p, k))) throw new AssertionError("random " + Arrays.toString(p) + " " + k);
        }
    }
}
```
