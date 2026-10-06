<!-- solutions-for: 07-iterator-foundations -->
### Solutions For The Tree Iterator

#### Solution: [Build] Push Left Spine (Author exercise)
<!-- id: tb-iter-left-spine -->

**Approach.**
The method starts at the root and pushes each node it reaches onto an `ArrayDeque` used as a stack. After each push it moves to the left child, and it stops when the current node is `null`. The nodes on the stack then form the chain of left children from the root to the node with no left child. The last pushed node holds the smallest key, because nothing in the tree lies to its left. The method reads the stack from the bottom to the top by iterating from the last element of the deque, which `descendingIterator` provides.

The invariant is that every pushed node is the left child of the previous one, so the stack holds a single downward chain. The top is the smallest key in the subtree of the first pushed node.

**Complexity.**
- **Time** is O(h), because the loop visits one node per level of the left edge.
- **Space** is O(h) for the stack and the returned list.

```java run
import java.util.*;

public final class LeftSpine {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the keys of the left spine from the bottom of the stack to the top.
     * Time: O(h), because the loop follows the left edge.
     * Space: O(h) for the stack and the result.
     * Invariant: each pushed node is the left child of the previous one.
     */
    static List<Integer> leftSpine(TreeNode root) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode node = root;
        while (node != null) {                 // stop at the first missing left child
            stack.push(node);
            node = node.left;
        }
        List<Integer> bottomToTop = new ArrayList<>();
        Iterator<TreeNode> it = stack.descendingIterator();   // the last pushed node comes last
        while (it.hasNext()) bottomToTop.add(it.next().val);
        return bottomToTop;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static int minKey(TreeNode n) {
        while (n.left != null) n = n.left;
        return n.val;
    }

    public static void main(String[] args) {
        // Example 1: the left edge of the seven-node tree.
        TreeNode r = new TreeNode(40);
        r.left = new TreeNode(20);
        r.right = new TreeNode(60);
        r.left.left = new TreeNode(10);
        r.left.right = new TreeNode(30);
        r.right.left = new TreeNode(50);
        r.right.right = new TreeNode(70);
        if (!leftSpine(r).equals(List.of(40, 20, 10))) throw new AssertionError("ex1");
        // Example 2: a root with only a right child.
        TreeNode s = new TreeNode(5);
        s.right = new TreeNode(8);
        if (!leftSpine(s).equals(List.of(5))) throw new AssertionError("ex2");
        if (!leftSpine(null).isEmpty()) throw new AssertionError("empty");
        // Random trees: the last entry is the minimum, and each entry is the left child of the one before.
        Random rnd = new Random(1661);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(50));
            List<Integer> got = leftSpine(x);
            if (got.get(got.size() - 1) != minKey(x)) throw new AssertionError("min " + t);
            TreeNode c = x;
            for (int key : got) {
                if (c == null || c.val != key) throw new AssertionError("chain " + t);
                c = c.left;
            }
            if (c != null) throw new AssertionError("short " + t);
        }
    }
}
```

#### Solution: [Vary] Advance One Inorder Step (Author exercise)
<!-- id: tb-iter-advance -->

**Approach.**
The method loads the left spine of the root, then repeats `j` times a pair of actions. The first action pops the top node, which holds the smallest key not yet returned. The second action pushes the left spine of the right child of the popped node. The keys of that right subtree come next in sorted order, and they are all smaller than the node that now lies below them on the stack. After the jth repetition the method reads the stack from the bottom to the top and returns the keys.

The invariant is that the stack holds the nodes still waiting, and the top is the smallest key not yet returned. The pop and the loading of the right spine keep it true.

**Complexity.**
- **Time** is O(h + j), because each node is pushed once and popped once, and at most `h` nodes are pushed before the first pop.
- **Space** is O(h) for the stack.

```java run
import java.util.*;

public final class AdvanceSteps {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void pushLeft(Deque<TreeNode> stack, TreeNode node) {
        while (node != null) { stack.push(node); node = node.left; }
    }

    /**
     * Returns the stack keys, bottom to top, after j pops.
     * Time: O(h + j), because each node is pushed and popped once.
     * Space: O(h) for the stack.
     * Invariant: the top is the smallest key not yet returned.
     */
    static List<Integer> afterPops(TreeNode root, int j) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        pushLeft(stack, root);                        // load the first path
        for (int i = 0; i < j; i++) {
            TreeNode popped = stack.pop();            // the next key in sorted order
            pushLeft(stack, popped.right);            // its right subtree comes next
        }
        List<Integer> out = new ArrayList<>();
        Iterator<TreeNode> it = stack.descendingIterator();
        while (it.hasNext()) out.add(it.next().val);
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

    /** Oracle: the waiting nodes are the ancestors of the next key whose key is larger than it, plus the next key itself. */
    static List<Integer> oracle(TreeNode root, int j, List<Integer> sorted) {
        if (j == sorted.size()) return new ArrayList<>();
        int next = sorted.get(j);
        List<Integer> out = new ArrayList<>();
        for (TreeNode c = root; c != null; ) {
            if (c.val >= next) out.add(c.val);            // a waiting node is not smaller than the next key
            if (next == c.val) break;
            c = next < c.val ? c.left : c.right;
        }
        return out;
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(40);
        r.left = new TreeNode(20);
        r.right = new TreeNode(60);
        r.left.left = new TreeNode(10);
        r.left.right = new TreeNode(30);
        r.right.left = new TreeNode(50);
        r.right.right = new TreeNode(70);
        // Example 1: after one pop the stack holds 40 and 20.
        if (!afterPops(r, 1).equals(List.of(40, 20))) throw new AssertionError("ex1");
        // Example 2: after two pops the stack holds 40 and 30.
        if (!afterPops(r, 2).equals(List.of(40, 30))) throw new AssertionError("ex2");
        // After all pops the stack is empty.
        if (!afterPops(r, 7).isEmpty()) throw new AssertionError("end");
        // Random trees: every j must match the ancestor-path oracle.
        Random rnd = new Random(1662);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(50));
            List<Integer> sorted = new ArrayList<>();
            inorder(x, sorted);
            for (int j = 1; j <= sorted.size(); j++) {
                List<Integer> want = oracle(x, j, sorted);
                if (!afterPops(x, j).equals(want)) throw new AssertionError("t=" + t + " j=" + j);
            }
        }
    }
}
```

#### Solution: [Boundary] Empty Iterator And Right Chain (Author exercise)
<!-- id: tb-iter-edges -->

**Approach.**
The method builds the stack from the left spine of the root and then loops while the stack is not empty, which is the test `hasNext`. Each pass pops a node, counts one returned key, and pushes the left spine of the popped node's right child. A running maximum records the largest stack size after each push step. A null root leaves the stack empty from the start, so the loop never runs and the answer is zero keys with a largest size of zero. In a chain where every node has only a right child, the spine of the root is the root itself. Each pop removes the only node and pushes the next single node, so the stack never holds more than one node.

The invariant is that the loop condition is true exactly when a key remains, so no pop runs on an empty stack.

**Complexity.**
- **Time** is O(n), because each node is pushed and popped once.
- **Space** is O(h) for the stack.

```java run
import java.util.*;

public final class IteratorEdges {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns {keys returned, largest stack size}.
     * Time: O(n), because each node is pushed and popped once.
     * Space: O(h) for the stack.
     * Invariant: the loop runs only while a key remains.
     */
    static int[] drain(TreeNode root) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        int count = 0, peak = 0;
        for (TreeNode n = root; n != null; n = n.left) stack.push(n);   // load the left spine
        peak = stack.size();
        while (!stack.isEmpty()) {                                      // the hasNext test
            TreeNode popped = stack.pop();
            count++;
            for (TreeNode n = popped.right; n != null; n = n.left) stack.push(n);   // load the right child's spine
            peak = Math.max(peak, stack.size());
        }
        return new int[] {count, peak};
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static int size(TreeNode n) { return n == null ? 0 : 1 + size(n.left) + size(n.right); }

    static int height(TreeNode n) { return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right)); }

    public static void main(String[] args) {
        // Example 1: the empty tree.
        if (!Arrays.equals(drain(null), new int[] {0, 0})) throw new AssertionError("ex1");
        // Example 2: a right chain keeps the stack at size 1.
        TreeNode c = new TreeNode(1);
        c.right = new TreeNode(2);
        c.right.right = new TreeNode(3);
        if (!Arrays.equals(drain(c), new int[] {3, 1})) throw new AssertionError("ex2");
        // A single node returns one key.
        if (!Arrays.equals(drain(new TreeNode(9)), new int[] {1, 1})) throw new AssertionError("single");
        // Random trees: the count equals the node count and the peak never exceeds the height.
        Random rnd = new Random(1663);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < rnd.nextInt(30); i++) x = insert(x, rnd.nextInt(60));
            int[] got = drain(x);
            if (got[0] != size(x) || got[1] > height(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Binary Search Tree Iterator (LeetCode 173)
<!-- id: tb-bst-iterator -->

**Approach.**
The constructor pushes the left spine of the root, so the top of the stack holds the smallest key. The method `hasNext` returns whether the stack is non-empty. The method `next` pops the top node, pushes the left spine of its right child, and returns the popped key. The keys of the right subtree are the next keys in sorted order, and they are smaller than every node still waiting on the stack, so the new top is the next smallest key. The stack holds one root-to-node path at most, so the memory is O(h). Every node is pushed once and popped once, so `n` calls cost at most `2n` operations in total, which is O(1) amortized per call.

The invariant is that the stack lists the waiting nodes and its top holds the smallest unreturned key. A call on an exhausted iterator pops an empty deque and throws, which keeps a wrong call from returning a wrong key.

**Complexity.**
- **Time** is O(1) amortized for `next` and O(1) for `hasNext`, with O(h) for a single `next` in the worst case.
- **Space** is O(h) for the stack.

```java run
import java.util.*;

public final class BstIteratorDemo {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Iterator over the keys of a search tree in sorted order.
     * Time: O(1) amortized per next, O(h) worst case for one call.
     * Space: O(h) for the stack.
     * Invariant: the stack top is the smallest key not yet returned.
     */
    static final class BSTIterator {
        private final Deque<TreeNode> stack = new ArrayDeque<>();
        long work = 0;                                     // pushes and pops, to check the amortized bound

        BSTIterator(TreeNode root) { pushLeft(root); }

        private void pushLeft(TreeNode node) {
            while (node != null) { stack.push(node); work++; node = node.left; }
        }

        boolean hasNext() { return !stack.isEmpty(); }

        int next() {
            TreeNode popped = stack.pop();                 // throws NoSuchElementException when empty
            work++;
            pushLeft(popped.right);                        // the right subtree's smallest keys come next
            return popped.val;
        }
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
        TreeNode r = new TreeNode(7);
        r.left = new TreeNode(3);
        r.right = new TreeNode(15);
        r.right.left = new TreeNode(9);
        r.right.right = new TreeNode(20);
        // Example 1: next, next, hasNext, next, hasNext.
        BSTIterator it = new BSTIterator(r);
        if (it.next() != 3 || it.next() != 7 || !it.hasNext() || it.next() != 9 || !it.hasNext()) throw new AssertionError("ex1");
        // Example 2: five keys, then the iterator is exhausted.
        it = new BSTIterator(r);
        int[] want = {3, 7, 9, 15, 20};
        for (int w : want) if (it.next() != w) throw new AssertionError("ex2");
        if (it.hasNext()) throw new AssertionError("ex2 end");
        // Java claim: next on an exhausted iterator throws NoSuchElementException.
        boolean threw = false;
        try { it.next(); } catch (NoSuchElementException e) { threw = true; }
        if (!threw) throw new AssertionError("exhausted");
        // Random trees: the keys must match the sorted list, and total work must stay within 2n.
        Random rnd = new Random(1664);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 1 + rnd.nextInt(40); i++) x = insert(x, rnd.nextInt(80));
            List<Integer> all = new ArrayList<>();
            inorder(x, all);
            BSTIterator bi = new BSTIterator(x);
            for (int key : all) {
                if (!bi.hasNext() || bi.next() != key) throw new AssertionError("order " + t);
            }
            if (bi.hasNext() || bi.work > 2L * all.size()) throw new AssertionError("work " + t);
        }
    }
}
```
