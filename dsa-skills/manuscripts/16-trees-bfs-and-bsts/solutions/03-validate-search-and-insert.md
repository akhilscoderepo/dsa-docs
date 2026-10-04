<!-- solutions-for: 03-validate-search-and-insert -->
### Validate Search And Insert

#### Solution: [Build] Search in a Binary Search Tree (LeetCode 700)
<!-- id: tb-bst-search -->

**Approach.** Compare the key with the current node and follow only the child that can still hold it, stopping at a match or at `null`. The subtree is returned as a level-order array, which is empty when nothing matched. The oracle ignores order completely: it collects every node in a preorder list and takes the first one whose value equals the key. The assertions compare the two on random search trees with keys that are both present and absent, and count how many comparisons the real search made to show that it never exceeds the tree height.

**Complexity.** O(h) time and O(1) space, which is O(n) in the worst case of a chain.

```java run
import java.util.*;

public final class BstSearchRun {
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
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Node plainInsert(Node root, int key) {
        if (root == null) return new Node(key);
        Node at = root;
        while (true) {
            if (key == at.val) return root;
            if (key < at.val) { if (at.left == null) { at.left = new Node(key); return root; } at = at.left; }
            else { if (at.right == null) { at.right = new Node(key); return root; } at = at.right; }
        }
    }

    static Node randomBst(Random rnd, int maxNodes, int range) {
        Node root = null;
        int n = rnd.nextInt(maxNodes + 1);
        for (int i = 0; i < n; i++) root = plainInsert(root, rnd.nextInt(range));
        return root;
    }

    static void inorderInto(Node n, List<Integer> out) {
        if (n == null) return;
        inorderInto(n.left, out);
        out.add(n.val);
        inorderInto(n.right, out);
    }
    static int steps;

    static Node search(Node root, int key) {
        Node node = root;
        while (node != null && node.val != key) {
            steps++;
            node = key < node.val ? node.left : node.right;
        }
        return node;
    }

    static int height(Node n) {
        return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right));
    }

    static void preorder(Node n, List<Node> out) {
        if (n == null) return;
        out.add(n);
        preorder(n.left, out);
        preorder(n.right, out);
    }

    public static void main(String[] args) {
        Node sample = build(new Integer[] {4, 2, 7, 1, 3});
        if (!Arrays.toString(levels(search(sample, 2))).equals("[2, 1, 3]")) throw new AssertionError("example 1");
        if (levels(search(sample, 5)).length != 0) throw new AssertionError("example 2");
        if (search(null, 3) != null) throw new AssertionError("empty tree");
        Random rnd = new Random(16301);
        for (int t = 0; t < 6000; t++) {
            Node root = randomBst(rnd, 16, 40);
            int key = rnd.nextInt(45);
            List<Node> all = new ArrayList<>();
            preorder(root, all);
            Node want = null;
            for (Node n : all) if (n.val == key) { want = n; break; }
            steps = 0;
            Node got = search(root, key);
            if (got != want) throw new AssertionError("wrong node for key " + key);
            if (steps > height(root)) throw new AssertionError("more steps than the height");
        }
    }
}
```

#### Solution: [Vary] Insert into a Binary Search Tree (LeetCode 701)
<!-- id: tb-bst-insert -->

**Approach.** Recurse down the one path the key would take and return a fresh node when the path runs off the tree; each caller stores the returned branch in its link, so nothing already in the tree moves. The oracle rebuilds the whole tree from scratch with an iterative insert, feeding it the original keys in preorder, which reproduces the original shape of a search tree, and then the new key. The assertions compare level-order arrays, check that the root object is unchanged for a non-empty tree, and check both examples.

**Complexity.** O(h) time and O(h) recursion stack.

```java run
import java.util.*;

public final class BstInsertRun {
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
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Node plainInsert(Node root, int key) {
        if (root == null) return new Node(key);
        Node at = root;
        while (true) {
            if (key == at.val) return root;
            if (key < at.val) { if (at.left == null) { at.left = new Node(key); return root; } at = at.left; }
            else { if (at.right == null) { at.right = new Node(key); return root; } at = at.right; }
        }
    }

    static Node randomBst(Random rnd, int maxNodes, int range) {
        Node root = null;
        int n = rnd.nextInt(maxNodes + 1);
        for (int i = 0; i < n; i++) root = plainInsert(root, rnd.nextInt(range));
        return root;
    }

    static void inorderInto(Node n, List<Integer> out) {
        if (n == null) return;
        inorderInto(n.left, out);
        out.add(n.val);
        inorderInto(n.right, out);
    }
    static Node insert(Node node, int key) {
        if (node == null) return new Node(key);
        if (key < node.val) node.left = insert(node.left, key);
        else if (key > node.val) node.right = insert(node.right, key);
        return node;
    }

    static void preorder(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        preorder(n.left, out);
        preorder(n.right, out);
    }

    public static void main(String[] args) {
        if (!Arrays.toString(levels(insert(build(new Integer[] {4, 2, 7, 1, 3}), 5))).equals("[4, 2, 7, 1, 3, 5]")) throw new AssertionError("example 1");
        if (!Arrays.toString(levels(insert(build(new Integer[] {3, null, 5}), 4))).equals("[3, null, 5, 4]")) throw new AssertionError("example 2");
        if (!Arrays.toString(levels(insert(null, 9))).equals("[9]")) throw new AssertionError("empty tree");
        Random rnd = new Random(16302);
        for (int t = 0; t < 6000; t++) {
            Node root = randomBst(rnd, 16, 60);
            List<Integer> keys = new ArrayList<>();
            preorder(root, keys);
            int key = rnd.nextInt(60);
            while (keys.contains(key)) key = rnd.nextInt(60);
            Node rebuilt = null;
            for (int k : keys) rebuilt = plainInsert(rebuilt, k);
            rebuilt = plainInsert(rebuilt, key);
            Node before = root;
            Node after = insert(root, key);
            if (before != null && after != before) throw new AssertionError("root object replaced");
            if (!Arrays.equals(levels(after), levels(rebuilt))) throw new AssertionError("differs for key " + key);
        }
    }
}
```

#### Solution: [Boundary] Duplicate-Key Policy (Author exercise)
<!-- id: tb-duplicate-key-policy -->

**Approach.** The comparison gets a third branch for equality. Under `reject` it leaves the tree alone, under `count` it increments a counter on the equal node, and under `right` it treats the key as larger and continues down the right side, which creates a new node. The node count, the height and the sorted listing are read off the finished tree. The oracle uses no node objects at all: it keeps arrays of left and right indices and records each new item's depth at the moment it is attached, and it cross-checks the sorted list against a `TreeMap` of counts. The assertions run random key lists under all three policies and check both examples as text.

**Complexity.** O(n * h) time for n insertions into a tree of height h, and O(n) space.

```java run
import java.util.*;

public final class DuplicatePolicyRun {
    static final class N {
        int key, count = 1;
        N left, right;
        N(int key) { this.key = key; }
    }

    static String run(int[] keys, String policy) {
        N root = null;
        for (int key : keys) {
            if (root == null) { root = new N(key); continue; }
            N at = root;
            while (true) {
                if (key == at.key && policy.equals("reject")) break;
                if (key == at.key && policy.equals("count")) { at.count++; break; }
                if (key < at.key) {
                    if (at.left == null) { at.left = new N(key); break; }
                    at = at.left;
                } else {
                    if (at.right == null) { at.right = new N(key); break; }
                    at = at.right;
                }
            }
        }
        List<Integer> sorted = new ArrayList<>();
        int[] shape = new int[2];
        walk(root, 1, sorted, shape);
        return "[" + shape[0] + ", " + shape[1] + ", " + sorted + "]";
    }

    static void walk(N n, int depth, List<Integer> sorted, int[] shape) {
        if (n == null) return;
        walk(n.left, depth + 1, sorted, shape);
        for (int i = 0; i < n.count; i++) sorted.add(n.key);
        shape[0]++;
        shape[1] = Math.max(shape[1], depth);
        walk(n.right, depth + 1, sorted, shape);
    }

    static String oracle(int[] keys, String policy) {
        int cap = keys.length + 1;
        int[] key = new int[cap], left = new int[cap], right = new int[cap], depth = new int[cap], count = new int[cap];
        Arrays.fill(left, -1);
        Arrays.fill(right, -1);
        int used = 0, height = 0;
        for (int k : keys) {
            int at = used == 0 ? -1 : 0, parent = -1;
            boolean goLeft = false, merged = false;
            while (at != -1) {
                parent = at;
                if (k == key[at] && !policy.equals("right")) { if (policy.equals("count")) count[at]++; merged = true; break; }
                goLeft = k < key[at];
                at = goLeft ? left[at] : right[at];
            }
            if (merged) continue;
            key[used] = k;
            count[used] = 1;
            depth[used] = parent == -1 ? 1 : depth[parent] + 1;
            if (parent != -1) { if (goLeft) left[parent] = used; else right[parent] = used; }
            height = Math.max(height, depth[used]);
            used++;
        }
        TreeMap<Integer, Integer> tally = new TreeMap<>();
        for (int k : keys) tally.merge(k, 1, Integer::sum);
        List<Integer> sorted = new ArrayList<>();
        for (Map.Entry<Integer, Integer> e : tally.entrySet()) {
            int times = policy.equals("reject") ? 1 : e.getValue();
            for (int i = 0; i < times; i++) sorted.add(e.getKey());
        }
        return "[" + used + ", " + height + ", " + sorted + "]";
    }

    public static void main(String[] args) {
        if (!run(new int[] {5, 3, 5, 8}, "count").equals("[3, 2, [3, 5, 5, 8]]")) throw new AssertionError("example 1");
        if (!run(new int[] {2, 2, 2}, "right").equals("[3, 3, [2, 2, 2]]")) throw new AssertionError("example 2");
        if (!run(new int[] {2, 2, 2}, "reject").equals("[1, 1, [2]]")) throw new AssertionError("reject keeps one");
        if (!run(new int[] {2, 2, 2}, "count").equals("[1, 1, [2, 2, 2]]")) throw new AssertionError("count keeps one node");
        if (!run(new int[] {}, "right").equals("[0, 0, []]")) throw new AssertionError("empty input");
        Random rnd = new Random(16303);
        String[] policies = {"reject", "count", "right"};
        for (int t = 0; t < 6000; t++) {
            int[] keys = new int[rnd.nextInt(30)];
            int range = 1 + rnd.nextInt(21);
            for (int i = 0; i < keys.length; i++) keys[i] = rnd.nextInt(range);
            for (String p : policies) {
                if (!run(keys, p).equals(oracle(keys, p))) throw new AssertionError(p + " differs on " + Arrays.toString(keys));
            }
        }
    }
}
```

#### Solution: [Recognize] Delete Node in a BST (LeetCode 450)
<!-- id: tb-delete-node -->

**Approach.** Descend by comparison and return the new top of each branch. A node with at most one child is replaced by that child, and a node with two children takes the value of its successor, the leftmost node of its right side, which is then removed from that side. The oracle is iterative and tracks parent links explicitly, which is a different shape of code from the recursion. The assertions compare level-order arrays on random trees, check that the remaining keys are the original keys minus the target in sorted order, and check both examples and the missing key case.

**Complexity.** O(h) time, and O(h) recursion stack.

```java run
import java.util.*;

public final class DeleteNodeRun {
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
    static Integer[] levels(Node root) {
        List<Integer> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            if (p == null) { out.add(null); continue; }
            out.add(p.val);
            line.add(p.left);
            line.add(p.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }
    static Node plainInsert(Node root, int key) {
        if (root == null) return new Node(key);
        Node at = root;
        while (true) {
            if (key == at.val) return root;
            if (key < at.val) { if (at.left == null) { at.left = new Node(key); return root; } at = at.left; }
            else { if (at.right == null) { at.right = new Node(key); return root; } at = at.right; }
        }
    }

    static Node randomBst(Random rnd, int maxNodes, int range) {
        Node root = null;
        int n = rnd.nextInt(maxNodes + 1);
        for (int i = 0; i < n; i++) root = plainInsert(root, rnd.nextInt(range));
        return root;
    }

    static void inorderInto(Node n, List<Integer> out) {
        if (n == null) return;
        inorderInto(n.left, out);
        out.add(n.val);
        inorderInto(n.right, out);
    }
    static Node remove(Node node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = remove(node.left, key); return node; }
        if (key > node.val) { node.right = remove(node.right, key); return node; }
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        Node succ = node.right;
        while (succ.left != null) succ = succ.left;
        node.val = succ.val;
        node.right = remove(node.right, succ.val);
        return node;
    }

    static Node oracle(Node root, int key) {
        Node parent = null, at = root;
        while (at != null && at.val != key) { parent = at; at = key < at.val ? at.left : at.right; }
        if (at == null) return root;
        if (at.left != null && at.right != null) {
            Node sp = at, s = at.right;
            while (s.left != null) { sp = s; s = s.left; }
            at.val = s.val;
            if (sp == at) sp.right = s.right; else sp.left = s.right;
            return root;
        }
        Node child = at.left != null ? at.left : at.right;
        if (parent == null) return child;
        if (parent.left == at) parent.left = child; else parent.right = child;
        return root;
    }

    public static void main(String[] args) {
        if (!Arrays.toString(levels(remove(build(new Integer[] {5, 3, 6, 2, 4, null, 7}), 3))).equals("[5, 4, 6, 2, null, null, 7]")) throw new AssertionError("example 1");
        if (!Arrays.toString(levels(remove(build(new Integer[] {5, 3, 6, 2, 4, null, 7}), 5))).equals("[6, 3, 7, 2, 4]")) throw new AssertionError("example 2");
        if (!Arrays.toString(levels(remove(build(new Integer[] {5, 3, 6, 2, 4, null, 7}), 0))).equals("[5, 3, 6, 2, 4, null, 7]")) throw new AssertionError("missing key leaves the tree alone");
        if (remove(null, 4) != null) throw new AssertionError("empty tree");
        if (remove(new Node(4), 4) != null) throw new AssertionError("single node removed");
        Random rnd = new Random(16304);
        for (int t = 0; t < 8000; t++) {
            Node root = randomBst(rnd, 16, 30);
            Integer[] v = levels(root);
            int key = rnd.nextInt(32);
            List<Integer> keep = new ArrayList<>();
            inorderInto(build(v), keep);
            keep.remove(Integer.valueOf(key));
            Node got = remove(build(v), key);
            Node want = oracle(build(v), key);
            if (!Arrays.equals(levels(got), levels(want))) throw new AssertionError("differs on " + Arrays.toString(v) + " key " + key);
            List<Integer> after = new ArrayList<>();
            inorderInto(got, after);
            if (!after.equals(keep)) throw new AssertionError("keys changed beyond the target on " + Arrays.toString(v));
        }
    }
}
```
