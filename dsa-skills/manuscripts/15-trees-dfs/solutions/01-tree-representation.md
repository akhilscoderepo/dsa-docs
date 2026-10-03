<!-- solutions-for: 01-tree-representation -->
### Tree Representation

#### Solution: [Build] Construct A Three-Node Tree (Author exercise)
<!-- id: tr-three-node-tree -->

**Approach.** Make a `Node` class with an integer value and two references, create the root, and attach a child object only when its value is given. Then count links by visiting each created node and adding one for every reference that is still `null`. The class is what turns the two optional values into two child slots per node, so a leaf contributes two empty subtrees without any special case. The assertions confirm that a fresh node starts with both references null, and compare the count with the identity that a tree of n nodes has n + 1 null links, over all nine combinations of present and absent children.

**Complexity.** Constant time and constant space, since at most three nodes exist.

```java run
public final class ThreeNodeTree {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int nullLinks(int rootVal, Integer leftVal, Integer rightVal) {
        Node root = new Node(rootVal);
        if (leftVal != null) root.left = new Node(leftVal);
        if (rightVal != null) root.right = new Node(rightVal);
        int nulls = 0;
        Node[] all = {root, root.left, root.right};
        for (Node n : all) {
            if (n == null) continue;
            if (n.left == null) nulls++;
            if (n.right == null) nulls++;
        }
        return nulls;
    }

    public static void main(String[] args) {
        if (nullLinks(1, 2, 3) != 4) throw new AssertionError("example 1");
        if (nullLinks(1, 2, null) != 3) throw new AssertionError("example 2");
        Node fresh = new Node(7);
        if (fresh.left != null || fresh.right != null) throw new AssertionError("a new node has two empty child slots");
        Integer[] options = {null, 5, 9};
        for (Integer l : options) {
            for (Integer r : options) {
                int nodes = 1 + (l != null ? 1 : 0) + (r != null ? 1 : 0);
                if (nullLinks(0, l, r) != nodes + 1) throw new AssertionError("n nodes have n + 1 null links: " + l + " " + r);
            }
        }
    }
}
```

#### Solution: [Vary] Count N-Ary Children (Author exercise)
<!-- id: tr-count-nary-children -->

**Approach.** Walk the list of lists once. For node `i`, the size of `children.get(i)` is its child count, so keep the largest size seen, and add one to a leaf counter whenever the size is zero. Nothing refers to a left or a right, because the shape of an N-ary node is just the length of its collection. The assertions build random trees by giving every node after the first a random earlier parent, and compare against counts taken from the parent array instead of from the lists.

**Complexity.** O(n) time over the n nodes, and O(1) extra space beyond the input.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CountNaryChildren {
    static int[] widestAndLeaves(List<List<Integer>> children) {
        int widest = 0, leaves = 0;
        for (List<Integer> kids : children) {
            widest = Math.max(widest, kids.size());
            if (kids.isEmpty()) leaves++;
        }
        return new int[] {widest, leaves};
    }

    static List<List<Integer>> of(int[][] raw) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : raw) {
            List<Integer> kids = new ArrayList<>();
            for (int v : row) kids.add(v);
            out.add(kids);
        }
        return out;
    }

    public static void main(String[] args) {
        int[][] a = {{1, 2, 3}, {4}, {}, {}, {}};
        if (!Arrays.equals(widestAndLeaves(of(a)), new int[] {3, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(widestAndLeaves(of(new int[][] {{}})), new int[] {0, 1})) throw new AssertionError("example 2");
        Random rnd = new Random(15101);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            int[] parent = new int[n];
            int[] count = new int[n];
            List<List<Integer>> kids = new ArrayList<>();
            for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
            for (int i = 1; i < n; i++) {
                parent[i] = rnd.nextInt(i);
                count[parent[i]]++;
                kids.get(parent[i]).add(i);
            }
            int widest = 0, leaves = 0;
            for (int i = 0; i < n; i++) {
                widest = Math.max(widest, count[i]);
                if (count[i] == 0) leaves++;
            }
            if (!Arrays.equals(widestAndLeaves(kids), new int[] {widest, leaves})) throw new AssertionError("differs on parents " + Arrays.toString(parent));
        }
    }
}
```

#### Solution: [Boundary] Empty And Single-Node Trees (Author exercise)
<!-- id: tr-empty-single-trees -->

**Approach.** Build real nodes from the level-order array with a queue of nodes still waiting for children, taking two entries for each queued node and creating a child for each non-null entry. Then fix the three answers at `null` first: size 0, height 0, leaves 0. A non-null node has size 1 plus the sizes below it, height 1 plus the larger child height, and leaf count equal to the sum below it, except that a node with two null children counts itself as one leaf. With those rules the empty array and a single node need no branch of their own. The assertions generate random shapes as left and right index arrays, serialise them to level order, and compare with an iterative count taken directly from those arrays.

**Complexity.** O(n) time for the n nodes, and O(h) recursion stack for height h, which is O(n) on a chain.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Queue;
import java.util.Random;

public final class EmptySingleTrees {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] values) {
        if (values.length == 0) return null;
        Node root = new Node(values[0]);
        Queue<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int i = 1;
        while (!waiting.isEmpty() && i < values.length) {
            Node cur = waiting.poll();
            if (i < values.length && values[i] != null) { cur.left = new Node(values[i]); waiting.add(cur.left); }
            i++;
            if (i < values.length && values[i] != null) { cur.right = new Node(values[i]); waiting.add(cur.right); }
            i++;
        }
        return root;
    }

    static int[] shape(Node node) {
        if (node == null) return new int[] {0, 0, 0};
        int[] l = shape(node.left);
        int[] r = shape(node.right);
        int leaves = (node.left == null && node.right == null) ? 1 : l[2] + r[2];
        return new int[] {1 + l[0] + r[0], 1 + Math.max(l[1], r[1]), leaves};
    }

    static int[] sizeHeightLeaves(Integer[] values) { return shape(build(values)); }

    static Integer[] serialise(int[] left, int[] right, int n) {
        List<Integer> out = new ArrayList<>();
        List<Integer> queue = new ArrayList<>();
        queue.add(0);
        out.add(0);
        for (int q = 0; q < queue.size(); q++) {
            int id = queue.get(q);
            int[] kids = {left[id], right[id]};
            for (int k : kids) {
                if (k < 0) out.add(null);
                else { out.add(k); queue.add(k); }
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(sizeHeightLeaves(new Integer[] {}), new int[] {0, 0, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(sizeHeightLeaves(new Integer[] {1, null, 2, null, 3}), new int[] {3, 3, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(sizeHeightLeaves(new Integer[] {5}), new int[] {1, 1, 1})) throw new AssertionError("single node");
        if (build(new Integer[] {}) != null) throw new AssertionError("the empty array builds the null tree");
        Random rnd = new Random(15102);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] left = new int[n], right = new int[n], depth = new int[n];
            Arrays.fill(left, -1);
            Arrays.fill(right, -1);
            for (int i = 1; i < n; i++) {
                while (true) {
                    int p = rnd.nextInt(i);
                    boolean useLeft = rnd.nextBoolean();
                    if (useLeft && left[p] < 0) { left[p] = i; depth[i] = depth[p] + 1; break; }
                    if (!useLeft && right[p] < 0) { right[p] = i; depth[i] = depth[p] + 1; break; }
                }
            }
            int height = 0, leaves = 0;
            for (int i = 0; i < n; i++) {
                height = Math.max(height, depth[i] + 1);
                if (left[i] < 0 && right[i] < 0) leaves++;
            }
            Integer[] values = serialise(left, right, n);
            if (!Arrays.equals(sizeHeightLeaves(values), new int[] {n, height, leaves})) throw new AssertionError("differs on " + Arrays.toString(values));
        }
    }
}
```

#### Solution: [Recognize] Maximum Depth of N-ary Tree (LeetCode 559)
<!-- id: tr-max-depth-nary -->

**Approach.** The depth of a node is one plus the largest depth among its children, and a node with an empty child list gets one plus zero, which is 1. A loop over the child list replaces the pair of calls a binary tree would make. The recursion is fine for the stated bound of 10000 nodes in the assertions' shapes, and the oracle avoids recursion altogether by using the parent array, where every node's depth is its parent's depth plus one. The assertions compare on random trees and on a chain of a few hundred nodes.

**Complexity.** O(n) time because each node is entered once, and O(h) stack for tree height h.

```java run
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class MaxDepthNary {
    static int depth(List<List<Integer>> children, int node) {
        int deepest = 0;
        for (int child : children.get(node)) deepest = Math.max(deepest, depth(children, child));
        return 1 + deepest;
    }

    static int maxDepth(List<List<Integer>> children) { return depth(children, 0); }

    static List<List<Integer>> of(int[][] raw) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : raw) {
            List<Integer> kids = new ArrayList<>();
            for (int v : row) kids.add(v);
            out.add(kids);
        }
        return out;
    }

    public static void main(String[] args) {
        if (maxDepth(of(new int[][] {{1, 2}, {3}, {}, {4}, {}})) != 4) throw new AssertionError("example 1");
        if (maxDepth(of(new int[][] {{}})) != 1) throw new AssertionError("example 2");
        Random rnd = new Random(15103);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(16);
            int[] level = new int[n];
            List<List<Integer>> kids = new ArrayList<>();
            for (int i = 0; i < n; i++) kids.add(new ArrayList<>());
            int best = 1;
            for (int i = 1; i < n; i++) {
                int p = rnd.nextInt(i);
                kids.get(p).add(i);
                level[i] = level[p] + 1;
                best = Math.max(best, level[i] + 1);
            }
            if (maxDepth(kids) != best) throw new AssertionError("differs at n = " + n);
        }
        int len = 400;
        List<List<Integer>> chain = new ArrayList<>();
        for (int i = 0; i < len; i++) {
            List<Integer> k = new ArrayList<>();
            if (i + 1 < len) k.add(i + 1);
            chain.add(k);
        }
        if (maxDepth(chain) != len) throw new AssertionError("a chain of " + len + " nodes has depth " + len);
    }
}
```
