<!-- solutions-for: 04-depth-and-path-state -->
### Depth And Path State

#### Solution: [Build] Maximum Depth of Binary Tree (LeetCode 104)
<!-- id: tr-depth-of-tree -->

**Approach.** A null subtree has depth 0, and any other node has depth one plus the larger depth of its two sides, so the answer is built only from return values and nothing is passed down. The tree is made of real nodes from the level-order array. The oracle uses no recursion: because a parent always sits earlier in the array than its children, a single left-to-right pass can set each child's depth to its parent's depth plus one, and the answer is the largest depth found. The assertions compare the two on random trees, and check the empty tree and a chain.

**Complexity.** O(n) time, and O(h) recursion stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class DepthOfTree {
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
            if (v[feed] != null) { seat[feed] = new Node(v[feed]); seat[p].left = seat[feed]; }
            feed++;
            if (feed < v.length) {
                if (v[feed] != null) { seat[feed] = new Node(v[feed]); seat[p].right = seat[feed]; }
                feed++;
            }
        }
        return seat[0];
    }

    static int maxDepth(Node node) {
        if (node == null) return 0;
        return 1 + Math.max(maxDepth(node.left), maxDepth(node.right));
    }

    static int oracle(Integer[] v) {
        int n = v.length;
        if (n == 0) return 0;
        int[] depth = new int[n];
        boolean[] present = new boolean[n];
        present[0] = true;
        depth[0] = 1;
        int best = 1, feed = 1;
        for (int p = 0; p < n && feed < n; p++) {
            if (!present[p]) continue;
            for (int c = 0; c < 2 && feed < n; c++, feed++) {
                if (v[feed] != null) { present[feed] = true; depth[feed] = depth[p] + 1; best = Math.max(best, depth[feed]); }
            }
        }
        return best;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(15);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(201) - 100);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(5) != 0) { out.add(rnd.nextInt(201) - 100); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (maxDepth(build(new Integer[] {3, 9, 20, null, null, 15, 7})) != 3) throw new AssertionError("example 1");
        if (maxDepth(build(new Integer[] {1, null, 2})) != 2) throw new AssertionError("example 2");
        if (maxDepth(build(new Integer[] {})) != 0) throw new AssertionError("empty tree has depth 0");
        if (maxDepth(build(new Integer[] {7})) != 1) throw new AssertionError("single node has depth 1");
        Random rnd = new Random(15401);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            if (maxDepth(build(v)) != oracle(v)) throw new AssertionError("differs on " + Arrays.toString(v));
        }
    }
}
```

#### Solution: [Vary] Path Sum (LeetCode 112)
<!-- id: tr-path-sum-exists -->

**Approach.** Pass the amount still needed down as an `int`. Each node subtracts its value, a leaf answers whether the amount left is zero, and an inner node answers true when either side does. A null child is false, which is safe because only a missing child of a one-sided node reaches it and that node is not a leaf. The oracle computes the sum from the root to every node with one pass over the array, using parent positions, and checks the sums at leaves only. The assertions compare the two with targets taken from real leaf sums and from random numbers, and check that a match at an inner node alone gives false.

**Complexity.** O(n) time, and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PathSumExists {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        List<Node> line = new ArrayList<>();
        Node root = new Node(v[0]);
        line.add(root);
        int at = 1;
        for (int p = 0; p < line.size() && at < v.length; p++) {
            Node parent = line.get(p);
            if (v[at] != null) { parent.left = new Node(v[at]); line.add(parent.left); }
            at++;
            if (at < v.length) {
                if (v[at] != null) { parent.right = new Node(v[at]); line.add(parent.right); }
                at++;
            }
        }
        return root;
    }

    static boolean hasPathSum(Node node, int remaining) {
        if (node == null) return false;
        remaining -= node.val;
        if (node.left == null && node.right == null) return remaining == 0;
        return hasPathSum(node.left, remaining) || hasPathSum(node.right, remaining);
    }

    static List<Integer> leafSums(Integer[] v) {
        List<Integer> sums = new ArrayList<>();
        int n = v.length;
        if (n == 0) return sums;
        int[] total = new int[n];
        boolean[] present = new boolean[n];
        boolean[] hasChild = new boolean[n];
        present[0] = true;
        total[0] = v[0];
        int feed = 1;
        for (int p = 0; p < n && feed < n; p++) {
            if (!present[p]) continue;
            for (int c = 0; c < 2 && feed < n; c++, feed++) {
                if (v[feed] != null) { present[feed] = true; total[feed] = total[p] + v[feed]; hasChild[p] = true; }
            }
        }
        for (int i = 0; i < n; i++) if (present[i] && !hasChild[i]) sums.add(total[i]);
        return sums;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(12);
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
        Integer[] a = {5, 4, 8, 11, null, 13, 4, 7, 2};
        if (!hasPathSum(build(a), 22)) throw new AssertionError("example 1");
        if (hasPathSum(build(new Integer[] {1, 2, 3}), 5)) throw new AssertionError("example 2");
        if (hasPathSum(build(new Integer[] {}), 0)) throw new AssertionError("an empty tree has no path");
        if (hasPathSum(build(new Integer[] {1, 2}), 1)) throw new AssertionError("a match at an inner node is not a root-to-leaf path");
        Random rnd = new Random(15402);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            List<Integer> sums = leafSums(v);
            int target = rnd.nextBoolean() ? sums.get(rnd.nextInt(sums.size())) : rnd.nextInt(81) - 40;
            if (hasPathSum(build(v), target) != sums.contains(target)) throw new AssertionError("differs on " + Arrays.toString(v) + " target " + target);
        }
    }
}
```

#### Solution: [Boundary] Leaf Versus Internal Match (Author exercise)
<!-- id: tr-leaf-versus-internal -->

**Approach.** Carry the running sum down as an `int`. At each node add its value, add one to the any-node count when the sum equals the target, and add one to the leaf count only when the node also has no children. A sum can pass the target and come back when negative values are present, so a walk may not stop early at a match or a miss. The oracle collects each node's root sum from a parent pass over the array and counts by position. The assertions compare the two counts on random trees with negative labels, and check that the leaf count never exceeds the other.

**Complexity.** O(n) time, since every node is entered once, and O(h) stack.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class LeafVersusInternal {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node[] byPos = new Node[v.length];
        byPos[0] = new Node(v[0]);
        int cursor = 1;
        for (int p = 0; p < v.length && cursor < v.length; p++) {
            if (byPos[p] == null) continue;
            Node left = v[cursor] == null ? null : new Node(v[cursor]);
            byPos[cursor++] = left;
            byPos[p].left = left;
            if (cursor < v.length) {
                Node right = v[cursor] == null ? null : new Node(v[cursor]);
                byPos[cursor++] = right;
                byPos[p].right = right;
            }
        }
        return byPos[0];
    }

    static int leaf, any;

    static void count(Node node, int sum, int target) {
        if (node == null) return;
        sum += node.val;
        if (sum == target) {
            any++;
            if (node.left == null && node.right == null) leaf++;
        }
        count(node.left, sum, target);
        count(node.right, sum, target);
    }

    static int[] matches(Integer[] v, int target) {
        leaf = 0;
        any = 0;
        count(build(v), 0, target);
        return new int[] {leaf, any};
    }

    static int[] oracle(Integer[] v, int target) {
        int n = v.length, leaves = 0, all = 0;
        if (n == 0) return new int[] {0, 0};
        int[] total = new int[n];
        boolean[] present = new boolean[n];
        boolean[] parentOfSomething = new boolean[n];
        present[0] = true;
        total[0] = v[0];
        int next = 1;
        for (int p = 0; p < n && next < n; p++) {
            if (!present[p]) continue;
            for (int c = 0; c < 2 && next < n; c++, next++) {
                if (v[next] != null) { present[next] = true; total[next] = total[p] + v[next]; parentOfSomething[p] = true; }
            }
        }
        for (int i = 0; i < n; i++) {
            if (!present[i] || total[i] != target) continue;
            all++;
            if (!parentOfSomething[i]) leaves++;
        }
        return new int[] {leaves, all};
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(12);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(7) - 3);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(7) - 3); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        if (!Arrays.equals(matches(new Integer[] {1, 2}, 1), new int[] {0, 1})) throw new AssertionError("example 1");
        if (!Arrays.equals(matches(new Integer[] {3, 0, -3}, 3), new int[] {1, 2})) throw new AssertionError("example 2");
        if (!Arrays.equals(matches(new Integer[] {}, 0), new int[] {0, 0})) throw new AssertionError("empty tree");
        Random rnd = new Random(15403);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            int target = rnd.nextInt(9) - 4;
            int[] got = matches(v, target);
            if (!Arrays.equals(got, oracle(v, target))) throw new AssertionError("differs on " + Arrays.toString(v) + " target " + target);
            if (got[0] > got[1]) throw new AssertionError("leaf matches are a subset of all matches");
        }
    }
}
```

#### Solution: [Recognize] Path Sum II (LeetCode 113)
<!-- id: tr-path-sum-routes -->

**Approach.** Keep one shared list. On entering a node, append its value and subtract it from the amount still needed. At a leaf with nothing left, store a copy of the list. After both child calls, remove the last element by index, which hands the list back as it was found. The oracle works from the other direction: it finds each matching leaf and climbs parent positions to rebuild the route in reverse, then orders the routes by the string of left and right turns that leads to each leaf. The assertions compare on random trees, and demonstrate the two Java hazards, that storing the shared list itself leaves only emptied lists behind and that `remove(Integer)` deletes the first equal value, not the last.

**Complexity.** O(n) time plus O(h) to copy each matching route, and O(h) stack besides the output.

```java run
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

public final class PathSumRoutes {
    static final class Node {
        final int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Node build(Integer[] v) {
        if (v.length == 0) return null;
        Node root = new Node(v[0]);
        List<Node> frontier = new ArrayList<>();
        frontier.add(root);
        int idx = 1;
        for (int f = 0; f < frontier.size() && idx < v.length; f++) {
            Node top = frontier.get(f);
            if (v[idx] != null) { top.left = new Node(v[idx]); frontier.add(top.left); }
            idx++;
            if (idx < v.length) {
                if (v[idx] != null) { top.right = new Node(v[idx]); frontier.add(top.right); }
                idx++;
            }
        }
        return root;
    }

    static void routes(Node node, int remaining, List<Integer> path, List<List<Integer>> found, boolean copy) {
        if (node == null) return;
        path.add(node.val);
        remaining -= node.val;
        if (node.left == null && node.right == null && remaining == 0) found.add(copy ? new ArrayList<>(path) : path);
        routes(node.left, remaining, path, found, copy);
        routes(node.right, remaining, path, found, copy);
        path.remove(path.size() - 1);
    }

    static List<List<Integer>> pathSum(Integer[] v, int target) {
        List<List<Integer>> found = new ArrayList<>();
        routes(build(v), target, new ArrayList<>(), found, true);
        return found;
    }

    static List<List<Integer>> oracle(Integer[] v, int target) {
        List<List<Integer>> out = new ArrayList<>();
        int n = v.length;
        if (n == 0) return out;
        int[] parent = new int[n], total = new int[n];
        String[] turns = new String[n];
        boolean[] present = new boolean[n], inner = new boolean[n];
        present[0] = true;
        total[0] = v[0];
        parent[0] = -1;
        turns[0] = "";
        int next = 1;
        for (int p = 0; p < n && next < n; p++) {
            if (!present[p]) continue;
            for (int c = 0; c < 2 && next < n; c++, next++) {
                if (v[next] == null) continue;
                present[next] = true;
                parent[next] = p;
                total[next] = total[p] + v[next];
                turns[next] = turns[p] + c;
                inner[p] = true;
            }
        }
        List<Integer> hits = new ArrayList<>();
        for (int i = 0; i < n; i++) if (present[i] && !inner[i] && total[i] == target) hits.add(i);
        hits.sort((a, b) -> turns[a].compareTo(turns[b]));
        for (int leafPos : hits) {
            List<Integer> route = new ArrayList<>();
            for (int at = leafPos; at >= 0; at = parent[at]) route.add(0, v[at]);
            out.add(route);
        }
        return out;
    }

    static Integer[] randomLevels(Random rnd) {
        int n = 1 + rnd.nextInt(12);
        List<Integer> out = new ArrayList<>();
        int made = 1, open = 1;
        out.add(rnd.nextInt(7) - 3);
        while (open > 0) {
            open--;
            for (int c = 0; c < 2; c++) {
                if (made < n && rnd.nextInt(4) != 0) { out.add(rnd.nextInt(7) - 3); made++; open++; }
                else out.add(null);
            }
        }
        while (!out.isEmpty() && out.get(out.size() - 1) == null) out.remove(out.size() - 1);
        return out.toArray(new Integer[0]);
    }

    public static void main(String[] args) {
        Integer[] a = {5, 4, 8, 11, null, 13, 4, 7, 2, null, null, 5, 1};
        if (!pathSum(a, 22).equals(List.of(List.of(5, 4, 11, 2), List.of(5, 8, 4, 5)))) throw new AssertionError("example 1");
        if (!pathSum(new Integer[] {1, 2}, 0).isEmpty()) throw new AssertionError("example 2");
        List<List<Integer>> aliased = new ArrayList<>();
        routes(build(new Integer[] {1, 2}), 3, new ArrayList<>(), aliased, false);
        if (aliased.size() != 1 || !aliased.get(0).isEmpty()) throw new AssertionError("a stored reference to the shared list ends up empty");
        List<Integer> sample = new ArrayList<>(List.of(5, 1, 5));
        sample.remove(Integer.valueOf(5));
        if (!sample.equals(List.of(1, 5))) throw new AssertionError("remove(Integer) deletes the first equal value");
        Random rnd = new Random(15404);
        for (int t = 0; t < 6000; t++) {
            Integer[] v = randomLevels(rnd);
            int target = rnd.nextInt(9) - 4;
            if (!pathSum(v, target).equals(oracle(v, target))) throw new AssertionError("differs on " + Arrays.toString(v) + " target " + target);
        }
    }
}
```
