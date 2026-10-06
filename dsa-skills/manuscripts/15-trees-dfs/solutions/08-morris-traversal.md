<!-- solutions-for: 08-morris-traversal -->
### Solutions For Walking Without A Stack

#### Solution: [Build] Find Inorder Predecessor (Author exercise)
<!-- id: mo-predecessor -->

**Approach.**
The predecessor of a node with a left child is the last node of the left subtree in inorder. The method moves to the left child once. It then follows `right` references while the current `right` reference is not `null`. The node where the loop stops has no right child, so inorder visits it last in that subtree. The invariant is that every node passed during the loop lies on the right edge of the left subtree and comes earlier in inorder than the next one.

**Complexity.**
- **Time** is O(h), because the search follows at most one path down the tree.
- **Space** is O(1), because the method holds one reference.

```java run
import java.util.*;

public final class FindPredecessor {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the predecessor of a node that has a left child.
     * Time: O(h).
     * Space: O(1).
     * Invariant: pred always lies on the right edge of the left subtree.
     */
    static Node predecessor(Node cur) {
        Node pred = cur.left;                                    // the search starts in the left subtree
        while (pred.right != null) pred = pred.right;            // the last node on the right edge has no right child
        return pred;
    }

    static void in(Node n, List<Node> out) { if (n == null) return; in(n.left, out); out.add(n); in(n.right, out); }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: node 4 of the five-node tree has the predecessor 3.
        Node n4 = new Node(4, new Node(2, new Node(1, null, null), new Node(3, null, null)), new Node(6, null, null));
        if (predecessor(n4).val != 3) throw new AssertionError("ex1");
        // Example 2: node 3 whose left child 1 has a right child 2.
        Node n3 = new Node(3, new Node(1, null, new Node(2, null, null)), null);
        if (predecessor(n3).val != 2) throw new AssertionError("ex2");
        // Random trees: the predecessor is the node just before cur in the inorder list.
        Random rnd = new Random(29);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, 0);
            List<Node> order = new ArrayList<>();
            in(x, order);
            for (int i = 0; i < order.size(); i++) {
                Node c = order.get(i);
                if (c.left != null && predecessor(c) != order.get(i - 1)) throw new AssertionError("random " + t);
            }
        }
    }
}
```

#### Solution: [Vary] Create And Remove One Thread (Author exercise)
<!-- id: mo-one-thread -->

**Approach.**
The method finds the predecessor `p` with a search that stops at `null` or at a reference equal to `cur`. If `p.right` is `null`, this is the first arrival. The method stores `cur` in `p.right` and returns `cur.left`. If `p.right` equals `cur`, this is the second arrival. The method sets `p.right` to `null` and returns `cur.right`. The invariant is that the single field `p.right` is the only memory of the first arrival, so the two cases are told apart by that field alone.

**Complexity.**
- **Time** is O(h), because the search follows one path down the left subtree.
- **Space** is O(1), because the method holds two references.

```java run
import java.util.*;

public final class OneThreadStep {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Performs one threaded step at a node that has a left child.
     * Time: O(h).
     * Space: O(1).
     * Invariant: p.right equals cur exactly between the first and the second arrival.
     */
    static Node step(Node cur) {
        Node p = cur.left;                                       // the search starts in the left subtree
        while (p.right != null && p.right != cur) p = p.right;   // stop at null or at a thread to cur
        if (p.right == null) {
            p.right = cur;                                       // first arrival: store the way back
            return cur.left;
        }
        p.right = null;                                          // second arrival: remove the thread
        return cur.right;
    }

    static void in(Node n, List<Node> out) { if (n == null) return; in(n.left, out); out.add(n); in(n.right, out); }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: the first call stores a thread from 3 to 4 and returns node 2.
        Node n3 = new Node(3, null, null), n2 = new Node(2, new Node(1, null, null), n3);
        Node n6 = new Node(6, null, null), n4 = new Node(4, n2, n6);
        if (step(n4) != n2 || n3.right != n4) throw new AssertionError("first call");
        // Example 2: the second call removes the thread and returns node 6.
        if (step(n4) != n6 || n3.right != null) throw new AssertionError("second call");
        // Random trees: the thread sits in the node just before cur in inorder.
        Random rnd = new Random(30);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, 0);
            List<Node> order = new ArrayList<>();
            in(x, order);
            for (int i = 0; i < order.size(); i++) {
                Node c = order.get(i);
                if (c.left == null) continue;
                Node prev = order.get(i - 1);
                Node oldRight = prev.right;                      // null by the predecessor property
                Node l = c.left, r = c.right;
                if (step(c) != l || prev.right != c || oldRight != null) throw new AssertionError("first " + t);
                if (step(c) != r || prev.right != null) throw new AssertionError("second " + t);
            }
        }
    }
}
```

#### Solution: [Boundary] No Left Child And Existing Thread (Author exercise)
<!-- id: mo-first-k -->

**Approach.**
The method runs the whole threaded walk and records a value only while fewer than `k` values are in the output. It does not stop at the `k`-th value. Stopping would leave every thread that is still stored in the tree, because a thread is removed only on the second arrival at its node. The walk therefore continues to the end, and every thread is removed on the way.

The three cases of the walk keep their meaning. A node with no left child is written at once and the walk moves along its `right` reference, which is a real child or a thread. A search that ends on `null` stores a thread. A search that ends on `cur` removes it and writes the node. The invariant is that every thread in the tree points to an ancestor whose left side is still being walked.

**Complexity.**
- **Time** is O(n), because the walk always runs to the end.
- **Space** is O(1) beyond the output of at most `k` values.

```java run
import java.util.*;

public final class FirstKValues {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the first k inorder values and leaves the tree unchanged.
     * Time: O(n), the walk always finishes.
     * Space: O(1) beyond the output.
     * Invariant: each stored thread points at an ancestor whose left side is in progress.
     */
    static List<Integer> firstK(Node root, int k, boolean stopEarly) {
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        while (cur != null) {                                    // one round per move
            if (cur.left == null) {
                if (out.size() < k) out.add(cur.val);            // record only the first k values
                if (stopEarly && out.size() == k) return out;    // unsafe: threads may remain
                cur = cur.right;
            } else {
                Node pred = cur.left;
                while (pred.right != null && pred.right != cur) pred = pred.right;
                if (pred.right == null) {
                    pred.right = cur;                            // first arrival
                    cur = cur.left;
                } else {
                    pred.right = null;                           // second arrival
                    if (out.size() < k) out.add(cur.val);
                    if (stopEarly && out.size() == k) return out;
                    cur = cur.right;
                }
            }
        }
        return out;
    }

    static void snap(Node n, List<Node> out) {
        if (n == null) return;
        out.add(n);
        out.add(n.left);
        out.add(n.right);
        snap(n.left, out);
        snap(n.right, out);
    }

    // Reads the structure without following any thread: a node list with both references, taken recursively.
    static List<Node> structure(Node root) {
        List<Node> out = new ArrayList<>();
        snap(root, out);
        return out;
    }

    static void in(Node n, List<Integer> o) { if (n == null) return; in(n.left, o); o.add(n.val); in(n.right, o); }

    static Node random(Random rnd, int d) {
        if (d > 5 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(2001) - 1000, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 9, left 5 with children 2 and 7, right 12, and k = 3.
        Node t = new Node(9, new Node(5, new Node(2, null, null), new Node(7, null, null)), new Node(12, null, null));
        List<Node> before = structure(t);
        if (!firstK(t, 3, false).equals(List.of(2, 5, 7))) throw new AssertionError("ex1");
        if (!structure(t).equals(before)) throw new AssertionError("tree changed");
        // Example 2: k = 0 gives the empty list.
        if (!firstK(t, 0, false).isEmpty()) throw new AssertionError("ex2");
        // k larger than the node count gives every value.
        if (!firstK(t, 99, false).equals(List.of(2, 5, 7, 9, 12))) throw new AssertionError("large k");
        // Stopping at the first value leaves threads in the tree: 2 points to 5 and 7 points to 9.
        Node u = new Node(9, new Node(5, new Node(2, null, null), new Node(7, null, null)), new Node(12, null, null));
        firstK(u, 1, true);
        if (u.left.left.right != u.left || u.left.right.right != u) throw new AssertionError("unsafe stop leaves threads");
        // Random trees: the output is a prefix of the inorder list and the structure is the same afterward.
        Random rnd = new Random(31);
        for (int i = 0; i < 600; i++) {
            Node x = random(rnd, 0);
            List<Integer> all = new ArrayList<>();
            in(x, all);
            int k = rnd.nextInt(all.size() + 3);
            List<Node> s = structure(x);
            List<Integer> got = firstK(x, k, false);
            if (!got.equals(all.subList(0, Math.min(k, all.size())))) throw new AssertionError("random " + i);
            if (!structure(x).equals(s)) throw new AssertionError("restored " + i);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: mo-inorder -->

**Approach.**
The method keeps `cur` and the output list. A node with no left child is written at once, and the walk moves along `right`. For a node with a left child, the method searches for the predecessor, stopping at `null` or at a reference equal to `cur`. A `null` means the first arrival, so the method stores the thread and moves left. A reference equal to `cur` means the second arrival, so it removes the thread, writes the node, and moves right.

The invariant is that every non-child `right` reference points to an ancestor whose left side is still being walked. When the walk ends, no such reference remains, so every `left` and `right` equals its original value. The checks below confirm two claims of the lesson. The stack method holds all nodes of a left chain at once. A walk that never removes its threads leaves a cycle.

**Complexity.**
- **Time** is O(n), because each right-going edge is followed by at most two predecessor searches.
- **Space** is O(1) beyond the output list.

```java run
import java.util.*;

public final class MorrisInorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the inorder values and restores every reference.
     * Time: O(n).
     * Space: O(1) beyond the output.
     * Invariant: a right reference that is not a child is a thread to an ancestor in progress.
     */
    static List<Integer> inorder(Node root, boolean removeThreads) {
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        while (cur != null) {                                    // one round per move
            if (cur.left == null) {
                out.add(cur.val);                                // no left side: write now
                cur = cur.right;                                 // a child or a thread
            } else {
                Node pred = cur.left;                            // search in the left subtree
                while (pred.right != null && pred.right != cur) pred = pred.right;
                if (pred.right == null) {
                    pred.right = cur;                            // first arrival: store a thread
                    cur = cur.left;
                } else {
                    if (removeThreads) pred.right = null;        // second arrival: remove the thread
                    else if (out.size() > 20) return out;        // the leaky variant would loop forever
                    out.add(cur.val);
                    cur = cur.right;
                }
            }
        }
        return out;
    }

    static int peakWaiting(Node root) {
        Deque<Node> waiting = new ArrayDeque<>();
        Node cur = root;
        int peak = 0;
        while (cur != null || !waiting.isEmpty()) {
            while (cur != null) { waiting.push(cur); cur = cur.left; }
            peak = Math.max(peak, waiting.size());
            cur = waiting.pop().right;
        }
        return peak;
    }

    static void collect(Node n, List<Node> out) {
        if (n == null) return;
        out.add(n);
        collect(n.left, out);
        collect(n.right, out);
    }

    static void recursive(Node n, List<Integer> out) {
        if (n == null) return;
        recursive(n.left, out);
        out.add(n.val);
        recursive(n.right, out);
    }

    static boolean hasCycle(Node root, Set<Node> path, Set<Node> done) {
        if (root == null || done.contains(root)) return false;
        if (!path.add(root)) return true;                        // a node reached twice on one path
        boolean c = hasCycle(root.left, path, done) || hasCycle(root.right, path, done);
        path.remove(root);
        done.add(root);
        return c;
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(201) - 100, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 7, left 3 with right child 5, right 9.
        Node t = new Node(7, new Node(3, null, new Node(5, null, null)), new Node(9, null, null));
        if (!inorder(t, true).equals(List.of(3, 5, 7, 9))) throw new AssertionError("ex1");
        // Example 2: the empty tree.
        if (!inorder(null, true).isEmpty()) throw new AssertionError("ex2");
        // The stack method holds the whole left chain: 5 nodes wait at once.
        Node chain = null;
        for (int i = 0; i < 5; i++) chain = new Node(i, chain, null);
        if (peakWaiting(chain) != 5) throw new AssertionError("peak");
        // The stack method on the five-node tree peaks at 3.
        Node five = new Node(4, new Node(2, new Node(1, null, null), new Node(3, null, null)), new Node(6, null, null));
        if (peakWaiting(five) != 3) throw new AssertionError("peak five");
        // A walk that never removes its threads leaves a cycle in the tree.
        Node leaky = new Node(4, new Node(2, new Node(1, null, null), new Node(3, null, null)), new Node(6, null, null));
        inorder(leaky, false);
        if (!hasCycle(leaky, new HashSet<>(), new HashSet<>())) throw new AssertionError("cycle");
        // Random trees: same values as the recursive walk, and every reference is unchanged.
        Random rnd = new Random(32);
        for (int k = 0; k < 600; k++) {
            Node x = random(rnd, 0);
            List<Node> nodes = new ArrayList<>();
            collect(x, nodes);
            List<Node> lefts = new ArrayList<>(), rights = new ArrayList<>();
            for (Node n : nodes) { lefts.add(n.left); rights.add(n.right); }
            List<Integer> want = new ArrayList<>();
            recursive(x, want);
            if (!inorder(x, true).equals(want)) throw new AssertionError("values " + k);
            for (int i = 0; i < nodes.size(); i++) {
                if (nodes.get(i).left != lefts.get(i) || nodes.get(i).right != rights.get(i)) throw new AssertionError("restored " + k);
            }
        }
    }
}
```
