<!-- solutions-for: 02-segment-trees -->
### Solutions For Segment Trees

#### Solution: [Build] Build Range Sums (Author exercise)
<!-- id: rq31-segment-build-sums -->

**Approach.** The recursion writes each node only after both children return.

A call receives a node number and the node range `lo` to `hi`. A leaf stores the array value at `lo`. Any other node splits at `mid = (lo + hi) / 2`, recurses into children `2k` and `2k + 1`, and then stores the total of their two stored values. The invariant is that a finished node holds the exact sum of its node range, so a parent can trust both children when it adds them.

For `[5, 2, 7, 1]`, the leaves 4 to 7 store 5, 2, 7 and 1. Node 2 stores 7, node 3 stores 8, and node 1 stores 15. The tree array has room for `4 * n` entries, and a node-existence flag selects only the created nodes, in increasing node number, for the result.

**Complexity.**

- **Time** is O(n), because the recursion creates 2n - 1 nodes and each does constant work.
- **Space** is O(n) for the tree array and O(log n) for the recursion stack.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class BuildRangeSums {
    /**
     * Builds the sum tree and returns the stored sums of created nodes in node order.
     * Time: O(n), because each of the 2n - 1 nodes is written once.
     * Space: O(n) for the arrays plus O(log n) recursion depth.
     * Invariant: after build(node, lo, hi) returns, tree[node] equals the sum of nums[lo..hi].
     */
    static long[] build(int[] nums) {
        // The 4n size keeps every node index of an uneven split inside the array.
        long[] tree = new long[4 * nums.length];
        // The flag array records which node numbers were created, because some numbers stay unused.
        boolean[] made = new boolean[4 * nums.length];
        // Start at the root, which owns every position.
        fill(nums, tree, made, 1, 0, nums.length - 1);
        // Count the created nodes so the result array has the exact length.
        int count = 0;
        // One pass over all node numbers collects the created ones in increasing order.
        for (boolean m : made) {
            // Only created nodes belong to the result.
            if (m) count++;
        }
        // The result array receives the stored sums.
        long[] out = new long[count];
        // The cursor tracks the next free result slot.
        int w = 0;
        // Walk node numbers in increasing order, which is the order the problem asks for.
        for (int k = 0; k < tree.length; k++) {
            // Skip numbers that no node uses.
            if (made[k]) out[w++] = tree[k];
        }
        // Return the sums of all created nodes.
        return out;
    }

    private static void fill(int[] a, long[] tree, boolean[] made, int node, int lo, int hi) {
        // Mark the node as created, because later code must skip unused numbers.
        made[node] = true;
        // A leaf owns one position, so it stores that value and needs no children.
        if (lo == hi) { tree[node] = a[lo]; return; }
        // Splitting at the midpoint gives the left half lo..mid and the right half mid+1..hi.
        int mid = (lo + hi) / 2;
        // Finish the left child first, so its sum exists when the parent adds.
        fill(a, tree, made, 2 * node, lo, mid);
        // Finish the right child, which completes the inputs of the parent.
        fill(a, tree, made, 2 * node + 1, mid + 1, hi);
        // The parent stores the sum of its two finished children.
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    /** Oracle: lists node ranges by an explicit work list and sums each range directly. */
    static long[] oracle(int[] nums) {
        // The list maps position k to the node range of node k, or null when unused.
        List<int[]> ranges = new ArrayList<>();
        // Reserve enough entries, all unused at first.
        for (int k = 0; k < 4 * nums.length; k++) ranges.add(null);
        // The root owns every position.
        ranges.set(1, new int[]{0, nums.length - 1});
        // Scan node numbers upward, so each parent is placed before its children.
        for (int k = 1; k < ranges.size() / 2; k++) {
            // Skip numbers that no node uses.
            if (ranges.get(k) == null) continue;
            int lo = ranges.get(k)[0], hi = ranges.get(k)[1];
            // A node with more than one position gets two children.
            if (lo < hi) {
                int mid = (lo + hi) / 2;
                ranges.set(2 * k, new int[]{lo, mid});
                ranges.set(2 * k + 1, new int[]{mid + 1, hi});
            }
        }
        // Collect direct range sums for the created nodes in node order.
        List<Long> sums = new ArrayList<>();
        for (int[] rg : ranges) {
            // Skip unused numbers.
            if (rg == null) continue;
            long s = 0;
            // Sum the range directly with no tree.
            for (int i = rg[0]; i <= rg[1]; i++) s += nums[i];
            sums.add(s);
        }
        // Convert the list to the array form.
        long[] out = new long[sums.size()];
        for (int i = 0; i < out.length; i++) out[i] = sums.get(i);
        // Return the oracle answer.
        return out;
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2 from the problem.
        if (!java.util.Arrays.equals(build(new int[]{5, 2, 7, 1}), new long[]{15, 7, 8, 5, 2, 7, 1})) throw new AssertionError("example 1");
        if (!java.util.Arrays.equals(build(new int[]{4, -1, 6}), new long[]{9, 3, 6, 4, -1})) throw new AssertionError("example 2");
        // Checks the smallest input of one value.
        if (!java.util.Arrays.equals(build(new int[]{9}), new long[]{9})) throw new AssertionError("single value");
        // Checks 500 random arrays against the oracle, with a fixed seed.
        Random rnd = new Random(31002);
        for (int t = 0; t < 500; t++) {
            int[] a = new int[1 + rnd.nextInt(40)];
            for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(2_000_001) - 1_000_000;
            int[] copy = a.clone();
            if (!java.util.Arrays.equals(build(a), oracle(a))) throw new AssertionError("random " + t);
            // The input array must stay unchanged.
            if (!java.util.Arrays.equals(a, copy)) throw new AssertionError("input mutated");
        }
    }
}
```

#### Solution: [Vary] Point Assignment (Author exercise)
<!-- id: rq31-segment-point-assign -->

**Approach.** An assignment changes one leaf, so only its ancestors can hold a stale sum.

The recursion descends toward the leaf that owns `pos`. It chooses the left child when `pos <= mid` and the right child otherwise. At the leaf it writes the new value. On the way back, each node on the path recomputes its sum from its two children, and the code counts each rewrite. Nodes off the path keep their node ranges and values, so they are never read for rewriting.

The invariant is that after the call returns, every node holds the sum of its node range under the new array. For five values, the path to position 4 has 3 nodes and the path to position 0 has 4, because the split of five positions is uneven.

**Complexity.**

- **Time** is O(log n) per assignment, because the path has one node per level.
- **Space** is O(n) for the tree and O(log n) for the recursion stack.

```java run
import java.util.Random;

public final class PointAssignment {
    private final long[] tree;
    private final int n;
    private int rewritten;

    /**
     * Builds the sum tree for the given array.
     * Time: O(n). Space: O(n).
     * Invariant: tree[node] equals the sum of the node range of node.
     */
    PointAssignment(int[] nums) {
        // Remember the length so every call starts from the root range.
        n = nums.length;
        // The 4n size covers every node number of an uneven split.
        tree = new long[4 * n];
        // Build from the root over positions 0..n-1.
        build(nums, 1, 0, n - 1);
    }

    private void build(int[] a, int node, int lo, int hi) {
        // A leaf stores one array value.
        if (lo == hi) { tree[node] = a[lo]; return; }
        // The midpoint splits the node range into two halves.
        int mid = (lo + hi) / 2;
        build(a, 2 * node, lo, mid);
        build(a, 2 * node + 1, mid + 1, hi);
        // The parent combines the finished children.
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    /**
     * Assigns one value and returns {rewritten nodes, root sum}.
     * Time: O(log n), because one node per level changes.
     * Space: O(log n) for the recursion stack.
     * Invariant: only nodes whose node range contains pos are rewritten.
     */
    long[] assign(int pos, int value) {
        // Reset the counter so each assignment reports its own rewrites.
        rewritten = 0;
        // Descend from the root toward the owner leaf of pos.
        walk(1, 0, n - 1, pos, value);
        // Return the count of rewrites and the new total of the whole array.
        return new long[]{rewritten, tree[1]};
    }

    private void walk(int node, int lo, int hi, int pos, int value) {
        // The leaf of pos receives the new value; this is one rewrite.
        if (lo == hi) { tree[node] = value; rewritten++; return; }
        int mid = (lo + hi) / 2;
        // Only the half that owns pos can contain the leaf, so the other half is skipped.
        if (pos <= mid) walk(2 * node, lo, mid, pos, value);
        else walk(2 * node + 1, mid + 1, hi, pos, value);
        // On the way back, the ancestor recomputes from its children; this is one rewrite.
        tree[node] = tree[2 * node] + tree[2 * node + 1];
        rewritten++;
    }

    public static void main(String[] args) {
        // Checks Example 1: two assignments on four values.
        PointAssignment p = new PointAssignment(new int[]{5, 2, 7, 1});
        if (!java.util.Arrays.equals(p.assign(2, 0), new long[]{3, 8})) throw new AssertionError("example 1a");
        if (!java.util.Arrays.equals(p.assign(0, 10), new long[]{3, 13})) throw new AssertionError("example 1b");
        // Checks Example 2: the unbalanced tree of five values has paths of length 3 and 4.
        PointAssignment q = new PointAssignment(new int[]{1, 1, 1, 1, 1});
        if (!java.util.Arrays.equals(q.assign(4, 6), new long[]{3, 10})) throw new AssertionError("example 2a");
        if (!java.util.Arrays.equals(q.assign(0, 0), new long[]{4, 9})) throw new AssertionError("example 2b");
        // Checks random sequences against a direct array and a depth count, with a fixed seed.
        Random rnd = new Random(31102);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(30);
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = rnd.nextInt(2001) - 1000;
            PointAssignment s = new PointAssignment(a);
            for (int step = 0; step < 20; step++) {
                int pos = rnd.nextInt(n), val = rnd.nextInt(2001) - 1000;
                a[pos] = val;
                long total = 0;
                for (int v : a) total += v;
                long[] got = s.assign(pos, val);
                // The oracle counts the nodes on the path by walking the ranges directly.
                int lo = 0, hi = n - 1, len = 1;
                while (lo < hi) {
                    int mid = (lo + hi) / 2;
                    if (pos <= mid) hi = mid; else lo = mid + 1;
                    len++;
                }
                if (got[1] != total || got[0] != len) throw new AssertionError("random " + t + " step " + step);
            }
        }
    }
}
```

#### Solution: [Boundary] No Overlap And Full Cover (Author exercise)
<!-- id: rq31-segment-no-overlap-full-cover -->

**Approach.** The check for no overlap runs first, then the check for full cover, then the split.

A node whose node range has `hi < l` or `lo > r` shares no position with the query, so it returns the identity and the code records its number. A node whose node range lies inside `l..r` returns its stored value, and the code records it as a full cover. Any other node overlaps in part, so it recurses into both children and records nothing itself.

Both stopping checks must run before the split, or the recursion would descend to every leaf. A non-empty node range cannot be both disjoint and inside the query, so the two stops never conflict. For `n = 5` and the query 1 to 1, nodes 8, 5 and 3 return the identity and node 9 is the only full cover.

**Complexity.**

- **Time** is O(log n) for the recursion, because at most two partial nodes exist per level and each has two children.
- **Space** is O(log n) for the stack plus the two output lists, which hold O(log n) nodes.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class NoOverlapFullCover {
    /**
     * Runs the query recursion and records full-cover and no-overlap node numbers.
     * Time: O(log n), because at most two nodes per level overlap in part.
     * Space: O(log n) for the stack and the recorded lists.
     * Invariant: a recorded node is a child of a node that overlaps the query in part.
     */
    static List<List<Integer>> classify(int n, int l, int r) {
        // Two lists collect the node numbers by outcome, in recursion order.
        List<Integer> full = new ArrayList<>(), none = new ArrayList<>();
        // Start at the root, which owns positions 0..n-1.
        visit(1, 0, n - 1, l, r, full, none);
        // Return the full-cover list first, then the no-overlap list.
        return List.of(full, none);
    }

    private static void visit(int node, int lo, int hi, int l, int r, List<Integer> full, List<Integer> none) {
        // No overlap comes first: the node range lies left or right of the query.
        if (r < lo || hi < l) { none.add(node); return; }
        // Full cover: every position of the node range is inside the query.
        if (l <= lo && hi <= r) { full.add(node); return; }
        // Partial overlap: split the node range and ask both children.
        int mid = (lo + hi) / 2;
        visit(2 * node, lo, mid, l, r, full, none);
        visit(2 * node + 1, mid + 1, hi, l, r, full, none);
    }

    /** Oracle: lists every node in pre-order, then filters by the definition with the parent's range. */
    static List<List<Integer>> oracle(int n, int l, int r) {
        // Collect all nodes with their ranges and parent numbers in pre-order.
        List<int[]> all = new ArrayList<>();
        collect(1, 0, n - 1, all);
        List<Integer> full = new ArrayList<>(), none = new ArrayList<>();
        for (int[] e : all) {
            // The root has no parent and the query is never empty, so it is never recorded alone.
            if (e[0] == 1) continue;
            // Look up the parent's range from the same list.
            int[] par = null;
            for (int[] f : all) if (f[0] == e[0] / 2) par = f;
            boolean parentInside = l <= par[1] && par[2] <= r;
            boolean parentOutside = r < par[1] || par[2] < l;
            // A recorded node needs a parent that overlaps in part.
            if (parentInside || parentOutside) continue;
            if (l <= e[1] && e[2] <= r) full.add(e[0]);
            else if (r < e[1] || e[2] < l) none.add(e[0]);
        }
        // The root itself is a full cover when the query spans every position.
        if (l == 0 && r == n - 1) full.add(1);
        return List.of(full, none);
    }

    private static void collect(int node, int lo, int hi, List<int[]> out) {
        // Record node number, lo and hi in pre-order.
        out.add(new int[]{node, lo, hi});
        // Leaves have no children.
        if (lo == hi) return;
        int mid = (lo + hi) / 2;
        collect(2 * node, lo, mid, out);
        collect(2 * node + 1, mid + 1, hi, out);
    }

    public static void main(String[] args) {
        // Checks Example 1 and Example 2.
        if (!classify(8, 2, 6).equals(List.of(List.of(5, 6, 14), List.of(4, 15)))) throw new AssertionError("example 1");
        if (!classify(5, 1, 1).equals(List.of(List.of(9), List.of(8, 5, 3)))) throw new AssertionError("example 2");
        // Checks a query that spans the whole array: the root is the only stop.
        if (!classify(5, 0, 4).equals(List.of(List.of(1), List.of()))) throw new AssertionError("whole array");
        // Checks every query for sizes 1 to 25 against the oracle.
        for (int n = 1; n <= 25; n++) {
            for (int l = 0; l < n; l++) {
                for (int r = l; r < n; r++) {
                    if (!classify(n, l, r).equals(oracle(n, l, r))) throw new AssertionError("n=" + n + " l=" + l + " r=" + r);
                }
            }
        }
        // Checks random larger sizes with a fixed seed.
        Random rnd = new Random(31202);
        for (int t = 0; t < 200; t++) {
            int n = 26 + rnd.nextInt(300);
            int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
            if (!classify(n, l, r).equals(oracle(n, l, r))) throw new AssertionError("large " + t);
        }
    }
}
```

#### Solution: [Recognize] Mutable Range Sum (LeetCode 307)
<!-- id: rq31-segment-mutable-sum -->

**Approach.** The recognition is that updates between queries rule out a fixed prefix-sum array, and sums need no inverse in a tree.

This solution stores the tree in a bottom-up layout. The leaf count `size` is the smallest power of two that is at least `n`. Leaf `i` lives at `size + i`, and node `k` has children `2k` and `2k + 1`, so node 1 is the root. An update writes the leaf and then halves the node number, recomputing each ancestor. A query over the half-open range `[left, right + 1)` moves two cursors up the tree. A cursor that is a right child contributes its node and steps inward, and a cursor that is a left child just moves to its parent.

The invariant is that every node stores the sum of the leaves below it. Padding leaves hold 0, which is the identity of addition, so they never change a sum.

**Complexity.**

- **Time** is O(n) to build and O(log n) per update and per query, because each walks one level per step.
- **Space** is O(n), because the array has 2 * size entries and size is under 2n.

```java run
import java.util.Random;

public final class NumArray {
    private final int size;
    private final long[] tree;

    /**
     * Builds the tree from the array.
     * Time: O(n). Space: O(n).
     * Invariant: tree[k] = tree[2k] + tree[2k+1] for every inner node k.
     */
    NumArray(int[] nums) {
        // Find the smallest power of two that holds every position.
        int s = 1;
        while (s < nums.length) s *= 2;
        size = s;
        // Leaves occupy size..2*size-1; padding leaves stay 0, the identity of addition.
        tree = new long[2 * size];
        // Copy the values into their leaves.
        for (int i = 0; i < nums.length; i++) tree[size + i] = nums[i];
        // Fill the inner nodes from the last to the first, so children come before parents.
        for (int k = size - 1; k >= 1; k--) tree[k] = tree[2 * k] + tree[2 * k + 1];
    }

    /**
     * Sets nums[index] to val.
     * Time: O(log n), one node per level. Space: O(1).
     * Invariant: after the loop, every ancestor of the leaf equals the sum of its children.
     */
    void update(int index, int val) {
        // Start at the leaf and write the new value.
        int k = size + index;
        tree[k] = val;
        // Move to the parent until the root is rewritten; this costs one step per level.
        for (k /= 2; k >= 1; k /= 2) {
            // Each ancestor recomputes from its two children.
            tree[k] = tree[2 * k] + tree[2 * k + 1];
        }
    }

    /**
     * Returns the sum of nums[left..right], both inclusive.
     * Time: O(log n), because each cursor climbs at most one level per step. Space: O(1).
     * Invariant: total plus the sum of leaves in [lo, hi) equals the answer.
     */
    long sumRange(int left, int right) {
        long total = 0;
        // Cursors cover the half-open leaf range [lo, hi).
        int lo = left + size, hi = right + 1 + size;
        // The loop ends when the cursors meet, which takes O(log n) steps.
        while (lo < hi) {
            // A right-child cursor is not covered by its parent's left side, so it adds itself.
            if ((lo & 1) == 1) total += tree[lo++];
            // A right-end cursor that is odd points past a right child, so the node before it is added.
            if ((hi & 1) == 1) total += tree[--hi];
            // Both cursors move to their parents, one level up.
            lo /= 2;
            hi /= 2;
        }
        // Return the accumulated sum.
        return total;
    }

    public static void main(String[] args) {
        // Checks Example 1: the three results 4, 8 and 15.
        NumArray a = new NumArray(new int[]{3, -2, 5, 1, 4});
        if (a.sumRange(1, 3) != 4) throw new AssertionError("example 1a");
        a.update(2, 9);
        if (a.sumRange(1, 3) != 8) throw new AssertionError("example 1b");
        if (a.sumRange(0, 4) != 15) throw new AssertionError("example 1c");
        // Checks Example 2: a single value, updated.
        NumArray b = new NumArray(new int[]{7});
        if (b.sumRange(0, 0) != 7) throw new AssertionError("example 2a");
        b.update(0, -3);
        if (b.sumRange(0, 0) != -3) throw new AssertionError("example 2b");
        // Checks random mixed calls against a direct array, with a fixed seed.
        Random rnd = new Random(31302);
        for (int t = 0; t < 300; t++) {
            int n = 1 + rnd.nextInt(40);
            int[] ref = new int[n];
            for (int i = 0; i < n; i++) ref[i] = rnd.nextInt(201) - 100;
            NumArray s = new NumArray(ref.clone());
            for (int step = 0; step < 60; step++) {
                if (rnd.nextBoolean()) {
                    int idx = rnd.nextInt(n), v = rnd.nextInt(201) - 100;
                    ref[idx] = v;
                    s.update(idx, v);
                } else {
                    int l = rnd.nextInt(n), r = l + rnd.nextInt(n - l);
                    long want = 0;
                    for (int i = l; i <= r; i++) want += ref[i];
                    if (s.sumRange(l, r) != want) throw new AssertionError("random " + t + " step " + step);
                }
            }
        }
    }
}
```
