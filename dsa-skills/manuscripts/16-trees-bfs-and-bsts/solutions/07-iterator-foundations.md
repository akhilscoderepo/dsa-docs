<!-- solutions-for: 07-iterator-foundations -->
### Iterator Foundations

#### Solution: [Build] Push Left Spine (Author exercise)
<!-- id: tb-push-left-spine -->

**Approach.** Push the root, then follow left links and push every node passed, and read the stack from its top. The top is the last node pushed, which is the smallest key in the tree. The oracle builds the same list by recursion: the spine of a node is the spine of its left child followed by the node itself. The assertions compare the loop with that recursion on random search trees, check that the first key equals the minimum of a full inorder listing, and check that the listing is strictly increasing, since each node on the spine is the parent of the one before it.

**Complexity.** O(h) time and O(h) space.

```java run
import java.util.*;

public final class LeftSpineRun {
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
    static List<Integer> spineTopFirst(Node root) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        for (Node node = root; node != null; node = node.left) stack.push(node);
        List<Integer> out = new ArrayList<>();
        for (Node n : stack) out.add(n.val);
        return out;
    }

    static List<Integer> spineByRecursion(Node n) {
        if (n == null) return new ArrayList<>();
        List<Integer> below = spineByRecursion(n.left);
        below.add(n.val);
        return below;
    }

    public static void main(String[] args) {
        if (!spineTopFirst(build(new Integer[] {10, 5, 15, 3, 7, 12, 20, 2, null, 6})).toString().equals("[2, 3, 5, 10]")) throw new AssertionError("example 1");
        if (!spineTopFirst(build(new Integer[] {4, null, 6})).toString().equals("[4]")) throw new AssertionError("example 2");
        if (!spineTopFirst(null).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(16701);
        for (int t = 0; t < 6000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Integer> got = spineTopFirst(root);
            if (!got.equals(spineByRecursion(root))) throw new AssertionError("loop and recursion differ");
            if (root == null) continue;
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            if (!got.get(0).equals(sorted.get(0))) throw new AssertionError("top is not the minimum");
            for (int i = 1; i < got.size(); i++) if (got.get(i) <= got.get(i - 1)) throw new AssertionError("not increasing from the top");
        }
    }
}
```

#### Solution: [Vary] Advance One Inorder Step (Author exercise)
<!-- id: tb-advance-one-step -->

**Approach.** Repeat m times: pop the top, push the left spine of its right child, and remember the popped key. Then report that key and the stack from its top. The oracle never touches a stack. The popped key must be entry m of the sorted listing, and the stack must hold the next key plus every ancestor of it that is larger, which the oracle finds by searching down from the root and keeping the path keys that are at least the next key, in increasing order. The assertions check every m from 1 to n on random search trees.

**Complexity.** O(h + m) time, because each node is pushed and popped at most once, and O(h) space.

```java run
import java.util.*;

public final class AdvanceStepRun {
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
    static List<Integer> advance(Node root, int m) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        for (Node node = root; node != null; node = node.left) stack.push(node);
        int popped = -1;
        for (int step = 0; step < m; step++) {
            Node top = stack.pop();
            popped = top.val;
            for (Node node = top.right; node != null; node = node.left) stack.push(node);
        }
        List<Integer> out = new ArrayList<>();
        out.add(popped);
        for (Node n : stack) out.add(n.val);
        return out;
    }

    static List<Integer> oracle(Node root, int m) {
        List<Integer> sorted = new ArrayList<>();
        inorderInto(root, sorted);
        List<Integer> out = new ArrayList<>();
        out.add(sorted.get(m - 1));
        if (m == sorted.size()) return out;
        int next = sorted.get(m);
        List<Integer> path = new ArrayList<>();
        for (Node at = root; ; at = next < at.val ? at.left : at.right) {
            if (at.val >= next) path.add(at.val);
            if (at.val == next) break;
        }
        Collections.sort(path);
        out.addAll(path);
        return out;
    }

    public static void main(String[] args) {
        if (!advance(build(new Integer[] {10, 5, 15, 3, 7, 12, 20, 2, null, 6}), 3).toString().equals("[5, 6, 7, 10]")) throw new AssertionError("example 1");
        if (!advance(build(new Integer[] {4, null, 6}), 1).toString().equals("[4, 6]")) throw new AssertionError("example 2");
        Random rnd = new Random(16702);
        for (int t = 0; t < 4000; t++) {
            Node root = randomBst(rnd, 18, 60);
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            for (int m = 1; m <= sorted.size(); m++) {
                Node fresh = build(levels(root));
                if (!advance(fresh, m).equals(oracle(root, m))) throw new AssertionError("m=" + m + " differs on " + sorted);
            }
        }
    }
}
```

#### Solution: [Boundary] Empty Iterator And Right Chain (Author exercise)
<!-- id: tb-empty-and-right-chain -->

**Approach.** Define `hasNext` as a non-empty stack, and make `next` check that condition before popping, answering `none` when it fails. The empty tree is the case where the stack is empty from the start, and a right-leaning chain keeps one node on the stack throughout. The oracle replays the operations against a sorted list and a position counter. The assertions also show that popping an empty `ArrayDeque` throws `NoSuchElementException`, which is why the guard is needed, and run random operation lists on random trees, including empty ones and chains.

**Complexity.** O(h) space, and O(n + q) total time for n nodes and q operations.

```java run
import java.util.*;

public final class EmptyIteratorRun {
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
    static List<String> run(Node root, String[] ops) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        for (Node node = root; node != null; node = node.left) stack.push(node);
        List<String> out = new ArrayList<>();
        for (String op : ops) {
            if (op.equals("hasNext")) { out.add(String.valueOf(!stack.isEmpty())); continue; }
            if (stack.isEmpty()) { out.add("none"); continue; }
            Node top = stack.pop();
            for (Node node = top.right; node != null; node = node.left) stack.push(node);
            out.add(String.valueOf(top.val));
        }
        return out;
    }

    static List<String> oracle(Node root, String[] ops) {
        List<Integer> sorted = new ArrayList<>();
        inorderInto(root, sorted);
        int place = 0;
        List<String> out = new ArrayList<>();
        for (String op : ops) {
            if (op.equals("hasNext")) out.add(String.valueOf(place < sorted.size()));
            else out.add(place < sorted.size() ? String.valueOf(sorted.get(place++)) : "none");
        }
        return out;
    }

    public static void main(String[] args) {
        if (!run(null, new String[] {"hasNext", "next"}).toString().equals("[false, none]")) throw new AssertionError("example 1");
        if (!run(build(new Integer[] {1, null, 2, null, 3}), new String[] {"next", "next", "hasNext", "next", "hasNext"}).toString().equals("[1, 2, true, 3, false]")) throw new AssertionError("example 2");
        boolean threw = false;
        try { new ArrayDeque<Node>().pop(); } catch (NoSuchElementException expected) { threw = true; }
        if (!threw) throw new AssertionError("popping an empty ArrayDeque should throw");
        Random rnd = new Random(16703);
        for (int t = 0; t < 5000; t++) {
            Node root = t % 7 == 0 ? null : randomBst(rnd, 14, 50);
            String[] ops = new String[1 + rnd.nextInt(30)];
            for (int i = 0; i < ops.length; i++) ops[i] = rnd.nextBoolean() ? "next" : "hasNext";
            if (!run(root, ops).equals(oracle(root, ops))) throw new AssertionError("differs on " + Arrays.toString(ops));
        }
        Node chain = null;
        for (int k = 30; k >= 1; k--) { Node n = new Node(k); n.right = chain; chain = n; }
        String[] many = new String[40];
        Arrays.fill(many, "next");
        List<String> got = run(chain, many);
        if (!got.get(29).equals("30") || !got.get(30).equals("none")) throw new AssertionError("chain should end after 30 keys");
    }
}
```

#### Solution: [Recognize] Binary Search Tree Iterator (LeetCode 173)
<!-- id: tb-bst-iterator -->

**Approach.** The class keeps one stack holding a left spine. The constructor pushes the spine of the root, `hasNext` tests that the stack is non-empty, and `next` pops, pushes the spine of the popped node's right child, and returns the key. Counters record every push and the largest stack size. The oracle is the flattened sorted list with an index, which is the plan the lesson rejected, used here only to check answers. The assertions replay random operation strings, check that the stack never exceeds the height, and that a complete reading pushes each node exactly once, which is the amortised argument in numbers.

**Complexity.** O(h) space, O(1) amortised per call, and O(h) for a single call in the worst case.

```java run
import java.util.*;

public final class BstIteratorRun {
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
    static final class Reader {
        private final ArrayDeque<Node> stack = new ArrayDeque<>();
        int pushes, deepest;

        Reader(Node root) { pushLeft(root); }

        private void pushLeft(Node node) {
            while (node != null) {
                stack.push(node);
                pushes++;
                node = node.left;
            }
            deepest = Math.max(deepest, stack.size());
        }

        boolean hasNext() { return !stack.isEmpty(); }

        int next() {
            Node top = stack.pop();
            pushLeft(top.right);
            return top.val;
        }
    }

    static String replay(Reader r, String ops) {
        List<Object> out = new ArrayList<>();
        for (char c : ops.toCharArray()) out.add(c == 'N' ? (Object) r.next() : (Object) r.hasNext());
        return out.toString();
    }

    static int height(Node n) {
        return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right));
    }

    public static void main(String[] args) {
        if (!replay(new Reader(build(new Integer[] {6, 2, 9, 1, 4, 8, 11})), "NNHNNNNH").equals("[1, 2, true, 4, 6, 8, 9, true]")) throw new AssertionError("example 1");
        if (!replay(new Reader(build(new Integer[] {5})), "NH").equals("[5, false]")) throw new AssertionError("example 2");
        Random rnd = new Random(16704);
        for (int t = 0; t < 5000; t++) {
            Node root = randomBst(rnd, 20, 70);
            if (root == null) continue;
            List<Integer> sorted = new ArrayList<>();
            inorderInto(root, sorted);
            StringBuilder ops = new StringBuilder();
            int taken = 0, length = 1 + rnd.nextInt(40);
            for (int i = 0; i < length; i++) {
                if (taken < sorted.size() && rnd.nextBoolean()) { ops.append('N'); taken++; } else ops.append('H');
            }
            List<Object> want = new ArrayList<>();
            int place = 0;
            for (char c : ops.toString().toCharArray()) want.add(c == 'N' ? (Object) sorted.get(place++) : (Object) (place < sorted.size()));
            Reader r = new Reader(root);
            if (!replay(r, ops.toString()).equals(want.toString())) throw new AssertionError("differs on " + ops);
            if (r.deepest > height(root)) throw new AssertionError("stack deeper than the tree");
            Reader whole = new Reader(root);
            while (whole.hasNext()) whole.next();
            if (whole.pushes != sorted.size()) throw new AssertionError("each node should be pushed exactly once");
        }
    }
}
```
