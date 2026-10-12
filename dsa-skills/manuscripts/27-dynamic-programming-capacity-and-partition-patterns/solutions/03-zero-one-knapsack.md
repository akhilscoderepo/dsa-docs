<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Zero-One Knapsack

#### Solution: [Build] One-Use Items (Author exercise)
<!-- id: cap-zok-one-use-items -->

**Approach.**
The table has one row for each item prefix. Entry `dp[i][c]` is the largest total value of a selection that uses only the first `i` items and weighs at most `c`. Row 0 is all zeros for the empty selection. For row `i`, the skip case copies `dp[i - 1][c]`. The take case applies only when `weight[i - 1] <= c`, and it adds `value[i - 1]` to `dp[i - 1][c - weight[i - 1]]`.

Both cases read row `i - 1` and write row `i`, so an entry never contains the item that it is adding. The invariant is that every row is final before the next row starts. The answer is the last row at `capacity`.

**Complexity.**
- **Time** is O(k * capacity), because each of the k rows fills `capacity + 1` entries with two reads.
- **Space** is O(k * capacity) for the table, and both input arrays stay unchanged.

```java run
import java.util.*;

public final class CapZokOneUseItems {
    /**
     * Returns the largest value of a one-use selection within capacity, using a full table.
     * Time: O(k * capacity). Space: O(k * capacity).
     * Invariant: row i is final before row i + 1 starts, and each row reads only the row before it.
     */
    static int tableBest(int[] weight, int[] value, int capacity) {
        int k = weight.length;
        // Row 0 is all zeros, because the empty prefix allows only the empty selection.
        int[][] dp = new int[k + 1][capacity + 1];
        // One row per item prefix costs k rows.
        for (int i = 1; i <= k; i++) {
            for (int c = 0; c <= capacity; c++) {
                // Skip case: the item stays out, so the previous row decides.
                dp[i][c] = dp[i - 1][c];
                // Take case: the item fits, so the rest comes from the previous row at the smaller capacity.
                if (weight[i - 1] <= c) {
                    dp[i][c] = Math.max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
                }
            }
        }
        // The last row at the full capacity covers every selection.
        return dp[k][capacity];
    }

    /** Oracle: tests every subset of the items. */
    static int oracle(int[] weight, int[] value, int capacity) {
        int n = weight.length;
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int w = 0, v = 0;
            for (int i = 0; i < n; i++) {
                if ((mask >> i & 1) == 1) {
                    w += weight[i];
                    v += value[i];
                }
            }
            if (w <= capacity) best = Math.max(best, v);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (tableBest(new int[] {1, 3, 4, 5}, new int[] {1, 4, 5, 7}, 7) != 9) throw new AssertionError("ex1");
        if (tableBest(new int[] {6, 7}, new int[] {3, 4}, 5) != 0) throw new AssertionError("ex2");
        // An empty item list and capacity 0 both return 0.
        if (tableBest(new int[] {}, new int[] {}, 9) != 0) throw new AssertionError("empty");
        if (tableBest(new int[] {2}, new int[] {5}, 0) != 0) throw new AssertionError("zero capacity");
        // A single item is used once, not twice.
        if (tableBest(new int[] {3}, new int[] {4}, 6) != 4) throw new AssertionError("single");
        // Both arrays stay unchanged.
        int[] w = {1, 3};
        int[] v = {2, 5};
        tableBest(w, v, 4);
        if (!Arrays.equals(w, new int[] {1, 3}) || !Arrays.equals(v, new int[] {2, 5})) throw new AssertionError("mutated");
        // Random inputs against the subset oracle.
        Random rnd = new Random(2706);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(9);
            int[] ww = new int[k];
            int[] vv = new int[k];
            for (int i = 0; i < k; i++) {
                ww[i] = 1 + rnd.nextInt(8);
                vv[i] = rnd.nextInt(15);
            }
            int cap = rnd.nextInt(30);
            if (tableBest(ww, vv, cap) != oracle(ww, vv, cap)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Descending Compression (Author exercise)
<!-- id: cap-zok-descending-compression -->

**Approach.**
One array `dp` of length `capacity + 1` holds the current row as it overwrites the previous row. For item `i`, the loop visits capacities from `capacity` down to `weight[i]`. When entry `c` is rewritten, every entry below `c` has not been rewritten yet for item `i`, so `dp[c - weight[i]]` still holds the previous row. The take value therefore never contains item `i`.

The invariant is that during item `i`, entries at or below the current index describe the previous row and entries above it describe the new row. After the last item, entry `c` is the best value at capacity `c`, so the whole array is the answer. The test compares every entry with a full table that has a separate row for each prefix.

**Complexity.**
- **Time** is O(k * capacity), because each item rewrites at most `capacity + 1` entries.
- **Space** is O(capacity) for the single array, and both input arrays stay unchanged.

```java run
import java.util.*;

public final class CapZokDescendingCompression {
    /**
     * Returns the best one-use value for every capacity from 0 to capacity.
     * Time: O(k * capacity). Space: O(capacity).
     * Invariant: entries at or below the current index hold the previous row.
     */
    static int[] bestRow(int[] weight, int[] value, int capacity) {
        // Every entry starts at 0 for the empty selection.
        int[] dp = new int[capacity + 1];
        for (int i = 0; i < weight.length; i++) {
            // Descending order keeps the smaller capacities unchanged until they are read.
            for (int c = capacity; c >= weight[i]; c--) {
                // The take value reads the previous row at the smaller capacity.
                int take = dp[c - weight[i]] + value[i];
                // The skip value is the entry before the rewrite.
                if (take > dp[c]) dp[c] = take;
            }
        }
        // The whole array is the final row.
        return dp;
    }

    /** Oracle: a full table with a separate row for each item prefix. */
    static int[] fullTable(int[] weight, int[] value, int capacity) {
        int k = weight.length;
        int[][] dp = new int[k + 1][capacity + 1];
        for (int i = 1; i <= k; i++) {
            for (int c = 0; c <= capacity; c++) {
                dp[i][c] = dp[i - 1][c];
                if (weight[i - 1] <= c) dp[i][c] = Math.max(dp[i][c], dp[i - 1][c - weight[i - 1]] + value[i - 1]);
            }
        }
        return dp[k];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(bestRow(new int[] {2, 3}, new int[] {3, 4}, 5), new int[] {0, 0, 3, 4, 4, 7})) throw new AssertionError("ex1");
        if (!Arrays.equals(bestRow(new int[] {4}, new int[] {9}, 3), new int[] {0, 0, 0, 0})) throw new AssertionError("ex2");
        // Capacity 0 returns a row of length 1.
        if (bestRow(new int[] {2}, new int[] {5}, 0).length != 1) throw new AssertionError("length");
        // Both input arrays stay unchanged.
        int[] w = {2, 3};
        int[] v = {3, 4};
        bestRow(w, v, 9);
        if (!Arrays.equals(w, new int[] {2, 3}) || !Arrays.equals(v, new int[] {3, 4})) throw new AssertionError("mutated");
        // Random inputs: every entry must equal the full table.
        Random rnd = new Random(2707);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(8);
            int[] ww = new int[k];
            int[] vv = new int[k];
            for (int i = 0; i < k; i++) {
                ww[i] = 1 + rnd.nextInt(8);
                vv[i] = rnd.nextInt(15);
            }
            int cap = rnd.nextInt(30);
            if (!Arrays.equals(bestRow(ww, vv, cap), fullTable(ww, vv, cap))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Ascending-Loop Counterexample (Author exercise)
<!-- id: cap-zok-ascending-counterexample -->

**Approach.**
The method builds two arrays with the same recurrence and different loop directions. The descending array is the correct one-use table. The ascending array lets entry `c` read `dp[c - weight[i]]` after item `i` has already rewritten it, so it can count item `i` several times. The method compares the arrays from capacity 0 upward and returns the first index where they differ, or -1 if they never differ.

A difference needs a repeated item, and the second copy of item `i` fits only when `c >= 2 * weight[i]`. So no index below the smallest such bound can differ, and an item with value 0 never raises an entry. The invariant for the descending array is the usual one: entries at or below the current index hold the previous row.

**Complexity.**
- **Time** is O(k * capacity) for the two tables and O(capacity) for the comparison.
- **Space** is O(capacity) for the two arrays, and both input arrays stay unchanged.

```java run
import java.util.*;

public final class CapZokAscendingCounterexample {
    /**
     * Returns the smallest capacity where the upward loop disagrees with the one-use table, or -1.
     * Time: O(k * capacity). Space: O(capacity).
     * Invariant: the descending array holds the correct one-use answers.
     */
    static int firstDifference(int[] weight, int[] value, int capacity) {
        int[] right = new int[capacity + 1];
        int[] wrong = new int[capacity + 1];
        for (int i = 0; i < weight.length; i++) {
            // The correct loop runs downward so that every read sees the previous row.
            for (int c = capacity; c >= weight[i]; c--) right[c] = Math.max(right[c], right[c - weight[i]] + value[i]);
            // The upward loop reads entries that the same item already rewrote.
            for (int c = weight[i]; c <= capacity; c++) wrong[c] = Math.max(wrong[c], wrong[c - weight[i]] + value[i]);
        }
        // The first mismatch from capacity 0 upward is the answer.
        for (int c = 0; c <= capacity; c++) if (right[c] != wrong[c]) return c;
        return -1;
    }

    /** Oracle: subset enumeration for the correct table, repeat enumeration for the upward table. */
    static int oracleDifference(int[] weight, int[] value, int capacity) {
        int n = weight.length;
        for (int c = 0; c <= capacity; c++) {
            int right = 0;
            for (int mask = 0; mask < (1 << n); mask++) {
                int w = 0, v = 0;
                for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) { w += weight[i]; v += value[i]; }
                if (w <= c) right = Math.max(right, v);
            }
            // The upward loop equals the best value when each item may repeat only if it was processed in order.
            int wrong = upwardOracle(weight, value, 0, c);
            if (right != wrong) return c;
        }
        return -1;
    }

    /** Value of the upward loop: each item repeats freely in item order, which is the repeatable table. */
    static int upwardOracle(int[] weight, int[] value, int i, int left) {
        if (i == weight.length) return 0;
        int best = 0;
        for (int copies = 0; copies * weight[i] <= left; copies++) {
            best = Math.max(best, copies * value[i] + upwardOracle(weight, value, i + 1, left - copies * weight[i]));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (firstDifference(new int[] {3}, new int[] {4}, 6) != 6) throw new AssertionError("ex1");
        if (firstDifference(new int[] {4}, new int[] {5}, 7) != -1) throw new AssertionError("ex2");
        // An item with value 0 never causes a difference, and an empty list agrees everywhere.
        if (firstDifference(new int[] {2}, new int[] {0}, 50) != -1) throw new AssertionError("zero value");
        if (firstDifference(new int[] {}, new int[] {}, 9) != -1) throw new AssertionError("empty");
        // Both input arrays stay unchanged.
        int[] w = {2, 5};
        int[] v = {3, 1};
        firstDifference(w, v, 9);
        if (!Arrays.equals(w, new int[] {2, 5}) || !Arrays.equals(v, new int[] {3, 1})) throw new AssertionError("mutated");
        // Random inputs against the enumeration oracle.
        Random rnd = new Random(2708);
        for (int t = 0; t < 1500; t++) {
            int k = rnd.nextInt(5);
            int[] ww = new int[k];
            int[] vv = new int[k];
            for (int i = 0; i < k; i++) {
                ww[i] = 1 + rnd.nextInt(6);
                vv[i] = rnd.nextInt(10);
            }
            int cap = rnd.nextInt(20);
            if (firstDifference(ww, vv, cap) != oracleDifference(ww, vv, cap)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Partition Equal Subset Sum (LeetCode 416)
<!-- id: cap-zok-equal-partition -->

**Approach.**
If the two groups have equal sums, each sums to half of the total, so the total must be even. The question becomes whether some subset of `nums` sums to `total / 2`, and then the rest sums to the same value. Each element weighs its own value and is used at most once, so the table is the one-use table with booleans: `reach[s]` is true when some subset of the elements processed so far sums to exactly `s`.

For each element `x`, the loop visits sums from `half` down to `x` and sets `reach[s]` when `reach[s - x]` is true. The descending order keeps `reach[s - x]` at the previous row, so no element is counted twice. The invariant is that `reach[s]` describes subsets of the processed elements. The answer is `reach[half]`.

**Complexity.**
- **Time** is O(n * total), because each element updates up to `total / 2` entries.
- **Space** is O(total) for the boolean array, and the input array stays unchanged.

```java run
import java.util.*;

public final class CapZokEqualPartition {
    /**
     * Returns whether nums splits into two groups with equal sums.
     * Time: O(n * total). Space: O(total).
     * Invariant: reach[s] is true when a subset of the processed elements sums to s.
     */
    static boolean canSplit(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        // An odd total cannot be halved into integers.
        if (total % 2 != 0) return false;
        int half = total / 2;
        boolean[] reach = new boolean[half + 1];
        // The empty subset sums to 0.
        reach[0] = true;
        for (int x : nums) {
            // Descending sums keep reach[s - x] at the previous row.
            for (int s = half; s >= x; s--) {
                // A sum becomes reachable when the sum x below it was reachable before this element.
                if (reach[s - x]) reach[s] = true;
            }
        }
        // One group sums to half exactly when half is reachable.
        return reach[half];
    }

    /** Oracle: tests every subset. */
    static boolean oracle(int[] nums) {
        int total = 0;
        for (int x : nums) total += x;
        for (int mask = 0; mask < (1 << nums.length); mask++) {
            int sum = 0;
            for (int i = 0; i < nums.length; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            if (sum * 2 == total) return true;
        }
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!canSplit(new int[] {3, 3, 6, 2, 4})) throw new AssertionError("ex1");
        if (canSplit(new int[] {2, 2, 3, 5})) throw new AssertionError("ex2");
        // One element can never be split, and two equal elements can.
        if (canSplit(new int[] {7})) throw new AssertionError("single");
        if (!canSplit(new int[] {4, 4})) throw new AssertionError("pair");
        // The input array stays unchanged.
        int[] nums = {3, 1, 4, 2};
        int[] copy = nums.clone();
        canSplit(nums);
        if (!Arrays.equals(nums, copy)) throw new AssertionError("mutated");
        // Random inputs against the subset oracle.
        Random rnd = new Random(2709);
        for (int t = 0; t < 3000; t++) {
            int[] a = new int[1 + rnd.nextInt(12)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(10);
            if (canSplit(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```
