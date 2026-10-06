<!-- solutions-for: 09-balanced-tree-concepts -->
### Solutions For Balanced Trees

#### Solution: [Build] Compare Search Heights (Author exercise)
<!-- id: tb-bal-heights -->

**Approach.**
The method inserts the keys one at a time into a plain tree with the one-path insert, so each key walks down from the root and attaches as a new leaf. No node ever moves. After the last insert it computes the height with a recursion that returns 0 for an empty slot and one more than the larger child height otherwise. The height depends on the arrival order, because each key lands below the nodes that arrived earlier. A sorted array makes every key the right child of the previous key, which gives a height equal to the length.

The invariant is that each key sits below exactly the earlier keys it was compared with on its way down. The height is therefore the longest chain of such comparisons plus one.

**Complexity.**
- **Time** is O(n * h) for the inserts, which is O(n^2) on a sorted input, plus O(n) for the height.
- **Space** is O(n) for the nodes, plus O(h) for the recursion.

```java run
import java.util.*;

public final class SearchHeights {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the height of the plain tree built by inserting keys in order.
     * Time: O(n * h) for the inserts, plus O(n) for the height.
     * Space: O(n) for the nodes, plus O(h) for the recursion.
     * Invariant: each key sits below exactly the earlier keys it was compared with.
     */
    static int heightAfterInserts(int[] keys) {
        TreeNode root = null;
        for (int key : keys) root = insert(root, key);
        return height(root);
    }

    static TreeNode insert(TreeNode node, int key) {
        if (node == null) return new TreeNode(key);              // the empty slot takes the leaf
        if (key < node.val) node.left = insert(node.left, key);
        else node.right = insert(node.right, key);
        return node;
    }

    static int height(TreeNode node) {
        return node == null ? 0 : 1 + Math.max(height(node.left), height(node.right));
    }

    /** Oracle: counts levels with a breadth-first pass over the built tree. */
    static int levels(TreeNode root) {
        if (root == null) return 0;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        int count = 0;
        while (!queue.isEmpty()) {
            for (int i = queue.size(); i > 0; i--) {
                TreeNode n = queue.poll();
                if (n.left != null) queue.add(n.left);
                if (n.right != null) queue.add(n.right);
            }
            count++;
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: a sorted array makes a chain.
        if (heightAfterInserts(new int[] {1, 2, 3}) != 3) throw new AssertionError("ex1");
        // Example 2: the middle key first gives two levels.
        if (heightAfterInserts(new int[] {2, 1, 3}) != 2) throw new AssertionError("ex2");
        if (heightAfterInserts(new int[] {}) != 0) throw new AssertionError("empty");
        // A sorted run of 1000 keys has height 1000, and the compact order has height 10 for 1023 keys.
        int[] sorted = new int[1000];
        for (int i = 0; i < sorted.length; i++) sorted[i] = i;
        if (heightAfterInserts(sorted) != 1000) throw new AssertionError("sorted");
        // Random orders must match the breadth-first level count.
        Random rnd = new Random(1681);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(40);
            List<Integer> keys = new ArrayList<>();
            for (int i = 0; i < n; i++) keys.add(i * 3 - 20);
            Collections.shuffle(keys, rnd);
            TreeNode root = null;
            int[] arr = new int[n];
            for (int i = 0; i < n; i++) { arr[i] = keys.get(i); root = insert(root, arr[i]); }
            if (heightAfterInserts(arr) != levels(root)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Identify One Rotation (Author exercise)
<!-- id: tb-bal-rotation-type -->

**Approach.**
The first key becomes the root, and the other two keys attach by comparison, so the order alone decides the shape. Three keys fall into four cases. When the second key is smaller than the first and the third key is smaller than the second, the keys form a chain that leans left, and one right rotation at the root lifts the middle key. When the keys increase, the chain leans right, and one left rotation fixes it. When the second and third keys lie on opposite sides of the first, the tree has height 2, and nothing needs repair. In the remaining case the second key lies on one side of the first, and the third key lands on the opposite side of the second, which makes a zigzag chain that needs two rotations.

The method classifies by comparing the three keys and does not need to build the tree. The invariant is that the root is the first key, and each later key follows the side its comparisons choose.

**Complexity.**
- **Time** is O(1), because three keys need a fixed number of comparisons.
- **Space** is O(1).

```java run
import java.util.*;

public final class RotationType {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Names the repair for the plain tree built from three keys.
     * Time: O(1).
     * Space: O(1).
     * Invariant: the first key is the root, and each later key follows its comparisons.
     */
    static String classify(int[] k) {
        int a = k[0], b = k[1], c = k[2];
        if (b < a && c < b) return "RIGHT_ROTATION";             // 3,2,1: the chain leans left
        if (b > a && c > b) return "LEFT_ROTATION";              // 1,2,3: the chain leans right
        boolean secondLeft = b < a;
        boolean thirdLeft = c < a;
        if (secondLeft != thirdLeft) return "NONE";              // the keys land on opposite sides of the root
        return "DOUBLE";                                         // a zigzag: both keys on one side, opposite sides of each other
    }

    static TreeNode insert(TreeNode node, int key) {
        if (node == null) return new TreeNode(key);
        if (key < node.val) node.left = insert(node.left, key);
        else node.right = insert(node.right, key);
        return node;
    }

    /** Oracle: build the tree and read its shape. */
    static String oracle(int[] k) {
        TreeNode root = null;
        for (int key : k) root = insert(root, key);
        if (root.left != null && root.left.left != null) return "RIGHT_ROTATION";
        if (root.right != null && root.right.right != null) return "LEFT_ROTATION";
        if (root.left != null && root.right != null) return "NONE";
        return "DOUBLE";
    }

    public static void main(String[] args) {
        // Example 1: decreasing keys lean left.
        if (!classify(new int[] {3, 2, 1}).equals("RIGHT_ROTATION")) throw new AssertionError("ex1");
        // Example 2: a zigzag needs two rotations.
        if (!classify(new int[] {1, 3, 2}).equals("DOUBLE")) throw new AssertionError("ex2");
        if (!classify(new int[] {2, 1, 3}).equals("NONE")) throw new AssertionError("none");
        // Every ordering of several key triples, including negative keys, must match the built tree.
        int[][] sets = {{1, 2, 3}, {-5, 0, 7}, {10, -10, 0}};
        for (int[] s : sets) {
            int[][] perms = {{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
            for (int[] p : perms) {
                int[] k = {s[p[0]], s[p[1]], s[p[2]]};
                if (!classify(k).equals(oracle(k))) throw new AssertionError(Arrays.toString(k));
            }
        }
    }
}
```

#### Solution: [Boundary] Preserve Inorder Through Rotation (Author exercise)
<!-- id: tb-bal-inorder -->

**Approach.**
The method finds the node `z` with the given key and its parent, and then applies a right rotation. The left child `y` of `z` rises above `z`. The right subtree of `y` holds keys larger than `y` and smaller than `z`, so it becomes the new left subtree of `z`. The node `z` becomes the right child of `y`. The parent of `z` now points at `y`, or the root changes to `y` when `z` was the root. Only three references change, so the relative order of all keys is untouched. The method then collects the keys by an inorder walk and returns them, and the harness compares them with the order before the rotation.

The invariant is that every key keeps the same position in sorted order, because each moved subtree still lies between the same two keys.

**Complexity.**
- **Time** is O(h) to find the node, plus O(1) for the rotation and O(n) for the final walk.
- **Space** is O(h) for the recursion of the walk.

```java run
import java.util.*;

public final class RotateInorder {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Rotates the node with the given key to the right and returns the sorted keys afterward.
     * Time: O(h) to find the node, O(1) to rotate, O(n) to list the keys.
     * Space: O(h) for the recursion of the listing.
     * Invariant: every moved subtree still lies between the same two keys.
     */
    static List<Integer> rotateAndList(TreeNode root, int key) {
        TreeNode top = rotateAt(root, key);
        List<Integer> out = new ArrayList<>();
        inorder(top, out);
        return out;
    }

    static TreeNode rotateAt(TreeNode node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = rotateAt(node.left, key); return node; }    // keep searching on the left
        if (key > node.val) { node.right = rotateAt(node.right, key); return node; }  // keep searching on the right
        TreeNode y = node.left;                                  // the child that rises
        node.left = y.right;                                     // keys between y and node move under node
        y.right = node;                                          // node drops to the right of y
        return y;                                                // the parent will point at y
    }

    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static boolean valid(TreeNode n, long lo, long hi) {
        return n == null || (n.val > lo && n.val < hi && valid(n.left, lo, n.val) && valid(n.right, n.val, hi));
    }

    static void collect(TreeNode n, List<TreeNode> out) {
        if (n == null) return;
        out.add(n);
        collect(n.left, out);
        collect(n.right, out);
    }

    public static void main(String[] args) {
        // Example 1: the left chain 3, 2, 1.
        TreeNode a = new TreeNode(3);
        a.left = new TreeNode(2);
        a.left.left = new TreeNode(1);
        if (!rotateAndList(a, 3).equals(List.of(1, 2, 3))) throw new AssertionError("ex1");
        // Example 2: the five-node tree rotates at the root.
        TreeNode b = new TreeNode(5);
        b.left = new TreeNode(3);
        b.right = new TreeNode(8);
        b.left.left = new TreeNode(2);
        b.left.right = new TreeNode(4);
        if (!rotateAndList(b, 5).equals(List.of(2, 3, 4, 5, 8))) throw new AssertionError("ex2");
        // Random trees: rotate every node that has a left child; the keys must keep their order and the tree must stay valid.
        Random rnd = new Random(1683);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 2 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(60));
            List<Integer> before = new ArrayList<>();
            inorder(x, before);
            List<TreeNode> all = new ArrayList<>();
            collect(x, all);
            for (TreeNode z : all) {
                if (z.left == null) continue;
                int key = z.val;
                TreeNode copy = null;                              // work on a fresh copy for each rotation
                for (int v : preorder(x)) copy = insert(copy, v);
                TreeNode top = rotateAt(copy, key);
                List<Integer> after = new ArrayList<>();
                inorder(top, after);
                if (!after.equals(before) || !valid(top, Long.MIN_VALUE, Long.MAX_VALUE)) throw new AssertionError("random " + t);
            }
        }
    }

    static List<Integer> preorder(TreeNode n) {
        List<Integer> out = new ArrayList<>();
        if (n == null) return out;
        out.add(n.val);
        out.addAll(preorder(n.left));
        out.addAll(preorder(n.right));
        return out;
    }
}
```

#### Solution: [Recognize] Explain Library Choice (Author exercise)
<!-- id: tb-bal-library-choice -->

**Approach.**
The method builds the plain tree by inserting the keys in arrival order and measures its height. The smallest possible height of a tree with `n` nodes is the number of bits of `n`, because a tree of height `h` holds at most `2^h - 1` nodes, so `h` must satisfy `2^h > n`. The method computes that number as `32 - Integer.numberOfLeadingZeros(n)`. It returns `true` when the measured height exceeds twice that number. A sorted order of seven keys gives height 7 against a limit of 6, which selects the library map. The compact order gives height 3 against the same limit, so the plain tree is acceptable. The harness also checks that `TreeMap` agrees with the successor rule from the earlier lesson, because the library hides the same structure.

The invariant is that the height of the plain tree is the longest chain of comparisons, and the bit count is a lower bound for any tree of that size.

**Complexity.**
- **Time** is O(n * h) for the inserts, which is O(n^2) in the worst case.
- **Space** is O(n) for the nodes, plus O(h) for the recursion.

```java run
import java.util.*;

public final class LibraryChoice {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns true when the plain tree is more than twice as tall as the best possible height.
     * Time: O(n * h) for the inserts.
     * Space: O(n) for the nodes, plus O(h) for the recursion.
     * Invariant: the bit count of n is a lower bound on the height of any tree with n nodes.
     */
    static boolean preferLibrary(int[] keys) {
        TreeNode root = null;
        for (int key : keys) root = insert(root, key);
        int bits = 32 - Integer.numberOfLeadingZeros(keys.length);    // smallest possible height
        return height(root) > 2 * bits;
    }

    static TreeNode insert(TreeNode node, int key) {
        if (node == null) return new TreeNode(key);
        if (key < node.val) node.left = insert(node.left, key);
        else node.right = insert(node.right, key);
        return node;
    }

    static int height(TreeNode node) {
        return node == null ? 0 : 1 + Math.max(height(node.left), height(node.right));
    }

    /** Successor by descent, as in the earlier lesson. */
    static Integer successor(TreeNode root, int key) {
        Integer best = null;
        for (TreeNode n = root; n != null; ) {
            if (n.val > key) { best = n.val; n = n.left; } else n = n.right;
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: sorted keys give height 7 against a limit of 6.
        if (!preferLibrary(new int[] {1, 2, 3, 4, 5, 6, 7})) throw new AssertionError("ex1");
        // Example 2: the compact order gives height 3.
        if (preferLibrary(new int[] {4, 2, 6, 1, 3, 5, 7})) throw new AssertionError("ex2");
        // Java claim: the bit count of 7 is 3, of 8 is 4, and of 1 is 1.
        if (32 - Integer.numberOfLeadingZeros(7) != 3 || 32 - Integer.numberOfLeadingZeros(8) != 4
                || 32 - Integer.numberOfLeadingZeros(1) != 1) throw new AssertionError("bits");
        // Java claim: TreeMap answers successor and predecessor queries, and it matches the descent rule.
        Random rnd = new Random(1684);
        for (int t = 0; t < 200; t++) {
            TreeMap<Integer, String> map = new TreeMap<>();
            TreeNode root = null;
            for (int i = 0; i < 1 + rnd.nextInt(30); i++) {
                int k = rnd.nextInt(50);
                map.put(k, "v");
                root = insert(root, k);
            }
            for (int q = -1; q <= 51; q++)
                if (!Objects.equals(map.higherKey(q), successor(root, q))) throw new AssertionError("higherKey " + t);
        }
        // Sorted input prefers the library from nine keys on.
        for (int n = 9; n <= 200; n += 7) {
            int[] sorted = new int[n];
            for (int i = 0; i < n; i++) sorted[i] = i;
            if (!preferLibrary(sorted)) throw new AssertionError("sorted " + n);
        }
    }
}
```
