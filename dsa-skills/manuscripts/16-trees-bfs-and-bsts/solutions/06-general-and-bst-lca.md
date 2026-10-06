<!-- solutions-for: 06-general-and-bst-lca -->
### Solutions For Common Ancestors

#### Solution: [Build] General-Tree Ancestor Return (Author exercise)
<!-- id: tb-lca-combine -->

**Approach.**
A recursive call returns the target leaf found in its subtree, or `null`. An empty slot returns `null`. A node whose value equals one of the two target values returns itself. Any other node first collects the answers of both children. When both answers are non-null, one target sits in each child subtree, so the current node is the lowest common ancestor, and the call returns the current node. When only one answer is non-null, the call returns it unchanged, and when both are null, the call returns `null`. The method then reads the value of the node the root call returns.

The invariant is that a call returns a target only if the target lies in its subtree. Two non-null reports prove that the targets are separated at the current node.

**Complexity.**
- **Time** is O(n), because each node is visited once.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class AncestorReturn {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the value of the lowest common ancestor of two leaves with values a and b.
     * Time: O(n), because each node is visited once.
     * Space: O(h) for the recursion stack.
     * Invariant: a call returns a target only if the target lies in its subtree.
     */
    static int lcaOfLeaves(TreeNode root, int a, int b) {
        return report(root, a, b).val;
    }

    private static TreeNode report(TreeNode node, int a, int b) {
        if (node == null) return null;                                   // nothing below an empty slot
        if (node.val == a || node.val == b) return node;                 // a target reports itself
        TreeNode left = report(node.left, a, b);                         // children report first
        TreeNode right = report(node.right, a, b);
        if (left != null && right != null) return node;                  // targets in different subtrees: the split
        return left != null ? left : right;                              // pass up the single report, or null
    }

    static TreeNode randomTree(Random rnd, int n) {
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(0));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(all.size());                       // distinct values
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    /** Oracle: root-to-node paths, then the last shared node. */
    static boolean path(TreeNode n, int v, List<TreeNode> out) {
        if (n == null) return false;
        out.add(n);
        if (n.val == v || path(n.left, v, out) || path(n.right, v, out)) return true;
        out.remove(out.size() - 1);
        return false;
    }

    static int oracle(TreeNode root, int a, int b) {
        List<TreeNode> pa = new ArrayList<>(), pb = new ArrayList<>();
        path(root, a, pa);
        path(root, b, pb);
        int i = 0;
        while (i < pa.size() && i < pb.size() && pa.get(i) == pb.get(i)) i++;
        return pa.get(i - 1).val;
    }

    public static void main(String[] args) {
        // Example 1: the leaves 6 and 9 meet at 7.
        TreeNode[] n = new TreeNode[9];
        int[] v = {10, 4, 15, 2, 7, 12, 20, 6, 9};
        for (int i = 0; i < 9; i++) n[i] = new TreeNode(v[i]);
        n[0].left = n[1]; n[0].right = n[2];
        n[1].left = n[3]; n[1].right = n[4];
        n[2].left = n[5]; n[2].right = n[6];
        n[4].left = n[7]; n[4].right = n[8];
        if (lcaOfLeaves(n[0], 6, 9) != 7) throw new AssertionError("ex1");
        // Example 2: the leaves 2 and 12 meet at the root.
        if (lcaOfLeaves(n[0], 2, 12) != 10) throw new AssertionError("ex2");
        // Random trees: every pair of leaves must match the path oracle.
        Random rnd = new Random(1651);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, 3 + rnd.nextInt(25));
            List<TreeNode> leaves = new ArrayList<>();
            Deque<TreeNode> st = new ArrayDeque<>();
            st.push(x);
            while (!st.isEmpty()) {
                TreeNode c = st.pop();
                if (c.left == null && c.right == null) leaves.add(c);
                if (c.left != null) st.push(c.left);
                if (c.right != null) st.push(c.right);
            }
            for (TreeNode p : leaves)
                for (TreeNode q : leaves)
                    if (p != q && lcaOfLeaves(x, p.val, q.val) != oracle(x, p.val, q.val)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Lowest Common Ancestor of a Binary Tree (LeetCode 236)
<!-- id: tb-lca-binary-tree -->

**Approach.**
The method uses the same report rule with nodes instead of values. A call returns `null` for an empty slot and returns the node itself when the node is `p` or `q`, without looking below it. Otherwise it collects both child answers. Two non-null answers make the current node the lowest common ancestor. One non-null answer passes up unchanged. A target that sits above the other target returns itself, and the report from its subtree is never needed, because the other target lies below it and the node is already the answer. References are compared with `==`, because values may repeat.

The invariant is that a call returns the lowest common ancestor of the targets inside its subtree when it holds both, and the single target when it holds one.

**Complexity.**
- **Time** is O(n), because each node is visited at most once.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class LcaBinaryTree {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the lowest common ancestor of p and q.
     * Time: O(n), because each node is visited at most once.
     * Space: O(h) for the recursion stack.
     * Invariant: the result is the LCA when both targets lie below, else the single target or null.
     */
    static TreeNode lowestCommonAncestor(TreeNode node, TreeNode p, TreeNode q) {
        if (node == null || node == p || node == q) return node;      // identity, not value
        TreeNode left = lowestCommonAncestor(node.left, p, q);
        TreeNode right = lowestCommonAncestor(node.right, p, q);
        if (left != null && right != null) return node;               // one target on each side
        return left != null ? left : right;
    }

    static TreeNode randomTree(Random rnd, int n) {
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(rnd.nextInt(3)));                        // small value range forces repeats
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(rnd.nextInt(3));
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    static void parents(TreeNode n, Map<TreeNode, TreeNode> par) {
        if (n == null) return;
        if (n.left != null) { par.put(n.left, n); parents(n.left, par); }
        if (n.right != null) { par.put(n.right, n); parents(n.right, par); }
    }

    /** Oracle: climb parent links from p to collect ancestors, then climb from q to the first hit. */
    static TreeNode oracle(TreeNode root, TreeNode p, TreeNode q) {
        Map<TreeNode, TreeNode> par = new IdentityHashMap<>();
        parents(root, par);
        Set<TreeNode> up = Collections.newSetFromMap(new IdentityHashMap<>());
        for (TreeNode c = p; c != null; c = par.get(c)) up.add(c);
        for (TreeNode c = q; c != null; c = par.get(c)) if (up.contains(c)) return c;
        return null;
    }

    public static void main(String[] args) {
        // Example 1: the nodes 8 and 11 meet at the root 9.
        TreeNode r = new TreeNode(9), a = new TreeNode(4), b = new TreeNode(11);
        TreeNode c = new TreeNode(8), d = new TreeNode(2), e = new TreeNode(7), f = new TreeNode(5);
        r.left = a; r.right = b; a.left = c; a.right = d; d.left = e; d.right = f;
        b.left = new TreeNode(0); b.right = new TreeNode(6);
        if (lowestCommonAncestor(r, c, b) != r) throw new AssertionError("ex1");
        // Example 2: the node 4 is an ancestor of 5, so it is the answer.
        if (lowestCommonAncestor(r, a, f) != a) throw new AssertionError("ex2");
        // Random trees with repeated values: every pair of nodes must match the parent-link oracle.
        Random rnd = new Random(1652);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, 2 + rnd.nextInt(20));
            List<TreeNode> all = new ArrayList<>();
            Deque<TreeNode> st = new ArrayDeque<>();
            st.push(x);
            while (!st.isEmpty()) {
                TreeNode cur = st.pop();
                all.add(cur);
                if (cur.left != null) st.push(cur.left);
                if (cur.right != null) st.push(cur.right);
            }
            for (TreeNode p : all)
                for (TreeNode q : all)
                    if (p != q && lowestCommonAncestor(x, p, q) != oracle(x, p, q)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] One Target Is Ancestor (Author exercise)
<!-- id: tb-lca-ancestor-target -->

**Approach.**
The report method already stops at a target. A call that meets a node with value `a` or `b` returns that node at once and never calls its children. The other target lies below that node, because the contract promises one target is an ancestor of the other, so the node is the lowest common ancestor. Every other call returns the single report of its children, since both targets cannot appear in two different child subtrees when one is an ancestor of the other. The method therefore returns the higher target, and no node below it is visited. The test harness counts visits to confirm that.

The invariant is that the first target on any root path is the higher target, and everything beneath it is irrelevant.

**Complexity.**
- **Time** is O(n) in the worst case, and the method visits only the nodes outside the subtree of the higher target and on the way to it.
- **Space** is O(h) for the recursion stack.

```java run
import java.util.*;

public final class AncestorIsTarget {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static final Set<TreeNode> visited = Collections.newSetFromMap(new IdentityHashMap<>());

    /**
     * Returns the value of the higher of two targets where one is an ancestor of the other.
     * Time: O(n), because only nodes outside the higher target's subtree are visited.
     * Space: O(h) for the recursion stack.
     * Invariant: the first target met on a path is the higher target.
     */
    static int higherTarget(TreeNode root, int a, int b) {
        return walk(root, a, b).val;
    }

    private static TreeNode walk(TreeNode node, int a, int b) {
        if (node == null) return null;
        visited.add(node);
        if (node.val == a || node.val == b) return node;              // stop here: the other target lies below
        TreeNode left = walk(node.left, a, b);
        TreeNode right = walk(node.right, a, b);
        return left != null ? left : right;                           // only one side can report
    }

    static TreeNode randomTree(Random rnd, int n) {
        List<TreeNode> all = new ArrayList<>();
        all.add(new TreeNode(0));
        while (all.size() < n) {
            TreeNode p = all.get(rnd.nextInt(all.size()));
            TreeNode c = new TreeNode(all.size());
            if (rnd.nextBoolean() && p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else if (p.left == null) p.left = c;
            else continue;
            all.add(c);
        }
        return all.get(0);
    }

    static void subtree(TreeNode n, Set<TreeNode> out) {
        if (n == null) return;
        out.add(n);
        subtree(n.left, out);
        subtree(n.right, out);
    }

    public static void main(String[] args) {
        // Example 1: 5 is above 2.
        TreeNode r = new TreeNode(3), five = new TreeNode(5), one = new TreeNode(1);
        r.left = five; r.right = one;
        five.left = new TreeNode(6); five.right = new TreeNode(2);
        one.left = new TreeNode(0); one.right = new TreeNode(8);
        if (higherTarget(r, 5, 2) != 5) throw new AssertionError("ex1");
        // Example 2: the root is above 8.
        if (higherTarget(r, 3, 8) != 3) throw new AssertionError("ex2");
        // Random trees: pick a node and a descendant; the result must be the node, and nothing below it may be visited.
        Random rnd = new Random(1653);
        for (int t = 0; t < 300; t++) {
            TreeNode x = randomTree(rnd, 2 + rnd.nextInt(25));
            List<TreeNode> all = new ArrayList<>();
            Deque<TreeNode> st = new ArrayDeque<>();
            st.push(x);
            while (!st.isEmpty()) {
                TreeNode cur = st.pop();
                all.add(cur);
                if (cur.left != null) st.push(cur.left);
                if (cur.right != null) st.push(cur.right);
            }
            TreeNode high = all.get(rnd.nextInt(all.size()));
            Set<TreeNode> below = Collections.newSetFromMap(new IdentityHashMap<>());
            subtree(high, below);
            if (below.size() < 2) continue;                           // the higher target needs a descendant
            List<TreeNode> cand = new ArrayList<>(below);
            cand.remove(high);
            TreeNode low = cand.get(rnd.nextInt(cand.size()));
            visited.clear();
            if (higherTarget(x, high.val, low.val) != high.val) throw new AssertionError("answer " + t);
            below.remove(high);
            for (TreeNode b : below) if (visited.contains(b)) throw new AssertionError("visited below " + t);
        }
    }
}
```

#### Solution: [Recognize] Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)
<!-- id: tb-lca-bst -->

**Approach.**
The method keeps one reference that starts at the root and compares the two target keys with the node key. When both keys are smaller, both targets lie in the left subtree, so the walk moves left. When both are larger, the walk moves right. Otherwise one key is smaller than or equal to the node key and the other is larger than or equal to it. Then either the paths to the targets separate at this node, or one target is this node, and in both cases this node is the lowest common ancestor. The walk follows one path and needs no recursion.

The invariant is that both targets lie in the subtree of the current node. A comparison of keys keeps it true on every move and ends at the split point.

**Complexity.**
- **Time** is O(h), because the walk follows one path.
- **Space** is O(1), because the loop keeps one reference.

```java run
import java.util.*;

public final class LcaBst {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /**
     * Returns the lowest common ancestor of two nodes of a search tree.
     * Time: O(h), because one path is followed.
     * Space: O(1).
     * Invariant: both targets lie in the subtree of node.
     */
    static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode node = root;
        while (node != null) {
            if (p.val < node.val && q.val < node.val) node = node.left;          // both on the left
            else if (p.val > node.val && q.val > node.val) node = node.right;    // both on the right
            else return node;                                                    // split point or a target
        }
        return null;
    }

    static TreeNode insert(TreeNode n, int v) {
        if (n == null) return new TreeNode(v);
        if (v < n.val) n.left = insert(n.left, v);
        else if (v > n.val) n.right = insert(n.right, v);
        return n;
    }

    static void collect(TreeNode n, List<TreeNode> out) {
        if (n == null) return;
        out.add(n);
        collect(n.left, out);
        collect(n.right, out);
    }

    /** Oracle: the report method that ignores key order. */
    static TreeNode report(TreeNode n, TreeNode p, TreeNode q) {
        if (n == null || n == p || n == q) return n;
        TreeNode l = report(n.left, p, q), r = report(n.right, p, q);
        if (l != null && r != null) return n;
        return l != null ? l : r;
    }

    public static void main(String[] args) {
        // Example 1: the nodes 8 and 30 meet at the root 20.
        TreeNode r = new TreeNode(20), a = new TreeNode(8), b = new TreeNode(30);
        r.left = a; r.right = b;
        a.left = new TreeNode(3); a.right = new TreeNode(12);
        b.left = new TreeNode(25); b.right = new TreeNode(40);
        if (lowestCommonAncestor(r, a, b) != r) throw new AssertionError("ex1");
        // Example 2: 12 lies below 8, so 8 is the answer.
        if (lowestCommonAncestor(r, a, a.right) != a) throw new AssertionError("ex2");
        // Random search trees: every pair must match the report oracle.
        Random rnd = new Random(1654);
        for (int t = 0; t < 300; t++) {
            TreeNode x = null;
            for (int i = 0; i < 2 + rnd.nextInt(25); i++) x = insert(x, rnd.nextInt(60));
            List<TreeNode> all = new ArrayList<>();
            collect(x, all);
            for (TreeNode p : all)
                for (TreeNode q : all)
                    if (p != q && lowestCommonAncestor(x, p, q) != report(x, p, q)) throw new AssertionError("random " + t);
        }
    }
}
```
