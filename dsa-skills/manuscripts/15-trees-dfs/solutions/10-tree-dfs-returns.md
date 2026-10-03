<!-- solutions-for: 10-tree-dfs-returns -->
### Tree DFS Returns

#### Solution: [Build] Maximum Depth of Binary Tree (LeetCode 104)
<!-- id: td-height-and-deepest -->

**Approach.** The return state is a pair of the height and the number of leaves at that height. A null child reports `{0, 0}`. A node with two null children is a leaf and reports `{1, 1}`. Otherwise it keeps the deeper side's pair with the height raised by one, and when the two heights are equal it adds the two counts. No separate result is needed, because the final answer is the root's own state. The oracle gives every node its depth by one pass over the level-order array, takes the largest depth, and counts the nodes at that depth, which are all leaves. The assertions compare on random trees, including ties between sides.

**Complexity.** O(n) time and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class HeightAndDeepest {
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

    static int[] state(Node node) {
        if (node == null) return new int[] {0, 0};
        if (node.left == null && node.right == null) return new int[] {1, 1};
        int[] l = state(node.left), r = state(node.right);
        if (l[0] > r[0]) return new int[] {1 + l[0], l[1]};
        if (r[0] > l[0]) return new int[] {1 + r[0], r[1]};
        return new int[] {1 + l[0], l[1] + r[1]};
    }

    static int[] oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return new int[] {0, 0};
        int[] depth = new int[n];
        boolean[] live = new boolean[n];
        live[0] = true;
        depth[0] = 1;
        int feed = 1, top = 1;
        for (int p = 0; p < n && feed < n; p++) {
            if (!live[p]) continue;
            for (int c = 0; c < 2 && feed < n; c++, feed++) {
                if (v[feed] != null) { live[feed] = true; depth[feed] = depth[p] + 1; top = Math.max(top, depth[feed]); }
            }
        }
        int count = 0;
        for (int i = 0; i < n; i++) if (live[i] && depth[i] == top) count++;
        return new int[] {top, count};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(15);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(201) - 100);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(rnd.nextInt(201) - 100); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(state(build(new Integer[] {1, 2, 3, 4})), new int[] {3, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(state(build(new Integer[] {1, 2, 3, 4, null, null, 5})), new int[] {3, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(state(build(new Integer[] {})), new int[] {0, 0})) throw new AssertionError("empty tree");
        Random rnd = new Random(151001);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (!Arrays.equals(state(build(v)), oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Diameter of Binary Tree (LeetCode 543)
<!-- id: td-diameter-turns -->

**Approach.** Each call returns its height in nodes. At a node the local chain is the sum of the two child heights, and it is folded into a running pair: when the chain exceeds the best so far the best is replaced and the count restarts at one, and when it equals the best the count grows by one. The running best starts at -1 so that a single node, whose local chain is 0, is counted. The count cannot be final until the whole tree is done, since a later larger chain discards earlier ties. The oracle takes every pair of nodes, finds the distance and the highest common ancestor by climbing parents, and collects the distinct ancestors of the pairs at the largest distance. The assertions compare both numbers on random trees.

**Complexity.** O(n) time and O(h) stack, against O(n^2) pairs for the oracle.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class DiameterTurns {
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

    static int best, turns;

    static int height(Node node) {
        if (node == null) return 0;
        int l = height(node.left), r = height(node.right);
        int chain = l + r;
        if (chain > best) { best = chain; turns = 1; }
        else if (chain == best) turns++;
        return 1 + Math.max(l, r);
    }

    static int[] diameterAndTurns(Integer[] v) {
        best = -1;
        turns = 0;
        Node root = build(v);
        if (root == null) return new int[] {0, 0};
        height(root);
        return new int[] {best, turns};
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
        Set<Integer> tops = new HashSet<>();
        for (int a = 0; a < n; a++) {
            if (!live[a]) continue;
            for (int b = a; b < n; b++) {
                if (!live[b]) continue;
                int x = a, y = b, d = 0;
                while (x != y) {
                    if (depth[x] >= depth[y]) x = parent[x]; else y = parent[y];
                    d++;
                }
                if (d > far) { far = d; tops.clear(); }
                if (d == far) tops.add(x);
            }
        }
        return new int[] {far, tops.size()};
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
        if (!Arrays.equals(diameterAndTurns(new Integer[] {1, 2, 3}), new int[] {2, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(diameterAndTurns(new Integer[] {1, 2, null, 3, 4}), new int[] {2, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(diameterAndTurns(new Integer[] {}), new int[] {0, 0})) throw new AssertionError("empty tree");
        if (!Arrays.equals(diameterAndTurns(new Integer[] {5}), new int[] {0, 1})) throw new AssertionError("single node");
        Random rnd = new Random(151002);
        for (int t = 0; t < 5000; t++) {
            Integer[] v = randomLevels(rnd);
            if (!Arrays.equals(diameterAndTurns(v), oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Boundary] Balanced Binary Tree (LeetCode 110)
<!-- id: td-weighted-balance -->

**Approach.** The state is a weighted height, a node's weight plus the larger child height, with 0 for a missing branch. Because weights are not negative, no valid state is negative, so -1 can mark failure. The call asks the left branch, ends at once on -1, asks the right branch, ends at once on -1, and only then compares the two states against the tolerance `k`, returning -1 when the difference exceeds it. The answer is true when the root's state is not -1. A node with weight 0 and no children has state 0, the same as a missing branch, which does not disturb the comparison. The oracle computes weighted heights for every node in a reverse pass over child positions and tests all nodes against `k`. The assertions compare on random trees and random tolerances, and run the empty tree.

**Complexity.** O(n) time and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class WeightedBalance {
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
        int at = 1;
        for (int k = 0; k < line.size() && at < v.length; k++) {
            Node parent = line.get(k);
            if (v[at] != null) { parent.left = new Node(v[at]); line.add(parent.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { parent.right = new Node(v[at]); line.add(parent.right); }
                at++;
            }
        }
        return root;
    }

    static final int FAILED = -1;

    static int weighted(Node node, int k) {
        if (node == null) return 0;
        int l = weighted(node.left, k);
        if (l == FAILED) return FAILED;
        int r = weighted(node.right, k);
        if (r == FAILED) return FAILED;
        if (Math.abs(l - r) > k) return FAILED;
        return node.val + Math.max(l, r);
    }

    static boolean balanced(Integer[] v, int k) { return weighted(build(v), k) != FAILED; }

    static boolean oracle(Integer[] v, int k) {
        int n = v.length;
        if (n == 0) return true;
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
        for (int p = n - 1; p >= 0; p--) {
            if (!live[p]) continue;
            int a = lc[p] >= 0 ? h[lc[p]] : 0, b = rc[p] >= 0 ? h[rc[p]] : 0;
            if (Math.abs(a - b) > k) return false;
            h[p] = v[p] + Math.max(a, b);
        }
        return true;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(14);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(6));
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(rnd.nextInt(6)); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!balanced(new Integer[] {3, 1, 2}, 1)) throw new AssertionError("example 1");
        if (balanced(new Integer[] {3, 1, 2}, 0)) throw new AssertionError("example 2");
        if (!balanced(new Integer[] {}, 0)) throw new AssertionError("empty tree");
        if (!balanced(new Integer[] {0, 0, 0}, 0)) throw new AssertionError("zero weights give zero heights");
        Random rnd = new Random(151003);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            int k = rnd.nextInt(8);
            if (balanced(v, k) != oracle(v, k)) throw new AssertionError("differs on " + Arrays.toString(v) + " k=" + k);
        }
    }
}
```

#### Solution: [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: td-path-sum-turn -->

**Approach.** Each call returns the gain of the best downward branch that starts at its node, equal to its value plus the better of its two cut-off child gains. At the node the local answer is its value plus both cut-off gains, and it is folded into a running pair of the best sum and the smallest top value that reached it: a larger sum replaces both, and an equal sum keeps the smaller top value. The running best starts at the smallest int, so an all-negative tree still reports a real path. The oracle takes every pair of nodes, sums the values on the path between them, finds the top node of the path by climbing to the common ancestor, and keeps the largest sum with the smallest top value among the pairs that reach it. The assertions compare on random trees with negative values.

**Complexity.** O(n) time and O(h) stack, against O(n^2) pairs for the oracle.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PathSumTurn {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        Node[] seat = new Node[v.length];
        seat[0] = new Node(v[0]);
        int feed = 1;
        for (int p = 0; p < v.length && feed < v.length; p++) {
            if (seat[p] == null) continue;
            Node l = v[feed] == null ? null : new Node(v[feed]);
            seat[feed++] = l;
            seat[p].left = l;
            if (feed < v.length) {
                Node r = v[feed] == null ? null : new Node(v[feed]);
                seat[feed++] = r;
                seat[p].right = r;
            }
        }
        return seat[0];
    }

    static int bestSum, turn;

    static int gain(Node node) {
        if (node == null) return 0;
        int l = Math.max(0, gain(node.left));
        int r = Math.max(0, gain(node.right));
        int through = node.val + l + r;
        if (through > bestSum) { bestSum = through; turn = node.val; }
        else if (through == bestSum) turn = Math.min(turn, node.val);
        return node.val + Math.max(l, r);
    }

    static int[] answer(Integer[] v) {
        bestSum = Integer.MIN_VALUE;
        turn = Integer.MAX_VALUE;
        gain(build(v));
        return new int[] {bestSum, turn};
    }

    static int[] oracle(Integer[] v) {
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
        int top = Integer.MIN_VALUE, who = Integer.MAX_VALUE;
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
                if (sum > top) { top = sum; who = v[x]; }
                else if (sum == top) who = Math.min(who, v[x]);
            }
        }
        return new int[] {top, who};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(13);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(21) - 10);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) < 3) { out.add(rnd.nextInt(21) - 10); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(answer(new Integer[] {2, -1, 3, null, 4}), new int[] {8, 2})) throw new AssertionError("example 1");
        if (!Arrays.equals(answer(new Integer[] {-4}), new int[] {-4, -4})) throw new AssertionError("example 2");
        Random rnd = new Random(151004);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (!Arrays.equals(answer(v), oracle(v))) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```
