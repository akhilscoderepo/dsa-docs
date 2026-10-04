<!-- solutions-for: 04-successor-and-predecessor -->
### Successor And Predecessor

#### Solution: [Build] Minimum Of Right Subtree (Author exercise)
<!-- id: tb-right-subtree-minimum -->

**Approach.** Search for the key by comparisons, step once to its right child, and then follow left links until the next one is null. The oracle does not use the shape at all: it gathers every key of the right side into a list with a plain traversal and takes the least. The assertions compare the two for every node that has a right side in random search trees, and check that the answer is the same as the next key in sorted order, which is why the exercise is the inside case of the successor.

**Complexity.** O(h) time and O(1) extra space.

```java run
import java.util.*;

public final class RightMinimumRun {
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
    static int rightMinimum(Node root, int key) {
        Node node = root;
        while (node.val != key) node = key < node.val ? node.left : node.right;
        node = node.right;
        while (node.left != null) node = node.left;
        return node.val;
    }

    static void gather(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        gather(n.left, out);
        gather(n.right, out);
    }

    static void allNodes(Node n, List<Node> out) {
        if (n == null) return;
        out.add(n);
        allNodes(n.left, out);
        allNodes(n.right, out);
    }

    public static void main(String[] args) {
        Integer[] sample = {8, 3, 10, 1, 6, null, 14, null, null, 4, 7, 13};
        if (rightMinimum(build(sample), 3) != 4) throw new AssertionError("example 1");
        if (rightMinimum(build(sample), 8) != 10) throw new AssertionError("example 2");
        if (rightMinimum(build(new Integer[] {5, null, 6, null, 7}), 5) != 6) throw new AssertionError("right chain");
        Random rnd = new Random(16401);
        int checked = 0;
        for (int t = 0; t < 5000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Node> nodes = new ArrayList<>();
            allNodes(root, nodes);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            for (Node n : nodes) {
                if (n.right == null) continue;
                List<Integer> side = new ArrayList<>();
                gather(n.right, side);
                int want = Collections.min(side);
                if (rightMinimum(root, n.val) != want) throw new AssertionError("differs at key " + n.val);
                if (sorted.get(sorted.indexOf(n.val) + 1) != want) throw new AssertionError("not the next sorted key at " + n.val);
                checked++;
            }
        }
        if (checked < 3000) throw new AssertionError("too few checks: " + checked);
    }
}
```

#### Solution: [Vary] Successor Without Parent Links (Author exercise)
<!-- id: tb-successor-no-parents -->

**Approach.** Walk from the root and keep a candidate. At a node higher than the target, save its key and go left, and at any other node go right. No search for the target's own node is needed, so the target may even be absent. The oracle writes all keys into a sorted list and returns the first one above the target. The assertions compare the two on random trees with targets inside and outside the key range, and check that an empty tree answers null.

**Complexity.** O(h) time and O(1) extra space.

```java run
import java.util.*;

public final class SuccessorWalkRun {
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
    static Integer successor(Node root, int target) {
        Integer best = null;
        Node node = root;
        while (node != null) {
            if (node.val > target) { best = node.val; node = node.left; }
            else node = node.right;
        }
        return best;
    }

    public static void main(String[] args) {
        Node sample = build(new Integer[] {5, 3, 6, 2, 4});
        if (successor(sample, 4) != 5) throw new AssertionError("example 1");
        if (successor(sample, 6) != null) throw new AssertionError("example 2");
        if (successor(null, 1) != null) throw new AssertionError("empty tree");
        if (successor(sample, 1) != 2) throw new AssertionError("absent target below every key");
        Random rnd = new Random(16402);
        for (int t = 0; t < 8000; t++) {
            Node root = randomBst(rnd, 18, 50);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            int target = rnd.nextInt(56) - 3;
            Integer want = null;
            for (int k : sorted) if (k > target) { want = k; break; }
            Integer got = successor(root, target);
            if (!Objects.equals(got, want)) throw new AssertionError("differs for target " + target + " on " + sorted);
        }
    }
}
```

#### Solution: [Boundary] Maximum And Minimum Keys (Author exercise)
<!-- id: tb-extreme-keys -->

**Approach.** Run the mirrored pair of walks, one saving a node whenever it is higher than the key and going left, the other saving a node whenever it is lower and going right. Each result starts as null and is never replaced by a sentinel number, so the largest key reports no successor and the smallest reports no predecessor. The oracle uses the sorted list and the position of the key in it. The assertions check every key of every random tree, including trees of one node, and demonstrate that unboxing a null `Integer` into an `int` throws a `NullPointerException`, the hazard that returning `Integer` avoids.

**Complexity.** O(h) time and O(1) extra space per query.

```java run
import java.util.*;

public final class NeighboursRun {
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
    static String neighbours(Node root, int key) {
        Integer below = null, above = null;
        Node node = root;
        while (node != null) {
            if (node.val > key) { above = node.val; node = node.left; }
            else node = node.right;
        }
        node = root;
        while (node != null) {
            if (node.val < key) { below = node.val; node = node.right; }
            else node = node.left;
        }
        return "[" + below + ", " + above + "]";
    }

    public static void main(String[] args) {
        if (!neighbours(build(new Integer[] {7}), 7).equals("[null, null]")) throw new AssertionError("example 1");
        if (!neighbours(build(new Integer[] {2, 1, 3}), 3).equals("[2, null]")) throw new AssertionError("example 2");
        if (!neighbours(build(new Integer[] {2, 1, 3}), 1).equals("[null, 2]")) throw new AssertionError("minimum key");
        boolean threw = false;
        try { Integer none = null; int unboxed = none; if (unboxed == 0) threw = false; } catch (NullPointerException expected) { threw = true; }
        if (!threw) throw new AssertionError("unboxing null should throw");
        Random rnd = new Random(16403);
        int extremes = 0;
        for (int t = 0; t < 5000; t++) {
            Node root = randomBst(rnd, 16, 40);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            for (int i = 0; i < sorted.size(); i++) {
                String want = "[" + (i == 0 ? null : sorted.get(i - 1)) + ", " + (i == sorted.size() - 1 ? null : sorted.get(i + 1)) + "]";
                if (!neighbours(root, sorted.get(i)).equals(want)) throw new AssertionError("differs at " + sorted.get(i) + " in " + sorted);
                if (i == 0 || i == sorted.size() - 1) extremes++;
            }
        }
        if (extremes < 2000) throw new AssertionError("too few extreme keys tested: " + extremes);
    }
}
```

#### Solution: [Recognize] Inorder Successor in BST (LeetCode 285)
<!-- id: tb-inorder-successor -->

**Approach.** Walk to the node by comparisons while remembering the last bell where the walk turned left. If the node has a right side, the answer is the leftmost key of that side, which is the inside case. Otherwise the remembered ancestor is the answer, or null if the walk never turned left. The oracle is the sorted list, and the assertions also compare this two-case method with the single-candidate walk of the previous rung on every node of every random tree. Both examples are checked, together with the largest key.

**Complexity.** O(h) time and O(1) extra space.

```java run
import java.util.*;

public final class InorderSuccessorRun {
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
    static Integer successorTwoCases(Node root, int p) {
        Node node = root;
        Integer lastLeftTurn = null;
        while (node.val != p) {
            if (p < node.val) { lastLeftTurn = node.val; node = node.left; }
            else node = node.right;
        }
        if (node.right == null) return lastLeftTurn;
        Node low = node.right;
        while (low.left != null) low = low.left;
        return low.val;
    }

    static Integer candidateWalk(Node root, int target) {
        Integer best = null;
        for (Node node = root; node != null; ) {
            if (node.val > target) { best = node.val; node = node.left; }
            else node = node.right;
        }
        return best;
    }

    public static void main(String[] args) {
        Integer[] sample = {20, 9, 25, 5, 12, null, null, null, null, 11, 14};
        if (successorTwoCases(build(sample), 12) != 14) throw new AssertionError("example 1");
        if (successorTwoCases(build(sample), 14) != 20) throw new AssertionError("example 2");
        if (successorTwoCases(build(sample), 25) != null) throw new AssertionError("largest key");
        if (successorTwoCases(build(new Integer[] {5, 3, 6, 2, 4, null, null, 1}), 6) != null) throw new AssertionError("right child leaf at the top");
        Random rnd = new Random(16404);
        for (int t = 0; t < 6000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            for (int i = 0; i < sorted.size(); i++) {
                Integer want = i + 1 < sorted.size() ? sorted.get(i + 1) : null;
                Integer got = successorTwoCases(root, sorted.get(i));
                if (!Objects.equals(got, want)) throw new AssertionError("two cases differ at " + sorted.get(i) + " in " + sorted);
                if (!Objects.equals(candidateWalk(root, sorted.get(i)), want)) throw new AssertionError("candidate walk differs at " + sorted.get(i));
            }
        }
    }
}
```
