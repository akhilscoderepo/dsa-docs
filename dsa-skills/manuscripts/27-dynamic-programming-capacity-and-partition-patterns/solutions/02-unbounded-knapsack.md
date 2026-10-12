<!-- solutions-for: 27-dynamic-programming-capacity-and-partition-patterns -->
### Solutions For Unbounded Knapsack

#### Solution: [Build] One Reusable Item (Author exercise)
<!-- id: cap-ukn-one-item -->

**Approach.**
The entry `dp[c]` holds the best value with total weight at most `c`, and every entry starts at 0 for the empty selection. With one item, the loop runs capacities from `weight` to `capacity`. Each entry compares the stored value with the value one copy below, which is `dp[c - weight] + value`. The current-row read is what chains the copies, because `dp[c - weight]` already holds the copies chosen below it.

The invariant is that `dp[c]` equals `(c / weight) * value` after the loop reaches `c`. The method returns `dp[capacity]`, which must equal the closed form `(capacity / weight) * value`, and the test checks that.

**Complexity.**
- **Time** is O(capacity), because each capacity does one read and one comparison.
- **Space** is O(capacity) for the table, and the inputs are not changed.

```java run
import java.util.*;

public final class CapUknOneItem {
    /**
     * Returns the best value of copies of one item within capacity.
     * Time: O(capacity). Space: O(capacity).
     * Invariant: after the loop passes c, dp[c] is (c / weight) * value.
     */
    static int oneItem(int weight, int value, int capacity) {
        // Java zero-fills the table, which matches the empty selection at every capacity.
        int[] dp = new int[capacity + 1];
        // Increasing capacity lets the entry read copies already counted below it.
        for (int c = weight; c <= capacity; c++) {
            // Taking one more copy reads the current row at the smaller capacity.
            int take = dp[c - weight] + value;
            // The entry keeps the larger of the stored value and the take value.
            if (take > dp[c]) dp[c] = take;
        }
        // The full capacity covers every smaller selection.
        return dp[capacity];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (oneItem(4, 7, 13) != 21) throw new AssertionError("ex1");
        if (oneItem(5, 9, 4) != 0) throw new AssertionError("ex2");
        // Capacity 0 returns 0.
        if (oneItem(3, 8, 0) != 0) throw new AssertionError("zero");
        // Every small input is checked against the closed form.
        for (int w = 1; w <= 20; w++) {
            for (int v = 0; v <= 10; v++) {
                for (int cap = 0; cap <= 100; cap++) {
                    if (oneItem(w, v, cap) != (cap / w) * v) throw new AssertionError(w + " " + v + " " + cap);
                }
            }
        }
    }
}
```

#### Solution: [Vary] Maximum Value With Reuse (Author exercise)
<!-- id: cap-ukn-max-value -->

**Approach.**
The outer loop processes one item kind at a time, and `dp[c]` holds the best value with weight at most `c` using the kinds processed so far. For item `i` and capacity `c`, the skip value is the entry already stored, which describes the earlier kinds. The take value is `dp[c - weight[i]] + value[i]`, where the entry at the smaller capacity was already rewritten for item `i`, so it may contain earlier copies of the same kind.

The invariant is that after item `i` finishes, `dp[c]` is the best value for every `c` when kinds 0 through `i` are allowed. The capacity loop must run upward for the current-row read to hold copies. The ratio greedy of the lesson fails on weights `[4,3]`, values `[5,3]` and capacity 6, and the test confirms it.

**Complexity.**
- **Time** is O(capacity * k) for k kinds, because each kind updates each capacity once.
- **Space** is O(capacity) for the table, and both arrays stay unchanged.

```java run
import java.util.*;

public final class CapUknMaxValue {
    /**
     * Returns the best total value of repeatable items within capacity.
     * Time: O(capacity * k). Space: O(capacity).
     * Invariant: after kind i finishes, dp[c] is the best value using kinds 0..i.
     */
    static int unboundedPack(int[] weight, int[] value, int capacity) {
        // Every entry starts at 0 for the empty selection.
        int[] dp = new int[capacity + 1];
        // One pass per item kind costs k passes over the table.
        for (int i = 0; i < weight.length; i++) {
            // Upward order makes dp[c - weight[i]] hold the current row.
            for (int c = weight[i]; c <= capacity; c++) {
                // The take value adds one copy to the best value of the smaller capacity.
                int take = dp[c - weight[i]] + value[i];
                // The skip value is the entry already stored, so the larger one stays.
                if (take > dp[c]) dp[c] = take;
            }
        }
        // The full capacity covers every smaller selection.
        return dp[capacity];
    }

    /** The ratio greedy of the lesson, kept to show that it fails. */
    static int greedy(int[] weight, int[] value, int capacity) {
        Integer[] order = new Integer[weight.length];
        for (int i = 0; i < order.length; i++) order[i] = i;
        Arrays.sort(order, (x, y) -> Long.compare((long) value[y] * weight[x], (long) value[x] * weight[y]));
        int left = capacity, total = 0;
        for (int i : order) {
            total += (left / weight[i]) * value[i];
            left %= weight[i];
        }
        return total;
    }

    /** Oracle: tries every vector of copy counts. */
    static int oracle(int[] weight, int[] value, int i, int left) {
        if (i == weight.length) return 0;
        int best = 0;
        for (int copies = 0; copies * weight[i] <= left; copies++) {
            best = Math.max(best, copies * value[i] + oracle(weight, value, i + 1, left - copies * weight[i]));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (unboundedPack(new int[] {4, 3}, new int[] {5, 3}, 6) != 6) throw new AssertionError("ex1");
        if (unboundedPack(new int[] {5, 7}, new int[] {6, 9}, 17) != 21) throw new AssertionError("ex2");
        // The greedy method returns 5 on the lesson input, while the table returns 6.
        if (greedy(new int[] {4, 3}, new int[] {5, 3}, 6) != 5) throw new AssertionError("greedy value");
        // An item heavier than the capacity changes nothing.
        if (unboundedPack(new int[] {50, 2}, new int[] {99, 1}, 7) != 3) throw new AssertionError("heavy");
        // Both arrays stay unchanged.
        int[] w = {4, 3};
        int[] v = {5, 3};
        unboundedPack(w, v, 20);
        if (!Arrays.equals(w, new int[] {4, 3}) || !Arrays.equals(v, new int[] {5, 3})) throw new AssertionError("mutated");
        // Random inputs against the exhaustive oracle.
        Random rnd = new Random(2704);
        for (int t = 0; t < 2000; t++) {
            int k = 1 + rnd.nextInt(4);
            int[] ww = new int[k];
            int[] vv = new int[k];
            for (int i = 0; i < k; i++) {
                ww[i] = 1 + rnd.nextInt(9);
                vv[i] = rnd.nextInt(15);
            }
            int cap = rnd.nextInt(30);
            if (unboundedPack(ww, vv, cap) != oracle(ww, vv, 0, cap)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Zero Capacity (Author exercise)
<!-- id: cap-ukn-zero-capacity -->

**Approach.**
A zero-weight item with positive value breaks the table. The inner loop would start at capacity 0 and read `dp[c - 0]`, which is the entry being written, so the update would add the value once and stop, while the true best total grows without limit. The method therefore scans the items first. If any item has weight 0 and value above 0, it returns -1 before any loop runs.

After that scan, a zero-weight item has value 0 and never changes an entry, so the loops skip it. Capacity 0 returns 0 because every other item has positive weight. The invariant of the main loop is unchanged: after item `i` finishes, `dp[c]` is the best value for every `c` using kinds 0 through `i`.

**Complexity.**
- **Time** is O(k + capacity * k), which is O(capacity * k) for the table and O(k) for the scan.
- **Space** is O(capacity) for the table, and both arrays stay unchanged.

```java run
import java.util.*;

public final class CapUknZeroCapacity {
    /**
     * Returns the best value of repeatable items within capacity, or -1 when the value is unbounded.
     * Time: O(capacity * k). Space: O(capacity).
     * Invariant: after kind i finishes, dp[c] is the best value using kinds 0..i.
     */
    static int packOrUnbounded(int[] weight, int[] value, int capacity) {
        // A free item with positive value can repeat forever, so no finite best exists.
        for (int i = 0; i < weight.length; i++) {
            if (weight[i] == 0 && value[i] > 0) return -1;
        }
        int[] dp = new int[capacity + 1];
        for (int i = 0; i < weight.length; i++) {
            // A zero-weight item now has value 0, so it can never change an entry.
            if (weight[i] == 0) continue;
            for (int c = weight[i]; c <= capacity; c++) {
                // The take value reads the current row at the smaller capacity.
                int take = dp[c - weight[i]] + value[i];
                if (take > dp[c]) dp[c] = take;
            }
        }
        // Capacity 0 returns dp[0], which is 0.
        return dp[capacity];
    }

    /** Oracle: tries every vector of copy counts over the positive-weight items. */
    static int oracle(int[] weight, int[] value, int i, int left) {
        if (i == weight.length) return 0;
        if (weight[i] == 0) return oracle(weight, value, i + 1, left);
        int best = 0;
        for (int copies = 0; copies * weight[i] <= left; copies++) {
            best = Math.max(best, copies * value[i] + oracle(weight, value, i + 1, left - copies * weight[i]));
        }
        return best;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (packOrUnbounded(new int[] {0, 5}, new int[] {0, 6}, 0) != 0) throw new AssertionError("ex1");
        if (packOrUnbounded(new int[] {0, 5}, new int[] {2, 6}, 7) != -1) throw new AssertionError("ex2");
        // An empty item list returns 0.
        if (packOrUnbounded(new int[] {}, new int[] {}, 9) != 0) throw new AssertionError("empty");
        // A zero-weight item with value 0 is ignored.
        if (packOrUnbounded(new int[] {0, 3}, new int[] {0, 4}, 7) != 8) throw new AssertionError("free zero");
        // Random inputs against the exhaustive oracle.
        Random rnd = new Random(2705);
        for (int t = 0; t < 2000; t++) {
            int k = rnd.nextInt(4);
            int[] ww = new int[k];
            int[] vv = new int[k];
            boolean unbounded = false;
            for (int i = 0; i < k; i++) {
                ww[i] = rnd.nextInt(7);
                vv[i] = rnd.nextInt(12);
                if (ww[i] == 0 && vv[i] > 0) unbounded = true;
            }
            int cap = rnd.nextInt(25);
            int want = unbounded ? -1 : oracle(ww, vv, 0, cap);
            if (packOrUnbounded(ww, vv, cap) != want) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Perfect Squares (LeetCode 279)
<!-- id: cap-ukn-perfect-squares -->

**Approach.**
Each perfect square up to `n` is an item whose weight is the square and whose use costs 1. The sum must be exactly `n`, and the goal is the fewest items, which is the coin change table with the squares as denominations. The entry `dp[a]` is the fewest squares that add up to `a`, with `dp[0] = 0` and the marker `n + 1` for amounts not yet reached. Every `a` from 1 to `n` is reachable, because 1 is a square.

The invariant is that `dp[a]` is exact for every amount the loop has passed. The loop over amounts runs upward, so a square may repeat. The inner loop tries each square `s * s <= a` as the last term.

**Complexity.**
- **Time** is O(n * sqrt(n)), because each amount tries at most sqrt(n) squares.
- **Space** is O(n) for the table.

```java run
import java.util.*;

public final class CapUknPerfectSquares {
    /**
     * Returns the fewest perfect squares that sum to n.
     * Time: O(n * sqrt(n)). Space: O(n).
     * Invariant: dp[a] is the fewest squares for a, for every amount the loop has passed.
     */
    static int fewestSquares(int n) {
        // The marker n + 1 is larger than any real count, because 1 is a square.
        int[] dp = new int[n + 1];
        Arrays.fill(dp, n + 1);
        // Zero squares add up to 0.
        dp[0] = 0;
        // Upward amounts let a square appear more than once.
        for (int a = 1; a <= n; a++) {
            // Each square that fits is a candidate for the last term.
            for (int s = 1; s * s <= a; s++) {
                // The candidate wins when the smaller amount plus one square is cheaper.
                if (dp[a - s * s] + 1 < dp[a]) dp[a] = dp[a - s * s] + 1;
            }
        }
        // Every amount is reachable, so no marker conversion is needed.
        return dp[n];
    }

    /** Oracle: breadth-first search by number of squares. */
    static int oracle(int n) {
        int[] dist = new int[n + 1];
        Arrays.fill(dist, -1);
        Deque<Integer> queue = new ArrayDeque<>();
        dist[0] = 0;
        queue.add(0);
        while (!queue.isEmpty()) {
            int cur = queue.poll();
            for (int s = 1; cur + s * s <= n; s++) {
                if (dist[cur + s * s] == -1) {
                    dist[cur + s * s] = dist[cur] + 1;
                    queue.add(cur + s * s);
                }
            }
        }
        return dist[n];
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (fewestSquares(12) != 3) throw new AssertionError("ex1");
        if (fewestSquares(28) != 4) throw new AssertionError("ex2");
        // A perfect square needs one term, and 1 needs one term.
        if (fewestSquares(1) != 1 || fewestSquares(49) != 1) throw new AssertionError("square");
        // Every n up to 2000 against the breadth-first oracle.
        for (int n = 1; n <= 2000; n++) {
            if (fewestSquares(n) != oracle(n)) throw new AssertionError("n=" + n);
        }
    }
}
```
