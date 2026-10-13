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

**Approach.** The loop tests `n * 2^n <= budget` as `2^n <= budget / n`, which never overflows.

The product `n * 2^n` grows with `n`, so the answer is the last `n` before the first failure. For `n = 0` the product is 0 and always fits. For `n >= 1` the condition `n * 2^n <= budget` is equivalent to `2^n <= floor(budget / n)`, because `2^n` is an integer. The right side is at most `10^18`, and the left side `1L << n` stays below 2^63 for `n <= 62`. The product itself would overflow `long` around `n = 58`, which is why the program never forms it. The shift uses `1L`, since `1 << 32` on an `int` equals 1.

**Complexity.**

- **Time** is O(1), because the loop stops by `n = 55` for any budget up to `10^18`.
- **Space** is O(1), as the loop keeps one counter.

```java run
import java.math.BigInteger;
import java.util.Random;

public final class ExponentialBudget {
    /**
     * Returns the largest n with n * 2^n <= budget.
     * Time: O(1), at most 62 iterations.
     * Space: O(1).
     * Invariant: every n below the loop counter satisfies n * 2^n <= budget.
     */
    static int largest(long budget) {
        int n = 0;
        // The next candidate is n + 1; test it without forming the product.
        while (n + 1 <= 62 && (1L << (n + 1)) <= budget / (n + 1)) {
            n++;
        }
        return n;
    }

    /** Oracle: exact product with BigInteger. */
    static int oracle(long budget) {
        int best = 0;
        for (int n = 0; n <= 70; n++) {
            BigInteger p = BigInteger.valueOf(n).shiftLeft(n);
            if (p.compareTo(BigInteger.valueOf(budget)) <= 0) best = n;
        }
        return best;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (largest(1000L) != 7) throw new AssertionError("example 1");
        if (largest(1_000_000_000_000_000_000L) != 54) throw new AssertionError("example 2");
        // Checks the smallest budgets.
        if (largest(1L) != 0 || largest(2L) != 1) throw new AssertionError("small budgets");
        // Checks the two Java facts the approach relies on.
        if ((1 << 32) != 1) throw new AssertionError("int shift uses five bits");
        if (58L * (1L << 58) >= 0) throw new AssertionError("the long product overflows for n = 58");
        // Checks random budgets of every magnitude against the BigInteger oracle.
        Random rnd = new Random(3025);
        for (int round = 0; round < 2000; round++) {
            long b = 1 + (rnd.nextLong() >>> 1) % (1L << (1 + rnd.nextInt(59)));
            if (b > 1_000_000_000_000_000_000L) b = 1_000_000_000_000_000_000L;
            if (largest(b) != oracle(b)) throw new AssertionError("budget " + b);
        }
    }
}
```

#### Solution: [Recognize] Shortest Path Visiting All Nodes (LeetCode 847)
<!-- id: bt05-walk-all-nodes -->

**Approach.** Breadth-first search runs over states made of a node and a visited mask.

One state is the pair `(node, mask)`, where bit `i` of `mask` is 1 when node `i` has been visited. The start state is `(s, 1 << s)` at distance 0. A move along an edge to neighbor `v` produces `(v, mask | (1 << v))` at distance plus 1. All moves cost one edge, so breadth-first search reaches each state first at its smallest distance. The first state with `mask` equal to the full mask `(1 << n) - 1` gives the answer. A `seen` table keyed by node and mask keeps each of the `n * 2^n` states from entering the queue twice. A single node starts with the full mask, so the answer is 0.

**Complexity.**

- **Time** is O(2^n * (n + E)) for `E` edges, because each of the `n * 2^n` states expands over its node's neighbors.
- **Space** is O(n * 2^n) for the `seen` table and the queue.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class WalkAllNodes {
    /**
     * Returns the fewest edges in a walk from s that visits every node.
     * Time: O(2^n * (n + E)).
     * Space: O(n * 2^n).
     * Invariant: a state (node, mask) is queued at most once, at its smallest distance.
     */
    static int shortest(int[][] graph, int s) {
        int n = graph.length;
        int full = (1 << n) - 1;
        // seen[node][mask] marks states that were already queued.
        boolean[][] seen = new boolean[n][1 << n];
        ArrayDeque<int[]> queue = new ArrayDeque<>();
        // The start state has only the start node visited.
        queue.add(new int[]{s, 1 << s, 0});
        seen[s][1 << s] = true;
        while (!queue.isEmpty()) {
            int[] cur = queue.poll();
            // The first full mask in breadth-first order is the shortest walk.
            if (cur[1] == full) return cur[2];
            for (int next : graph[cur[0]]) {
                // Moving to next marks bit next as visited.
                int mask = cur[1] | (1 << next);
                if (!seen[next][mask]) {
                    seen[next][mask] = true;
                    queue.add(new int[]{next, mask, cur[2] + 1});
                }
            }
        }
        // A connected graph always reaches the full mask before the queue empties.
        throw new AssertionError("graph is not connected");
    }

    /** Oracle: grow the set of reachable (node, visited set) pairs one edge at a time. */
    static int oracle(int[][] graph, int s) {
        int n = graph.length;
        Set<List<Integer>> cur = new HashSet<>();
        cur.add(List.of(s, 1 << s));
        for (int len = 0; len < 60; len++) {
            for (List<Integer> st : cur) if (st.get(1) == (1 << n) - 1) return len;
            Set<List<Integer>> nxt = new HashSet<>();
            for (List<Integer> st : cur) {
                for (int v : graph[st.get(0)]) nxt.add(List.of(v, st.get(1) | (1 << v)));
            }
            cur = nxt;
        }
        throw new AssertionError("no walk");
    }

    public static void main(String[] args) {
        // Checks Example 1 on a star graph and Example 2 on a single node.
        if (shortest(new int[][]{{1, 2, 3}, {0}, {0}, {0}}, 1) != 4) throw new AssertionError("example 1");
        if (shortest(new int[][]{{}}, 0) != 0) throw new AssertionError("example 2");
        // Checks random connected graphs against the oracle with a fixed seed.
        Random rnd = new Random(3085);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(7);
            List<List<Integer>> adj = new ArrayList<>();
            for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
            // A random tree keeps the graph connected; extra edges follow.
            for (int v = 1; v < n; v++) {
                int u = rnd.nextInt(v);
                adj.get(u).add(v);
                adj.get(v).add(u);
            }
            for (int k = rnd.nextInt(n + 1); k > 0; k--) {
                int a = rnd.nextInt(n), b = rnd.nextInt(n);
                if (a != b && !adj.get(a).contains(b)) {
                    adj.get(a).add(b);
                    adj.get(b).add(a);
                }
            }
            int[][] graph = new int[n][];
            for (int i = 0; i < n; i++) graph[i] = adj.get(i).stream().mapToInt(Integer::intValue).toArray();
            int s = rnd.nextInt(n);
            if (shortest(graph, s) != oracle(graph, s)) throw new AssertionError("round " + round);
        }
    }
}
```
