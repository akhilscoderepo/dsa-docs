<!-- solutions-for: 01-levels-zigzag-and-views -->
### Levels Zigzag And Views

#### Solution: [Build] Binary Tree Level Order Traversal (LeetCode 102)
<!-- id: tb-level-order -->

**Approach.** Read the queue length once before each ring and remove exactly that many nodes, appending their children for the next ring. The tree is made of real nodes from the array. The oracle is a recursive preorder walk that appends each value to the list for its depth, which never looks at a queue. Five thousand random trees are run through both methods in the assertions, run both examples, and show that rereading the live queue size merges rings into one list.

**Complexity.** Each node is enqueued and dequeued once, giving O(n) time and O(w) queue space for a widest ring w.

```java run
import java.util.*;

public final class LevelOrderRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static List<List<Integer>> levelOrder(Node root) {
        List<List<Integer>> cards = new ArrayList<>();
        if (root == null) return cards;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> ring = new ArrayList<>();
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                ring.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            cards.add(ring);
        }
        return cards;
    }

    static List<List<Integer>> misreadSize(Node root) {
        List<Integer> everything = new ArrayList<>();
        ArrayDeque<Node> queue = new ArrayDeque<>();
        if (root != null) queue.add(root);
        while (!queue.isEmpty()) {
            for (int k = 0; k < queue.size() && !queue.isEmpty(); k++) {
                Node node = queue.poll();
                everything.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        List<List<Integer>> one = new ArrayList<>();
        if (!everything.isEmpty()) one.add(everything);
        return one;
    }

    static void byDepth(Node n, int depth, List<List<Integer>> out) {
        if (n == null) return;
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(n.val);
        byDepth(n.left, depth + 1, out);
        byDepth(n.right, depth + 1, out);
    }

    public static void main(String[] args) {
        if (!levelOrder(build(new Integer[] {3, 9, 20, null, null, 15, 7})).toString().equals("[[3], [9, 20], [15, 7]]")) throw new AssertionError("example 1");
        if (!levelOrder(build(new Integer[] {1, null, 2, null, 3})).toString().equals("[[1], [2], [3]]")) throw new AssertionError("example 2");
        if (!levelOrder(build(new Integer[] {})).isEmpty()) throw new AssertionError("empty tree");
        List<List<Integer>> merged = misreadSize(build(new Integer[] {3, 9, 20, null, null, 15, 7}));
        if (merged.size() != 1 || merged.get(0).size() != 5) throw new AssertionError("a live size reading should blend every ring into one list: " + merged);
        Random rnd = new Random(16101);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 18, -50, 50);
            List<List<Integer>> want = new ArrayList<>();
            byDepth(build(v), 0, want);
            if (!levelOrder(build(v)).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Binary Tree Zigzag Level Order Traversal (LeetCode 103)
<!-- id: tb-zigzag-order -->

**Approach.** Enqueue left then right exactly as in the plain method, and flip a direction flag after each ring. A ring is stored in a `LinkedList`, and a value goes to the front when the flag says right to left. The oracle takes the plain depth groups from a recursive walk and reverses every odd-indexed group afterwards. Both methods are run on thousands of random trees by the assertions and confirm that the first ring of the second example stays untouched while the next one reverses.

**Complexity.** O(n) time for n nodes, with O(w) extra space for the widest ring.

```java run
import java.util.*;

public final class ZigzagRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static List<List<Integer>> zigzag(Node root) {
        List<List<Integer>> cards = new ArrayList<>();
        if (root == null) return cards;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        boolean leftToRight = true;
        while (!queue.isEmpty()) {
            int size = queue.size();
            LinkedList<Integer> ring = new LinkedList<>();
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                if (leftToRight) ring.addLast(node.val); else ring.addFirst(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            cards.add(ring);
            leftToRight = !leftToRight;
        }
        return cards;
    }

    static void byDepth(Node n, int depth, List<List<Integer>> out) {
        if (n == null) return;
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(n.val);
        byDepth(n.left, depth + 1, out);
        byDepth(n.right, depth + 1, out);
    }

    public static void main(String[] args) {
        if (!zigzag(build(new Integer[] {3, 9, 20, null, null, 15, 7})).toString().equals("[[3], [20, 9], [15, 7]]")) throw new AssertionError("example 1");
        if (!zigzag(build(new Integer[] {1, 2, 3, 4, 5, 6, 7, 8, 9})).toString().equals("[[1], [3, 2], [4, 5, 6, 7], [9, 8]]")) throw new AssertionError("example 2");
        if (!zigzag(null).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(16102);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 20, -50, 50);
            List<List<Integer>> want = new ArrayList<>();
            byDepth(build(v), 0, want);
            for (int d = 1; d < want.size(); d += 2) Collections.reverse(want.get(d));
            if (!zigzag(build(v)).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tb-empty-and-chains -->

**Approach.** Return the empty outer list before touching the queue when the root is null, because an `ArrayDeque` throws on `add(null)`. Everything else is the plain ring method, which uses no recursion, so a chain of one hundred thousand levels needs no call stack. The chain is built by a loop so the test itself also avoids recursion. The assertions check that `ArrayDeque.add(null)` really throws, run both examples, check left and right chains of 100000 nodes, and compare against a depth-grouping oracle on small random trees.

**Complexity.** O(n) time and O(1) queue size for a chain, since each ring holds a single node.

```java run
import java.util.*;

public final class ChainRingsRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static List<List<Integer>> rings(Node root) {
        List<List<Integer>> cards = new ArrayList<>();
        if (root == null) return cards;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> ring = new ArrayList<>(size);
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                ring.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            cards.add(ring);
        }
        return cards;
    }

    static void byDepth(Node n, int depth, List<List<Integer>> out) {
        if (n == null) return;
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(n.val);
        byDepth(n.left, depth + 1, out);
        byDepth(n.right, depth + 1, out);
    }

    static Node chain(int n, boolean leanLeft) {
        Node root = new Node(0), tail = root;
        for (int i = 1; i < n; i++) {
            Node next = new Node(i);
            if (leanLeft) tail.left = next; else tail.right = next;
            tail = next;
        }
        return root;
    }

    public static void main(String[] args) {
        boolean threw = false;
        try { new ArrayDeque<Node>().add(null); } catch (NullPointerException expected) { threw = true; }
        if (!threw) throw new AssertionError("ArrayDeque should reject null");
        if (!rings(build(new Integer[] {})).isEmpty()) throw new AssertionError("example 1");
        if (!rings(build(new Integer[] {1, 2, null, 3, null, 4})).toString().equals("[[1], [2], [3], [4]]")) throw new AssertionError("example 2");
        for (boolean lean : new boolean[] {true, false}) {
            List<List<Integer>> got = rings(chain(100000, lean));
            if (got.size() != 100000) throw new AssertionError("chain should have one ring per node");
            for (int d = 0; d < got.size(); d += 9973) {
                if (got.get(d).size() != 1 || got.get(d).get(0) != d) throw new AssertionError("ring " + d);
            }
        }
        Random rnd = new Random(16103);
        for (int t = 0; t < 4000; t++) {
            Integer[] v = randomLevels(rnd, 16, 0, 9);
            List<List<Integer>> want = new ArrayList<>();
            byDepth(build(v), 0, want);
            if (!rings(build(v)).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Right Side View (LeetCode 199)
<!-- id: tb-right-side-view -->

**Approach.** Run the ring loop and record the value of the removal whose counter equals the snapshot minus one. A right child chain is the wrong tool, because a left child under a missing right branch still shows from the side. The oracle walks preorder, left before right, and overwrites the slot for each depth, so the last write at a depth is the rightmost node there. Random trees of many shapes feed both methods in the assertions and check the two examples, including the left-only chain.

**Complexity.** O(n) time and O(w) space, with no list built per ring.

```java run
import java.util.*;

public final class RightViewRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }
    static Integer[] randomLevels(Random rnd, int maxNodes, int lo, int hi) {
        int n = 1 + rnd.nextInt(maxNodes);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(lo + rnd.nextInt(hi - lo + 1));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(lo + rnd.nextInt(hi - lo + 1)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static List<Integer> rightView(Node root) {
        List<Integer> view = new ArrayList<>();
        if (root == null) return view;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                if (k == size - 1) view.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        return view;
    }

    static List<Integer> rightChainOnly(Node root) {
        List<Integer> view = new ArrayList<>();
        for (Node at = root; at != null; at = at.right) view.add(at.val);
        return view;
    }

    static void overwrite(Node n, int depth, List<Integer> slots) {
        if (n == null) return;
        if (slots.size() == depth) slots.add(n.val); else slots.set(depth, n.val);
        overwrite(n.left, depth + 1, slots);
        overwrite(n.right, depth + 1, slots);
    }

    public static void main(String[] args) {
        if (!rightView(build(new Integer[] {1, 2, 3, null, 5, null, 4})).toString().equals("[1, 3, 4]")) throw new AssertionError("example 1");
        if (!rightView(build(new Integer[] {1, 2, null, 3})).toString().equals("[1, 2, 3]")) throw new AssertionError("example 2");
        if (!rightChainOnly(build(new Integer[] {1, 2, null, 3})).toString().equals("[1]")) throw new AssertionError("right chain misses left-hanging nodes");
        if (!rightView(null).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(16104);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 18, -9, 9);
            List<Integer> want = new ArrayList<>();
            overwrite(build(v), 0, want);
            if (!rightView(build(v)).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```
