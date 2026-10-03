<!-- solutions-for: 07-traversal-reconstruction -->
### Traversal Reconstruction

#### Solution: [Build] Split One Root (Author exercise)
<!-- id: tr-split-one-root -->

**Approach.** The first preorder label is the root. Scan the inorder sequence for it, and the number of labels before it is the left size, while everything after it is the right size, which is the total minus the left size minus one. An empty input returns both sizes as zero. The assertions generate random trees with distinct labels, record the true subtree sizes from the structure while building, produce both traversals by recursion, and compare the answer with those sizes. They also check that swapping the roles of left and right changes the answer, which shows that the inorder position is what carries the information.

**Complexity.** O(n) time for the scan and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class SplitOneRoot {
    static final class Node {
        final int val;
        Node left, right;
        int size;
        Node(int val) { this.val = val; }
    }

    static int[] split(int[] preorder, int[] inorder) {
        if (preorder.length == 0) return new int[] {0, 0};
        int at = 0;
        while (inorder[at] != preorder[0]) at++;
        return new int[] {at, preorder.length - at - 1};
    }

    static int cursor;
    static List<Integer> labels;

    static Node shape(Random rnd, int n) {
        if (n == 0) return null;
        Node node = new Node(labels.get(cursor++));
        int leftCount = rnd.nextInt(n);
        node.left = shape(rnd, leftCount);
        node.right = shape(rnd, n - 1 - leftCount);
        node.size = n;
        return node;
    }

    static void walkPre(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        walkPre(n.left, out);
        walkPre(n.right, out);
    }

    static void walkIn(Node n, List<Integer> out) {
        if (n == null) return;
        walkIn(n.left, out);
        out.add(n.val);
        walkIn(n.right, out);
    }

    static int[] toArray(List<Integer> list) {
        int[] a = new int[list.size()];
        for (int i = 0; i < a.length; i++) a[i] = list.get(i);
        return a;
    }

    public static void main(String[] args) {
        if (!Arrays.equals(split(new int[] {3, 9, 20, 15, 7}, new int[] {9, 3, 15, 20, 7}), new int[] {1, 3})) throw new AssertionError("example 1");
        if (!Arrays.equals(split(new int[] {1}, new int[] {1}), new int[] {0, 0})) throw new AssertionError("example 2");
        if (!Arrays.equals(split(new int[0], new int[0]), new int[] {0, 0})) throw new AssertionError("empty input");
        Random rnd = new Random(15701);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(12);
            labels = new ArrayList<>();
            for (int i = 0; i < n; i++) labels.add(i * 3 - 10);
            Collections.shuffle(labels, rnd);
            cursor = 0;
            Node root = shape(rnd, n);
            List<Integer> pre = new ArrayList<>(), in = new ArrayList<>();
            walkPre(root, pre);
            walkIn(root, in);
            int leftSize = root.left == null ? 0 : root.left.size;
            int rightSize = root.right == null ? 0 : root.right.size;
            int[] got = split(toArray(pre), toArray(in));
            if (got[0] != leftSize || got[1] != rightSize) throw new AssertionError("sizes differ on " + pre + " " + in);
            if (got[0] + got[1] + 1 != n) throw new AssertionError("the two sides and the root cover every label");
        }
    }
}
```

#### Solution: [Vary] Reconstruct By Index Ranges (Author exercise)
<!-- id: tr-rebuild-by-ranges -->

**Approach.** Fill a map from label to inorder position, then call a builder with the two end positions of the stretch it owns. An empty stretch returns null. Otherwise the builder takes the next preorder label as the root, looks up its position, builds the left subtree on the stretch before it, and then builds the right subtree on the stretch after it, in that order because the shared counter follows preorder. The result is then read out in postorder. The oracle is the random tree itself: the assertions generate a tree with distinct labels, derive both sequences, rebuild, and compare the postorder of the rebuilt tree with the postorder of the original. They also verify that the counter ends at the length of the sequence.

**Complexity.** O(n) time and O(n) space for the map and the stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class RebuildByRanges {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int next;
    static int[] pre;
    static Map<Integer, Integer> where;

    static Node build(int lo, int hi) {
        if (lo > hi) return null;
        Node node = new Node(pre[next++]);
        int mid = where.get(node.val);
        node.left = build(lo, mid - 1);
        node.right = build(mid + 1, hi);
        return node;
    }

    static List<Integer> postorderOfRebuild(int[] preorder, int[] inorder) {
        pre = preorder;
        next = 0;
        where = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) where.put(inorder[i], i);
        Node root = build(0, inorder.length - 1);
        if (next != preorder.length) throw new AssertionError("every preorder label is consumed once");
        List<Integer> out = new ArrayList<>();
        post(root, out);
        return out;
    }

    static void post(Node n, List<Integer> out) {
        if (n == null) return;
        post(n.left, out);
        post(n.right, out);
        out.add(n.val);
    }

    static Node randomTree(Random rnd, int n, int[] labels, int[] used) {
        if (n == 0) return null;
        Node node = new Node(labels[used[0]++]);
        int leftCount = rnd.nextInt(n);
        node.left = randomTree(rnd, leftCount, labels, used);
        node.right = randomTree(rnd, n - 1 - leftCount, labels, used);
        return node;
    }

    static void pre(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        pre(n.left, out);
        pre(n.right, out);
    }

    static void in(Node n, List<Integer> out) {
        if (n == null) return;
        in(n.left, out);
        out.add(n.val);
        in(n.right, out);
    }

    static int[] arr(List<Integer> l) {
        return l.stream().mapToInt(Integer::intValue).toArray();
    }

    public static void main(String[] args) {
        if (!postorderOfRebuild(new int[] {3, 9, 20, 15, 7}, new int[] {9, 3, 15, 20, 7}).equals(List.of(9, 15, 7, 20, 3))) throw new AssertionError("example 1");
        if (!postorderOfRebuild(new int[] {1, 2, 3}, new int[] {2, 1, 3}).equals(List.of(2, 3, 1))) throw new AssertionError("example 2");
        if (!postorderOfRebuild(new int[0], new int[0]).isEmpty()) throw new AssertionError("empty input");
        Random rnd = new Random(15702);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(14);
            List<Integer> pool = new ArrayList<>();
            for (int i = 0; i < n; i++) pool.add(100 + i * 7);
            Collections.shuffle(pool, rnd);
            Node original = randomTree(rnd, n, arr(pool), new int[] {0});
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>(), want = new ArrayList<>();
            pre(original, p);
            in(original, i);
            post(original, want);
            if (!postorderOfRebuild(arr(p), arr(i)).equals(want)) throw new AssertionError("differs on " + p + " " + i);
        }
    }
}
```

#### Solution: [Boundary] Empty Range And Skewed Tree (Author exercise)
<!-- id: tr-empty-range-skewed -->

**Approach.** The builder stops exactly when its stretch is empty, meaning the start is greater than the end, and it counts that entry before returning. Each real call creates one node and makes two further calls, so a tree of n nodes makes n real calls and n + 1 empty ones, whatever its shape. The height comes back as one plus the larger of the two child heights during the same walk, so a chain of nodes gives the full length without a separate pass. An empty input makes one empty call and has height 0. The assertions check the identity n + 1 on random trees, compare the height with the height of the generated tree, and run chains of 2000 nodes down both sides.

**Complexity.** O(n) time and O(h) stack beyond the map.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class EmptyRangeSkewed {
    static int next, emptyCalls;
    static int[] pre;
    static Map<Integer, Integer> where;

    static int heightOfBuild(int lo, int hi) {
        if (lo > hi) { emptyCalls++; return 0; }
        int root = pre[next++];
        int mid = where.get(root);
        int l = heightOfBuild(lo, mid - 1);
        int r = heightOfBuild(mid + 1, hi);
        return 1 + Math.max(l, r);
    }

    static int[] measure(int[] preorder, int[] inorder) {
        pre = preorder;
        next = 0;
        emptyCalls = 0;
        where = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) where.put(inorder[i], i);
        int h = heightOfBuild(0, inorder.length - 1);
        return new int[] {h, emptyCalls};
    }

    static final class Tree {
        final int val;
        Tree left, right;
        Tree(int val) { this.val = val; }
    }

    static Tree random(Random rnd, int n, List<Integer> labels) {
        if (n == 0) return null;
        Tree t = new Tree(labels.remove(labels.size() - 1));
        int k = rnd.nextInt(n);
        t.left = random(rnd, k, labels);
        t.right = random(rnd, n - 1 - k, labels);
        return t;
    }

    static void preOf(Tree t, List<Integer> out) {
        if (t == null) return;
        out.add(t.val);
        preOf(t.left, out);
        preOf(t.right, out);
    }

    static void inOf(Tree t, List<Integer> out) {
        if (t == null) return;
        inOf(t.left, out);
        out.add(t.val);
        inOf(t.right, out);
    }

    static int heightOf(Tree t) { return t == null ? 0 : 1 + Math.max(heightOf(t.left), heightOf(t.right)); }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        if (!Arrays.equals(measure(new int[0], new int[0]), new int[] {0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(measure(new int[] {1, 2, 3}, new int[] {3, 2, 1}), new int[] {3, 4})) throw new AssertionError("example 2");
        Random rnd = new Random(15703);
        for (int t = 0; t < 4000; t++) {
            int n = rnd.nextInt(15);
            List<Integer> labels = new ArrayList<>();
            for (int i = 0; i < n; i++) labels.add(i * 5 + 1);
            Collections.shuffle(labels, rnd);
            Tree tree = random(rnd, n, labels);
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>();
            preOf(tree, p);
            inOf(tree, i);
            int[] got = measure(arr(p), arr(i));
            if (got[0] != heightOf(tree)) throw new AssertionError("height differs on " + p + " " + i);
            if (got[1] != n + 1) throw new AssertionError("a tree of " + n + " nodes makes " + (n + 1) + " empty calls, got " + got[1]);
        }
        int len = 2000;
        int[] down = new int[len], up = new int[len];
        for (int k = 0; k < len; k++) { down[k] = k; up[k] = len - 1 - k; }
        if (!Arrays.equals(measure(down, up), new int[] {len, len + 1})) throw new AssertionError("left chain");
        if (!Arrays.equals(measure(down, down), new int[] {len, len + 1})) throw new AssertionError("right chain");
    }
}
```

#### Solution: [Recognize] Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105)
<!-- id: tr-construct-from-pre-in -->

**Approach.** Build an index map from each label to its inorder position, then recurse on stretches with a shared preorder counter: take the next preorder label as the root, split the stretch at the root's position, build the left side, and then the right. The finished tree is written out level by level, with `null` for missing children and the trailing nulls removed, to match the output format. The linear-search version, which scans the inorder sequence for every root, serves as the oracle for the work done, and the assertions compare its trees with the map version on random inputs and count the scanned positions on a chain, where the map does none. The expected level-order array comes from the generated tree itself.

**Complexity.** O(n) time with the map, against O(n^2) for repeated scans, and O(n) space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Deque;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class ConstructFromPreIn {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int next;
    static int[] pre, in;
    static Map<Integer, Integer> where;
    static long scanned;

    static Node build(int lo, int hi) {
        if (lo > hi) return null;
        Node node = new Node(pre[next++]);
        int mid = where.get(node.val);
        node.left = build(lo, mid - 1);
        node.right = build(mid + 1, hi);
        return node;
    }

    static Node construct(int[] preorder, int[] inorder) {
        pre = preorder;
        next = 0;
        where = new HashMap<>();
        for (int i = 0; i < inorder.length; i++) where.put(inorder[i], i);
        return build(0, inorder.length - 1);
    }

    static Node buildScan(int lo, int hi) {
        if (lo > hi) return null;
        Node node = new Node(pre[next++]);
        int mid = lo;
        while (in[mid] != node.val) { mid++; scanned++; }
        node.left = buildScan(lo, mid - 1);
        node.right = buildScan(mid + 1, hi);
        return node;
    }

    static Node constructByScan(int[] preorder, int[] inorder) {
        pre = preorder;
        in = inorder;
        next = 0;
        scanned = 0;
        return buildScan(0, inorder.length - 1);
    }

    static List<Integer> levels(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> q = new LinkedList<>();
        if (root != null) q.add(root);
        while (!q.isEmpty()) {
            Node cur = q.poll();
            if (cur == null) { out.add(null); continue; }
            out.add(cur.val);
            q.add(cur.left);
            q.add(cur.right);
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out;
    }

    static Node random(Random rnd, int n, List<Integer> labels) {
        if (n == 0) return null;
        Node t = new Node(labels.remove(labels.size() - 1));
        int k = rnd.nextInt(n);
        t.left = random(rnd, k, labels);
        t.right = random(rnd, n - 1 - k, labels);
        return t;
    }

    static void preOf(Node t, List<Integer> out) {
        if (t == null) return;
        out.add(t.val);
        preOf(t.left, out);
        preOf(t.right, out);
    }

    static void inOf(Node t, List<Integer> out) {
        if (t == null) return;
        inOf(t.left, out);
        out.add(t.val);
        inOf(t.right, out);
    }

    static int[] arr(List<Integer> l) { return l.stream().mapToInt(Integer::intValue).toArray(); }

    public static void main(String[] args) {
        if (!levels(construct(new int[] {1, 2, 4, 5, 3}, new int[] {4, 2, 5, 1, 3})).equals(Arrays.asList(1, 2, 3, 4, 5))) throw new AssertionError("example 1");
        if (!levels(construct(new int[] {5, 6, 7}, new int[] {5, 6, 7})).equals(Arrays.asList(5, null, 6, null, 7))) throw new AssertionError("example 2");
        Random rnd = new Random(15704);
        for (int t = 0; t < 4000; t++) {
            int n = 1 + rnd.nextInt(14);
            List<Integer> labels = new ArrayList<>();
            for (int i = 0; i < n; i++) labels.add(i * 4 - 20);
            Collections.shuffle(labels, rnd);
            Node original = random(rnd, n, labels);
            List<Integer> p = new ArrayList<>(), i = new ArrayList<>();
            preOf(original, p);
            inOf(original, i);
            List<Integer> want = levels(original);
            if (!levels(construct(arr(p), arr(i))).equals(want)) throw new AssertionError("map version differs on " + p + " " + i);
            if (!levels(constructByScan(arr(p), arr(i))).equals(want)) throw new AssertionError("scan version differs on " + p + " " + i);
        }
        int len = 1500;
        int[] a = new int[len], b = new int[len];
        for (int k = 0; k < len; k++) { a[k] = k; b[k] = len - 1 - k; }
        constructByScan(a, b);
        if (scanned < (long) len * (len - 1) / 2 / 2) throw new AssertionError("the scanning version does quadratic work on a chain: " + scanned);
    }
}
```
