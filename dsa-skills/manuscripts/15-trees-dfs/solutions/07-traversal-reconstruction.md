<!-- solutions-for: 07-traversal-reconstruction -->
### Solutions For Rebuilding A Tree

#### Solution: [Build] Split One Root (Author exercise)
<!-- id: tw-split-root -->

**Approach.**
The first value of `pre` is the root, because preorder visits a root before its descendants. The method finds that value in `in` with one scan. Every position before it holds a left-subtree value, so the left size equals the position. Every position after it holds a right-subtree value, so the right size equals `n - 1 - position`. The invariant is that inorder places the left subtree entirely before the root, so the position of the root alone fixes both sizes.

**Complexity.**
- **Time** is O(n), because one scan of `in` finds the root.
- **Space** is O(1), because the method stores two integers.

```java run
import java.util.*;

public final class SplitOneRoot {
    /**
     * Returns {left size, right size} of the root of the described tree.
     * Time: O(n), one scan.
     * Space: O(1).
     * Invariant: the inorder position of the root equals the size of the left subtree.
     */
    static int[] split(int[] pre, int[] in) {
        int k = 0;                                               // the scan starts at the first inorder position
        while (in[k] != pre[0]) k++;                             // stop at the root, which pre[0] names
        return new int[] {k, in.length - 1 - k};                 // values before it go left, the rest go right
    }

    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int count(Node n) { return n == null ? 0 : 1 + count(n.left) + count(n.right); }

    static void pre(Node n, List<Integer> o) { if (n == null) return; o.add(n.val); pre(n.left, o); pre(n.right, o); }

    static void in(Node n, List<Integer> o) { if (n == null) return; in(n.left, o); o.add(n.val); in(n.right, o); }

    static Node random(Random rnd, int[] next, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        int v = next[0]++;                                       // distinct values come from a counter
        Node l = random(rnd, next, d + 1);
        Node r = random(rnd, next, d + 1);
        return new Node(v, l, r);
    }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        // Example 1: the root 8 sits at inorder position 3.
        if (!Arrays.equals(split(new int[] {8, 5, 2, 9, 4, 7}, new int[] {2, 5, 9, 8, 7, 4}), new int[] {3, 2})) throw new AssertionError("ex1");
        // Example 2: a single node has two empty sides.
        if (!Arrays.equals(split(new int[] {1}, new int[] {1}), new int[] {0, 0})) throw new AssertionError("ex2");
        // Random trees: the sizes equal the node counts of the real subtrees.
        Random rnd = new Random(25);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, new int[] {0}, 0);
            if (x == null) continue;
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>();
            pre(x, p);
            in(x, i);
            if (!Arrays.equals(split(arr(p), arr(i)), new int[] {count(x.left), count(x.right)})) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Reconstruct By Index Ranges (Author exercise)
<!-- id: tw-postorder -->

**Approach.**
The call owns a preorder window and an inorder window of equal length. An empty window returns at once. Otherwise the call reads the root from the first preorder index and looks up its inorder position in the index map. The left size is that position minus the first inorder index. The call handles the left windows first, then the right windows, and appends the root last, which is the postorder rule.

The invariant is that the two windows always hold the same set of values and describe one subtree. No array is copied, because each call passes only four integers and the map.

**Complexity.**
- **Time** is O(n), because the map takes n steps and each node receives one call.
- **Space** is O(n) for the map and the output, plus a stack of pending calls as deep as the height.

```java run
import java.util.*;

public final class PostorderFromWindows {
    /**
     * Returns the postorder of the tree described by pre and in.
     * Time: O(n).
     * Space: O(n) for the map and the result.
     * Invariant: both windows hold the same set of values and one subtree.
     */
    static List<Integer> postorder(int[] pre, int[] in) {
        Map<Integer, Integer> where = new HashMap<>();
        for (int i = 0; i < in.length; i++) where.put(in[i], i);     // one pass fills the lookup table
        List<Integer> out = new ArrayList<>();
        walk(pre, 0, pre.length - 1, 0, in.length - 1, where, out);
        return out;
    }

    private static void walk(int[] pre, int pl, int pr, int il, int ir, Map<Integer, Integer> where, List<Integer> out) {
        if (pl > pr) return;                                     // an empty window has no values
        int root = pre[pl];                                      // the first preorder value is the root
        int k = where.get(root);                                 // its inorder position
        int leftSize = k - il;                                   // the values before it form the left subtree
        walk(pre, pl + 1, pl + leftSize, il, k - 1, where, out);       // left windows come first
        walk(pre, pl + leftSize + 1, pr, k + 1, ir, where, out);       // right windows come second
        out.add(root);                                           // postorder writes the root last
    }

    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void pre(Node n, List<Integer> o) { if (n == null) return; o.add(n.val); pre(n.left, o); pre(n.right, o); }

    static void in(Node n, List<Integer> o) { if (n == null) return; in(n.left, o); o.add(n.val); in(n.right, o); }

    static void post(Node n, List<Integer> o) { if (n == null) return; post(n.left, o); post(n.right, o); o.add(n.val); }

    static Node random(Random rnd, int[] next, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        int v = next[0]++;
        Node l = random(rnd, next, d + 1);
        Node r = random(rnd, next, d + 1);
        return new Node(v, l, r);
    }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        // Example 1: the six-node tree.
        if (!postorder(new int[] {8, 5, 2, 9, 4, 7}, new int[] {2, 5, 9, 8, 7, 4}).equals(List.of(2, 9, 5, 7, 4, 8))) throw new AssertionError("ex1");
        // Example 2: root 3 with children 1 and 2.
        if (!postorder(new int[] {3, 1, 2}, new int[] {1, 3, 2}).equals(List.of(1, 2, 3))) throw new AssertionError("ex2");
        // The empty lists give the empty list.
        if (!postorder(new int[0], new int[0]).isEmpty()) throw new AssertionError("empty");
        // Random trees: the result equals the real postorder.
        Random rnd = new Random(26);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, new int[] {0}, 0);
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>(), q = new ArrayList<>();
            pre(x, p);
            in(x, i);
            post(x, q);
            if (!postorder(arr(p), arr(i)).equals(q)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty Range And Skewed Tree (Author exercise)
<!-- id: tw-height -->

**Approach.**
The call owns two windows and returns the height of the subtree that they describe. An empty window means that the preorder start index is past the end index, and the call returns 0 at that point, so no lookup runs on an empty range. A non-empty call reads the root, finds its inorder position, computes the left size, and returns one plus the larger of the two child heights. On a chain, one child window is empty at every call, and the other has one value fewer.

The invariant is that the window length equals `pr - pl + 1` and equals `ir - il + 1`. The empty test uses either pair, and the two always agree.

**Complexity.**
- **Time** is O(n), because the map takes n steps and each node receives one call.
- **Space** is O(n) for the map, plus a stack of pending calls as deep as the height.

```java run
import java.util.*;

public final class HeightFromWindows {
    /**
     * Returns the height in nodes of the described tree.
     * Time: O(n).
     * Space: O(n) for the map, plus pending calls.
     * Invariant: the two windows always have equal length.
     */
    static int height(int[] pre, int[] in) {
        Map<Integer, Integer> where = new HashMap<>();
        for (int i = 0; i < in.length; i++) where.put(in[i], i);     // lookup table of inorder positions
        return h(pre, 0, pre.length - 1, 0, in.length - 1, where);
    }

    private static int h(int[] pre, int pl, int pr, int il, int ir, Map<Integer, Integer> where) {
        if (pl > pr) return 0;                                   // the empty window ends the recursion
        int k = where.get(pre[pl]);                              // inorder position of the root
        int leftSize = k - il;                                   // size of the left window
        int left = h(pre, pl + 1, pl + leftSize, il, k - 1, where);
        int right = h(pre, pl + leftSize + 1, pr, k + 1, ir, where);
        return 1 + Math.max(left, right);                        // the taller child plus the root
    }

    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void pre(Node n, List<Integer> o) { if (n == null) return; o.add(n.val); pre(n.left, o); pre(n.right, o); }

    static void in(Node n, List<Integer> o) { if (n == null) return; in(n.left, o); o.add(n.val); in(n.right, o); }

    static int realHeight(Node n) { return n == null ? 0 : 1 + Math.max(realHeight(n.left), realHeight(n.right)); }

    static Node random(Random rnd, int[] next, int d) {
        if (d > 8 || rnd.nextInt(4) == 0) return null;
        int v = next[0]++;
        Node l = random(rnd, next, d + 1);
        Node r = random(rnd, next, d + 1);
        return new Node(v, l, r);
    }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        // Example 1: empty lists give height 0.
        if (height(new int[0], new int[0]) != 0) throw new AssertionError("empty");
        // Example 2: a left chain of three nodes.
        if (height(new int[] {5, 4, 3}, new int[] {3, 4, 5}) != 3) throw new AssertionError("left chain");
        // A right chain has the same height.
        if (height(new int[] {3, 4, 5}, new int[] {3, 4, 5}) != 3) throw new AssertionError("right chain");
        // A long chain of 3000 nodes works.
        int[] pre = new int[3000], in = new int[3000];
        for (int i = 0; i < 3000; i++) { pre[i] = 3000 - i; in[i] = i + 1; }
        if (height(pre, in) != 3000) throw new AssertionError("long chain");
        // Random trees: the height equals the real height.
        Random rnd = new Random(27);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, new int[] {0}, 0);
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>();
            pre(x, p);
            in(x, i);
            if (height(arr(p), arr(i)) != realHeight(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Construct Binary Tree From Preorder And Inorder (LeetCode 105)
<!-- id: tw-construct -->

**Approach.**
The method fills an index map from each inorder value to its position. A call owns a preorder window and an inorder window. It creates the root from the first preorder value, looks up the inorder position of that value, and computes the left size. It builds the left child from the next `leftSize` preorder values and the inorder values before the root. It builds the right child from the remaining windows. An empty window returns `null`.

The invariant is that the two windows hold the same set of values and describe exactly one subtree. The checks below confirm three claims of the lesson. Preorder alone does not fix the tree. Preorder with postorder does not fix a tree with one-child nodes. Repeated values break the index map.

**Complexity.**
- **Time** is O(n), because the map takes n steps and each node receives one call with constant work.
- **Space** is O(n) for the map and the tree, plus a stack of pending calls as deep as the height.

```java run
import java.util.*;

public final class ConstructTree {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    /**
     * Rebuilds the tree from preorder and inorder lists of distinct values.
     * Time: O(n).
     * Space: O(n) for the map and the tree.
     * Invariant: each call owns matching windows of one subtree.
     */
    static Node build(int[] pre, int[] in) {
        Map<Integer, Integer> where = new HashMap<>();
        for (int i = 0; i < in.length; i++) where.put(in[i], i);     // inorder positions in one pass
        return rebuild(pre, 0, pre.length - 1, 0, in.length - 1, where);
    }

    private static Node rebuild(int[] pre, int pl, int pr, int il, int ir, Map<Integer, Integer> where) {
        if (pl > pr) return null;                                // an empty window owns no node
        Node root = new Node(pre[pl]);                           // the first preorder value is the root
        int k = where.get(pre[pl]);                              // constant-time lookup
        int leftSize = k - il;                                   // size of the left subtree
        root.left = rebuild(pre, pl + 1, pl + leftSize, il, k - 1, where);
        root.right = rebuild(pre, pl + leftSize + 1, pr, k + 1, ir, where);
        return root;
    }

    static void pre(Node n, List<Integer> o) { if (n == null) return; o.add(n.val); pre(n.left, o); pre(n.right, o); }

    static void in(Node n, List<Integer> o) { if (n == null) return; in(n.left, o); o.add(n.val); in(n.right, o); }

    static void post(Node n, List<Integer> o) { if (n == null) return; post(n.left, o); post(n.right, o); o.add(n.val); }

    static boolean same(Node a, Node b) {
        if (a == null || b == null) return a == b;
        return a.val == b.val && same(a.left, b.left) && same(a.right, b.right);
    }

    static Node random(Random rnd, int[] next, int d) {
        if (d > 8 || rnd.nextInt(4) == 0) return null;
        Node n = new Node(next[0]++);
        n.left = random(rnd, next, d + 1);
        n.right = random(rnd, next, d + 1);
        return n;
    }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        // Example 1: the six-node tree has the expected shape.
        Node r = build(new int[] {8, 5, 2, 9, 4, 7}, new int[] {2, 5, 9, 8, 7, 4});
        if (r.val != 8 || r.left.val != 5 || r.left.left.val != 2 || r.left.right.val != 9
                || r.right.val != 4 || r.right.left.val != 7 || r.right.right != null) throw new AssertionError("ex1");
        // Example 2: a single node.
        Node s = build(new int[] {6}, new int[] {6});
        if (s.val != 6 || s.left != null || s.right != null) throw new AssertionError("ex2");
        // Preorder alone is ambiguous: two trees share the list 1, 2, and the second list separates them.
        Node a = build(new int[] {1, 2}, new int[] {2, 1});
        Node b = build(new int[] {1, 2}, new int[] {1, 2});
        List<Integer> pa = new ArrayList<>(), pb = new ArrayList<>();
        pre(a, pa);
        pre(b, pb);
        if (!pa.equals(pb) || a.left == null || b.right == null) throw new AssertionError("ambiguity");
        // Preorder with postorder is ambiguous for one-child nodes: both trees give 1, 2 and 2, 1.
        List<Integer> qa = new ArrayList<>(), qb = new ArrayList<>();
        post(a, qa);
        post(b, qb);
        if (!qa.equals(qb)) throw new AssertionError("pre and post");
        // A repeated value keeps only its last position in the index map.
        Map<Integer, Integer> m = new HashMap<>();
        m.put(7, 0);
        m.put(7, 3);
        if (m.get(7) != 3) throw new AssertionError("duplicate keys");
        // Random trees: rebuilding gives the same tree, and the lists round-trip.
        Random rnd = new Random(28);
        for (int t = 0; t < 600; t++) {
            Node x = random(rnd, new int[] {0}, 0);
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>();
            pre(x, p);
            in(x, i);
            Node y = build(arr(p), arr(i));
            if (!same(x, y)) throw new AssertionError("random " + t);
        }
    }
}
```
