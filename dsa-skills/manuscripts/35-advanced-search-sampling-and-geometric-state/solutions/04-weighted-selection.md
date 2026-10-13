<!-- solutions-for: 04-weighted-selection -->
### Solutions For Weighted Selection

#### Solution: [Build] Prefix Weight Intervals (Author exercise)
<!-- id: ws35-prefix-intervals -->

**Approach.**
The method keeps a running sum `run` of the weights seen so far. Index `i` owns the tickets above the old sum and up to the new sum, so the owner is the first index where `run` reaches `ticket`. The comparison `run >= ticket` gives a boundary ticket to the earlier index, since that index's range ends exactly at the ticket. The sum is a `long`, because a total near 10^14 does not fit in an `int`. The invariant is that before index `i`, the variable `run` equals the sum of the weights of the earlier indexes, and every earlier range ended below the ticket.

The program compares the method with a table that lists each index `w[i]` times, for every ticket of random small weight arrays. It also checks the two examples and confirms that two weights of 10^9 overflow in `int` but not in `long`.

**Complexity.**
- **Time** is O(n), because the scan stops at the owner and may read every weight.
- **Space** is O(1), because the method keeps one `long`.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class PrefixIntervalsBuild {
    /**
     * Returns the index that owns the ticket.
     * Time: O(n). Space: O(1).
     * Invariant: run is the sum of the weights before index i.
     */
    static int ownerOf(int[] w, long ticket) {
        long run = 0; // long: totals reach 10^14
        for (int i = 0; i < w.length; i++) {
            run += w[i]; // the range of index i ends at run
            if (run >= ticket) return i; // a boundary ticket stays with the earlier index
        }
        throw new IllegalArgumentException("ticket above the total");
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        if (ownerOf(new int[]{2, 5, 3}, 7) != 1) throw new AssertionError("ex1");
        if (ownerOf(new int[]{2, 5, 3}, 8) != 2) throw new AssertionError("ex2");
        // int addition of two weights of 10^9 and 2 * 10^9 wraps, long does not
        int wrapped = 1_000_000_000 + 1_000_000_000 + 1_000_000_000;
        if (wrapped >= 0 || 3L * 1_000_000_000 != 3_000_000_000L) throw new AssertionError("overflow claim");
        if (ownerOf(new int[]{1_000_000_000, 1_000_000_000, 1_000_000_000}, 3_000_000_000L) != 2) throw new AssertionError("large");
        // random weights: every ticket agrees with an expanded table
        Random rnd = new Random(51);
        for (int t = 0; t < 300; t++) {
            int[] w = new int[1 + rnd.nextInt(6)];
            List<Integer> table = new ArrayList<>();
            for (int i = 0; i < w.length; i++) { w[i] = 1 + rnd.nextInt(5); for (int c = 0; c < w[i]; c++) table.add(i); }
            for (int ticket = 1; ticket <= table.size(); ticket++)
                if (ownerOf(w, ticket) != table.get(ticket - 1)) throw new AssertionError("table mismatch");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Vary] Random Pick With Weight (LeetCode 528)
<!-- id: ws35-random-pick-weight -->

**Approach.**
The constructor builds the prefix totals once. Each pick draws `ticket = draw + 1`, which lies in 1 to the total, and runs a lower-bound search for the first prefix total that is at least the ticket. The search keeps the answer inside `[lo, hi]` and moves `hi` to `mid` when `prefix[mid] >= ticket`, since `mid` may be the answer, and moves `lo` past `mid` otherwise. When the bounds meet, they point at the owner. Because index `i` owns exactly `w[i]` tickets, a uniform draw gives it chance `w[i] / total`. The invariant is that the owner of the ticket always lies in `[lo, hi]`.

The program checks fairness by running every possible draw from 0 to `total - 1` and counting results. Each index must be returned exactly `w[i]` times. It also checks the examples.

**Complexity.**
- **Time** is O(n) for the constructor and O(log n) per pick.
- **Space** is O(n) for the prefix totals.

```java run
import java.util.Random;
import java.util.function.LongUnaryOperator;

public final class RandomPickWeightVary {
    static final class Picker {
        private final long[] prefix;
        private final LongUnaryOperator pick;

        Picker(int[] w, LongUnaryOperator pick) {
            prefix = new long[w.length];
            long run = 0;
            for (int i = 0; i < w.length; i++) { run += w[i]; prefix[i] = run; } // cumulative sums, built once
            this.pick = pick;
        }

        /**
         * Returns an index with chance proportional to its weight.
         * Time: O(log n). Space: O(1).
         * Invariant: the owner of the ticket lies in [lo, hi].
         */
        int pickIndex() {
            long ticket = pick.applyAsLong(prefix[prefix.length - 1]) + 1; // 1 to total
            int lo = 0, hi = prefix.length - 1;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (prefix[mid] >= ticket) hi = mid; // mid may be the owner
                else lo = mid + 1; // the owner is after mid
            }
            return lo;
        }
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d1 = {0, 1, 3};
        int[] at1 = {0};
        Picker p1 = new Picker(new int[]{1, 3}, b -> d1[at1[0]++]);
        if (p1.pickIndex() != 0 || p1.pickIndex() != 1 || p1.pickIndex() != 1) throw new AssertionError("ex1");
        if (new Picker(new int[]{2, 5, 3}, b -> 6).pickIndex() != 1) throw new AssertionError("ex2");
        // exact fairness: running every possible draw returns index i exactly w[i] times
        Random rnd = new Random(52);
        for (int t = 0; t < 300; t++) {
            int[] w = new int[1 + rnd.nextInt(7)];
            long total = 0;
            for (int i = 0; i < w.length; i++) { w[i] = 1 + rnd.nextInt(6); total += w[i]; }
            long[] counts = new long[w.length];
            for (long draw = 0; draw < total; draw++) {
                final long d = draw;
                long[] bounds = new long[1];
                counts[new Picker(w, b -> { bounds[0] = b; return d; }).pickIndex()]++;
                if (bounds[0] != total) throw new AssertionError("draw bound must be the total");
            }
            for (int i = 0; i < w.length; i++) if (counts[i] != w[i]) throw new AssertionError("unfair");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Boundary] Large Total And Zero Weight Policy (Author exercise)
<!-- id: ws35-large-total-zero-weight -->

**Approach.**
The constructor validates the input before it builds anything. An empty array, a negative weight or a zero total has no valid ticket, so each throws `IllegalArgumentException`. The prefix totals are `long`, since three weights of 10^9 already exceed the `int` range. A zero-weight index repeats the previous prefix total. The lower-bound search returns the first index that reaches the ticket, so it stops at the earlier index and never at the repeat. A zero weight at index 0 gives the prefix 0, which no ticket from 1 reaches, so it is skipped as well. The invariant is that the prefix totals never decrease and the returned index always has a positive weight.

The program runs every draw for random arrays with many zeros and counts the results, so index `i` must appear `w[i]` times and zero-weight indexes never. It also checks the exception cases and the overflow example.

**Complexity.**
- **Time** is O(n) for the constructor and O(log n) per pick.
- **Space** is O(n).

```java run
import java.util.Random;
import java.util.function.LongUnaryOperator;

public final class LargeTotalZeroWeightBoundary {
    static final class SafePicker {
        private final long[] prefix;
        private final LongUnaryOperator pick;

        SafePicker(int[] w, LongUnaryOperator pick) {
            if (w.length == 0) throw new IllegalArgumentException("empty");
            prefix = new long[w.length];
            long run = 0;
            for (int i = 0; i < w.length; i++) {
                if (w[i] < 0) throw new IllegalArgumentException("negative weight"); // no negative ranges
                run += w[i]; // long sum: up to 10^14
                prefix[i] = run;
            }
            if (run == 0) throw new IllegalArgumentException("zero total"); // no ticket exists
            this.pick = pick;
        }

        /**
         * Returns an index with a positive weight, chosen proportionally to the weights.
         * Time: O(log n). Space: O(1).
         * Invariant: prefix is non-decreasing, and the result has prefix[i] > prefix[i-1].
         */
        int pickIndex() {
            long ticket = pick.applyAsLong(prefix[prefix.length - 1]) + 1; // 1 to total
            int lo = 0, hi = prefix.length - 1;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (prefix[mid] >= ticket) hi = mid; else lo = mid + 1; // first prefix total at least the ticket
            }
            return lo;
        }
    }

    static boolean throwsIllegal(int[] w) {
        try { new SafePicker(w, b -> 0); return false; } catch (IllegalArgumentException e) { return true; }
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] d1 = {0, 3, 4};
        int[] at1 = {0};
        SafePicker p1 = new SafePicker(new int[]{0, 4, 0, 1}, b -> d1[at1[0]++]);
        if (p1.pickIndex() != 1 || p1.pickIndex() != 1 || p1.pickIndex() != 3) throw new AssertionError("ex1");
        if (new SafePicker(new int[]{1_000_000_000, 1_000_000_000, 1_000_000_000}, b -> 2_999_999_999L).pickIndex() != 2) throw new AssertionError("ex2");
        if (!throwsIllegal(new int[]{0, 0}) || !throwsIllegal(new int[0]) || !throwsIllegal(new int[]{3, -1})) throw new AssertionError("policy");
        // three weights of 10^9 overflow an int sum
        if (1_000_000_000 + 1_000_000_000 + 1_000_000_000 >= 0) throw new AssertionError("int sum should wrap");
        // exact counts over every draw, with many zero weights
        Random rnd = new Random(53);
        for (int t = 0; t < 300; t++) {
            int[] w = new int[1 + rnd.nextInt(8)];
            long total = 0;
            for (int i = 0; i < w.length; i++) { w[i] = rnd.nextInt(3) == 0 ? 0 : 1 + rnd.nextInt(5); total += w[i]; }
            if (total == 0) continue;
            long[] counts = new long[w.length];
            for (long draw = 0; draw < total; draw++) {
                final long d = draw;
                counts[new SafePicker(w, b -> d).pickIndex()]++;
            }
            for (int i = 0; i < w.length; i++) if (counts[i] != w[i]) throw new AssertionError("count mismatch");
        }
        System.out.println("ok");
    }
}
```

#### Solution: [Recognize] Mutable Weight Discussion (Author exercise)
<!-- id: ws35-mutable-weights -->

**Approach.**
Static prefix totals break when a weight changes, because one update shifts every later prefix total and repairing them costs O(n). A Fenwick tree stores partial sums so that a point update touches O(log n) cells and a prefix query reads O(log n) cells. The picker stores the current weights and a Fenwick tree. An update adds the difference `newWeight - old` along the update path. For a pick, the method draws the ticket and finds the owner by descent: starting from position 0, it tries the largest power-of-two step; if the tree cell at the next position holds less than the remaining ticket, it moves there and subtracts the cell. After the last step, the position is the count of indexes whose prefix is below the ticket, and that count is the owner's zero-based index. A pick with a total of 0 throws `IllegalStateException`. The invariant is that the tree always equals the Fenwick representation of the current weights, and the descent keeps the remaining ticket positive.

The program applies random updates and picks, and it compares each pick with a scan over a plain weight array. It also runs every draw after the updates and checks that each index appears exactly as often as its weight.

**Complexity.**
- **Time** is O(n) for the constructor with the linear-time build, and O(log n) per update and per pick.
- **Space** is O(n) for the tree and the weight copy.

```java run
import java.util.Random;
import java.util.function.LongUnaryOperator;

public final class MutableWeightsRecognize {
    static final class LivePicker {
        private final int n;
        private final long[] tree; // 1-based Fenwick tree
        private final int[] w;
        private final LongUnaryOperator pick;
        private long total;

        LivePicker(int[] weights, LongUnaryOperator pick) {
            n = weights.length;
            w = weights.clone();
            tree = new long[n + 1];
            for (int i = 1; i <= n; i++) {
                tree[i] += w[i - 1]; // add the weight of position i
                int parent = i + (i & -i);
                if (parent <= n) tree[parent] += tree[i]; // push the partial sum to its parent
                total += w[i - 1];
            }
            this.pick = pick;
        }

        /** Sets w[i]. Time: O(log n). Space: O(1). */
        void update(int i, int newWeight) {
            long delta = (long) newWeight - w[i]; // change to propagate
            w[i] = newWeight;
            total += delta;
            for (int p = i + 1; p <= n; p += p & -p) tree[p] += delta; // touch O(log n) cells
        }

        /**
         * Returns an index chosen proportionally to the current weights.
         * Time: O(log n). Space: O(1).
         * Invariant: remaining ticket stays positive and pos counts indexes whose prefix is below the ticket.
         */
        int pickIndex() {
            if (total == 0) throw new IllegalStateException("zero total");
            long ticket = pick.applyAsLong(total) + 1; // 1 to total
            int pos = 0;
            for (int step = Integer.highestOneBit(n); step > 0; step >>= 1) { // descend from the largest power of two
                if (pos + step <= n && tree[pos + step] < ticket) { pos += step; ticket -= tree[pos]; }
            }
            return pos; // zero-based index of the owner
        }
    }

    static int scan(int[] w, long ticket) {
        long run = 0;
        for (int i = 0; i < w.length; i++) { run += w[i]; if (run >= ticket) return i; }
        throw new AssertionError("ticket above total");
    }

    public static void main(String[] args) {
        // the two examples from the problem text
        long[] draw = {3};
        LivePicker p = new LivePicker(new int[]{3, 1, 2}, b -> draw[0]);
        if (p.pickIndex() != 1) throw new AssertionError("ex1 before");
        p.update(1, 5);
        if (p.pickIndex() != 1) throw new AssertionError("ex1 after, draw 3");
        draw[0] = 8;
        if (p.pickIndex() != 2) throw new AssertionError("ex1 after, draw 8");
        long[] draw2 = {3};
        LivePicker single = new LivePicker(new int[]{4}, b -> draw2[0]);
        if (single.pickIndex() != 0) throw new AssertionError("ex2");
        single.update(0, 0);
        boolean threw = false;
        try { single.pickIndex(); } catch (IllegalStateException e) { threw = true; }
        if (!threw) throw new AssertionError("zero total");
        // random updates: every possible draw agrees with a scan over the plain weights
        Random rnd = new Random(54);
        for (int t = 0; t < 200; t++) {
            int n = 1 + rnd.nextInt(9);
            int[] w = new int[n];
            for (int i = 0; i < n; i++) w[i] = rnd.nextInt(5);
            long[] d = {0};
            LivePicker lp = new LivePicker(w, b -> d[0]);
            for (int op = 0; op < 12; op++) {
                int i = rnd.nextInt(n), v = rnd.nextInt(6);
                lp.update(i, v);
                w[i] = v;
                long total = 0;
                for (int x : w) total += x;
                if (total == 0) continue;
                long[] counts = new long[n];
                for (long dr = 0; dr < total; dr++) {
                    d[0] = dr;
                    int got = lp.pickIndex();
                    if (got != scan(w, dr + 1)) throw new AssertionError("scan mismatch");
                    counts[got]++;
                }
                for (int j = 0; j < n; j++) if (counts[j] != w[j]) throw new AssertionError("unfair after update");
            }
        }
        System.out.println("ok");
    }
}
```
