<!-- solutions-for: 05-kth-and-range-queries -->
### Solutions For Rank And Range Questions

#### Solution: [Build] First K Inorder Values (Author exercise)
<!-- id: tb-kth-first-k -->

**Approach.**
The method runs an iterative inorder walk with an `ArrayDeque` used as a stack. The inner loop pushes the left spine of the current node, so the top of the stack always holds the smallest unread key. The method pops the top, appends its key to the answer, and moves to the right child of the popped node. The outer loop condition includes the size of the answer, so the loop ends as soon as `k` keys are collected. A tree with fewer than `k` keys empties the stack first, and the loop ends with every key collected.

The invariant is that the answer holds the smallest keys in sorted order, and the stack top is the next one. Stopping at `k` leaves the rest of the tree unread.

**Complexity.**
- **Time** is O(h + k), because the walk pushes at most `h` nodes before the first read and then spends constant work per key.
- **Space** is O(h) for the stack, plus O(k) for the answer.

```java run
import java.util.*;

public final class FirstK {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the first k keys in sorted order.
     * Time: O(h + k), because the walk stops after k reads.
     * Space: O(h) for the stack, plus the answer.
     * Invariant: the stack top is the smallest key not yet read.
     */
    static List<Integer> firstK(TreeNode root, int k) {
        List<Integer> out = new ArrayList<>();
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        // The walk ends when k keys are read or the whole tree is read.
        while (out.size() < k && (node != null || !stack.isEmpty())) {
            while (node != null) { stack.push(node); node = node.left; }   // push the left spine
            node = stack.pop();                                            // smallest unread key
            out.add(node.val);
            node = node.right;                                             // its right subtree comes next
        }
        return out;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(6);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        // Example 1: the first three keys.
        if (!firstK(r, 3).equals(List.of(2, 3, 4))) throw new AssertionError("ex1");
        // Example 2: k = 0 reads nothing.
        if (!firstK(r, 0).isEmpty()) throw new AssertionError("ex2");
        // A k larger than the tree returns every key.
        if (!firstK(r, 10).equals(List.of(2, 3, 4, 5, 6))) throw new AssertionError("large k");
        // Random trees must match a prefix of the full inorder list.
        Random rnd = new Random(1641);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            for (int k = 0; k <= all.size() + 2; k++)
                if (!firstK(x, k).equals(all.subList(0, Math.min(k, all.size())))) throw new AssertionError("t=" + t + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Kth Smallest Element in a BST (LeetCode 230)
<!-- id: tb-kth-smallest -->

**Approach.**
The method uses the same stack walk and returns instead of collecting. A counter starts at `k` and drops by one at every pop. When the counter reaches zero, the popped node holds the kth smallest key, and the method returns its value at once. The contract guarantees `1 <= k <= n`, so the walk always finds the key. Nothing to the right of the answer is read, so a small `k` reads only the left edge of the tree.

The invariant is that the number of keys already popped equals the number of keys smaller than the stack top. The kth pop therefore has exactly `k - 1` smaller keys.

**Complexity.**
- **Time** is O(h + k), because the walk reads `k` keys after pushing at most `h` nodes.
- **Space** is O(h) for the stack.

```java run
import java.util.*;

public final class KthSmallest {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the kth smallest key, with rank 1 for the minimum.
     * Time: O(h + k), because k keys are read.
     * Space: O(h) for the stack.
     * Invariant: popped keys equal the keys smaller than the stack top.
     */
    static int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }   // push the left spine
            node = stack.pop();                                            // the next key in sorted order
            if (--k == 0) return node.val;                                 // the kth pop is the answer
            node = node.right;
        }
        throw new IllegalArgumentException("k exceeds the node count");
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    public static void main(String[] args) {
        // Example 1: the minimum of 3, 1, 4, 2.
        TreeNode a = new TreeNode(3);
        a.left = new TreeNode(1);
        a.right = new TreeNode(4);
        a.left.right = new TreeNode(2);
        if (kthSmallest(a, 1) != 1) throw new AssertionError("ex1");
        // Example 2: the third key of 1 to 6.
        TreeNode b = new TreeNode(5);
        b.left = new TreeNode(3);
        b.right = new TreeNode(6);
        b.left.left = new TreeNode(2);
        b.left.right = new TreeNode(4);
        b.left.left.left = new TreeNode(1);
        if (kthSmallest(b, 3) != 3) throw new AssertionError("ex2");
        // Java claim: the walk throws instead of returning a wrong key when k is too large.
        boolean threw = false;
        try { kthSmallest(b, 7); } catch (IllegalArgumentException e) { threw = true; }
        if (!threw) throw new AssertionError("out of range");
        // Random trees must match the sorted list at every rank.
        Random rnd = new Random(1642);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            for (int k = 1; k <= all.size(); k++)
                if (kthSmallest(x, k) != all.get(k - 1)) throw new AssertionError("t=" + t + " k=" + k);
        }
    }
}
```

#### Solution: [Boundary] K At Either End (Author exercise)
<!-- id: tb-kth-both-ends -->

**Approach.**
The method runs two walks that mirror each other. The first walk is the ordinary stack walk with the left spine pushed first, and its kth pop is the kth smallest key. The second walk swaps the roles of left and right: it pushes the right spine first, so the top of the stack always holds the largest unread key, and its kth pop is the kth largest key. A helper takes a flag that selects the direction, so the two walks share one body. The smallest valid rank 1 returns the minimum and the maximum, and the largest valid rank `n` returns the maximum and the minimum, because the kth largest equals the (n + 1 - k)th smallest.

The invariant of each walk is that the number of popped keys equals the number of keys on its side of the stack top.

**Complexity.**
- **Time** is O(h + k) per walk, which is O(h + k) in total.
- **Space** is O(h) for the stack of each walk.

```java run
import java.util.*;

public final class BothEnds {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /** Reads the kth key from the small end when ascending is true, otherwise from the large end. */
    static int kth(TreeNode root, int k, boolean ascending) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = ascending ? node.left : node.right; }   // the spine on the walk's near side
            node = stack.pop();
            if (--k == 0) return node.val;
            node = ascending ? node.right : node.left;                                              // the far side comes next
        }
        throw new IllegalArgumentException("k exceeds the node count");
    }

    /**
     * Returns {kth smallest, kth largest}.
     * Time: O(h + k) per walk.
     * Space: O(h) for each stack.
     * Invariant: the stack top is the smallest (or largest) unread key.
     */
    static int[] bothEnds(TreeNode root, int k) {
        return new int[] {kth(root, k, true), kth(root, k, false)};
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(6);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        // Example 1: rank 1 gives the minimum and the maximum.
        if (!Arrays.equals(bothEnds(r, 1), new int[] {2, 6})) throw new AssertionError("ex1");
        // Example 2: rank n gives the maximum and the minimum.
        if (!Arrays.equals(bothEnds(r, 5), new int[] {6, 2})) throw new AssertionError("ex2");
        // A single node answers itself from both ends.
        if (!Arrays.equals(bothEnds(new TreeNode(7), 1), new int[] {7, 7})) throw new AssertionError("single");
        // Random trees must match the sorted list from both ends at every rank.
        Random rnd = new Random(1643);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            int n = all.size();
            for (int k = 1; k <= n; k++) {
                int[] want = {all.get(k - 1), all.get(n - k)};
                if (!Arrays.equals(bothEnds(x, k), want)) throw new AssertionError("t=" + t + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Range Sum of BST (LeetCode 938)
<!-- id: tb-range-sum -->

**Approach.**
The method recurses from the root and uses the order of the keys to skip subtrees. A node below `low` sends the recursion to the right child only, because the node and every key in its left subtree are smaller than `low`. A node above `high` sends the recursion to the left child only, because the node and every key in its right subtree are larger than `high`. A node inside the range adds its key and recurses on both children, since keys inside the range can sit on either side. Each skipped subtree is pruned after one comparison, so the visits stay on the in-range nodes and the two paths that border the range.

The invariant is that a subtree skipped by a comparison holds no key in the closed range. The recursion therefore sums exactly the in-range keys.

**Complexity.**
- **Time** is O(h + m), where `m` is the number of keys in the range, because only in-range nodes and the border paths are visited.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class RangeSum {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the sum of keys in the closed range [low, high].
     * Time: O(h + m), where m is the number of keys in the range.
     * Space: O(h) for the recursion stack.
     * Invariant: a skipped subtree holds no key in the range.
     */
    static int rangeSumBST(TreeNode node, int low, int high) {
        if (node == null) return 0;
        if (node.val < low) return rangeSumBST(node.right, low, high);     // node and its left subtree are too small
        if (node.val > high) return rangeSumBST(node.left, low, high);     // node and its right subtree are too large
        // The key is inside the range, so keys inside the range may lie on both sides.
        return node.val + rangeSumBST(node.left, low, high) + rangeSumBST(node.right, low, high);
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    public static void main(String[] args) {
        // Example 1: the keys 7, 10 and 15 sum to 32.
        TreeNode a = new TreeNode(10);
        a.left = new TreeNode(5);
        a.right = new TreeNode(15);
        a.left.left = new TreeNode(3);
        a.left.right = new TreeNode(7);
        a.right.right = new TreeNode(18);
        if (rangeSumBST(a, 7, 15) != 32) throw new AssertionError("ex1");
        // Example 2: the keys 6, 7 and 10 sum to 23.
        a.left.left.left = new TreeNode(1);
        a.left.right.left = new TreeNode(6);
        if (rangeSumBST(a, 6, 10) != 23) throw new AssertionError("ex2");
        // Random trees must match a scan of the sorted list for many ranges.
        Random rnd = new Random(1644);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            for (int low = 0; low < 40; low += 3)
                for (int high = low; high < 42; high += 4) {
                    int want = 0;
                    for (int v : all) if (v >= low && v <= high) want += v;
                    if (rangeSumBST(x, low, high) != want) throw new AssertionError("t=" + t + " " + low + ".." + high);
                }
        }
    }
}
```
