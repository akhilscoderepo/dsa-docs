<!-- solutions-for: 05-kth-and-range-queries -->
### Kth And Range Queries

#### Solution: [Build] First K Inorder Values (Author exercise)
<!-- id: tb-first-k-inorder -->

**Approach.** Drive the sorted visit with an explicit stack: push a crate and move left until nothing remains, pop, record the key, and then move right. The loop ends the instant k keys have been recorded. A pop counter is kept so that the assertions can show the walk made exactly k pops. The oracle is the complete recursive inorder list cut to its first k entries, which does all the work the early stop avoids. Every k from 1 to n is tried on every random tree.

**Complexity.** O(h + k) time and O(h) stack space.

```java run
import java.util.*;

public final class FirstKRun {
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
    static int pops;

    static List<Integer> firstK(Node root, int k) {
        List<Integer> out = new ArrayList<>();
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (out.size() < k && (node != null || !stack.isEmpty())) {
            while (node != null) { stack.push(node); node = node.left; }
            node = stack.pop();
            pops++;
            out.add(node.val);
            node = node.right;
        }
        return out;
    }

    public static void main(String[] args) {
        if (!firstK(build(new Integer[] {5, 3, 6, 2, 4, null, null, 1}), 3).toString().equals("[1, 2, 3]")) throw new AssertionError("example 1");
        if (!firstK(build(new Integer[] {3, null, 4, null, 5}), 2).toString().equals("[3, 4]")) throw new AssertionError("example 2");
        Random rnd = new Random(16501);
        for (int t = 0; t < 4000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Integer> all = new ArrayList<>();
            inorderInto(root, all);
            for (int k = 1; k <= all.size(); k++) {
                pops = 0;
                List<Integer> got = firstK(root, k);
                if (!got.equals(all.subList(0, k))) throw new AssertionError("wrong prefix for k=" + k + " on " + all);
                if (pops != k) throw new AssertionError("the walk should stop after exactly k pops");
            }
        }
    }
}
```

#### Solution: [Vary] Kth Smallest Element in a BST (LeetCode 230)
<!-- id: tb-kth-smallest -->

**Approach.** The same stack walk keeps only a countdown. Each pop decreases it, and the pop that brings it to zero returns its key from inside the loop, so no list is built. The countdown is a local variable so that a second query starts fresh, which the assertions confirm by asking several ranks one after another on the same tree. The oracle sorts the keys collected by a plain traversal and reads index k minus one.

**Complexity.** O(h + k) time and O(h) stack space.

```java run
import java.util.*;

public final class KthSmallestRun {
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
    static int kthSmallest(Node root, int k) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = node.left; }
            node = stack.pop();
            if (--k == 0) return node.val;
            node = node.right;
        }
        throw new IllegalArgumentException("k is larger than the tree");
    }

    static void spill(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        spill(n.left, out);
        spill(n.right, out);
    }

    public static void main(String[] args) {
        if (kthSmallest(build(new Integer[] {3, 1, 4, null, 2}), 1) != 1) throw new AssertionError("example 1");
        if (kthSmallest(build(new Integer[] {5, 3, 6, 2, 4, null, null, 1}), 3) != 3) throw new AssertionError("example 2");
        boolean threw = false;
        try { kthSmallest(build(new Integer[] {2, 1}), 3); } catch (IllegalArgumentException expected) { threw = true; }
        if (!threw) throw new AssertionError("a rank beyond the size should be refused");
        Random rnd = new Random(16502);
        for (int t = 0; t < 5000; t++) {
            Node root = randomBst(rnd, 20, 80);
            List<Integer> keys = new ArrayList<>();
            spill(root, keys);
            Collections.sort(keys);
            for (int k = 1; k <= keys.size(); k++) {
                if (kthSmallest(root, k) != keys.get(k - 1)) throw new AssertionError("rank " + k + " wrong on " + keys);
            }
        }
    }
}
```

#### Solution: [Boundary] K At Either End (Author exercise)
<!-- id: tb-k-at-either-end -->

**Approach.** The smallest side is the stack walk that explores left first, and the largest side is the same walk with left and right exchanged, which produces keys in decreasing order. Each walk has its own countdown. Rank 1 gives the extremes and rank n gives them back swapped, so the assertions check those two ranks on every random tree besides all ranks in between. The oracle indexes a sorted list from the front and from the back.

**Complexity.** O(h + k) time for each walk, and O(h) stack space.

```java run
import java.util.*;

public final class BothEndsRun {
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
    static int rank(Node root, int k, boolean fromTop) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) { stack.push(node); node = fromTop ? node.right : node.left; }
            node = stack.pop();
            if (--k == 0) return node.val;
            node = fromTop ? node.left : node.right;
        }
        throw new IllegalArgumentException("rank out of range");
    }

    static String bothEnds(Node root, int k) {
        return "[" + rank(root, k, false) + ", " + rank(root, k, true) + "]";
    }

    public static void main(String[] args) {
        if (!bothEnds(build(new Integer[] {2, 1, 3}), 1).equals("[1, 3]")) throw new AssertionError("example 1");
        if (!bothEnds(build(new Integer[] {2, 1, 3}), 3).equals("[3, 1]")) throw new AssertionError("example 2");
        if (!bothEnds(build(new Integer[] {9}), 1).equals("[9, 9]")) throw new AssertionError("single key");
        Random rnd = new Random(16503);
        int ends = 0;
        for (int t = 0; t < 5000; t++) {
            Node root = randomBst(rnd, 18, 70);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            int n = sorted.size();
            for (int k = 1; k <= n; k++) {
                String want = "[" + sorted.get(k - 1) + ", " + sorted.get(n - k) + "]";
                if (!bothEnds(root, k).equals(want)) throw new AssertionError("rank " + k + " differs on " + sorted);
                if (k == 1 || k == n) ends++;
            }
        }
        if (ends < 3000) throw new AssertionError("too few end ranks tested: " + ends);
    }
}
```

#### Solution: [Recognize] Range Sum of BST (LeetCode 938)
<!-- id: tb-range-sum-bst -->

**Approach.** At a key below `low` only the right side can reach the band, at a key above `high` only the left side can, and at a key inside the band the key is added and both sides are entered. A visit counter shows the pruning at work. Every visited node is either in the band or lies on one of the two search paths for the limits, so the number of visits cannot exceed the band population plus twice the height, and the assertions check that bound. The oracle adds every key of a complete traversal that falls in the band and is accumulated as a `long`, which the same assertions use as the comparison value.

**Complexity.** O(h + m) time for m keys in the band, and O(h) recursion.

```java run
import java.util.*;

public final class RangeSumRun {
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
    static int visits;

    static long bandSum(Node node, int low, int high) {
        if (node == null) return 0;
        visits++;
        if (node.val < low) return bandSum(node.right, low, high);
        if (node.val > high) return bandSum(node.left, low, high);
        return node.val + bandSum(node.left, low, high) + bandSum(node.right, low, high);
    }

    static int height(Node n) {
        return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right));
    }

    public static void main(String[] args) {
        Node full = build(new Integer[] {8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15});
        if (bandSum(full, 5, 9) != 35) throw new AssertionError("example 1");
        if (bandSum(build(new Integer[] {10, 5, 15, 3, 7, null, 18}), 8, 9) != 0) throw new AssertionError("example 2");
        visits = 0;
        bandSum(full, 5, 9);
        if (visits != 8) throw new AssertionError("only eight of fifteen crates should be visited, saw " + visits);
        Random rnd = new Random(16504);
        for (int t = 0; t < 8000; t++) {
            Node root = randomBst(rnd, 22, 90);
            List<Integer> keys = new ArrayList<>();
            inorderInto(root, keys);
            int a = rnd.nextInt(95), b = rnd.nextInt(95);
            int low = Math.min(a, b), high = Math.max(a, b);
            long want = 0;
            int inside = 0;
            for (int k : keys) if (k >= low && k <= high) { want += k; inside++; }
            visits = 0;
            long got = bandSum(root, low, high);
            if (got != want) throw new AssertionError("sum differs for band " + low + ".." + high + " on " + keys);
            if (visits > inside + 2 * height(root)) throw new AssertionError("pruning did not hold: " + visits + " visits for " + inside + " keys");
        }
    }
}
```
