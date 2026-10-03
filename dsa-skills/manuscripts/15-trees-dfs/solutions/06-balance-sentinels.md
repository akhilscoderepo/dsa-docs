<!-- solutions-for: 06-balance-sentinels -->
### Balance Sentinels

#### Solution: [Build] Height Or Failure (Author exercise)
<!-- id: tr-height-or-failure -->

**Approach.** The helper returns the node-count height of a steady subtree and -1 for a failed one. It asks the left side first and returns -1 immediately when that fails, then the right side with the same rule, and only then compares the two heights, so a sentinel is never used as a height. A null side returns 0. The oracle takes a different route: it computes true heights for every node by a reverse pass over child positions, checks all nodes for a difference above one, and answers the root height or -1. The assertions compare on random trees, including some skewed ones, and check that a failure on the left side stops the walk before the right side is entered, by counting calls.

**Complexity.** O(n) time and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class HeightOrFailure {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node[] seat = new Node[v.length];
        seat[0] = new Node(v[0]);
        int feed = 1;
        for (int p = 0; p < v.length && feed < v.length; p++) {
            if (seat[p] == null) continue;
            if (v[feed] != null) seat[p].left = seat[feed] = new Node(v[feed]);
            feed++;
            if (feed < v.length) {
                if (v[feed] != null) seat[p].right = seat[feed] = new Node(v[feed]);
                feed++;
            }
        }
        return seat[0];
    }

    static final int FAILED = -1;
    static int calls;

    static int heightOrFailed(Node node) {
        calls++;
        if (node == null) return 0;
        int l = heightOrFailed(node.left);
        if (l == FAILED) return FAILED;
        int r = heightOrFailed(node.right);
        if (r == FAILED) return FAILED;
        if (Math.abs(l - r) > 1) return FAILED;
        return 1 + Math.max(l, r);
    }

    static int oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return 0;
        int[] lc = new int[n], rc = new int[n], h = new int[n];
        Arrays.fill(lc, -1);
        Arrays.fill(rc, -1);
        boolean[] live = new boolean[n];
        live[0] = true;
        int nx = 1;
        for (int p = 0; p < n && nx < n; p++) {
            if (!live[p]) continue;
            if (v[nx] != null) { lc[p] = nx; live[nx] = true; }
            nx++;
            if (nx < n) {
                if (v[nx] != null) { rc[p] = nx; live[nx] = true; }
                nx++;
            }
        }
        boolean ok = true;
        for (int p = n - 1; p >= 0; p--) {
            if (!live[p]) continue;
            int a = lc[p] >= 0 ? h[lc[p]] : 0;
            int b = rc[p] >= 0 ? h[rc[p]] : 0;
            if (Math.abs(a - b) > 1) ok = false;
            h[p] = 1 + Math.max(a, b);
        }
        return ok ? h[0] : -1;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        int lean = rnd.nextInt(3);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(1001));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                boolean take = made < n && rnd.nextInt(lean == 0 ? 2 : 4) != 0 && (lean != 1 || c == 0 || rnd.nextInt(6) == 0);
                if (take) { out.add(rnd.nextInt(1001)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (heightOrFailed(build(new Integer[] {3, 9, 20, null, null, 15, 7})) != 3) throw new AssertionError("example 1");
        if (heightOrFailed(build(new Integer[] {1, 2, null, 3})) != -1) throw new AssertionError("example 2");
        if (heightOrFailed(build(new Integer[] {})) != 0) throw new AssertionError("empty tree has height 0");
        calls = 0;
        Node deepLeft = build(new Integer[] {1, 2, 3, 4, null, null, null, 5, null});
        if (heightOrFailed(deepLeft) != -1) throw new AssertionError("left failure");
        if (calls >= 13) throw new AssertionError("the right side is not entered after a left failure: " + calls);
        Random rnd = new Random(15601);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (heightOrFailed(build(v)) != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Detect Local Imbalance (Author exercise)
<!-- id: tr-local-imbalance -->

**Approach.** Use the same one-pass helper on child positions, with one addition: when a comparison fails, store the label of that node, but only if no label has been stored yet, and return the failure value. A node whose child already failed returns failure without comparing, so the stored label belongs to the first failing node in postorder, whose two sides are both valid. The oracle computes true heights for every node first, then lists nodes in postorder by an independent recursion and picks the first whose heights differ by more than one. The assertions compare the two labels on random trees and check the answer -1 on a balanced tree.

**Complexity.** O(n) time and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class LocalImbalance {
    static int[] lc, rc;
    static Integer[] vals;
    static int culprit;

    static void link(Integer[] v) {
        vals = v;
        int n = v.length;
        lc = new int[n];
        rc = new int[n];
        Arrays.fill(lc, -1);
        Arrays.fill(rc, -1);
        boolean[] live = new boolean[n];
        if (n > 0) live[0] = true;
        int k = 1;
        for (int p = 0; p < n && k < n; p++) {
            if (!live[p]) continue;
            if (v[k] != null) { lc[p] = k; live[k] = true; }
            k++;
            if (k < n) {
                if (v[k] != null) { rc[p] = k; live[k] = true; }
                k++;
            }
        }
    }

    static int helper(int at) {
        if (at < 0) return 0;
        int l = helper(lc[at]);
        if (l < 0) return -1;
        int r = helper(rc[at]);
        if (r < 0) return -1;
        if (Math.abs(l - r) > 1) {
            if (culprit == -1) culprit = vals[at];
            return -1;
        }
        return 1 + Math.max(l, r);
    }

    static int firstCulprit(Integer[] v) {
        link(v);
        culprit = -1;
        if (v.length > 0) helper(0);
        return culprit;
    }

    static int trueHeight(int at) {
        return at < 0 ? 0 : 1 + Math.max(trueHeight(lc[at]), trueHeight(rc[at]));
    }

    static void postorder(int at, List<Integer> out) {
        if (at < 0) return;
        postorder(lc[at], out);
        postorder(rc[at], out);
        out.add(at);
    }

    static int oracle(Integer[] v) {
        link(v);
        if (v.length == 0) return -1;
        List<Integer> order = new ArrayList<>();
        postorder(0, order);
        for (int at : order) {
            if (Math.abs(trueHeight(lc[at]) - trueHeight(rc[at])) > 1) return v[at];
        }
        return -1;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(1001));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < (c == 0 ? 4 : 2)) { out.add(rnd.nextInt(1001)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (firstCulprit(new Integer[] {1, 2, null, 3}) != 1) throw new AssertionError("example 1");
        if (firstCulprit(new Integer[] {1, 2, 3, 4, null, null, null, 5}) != 2) throw new AssertionError("example 2");
        if (firstCulprit(new Integer[] {1, 2, 3}) != -1) throw new AssertionError("balanced tree");
        if (firstCulprit(new Integer[] {}) != -1) throw new AssertionError("empty tree");
        Random rnd = new Random(15602);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            int got = firstCulprit(v);
            if (got != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Empty Tree Height (Author exercise)
<!-- id: tr-empty-tree-height -->

**Approach.** With heights counted in edges, a null side returns -1 and a leaf returns 0, so the old failure value -1 would be a legal result. The failure constant therefore moves to -2, which no tree can have as a height. The helper checks for -2 before any arithmetic, compares the two heights with a difference of at most one, which holds for the pair `(-1, 0)` of a leaf with a missing side, and returns one plus the larger height. The assertions show the collision directly, by running a version that keeps -1 as the failure value and reporting a wrong failure for a lopsided but steady tree, and show that `Math.abs(Integer.MIN_VALUE)` stays negative, which is why the sentinel is small rather than extreme. The oracle derives edge heights from the node-count pass.

**Complexity.** O(n) time and O(h) stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class EmptyTreeHeight {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node root = new Node(v[0]);
        Deque<Node> parents = new ArrayDeque<>();
        parents.add(root);
        boolean toLeft = true;
        for (int i = 1; i < v.length; i++) {
            Node parent = parents.peek();
            Node child = v[i] == null ? null : new Node(v[i]);
            if (child != null) parents.add(child);
            if (toLeft) { parent.left = child; toLeft = false; }
            else { parent.right = child; toLeft = true; parents.poll(); }
        }
        return root;
    }

    static final int FAILED = -2;

    static int edgeHeight(Node node) {
        if (node == null) return -1;
        int l = edgeHeight(node.left);
        if (l == FAILED) return FAILED;
        int r = edgeHeight(node.right);
        if (r == FAILED) return FAILED;
        if (Math.abs(l - r) > 1) return FAILED;
        return 1 + Math.max(l, r);
    }

    static int collidingEdgeHeight(Node node) {
        if (node == null) return -1;
        int l = collidingEdgeHeight(node.left);
        if (l == -1 && node.left != null) return -1;
        if (l == -1) l = -1;
        int r = collidingEdgeHeight(node.right);
        if (r == -1 && node.right != null) return -1;
        if (node.left == null && node.right == null) return 0;
        if (Math.abs(l - r) > 1) return -1;
        return 1 + Math.max(l, r);
    }

    static int oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return -1;
        int[] lc = new int[n], rc = new int[n], h = new int[n];
        Arrays.fill(lc, -1);
        Arrays.fill(rc, -1);
        boolean[] live = new boolean[n];
        live[0] = true;
        int nx = 1;
        for (int p = 0; p < n && nx < n; p++) {
            if (!live[p]) continue;
            if (v[nx] != null) { lc[p] = nx; live[nx] = true; }
            nx++;
            if (nx < n) {
                if (v[nx] != null) { rc[p] = nx; live[nx] = true; }
                nx++;
            }
        }
        boolean ok = true;
        for (int p = n - 1; p >= 0; p--) {
            if (!live[p]) continue;
            int a = lc[p] >= 0 ? h[lc[p]] : -1;
            int b = rc[p] >= 0 ? h[rc[p]] : -1;
            if (Math.abs(a - b) > 1) ok = false;
            h[p] = 1 + Math.max(a, b);
        }
        return ok ? h[0] : -2;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(1001));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < (c == 0 ? 4 : 2)) { out.add(rnd.nextInt(1001)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (edgeHeight(build(new Integer[] {})) != -1) throw new AssertionError("example 1");
        if (edgeHeight(build(new Integer[] {1, 2, null, 3})) != -2) throw new AssertionError("example 2");
        if (edgeHeight(build(new Integer[] {5})) != 0) throw new AssertionError("a single node has edge height 0");
        if (edgeHeight(build(new Integer[] {1, 2})) != 1) throw new AssertionError("a node with one leaf is steady");
        if (Math.abs(Integer.MIN_VALUE) >= 0) throw new AssertionError("abs of the smallest int stays negative");
        if (collidingEdgeHeight(build(new Integer[] {1, 2})) != 1) throw new AssertionError("this case happens to survive the collision");
        Random rnd = new Random(15603);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (edgeHeight(build(v)) != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Recognize] Balanced Binary Tree (LeetCode 110)
<!-- id: tr-balanced-tree -->

**Approach.** Fold detection and measurement into one postorder helper that returns the height or the failure value, and report true when the final value is not the failure value. The brute-force oracle is the separate-height version that checks every node by re-measuring both sides, which is correct but repeats work. The assertions compare the two verdicts on random trees with labels that may be negative, and count calls on a perfect tree of 4095 rods to show that the one-pass helper makes about two calls per rod while the re-measuring version makes several times as many, because each rod is measured again by every rod above it.

**Complexity.** O(n) time and O(h) stack, against O(n log n) on a steady tree for the re-measuring version.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class BalancedTree {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        List<Node> level = new ArrayList<>();
        Node root = new Node(v[0]);
        level.add(root);
        int pos = 1;
        for (int k = 0; k < level.size() && pos < v.length; k++) {
            Node parent = level.get(k);
            for (int side = 0; side < 2 && pos < v.length; side++, pos++) {
                if (v[pos] == null) continue;
                Node child = new Node(v[pos]);
                if (side == 0) parent.left = child; else parent.right = child;
                level.add(child);
            }
        }
        return root;
    }

    static long onePassCalls, remeasureCalls;

    static int heightOrFailed(Node node) {
        onePassCalls++;
        if (node == null) return 0;
        int l = heightOrFailed(node.left);
        if (l < 0) return -1;
        int r = heightOrFailed(node.right);
        if (r < 0) return -1;
        return Math.abs(l - r) > 1 ? -1 : 1 + Math.max(l, r);
    }

    static boolean isBalanced(Node root) { return heightOrFailed(root) >= 0; }

    static int reach(Node node) {
        remeasureCalls++;
        return node == null ? 0 : 1 + Math.max(reach(node.left), reach(node.right));
    }

    static Node full(int levels) {
        if (levels == 0) return null;
        Node n = new Node(levels);
        n.left = full(levels - 1);
        n.right = full(levels - 1);
        return n;
    }

    static boolean remeasuring(Node node) {
        if (node == null) return true;
        if (Math.abs(reach(node.left) - reach(node.right)) > 1) return false;
        return remeasuring(node.left) && remeasuring(node.right);
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(15);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(2001) - 1000);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < (c == 0 ? 4 : 3)) { out.add(rnd.nextInt(2001) - 1000); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!isBalanced(build(new Integer[] {2, 1, 3, 0, 7}))) throw new AssertionError("example 1");
        if (isBalanced(build(new Integer[] {1, null, 2, null, 3}))) throw new AssertionError("example 2");
        if (!isBalanced(null)) throw new AssertionError("the empty tree is balanced");
        Random rnd = new Random(15604);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            if (isBalanced(root) != remeasuring(root)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
        int levels = 12;
        Node perfect = full(levels);
        onePassCalls = 0;
        remeasureCalls = 0;
        if (!isBalanced(perfect) || !remeasuring(perfect)) throw new AssertionError("a perfect tree is balanced");
        if (onePassCalls != 2L * ((1 << levels) - 1) + 1) throw new AssertionError("one pass makes two calls per rod and one for the root: " + onePassCalls);
        if (remeasureCalls < 4 * onePassCalls) throw new AssertionError("re-measuring repeats work: " + remeasureCalls + " against " + onePassCalls);
    }
}
```
