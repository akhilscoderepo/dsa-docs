<!-- solutions-for: 01-levels-zigzag-and-views -->
### Solutions For Level Traversal

#### Solution: [Build] Binary Tree Level Order Traversal (LeetCode 102)
<!-- id: tb-level-order -->

**Approach.**
The method puts the root into an `ArrayDeque` and repeats one outer pass per depth. At the top of each pass the queue holds exactly the nodes of one depth, so the method reads `queue.size()` once and stores it. The inner loop removes that many nodes, appends each value to the level list, and queues the non-null children behind the level. Those children form the next depth, and the stored size keeps them out of the current pass. A null root returns early because `ArrayDeque` rejects null elements.

The invariant is that the queue holds one whole depth at the top of every pass. The stored size preserves it, and the empty queue ends the loop after the deepest level.

**Complexity.**
- **Time** is O(n), because each node is queued once and removed once, and each removal does constant work.
- **Space** is O(w) for the queue, where `w` is the widest level, plus the output lists.

```java run
import java.util.*;

public final class LevelOrder {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the node values grouped by depth, left to right.
     * Time: O(n), because every node is queued and removed once.
     * Space: O(w) for the queue, where w is the widest level.
     * Invariant: at the top of each pass the queue holds exactly one depth.
     */
    static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;                  // ArrayDeque cannot hold null
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        // One pass per depth; the loop ends when no node waits.
        while (!queue.isEmpty()) {
            int size = queue.size();                      // fixed before any removal of this depth
            List<Integer> level = new ArrayList<>(size);
            // Exactly size removals belong to this depth.
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.add(node.left);     // child joins the next depth
                if (node.right != null) queue.add(node.right);
            }
            result.add(level);
        }
        return result;
    }

    /** Oracle: recursive walk that appends each value to the list of its depth. */
    static void dfs(TreeNode node, int depth, List<List<Integer>> out) {
        if (node == null) return;
        if (depth == out.size()) out.add(new ArrayList<>());
        out.get(depth).add(node.val);
        dfs(node.left, depth + 1, out);                   // left subtree first keeps left-to-right order
        dfs(node.right, depth + 1, out);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        TreeNode root = new TreeNode(rnd.nextInt(7) - 3);
        all.add(root);
        // Attach each new node to a random node that still has a free child slot.
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(7) - 3);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    public static void main(String[] args) {
        // Example 1: the five-node tree from the statement.
        TreeNode r = new TreeNode(3);
        r.left = new TreeNode(9);
        r.right = new TreeNode(20);
        r.right.left = new TreeNode(15);
        r.right.right = new TreeNode(7);
        if (!levelOrder(r).equals(List.of(List.of(3), List.of(9, 20), List.of(15, 7)))) throw new AssertionError("ex1");
        // Example 2: a zigzag chain gives one value per level.
        TreeNode c = new TreeNode(1);
        c.left = new TreeNode(2);
        c.left.right = new TreeNode(3);
        if (!levelOrder(c).equals(List.of(List.of(1), List.of(2), List.of(3)))) throw new AssertionError("ex2");
        // The empty tree gives an empty outer list.
        if (!levelOrder(null).isEmpty()) throw new AssertionError("empty");
        // Java claim: ArrayDeque rejects a null element.
        boolean threw = false;
        try { new ArrayDeque<TreeNode>().add(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("null deque");
        // Random trees must match the recursive oracle.
        Random rnd = new Random(1601);
        for (int t = 0; t < 400; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<List<Integer>> want = new ArrayList<>();
            dfs(x, 0, want);
            if (!levelOrder(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Binary Tree Zigzag Level Order Traversal (LeetCode 103)
<!-- id: tb-zigzag -->

**Approach.**
The queue logic is the same as in the plain traversal, so the nodes still leave the queue from left to right in every level. Only the placement of each value changes. A flag records whether the current depth reads from right to left. The method collects each level in an `ArrayDeque<Integer>`, where `addLast` keeps the arrival order and `addFirst` reverses it. After the inner loop the method copies the deque into a list and flips the flag.

The invariant is that the queue order never depends on the flag. The flag affects only the output, which is why a reversal can never lose a child.

**Complexity.**
- **Time** is O(n), because each node is queued once and each value is placed in constant time.
- **Space** is O(w) for the queue and the level buffer, plus the output.

```java run
import java.util.*;

public final class Zigzag {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the values by depth, alternating left-to-right and right-to-left.
     * Time: O(n), because each node is queued and placed once.
     * Space: O(w) for the queue and the level buffer.
     * Invariant: queue order is always left to right; only placement depends on the flag.
     */
    static List<List<Integer>> zigzag(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        boolean rightToLeft = false;                      // depth 0 reads left to right
        while (!queue.isEmpty()) {
            int size = queue.size();                      // level boundary
            Deque<Integer> level = new ArrayDeque<>();
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (rightToLeft) level.addFirst(node.val);        // later nodes land in front
                else level.addLast(node.val);                     // later nodes land behind
                if (node.left != null) queue.add(node.left);      // enqueue order never changes
                if (node.right != null) queue.add(node.right);
            }
            result.add(new ArrayList<>(level));
            rightToLeft = !rightToLeft;                   // the next depth reads the other way
        }
        return result;
    }

    /** Oracle: plain level lists from a recursive walk, with each odd depth reversed. */
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
        TreeNode root = new TreeNode(rnd.nextInt(7) - 3);
        all.add(root);
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(7) - 3);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    public static void main(String[] args) {
        // Example 1: the five-node tree reverses depth 1.
        TreeNode r = new TreeNode(3);
        r.left = new TreeNode(9);
        r.right = new TreeNode(20);
        r.right.left = new TreeNode(15);
        r.right.right = new TreeNode(7);
        if (!zigzag(r).equals(List.of(List.of(3), List.of(20, 9), List.of(15, 7)))) throw new AssertionError("ex1");
        // Example 2: a complete tree with values 1 to 7.
        TreeNode[] n = new TreeNode[8];
        for (int i = 1; i <= 7; i++) n[i] = new TreeNode(i);
        for (int i = 1; i <= 3; i++) { n[i].left = n[2 * i]; n[i].right = n[2 * i + 1]; }
        if (!zigzag(n[1]).equals(List.of(List.of(1), List.of(3, 2), List.of(4, 5, 6, 7)))) throw new AssertionError("ex2");
        if (!zigzag(null).isEmpty()) throw new AssertionError("empty");
        // Random trees must match the oracle.
        Random rnd = new Random(1602);
        for (int t = 0; t < 400; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<List<Integer>> want = new ArrayList<>();
            dfs(x, 0, want);
            for (int d = 1; d < want.size(); d += 2) Collections.reverse(want.get(d));   // odd depths read right to left
            if (!zigzag(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tb-level-edges -->

**Approach.**
The method returns the stored size of every level and ignores the values. A null root returns an empty list before any queue exists, because `ArrayDeque` rejects null. On a chain, every pass stores a size of 1, removes one node, queues its single child, and ends with an empty queue after the last node. The sum of the returned entries equals the node count, because every node is removed in exactly one pass.

The invariant is the same as in the plain traversal: the stored size equals the number of nodes of the depth at the top of each pass.

**Complexity.**
- **Time** is O(n), because each node is queued and removed once.
- **Space** is O(w) for the queue, plus O(h) for the output list.

```java run
import java.util.*;

public final class LevelWidths {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the number of nodes at each depth.
     * Time: O(n), because each node is queued and removed once.
     * Space: O(w) for the queue.
     * Invariant: the stored size equals the width of the depth being read.
     */
    static List<Integer> widths(TreeNode root) {
        List<Integer> result = new ArrayList<>();
        if (root == null) return result;                  // null must never enter the queue
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                      // width of this depth
            result.add(size);
            // Remove exactly the nodes of this depth and queue their children.
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        return result;
    }

    /** Oracle: counts nodes per depth with a recursive walk. */
    static void count(TreeNode node, int depth, List<Integer> out) {
        if (node == null) return;
        if (depth == out.size()) out.add(0);
        out.set(depth, out.get(depth) + 1);
        count(node.left, depth + 1, out);
        count(node.right, depth + 1, out);
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        TreeNode root = new TreeNode(rnd.nextInt(7) - 3);
        all.add(root);
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(7) - 3);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    public static void main(String[] args) {
        // Example 1: the null root gives an empty list.
        if (!widths(null).isEmpty()) throw new AssertionError("null root");
        // Example 2: a left chain of four nodes gives four ones.
        TreeNode a = new TreeNode(1);
        a.left = new TreeNode(2);
        a.left.left = new TreeNode(3);
        a.left.left.left = new TreeNode(4);
        if (!widths(a).equals(List.of(1, 1, 1, 1))) throw new AssertionError("left chain");
        // A right chain behaves the same.
        TreeNode b = new TreeNode(1);
        b.right = new TreeNode(2);
        if (!widths(b).equals(List.of(1, 1))) throw new AssertionError("right chain");
        // Java claim: ArrayDeque rejects null, which is why the root check comes first.
        boolean threw = false;
        try { new ArrayDeque<TreeNode>().add(null); } catch (NullPointerException e) { threw = true; }
        if (!threw) throw new AssertionError("null deque");
        // Random trees must match the oracle, and the widths must sum to the node count.
        Random rnd = new Random(1603);
        for (int t = 0; t < 400; t++) {
            int n = rnd.nextInt(30);
            TreeNode x = randomTree(rnd, n);
            List<Integer> want = new ArrayList<>();
            count(x, 0, want);
            List<Integer> got = widths(x);
            if (!got.equals(want)) throw new AssertionError("random " + t);
            int sum = 0;
            for (int w : got) sum += w;
            if (sum != n) throw new AssertionError("sum " + t);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Right Side View (LeetCode 199)
<!-- id: tb-right-view -->

**Approach.**
The method runs the standard level loop and keeps one value per pass. Inside the inner loop, the node removed at index `size - 1` is the last node of its depth in left-to-right order, so that node is the visible one. The method adds its value to the answer when the loop counter reaches `size - 1`. The queue order stays left to right, so the last removal of a depth is always its rightmost node, even when that node is a left child.

The invariant is that the last of the `size` removals of a pass is the rightmost node of the depth. The check `i == size - 1` selects it without a second pass.

**Complexity.**
- **Time** is O(n), because every node is still queued and removed once.
- **Space** is O(w) for the queue, plus O(h) for the answer.

```java run
import java.util.*;

public final class RightView {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the value of the rightmost node at every depth.
     * Time: O(n), because every node is queued and removed once.
     * Space: O(w) for the queue.
     * Invariant: the last removal of a pass is the rightmost node of that depth.
     */
    static List<Integer> rightSide(TreeNode root) {
        List<Integer> view = new ArrayList<>();
        if (root == null) return view;
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                      // level boundary
            for (int i = 0; i < size; i++) {
                TreeNode node = queue.poll();
                if (i == size - 1) view.add(node.val);    // last removal of the depth is visible
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        return view;
    }

    /** Oracle: the last value of each depth list built by a left-first recursive walk. */
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
        TreeNode root = new TreeNode(rnd.nextInt(7) - 3);
        all.add(root);
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(7) - 3);
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    public static void main(String[] args) {
        // Example 1: right children hide the left ones at depths 1 and 2.
        TreeNode r = new TreeNode(1);
        r.left = new TreeNode(2);
        r.right = new TreeNode(3);
        r.left.right = new TreeNode(5);
        r.right.right = new TreeNode(4);
        if (!rightSide(r).equals(List.of(1, 3, 4))) throw new AssertionError("ex1");
        // Example 2: a left-only branch stays visible.
        TreeNode l = new TreeNode(1);
        l.left = new TreeNode(2);
        l.left.left = new TreeNode(4);
        if (!rightSide(l).equals(List.of(1, 2, 4))) throw new AssertionError("ex2");
        if (!rightSide(null).isEmpty()) throw new AssertionError("empty");
        // Random trees must match the oracle.
        Random rnd = new Random(1604);
        for (int t = 0; t < 400; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(30));
            List<List<Integer>> lv = new ArrayList<>();
            dfs(x, 0, lv);
            List<Integer> want = new ArrayList<>();
            for (List<Integer> level : lv) want.add(level.get(level.size() - 1));
            if (!rightSide(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```
