<!-- solutions-for: 01-tree-representation -->
### Solutions For Node Object Trees

#### Solution: [Build] Construct A Three-Node Tree (Author exercise)
<!-- id: tr-three-node -->

**Approach.**
The method creates the two leaves first, because a node can only hold references to objects that already exist. Each leaf receives `null` for both children. The root then receives the two leaves as its left and right child. The invariant is that every node object is created once, and every field holds an existing node or `null`. The result therefore has exactly three nodes and four `null` fields.

The same section checks two claims of the lesson. A tree whose child points back at the root never reaches a base case in the recursive count. A child shared by two parents is counted twice.

**Complexity.**
- **Time** is O(1), because the method makes exactly three constructor calls.
- **Space** is O(1), because the result holds three nodes, a fixed number.

```java run
import java.util.*;

public final class BuildThree {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Builds the three-node tree.
     * Time: O(1), three constructor calls.
     * Space: O(1), three nodes.
     * Invariant: each field holds an existing node or null.
     */
    static Node build(int a, int b, int c) {
        Node leftLeaf = new Node(b, null, null);       // the left leaf has two empty subtrees
        Node rightLeaf = new Node(c, null, null);      // the right leaf has two empty subtrees
        return new Node(a, leftLeaf, rightLeaf);       // the root links to both leaves
    }

    static int count(Node node) {
        if (node == null) return 0;                    // an empty subtree has no nodes
        return 1 + count(node.left) + count(node.right);   // this node plus both child subtrees
    }

    public static void main(String[] args) {
        // Example 1: the shape and the values.
        Node r = build(1, 2, 3);
        if (r.val != 1 || r.left.val != 2 || r.right.val != 3) throw new AssertionError("values");
        // Both leaves keep four null fields in total.
        int nulls = 0;
        for (Node leaf : new Node[] {r.left, r.right}) {
            if (leaf.left == null) nulls++;
            if (leaf.right == null) nulls++;
        }
        if (nulls != 4) throw new AssertionError("null fields");
        // Example 2: equal values still give three distinct objects.
        Node e = build(5, 5, 5);
        if (e == e.left || e == e.right || e.left == e.right) throw new AssertionError("identity");
        // The count of a tree with three nodes is three.
        if (count(r) != 3) throw new AssertionError("count");
        // A child shared by two parents is counted once per parent.
        Node shared = new Node(9, null, null);
        Node dag = new Node(1, shared, shared);
        if (count(dag) != 3) throw new AssertionError("shared child counted twice");
        // A cycle never reaches the base case, so the recursion overflows the stack.
        Node loop = new Node(1, null, null);
        loop.left = loop;
        boolean overflow = false;
        try { count(loop); } catch (StackOverflowError ex) { overflow = true; }
        if (!overflow) throw new AssertionError("cycle");
        // Random values: the root and both children keep what was passed in.
        Random rnd = new Random(1);
        for (int t = 0; t < 300; t++) {
            int a = rnd.nextInt(2001) - 1000, b = rnd.nextInt(2001) - 1000, c = rnd.nextInt(2001) - 1000;
            Node x = build(a, b, c);
            if (x.val != a || x.left.val != b || x.right.val != c || count(x) != 3) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Count N-Ary Children (Author exercise)
<!-- id: tr-nary-children -->

**Approach.**
Each call receives one node and returns the largest child-list length found in its own subtree. The call starts with the length of its own child list. It then loops over the child list, calls itself on each child, and keeps the larger value. The invariant is that the return value of a call is the maximum child count over exactly the nodes of its subtree.

A leaf has an empty child list, so its loop does nothing and its answer is 0. The recursion needs no base case at `null`, because the input promises that a child list never holds `null`.

**Complexity.**
- **Time** is O(n) for n nodes, because each node is visited once and the child lists hold n - 1 entries in total.
- **Space** is O(h) for the call stack, where h is the height of the tree.

```java run
import java.util.*;

public final class NaryChildren {
    static final class NNode {
        int val;
        List<NNode> children = new ArrayList<>();
        NNode(int val) { this.val = val; }
    }

    /**
     * Returns the largest child count in the subtree of node.
     * Time: O(n), each node is visited once.
     * Space: O(h), one frame per level.
     * Invariant: the result covers exactly the nodes of the subtree.
     */
    static int maxChildren(NNode node) {
        int best = node.children.size();                       // this node's own child count
        for (NNode child : node.children) {                    // one call per child, whatever the count
            best = Math.max(best, maxChildren(child));         // keep the larger of the two values
        }
        return best;                                           // the maximum over the whole subtree
    }

    static NNode random(Random rnd, int[] budget, int depth) {
        NNode n = new NNode(rnd.nextInt(10));
        budget[0]--;                                           // each created node uses one unit
        int kids = depth > 6 ? 0 : rnd.nextInt(5);
        for (int i = 0; i < kids && budget[0] > 0; i++) n.children.add(random(rnd, budget, depth + 1));
        return n;
    }

    // Oracle: breadth-first walk with a queue, tracking the maximum list size.
    static int oracle(NNode root) {
        int best = 0;
        Deque<NNode> q = new ArrayDeque<>();
        q.add(root);
        while (!q.isEmpty()) {                                 // visit every node once
            NNode n = q.poll();
            best = Math.max(best, n.children.size());
            q.addAll(n.children);
        }
        return best;
    }

    public static void main(String[] args) {
        // Example 1: root 1 with children 2, 3, 4 and node 3 with child 5.
        NNode r = new NNode(1), a = new NNode(2), b = new NNode(3), c = new NNode(4);
        r.children.addAll(List.of(a, b, c));
        b.children.add(new NNode(5));
        if (maxChildren(r) != 3) throw new AssertionError("ex1");
        // Example 2: a chain has one child per node, so the answer is 1.
        NNode chain = new NNode(0), cur = chain;
        for (int i = 1; i < 20; i++) { NNode nx = new NNode(i); cur.children.add(nx); cur = nx; }
        if (maxChildren(chain) != 1) throw new AssertionError("ex2");
        // A single leaf has an empty child list and answer 0.
        if (maxChildren(new NNode(1)) != 0) throw new AssertionError("leaf");
        // A widest node deep in the tree still wins over the root.
        NNode deep = new NNode(1), mid = new NNode(2);
        deep.children.add(mid);
        for (int i = 0; i < 6; i++) mid.children.add(new NNode(i));
        if (maxChildren(deep) != 6) throw new AssertionError("deep");
        // Random trees must match the queue-based oracle.
        Random rnd = new Random(2);
        for (int t = 0; t < 400; t++) {
            NNode x = random(rnd, new int[] {1 + rnd.nextInt(60)}, 0);
            if (maxChildren(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And Single-Node Trees (Author exercise)
<!-- id: tr-leaf-count -->

**Approach.**
The method has two base cases. A `null` reference is an empty subtree and has no leaves, so it returns 0. A node whose `left` and `right` are both `null` is a leaf, so it returns 1. Any other node returns the sum of the leaf counts of its two sides. The second base case is needed because a leaf has two empty sides. Without it, the sum rule would add 0 and 0 and return 0 for a leaf.

Each call returns the number of leaves in exactly its subtree.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives one call.
- **Space** is O(h) for the call stack, where h is the height of the tree.

```java run
import java.util.*;

public final class LeafCount {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Counts the leaves of the subtree of node.
     * Time: O(n), one call per node and per null side.
     * Space: O(h), one frame per level.
     * Invariant: the result counts leaves of exactly this subtree.
     */
    static int leaves(Node node) {
        if (node == null) return 0;                              // an empty subtree has no leaves
        if (node.left == null && node.right == null) return 1;   // both sides empty: this node is a leaf
        return leaves(node.left) + leaves(node.right);           // otherwise add the two sides
    }

    static Node random(Random rnd, int depth) {
        if (depth > 6 || rnd.nextInt(4) == 0) return null;       // random empty side
        return new Node(rnd.nextInt(10), random(rnd, depth + 1), random(rnd, depth + 1));
    }

    // Oracle: iterative walk that tests the leaf condition on every visited node.
    static int oracle(Node root) {
        int count = 0;
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {                               // visit every node
            Node n = stack.pop();
            if (n.left == null && n.right == null) count++;
            if (n.left != null) stack.push(n.left);
            if (n.right != null) stack.push(n.right);
        }
        return count;
    }

    public static void main(String[] args) {
        // Example 1: the empty tree has no leaves.
        if (leaves(null) != 0) throw new AssertionError("empty");
        // Example 2: root 1 with only a right child 2 has one leaf.
        Node one = new Node(1, null, new Node(2, null, null));
        if (leaves(one) != 1) throw new AssertionError("one child");
        // A single node is one leaf.
        if (leaves(new Node(7, null, null)) != 1) throw new AssertionError("single");
        // A node with two leaf children has two leaves, not three.
        if (leaves(new Node(1, new Node(2, null, null), new Node(3, null, null))) != 2) throw new AssertionError("two");
        // Random trees must match the iterative oracle.
        Random rnd = new Random(3);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            if (leaves(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Maximum Depth Of N-ary Tree (LeetCode 559)
<!-- id: tr-nary-depth -->

**Approach.**
The depth of a node is one more than the depth of its deepest child, and a node with an empty child list has depth 1. A call returns 0 for `null`, which covers the empty tree. For any other node the call loops over the child list, keeps the largest child depth, and adds one for the node itself. The invariant is that the return value is the node count of the longest downward path inside exactly this subtree.

**Complexity.**
- **Time** is O(n), because each node is visited once and each child-list entry is read once.
- **Space** is O(h) for the call stack, where h is the height of the tree.

```java run
import java.util.*;

public final class NaryDepth {
    static final class NNode {
        int val;
        List<NNode> children = new ArrayList<>();
        NNode(int val) { this.val = val; }
    }

    /**
     * Returns the node count of the longest downward path.
     * Time: O(n), each node is visited once.
     * Space: O(h), one frame per level.
     * Invariant: the result is the depth of exactly this subtree.
     */
    static int depth(NNode node) {
        if (node == null) return 0;                       // the empty tree has depth 0
        int deepest = 0;                                  // a leaf has no child depth
        for (NNode child : node.children) {               // visit every child, however many
            deepest = Math.max(deepest, depth(child));    // keep the deepest child
        }
        return deepest + 1;                               // count this node as well
    }

    static NNode random(Random rnd, int[] budget, int depth) {
        NNode n = new NNode(rnd.nextInt(10));
        budget[0]--;
        int kids = depth > 8 ? 0 : rnd.nextInt(4);
        for (int i = 0; i < kids && budget[0] > 0; i++) n.children.add(random(rnd, budget, depth + 1));
        return n;
    }

    // Oracle: level-by-level walk, one round per level.
    static int oracle(NNode root) {
        if (root == null) return 0;
        int levels = 0;
        List<NNode> level = List.of(root);
        while (!level.isEmpty()) {                        // one round per level of the tree
            levels++;
            List<NNode> next = new ArrayList<>();
            for (NNode n : level) next.addAll(n.children);
            level = next;
        }
        return levels;
    }

    public static void main(String[] args) {
        // Example 1: root 1 with children 2, 3, 4 and node 3 with child 5 has depth 3.
        NNode r = new NNode(1), b = new NNode(3);
        r.children.addAll(List.of(new NNode(2), b, new NNode(4)));
        b.children.add(new NNode(5));
        if (depth(r) != 3) throw new AssertionError("ex1");
        // Example 2: a single node has depth 1.
        if (depth(new NNode(1)) != 1) throw new AssertionError("ex2");
        // The empty tree has depth 0.
        if (depth(null) != 0) throw new AssertionError("empty");
        // Random trees must match the level-by-level oracle.
        Random rnd = new Random(4);
        for (int t = 0; t < 400; t++) {
            NNode x = random(rnd, new int[] {1 + rnd.nextInt(80)}, 0);
            if (depth(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```
