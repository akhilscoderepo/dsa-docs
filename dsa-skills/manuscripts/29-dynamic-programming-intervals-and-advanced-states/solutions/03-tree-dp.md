<!-- solutions-for: 29-dynamic-programming-intervals-and-advanced-states -->
### Solutions For Tree DP

#### Solution: [Build] Take Or Skip Node (Author exercise)
<!-- id: dp29-take-or-skip-node -->

**Approach.**
Two arrays `take` and `skip` hold one pair for each node. Entry `take[v]` is the largest valid total in the subtree of `v` when `v` is chosen, and `skip[v]` is the same total when `v` is left out. Every node starts with `take[v] = w[v]` and `skip[v] = 0`, which is the pair of a leaf. The loop then visits nodes from `n - 1` down to 1. Because `parent[i] < i`, every child has a larger index than its parent, so each node is finished before the loop reaches its parent. A finished child adds `skip[v]` to `take[p]`, since a chosen parent blocks the child. It adds `max(take[v], skip[v])` to `skip[p]`, since a free parent lets the child choose.

The invariant is that when the loop reaches node `v`, all of its children have already pushed their contributions, so `take[v]` and `skip[v]` are final. The method never recurses, so a chain of 100000 nodes needs no stack depth.

**Complexity.**
- **Time** is O(n), because the loop visits each node once and does constant work for it.
- **Space** is O(n) for the two arrays, and the input arrays stay unchanged.

```java run
import java.util.*;

public final class DpTakeOrSkipNode {
    /**
     * Returns {best with node 0 chosen, best with node 0 left out}.
     * Time: O(n). Space: O(n).
     * Invariant: take[v] and skip[v] are final once every child of v has been visited.
     */
    static int[] rootPair(int[] parent, int[] w) {
        // n nodes, so each of the two arrays has n entries.
        int n = w.length;
        int[] take = new int[n];
        int[] skip = new int[n];
        // Every node starts as a leaf: chosen total is its weight, left-out total is 0.
        for (int v = 0; v < n; v++) take[v] = w[v];
        // Visit from the last index down, so children come before their parent.
        for (int v = n - 1; v >= 1; v--) {
            int p = parent[v];
            // A chosen parent blocks this child, so only the child's skip total counts.
            take[p] += skip[v];
            // A free parent lets the child pick its better case.
            skip[p] += Math.max(take[v], skip[v]);
        }
        // The root pair summarizes the whole tree.
        return new int[] {take[0], skip[0]};
    }

    /** Oracle: tries every subset of nodes and keeps the valid ones. */
    static int[] oracle(int[] parent, int[] w) {
        int n = w.length;
        int withRoot = Integer.MIN_VALUE;
        int withoutRoot = Integer.MIN_VALUE;
        for (int mask = 0; mask < (1 << n); mask++) {
            boolean ok = true;
            int sum = 0;
            for (int v = 0; v < n && ok; v++) {
                if ((mask >> v & 1) == 0) continue;
                sum += w[v];
                if (v > 0 && (mask >> parent[v] & 1) == 1) ok = false;
            }
            if (!ok) continue;
            if ((mask & 1) == 1) withRoot = Math.max(withRoot, sum);
            else withoutRoot = Math.max(withoutRoot, sum);
        }
        return new int[] {withRoot, withoutRoot};
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(rootPair(new int[] {-1, 0, 0, 1, 1}, new int[] {2, 7, 4, 6, 1}), new int[] {9, 11})) throw new AssertionError("ex1");
        if (!Arrays.equals(rootPair(new int[] {-1, 0, 1, 2}, new int[] {5, 1, 1, 5}), new int[] {10, 6})) throw new AssertionError("ex2");
        // A single node: choosing it gives its weight, leaving it out gives 0.
        if (!Arrays.equals(rootPair(new int[] {-1}, new int[] {7}), new int[] {7, 0})) throw new AssertionError("single");
        // A new int array holds zeros, which is the skip total of a leaf.
        int[] fresh = new int[3];
        if (fresh[0] != 0 || fresh[1] != 0 || fresh[2] != 0) throw new AssertionError("zero fill");
        // A chain of 100000 nodes runs without recursion and takes every other node.
        int big = 100000;
        int[] chainParent = new int[big];
        int[] chainWeight = new int[big];
        chainParent[0] = -1;
        for (int i = 1; i < big; i++) chainParent[i] = i - 1;
        Arrays.fill(chainWeight, 1);
        int[] chain = rootPair(chainParent, chainWeight);
        if (chain[0] != 50000 || chain[1] != 50000) throw new AssertionError("chain");
        // The input arrays are not modified.
        int[] par = {-1, 0, 0};
        int[] wt = {10, 6, 7};
        rootPair(par, wt);
        if (!Arrays.equals(par, new int[] {-1, 0, 0}) || !Arrays.equals(wt, new int[] {10, 6, 7})) throw new AssertionError("mutated");
        // Random trees against the subset oracle.
        Random rnd = new Random(2931);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(11);
            int[] p = new int[n];
            int[] w = new int[n];
            p[0] = -1;
            for (int i = 1; i < n; i++) p[i] = rnd.nextInt(i);
            for (int i = 0; i < n; i++) w[i] = rnd.nextInt(10);
            if (!Arrays.equals(rootPair(p, w), oracle(p, w))) throw new AssertionError("random " + t);
        }
    }
}
```

#### Solution: [Vary] House Robber III (LeetCode 337)
<!-- id: dp29-house-robber-iii -->

**Approach.**
A recursive helper returns an `int[2]` for each node, with the take total at index 0 and the skip total at index 1. A `null` node returns `{0, 0}`. For a real node, the helper first gets the pairs of its two children. The take total adds the node amount to both child skip totals, because a chosen node blocks its children. The skip total adds the better case of the left child to the better case of the right child. The main method returns the larger entry of the root pair.

The invariant is that each returned pair is final and describes only the subtree of that node. A parent never revisits a child. The recursion depth equals the tree height, which the constraints cap at 1000. The solution also contains the direct recursion from the lesson, to count its calls.

**Complexity.**
- **Time** is O(n) for n nodes, because each node is visited once and combines two pairs in constant time.
- **Space** is O(h) for the call stack on a tree of height h, plus a constant-size pair per active call.

```java run
import java.util.*;

public final class DpHouseRobberThree {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    /**
     * Returns the largest total of nodes where no chosen node is the parent of another.
     * Time: O(n). Space: O(h).
     * Invariant: the pair of a subtree is final before its parent reads it.
     */
    static int rob(Node root) {
        // The root pair covers the whole tree, and the better entry is the answer.
        int[] pair = pairOf(root);
        return Math.max(pair[0], pair[1]);
    }

    /** Returns {take, skip} for the subtree of node. Time: O(size). Space: O(height). */
    static int[] pairOf(Node node) {
        // A missing subtree adds nothing in either case.
        if (node == null) return new int[] {0, 0};
        // Children finish first, so their pairs are final.
        int[] left = pairOf(node.left);
        int[] right = pairOf(node.right);
        // Choosing node forces both children into their skip totals.
        int take = node.val + left[1] + right[1];
        // Leaving node out lets each child pick its better case.
        int skip = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
        return new int[] {take, skip};
    }

    static long calls = 0;

    /** The direct recursion from the lesson, with a call counter. */
    static int direct(Node node) {
        calls++;
        if (node == null) return 0;
        int withNode = node.val;
        if (node.left != null) withNode += direct(node.left.left) + direct(node.left.right);
        if (node.right != null) withNode += direct(node.right.left) + direct(node.right.right);
        int withoutNode = direct(node.left) + direct(node.right);
        return Math.max(withNode, withoutNode);
    }

    /** Builds a tree from a level-order list where null marks a missing child. */
    static Node fromLevels(Integer[] a) {
        if (a.length == 0 || a[0] == null) return null;
        Node root = new Node(a[0]);
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        int i = 1;
        while (!queue.isEmpty() && i < a.length) {
            Node cur = queue.poll();
            if (i < a.length && a[i] != null) { cur.left = new Node(a[i]); queue.add(cur.left); }
            i++;
            if (i < a.length && a[i] != null) { cur.right = new Node(a[i]); queue.add(cur.right); }
            i++;
        }
        return root;
    }

    /** Oracle: lists every node, then tries all subsets and rejects parent-child pairs. */
    static int oracle(Node root) {
        List<Node> nodes = new ArrayList<>();
        Map<Node, Node> parentOf = new IdentityHashMap<>();
        ArrayDeque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            nodes.add(cur);
            if (cur.left != null) { parentOf.put(cur.left, cur); stack.push(cur.left); }
            if (cur.right != null) { parentOf.put(cur.right, cur); stack.push(cur.right); }
        }
        int n = nodes.size();
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            Set<Node> chosen = Collections.newSetFromMap(new IdentityHashMap<>());
            int sum = 0;
            for (int k = 0; k < n; k++) if ((mask >> k & 1) == 1) { chosen.add(nodes.get(k)); sum += nodes.get(k).val; }
            boolean ok = true;
            for (Node c : chosen) if (chosen.contains(parentOf.get(c))) ok = false;
            if (ok) best = Math.max(best, sum);
        }
        return best;
    }

    static Node randomTree(Random rnd, int n, int lo, int hi) {
        if (n == 0) return null;
        Node root = new Node(lo + rnd.nextInt(hi - lo + 1));
        List<Node> open = new ArrayList<>();
        open.add(root);
        for (int made = 1; made < n; ) {
            Node p = open.get(rnd.nextInt(open.size()));
            Node c = new Node(lo + rnd.nextInt(hi - lo + 1));
            if (rnd.nextBoolean()) { if (p.left == null) p.left = c; else if (p.right == null) p.right = c; else continue; }
            else { if (p.right == null) p.right = c; else if (p.left == null) p.left = c; else continue; }
            open.add(c);
            made++;
        }
        return root;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (rob(fromLevels(new Integer[] {5, 4, 3, 2, 1})) != 8) throw new AssertionError("ex1");
        if (rob(fromLevels(new Integer[] {4, 1, null, 2, null, 3})) != 7) throw new AssertionError("ex2");
        // The opening example of the lesson: a manager of weight 5 with two reports of weight 4.
        if (rob(fromLevels(new Integer[] {5, 4, 4})) != 8) throw new AssertionError("opening");
        // The two traced trees of the lesson, written in level order.
        if (rob(fromLevels(new Integer[] {6, 2, 5, 4, 1, null, 3})) != 14) throw new AssertionError("trace1");
        if (rob(fromLevels(new Integer[] {2, 1, 3, null, 4})) != 7) throw new AssertionError("trace2");
        // The direct recursion makes 7049153 calls on a chain of 30 nodes, and the pair method visits each node once.
        Node chain = null;
        for (int i = 0; i < 30; i++) { Node c = new Node(1); c.left = chain; chain = c; }
        calls = 0;
        int directAnswer = direct(chain);
        if (calls != 7049153L) throw new AssertionError("calls " + calls);
        if (directAnswer != rob(chain) || directAnswer != 15) throw new AssertionError("chain answer");
        // A chain of one million nodes overflows the call stack of the recursive helper.
        Node deep = null;
        for (int i = 0; i < 1000000; i++) { Node c = new Node(1); c.left = deep; deep = c; }
        boolean overflow = false;
        try { rob(deep); } catch (StackOverflowError e) { overflow = true; }
        if (!overflow) throw new AssertionError("expected stack overflow");
        // The input tree is not modified by the pair computation.
        Node t = fromLevels(new Integer[] {3, 1, 2});
        rob(t);
        if (t.val != 3 || t.left.val != 1 || t.right.val != 2) throw new AssertionError("mutated");
        // Random trees with non-negative values against the subset oracle.
        Random rnd = new Random(2932);
        for (int k = 0; k < 1500; k++) {
            Node tree = randomTree(rnd, 1 + rnd.nextInt(11), 0, 9);
            if (rob(tree) != oracle(tree)) throw new AssertionError("random " + k);
        }
    }
}
```

#### Solution: [Boundary] Null And Negative Values (Author exercise)
<!-- id: dp29-null-and-negative -->

**Approach.**
The helper returns `{take, skip}` for each subtree and returns `{0, 0}` for a `null` node. The take total adds the node value to the skip totals of both children. The skip total adds the better case of each child. A negative value can make a take total negative, but the skip total of any subtree is at least 0, because a leaf has skip 0 and each combination adds non-negative terms. The skip total therefore always allows the empty choice, and the answer, which is the larger entry of the root pair, is at least 0. An empty tree returns 0 at once.

The invariant is that the pair of a subtree is final and that skip is never negative. A different neutral value breaks it. If a missing child returned `Integer.MIN_VALUE` as its take total, a parent that adds two of them overflows to 0 and gives a wrong answer, which is why the neutral pair uses 0.

**Complexity.**
- **Time** is O(n) for n nodes, because each node is visited once and combines two pairs in constant time.
- **Space** is O(h) for the call stack on a tree of height h.

```java run
import java.util.*;

public final class DpNullAndNegative {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    /**
     * Returns the largest total of a valid set of nodes, where the empty set counts as 0.
     * Time: O(n). Space: O(h).
     * Invariant: each skip total is at least 0, because the empty set is allowed.
     */
    static int bestSet(Node root) {
        // A null root has the neutral pair, so the answer is 0.
        int[] pair = pairOf(root);
        return Math.max(pair[0], pair[1]);
    }

    /** Returns {take, skip} for the subtree of node. Time: O(size). Space: O(height). */
    static int[] pairOf(Node node) {
        // A missing subtree has no nodes, so both totals are 0.
        if (node == null) return new int[] {0, 0};
        int[] left = pairOf(node.left);
        int[] right = pairOf(node.right);
        // A chosen node blocks both children, so their skip totals add to its value.
        int take = node.val + left[1] + right[1];
        // A free node lets each child pick its better case, which can be the empty choice.
        int skip = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
        return new int[] {take, skip};
    }

    static Node fromLevels(Integer[] a) {
        if (a.length == 0 || a[0] == null) return null;
        Node root = new Node(a[0]);
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        int i = 1;
        while (!queue.isEmpty() && i < a.length) {
            Node cur = queue.poll();
            if (i < a.length && a[i] != null) { cur.left = new Node(a[i]); queue.add(cur.left); }
            i++;
            if (i < a.length && a[i] != null) { cur.right = new Node(a[i]); queue.add(cur.right); }
            i++;
        }
        return root;
    }

    /** Oracle: tries every subset of the nodes, including the empty one. */
    static int oracle(Node root) {
        List<Node> nodes = new ArrayList<>();
        Map<Node, Node> parentOf = new IdentityHashMap<>();
        ArrayDeque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);
        while (!stack.isEmpty()) {
            Node cur = stack.pop();
            nodes.add(cur);
            if (cur.left != null) { parentOf.put(cur.left, cur); stack.push(cur.left); }
            if (cur.right != null) { parentOf.put(cur.right, cur); stack.push(cur.right); }
        }
        int n = nodes.size();
        int best = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            Set<Node> chosen = Collections.newSetFromMap(new IdentityHashMap<>());
            int sum = 0;
            for (int k = 0; k < n; k++) if ((mask >> k & 1) == 1) { chosen.add(nodes.get(k)); sum += nodes.get(k).val; }
            boolean ok = true;
            for (Node c : chosen) if (chosen.contains(parentOf.get(c))) ok = false;
            if (ok) best = Math.max(best, sum);
        }
        return best;
    }

    static Node randomTree(Random rnd, int n, int lo, int hi) {
        if (n == 0) return null;
        Node root = new Node(lo + rnd.nextInt(hi - lo + 1));
        List<Node> open = new ArrayList<>();
        open.add(root);
        for (int made = 1; made < n; ) {
            Node p = open.get(rnd.nextInt(open.size()));
            Node c = new Node(lo + rnd.nextInt(hi - lo + 1));
            if (p.left == null) p.left = c;
            else if (p.right == null) p.right = c;
            else continue;
            open.add(c);
            made++;
        }
        return root;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (bestSet(fromLevels(new Integer[] {-3, -2, -4})) != 0) throw new AssertionError("ex1");
        if (bestSet(fromLevels(new Integer[] {5, -10, 5, -1, 7})) != 12) throw new AssertionError("ex2");
        // A null root and a single negative node both return 0, and a single positive node returns its value.
        if (bestSet(null) != 0) throw new AssertionError("null root");
        if (bestSet(new Node(-9)) != 0) throw new AssertionError("single negative");
        if (bestSet(new Node(9)) != 9) throw new AssertionError("single positive");
        // The neutral pair is two zeros, and a negative leaf has take below 0 and skip exactly 0.
        if (!Arrays.equals(pairOf(null), new int[] {0, 0})) throw new AssertionError("neutral");
        if (!Arrays.equals(pairOf(new Node(-4)), new int[] {-4, 0})) throw new AssertionError("negative leaf");
        // Using Integer.MIN_VALUE as the neutral take total overflows when two of them are added.
        if (Integer.MIN_VALUE + Integer.MIN_VALUE != 0) throw new AssertionError("overflow claim");
        // The input tree is not modified.
        Node t = fromLevels(new Integer[] {-1, 2, -3});
        bestSet(t);
        if (t.val != -1 || t.left.val != 2 || t.right.val != -3) throw new AssertionError("mutated");
        // Random trees with values from -6 to 6 against the subset oracle, including empty trees.
        Random rnd = new Random(2933);
        for (int k = 0; k < 2000; k++) {
            Node tree = randomTree(rnd, rnd.nextInt(12), -6, 6);
            if (bestSet(tree) != oracle(tree)) throw new AssertionError("random " + k);
        }
    }
}
```

#### Solution: [Recognize] Rerooted Distance Sums (Author exercise)
<!-- id: dp29-rerooted-distance-sums -->

**Approach.**
The method roots the tree at node 0 and finds a breadth-first order, which lists every parent before its children. The first pass walks that order backward. For each node `v` it computes `size[v]`, the number of nodes in its subtree, and `down[v]`, the sum of distances from `v` to the nodes in its subtree. A child `c` adds `size[c]` to its parent's `down` because every node in the child subtree is one edge farther from the parent, and it adds `down[c]`. The value `down[0]` is already the full answer for node 0.

The second pass walks the order forward and carries the answer from each parent to its children. Moving the root from `p` to a child `c` makes the `size[c]` nodes in the child subtree one edge closer, and it makes the other `n - size[c]` nodes one edge farther. So `ans[c] = ans[p] - size[c] + (n - size[c])`. The invariant is that when the second pass reaches `c`, `ans[p]` is final and `size[c]` is final from the first pass. Both passes use arrays, so no recursion is needed.

**Complexity.**
- **Time** is O(n), because the breadth-first order and the two passes each touch every node and edge once.
- **Space** is O(n) for the adjacency lists, the order and the three arrays.

```java run
import java.util.*;

public final class DpRerootedDistanceSums {
    /**
     * Returns, for every node, the sum of its distances to all nodes.
     * Time: O(n). Space: O(n).
     * Invariant: when the downward pass reaches a node, its parent answer is final.
     */
    static int[] distanceSums(int n, int[][] edges) {
        // Adjacency lists give every neighbor of a node in one array slice.
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        // Breadth-first order from node 0 lists every parent before its children.
        int[] order = new int[n];
        int[] parent = new int[n];
        Arrays.fill(parent, -1);
        boolean[] seen = new boolean[n];
        int head = 0, tail = 0;
        order[tail++] = 0;
        seen[0] = true;
        while (head < tail) {
            int v = order[head++];
            for (int c : adj.get(v)) {
                if (seen[c]) continue;
                seen[c] = true;
                parent[c] = v;
                order[tail++] = c;
            }
        }
        // First pass: size[v] counts the subtree nodes and down[v] sums their distances to v.
        int[] size = new int[n];
        int[] down = new int[n];
        Arrays.fill(size, 1);
        for (int k = n - 1; k >= 1; k--) {
            int c = order[k];
            int p = parent[c];
            // Every node in the child subtree is one edge farther from the parent.
            size[p] += size[c];
            down[p] += down[c] + size[c];
        }
        // Second pass: move the root from each parent to each child in order.
        int[] ans = new int[n];
        ans[0] = down[0];
        for (int k = 1; k < n; k++) {
            int c = order[k];
            // size[c] nodes get one edge closer and the other n - size[c] nodes get one edge farther.
            ans[c] = ans[parent[c]] - size[c] + (n - size[c]);
        }
        return ans;
    }

    /** Oracle: runs a breadth-first search from every node and adds the distances. */
    static int[] oracle(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] e : edges) { adj.get(e[0]).add(e[1]); adj.get(e[1]).add(e[0]); }
        int[] out = new int[n];
        for (int s = 0; s < n; s++) {
            int[] d = new int[n];
            Arrays.fill(d, -1);
            d[s] = 0;
            ArrayDeque<Integer> q = new ArrayDeque<>();
            q.add(s);
            while (!q.isEmpty()) {
                int v = q.poll();
                for (int c : adj.get(v)) if (d[c] < 0) { d[c] = d[v] + 1; q.add(c); }
            }
            for (int x : d) out[s] += x;
        }
        return out;
    }

    public static void main(String[] args) {
        // The two examples of the exercise.
        if (!Arrays.equals(distanceSums(4, new int[][] {{0, 1}, {0, 2}, {2, 3}}), new int[] {4, 6, 4, 6})) throw new AssertionError("ex1");
        if (!Arrays.equals(distanceSums(5, new int[][] {{0, 1}, {1, 2}, {2, 3}, {3, 4}}), new int[] {10, 7, 6, 7, 10})) throw new AssertionError("ex2");
        // One node has sum 0, and two nodes have sum 1 each.
        if (!Arrays.equals(distanceSums(1, new int[][] {}), new int[] {0})) throw new AssertionError("single");
        if (!Arrays.equals(distanceSums(2, new int[][] {{1, 0}}), new int[] {1, 1})) throw new AssertionError("pair");
        // The largest allowed chain keeps every sum inside int: the end sum is 10000 * 9999 / 2.
        int n = 10000;
        int[][] chain = new int[n - 1][];
        for (int i = 0; i < n - 1; i++) chain[i] = new int[] {i, i + 1};
        int[] big = distanceSums(n, chain);
        if (big[0] != 49995000 || big[n - 1] != 49995000) throw new AssertionError("big chain");
        // The edge list is not modified.
        int[][] edges = {{0, 1}, {1, 2}};
        distanceSums(3, edges);
        if (!Arrays.deepEquals(edges, new int[][] {{0, 1}, {1, 2}})) throw new AssertionError("mutated");
        // Random trees, with random labels, against the search from every node.
        Random rnd = new Random(2934);
        for (int t = 0; t < 2000; t++) {
            int m = 1 + rnd.nextInt(12);
            int[] label = new int[m];
            for (int i = 0; i < m; i++) label[i] = i;
            for (int i = m - 1; i > 0; i--) { int j = rnd.nextInt(i + 1); int tmp = label[i]; label[i] = label[j]; label[j] = tmp; }
            int[][] es = new int[m - 1][];
            for (int i = 1; i < m; i++) es[i - 1] = new int[] {label[i], label[rnd.nextInt(i)]};
            if (!Arrays.equals(distanceSums(m, es), oracle(m, es))) throw new AssertionError("random " + t);
        }
    }
}
```
