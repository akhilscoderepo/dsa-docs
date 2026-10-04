<!-- solutions-for: 11-bst-and-bounds -->
### BST And Bounds

#### Solution: [Build] Search With Its Stopping Interval (LeetCode 700)
<!-- id: tc-search-stopping-interval -->

**Approach.** Walk down by comparison and replace one end of the interval at each step: the upper end when going left, the lower end when going right. Report whether the walk stopped on the key, together with the two ends. For a missing key the ends must be its neighbours in sorted order, and for a present key they are the nearest ancestors on each side. The oracle for a present key collects the keys on the route from the root and takes the largest smaller one and the smallest larger one. For a missing key the assertions also compare the ends directly with the sorted listing, the largest key below and the smallest key above, which is an independent statement of the neighbour claim.

**Complexity.** O(h) time and O(1) space.

```java run
import java.util.*;

public final class StoppingIntervalRun {
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
    static String search(Node root, int key) {
        Integer lo = null, hi = null;
        Node node = root;
        while (node != null && node.val != key) {
            if (key < node.val) { hi = node.val; node = node.left; }
            else { lo = node.val; node = node.right; }
        }
        return "[" + (node != null) + ", " + lo + ", " + hi + "]";
    }

    static void route(Node n, int key, List<Integer> above) {
        if (n == null || n.val == key) return;
        above.add(n.val);
        route(key < n.val ? n.left : n.right, key, above);
    }

    static String viaRoute(Node root, int key, boolean present) {
        List<Integer> above = new ArrayList<>();
        route(root, key, above);
        Integer lo = null, hi = null;
        for (int a : above) {
            if (a < key && (lo == null || a > lo)) lo = a;
            if (a > key && (hi == null || a < hi)) hi = a;
        }
        return "[" + present + ", " + lo + ", " + hi + "]";
    }

    public static void main(String[] args) {
        Integer[] sample = {8, 3, 10, 1, 6, null, 14};
        if (!search(build(sample), 7).equals("[false, 6, 8]")) throw new AssertionError("example 1");
        if (!search(build(sample), 0).equals("[false, null, 1]")) throw new AssertionError("example 2");
        if (!search(build(sample), 6).equals("[true, 3, 8]")) throw new AssertionError("present key");
        if (!search(null, 5).equals("[false, null, null]")) throw new AssertionError("empty tree");
        Random rnd = new Random(161101);
        for (int t = 0; t < 8000; t++) {
            Node root = randomBst(rnd, 18, 50);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            int key = rnd.nextInt(56) - 3;
            boolean present = sorted.contains(key);
            if (!search(root, key).equals(viaRoute(root, key, present))) throw new AssertionError("route oracle differs for " + key + " in " + sorted);
            if (!present) {
                Integer below = null, above = null;
                for (int x : sorted) { if (x < key) below = x; else if (above == null) above = x; }
                if (!search(root, key).equals("[false, " + below + ", " + above + "]")) throw new AssertionError("ends are not the neighbours of " + key + " in " + sorted);
            }
        }
    }
}
```

#### Solution: [Vary] First Violation Of The Numbering (LeetCode 98)
<!-- id: tc-first-violation -->

**Approach.** Carry exclusive `long` ends down the walk and return the array position of the first node, in preorder, that does not fit. The left branch is searched before the right, so the first failure found is the first in preorder. Nodes remember the position they had in the input array. The oracle does not carry an interval. It keeps the list of ancestors with the side taken at each, and checks every node in preorder against every ancestor, so the first node that breaks any ancestor's rule is returned. The test trees are built by taking a random shape, relabelling it in inorder order so that it obeys the numbering, and then overwriting one key in many of them, so that both valid and invalid trees are common.

**Complexity.** O(n) time and O(h) recursion.

```java run
import java.util.*;

public final class FirstViolationRun {
    static final class Node {
        final int idx;
        int val;
        Node left, right;
        Node(int idx, int val) { this.idx = idx; this.val = val; }
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
    static Node build(Integer[] v) {
        if (v.length == 0 || v[0] == null) return null;
        Node root = new Node(0, v[0]);
        ArrayDeque<Node> waiting = new ArrayDeque<>();
        waiting.add(root);
        int at = 1;
        while (!waiting.isEmpty() && at < v.length) {
            Node p = waiting.poll();
            if (v[at] != null) { p.left = new Node(at, v[at]); waiting.add(p.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { p.right = new Node(at, v[at]); waiting.add(p.right); }
                at++;
            }
        }
        return root;
    }

    static int firstViolation(Node node, long lo, long hi) {
        if (node == null) return -1;
        if (node.val <= lo || node.val >= hi) return node.idx;
        int inLeft = firstViolation(node.left, lo, node.val);
        return inLeft != -1 ? inLeft : firstViolation(node.right, node.val, hi);
    }

    static int oracle(Node node, List<Node> path, List<Boolean> wentLeft) {
        if (node == null) return -1;
        for (int i = 0; i < path.size(); i++) {
            boolean ok = wentLeft.get(i) ? node.val < path.get(i).val : node.val > path.get(i).val;
            if (!ok) return node.idx;
        }
        path.add(node);
        wentLeft.add(true);
        int found = oracle(node.left, path, wentLeft);
        wentLeft.set(wentLeft.size() - 1, false);
        if (found == -1) found = oracle(node.right, path, wentLeft);
        path.remove(path.size() - 1);
        wentLeft.remove(wentLeft.size() - 1);
        return found;
    }

    static int counter;

    static void relabel(Node n) {
        if (n == null) return;
        relabel(n.left);
        n.val = 10 * counter++;
        relabel(n.right);
    }

    static Integer[] valuesOf(Node root, Integer[] shape) {
        Integer[] out = shape.clone();
        fillByIndex(root, out);
        return out;
    }

    static void fillByIndex(Node n, Integer[] out) {
        if (n == null) return;
        out[n.idx] = n.val;
        fillByIndex(n.left, out);
        fillByIndex(n.right, out);
    }

    static int check(Integer[] v) {
        Node root = build(v);
        int fast = firstViolation(root, Long.MIN_VALUE, Long.MAX_VALUE);
        int slow = oracle(build(v), new ArrayList<>(), new ArrayList<>());
        if (fast != slow) throw new AssertionError("differs on " + Arrays.toString(v) + ": " + fast + " vs " + slow);
        return fast;
    }

    public static void main(String[] args) {
        if (check(new Integer[] {5, 4, 6, null, null, 3, 7}) != 5) throw new AssertionError("example 1");
        if (check(new Integer[] {2, 1, 3}) != -1) throw new AssertionError("example 2");
        if (check(new Integer[] {}) != -1) throw new AssertionError("empty tree");
        if (check(new Integer[] {Integer.MIN_VALUE, null, Integer.MAX_VALUE}) != -1) throw new AssertionError("extremes fit");
        if (check(new Integer[] {Integer.MIN_VALUE, Integer.MIN_VALUE}) != 1) throw new AssertionError("equal child violates");
        Random rnd = new Random(161102);
        int valid = 0, broken = 0;
        for (int t = 0; t < 6000; t++) {
            Integer[] shape = randomLevels(rnd, 18, 0, 0);
            Node root = build(shape);
            counter = 0;
            relabel(root);
            Integer[] v = valuesOf(root, shape);
            if (rnd.nextInt(3) != 0) {
                int at = rnd.nextInt(v.length);
                if (v[at] != null) v[at] = rnd.nextInt(10 * v.length);
            }
            if (check(v) == -1) valid++; else broken++;
        }
        if (valid < 500 || broken < 500) throw new AssertionError("test mix too lopsided: " + valid + "/" + broken);
    }
}
```

#### Solution: [Boundary] Kth Smallest Inside A Band (LeetCode 230)
<!-- id: tc-kth-in-band -->

**Approach.** Run the sorted visit with an explicit stack, but never push a key below the band: such a key and its whole left side are skipped by stepping to its right child. When a popped key is above the band the walk ends with `null`, since everything still waiting is larger, and otherwise the countdown decreases and the pop that makes it zero is the answer. The oracle filters a complete sorted listing to the band and reads index k minus one, or returns `null` when the filtered list is too short. The assertions try ranks from 1 up to two beyond the band population, with random bands, and also check a band that holds nothing.

**Complexity.** O(h + k) time for the walk and O(h) stack space.

```java run
import java.util.*;

public final class KthInBandRun {
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
    static Integer kthInBand(Node root, int low, int high, int k) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                if (node.val < low) node = node.right;
                else { stack.push(node); node = node.left; }
            }
            if (stack.isEmpty()) break;
            node = stack.pop();
            if (node.val > high) return null;
            if (--k == 0) return node.val;
            node = node.right;
        }
        return null;
    }

    public static void main(String[] args) {
        Integer[] full = {8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15};
        if (kthInBand(build(full), 5, 12, 3) != 7) throw new AssertionError("example 1");
        if (kthInBand(build(full), 5, 7, 4) != null) throw new AssertionError("example 2");
        if (kthInBand(null, 0, 10, 1) != null) throw new AssertionError("empty tree");
        if (kthInBand(build(full), 100, 200, 1) != null) throw new AssertionError("band above every key");
        Random rnd = new Random(161103);
        for (int t = 0; t < 6000; t++) {
            Node root = randomBst(rnd, 22, 80);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            int a = rnd.nextInt(85), b = rnd.nextInt(85);
            int low = Math.min(a, b), high = Math.max(a, b);
            List<Integer> band = new ArrayList<>();
            for (int x : sorted) if (x >= low && x <= high) band.add(x);
            for (int k = 1; k <= band.size() + 2; k++) {
                Integer want = k <= band.size() ? band.get(k - 1) : null;
                Integer got = kthInBand(root, low, high, k);
                if (!Objects.equals(got, want)) throw new AssertionError("k=" + k + " band " + low + ".." + high + " on " + sorted);
            }
        }
    }
}
```

#### Solution: [Recognize] Delete By Predecessor (LeetCode 450)
<!-- id: tc-delete-by-predecessor -->

**Approach.** Descend by comparison, returning the new top of each branch. A node with at most one child is replaced by that child. A node with two children takes the key of the largest node on its left side, found by following right links, and that node is then removed from the left side, where it has no right child. The oracle is iterative and keeps parent links explicitly. The assertions compare level-order arrays on random trees, check that the remaining keys equal the original keys minus the target in sorted order, check that the result is still a valid search tree, and confirm that the predecessor version gives a different shape from the successor version on at least some two-child deletions.

**Complexity.** O(h) time and O(h) recursion stack.

```java run
import java.util.*;

public final class DeletePredecessorRun {
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
    static Node removeByPredecessor(Node node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = removeByPredecessor(node.left, key); return node; }
        if (key > node.val) { node.right = removeByPredecessor(node.right, key); return node; }
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        Node pred = node.left;
        while (pred.right != null) pred = pred.right;
        node.val = pred.val;
        node.left = removeByPredecessor(node.left, pred.val);
        return node;
    }

    static Node removeBySuccessor(Node node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = removeBySuccessor(node.left, key); return node; }
        if (key > node.val) { node.right = removeBySuccessor(node.right, key); return node; }
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        Node succ = node.right;
        while (succ.left != null) succ = succ.left;
        node.val = succ.val;
        node.right = removeBySuccessor(node.right, succ.val);
        return node;
    }

    static Node oracle(Node root, int key) {
        Node parent = null, at = root;
        while (at != null && at.val != key) { parent = at; at = key < at.val ? at.left : at.right; }
        if (at == null) return root;
        if (at.left != null && at.right != null) {
            Node pp = at, p = at.left;
            while (p.right != null) { pp = p; p = p.right; }
            at.val = p.val;
            if (pp == at) pp.left = p.left; else pp.right = p.left;
            return root;
        }
        Node child = at.left != null ? at.left : at.right;
        if (parent == null) return child;
        if (parent.left == at) parent.left = child; else parent.right = child;
        return root;
    }

    public static void main(String[] args) {
        Integer[] sample = {5, 3, 6, 2, 4, null, 7};
        if (!Arrays.toString(levels(removeByPredecessor(build(sample), 3))).equals("[5, 2, 6, null, 4, null, 7]")) throw new AssertionError("example 1");
        if (!Arrays.toString(levels(removeByPredecessor(build(sample), 5))).equals("[4, 3, 6, 2, null, null, 7]")) throw new AssertionError("example 2");
        if (!Arrays.toString(levels(removeByPredecessor(build(sample), 9))).equals(Arrays.toString(sample))) throw new AssertionError("missing key");
        if (removeByPredecessor(null, 1) != null) throw new AssertionError("empty tree");
        Random rnd = new Random(161104);
        int differentShapes = 0;
        for (int t = 0; t < 8000; t++) {
            Node root = randomBst(rnd, 16, 30);
            Integer[] v = levels(root);
            int key = rnd.nextInt(32);
            List<Integer> keep = new ArrayList<>();
            inorderInto(build(v), keep);
            keep.remove(Integer.valueOf(key));
            Node got = removeByPredecessor(build(v), key);
            if (!Arrays.equals(levels(got), levels(oracle(build(v), key)))) throw new AssertionError("differs on " + Arrays.toString(v) + " key " + key);
            List<Integer> after = new ArrayList<>();
            inorderInto(got, after);
            if (!after.equals(keep)) throw new AssertionError("keys changed beyond the target");
            for (int i = 1; i < after.size(); i++) if (after.get(i) <= after.get(i - 1)) throw new AssertionError("numbering broken");
            if (!Arrays.equals(levels(got), levels(removeBySuccessor(build(v), key)))) differentShapes++;
        }
        if (differentShapes < 100) throw new AssertionError("the two policies should often differ: " + differentShapes);
    }
}
```
