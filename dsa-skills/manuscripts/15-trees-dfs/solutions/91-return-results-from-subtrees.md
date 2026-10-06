<!-- solutions-for: 91-return-results-from-subtrees -->
### Solutions For Returning Results From Subtrees

#### Solution: [Build] Maximum Depth With Deepest Leaf Count (LeetCode 104)
<!-- id: rr-depth-count -->

**Approach.**
Each call returns a record with the depth of its subtree in nodes and the number of leaves at that depth. A call on `null` returns two zeros. For a node, the call compares the two child depths. If one child is deeper, the node takes that child's count. If the depths are equal, the node adds the two counts. A node with two empty children has depth 1 and count 1. The equal case would give count 0 there, so the call replaces a count of 0 by 1 at that node.

The invariant is that the count belongs to the deepest level of exactly this subtree. The parent never merges counts of different depths.

**Complexity.**
- **Time** is O(n), because each node receives one call and the merge does constant work.
- **Space** is O(h) on the chain of pending calls, and each call holds one small record.

```java run
import java.util.*;

public final class DepthAndCount {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    record Depth(int depth, int count) {}

    /**
     * Returns the depth in nodes and the number of leaves at that depth.
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: count belongs to the deepest level of exactly this subtree.
     */
    static Depth deepest(Node node) {
        if (node == null) return new Depth(0, 0);                // an empty subtree has no leaves
        Depth l = deepest(node.left);
        Depth r = deepest(node.right);
        if (l.depth() > r.depth()) return new Depth(l.depth() + 1, l.count());   // only the left side reaches the deepest level
        if (r.depth() > l.depth()) return new Depth(r.depth() + 1, r.count());   // only the right side reaches it
        int count = l.count() + r.count();                       // equal depths: both sides contribute
        return new Depth(l.depth() + 1, count == 0 ? 1 : count); // two empty sides make this node the leaf
    }

    static int[] answer(Node root) {
        Depth d = deepest(root);
        return new int[] {d.depth(), d.count()};
    }

    // Oracle: level by level, the last level holds the deepest leaves.
    static int[] oracle(Node root) {
        if (root == null) return new int[] {0, 0};
        List<Node> level = List.of(root);
        int depth = 0;
        while (true) {                                           // one round per level
            depth++;
            List<Node> next = new ArrayList<>();
            for (Node n : level) {
                if (n.left != null) next.add(n.left);
                if (n.right != null) next.add(n.right);
            }
            if (next.isEmpty()) return new int[] {depth, level.size()};
            level = next;
        }
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 9, left 4 with left child 2, right 7 with right child 8 and then 1.
        Node t1 = new Node(9, new Node(4, new Node(2, null, null), null),
                new Node(7, null, new Node(8, null, new Node(1, null, null))));
        if (!Arrays.equals(answer(t1), new int[] {4, 1})) throw new AssertionError("ex1");
        // Example 2: root 5 with two leaves.
        if (!Arrays.equals(answer(new Node(5, new Node(3, null, null), new Node(8, null, null))), new int[] {2, 2})) throw new AssertionError("ex2");
        // The empty tree gives [0, 0], and a single node gives [1, 1].
        if (!Arrays.equals(answer(null), new int[] {0, 0}) || !Arrays.equals(answer(new Node(1, null, null)), new int[] {1, 1})) throw new AssertionError("small");
        // Random trees match the level-by-level oracle.
        Random rnd = new Random(37);
        for (int t = 0; t < 800; t++) {
            Node x = random(rnd, 0);
            if (!Arrays.equals(answer(x), oracle(x))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Diameter With Edge Costs (LeetCode 543)
<!-- id: rr-weighted-diameter -->

**Approach.**
Each call returns the cost of the best downward branch that starts at the edge above the node and ends anywhere below. That cost is the node's own `val` plus the larger branch cost of its two children, and it is 0 for `null`. The call also forms the cost of the path with the node on top, the sum of the two child branch costs. It folds that cost into a running maximum in a one-element array. The parent never receives the path cost, because a path that uses two branches cannot be extended.

The invariant is that the returned cost is a single branch, and the array holds the largest two-branch cost seen. The root's `val` is never added, because the root has no parent edge and nothing calls its branch.

**Complexity.**
- **Time** is O(n), because each node receives one call.
- **Space** is O(h) for the pending calls, plus one array cell.

```java run
import java.util.*;

public final class WeightedDiameter {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the best branch cost that includes the edge above node, and updates best[0].
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: the return value is one branch, best[0] is the largest two-branch cost.
     */
    static int branch(Node node, int[] best) {
        if (node == null) return 0;                              // an empty side costs nothing
        int l = branch(node.left, best);
        int r = branch(node.right, best);
        best[0] = Math.max(best[0], l + r);                      // the path with this node on top uses both branches
        return node.val + Math.max(l, r);                        // the parent extends one branch, through this edge
    }

    static int diameter(Node root) {
        int[] best = {0};                                        // a single node has cost 0
        branch(root, best);
        return best[0];
    }

    // Oracle: a search from every node over undirected weighted edges.
    static int oracle(Node root) {
        Map<Node, List<Object[]>> adj = new IdentityHashMap<>();
        List<Node> all = new ArrayList<>();
        Deque<Node> st = new ArrayDeque<>();
        st.push(root);
        adj.put(root, new ArrayList<>());
        while (!st.isEmpty()) {
            Node n = st.pop();
            all.add(n);
            for (Node c : new Node[] {n.left, n.right}) if (c != null) {
                adj.put(c, new ArrayList<>());
                adj.get(n).add(new Object[] {c, c.val});
                adj.get(c).add(new Object[] {n, c.val});
                st.push(c);
            }
        }
        int best = 0;
        for (Node s : all) best = Math.max(best, far(s, null, adj, 0));
        return best;
    }

    static int far(Node n, Node parent, Map<Node, List<Object[]>> adj, int dist) {
        int best = dist;
        for (Object[] e : adj.get(n)) if (e[0] != parent) best = Math.max(best, far((Node) e[0], n, adj, dist + (Integer) e[1]));
        return best;
    }

    static Node random(Random rnd, int d, boolean root) {
        if (d > 6 || (!root && rnd.nextInt(4) == 0)) return null;
        return new Node(root ? 0 : 1 + rnd.nextInt(100), random(rnd, d + 1, false), random(rnd, d + 1, false));
    }

    public static void main(String[] args) {
        // Example 1: root 0, left 4 with children 2 and 3, right 5; the best path is 3, 4, root, 5.
        Node t1 = new Node(0, new Node(4, new Node(2, null, null), new Node(3, null, null)), new Node(5, null, null));
        if (diameter(t1) != 12) throw new AssertionError("ex1");
        // Example 2: a single node costs 0.
        if (diameter(new Node(0, null, null)) != 0) throw new AssertionError("ex2");
        // A path that avoids the root can win: the root has one child whose subtree is heavier.
        Node t3 = new Node(0, new Node(1, new Node(50, null, null), new Node(60, null, null)), null);
        if (diameter(t3) != 110) throw new AssertionError("avoids root");
        // Random trees match the all-sources search.
        Random rnd = new Random(38);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, 0, true);
            if (diameter(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Balanced With Tolerance (LeetCode 110)
<!-- id: rr-tolerance -->

**Approach.**
The helper returns the height of a subtree when every node inside it keeps the allowed difference, and the sentinel `-1` otherwise. A call on `null` returns 0. A call on a node returns the sentinel at once if the left call returned it, then does the same for the right call. Only when both are real heights does it compare them. A difference above `k` returns the sentinel, and otherwise the call returns one plus the larger height. With `k = 0` the comparison accepts only equal heights.

The invariant is that the sentinel never takes part in a comparison, and that a real height is never negative. The tree passes exactly when the root's result is not the sentinel.

**Complexity.**
- **Time** is O(n), because each node receives at most one call.
- **Space** is O(h) for the pending calls.

```java run
import java.util.*;

public final class ToleranceBalance {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int FAIL = -1;

    /**
     * Returns the height, or FAIL when some node differs by more than k.
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: FAIL never takes part in a comparison.
     */
    static int height(Node node, int k) {
        if (node == null) return 0;                              // an empty side has height 0
        int l = height(node.left, k);
        if (l == FAIL) return FAIL;                              // a failure below decides the answer
        int r = height(node.right, k);
        if (r == FAIL) return FAIL;
        if (Math.abs(l - r) > k) return FAIL;                    // both heights are real, so compare them with k
        return 1 + Math.max(l, r);
    }

    static boolean balanced(Node root, int k) { return height(root, k) != FAIL; }

    // Oracle: the top-down check with a separate height method.
    static int h(Node n) { return n == null ? 0 : 1 + Math.max(h(n.left), h(n.right)); }

    static boolean oracle(Node n, int k) {
        if (n == null) return true;
        return Math.abs(h(n.left) - h(n.right)) <= k && oracle(n.left, k) && oracle(n.right, k);
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1 and 2: root 6, left 4 with a chain 2 then 1, right 8.
        Node t = new Node(6, new Node(4, new Node(2, new Node(1, null, null), null), null), new Node(8, null, null));
        if (balanced(t, 1)) throw new AssertionError("k = 1");
        if (!balanced(t, 2)) throw new AssertionError("k = 2");
        // The empty tree passes for every k, including 0.
        if (!balanced(null, 0)) throw new AssertionError("empty");
        // With k = 0 a root with one child fails, and a root with two leaves passes.
        if (balanced(new Node(1, new Node(2, null, null), null), 0)) throw new AssertionError("k = 0 one child");
        if (!balanced(new Node(1, new Node(2, null, null), new Node(3, null, null)), 0)) throw new AssertionError("k = 0 two leaves");
        // Random trees and random k match the top-down oracle.
        Random rnd = new Random(39);
        for (int i = 0; i < 800; i++) {
            Node x = random(rnd, 0);
            int k = rnd.nextInt(4);
            if (balanced(x, k) != oracle(x, k)) throw new AssertionError("random " + i);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: rr-two-node-path -->

**Approach.**
Each call returns the best sum of a downward branch that starts at its node and may stop at any node below. That sum is the node's value plus the larger of 0 and the two child branches, because a branch may stop at the node itself. A missing child is marked with a very negative number, so it never wins the maximum and never takes part in a sum.

The path with the node on top must contain at least two nodes, so it must use at least one child. With one child present, the path sum is the node's value plus that child's branch, even when the branch is negative. With both children present, the best path is the node's value plus the larger of the sum of both branches and each single branch. The call folds this value into a running maximum and returns only the single branch.

The invariant is that the returned number is one branch, and the maximum holds the best path of two or more nodes. The checks below confirm that returning the two-branch path to the parent gives a wrong answer.

**Complexity.**
- **Time** is O(n), because each node receives one call and does constant work.
- **Space** is O(h) for the pending calls, plus one array cell.

```java run
import java.util.*;

public final class TwoNodePathSum {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int ABSENT = Integer.MIN_VALUE / 4;             // far below any real branch sum

    /**
     * Returns the best branch sum from node downward and updates best[0].
     * Time: O(n).
     * Space: O(h) for the pending calls.
     * Invariant: the return value is one branch, best[0] is the best path with at least two nodes.
     */
    static int branch(Node node, int[] best, boolean returnPath) {
        int l = node.left == null ? ABSENT : branch(node.left, best, returnPath);
        int r = node.right == null ? ABSENT : branch(node.right, best, returnPath);
        int top = ABSENT;                                        // the best path of two or more nodes with node on top
        if (l != ABSENT || r != ABSENT) top = node.val + Math.max(l, r);       // at least one child is forced into the path
        if (l != ABSENT && r != ABSENT) top = Math.max(top, node.val + l + r);  // both branches, when both children exist
        best[0] = Math.max(best[0], top);
        int up = node.val + Math.max(0, Math.max(l, r));         // a branch may stop at this node
        return returnPath && top != ABSENT ? Math.max(up, top) : up;   // the wrong variant passes the two-branch path up
    }

    static int best(Node root, boolean returnPath) {
        int[] best = {Integer.MIN_VALUE};
        branch(root, best, returnPath);
        return best[0];
    }

    // Oracle: sum every path of two or more nodes by a search from each start node.
    static int oracle(Node root) {
        Map<Node, List<Node>> adj = new IdentityHashMap<>();
        List<Node> all = new ArrayList<>();
        Deque<Node> st = new ArrayDeque<>();
        st.push(root);
        adj.put(root, new ArrayList<>());
        while (!st.isEmpty()) {
            Node n = st.pop();
            all.add(n);
            for (Node c : new Node[] {n.left, n.right}) if (c != null) {
                adj.put(c, new ArrayList<>());
                adj.get(n).add(c);
                adj.get(c).add(n);
                st.push(c);
            }
        }
        int best = Integer.MIN_VALUE;
        for (Node s : all) for (Node m : adj.get(s)) best = Math.max(best, walk(m, s, adj, s.val + m.val));
        return best;
    }

    static int walk(Node n, Node parent, Map<Node, List<Node>> adj, int sum) {
        int best = sum;                                          // the path may stop here
        for (Node m : adj.get(n)) if (m != parent) best = Math.max(best, walk(m, n, adj, sum + m.val));
        return best;
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(21) - 10, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root -3 with children -5 and -2 gives -3 + -2.
        if (best(new Node(-3, new Node(-5, null, null), new Node(-2, null, null)), false) != -5) throw new AssertionError("ex1");
        // Example 2: root 10 with one child -4 gives 6, the only path of two nodes.
        if (best(new Node(10, new Node(-4, null, null), null), false) != 6) throw new AssertionError("ex2");
        // Returning the two-branch path to the parent overstates the answer on a chain with a fork below.
        Node t = new Node(1, new Node(2, new Node(3, null, null), new Node(4, null, null)), null);
        if (best(t, false) != 9 || best(t, true) <= 9) throw new AssertionError("false friend");
        // Random trees with at least two nodes match the all-sources search.
        Random rnd = new Random(40);
        for (int k = 0; k < 800; k++) {
            Node x = random(rnd, 0);
            if (x == null || (x.left == null && x.right == null)) continue;
            if (best(x, false) != oracle(x)) throw new AssertionError("random " + k);
        }
    }
}
```
