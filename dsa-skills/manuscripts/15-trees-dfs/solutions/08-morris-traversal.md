<!-- solutions-for: 08-morris-traversal -->
### Morris Traversal

#### Solution: [Build] Find Inorder Predecessor (Author exercise)
<!-- id: tr-find-predecessor -->

**Approach.** Locate the node holding `x` by scanning the built nodes. If it has no left child, the answer is -1. Otherwise step to the left child and then follow right links while they exist, and the node reached has a null right link and is the rightmost node of the left subtree. The oracle uses a different fact: the node met just before `x` in an ordinary recursive inorder listing is the predecessor whenever `x` has a left child, so the label just before `x` in that list should agree. The assertions check both on random trees for every node, and check a node without a left child separately.

**Complexity.** O(n) time to find the node and O(h) for the descent, with O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public final class FindPredecessor {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        List<Node> frontier = new ArrayList<>();
        Node root = new Node(v[0]);
        frontier.add(root);
        int at = 1;
        for (int f = 0; f < frontier.size() && at < v.length; f++) {
            Node top = frontier.get(f);
            for (int side = 0; side < 2 && at < v.length; side++, at++) {
                if (v[at] == null) continue;
                Node child = new Node(v[at]);
                if (side == 0) top.left = child; else top.right = child;
                frontier.add(child);
            }
        }
        return root;
    }

    static Node find(Node n, int x) {
        if (n == null) return null;
        if (n.val == x) return n;
        Node l = find(n.left, x);
        return l != null ? l : find(n.right, x);
    }

    static int predecessorInLeft(Node root, int x) {
        Node node = find(root, x);
        if (node.left == null) return -1;
        Node p = node.left;
        while (p.right != null) p = p.right;
        return p.val;
    }

    static void inorder(Node n, List<Integer> out) {
        if (n == null) return;
        inorder(n.left, out);
        out.add(n.val);
        inorder(n.right, out);
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(13);
        List<Integer> labels = new ArrayList<>();
        for (int i = 0; i < n; i++) labels.add(i * 11 + 3);
        Collections.shuffle(labels, rnd);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(labels.get(0));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(labels.get(made++)); open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        Node a = build(new Integer[] {4, 2, 7, 1, 3});
        if (predecessorInLeft(a, 4) != 3) throw new AssertionError("example 1");
        if (predecessorInLeft(a, 1) != -1) throw new AssertionError("example 2");
        if (predecessorInLeft(a, 2) != 1) throw new AssertionError("a node with a leaf on its left");
        Random rnd = new Random(15801);
        for (int t = 0; t < 4000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            List<Integer> in = new ArrayList<>();
            inorder(root, in);
            for (int idx = 0; idx < in.size(); idx++) {
                int x = in.get(idx);
                int got = predecessorInLeft(root, x);
                int want = find(root, x).left == null ? -1 : in.get(idx - 1);
                if (got != want) throw new AssertionError("differs for " + x + " on " + Arrays.toString(v));
            }
        }
    }
}
```

#### Solution: [Vary] Create And Remove One Thread (Author exercise)
<!-- id: tr-create-remove-thread -->

**Approach.** Run the Morris loop with three counters. At a node with a left child, find the predecessor by going left once and right until a null link or a link back to the current node. A null link means a first arrival: tie the thread, add one to the created count and to the number alive, update the largest alive count, and go left. A link back means a second arrival: cut it, add one to the removed count, subtract one from the number alive, and go right. The oracle needs no walk. Created and removed both equal the number of nodes that have a left child, and the most threads alive at once equals the largest number of left edges on any root-to-node path, because a thread is alive exactly while the walk is inside the left subtree it belongs to. The assertions compare on random trees.

**Complexity.** O(n) time and O(1) extra space apart from the counters.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class CreateRemoveThread {
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

    static int[] threadCounts(Node root) {
        int created = 0, removed = 0, alive = 0, most = 0;
        Node cur = root;
        while (cur != null) {
            if (cur.left == null) { cur = cur.right; continue; }
            Node pred = cur.left;
            while (pred.right != null && pred.right != cur) pred = pred.right;
            if (pred.right == null) {
                pred.right = cur;
                created++;
                alive++;
                most = Math.max(most, alive);
                cur = cur.left;
            } else {
                pred.right = null;
                removed++;
                alive--;
                cur = cur.right;
            }
        }
        return new int[] {created, removed, most};
    }

    static int withLeft(Node n) {
        if (n == null) return 0;
        return (n.left != null ? 1 : 0) + withLeft(n.left) + withLeft(n.right);
    }

    static int leftTurns(Node n, int sofar) {
        if (n == null) return sofar;
        int best = sofar;
        if (n.left != null) best = Math.max(best, leftTurns(n.left, sofar + 1));
        if (n.right != null) best = Math.max(best, leftTurns(n.right, sofar));
        return best;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(0);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < (c == 0 ? 3 : 3)) { out.add(made++); open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(threadCounts(build(new Integer[] {2, 1, 3})), new int[] {1, 1, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(threadCounts(build(new Integer[] {1, 2, null, 3})), new int[] {2, 2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(threadCounts(build(new Integer[] {})), new int[] {0, 0, 0})) throw new AssertionError("empty tree");
        Random rnd = new Random(15802);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            Node expectedShape = build(v);
            int withLeftChild = withLeft(expectedShape);
            int most = leftTurns(expectedShape, 0);
            int[] got = threadCounts(build(v));
            if (!Arrays.equals(got, new int[] {withLeftChild, withLeftChild, most})) throw new AssertionError("differs on " + Arrays.toString(v) + " got " + Arrays.toString(got));
        }
    }
}
```

#### Solution: [Boundary] No Left Child And Existing Thread (Author exercise)
<!-- id: tr-direct-versus-restored -->

**Approach.** In the Morris loop, a node without a left child is recorded right away and counts as direct, and moving right may follow a thread to an ancestor, which is not a new arrival of a different kind. A node with a left child is reached twice. The first arrival finds a null link and ties a thread without recording anything. The second arrival finds the thread, cuts it, records the node, and counts as restored. So direct equals the number of nodes with no left child and restored equals the number with one, and the two sum to the node count. The assertions compute both numbers by structure on random trees, and show with an existing thread, tied by hand, that the loop cuts it and counts the node as restored instead of tying a second one.

**Complexity.** O(n) time and O(1) extra space.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DirectVersusRestored {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node root = new Node(v[0]);
        List<Node> line = new ArrayList<>();
        line.add(root);
        int pos = 1;
        for (int k = 0; k < line.size() && pos < v.length; k++) {
            Node parent = line.get(k);
            Integer a = v[pos++];
            if (a != null) { parent.left = new Node(a); line.add(parent.left); }
            if (pos < v.length) {
                Integer b = v[pos++];
                if (b != null) { parent.right = new Node(b); line.add(parent.right); }
            }
        }
        return root;
    }

    static int[] directAndRestored(Node root) {
        int direct = 0, restored = 0;
        Node cur = root;
        while (cur != null) {
            if (cur.left == null) { direct++; cur = cur.right; continue; }
            Node pred = cur.left;
            while (pred.right != null && pred.right != cur) pred = pred.right;
            if (pred.right == null) { pred.right = cur; cur = cur.left; }
            else { pred.right = null; restored++; cur = cur.right; }
        }
        return new int[] {direct, restored};
    }

    static int[] byStructure(Node n) {
        if (n == null) return new int[] {0, 0};
        int[] l = byStructure(n.left), r = byStructure(n.right);
        int d = l[0] + r[0] + (n.left == null ? 1 : 0);
        int s = l[1] + r[1] + (n.left != null ? 1 : 0);
        return new int[] {d, s};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(0);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(made++); open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(directAndRestored(build(new Integer[] {1, null, 2, null, 3})), new int[] {3, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(directAndRestored(build(new Integer[] {2, 1, 3})), new int[] {2, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(directAndRestored(null), new int[] {0, 0})) throw new AssertionError("empty tree");
        Node root = build(new Integer[] {2, 1, 3});
        root.left.right = root;
        int[] withThread = directAndRestored(root);
        if (root.left.right != null) throw new AssertionError("an existing thread is cut on arrival");
        if (withThread[1] != 1) throw new AssertionError("the node with a left child is restored once");
        Random rnd = new Random(15803);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            int[] want = byStructure(build(v));
            int[] got = directAndRestored(build(v));
            if (!Arrays.equals(got, want)) throw new AssertionError("differs on " + Arrays.toString(v));
            if (got[0] + got[1] != v.length - Arrays.stream(v).filter(x -> x == null).count()) throw new AssertionError("every node is recorded exactly once");
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: tr-morris-inorder -->

**Approach.** Run the Morris loop and build the result with the thread count first. A node with no left child is appended and the cursor moves right. Otherwise find the predecessor, and a null link on it means tie a thread, count it, and go left, while a link back to the cursor means cut it, append the node, and go right. Because every thread is cut on the second arrival, the tree returns to its original shape. The assertions record the left and right references of every node before the walk and compare them after it, compare the values with a recursive inorder, and compare the count with the number of nodes having a left child. They also run a version that forgets the cut, and show that a recursive walk of the damaged tree exceeds a generous call budget, because the leftover thread leads back to an ancestor.

**Complexity.** O(n) time and O(1) extra space besides the result.

```java run
import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

public final class MorrisInorder {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node root = new Node(v[0]);
        List<Node> level = new ArrayList<>();
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

    static List<Integer> morris(Node root, boolean cut) {
        List<Integer> out = new ArrayList<>();
        out.add(0);
        int threads = 0;
        Node cur = root;
        while (cur != null) {
            if (cur.left == null) { out.add(cur.val); cur = cur.right; continue; }
            Node pred = cur.left;
            while (pred.right != null && pred.right != cur) pred = pred.right;
            if (pred.right == null) { pred.right = cur; threads++; cur = cur.left; }
            else { if (cut) pred.right = null; out.add(cur.val); cur = cur.right; }
        }
        out.set(0, threads);
        return out;
    }

    static void recursive(Node n, List<Integer> out) {
        if (n == null) return;
        recursive(n.left, out);
        out.add(n.val);
        recursive(n.right, out);
    }

    static int withLeft(Node n) {
        return n == null ? 0 : (n.left != null ? 1 : 0) + withLeft(n.left) + withLeft(n.right);
    }

    static void snapshot(Node n, Map<Node, Node[]> into) {
        if (n == null) return;
        into.put(n, new Node[] {n.left, n.right});
        snapshot(n.left, into);
        snapshot(n.right, into);
    }

    static int calls, budget;

    static boolean exceeds(Node n) {
        if (n == null) return false;
        if (++calls > budget) return true;
        return exceeds(n.left) || exceeds(n.right);
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(2001) - 1000);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(made * 3 + rnd.nextInt(2)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!morris(build(new Integer[] {2, 1, 3}), true).equals(List.of(1, 1, 2, 3))) throw new AssertionError("example 1");
        if (!morris(build(new Integer[] {1, null, 2, 3}), true).equals(List.of(1, 1, 3, 2))) throw new AssertionError("example 2");
        Random rnd = new Random(15804);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            Map<Node, Node[]> before = new IdentityHashMap<>();
            snapshot(root, before);
            List<Integer> got = morris(root, true);
            List<Integer> want = new ArrayList<>();
            want.add(withLeft(root));
            recursive(root, want);
            if (!got.equals(want)) throw new AssertionError("differs on " + java.util.Arrays.toString(v));
            for (Map.Entry<Node, Node[]> e : before.entrySet()) {
                if (e.getKey().left != e.getValue()[0] || e.getKey().right != e.getValue()[1]) throw new AssertionError("the tree changed");
            }
        }
        Node damaged = build(new Integer[] {2, 1, 3});
        morris(damaged, false);
        calls = 0;
        budget = 100;
        if (!exceeds(damaged)) throw new AssertionError("a thread left in place makes a recursive walk loop");
    }
}
```
