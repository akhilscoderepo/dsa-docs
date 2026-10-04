<!-- solutions-for: 09-balanced-tree-concepts -->
### Balanced-Tree Concepts

#### Solution: [Build] Compare Search Heights (Author exercise)
<!-- id: tb-compare-search-heights -->

**Approach.** Simulate both insertion orders on arrays of left and right links, recording each key's depth at the moment it is attached, so no recursion is needed even for a chain of ten thousand keys. The height is the largest depth, and the lookup total is the sum of depths, since a lookup visits one board per level. The median-first order comes from a recursion that is only about fourteen levels deep. The oracle is closed-form: the chain has height n and total n(n+1)/2, and a tree whose levels are full except the last has height floor(log2 n) + 1 and a total found by counting the boards on each level. The assertions compare every n up to 300 and the largest case.

**Complexity.** The chain simulation is O(n^2) because each insertion walks to the bottom, and the balanced one is O(n log n).

```java run
import java.util.*;

public final class SearchHeightsRun {
    static long[] simulate(int[] order, int n) {
        int[] left = new int[n + 1], right = new int[n + 1], depth = new int[n + 1];
        int[] keyAt = new int[n];
        int used = 0;
        long height = 0, total = 0;
        for (int key : order) {
            int slot = used++;
            keyAt[slot] = key;
            if (slot == 0) depth[slot] = 1;
            else {
                int at = 0;
                while (true) {
                    boolean goLeft = key < keyAt[at];
                    int next = goLeft ? left[at] : right[at];
                    if (next == 0) {
                        if (goLeft) left[at] = slot; else right[at] = slot;
                        depth[slot] = depth[at] + 1;
                        break;
                    }
                    at = next;
                }
            }
            height = Math.max(height, depth[slot]);
            total += depth[slot];
        }
        return new long[] {height, total};
    }

    static void medianFirst(int lo, int hi, List<Integer> out) {
        if (lo > hi) return;
        int mid = (lo + hi) / 2;
        out.add(mid);
        medianFirst(lo, mid - 1, out);
        medianFirst(mid + 1, hi, out);
    }

    static String compare(int n) {
        int[] increasing = new int[n];
        for (int i = 0; i < n; i++) increasing[i] = i + 1;
        List<Integer> mf = new ArrayList<>();
        medianFirst(1, n, mf);
        int[] balanced = mf.stream().mapToInt(Integer::intValue).toArray();
        long[] a = simulate(increasing, n), b = simulate(balanced, n);
        return "[" + a[0] + ", " + b[0] + ", " + a[1] + ", " + b[1] + "]";
    }

    static String closedForm(int n) {
        int h = 0;
        while ((1L << h) - 1 < n) h++;
        long total = 0;
        for (int d = 1; d <= h; d++) {
            long before = (1L << (d - 1)) - 1;
            long onLevel = Math.min(1L << (d - 1), n - before);
            total += d * onLevel;
        }
        return "[" + n + ", " + h + ", " + ((long) n * (n + 1) / 2) + ", " + total + "]";
    }

    public static void main(String[] args) {
        if (!compare(7).equals("[7, 3, 28, 17]")) throw new AssertionError("example 1");
        if (!compare(1).equals("[1, 1, 1, 1]")) throw new AssertionError("example 2");
        if (!compare(3).equals("[3, 2, 6, 5]")) throw new AssertionError("three keys");
        for (int n = 1; n <= 300; n++) {
            if (!compare(n).equals(closedForm(n))) throw new AssertionError("differs at n=" + n + ": " + compare(n) + " vs " + closedForm(n));
        }
        if (!compare(10000).equals(closedForm(10000))) throw new AssertionError("largest case");
    }
}
```

#### Solution: [Vary] Identify One Rotation (Author exercise)
<!-- id: tb-identify-rotation -->

**Approach.** Hang the three keys in a plain tree and read its shape: a root with two children needs nothing, a line leaning left needs a right rotation, a line leaning right needs a left rotation, and a bend needs a double rotation. The oracle does not read shapes at all. For every one of the six orders it tries each candidate repair on a fresh copy of the tree, a rotation at the root, a rotation at the child followed by one at the root, or nothing, and keeps those that give a valid search tree of height 2. The assertions require exactly one label to survive for each order and that label must match the shape rule.

**Complexity.** O(1) for three keys.

```java run
import java.util.*;

public final class OneRotationRun {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node hang(int[] keys) {
        Node root = new Node(keys[0]);
        for (int i = 1; i < keys.length; i++) {
            Node at = root;
            while (true) {
                if (keys[i] < at.val) { if (at.left == null) { at.left = new Node(keys[i]); break; } at = at.left; }
                else { if (at.right == null) { at.right = new Node(keys[i]); break; } at = at.right; }
            }
        }
        return root;
    }

    static String byShape(int[] keys) {
        Node r = hang(keys);
        if (r.left != null && r.right != null) return "none";
        if (r.left != null) return r.left.left != null ? "rotate right" : "double rotation";
        return r.right.right != null ? "rotate left" : "double rotation";
    }

    static Node rotateRight(Node top) { Node p = top.left; top.left = p.right; p.right = top; return p; }

    static Node rotateLeft(Node top) { Node p = top.right; top.right = p.left; p.left = top; return p; }

    static int height(Node n) { return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right)); }

    static void inorder(Node n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    static boolean good(Node n) {
        List<Integer> keys = new ArrayList<>();
        inorder(n, keys);
        List<Integer> sorted = new ArrayList<>(keys);
        Collections.sort(sorted);
        return keys.equals(sorted) && height(n) == 2;
    }

    static Set<String> byTrying(int[] keys) {
        Set<String> works = new TreeSet<>();
        if (good(hang(keys))) works.add("none");
        Node a = hang(keys);
        if (a.left != null && good(rotateRight(a))) works.add("rotate right");
        Node b = hang(keys);
        if (b.right != null && good(rotateLeft(b))) works.add("rotate left");
        Node c = hang(keys);
        if (c.left != null && c.left.right != null) { c.left = rotateLeft(c.left); if (good(rotateRight(c))) works.add("double rotation"); }
        Node d = hang(keys);
        if (d.right != null && d.right.left != null) { d.right = rotateRight(d.right); if (good(rotateLeft(d))) works.add("double rotation"); }
        return works;
    }

    public static void main(String[] args) {
        if (!byShape(new int[] {3, 2, 1}).equals("rotate right")) throw new AssertionError("example 1");
        if (!byShape(new int[] {1, 3, 2}).equals("double rotation")) throw new AssertionError("example 2");
        int[][] orders = {{1, 2, 3}, {1, 3, 2}, {2, 1, 3}, {2, 3, 1}, {3, 1, 2}, {3, 2, 1}};
        int[] scale = {10, 500, 999};
        for (int base : scale) {
            for (int[] o : orders) {
                int[] keys = {o[0] + base - 1, o[1] + base - 1, o[2] + base - 1};
                Set<String> tried = byTrying(keys);
                if (tried.size() != 1 || !tried.contains(byShape(keys))) throw new AssertionError("labels disagree for " + Arrays.toString(keys) + ": " + tried);
            }
        }
    }
}
```

#### Solution: [Boundary] Preserve Inorder Through Rotation (Author exercise)
<!-- id: tb-rotation-preserves-order -->

**Approach.** Walk to the named node while remembering its parent, then rewrite three links: the child on the heavy side becomes the new top, the old top becomes its child on the other side, and the middle subtree moves across to the old top. The parent link is redirected last, or the root changes if there was no parent. The assertions do not trust a second copy of the same code. They check that the sorted listing is identical before and after, that the result is still a search tree, that the old top is now the child of the lifted node, and that the three subtrees involved have the same level-order contents as before, by comparing arrays taken from the tree before it was changed. A height-balanced tree that is not complete is also checked, for the false friend in the applicability section.

**Complexity.** O(h) to find the node, and O(1) for the rotation itself.

```java run
import java.util.*;

public final class RotationOrderRun {
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
    static Node rotateAt(Node root, int key, boolean right) {
        Node parent = null, at = root;
        while (at.val != key) { parent = at; at = key < at.val ? at.left : at.right; }
        Node pivot;
        if (right) { pivot = at.left; at.left = pivot.right; pivot.right = at; }
        else { pivot = at.right; at.right = pivot.left; pivot.left = at; }
        if (parent == null) return pivot;
        if (parent.left == at) parent.left = pivot; else parent.right = pivot;
        return root;
    }

    static Node locate(Node n, int key) {
        while (n != null && n.val != key) n = key < n.val ? n.left : n.right;
        return n;
    }

    static boolean isSearchTree(Node n, long lo, long hi) {
        if (n == null) return true;
        return n.val > lo && n.val < hi && isSearchTree(n.left, lo, n.val) && isSearchTree(n.right, n.val, hi);
    }

    static int balancedHeight(Node n) {
        if (n == null) return 0;
        int l = balancedHeight(n.left), r = balancedHeight(n.right);
        if (l < 0 || r < 0 || Math.abs(l - r) > 1) return -1;
        return 1 + Math.max(l, r);
    }

    static String text(Integer[] a) { return Arrays.toString(a); }

    public static void main(String[] args) {
        if (!text(levels(rotateAt(build(new Integer[] {5, 3, 8, 2, 4}), 5, true))).equals("[3, 2, 5, null, null, 4, 8]")) throw new AssertionError("example 1");
        if (!text(levels(rotateAt(build(new Integer[] {4, 2, 6, null, null, 5, 7}), 4, false))).equals("[6, 4, 7, 2, 5]")) throw new AssertionError("example 2");
        if (balancedHeight(build(new Integer[] {5, 3, 8, 2})) < 0) throw new AssertionError("a tree with a deeper left side can still be balanced");
        if (balancedHeight(build(new Integer[] {1, null, 2, null, 3})) >= 0) throw new AssertionError("a line of three is not balanced");
        Random rnd = new Random(16903);
        int tried = 0;
        for (int t = 0; t < 3000; t++) {
            Node original = randomBst(rnd, 16, 60);
            List<Integer> keys = new ArrayList<>();
            inorderInto(original, keys);
            for (int key : keys) {
                for (boolean right : new boolean[] {true, false}) {
                    Node fresh = build(levels(original));
                    Node target = locate(fresh, key);
                    Node pivotBefore = right ? target.left : target.right;
                    if (pivotBefore == null) continue;
                    Integer[] middle = levels(right ? pivotBefore.right : pivotBefore.left);
                    Integer[] outer = levels(right ? pivotBefore.left : pivotBefore.right);
                    Integer[] farSide = levels(right ? target.right : target.left);
                    int pivotKey = pivotBefore.val;
                    Node after = rotateAt(fresh, key, right);
                    List<Integer> keysAfter = new ArrayList<>();
                    inorderInto(after, keysAfter);
                    if (!keysAfter.equals(keys)) throw new AssertionError("inorder changed");
                    if (!isSearchTree(after, Long.MIN_VALUE, Long.MAX_VALUE)) throw new AssertionError("no longer a search tree");
                    Node lifted = locate(after, pivotKey);
                    Node oldTop = right ? lifted.right : lifted.left;
                    if (oldTop == null || oldTop.val != key) throw new AssertionError("old top should be a child of the lifted node");
                    if (!Arrays.equals(levels(right ? oldTop.left : oldTop.right), middle)) throw new AssertionError("middle subtree moved wrongly");
                    if (!Arrays.equals(levels(right ? lifted.left : lifted.right), outer)) throw new AssertionError("outer subtree changed");
                    if (!Arrays.equals(levels(right ? oldTop.right : oldTop.left), farSide)) throw new AssertionError("far side changed");
                    tried++;
                }
            }
        }
        if (tried < 5000) throw new AssertionError("too few rotations tried: " + tried);
    }
}
```

#### Solution: [Recognize] Explain Library Choice (Author exercise)
<!-- id: tb-library-choice -->

**Approach.** The decision is a small table: no need for order gives `HashMap`, order without later changes gives a sorted array, and order with changes gives `TreeMap`. The oracle is a capability model that picks the cheapest structure meeting both requirements, and the assertions compare the table with it for all four combinations. The rest of the file backs the reasons with running code. A plain search tree fed 3000 sorted keys has height 3000, while the rebalancing insertion of the lesson stays within the proven bound of 1.4405 times log2(n + 2). A `TreeMap` fed a hundred thousand sorted keys still answers first, last and next-key queries correctly, and `HashMap` has no next-key method at all.

**Complexity.** The decision is O(1). The plain chain build in the checks is O(n^2) for n = 3000, and the rebalancing build is O(n log n).

```java run
import java.util.*;

public final class LibraryChoiceRun {
    static String choose(boolean needsOrder, boolean dataChanges) {
        if (!needsOrder) return "HashMap";
        return dataChanges ? "TreeMap" : "sorted array";
    }

    static String byCapabilities(boolean needsOrder, boolean dataChanges) {
        String[] names = {"HashMap", "sorted array", "TreeMap"};
        boolean[] ordered = {false, true, true};
        boolean[] updatable = {true, false, true};
        for (int i = 0; i < names.length; i++) {
            if ((!needsOrder || ordered[i]) && (!dataChanges || updatable[i])) return names[i];
        }
        throw new AssertionError("no structure fits");
    }

    static final class Plain {
        int val;
        Plain left, right;
        Plain(int val) { this.val = val; }
    }

    static int plainHeightForSorted(int n) {
        Plain root = new Plain(1);
        Plain deepest = root;
        int height = 1;
        for (int k = 2; k <= n; k++) {
            Plain at = root;
            int depth = 1;
            while (at.right != null) { at = at.right; depth++; }
            at.right = new Plain(k);
            height = depth + 1;
        }
        return height;
    }

    static final class Avl {
        int val, height = 1;
        Avl left, right;
        Avl(int val) { this.val = val; }
    }

    static int h(Avl n) { return n == null ? 0 : n.height; }
    static void refresh(Avl n) { n.height = 1 + Math.max(h(n.left), h(n.right)); }

    static Avl rotateRight(Avl top) {
        Avl p = top.left;
        top.left = p.right;
        p.right = top;
        refresh(top);
        refresh(p);
        return p;
    }

    static Avl rotateLeft(Avl top) {
        Avl p = top.right;
        top.right = p.left;
        p.left = top;
        refresh(top);
        refresh(p);
        return p;
    }

    static Avl insert(Avl node, int key) {
        if (node == null) return new Avl(key);
        if (key < node.val) node.left = insert(node.left, key);
        else if (key > node.val) node.right = insert(node.right, key);
        else return node;
        refresh(node);
        int b = h(node.left) - h(node.right);
        if (b > 1) {
            if (h(node.left.left) < h(node.left.right)) node.left = rotateLeft(node.left);
            return rotateRight(node);
        }
        if (b < -1) {
            if (h(node.right.right) < h(node.right.left)) node.right = rotateRight(node.right);
            return rotateLeft(node);
        }
        return node;
    }

    public static void main(String[] args) throws Exception {
        if (!choose(true, true).equals("TreeMap")) throw new AssertionError("example 1");
        if (!choose(false, true).equals("HashMap")) throw new AssertionError("example 2");
        for (boolean order : new boolean[] {false, true}) {
            for (boolean change : new boolean[] {false, true}) {
                if (!choose(order, change).equals(byCapabilities(order, change))) throw new AssertionError("table differs at " + order + "," + change);
            }
        }
        if (plainHeightForSorted(3000) != 3000) throw new AssertionError("sorted input should make a chain");
        for (int n : new int[] {1, 2, 3, 10, 100, 1000, 3000}) {
            Avl root = null;
            for (int k = 1; k <= n; k++) root = insert(root, k);
            double bound = 1.4405 * Math.log(n + 2) / Math.log(2);
            if (root.height > bound) throw new AssertionError("height " + root.height + " exceeds " + bound + " for n=" + n);
        }
        TreeMap<Integer, Integer> map = new TreeMap<>();
        for (int k = 1; k <= 100000; k++) map.put(k, k);
        if (map.firstKey() != 1 || map.lastKey() != 100000 || map.higherKey(500) != 501 || map.higherKey(100000) != null) throw new AssertionError("ordered queries");
        boolean missing = false;
        try { HashMap.class.getMethod("higherKey", Object.class); } catch (NoSuchMethodException expected) { missing = true; }
        if (!missing) throw new AssertionError("HashMap should have no next-key method");
    }
}
```
