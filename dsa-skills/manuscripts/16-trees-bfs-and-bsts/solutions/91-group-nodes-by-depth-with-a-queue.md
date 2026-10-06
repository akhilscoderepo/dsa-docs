<!-- solutions-for: 91-group-nodes-by-depth-with-a-queue -->
### Solutions For Row Loops

#### Solution: [Build] Level Sums Of A Binary Tree (LeetCode 102)
<!-- id: tbc-level-sums -->

**Approach.**
The method runs the row loop and keeps one `long` accumulator for each pass. At the top of a pass it reads `queue.size()` and stores it. The inner loop removes exactly that many nodes, adds each value to the accumulator, and queues the non-null children. When the inner loop ends, the accumulator holds the sum of one depth, and the method appends it to the result and starts the next pass with a fresh accumulator. The accumulator is a `long`, because a row of 10^5 values near 10^9 reaches 10^14, which is far outside the `int` range. A recursive version fails on a very tall chain, while the loop keeps its nodes in a heap-based queue.

The invariant is that the queue holds exactly one depth at the top of each pass, and the accumulator starts at 0 for that depth.

**Complexity.**
- **Time** is O(n), because each node is queued once and removed once.
- **Space** is O(w) for the queue, where `w` is the widest row, plus O(h) for the result.

```java run
import java.util.*;

public final class LevelSums {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the sum of values at each depth.
     * Time: O(n), because each node is queued and removed once.
     * Space: O(w) for the queue, plus the result.
     * Invariant: the queue holds exactly one depth at the top of each pass.
     */
    static List<Long> levelSums(TreeNode root) {
        List<Long> result = new ArrayList<>();
        if (root == null) return result;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                        // the row boundary
            long row = 0;                                   // a long keeps large sums exact
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                row += node.val;
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            result.add(row);
        }
        return result;
    }

    /** Oracle: recursive walk that carries the depth. */
    static void walk(TreeNode node, int depth, List<Long> sums) {
        if (node == null) return;
        if (depth == sums.size()) sums.add(0L);
        sums.set(depth, sums.get(depth) + node.val);
        walk(node.left, depth + 1, sums);
        walk(node.right, depth + 1, sums);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(2001) - 1000));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(2001) - 1000);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        // Example 1: sums of the three rows.
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(3);
        r.right = new TreeNode(8);
        r.left.left = new TreeNode(1);
        r.left.right = new TreeNode(4);
        if (!levelSums(r).equals(List.of(5L, 11L, 5L))) throw new AssertionError("ex1");
        // Example 2: a row sum above the int range.
        TreeNode big = new TreeNode(1_000_000_000);
        big.left = new TreeNode(1_000_000_000);
        big.right = new TreeNode(1_000_000_000);
        if (!levelSums(big).equals(List.of(1_000_000_000L, 2_000_000_000L))) throw new AssertionError("ex2");
        if (!levelSums(null).isEmpty()) throw new AssertionError("empty");
        // Java claim: a recursive walk overflows the call stack on a very tall chain, and the loop does not.
        TreeNode chain = new TreeNode(1), tail = chain;
        for (int i = 1; i < 500_000; i++) { tail.right = new TreeNode(1); tail = tail.right; }
        if (levelSums(chain).size() != 500_000) throw new AssertionError("loop on chain");
        boolean overflowed = false;
        try { walk(chain, 0, new ArrayList<>()); } catch (StackOverflowError e) { overflowed = true; }
        if (!overflowed) throw new AssertionError("expected overflow");
        // Random trees must match the recursive oracle.
        Random rnd = new Random(1691);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<Long> want = new ArrayList<>();
            walk(x, 0, want);
            if (!levelSums(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Bottom-Up Zigzag Level Order (LeetCode 103)
<!-- id: tbc-bottom-up-zigzag -->

**Approach.**
The method keeps the queue order left to right and uses the pass counter as the depth. Each pass collects its row into an `ArrayDeque<Integer>`: for an even depth the method uses `addLast`, and for an odd depth it uses `addFirst`, so the row comes out reversed. The finished row is inserted at index 0 of the result, which puts the deepest row first at the end. Both rules read the depth, so the direction depends on the depth of the row and not on its place in the output. A row at depth 1 is still reversed, even though it ends up second from the end.

The invariant is that the queue order never changes, and only the placement into the row and the placement of the row depend on the depth.

**Complexity.**
- **Time** is O(n) for the rows, plus the cost of inserting each row at the front of the result, which is O(h^2) for h rows and fits within O(n) for the sizes allowed.
- **Space** is O(w) for the queue, plus the result.

```java run
import java.util.*;

public final class BottomUpZigzag {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the rows deepest first, with odd depths reading right to left.
     * Time: O(n) for the rows, plus front insertions into the result.
     * Space: O(w) for the queue, plus the result.
     * Invariant: queue order is always left to right; the depth chooses the placement.
     */
    static List<List<Integer>> bottomUpZigzag(TreeNode root) {
        LinkedList<List<Integer>> result = new LinkedList<>();
        if (root == null) return result;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        int depth = 0;                                      // the pass counter is the depth
        while (!queue.isEmpty()) {
            int size = queue.size();
            Deque<Integer> row = new ArrayDeque<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (depth % 2 == 0) row.addLast(node.val); else row.addFirst(node.val);   // odd depths reverse
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            result.addFirst(new ArrayList<>(row));          // the deepest row ends up first
            depth++;
        }
        return result;
    }

    static void dfs(TreeNode node, int depth, List<List<Integer>> out) {
        if (node == null) return;
        if (depth == out.size()) out.add(new ArrayList<>());
        out.get(depth).add(node.val);
        dfs(node.left, depth + 1, out);
        dfs(node.right, depth + 1, out);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(9)));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(9));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        // Example 1: the deepest row first, depth 1 reversed.
        TreeNode r = new TreeNode(3);
        r.left = new TreeNode(9);
        r.right = new TreeNode(20);
        r.right.left = new TreeNode(15);
        r.right.right = new TreeNode(7);
        if (!bottomUpZigzag(r).equals(List.of(List.of(15, 7), List.of(20, 9), List.of(3)))) throw new AssertionError("ex1");
        // Example 2: two rows below the root.
        TreeNode s = new TreeNode(1);
        s.left = new TreeNode(2);
        s.right = new TreeNode(3);
        s.left.left = new TreeNode(4);
        s.right.left = new TreeNode(5);
        if (!bottomUpZigzag(s).equals(List.of(List.of(4, 5), List.of(3, 2), List.of(1)))) throw new AssertionError("ex2");
        if (!bottomUpZigzag(null).isEmpty()) throw new AssertionError("empty");
        // Random trees must match rows from a recursive walk, reversed on odd depths and then listed bottom-up.
        Random rnd = new Random(1692);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<List<Integer>> rows = new ArrayList<>();
            dfs(x, 0, rows);
            for (int d = 1; d < rows.size(); d += 2) Collections.reverse(rows.get(d));
            Collections.reverse(rows);
            if (!bottomUpZigzag(x).equals(rows)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Right View Of The First K Rows (LeetCode 199)
<!-- id: tbc-right-view-k -->

**Approach.**
The outer loop runs while the queue is not empty and the pass counter is below `k`. Each pass stores the row size, removes that many nodes, and remembers the last removed node. After the inner loop the method appends that node's value to the view and increments the counter. The test `depth < k` runs before each pass, so `k = 0` runs no pass and returns an empty list, and a `k` larger than the height ends when the queue empties. Nodes discovered by the last allowed pass are never removed, which saves the work of the deeper rows.

The invariant is that the queue holds one whole row at the top of each pass, and the counter equals the number of rows already in the view.

**Complexity.**
- **Time** is O(m), where `m` is the number of nodes in the first `k` rows, plus the queue entries of the row after them.
- **Space** is O(w) for the queue.

```java run
import java.util.*;

public final class RightViewK {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the rightmost value of each of the first k rows.
     * Time: O(m) for the m nodes in the first k rows.
     * Space: O(w) for the queue.
     * Invariant: the counter equals the number of rows in the view.
     */
    static List<Integer> rightViewFirstK(TreeNode root, int k) {
        List<Integer> view = new ArrayList<>();
        if (root == null) return view;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        int depth = 0;
        while (!queue.isEmpty() && depth < k) {             // the second stopping rule reads the counter
            int size = queue.size();
            TreeNode last = null;
            for (int i = 0; i < size; i++) {
                last = queue.poll();
                if (last.left != null) queue.add(last.left);
                if (last.right != null) queue.add(last.right);
            }
            view.add(last.val);                             // the last node removed is the visible one
            depth++;
        }
        return view;
    }

    static void dfs(TreeNode node, int depth, List<List<Integer>> out) {
        if (node == null) return;
        if (depth == out.size()) out.add(new ArrayList<>());
        out.get(depth).add(node.val);
        dfs(node.left, depth + 1, out);
        dfs(node.right, depth + 1, out);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(9)));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(9));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        TreeNode r = new TreeNode(1);
        r.left = new TreeNode(2);
        r.right = new TreeNode(3);
        r.left.right = new TreeNode(5);
        r.right.right = new TreeNode(4);
        // Example 1: the first two rows give 1 and 3.
        if (!rightViewFirstK(r, 2).equals(List.of(1, 3))) throw new AssertionError("ex1");
        // Example 2: k = 0 gives an empty view.
        if (!rightViewFirstK(r, 0).isEmpty()) throw new AssertionError("ex2");
        // A k above the height gives every row.
        if (!rightViewFirstK(r, 10).equals(List.of(1, 3, 4))) throw new AssertionError("large k");
        // Random trees and every k must match the last entries of the first k rows from a recursive walk.
        Random rnd = new Random(1693);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<List<Integer>> rows = new ArrayList<>();
            dfs(x, 0, rows);
            for (int k = 0; k <= rows.size() + 2; k++) {
                List<Integer> want = new ArrayList<>();
                for (int d = 0; d < Math.min(k, rows.size()); d++) want.add(rows.get(d).get(rows.get(d).size() - 1));
                if (!rightViewFirstK(x, k).equals(want)) throw new AssertionError("t=" + t + " k=" + k);
            }
        }
    }
}
```

#### Solution: [Recognize] N-ary Tree Level Order Traversal (LeetCode 429)
<!-- id: tbc-nary-level-order -->

**Approach.**
The row loop does not change for an N-ary tree, and only the step that adds children changes. A node holds a list of children, so after removing a node the method calls `queue.addAll(node.children)`, which appends every child in list order. The stored size still marks the row boundary, because all children are added behind the current row. A null root returns an empty list before any queue exists. A node with no children adds nothing, and a node with many children adds all of them in one call.

The invariant is the same as in the binary case: the queue holds one depth at the top of each pass, and the children of the removed nodes land behind it in discovery order.

**Complexity.**
- **Time** is O(n), because each node is queued and removed once and each child link is read once.
- **Space** is O(w) for the queue, where `w` is the widest row.

```java run
import java.util.*;

public final class NaryLevelOrder {
    static final class Node {
        int val;
        List<Node> children = new ArrayList<>();
        Node(int val) { this.val = val; }
    }

    /**
     * Returns the values grouped by depth for an N-ary tree.
     * Time: O(n), because each node is queued and removed once.
     * Space: O(w) for the queue.
     * Invariant: the queue holds one depth at the top of each pass.
     */
    static List<List<Integer>> levelOrder(Node root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Deque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                        // the row boundary
            List<Integer> row = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                Node node = queue.poll();
                row.add(node.val);
                queue.addAll(node.children);                // every child, in list order
            }
            result.add(row);
        }
        return result;
    }

    static void dfs(Node node, int depth, List<List<Integer>> out) {
        if (depth == out.size()) out.add(new ArrayList<>());
        out.get(depth).add(node.val);
        for (Node c : node.children) dfs(c, depth + 1, out);   // children in list order keep each row ordered
    }

    static Node randomTree(Random rnd, int n) {
        List<Node> all = new ArrayList<>();
        all.add(new Node(rnd.nextInt(10)));
        while (all.size() < n) {
            Node p = all.get(rnd.nextInt(all.size()));
            Node c = new Node(rnd.nextInt(10));
            p.children.add(c);
            all.add(c);
        }
        return all.get(0);
    }

    public static void main(String[] args) {
        // Example 1: a root with three children, one of which has two children.
        Node r = new Node(1), a = new Node(3), b = new Node(2), c = new Node(4);
        r.children.addAll(List.of(a, b, c));
        a.children.addAll(List.of(new Node(5), new Node(6)));
        if (!levelOrder(r).equals(List.of(List.of(1), List.of(3, 2, 4), List.of(5, 6)))) throw new AssertionError("ex1");
        // Example 2: a single node.
        if (!levelOrder(new Node(7)).equals(List.of(List.of(7)))) throw new AssertionError("ex2");
        if (!levelOrder(null).isEmpty()) throw new AssertionError("empty");
        // Random trees with arbitrary child counts must match the recursive oracle.
        Random rnd = new Random(1694);
        for (int t = 0; t < 300; t++) {
            Node x = randomTree(rnd, 1 + rnd.nextInt(30));
            List<List<Integer>> want = new ArrayList<>();
            dfs(x, 0, want);
            if (!levelOrder(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```
