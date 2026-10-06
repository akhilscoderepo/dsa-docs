<!-- solutions-for: 04-successor-and-predecessor -->
### Solutions For Next And Previous Keys

#### Solution: [Build] Minimum Of Right Subtree (Author exercise)
<!-- id: tb-succ-right-min -->

**Approach.**
The method moves to the right child of the given node, since every key in the right subtree is larger than the node. It then follows left links while the current node has a left child. A node with no left child holds the smallest key of that subtree, because any smaller key would have to sit in its left subtree. The loop stops there and returns that node.

The invariant is that the smallest key of the right subtree lies in the subtree of the current node. Moving left keeps it true, and the missing left child proves the current node is the minimum.

**Complexity.**
- **Time** is O(h), because the walk follows at most one path down.
- **Space** is O(1), because the loop keeps one reference.

```java run
import java.util.*;

public final class RightMin {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the node with the smallest key under p.right.
     * Time: O(h), because the walk follows one path.
     * Space: O(1).
     * Invariant: the minimum of the right subtree lies in the subtree of node.
     */
    static TreeNode rightMin(TreeNode p) {
        TreeNode node = p.right;                       // every key here is larger than p
        while (node.left != null) node = node.left;    // a smaller key can only sit on the left
        return node;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void collect(TreeNode n, List<TreeNode> out) {
        if (n == null) return;
        collect(n.left, out);
        out.add(n);
        collect(n.right, out);
    }

    static TreeNode example() {
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(8);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        r.right.left = new TreeNode(6);
        r.right.right = new TreeNode(9);
        r.right.left.right = new TreeNode(7);
        return r;
    }

    public static void main(String[] args) {
        // Example 1: the right subtree of 5 has the minimum 6.
        TreeNode r = example();
        if (rightMin(r).val != 6) throw new AssertionError("ex1");
        // Example 2: the right subtree of 3 is the single node 4.
        if (rightMin(r.left).val != 4) throw new AssertionError("ex2");
        // Random trees: the result must be the first node after p in sorted order, for every p with a right child.
        Random rnd = new Random(1631);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 2 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(50));
            List<TreeNode> sorted = new ArrayList<>();
            collect(x, sorted);
            for (int i = 0; i < sorted.size(); i++)
                if (sorted.get(i).right != null && rightMin(sorted.get(i)) != sorted.get(i + 1)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Successor Without Parent Links (Author exercise)
<!-- id: tb-succ-no-parent -->

**Approach.**
The method walks from the root and keeps `best`, the last node larger than the key. A node larger than the key becomes `best`, and the walk goes left to look for a smaller node that still beats the key. A node not larger than the key is skipped together with its left subtree, because every key there is at most the node key, and the walk goes right. Each new `best` is smaller than the previous one, since the walk only moves below a recorded node on its left side. When the walk reaches `null`, no node can improve `best`, and the method returns its key or `null`.

The invariant is that the successor is either `best` or a node inside the subtree of the current node. The check `node.val > key` is strict, so a key equal to the target is never its own successor.

**Complexity.**
- **Time** is O(h), because each step moves one level down.
- **Space** is O(1), because the method stores two references.

```java run
import java.util.*;

public final class SuccessorByKey {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the smallest key greater than key, or null.
     * Time: O(h), because each step moves one level down.
     * Space: O(1).
     * Invariant: the answer is best or lies in the subtree of node.
     */
    static Integer successor(TreeNode root, int key) {
        TreeNode best = null;
        TreeNode node = root;
        while (node != null) {
            if (node.val > key) { best = node; node = node.left; }   // larger: record it, then look for a smaller one
            else node = node.right;                                   // too small: skip it and its left side
        }
        return best == null ? null : best.val;
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
        r.right = new TreeNode(8);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        r.right.left = new TreeNode(6);
        r.right.right = new TreeNode(9);
        r.right.left.right = new TreeNode(7);
        // Example 1: 7 is followed by 8 two levels up.
        if (successor(r, 7) != 8) throw new AssertionError("ex1");
        // Example 2: 1 is below every key, so the minimum 2 follows.
        if (successor(r, 1) != 2) throw new AssertionError("ex2");
        if (successor(null, 0) != null) throw new AssertionError("empty");
        // Random trees: every key in range, present or absent, must match the sorted-list scan.
        Random rnd = new Random(1632);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> keys = new ArrayList<>();
            inorder(x, keys);
            for (int k = -2; k <= 42; k++) {
                Integer want = null;
                for (int v : keys) if (v > k) { want = v; break; }
                Integer got = successor(x, k);
                if (!Objects.equals(got, want)) throw new AssertionError("t=" + t + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Boundary] Maximum And Minimum Keys (Author exercise)
<!-- id: tb-succ-extremes -->

**Approach.**
Two loops run from the root, one for each neighbor, and each is the mirror of the other. The successor loop records a node larger than the key and goes left, and it goes right otherwise. The predecessor loop records a node smaller than the key and goes right, and it goes left otherwise. A candidate that was never set stays `null`, and the method reports `null` for that side. The smallest key sees no node smaller than itself, so its predecessor loop never records a candidate, and the largest key behaves the same way on the successor side.

The invariant of each loop is that the neighbor is either the recorded candidate or inside the subtree of the current node. The strict comparisons exclude the key itself.

**Complexity.**
- **Time** is O(h), because each loop takes one path down.
- **Space** is O(1), because the loops keep a few references.

```java run
import java.util.*;

public final class NeighborPair {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns {predecessor, successor} of key, using null for a missing neighbor.
     * Time: O(h), because each loop follows one path.
     * Space: O(1).
     * Invariant: each neighbor is the candidate or lies in the subtree of node.
     */
    static Integer[] neighbors(TreeNode root, int key) {
        TreeNode pred = null, succ = null;
        for (TreeNode node = root; node != null; ) {
            if (node.val > key) { succ = node; node = node.left; }    // larger node: a successor candidate
            else node = node.right;
        }
        for (TreeNode node = root; node != null; ) {
            if (node.val < key) { pred = node; node = node.right; }   // smaller node: a predecessor candidate
            else node = node.left;
        }
        return new Integer[] {pred == null ? null : pred.val, succ == null ? null : succ.val};
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
        r.right = new TreeNode(8);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        r.right.left = new TreeNode(6);
        r.right.right = new TreeNode(9);
        r.right.left.right = new TreeNode(7);
        // Example 1: the minimum has no predecessor.
        if (!Arrays.equals(neighbors(r, 2), new Integer[] {null, 3})) throw new AssertionError("ex1");
        // Example 2: the maximum has no successor.
        if (!Arrays.equals(neighbors(r, 9), new Integer[] {8, null})) throw new AssertionError("ex2");
        // The empty tree has neither neighbor.
        if (!Arrays.equals(neighbors(null, 0), new Integer[] {null, null})) throw new AssertionError("empty");
        // Random trees: every probe must match a scan of the sorted keys.
        Random rnd = new Random(1633);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            List<Integer> keys = new ArrayList<>();
            inorder(x, keys);
            for (int k = -2; k <= 42; k++) {
                Integer p = null, s = null;
                for (int v : keys) { if (v < k) p = v; if (v > k && s == null) s = v; }
                if (!Arrays.equals(neighbors(x, k), new Integer[] {p, s})) throw new AssertionError("t=" + t + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Recognize] Inorder Successor in BST (LeetCode 285)
<!-- id: tb-succ-inorder -->

**Approach.**
The method descends from the root by the key of `p` and records the last node larger than that key. When the node `p` has a right subtree, the descent reaches `p`, turns right, and then turns left at every node, because each node there is larger than the key. The last recorded node is then the leftmost node of the right subtree. When `p` has no right subtree, the descent ends below `p`, and the last recorded node is the nearest ancestor where the path turned left. A single loop covers both cases, and the answer is `null` when no node larger than the key was seen.

The invariant is the same as in the key-based successor: the answer is the recorded node or lies below the current node. Distinct keys make comparison by value safe, because the node `p` is the only node that holds its key.

**Complexity.**
- **Time** is O(h), because the descent crosses one level per step.
- **Space** is O(1), because the loop keeps two references.

```java run
import java.util.*;

public final class InorderSuccessor {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the node after p in sorted order, or null.
     * Time: O(h), because the descent crosses one level per step.
     * Space: O(1).
     * Invariant: the answer is best or lies in the subtree of node.
     */
    static TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        TreeNode best = null;
        TreeNode node = root;
        while (node != null) {
            if (node.val > p.val) { best = node; node = node.left; }   // covers both the subtree case and the ancestor case
            else node = node.right;
        }
        return best;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void collect(TreeNode n, List<TreeNode> out) {
        if (n == null) return;
        collect(n.left, out);
        out.add(n);
        collect(n.right, out);
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(8);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        r.right.left = new TreeNode(6);
        r.right.right = new TreeNode(9);
        r.right.left.right = new TreeNode(7);
        // Example 1: the node 4 has no right subtree, so the ancestor 5 follows.
        if (inorderSuccessor(r, r.left.right) != r) throw new AssertionError("ex1");
        // Example 2: the largest key has no successor.
        if (inorderSuccessor(r, r.right.right) != null) throw new AssertionError("ex2");
        // The right-subtree case: the successor of 5 is the leftmost node under 8.
        if (inorderSuccessor(r, r) != r.right.left) throw new AssertionError("subtree");
        // Random trees: every node must map to the next node of the sorted node list.
        Random rnd = new Random(1634);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(50));
            List<TreeNode> sorted = new ArrayList<>();
            collect(x, sorted);
            for (int i = 0; i < sorted.size(); i++) {
                TreeNode want = i + 1 < sorted.size() ? sorted.get(i + 1) : null;
                if (inorderSuccessor(x, sorted.get(i)) != want) throw new AssertionError("t=" + t + " i=" + i);
            }
        }
    }
}
```
