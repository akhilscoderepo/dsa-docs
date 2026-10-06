<!-- solutions-for: 02-bst-invariant-and-bounds -->
### Solutions For Value Limits

#### Solution: [Build] Validate One Root And Children (Author exercise)
<!-- id: tb-bst-root-children -->

**Approach.**
The method treats the root as the source of two intervals. The left child must lie strictly between negative infinity and the root key, and the right child must lie strictly between the root key and positive infinity. Because no node exists below a child, no further interval is needed. A helper `inside(node, low, high)` returns `true` for a missing child and otherwise compares the key with both limits. The method returns `true` only when both helper calls return `true`.

The invariant is that each child is compared with the limit its side of the root imposes, and the other side stays unbounded. Long limits keep the comparison safe at the extremes of `int`.

**Complexity.**
- **Time** is O(1), because the tree holds at most three nodes.
- **Space** is O(1), because the method stores two limits.

```java run
import java.util.*;

public final class RootChildren {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /** True when the child is missing or its key lies strictly between the limits. */
    static boolean inside(TreeNode child, long low, long high) {
        return child == null || (child.val > low && child.val < high);
    }

    /**
     * Validates a root with at most two leaf children.
     * Time: O(1), because at most three nodes exist.
     * Space: O(1).
     * Invariant: the left child is limited above by the root key and the right child below.
     */
    static boolean validRootAndChildren(TreeNode root) {
        // The left child lives in (-infinity, root); the right child lives in (root, +infinity).
        return inside(root.left, Long.MIN_VALUE, root.val) && inside(root.right, root.val, Long.MAX_VALUE);
    }

    public static void main(String[] args) {
        // Example 1: 1, 2, 3 is valid.
        TreeNode a = new TreeNode(2);
        a.left = new TreeNode(1);
        a.right = new TreeNode(3);
        if (!validRootAndChildren(a)) throw new AssertionError("ex1");
        // Example 2: an equal left child is not allowed.
        a.left = new TreeNode(2);
        if (validRootAndChildren(a)) throw new AssertionError("ex2");
        // A lone root is valid.
        if (!validRootAndChildren(new TreeNode(Integer.MIN_VALUE))) throw new AssertionError("lone");
        // Every combination of small keys must match the direct comparison.
        for (int r = -2; r <= 2; r++)
            for (int l = -3; l <= 3; l++)
                for (int g = -3; g <= 3; g++) {
                    TreeNode t = new TreeNode(r);
                    t.left = new TreeNode(l);
                    t.right = new TreeNode(g);
                    boolean want = l < r && r < g;
                    if (validRootAndChildren(t) != want) throw new AssertionError(r + " " + l + " " + g);
                }
    }
}
```

#### Solution: [Vary] Propagate Ancestor Bounds (Author exercise)
<!-- id: tb-bst-count-inside -->

**Approach.**
The method walks the tree once and passes the interval down. At each node it adds 1 to the count when the key lies strictly inside the interval. It then recurses on both children whether or not the node passed, so a failed node does not stop the walk. The left call uses the smaller of the old upper limit and the node key, and the right call uses the larger of the old lower limit and the node key. A node that broke its own limits can have a key looser than the limit it holds, and the minimum and maximum keep the stronger limit from the ancestors above.

The invariant is that each call receives the intersection of the turns of all ancestors on its path. The count of a subtree is the count of its root plus the counts of its two children.

**Complexity.**
- **Time** is O(n), because each node is visited once.
- **Space** is O(h) for the recursion stack, where `h` is the height.

```java run
import java.util.*;

public final class CountInside {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Counts the nodes whose key lies in the open interval inherited from all ancestors.
     * Time: O(n), because each node is visited once.
     * Space: O(h) for the recursion stack.
     * Invariant: low and high are the strongest limits from all right and left turns on the path.
     */
    static int countInside(TreeNode node, long low, long high) {
        if (node == null) return 0;                                  // an absent child adds nothing
        int self = (node.val > low && node.val < high) ? 1 : 0;      // strict policy: both ends open
        // The children keep the stronger limit even when this node failed.
        return self + countInside(node.left, low, Math.min(high, node.val))
                    + countInside(node.right, Math.max(low, node.val), high);
    }

    /** Oracle: checks each node against every ancestor with an explicit path list. */
    static int oracle(TreeNode node, List<TreeNode> path, List<Boolean> wentLeft) {
        if (node == null) return 0;
        boolean good = true;
        for (int i = 0; i < path.size(); i++) {
            int a = path.get(i).val;
            if (wentLeft.get(i) ? node.val >= a : node.val <= a) good = false;   // a left turn needs smaller keys
        }
        path.add(node);
        wentLeft.add(true);
        int total = good ? 1 : 0;
        total += oracle(node.left, path, wentLeft);
        wentLeft.set(wentLeft.size() - 1, false);
        total += oracle(node.right, path, wentLeft);
        path.remove(path.size() - 1);
        wentLeft.remove(wentLeft.size() - 1);
        return total;
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        TreeNode root = new TreeNode(rnd.nextInt(9));
        all.add(root);
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(9));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    public static void main(String[] args) {
        // Example 1: the node 3 lies outside (5, 6), so 4 of 5 nodes count.
        TreeNode r = new TreeNode(5);
        r.left = new TreeNode(1);
        r.right = new TreeNode(6);
        r.right.left = new TreeNode(3);
        r.right.right = new TreeNode(7);
        if (countInside(r, Long.MIN_VALUE, Long.MAX_VALUE) != 4) throw new AssertionError("ex1");
        // Example 2: an equal right child fails.
        TreeNode e = new TreeNode(4);
        e.right = new TreeNode(4);
        if (countInside(e, Long.MIN_VALUE, Long.MAX_VALUE) != 1) throw new AssertionError("ex2");
        if (countInside(null, Long.MIN_VALUE, Long.MAX_VALUE) != 0) throw new AssertionError("empty");
        // Random trees must match the ancestor-path oracle.
        Random rnd = new Random(1611);
        for (int t = 0; t < 500; t++) {
            TreeNode x = randomTree(rnd, rnd.nextInt(25));
            int want = oracle(x, new ArrayList<>(), new ArrayList<>());
            if (countInside(x, Long.MIN_VALUE, Long.MAX_VALUE) != want) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Integer Extremes And Duplicates (Author exercise)
<!-- id: tb-bst-extremes -->

**Approach.**
Equal keys are legal on the right, so the lower end of each interval is closed and the upper end stays open. A node with key `k` and interval `[low, high)` is legal when `low <= k < high`. The left child receives `[low, k)`, because every left key must be strictly smaller. The right child receives `[k, high)`, because an equal key may appear there. The root receives `[Long.MIN_VALUE, Long.MAX_VALUE)`, and every `int` key falls inside it, including `Integer.MAX_VALUE`, because the long limit is larger than any `int`.

The invariant is that each call gets exactly the keys allowed by its ancestors under the stated policy. Long arithmetic avoids the overflow that a limit of `Integer.MAX_VALUE + 1` would cause in `int`.

**Complexity.**
- **Time** is O(n), because each node is visited once.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class ExtremeKeys {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Validates with equal keys allowed on the right only.
     * Time: O(n), because each node is visited once.
     * Space: O(h) for the recursion stack.
     * Invariant: each key must satisfy low <= key < high for the limits of its path.
     */
    static boolean valid(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val < low || node.val >= high) return false;     // low is closed, high is open
        return valid(node.left, low, node.val)                    // left keys must be strictly smaller
            && valid(node.right, node.val, high);                 // right keys may equal the node
    }

    static void collect(TreeNode n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        collect(n.left, out);
        collect(n.right, out);
    }

    /** Oracle: compares each node with every key of its two subtrees. */
    static boolean oracle(TreeNode n) {
        if (n == null) return true;
        List<Integer> l = new ArrayList<>(), r = new ArrayList<>();
        collect(n.left, l);
        collect(n.right, r);
        for (int v : l) if (v >= n.val) return false;
        for (int v : r) if (v < n.val) return false;
        return oracle(n.left) && oracle(n.right);
    }

    static final int[] KEYS = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -1, 0, 1, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};

    /** Inserts under the policy: smaller goes left, equal or larger goes right. */
    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else n.right = insert(n.right, v);
        return n;
    }

    static boolean check(TreeNode root) { return valid(root, Long.MIN_VALUE, Long.MAX_VALUE); }

    public static void main(String[] args) {
        // Example 1: an equal right child is legal.
        TreeNode a = new TreeNode(2);
        a.right = new TreeNode(2);
        if (!check(a)) throw new AssertionError("ex1");
        // Example 2: nothing is smaller than the minimum int.
        TreeNode b = new TreeNode(Integer.MIN_VALUE);
        b.left = new TreeNode(Integer.MIN_VALUE);
        if (check(b)) throw new AssertionError("ex2");
        // The maximum int is a legal root and a legal right child.
        TreeNode c = new TreeNode(Integer.MAX_VALUE);
        c.right = new TreeNode(Integer.MAX_VALUE);
        if (!check(c) || !check(null)) throw new AssertionError("max");
        // Random trees: policy-built trees must be valid, and mutated ones must match the oracle.
        Random rnd = new Random(1612);
        for (int t = 0; t < 500; t++) {
            TreeNode root = null;
            int n = rnd.nextInt(14);
            for (int i = 0; i < n; i++) root = insert(root, KEYS[rnd.nextInt(KEYS.length)]);
            if (!check(root) || !oracle(root)) throw new AssertionError("built " + t);
            List<TreeNode> all = new ArrayList<>();
            Deque<TreeNode> st = new ArrayDeque<>();
            if (root != null) st.push(root);
            while (!st.isEmpty()) {
                TreeNode x = st.pop();
                all.add(x);
                if (x.left != null) st.push(x.left);
                if (x.right != null) st.push(x.right);
            }
            if (!all.isEmpty()) all.get(rnd.nextInt(all.size())).val = KEYS[rnd.nextInt(KEYS.length)];   // break the order at random
            if (check(root) != oracle(root)) throw new AssertionError("mutated " + t);
        }
    }
}
```

#### Solution: [Recognize] Validate Binary Search Tree (LeetCode 98)
<!-- id: tb-validate-bst -->

**Approach.**
The method passes an open interval down the recursion. The root starts with limits outside the `int` range, so the first key always fits. A node is rejected when its key is at or below the lower limit or at or above the upper limit. The left call tightens the upper limit to the node key, and the right call tightens the lower limit to the node key. Because the limits come from all turns on the path, a key such as 3 under the right child of 5 is rejected by the lower limit 5, even though it is smaller than its own parent 6.

The invariant is that the interval of a node equals the intersection of all ancestor turns. A subtree is valid exactly when its root fits the interval and both child subtrees are valid under the narrowed intervals.

**Complexity.**
- **Time** is O(n), because the recursion stops early on failure and otherwise visits each node once.
- **Space** is O(h) for the recursion stack, which is O(n) on a chain.

```java run
import java.util.*;

public final class ValidateBst {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns true when the tree is a strict binary search tree.
     * Time: O(n), because each node is visited at most once.
     * Space: O(h) for the recursion stack.
     * Invariant: the interval (low, high) holds the keys allowed by all ancestors.
     */
    static boolean isValidBST(TreeNode root) {
        return check(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean check(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val <= low || node.val >= high) return false;    // open interval on both ends
        return check(node.left, low, node.val)                    // upper limit tightens on a left turn
            && check(node.right, node.val, high);                 // lower limit tightens on a right turn
    }

    /** Oracle: an inorder walk must be strictly increasing. */
    static void inorder(TreeNode n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    static boolean oracle(TreeNode root) {
        List<Integer> keys = new ArrayList<>();
        inorder(root, keys);
        for (int i = 1; i < keys.size(); i++) if (keys.get(i - 1) >= keys.get(i)) return false;
        return true;
    }

    static TreeNode randomTree(Random rnd, int n) {
        if (n == 0) return null;
        List<TreeNode> all = new ArrayList<>();
        TreeNode root = new TreeNode(rnd.nextInt(9));
        all.add(root);
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(9));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return root;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    public static void main(String[] args) {
        // Example 1: the node 3 hides below the right child of 5.
        TreeNode a = new TreeNode(5);
        a.left = new TreeNode(1);
        a.right = new TreeNode(4);
        a.right.left = new TreeNode(3);
        a.right.right = new TreeNode(6);
        if (isValidBST(a)) throw new AssertionError("ex1");
        // Example 2: 1, 2, 3 is valid.
        TreeNode b = new TreeNode(2);
        b.left = new TreeNode(1);
        b.right = new TreeNode(3);
        if (!isValidBST(b)) throw new AssertionError("ex2");
        // The extreme keys are legal in a valid tree.
        TreeNode c = new TreeNode(0);
        c.left = new TreeNode(Integer.MIN_VALUE);
        c.right = new TreeNode(Integer.MAX_VALUE);
        if (!isValidBST(c)) throw new AssertionError("extremes");
        // Random shapes must match the strictly increasing inorder oracle.
        Random rnd = new Random(1613);
        for (int t = 0; t < 600; t++) {
            TreeNode x = randomTree(rnd, 1 + rnd.nextInt(12));
            if (isValidBST(x) != oracle(x)) throw new AssertionError("shape " + t);
            TreeNode y = null;                                    // built trees must be valid
            for (int i = 0; i < 1 + rnd.nextInt(12); i++) y = insert(y, rnd.nextInt(30));
            if (!isValidBST(y)) throw new AssertionError("built " + t);
        }
    }
}
```
