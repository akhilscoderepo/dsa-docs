<!-- solutions-for: 28-dynamic-programming-state-machines-and-sequences -->
### Solutions For Transaction Variants

#### Solution: [Build] Stock With Cooldown (LeetCode 309)
<!-- id: tv-cooldown-profit -->

**Approach.**
The method keeps three profits. The value `hold` covers histories that own a share. The value `sold` covers histories that sold today. The value `rest` covers histories that own nothing and did not sell today. A purchase reads only `rest`, so it cannot follow a sale on the previous day. A sale reads `hold`. The sale profit enters `rest` one day later, which is the waiting day.

All three new values come from the previous day's values and the method stores them in temporaries before any assignment. The invariant is that after day `i`, each variable is the best profit of histories that end day `i` in that situation. The answer is the larger of `sold` and `rest`, because an owned share has no realized profit. The test compares the method with an exhaustive search over the legal actions.

**Complexity.**
- **Time** is O(n), because each day does a constant number of comparisons.
- **Space** is O(1), because three profits and three temporaries are the only extra memory, and the input array stays unchanged.

```java run
import java.util.*;

public final class TvCooldownProfit {
    /**
     * Returns the largest profit when a purchase on the day after a sale is illegal.
     * Time: O(n). Space: O(1).
     * Invariant: after day i, hold, sold and rest are the best profits of histories ending day i in that situation.
     */
    static int cooldownProfit(int[] prices) {
        // Day 0 allows only a purchase, so hold pays the first price.
        int hold = -prices[0];
        // No sale is possible on day 0.
        int sold = 0;
        // Owning nothing with no sale today starts at profit 0.
        int rest = 0;
        // Each later day costs a constant number of steps.
        for (int i = 1; i < prices.length; i++) {
            // A purchase reads rest only, so it never follows a sale of the previous day.
            int nextHold = Math.max(hold, rest - prices[i]);
            // A sale turns the held share into profit today.
            int nextSold = hold + prices[i];
            // Yesterday's sale becomes free to act on after one waiting day.
            int nextRest = Math.max(rest, sold);
            // The three assignments happen after all three reads.
            hold = nextHold;
            sold = nextSold;
            rest = nextRest;
        }
        // An owned share has no realized profit, so hold is excluded.
        return Math.max(sold, rest);
    }

    /** Oracle: explores skip, buy and sell with the cooldown flag. */
    static int oracle(int[] p, int i, boolean holding, boolean cool) {
        if (i == p.length) return 0;
        int best = oracle(p, i + 1, holding, false);
        if (holding) best = Math.max(best, p[i] + oracle(p, i + 1, false, true));
        else if (!cool) best = Math.max(best, -p[i] + oracle(p, i + 1, true, false));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (cooldownProfit(new int[] {6, 1, 3, 2, 4, 7}) != 6) throw new AssertionError("ex1");
        if (cooldownProfit(new int[] {5, 4, 3}) != 0) throw new AssertionError("ex2");
        // The opening list returns 3, while the two-state update would return 4.
        if (cooldownProfit(new int[] {2, 3, 4, 1, 3}) != 3) throw new AssertionError("opening");
        // A single day cannot realize any profit.
        if (cooldownProfit(new int[] {7}) != 0) throw new AssertionError("single");
        // The input array stays unchanged.
        int[] p = {2, 3, 4, 1, 3};
        cooldownProfit(p);
        if (!Arrays.equals(p, new int[] {2, 3, 4, 1, 3})) throw new AssertionError("mutated");
        // Random lists against the exhaustive search.
        Random rnd = new Random(2802);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] q = new int[n];
            for (int i = 0; i < n; i++) q[i] = rnd.nextInt(10);
            if (cooldownProfit(q) != oracle(q, 0, false, false)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Stock With Transaction Fee (LeetCode 714)
<!-- id: tv-fee-profit -->

**Approach.**
Two states describe the rule completely, because the fee does not restrict any action. The value `hold` is the best profit while owning a share, and `cash` is the best profit while owning none. A purchase subtracts the price. A sale adds the price and subtracts the fee, so each completed transaction pays the fee exactly once.

Both new values read the previous day's values through temporaries. The invariant is that after day `i`, `cash` is the best profit with no open position, and `hold` is the best profit with an open position, and every completed sale has paid its fee. The answer is `cash` after the last day. The test compares the method with an exhaustive search that charges the fee on every sale.

**Complexity.**
- **Time** is O(n), because each day compares two candidates for each of two values.
- **Space** is O(1), because two profits and two temporaries are the only extra memory, and the input array stays unchanged.

```java run
import java.util.*;

public final class TvFeeProfit {
    /**
     * Returns the largest profit when each sale pays a flat fee once.
     * Time: O(n). Space: O(1).
     * Invariant: after day i, cash and hold are the best profits without and with an open position.
     */
    static int feeProfit(int[] prices, int fee) {
        // Day 0 allows only a purchase, so hold pays the first price.
        int hold = -prices[0];
        // Cash starts at profit 0 with no position.
        int cash = 0;
        // Each later day costs a constant number of steps.
        for (int i = 1; i < prices.length; i++) {
            // Keep the share or buy with the previous day's cash.
            int nextHold = Math.max(hold, cash - prices[i]);
            // Keep the cash or sell the held share and pay the fee once.
            int nextCash = Math.max(cash, hold + prices[i] - fee);
            // Both assignments happen after both reads.
            hold = nextHold;
            cash = nextCash;
        }
        // Only a closed position has a realized profit.
        return cash;
    }

    /** Oracle: explores skip, buy and sell with the fee charged at each sale. */
    static int oracle(int[] p, int fee, int i, boolean holding) {
        if (i == p.length) return 0;
        int best = oracle(p, fee, i + 1, holding);
        if (holding) best = Math.max(best, p[i] - fee + oracle(p, fee, i + 1, false));
        else best = Math.max(best, -p[i] + oracle(p, fee, i + 1, true));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (feeProfit(new int[] {3, 8, 5, 10, 4, 9}, 2) != 9) throw new AssertionError("ex1");
        if (feeProfit(new int[] {4, 5, 6}, 5) != 0) throw new AssertionError("ex2");
        // A fee of 0 allows every transaction and matches the unlimited case.
        if (feeProfit(new int[] {1, 3, 2, 4}, 0) != 4) throw new AssertionError("zero fee");
        // A single day returns 0.
        if (feeProfit(new int[] {9}, 3) != 0) throw new AssertionError("single");
        // The input array stays unchanged.
        int[] p = {3, 8, 5};
        feeProfit(p, 1);
        if (!Arrays.equals(p, new int[] {3, 8, 5})) throw new AssertionError("mutated");
        // Random lists and fees against the exhaustive search.
        Random rnd = new Random(2803);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] q = new int[n];
            for (int i = 0; i < n; i++) q[i] = rnd.nextInt(12);
            int fee = rnd.nextInt(8);
            if (feeProfit(q, fee) != oracle(q, fee, 0, false)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Update Aliasing (Author exercise)
<!-- id: tv-update-aliasing -->

**Approach.**
The method runs the two updates side by side from the same start. The correct update computes `nextHold`, `nextSold` and `nextRest` from the previous day and assigns them together. The faulty update assigns `sold`, then lets `rest` read the new `sold`, then lets `hold` read the new `rest`. Each assignment feeds the next, so the faulty `rest` contains a sale made on the current day, and a purchase on the following day reads it.

After each day the method compares the two values of `max(sold, rest)` and returns the first day with a difference. The invariant is that before day `i`, both runs have produced equal profits on every earlier day. The test compares the correct run with an exhaustive search on every prefix, and it computes the faulty run by a separate array-based simulation.

**Complexity.**
- **Time** is O(n), because each day updates six values in constant time.
- **Space** is O(1), because only six profits and three temporaries exist, and the input array stays unchanged.

```java run
import java.util.*;

public final class TvUpdateAliasing {
    /**
     * Returns the first day where the in-place update and the correct update differ, or -1.
     * Time: O(n). Space: O(1).
     * Invariant: before day i, the two runs agree on the profit of every earlier day.
     */
    static int firstDifference(int[] prices) {
        // Both runs share the same start values after day 0.
        int hold = -prices[0], sold = 0, rest = 0;
        int fHold = hold, fSold = 0, fRest = 0;
        // Each later day updates both runs in constant time.
        for (int i = 1; i < prices.length; i++) {
            int p = prices[i];
            // The correct update reads only the previous day.
            int nextHold = Math.max(hold, rest - p);
            int nextSold = hold + p;
            int nextRest = Math.max(rest, sold);
            hold = nextHold;
            sold = nextSold;
            rest = nextRest;
            // The faulty update lets each assignment feed the next one.
            fSold = fHold + p;
            fRest = Math.max(fRest, fSold);
            fHold = Math.max(fHold, fRest - p);
            // The first unequal profit ends the scan.
            if (Math.max(sold, rest) != Math.max(fSold, fRest)) return i;
        }
        // Equal profits on every day give -1.
        return -1;
    }

    /** Oracle: the correct profit of one prefix by exhaustive search. */
    static int exhaustive(int[] p, int i, int end, boolean holding, boolean cool) {
        if (i == end) return 0;
        int best = exhaustive(p, i + 1, end, holding, false);
        if (holding) best = Math.max(best, p[i] + exhaustive(p, i + 1, end, false, true));
        else if (!cool) best = Math.max(best, -p[i] + exhaustive(p, i + 1, end, true, false));
        return best;
    }

    /** Oracle: the faulty profit after each day, simulated with an array of three slots. */
    static int oracleFirst(int[] p) {
        int[] s = {-p[0], 0, 0};
        for (int i = 1; i < p.length; i++) {
            s[1] = s[0] + p[i];
            s[2] = Math.max(s[2], s[1]);
            s[0] = Math.max(s[0], s[2] - p[i]);
            // The faulty value at day i is compared with the exhaustive profit of the prefix.
            if (Math.max(s[1], s[2]) != exhaustive(p, 0, i + 1, false, false)) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (firstDifference(new int[] {2, 5, 1, 4}) != 3) throw new AssertionError("ex1");
        if (firstDifference(new int[] {3, 3, 3}) != -1) throw new AssertionError("ex2");
        // A single day has no later day to compare.
        if (firstDifference(new int[] {7}) != -1) throw new AssertionError("single");
        // A falling list never makes the forbidden purchase pay off.
        if (firstDifference(new int[] {5, 4, 3, 2}) != -1) throw new AssertionError("falling");
        // The input array stays unchanged.
        int[] p = {2, 5, 1, 4};
        firstDifference(p);
        if (!Arrays.equals(p, new int[] {2, 5, 1, 4})) throw new AssertionError("mutated");
        // Random lists against the exhaustive search on every prefix.
        Random rnd = new Random(2804);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(10);
            int[] q = new int[n];
            for (int i = 0; i < n; i++) q[i] = rnd.nextInt(10);
            if (firstDifference(q) != oracleFirst(q)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Stock III At Most Two Transactions (LeetCode 123)
<!-- id: tv-two-transactions -->

**Approach.**
The state needs the number of completed sales and the possession flag. The method keeps `hold1` for owning the first share, `done1` for one completed sale, `hold2` for owning the second share, and `done2` for two completed sales. A purchase moves from a done value to the next hold value, and a sale moves from a hold value to the next done value.

Each of the four new values reads only the four values of the previous day. The invariant is that after day `i`, each value is the best profit of histories with that count and that possession flag. A history with fewer sales stays inside `done1` or `done2`, because each done value keeps its previous best. The answer is `done2`, since it is at least `done1` and at least 0. The test compares the method with an exhaustive search that tracks the number of sales left.

**Complexity.**
- **Time** is O(n), because each day updates four values in constant time.
- **Space** is O(1), because four profits and four temporaries are the only extra memory, and the input array stays unchanged.

```java run
import java.util.*;

public final class TvTwoTransactions {
    /**
     * Returns the largest profit from at most two transactions.
     * Time: O(n). Space: O(1).
     * Invariant: after day i, each value is the best profit for its sale count and possession flag.
     */
    static int twoTransactions(int[] prices) {
        // Day 0 allows only a first purchase.
        int hold1 = -prices[0];
        // No sale is possible yet, so profit stays 0.
        int done1 = 0;
        // Selling and rebuying on day 0 gives the same price, so hold2 starts equal to hold1.
        int hold2 = -prices[0];
        // Two completed sales start at profit 0.
        int done2 = 0;
        // Each later day costs a constant number of steps.
        for (int i = 1; i < prices.length; i++) {
            int p = prices[i];
            // The first purchase starts from profit 0.
            int nextHold1 = Math.max(hold1, -p);
            // The first sale closes the first purchase.
            int nextDone1 = Math.max(done1, hold1 + p);
            // The second purchase starts from the first completed sale of the previous day.
            int nextHold2 = Math.max(hold2, done1 - p);
            // The second sale closes the second purchase.
            int nextDone2 = Math.max(done2, hold2 + p);
            // All four assignments happen after all four reads.
            hold1 = nextHold1;
            done1 = nextDone1;
            hold2 = nextHold2;
            done2 = nextDone2;
        }
        // Done2 keeps the best of zero, one and two completed transactions.
        return Math.max(done2, done1);
    }

    /** Oracle: explores skip, buy and sell with a count of sales left. */
    static int oracle(int[] p, int i, boolean holding, int left) {
        if (i == p.length) return 0;
        int best = oracle(p, i + 1, holding, left);
        if (holding) best = Math.max(best, p[i] + oracle(p, i + 1, false, left));
        else if (left > 0) best = Math.max(best, -p[i] + oracle(p, i + 1, true, left - 1));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (twoTransactions(new int[] {4, 2, 6, 1, 5, 3, 8}) != 11) throw new AssertionError("ex1");
        if (twoTransactions(new int[] {9, 7, 5}) != 0) throw new AssertionError("ex2");
        // A single day returns 0.
        if (twoTransactions(new int[] {3}) != 0) throw new AssertionError("single");
        // One rising run uses one transaction only.
        if (twoTransactions(new int[] {1, 2, 3, 4}) != 3) throw new AssertionError("rising");
        // The input array stays unchanged.
        int[] p = {4, 2, 6};
        twoTransactions(p);
        if (!Arrays.equals(p, new int[] {4, 2, 6})) throw new AssertionError("mutated");
        // Random lists against the exhaustive search.
        Random rnd = new Random(2805);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] q = new int[n];
            for (int i = 0; i < n; i++) q[i] = rnd.nextInt(10);
            if (twoTransactions(q) != oracle(q, 0, false, 2)) throw new AssertionError("random " + t);
        }
    }
}
```
