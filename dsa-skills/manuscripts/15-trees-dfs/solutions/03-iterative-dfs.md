<!-- solutions-for: 03-iterative-dfs -->
### Solutions For Walking With A Stack

#### Solution: [Build] Iterative Preorder (Author exercise)
<!-- id: it-preorder -->

**Approach.**
The method starts with the root on a `Deque` and loops while the stack is not empty. Each round pops one node, appends its value, and pushes the right child and then the left child. A stack returns the most recent push first, so the left child is popped next and the right child waits underneath until the whole left subtree is finished.

The invariant is that the stack holds exactly the subtrees that have not started, with the next subtree on top, and every node already popped has been written once. The stack never holds more than h + 1 nodes, because each level contributes at most one waiting right sibling.

**Complexity.**
- **Time** is O(n), because each node is pushed once and popped once.
- **Space** is O(h) for the stack, plus the n result values.

```java run
import java.util.*;

public final class IterativePreorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int maxStack;                                         // the largest stack size seen, for the memory claim

    /**
     * Returns the preorder values without recursion.
     * Time: O(n), one push and one pop per node.
     * Space: O(h) for the stack.
     * Invariant: the stack holds the subtrees that have not started.
     */
    static List<Integer> preorder(Node root, boolean leftFirst) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);                      // an empty tree leaves the stack empty
        while (!stack.isEmpty()) {                               // one round per node
            maxStack = Math.max(maxStack, stack.size());
            Node node = stack.pop();                             // the top subtree starts now
            out.add(node.val);                                   // preorder handles the node first
            Node first = leftFirst ? node.left : node.right;     // the child that is pushed first
            Node second = leftFirst ? node.right : node.left;    // the child that is pushed second
            if (first != null) stack.push(first);                // the first push comes out last
            if (second != null) stack.push(second);              // the second push comes out next
        }
        return out;
    }

    static List<Integer> preorder(Node root) { return preorder(root, false); }   // right first, so left comes out first

    static void recursive(Node node, List<Integer> out) {
        if (node == null) return;
        out.add(node.val);
        recursive(node.left, out);
        recursive(node.right, out);
    }

    static int height(Node node) { return node == null ? 0 : 1 + Math.max(height(node.left), height(node.right)); }

    static Node random(Random rnd, int depth) {
        if (depth > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 6, left 2 with right child 4, right 9.
        Node t1 = new Node(6, new Node(2, null, new Node(4, null, null)), new Node(9, null, null));
        if (!preorder(t1).equals(List.of(6, 2, 4, 9))) throw new AssertionError("ex1");
        // Example 2: root 1 with right child 3 that has right child 5.
        Node t2 = new Node(1, null, new Node(3, null, new Node(5, null, null)));
        if (!preorder(t2).equals(List.of(1, 3, 5))) throw new AssertionError("ex2");
        // The empty tree gives the empty list.
        if (!preorder(null).isEmpty()) throw new AssertionError("empty");
        // Pushing left before right gives right-first order: 1, 3, 2 for root 1 with children 2 and 3.
        Node t3 = new Node(1, new Node(2, null, null), new Node(3, null, null));
        if (!preorder(t3, true).equals(List.of(1, 3, 2))) throw new AssertionError("false friend");
        // Random trees match the recursive walk, and the stack never exceeds h + 1 nodes.
        Random rnd = new Random(9);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<Integer> want = new ArrayList<>();
            recursive(x, want);
            maxStack = 0;
            if (!preorder(x).equals(want)) throw new AssertionError("random " + t);
            if (maxStack > height(x) + 1) throw new AssertionError("stack bound " + t);
        }
    }
}
```

#### Solution: [Vary] Iterative Inorder (Author exercise)
<!-- id: it-inorder -->

**Approach.**
The method keeps a reference `cur` to the node it is about to enter, and a stack of nodes that wait for their action. An inner loop pushes `cur` and moves to its left child until `cur` is `null`, so the stack ends with the left spine on it. The method then pops the top node, which has an empty left side, appends its value, and sets `cur` to its right child. The outer loop stops when `cur` is `null` and the stack is empty.

The invariant is that every node on the stack has its left subtree started or finished and its own value not yet written. A node is written exactly when it is popped, so the order is left subtree, node, right subtree.

**Complexity.**
- **Time** is O(n), because each node is pushed once and popped once.
- **Space** is O(h) for the stack, plus the n result values.

```java run
import java.util.*;

public final class IterativeInorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the inorder values without recursion.
     * Time: O(n), one push and one pop per node.
     * Space: O(h) for the stack.
     * Invariant: each stacked node waits for its own write, below the node being walked.
     */
    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {                // continue while a node can be entered or popped
            while (cur != null) {                                // push the left spine of cur
                stack.push(cur);
                cur = cur.left;
            }
            Node node = stack.pop();                             // the deepest node has an empty left side
            out.add(node.val);                                   // its left subtree is done, so write it
            cur = node.right;                                    // the right subtree comes next
        }
        return out;
    }

    static void recursive(Node node, List<Integer> out) {
        if (node == null) return;
        recursive(node.left, out);
        out.add(node.val);
        recursive(node.right, out);
    }

    static Node random(Random rnd, int depth) {
        if (depth > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 6, left 2 with right child 4, right 9.
        Node t1 = new Node(6, new Node(2, null, new Node(4, null, null)), new Node(9, null, null));
        if (!inorder(t1).equals(List.of(2, 4, 6, 9))) throw new AssertionError("ex1");
        // Example 2: root 8 with left child 5 that has left child 3.
        Node t2 = new Node(8, new Node(5, new Node(3, null, null), null), null);
        if (!inorder(t2).equals(List.of(3, 5, 8))) throw new AssertionError("ex2");
        // The empty tree gives the empty list, and a single node gives itself.
        if (!inorder(null).isEmpty() || !inorder(new Node(4, null, null)).equals(List.of(4))) throw new AssertionError("small");
        // Random trees match the recursive walk.
        Random rnd = new Random(10);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<Integer> want = new ArrayList<>();
            recursive(x, want);
            if (!inorder(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Deep Skewed Tree (Author exercise)
<!-- id: it-deep-sum -->

**Approach.**
The sum does not depend on the order of the walk, so the method uses the simplest loop. It pops a node, adds the value to a `long` total, and pushes each non-null child. An empty tree never enters the loop and returns 0. The stack lives on the heap, so a chain of 200,000 nodes needs a stack of at most two entries and no deep call stack.

The invariant is that the total equals the sum of the nodes already popped, and every unpopped node lies below a node on the stack or on the stack itself. The recursive sum on the same chain overflows a small thread stack, which the check below confirms on a thread with 256 KB of stack.

**Complexity.**
- **Time** is O(n), because each node is pushed once and popped once.
- **Space** is O(w) for the stack, where w is the largest number of waiting nodes, which is O(1) for a chain and O(h) in general.

```java run
import java.util.*;

public final class DeepSum {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the sum of all values without recursion.
     * Time: O(n), each node is pushed and popped once.
     * Space: O(h) on the heap.
     * Invariant: total is the sum of the nodes popped so far.
     */
    static long sum(Node root) {
        long total = 0;                                          // a long avoids int overflow on large trees
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);                      // an empty tree skips the loop
        while (!stack.isEmpty()) {                               // one round per node
            Node node = stack.pop();
            total += node.val;                                   // the order does not matter for a sum
            if (node.left != null) stack.push(node.left);
            if (node.right != null) stack.push(node.right);
        }
        return total;
    }

    static long recursiveSum(Node node) {
        if (node == null) return 0;
        return node.val + recursiveSum(node.left) + recursiveSum(node.right);
    }

    static Node chain(int n, int val, boolean leftLeaning) {
        Node head = null;
        for (int i = 0; i < n; i++) head = leftLeaning ? new Node(val, head, null) : new Node(val, null, head);   // built bottom-up without recursion
        return head;
    }

    static Node random(Random rnd, int depth) {
        if (depth > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) throws Exception {
        // Example 1: the empty tree has sum 0.
        if (sum(null) != 0) throw new AssertionError("empty");
        // Example 2: a left-leaning chain of 200000 nodes that each hold 1.
        Node deep = chain(200_000, 1, true);
        if (sum(deep) != 200_000L) throw new AssertionError("chain");
        if (sum(chain(200_000, 1, false)) != 200_000L) throw new AssertionError("right chain");
        // The recursive sum overflows a thread with a 256 KB stack on the same chain.
        boolean[] overflowed = {false};
        Thread th = new Thread(null, () -> {
            try { recursiveSum(deep); } catch (StackOverflowError e) { overflowed[0] = true; }
        }, "small", 256 * 1024);
        th.start();
        th.join();
        if (!overflowed[0]) throw new AssertionError("recursion should overflow");
        // The iterative sum succeeds on a thread with the same small stack.
        long[] got = {0};
        Thread th2 = new Thread(null, () -> got[0] = sum(deep), "small2", 256 * 1024);
        th2.start();
        th2.join();
        if (got[0] != 200_000L) throw new AssertionError("iterative in small thread");
        // Negative values and a sum above the int range both work.
        if (sum(chain(5, -3, true)) != -15) throw new AssertionError("negative");
        if (sum(chain(3000, 1_000_000, true)) != 3_000_000_000L) throw new AssertionError("long");
        // Random trees match the recursive sum.
        Random rnd = new Random(11);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            if (sum(x) != recursiveSum(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Postorder Without Recursion (LeetCode 145)
<!-- id: it-postorder -->

**Approach.**
A node must be written after both sides, so the loop meets a node on top of the stack more than once. The method pushes the left spine of `cur`, then looks at the top node without removing it. Suppose the top node has a right child that differs from `last`. The right side has not been written, so `cur` moves to that child and the next round pushes its left spine. Otherwise both sides are done, so the method writes the top node, pops it, and stores it in `last`.

The invariant is that the stack holds the ancestors of the current position, and `last` is the most recently written node. A parent is written right after its right child, or right after its left child when the right side is empty. The variable `last` separates these cases.

**Complexity.**
- **Time** is O(n), because each node is pushed once and popped once, and each node is peeked at most twice.
- **Space** is O(h) for the stack, plus the n result values.

```java run
import java.util.*;

public final class IterativePostorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the postorder values without recursion.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: the stack holds the ancestors of the current position, and last is the latest write.
     */
    static List<Integer> postorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root, last = null;
        while (cur != null || !stack.isEmpty()) {                // continue while work remains
            while (cur != null) {                                // push the left spine
                stack.push(cur);
                cur = cur.left;
            }
            Node top = stack.peek();                             // inspect the node without removing it
            if (top.right != null && top.right != last) {
                cur = top.right;                                 // the right side has not been written yet
            } else {
                out.add(top.val);                                // both sides are done, so write the node
                last = stack.pop();                              // remember it for its parent
            }
        }
        return out;
    }

    static void recursive(Node node, List<Integer> out) {
        if (node == null) return;
        recursive(node.left, out);
        recursive(node.right, out);
        out.add(node.val);
    }

    static Node random(Random rnd, int depth) {
        if (depth > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) throws Exception {
        // Example 1: root 4, left 2 with children 1 and 3.
        Node t1 = new Node(4, new Node(2, new Node(1, null, null), new Node(3, null, null)), null);
        if (!postorder(t1).equals(List.of(1, 3, 2, 4))) throw new AssertionError("ex1");
        // Example 2: root 5 with right child 7 that has left child 6.
        Node t2 = new Node(5, null, new Node(7, new Node(6, null, null), null));
        if (!postorder(t2).equals(List.of(6, 7, 5))) throw new AssertionError("ex2");
        // The empty tree gives the empty list.
        if (!postorder(null).isEmpty()) throw new AssertionError("empty");
        // A chain of 100000 nodes works on a thread with a 256 KB stack.
        Node head = null;
        for (int i = 0; i < 100_000; i++) head = new Node(i, head, null);
        final Node deep = head;
        int[] size = {0};
        Thread th = new Thread(null, () -> size[0] = postorder(deep).size(), "small", 256 * 1024);
        th.start();
        th.join();
        if (size[0] != 100_000) throw new AssertionError("deep chain");
        // Random trees match the recursive walk.
        Random rnd = new Random(12);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<Integer> want = new ArrayList<>();
            recursive(x, want);
            if (!postorder(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```
