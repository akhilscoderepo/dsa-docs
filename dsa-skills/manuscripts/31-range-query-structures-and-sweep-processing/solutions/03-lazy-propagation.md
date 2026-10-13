<!-- solutions-for: 03-lazy-propagation -->
### Solutions For Lazy Propagation

#### Solution: [Build] Range Add One Node (Author exercise)
<!-- id: rq31-range-add-one-node -->

**Approach.** The node keeps its sum and its pending tag as two `long` values. Applying a delta multiplies it by the node length, adds that product to the sum and adds the delta itself to the tag.

The invariant is that the sum always equals the starting sum plus the tag times the length. The tag stays in per-position units, so a later push down can hand it to a child of any length. The product uses `long` arithmetic, because a delta of 10^9 times a length of 10^5 exceeds the `int` range. An empty list leaves both values unchanged.

**Complexity.**

- **Time** is O(m) for `m` deltas, because each delta costs one multiplication and two additions.
- **Space** is O(1), because the node stores only the sum and the tag.

```java run
import java.util.Random;

public final class RangeAddOneNode {
    /**
     * Applies whole-node deltas and returns {sum, tag}.
     * Time: O(m) for m deltas. Space: O(1) beyond the two-element result.
     * Invariant: sum equals startSum + tag * len after every delta.
     */
    static long[] apply(int len, long startSum, long[] deltas) {
        // The sum starts at the stored value and the pending tag starts empty.
        long sum = startSum, tag = 0;
        // One iteration per delta, which is the only source of cost.
        for (long d : deltas) {
            // The delta reaches every one of the len positions, so the sum moves by d * len in long arithmetic.
            sum += d * len;
            // The tag keeps the per-position amount for the children, so it does not scale by len.
            tag += d;
        }
        // Return both values so the caller can compare them with the expected result.
        return new long[]{sum, tag};
    }

    /** Oracle: materializes the positions and adds each delta to every one of them. */
    static long[] brute(int len, long startSum, long[] deltas) {
        // Spread the starting sum over positions: the first holds the remainder, the others hold 0.
        long[] pos = new long[len];
        pos[0] = startSum;
        // Track the per-position total independently of the node formula.
        long tag = 0;
        // Apply every delta to every position one by one.
        for (long d : deltas) {
            for (int i = 0; i < len; i++) pos[i] += d;
            tag += d;
        }
        // Sum the positions to obtain the true node total.
        long s = 0;
        for (long x : pos) s += x;
        return new long[]{s, tag};
    }

    public static void main(String[] args) {
        // Checks Example 1 against the stated output.
        long[] r1 = apply(4, 10, new long[]{3, -1, 2});
        if (r1[0] != 26 || r1[1] != 4) throw new AssertionError("example 1");
        // Checks Example 2: values beyond the int range need long arithmetic.
        long[] r2 = apply(100000, 0, new long[]{1_000_000_000L, 1_000_000_000L, 1_000_000_000L});
        if (r2[0] != 300_000_000_000_000L || r2[1] != 3_000_000_000L) throw new AssertionError("example 2");
        // Checks the empty list: nothing changes.
        long[] r3 = apply(5, -7, new long[0]);
        if (r3[0] != -7 || r3[1] != 0) throw new AssertionError("empty list");
        // Compares with the brute force on random nodes and delta lists using a fixed seed.
        Random rnd = new Random(31_03_01);
        for (int t = 0; t < 500; t++) {
            int len = 1 + rnd.nextInt(8);
            long s = rnd.nextInt(2001) - 1000;
            long[] ds = new long[rnd.nextInt(6)];
            for (int i = 0; i < ds.length; i++) ds[i] = rnd.nextInt(41) - 20;
            long[] a = apply(len, s, ds), b = brute(len, s, ds);
            if (a[0] != b[0] || a[1] != b[1]) throw new AssertionError("mismatch at trial " + t);
        }
    }
}
```

#### Solution: [Vary] Push Before Descent (Author exercise)
<!-- id: rq31-push-before-descent -->

**Approach.** The push scales the parent tag by each child's own length and not by the parent's length. Each child gains `tag * childLength` in its sum and `tag` in its own tag. The parent tag then becomes 0.

The invariant is that the parent's sum equals the sum of its children's sums after the push, and it is equal to the parent's sum before the push when the children were consistent with the parent tag. Because the parent tag is cleared, a second push finds nothing to move and changes nothing. Skipping the clearing step would apply the same amount twice.

**Complexity.**

- **Time** is O(1), because the push touches exactly three nodes and does a fixed number of operations.
- **Space** is O(1), because the result holds five numbers.

```java run
import java.util.Random;

public final class PushBeforeDescent {
    /**
     * Pushes the parent tag to both children and returns {parentTag, leftSum, leftTag, rightSum, rightTag}.
     * Time: O(1). Space: O(1).
     * Invariant: afterwards the parent tag is 0, so a repeated push moves nothing.
     */
    static long[] push(int a, int b, long parentTag, long leftSum, long leftTag, long rightSum, long rightTag) {
        // A zero tag means the children are already current, so there is nothing to move.
        if (parentTag != 0) {
            // The left child covers a positions, so its sum grows by tag times a.
            leftSum += parentTag * a;
            // The left child keeps the amount as its own pending tag for its children.
            leftTag += parentTag;
            // The right child covers b positions, so its sum grows by tag times b.
            rightSum += parentTag * b;
            // The right child also records the amount as pending.
            rightTag += parentTag;
            // Clearing the parent tag makes the transfer happen exactly once.
            parentTag = 0;
        }
        // Return the five values in the order the problem states.
        return new long[]{parentTag, leftSum, leftTag, rightSum, rightTag};
    }

    public static void main(String[] args) {
        // Checks Example 1 against the stated output.
        if (!java.util.Arrays.equals(push(2, 3, 4, 10, 1, 30, 0), new long[]{0, 18, 5, 42, 4})) throw new AssertionError("example 1");
        // Checks Example 2 with a negative parent tag and a nonzero right tag.
        if (!java.util.Arrays.equals(push(1, 4, -3, 5, 0, -2, 2), new long[]{0, 2, -3, -14, -1})) throw new AssertionError("example 2");
        // Compares with a model that rebuilds each child sum from its explicit positions, using a fixed seed.
        Random rnd = new Random(31_03_02);
        for (int t = 0; t < 500; t++) {
            int a = 1 + rnd.nextInt(5), b = 1 + rnd.nextInt(5);
            long pt = rnd.nextInt(21) - 10;
            long ls = rnd.nextInt(101) - 50, lt = rnd.nextInt(11) - 5;
            long rs = rnd.nextInt(101) - 50, rt = rnd.nextInt(11) - 5;
            long[] got = push(a, b, pt, ls, lt, rs, rt);
            // Model: every position under the left child gains pt, so the sum gains pt once per position.
            long modelLeft = ls;
            for (int i = 0; i < a; i++) modelLeft += pt;
            long modelRight = rs;
            for (int i = 0; i < b; i++) modelRight += pt;
            if (got[0] != 0 || got[1] != modelLeft || got[3] != modelRight || got[2] != lt + pt || got[4] != rt + pt) throw new AssertionError("mismatch at trial " + t);
            // A second push must change nothing, which proves the transfer happens once.
            long[] again = push(a, b, got[0], got[1], got[2], got[3], got[4]);
            if (!java.util.Arrays.equals(got, again)) throw new AssertionError("second push changed state at trial " + t);
        }
    }
}
```

#### Solution: [Boundary] Assignment Versus Addition Tags (Author exercise)
<!-- id: rq31-assignment-versus-addition -->

**Approach.** The tag is a pair of a kind and a number, and each new operation composes with the current tag by a fixed rule. An assignment replaces the tag. An addition on an empty or addition tag adds the amounts. An addition on an assignment of `v` gives an assignment of `v + d`.

The invariant is that the tag applied to the untouched positions gives the same result as running all operations in order. Once the final tag is an assignment, the old child sum is irrelevant, and the child sum becomes `v * c`. For an addition tag, the child sum becomes `sc + d * c`. Swapping the order of an addition and an assignment changes the tag, which the second example shows.

**Complexity.**

- **Time** is O(m) for `m` operations, because each operation composes with the tag in constant time.
- **Space** is O(1), because the tag is one kind and one number.

```java run
import java.util.Random;

public final class TagComposition {
    /** Operation kinds: 0 is add, 1 is set. Tag kinds: 0 is none, 1 is add, 2 is set. */
    /**
     * Composes the operations and returns {nodeSum, tagKind, tagValue, childSum}.
     * Time: O(m) for m operations. Space: O(1).
     * Invariant: the tag alone reproduces the effect of all operations applied so far.
     */
    static long[] run(int len, long sum, int[] kinds, long[] vals, int c, long childSum) {
        // Start with an empty tag, which changes nothing.
        int tagKind = 0;
        long tagVal = 0;
        // Compose one operation at a time, in the given order.
        for (int i = 0; i < kinds.length; i++) {
            // A set operation ignores every earlier tag, because it overwrites all old values.
            if (kinds[i] == 1) {
                tagKind = 2;
                tagVal = vals[i];
            } else if (tagKind == 0) {
                // An add on an empty tag starts an addition tag.
                tagKind = 1;
                tagVal = vals[i];
            } else {
                // An add on an add tag sums the amounts, and an add on a set tag shifts the assigned value.
                tagVal += vals[i];
            }
        }
        // Apply the final tag to the node sum and push it to the child.
        if (tagKind == 1) {
            // Addition changes both sums by the amount times the node length.
            sum += tagVal * len;
            childSum += tagVal * c;
        } else if (tagKind == 2) {
            // Assignment makes the old sums irrelevant, so both are recomputed from the value alone.
            sum = tagVal * len;
            childSum = tagVal * c;
        }
        // Return all four values so the harness can compare the whole state.
        return new long[]{sum, tagKind, tagVal, childSum};
    }

    public static void main(String[] args) {
        // Checks Example 1: add 3, set 5, add 2 gives set 7.
        if (!java.util.Arrays.equals(run(4, 10, new int[]{0, 1, 0}, new long[]{3, 5, 2}, 2, 6), new long[]{28, 2, 7, 14})) throw new AssertionError("example 1");
        // Checks Example 2: swapping add and set changes the tag from set 5 to set 7.
        if (!java.util.Arrays.equals(run(4, 10, new int[]{0, 1}, new long[]{2, 5}, 2, 6), new long[]{20, 2, 5, 10})) throw new AssertionError("add then set");
        if (!java.util.Arrays.equals(run(4, 10, new int[]{1, 0}, new long[]{5, 2}, 2, 6), new long[]{28, 2, 7, 14})) throw new AssertionError("set then add");
        // Compares with an element-by-element simulation using a fixed seed.
        Random rnd = new Random(31_03_03);
        for (int t = 0; t < 500; t++) {
            int len = 1 + rnd.nextInt(6), c = 1 + rnd.nextInt(len);
            long[] pos = new long[len];
            for (int i = 0; i < len; i++) pos[i] = rnd.nextInt(21) - 10;
            long s = 0, cs = 0;
            for (int i = 0; i < len; i++) { s += pos[i]; if (i < c) cs += pos[i]; }
            int m = rnd.nextInt(6);
            int[] kinds = new int[m];
            long[] vals = new long[m];
            for (int i = 0; i < m; i++) {
                kinds[i] = rnd.nextInt(2);
                vals[i] = rnd.nextInt(21) - 10;
                // Simulate the operation on every position directly.
                for (int j = 0; j < len; j++) pos[j] = kinds[i] == 1 ? vals[i] : pos[j] + vals[i];
            }
            long ns = 0, ncs = 0;
            for (int j = 0; j < len; j++) { ns += pos[j]; if (j < c) ncs += pos[j]; }
            long[] got = run(len, s, kinds, vals, c, cs);
            if (got[0] != ns || got[3] != ncs) throw new AssertionError("mismatch at trial " + t);
        }
    }
}
```

#### Solution: [Recognize] Range Add Range Sum (Author exercise)
<!-- id: rq31-range-add-range-sum -->

**Approach.** A tree of sums with a pending amount per node answers both operations in logarithmic time. A range add stops at every node whose range lies inside the update and records the amount there. A range sum stops at every node inside the query and reads its stored sum.

The invariant is that every stored total already includes the tags at its own node, while the children may lag behind by that tag. Any operation that must enter a node with a nonzero pending amount first hands the amount to both children, scaled by their lengths, and clears it. After an update returns from its children, the node recomputes its total from them. Half-open ranges and `long` totals keep the boundaries and the large values safe.

**Complexity.**

- **Time** is O(n + q log n) for `q` operations, because building costs O(n) and each operation visits O(log n) nodes.
- **Space** is O(n), because the two arrays hold `4n` entries each.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class RangeAddRangeSum {
    private final int n;
    private final long[] total;    // total[k]: sum of node k's range with its own pending amount applied
    private final long[] pending;  // pending[k]: per-position amount the children have not received

    RangeAddRangeSum(int[] a) {
        // Remember the length and allocate four slots per position, which covers any tree shape.
        n = a.length;
        total = new long[4 * n];
        pending = new long[4 * n];
        // Build bottom-up values once, which costs O(n).
        init(1, 0, n, a);
    }

    private void init(int k, int lo, int hi, int[] a) {
        // A leaf stores its element directly.
        if (hi - lo == 1) { total[k] = a[lo]; return; }
        // Split the half-open range in the middle and build both halves.
        int mid = (lo + hi) / 2;
        init(2 * k, lo, mid, a);
        init(2 * k + 1, mid, hi, a);
        // An internal total is the sum of its two children.
        total[k] = total[2 * k] + total[2 * k + 1];
    }

    private void absorb(int k, int len, long d) {
        // The node total moves by the amount times the node length.
        total[k] += d * len;
        // The amount waits in pending for the children.
        pending[k] += d;
    }

    private void release(int k, int lo, int hi) {
        // Skip the work when nothing waits, so the children are already current.
        if (pending[k] == 0) return;
        int mid = (lo + hi) / 2;
        // Each child receives the amount scaled by its own length.
        absorb(2 * k, mid - lo, pending[k]);
        absorb(2 * k + 1, hi - mid, pending[k]);
        // Clearing the amount guarantees the transfer happens once.
        pending[k] = 0;
    }

    void add(int k, int lo, int hi, int l, int r, long d) {
        // A node outside the range changes nothing.
        if (r <= lo || hi <= l) return;
        // A node inside the range absorbs the amount and stops the descent.
        if (l <= lo && hi <= r) { absorb(k, hi - lo, d); return; }
        // A partial overlap needs current children before the recursion.
        release(k, lo, hi);
        int mid = (lo + hi) / 2;
        add(2 * k, lo, mid, l, r, d);
        add(2 * k + 1, mid, hi, l, r, d);
        // The node total must reflect the changed children.
        total[k] = total[2 * k] + total[2 * k + 1];
    }

    long sum(int k, int lo, int hi, int l, int r) {
        // A node outside the range contributes nothing.
        if (r <= lo || hi <= l) return 0;
        // A node inside the range contributes its stored total.
        if (l <= lo && hi <= r) return total[k];
        // A partial overlap releases its amount before reading the children.
        release(k, lo, hi);
        int mid = (lo + hi) / 2;
        return sum(2 * k, lo, mid, l, r) + sum(2 * k + 1, mid, hi, l, r);
    }

    /**
     * Processes the operations and returns the answers of the sum operations.
     * Time: O(n + q log n). Space: O(n).
     * Invariant: total[k] includes pending[k]; children lag by exactly pending[k].
     */
    static List<Long> solve(int[] a, int[][] ops) {
        // Build the structure once from the starting array.
        RangeAddRangeSum t = new RangeAddRangeSum(a);
        List<Long> out = new ArrayList<>();
        // Process the operations in order, each costing O(log n).
        for (int[] op : ops) {
            if (op[0] == 1) t.add(1, 0, t.n, op[1], op[2], op[3]);
            else out.add(t.sum(1, 0, t.n, op[1], op[2]));
        }
        return out;
    }

    /** Oracle: applies each operation directly to the array. */
    static List<Long> brute(int[] a, int[][] ops) {
        // Work on long copies so that sums cannot overflow.
        long[] b = new long[a.length];
        for (int i = 0; i < a.length; i++) b[i] = a[i];
        List<Long> out = new ArrayList<>();
        for (int[] op : ops) {
            long s = 0;
            for (int i = op[1]; i < op[2]; i++) {
                if (op[0] == 1) b[i] += op[3]; else s += b[i];
            }
            if (op[0] == 2) out.add(s);
        }
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 against the stated output.
        int[][] ops1 = {{2, 0, 5, 0}, {1, 1, 4, 10}, {2, 0, 3, 0}, {1, 0, 5, -2}, {2, 2, 5, 0}, {2, 3, 4, 0}};
        if (!solve(new int[]{3, 1, 4, 1, 5}, ops1).equals(List.of(14L, 28L, 24L, 9L))) throw new AssertionError("example 1");
        // Checks Example 2: a single element with extreme deltas.
        int[][] ops2 = {{1, 0, 1, -10_000}, {2, 0, 1, 0}, {1, 0, 1, 10_000}, {2, 0, 1, 0}};
        if (!solve(new int[]{7}, ops2).equals(List.of(-9_993L, 7L))) throw new AssertionError("example 2");
        // Compares with the brute force on random arrays and operation lists using a fixed seed.
        Random rnd = new Random(31_03_04);
        for (int t = 0; t < 400; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(41) - 20;
            int[][] ops = new int[1 + rnd.nextInt(15)][];
            for (int i = 0; i < ops.length; i++) {
                int l = rnd.nextInt(n), r = l + 1 + rnd.nextInt(n - l);
                ops[i] = rnd.nextBoolean() ? new int[]{1, l, r, rnd.nextInt(41) - 20} : new int[]{2, l, r, 0};
            }
            if (!solve(a, ops).equals(brute(a, ops))) throw new AssertionError("mismatch at trial " + t);
        }
    }
}
```
