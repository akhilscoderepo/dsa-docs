<!-- solutions-for: 02-bst-invariant-and-bounds -->
### BST Invariant And Bounds

#### Solution: [Build] Validate One Root And Children (Author exercise)
<!-- id: tb-root-and-child-intervals -->

**Approach.** The left child inherits the lower end unchanged and takes `r` as its upper end, and the right child takes `r` as its lower end and keeps the upper end. Whether `r` fits is a strict comparison against whichever ends are not null. The oracle never builds intervals: for every candidate child value from -30 to 30 on a shelf that fits, it applies all three ancestor demands directly, and the assertions require that a value lies inside the returned left or right interval exactly when the direct demands say it may sit there. Both examples are checked as exact text.

**Complexity.** O(1) time and space for one shelf.

```java run
import java.util.*;

public final class ChildIntervalsRun {
    static Integer[][] childIntervals(int r, Integer lo, Integer hi) {
        return new Integer[][] {{lo, r}, {r, hi}};
    }

    static boolean fits(int r, Integer lo, Integer hi) {
        return (lo == null || r > lo) && (hi == null || r < hi);
    }

    static String describe(int r, Integer lo, Integer hi) {
        Integer[][] c = childIntervals(r, lo, hi);
        return "[" + Arrays.toString(c[0]) + ", " + Arrays.toString(c[1]) + ", " + fits(r, lo, hi) + "]";
    }

    static boolean inside(int y, Integer[] iv) {
        return (iv[0] == null || y > iv[0]) && (iv[1] == null || y < iv[1]);
    }

    public static void main(String[] args) {
        if (!describe(7, null, 10).equals("[[null, 7], [7, 10], true]")) throw new AssertionError("example 1");
        if (!describe(10, 5, 10).equals("[[5, 10], [10, 10], false]")) throw new AssertionError("example 2");
        Random rnd = new Random(16201);
        for (int t = 0; t < 20000; t++) {
            int r = rnd.nextInt(41) - 20;
            Integer lo = rnd.nextInt(4) == 0 ? null : rnd.nextInt(41) - 20;
            Integer hi = rnd.nextInt(4) == 0 ? null : rnd.nextInt(41) - 20;
            Integer[][] c = childIntervals(r, lo, hi);
            for (int y = -30; y <= 30 && fits(r, lo, hi); y++) {
                boolean base = (lo == null || y > lo) && (hi == null || y < hi);
                if (inside(y, c[0]) != (base && y < r)) throw new AssertionError("left interval wrong for " + y + " r=" + r + " lo=" + lo + " hi=" + hi);
                if (inside(y, c[1]) != (base && y > r)) throw new AssertionError("right interval wrong for " + y + " r=" + r + " lo=" + lo + " hi=" + hi);
            }
            if (fits(r, lo, hi) != ((lo == null || lo < r) && (hi == null || r < hi))) throw new AssertionError("fits");
        }
    }
}
```

#### Solution: [Vary] Propagate Ancestor Bounds (Author exercise)
<!-- id: tb-propagate-bounds -->

**Approach.** Walk level by level with a queue whose entries carry a node together with its inherited interval, and give each child the parent's interval with one end replaced. The oracle ignores inheritance. It keeps the list of ancestors on the route to every node and takes the largest ancestor smaller than the node as the lower end and the smallest ancestor larger than the node as the upper end. The assertions compare both on random search trees and check the two examples as text.

**Complexity.** O(n) time and O(w) queue space.

```java run
import java.util.*;

public final class PropagateBoundsRun {
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
    record Item(Node node, Integer lo, Integer hi) {}

    static List<String> inherited(Node root) {
        List<String> out = new ArrayList<>();
        if (root == null) return out;
        ArrayDeque<Item> queue = new ArrayDeque<>();
        queue.add(new Item(root, null, null));
        while (!queue.isEmpty()) {
            Item it = queue.poll();
            out.add("[" + it.lo() + ", " + it.hi() + "]");
            if (it.node().left != null) queue.add(new Item(it.node().left, it.lo(), it.node().val));
            if (it.node().right != null) queue.add(new Item(it.node().right, it.node().val, it.hi()));
        }
        return out;
    }

    static void viaAncestors(Node n, List<Node> route, IdentityHashMap<Node, String> out) {
        if (n == null) return;
        Integer lo = null, hi = null;
        for (Node a : route) {
            if (a.val < n.val && (lo == null || a.val > lo)) lo = a.val;
            if (a.val > n.val && (hi == null || a.val < hi)) hi = a.val;
        }
        out.put(n, "[" + lo + ", " + hi + "]");
        route.add(n);
        viaAncestors(n.left, route, out);
        viaAncestors(n.right, route, out);
        route.remove(route.size() - 1);
    }

    static List<String> oracle(Node root) {
        IdentityHashMap<Node, String> by = new IdentityHashMap<>();
        viaAncestors(root, new ArrayList<>(), by);
        List<String> out = new ArrayList<>();
        List<Node> line = new ArrayList<>();
        if (root != null) line.add(root);
        for (int i = 0; i < line.size(); i++) {
            Node p = line.get(i);
            out.add(by.get(p));
            if (p.left != null) line.add(p.left);
            if (p.right != null) line.add(p.right);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!inherited(build(new Integer[] {5, 3, 8, null, 4})).toString().equals("[[null, null], [null, 5], [5, null], [3, 5]]")) throw new AssertionError("example 1");
        if (!inherited(build(new Integer[] {4, 2, 6, 1, 3, 5, 7})).toString().equals("[[null, null], [null, 4], [4, null], [null, 2], [2, 4], [4, 6], [6, null]]")) throw new AssertionError("example 2");
        Random rnd = new Random(16202);
        for (int t = 0; t < 4000; t++) {
            Node root = randomBst(rnd, 16, 60);
            Node again = build(levels(root));
            if (!inherited(again).equals(oracle(again))) throw new AssertionError("differs on " + Arrays.toString(root == null ? new Integer[0] : levels(root)));
        }
    }
}
```

#### Solution: [Boundary] Integer Extremes And Duplicates (Author exercise)
<!-- id: tb-extremes-and-equality -->

**Approach.** Keep both bounds as exclusive `long` limits. Going left the upper limit becomes the node value, or the node value plus one when equal keys may go left, which says "at most the node value" without overflow because `long` has room above `Integer.MAX_VALUE`. Going right the lower limit becomes the node value. The oracle is quadratic and rule-based: for every node it collects the values of its left and right subtrees and tests each one against the policy. The trees come from inserting values chosen from the extremes under the policy, sometimes with one value overwritten, so valid and invalid cases both occur and the assertions count that both were seen.

**Complexity.** O(n) time and O(h) recursion for the walk, against O(n * h) for the oracle.

```java run
import java.util.*;

public final class ExtremesRun {
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
    static final int[] TABLE = {Integer.MIN_VALUE, Integer.MIN_VALUE + 1, -1, 0, 1, Integer.MAX_VALUE - 1, Integer.MAX_VALUE};

    static boolean valid(Integer[] values, boolean equalGoesLeft) {
        return walk(build(values), Long.MIN_VALUE, Long.MAX_VALUE, equalGoesLeft);
    }

    static boolean walk(Node n, long lo, long hi, boolean equalLeft) {
        if (n == null) return true;
        if (n.val <= lo || n.val >= hi) return false;
        long leftHi = equalLeft ? (long) n.val + 1 : n.val;
        return walk(n.left, lo, leftHi, equalLeft) && walk(n.right, n.val, hi, equalLeft);
    }

    static void collect(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        collect(n.left, out);
        collect(n.right, out);
    }

    static boolean oracle(Node n, boolean equalLeft) {
        if (n == null) return true;
        List<Integer> l = new ArrayList<>(), r = new ArrayList<>();
        collect(n.left, l);
        collect(n.right, r);
        for (int x : l) if (equalLeft ? x > n.val : x >= n.val) return false;
        for (int x : r) if (x <= n.val) return false;
        return oracle(n.left, equalLeft) && oracle(n.right, equalLeft);
    }

    static Node insert(Node root, int key, boolean equalLeft) {
        if (root == null) return new Node(key);
        Node at = root;
        while (true) {
            boolean goLeft = equalLeft ? key <= at.val : key < at.val;
            if (goLeft) { if (at.left == null) { at.left = new Node(key); return root; } at = at.left; }
            else { if (at.right == null) { at.right = new Node(key); return root; } at = at.right; }
        }
    }

    public static void main(String[] args) {
        if (!valid(new Integer[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, true)) throw new AssertionError("example 1");
        if (valid(new Integer[] {Integer.MIN_VALUE, null, Integer.MIN_VALUE}, true)) throw new AssertionError("example 2");
        if (!valid(new Integer[] {}, false)) throw new AssertionError("empty tree is valid");
        if (valid(new Integer[] {Integer.MAX_VALUE, Integer.MAX_VALUE}, false)) throw new AssertionError("equal keys rejected without the flag");
        if (!valid(new Integer[] {Integer.MIN_VALUE, null, Integer.MAX_VALUE}, false)) throw new AssertionError("both extremes can sit together");
        Random rnd = new Random(16203);
        int good = 0, bad = 0;
        for (int t = 0; t < 8000; t++) {
            boolean flag = rnd.nextBoolean();
            Node root = null;
            int n = 1 + rnd.nextInt(10);
            for (int i = 0; i < n; i++) root = insert(root, TABLE[rnd.nextInt(TABLE.length)], flag);
            Integer[] v = levels(root);
            if (rnd.nextInt(3) == 0) {
                int at = rnd.nextInt(v.length);
                if (v[at] != null) v[at] = TABLE[rnd.nextInt(TABLE.length)];
            }
            boolean want = oracle(build(v), flag);
            if (valid(v, flag) != want) throw new AssertionError("differs on " + Arrays.toString(v) + " flag " + flag);
            if (want) good++; else bad++;
        }
        if (good < 200 || bad < 200) throw new AssertionError("test mix too lopsided: " + good + "/" + bad);
    }
}
```

#### Solution: [Recognize] Validate Binary Search Tree (LeetCode 98)
<!-- id: tb-validate-bst -->

**Approach.** Pass an exclusive `long` interval down, test each node once, and narrow the interval by the node value on the way to each child. A parent-only check is included in the file so that the assertions can show it accepting a tree with a deep violation. The oracle is a different idea entirely: an iterative inorder walk, which must yield a strictly increasing sequence for a valid tree. The assertions compare the two on random trees, on trees built by real insertion and then perturbed, and on the extreme values.

**Complexity.** O(n) time and O(h) stack space.

```java run
import java.util.*;

public final class ValidateBstRun {
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
    static boolean isValid(Node root) {
        return within(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    static boolean within(Node n, long lo, long hi) {
        if (n == null) return true;
        if (n.val <= lo || n.val >= hi) return false;
        return within(n.left, lo, n.val) && within(n.right, n.val, hi);
    }

    static boolean parentOnly(Node n) {
        if (n == null) return true;
        if (n.left != null && n.left.val >= n.val) return false;
        if (n.right != null && n.right.val <= n.val) return false;
        return parentOnly(n.left) && parentOnly(n.right);
    }

    static boolean viaInorder(Node root) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        long prev = Long.MIN_VALUE;
        Node at = root;
        while (at != null || !stack.isEmpty()) {
            while (at != null) { stack.push(at); at = at.left; }
            at = stack.pop();
            if (at.val <= prev) return false;
            prev = at.val;
            at = at.right;
        }
        return true;
    }

    public static void main(String[] args) {
        if (isValid(build(new Integer[] {5, 1, 4, null, null, 3, 6}))) throw new AssertionError("example 1");
        if (isValid(build(new Integer[] {10, 5, 15, null, null, 6, 20}))) throw new AssertionError("example 2");
        if (!parentOnly(build(new Integer[] {10, 5, 15, null, null, 6, 20}))) throw new AssertionError("the parent-only check should accept the deep violation");
        if (!isValid(build(new Integer[] {Integer.MAX_VALUE}))) throw new AssertionError("max alone");
        if (!isValid(build(new Integer[] {Integer.MIN_VALUE, null, Integer.MAX_VALUE}))) throw new AssertionError("both extremes");
        if (isValid(build(new Integer[] {Integer.MIN_VALUE, Integer.MIN_VALUE}))) throw new AssertionError("equal child");
        if (!isValid(null)) throw new AssertionError("empty tree");
        Random rnd = new Random(16204);
        int good = 0;
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd, 12, 0, 14);
            Node root = build(v);
            if (isValid(root) != viaInorder(root)) throw new AssertionError("random differs on " + Arrays.toString(v));
            Node real = randomBst(rnd, 14, 50);
            Integer[] w = real == null ? new Integer[0] : levels(real);
            if (w.length > 0 && rnd.nextInt(2) == 0) {
                int at = rnd.nextInt(w.length);
                if (w[at] != null) w[at] = rnd.nextInt(50);
            }
            Node tree = build(w);
            boolean got = isValid(tree);
            if (got != viaInorder(tree)) throw new AssertionError("perturbed differs on " + Arrays.toString(w));
            if (got) good++;
        }
        if (good < 300) throw new AssertionError("too few valid trees were tested: " + good);
    }
}
```
