<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Permutation Counts

#### Solution: [Build] Ordered Sums To Four (Author exercise)
<!-- id: cap-prm-ordered-sums -->

**Approach.**
The entry `ways[t]` counts the sequences of 1s and 2s that add up to `t`. The seed `ways[0] = 1` is the empty sequence. Every nonempty sequence ends in a 1 or a 2. Removing a final 1 leaves a sequence for `t - 1`, and removing a final 2 leaves a sequence for `t - 2`. So `ways[t]` equals `ways[t - 1]` plus `ways[t - 2]`, where the second term applies only for `t >= 2`.

The invariant is that every entry the loop has passed is exact. The totals run upward, so both earlier entries are final when `t` is computed. The values satisfy `ways[t] = F(t + 1)` for the Fibonacci numbers F(1) = F(2) = 1, and the test checks that fact for every total up to 60.

**Complexity.**
- **Time** is O(total), because each total does at most two additions.
- **Space** is O(total) for the table, and the input is a single integer.

```java run
import java.util.*;

public final class CapPrmOrderedSums {
    /**
     * Returns the number of ordered sequences of 1s and 2s that add up to total.
     * Time: O(total). Space: O(total).
     * Invariant: ways[s] is exact for every total s the loop has passed.
     */
    static long orderedSums(int total) {
        long[] ways = new long[total + 1];
        // The empty sequence adds up to 0.
        ways[0] = 1;
        // Increasing totals make both earlier entries final before they are read.
        for (int t = 1; t <= total; t++) {
            // A final 1 extends a sequence for t - 1.
            ways[t] += ways[t - 1];
            // A final 2 extends a sequence for t - 2, and it needs t >= 2.
            if (t >= 2) ways[t] += ways[t - 2];
        }
        return ways[total];
    }

    /** Oracle: recursion on the first element. */
    static long oracle(int left) {
        if (left == 0) return 1;
        long count = oracle(left - 1);
        if (left >= 2) count += oracle(left - 2);
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (orderedSums(4) != 5) throw new AssertionError("ex1");
        if (orderedSums(0) != 1) throw new AssertionError("ex2");
        // Total 1 has the single sequence 1.
        if (orderedSums(1) != 1) throw new AssertionError("one");
        // Every small total against the recursion, and every total up to 60 against the Fibonacci identity.
        for (int n = 0; n <= 20; n++) if (orderedSums(n) != oracle(n)) throw new AssertionError("n=" + n);
        long prev = 1, cur = 1;
        for (int n = 0; n <= 60; n++) {
            // prev and cur hold F(n + 1) and F(n + 2) at the start of each pass.
            if (orderedSums(n) != prev) throw new AssertionError("fib " + n);
            long next = prev + cur;
            prev = cur;
            cur = next;
        }
    }
}
```

#### Solution: [Vary] Combination Sum IV (LeetCode 377)
<!-- id: cap-prm-combination-sum-four -->

**Approach.**
The entry `ways[t]` counts the sequences whose values add up to `t`, with the seed `ways[0] = 1`. The last element of a nonempty sequence with sum `t` is some value `v` with `v <= t`, and removing it leaves a sequence with sum `t - v`. The pairing between sequences and their last elements is one to one, so `ways[t]` is the sum of `ways[t - v]` over all values `v` that fit.

The totals form the outer loop, in increasing order, and the values form the inner loop. When the loop reaches `t`, every smaller total is final, so each `ways[t - v]` is exact. The invariant is that each entry the loop has passed equals the number of sequences with that sum. The values must be positive for this order to work.

**Complexity.**
- **Time** is O(target * k) for k values, because each total tries each value once.
- **Space** is O(target) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPrmCombinationSumFour {
    /**
     * Returns the number of ordered sequences of values from nums that add up to target.
     * Time: O(target * k). Space: O(target).
     * Invariant: ways[s] is the exact number of sequences with sum s for every total the loop has passed.
     */
    static long sequences(int[] nums, int target) {
        long[] ways = new long[target + 1];
        // The empty sequence adds up to 0.
        ways[0] = 1;
        // Totals outside: every smaller total is final when t is computed.
        for (int t = 1; t <= target; t++) {
            // Values inside: each value tries to be the last element.
            for (int value : nums) {
                // A value above t cannot be the last element.
                if (value <= t) ways[t] += ways[t - value];
            }
        }
        return ways[target];
    }

    /** The combination loop of the previous lesson, kept to show that it counts fewer. */
    static long combinations(int[] nums, int target) {
        long[] ways = new long[target + 1];
        ways[0] = 1;
        for (int value : nums) {
            for (int t = value; t <= target; t++) ways[t] += ways[t - value];
        }
        return ways[target];
    }

    /** Oracle: recursion on the first element. */
    static long oracle(int[] nums, int left) {
        if (left == 0) return 1;
        long count = 0;
        for (int value : nums) if (value <= left) count += oracle(nums, left - value);
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (sequences(new int[] {2, 3, 6}, 8) != 6) throw new AssertionError("ex1");
        if (sequences(new int[] {5}, 3) != 0) throw new AssertionError("ex2");
        // The maintenance window: five sequences but three combinations.
        if (sequences(new int[] {1, 2}, 4) != 5 || combinations(new int[] {1, 2}, 4) != 3) throw new AssertionError("window");
        // Target 0 has the empty sequence.
        if (sequences(new int[] {7}, 0) != 1) throw new AssertionError("zero");
        // The input array stays unchanged.
        int[] nums = {3, 1, 2};
        int[] copy = nums.clone();
        sequences(nums, 9);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the recursive oracle.
        Random rnd = new Random(2721);
        for (int t = 0; t < 2000; t++) {
            int k = 1 + rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(8));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int target = rnd.nextInt(18);
            if (sequences(c, target) != oracle(c, target)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Overflow And Nonpositive Values (Author exercise)
<!-- id: cap-prm-overflow-nonpositive -->

**Approach.**
A value of zero or less breaks the evaluation order. For a value `v <= 0`, the index `t - v` is at least `t`, so the update would read the entry being written or an entry that is not final, and for a negative `v` the index can also leave the table. The method therefore skips every value that is not positive. After that filter, every transition lowers the total by at least 1, and the totals-outside loop is valid.

The table type is `long`, because the number of sequences grows exponentially: the values 1, 2 and 3 with target 40 give about 2.4 * 10^10, which does not fit in an `int`. The test asserts that count. The seed `ways[0] = 1` makes the empty sequence count for target 0, so an empty array still returns 1 there.

**Complexity.**
- **Time** is O(target * k), because each total tries each value once and a skipped value costs O(1).
- **Space** is O(target) for the table, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPrmOverflowNonpositive {
    /**
     * Returns the number of ordered sequences of the positive values of nums that add up to target.
     * Time: O(target * k). Space: O(target).
     * Invariant: ways[s] is exact for every total the loop has passed, and every transition lowers the total.
     */
    static long sequences(int[] nums, int target) {
        long[] ways = new long[target + 1];
        // The empty sequence adds up to 0.
        ways[0] = 1;
        for (int t = 1; t <= target; t++) {
            for (int value : nums) {
                // A non-positive value would read an unfinished entry, and a large one does not fit.
                if (value <= 0 || value > t) continue;
                ways[t] += ways[t - value];
            }
        }
        return ways[target];
    }

    /** Oracle: recursion over the positive values only. */
    static long oracle(int[] nums, int left) {
        if (left == 0) return 1;
        long count = 0;
        for (int value : nums) if (value > 0 && value <= left) count += oracle(nums, left - value);
        return count;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (sequences(new int[] {0, -2, 3}, 6) != 1) throw new AssertionError("ex1");
        if (sequences(new int[] {}, 0) != 1) throw new AssertionError("ex2");
        // Only non-positive values leave nothing for a positive target.
        if (sequences(new int[] {0, -1, -5}, 4) != 0) throw new AssertionError("nonpositive only");
        // Java fact: the count for the values 1, 2, 3 and target 40 exceeds the int range.
        long big = sequences(new int[] {1, 2, 3}, 40);
        if (big <= Integer.MAX_VALUE) throw new AssertionError("should exceed int");
        // The input array stays unchanged.
        int[] nums = {3, 0, -1};
        int[] copy = nums.clone();
        sequences(nums, 9);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs with non-positive values against the recursive oracle.
        Random rnd = new Random(2722);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(5);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(rnd.nextInt(11) - 3);
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int target = rnd.nextInt(16);
            if (sequences(c, target) != oracle(c, target)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Compare With Coin Change II (Author exercise)
<!-- id: cap-prm-compare-coin-change -->

**Approach.**
Both counts satisfy the same update, `ways[a] += ways[a - coin]`, and they differ only in which loop owns the outside. With the coins outside, every combination is written in one fixed order of denominations, so the table counts combinations. With the amounts outside and the coins inside, every coin is tried as the last element, so the table counts sequences.

The method builds both tables up to `amount` and compares them entry by entry, counting the amounts `a` where the sequence count is strictly larger. A sequence count is never below the combination count, because every combination has at least one sequence. The invariant for each table is that every entry the loop has passed is exact for its question.

**Complexity.**
- **Time** is O(amount * k) for each table and O(amount) for the comparison.
- **Space** is O(amount) for the two tables, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapPrmCompareCoinChange {
    /**
     * Returns how many amounts a in 0..amount have more sequences than combinations.
     * Time: O(amount * k). Space: O(amount).
     * Invariant: combos[a] and seqs[a] are exact for every amount a the loops have passed.
     */
    static int differingAmounts(int[] coins, int amount) {
        long[] combos = new long[amount + 1];
        long[] seqs = new long[amount + 1];
        // Both tables start from the empty combination and the empty sequence.
        combos[0] = 1;
        seqs[0] = 1;
        // Coins outside: one fixed order of denominations per combination.
        for (int coin : coins) {
            for (int a = coin; a <= amount; a++) combos[a] += combos[a - coin];
        }
        // Amounts outside: every coin is tried as the last element.
        for (int a = 1; a <= amount; a++) {
            for (int coin : coins) if (coin <= a) seqs[a] += seqs[a - coin];
        }
        // Count the amounts where order creates extra sequences.
        int differing = 0;
        for (int a = 0; a <= amount; a++) if (seqs[a] > combos[a]) differing++;
        return differing;
    }

    /** Oracle: counts combinations and sequences by recursion for each amount. */
    static int oracle(int[] coins, int amount) {
        int differing = 0;
        for (int a = 0; a <= amount; a++) {
            if (seqOracle(coins, a) > comboOracle(coins, 0, a)) differing++;
        }
        return differing;
    }

    static long comboOracle(int[] coins, int i, int left) {
        if (i == coins.length) return left == 0 ? 1 : 0;
        long total = 0;
        for (int copies = 0; copies * coins[i] <= left; copies++) total += comboOracle(coins, i + 1, left - copies * coins[i]);
        return total;
    }

    static long seqOracle(int[] coins, int left) {
        if (left == 0) return 1;
        long total = 0;
        for (int coin : coins) if (coin <= left) total += seqOracle(coins, left - coin);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (differingAmounts(new int[] {1, 2}, 4) != 2) throw new AssertionError("ex1");
        if (differingAmounts(new int[] {3}, 10) != 0) throw new AssertionError("ex2");
        // Amount 0 never differs, because both counts are 1.
        if (differingAmounts(new int[] {2, 5}, 0) != 0) throw new AssertionError("zero");
        // The input array stays unchanged.
        int[] coins = {2, 1};
        int[] copy = coins.clone();
        differingAmounts(coins, 12);
        if (!Arrays.equals(coins, copy)) throw new AssertionError("mutated");
        // Random inputs against the recursive oracle.
        Random rnd = new Random(2723);
        for (int t = 0; t < 1000; t++) {
            int k = 1 + rnd.nextInt(4);
            Set<Integer> chosen = new LinkedHashSet<>();
            while (chosen.size() < k) chosen.add(1 + rnd.nextInt(7));
            int[] c = chosen.stream().mapToInt(Integer::intValue).toArray();
            int amount = rnd.nextInt(14);
            if (differingAmounts(c, amount) != oracle(c, amount)) throw new AssertionError("random " + t);
        }
    }
}
```
