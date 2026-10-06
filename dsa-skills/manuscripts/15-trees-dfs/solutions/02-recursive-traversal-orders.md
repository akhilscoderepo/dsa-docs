<!-- solutions-for: 02-recursive-traversal-orders -->
### Solutions For Three Walking Orders

#### Solution: [Build] Binary Tree Preorder Traversal (LeetCode 144)
<!-- id: ro-preorder -->

**Approach.**
The method keeps one list that the caller creates. A call on `null` returns at once. A call on a node first appends the value of the node, then calls itself on `left`, then on `right`. The invariant is that each call appends exactly the preorder of its own subtree. The new values follow everything that was in the list before the call.

The same section checks two claims of the lesson: the list must be fresh for each walk, and reversing the preorder list does not give postorder.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives one call.
- **Space** is O(h) on the chain of open calls, where h is the height, plus the n result values.

```java run
import java.util.*;

public final class PreorderWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final List<Integer> shared = new ArrayList<>();   // a static list that would leak between walks

    /**
     * Appends the preorder of the subtree of node to out.
     * Time: O(n), one call per node and per null side.
     * Space: O(h) for the stack.
     * Invariant: out grows by exactly this subtree, node first.
     */
    static void preorder(Node node, List<Integer> out) {
        if (node == null) return;                  // an empty subtree adds nothing
        out.add(node.val);                         // the action runs before both child calls
        preorder(node.left, out);                  // the whole left subtree comes next
        preorder(node.right, out);                 // the whole right subtree comes last
    }

    static List<Integer> preorderList(Node root) {
        List<Integer> out = new ArrayList<>();     // a fresh list for every walk
        preorder(root, out);
        return out;
    }

    // Oracle: iterative walk with an explicit stack, pushing the right child first.
    static List<Integer> oracle(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {                 // one pop per node
            Node n = stack.pop();
            out.add(n.val);
            if (n.right != null) stack.push(n.right);
            if (n.left != null) stack.push(n.left);
        }
        return out;
    }

    static Node random(Random rnd, int depth) {
        if (depth > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(201) - 100, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    static List<Integer> postorder(Node node) {
        List<Integer> out = new ArrayList<>();
        if (node == null) return out;
        out.addAll(postorder(node.left));
        out.addAll(postorder(node.right));
        out.add(node.val);
        return out;
    }

    public static void main(String[] args) {
        // Example 1: root 4 with 2 (children 1 and 3) and 6.
        Node t1 = new Node(4, new Node(2, new Node(1, null, null), new Node(3, null, null)), new Node(6, null, null));
        if (!preorderList(t1).equals(List.of(4, 2, 1, 3, 6))) throw new AssertionError("ex1");
        // Example 2: root 8 with right child 9 that has left child 7.
        Node t2 = new Node(8, null, new Node(9, new Node(7, null, null), null));
        if (!preorderList(t2).equals(List.of(8, 9, 7))) throw new AssertionError("ex2");
        // The empty tree gives the empty list.
        if (!preorderList(null).isEmpty()) throw new AssertionError("empty");
        // A static list keeps the values of the previous walk.
        preorder(t2, shared);
        preorder(t2, shared);
        if (shared.size() != 6) throw new AssertionError("static list mixes walks");
        // Reversing the preorder of root 1 with children 2 and 3 gives 3, 2, 1, but postorder is 2, 3, 1.
        Node t3 = new Node(1, new Node(2, null, null), new Node(3, null, null));
        List<Integer> rev = new ArrayList<>(preorderList(t3));
        Collections.reverse(rev);
        if (!rev.equals(List.of(3, 2, 1)) || !postorder(t3).equals(List.of(2, 3, 1))) throw new AssertionError("reverse claim");
        // The preorder of a one-sided tree is not its inorder: 3, 5, 4 against 3, 4, 5.
        Node t4 = new Node(3, null, new Node(5, new Node(4, null, null), null));
        if (!preorderList(t4).equals(List.of(3, 5, 4))) throw new AssertionError("one side");
        // Random trees must match the iterative oracle.
        Random rnd = new Random(5);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            if (!preorderList(x).equals(oracle(x))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: ro-inorder -->

**Approach.**
The method is the preorder method with one line moved. A call returns at `null`, then calls itself on `left`, then appends its own value, then calls itself on `right`. The invariant is that when the call on a node returns, the list ends with the inorder of that subtree. The left subtree is always complete before the node, and the right subtree always follows it.

The first value written is the value of the leftmost node, which the walk reaches by following `left` references from the root.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives one call.
- **Space** is O(h) on the chain of open calls, plus the n result values.

```java run
import java.util.*;

public final class InorderWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Appends the inorder of the subtree of node to out.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: out grows by exactly this subtree, left side first, node in the middle.
     */
    static void inorder(Node node, List<Integer> out) {
        if (node == null) return;                  // an empty subtree adds nothing
        inorder(node.left, out);                   // every left node comes before this node
        out.add(node.val);                         // the action sits between the child calls
        inorder(node.right, out);                  // every right node comes after this node
    }

    static List<Integer> inorderList(Node root) {
        List<Integer> out = new ArrayList<>();
        inorder(root, out);
        return out;
    }

    // Oracle: iterative walk that pushes the whole left spine, then pops and moves right.
    static List<Integer> oracle(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {  // stop when no node is left anywhere
            while (cur != null) { stack.push(cur); cur = cur.left; }
            cur = stack.pop();
            out.add(cur.val);
            cur = cur.right;
        }
        return out;
    }

    static Node random(Random rnd, int depth) {
        if (depth > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(201) - 100, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 5, left 3 with right child 4, right 7.
        Node t1 = new Node(5, new Node(3, null, new Node(4, null, null)), new Node(7, null, null));
        if (!inorderList(t1).equals(List.of(3, 4, 5, 7))) throw new AssertionError("ex1");
        // Example 2: root 2, left 1, whose left child is 0.
        Node t2 = new Node(2, new Node(1, new Node(0, null, null), null), null);
        if (!inorderList(t2).equals(List.of(0, 1, 2))) throw new AssertionError("ex2");
        // The empty tree gives the empty list.
        if (!inorderList(null).isEmpty()) throw new AssertionError("empty");
        // The inorder of a general tree is not sorted: root 1 with left child 2.
        if (inorderList(new Node(1, new Node(2, null, null), null)).equals(List.of(1, 2))) throw new AssertionError("not sorted");
        // The one-sided tree 3, right 5, 5 with left child 4 gives 3, 4, 5.
        Node t4 = new Node(3, null, new Node(5, new Node(4, null, null), null));
        if (!inorderList(t4).equals(List.of(3, 4, 5))) throw new AssertionError("one side");
        // Random trees must match the iterative oracle.
        Random rnd = new Random(6);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            if (!inorderList(x).equals(oracle(x))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: ro-marked -->

**Approach.**
The method is the inorder walk with one change: the base case at `null` appends the text `x` and returns. Each call on a node walks the left side, appends the value, and walks the right side. The invariant is that a call returns with the marked inorder of its own subtree appended, so each missing side keeps its place.

The output alternates `x` and a value, starting and ending with `x`. Between two consecutive nodes in inorder, exactly one empty side lies. Either the later node has no left child, or the earlier node has no right child. The result therefore has `n + 1` entries of `x` for `n` nodes.

**Complexity.**
- **Time** is O(n), because there are n node calls and n + 1 `null` calls.
- **Space** is O(h) on the chain of open calls, plus 2n + 1 result entries.

```java run
import java.util.*;

public final class MarkedInorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Appends the marked inorder of the subtree of node to out.
     * Time: O(n), n node calls plus n + 1 null calls.
     * Space: O(h) for the stack.
     * Invariant: each empty subtree appends one x at its position.
     */
    static void marked(Node node, List<String> out) {
        if (node == null) { out.add("x"); return; }    // an empty side is written, not skipped
        marked(node.left, out);                        // the left side keeps its place
        out.add(String.valueOf(node.val));             // the node sits between its sides
        marked(node.right, out);                       // the right side keeps its place
    }

    static List<String> markedList(Node root) {
        List<String> out = new ArrayList<>();
        marked(root, out);
        return out;
    }

    // Oracle: the plain inorder values joined by x, with an x at both ends.
    static List<String> oracle(Node root) {
        List<Integer> vals = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) { stack.push(cur); cur = cur.left; }
            cur = stack.pop();
            vals.add(cur.val);
            cur = cur.right;
        }
        List<String> out = new ArrayList<>();
        out.add("x");                                  // an x before the first node
        for (int v : vals) { out.add(String.valueOf(v)); out.add("x"); }   // an x after each node
        return out;
    }

    static Node random(Random rnd, int depth) {
        if (depth > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(201) - 100, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) {
        // Example 1: the empty tree gives a single x.
        if (!markedList(null).equals(List.of("x"))) throw new AssertionError("empty");
        // Example 2: root 1 with right child 2.
        Node t2 = new Node(1, null, new Node(2, null, null));
        if (!markedList(t2).equals(List.of("x", "1", "x", "2", "x"))) throw new AssertionError("ex2");
        // A left-only chain puts every x before the nodes except the last one.
        Node t3 = new Node(3, new Node(2, null, null), null);
        if (!markedList(t3).equals(List.of("x", "2", "x", "3", "x"))) throw new AssertionError("left chain");
        // Random trees match the oracle, alternate x and values, and hold n + 1 marks.
        Random rnd = new Random(7);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<String> got = markedList(x);
            if (!got.equals(oracle(x))) throw new AssertionError("random " + t);
            for (int i = 0; i < got.size(); i++) if (got.get(i).equals("x") != (i % 2 == 0)) throw new AssertionError("alternation " + t);
            if (got.size() % 2 != 1) throw new AssertionError("odd length " + t);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: ro-postorder -->

**Approach.**
The action moves to the end of the call. A call on `null` returns. A call on a node calls itself on `left`, then on `right`, then appends its own value. The invariant is that each call appends exactly the postorder of its own subtree. A node therefore appears after every node below it. The root of the whole tree is therefore the last value.

**Complexity.**
- **Time** is O(n), because each node and each `null` side receives one call.
- **Space** is O(h) on the chain of open calls, plus the n result values.

```java run
import java.util.*;

public final class PostorderWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Appends the postorder of the subtree of node to out.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: out grows by exactly this subtree, node last.
     */
    static void postorder(Node node, List<Integer> out) {
        if (node == null) return;                  // an empty subtree adds nothing
        postorder(node.left, out);                 // left subtree first
        postorder(node.right, out);                // right subtree second
        out.add(node.val);                         // the action runs after both child calls
    }

    static List<Integer> postorderList(Node root) {
        List<Integer> out = new ArrayList<>();
        postorder(root, out);
        return out;
    }

    // Oracle: walk node, right, left with a stack, then reverse the result.
    static List<Integer> oracle(Node root) {
        List<Integer> rev = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {
            Node n = stack.pop();
            rev.add(n.val);
            if (n.left != null) stack.push(n.left);
            if (n.right != null) stack.push(n.right);
        }
        Collections.reverse(rev);
        return rev;
    }

    static Node random(Random rnd, int depth) {
        if (depth > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(201) - 100, random(rnd, depth + 1), random(rnd, depth + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 5, left 3 with children 1 and 4, right 8 with right child 9.
        Node t1 = new Node(5, new Node(3, new Node(1, null, null), new Node(4, null, null)),
                new Node(8, null, new Node(9, null, null)));
        if (!postorderList(t1).equals(List.of(1, 4, 3, 9, 8, 5))) throw new AssertionError("ex1");
        // Example 2: a single node.
        if (!postorderList(new Node(7, null, null)).equals(List.of(7))) throw new AssertionError("ex2");
        // The root is always the last value, and the empty tree gives the empty list.
        if (postorderList(t1).get(5) != 5 || !postorderList(null).isEmpty()) throw new AssertionError("root last");
        // The one-sided tree 3, right 5, 5 with left child 4 gives 4, 5, 3.
        Node t4 = new Node(3, null, new Node(5, new Node(4, null, null), null));
        if (!postorderList(t4).equals(List.of(4, 5, 3))) throw new AssertionError("one side");
        // Random trees must match the reversed node-right-left oracle, and the root comes last.
        Random rnd = new Random(8);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<Integer> got = postorderList(x);
            if (!got.equals(oracle(x))) throw new AssertionError("random " + t);
            if (x != null && got.get(got.size() - 1) != x.val) throw new AssertionError("root " + t);
        }
    }
}
```
