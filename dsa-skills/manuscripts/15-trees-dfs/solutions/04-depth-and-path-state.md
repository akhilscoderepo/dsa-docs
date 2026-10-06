<!-- solutions-for: 04-depth-and-path-state -->
### Solutions For Depth And Path State

#### Solution: [Build] Maximum Depth Of Binary Tree (LeetCode 104)
<!-- id: dp-height -->

**Approach.**
Each call returns the number of nodes on the longest downward path in its own subtree. A call on `null` returns 0. A call on a node asks both children for their heights and returns one more than the larger answer. The invariant is that a return value is complete the moment the call returns, so the parent only compares two numbers and never looks into the child subtree.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives one call.
- **Space** is O(h) for the call stack, where h is the height of the tree.

```java run
import java.util.*;

public final class MaxDepth {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the number of nodes on the longest downward path.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: the result describes exactly the subtree of node.
     */
    static int depth(Node node) {
        if (node == null) return 0;                      // the empty tree has no nodes on any path
        int left = depth(node.left);                     // upward state of the left subtree
        int right = depth(node.right);                   // upward state of the right subtree
        return Math.max(left, right) + 1;                // the taller side plus this node
    }

    // Oracle: level-by-level count with a queue.
    static int oracle(Node root) {
        if (root == null) return 0;
        int levels = 0;
        Deque<Node> q = new ArrayDeque<>();
        q.add(root);
        while (!q.isEmpty()) {                           // one round per level
            levels++;
            for (int k = q.size(); k > 0; k--) {
                Node n = q.poll();
                if (n.left != null) q.add(n.left);
                if (n.right != null) q.add(n.right);
            }
        }
        return levels;
    }

    static Node random(Random rnd, int d) {
        if (d > 8 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 9, left 4 with left child 2, right 7 with right child 8 and then 1.
        Node t1 = new Node(9, new Node(4, new Node(2, null, null), null),
                new Node(7, null, new Node(8, null, new Node(1, null, null))));
        if (depth(t1) != 4) throw new AssertionError("ex1");
        // Example 2: root 3 with left child 1.
        if (depth(new Node(3, new Node(1, null, null), null)) != 2) throw new AssertionError("ex2");
        // The empty tree has depth 0, and a single node has depth 1.
        if (depth(null) != 0 || depth(new Node(1, null, null)) != 1) throw new AssertionError("small");
        // Random trees match the level-by-level oracle.
        Random rnd = new Random(13);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            if (depth(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Path Sum (LeetCode 112)
<!-- id: dp-path-sum -->

**Approach.**
The call receives the part of the target that its subtree must still supply. A call on `null` returns `false`, because a missing child ends no route. A call on a node subtracts its own value from the amount. At a leaf the call returns whether the new amount is zero. At any other node the call returns `true` if either child call returns `true`. The invariant is that `remaining` equals the target minus the values on the route above the node, so no list is needed.

The amount is an `int` passed by value, so a sibling call is never affected by the first child call and nothing needs undoing.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives at most one call.
- **Space** is O(h) for the call stack, and no list is stored.

```java run
import java.util.*;

public final class PathSum {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Tells whether some root-to-leaf path sums to the amount.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: remaining is the target minus the route above node.
     */
    static boolean hasPathSum(Node node, int remaining) {
        if (node == null) return false;                          // a missing child ends no route
        int left = remaining - node.val;                         // the amount that the children must still supply
        if (node.left == null && node.right == null) return left == 0;   // only a leaf can close a route
        return hasPathSum(node.left, left) || hasPathSum(node.right, left);   // either side may match
    }

    // Oracle: enumerate every root-to-leaf sum with an explicit stack.
    static boolean oracle(Node root, int target) {
        if (root == null) return false;
        Deque<Object[]> stack = new ArrayDeque<>();
        stack.push(new Object[] {root, 0});
        while (!stack.isEmpty()) {
            Object[] top = stack.pop();
            Node n = (Node) top[0];
            int sum = (Integer) top[1] + n.val;
            if (n.left == null && n.right == null && sum == target) return true;
            if (n.left != null) stack.push(new Object[] {n.left, sum});
            if (n.right != null) stack.push(new Object[] {n.right, sum});
        }
        return false;
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(7) - 3, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // The shared tree: root 8, left 3 with children 1 and 6, right 10.
        Node t = new Node(8, new Node(3, new Node(1, null, null), new Node(6, null, null)), new Node(10, null, null));
        // Example 1: target 12 matches the route 8, 3, 1.
        if (!hasPathSum(t, 12)) throw new AssertionError("ex1");
        // Example 2: target 11 is reached at the node 3, which is not a leaf.
        if (hasPathSum(t, 11)) throw new AssertionError("ex2");
        // The empty tree has no path, even for target 0.
        if (hasPathSum(null, 0)) throw new AssertionError("empty");
        // A single node matches only its own value.
        if (!hasPathSum(new Node(5, null, null), 5) || hasPathSum(new Node(5, null, null), 4)) throw new AssertionError("single");
        // Random trees must match the explicit enumeration.
        Random rnd = new Random(14);
        for (int k = 0; k < 800; k++) {
            Node x = random(rnd, 0);
            int target = rnd.nextInt(15) - 7;
            if (hasPathSum(x, target) != oracle(x, target)) throw new AssertionError("random " + k);
        }
    }
}
```

#### Solution: [Boundary] Leaf Versus Internal Match (Author exercise)
<!-- id: dp-leaf-count -->

**Approach.**
The method has the same shape as the existence check, but it adds the answers of the two children and never returns early. A call on `null` returns 0. At a leaf the call returns 1 if the new remaining amount is 0, and 0 otherwise. At any other node the call returns the sum of its two child counts. A node with one child passes the `null` side through the first base case, so it adds 0 for that side.

The invariant is that a call returns the number of matching leaf routes in its own subtree, given the amount that the route above it left over.

**Complexity.**
- **Time** is O(n), because every node is visited once and no call returns early.
- **Space** is O(h) for the call stack.

```java run
import java.util.*;

public final class LeafPathCount {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Counts root-to-leaf paths that sum to the amount.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: the result counts matching leaf routes of this subtree.
     */
    static int count(Node node, int remaining) {
        if (node == null) return 0;                              // a missing child ends no route
        int left = remaining - node.val;                         // the amount for the children
        if (node.left == null && node.right == null) return left == 0 ? 1 : 0;   // only a leaf closes a route
        return count(node.left, left) + count(node.right, left); // add both sides, no early exit
    }

    // Oracle: collect every leaf-route sum into a list, then count the matches.
    static int oracle(Node root, int target) {
        List<Integer> sums = new ArrayList<>();
        collect(root, 0, sums);
        int c = 0;
        for (int s : sums) if (s == target) c++;
        return c;
    }

    static void collect(Node n, int sum, List<Integer> sums) {
        if (n == null) return;
        if (n.left == null && n.right == null) { sums.add(sum + n.val); return; }
        collect(n.left, sum + n.val, sums);
        collect(n.right, sum + n.val, sums);
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(7) - 3, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 5 with only a left child 3 and target 5; the root is not a leaf.
        if (count(new Node(5, new Node(3, null, null), null), 5) != 0) throw new AssertionError("ex1");
        // Example 2: root 2 with two children 3 and target 5 gives two matches.
        if (count(new Node(2, new Node(3, null, null), new Node(3, null, null)), 5) != 2) throw new AssertionError("ex2");
        // The empty tree gives 0, even for target 0.
        if (count(null, 0) != 0) throw new AssertionError("empty");
        // A single node matches its own value once.
        if (count(new Node(4, null, null), 4) != 1) throw new AssertionError("single");
        // Random trees must match the collected sums.
        Random rnd = new Random(15);
        for (int k = 0; k < 800; k++) {
            Node x = random(rnd, 0);
            int target = rnd.nextInt(15) - 7;
            if (count(x, target) != oracle(x, target)) throw new AssertionError("random " + k);
        }
    }
}
```

#### Solution: [Recognize] Path Sum II (LeetCode 113)
<!-- id: dp-path-list -->

**Approach.**
The method keeps one shared list for the current route and passes the remaining amount by value. A call adds its node to the list before it looks at the children. At a leaf with remaining amount 0, the call stores a copy of the list, because the shared list changes later. The call then runs both child calls and removes the last entry of the list by index. That removal is the backtracking step, and it runs for every node, matching or not.

The invariant is that on entry to a call the list holds exactly the route above the node, and on exit it holds that same route again.

**Complexity.**
- **Time** is O(n * h) in the worst case, because each stored route costs up to h to copy, and there are at most n leaves.
- **Space** is O(h) for the call stack and the shared list, plus the stored answers.

```java run
import java.util.*;

public final class PathSumTwo {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Collects every root-to-leaf route that sums to the target.
     * Time: O(n * h), copying a route costs up to h.
     * Space: O(h) beside the answers.
     * Invariant: the list equals the route above the node on entry and on exit.
     */
    static void walk(Node node, int remaining, List<Integer> route, List<List<Integer>> out, boolean copy) {
        if (node == null) return;                                // a missing child ends no route
        route.add(node.val);                                     // extend the shared list before the children
        int left = remaining - node.val;                         // the amount for the children, passed by value
        if (node.left == null && node.right == null && left == 0) {
            out.add(copy ? new ArrayList<>(route) : route);      // a copy keeps the route as it is now
        }
        walk(node.left, left, route, out, copy);
        walk(node.right, left, route, out, copy);
        route.remove(route.size() - 1);                          // backtrack by index after both child calls
    }

    static List<List<Integer>> paths(Node root, int target) {
        List<List<Integer>> out = new ArrayList<>();
        walk(root, target, new ArrayList<>(), out, true);
        return out;
    }

    // Oracle: explicit stack that carries a private route copy for every node.
    static List<List<Integer>> oracle(Node root, int target) {
        List<List<Integer>> out = new ArrayList<>();
        if (root == null) return out;
        Deque<Object[]> stack = new ArrayDeque<>();
        stack.push(new Object[] {root, new ArrayList<Integer>()});
        while (!stack.isEmpty()) {
            Object[] top = stack.pop();
            Node n = (Node) top[0];
            @SuppressWarnings("unchecked") List<Integer> r = new ArrayList<>((List<Integer>) top[1]);
            r.add(n.val);
            int sum = 0;
            for (int v : r) sum += v;
            if (n.left == null && n.right == null && sum == target) out.add(r);
            if (n.right != null) stack.push(new Object[] {n.right, r});
            if (n.left != null) stack.push(new Object[] {n.left, r});
        }
        return out;
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(7) - 3, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        Node t = new Node(8, new Node(3, new Node(1, null, null), new Node(6, null, null)), new Node(10, null, null));
        // Example 1: target 17 gives the single route 8, 3, 6.
        if (!paths(t, 17).equals(List.of(List.of(8, 3, 6)))) throw new AssertionError("ex1");
        // Example 2: root 1 with two children 2 and target 3 gives two equal routes.
        Node e = new Node(1, new Node(2, null, null), new Node(2, null, null));
        if (!paths(e, 3).equals(List.of(List.of(1, 2), List.of(1, 2)))) throw new AssertionError("ex2");
        // The empty tree and a missing target give the empty answer.
        if (!paths(null, 0).isEmpty() || !paths(t, 99).isEmpty()) throw new AssertionError("empty");
        // Storing the shared list itself keeps a reference, and backtracking empties it afterward.
        List<List<Integer>> aliased = new ArrayList<>();
        walk(t, 17, new ArrayList<>(), aliased, false);
        if (aliased.size() != 1 || !aliased.get(0).isEmpty()) throw new AssertionError("aliasing");
        // remove(Integer) deletes the first equal value, not the last entry.
        List<Integer> r = new ArrayList<>(List.of(3, 5, 3));
        r.remove(Integer.valueOf(3));
        if (!r.equals(List.of(5, 3))) throw new AssertionError("remove by value");
        // Random trees must match the oracle in content and order.
        Random rnd = new Random(16);
        for (int k = 0; k < 800; k++) {
            Node x = random(rnd, 0);
            int target = rnd.nextInt(15) - 7;
            if (!paths(x, target).equals(oracle(x, target))) throw new AssertionError("random " + k);
        }
    }
}
```
