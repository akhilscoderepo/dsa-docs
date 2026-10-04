<!-- solutions-for: 10-tree-and-bfs -->
### Tree And BFS

#### Solution: [Build] Level Order As Count And Sum (LeetCode 102)
<!-- id: tc-level-count-sum -->

**Approach.** Read the queue length once per wave and, during exactly that many removals, add each value to a `long` running total while queueing the children. The pair of the snapshot and the total is then written for the wave, and no per-wave list is ever built. The oracle never uses a queue. It walks the tree recursively and adds each node to the count and total kept at its depth. The assertions check both examples, negative values, a long chain, and thousands of random trees with signed values.

**Complexity.** O(n) time and O(w) queue space for a widest wave w.

```java run
import java.util.*;

public final class CountAndSumRun {
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
    static String waves(Node root) {
        StringBuilder out = new StringBuilder("[");
        if (root != null) {
            ArrayDeque<Node> queue = new ArrayDeque<>();
            queue.add(root);
            while (!queue.isEmpty()) {
                int size = queue.size();
                long sum = 0;
                for (int k = 0; k < size; k++) {
                    Node n = queue.poll();
                    sum += n.val;
                    if (n.left != null) queue.add(n.left);
                    if (n.right != null) queue.add(n.right);
                }
                if (out.length() > 1) out.append(", ");
                out.append('[').append(size).append(", ").append(sum).append(']');
            }
        }
        return out.append(']').toString();
    }

    static void tally(Node n, int depth, List<long[]> by) {
        if (n == null) return;
        if (by.size() == depth) by.add(new long[2]);
        by.get(depth)[0]++;
        by.get(depth)[1] += n.val;
        tally(n.left, depth + 1, by);
        tally(n.right, depth + 1, by);
    }

    static String oracle(Node root) {
        List<long[]> by = new ArrayList<>();
        tally(root, 0, by);
        StringBuilder out = new StringBuilder("[");
        for (long[] p : by) {
            if (out.length() > 1) out.append(", ");
            out.append('[').append(p[0]).append(", ").append(p[1]).append(']');
        }
        return out.append(']').toString();
    }

    public static void main(String[] args) {
        if (!waves(build(new Integer[] {3, 9, 20, null, null, 15, 7})).equals("[[1, 3], [2, 29], [2, 22]]")) throw new AssertionError("example 1");
        if (!waves(build(new Integer[] {1, -5, null, 2, null, -3})).equals("[[1, 1], [1, -5], [1, 2], [1, -3]]")) throw new AssertionError("example 2");
        if (!waves(null).equals("[]")) throw new AssertionError("empty tree");
        Node chain = new Node(1000), tail = chain;
        for (int i = 1; i < 50000; i++) { tail.right = new Node(1000); tail = tail.right; }
        String big = waves(chain);
        if (!big.startsWith("[[1, 1000], [1, 1000]") || !big.endsWith("[1, 1000]]")) throw new AssertionError("long chain");
        Random rnd = new Random(161001);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 22, -1000, 1000);
            if (!waves(build(v)).equals(oracle(build(v)))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Zigzag In Blocks Of K (LeetCode 103)
<!-- id: tc-zigzag-every-kth -->

**Approach.** The queue is filled left child first, always. Each wave decides its own direction from the test `depth % k == k - 1`, and a reversed wave puts each removed value at the front of its list while a normal wave puts it at the back. The oracle groups values by depth with a recursive walk and then reverses the groups whose depth satisfies the same test. A third check compares k = 2 with the classic zigzag, in which every odd-numbered wave is reversed.

**Complexity.** O(n) time and O(w) extra space.

```java run
import java.util.*;

public final class ZigzagBlocksRun {
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
    static List<List<Integer>> reverseEveryKth(Node root, int k) {
        List<List<Integer>> waves = new ArrayList<>();
        if (root == null) return waves;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        for (int depth = 0; !queue.isEmpty(); depth++) {
            int size = queue.size();
            LinkedList<Integer> wave = new LinkedList<>();
            boolean reversed = depth % k == k - 1;
            for (int i = 0; i < size; i++) {
                Node n = queue.poll();
                if (reversed) wave.addFirst(n.val); else wave.addLast(n.val);
                if (n.left != null) queue.add(n.left);
                if (n.right != null) queue.add(n.right);
            }
            waves.add(wave);
        }
        return waves;
    }

    static void byDepth(Node n, int depth, List<List<Integer>> out) {
        if (n == null) return;
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(n.val);
        byDepth(n.left, depth + 1, out);
        byDepth(n.right, depth + 1, out);
    }

    public static void main(String[] args) {
        Node nine = build(new Integer[] {1, 2, 3, 4, 5, 6, 7, 8, 9});
        if (!reverseEveryKth(nine, 3).toString().equals("[[1], [2, 3], [7, 6, 5, 4], [8, 9]]")) throw new AssertionError("example 1");
        if (!reverseEveryKth(nine, 1).toString().equals("[[1], [3, 2], [7, 6, 5, 4], [9, 8]]")) throw new AssertionError("example 2");
        if (!reverseEveryKth(null, 2).isEmpty()) throw new AssertionError("empty tree");
        Random rnd = new Random(161002);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd, 24, -50, 50);
            int k = 1 + rnd.nextInt(5);
            List<List<Integer>> want = new ArrayList<>();
            byDepth(build(v), 0, want);
            for (int d = 0; d < want.size(); d++) if (d % k == k - 1) Collections.reverse(want.get(d));
            if (!reverseEveryKth(build(v), k).equals(want)) throw new AssertionError("differs for k=" + k + " on " + Arrays.toString(v));
            List<List<Integer>> classic = new ArrayList<>();
            byDepth(build(v), 0, classic);
            for (int d = 1; d < classic.size(); d += 2) Collections.reverse(classic.get(d));
            if (!reverseEveryKth(build(v), 2).equals(classic)) throw new AssertionError("k=2 should be the classic zigzag");
        }
    }
}
```

#### Solution: [Boundary] Both Side Views And Hidden Count (LeetCode 199)
<!-- id: tc-both-views-hidden -->

**Approach.** In each wave the removal counter is 0 for the first person and `size - 1` for the last, so both are picked by comparing the counter with the snapshot. A wave of one person is both first and last, and the hidden count of a wave is `size - 2` when the wave has more than two people and zero otherwise. The oracle fills one list per depth with a recursive walk and then reads the first entry, the last entry and the length of every list. The assertions check both examples and random trees, and they confirm that every node is accounted for as left-visible, right-visible, or hidden once the single-person waves are taken into account.

**Complexity.** O(n) time and O(w) queue space.

```java run
import java.util.*;

public final class BothViewsRun {
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
    static String report(Node root) {
        List<Integer> left = new ArrayList<>(), right = new ArrayList<>();
        int hidden = 0;
        if (root != null) {
            ArrayDeque<Node> queue = new ArrayDeque<>();
            queue.add(root);
            while (!queue.isEmpty()) {
                int size = queue.size();
                for (int k = 0; k < size; k++) {
                    Node n = queue.poll();
                    if (k == 0) left.add(n.val);
                    if (k == size - 1) right.add(n.val);
                    if (k > 0 && k < size - 1) hidden++;
                    if (n.left != null) queue.add(n.left);
                    if (n.right != null) queue.add(n.right);
                }
            }
        }
        return "[" + left + ", " + right + ", " + hidden + "]";
    }

    static void byDepth(Node n, int depth, List<List<Integer>> out) {
        if (n == null) return;
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(n.val);
        byDepth(n.left, depth + 1, out);
        byDepth(n.right, depth + 1, out);
    }

    public static void main(String[] args) {
        if (!report(build(new Integer[] {1, 2, 3, 4, 5, 6, 7})).equals("[[1, 2, 4], [1, 3, 7], 2]")) throw new AssertionError("example 1");
        if (!report(build(new Integer[] {1, 2, 3, null, 5, null, 4})).equals("[[1, 2, 5], [1, 3, 4], 0]")) throw new AssertionError("example 2");
        if (!report(null).equals("[[], [], 0]")) throw new AssertionError("empty tree");
        Random rnd = new Random(161003);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd, 26, -9, 9);
            List<List<Integer>> rows = new ArrayList<>();
            byDepth(build(v), 0, rows);
            List<Integer> left = new ArrayList<>(), right = new ArrayList<>();
            int hidden = 0, nodes = 0, visible = 0;
            for (List<Integer> row : rows) {
                left.add(row.get(0));
                right.add(row.get(row.size() - 1));
                hidden += Math.max(0, row.size() - 2);
                nodes += row.size();
                visible += Math.min(row.size(), 2);
            }
            String want = "[" + left + ", " + right + ", " + hidden + "]";
            if (!report(build(v)).equals(want)) throw new AssertionError("differs on " + Arrays.toString(v));
            if (hidden + visible != nodes) throw new AssertionError("every node is visible or hidden");
        }
    }
}
```

#### Solution: [Recognize] N-ary Tree Level Order Traversal (LeetCode 429)
<!-- id: tc-nary-level-order -->

**Approach.** The wave method is unchanged except that the two child checks become a loop over `children.get(node)`, which adds each child in list order. The tree needs no node objects, since the node numbers index the lists. The oracle is a recursive preorder walk that appends each node number to the list of its depth, which orders nodes inside a depth the same way the queue does, by the order of their ancestors' lists. The assertions check both examples, thousands of random rooted trees, and a chain of 20000 nodes that a recursive method would struggle with.

**Complexity.** O(n) time and O(w) queue space.

```java run
import java.util.*;

public final class NaryWavesRun {
    static List<List<Integer>> waves(List<List<Integer>> children) {
        List<List<Integer>> out = new ArrayList<>();
        ArrayDeque<Integer> queue = new ArrayDeque<>();
        queue.add(0);
        while (!queue.isEmpty()) {
            int size = queue.size();
            List<Integer> wave = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                int who = queue.poll();
                wave.add(who);
                for (int child : children.get(who)) queue.add(child);
            }
            out.add(wave);
        }
        return out;
    }

    static void byDepth(List<List<Integer>> children, int who, int depth, List<List<Integer>> out) {
        if (out.size() == depth) out.add(new ArrayList<>());
        out.get(depth).add(who);
        for (int child : children.get(who)) byDepth(children, child, depth + 1, out);
    }

    static List<List<Integer>> lists(int[][] raw) {
        List<List<Integer>> out = new ArrayList<>();
        for (int[] row : raw) {
            List<Integer> one = new ArrayList<>();
            for (int x : row) one.add(x);
            out.add(one);
        }
        return out;
    }

    public static void main(String[] args) {
        if (!waves(lists(new int[][] {{1, 2, 3}, {4, 5}, {}, {6}, {}, {}, {}})).toString().equals("[[0], [1, 2, 3], [4, 5, 6]]")) throw new AssertionError("example 1");
        if (!waves(lists(new int[][] {{1}, {2}, {3}, {}})).toString().equals("[[0], [1], [2], [3]]")) throw new AssertionError("example 2");
        if (!waves(lists(new int[][] {{}})).toString().equals("[[0]]")) throw new AssertionError("single node");
        List<List<Integer>> chain = new ArrayList<>();
        for (int i = 0; i < 20000; i++) chain.add(i + 1 < 20000 ? List.of(i + 1) : List.of());
        if (waves(chain).size() != 20000) throw new AssertionError("chain depth");
        Random rnd = new Random(161004);
        for (int t = 0; t < 5000; t++) {
            int n = 1 + rnd.nextInt(40);
            List<List<Integer>> children = new ArrayList<>();
            for (int i = 0; i < n; i++) children.add(new ArrayList<>());
            for (int i = 1; i < n; i++) children.get(rnd.nextInt(i)).add(i);
            for (List<Integer> c : children) Collections.shuffle(c, rnd);
            List<List<Integer>> want = new ArrayList<>();
            byDepth(children, 0, 0, want);
            if (!waves(children).equals(want)) throw new AssertionError("differs on " + children);
        }
    }
}
```
