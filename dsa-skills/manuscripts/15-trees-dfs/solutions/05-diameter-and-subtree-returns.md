<!-- solutions-for: 05-diameter-and-subtree-returns -->
### Diameter And Subtree Returns

#### Solution: [Build] Return Subtree Height (Author exercise)
<!-- id: tr-subtree-height -->

**Approach.** Let each call return its height, counted in nodes, with 0 for a null side. After both child calls have returned, the node compares the two heights, adds one to a counter when they differ, and returns one plus the larger. The counter is a field that is reset before each walk. The tree is assembled from the array by first finding every node's child positions and then creating nodes from the last position to the first, so that a node's children already exist when it is linked. The oracle computes the same heights by a reverse pass over child positions with no recursion. The assertions compare the pair on random trees.

**Complexity.** O(n) time, and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class SubtreeHeight {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int[][] childPositions(Integer[] v) {
        int n = v.length;
        int[] lc = new int[n], rc = new int[n];
        Arrays.fill(lc, -1);
        Arrays.fill(rc, -1);
        boolean[] present = new boolean[n];
        if (n > 0) present[0] = true;
        int next = 1;
        for (int p = 0; p < n && next < n; p++) {
            if (!present[p]) continue;
            if (v[next] != null) { lc[p] = next; present[next] = true; }
            next++;
            if (next < n) {
                if (v[next] != null) { rc[p] = next; present[next] = true; }
                next++;
            }
        }
        return new int[][] {lc, rc};
    }

    static Node build(Integer[] v) {
        int n = v.length;
        if (n == 0) return null;
        int[][] cp = childPositions(v);
        Node[] made = new Node[n];
        for (int p = n - 1; p >= 0; p--) {
            if (p > 0 && v[p] == null) continue;
            made[p] = new Node(v[p]);
            if (cp[0][p] >= 0) made[p].left = made[cp[0][p]];
            if (cp[1][p] >= 0) made[p].right = made[cp[1][p]];
        }
        return made[0];
    }

    static int uneven;

    static int height(Node node) {
        if (node == null) return 0;
        int l = height(node.left);
        int r = height(node.right);
        if (l != r) uneven++;
        return 1 + Math.max(l, r);
    }

    static int[] heightAndUneven(Integer[] v) {
        uneven = 0;
        int h = height(build(v));
        return new int[] {h, uneven};
    }

    static int[] oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return new int[] {0, 0};
        int[][] cp = childPositions(v);
        int[] h = new int[n];
        int differ = 0;
        for (int p = n - 1; p >= 0; p--) {
            if (p > 0 && v[p] == null) continue;
            int l = cp[0][p] >= 0 ? h[cp[0][p]] : 0;
            int r = cp[1][p] >= 0 ? h[cp[1][p]] : 0;
            if (l != r) differ++;
            h[p] = 1 + Math.max(l, r);
        }
        return new int[] {h[0], differ};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(201) - 100);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(201) - 100); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(heightAndUneven(new Integer[] {1, 2, 3}), new int[] {2, 0})) throw new AssertionError("example 1");
        if (!Arrays.equals(heightAndUneven(new Integer[] {1, 2, null, 3}), new int[] {3, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(heightAndUneven(new Integer[] {}), new int[] {0, 0})) throw new AssertionError("empty tree");
        Random rnd = new Random(15501);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (!Arrays.equals(heightAndUneven(v), oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Diameter of Binary Tree (LeetCode 543)
<!-- id: tr-diameter-of-tree -->

**Approach.** Work on child position arrays directly. A call returns the height of the subtree in nodes. It reads the heights of its two sides, raises the running best to their sum, which is the number of edges on the best path that turns at this node, and returns one plus the larger height. The running best is reset at the start of each query. The oracle ignores recursion altogether: it treats the tree as an undirected graph, runs a breadth-first distance search from every node, and takes the largest distance found. The assertions compare the two on random trees, and show that a running best that is not reset carries a larger tree's answer into the next query.

**Complexity.** O(n) time, and O(h) stack, against O(n^2) for the all-sources oracle.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Random;

public final class DiameterOfTree {
    static int[] lc, rc;
    static int best;

    static void link(Integer[] v) {
        int n = v.length;
        lc = new int[n];
        rc = new int[n];
        Arrays.fill(lc, -1);
        Arrays.fill(rc, -1);
        boolean[] live = new boolean[n];
        if (n > 0) live[0] = true;
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
    }

    static int heightOf(int at) {
        if (at < 0) return 0;
        int l = heightOf(lc[at]);
        int r = heightOf(rc[at]);
        best = Math.max(best, l + r);
        return 1 + Math.max(l, r);
    }

    static int diameter(Integer[] v) {
        link(v);
        best = 0;
        if (v.length > 0) heightOf(0);
        return best;
    }

    static int diameterWithoutReset(Integer[] v) {
        link(v);
        if (v.length > 0) heightOf(0);
        return best;
    }

    static int oracle(Integer[] v) {
        link(v);
        int n = v.length, far = 0;
        if (n == 0) return 0;
        boolean[] live = new boolean[n];
        live[0] = true;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int p = 0; p < n; p++) {
            if (lc[p] >= 0) { adj.get(p).add(lc[p]); adj.get(lc[p]).add(p); }
            if (rc[p] >= 0) { adj.get(p).add(rc[p]); adj.get(rc[p]).add(p); }
        }
        for (int s = 0; s < n; s++) {
            if (s > 0 && v[s] == null) continue;
            int[] dist = new int[n];
            Arrays.fill(dist, -1);
            Deque<Integer> queue = new ArrayDeque<>();
            queue.add(s);
            dist[s] = 0;
            while (!queue.isEmpty()) {
                int u = queue.poll();
                far = Math.max(far, dist[u]);
                for (int w : adj.get(u)) if (dist[w] < 0) { dist[w] = dist[u] + 1; queue.add(w); }
            }
        }
        return far;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(201) - 100);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(201) - 100); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (diameter(new Integer[] {1, 2, 3, 4, 5}) != 3) throw new AssertionError("example 1");
        if (diameter(new Integer[] {1, 2}) != 1) throw new AssertionError("example 2");
        if (diameter(new Integer[] {}) != 0) throw new AssertionError("empty tree");
        if (diameter(new Integer[] {9}) != 0) throw new AssertionError("one node has no edges");
        diameter(new Integer[] {1, 2, 3, 4, 5});
        if (diameterWithoutReset(new Integer[] {1, 2}) != 3) throw new AssertionError("a best that is not reset keeps the earlier answer");
        Random rnd = new Random(15502);
        for (int t = 0; t < 4000; t++) {
            Integer[] v = randomLevels(rnd);
            if (diameter(v) != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Nodes Versus Edges (Author exercise)
<!-- id: tr-nodes-versus-edges -->

**Approach.** Heights count nodes, so a null side is 0 and a leaf is 1. At each node the sum of its two heights is the number of edges on the best path turning there, since each height already counts the node at its far end and the turning node itself is the shared point. The final answer in edges is the largest such sum, and the answer in nodes is that value plus one, but only when the tree has at least one node. The empty tree gives `[0, 0]` by the guard and a single node gives `[0, 1]`. The oracle computes distances between every pair of nodes through the nearest common ancestor. The assertions compare both units on random trees.

**Complexity.** O(n) time and O(h) stack, against O(n^2) pairs for the oracle.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Random;

public final class NodesVersusEdges {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Iterator<Integer> it = Arrays.asList(v).iterator();
        Node root = new Node(it.next());
        Queue<Node> open = new LinkedList<>();
        open.add(root);
        while (!open.isEmpty() && it.hasNext()) {
            Node cur = open.remove();
            Integer a = it.next();
            if (a != null) { cur.left = new Node(a); open.add(cur.left); }
            if (it.hasNext()) {
                Integer b = it.next();
                if (b != null) { cur.right = new Node(b); open.add(cur.right); }
            }
        }
        return root;
    }

    static int longestSum;

    static int heightInNodes(Node node) {
        if (node == null) return 0;
        int l = heightInNodes(node.left);
        int r = heightInNodes(node.right);
        longestSum = Math.max(longestSum, l + r);
        return 1 + Math.max(l, r);
    }

    static int[] edgesAndNodes(Integer[] v) {
        Node root = build(v);
        if (root == null) return new int[] {0, 0};
        longestSum = 0;
        heightInNodes(root);
        return new int[] {longestSum, longestSum + 1};
    }

    static int[] oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return new int[] {0, 0};
        int[] parent = new int[n], depth = new int[n];
        boolean[] live = new boolean[n];
        live[0] = true;
        parent[0] = -1;
        int feed = 1;
        for (int p = 0; p < n && feed < n; p++) {
            if (!live[p]) continue;
            for (int c = 0; c < 2 && feed < n; c++, feed++) {
                if (v[feed] != null) { live[feed] = true; parent[feed] = p; depth[feed] = depth[p] + 1; }
            }
        }
        int far = 0;
        for (int a = 0; a < n; a++) {
            if (!live[a]) continue;
            for (int b = a; b < n; b++) {
                if (!live[b]) continue;
                int x = a, y = b, d = 0;
                while (x != y) {
                    if (depth[x] >= depth[y]) x = parent[x]; else y = parent[y];
                    d++;
                }
                far = Math.max(far, d);
            }
        }
        return new int[] {far, far + 1};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(201) - 100);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(201) - 100); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(edgesAndNodes(new Integer[] {7}), new int[] {0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(edgesAndNodes(new Integer[] {1, 2, 3, 4, 5}), new int[] {3, 4})) throw new AssertionError("example 2");
        if (!Arrays.equals(edgesAndNodes(new Integer[] {}), new int[] {0, 0})) throw new AssertionError("empty tree");
        Random rnd = new Random(15503);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            if (!Arrays.equals(edgesAndNodes(v), oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: tr-max-path-sum -->

**Approach.** A call returns the best downward branch sum starting at its node, cut off at zero: `max(0, ...)` is applied to each child's report before it is used, because a negative branch only lowers the total and may be dropped. At the node the complete answer is its value plus the two cut-off branches, and that number updates the running best, which starts at the smallest `int` so that an all-negative tree still reports its largest single value. The node returns its value plus the larger branch, which the parent in turn cuts off at zero. The oracle sums the values on the path between every pair of nodes, including a node with itself. The assertions compare on random trees with negative labels, and show that a best that starts at zero would be wrong for one negative node.

**Complexity.** O(n) time and O(h) stack, against O(n^2) pairs for the oracle.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class MaxPathSum {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        List<Node> level = new ArrayList<>();
        if (v.length == 0) return null;
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

    static int best;

    static int gain(Node node) {
        if (node == null) return 0;
        int l = Math.max(0, gain(node.left));
        int r = Math.max(0, gain(node.right));
        best = Math.max(best, node.val + l + r);
        return node.val + Math.max(l, r);
    }

    static int maxPathSum(Integer[] v) {
        best = Integer.MIN_VALUE;
        gain(build(v));
        return best;
    }

    static int zeroStart(Integer[] v) {
        best = 0;
        gain(build(v));
        return best;
    }

    static int oracle(Integer[] v) {
        int n = v.length;
        int[] parent = new int[n], depth = new int[n];
        boolean[] live = new boolean[n];
        live[0] = true;
        parent[0] = -1;
        int feed = 1;
        for (int p = 0; p < n && feed < n; p++) {
            if (!live[p]) continue;
            for (int c = 0; c < 2 && feed < n; c++, feed++) {
                if (v[feed] != null) { live[feed] = true; parent[feed] = p; depth[feed] = depth[p] + 1; }
            }
        }
        int top = Integer.MIN_VALUE;
        for (int a = 0; a < n; a++) {
            if (!live[a]) continue;
            for (int b = a; b < n; b++) {
                if (!live[b]) continue;
                int x = a, y = b, sum = 0;
                while (x != y) {
                    if (depth[x] >= depth[y]) { sum += v[x]; x = parent[x]; }
                    else { sum += v[y]; y = parent[y]; }
                }
                sum += v[x];
                top = Math.max(top, sum);
            }
        }
        return top;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(13);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(41) - 20);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(41) - 20); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (maxPathSum(new Integer[] {2, -1, 3, null, 4}) != 8) throw new AssertionError("example 1");
        if (maxPathSum(new Integer[] {-4}) != -4) throw new AssertionError("example 2");
        if (zeroStart(new Integer[] {-4}) != 0) throw new AssertionError("a best that starts at zero ignores an all-negative tree");
        Random rnd = new Random(15504);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (maxPathSum(v) != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```
