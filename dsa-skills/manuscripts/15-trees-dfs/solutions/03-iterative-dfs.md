<!-- solutions-for: 03-iterative-dfs -->
### Iterative DFS

#### Solution: [Build] Iterative Preorder (Author exercise)
<!-- id: tr-iter-preorder -->

**Approach.** Keep an `ArrayDeque` of nodes that starts with the root when there is one. Each round pops the top, appends its value, and pushes the right child and then the left child when they exist, so the left child sits on top. After the pushes of a round, compare the stack size with the best so far, which also covers the first size of one for the initial root. The result array stores that peak first and the values after it. The assertions compare the values with a recursive preorder on random trees, check that the peak never exceeds the height plus one, and show that pushing left before right produces a right-first order.

**Complexity.** O(n) time, and O(h) stack entries, with h at most n.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class IterativePreorder {
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
        boolean fillLeft = true;
        for (int i = 1; i < v.length; i++) {
            Node parent = parents.peek();
            Node child = v[i] == null ? null : new Node(v[i]);
            if (child != null) parents.add(child);
            if (fillLeft) { parent.left = child; fillLeft = false; }
            else { parent.right = child; fillLeft = true; parents.poll(); }
        }
        return root;
    }

    static List<Integer> walk(Node root) {
        List<Integer> out = new ArrayList<>();
        out.add(0);
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        int peak = stack.size();
        while (!stack.isEmpty()) {
            Node node = stack.pop();
            out.add(node.val);
            if (node.right != null) stack.push(node.right);
            if (node.left != null) stack.push(node.left);
            peak = Math.max(peak, stack.size());
        }
        out.set(0, peak);
        return out;
    }

    static void recursive(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        recursive(n.left, out);
        recursive(n.right, out);
    }

    static int height(Node n) { return n == null ? 0 : 1 + Math.max(height(n.left), height(n.right)); }

    static List<Integer> wrongOrder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {
            Node node = stack.pop();
            out.add(node.val);
            if (node.left != null) stack.push(node.left);
            if (node.right != null) stack.push(node.right);
        }
        return out;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(13);
        List<Integer> out = new ArrayList<>();
        int made = 1, queued = 1;
        out.add(rnd.nextInt(2001) - 1000);
        for (int q = 0; q < queued; q++) {
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(rnd.nextInt(2001) - 1000); made++; queued++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!walk(build(new Integer[] {1, 2, 3, 4})).equals(List.of(2, 1, 2, 4, 3))) throw new AssertionError("example 1");
        if (!walk(build(new Integer[] {})).equals(List.of(0))) throw new AssertionError("example 2");
        if (!wrongOrder(build(new Integer[] {1, 2, 3})).equals(List.of(1, 3, 2))) throw new AssertionError("left pushed first visits the right side first");
        Random rnd = new Random(15301);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            List<Integer> got = walk(root);
            List<Integer> want = new ArrayList<>();
            recursive(root, want);
            if (!got.subList(1, got.size()).equals(want)) throw new AssertionError("values differ on " + Arrays.toString(v));
            if (got.get(0) < 1 || got.get(0) > height(root) + 1) throw new AssertionError("peak out of range on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Iterative Inorder (Author exercise)
<!-- id: tr-iter-inorder -->

**Approach.** Use a cursor and a stack. While the cursor is a node, push it and move to its left child, which walks down the left spine. When the cursor becomes null, pop a node, append its value, and set the cursor to that node's right child, so the same descent starts on the right side. The loop ends when the cursor is null and the stack is empty. No null is ever pushed, which matters because `ArrayDeque` rejects it. The assertions compare with a recursive inorder on random trees and check the null rejection directly.

**Complexity.** O(n) time, because each node is pushed and popped once, and O(h) space for the stack.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class IterativeInorder {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node[] seats = new Node[v.length];
        seats[0] = new Node(v[0]);
        int read = 1;
        for (int at = 0; at < v.length && read < v.length; at++) {
            if (seats[at] == null) continue;
            if (v[read] != null) seats[at].left = seats[read] = new Node(v[read]);
            read++;
            if (read < v.length) {
                if (v[read] != null) seats[at].right = seats[read] = new Node(v[read]);
                read++;
            }
        }
        return seats[0];
    }

    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) { stack.push(cur); cur = cur.left; }
            cur = stack.pop();
            out.add(cur.val);
            cur = cur.right;
        }
        return out;
    }

    static void recursive(Node n, List<Integer> out) {
        if (n == null) return;
        recursive(n.left, out);
        out.add(n.val);
        recursive(n.right, out);
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1;
        int pending = 1;
        out.add(rnd.nextInt(2001) - 1000);
        while (pending > 0) {
            pending--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(2001) - 1000); made++; pending++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!inorder(build(new Integer[] {4, 2, 7, 1, 3})).equals(List.of(1, 2, 3, 4, 7))) throw new AssertionError("example 1");
        if (!inorder(build(new Integer[] {3, null, 5, 4})).equals(List.of(3, 4, 5))) throw new AssertionError("example 2");
        if (!inorder(null).isEmpty()) throw new AssertionError("null root");
        boolean rejected = false;
        try { new ArrayDeque<Integer>().push(null); } catch (NullPointerException e) { rejected = true; }
        if (!rejected) throw new AssertionError("ArrayDeque rejects null elements");
        Random rnd = new Random(15302);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            List<Integer> want = new ArrayList<>();
            recursive(root, want);
            if (!inorder(root).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Deep Skewed Tree (Author exercise)
<!-- id: tr-deep-skewed -->

**Approach.** Build the chain by linking each new node under the previous one on the requested side, and run the cursor-and-stack inorder walk that never recurses. A null root skips both loops and gives size 0 with the two markers set to -1. For a long chain the walk records the first and last value it appends and counts the size, which avoids holding a huge output list. The assertions compare with a formula for large chains, where a left chain visits n first and 1 last and a right chain the reverse, and with a recursive oracle for small ones. They also run a recursive walk on a chain in a thread with a small call stack to show that it overflows.

**Complexity.** O(n) time, and O(n) heap space on a left chain, where the stack holds every node.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class DeepSkewedTree {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node chain(int n, boolean leftSide) {
        if (n == 0) return null;
        Node root = new Node(1), tail = root;
        for (int v = 2; v <= n; v++) {
            Node next = new Node(v);
            if (leftSide) tail.left = next; else tail.right = next;
            tail = next;
        }
        return root;
    }

    static long[] summary(Node root) {
        long size = 0, first = -1, last = -1;
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) { stack.push(cur); cur = cur.left; }
            cur = stack.pop();
            if (size == 0) first = cur.val;
            last = cur.val;
            size++;
            cur = cur.right;
        }
        return new long[] {size, first, last};
    }

    static void recursive(Node n, List<Integer> out) {
        if (n == null) return;
        recursive(n.left, out);
        out.add(n.val);
        recursive(n.right, out);
    }

    static boolean overflows(Node root) throws InterruptedException {
        boolean[] hit = {false};
        Thread t = new Thread(null, () -> {
            try { recursive(root, new ArrayList<>()); }
            catch (StackOverflowError e) { hit[0] = true; }
        }, "small-stack", 128 * 1024);
        t.start();
        t.join();
        return hit[0];
    }

    public static void main(String[] args) throws Exception {
        if (!Arrays.equals(summary(chain(0, true)), new long[] {0, -1, -1})) throw new AssertionError("example 1");
        if (!Arrays.equals(summary(chain(3, true)), new long[] {3, 3, 1})) throw new AssertionError("example 2");
        if (!Arrays.equals(summary(chain(3, false)), new long[] {3, 1, 3})) throw new AssertionError("right chain of three");
        int big = 300000;
        if (!Arrays.equals(summary(chain(big, true)), new long[] {big, big, 1})) throw new AssertionError("left chain of " + big);
        if (!Arrays.equals(summary(chain(big, false)), new long[] {big, 1, big})) throw new AssertionError("right chain of " + big);
        Random rnd = new Random(15303);
        for (int t = 0; t < 300; t++) {
            int n = rnd.nextInt(40);
            boolean side = rnd.nextBoolean();
            List<Integer> want = new ArrayList<>();
            recursive(chain(n, side), want);
            long[] got = summary(chain(n, side));
            if (got[0] != want.size()) throw new AssertionError("size differs at n = " + n);
            if (n > 0 && (got[1] != want.get(0) || got[2] != want.get(n - 1))) throw new AssertionError("ends differ at n = " + n);
        }
        if (!overflows(chain(200000, true))) throw new AssertionError("recursion on a long chain overflows a small stack");
    }
}
```

#### Solution: [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: tr-iter-postorder-mirror -->

**Approach.** Give every stack entry a state. The first time a node reaches the top it has not been expanded, so replace it by an expanded copy and push its left child and then its right child, which leaves the right child on top and so makes the right side finish first. When an expanded entry reaches the top, both sides are finished, so pop it and append its value. The result is the right subtree, the left subtree, and then the node. The assertions compare the state-machine walk with two independent constructions: a recursive mirrored postorder, and the ordinary preorder written backwards.

**Complexity.** O(n) time because each node enters the stack twice, and O(h) stack space.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class MirroredPostorder {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        List<Node> order = new ArrayList<>();
        Node root = new Node(v[0]);
        order.add(root);
        int next = 1;
        for (int p = 0; p < order.size() && next < v.length; p++) {
            Node parent = order.get(p);
            Integer lv = v[next++];
            if (lv != null) { parent.left = new Node(lv); order.add(parent.left); }
            if (next < v.length) {
                Integer rv = v[next++];
                if (rv != null) { parent.right = new Node(rv); order.add(parent.right); }
            }
        }
        return root;
    }

    static List<Integer> mirrored(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> nodes = new ArrayDeque<>();
        Deque<Boolean> expanded = new ArrayDeque<>();
        if (root != null) { nodes.push(root); expanded.push(false); }
        while (!nodes.isEmpty()) {
            Node top = nodes.pop();
            boolean done = expanded.pop();
            if (done) { out.add(top.val); continue; }
            nodes.push(top); expanded.push(true);
            if (top.left != null) { nodes.push(top.left); expanded.push(false); }
            if (top.right != null) { nodes.push(top.right); expanded.push(false); }
        }
        return out;
    }

    static void rightFirst(Node n, List<Integer> out) {
        if (n == null) return;
        rightFirst(n.right, out);
        rightFirst(n.left, out);
        out.add(n.val);
    }

    static void plainPreorder(Node n, List<Integer> out) {
        if (n == null) return;
        out.add(n.val);
        plainPreorder(n.left, out);
        plainPreorder(n.right, out);
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(13);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(2001) - 1000);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(rnd.nextInt(2001) - 1000); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!mirrored(build(new Integer[] {5, 3, 8, 1})).equals(List.of(8, 1, 3, 5))) throw new AssertionError("example 1");
        if (!mirrored(build(new Integer[] {2, null, 7, 6})).equals(List.of(6, 7, 2))) throw new AssertionError("example 2");
        if (!mirrored(null).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(15304);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            Node root = build(v);
            List<Integer> got = mirrored(root);
            List<Integer> a = new ArrayList<>();
            rightFirst(root, a);
            List<Integer> b = new ArrayList<>();
            plainPreorder(root, b);
            Collections.reverse(b);
            if (!got.equals(a)) throw new AssertionError("differs from the recursive version on " + Arrays.toString(v));
            if (!got.equals(b)) throw new AssertionError("differs from reversed preorder on " + Arrays.toString(v));
        }
    }
}
```
