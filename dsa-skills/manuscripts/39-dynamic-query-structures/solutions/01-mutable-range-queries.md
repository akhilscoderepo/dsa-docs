<!-- solutions-for: 01-mutable-range-queries -->
### Solutions For Mutable Range Queries

#### Solution: [Build] Mutable Range Sum (LeetCode 307)
<!-- id: dq39-mutable-range-sum -->

**Approach.** The class keeps a Fenwick tree of `long` sums and a plain copy of the current values.

An update computes the difference between the new value and the stored value, and then adds that difference to every entry whose owned range contains the position. The walk starts at the one-based entry `index + 1` and adds the lowest set bit each time. A sum query converts the closed range `[left, right]` to the half-open range `[left, right + 1)`. It then subtracts one prefix walk from another, where each prefix walk clears the lowest set bit of its index.

The invariant is that every tree entry equals the sum of the copy over the positions it owns, after each call. The update keeps it because only the changed position differs, and the difference reaches exactly the entries that own that position.

**Complexity.**

- **Time** is O(log n) per call, because each walk changes the index by its lowest set bit and visits at most about log2(n) + 1 entries.
- **Space** is O(n), because the tree and the value copy each hold one `long` per position.

```java run
import java.util.Random;

public final class MutableRangeSum {
    static final class NumArray {
        private final int n;            // number of positions
        private final long[] tree;      // tree[i] sums the owned range of entry i, one-based
        private final long[] values;    // current value at each zero-based position

        /**
         * Builds the tree from the starting values.
         * Time: O(n log n), because each position is added by one update walk.
         * Space: O(n), because the tree and the copy hold n longs each.
         * Invariant: every tree entry equals the sum of its owned positions.
         */
        NumArray(int[] nums) {
            // Remember the size so every walk knows where to stop.
            n = nums.length;
            // One extra slot because entries are one-based.
            tree = new long[n + 1];
            // The copy lets update compute the old value in O(1).
            values = new long[n];
            // Insert each starting value as an update from zero.
            for (int i = 0; i < n; i++) update(i, nums[i]);
        }

        /**
         * Assigns val to nums[index].
         * Time: O(log n), because the walk moves up by the lowest set bit each step.
         * Space: O(1), because only a few locals are used.
         * Invariant: the difference reaches exactly the entries that own the position.
         */
        void update(int index, int val) {
            // The difference from the old value is what the covering entries must gain.
            long delta = (long) val - values[index];
            // Store the new value so the next update computes its difference correctly.
            values[index] = val;
            // Walk from the one-based entry upward while the entry exists; each step adds the lowest set bit.
            for (int i = index + 1; i <= n; i += i & -i) {
                // Every visited entry owns the position, so it gains the difference.
                tree[i] += delta;
            }
        }

        // Sums positions [0, end) by clearing the lowest set bit of the entry each step; O(log n).
        private long prefix(int end) {
            // Accumulator is a long because sums can exceed the int range.
            long sum = 0;
            // Stop at entry 0; the visited owned ranges tile [0, end) exactly.
            for (int i = end; i > 0; i -= i & -i) {
                // Add the whole owned range of this entry in one read.
                sum += tree[i];
            }
            // Return the prefix total.
            return sum;
        }

        /**
         * Returns the sum of nums[left..right], both included.
         * Time: O(log n), because it runs two prefix walks.
         * Space: O(1), because only locals are used.
         * Invariant: the closed range converts once to the half-open range [left, right + 1).
         */
        long sumRange(int left, int right) {
            // The right endpoint is closed, so the exclusive prefix end is right + 1.
            return prefix(right + 1) - prefix(left);
        }
    }

    public static void main(String[] args) {
        // Check Example 1: query, update, query again.
        NumArray a = new NumArray(new int[] {3, 1, 4, 1, 5, 9});
        if (a.sumRange(1, 3) != 6) throw new AssertionError("example 1 before");
        a.update(2, 10);
        if (a.sumRange(1, 3) != 12) throw new AssertionError("example 1 after");
        // Check Example 2: a single element with a negative assignment.
        NumArray b = new NumArray(new int[] {7});
        b.update(0, -2);
        if (b.sumRange(0, 0) != -2) throw new AssertionError("example 2");
        // Compare with a brute-force array on random interleaved calls.
        Random rnd = new Random(307);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(40);
            int[] ref = new int[n];
            for (int i = 0; i < n; i++) ref[i] = rnd.nextInt(201) - 100;
            NumArray s = new NumArray(ref.clone());
            for (int op = 0; op < 120; op++) {
                if (rnd.nextBoolean()) {
                    int idx = rnd.nextInt(n);
                    int v = rnd.nextInt(201) - 100;
                    ref[idx] = v;
                    s.update(idx, v);
                } else {
                    int l = rnd.nextInt(n);
                    int r = l + rnd.nextInt(n - l);
                    long want = 0;
                    for (int i = l; i <= r; i++) want += ref[i];
                    if (s.sumRange(l, r) != want) throw new AssertionError("random mismatch");
                }
            }
        }
    }
}
```

#### Solution: [Vary] Mutable Matrix Region Sum (LeetCode 308)
<!-- id: dq39-mutable-matrix-sum -->

**Approach.** The class nests a column walk inside a row walk over a table of `long` entries.

Entry `(r, c)` owns the rectangle whose rows are owned by `r` in the row dimension and whose columns are owned by `c` in the column dimension. An update computes the difference from the stored cell and adds it to every entry reached by the nested upward walks. A prefix query sums every entry reached by the nested downward walks and returns the total of the rectangle from the origin to an exclusive corner.

A region with closed bounds converts to exclusive corners `(row2 + 1, col2 + 1)` and `(row1, col1)`. Inclusion and exclusion then give four prefix terms, where the overlap is added back once. The invariant is that each entry equals the cell sum over the rectangle it owns after every call.

**Complexity.**

- **Time** is O(log m * log n) per call, because each of the two nested walks visits at most about log2 of its dimension plus one entries.
- **Space** is O(m * n), because the table and the cell copy each hold one `long` per cell.

```java run
import java.util.Random;

public final class MutableMatrixSum {
    static final class NumMatrix {
        private final int rows;         // number of rows
        private final int cols;         // number of columns
        private final long[][] tree;    // tree[r][c] sums the rectangle owned by entry (r, c), one-based
        private final long[][] cells;   // current value of each zero-based cell

        /**
         * Builds the table from the starting matrix.
         * Time: O(m * n * log m * log n), because each cell is inserted by one update.
         * Space: O(m * n), because the table and the copy hold one long per cell.
         * Invariant: every entry equals the cell sum over its owned rectangle.
         */
        NumMatrix(int[][] matrix) {
            // Store the dimensions so the walks know their limits.
            rows = matrix.length;
            cols = matrix[0].length;
            // Extra row and column because entries are one-based.
            tree = new long[rows + 1][cols + 1];
            // The copy gives the old value of a cell in O(1).
            cells = new long[rows][cols];
            // Insert every starting cell as an update from zero.
            for (int r = 0; r < rows; r++)
                for (int c = 0; c < cols; c++) update(r, c, matrix[r][c]);
        }

        /**
         * Assigns val to one cell.
         * Time: O(log m * log n), because the outer and inner walks each move up by the lowest set bit.
         * Space: O(1), because only locals are used.
         * Invariant: the difference reaches exactly the entries whose rectangles contain the cell.
         */
        void update(int row, int col, int val) {
            // Difference from the stored value; adding val directly would count the cell twice.
            long delta = (long) val - cells[row][col];
            // Store the new value for future differences.
            cells[row][col] = val;
            // Outer walk over row entries that own this row.
            for (int i = row + 1; i <= rows; i += i & -i) {
                // Inner walk over column entries that own this column.
                for (int j = col + 1; j <= cols; j += j & -j) {
                    // Entry (i, j) owns the cell, so it gains the difference.
                    tree[i][j] += delta;
                }
            }
        }

        // Sums the rectangle of rows [0, endRow) and columns [0, endCol); O(log m * log n).
        private long prefix(int endRow, int endCol) {
            // Accumulator is a long because region sums can pass the int range.
            long sum = 0;
            // Outer walk clears the lowest set bit of the row entry each step.
            for (int i = endRow; i > 0; i -= i & -i) {
                // Inner walk does the same for the column entry.
                for (int j = endCol; j > 0; j -= j & -j) {
                    // The owned rectangles of the visited entries tile the prefix rectangle.
                    sum += tree[i][j];
                }
            }
            // Return the rectangle total.
            return sum;
        }

        /**
         * Returns the sum of all cells in the closed rectangle.
         * Time: O(log m * log n), because it runs four prefix walks.
         * Space: O(1), because only locals are used.
         * Invariant: closed bounds convert once to exclusive corners.
         */
        long sumRegion(int row1, int col1, int row2, int col2) {
            // Inclusion and exclusion: add the big corner, remove the two strips, add the overlap back.
            return prefix(row2 + 1, col2 + 1) - prefix(row1, col2 + 1)
                 - prefix(row2 + 1, col1) + prefix(row1, col1);
        }
    }

    public static void main(String[] args) {
        // Check Example 1: query, update, then two queries.
        NumMatrix m = new NumMatrix(new int[][] {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}});
        if (m.sumRegion(0, 0, 1, 1) != 12) throw new AssertionError("example 1 before");
        m.update(1, 1, 0);
        if (m.sumRegion(0, 0, 1, 1) != 7) throw new AssertionError("example 1 after");
        if (m.sumRegion(1, 1, 2, 2) != 23) throw new AssertionError("example 1 lower right");
        // Check Example 2: a single cell.
        NumMatrix one = new NumMatrix(new int[][] {{5}});
        one.update(0, 0, -5);
        if (one.sumRegion(0, 0, 0, 0) != -5) throw new AssertionError("example 2");
        // Compare with a brute-force matrix on random interleaved calls.
        Random rnd = new Random(308);
        for (int round = 0; round < 200; round++) {
            int h = 1 + rnd.nextInt(8), w = 1 + rnd.nextInt(8);
            int[][] ref = new int[h][w];
            for (int[] row : ref) for (int c = 0; c < w; c++) row[c] = rnd.nextInt(2001) - 1000;
            int[][] copy = new int[h][];
            for (int r = 0; r < h; r++) copy[r] = ref[r].clone();
            NumMatrix s = new NumMatrix(copy);
            for (int op = 0; op < 80; op++) {
                if (rnd.nextInt(5) == 0) {
                    int r = rnd.nextInt(h), c = rnd.nextInt(w), v = rnd.nextInt(2001) - 1000;
                    ref[r][c] = v;
                    s.update(r, c, v);
                } else {
                    int r1 = rnd.nextInt(h), r2 = r1 + rnd.nextInt(h - r1);
                    int c1 = rnd.nextInt(w), c2 = c1 + rnd.nextInt(w - c1);
                    long want = 0;
                    for (int r = r1; r <= r2; r++) for (int c = c1; c <= c2; c++) want += ref[r][c];
                    if (s.sumRegion(r1, c1, r2, c2) != want) throw new AssertionError("random mismatch");
                }
            }
        }
    }
}
```

#### Solution: [Boundary] Repeated Assignment (Author exercise)
<!-- id: dq39-repeated-assignment -->

**Approach.** The ledger keeps a Fenwick tree and a copy of the current slot values, and each assignment adds only the difference from the copy.

The first `set(1,5)` adds 5. The second `set(1,5)` computes a difference of 0 and changes nothing. The later `set(1,2)` adds -3, so the total becomes 2. An implementation that adds `value` directly would report 12 for Example 1, because it counts the slot three times.

The difference between two `int` values can need 33 bits, so the code subtracts in `long`. Sums use `long` as well. The query takes the half-open range `[from, to)`, so `from == to` yields 0 without a special case. The invariant is that the copy always equals the last assigned value of each slot, and each tree entry equals the sum of the copy over its owned range.

**Complexity.**

- **Time** is O(log n) per call, because each update and each prefix walk visits at most about log2(n) + 1 entries.
- **Space** is O(n), because the tree and the copy each hold one `long` per slot.

```java run
import java.util.Random;

public final class RepeatedAssignment {
    static final class Ledger {
        private final int n;            // number of slots
        private final long[] tree;      // tree[i] sums the owned range of entry i, one-based
        private final long[] current;   // last assigned value of each slot

        /**
         * Creates a ledger of n slots, all zero.
         * Time: O(n), because the arrays are allocated and zero-filled.
         * Space: O(n), because the tree and the copy hold n longs each.
         * Invariant: the empty tree matches the all-zero copy.
         */
        Ledger(int n) {
            // Keep the size for the walk limits.
            this.n = n;
            // Extra slot because entries are one-based.
            tree = new long[n + 1];
            // Zero-filled copy: every slot starts at 0.
            current = new long[n];
        }

        /**
         * Assigns value to a slot, as many times as the caller likes.
         * Time: O(log n), because the walk moves up by the lowest set bit.
         * Space: O(1), because only locals are used.
         * Invariant: the tree changes by value minus the last assigned value, never by value itself.
         */
        void set(int slot, int value) {
            // Subtract in long: the difference of two ints can need 33 bits.
            long delta = (long) value - current[slot];
            // Record the assignment so the next set sees this value as the old one.
            current[slot] = value;
            // Walk upward through every entry that owns the slot; a delta of 0 adds nothing.
            for (int i = slot + 1; i <= n; i += i & -i) {
                // Each owning entry gains only the difference.
                tree[i] += delta;
            }
        }

        // Sums slots [0, end) by clearing the lowest set bit each step; O(log n).
        private long prefix(int end) {
            // Long accumulator, since four billion does not fit in an int.
            long sum = 0;
            // Stop at entry 0.
            for (int i = end; i > 0; i -= i & -i) {
                // Add the whole owned range of the entry.
                sum += tree[i];
            }
            // Return the prefix total.
            return sum;
        }

        /**
         * Returns the sum of slots in the half-open range [from, to).
         * Time: O(log n), because it runs two prefix walks.
         * Space: O(1), because only locals are used.
         * Invariant: an empty range gives prefix(from) - prefix(from) = 0.
         */
        long total(int from, int to) {
            // Half-open endpoints need no adjustment.
            return prefix(to) - prefix(from);
        }
    }

    public static void main(String[] args) {
        // Check Example 1: repeated and changed assignments to one slot.
        Ledger a = new Ledger(4);
        a.set(1, 5);
        a.set(1, 5);
        if (a.total(0, 4) != 5) throw new AssertionError("repeat of the same value adds nothing");
        a.set(1, 2);
        if (a.total(0, 4) != 2) throw new AssertionError("example 1");
        // Show that adding the value directly would give 12, not 2.
        if (5 + 5 + 2 != 12) throw new AssertionError("direct addition counts the slot three times");
        // Check Example 2: the total passes the int range.
        Ledger b = new Ledger(2);
        b.set(0, 2_000_000_000);
        b.set(1, 2_000_000_000);
        if (b.total(0, 2) != 4_000_000_000L) throw new AssertionError("example 2");
        // Check that the int-sized difference of the extreme values overflows int but not long.
        if ((Integer.MAX_VALUE - Integer.MIN_VALUE) != -1) throw new AssertionError("int subtraction wraps");
        Ledger c = new Ledger(1);
        c.set(0, Integer.MIN_VALUE);
        c.set(0, Integer.MAX_VALUE);
        if (c.total(0, 1) != Integer.MAX_VALUE) throw new AssertionError("extreme reassignment");
        // Check that an empty range returns 0.
        if (a.total(2, 2) != 0) throw new AssertionError("empty range");
        // Compare with a brute-force array on random calls with many repeated slots.
        Random rnd = new Random(2024);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(12);
            long[] ref = new long[n];
            Ledger s = new Ledger(n);
            for (int op = 0; op < 150; op++) {
                if (rnd.nextInt(3) != 0) {
                    int slot = rnd.nextInt(Math.min(n, 3));
                    int v = rnd.nextBoolean() ? rnd.nextInt(5) : rnd.nextInt();
                    ref[slot] = v;
                    s.set(slot, v);
                } else {
                    int from = rnd.nextInt(n + 1), to = from + rnd.nextInt(n + 1 - from);
                    long want = 0;
                    for (int i = from; i < to; i++) want += ref[i];
                    if (s.total(from, to) != want) throw new AssertionError("random mismatch");
                }
            }
        }
    }
}
```

#### Solution: [Recognize] Mutable Range Minimum (Author exercise)
<!-- id: dq39-mutable-range-minimum -->

**Approach.** The choice is a segment tree, because a Fenwick tree cannot undo a stored minimum.

A Fenwick entry for addition is patched by a difference, since subtracting the old value restores the sum without it. A stored minimum has no such repair. When a leaf that equals the stored minimum rises, the entry needs the next smallest value in its owned range, and the entry does not contain it. A Fenwick variant that only lowers entries with `min` therefore keeps stale small values. The harness shows this on `[5, 2, 8, 6]`, where it still reports 2 after position 1 changes to 9.

The segment tree stores the minimum of each node over a block of leaves. An update writes the leaf and then recomputes each ancestor as the minimum of its two children, so a rise propagates correctly. A query on `[from, to)` combines the O(log n) nodes that tile the range. The invariant is that each node equals the minimum of its leaves after every call.

**Complexity.**

- **Time** is O(log n) per call, because an update recomputes one node per level and a query visits at most two nodes per level.
- **Space** is O(n), because the tree holds 2n `int` values.

```java run
import java.util.Random;

public final class MutableRangeMinimum {
    static final class MinTree {
        private final int n;            // number of leaves
        private final int[] node;       // node[n + i] is leaf i; node[p] = min(node[2p], node[2p + 1])

        /**
         * Builds the tree bottom-up from the starting values.
         * Time: O(n), because each internal node is computed once.
         * Space: O(n), because 2n ints are stored.
         * Invariant: every internal node equals the minimum of its two children.
         */
        MinTree(int[] values) {
            // Remember the leaf count.
            n = values.length;
            // Leaves occupy the upper half; internal nodes occupy the lower half.
            node = new int[2 * n];
            // Copy the values into the leaf positions.
            System.arraycopy(values, 0, node, n, n);
            // Fill internal nodes from the last to the first so children exist before parents.
            for (int p = n - 1; p >= 1; p--) node[p] = Math.min(node[2 * p], node[2 * p + 1]);
        }

        /**
         * Assigns value to one leaf and recomputes its ancestors.
         * Time: O(log n), because the walk halves the node index each step.
         * Space: O(1), because only locals are used.
         * Invariant: every ancestor is recomputed from its children, so a rise is never hidden.
         */
        void set(int index, int value) {
            // Start at the leaf position.
            int p = index + n;
            // Write the new value.
            node[p] = value;
            // Move to the parent until the root; each parent is rebuilt from both children.
            while (p > 1) {
                // Parent index is p / 2.
                p >>= 1;
                // Recompute rather than patch, since min has no inverse.
                node[p] = Math.min(node[2 * p], node[2 * p + 1]);
            }
        }

        /**
         * Returns the minimum over the half-open range [from, to).
         * Time: O(log n), because each level contributes at most two nodes.
         * Space: O(1), because only locals are used.
         * Invariant: the visited nodes tile [from, to) exactly.
         */
        int min(int from, int to) {
            // Identity of min, so the first real value replaces it.
            int best = Integer.MAX_VALUE;
            // Shift both ends to leaf positions; the loop ends when the ends meet.
            for (int l = from + n, r = to + n; l < r; l >>= 1, r >>= 1) {
                // An odd left end is a right child, so take it alone and move right.
                if ((l & 1) == 1) best = Math.min(best, node[l++]);
                // An odd right end excludes its right sibling, so take the node before it.
                if ((r & 1) == 1) best = Math.min(best, node[--r]);
            }
            // Return the range minimum.
            return best;
        }
    }

    // A Fenwick tree that only lowers entries; shown to fail once a value rises.
    static final class BrokenFenwickMin {
        private final int n;
        private final int[] tree;
        BrokenFenwickMin(int[] values) {
            // Initialize every entry as the identity of min.
            n = values.length;
            tree = new int[n + 1];
            java.util.Arrays.fill(tree, Integer.MAX_VALUE);
            for (int i = 0; i < n; i++) set(i, values[i]);
        }
        void set(int index, int value) {
            // Lower each covering entry; nothing can raise an entry again.
            for (int i = index + 1; i <= n; i += i & -i) tree[i] = Math.min(tree[i], value);
        }
        int prefixMin(int end) {
            // Minimum of positions [0, end) by the usual downward walk.
            int best = Integer.MAX_VALUE;
            for (int i = end; i > 0; i -= i & -i) best = Math.min(best, tree[i]);
            return best;
        }
    }

    public static void main(String[] args) {
        // Check Example 1: the minimum rises after the smallest value is replaced.
        MinTree t = new MinTree(new int[] {5, 2, 8, 6});
        if (t.min(0, 4) != 2) throw new AssertionError("example 1 before");
        t.set(1, 9);
        if (t.min(0, 4) != 5) throw new AssertionError("example 1 after");
        // Check Example 2: a single leaf.
        MinTree one = new MinTree(new int[] {4});
        one.set(0, -3);
        if (one.min(0, 1) != -3) throw new AssertionError("example 2");
        // Show that the lowering-only Fenwick variant keeps the stale minimum 2.
        BrokenFenwickMin bad = new BrokenFenwickMin(new int[] {5, 2, 8, 6});
        bad.set(1, 9);
        if (bad.prefixMin(4) != 2) throw new AssertionError("the Fenwick variant keeps the stale minimum");
        // Compare with a brute-force scan on random interleaved calls, including extreme values.
        Random rnd = new Random(2025);
        for (int round = 0; round < 300; round++) {
            int n = 1 + rnd.nextInt(30);
            int[] ref = new int[n];
            for (int i = 0; i < n; i++) ref[i] = rnd.nextInt();
            MinTree s = new MinTree(ref.clone());
            for (int op = 0; op < 120; op++) {
                if (rnd.nextBoolean()) {
                    int idx = rnd.nextInt(n), v = rnd.nextInt();
                    ref[idx] = v;
                    s.set(idx, v);
                } else {
                    int from = rnd.nextInt(n), to = from + 1 + rnd.nextInt(n - from);
                    int want = Integer.MAX_VALUE;
                    for (int i = from; i < to; i++) want = Math.min(want, ref[i]);
                    if (s.min(from, to) != want) throw new AssertionError("random mismatch");
                }
            }
        }
    }
}
```
