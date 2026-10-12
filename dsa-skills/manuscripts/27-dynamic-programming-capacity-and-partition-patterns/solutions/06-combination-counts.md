<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Combination Counts

#### Solution: [Build] Count With One Coin (Author exercise)
<!-- id: cap-cmb-one-coin -->

**Approach.**
The table `ways[a]` counts the combinations that add up to `a`. The seed `ways[0] = 1` stands for the empty combination. With one denomination, the loop runs `a` from `coin` to `amount` and adds `ways[a - coin]` to `ways[a]`. Each entry therefore copies the entry one coin below it, so the 1 from the seed travels along the multiples of the coin.

The entries at amounts that are not multiples of the coin stay 0, because no chain of steps of size `coin` reaches them from 0. The count is 1 exactly when `amount % coin == 0`, and the test checks that equivalence.

**Complexity.**
- **Time** is O(amount), because each amount does one addition.
- **Space** is O(amount) for the table, and the inputs are not changed.

```java run
import java.util.*;

public final class CapCmbOneCoin {
    /**
     * Returns the number of combinations of one denomination that add up to amount.
     * Time: O(amount). Space: O(amount).
     * Invariant: ways[a] counts combinations of the coin that add up to a.
     */
    static long oneCoin(int coin, int amount) {
        long[] ways = new long[amount + 1];
        // The empty combination adds up to 0.
        ways[0] = 1;
        // Increasing amounts let the seed travel along the multiples of the coin.
        for (int a = coin; a <= amount; a++) ways[a] += ways[a - coin];
        return ways[amount];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (oneCoin(3, 12) != 1) throw new AssertionError("ex1");
        if (oneCoin(5, 12) != 0) throw new AssertionError("ex2");
        // Amount 0 has one combination, and a coin above the amount gives none.
        if (oneCoin(4, 0) != 1 || oneCoin(9, 5) != 0) throw new AssertionError("edges");
        // Every pair is checked against the divisibility test.
        for (int coin = 1; coin <= 30; coin++) {
            for (int amount = 0; amount <= 200; amount++) {
                long expected = amount % coin == 0 ? 1 : 0;
                if (oneCoin(coin, amount) != expected) throw new AssertionError(coin + " " + amount);
            }
        }
    }
}
```

#### Solution: [Vary] Coin Change II (LeetCode 518)
<!-- id: cap-cmb-coin-change-two -->

**Approach.**
The method processes one denomination per outer iteration, in array order. After denomination `c` is processed, `ways[a]` counts the combinations of `a` that use only the denominations seen so far. A new combination either uses no copy of `c`, which the old entry counts, or ends with a last copy of `c`. Removing that copy leaves a combination of `a - c` over the same denominations, and `ways[a - c]` has already been updated for `c`.

Because all copies of one denomination are placed before the next denomination, each combination has a single path through the table. The inner loop runs upward, so a denomination can appear many times. The seed `ways[0] = 1` is the empty combination. Swapping the two loops would count sequences, and the test shows the difference.

**Complexity.**
- **Time** is O(amount * k) for k denominations, because each denomination updates each amount once.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapCmbCoinChangeTwo {
    /**
     * Returns the number of combinations of the coins that add up to amount.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: after a coin is processed, ways[a] counts combinations that use only the coins seen so far.
     */
    static long change(int[] coins, int amount) {
        long[] ways = new long[amount + 1];
        // The empty combination adds up to 0.
        ways[0] = 1;
        // Coins outside: all copies of one coin come before the next coin in every combination.
        for (int coin : coins) {
            // Increasing amounts let the coin appear several times.
            for (int a = coin; a <= amount; a++) ways[a] += ways[a - coin];
        }
        return ways[amount];
    }

    /** The swapped loop order, kept to show that it counts sequences. */
    static long sequences(int[] coins, int amount) {
        long[] ways = new long[amount + 1];
        ways[0] = 1;
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) if (coin <= a) ways[a] += ways[a - coin];
        }
        return ways[amount];
    }

    /** Oracle: chooses a count for each denomination by recursion. */
    static long oracle(int[] coins, int i, int left) {
        if (i == coins.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int copies = 0; copies * coins[i] <= left; copies++) total += oracle(coins, i + 1, left - copies * coins[i]);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (change(new int[] {2, 3, 7}, 12) != 4) throw new AssertionError("ex1");
        if (change(new int[] {4}, 10) != 0) throw new AssertionError("ex2");
        // The cashier example: four combinations but nine sequences.
        if (change(new int[] {1, 2, 5}, 5) != 4 || sequences(new int[] {1, 2, 5}, 5) != 9) throw new AssertionError("cashier");
        // The order of the denominations in the array does not change the answer.
        if (change(new int[] {5, 2, 1}, 5) != 4) throw new AssertionError("array order");
        // The input array stays unchanged.
        int[] coins = {3, 1, 2};
        int[] copy = coins.clone();
        change(coins, 9);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs against the recursive oracle.
        Random rnd = new Random(2718);
        for (int t = 0; t < 2000; t++) {
            int k = 1 + rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(9));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(30);
            if (change(c, amount) != oracle(c, 0, amount)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Combination (Author exercise)
<!-- id: cap-cmb-empty-combination -->

**Approach.**
The seed `ways[0] = 1` is set before any loop, so the empty combination exists even when `coins` is empty. For an empty array the outer loop does nothing, and the method returns `ways[amount]`. That entry is 1 for amount 0 and 0 for every positive amount, which matches the definition. A denomination larger than the amount never enters the inner loop and cannot change any entry.

The table is a `long[]`, because the count for the denominations 1 through 8 and amount 600 is about 1.7 * 10^11, which does not fit in an `int`. The test asserts that value. The coins stay in the outer loop, so the count remains the count of combinations.

**Complexity.**
- **Time** is O(amount * k), and it is O(amount) when the array is empty because only the allocation runs.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapCmbEmptyCombination {
    /**
     * Returns the number of combinations that add up to amount, where the array may be empty.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: after a coin is processed, ways[a] counts combinations that use only the coins seen so far.
     */
    static long countCombinations(int[] coins, int amount) {
        long[] ways = new long[amount + 1];
        // The seed is set before any loop, so an empty array still answers 1 for amount 0.
        ways[0] = 1;
        for (int coin : coins) {
            // A coin above the amount skips the loop and changes nothing.
            for (int a = coin; a <= amount; a++) ways[a] += ways[a - coin];
        }
        return ways[amount];
    }

    /** Oracle: chooses a count for each denomination by recursion. */
    static long oracle(int[] coins, int i, int left) {
        if (i == coins.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int copies = 0; copies * coins[i] <= left; copies++) total += oracle(coins, i + 1, left - copies * coins[i]);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countCombinations(new int[] {}, 0) != 1) throw new AssertionError("ex1");
        if (countCombinations(new int[] {7, 9}, 5) != 0) throw new AssertionError("ex2");
        // An empty array with a positive amount has no combination.
        if (countCombinations(new int[] {}, 4) != 0) throw new AssertionError("empty positive");
        // Java fact: the count for denominations 1 to 8 and amount 600 exceeds the int range.
        long big = countCombinations(new int[] {1, 2, 3, 4, 5, 6, 7, 8}, 600);
        if (big <= Integer.MAX_VALUE) throw new AssertionError("should exceed int");
        if ((int) big == big) throw new AssertionError("narrowing should lose bits");
        // The input array stays unchanged.
        int[] coins = {2, 5};
        int[] copy = coins.clone();
        countCombinations(coins, 20);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs, including empty arrays, against the recursive oracle.
        Random rnd = new Random(2719);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(5);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(8));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(30);
            if (countCombinations(c, amount) != oracle(c, 0, amount)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Explain Loop Order (Author exercise)
<!-- id: cap-cmb-explain-loop-order -->

**Approach.**
Both counts use the same update, `ways[a] += ways[a - coin]`, and they differ only in which loop is outside. With the coins outside, every combination is built in one fixed order of denominations, so each combination has one path and the table counts combinations. With the amounts outside, the entry for `a` adds `ways[a - coin]` for every coin as the last coin, so a combination reached by several orders is added once per order, and the table counts sequences.

The method fills two arrays and returns the two final entries. The invariant for the first array is that after each coin, its entries count combinations over the coins seen so far. The invariant for the second array is that each entry `a` counts the sequences that add up to `a`, built from smaller entries that are already final. The test checks both against recursive counts.

**Complexity.**
- **Time** is O(amount * k) for each table, which is O(amount * k) in total.
- **Space** is O(amount) for the two arrays, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapCmbExplainLoopOrder {
    /**
     * Returns {combinations, sequences} that add up to amount.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: the first array counts combinations over the coins seen so far; the second counts sequences.
     */
    static long[] bothCounts(int[] coins, int amount) {
        long[] combos = new long[amount + 1];
        long[] seqs = new long[amount + 1];
        // Both tables are seeded with the empty combination and the empty sequence.
        combos[0] = 1;
        seqs[0] = 1;
        // Coins outside: one fixed order of denominations per combination.
        for (int coin : coins) {
            for (int a = coin; a <= amount; a++) combos[a] += combos[a - coin];
        }
        // Amounts outside: every coin is tried as the last coin, so each order is a separate path.
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) if (coin <= a) seqs[a] += seqs[a - coin];
        }
        return new long[] {combos[amount], seqs[amount]};
    }

    /** Oracle: counts combinations by recursion over denominations. */
    static long comboOracle(int[] coins, int i, int left) {
        if (i == coins.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int copies = 0; copies * coins[i] <= left; copies++) total += comboOracle(coins, i + 1, left - copies * coins[i]);
        return total;
    }

    /** Oracle: counts sequences by recursion on the first coin. */
    static long seqOracle(int[] coins, int left) {
        if (left == 0) return 1;
        long total = 0;
        for (int coin : coins) if (coin <= left) total += seqOracle(coins, left - coin);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bothCounts(new int[] {1, 2}, 4), new long[] {3, 5})) throw new AssertionError("ex1");
        if (!Arrays.equals(bothCounts(new int[] {3, 4}, 7), new long[] {1, 2})) throw new AssertionError("ex2");
        // Amount 0 gives one combination and one empty sequence.
        if (!Arrays.equals(bothCounts(new int[] {2, 5}, 0), new long[] {1, 1})) throw new AssertionError("zero");
        // The two counts are equal when only one denomination exists.
        if (bothCounts(new int[] {3}, 9)[0] != bothCounts(new int[] {3}, 9)[1]) throw new AssertionError("single coin");
        // The input array stays unchanged.
        int[] coins = {2, 1};
        int[] copy = coins.clone();
        bothCounts(coins, 8);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs against the two recursive oracles.
        Random rnd = new Random(2720);
        for (int t = 0; t < 1500; t++) {
            int k = 1 + rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(7));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(16);
            long[] got = bothCounts(c, amount);
            if (got[0] != comboOracle(c, 0, amount) || got[1] != seqOracle(c, amount)) throw new AssertionError("random " + t);
        }
    }
}
```
