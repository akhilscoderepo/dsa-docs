<!-- solutions-for: 05-subset-masks -->
### Solutions For Subset Masks

#### Solution: [Build] Enumerate All Masks (Author exercise)
<!-- id: bt05-subset-sum-count -->

**Approach.** One counter loop visits each subset once, and the bit test decides which items add to the sum.

The loop variable `mask` runs from 0 to `(1 << n) - 1`. Bit `i` of `mask` is 1 exactly when position `i` is in the subset, so the inner loop adds `w[i]` only for those positions. The invariant is that after the inner loop `sum` equals the total of the selected items for the current mask. The empty mask has no set bit, so its sum is 0, and it counts when `target` is 0. Equal values at different positions form different masks, so they count separately. For `n = 0` the outer loop runs once with `mask = 0`.

**Complexity.**

- **Time** is O(n * 2^n), because the outer loop has `2^n` masks and each mask scans `n` bits.
- **Space** is O(1), since only the counter, the running sum and the count are kept.

```java run
import java.util.Random;

public final class SubsetSumCount {
    /**
     * Counts the position subsets of w whose elements add up to target.
     * Time: O(n * 2^n), one scan of n bits per mask.
     * Space: O(1).
     * Invariant: after the inner loop, sum is the total of the items whose bits are set in mask.
     */
    static long count(int[] w, int target) {
        int n = w.length;
        long count = 0;
        // Each integer from 0 to 2^n - 1 is one subset, so no subset repeats.
        for (int mask = 0; mask < (1 << n); mask++) {
            long sum = 0;
            // Scan every item and test its bit.
            for (int i = 0; i < n; i++) {
                // Bit i is 1 exactly when item i is in the subset.
                if (((mask >> i) & 1) == 1) {
                    sum += w[i];
                }
            }
            // The mask counts when its subset reaches the target.
            if (sum == target) count++;
        }
        return count;
    }

    /** Oracle: recursion over include or skip for each position. */
    static long oracle(int[] w, int i, long left) {
        if (i == w.length) return left == 0 ? 1 : 0;
        return oracle(w, i + 1, left) + oracle(w, i + 1, left - w[i]);
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (count(new int[]{3, 1, 4, 2}, 5) != 2) throw new AssertionError("example 1");
        if (count(new int[]{0, 2, -2}, 0) != 4) throw new AssertionError("example 2");
        // Checks the empty array: only the empty subset exists.
        if (count(new int[]{}, 0) != 1 || count(new int[]{}, 3) != 0) throw new AssertionError("empty");
        // Checks random arrays against the recursive oracle with a fixed seed.
        Random rnd = new Random(3005);
        for (int round = 0; round < 300; round++) {
            int n = rnd.nextInt(11);
            int[] w = new int[n];
            for (int i = 0; i < n; i++) w[i] = rnd.nextInt(21) - 10;
            int target = rnd.nextInt(41) - 20;
            if (count(w, target) != oracle(w, 0, target)) throw new AssertionError("round " + round);
        }
    }
}
```

#### Solution: [Vary] Subsets (LeetCode 78)
<!-- id: bt05-subset-list -->

**Approach.** The update `(sub - 1) & m` moves from one submask to the next smaller one, and each submask becomes one list.

Subtracting 1 turns the lowest set bit of `sub` into 0 and turns all lower bits into 1. The AND with `m` removes every lower bit that `m` does not contain. The result is the largest submask below `sub`, because no submask lies strictly between them. Starting at `sub = m` therefore yields the submasks in descending order, which is the order the contract demands. For each submask the program scans positions from 0 upward and copies `nums[i]` when bit `i` is set, so each list is in increasing position order. The loop adds the list first and tests for 0 afterward, since a loop that stops before 0 would lose the empty subset. For `m = 0` the loop adds one empty list and stops.

**Complexity.**

- **Time** is O(n * 2^p) for `p` set bits, because each of the `2^p` submasks costs one O(1) update and an O(n) scan.
- **Space** is O(n * 2^p) for the returned lists, and O(1) beyond them.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class SubsetsInsideMask {
    /**
     * Returns one list per submask of m, in descending submask order.
     * Time: O(n * 2^p) for p set bits of m.
     * Space: O(n * 2^p) for the output lists.
     * Invariant: sub is a submask of m, and every larger submask already produced its list.
     */
    static List<List<Integer>> subsets(int[] nums, int m) {
        List<List<Integer>> out = new ArrayList<>();
        // The first submask is m itself; each update gives the next smaller one.
        for (int sub = m; ; sub = (sub - 1) & m) {
            List<Integer> one = new ArrayList<>();
            // Bit i of sub selects nums[i], and positions stay in increasing order.
            for (int i = 0; i < nums.length; i++) {
                if (((sub >> i) & 1) == 1) one.add(nums[i]);
            }
            out.add(one);
            // Stop after 0 is processed, because (0 - 1) & m would return m again.
            if (sub == 0) break;
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        List<List<Integer>> e1 = subsets(new int[]{7, -2, 5}, 5);
        if (!e1.equals(List.of(List.of(7, 5), List.of(5), List.of(7), List.of()))) throw new AssertionError("example 1 " + e1);
        if (!subsets(new int[]{4}, 0).equals(List.of(List.of()))) throw new AssertionError("example 2");
        // Checks that the update from 0 would wrap back to m, which is why the loop stops there.
        if (((0 - 1) & 45) != 45) throw new AssertionError("zero update");
        // Checks random inputs against a scan of every integer from m down to 0.
        Random rnd = new Random(3015);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(8);
            int[] nums = new int[n];
            for (int i = 0; i < n; i++) nums[i] = i * 7 - 20;
            int m = rnd.nextInt(1 << n);
            List<List<Integer>> brute = new ArrayList<>();
            for (int s = m; s >= 0; s--) {
                if ((s & m) != s) continue;
                List<Integer> one = new ArrayList<>();
                for (int i = 0; i < n; i++) if ((s & (1 << i)) != 0) one.add(nums[i]);
                brute.add(one);
            }
            if (!subsets(nums, m).equals(brute)) throw new AssertionError("m " + m);
            if (subsets(nums, m).size() != (1 << Integer.bitCount(m))) throw new AssertionError("size " + m);
        }
    }
}
```

#### Solution: [Boundary] Exponential Budget (Author exercise)
<!-- id: bt05-exponential-budget -->

**Approach.** The loop grows `n` from 0 and stops before the first product that exceeds the budget.

The product `n * 2^n` grows with `n`, so the answer is the last `n` whose product fits. For `n = 0` the product is 0 and always fits. The loop tests the next candidate `n + 1` by forming `(n + 1) * (1L << (n + 1))` and comparing it with `budget`. The budget is at most 10^12, and the loop stops by `n = 34`, so the largest product it forms is the one for 35, which is about 1.2 * 10^12. That value fits in a `long` with a wide margin. The shift uses `1L`, since `1 << 32` on an `int` equals 1.

**Complexity.**

- **Time** is O(1), because the loop stops by `n = 35` for any budget up to `10^12`.
- **Space** is O(1), as the loop keeps one counter.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class ExponentialBudget {
    /**
     * Returns the largest n with n * 2^n <= budget, for budget up to 10^12.
     * Time: O(1), at most 36 iterations.
     * Space: O(1).
     * Invariant: every n up to the loop counter satisfies n * 2^n <= budget.
     */
    static int largest(long budget) {
        int n = 0;
        // The next candidate is n + 1; its product is small enough for a long.
        while ((long) (n + 1) * (1L << (n + 1)) <= budget) {
            n++;
        }
        return n;
    }

    /** Oracle: exact product with BigInteger. */
    static int oracle(long budget) {
        int best = 0;
        for (int n = 0; n <= 60; n++) {
            BigInteger p = BigInteger.valueOf(n).shiftLeft(n);
            if (p.compareTo(BigInteger.valueOf(budget)) <= 0) best = n;
        }
        return best;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (largest(1000L) != 7) throw new AssertionError("example 1");
        if (largest(1_000_000_000_000L) != 34) throw new AssertionError("example 2");
        // Checks the smallest budgets.
        if (largest(1L) != 0 || largest(2L) != 1) throw new AssertionError("small budgets");
        // Checks the Java fact the approach relies on.
        if ((1 << 32) != 1) throw new AssertionError("int shift uses five bits");
        // Checks that the largest product the loop forms fits in a long.
        if (35L * (1L << 35) <= 0) throw new AssertionError("product fits");
        // Checks random budgets of every magnitude against the BigInteger oracle.
        Random rnd = new Random(3025);
        for (int round = 0; round < 2000; round++) {
            long b = 1 + (rnd.nextLong() >>> 1) % (1L << (1 + rnd.nextInt(40)));
            if (b > 1_000_000_000_000L) b = 1_000_000_000_000L;
            if (largest(b) != oracle(b)) throw new AssertionError("budget " + b);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path Visiting All Nodes (LeetCode 847)
<!-- id: bt05-walk-all-nodes -->

**Approach.** One pass over the route keeps a visited mask and tests each step against an adjacency mask.

The visited mask starts with the bit of the first route node. For each later node `v`, the previous node `u` must satisfy `(adj[u] >> v) & 1`, which reads the edge bit. A failed test makes the route invalid. Otherwise the loop sets bit `v` with OR. After the last node, the route is valid exactly when the visited mask equals the full mask `(1 << n) - 1`. The invariant is that bit `i` of the visited mask is 1 exactly when node `i` appears in the prefix read so far. A route of one node has no steps, and it is valid only for a graph with one node.

**Complexity.**

- **Time** is O(r) for a route of `r` nodes, because each step costs two bit operations.
- **Space** is O(1), since the program keeps one visited mask.

```java run
import java.util.Random;

public final class WalkAllNodes {
    /**
     * Returns true when the route follows edges and visits every node.
     * Time: O(r) for a route of r nodes.
     * Space: O(1).
     * Invariant: bit i of visited is 1 exactly when node i appears in the prefix read so far.
     */
    static boolean validRoute(int[] adj, int[] route) {
        int n = adj.length;
        int full = (1 << n) - 1;
        // The first node starts the visited mask.
        int visited = 1 << route[0];
        for (int k = 1; k < route.length; k++) {
            // The step needs an edge bit between the previous node and this one.
            if (((adj[route[k - 1]] >> route[k]) & 1) == 0) return false;
            // OR records the node and never removes another.
            visited |= 1 << route[k];
        }
        // Equality with the full mask means no node is missing.
        return visited == full;
    }

    /** Oracle: matrix and boolean array. */
    static boolean oracle(int[] adj, int[] route) {
        int n = adj.length;
        boolean[] seen = new boolean[n];
        seen[route[0]] = true;
        for (int k = 1; k < route.length; k++) {
            boolean edge = false;
            for (int j = 0; j < n; j++) {
                if (j == route[k] && (adj[route[k - 1]] & (1 << j)) != 0) edge = true;
            }
            if (!edge) return false;
            seen[route[k]] = true;
        }
        for (boolean b : seen) if (!b) return false;
        return true;
    }

    public static void main(String[] args) {
        // Checks Example 1 on a star graph, including the route that misses node 3.
        int[] star = {14, 1, 1, 1};
        if (!validRoute(star, new int[]{1, 0, 2, 0, 3})) throw new AssertionError("example 1a");
        if (validRoute(star, new int[]{1, 0, 2})) throw new AssertionError("example 1b");
        // Checks Example 2, where node 2 is isolated.
        if (validRoute(new int[]{2, 1, 0}, new int[]{0, 1, 0})) throw new AssertionError("example 2");
        // Checks a single node graph.
        if (!validRoute(new int[]{0}, new int[]{0})) throw new AssertionError("single node");
        // Checks random graphs and routes against the oracle with a fixed seed.
        Random rnd = new Random(3085);
        for (int round = 0; round < 3000; round++) {
            int n = 1 + rnd.nextInt(6);
            int[] adj = new int[n];
            for (int a = 0; a < n; a++) {
                for (int b = a + 1; b < n; b++) {
                    if (rnd.nextInt(3) > 0) {
                        adj[a] |= 1 << b;
                        adj[b] |= 1 << a;
                    }
                }
            }
            int[] route = new int[1 + rnd.nextInt(10)];
            route[0] = rnd.nextInt(n);
            for (int k = 1; k < route.length; k++) {
                // Mostly pick a neighbor so that some routes stay valid.
                int next = rnd.nextInt(n);
                for (int tries = 0; tries < 4 && ((adj[route[k - 1]] >> next) & 1) == 0; tries++) next = rnd.nextInt(n);
                route[k] = next;
            }
            if (validRoute(adj, route) != oracle(adj, route)) throw new AssertionError("round " + round);
        }
    }
}
```
