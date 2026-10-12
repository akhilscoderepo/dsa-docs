<!-- solutions-for: 26-dynamic-programming-foundations -->
### Solutions For Rolling State

#### Solution: [Build] Two-State Fibonacci (Author exercise)
<!-- id: dp-roll-two-state-fib -->

**Approach.**
The method returns `a` when n is 0 and `b` when n is 1, because those indices are seeds and no iteration computes them. For larger n, it keeps `older` for `f(i - 2)` and `newer` for `f(i - 1)`. Each iteration adds the two values in a `long`, reduces the sum modulo 1000000007, moves `newer` into `older`, and stores the sum in `newer`. The assignment of `older` runs before the assignment of `newer`, so the old `newer` is read before it is lost.

The invariant is that before the iteration for index `i`, `older` equals `f(i - 2)` and `newer` equals `f(i - 1)`. After the last iteration, `newer` equals `f(n)`. The sum of two reduced values is below 2 * 10^9 + 12, so a `long` is a safe choice and the tests also confirm that this sum fits in an `int`.

**Complexity.**
- **Time** is O(n), because the loop runs once for each index from 2 to n and each iteration does constant work.
- **Space** is O(1), because the method keeps two saved values and one sum.

```java run
import java.util.*;

public final class RollFib {
    static final int MOD = 1_000_000_007;

    /**
     * Returns f(n) for f(0)=a, f(1)=b, f(i)=(f(i-1)+f(i-2)) mod 1000000007.
     * Time: O(n). Space: O(1).
     * Invariant: before index i, older = f(i-2) and newer = f(i-1).
     */
    static int fib(int a, int b, int n) {
        // Indices 0 and 1 are seeds, so no iteration is needed for them.
        if (n == 0) return a;
        long older = a;
        long newer = b;
        // One iteration per computed index, so the loop costs O(n) time.
        for (int i = 2; i <= n; i++) {
            // The sum reads both saved values before either is overwritten.
            long next = (older + newer) % MOD;
            // The older slot is written first, so the old newer value is still available.
            older = newer;
            // The new value becomes the most recent saved value.
            newer = next;
        }
        // For n = 1 the loop never runs and newer still holds the seed b.
        return (int) newer;
    }

    /** Oracle: the full table. */
    static int oracle(int a, int b, int n) {
        long[] t = new long[Math.max(n + 1, 2)];
        t[0] = a;
        t[1] = b;
        for (int i = 2; i <= n; i++) t[i] = (t[i - 1] + t[i - 2]) % MOD;
        return (int) t[n];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (fib(0, 1, 10) != 55) throw new AssertionError("ex1");
        if (fib(1000000006, 1000000006, 2) != 1000000005) throw new AssertionError("ex2");
        // Boundary indices return the seeds directly.
        if (fib(3, 4, 0) != 3 || fib(3, 4, 1) != 4) throw new AssertionError("seeds");
        // Java fact: two reduced values sum to less than the int maximum, so int addition is safe here.
        int top = MOD - 1;
        if (top + top < 0 || (long) top + top != 2_000_000_012L) throw new AssertionError("int sum");
        // Random seeds and indices against the full table.
        Random rnd = new Random(2601);
        for (int t = 0; t < 3000; t++) {
            int a = rnd.nextInt(3) == 0 ? MOD - 1 - rnd.nextInt(3) : rnd.nextInt(MOD);
            int b = rnd.nextInt(MOD);
            int n = rnd.nextInt(200);
            if (fib(a, b, n) != oracle(a, b, n)) throw new AssertionError("random " + t);
        }
        // A large index runs in constant memory and matches the table.
        if (fib(7, 11, 3_000_000) != oracle(7, 11, 3_000_000)) throw new AssertionError("large");
    }
}
```

#### Solution: [Vary] House Robber (LeetCode 198)
<!-- id: dp-roll-robber-negative -->

**Approach.**
Let `best[i]` be the largest total over the first `i` houses. The last house is either skipped, which leaves `best[i - 1]`, or taken, which adds its value to `best[i - 2]`. So `best[i]` is the larger of the two. The method keeps `skip2` for `best[i - 2]` and `skip1` for `best[i - 1]`, and both start at 0, because zero houses give the empty selection with total 0.

The invariant is that before house `i`, `skip2` equals `best[i - 2]` and `skip1` equals `best[i - 1]`. Because the empty selection is allowed, a negative house never lowers `best`, since skipping it is always an option. The assignment of `skip2` runs before the assignment of `skip1`. The tests compare against a bitmask search over every legal selection.

**Complexity.**
- **Time** is O(n), because the loop visits each house once and does one comparison.
- **Space** is O(1), because two saved values replace the table of n + 1 entries.

```java run
import java.util.*;

public final class RollRobber {
    /**
     * Returns the largest total of a set of non-adjacent values, where the empty set is allowed.
     * Time: O(n). Space: O(1).
     * Invariant: before house i, skip2 = best over houses 0..i-2 and skip1 = best over houses 0..i-1.
     */
    static int rob(int[] nums) {
        // Zero houses give the empty selection, so both saved values start at 0.
        int skip2 = 0;
        int skip1 = 0;
        // One iteration per house, so the loop costs O(n) time.
        for (int v : nums) {
            // Taking the house adds v to the best total two houses back; skipping keeps skip1.
            int cur = Math.max(skip1, skip2 + v);
            // The older slot is written first so the old skip1 is read before it is replaced.
            skip2 = skip1;
            // The new total becomes the most recent saved value.
            skip1 = cur;
        }
        // skip1 holds the best total over all houses.
        return skip1;
    }

    /** Oracle: try every subset with no two adjacent indices. */
    static int oracle(int[] nums) {
        int n = nums.length;
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            if ((mask & (mask >> 1)) != 0) continue;
            int sum = 0;
            for (int i = 0; i < n; i++) if ((mask >> i & 1) == 1) sum += nums[i];
            best = Math.max(best, sum);
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (rob(new int[] {3, -2, 7, 5}) != 10) throw new AssertionError("ex1");
        if (rob(new int[] {-4, -1, -6}) != 0) throw new AssertionError("ex2");
        // Empty input and a single positive house.
        if (rob(new int[0]) != 0 || rob(new int[] {5}) != 5) throw new AssertionError("small");
        // The input is not changed.
        int[] keep = {6, -1, 6, 6};
        int[] copy = keep.clone();
        if (rob(keep) != 12 || !Arrays.equals(keep, copy)) throw new AssertionError("mutation");
        // Random arrays with negative values against the subset search.
        Random rnd = new Random(2602);
        for (int t = 0; t < 4000; t++) {
            int[] a = new int[rnd.nextInt(13)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(41) - 20;
            if (rob(a) != oracle(a)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Update Order (Author exercise)
<!-- id: dp-roll-update-order -->

**Approach.**
The method returns the seed `a`, `b` or `c` when n is 0, 1 or 2. For larger n, it keeps `x` for `t(i - 3)`, `y` for `t(i - 2)` and `z` for `t(i - 1)`. Each iteration computes the sum of the three values in a `long`, reduces it modulo 1000000007, and then shifts. The shift writes `x` from `y`, then `y` from `z`, then `z` from the new sum. Every variable is read by the assignment that follows it before the variable itself is overwritten.

The invariant is that before index `i`, the three variables equal `t(i - 3)`, `t(i - 2)` and `t(i - 1)`. The sum of three reduced values can reach about 3 * 10^9, which exceeds the largest `int`, so the addition must happen in `long`. The tests assert that overflow and compare against a full table.

**Complexity.**
- **Time** is O(n), because each of the n - 2 iterations performs one sum and three assignments.
- **Space** is O(1), because three saved values replace the table.

```java run
import java.util.*;

public final class RollTribonacci {
    static final int MOD = 1_000_000_007;

    /**
     * Returns t(n) for three seeds and t(i) = t(i-1) + t(i-2) + t(i-3) mod 1000000007.
     * Time: O(n). Space: O(1).
     * Invariant: before index i, x = t(i-3), y = t(i-2), z = t(i-1).
     */
    static int tri(int a, int b, int c, int n) {
        // Indices 0, 1 and 2 are seeds and never computed.
        if (n == 0) return a;
        if (n == 1) return b;
        if (n == 2) return c;
        long x = a, y = b, z = c;
        // Indices 3..n are computed, so the loop runs n - 2 times.
        for (int i = 3; i <= n; i++) {
            // The sum is formed in long because three values near the modulus exceed int.
            long next = (x + y + z) % MOD;
            // Oldest first: x takes y, so the old x is dropped after it has been read.
            x = y;
            // y takes z, which has not changed yet.
            y = z;
            // z takes the new value last.
            z = next;
        }
        // z holds t(n) after the last shift.
        return (int) z;
    }

    /** Oracle: the full table. */
    static int oracle(int a, int b, int c, int n) {
        long[] t = new long[Math.max(n + 1, 3)];
        t[0] = a;
        t[1] = b;
        t[2] = c;
        for (int i = 3; i <= n; i++) t[i] = (t[i - 1] + t[i - 2] + t[i - 3]) % MOD;
        return (int) t[n];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (tri(1, 2, 3, 6) != 37) throw new AssertionError("ex1");
        if (tri(1000000006, 1000000006, 1000000006, 3) != 1000000004) throw new AssertionError("ex2");
        // Seeds for n = 0, 1, 2.
        if (tri(5, 6, 7, 0) != 5 || tri(5, 6, 7, 1) != 6 || tri(5, 6, 7, 2) != 7) throw new AssertionError("seeds");
        // Java fact: three reduced values overflow int but not long.
        int top = MOD - 1;
        if (top + top + top >= 0) throw new AssertionError("int should overflow");
        if ((long) top * 3 != 3_000_000_018L) throw new AssertionError("long sum");
        // Random seeds and indices against the full table.
        Random rnd = new Random(2603);
        for (int t = 0; t < 3000; t++) {
            int a = rnd.nextInt(3) == 0 ? MOD - 1 : rnd.nextInt(MOD);
            int b = rnd.nextInt(MOD);
            int c = rnd.nextInt(3) == 0 ? MOD - 1 : rnd.nextInt(MOD);
            int n = rnd.nextInt(150);
            if (tri(a, b, c, n) != oracle(a, b, c, n)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Min Cost Climbing Stairs (LeetCode 746)
<!-- id: dp-roll-min-cost-stairs -->

**Approach.**
Let `low[p]` be the lowest total price to stand on position `p`, where the top is position `cost.length`. The climber starts on step 0 or step 1, so `low[0]` and `low[1]` are both 0. Position `p` is reached from `p - 1` by paying `cost[p - 1]` or from `p - 2` by paying `cost[p - 2]`. So `low[p]` is the smaller of `low[p - 1] + cost[p - 1]` and `low[p - 2] + cost[p - 2]`. The answer is `low[cost.length]`.

Since `low[p]` reads only the two previous positions, two variables replace the table. The invariant is that before position `p`, `two` equals `low[p - 2]` and `one` equals `low[p - 1]`. The assignment of `two` runs before the assignment of `one`. The tests compare against an exhaustive recursion.

**Complexity.**
- **Time** is O(n), because the loop visits each position from 2 to n once.
- **Space** is O(1), because the method keeps two saved prices and one candidate.

```java run
import java.util.*;

public final class RollStairs {
    /**
     * Returns the lowest total price to reach position cost.length.
     * Time: O(n). Space: O(1).
     * Invariant: before position p, two = low[p-2] and one = low[p-1].
     */
    static int minCost(int[] cost) {
        // The climber may start on step 0 or step 1 without paying.
        int two = 0;
        int one = 0;
        // Positions 2..n are computed; each costs constant time.
        for (int p = 2; p <= cost.length; p++) {
            // Arrive from the previous step or from two steps back, paying for the step left.
            int cur = Math.min(one + cost[p - 1], two + cost[p - 2]);
            // Older slot first, so the old one is read before it is replaced.
            two = one;
            // The new price becomes the most recent saved value.
            one = cur;
        }
        // one holds the lowest price for the top position.
        return one;
    }

    /** Oracle: exhaustive recursion over every legal move sequence. */
    static int oracle(int[] cost, int pos) {
        if (pos >= cost.length) return 0;
        return cost[pos] + Math.min(oracle(cost, pos + 1), oracle(cost, pos + 2));
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (minCost(new int[] {4, 1, 9, 2, 8, 3}) != 6) throw new AssertionError("ex1");
        if (minCost(new int[] {5, 0, 0, 5, 0}) != 0) throw new AssertionError("ex2");
        // Length 2 pays for the cheaper of the two start steps.
        if (minCost(new int[] {7, 7}) != 7 || minCost(new int[] {9, 2}) != 2) throw new AssertionError("short");
        // The input is not changed.
        int[] keep = {3, 8, 1, 4};
        int[] copy = keep.clone();
        minCost(keep);
        if (!Arrays.equals(keep, copy)) throw new AssertionError("mutation");
        // Random price arrays against the recursion; the start is either of the first two steps.
        Random rnd = new Random(2604);
        for (int t = 0; t < 3000; t++) {
            int[] c = new int[2 + rnd.nextInt(12)];
            for (int i = 0; i < c.length; i++) c[i] = rnd.nextInt(10);
            int expected = Math.min(oracle(c, 0), oracle(c, 1));
            if (minCost(c) != expected) throw new AssertionError("random " + t);
        }
    }
}
```
