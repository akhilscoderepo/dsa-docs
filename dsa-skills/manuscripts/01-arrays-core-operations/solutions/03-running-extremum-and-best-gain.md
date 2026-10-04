<!-- solutions-for: 01-arrays-core-operations -->
### Solutions For Running Extremum And Best Gain

#### Solution: [Build] Best Time to Buy and Sell Stock (LeetCode 121)
<!-- id: ar-best-time-buy-sell -->

**Approach.** The method keeps `lowestSoFar`, the smallest price among the days already read, and `bestGain`, the largest profit of any pair seen so far. For each later day it scores the sell price against `lowestSoFar`, keeps the larger of the old and new gain, and only then lowers `lowestSoFar` if the current price is smaller. Scoring before updating means a day never pairs with itself. `bestGain` starts at 0, so a market that never rises returns 0 by contract.

The context of the lesson claims that comparing neighboring days gives 4 for `[4, 2, 6, 5, 9]` while the true best is 7. The harness asserts both numbers. It also compares the scan with the all-pairs method on 2,000 random arrays.

**Complexity.**

- **Time** is O(n), as the loop scores each of the `n - 1` later days once.
- **Space** is O(1), since two integers carry all the state.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BestGainScan {
    /**
     * Returns the largest sell-minus-buy profit with the buy day first, or 0 when no trade earns a profit.
     * Time: O(n), because each day is scored once.
     * Space: O(1), because only lowestSoFar and bestGain are stored.
     * Invariant: before reading prices[i], lowestSoFar is the minimum of prices[0..i-1] and bestGain is the best profit inside that prefix.
     */
    static int bestGain(int[] prices) {
        // An empty input has no pair, so the contract answer is 0.
        if (prices.length == 0) return 0;
        // The first day is the only candidate buy price before the loop starts.
        int lowestSoFar = prices[0];
        // Zero encodes the no-trade answer that the contract allows.
        int bestGain = 0;
        // Score each later day once, which gives O(n) time.
        for (int i = 1; i < prices.length; i++) {
            // Score selling today against the cheapest earlier price, before today can change that minimum.
            bestGain = Math.max(bestGain, prices[i] - lowestSoFar);
            // Update the remembered minimum afterwards so a day never pairs with itself.
            lowestSoFar = Math.min(lowestSoFar, prices[i]);
        }
        // The prefix is now the whole array.
        return bestGain;
    }

    /** The all-pairs method from the lesson. */
    static int maxProfitPairs(int[] prices) {
        int answer = 0;
        for (int buy = 0; buy < prices.length; buy++)
            for (int sell = buy + 1; sell < prices.length; sell++)
                answer = Math.max(answer, prices[sell] - prices[buy]);
        return answer;
    }

    /** The adjacent-day method from the lesson's opening: it compares neighbors only. */
    static int biggestNeighborJump(int[] prices) {
        int best = 0;
        for (int i = 1; i < prices.length; i++) best = Math.max(best, prices[i] - prices[i - 1]);
        return best;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (bestGain(new int[] {9, 4, 6, 3, 8, 5}) != 5) throw new AssertionError("example 1");
        if (bestGain(new int[] {5}) != 0) throw new AssertionError("example 2");
        // Checks the opening claim: neighbors give 4 while the true best profit is 7.
        if (biggestNeighborJump(new int[] {4, 2, 6, 5, 9}) != 4) throw new AssertionError("neighbor jump");
        if (bestGain(new int[] {4, 2, 6, 5, 9}) != 7) throw new AssertionError("true best");
        // Checks a falling market and an empty array, both of which return 0.
        if (bestGain(new int[] {8, 6, 5, 2}) != 0) throw new AssertionError("falling");
        if (bestGain(new int[] {}) != 0) throw new AssertionError("empty");
        // Checks 2,000 random arrays against the all-pairs method.
        Random rnd = new Random(53);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(15);
            if (bestGain(x) != maxProfitPairs(x)) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Vary] Largest Drop (Author exercise)
<!-- id: ar-largest-drop -->

**Approach.** The scan mirrors the gain scan. The remembered value becomes `highestSoFar`, the largest value among earlier positions, and the score of position `j` becomes `highestSoFar - nums[j]`. The method scores first and updates `highestSoFar` afterwards. `bestDrop` starts at 0, which is the contract answer when no earlier value exceeds a later one.

Only two decisions changed from the previous problem: the extremum is a maximum, and the subtraction swaps operands. The harness checks the scan against an all-pairs oracle on random arrays.

**Complexity.**

- **Time** is O(n), because each position is scored once against the remembered maximum.
- **Space** is O(1), since `highestSoFar` and `bestDrop` are the only state.

```java run
import java.util.Arrays;
import java.util.Random;

public final class LargestDrop {
    /**
     * Returns the largest nums[i] - nums[j] over pairs with i < j, or 0 when no pair is positive.
     * Time: O(n), because each position is scored once.
     * Space: O(1), because only highestSoFar and bestDrop are stored.
     * Invariant: before reading nums[j], highestSoFar is the maximum of nums[0..j-1].
     */
    static int largestDrop(int[] nums) {
        // An empty input has no pair, so the contract answer is 0.
        if (nums.length == 0) return 0;
        // Before the loop, the only earlier value is the first element.
        int highestSoFar = nums[0];
        // Zero is the answer when no earlier value exceeds a later one.
        int bestDrop = 0;
        // One pass gives O(n) time.
        for (int j = 1; j < nums.length; j++) {
            // Score position j against the highest earlier value, before j can change that maximum.
            bestDrop = Math.max(bestDrop, highestSoFar - nums[j]);
            // Update the remembered maximum afterwards.
            highestSoFar = Math.max(highestSoFar, nums[j]);
        }
        // The prefix is the whole array.
        return bestDrop;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (largestDrop(new int[] {3, 9, 4, 1, 6}) != 8) throw new AssertionError("example 1");
        if (largestDrop(new int[] {1, 2, 3}) != 0) throw new AssertionError("example 2");
        // Checks the empty and single-element arrays.
        if (largestDrop(new int[] {}) != 0 || largestDrop(new int[] {7}) != 0) throw new AssertionError("short arrays");
        // Checks 2,000 random arrays with negative values against an all-pairs oracle.
        Random rnd = new Random(59);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(9)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(21) - 10;
            int expected = 0;
            for (int i = 0; i < x.length; i++)
                for (int j = i + 1; j < x.length; j++) expected = Math.max(expected, x[i] - x[j]);
            if (largestDrop(x) != expected) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Boundary] No Profitable Pair (Author exercise)
<!-- id: ar-no-profitable-pair -->

**Approach.** The contract comes first: the answer is the largest positive difference, and it is 0 when there is none. The variable `bestGain` therefore starts at 0, and it never becomes negative. The variable `lowestSoFar` starts at the first element, and the scan avoids `Integer.MAX_VALUE` as a starting value, because subtracting it from a negative value wraps around. The difference is computed in `long`, because two `int` values can be more than `Integer.MAX_VALUE` apart.

The harness shows both hazards. Subtracting `Integer.MAX_VALUE` from -2 wraps to a positive `int`, and the difference of the two extreme `int` values wraps to -1 in `int` arithmetic while the `long` difference is 4,294,967,295. The harness then compares the scan with a `long` all-pairs oracle on random arrays that include the extreme values.

**Complexity.**

- **Time** is O(n), because the loop reads each value once and each step costs constant time.
- **Space** is O(1), since the method keeps `lowestSoFar`, `bestGain` and the index.

```java run
import java.util.Arrays;
import java.util.Random;

public final class NoProfitablePair {
    /**
     * Returns the largest values[j] - values[i] with i < j as a long, or 0 when no difference is positive.
     * Time: O(n), because each value is read once.
     * Space: O(1), because only lowestSoFar and bestGain are stored.
     * Invariant: before reading values[j], lowestSoFar is the minimum of values[0..j-1] and bestGain is the best positive difference inside that prefix.
     */
    static long bestGain(int[] values) {
        // Fewer than two values give no pair, so the contract answer is 0.
        if (values.length < 2) return 0;
        // Start from the data; Integer.MAX_VALUE would make later subtractions wrap around.
        int lowestSoFar = values[0];
        // Zero is the contract answer for falling or flat input and never goes below zero.
        long bestGain = 0;
        // One pass gives O(n) time.
        for (int j = 1; j < values.length; j++) {
            // Cast one operand to long so the subtraction cannot wrap, then keep the larger gain.
            bestGain = Math.max(bestGain, (long) values[j] - lowestSoFar);
            // Update the minimum after scoring so a position never pairs with itself.
            lowestSoFar = Math.min(lowestSoFar, values[j]);
        }
        // The prefix is the whole array.
        return bestGain;
    }

    public static void main(String[] args) {
        // Checks both examples; the second answer exceeds the range of int.
        if (bestGain(new int[] {9, 7, 4, 3}) != 0) throw new AssertionError("example 1");
        if (bestGain(new int[] {-2000000000, 2000000000}) != 4000000000L) throw new AssertionError("example 2");
        // Checks ties and short arrays, which all return 0.
        if (bestGain(new int[] {5, 5, 5}) != 0) throw new AssertionError("ties");
        if (bestGain(new int[] {}) != 0 || bestGain(new int[] {1}) != 0) throw new AssertionError("short");
        // Checks the lesson claim: subtracting Integer.MAX_VALUE from -2 wraps to a positive int.
        int wrapped = -2 - Integer.MAX_VALUE;
        if (wrapped <= 0) throw new AssertionError("int subtraction wraps");
        // Checks the claim: the extreme difference wraps in int but not in long.
        if (Integer.MAX_VALUE - Integer.MIN_VALUE != -1) throw new AssertionError("int difference wraps to -1");
        if ((long) Integer.MAX_VALUE - Integer.MIN_VALUE != 4294967295L) throw new AssertionError("long difference");
        // Checks 2,000 random arrays that include the extreme values against a long all-pairs oracle.
        Random rnd = new Random(61);
        int[] pool = {Integer.MIN_VALUE, Integer.MAX_VALUE, -5, 0, 3, 8, -1};
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[rnd.nextInt(8)];
            for (int i = 0; i < x.length; i++) x[i] = pool[rnd.nextInt(pool.length)];
            long expected = 0;
            for (int i = 0; i < x.length; i++)
                for (int j = i + 1; j < x.length; j++) expected = Math.max(expected, (long) x[j] - x[i]);
            if (bestGain(x) != expected) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```

#### Solution: [Recognize] Best Time to Buy and Sell Stock II (LeetCode 122)
<!-- id: ar-buy-sell-many -->

**Approach.** With many trades allowed, a single remembered minimum is the wrong state. Every rise between two neighboring days can be collected as its own trade, because buying on the lower day and selling on the next higher day earns exactly that rise. A multi-day climb equals the sum of its daily rises, so the total profit is the sum of all positive day-to-day differences. Falling days earn nothing and are skipped, because holding no share avoids their loss.

The harness shows that the lesson's single-minimum scan answers 5 for `[4, 1, 3, 2, 6, 5]`, while the correct answer is 6. It then compares the new method with a two-state oracle that tracks the best cash value with and without a share held.

**Complexity.**

- **Time** is O(n), since one pass reads each neighboring pair once.
- **Space** is O(1), because one running total is the only state.

```java run
import java.util.Arrays;
import java.util.Random;

public final class BuySellMany {
    /**
     * Returns the largest total profit with unlimited trades and at most one share held.
     * Time: O(n), because each neighboring pair is read once.
     * Space: O(1), because only the total is stored.
     * Invariant: before reading prices[i], total is the best profit achievable inside prices[0..i-1].
     */
    static int maxProfitMany(int[] prices) {
        // No trades have happened before the first day.
        int total = 0;
        // Compare each day with the day before it; the loop gives O(n) time.
        for (int i = 1; i < prices.length; i++) {
            // A rise is a trade that buys yesterday and sells today; a fall earns nothing and is skipped.
            if (prices[i] > prices[i - 1]) total += prices[i] - prices[i - 1];
        }
        // The prefix is the whole array.
        return total;
    }

    /** The single-trade scan from the lesson, used here to show it is the wrong state. */
    static int singleTrade(int[] prices) {
        int lowestSoFar = prices[0], bestGain = 0;
        for (int i = 1; i < prices.length; i++) {
            bestGain = Math.max(bestGain, prices[i] - lowestSoFar);
            lowestSoFar = Math.min(lowestSoFar, prices[i]);
        }
        return bestGain;
    }

    /** Oracle: best cash while holding a share and while holding none, updated day by day. */
    static int oracle(int[] prices) {
        int cash = 0, hold = -prices[0];
        for (int i = 1; i < prices.length; i++) {
            int newCash = Math.max(cash, hold + prices[i]);
            int newHold = Math.max(hold, cash - prices[i]);
            cash = newCash;
            hold = newHold;
        }
        return cash;
    }

    public static void main(String[] args) {
        // Checks both examples.
        if (maxProfitMany(new int[] {4, 1, 3, 2, 6, 5}) != 6) throw new AssertionError("example 1");
        if (maxProfitMany(new int[] {9, 6, 3}) != 0) throw new AssertionError("example 2");
        // Checks the false-friend claim: one remembered minimum gives 5 here, which is too small.
        if (singleTrade(new int[] {4, 1, 3, 2, 6, 5}) != 5) throw new AssertionError("single trade answer");
        // Checks a single price, which has no pair.
        if (maxProfitMany(new int[] {7}) != 0) throw new AssertionError("single day");
        // Checks 2,000 random arrays against the two-state oracle.
        Random rnd = new Random(67);
        for (int t = 0; t < 2000; t++) {
            int[] x = new int[1 + rnd.nextInt(9)];
            for (int i = 0; i < x.length; i++) x[i] = rnd.nextInt(15);
            if (maxProfitMany(x) != oracle(x)) throw new AssertionError("mismatch on " + Arrays.toString(x));
        }
    }
}
```
