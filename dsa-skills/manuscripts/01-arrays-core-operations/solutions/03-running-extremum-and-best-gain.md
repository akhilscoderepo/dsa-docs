<!-- solutions-for: 03-running-extremum-and-best-gain -->
### Running Extremum And Best Gain

#### Solution: [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ar-best-time-single -->

**Approach.** Carry `lowest`, the cheapest price seen before today, and `best`, the largest gain found. At each later day, form the gain `price - lowest` and keep the larger result, then let today's price lower `lowest` if it is cheaper. The best gain starts at 0 because skipping the trade is allowed. The assertions include the early-peak case where the careless maximum minus minimum gives an impossible 7, and a randomized comparison with the pair-loop oracle.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class BestTimeSingle {
    static int bestFlip(int[] prices) {
        int lowest = prices[0], best = 0;
        for (int i = 1; i < prices.length; i++) {
            best = Math.max(best, prices[i] - lowest);
            lowest = Math.min(lowest, prices[i]);
        }
        return best;
    }
    static int oracle(int[] prices) {
        int best = 0;
        for (int b = 0; b < prices.length; b++) for (int s = b + 1; s < prices.length; s++) best = Math.max(best, prices[s] - prices[b]);
        return best;
    }
    static int maxMinusMin(int[] prices) {
        int mx = prices[0], mn = prices[0];
        for (int p : prices) { mx = Math.max(mx, p); mn = Math.min(mn, p); }
        return mx - mn;
    }

    public static void main(String[] args) {
        int[] early = {9, 3, 6, 2, 8, 5};
        if (bestFlip(early) != 6) throw new AssertionError("example 1");
        if (bestFlip(new int[] {5, 4, 3, 2}) != 0) throw new AssertionError("example 2");
        if (maxMinusMin(early) != 7) throw new AssertionError("the careless answer is 7, which cannot be collected");
        Random rnd = new Random(9);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(20);
            if (bestFlip(a) != oracle(a)) throw new AssertionError("disagrees with the oracle");
        }
    }
}
```

#### Solution: [Vary] Largest Drop (Author exercise)
<!-- id: ar-largest-drop -->

**Approach.** Mirror the previous scan: carry `highest`, the largest value among earlier positions, and `drop`, the largest `highest - value` found. Compute the candidate before letting the current value raise `highest`, so the earlier element always comes first. Start `drop` at 0, since the contract returns 0 when no falling pair exists. The sums are held in `long` in the code so that extreme inputs near 10^9 and -10^9 cannot overflow the subtraction.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class LargestDrop {
    static long largestDrop(int[] values) {
        if (values.length == 0) return 0;
        long highest = values[0], drop = 0;
        for (int i = 1; i < values.length; i++) {
            drop = Math.max(drop, highest - values[i]);
            highest = Math.max(highest, values[i]);
        }
        return drop;
    }
    static long oracle(int[] v) {
        long best = 0;
        for (int i = 0; i < v.length; i++) for (int j = i + 1; j < v.length; j++) best = Math.max(best, (long) v[i] - v[j]);
        return best;
    }

    public static void main(String[] args) {
        if (largestDrop(new int[] {4, 9, 2, 7, 1}) != 8) throw new AssertionError("example 1");
        if (largestDrop(new int[] {1, 2, 3}) != 0) throw new AssertionError("example 2");
        if (largestDrop(new int[] {}) != 0) throw new AssertionError("empty");
        if (largestDrop(new int[] {1_000_000_000, -1_000_000_000}) != 2_000_000_000L) throw new AssertionError("needs long: the difference exceeds the int range");
        Random rnd = new Random(2);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(21) - 10;
            if (largestDrop(a) != oracle(a)) throw new AssertionError("disagrees with the oracle");
        }
    }
}
```

#### Solution: [Boundary] No Profitable Pair (Author exercise)
<!-- id: ar-no-profitable-pair -->

**Approach.** Under the optional-trade contract the best gain starts at 0, so a falling list never produces a negative result and a single price returns 0. Under a mandatory-trade contract the answer must come from a real pair, so the best starts at the smallest possible value and at least two prices are required. For `[8, 6, 5, 1]` the pair differences are -2, -3, -7, -1, -5 and -4, whose maximum is -1, from buying at 6 and selling at 5. The only change between the contracts is that one starting value and the length requirement.

**Complexity.** O(n) time and O(1) extra space for both variants.

```java run
public final class NoProfitablePair {
    static int optionalTrade(int[] prices) {
        int lowest = prices[0], best = 0;
        for (int i = 1; i < prices.length; i++) {
            best = Math.max(best, prices[i] - lowest);
            lowest = Math.min(lowest, prices[i]);
        }
        return best;
    }
    static int mandatoryTrade(int[] prices) {          // contract: at least two prices
        int lowest = prices[0], best = Integer.MIN_VALUE;
        for (int i = 1; i < prices.length; i++) {
            best = Math.max(best, prices[i] - lowest);
            lowest = Math.min(lowest, prices[i]);
        }
        return best;
    }

    public static void main(String[] args) {
        int[] falling = {8, 6, 5, 1};
        if (optionalTrade(falling) != 0) throw new AssertionError("optional contract");
        if (optionalTrade(new int[] {5}) != 0) throw new AssertionError("single price");
        if (mandatoryTrade(falling) != -1) throw new AssertionError("mandatory contract: the least bad loss");
        int brute = Integer.MIN_VALUE;
        for (int b = 0; b < falling.length; b++) for (int s = b + 1; s < falling.length; s++) brute = Math.max(brute, falling[s] - falling[b]);
        if (brute != -1) throw new AssertionError("brute force agrees on the mandatory answer");
    }
}
```

#### Solution: [Recognize] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ar-best-time-multiple -->

**Approach.** With unlimited trades and one share at a time, every rise from one day to the next can be collected by buying the day before and selling the day after, and every fall can be skipped. The best profit is therefore the sum of all positive day-to-day differences, and no running minimum is needed. The state is a single total updated from adjacent pairs, which makes this a different pattern from the single-trade lesson. The check compares the sum of rises with a small exhaustive search over buy and sell schedules.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.Random;

public final class BestTimeMultiple {
    static int maxProfit(int[] prices) {
        int total = 0;
        for (int i = 1; i < prices.length; i++) total += Math.max(0, prices[i] - prices[i - 1]);
        return total;
    }
    // Exhaustive: each day choose hold-or-not by trying every subset of "own the share overnight" states.
    static int oracle(int[] prices) {
        int n = prices.length, best = 0;
        for (int mask = 0; mask < 1 << (n - 1); mask++) {
            // bit i set means we hold the share from day i to day i+1
            int profit = 0;
            for (int i = 0; i < n - 1; i++) if ((mask >> i & 1) == 1) profit += prices[i + 1] - prices[i];
            best = Math.max(best, profit);
        }
        return best;
    }

    public static void main(String[] args) {
        if (maxProfit(new int[] {1, 5, 2, 6, 3}) != 8) throw new AssertionError("example 1");
        if (maxProfit(new int[] {4, 3, 2}) != 0) throw new AssertionError("example 2");
        Random rnd = new Random(4);
        for (int t = 0; t < 2000; t++) {
            int[] a = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(10);
            if (maxProfit(a) != oracle(a)) throw new AssertionError("disagrees with the exhaustive oracle");
        }
    }
}
```
