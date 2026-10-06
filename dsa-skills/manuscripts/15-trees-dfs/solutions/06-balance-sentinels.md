<!-- solutions-for: 06-balance-sentinels -->
### Solutions For One-Pass Balance Checks

#### Solution: [Build] Height Or Failure (Author exercise)
<!-- id: bs-height-or-fail -->

**Approach.**
The call returns the height of its subtree when every value in it is non-negative, and `-1` otherwise. A call on `null` returns 0. A call on a node first checks its own value, and a negative value returns `-1` at once. It then calls the left child, and if that result is `-1` it returns `-1` without touching the right child. The same rule applies to the right result. When both results are heights, the call returns one plus the larger.

The invariant is that `-1` appears only when a negative value exists in the subtree, and that a height is never negative. The sentinel therefore cannot be mistaken for an answer.

**Complexity.**
- **Time** is O(n), because each node receives at most one call.
- **Space** is O(h) for the pending calls, because the early exit never opens more calls than the height.

```java run
import java.util.*;

public final class HeightOrFail {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int visited;                                          // counts calls on real nodes, for the early-exit claim

    /**
     * Returns the height in nodes of a clean tree, or -1 when a negative value exists.
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: -1 means a negative value lies in the subtree, anything else is the exact height.
     */
    static int cleanHeight(Node node) {
        if (node == null) return 0;                              // an empty subtree is clean with height 0
        visited++;
        if (node.val < 0) return -1;                             // this node itself breaks the rule
        int l = cleanHeight(node.left);
        if (l == -1) return -1;                                  // a failed left side ends the call
        int r = cleanHeight(node.right);
        if (r == -1) return -1;                                  // a failed right side ends the call
        return 1 + Math.max(l, r);                               // both sides are clean
    }

    // Oracle: a plain height method plus a separate scan for a negative value.
    static int height(Node n) { return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right)); }

    static boolean hasNegative(Node n) { return n != null && (n.val < 0 || hasNegative(n.left) || hasNegative(n.right)); }

    static int count(Node n) { return n == null ? 0 : 1 + count(n.left) + count(n.right); }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(21) - 2, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 4, left 2, right 7 with right child 9 gives height 3.
        Node t1 = new Node(4, new Node(2, null, null), new Node(7, null, new Node(9, null, null)));
        if (cleanHeight(t1) != 3) throw new AssertionError("ex1");
        // Example 2: a negative left child gives -1.
        if (cleanHeight(new Node(4, new Node(-2, null, null), new Node(7, null, null))) != -1) throw new AssertionError("ex2");
        // The empty tree is clean with height 0.
        if (cleanHeight(null) != 0) throw new AssertionError("empty");
        // A failed left child skips the right subtree: only the root and the left child are visited.
        Node big = new Node(1, new Node(-1, null, null), new Node(2, new Node(3, null, null), new Node(4, null, null)));
        visited = 0;
        if (cleanHeight(big) != -1 || visited != 2) throw new AssertionError("early exit " + visited);
        // Random trees match the separate height and scan.
        Random rnd = new Random(21);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, 0);
            int want = hasNegative(x) ? -1 : height(x);
            if (cleanHeight(x) != want) throw new AssertionError("random " + t);
            visited = 0;
            cleanHeight(x);
            if (visited > count(x)) throw new AssertionError("visits " + t);
        }
    }
}
```

#### Solution: [Vary] Detect Local Imbalance (Author exercise)
<!-- id: bs-first-bad -->

**Approach.**
The helper returns a height or the sentinel `-1`, and it stores the value of the first failing node in a one-element array. A call on `null` returns 0. A call on a node calls the left child and returns `-1` if that result is `-1`, then does the same for the right child. Only when both results are heights does the call compare them. If the difference is more than one, it stores its own value in the array and returns `-1`.

The first failure in finishing order is stored, because every caller above returns at once and never stores a second value. The invariant is that the array is empty until a node fails its own comparison and holds that node's value afterward.

**Complexity.**
- **Time** is O(n), because each node receives at most one call.
- **Space** is O(h) for the pending calls, plus one array cell.

```java run
import java.util.*;

public final class FirstBadNode {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int FAIL = -1;

    /**
     * Returns the height, or FAIL after storing the first failing node in bad[0].
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: bad[0] is set only by the first node whose own comparison fails.
     */
    static int checked(Node node, int[] bad) {
        if (node == null) return 0;                              // an empty subtree has height 0
        int l = checked(node.left, bad);
        if (l == FAIL) return FAIL;                              // a failure below was already stored
        int r = checked(node.right, bad);
        if (r == FAIL) return FAIL;
        if (Math.abs(l - r) > 1) { bad[0] = node.val; return FAIL; }   // this node is the first failure
        return 1 + Math.max(l, r);
    }

    static int firstBad(Node root) {
        int[] bad = {-1};                                        // -1 means that no node failed
        checked(root, bad);
        return bad[0];
    }

    // Oracle: list the nodes in finishing order and test each with separate height calls.
    static int height(Node n) { return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right)); }

    static void post(Node n, List<Node> out) {
        if (n == null) return;
        post(n.left, out);
        post(n.right, out);
        out.add(n);
    }

    static int oracle(Node root) {
        List<Node> order = new ArrayList<>();
        post(root, order);
        for (Node n : order) if (Math.abs(height(n.left) - height(n.right)) > 1) return n.val;
        return -1;
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(1001), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 6, left 4 with chain 2 then 1, right 8; the first failing node is 4.
        Node t1 = new Node(6, new Node(4, new Node(2, new Node(1, null, null), null), null), new Node(8, null, null));
        if (firstBad(t1) != 4) throw new AssertionError("ex1");
        // Example 2: root 5 with children 3 and 8 passes everywhere.
        if (firstBad(new Node(5, new Node(3, null, null), new Node(8, null, null))) != -1) throw new AssertionError("ex2");
        // The empty tree has no failing node.
        if (firstBad(null) != -1) throw new AssertionError("empty");
        // A failure above the first one must not hide it: the root also fails, but 4 is reported.
        Node deep = new Node(9, new Node(4, new Node(2, new Node(1, null, null), null), null), null);
        if (firstBad(deep) != 4) throw new AssertionError("hidden");
        // Random trees match the finishing-order oracle.
        Random rnd = new Random(22);
        for (int t = 0; t < 800; t++) {
            Node x = random(rnd, 0);
            if (firstBad(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Tree Height (Author exercise)
<!-- id: bs-empty-height -->

**Approach.**
With heights in edges, the empty tree has height -1 and a leaf has height 0. The value -1 is therefore a real height, and it cannot also mean failure. The method uses `Integer.MIN_VALUE` as the sentinel, which no real height can equal. A call on `null` returns -1. A call on a node returns the sentinel if either child returns it. It also returns the sentinel if the two heights differ by more than one. Otherwise it returns one plus the larger height.

The invariant is that the sentinel lies below every real height. The comparison of two real heights never overflows, because both lie between -1 and n.

**Complexity.**
- **Time** is O(n), because each node receives at most one call.
- **Space** is O(h) for the pending calls.

```java run
import java.util.*;

public final class EdgeHeightBalance {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int FAIL = Integer.MIN_VALUE;                   // below every real height
    static final int WRONG_FAIL = -1;                            // collides with the height of the empty tree

    /**
     * Returns the height in edges, or FAIL when some node breaks the rule.
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: FAIL is below every real height, which starts at -1.
     */
    static int edgeHeight(Node node) {
        if (node == null) return -1;                             // an empty subtree has height -1 in edges
        int l = edgeHeight(node.left);
        if (l == FAIL) return FAIL;                              // a failed left side ends the call
        int r = edgeHeight(node.right);
        if (r == FAIL) return FAIL;                              // a failed right side ends the call
        if (Math.abs(l - r) > 1) return FAIL;                    // both heights are real, so compare them
        return 1 + Math.max(l, r);                               // edges to the deepest leaf
    }

    static boolean isBalanced(Node root) { return edgeHeight(root) != FAIL; }

    // The same method with the sentinel -1: the empty tree now looks like a failure.
    static int brokenHeight(Node node) {
        if (node == null) return -1;
        int l = brokenHeight(node.left);
        if (l == WRONG_FAIL) return WRONG_FAIL;
        int r = brokenHeight(node.right);
        if (r == WRONG_FAIL) return WRONG_FAIL;
        if (Math.abs(l - r) > 1) return WRONG_FAIL;
        return 1 + Math.max(l, r);
    }

    // Oracle: top-down check with a separate height method in edges.
    static int height(Node n) { return n == null ? -1 : 1 + Math.max(height(n.left), height(n.right)); }

    static boolean oracle(Node n) {
        if (n == null) return true;
        return Math.abs(height(n.left) - height(n.right)) <= 1 && oracle(n.left) && oracle(n.right);
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: the empty tree is balanced.
        if (!isBalanced(null)) throw new AssertionError("empty");
        // Example 2: root 1 with left child 2 that has left child 3 is not balanced.
        if (isBalanced(new Node(1, new Node(2, new Node(3, null, null), null), null))) throw new AssertionError("ex2");
        // A single node has height 0 in edges.
        if (edgeHeight(new Node(1, null, null)) != 0) throw new AssertionError("single height");
        // The sentinel -1 breaks the check: a single node would look like a failure.
        if (brokenHeight(new Node(1, null, null)) != WRONG_FAIL) throw new AssertionError("collision");
        // Random trees match the top-down oracle.
        Random rnd = new Random(23);
        for (int t = 0; t < 800; t++) {
            Node x = random(rnd, 0);
            if (isBalanced(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Balanced Binary Tree (LeetCode 110)
<!-- id: bs-balanced -->

**Approach.**
One postorder pass returns the height of a subtree when every node in it passes, and the sentinel `-1` otherwise. A call on `null` returns 0. A call on a node returns the sentinel as soon as a child returns it, so the right side is skipped after a left failure. When both children return heights, the call compares them, returns the sentinel for a difference above one, and otherwise returns one plus the larger height. The tree is balanced exactly when the root's result is not the sentinel.

The invariant is that a returned height is exact and that the sentinel never takes part in the comparison. The check below also confirms the cost claim of the lesson. The top-down method visits a perfect tree of height 10 exactly `(k - 2) * 2^k + 2` times, which is far above n.

**Complexity.**
- **Time** is O(n), because each node receives at most one call.
- **Space** is O(h) for the pending calls.

```java run
import java.util.*;

public final class BalancedTree {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int FAIL = -1;
    static long heightVisits;                                    // counts node visits of the top-down method

    /**
     * Returns the height in nodes, or FAIL when some node breaks the rule.
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: a result other than FAIL is the exact height of the subtree.
     */
    static int checkedHeight(Node node) {
        if (node == null) return 0;                              // an empty subtree has height 0
        int l = checkedHeight(node.left);
        if (l == FAIL) return FAIL;                              // skip the right side after a left failure
        int r = checkedHeight(node.right);
        if (r == FAIL) return FAIL;
        if (Math.abs(l - r) > 1) return FAIL;                    // both heights are real, so compare them
        return 1 + Math.max(l, r);
    }

    static boolean isBalanced(Node root) { return checkedHeight(root) != FAIL; }

    // The same method without the two sentinel checks: -1 acts like a real height.
    static int unchecked(Node node) {
        if (node == null) return 0;
        int l = unchecked(node.left), r = unchecked(node.right);
        if (Math.abs(l - r) > 1) return FAIL;
        return 1 + Math.max(l, r);
    }

    // Oracle: the top-down method with a separate height call at every node.
    static int height(Node n) {
        if (n == null) return 0;
        heightVisits++;
        return 1 + Math.max(height(n.left), height(n.right));
    }

    static boolean oracle(Node n) {
        if (n == null) return true;
        return Math.abs(height(n.left) - height(n.right)) <= 1 && oracle(n.left) && oracle(n.right);
    }

    static Node perfect(int k) { return k == 0 ? null : new Node(1, perfect(k - 1), perfect(k - 1)); }

    static Node random(Random rnd, int d) {
        if (d > 8 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 5, left 3 with left child 1, right 8 with children 7 and 9.
        Node t1 = new Node(5, new Node(3, new Node(1, null, null), null), new Node(8, new Node(7, null, null), new Node(9, null, null)));
        if (!isBalanced(t1)) throw new AssertionError("ex1");
        // Example 2: root 6 with 4 and 8, where 4 has a chain 2 then 1.
        Node t2 = new Node(6, new Node(4, new Node(2, new Node(1, null, null), null), null), new Node(8, null, null));
        if (isBalanced(t2)) throw new AssertionError("ex2");
        // The empty tree is balanced.
        if (!isBalanced(null)) throw new AssertionError("empty");
        // Without the sentinel checks a failed left side (-1) against an empty right side (0) looks valid.
        Node hidden = new Node(9, new Node(4, new Node(2, new Node(1, null, null), null), null), null);
        if (isBalanced(hidden) || unchecked(hidden) == FAIL) throw new AssertionError("unchecked comparison");
        // The top-down method visits a perfect tree of height 10 exactly (k - 2) * 2^k + 2 times.
        heightVisits = 0;
        oracle(perfect(10));
        if (heightVisits != 8L * 1024 + 2) throw new AssertionError("visits " + heightVisits);
        // Random trees match the top-down oracle.
        Random rnd = new Random(24);
        for (int t = 0; t < 800; t++) {
            Node x = random(rnd, 0);
            if (isBalanced(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```
