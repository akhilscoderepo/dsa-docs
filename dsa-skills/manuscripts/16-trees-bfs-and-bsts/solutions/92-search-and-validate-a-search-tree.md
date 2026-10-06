<!-- solutions-for: 92-search-and-validate-a-search-tree -->
### Solutions For Search With Limits

#### Solution: [Build] Depth Of A Key In A Search Tree (LeetCode 700)
<!-- id: tbc-key-depth -->

**Approach.**
The method walks down from the root with one reference and a depth counter that starts at 1. Each step compares the key with the key of the current node. A match returns the current depth. A smaller key moves to the left child and a larger key moves to the right child, and each move increases the counter by one. The branch that the walk leaves holds no key equal to the target, because all of its keys lie on the other side of the node. When the reference becomes `null`, the walk has reached an empty slot, and the method returns 0.

The invariant is that the key, if present, lies in the subtree of the current node, and the counter equals the depth of that node.

**Complexity.**
- **Time** is O(h), because each step moves one level down.
- **Space** is O(1), because the loop keeps one reference and one counter.

```java run
import java.util.*;

public final class KeyDepth {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the depth of the node holding key, with the root at depth 1, or 0 if absent.
     * Time: O(h), because each step moves one level down.
     * Space: O(1).
     * Invariant: the key, if present, lies in the subtree of node, and depth is the depth of node.
     */
    static int depthOf(TreeNode root, int key) {
        int depth = 1;
        TreeNode node = root;
        while (node != null) {
            if (node.val == key) return depth;               // found at this depth
            node = key < node.val ? node.left : node.right;  // one branch per comparison
            depth++;                                         // the next node lies one level lower
        }
        return 0;                                            // an empty slot means the key is absent
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    /** Oracle: breadth-first scan that reports the level of the first node with the key. */
    static int oracle(TreeNode root, int key) {
        if (root == null) return 0;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        int level = 0;
        while (!queue.isEmpty()) {
            level++;
            for (int i = queue.size(); i > 0; i--) {
                TreeNode n = queue.poll();
                if (n.val == key) return level;
                if (n.left != null) queue.add(n.left);
                if (n.right != null) queue.add(n.right);
            }
        }
        return 0;
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(20);
        r.left = new TreeNode(10);
        r.right = new TreeNode(30);
        r.left.left = new TreeNode(5);
        r.left.right = new TreeNode(15);
        r.right.left = new TreeNode(25);
        r.right.right = new TreeNode(40);
        // Example 1: the key 15 sits at depth 3.
        if (depthOf(r, 15) != 3) throw new AssertionError("ex1");
        // Example 2: the key 17 is absent.
        if (depthOf(r, 17) != 0) throw new AssertionError("ex2");
        if (depthOf(null, 1) != 0 || depthOf(r, 20) != 1) throw new AssertionError("edges");
        // Random trees must match the breadth-first oracle for present and absent keys.
        Random rnd = new Random(1692);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(30); i++) x = insert(x, rnd.nextInt(60));
            for (int k = -1; k <= 61; k++)
                if (depthOf(x, k) != oracle(x, k)) throw new AssertionError("t=" + t + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Validate A Subtree Against Outer Limits (LeetCode 98)
<!-- id: tbc-validate-limits -->

**Approach.**
The method starts the recursion with the limits from the caller and not with unbounded limits. The limits are stored as `long`, so the comparisons stay exact when `low` or `high` is `Integer.MIN_VALUE` or `Integer.MAX_VALUE`. A node is accepted when its key lies strictly between the current limits. The left call narrows the upper limit to the node key, and the right call narrows the lower limit to the node key, so each limit is always the strictest one on the path. The caller's limits are therefore the starting slot interval, and every key in the subtree must also lie inside it.

The invariant is that each call holds the slot interval of its node, which is the intersection of the caller's interval with the turns on the path.

**Complexity.**
- **Time** is O(n), because each node is visited at most once.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class ValidateWithLimits {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns true when the tree is a valid search tree with every key strictly between low and high.
     * Time: O(n), because each node is visited at most once.
     * Space: O(h) for the recursion stack.
     * Invariant: each call holds the slot interval of its node.
     */
    static boolean validBetween(TreeNode root, int low, int high) {
        return check(root, low, high);                       // the caller's limits start the recursion
    }

    private static boolean check(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val <= low || node.val >= high) return false;
        return check(node.left, low, node.val) && check(node.right, node.val, high);
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    /** Oracle: inorder keys must increase strictly and lie inside the limits. */
    static boolean oracle(TreeNode root, int low, int high) {
        List<Integer> keys = new ArrayList<>();
        inorder(root, keys);
        for (int i = 0; i < keys.size(); i++) {
            if (keys.get(i) <= low || keys.get(i) >= high) return false;
            if (i > 0 && keys.get(i - 1) >= keys.get(i)) return false;
        }
        return true;
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(12)));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(12));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(10);
        r.left = new TreeNode(5);
        r.right = new TreeNode(15);
        // Example 1: all keys lie in (0, 20).
        if (!validBetween(r, 0, 20)) throw new AssertionError("ex1");
        // Example 2: the key 5 is not above the lower limit 5.
        if (validBetween(r, 5, 20)) throw new AssertionError("ex2");
        // The extreme limits accept the extreme keys.
        TreeNode e = new TreeNode(0);
        e.left = new TreeNode(Integer.MIN_VALUE + 1);
        e.right = new TreeNode(Integer.MAX_VALUE - 1);
        if (!validBetween(e, Integer.MIN_VALUE, Integer.MAX_VALUE) || !validBetween(null, 0, 1)) throw new AssertionError("extremes");
        // Random shapes and built trees, with several limit pairs, must match the oracle.
        Random rnd = new Random(1693);
        for (int t = 0; t < 400; t++) {
            TreeNode x = rnd.nextBoolean() ? randomTree(rnd, rnd.nextInt(12)) : null;
            if (x == null) for (int i = 0; i < rnd.nextInt(12); i++) x = insert(x, rnd.nextInt(12));
            int low = rnd.nextInt(14) - 2, high = low + 1 + rnd.nextInt(12);
            if (validBetween(x, low, high) != oracle(x, low, high)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Kth Largest Element In A BST (LeetCode 230)
<!-- id: tbc-kth-largest -->

**Approach.**
The method mirrors the stack walk of the kth smallest query. The inner loop pushes the right spine, so the top of the stack always holds the largest key not yet read. A counter starts at `k`, and each pop reduces it by one. When it reaches zero, the popped node holds the kth largest key, and the method returns it. After a pop the walk moves to the left child of the popped node, because the keys of that subtree are the next smaller keys. The method uses no numeric interval, since the answer depends only on the position in sorted order.

The invariant is that the popped keys are exactly the largest keys in decreasing order, and the stack top is the largest key not yet read.

**Complexity.**
- **Time** is O(h + k), because the walk pushes at most `h` nodes before the first read and then reads `k` keys.
- **Space** is O(h) for the stack.

```java run
import java.util.*;

public final class KthLargest {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the kth largest key, with rank 1 for the maximum.
     * Time: O(h + k), because k keys are read.
     * Space: O(h) for the stack.
     * Invariant: popped keys are the largest keys in decreasing order.
     */
    static int kthLargest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.right; }   // push the right spine
            node = stack.pop();                                             // the largest unread key
            if (--k == 0) return node.val;
            node = node.left;                                               // smaller keys come next
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
        TreeNode r = new TreeNode(20);
        r.left = new TreeNode(10);
        r.right = new TreeNode(30);
        r.left.left = new TreeNode(5);
        r.left.right = new TreeNode(15);
        r.right.left = new TreeNode(25);
        r.right.right = new TreeNode(40);
        // Example 1: the largest key.
        if (kthLargest(r, 1) != 40) throw new AssertionError("ex1");
        // Example 2: the third largest key.
        if (kthLargest(r, 3) != 25) throw new AssertionError("ex2");
        // The smallest key is the nth largest.
        if (kthLargest(r, 7) != 5) throw new AssertionError("min");
        // Random trees must match the descending sorted list at every rank.
        Random rnd = new Random(1694);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(30); i++) x = insert(x, rnd.nextInt(60));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            for (int k = 1; k <= all.size(); k++)
                if (kthLargest(x, k) != all.get(all.size() - k)) throw new AssertionError("t=" + t + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Delete A Node With Predecessor Replacement (LeetCode 450)
<!-- id: tbc-delete-predecessor -->

**Approach.**
The method descends by the key and rewrites the child reference that points at the removed node. When the node lacks a left child, its right child takes its place, and when it lacks a right child, its left child takes its place. Together these two rules cover leaves and nodes with one child. A node with two children takes the largest key of its left subtree, which is the rightmost node there. That key is smaller than every key on the right and larger than every other key on the left, so it lies inside the slot interval of the removed node. The method then deletes the rightmost node from the left subtree, and that node has no right child, so the one-child rule applies to it.

The invariant is that the sorted order of the keys equals the old order without the removed key, and every key stays inside its slot interval.

**Complexity.**
- **Time** is O(h), because one search path and one rightmost walk are followed.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class DeleteByPredecessor {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Removes key and returns the new root of the subtree.
     * Time: O(h), because one search path and one rightmost walk are followed.
     * Space: O(h) for the recursion stack.
     * Invariant: the keys in sorted order equal the old keys without key.
     */
    static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;
        if (key < root.val) { root.left = deleteNode(root.left, key); return root; }
        if (key > root.val) { root.right = deleteNode(root.right, key); return root; }
        if (root.left == null) return root.right;                 // leaf or only a right child
        if (root.right == null) return root.left;                 // only a left child
        TreeNode largest = root.left;
        while (largest.right != null) largest = largest.right;    // the rightmost node of the left subtree
        root.val = largest.val;                                   // this key fits the slot interval of root
        root.left = deleteNode(root.left, largest.val);           // remove the original, which has no right child
        return root;
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

    static boolean valid(TreeNode n, long lo, long hi) {
        return n == null || (n.val > lo && n.val < hi && valid(n.left, lo, n.val) && valid(n.right, n.val, hi));
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(20);
        r.left = new TreeNode(10);
        r.right = new TreeNode(30);
        r.left.left = new TreeNode(5);
        r.left.right = new TreeNode(15);
        r.right.left = new TreeNode(25);
        r.right.right = new TreeNode(40);
        // Example 1: deleting the root copies 15 up and leaves 10 with only the child 5.
        TreeNode a = deleteNode(r, 20);
        if (a.val != 15 || a.left.val != 10 || a.left.left.val != 5 || a.left.right != null || a.right.val != 30) throw new AssertionError("ex1");
        // Example 2: deleting the leaf 5 leaves 10 with only the child 15.
        TreeNode b = new TreeNode(20);
        b.left = new TreeNode(10);
        b.right = new TreeNode(30);
        b.left.left = new TreeNode(5);
        b.left.right = new TreeNode(15);
        b = deleteNode(b, 5);
        if (b.left.left != null || b.left.right.val != 15) throw new AssertionError("ex2");
        if (deleteNode(new TreeNode(1), 1) != null) throw new AssertionError("single");
        // Random trees: any key, present or absent, must leave a valid tree with exactly that key removed.
        Random rnd = new Random(1695);
        for (int t = 0; t < 400; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(30));
            int key = rnd.nextInt(32) - 1;
            List<Integer> want = new ArrayList<>();
            inorder(x, want);
            want.remove((Integer) key);
            x = deleteNode(x, key);
            List<Integer> got = new ArrayList<>();
            inorder(x, got);
            if (!got.equals(want) || !valid(x, Long.MIN_VALUE, Long.MAX_VALUE)) throw new AssertionError("random " + t);
        }
    }
}
```
