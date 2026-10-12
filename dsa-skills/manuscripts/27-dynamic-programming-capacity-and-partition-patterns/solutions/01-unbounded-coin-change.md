<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Unbounded Coin Change

#### Solution: [Build] One Denomination (Author exercise)
<!-- id: cap-coin-one-denomination -->

**Approach.**
The table entry `dp[a]` holds the smallest token count for amount `a`, and the marker `amount + 1` stands for an unreachable amount. With one denomination the last coin is always `coin`, so the entry reads only `dp[a - coin]` when that index exists. The base entry `dp[0]` is 0. The invariant is that every entry the loop has passed is exact, and an entry keeps the marker exactly when `a` is not a multiple of `coin`.

The loop runs in increasing order of `a`. When it reaches a multiple of the coin, the entry one coin earlier is already final, so the count grows by one per coin. The closed form `amount / coin` agrees with the table, and the test below checks that.

**Complexity.**
- **Time** is O(amount), because each amount does one comparison and one table read.
- **Space** is O(amount) for the table, and the inputs are not changed.

```java run
import java.util.*;

public final class CapCoinOneDenomination {
    /**
     * Returns the fewest tokens of one denomination that add up to amount, or -1.
     * Time: O(amount). Space: O(amount).
     * Invariant: dp[a] is exact for every amount the loop has passed.
     */
    static int oneDenomination(int coin, int amount) {
        // The marker amount + 1 is larger than any real token count.
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        // Paying nothing needs no tokens.
        dp[0] = 0;
        // Increasing amounts make each earlier entry final before it is read.
        for (int a = 1; a <= amount; a++) {
            // The only possible last coin is the single denomination.
            if (coin <= a && dp[a - coin] + 1 < dp[a]) dp[a] = dp[a - coin] + 1;
        }
        // The marker becomes -1 at the return.
        return dp[amount] > amount ? -1 : dp[amount];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (oneDenomination(4, 12) != 3) throw new AssertionError("ex1");
        if (oneDenomination(4, 10) != -1) throw new AssertionError("ex2");
        // Amount 0 needs no tokens, and a coin above the amount cannot be used.
        if (oneDenomination(5, 0) != 0) throw new AssertionError("zero");
        if (oneDenomination(5, 3) != -1) throw new AssertionError("too big");
        // Every pair is checked against the closed form.
        for (int coin = 1; coin <= 30; coin++) {
            for (int amount = 0; amount <= 200; amount++) {
                int expected = amount % coin == 0 ? amount / coin : -1;
                if (oneDenomination(coin, amount) != expected) throw new AssertionError(coin + " " + amount);
            }
        }
    }
}
```

#### Solution: [Vary] Coin Change (LeetCode 322)
<!-- id: cap-coin-fewest-coins -->

**Approach.**
The table keeps the same meaning, and the entry for amount `a` now takes the smallest value of `dp[a - coin] + 1` over every denomination with `coin <= a`. Each such denomination is a candidate for the last coin. The base entry is `dp[0] = 0`, and the marker `amount + 1` is larger than any real count because each coin is worth at least 1.

The invariant is that `dp[a]` is the fewest coins for `a` for every amount the loop has passed. Increasing order of `a` is what lets a denomination appear more than once, since `dp[a - coin]` may already use it. A downward loop would answer a different question. The greedy method of the lesson fails on `[1,3,4]` with amount 6, and the test checks that the table does not.

**Complexity.**
- **Time** is O(amount * k) for k denominations, because each amount tries each denomination once.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapCoinFewestCoins {
    /**
     * Returns the fewest coins that add up to amount, or -1 when no combination does.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: dp[a] is the fewest coins for a, for every amount the loop has passed.
     */
    static int minCoins(int[] coins, int amount) {
        // The marker amount + 1 stands for an unreachable amount.
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        // Paying nothing needs no coins.
        dp[0] = 0;
        // Increasing amounts allow the same denomination to appear again.
        for (int a = 1; a <= amount; a++) {
            // Each denomination that fits is a candidate for the last coin.
            for (int coin : coins) {
                // The candidate wins when the smaller amount plus one coin is cheaper.
                if (coin <= a && dp[a - coin] + 1 < dp[a]) dp[a] = dp[a - coin] + 1;
            }
        }
        // The marker becomes -1 at the return.
        return dp[amount] > amount ? -1 : dp[amount];
    }

    /** The greedy method of the lesson, kept to show that it fails. */
    static int greedy(int[] coins, int amount) {
        int[] sorted = coins.clone();
        Arrays.sort(sorted);
        int left = amount, count = 0;
        for (int i = sorted.length - 1; i >= 0; i--) {
            count += left / sorted[i];
            left %= sorted[i];
        }
        return left == 0 ? count : -1;
    }

    /** Oracle: breadth-first search over remaining amounts, one level per coin. */
    static int oracle(int[] coins, int amount) {
        int[] dist = new int[amount + 1];
        Arrays.fill(dist, -1);
        Deque<Integer> queue = new ArrayDeque<>();
        dist[0] = 0;
        queue.add(0);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int coin : coins) {
                int next = cur + coin;
                if (next <= amount && dist[next] == -1) {
                    dist[next] = dist[cur] + 1;
                    queue.add(next);
                }
            }
        }
        return dist[amount];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCoins(new int[] {3, 7, 10}, 14) != 2) throw new AssertionError("ex1");
        if (minCoins(new int[] {5, 9}, 8) != -1) throw new AssertionError("ex2");
        // The greedy method returns 3 for the lesson input, while the table returns 2.
        if (greedy(new int[] {1, 3, 4}, 6) != 3) throw new AssertionError("greedy value");
        if (minCoins(new int[] {1, 3, 4}, 6) != 2) throw new AssertionError("table value");
        // The input array stays unchanged.
        int[] coins = {4, 1, 3};
        int[] copy = coins.clone();
        minCoins(coins, 11);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs against the breadth-first oracle.
        Random rnd = new Random(2701);
        for (int t = 0; t < 3000; t++) {
            int k = 1 + rnd.nextInt(5);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(12));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(60);
            if (minCoins(c, amount) != oracle(c, amount)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Amount Zero And Impossible Target (Author exercise)
<!-- id: cap-coin-zero-and-impossible -->

**Approach.**
The table is the same as before, and the work is in the two edges. Amount 0 is answered by `dp[0] = 0`, which is set before any loop, so the answer is 0 even when `coins` is empty and the inner loop has nothing to try. An impossible amount keeps the table marker `amount + 1`. The method converts the marker to the caller's `failure` only in the final statement.

The invariant is that the table never stores `failure`. A caller value such as 0 or 2 is a legal count, and storing it inside the table would make a failed entry look like a payout. Keeping a separate marker avoids that, and the test uses a `failure` equal to a real count.

**Complexity.**
- **Time** is O(amount * k), and it is O(amount) when `coins` is empty because the inner loop does nothing.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapCoinZeroAndImpossible {
    /**
     * Returns the fewest coins for amount, or failure when no combination reaches it.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: the table holds only real counts and the marker amount + 1.
     */
    static int coinsOrFailure(int[] coins, int amount, int failure) {
        // The marker stays inside the table and never equals the caller's failure value.
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        // Amount 0 is answered before any loop runs, so an empty coin array still returns 0.
        dp[0] = 0;
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) {
                // Only a coin that fits can be the last coin.
                if (coin <= a && dp[a - coin] + 1 < dp[a]) dp[a] = dp[a - coin] + 1;
            }
        }
        // Only the final statement maps the marker to the caller's value.
        return dp[amount] > amount ? failure : dp[amount];
    }

    /** Oracle: exhaustive recursion on the remaining amount, fine for small amounts. */
    static int oracle(int[] coins, int amount) {
        if (amount == 0) return 0;
        int best = Integer.MAX_VALUE;
        for (int coin : coins) {
            if (coin <= amount) {
                int sub = oracle(coins, amount - coin);
                if (sub != Integer.MAX_VALUE) best = Math.min(best, sub + 1);
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (coinsOrFailure(new int[] {}, 0, -7) != 0) throw new AssertionError("ex1");
        if (coinsOrFailure(new int[] {6, 10}, 9, 2) != 2) throw new AssertionError("ex2");
        // A failure equal to a real count is still returned only for impossible amounts.
        if (coinsOrFailure(new int[] {3}, 6, 2) != 2) throw new AssertionError("real two");
        if (coinsOrFailure(new int[] {3}, 7, 2) != 2) throw new AssertionError("failure two");
        if (coinsOrFailure(new int[] {}, 5, 0) != 0) throw new AssertionError("failure zero");
        // Java fact: the sentinel Integer.MAX_VALUE overflows when 1 is added.
        if (Integer.MAX_VALUE + 1 >= 0) throw new AssertionError("overflow");
        // Random inputs against the recursive oracle, including empty coin arrays.
        Random rnd = new Random(2702);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(9));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(25);
            int failure = rnd.nextInt(7) - 3;
            int want = oracle(c, amount);
            if (want == Integer.MAX_VALUE) want = failure;
            if (coinsOrFailure(c, amount, failure) != want) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Reconstruct One Minimum Set (Author exercise)
<!-- id: cap-coin-reconstruct -->

**Approach.**
The count table is unchanged, and a parallel array `choice` records the last coin each time an entry improves. When the method finishes, `choice[amount]` names one last coin of a smallest payout, and `amount - choice[amount]` is the remaining amount, whose own entry also holds a recorded coin. Following that chain down to 0 lists the coins.

The invariant is that `choice[a]` is a coin for which `dp[a - choice[a]] + 1 == dp[a]`, so every step of the walk removes exactly one coin from a smallest payout. The walk collects coins in the order of the chain, and the method sorts them from largest to smallest to match the stated output. An amount of 0 gives an empty array and an unreachable amount gives `null`.

**Complexity.**
- **Time** is O(amount * k) for the table and O(amount) for the walk, which is O(amount * k) in total.
- **Space** is O(amount) for the two arrays, and the output has at most `amount` entries.

```java run
import java.util.*;

public final class CapCoinReconstruct {
    /**
     * Returns one smallest set of coins that adds up to amount, largest first, or null.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: dp[a] - 1 == dp[a - choice[a]] for every reachable a above 0.
     */
    static int[] oneMinimumSet(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        int[] choice = new int[amount + 1];
        Arrays.fill(dp, amount + 1);
        // Paying nothing needs no coins and records no last coin.
        dp[0] = 0;
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) {
                // An improvement also stores the coin that caused it.
                if (coin <= a && dp[a - coin] + 1 < dp[a]) {
                    dp[a] = dp[a - coin] + 1;
                    choice[a] = coin;
                }
            }
        }
        // An unreachable amount has no payout to list.
        if (dp[amount] > amount) return null;
        int[] out = new int[dp[amount]];
        // The walk removes one recorded last coin per step until the amount reaches 0.
        int rest = amount;
        for (int i = 0; rest > 0; i++) {
            out[i] = choice[rest];
            rest -= choice[rest];
        }
        // Largest first, as the output contract states.
        Arrays.sort(out);
        for (int i = 0, j = out.length - 1; i < j; i++, j--) {
            int tmp = out[i];
            out[i] = out[j];
            out[j] = tmp;
        }
        return out;
    }

    /** Oracle: breadth-first search for the smallest count. */
    static int oracleCount(int[] coins, int amount) {
        int[] dist = new int[amount + 1];
        Arrays.fill(dist, -1);
        Deque<Integer> queue = new ArrayDeque<>();
        dist[0] = 0;
        queue.add(0);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int coin : coins) {
                int next = cur + coin;
                if (next <= amount && dist[next] == -1) {
                    dist[next] = dist[cur] + 1;
                    queue.add(next);
                }
            }
        }
        return dist[amount];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(oneMinimumSet(new int[] {1, 3, 4}, 6), new int[] {3, 3})) throw new AssertionError("ex1");
        if (oneMinimumSet(new int[] {2, 5}, 3) != null) throw new AssertionError("ex2");
        // Amount 0 returns an empty array.
        if (oneMinimumSet(new int[] {2, 5}, 0).length != 0) throw new AssertionError("zero");
        // The input array stays unchanged.
        int[] coins = {5, 2, 4};
        int[] copy = coins.clone();
        oneMinimumSet(coins, 13);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs: the set must use given coins, sum to the amount, be sorted downward and have the oracle's length.
        Random rnd = new Random(2703);
        for (int t = 0; t < 3000; t++) {
            int k = 1 + rnd.nextInt(5);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(12));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(60);
            int[] got = oneMinimumSet(c, amount);
            int want = oracleCount(c, amount);
            if (want == -1) {
                if (got != null) throw new AssertionError("expected null " + t);
                continue;
            }
            if (got == null || got.length != want) throw new AssertionError("length " + t);
            int sum = 0;
            for (int i = 0; i < got.length; i++) {
                sum += got[i];
                if (i > 0 && got[i] > got[i - 1]) throw new AssertionError("order " + t);
                boolean known = false;
                for (int coin : c) if (coin == got[i]) known = true;
                if (!known) throw new AssertionError("unknown coin " + t);
            }
            if (sum != amount) throw new AssertionError("sum " + t);
        }
    }
}
```
