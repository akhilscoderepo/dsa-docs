<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Linear Recurrence

#### Solution: [Build] Climbing Stairs (LeetCode 70)
<!-- id: dp-linrec-climb-stairs -->

**Approach.**
The method stores `ways[i]`, the number of move lists that reach step `i`. The table has `n + 2` slots, so the base cases `ways[0] = 1` and `ways[1] = 1` exist for every allowed `n`. A move list that reaches step `i` ends with a move of 1 from step `i - 1` or a move of 2 from step `i - 2`. These two groups share no list, so `ways[i]` is their sum.

The invariant is that every entry below `i` is final when the loop reaches `i`. The type matters too. The value for `n = 45` is 1836311903 and fits in an `int`, while the value for `n = 46` is 2971215073 and wraps. The tests assert both facts.

**Complexity.**
- **Time** is O(n), because the loop computes each entry from two earlier entries once.
- **Space** is O(n) for the table, since no entry is discarded before the end.

```java run
public final class DpLinrecClimbStairs {
    /**
     * Returns the number of ordered move lists of 1s and 2s that add up to n.
     * Time: O(n). Space: O(n).
     * Invariant: before iteration i, ways[0..i-1] are final counts.
     */
    static int climb(int n) {
        // Two spare slots keep ways[1] legal for every n.
        int[] ways = new int[n + 2];
        // The empty move list reaches step 0, and one move of 1 reaches step 1.
        ways[0] = 1;
        ways[1] = 1;
        // Each step reads the two entries below it, so the loop costs O(n).
        for (int i = 2; i <= n; i++) {
            // The last move is 1 or 2, and the two groups are disjoint.
            ways[i] = ways[i - 1] + ways[i - 2];
        }
        // The last entry answers the question for the full staircase.
        return ways[n];
    }

    /** Oracle: builds every move list recursively and counts the lists that land on n. */
    static int oracle(int stepsLeft) {
        if (stepsLeft == 0) return 1;
        int total = oracle(stepsLeft - 1);
        if (stepsLeft >= 2) total += oracle(stepsLeft - 2);
        return total;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (climb(4) != 5) throw new AssertionError("ex1");
        if (climb(7) != 21) throw new AssertionError("ex2");
        // Java facts: n = 45 fits in an int, and the next value would wrap to a negative number.
        if (climb(45) != 1836311903) throw new AssertionError("n45");
        if ((int) (1836311903L + 1134903170L) >= 0) throw new AssertionError("wrap");
        // Every small n is checked against exhaustive enumeration.
        for (int n = 1; n <= 24; n++) {
            if (climb(n) != oracle(n)) throw new AssertionError("n=" + n);
        }
        // The table is strictly increasing from n = 2, which rules out a stale entry.
        for (int n = 2; n <= 45; n++) {
            if (climb(n) <= climb(n - 1)) throw new AssertionError("monotone " + n);
        }
    }
}
```

#### Solution: [Vary] Min Cost Climbing Stairs (LeetCode 746)
<!-- id: dp-linrec-min-cost-climb -->

**Approach.**
The method stores `dp[i]`, the lowest total price to stand on position `i`, for `i` from 0 to `cost.length`. Both starts are free, so `dp[0]` and `dp[1]` are 0. A climber reaches position `i` from `i - 1` after paying `cost[i - 1]`, or from `i - 2` after paying `cost[i - 2]`. The entry is the smaller of those two sums.

This invariant matches the counting version: both window entries are final before the loop uses them. The change is the combining operation, which is a minimum of two sums and not a sum of two counts. The method reads the array `cost` and never writes it, and the tests check that.

**Complexity.**
- **Time** is O(n), because each of the n - 1 entries takes one comparison of two sums.
- **Space** is O(n) for the table; the input array stays unchanged.

```java run
import java.util.*;

public final class DpLinrecMinCostClimb {
    /**
     * Returns the lowest price to reach position cost.length from a free start on step 0 or 1.
     * Time: O(n). Space: O(n).
     * Invariant: before iteration i, dp[0..i-1] hold the lowest prices to stand on those positions.
     */
    static int lowest(int[] cost) {
        int n = cost.length;
        // Java zero-fills the array, so dp[0] and dp[1] are the free starts.
        int[] dp = new int[n + 1];
        // Each position reads the two positions below it, so the loop costs O(n).
        for (int i = 2; i <= n; i++) {
            // Leaving position i - 1 or i - 2 costs the price printed on that step.
            dp[i] = Math.min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2]);
        }
        // The top is position n, one past the last step.
        return dp[n];
    }

    /** Oracle: tries every sequence of moves from both starts and keeps the cheapest. */
    static int oracle(int[] cost) {
        int best = Integer.MAX_VALUE;
        for (int start = 0; start <= 1; start++) best = Math.min(best, walk(cost, start));
        return best;
    }

    /** Returns the lowest price to reach the top from position pos. */
    static int walk(int[] cost, int pos) {
        if (pos >= cost.length) return 0;
        int best = cost[pos] + walk(cost, pos + 1);
        best = Math.min(best, cost[pos] + walk(cost, pos + 2));
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (lowest(new int[] {4, 2, 9, 1, 7}) != 3) throw new AssertionError("ex1");
        if (lowest(new int[] {5, 5}) != 5) throw new AssertionError("ex2");
        // The input array is read only.
        int[] c = {3, 1, 4, 1, 5};
        int[] copy = c.clone();
        lowest(c);
        if (!Arrays.equals(c, copy)) throw new AssertionError("mutated");
        // Random arrays against exhaustive search, including zero prices.
        Random rnd = new Random(2603);
        for (int t = 0; t < 3000; t++) {
            int[] cost = new int[2 + rnd.nextInt(10)];
            for (int i = 0; i < cost.length; i++) cost[i] = rnd.nextInt(20);
            if (lowest(cost) != oracle(cost)) throw new AssertionError("random " + t + " " + Arrays.toString(cost));
        }
    }
}
```

#### Solution: [Boundary] Short Arrays (Author exercise)
<!-- id: dp-linrec-short-arrays -->

**Approach.**
The method stores `dp[i]`, the highest score of a path that starts at cell 0 or 1 and ends on cell `i`. The empty array returns 0 first, and the one-cell array returns `gain[0]`, because cell 1 does not exist. For a longer array, `dp[0]` is `gain[0]`. The entry `dp[1]` is `gain[1] + max(0, dp[0])`, where the 0 stands for a path that starts on cell 1.

From cell 2 on, no path may start there, so `dp[i]` is `gain[i] + max(dp[i - 1], dp[i - 2])`. Values can be negative, so the maximum cannot ignore a bad predecessor, and the zero option appears only for cell 1. The invariant is that every entry below `i` is the best score over legal paths to that cell.

**Complexity.**
- **Time** is O(n), because each cell is processed once with a constant number of comparisons.
- **Space** is O(n) for `dp`; the input array stays unchanged.

```java run
import java.util.*;

public final class DpLinrecShortArrays {
    /**
     * Returns the highest score of a path from cell 0 or 1 to the last cell.
     * Time: O(n). Space: O(n).
     * Invariant: before iteration i, dp[0..i-1] hold the best score of legal paths ending there.
     */
    static int best(int[] gain) {
        int n = gain.length;
        // An empty array has no cells to visit, so the score is 0.
        if (n == 0) return 0;
        // A single cell is the only start and the only end.
        if (n == 1) return gain[0];
        int[] dp = new int[n];
        // Cell 0 is a start, so its best path is the cell alone.
        dp[0] = gain[0];
        // Cell 1 is either a second start or a step from cell 0.
        dp[1] = gain[1] + Math.max(0, dp[0]);
        // Each later cell reads the two cells below it, so the loop costs O(n).
        for (int i = 2; i < n; i++) {
            // Cell i is reached from cell i - 1 or i - 2, and both predecessors are legal paths.
            dp[i] = gain[i] + Math.max(dp[i - 1], dp[i - 2]);
        }
        // The path must end on the last cell.
        return dp[n - 1];
    }

    /** Oracle: enumerates every path from each legal start recursively. */
    static int oracle(int[] gain) {
        int n = gain.length;
        if (n == 0) return 0;
        int bestScore = Integer.MIN_VALUE;
        for (int start = 0; start <= 1 && start < n; start++) bestScore = Math.max(bestScore, walk(gain, start));
        return bestScore;
    }

    /** Returns the highest score of a path that begins at pos and ends on the last cell. */
    static int walk(int[] gain, int pos) {
        if (pos == gain.length - 1) return gain[pos];
        int result = Integer.MIN_VALUE;
        for (int move = 1; move <= 2; move++) {
            if (pos + move >= gain.length) continue;
            result = Math.max(result, gain[pos] + walk(gain, pos + move));
        }
        return result;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (best(new int[] {-3, 8}) != 8) throw new AssertionError("ex1");
        if (best(new int[] {2, -7, 4, -1, 5}) != 11) throw new AssertionError("ex2");
        // Short arrays: empty, one cell, and two cells with a negative start.
        if (best(new int[] {}) != 0) throw new AssertionError("empty");
        if (best(new int[] {-4}) != -4) throw new AssertionError("single");
        if (best(new int[] {5, 6}) != 11) throw new AssertionError("pair");
        // The input array is read only.
        int[] g = {1, -2, 3};
        int[] copy = g.clone();
        best(g);
        if (!Arrays.equals(g, copy)) throw new AssertionError("mutated");
        // Random arrays with negative values against exhaustive search.
        Random rnd = new Random(2604);
        for (int t = 0; t < 4000; t++) {
            int[] gain = new int[rnd.nextInt(10)];
            for (int i = 0; i < gain.length; i++) gain[i] = rnd.nextInt(21) - 10;
            if (best(gain) != oracle(gain)) throw new AssertionError("random " + t + " " + Arrays.toString(gain));
        }
    }
}
```

#### Solution: [Recognize] N-th Tribonacci Number (LeetCode 1137)
<!-- id: dp-linrec-tribonacci -->

**Approach.**
The method stores `t[i]` with `T(i)` for `i` from 0 to `n`. The table needs three base cases, so the method answers `n` of 0, 1 and 2 directly and never reads a missing entry. For `n` of 3 or more, the loop starts at index 3 and computes `t[i]` as the sum of the three entries below it.

The invariant is that `t[i - 1]`, `t[i - 2]` and `t[i - 3]` are final when the loop reaches `i`. The window has width three, so the first index that reads all three base cases is 3. The largest allowed value, `T(37)`, is 2082876103 and fits in an `int`.

**Complexity.**
- **Time** is O(n), because each entry is a sum of three earlier entries.
- **Space** is O(n) for the table, since the method keeps every entry.

```java run
public final class DpLinrecTribonacci {
    /**
     * Returns T(n) for T(0)=0, T(1)=1, T(2)=1 and T(n)=T(n-1)+T(n-2)+T(n-3).
     * Time: O(n). Space: O(n).
     * Invariant: before iteration i, t[0..i-1] hold T(0)..T(i-1).
     */
    static int trib(int n) {
        // Small indexes return before the loop could read a missing base case.
        if (n == 0) return 0;
        if (n <= 2) return 1;
        int[] t = new int[n + 1];
        // The three base cases fill the window.
        t[1] = 1;
        t[2] = 1;
        // The first index that reads all three base cases is 3, and the loop costs O(n).
        for (int i = 3; i <= n; i++) {
            // Each entry sums the window of width three.
            t[i] = t[i - 1] + t[i - 2] + t[i - 3];
        }
        // The last entry is the requested term.
        return t[n];
    }

    /** Oracle: follows the definition by direct recursion. */
    static int oracle(int n) {
        if (n == 0) return 0;
        if (n <= 2) return 1;
        return oracle(n - 1) + oracle(n - 2) + oracle(n - 3);
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (trib(5) != 7) throw new AssertionError("ex1");
        if (trib(0) != 0) throw new AssertionError("ex2");
        // Java fact: the largest allowed term fits in an int.
        if (trib(37) != 2082876103) throw new AssertionError("n37");
        if (trib(37) < 0) throw new AssertionError("sign");
        // Every small index is checked against the recursive definition.
        for (int n = 0; n <= 22; n++) {
            if (trib(n) != oracle(n)) throw new AssertionError("n=" + n);
        }
        // Larger indexes satisfy the recurrence among neighbours.
        for (int n = 3; n <= 37; n++) {
            if (trib(n) != trib(n - 1) + trib(n - 2) + trib(n - 3)) throw new AssertionError("rec " + n);
        }
    }
}
```
