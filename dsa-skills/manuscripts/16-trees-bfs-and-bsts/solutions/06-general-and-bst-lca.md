<!-- solutions-for: 06-general-and-bst-lca -->
### General And BST LCA

#### Solution: [Build] General-Tree Ancestor Return (Author exercise)
<!-- id: tb-meeting-junction -->

**Approach.** Each call returns the camper found in its branch, or null. The depth is passed down as an argument, and when both branches return a camper the junction records its own label and depth, which can be read straight away. Because neither label is an ancestor of the other, the first such junction is the answer, and every junction above it receives a single report. The oracle walks parent links instead: it marks the chain from `p` to the root and climbs from `q` until it meets that chain, and then counts the climb back to the root. The assertions try every pair of labels on random trees, keeping only the pairs whose answer is neither label, which is the exercise guarantee.

**Complexity.** O(n) time and O(h) recursion.

```java run
import java.util.*;

public final class MeetingJunctionRun {
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
    static Integer[] relabel(Integer[] shape) {
        Integer[] out = shape.clone();
        int next = 0;
        for (int i = 0; i < out.length; i++) if (out[i] != null) out[i] = next++;
        return out;
    }

    static int countNodes(Integer[] v) {
        int c = 0;
        for (Integer x : v) if (x != null) c++;
        return c;
    }
    static Node find(Node n, int val) {
        if (n == null) return null;
        if (n.val == val) return n;
        Node inLeft = find(n.left, val);
        return inLeft != null ? inLeft : find(n.right, val);
    }

    static Node viaParents(Node root, int p, int q) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        Set<Node> above = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node a = find(root, p); a != null; a = parent.get(a)) above.add(a);
        Node a = find(root, q);
        while (!above.contains(a)) a = parent.get(a);
        return a;
    }
    static int[] found;

    static Node meeting(Node node, int p, int q, int depth) {
        if (node == null) return null;
        if (node.val == p || node.val == q) return node;
        Node left = meeting(node.left, p, q, depth + 1);
        Node right = meeting(node.right, p, q, depth + 1);
        if (left != null && right != null) { found = new int[] {node.val, depth}; return node; }
        return left != null ? left : right;
    }

    static String answer(Node root, int p, int q) {
        found = null;
        meeting(root, p, q, 0);
        return Arrays.toString(found);
    }

    static int depthOfNode(Node root, Node target) {
        if (root == target) return 0;
        for (Node child : new Node[] {root.left, root.right}) {
            if (child == null) continue;
            int d = depthOfNode(child, target);
            if (d >= 0) return d + 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        Node sample = build(new Integer[] {1, 2, 3, 4, 5, 6, 7, null, null, 8, 9});
        if (!answer(sample, 8, 7).equals("[1, 0]")) throw new AssertionError("example 1");
        if (!answer(sample, 8, 9).equals("[5, 2]")) throw new AssertionError("example 2");
        Random rnd = new Random(16601);
        int pairs = 0;
        for (int t = 0; t < 2500; t++) {
            Integer[] v = relabel(randomLevels(rnd, 14, 0, 0));
            Node root = build(v);
            int n = countNodes(v);
            for (int p = 0; p < n; p++) {
                for (int q = p + 1; q < n; q++) {
                    Node lca = viaParents(root, p, q);
                    if (lca.val == p || lca.val == q) continue;
                    String want = "[" + lca.val + ", " + depthOfNode(root, lca) + "]";
                    if (!answer(root, p, q).equals(want)) throw new AssertionError("differs for " + p + "," + q + " on " + Arrays.toString(v));
                    pairs++;
                }
            }
        }
        if (pairs < 5000) throw new AssertionError("too few pairs: " + pairs);
    }
}
```

#### Solution: [Vary] Lowest Common Ancestor of a Binary Tree (LeetCode 236)
<!-- id: tb-lca-binary-tree -->

**Approach.** A call that meets either label returns its own node at once. Otherwise it asks both sides and returns itself when both answer, or the one non-null answer. When one label lies below the other, the upper label is returned before the search can descend, which is correct because the lower label is guaranteed to exist. The oracle is the parent-chain method used in the previous rung. The assertions try every ordered pair of distinct labels on random trees, including pairs where one label is above the other, and compare node identity.

**Complexity.** O(n) time and O(h) recursion.

```java run
import java.util.*;

public final class LcaBinaryTreeRun {
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
    static Integer[] relabel(Integer[] shape) {
        Integer[] out = shape.clone();
        int next = 0;
        for (int i = 0; i < out.length; i++) if (out[i] != null) out[i] = next++;
        return out;
    }

    static int countNodes(Integer[] v) {
        int c = 0;
        for (Integer x : v) if (x != null) c++;
        return c;
    }
    static Node find(Node n, int val) {
        if (n == null) return null;
        if (n.val == val) return n;
        Node inLeft = find(n.left, val);
        return inLeft != null ? inLeft : find(n.right, val);
    }

    static Node viaParents(Node root, int p, int q) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        Set<Node> above = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node a = find(root, p); a != null; a = parent.get(a)) above.add(a);
        Node a = find(root, q);
        while (!above.contains(a)) a = parent.get(a);
        return a;
    }
    static Node lca(Node node, Node p, Node q) {
        if (node == null || node == p || node == q) return node;
        Node left = lca(node.left, p, q);
        Node right = lca(node.right, p, q);
        if (left != null && right != null) return node;
        return left != null ? left : right;
    }

    public static void main(String[] args) {
        Node sample = build(new Integer[] {1, 2, 3, 4, 5, 6, 7, null, null, 8, 9});
        if (lca(sample, find(sample, 4), find(sample, 9)).val != 2) throw new AssertionError("example 1");
        if (lca(sample, find(sample, 2), find(sample, 9)).val != 2) throw new AssertionError("example 2");
        Random rnd = new Random(16602);
        int ancestorPairs = 0;
        for (int t = 0; t < 2500; t++) {
            Integer[] v = relabel(randomLevels(rnd, 14, 0, 0));
            if (v.length < 2 || countNodes(v) < 2) continue;
            Node root = build(v);
            int n = countNodes(v);
            for (int p = 0; p < n; p++) {
                for (int q = 0; q < n; q++) {
                    if (p == q) continue;
                    Node got = lca(root, find(root, p), find(root, q));
                    Node want = viaParents(root, p, q);
                    if (got != want) throw new AssertionError("differs for " + p + "," + q + " on " + Arrays.toString(v));
                    if (want.val == p || want.val == q) ancestorPairs++;
                }
            }
        }
        if (ancestorPairs < 1000) throw new AssertionError("too few ancestor pairs: " + ancestorPairs);
    }
}
```

#### Solution: [Boundary] One Target Is Ancestor (Author exercise)
<!-- id: tb-target-is-ancestor -->

**Approach.** Equal labels are answered directly with distance zero. Otherwise one full pass counts the labels found in each subtree and records the depth of each label as it is met, and the first junction in postorder whose subtree holds both labels is the answer, with its depth recorded at that moment. The route length is the depth of `p` plus the depth of `q` minus twice the depth of the answer. Nothing returns early, so a label below the other is still seen. The oracle climbs parent links from both labels and counts the climbs. The assertions run all pairs, including equal labels and ancestor pairs, on random trees.

**Complexity.** O(n) time and O(h) recursion.

```java run
import java.util.*;

public final class AncestorDistanceRun {
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
    static Integer[] relabel(Integer[] shape) {
        Integer[] out = shape.clone();
        int next = 0;
        for (int i = 0; i < out.length; i++) if (out[i] != null) out[i] = next++;
        return out;
    }

    static int countNodes(Integer[] v) {
        int c = 0;
        for (Integer x : v) if (x != null) c++;
        return c;
    }
    static Node find(Node n, int val) {
        if (n == null) return null;
        if (n.val == val) return n;
        Node inLeft = find(n.left, val);
        return inLeft != null ? inLeft : find(n.right, val);
    }

    static Node viaParents(Node root, int p, int q) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        Set<Node> above = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node a = find(root, p); a != null; a = parent.get(a)) above.add(a);
        Node a = find(root, q);
        while (!above.contains(a)) a = parent.get(a);
        return a;
    }
    static int depthP, depthQ, depthAnswer, answerLabel;

    static int count(Node node, int p, int q, int depth) {
        if (node == null) return 0;
        if (node.val == p) depthP = depth;
        if (node.val == q) depthQ = depth;
        int here = (node.val == p ? 1 : 0) + (node.val == q ? 1 : 0);
        int total = count(node.left, p, q, depth + 1) + count(node.right, p, q, depth + 1) + here;
        if (total == 2 && answerLabel < 0) { answerLabel = node.val; depthAnswer = depth; }
        return total;
    }

    static String answer(Node root, int p, int q) {
        if (p == q) return "[" + p + ", 0]";
        answerLabel = -1;
        count(root, p, q, 0);
        return "[" + answerLabel + ", " + (depthP + depthQ - 2 * depthAnswer) + "]";
    }

    static int climbs(Node root, int from, int to) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        int steps = 0;
        for (Node a = find(root, from); a != find(root, to); a = parent.get(a)) steps++;
        return steps;
    }

    public static void main(String[] args) {
        Node sample = build(new Integer[] {1, 2, 3, 4, 5, 6, 7, null, null, 8, 9});
        if (!answer(sample, 2, 9).equals("[2, 2]")) throw new AssertionError("example 1");
        if (!answer(sample, 5, 5).equals("[5, 0]")) throw new AssertionError("example 2");
        if (!answer(sample, 9, 2).equals("[2, 2]")) throw new AssertionError("order of labels must not matter");
        Random rnd = new Random(16603);
        int ancestorCases = 0;
        for (int t = 0; t < 2500; t++) {
            Integer[] v = relabel(randomLevels(rnd, 14, 0, 0));
            Node root = build(v);
            int n = countNodes(v);
            for (int p = 0; p < n; p++) {
                for (int q = 0; q < n; q++) {
                    Node lca = viaParents(root, p, q);
                    String want = "[" + lca.val + ", " + (climbs(root, p, lca.val) + climbs(root, q, lca.val)) + "]";
                    if (!answer(root, p, q).equals(want)) throw new AssertionError("differs for " + p + "," + q + " on " + Arrays.toString(v));
                    if (p != q && (lca.val == p || lca.val == q)) ancestorCases++;
                }
            }
        }
        if (ancestorCases < 1000) throw new AssertionError("too few ancestor cases: " + ancestorCases);
    }
}
```

#### Solution: [Recognize] Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)
<!-- id: tb-lca-bst -->

**Approach.** Walk down from the root. While both keys are smaller than the current key go left, while both are larger go right, and stop at the first node that is neither, which is where the routes separate or where one key sits. No reports are collected, so the walk costs one path. The oracle is the parent-chain method, which does not use the ordering at all. The assertions try every pair of distinct keys on random search trees and also count the steps to show that the walk never takes more steps than the tree height. A short assertion shows that two boxed `Integer` objects holding 1000 are different objects, the reason the numbers are compared as `int` values.

**Complexity.** O(h) time and O(1) space.

```java run
import java.util.*;

public final class LcaBstRun {
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
    static Node find(Node n, int val) {
        if (n == null) return null;
        if (n.val == val) return n;
        Node inLeft = find(n.left, val);
        return inLeft != null ? inLeft : find(n.right, val);
    }

    static Node viaParents(Node root, int p, int q) {
        IdentityHashMap<Node, Node> parent = new IdentityHashMap<>();
        ArrayDeque<Node> todo = new ArrayDeque<>();
        todo.add(root);
        parent.put(root, null);
        while (!todo.isEmpty()) {
            Node n = todo.poll();
            for (Node c : new Node[] {n.left, n.right}) if (c != null) { parent.put(c, n); todo.add(c); }
        }
        Set<Node> above = Collections.newSetFromMap(new IdentityHashMap<>());
        for (Node a = find(root, p); a != null; a = parent.get(a)) above.add(a);
        Node a = find(root, q);
        while (!above.contains(a)) a = parent.get(a);
        return a;
    }
    static int steps;

    static Node splitPoint(Node root, int p, int q) {
        Node node = root;
        while (node != null) {
            steps++;
            if (p < node.val && q < node.val) node = node.left;
            else if (p > node.val && q > node.val) node = node.right;
            else return node;
        }
        return null;
    }

    static int height(Node n) {
        return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right));
    }

    public static void main(String[] args) {
        Integer[] sample = {20, 10, 30, 5, 15, 25, 35, null, null, 12, 18};
        if (splitPoint(build(sample), 12, 18).val != 15) throw new AssertionError("example 1");
        if (splitPoint(build(sample), 10, 12).val != 10) throw new AssertionError("example 2");
        Integer a = 1000, b = 1000;
        if (a == b) throw new AssertionError("boxed values above the cache are separate objects");
        if (!a.equals(b)) throw new AssertionError("equals should still hold");
        Random rnd = new Random(16604);
        for (int t = 0; t < 4000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Integer> keys = new ArrayList<>();
            inorderInto(root, keys);
            for (int i = 0; i < keys.size(); i++) {
                for (int j = i + 1; j < keys.size(); j++) {
                    steps = 0;
                    Node got = splitPoint(root, keys.get(i), keys.get(j));
                    if (got != viaParents(root, keys.get(i), keys.get(j))) throw new AssertionError("differs for " + keys.get(i) + "," + keys.get(j) + " in " + keys);
                    if (steps > height(root)) throw new AssertionError("more steps than the height");
                }
            }
        }
    }
}
```
