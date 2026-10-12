<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For DP And Capacity

#### Solution: [Build] Coin Change (LeetCode 322)
<!-- id: cap-dpc-coin-change-flag -->

**Approach.**
The table `dp[a]` holds the fewest coins for amount `a`, with `dp[0] = 0` and the marker `amount + 1` for amounts not yet reached. Coins form the outer loop. For a reusable coin, the inner loop runs upward, so `dp[a - coin]` may already include the same coin. For a single-use coin, the inner loop runs downward, so `dp[a - coin]` still describes the earlier coins and each array position joins at most once.

The invariant is that after each coin, `dp[a]` is the fewest coins for `a` using the coins seen so far under the chosen reuse rule. Only the direction of the inner loop depends on the flag. The marker becomes -1 at the return.

**Complexity.**
- **Time** is O(amount * k) for k coins, because each coin updates each amount at most once.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapDpcCoinChangeFlag {
    /**
     * Returns the fewest coins that add up to amount, with coins reusable or single-use, or -1.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: after each coin, dp[a] is the fewest coins for a using the coins seen so far.
     */
    static int fewest(int[] coins, int amount, boolean reusable) {
        int[] dp = new int[amount + 1];
        // The marker amount + 1 is larger than any real count.
        Arrays.fill(dp, amount + 1);
        dp[0] = 0;
        for (int coin : coins) {
            if (reusable) {
                // Upward amounts read dp[a - coin] after this coin updated it, so the coin repeats.
                for (int a = coin; a <= amount; a++) dp[a] = Math.min(dp[a], dp[a - coin] + 1);
            } else {
                // Downward amounts read dp[a - coin] before this coin updated it, so the coin joins once.
                for (int a = amount; a >= coin; a--) dp[a] = Math.min(dp[a], dp[a - coin] + 1);
            }
        }
        // The marker becomes -1 at the return.
        return dp[amount] > amount ? -1 : dp[amount];
    }

    /** Oracle: single-use by subset enumeration, reusable by breadth-first search. */
    static int oracle(int[] coins, int amount, boolean reusable) {
        if (!reusable) {
            int best = -1;
            for (int mask = 0; mask < (1 << coins.length); mask++) {
                int sum = 0;
                for (int i = 0; i < coins.length; i++) if ((mask >> i & 1) == 1) sum += coins[i];
                if (sum == amount) {
                    int size = Integer.bitCount(mask);
                    if (best == -1 || size < best) best = size;
                }
            }
            return best;
        }
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
        if (fewest(new int[] {1, 3, 4}, 6, true) != 2) throw new AssertionError("ex1");
        if (fewest(new int[] {1, 3, 4}, 6, false) != -1) throw new AssertionError("ex2");
        // Amount 0 returns 0 in both modes, and equal values at two positions are two coins.
        if (fewest(new int[] {}, 0, false) != 0 || fewest(new int[] {5, 5}, 10, false) != 2) throw new AssertionError("edges");
        // The input array stays unchanged.
        int[] coins = {4, 1, 3};
        int[] copy = coins.clone();
        fewest(coins, 7, false);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs in both modes against the oracles.
        Random rnd = new Random(2724);
        for (int t = 0; t < 3000; t++) {
            int[] c = new int[rnd.nextInt(7)];
            for (int i = 0; i < c.length; i++) c[i] = 1 + rnd.nextInt(10);
            int amount = rnd.nextInt(40);
            boolean reusable = rnd.nextBoolean();
            if (reusable) {
                // The breadth-first oracle treats equal values as one denomination, which is the same for reuse.
                if (fewest(c, amount, true) != oracle(c, amount, true)) throw new AssertionError("reusable " + t);
            } else if (fewest(c, amount, false) != oracle(c, amount, false)) throw new AssertionError("single " + t);
        }
    }
}
```

#### Solution: [Vary] Coin Change II (LeetCode 518)
<!-- id: cap-dpc-coin-change-two-ordered -->

**Approach.**
Both answers share the seed `ways[0] = 1` and the update that adds `ways[t - v]` to `ways[t]`. For combinations, the coins are the outer loop and the totals run upward, so each combination is written once in the order of the array. For sequences, the totals are the outer loop and every coin is tried as the last element, so each order is a separate path.

The flag selects the loop owner and nothing else. The invariant for the combination branch is that after each coin, `ways[t]` counts combinations over the coins seen so far. The invariant for the sequence branch is that every total the loop has passed holds its exact sequence count. The table is a `long` array.

**Complexity.**
- **Time** is O(amount * k) in both branches, because each total meets each coin once.
- **Space** is O(amount) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapDpcCoinChangeTwoOrdered {
    /**
     * Returns the number of combinations or, when ordered, the number of sequences that add up to amount.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: every entry the loops have finished is exact for the chosen question.
     */
    static long ways(int[] coins, int amount, boolean ordered) {
        long[] ways = new long[amount + 1];
        // The empty combination and the empty sequence both add up to 0.
        ways[0] = 1;
        if (ordered) {
            // Totals outside: every coin may be the last element of a sequence.
            for (int t = 1; t <= amount; t++) {
                for (int coin : coins) if (coin <= t) ways[t] += ways[t - coin];
            }
        } else {
            // Coins outside: one fixed order of denominations per combination.
            for (int coin : coins) {
                for (int t = coin; t <= amount; t++) ways[t] += ways[t - coin];
            }
        }
        return ways[amount];
    }

    /** Oracle: combinations by choosing a count for each coin, sequences by recursion on the first coin. */
    static long oracle(int[] coins, int left, int i, boolean ordered) {
        if (ordered) {
            if (left == 0) return 1;
            long total = 0;
            for (int coin : coins) if (coin <= left) total += oracle(coins, left - coin, 0, true);
            return total;
        }
        if (i == coins.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int copies = 0; copies * coins[i] <= left; copies++) total += oracle(coins, left - copies * coins[i], i + 1, false);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (ways(new int[] {2, 4, 5}, 9, false) != 2) throw new AssertionError("ex1");
        if (ways(new int[] {2, 4, 5}, 9, true) != 5) throw new AssertionError("ex2");
        // The billing example: 4 bundles and 7 purchase orders.
        if (ways(new int[] {1, 2, 3}, 4, false) != 4 || ways(new int[] {1, 2, 3}, 4, true) != 7) throw new AssertionError("billing");
        // Amount 0 has one outcome in both modes.
        if (ways(new int[] {3, 7}, 0, false) != 1 || ways(new int[] {3, 7}, 0, true) != 1) throw new AssertionError("zero");
        // The input array stays unchanged.
        int[] coins = {5, 2, 4};
        int[] copy = coins.clone();
        ways(coins, 30, true);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs in both modes against the recursive oracle.
        Random rnd = new Random(2725);
        for (int t = 0; t < 2000; t++) {
            int k = 1 + rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(8));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(16);
            boolean ordered = rnd.nextBoolean();
            if (ways(c, amount, ordered) != oracle(c, amount, 0, ordered)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Partition Equal Subset Sum (LeetCode 416)
<!-- id: cap-dpc-partition-nonempty -->

**Approach.**
A split needs a subset that sums to half of the total and leaves a nonempty complement. The method first checks that the total is even. It then counts subsets with sum `half` using the descending one-use table `ways`, where `ways[0] = 1` for the empty subset. The count includes subsets that are empty or complete, which are not legal groups.

The empty subset sums to `half` only when `half` is 0, and the complete set sums to `half` only when the total is 0. So the method subtracts 1 for each of those two cases. A legal split exists exactly when the remaining count is positive. For an array of zeros, the count is 2^n, and the subtraction leaves 2^n - 2, which is positive only for n of at least 2. The counts are `long` values, which cover 2^40.

**Complexity.**
- **Time** is O(n * half), because each element updates up to `half` entries.
- **Space** is O(half) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapDpcPartitionNonempty {
    /**
     * Returns whether nums splits into two nonempty groups with equal sums.
     * Time: O(n * half). Space: O(half).
     * Invariant: after each element, ways[s] counts subsets of the processed elements with sum s.
     */
    static boolean canSplit(int[] nums) {
        long total = 0;
        for (int x : nums) total += x;
        // An odd total cannot be halved.
        if (total % 2 != 0) return false;
        int half = (int) (total / 2);
        long[] ways = new long[half + 1];
        // The empty subset is one subset with sum 0.
        ways[0] = 1;
        for (int x : nums) {
            // Descending sums keep ways[s - x] at the state before x, and x = 0 doubles every entry.
            for (int s = half; s >= x; s--) ways[s] += ways[s - x];
        }
        long legal = ways[half];
        // The empty subset reaches half only when half is 0.
        if (half == 0) legal--;
        // The complete set reaches half only when the total is 0.
        if (total == 0) legal--;
        return legal > 0;
    }

    /** Oracle: tests every proper nonempty subset. */
    static boolean oracle(int[] nums) {
        int n = nums.length;
        long total = 0;
        for (int x : nums) total += x;
        for (int mask = 1; mask < (1 << n) - 1; mask++) {
            long sum = 0;
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum * 2 == total) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canSplit(new int[] {0, 0})) throw new AssertionError("ex1");
        if (canSplit(new int[] {0})) throw new AssertionError("ex2");
        // A single positive element and an odd total cannot be split.
        if (canSplit(new int[] {6}) || canSplit(new int[] {1, 2, 4})) throw new AssertionError("no split");
        // A positive element beside a zero cannot be split, but two equal elements can.
        if (canSplit(new int[] {5, 0}) || !canSplit(new int[] {5, 5})) throw new AssertionError("pairs");
        // Forty zeros give 2^40 subsets, which a long holds exactly.
        if (!canSplit(new int[40])) throw new AssertionError("zeros");
        // The input array stays unchanged.
        int[] nums = {3, 0, 3};
        int[] copy = nums.clone();
        canSplit(nums);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs with many zeros against the subset oracle.
        Random rnd = new Random(2726);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[1 + rnd.nextInt(11)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(3) == 0 ? 0 : rnd.nextInt(9);
            if (canSplit(a) != oracle(a)) throw new AssertionError("random " + t + " " + Arrays.toString(a));
        }
    }
}
```

#### Solution: [Recognize] Target Sum (LeetCode 494)
<!-- id: cap-dpc-signed-range -->

**Approach.**
For a sign assignment, let P be the sum of the plus group. The signed sum equals `2P - total`, so the condition `lo <= s <= hi` is the same as `(total + lo) / 2 <= P <= (total + hi) / 2`. Because P is an integer, the lower bound rounds up and the upper bound rounds down. The method also clamps both bounds to the range 0 to `total`, since P is a sum of nonnegative elements within the total.

The method builds one table of subset counts with the descending loop, where `ways[p]` counts the subsets of the processed elements whose sum is `p`. It then adds the entries from the lower bound to the upper bound. An empty range gives 0. The floor division uses `Math.floorDiv`, so negative values round in the correct direction.

**Complexity.**
- **Time** is O(n * total) for the table and O(total) for the range sum.
- **Space** is O(total) for the count array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapDpcSignedRange {
    /**
     * Returns the number of sign assignments whose signed sum lies in [lo, hi].
     * Time: O(n * total). Space: O(total).
     * Invariant: after each element, ways[p] counts subsets of the processed elements with sum p.
     */
    static long countInRange(int[] nums, int lo, int hi) {
        int total = 0;
        for (int x : nums) total += x;
        long[] ways = new long[total + 1];
        // The empty subset is one subset with sum 0.
        ways[0] = 1;
        for (int x : nums) {
            // Descending sums keep ways[p - x] at the state before x.
            for (int p = total; p >= x; p--) ways[p] += ways[p - x];
        }
        // The signed sum is 2p - total, so p must lie between the rounded-up and rounded-down bounds.
        int low = Math.max(0, -Math.floorDiv(-(total + lo), 2));
        int high = Math.min(total, Math.floorDiv(total + hi, 2));
        long count = 0;
        // An empty range adds nothing.
        for (int p = low; p <= high; p++) count += ways[p];
        return count;
    }

    /** Oracle: tries every sign assignment. */
    static long oracle(int[] nums, int lo, int hi) {
        long count = 0;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) sum += (mask >> i & 1) == 1 ? nums[i] : -nums[i];
            if (lo <= sum && sum <= hi) count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (countInRange(new int[] {1, 2, 3}, 0, 2) != 3) throw new AssertionError("ex1");
        if (countInRange(new int[] {4, 1, 3, 2}, -2, 3) != 6) throw new AssertionError("ex2");
        // A range that excludes every signed sum returns 0, and a point range equals the plain target count.
        if (countInRange(new int[] {1, 2}, 10, 20) != 0) throw new AssertionError("outside");
        if (countInRange(new int[] {1, 1, 1, 1, 1}, 3, 3) != 5) throw new AssertionError("point");
        // The input array stays unchanged.
        int[] nums = {2, 0, 5};
        int[] copy = nums.clone();
        countInRange(nums, -3, 3);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs, including zeros and ranges beyond the total, against the assignment oracle.
        Random rnd = new Random(2727);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(10)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(9);
            int lo = rnd.nextInt(61) - 30;
            int hi = lo + rnd.nextInt(30);
            if (countInRange(a, lo, hi) != oracle(a, lo, hi)) throw new AssertionError("random " + t);
        }
    }
}
```
