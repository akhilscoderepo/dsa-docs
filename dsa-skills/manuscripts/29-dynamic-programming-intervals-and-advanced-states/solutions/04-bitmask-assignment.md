<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Bitmask Assignment

#### Solution: [Build] Set Test And Clear Bits (Author exercise)
<!-- id: dp29-set-test-clear -->

**Approach.**
The integer `mask` starts at 0, which is the empty set. Adding item `i` ORs the mask with `1 << i`, which sets bit `i` and leaves every other bit alone. Removing item `i` ANDs the mask with the complement of `1 << i`, which clears bit `i` and also works when the bit is already 0. All additions run before all removals, in the order the arrays give.

The invariant is that after each update, bit `i` is 1 exactly when item `i` has been added more recently than it was removed. Because `n <= 30`, every shift stays below bit 31, so the sign bit is never set and the result is nonnegative.

**Complexity.**
- **Time** is O(a + r), where `a` and `r` are the array lengths, because each update is one bit operation.
- **Space** is O(1), because the whole set lives in one `int`.

```java run
import java.util.*;

public final class Dp29SetTestClear {
    /**
     * Returns the integer set after all additions and then all removals.
     * Time: O(a + r). Space: O(1).
     * Invariant: bit i is 1 exactly when item i is currently in the set.
     */
    static int apply(int n, int[] add, int[] remove) {
        // Zero is the empty set because no bit is set.
        int mask = 0;
        // Each addition sets one bit and keeps the others.
        for (int item : add) {
            mask |= 1 << item;
        }
        // Each removal clears one bit, and clearing a bit that is 0 changes nothing.
        for (int item : remove) {
            mask &= ~(1 << item);
        }
        // The integer is the complete answer.
        return mask;
    }

    /** Oracle: keeps the set in a boolean array and rebuilds the integer from it. */
    static int oracle(int n, int[] add, int[] remove) {
        boolean[] in = new boolean[n];
        for (int item : add) in[item] = true;
        for (int item : remove) in[item] = false;
        int value = 0;
        for (int i = 0; i < n; i++) if (in[i]) value += 1 << i;
        return value;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (apply(5, new int[]{0, 2, 4}, new int[]{2}) != 17) throw new AssertionError("ex1");
        if (apply(4, new int[]{1, 1, 3}, new int[]{0}) != 10) throw new AssertionError("ex2");
        // Empty arrays leave the empty set, and removing an absent item changes nothing.
        if (apply(3, new int[]{}, new int[]{}) != 0) throw new AssertionError("empty");
        if (apply(3, new int[]{}, new int[]{1}) != 0) throw new AssertionError("absent");
        // The operators behave as the approach claims on small values.
        if ((1 << 3) != 8) throw new AssertionError("shift");
        if ((5 | (1 << 1)) != 7) throw new AssertionError("or");
        if ((7 & ~(1 << 1)) != 5) throw new AssertionError("andnot");
        if (((5 >> 2) & 1) != 1 || ((5 >> 1) & 1) != 0) throw new AssertionError("test");
        // With n = 30 the highest item is bit 29, so the result stays positive.
        if (apply(30, new int[]{29}, new int[]{}) <= 0) throw new AssertionError("sign");
        // Random inputs against the boolean array oracle.
        Random rnd = new Random(2901);
        for (int t = 0; t < 3000; t++) {
            int n = rnd.nextInt(31);
            if (n == 0) continue;
            int[] add = pick(rnd, n);
            int[] remove = pick(rnd, n);
            if (apply(n, add, remove) != oracle(n, add, remove)) throw new AssertionError("random " + t);
        }
    }

    static int[] pick(Random rnd, int n) {
        int[] a = new int[rnd.nextInt(12)];
        for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(n);
        return a;
    }
}
```

#### Solution: [Vary] Minimum Assignment Cost (Author exercise)
<!-- id: dp29-min-assignment-cost -->

**Approach.**
The mask ranges over the `m` columns. Entry `dp[mask]` is the smallest cost of giving the first `popcount(mask)` rows different columns, using exactly the columns in `mask`. A mask with more than `n` bits is skipped, because only `n` rows exist. For a nonempty mask, row `popcount(mask) - 1` takes one column `j` of the mask, and the rest come from `dp[mask ^ (1 << j)]`.

The invariant is that `mask ^ (1 << j)` is smaller than `mask`, so every entry is final when read. The answer is the smallest `dp[mask]` over the masks with exactly `n` bits, since the unused columns are free to stay out of the mask.

**Complexity.**
- **Time** is O(m * 2^m), because each of the `2^m` masks tries at most `m` columns.
- **Space** is O(2^m) for the array of entries.

```java run
import java.util.*;

public final class Dp29MinAssignmentCost {
    /**
     * Returns the smallest total cost of giving every row a different column.
     * Time: O(m * 2^m). Space: O(2^m).
     * Invariant: dp[mask] is final once the loop passes mask, and bit j means column j is used.
     */
    static int minCost(int[][] cost) {
        int n = cost.length;
        int m = cost[0].length;
        // One entry per set of columns; a very large value marks an unreachable set.
        int[] dp = new int[1 << m];
        Arrays.fill(dp, Integer.MAX_VALUE);
        // Zero columns used costs nothing.
        dp[0] = 0;
        int answer = Integer.MAX_VALUE;
        // Counting up guarantees that every smaller mask is final first.
        for (int mask = 1; mask < (1 << m); mask++) {
            // The popcount is the number of rows already served.
            int served = Integer.bitCount(mask);
            // A mask with more bits than rows cannot be reached.
            if (served > n) continue;
            int w = served - 1;
            int best = Integer.MAX_VALUE;
            // Try each column of the mask as the one that row w takes.
            for (int j = 0; j < m; j++) {
                if ((mask >> j & 1) == 1) {
                    best = Math.min(best, dp[mask ^ (1 << j)] + cost[w][j]);
                }
            }
            dp[mask] = best;
            // Only masks with exactly n bits are complete assignments.
            if (served == n) answer = Math.min(answer, best);
        }
        return answer;
    }

    /** Oracle: recursive search over all injective column choices. */
    static int oracle(int[][] cost, int row, boolean[] used) {
        if (row == cost.length) return 0;
        int best = Integer.MAX_VALUE;
        for (int j = 0; j < used.length; j++) {
            if (!used[j]) {
                used[j] = true;
                best = Math.min(best, cost[row][j] + oracle(cost, row + 1, used));
                used[j] = false;
            }
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCost(new int[][]{{4, 2, 8}, {4, 3, 7}}) != 6) throw new AssertionError("ex1");
        if (minCost(new int[][]{{5, 9, 1, 6}}) != 1) throw new AssertionError("ex2");
        // The square case matches the lesson example 10.
        if (minCost(new int[][]{{3, 3, 9}, {2, 8, 9}, {7, 6, 5}}) != 10) throw new AssertionError("square");
        // Integer.bitCount counts the 1 bits.
        if (Integer.bitCount(0b10110) != 3) throw new AssertionError("bitCount");
        // Random matrices against the recursive oracle.
        Random rnd = new Random(2902);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(4);
            int m = n + rnd.nextInt(3);
            int[][] c = new int[n][m];
            for (int[] row : c) for (int j = 0; j < m; j++) row[j] = rnd.nextInt(20);
            if (minCost(c) != oracle(c, 0, new boolean[m])) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Full Mask And State Count (Author exercise)
<!-- id: dp29-full-mask-count -->

**Approach.**
The full mask for `n` items has bits 0 to n - 1 set, so it equals `(1 << n) - 1`. The masks from 0 to the full mask number `1 << n`, which is `full + 1`. Each state needs 4 bytes in an `int[]`, so the byte count is the state count times 4. For n = 30 the state count is 1,073,741,824 and the byte count is 4,294,967,296, which exceeds `Integer.MAX_VALUE`. The method therefore computes every value as a `long`, with `1L << n`.

The invariant is that the three returned values satisfy `states = full + 1` and `bytes = 4 * states`. For n = 0 the full mask is 0 and the single state is the empty set.

**Complexity.**
- **Time** is O(1), because the method does three arithmetic operations.
- **Space** is O(1), because it returns three numbers.

```java run
import java.util.*;

public final class Dp29FullMaskCount {
    /**
     * Returns {full mask, state count, bytes of an int table with one entry per state}.
     * Time: O(1). Space: O(1).
     * Invariant: states = full + 1 and bytes = 4 * states, all in long arithmetic.
     */
    static long[] budget(int n) {
        // A long shift avoids the int overflow that begins at bit 31.
        long states = 1L << n;
        // The full mask has bits 0 to n - 1 set, which is one less than the state count.
        long full = states - 1;
        // Each int entry takes 4 bytes.
        long bytes = 4 * states;
        return new long[]{full, states, bytes};
    }

    /** Oracle: counts masks by looping, and builds the full mask by setting bits one at a time. */
    static long[] oracle(int n) {
        long count = 0;
        for (int mask = 0; mask < (1 << n); mask++) count++;
        long full = 0;
        for (int i = 0; i < n; i++) full |= 1L << i;
        return new long[]{full, count, 4 * count};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(budget(3), new long[]{7, 8, 32})) throw new AssertionError("ex1");
        if (!Arrays.equals(budget(0), new long[]{0, 1, 4})) throw new AssertionError("ex2");
        // The largest allowed n needs a byte count above the int range.
        long[] big = budget(30);
        if (big[2] != 4294967296L || big[2] <= Integer.MAX_VALUE) throw new AssertionError("big");
        // An int shift of 31 reaches the sign bit, and an int shift of 32 wraps to a shift of 0.
        if ((1 << 31) >= 0) throw new AssertionError("int 31");
        if ((1 << 32) != 1) throw new AssertionError("int 32");
        if ((1L << 31) != 2147483648L) throw new AssertionError("long 31");
        // The int full mask for n = 30 is still positive.
        if (((1 << 30) - 1) != 1073741823) throw new AssertionError("full 30");
        // Small n against the counting oracle.
        for (int n = 0; n <= 20; n++) {
            if (!Arrays.equals(budget(n), oracle(n))) throw new AssertionError("n " + n);
        }
    }
}
```

#### Solution: [Recognize] Partition To K Equal Sum Subsets (LeetCode 698)
<!-- id: dp29-partition-k-subsets -->

**Approach.**
Let `total` be the sum of `nums`. If `total` is not divisible by `k`, the answer is false. Otherwise the target is `t = total / k`, and a number larger than `t` makes the answer false. Entry `fill[mask]` stores the fill of the group in progress after the numbers in `mask` are placed, as `sum(mask) % t`, or -1 when the placement is impossible. The set of placed numbers is the mask, and the fill is the second state part.

From a reachable mask, the method tries each unplaced number `j`. It is allowed when `fill[mask] + nums[j] <= t`. The new fill is `(fill[mask] + nums[j]) % t`, which becomes 0 when a group closes exactly. The invariant is that every reachable mask has placed numbers whose sum is `groups * t + fill`, with all closed groups equal to `t`. The answer is true when `fill[full]` is 0, which means the last group also closed.

**Complexity.**
- **Time** is O(n * 2^n), because each of the `2^n` masks tries at most `n` numbers.
- **Space** is O(2^n) for the `fill` array.

```java run
import java.util.*;

public final class Dp29PartitionKSubsets {
    /**
     * Returns true when nums splits into k groups with equal sums.
     * Time: O(n * 2^n). Space: O(2^n).
     * Invariant: fill[mask] is the sum of the open group, or -1 when mask cannot be placed.
     */
    static boolean canPartition(int[] nums, int k) {
        int n = nums.length;
        int total = 0;
        for (int x : nums) total += x;
        // A total that k cannot divide rules out equal groups.
        if (total % k != 0) return false;
        int t = total / k;
        // One entry per set of placed numbers; -1 marks an impossible set.
        int[] fill = new int[1 << n];
        Arrays.fill(fill, -1);
        fill[0] = 0;
        // Counting up visits every set after all of its subsets.
        for (int mask = 0; mask < (1 << n); mask++) {
            // Unreachable sets cannot extend.
            if (fill[mask] < 0) continue;
            // Try each unplaced number as the next one in the open group.
            for (int j = 0; j < n; j++) {
                if ((mask >> j & 1) == 0 && fill[mask] + nums[j] <= t) {
                    // The remainder is 0 exactly when the open group reaches t and closes.
                    fill[mask | (1 << j)] = (fill[mask] + nums[j]) % t;
                }
            }
        }
        // All numbers placed and no open group left means every group has sum t.
        return fill[(1 << n) - 1] == 0;
    }

    /** Oracle: assigns each number to one of k groups in every possible way and compares the sums. */
    static boolean oracle(int[] nums, int k) {
        int n = nums.length;
        int combos = 1;
        for (int i = 0; i < n; i++) combos *= k;
        for (int code = 0; code < combos; code++) {
            int[] sums = new int[k];
            boolean[] used = new boolean[k];
            int c = code;
            for (int i = 0; i < n; i++) {
                sums[c % k] += nums[i];
                used[c % k] = true;
                c /= k;
            }
            boolean ok = true;
            for (int g = 0; g < k; g++) if (!used[g] || sums[g] != sums[0]) ok = false;
            if (ok) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canPartition(new int[]{2, 2, 2, 3, 3}, 2)) throw new AssertionError("ex1");
        if (canPartition(new int[]{5, 5, 5, 5, 2, 2}, 3)) throw new AssertionError("ex2");
        // One group always works, and an indivisible total never does.
        if (!canPartition(new int[]{4}, 1)) throw new AssertionError("single");
        if (canPartition(new int[]{1, 2, 3, 4}, 3)) throw new AssertionError("indivisible");
        // The remainder operator returns 0 when a group closes exactly.
        if ((4 + 2) % 6 != 0 || (4 + 1) % 6 != 5) throw new AssertionError("remainder");
        // Random inputs against the assignment oracle.
        Random rnd = new Random(2903);
        for (int t = 0; t < 1500; t++) {
            int n = 1 + rnd.nextInt(7);
            int k = 1 + rnd.nextInt(Math.min(3, n));
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = 1 + rnd.nextInt(5);
            if (canPartition(nums, k) != oracle(nums, k)) throw new AssertionError("random " + t);
        }
    }
}
```
