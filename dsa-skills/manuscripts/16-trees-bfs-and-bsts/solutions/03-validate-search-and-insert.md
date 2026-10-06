<!-- solutions-for: 03-validate-search-and-insert -->
### Solutions For Search And Insert

#### Solution: [Build] Search in a Binary Search Tree (LeetCode 700)
<!-- id: tb-bst-search -->

**Approach.**
The method keeps one reference that starts at the root. At each node it compares the key with the node key. An equal key ends the loop with a match. A smaller key moves the reference to the left child, and a larger key moves it to the right child. The branch that the reference leaves is the discarded subtree, which holds no key equal to the target because all of its keys lie on the other side of the node. A reference of `null` means the key is absent.

The invariant is that, if the key exists, it lies in the subtree of the current reference. Each comparison keeps that true by moving to the only child that can hold the key.

**Complexity.**
- **Time** is O(h), because each step moves one level down and the tree has height `h`.
- **Space** is O(1), because the loop stores one reference.

```java run
import java.util.*;

public final class BstSearch {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the node holding val, or null when no node holds it.
     * Time: O(h), because one level is crossed per comparison.
     * Space: O(1).
     * Invariant: if val exists, it lies in the subtree of node.
     */
    static TreeNode searchBST(TreeNode root, int val) {
        TreeNode node = root;
        // The loop stops at a match or at an empty slot.
        while (node != null && node.val != val) {
            node = val < node.val ? node.left : node.right;      // the other side cannot hold val
        }
        return node;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    /** Oracle: full scan of every node. */
    static TreeNode scan(TreeNode n, int v) {
        if (n == null) return null;
        if (n.val == v) return n;
        TreeNode l = scan(n.left, v);
        return l != null ? l : scan(n.right, v);
    }

    public static void main(String[] args) {
        // Example 1: the node 2 is returned with its children.
        TreeNode r = new TreeNode(4);
        r.left = new TreeNode(2);
        r.right = new TreeNode(7);
        r.left.left = new TreeNode(1);
        r.left.right = new TreeNode(3);
        TreeNode hit = searchBST(r, 2);
        if (hit != r.left || hit.left.val != 1 || hit.right.val != 3) throw new AssertionError("ex1");
        // Example 2: an absent key gives null.
        if (searchBST(r, 5) != null) throw new AssertionError("ex2");
        if (searchBST(null, 5) != null) throw new AssertionError("empty");
        // A long chain needs no deep call stack because the loop is iterative.
        TreeNode chain = new TreeNode(0), tail = chain;
        for (int i = 1; i < 100000; i++) { tail.right = new TreeNode(i); tail = tail.right; }
        if (searchBST(chain, 99999) != tail) throw new AssertionError("chain");
        // Random search trees must match the full scan for present and absent keys.
        Random rnd = new Random(1621);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(40));
            for (int k = -1; k <= 41; k++)
                if (searchBST(x, k) != scan(x, k)) throw new AssertionError("t=" + t + " k=" + k);
        }
    }
}
```

#### Solution: [Vary] Insert into a Binary Search Tree (LeetCode 701)
<!-- id: tb-bst-insert -->

**Approach.**
The method returns a new single node for an empty tree. Otherwise it walks down with one reference, going left for a smaller key and right for a larger key. The walk stops when the chosen child is `null`, and that empty slot is the insertion point. The method writes the new node into the slot and returns the original root. No existing node moves, so every key that was findable stays findable under the same comparisons, and the new leaf sits where its own search will end.

The invariant is that the key belongs in the subtree of the current node. The slot at the end of the path is the only empty place where that holds for every ancestor at once.

**Complexity.**
- **Time** is O(h), because the walk crosses one level per comparison.
- **Space** is O(1), because the loop keeps one reference.

```java run
import java.util.*;

public final class BstInsert {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Inserts val as a new leaf and returns the root.
     * Time: O(h), because the walk crosses one level per comparison.
     * Space: O(1).
     * Invariant: val belongs in the subtree of node, and an empty slot ends the walk.
     */
    static TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) return new TreeNode(val);               // the first node becomes the root
        TreeNode node = root;
        while (true) {
            if (val < node.val) {
                if (node.left == null) { node.left = new TreeNode(val); break; }     // empty left slot
                node = node.left;
            } else {
                if (node.right == null) { node.right = new TreeNode(val); break; }   // empty right slot
                node = node.right;
            }
        }
        return root;
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
        // Example 1: 5 becomes the left child of 7.
        TreeNode r = new TreeNode(4);
        r.left = new TreeNode(2);
        r.right = new TreeNode(7);
        r.left.left = new TreeNode(1);
        r.left.right = new TreeNode(3);
        if (insertIntoBST(r, 5) != r || r.right.left == null || r.right.left.val != 5) throw new AssertionError("ex1");
        // Example 2: the empty tree gets a root.
        TreeNode e = insertIntoBST(null, 5);
        if (e.val != 5 || e.left != null || e.right != null) throw new AssertionError("ex2");
        // Random distinct keys: the tree stays valid, keeps its root, and holds exactly the sorted keys.
        Random rnd = new Random(1622);
        for (int t = 0; t < 300; t++) {
            List<Integer> keys = new ArrayList<>();
            for (int i = 0; i < 30; i++) keys.add(i);
            Collections.shuffle(keys, rnd);
            TreeNode root = null;
            int count = rnd.nextInt(30);
            for (int i = 0; i < count; i++) {
                TreeNode before = root;
                root = insertIntoBST(root, keys.get(i));
                if (before != null && root != before) throw new AssertionError("root moved");
            }
            List<Integer> got = new ArrayList<>(), want = new ArrayList<>(keys.subList(0, count));
            Collections.sort(want);
            inorder(root, got);
            if (!got.equals(want) || !valid(root, Long.MIN_VALUE, Long.MAX_VALUE)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Duplicate-Key Policy (Author exercise)
<!-- id: tb-bst-duplicate-policy -->

**Approach.**
Under the count policy an equal key never creates a node, so the walk has three outcomes at each node: go left, go right, or stop on equality. On equality the method increments the count of that node and returns the new count. When the walk reaches an empty slot, the method writes a node with count 1 and returns 1. An empty tree gets a root with count 1 and returns 1. Equal keys cannot hide below a node, because the first insert of a key is the only one that creates its node and every later insert finds it on the same path.

The invariant is that each key has at most one node, and a search for it ends at that node. The count stores the multiplicity, so the shape of the tree never depends on repeats.

**Complexity.**
- **Time** is O(h), because the walk crosses one level per comparison.
- **Space** is O(1) besides the one new node.

```java run
import java.util.*;

public final class DuplicatePolicy {
    static final class Node {
        int key, count = 1;
        Node left, right;
        Node(int key) { this.key = key; }
    }

    /** Wrapper that owns the root so an empty tree can gain one. */
    static final class CountTree {
        Node root;

        /**
         * Inserts key and returns its count afterwards.
         * Time: O(h), because the walk crosses one level per comparison.
         * Space: O(1) besides the new node.
         * Invariant: each key has at most one node.
         */
        int add(int key) {
            if (root == null) { root = new Node(key); return 1; }    // first key creates the root
            Node node = root;
            while (true) {
                if (key == node.key) return ++node.count;            // equal key: update the count
                Node next = key < node.key ? node.left : node.right;
                if (next == null) {
                    Node fresh = new Node(key);
                    if (key < node.key) node.left = fresh; else node.right = fresh;   // write into the empty slot
                    return 1;
                }
                node = next;
            }
        }
    }

    static int nodes(Node n) { return n == null ? 0 : 1 + nodes(n.left) + nodes(n.right); }

    public static void main(String[] args) {
        // Example 1: the key 5 already has count 2 and gains one.
        CountTree a = new CountTree();
        a.add(5);
        a.add(5);
        if (a.add(5) != 3) throw new AssertionError("ex1");
        // Example 2: the empty tree gains one node.
        CountTree b = new CountTree();
        if (b.add(5) != 1 || nodes(b.root) != 1) throw new AssertionError("ex2");
        // Random inserts must match a TreeMap count, and the node count must equal the distinct keys.
        Random rnd = new Random(1623);
        for (int t = 0; t < 300; t++) {
            CountTree tree = new CountTree();
            Map<Integer, Integer> want = new TreeMap<>();
            for (int i = 0; i < rnd.nextInt(60); i++) {
                int k = rnd.nextInt(12) - 6;
                int expected = want.merge(k, 1, Integer::sum);
                if (tree.add(k) != expected) throw new AssertionError("count " + t);
            }
            if (nodes(tree.root) != want.size()) throw new AssertionError("nodes " + t);
        }
    }
}
```

#### Solution: [Recognize] Delete Node in a BST (LeetCode 450)
<!-- id: tb-bst-delete -->

**Approach.**
The method searches for the key while it remembers the parent and the side, so it can rewrite the slot of the removed node. If the key is absent, the tree stays unchanged. A node with no left child is replaced by its right child, and a node with no right child is replaced by its left child. This covers the leaf case and the one-child case together, because a missing child is `null`. A node with two children takes the smallest key of its right subtree, which is the leftmost node there. The method then removes that leftmost node from the right subtree, and that node has no left child, so the earlier one-child rule applies to it.

The invariant is that the inorder sequence of the tree equals the old sequence without the key. The copied key sits between the left keys and the other right keys, so the order is preserved.

**Complexity.**
- **Time** is O(h), because the search takes one path and the removal of the smallest node takes one more path.
- **Space** is O(h) for the recursion stack of the recursive form used here.

```java run
import java.util.*;

public final class BstDelete {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Removes key and returns the new root of the subtree.
     * Time: O(h), because one search path and one leftmost walk are followed.
     * Space: O(h) for the recursion stack.
     * Invariant: the inorder keys equal the old keys without key.
     */
    static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;                            // absent key: nothing to remove
        if (key < root.val) { root.left = deleteNode(root.left, key); return root; }     // key lives on the left
        if (key > root.val) { root.right = deleteNode(root.right, key); return root; }   // key lives on the right
        if (root.left == null) return root.right;                 // leaf or only a right child
        if (root.right == null) return root.left;                 // only a left child
        TreeNode smallest = root.right;
        while (smallest.left != null) smallest = smallest.left;   // leftmost node of the right subtree
        root.val = smallest.val;                                  // the copied key fits between both sides
        root.right = deleteNode(root.right, smallest.val);        // remove the original, which has no left child
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
        // Example 1: deleting 3 copies 4 up and keeps 2 on the left.
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(6);
        r.left.left = new TreeNode(2);
        r.left.right = new TreeNode(4);
        r.right.right = new TreeNode(7);
        r = deleteNode(r, 3);
        if (r.left.val != 4 || r.left.left.val != 2 || r.left.right != null || r.right.val != 6) throw new AssertionError("ex1");
        // Example 2: an absent key leaves the tree unchanged.
        List<Integer> before = new ArrayList<>(), after = new ArrayList<>();
        inorder(r, before);
        r = deleteNode(r, 0);
        inorder(r, after);
        if (!before.equals(after)) throw new AssertionError("ex2");
        // Deleting the only node returns null.
        if (deleteNode(new TreeNode(1), 1) != null) throw new AssertionError("single");
        // Random trees: removing any key must give a valid tree whose inorder keys lose exactly that key.
        Random rnd = new Random(1624);
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
