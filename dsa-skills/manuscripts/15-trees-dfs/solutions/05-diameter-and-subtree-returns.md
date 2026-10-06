<!-- solutions-for: 05-diameter-and-subtree-returns -->
### Solutions For Longest Path In A Tree

#### Solution: [Build] Return Subtree Height (Author exercise)
<!-- id: dr-heights -->

**Approach.**
The call returns the height of its subtree in nodes and appends that height to a shared list after both child calls have returned. A call on `null` returns 0 and appends nothing. A call on a node first computes the two child heights, then returns one plus the larger one, and appends that value. The invariant is that the list receives each height exactly when its call finishes, so the order is left subtree, right subtree, node.

**Complexity.**
- **Time** is O(n), because each node receives one call.
- **Space** is O(h) for the recursion depth, plus the n entries of the result.

```java run
import java.util.*;

public final class SubtreeHeights {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the height of the subtree and appends it to out.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: out receives the height of a node after both children finished.
     */
    static int heights(Node node, List<Integer> out) {
        if (node == null) return 0;                      // an empty subtree has height 0 and no entry
        int l = heights(node.left, out);                 // left heights are appended first
        int r = heights(node.right, out);                // right heights follow
        int h = 1 + Math.max(l, r);                      // the taller side plus this node
        out.add(h);                                      // the node's own entry comes last
        return h;
    }

    static List<Integer> heightList(Node root) {
        List<Integer> out = new ArrayList<>();
        heights(root, out);
        return out;
    }

    // Oracle: the postorder node list from an explicit walk, each height measured separately.
    static int measure(Node n) { return n == null ? 0 : 1 + Math.max(measure(n.left), measure(n.right)); }

    static void post(Node n, List<Node> out) {
        if (n == null) return;
        post(n.left, out);
        post(n.right, out);
        out.add(n);
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 4 with left 2 and right 6, where 6 has left child 5.
        Node t1 = new Node(4, new Node(2, null, null), new Node(6, new Node(5, null, null), null));
        if (!heightList(t1).equals(List.of(1, 1, 2, 3))) throw new AssertionError("ex1");
        // Example 2: a single node gives 1, and the empty tree gives the empty list.
        if (!heightList(new Node(9, null, null)).equals(List.of(1)) || !heightList(null).isEmpty()) throw new AssertionError("small");
        // Random trees match one separate height measurement per node, in finishing order.
        Random rnd = new Random(17);
        for (int t = 0; t < 500; t++) {
            Node x = random(rnd, 0);
            List<Node> order = new ArrayList<>();
            post(x, order);
            List<Integer> want = new ArrayList<>();
            for (Node n : order) want.add(measure(n));
            if (!heightList(x).equals(want)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] Diameter Of Binary Tree (LeetCode 543)
<!-- id: dr-diameter -->

**Approach.**
Each call returns a `Summary` with the height of its subtree in nodes and the best path length in edges found inside it. A call on `null` returns two zeros. A call on a node reads the two child summaries and forms `through`, the sum of the two child heights. That sum is the edge count of the complete path with this node on top. The best value is the maximum of `through` and the two child best values. The height is one plus the larger child height.

The invariant is that the height describes a single branch that a parent can extend, and the best value describes the longest path anywhere below. The complete path is never returned as a branch. The check below shows that returning it gives a wrong answer.

**Complexity.**
- **Time** is O(n), because each node receives one call.
- **Space** is O(h) for the recursion depth, because each call holds one small summary.

```java run
import java.util.*;

public final class DiameterSummary {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    record Summary(int height, int best) {}

    /**
     * Returns the height in nodes and the best path in edges of the subtree.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: height is a single branch, best is the longest path inside.
     */
    static Summary summarize(Node node) {
        if (node == null) return new Summary(0, 0);               // an empty subtree has no nodes and no edges
        Summary l = summarize(node.left);                         // left subtree finishes first
        Summary r = summarize(node.right);                        // then the right subtree
        int through = l.height() + r.height();                    // edges of the complete path with this node on top
        int best = Math.max(through, Math.max(l.best(), r.best())); // the best path may lie below
        return new Summary(1 + Math.max(l.height(), r.height()), best); // only one branch goes up
    }

    static int diameter(Node root) { return summarize(root).best(); }

    // Broken variant: returns the complete path as if it were a branch.
    static int[] broken(Node node) {
        if (node == null) return new int[] {0, 0};
        int[] l = broken(node.left), r = broken(node.right);
        int through = l[0] + r[0];
        return new int[] {through + 1, Math.max(through, Math.max(l[1], r[1]))};
    }

    // Oracle: breadth-first search from every node over an undirected edge list.
    static int oracle(Node root) {
        if (root == null) return 0;
        List<Node> nodes = new ArrayList<>();
        Map<Node, List<Node>> adj = new IdentityHashMap<>();
        Deque<Node> st = new ArrayDeque<>();
        st.push(root);
        while (!st.isEmpty()) {                                   // collect nodes and undirected edges
            Node n = st.pop();
            nodes.add(n);
            adj.putIfAbsent(n, new ArrayList<>());
            for (Node c : new Node[] {n.left, n.right}) {
                if (c == null) continue;
                adj.putIfAbsent(c, new ArrayList<>());
                adj.get(n).add(c);
                adj.get(c).add(n);
                st.push(c);
            }
        }
        int best = 0;
        for (Node s : nodes) {                                    // one search per start node
            Map<Node, Integer> dist = new IdentityHashMap<>();
            Deque<Node> q = new ArrayDeque<>();
            q.add(s);
            dist.put(s, 0);
            while (!q.isEmpty()) {
                Node n = q.poll();
                best = Math.max(best, dist.get(n));
                for (Node m : adj.get(n)) if (!dist.containsKey(m)) { dist.put(m, dist.get(n) + 1); q.add(m); }
            }
        }
        return best;
    }

    static Node random(Random rnd, int d) {
        if (d > 7 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 6, left 2 with chain 1 and 0, right 8.
        Node t1 = new Node(6, new Node(2, new Node(1, new Node(0, null, null), null), null), new Node(8, null, null));
        if (diameter(t1) != 4) throw new AssertionError("ex1");
        // Example 2: the best path avoids the root.
        Node t2 = new Node(1, new Node(2, new Node(3, new Node(5, null, null), null), new Node(4, null, new Node(6, null, null))), null);
        if (diameter(t2) != 4) throw new AssertionError("ex2");
        // A single node and the empty tree have diameter 0.
        if (diameter(new Node(1, null, null)) != 0 || diameter(null) != 0) throw new AssertionError("small");
        // Returning the complete path as a branch overstates the answer: 4 edges for root 1, left 2 (4, 5), right 3.
        Node t3 = new Node(1, new Node(2, new Node(4, null, null), new Node(5, null, null)), new Node(3, null, null));
        if (diameter(t3) != 3 || broken(t3)[1] != 4) throw new AssertionError("false friend");
        // Random trees match the all-pairs search.
        Random rnd = new Random(18);
        for (int t = 0; t < 400; t++) {
            Node x = random(rnd, 0);
            if (diameter(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Boundary] Nodes Versus Edges (Author exercise)
<!-- id: dr-node-count -->

**Approach.**
The method needs the same summary, and the unit of the final answer decides one extra rule. A path with `k` edges has `k + 1` nodes, but only when the tree is not empty. The method therefore returns 0 for `null` before any addition, and it returns the edge diameter plus one for every other tree. The invariant is that the helper works in edges, and the single conversion happens once at the top, so no recursive call mixes the two units.

**Complexity.**
- **Time** is O(n), because each node receives one call.
- **Space** is O(h) for the recursion depth.

```java run
import java.util.*;

public final class DiameterNodes {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    record Summary(int height, int best) {}

    static Summary summarize(Node node) {
        if (node == null) return new Summary(0, 0);               // heights in nodes, paths in edges
        Summary l = summarize(node.left);
        Summary r = summarize(node.right);
        int through = l.height() + r.height();
        return new Summary(1 + Math.max(l.height(), r.height()), Math.max(through, Math.max(l.best(), r.best())));
    }

    /**
     * Returns how many nodes lie on the longest path.
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: the helper counts edges, and the conversion to nodes happens once here.
     */
    static int longestPathNodes(Node root) {
        if (root == null) return 0;                               // no path exists, so no node is counted
        return summarize(root).best() + 1;                        // k edges join k + 1 nodes
    }

    // Oracle: compare every pair of nodes by the number of nodes on the route between them.
    static int oracle(Node root) {
        if (root == null) return 0;
        List<Node> all = new ArrayList<>();
        Map<Node, Node> parent = new IdentityHashMap<>();
        Deque<Node> st = new ArrayDeque<>();
        st.push(root);
        parent.put(root, null);
        while (!st.isEmpty()) {
            Node n = st.pop();
            all.add(n);
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); st.push(c); }
        }
        int best = 1;
        for (Node a : all) for (Node b : all) {                   // every ordered pair
            List<Node> up = new ArrayList<>();
            for (Node x = a; x != null; x = parent.get(x)) up.add(x);   // ancestors of a, including a
            Set<Node> seen = Collections.newSetFromMap(new IdentityHashMap<>());
            seen.addAll(up);
            int steps = 0;
            Node x = b;
            while (!seen.contains(x)) { x = parent.get(x); steps++; }   // climb from b to the meeting node
            int toMeet = up.indexOf(x);                           // edges from a to the meeting node
            best = Math.max(best, toMeet + steps + 1);
        }
        return best;
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(10), random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: the empty tree gives 0 and not 1.
        if (longestPathNodes(null) != 0) throw new AssertionError("empty");
        // Example 2: root 1 with left child 2 gives 2 nodes.
        if (longestPathNodes(new Node(1, new Node(2, null, null), null)) != 2) throw new AssertionError("ex2");
        // A single node is a path of one node.
        if (longestPathNodes(new Node(1, null, null)) != 1) throw new AssertionError("single");
        // A path of one node has no edges, so the edge diameter of a single node is 0.
        if (summarize(new Node(1, null, null)).best() != 0) throw new AssertionError("edges");
        // Random trees match the all-pairs oracle.
        Random rnd = new Random(19);
        for (int t = 0; t < 300; t++) {
            Node x = random(rnd, 0);
            if (longestPathNodes(x) != oracle(x)) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: dr-max-path -->

**Approach.**
The return value of a call is the best single branch that starts at the node, measured as a sum. A child branch with a negative sum only hurts, so the call replaces a negative child result with 0, which means the path stops at the node. The call then forms the complete path at the node: its own value plus the two non-negative child gains. That number is compared with the best answer so far and is not returned. The call returns its own value plus the larger child gain, so the parent receives one branch.

The invariant is that the returned gain is the largest sum of a single branch starting at the node, and `best` holds the largest complete-path sum seen. The method starts `best` at the smallest `int` value, because every value may be negative and the answer must still hold one real node.

**Complexity.**
- **Time** is O(n), because each node receives one call.
- **Space** is O(h) for the recursion depth, and `best` is a one-element array.

```java run
import java.util.*;

public final class MaxPathSum {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    /**
     * Returns the best single-branch sum from node downward and updates best[0].
     * Time: O(n).
     * Space: O(h) for the stack.
     * Invariant: the return value is a branch, best[0] is the best complete path seen.
     */
    static int gain(Node node, int[] best) {
        if (node == null) return 0;                              // an empty side adds nothing
        int l = Math.max(0, gain(node.left, best));              // drop a negative left branch
        int r = Math.max(0, gain(node.right, best));             // drop a negative right branch
        best[0] = Math.max(best[0], node.val + l + r);           // the complete path with this node on top
        return node.val + Math.max(l, r);                        // the parent extends only one branch
    }

    static int maxPathSum(Node root) {
        int[] best = {Integer.MIN_VALUE};                        // all-negative trees must still report a real sum
        gain(root, best);
        return best[0];
    }

    // Oracle: the best path sum over all pairs of start and end nodes, found by a search from each start.
    static int oracle(Node root) {
        List<Node> all = new ArrayList<>();
        Map<Node, List<Node>> adj = new IdentityHashMap<>();
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
        for (Node s : all) best = Math.max(best, from(s, null, adj, s.val));
        return best;
    }

    static int from(Node n, Node parent, Map<Node, List<Node>> adj, int sum) {
        int best = sum;                                          // the path may stop here
        for (Node m : adj.get(n)) if (m != parent) best = Math.max(best, from(m, n, adj, sum + m.val));
        return best;
    }

    static Node random(Random rnd, int d) {
        if (d > 6 || rnd.nextInt(4) == 0) return null;
        return new Node(rnd.nextInt(21) - 10, random(rnd, d + 1), random(rnd, d + 1));
    }

    public static void main(String[] args) {
        // Example 1: root 2 with children -1 and 3 gives 2 + 3.
        if (maxPathSum(new Node(2, new Node(-1, null, null), new Node(3, null, null))) != 5) throw new AssertionError("ex1");
        // Example 2: all values negative gives the largest single value.
        if (maxPathSum(new Node(-3, new Node(-5, null, null), new Node(-2, null, null))) != -2) throw new AssertionError("ex2");
        // A single negative node returns its own value.
        if (maxPathSum(new Node(-7, null, null)) != -7) throw new AssertionError("single");
        // A path that avoids the root wins when the root is very negative.
        Node t = new Node(-50, new Node(10, new Node(20, null, null), new Node(30, null, null)), null);
        if (maxPathSum(t) != 60) throw new AssertionError("avoids root");
        // Random trees match the all-pairs oracle.
        Random rnd = new Random(20);
        for (int k = 0; k < 400; k++) {
            Node x = random(rnd, 0);
            if (x == null) continue;
            if (maxPathSum(x) != oracle(x)) throw new AssertionError("random " + k);
        }
    }
}
```
