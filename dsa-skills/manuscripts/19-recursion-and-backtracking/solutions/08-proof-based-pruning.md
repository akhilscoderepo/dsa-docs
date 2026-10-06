<!-- solutions-for: 08-proof-based-pruning -->
### Solutions For Proving A Branch Fails

#### Solution: [Build] Positive Remaining Sum (Author exercise)
<!-- id: bt-positive-remaining-sum -->

**Approach.**
The values are positive and sorted, so the sum of a path only grows as the path extends. A call with remaining target 0 has found a subset and returns true, which covers the empty subset for target 0. The loop starts at `start` and stops at the first value that exceeds the remaining target. That stop is safe, because every later value is at least as large, so adding it would overshoot and no extension could recover. A recursive call that returns true ends the whole search at once. If the loop ends, the call returns false.

**Complexity.**
- **Time** is O(2^n) in the worst case, and far less when the stop removes large values early.
- **Space** is O(n) for the stack.

```java run
import java.util.*;

public final class PositiveRemainingSum {
    /**
     * Returns true when some subset of the sorted positive values adds up to target.
     * Time: O(2^n) worst case. Space: O(n) stack frames.
     * Invariant: remain is target minus the sum of the path, and every later value is at least as large as the current one.
     */
    static boolean exists(int[] values, int target) {
        return go(0, target, values);
    }

    private static boolean go(int start, int remain, int[] a) {
        if (remain == 0) return true;                        // the path is a result, the empty path for target 0
        for (int i = start; i < a.length; i++) {
            if (a[i] > remain) break;                        // sorted positives: every later value overshoots too
            if (go(i + 1, remain - a[i], a)) return true;    // a success ends the search
        }
        return false;                                        // no extension of this path reaches the target
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!exists(new int[] {3, 4, 6, 9}, 10)) throw new AssertionError("ex1");
        if (exists(new int[] {5, 7}, 6)) throw new AssertionError("ex2");
        if (!exists(new int[] {}, 0)) throw new AssertionError("empty subset");
        if (exists(new int[] {}, 1)) throw new AssertionError("empty array");
        // Random sorted inputs must match a mask enumeration.
        Random rnd = new Random(1981);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(30);
            Arrays.sort(a);
            int target = rnd.nextInt(120);
            boolean want = false;
            for (int mask = 0; mask < (1 << a.length) && !want; mask++) {
                int sum = 0;
                for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) sum += a[i];
                want = sum == target;
            }
            if (exists(a, target) != want) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Remaining-Slots Bound (Author exercise)
<!-- id: bt-remaining-slots-bound -->

**Approach.**
A call at index `start` has `left` slots to fill and a remaining target. The sorted order gives two bounds. The `left` smallest values from `start` are the next `left` values. The `left` largest values are the last `left` values of the array. If fewer than `left` indices remain, no extension fills the slots. If the sum of the next `left` values exceeds the remaining target, every extension is at least that sum, so the call returns 0. If the sum of the last `left` values falls below the remaining target, every extension is at most that sum, so the call returns 0. A call with no slots left counts 1 when the remaining target is 0. All three skips follow from the sorted order and the positive values, and they remove no result.

**Complexity.**
- **Time** is O(C(n, k)) in the worst case, and far less when the bounds cut early.
- **Space** is O(n) for the prefix sums and the stack.

```java run
import java.util.*;

public final class RemainingSlotsBound {
    /**
     * Counts subsets of exactly k indices of sorted positive values that add up to target.
     * Time: O(C(n, k)) worst case. Space: O(n).
     * Invariant: every skipped branch has a proven range of totals that excludes the remaining target.
     */
    static int count(int[] a, int k, int target) {
        int n = a.length;
        long[] pre = new long[n + 1];                        // pre[i] is the sum of a[0..i)
        for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
        return go(0, k, target, a, pre);
    }

    private static int go(int start, int left, long remain, int[] a, long[] pre) {
        int n = a.length;
        if (left == 0) return remain == 0 ? 1 : 0;           // all slots filled: the sum decides
        if (n - start < left) return 0;                      // slots bound: too few indices remain
        long smallest = pre[start + left] - pre[start];      // the next `left` values are the smallest completion
        long largest = pre[n] - pre[n - left];               // the last `left` values are the largest completion
        if (remain < smallest || remain > largest) return 0; // the range of reachable totals excludes remain
        int total = 0;
        for (int i = start; i < n; i++) {                    // choose index i as the next value
            if (a[i] > remain) break;                        // sorted positives: later values overshoot
            total += go(i + 1, left - 1, remain - a[i], a, pre);
        }
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(new int[] {1, 2, 3, 4, 5}, 2, 6) != 2) throw new AssertionError("ex1");
        if (count(new int[] {4, 9}, 3, 13) != 0) throw new AssertionError("ex2");
        if (count(new int[] {}, 1, 0) != 0) throw new AssertionError("empty array");
        // Random sorted inputs must match a mask enumeration over subsets of size k.
        Random rnd = new Random(1982);
        for (int t = 0; t < 400; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = 1 + rnd.nextInt(20);
            Arrays.sort(a);
            int k = 1 + rnd.nextInt(6), target = rnd.nextInt(80);
            int want = 0;
            for (int mask = 0; mask < (1 << a.length); mask++) {
                if (Integer.bitCount(mask) != k) continue;
                int sum = 0;
                for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) sum += a[i];
                if (sum == target) want++;
            }
            if (count(a, k, target) != want) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Negative Values Break Sum Pruning (Author exercise)
<!-- id: bt-negative-values-break-pruning -->

**Approach.**
With negative values, the sum of a path can pass the target and return, as in `[5, -3]` with target 2, so the overshoot rule is unsafe. The method precomputes two suffix arrays. The array `pos[i]` holds the sum of the positive values from index `i`, and `neg[i]` holds the sum of the negative values from index `i`. Every subset of the suffix has a total between `neg[i]` and `pos[i]`. A remaining target outside that range cannot be reached, so the call returns false. A remaining target of 0 returns true because the empty extension is a subset. This rule needs no assumption about the sign or the order of the values.

**Complexity.**
- **Time** is O(2^n) in the worst case, because totals inside the range may still fail to match.
- **Space** is O(n) for the two arrays and the stack.

```java run
import java.util.*;

public final class NegativeValuesBreakPruning {
    /**
     * Returns true when some subset of values adds up to target, for values of any sign.
     * Time: O(2^n) worst case. Space: O(n).
     * Invariant: every subset of the suffix from i has a total in [neg[i], pos[i]].
     */
    static boolean exists(int[] values, int target) {
        int n = values.length;
        int[] pos = new int[n + 1], neg = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {                   // suffix sums of the positive and the negative values
            pos[i] = pos[i + 1] + Math.max(values[i], 0);
            neg[i] = neg[i + 1] + Math.min(values[i], 0);
        }
        return go(0, target, values, pos, neg);
    }

    private static boolean go(int start, int remain, int[] a, int[] pos, int[] neg) {
        if (remain == 0) return true;                        // the empty extension completes the path
        if (remain > pos[start] || remain < neg[start]) return false;   // the range of reachable totals excludes remain
        for (int i = start; i < a.length; i++)               // choose index i
            if (go(i + 1, remain - a[i], a, pos, neg)) return true;
        return false;
    }

    /** The unsafe rule from the positive case, used to show that it fails here. */
    static boolean overshootRule(int start, int remain, int[] a) {
        if (remain == 0) return true;
        if (remain < 0) return false;                        // wrong when later values may be negative
        for (int i = start; i < a.length; i++) if (overshootRule(i + 1, remain - a[i], a)) return true;
        return false;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!exists(new int[] {5, -3}, 2)) throw new AssertionError("ex1");
        if (!exists(new int[] {6, -6, 1}, 7)) throw new AssertionError("ex2");
        if (!exists(new int[] {}, 0) || exists(new int[] {}, 3)) throw new AssertionError("empty");
        // The overshoot rule loses the recovery in [5, -3].
        if (overshootRule(0, 2, new int[] {5, -3})) throw new AssertionError("overshoot rule should fail");
        // Random inputs of any sign must match a mask enumeration.
        Random rnd = new Random(1983);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            int target = rnd.nextInt(81) - 40;
            boolean want = false;
            for (int mask = 0; mask < (1 << a.length) && !want; mask++) {
                int sum = 0;
                for (int i = 0; i < a.length; i++) if ((mask >> i & 1) == 1) sum += a[i];
                want = sum == target;
            }
            if (exists(a, target) != want) throw new AssertionError("random " + t);
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] N-Queens Count (LeetCode 51)
<!-- id: bt-n-queens-count -->

**Approach.**
The call at row `r` places one queen in row `r`, so rows never conflict. Two cells share a column when their column numbers are equal. They share a diagonal when `r - c` is equal, or when `r + c` is equal. The search keeps three boolean arrays for the columns, the differences `r - c + n - 1` and the sums `r + c`. A cell is rejected when any of its three marks is true. This rule is exact, so it removes no valid placement. A call places a queen by setting the three marks, calls the next row and clears the same marks. A call at row `n` counts one placement.

**Complexity.**
- **Time** is O(n!) in the worst case, and far less in practice, because every rejected cell removes a whole subtree.
- **Space** is O(n) for the three arrays of length `n` and `2n - 1` and the stack.

```java run
import java.util.*;

public final class NQueensCount {
    /**
     * Counts the placements of n non-attacking queens, one per row.
     * Time: O(n!) worst case. Space: O(n).
     * Invariant: the marks are true exactly for the columns and diagonals of the queens in rows above r.
     */
    static int count(int n) {
        return go(0, n, new boolean[n], new boolean[2 * n - 1], new boolean[2 * n - 1]);
    }

    private static int go(int r, int n, boolean[] col, boolean[] diff, boolean[] sum) {
        if (r == n) return 1;                                // every row holds a queen
        int total = 0;
        for (int c = 0; c < n; c++) {
            int d = r - c + n - 1, s = r + c;                // the indices of the two diagonals
            if (col[c] || diff[d] || sum[s]) continue;       // an earlier queen attacks this cell
            col[c] = diff[d] = sum[s] = true;                // choose: set the three marks
            total += go(r + 1, n, col, diff, sum);           // explore the next row
            col[c] = diff[d] = sum[s] = false;               // undo: clear the same three marks
        }
        return total;
    }

    /** Oracle: try every column assignment with distinct columns and check the diagonals pairwise. */
    static int oracle(int n) {
        int[] cols = new int[n]; int[] total = {0};
        permute(0, cols, new boolean[n], n, total);
        return total[0];
    }

    private static void permute(int r, int[] cols, boolean[] used, int n, int[] total) {
        if (r == n) {
            for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (Math.abs(cols[i] - cols[j]) == j - i) return;
            total[0]++; return;
        }
        for (int c = 0; c < n; c++) if (!used[c]) { used[c] = true; cols[r] = c; permute(r + 1, cols, used, n, total); used[c] = false; }
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (count(4) != 2) throw new AssertionError("ex1");
        if (count(3) != 0) throw new AssertionError("ex2");
        if (count(1) != 1 || count(2) != 0) throw new AssertionError("small boards");
        // Every size up to 8 must match the oracle, and the known counts of 6 and 8 must hold.
        for (int n = 1; n <= 8; n++) if (count(n) != oracle(n)) throw new AssertionError("oracle " + n);
        if (count(6) != 4 || count(8) != 92 || count(9) != 352) throw new AssertionError("known counts");
        System.out.println("ok");
    }
}
```
