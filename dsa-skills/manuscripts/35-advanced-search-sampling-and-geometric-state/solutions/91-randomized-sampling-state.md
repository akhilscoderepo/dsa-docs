<!-- solutions-for: 91-randomized-sampling-state -->
### Solutions For Randomized Sampling State

#### Solution: [Build] Random Pick Index (LeetCode 398)
<!-- id: rss35-random-pick-window -->

**Approach.**
The eligible positions are those inside `[from, to]` whose value equals `target`. The method scans only that window and keeps a counter `m` of eligible positions seen so far. The first eligible position is stored without a draw. For the `m`-th one, the method draws from bound `m` and stores the position when the result is 0, so its chance is `1 / m`. By the induction from the Reservoir Sampling lesson, every eligible position has chance `1 / m` after `m` eligible positions. Positions outside the window and positions with other values never change `m`, so the denominator counts eligible positions only. When `m` stays 0, the method returns -1 and makes no draw. The invariant is that after `m` eligible positions, each of them is held with chance `1 / m`.

The program enumerates all draw sequences for several windows and checks that every eligible position is returned equally often. It checks the examples, an empty window result and that no draw happens when nothing matches.

**Complexity.**
- **Time** is O(window length).
- **Space** is O(1).

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.function.LongUnaryOperator;

public final class RandomPickWindowBuild {
    /**
     * Returns an eligible position chosen uniformly, or -1.
     * Time: O(to - from + 1). Space: O(1).
     * Invariant: after m eligible positions each is held with chance 1/m.
     */
    static int pickInWindow(int[] nums, int target, int from, int to, LongUnaryOperator pick) {
        int held = -1;
        long m = 0; // count of eligible positions
        for (int i = from; i <= to; i++) {
            if (nums[i] != target) continue; // not eligible
            m++;
            if (m == 1 || pick.applyAsLong(m) == 0) held = i; // the first enters, later ones with chance 1/m
        }
        return held;
    }

    static int run(int[] nums, int target, int from, int to, long[] draws) {
        int[] at = {0};
        return pickInWindow(nums, target, from, to, b -> draws[at[0]++]);
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (run(new int[]{2, 7, 2, 2, 9, 2}, 2, 1, 5, new long[]{0, 2}) != 3) throw new AssertionError("ex1");
        if (pickInWindow(new int[]{4, 5}, 9, 0, 1, b -> { throw new AssertionError("no draw expected"); }) != -1) throw new AssertionError("ex2");
        // exact fairness over all draw sequences for several windows
        int[][] arrays = {{2, 7, 2, 2, 9, 2}, {1, 1, 1, 1, 1}, {5, 2, 5, 2, 5, 2, 5}};
        int[][] windows = {{0, 5}, {1, 5}, {2, 3}, {0, 4}, {1, 6}};
        for (int[] nums : arrays) for (int[] win : windows) {
            if (win[1] >= nums.length) continue;
            int target = nums[0];
            List<Integer> eligible = new ArrayList<>();
            for (int i = win[0]; i <= win[1]; i++) if (nums[i] == target) eligible.add(i);
            if (eligible.isEmpty()) continue;
            int draws = eligible.size() - 1;
            long[] seq = new long[draws];
            long[] counts = new long[nums.length];
            while (true) {
                counts[run(nums, target, win[0], win[1], seq.clone())]++;
                int pos = 0; // odometer: draw p has bound p + 2
                while (pos < draws && ++seq[pos] == pos + 2) seq[pos++] = 0;
                if (pos == draws) break;
            }
            long expected = counts[eligible.get(0)];
            for (int i : eligible) if (counts[i] != expected) throw new AssertionError("unfair");
            for (int i = 0; i < nums.length; i++) if (!eligible.contains(i) && counts[i] != 0) throw new AssertionError("ineligible chosen");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Linked List Random Node (LeetCode 382)
<!-- id: rss35-weighted-list-node -->

**Approach.**
A node with count `c` stands for `c` copies, so the denominator is the sum of counts read so far. The first node is held without a draw. For a later node, the method adds its count to `total`, draws from bound `total`, and replaces the held value when the draw is below the node's count. That replacement has chance `c / total`. Suppose node `j` is held with chance `c_j / T_before`. It survives the new node with chance `T_before / T`, so it is held with chance `c_j / T`. The new node is held with chance `c / T`. By induction, after the whole list, a node is held with chance `c / T_final`, which is the share of the expanded sequence that it occupies. The invariant is that after each node the held value has chance proportional to the node's count among the nodes read.

The program enumerates every draw sequence for lists with 1 to 4 nodes and counts how often each node is returned. It compares `count[j] * T` with `c_j * (number of sequences)`, which is the exact proportion. It also checks the examples and that the list is unchanged.

**Complexity.**
- **Time** is O(n) for one walk.
- **Space** is O(1).

```java run
import java.util.function.LongUnaryOperator;

public final class WeightedListNodeVary {
    static final class RunNode {
        final int val; final long count; RunNode next;
        RunNode(int val, long count, RunNode next) { this.val = val; this.count = count; this.next = next; }
    }

    /**
     * Returns a value so that each element of the expanded sequence is equally likely.
     * Time: O(n). Space: O(1).
     * Invariant: after each node the held value has chance proportional to its node's count.
     */
    static int weightedNode(RunNode head, LongUnaryOperator pick) {
        int held = head.val; // the first node needs no draw
        long total = head.count;
        for (RunNode cur = head.next; cur != null; cur = cur.next) {
            total += cur.count; // the denominator grows by the weight of this node
            if (pick.applyAsLong(total) < cur.count) held = cur.val; // chance count / total
        }
        return held;
    }

    static RunNode build(int[] vals, long[] counts) {
        RunNode head = null;
        for (int i = vals.length - 1; i >= 0; i--) head = new RunNode(vals[i], counts[i], head);
        return head;
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d = {0, 4};
        int[] at = {0};
        if (weightedNode(build(new int[]{5, 8, 3}, new long[]{2, 1, 3}), b -> d[at[0]++]) != 8) throw new AssertionError("ex1");
        if (weightedNode(build(new int[]{7}, new long[]{4}), b -> { throw new AssertionError("no draw"); }) != 7) throw new AssertionError("ex2");
        // exact proportions over every draw sequence
        long[][] countCases = {{1}, {2, 3}, {1, 1, 1}, {2, 1, 3}, {3, 1, 2, 2}};
        for (long[] counts : countCases) {
            int n = counts.length;
            int[] vals = new int[n];
            for (int i = 0; i < n; i++) vals[i] = 10 + i;
            RunNode head = build(vals, counts);
            long[] bounds = new long[Math.max(0, n - 1)];
            long run = counts[0], seqCount = 1;
            for (int i = 1; i < n; i++) { run += counts[i]; bounds[i - 1] = run; seqCount *= run; } // bound for node i is the prefix sum
            long totalWeight = run;
            long[] seq = new long[bounds.length];
            long[] hits = new long[n];
            while (true) {
                final long[] copy = seq.clone();
                final int[] cursor = {0};
                hits[weightedNode(head, b -> copy[cursor[0]++]) - 10]++;
                int pos = 0;
                while (pos < seq.length && ++seq[pos] == bounds[pos]) seq[pos++] = 0;
                if (pos == seq.length) break;
            }
            for (int i = 0; i < n; i++) if (hits[i] * totalWeight != counts[i] * seqCount) throw new AssertionError("proportion " + i);
            RunNode cur = head;
            for (int i = 0; i < n; i++, cur = cur.next) if (cur.val != 10 + i || cur.count != counts[i]) throw new AssertionError("list changed");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Random Pick With Weight (LeetCode 528)
<!-- id: rss35-wide-ticket-picker -->

**Approach.**
The constructor builds prefix totals with `Math.addExact`, which throws `ArithmeticException` instead of wrapping when a sum exceeds `Long.MAX_VALUE`. Invalid inputs fail early with `IllegalArgumentException`, because an input with no items, a negative weight or a total of zero has no valid ticket. A zero-based ticket `t` lies from 0 to `total - 1`, and index `i` owns the tickets from `P[i-1]` to `P[i] - 1`, where `P[-1]` is 0. The owner of `t` is therefore the first index whose prefix total is strictly greater than `t`. The binary search keeps `hi` at an index whose prefix is above the ticket and `lo` at the earliest candidate. A zero-weight index repeats a prefix total, so the search stops at the first index with that value and skips the repeat. The invariant here is the same window rule: whichever branch runs, the owner still lies in `[lo, hi]`.

The program checks every ticket for small weight arrays against a table of owners. It runs the large examples, and it checks the overflow cases and that two weights of 4 * 10^18 add without overflow while `Long.MAX_VALUE + 1` does overflow.

**Complexity.**
- **Time** is O(n) for the constructor and O(log n) per pick.
- **Space** is O(n).

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.function.LongUnaryOperator;

public final class WideTicketPickerBoundary {
    static final class WidePicker {
        private final long[] prefix;
        private final LongUnaryOperator pick;

        WidePicker(long[] w, LongUnaryOperator pick) {
            if (w.length == 0) throw new IllegalArgumentException("empty");
            prefix = new long[w.length];
            long run = 0;
            for (int i = 0; i < w.length; i++) {
                if (w[i] < 0) throw new IllegalArgumentException("negative");
                run = Math.addExact(run, w[i]); // throws ArithmeticException on overflow
                prefix[i] = run;
            }
            if (run == 0) throw new IllegalArgumentException("zero total");
            this.pick = pick;
        }

        /**
         * Returns the index that owns a zero-based ticket.
         * Time: O(log n). Space: O(1).
         * Invariant: the owner of the ticket lies in [lo, hi].
         */
        int pickIndex() {
            long ticket = pick.applyAsLong(prefix[prefix.length - 1]); // 0 to total - 1
            int lo = 0, hi = prefix.length - 1;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (prefix[mid] > ticket) hi = mid; // strictly above: mid may own the ticket
                else lo = mid + 1; // the range of mid ended at or below the ticket
            }
            return lo;
        }
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d = {2, 3};
        int[] at = {0};
        WidePicker p = new WidePicker(new long[]{3, 0, 2}, b -> d[at[0]++]);
        if (p.pickIndex() != 0 || p.pickIndex() != 2) throw new AssertionError("ex1");
        boolean overflow = false;
        try { new WidePicker(new long[]{Long.MAX_VALUE, 1}, b -> 0); } catch (ArithmeticException e) { overflow = true; }
        if (!overflow) throw new AssertionError("overflow not detected");
        if (new WidePicker(new long[]{4_000_000_000_000_000_000L, 4_000_000_000_000_000_000L}, b -> 7_999_999_999_999_999_999L).pickIndex() != 1) throw new AssertionError("large");
        // the sum of two such weights still fits, and Long.MAX_VALUE + 1 wraps
        if (4_000_000_000_000_000_000L + 4_000_000_000_000_000_000L < 0 || Long.MAX_VALUE + 1 >= 0) throw new AssertionError("range claim");
        // invalid input
        int rejected = 0;
        for (long[] bad : new long[][]{{}, {0, 0}, {2, -1}}) {
            try { new WidePicker(bad, b -> 0); } catch (IllegalArgumentException e) { rejected++; }
        }
        if (rejected != 3) throw new AssertionError("policy");
        // every ticket of random small arrays has the owner given by an explicit table
        Random rnd = new Random(81);
        for (int t = 0; t < 300; t++) {
            long[] w = new long[1 + rnd.nextInt(7)];
            List<Integer> table = new ArrayList<>();
            for (int i = 0; i < w.length; i++) { w[i] = rnd.nextInt(3) == 0 ? 0 : 1 + rnd.nextInt(4); for (int c = 0; c < w[i]; c++) table.add(i); }
            if (table.isEmpty()) continue;
            for (int ticket = 0; ticket < table.size(); ticket++) {
                final long tk = ticket;
                if (new WidePicker(w, b -> tk).pickIndex() != table.get(ticket)) throw new AssertionError("owner mismatch");
            }
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Generate Random Point In A Circle (LeetCode 478)
<!-- id: rss35-random-point-ring -->

**Approach.**
The ring is the circle of radius `outer` minus the disc of radius `inner`. The method works in unit coordinates, where the outer circle has radius 1 and the hole has radius `rho = inner / outer`. Each trial draws a uniform point in the square from -1 to 1, and the test `rho^2 <= ux^2 + uy^2 <= 1` accepts points of the ring only. The accepted point is uniform over the ring, since every patch of the ring is accepted with the same chance `1 / 4` per unit of area and the rejected region carries no weight. The method scales the accepted point by `outer`. The acceptance probability is the area of the ring divided by the area of the square, which is `pi * (1 - rho^2) / 4`. For `rho = 0.5` this is about 0.589, so the expected number of trials is about 1.70. The invariant is that every draw is uniform over the square and only the ring passes the test.

The program checks the examples. It then runs 200000 seeded samples for `inner = 1`, `outer = 2` and checks three facts: every point lies in the ring, the mean number of trials is near `4 / (pi * 0.75)`. The fraction of points within distance 1.5 equals the ratio of areas `(1.5^2 - 1) / (2^2 - 1)`.

**Complexity.**
- **Time** is O(1) expected, with `4 / (pi * (1 - rho^2))` trials.
- **Space** is O(1).

```java run
import java.util.Random;
import java.util.function.DoubleSupplier;

public final class RandomPointRingRecognize {
    static long trials; // trials used since the counter was reset

    /**
     * Returns a uniform point in the ring inner <= r <= outer.
     * Time: O(1) expected. Space: O(1).
     * Invariant: each draw is uniform over the unit square and only the ring passes the test.
     */
    static double[] ringPoint(double inner, double outer, DoubleSupplier rand) {
        double rho2 = (inner / outer) * (inner / outer); // squared radius of the hole in unit coordinates
        while (true) {
            trials++;
            double ux = 2 * rand.getAsDouble() - 1;
            double uy = 2 * rand.getAsDouble() - 1;
            double r2 = ux * ux + uy * uy;
            if (rho2 <= r2 && r2 <= 1) return new double[]{outer * ux, outer * uy}; // inside the ring: scale and return
        }
    }

    static DoubleSupplier script(double... v) {
        int[] at = {0};
        return () -> v[at[0]++];
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        double[] a = ringPoint(1, 2, script(0.5, 0.5, 0.9, 0.5));
        if (a[0] != 1.6 || a[1] != 0.0) throw new AssertionError("ex1 " + a[0] + " " + a[1]);
        double[] b = ringPoint(0, 3, script(0.5, 0.5));
        if (b[0] != 0.0 || b[1] != 0.0) throw new AssertionError("ex2");
        // statistics for inner = 1, outer = 2
        Random rnd = new Random(82);
        DoubleSupplier src = rnd::nextDouble;
        int n = 200_000, within = 0;
        trials = 0;
        for (int i = 0; i < n; i++) {
            double[] p = ringPoint(1, 2, src);
            double r = Math.hypot(p[0], p[1]);
            if (r < 1 - 1e-12 || r > 2 + 1e-12) throw new AssertionError("outside the ring");
            if (r <= 1.5) within++;
        }
        double meanTrials = trials / (double) n;
        if (Math.abs(meanTrials - 4 / (Math.PI * 0.75)) > 0.02) throw new AssertionError("mean trials " + meanTrials);
        double areaShare = (1.5 * 1.5 - 1) / (4 - 1); // share of the ring inside radius 1.5
        if (Math.abs(within / (double) n - areaShare) > 0.01) throw new AssertionError("area share");
        System.out.println("ok");
    }
}
```
