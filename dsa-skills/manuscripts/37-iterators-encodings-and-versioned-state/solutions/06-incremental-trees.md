<!-- solutions-for: 06-incremental-trees -->
### Solutions For Tree Method Calls

#### Solution: [Build] Complete Binary Tree Inserter (LeetCode 919)
<!-- id: it37-complete-tree-inserter -->

**Approach.**
The class stores the root and a queue named `frontier`. The queue holds every node with fewer than two children, in level order. In a complete tree these nodes form the tail of the level order, so the head is always the parent of the next insertion. The constructor builds the queue with one level-order walk. The method `insert` reads the head and fills its left slot when that slot is empty. Otherwise it fills the right slot and removes the head, because the head now has two children. In both cases the new leaf joins the back of the queue, because it has two open slots.

The invariant is that the queue equals the list of nodes with fewer than two children in level order after the constructor and after every insert. An insert keeps the invariant because it removes the one node that became full and appends the one node that appeared. The new node belongs after all older nodes in level order. The program checks the claim against the naive walk from the lesson on random complete trees and against a plain list that appends each value.

**Complexity.**
- **Time** is O(n) for the constructor on `n` nodes and O(1) per insert, since an insert touches one head, one new node and one queue end.
- **Space** is O(n) for the queue, which holds about half of the nodes, plus the O(1) extra work per call.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class CompleteTreeInserterBuild {
    /** Linked binary tree node. */
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /** Inserter that keeps the nodes with an open child slot in level order. */
    static final class CBTInserter {
        private final TreeNode root;
        private final ArrayDeque<TreeNode> frontier = new ArrayDeque<>();

        /**
         * Reads the tree once and stores every node with fewer than two children.
         * Time: O(n). Space: O(n).
         * Invariant: frontier lists exactly the nodes with an open slot, in level order.
         */
        CBTInserter(TreeNode root) {
            // The root stays fixed because inserts only add leaves.
            this.root = root;
            ArrayDeque<TreeNode> walk = new ArrayDeque<>();
            // The level-order walk starts at the root and visits each node once.
            walk.add(root);
            while (!walk.isEmpty()) {
                // Each loop pass removes one node, so the loop runs n times.
                TreeNode node = walk.poll();
                // Children are queued so that the walk follows level order.
                if (node.left != null) walk.add(node.left);
                if (node.right != null) walk.add(node.right);
                // A node with an open slot joins the frontier in level order.
                if (node.left == null || node.right == null) frontier.add(node);
            }
        }

        /**
         * Adds a leaf at the first free position in level order and returns the parent value.
         * Time: O(1). Space: O(1) extra.
         * Invariant: the one node that becomes full leaves the frontier and the new leaf joins it.
         */
        int insert(int val) {
            // The head is the parent of the next position in level order.
            TreeNode parent = frontier.peek();
            // The new leaf has no children yet.
            TreeNode fresh = new TreeNode(val);
            if (parent.left == null) {
                // An empty left slot takes the child, and the parent keeps one open slot.
                parent.left = fresh;
            } else {
                // The right slot fills the parent, so the parent leaves the frontier.
                parent.right = fresh;
                frontier.poll();
            }
            // The leaf has two open slots and belongs after all older nodes.
            frontier.add(fresh);
            // The caller receives the value of the node that gained a child.
            return parent.val;
        }

        /** Returns the root. Time: O(1). Space: O(1). */
        TreeNode getRoot() {
            // The root never changes, so the caller always sees the same object.
            return root;
        }
    }

    /** Oracle: the naive walk from the lesson, restarted from the root at every call. */
    static int naiveInsert(TreeNode root, int val) {
        ArrayDeque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (true) {
            TreeNode node = queue.poll();
            if (node.left == null) { node.left = new TreeNode(val); return node.val; }
            if (node.right == null) { node.right = new TreeNode(val); return node.val; }
            queue.add(node.left);
            queue.add(node.right);
        }
    }

    static TreeNode build(int[] values) {
        TreeNode[] nodes = new TreeNode[values.length];
        for (int i = 0; i < values.length; i++) nodes[i] = new TreeNode(values[i]);
        for (int i = 0; i < values.length; i++) {
            if (2 * i + 1 < values.length) nodes[i].left = nodes[2 * i + 1];
            if (2 * i + 2 < values.length) nodes[i].right = nodes[2 * i + 2];
        }
        return nodes[0];
    }

    static List<Integer> levelOrder(TreeNode root) {
        List<Integer> out = new ArrayList<>();
        ArrayDeque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            out.add(node.val);
            if (node.left != null) queue.add(node.left);
            if (node.right != null) queue.add(node.right);
        }
        return out;
    }

    public static void main(String[] args) {
        // Example 1: parents 3 and 8, final level order of six values.
        CBTInserter a = new CBTInserter(build(new int[] {5, 3, 8, 1}));
        if (a.insert(9) != 3 || a.insert(4) != 8) throw new AssertionError("example 1 parents");
        if (!levelOrder(a.getRoot()).equals(List.of(5, 3, 8, 1, 9, 4))) throw new AssertionError("example 1 tree");
        // Example 2: a single node takes two children, then the next level starts.
        CBTInserter b = new CBTInserter(build(new int[] {7}));
        if (b.insert(2) != 7 || b.insert(6) != 7 || b.insert(1) != 2) throw new AssertionError("example 2 parents");
        if (!levelOrder(b.getRoot()).equals(List.of(7, 2, 6, 1))) throw new AssertionError("example 2 tree");
        // The lesson trace: the tree 1,2,3 grows to 1..8 and the parents follow (n - 1) / 2.
        CBTInserter c = new CBTInserter(build(new int[] {1, 2, 3}));
        int[] expectedParents = {2, 2, 3, 3, 4};
        for (int v = 4; v <= 8; v++) {
            if (c.insert(v) != expectedParents[v - 4]) throw new AssertionError("trace parent " + v);
        }
        // Random complete trees: the frontier class agrees with the naive walk and with a list model.
        Random rnd = new Random(3706L);
        for (int t = 0; t < 2000; t++) {
            int size = 1 + rnd.nextInt(20);
            int[] start = new int[size];
            List<Integer> model = new ArrayList<>();
            for (int i = 0; i < size; i++) { start[i] = rnd.nextInt(50); model.add(start[i]); }
            CBTInserter fast = new CBTInserter(build(start));
            TreeNode slowRoot = build(start);
            for (int step = rnd.nextInt(40); step > 0; step--) {
                int val = rnd.nextInt(50);
                int expectedParent = model.get((model.size() - 1) / 2);
                model.add(val);
                // The parent of position n is at (n - 1) / 2 in the array layout.
                int fastParent = fast.insert(val);
                int slowParent = naiveInsert(slowRoot, val);
                if (fastParent != expectedParent || slowParent != expectedParent) throw new AssertionError("parent");
                if (!levelOrder(fast.getRoot()).equals(model)) throw new AssertionError("level order");
            }
            if (!levelOrder(slowRoot).equals(model)) throw new AssertionError("oracle tree");
        }
    }
}
```

#### Solution: [Vary] Binary Search Tree Iterator II With A Window (LeetCode 1586)
<!-- id: it37-window-bst-iterator -->

**Approach.**
The class combines a stack of unfinished nodes with a ring buffer of size `k`. The stack gives the next larger value, as in a plain inorder iterator. The **left spine** of a node is that node followed by its left child, that child's left child, and so on down to a node with no left child. The call `next` pops a node, pushes the left spine of its right child, and returns the node value. The ring buffer records each produced value at slot `position % k`, where `position` counts the values produced so far. The integer `cur` is the absolute position of the value that the cursor sits on, and it is -1 before the first call.

The state has four values:
- **ring** holds the last `k` produced values, and slot `position % k` holds the value at that position.
- **produced** counts the values taken from the tree so far.
- **cur** is the absolute position under the cursor.
- **oldest retained** is `max(0, produced - k)`, the smallest position whose slot still holds its value.

A call to `next` first checks whether `cur + 1` is below the produced count. If it is, the cursor re-enters a stored value and moves forward without touching the tree. Otherwise the stack produces a new value, which overwrites the oldest slot once `k` values exist. A call to `prev` moves `cur` back by one and reads the ring. The method `hasPrev` is true while `cur - 1` is at least the oldest retained position, which is `max(0, produced - k)`. The invariant says that `cur` lies between the oldest retained position and `produced - 1` after the first call. Every read therefore hits a slot that still holds its value.

Take the tree `[2,1,3]` with `k = 2`. Three calls to `next` return 1, 2 and 3, so `produced` is 3, `cur` is 2 and the ring is `[3,2]`, because the value 3 overwrote the value 1 in slot 0. Now `prev` returns 2 and moves `cur` to 1. The oldest retained position is `3 - 2 = 1`, so `hasPrev` is false, and the value 1 is gone. The program compares the class with a model that keeps an explicit window list on random trees. It also drives a chain of 100 000 nodes, which a recursive traversal could not survive.

**Complexity.**
- **Time** is O(1) amortized per call, because the left-spine pushes across all `next` calls total at most the number of nodes.
- **Space** is O(h + k) for the stack of height `h` and the ring of size `k`.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;

public final class WindowBstIteratorVary {
    /** Linked binary tree node. */
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    /** Inorder iterator with backward steps limited to the last k produced values. */
    static final class WindowBstIterator {
        private final ArrayDeque<TreeNode> stack = new ArrayDeque<>();
        private final int[] ring;
        private final int k;
        private int produced;   // number of values taken from the tree so far
        private int cur = -1;   // absolute position of the value under the cursor

        /**
         * Prepares the left spine of the tree and an empty ring.
         * Time: O(h). Space: O(h + k).
         * Invariant: stack holds the unfinished nodes whose values are larger than every produced value.
         */
        WindowBstIterator(TreeNode root, int k) {
            // The ring size fixes the history bound.
            this.k = k;
            this.ring = new int[k];
            // The smallest value sits at the end of the left spine.
            pushLeft(root);
        }

        private void pushLeft(TreeNode node) {
            // Each node is pushed once over the whole run.
            while (node != null) {
                stack.push(node);
                node = node.left;
            }
        }

        /** Reports whether a larger value exists. Time: O(1). Space: O(1). */
        boolean hasNext() {
            // A stored value ahead of the cursor or an unfinished node both count.
            return cur + 1 < produced || !stack.isEmpty();
        }

        /**
         * Moves the cursor to the next larger value and returns it.
         * Time: O(1) amortized. Space: O(1) extra.
         * Invariant: cur stays between the oldest retained position and produced - 1.
         */
        int next() {
            // The cursor is behind the newest value, so the ring supplies the answer.
            if (cur + 1 < produced) {
                cur++;
                return ring[cur % k];
            }
            // Exhaustion is a caller error, and this class reports it with an exception.
            if (stack.isEmpty()) throw new NoSuchElementException();
            // The stack top is the smallest value not yet produced.
            TreeNode node = stack.pop();
            // The right subtree holds the values that follow this node.
            pushLeft(node.right);
            // The new value overwrites the oldest slot once the ring is full.
            ring[produced % k] = node.val;
            produced++;
            cur++;
            return node.val;
        }

        /** Reports whether an older retained value exists. Time: O(1). Space: O(1). */
        boolean hasPrev() {
            // Positions below produced - k were overwritten, and position 0 has no predecessor.
            return cur - 1 >= Math.max(0, produced - k);
        }

        /**
         * Moves the cursor to the previous retained value and returns it.
         * Time: O(1). Space: O(1).
         * Invariant: the target position is inside the retained window, so its slot is intact.
         */
        int prev() {
            // A step past the window is a caller error.
            if (!hasPrev()) throw new NoSuchElementException();
            // Moving back changes only the cursor, not the tree state.
            cur--;
            return ring[cur % k];
        }
    }

    /** Oracle: sorted array plus an explicit list of the last k values. */
    static final class Model {
        private final int[] sorted;
        private final int k;
        private final List<Integer> window = new ArrayList<>();
        private int taken;
        private int cur = -1;
        Model(int[] sorted, int k) { this.sorted = sorted; this.k = k; }
        boolean hasNext() { return cur + 1 < window.size() || taken < sorted.length; }
        int next() {
            if (cur + 1 < window.size()) { cur++; return window.get(cur); }
            window.add(sorted[taken++]);
            if (window.size() > k) window.remove(0);
            cur = window.size() - 1;
            return window.get(cur);
        }
        boolean hasPrev() { return cur >= 1; }
        int prev() { cur--; return window.get(cur); }
    }

    static TreeNode insert(TreeNode root, int v) {
        if (root == null) return new TreeNode(v);
        TreeNode node = root;
        while (true) {
            if (v < node.val) { if (node.left == null) { node.left = new TreeNode(v); break; } node = node.left; }
            else { if (node.right == null) { node.right = new TreeNode(v); break; } node = node.right; }
        }
        return root;
    }

    static TreeNode fromLevels(Integer[] levels) {
        TreeNode[] nodes = new TreeNode[levels.length];
        for (int i = 0; i < levels.length; i++) if (levels[i] != null) nodes[i] = new TreeNode(levels[i]);
        int child = 1;
        for (int i = 0; i < levels.length && child < levels.length; i++) {
            if (nodes[i] == null) continue;
            nodes[i].left = nodes[child++];
            if (child < levels.length) nodes[i].right = nodes[child++];
        }
        return nodes[0];
    }

    public static void main(String[] args) {
        // Example 1: window of 3 over 1..7, 1 falls out of the window after the fourth next.
        WindowBstIterator it = new WindowBstIterator(fromLevels(new Integer[] {4, 2, 6, 1, 3, 5, 7}), 3);
        int[] firstFour = {it.next(), it.next(), it.next(), it.next()};
        if (!Arrays.equals(firstFour, new int[] {1, 2, 3, 4}) || !it.hasPrev()) throw new AssertionError("example 1 forward");
        if (it.prev() != 3 || it.prev() != 2 || it.hasPrev()) throw new AssertionError("example 1 backward");
        if (it.next() != 3 || it.next() != 4 || it.next() != 5 || !it.hasNext()) throw new AssertionError("example 1 replay");
        if (it.next() != 6 || !it.hasNext()) throw new AssertionError("example 1 tail");
        // Example 2: a window of 1 never allows a step back.
        WindowBstIterator one = new WindowBstIterator(fromLevels(new Integer[] {5, 2, 9}), 1);
        if (one.next() != 2 || one.next() != 5 || one.hasPrev() || !one.hasNext()) throw new AssertionError("example 2 start");
        if (one.next() != 9 || one.hasNext() || one.hasPrev()) throw new AssertionError("example 2 end");
        // Exhausted next and an illegal prev throw NoSuchElementException in this class.
        try { one.next(); throw new AssertionError("next should throw"); } catch (NoSuchElementException expected) { }
        try { one.prev(); throw new AssertionError("prev should throw"); } catch (NoSuchElementException expected) { }
        // Random trees and random call sequences agree with the model on every answer.
        Random rnd = new Random(3707L);
        for (int t = 0; t < 2000; t++) {
            int n = 1 + rnd.nextInt(15);
            boolean[] used = new boolean[60];
            TreeNode root = null;
            int count = 0;
            while (count < n) {
                int v = rnd.nextInt(60);
                if (used[v]) continue;
                used[v] = true;
                root = insert(root, v);
                count++;
            }
            int[] sorted = new int[n];
            int idx = 0;
            for (int v = 0; v < 60; v++) if (used[v]) sorted[idx++] = v;
            int k = 1 + rnd.nextInt(5);
            WindowBstIterator real = new WindowBstIterator(root, k);
            Model model = new Model(sorted, k);
            for (int step = 0; step < 40; step++) {
                // Both classes must agree on availability before the caller chooses a move.
                if (real.hasNext() != model.hasNext() || real.hasPrev() != model.hasPrev()) throw new AssertionError("availability");
                int op = rnd.nextInt(2);
                if (op == 0 && model.hasNext()) { if (real.next() != model.next()) throw new AssertionError("next"); }
                if (op == 1 && model.hasPrev()) { if (real.prev() != model.prev()) throw new AssertionError("prev"); }
            }
        }
        // A left chain of 100 000 nodes would overflow a recursive traversal; the explicit stack handles it.
        TreeNode chain = null;
        for (int v = 0; v < 100_000; v++) { TreeNode top = new TreeNode(v); top.left = chain; chain = top; }
        WindowBstIterator deep = new WindowBstIterator(chain, 2);
        for (int v = 0; v < 100_000; v++) if (deep.next() != v) throw new AssertionError("deep chain " + v);
        if (deep.hasNext() || deep.prev() != 99_998) throw new AssertionError("deep end");
    }
}
```

#### Solution: [Boundary] Find Elements In A Contaminated Binary Tree (LeetCode 1261)
<!-- id: it37-contaminated-tree-find -->

**Approach.**
The stored values carry no information, so the class rebuilds the original numbering from the shape. The root gets 0, a left child of `x` gets `2x + 1`, and a right child gets `2x + 2`. The constructor walks the tree with an explicit stack of node and value pairs and stores each recovered value in a hash set. Then `find` is one set lookup. All arithmetic uses `long`, because a left-right path of depth 58 produces values near `2^59`, which exceeds the `int` range.

A second method needs no constructor work at all. Add 1 to the target. The bits of `target + 1` after the leading 1 spell the path from the root, where 0 means left and 1 means right. This works because the left child gives `(2x + 1) + 1 = 2(x + 1)` and the right child gives `(2x + 2) + 1 = 2(x + 1) + 1`. Each step appends one bit to `x + 1`. The invariant is that every node's recovered value plus 1 equals the binary number formed by its path bits after a leading 1. The program checks the set, the bit path and a recursive brute force against each other on random shapes. It also checks deep chains whose values exceed the `int` range.

**Complexity.**
- **Time** is O(n) for the constructor and O(1) expected per set lookup, or O(h) per bit-path lookup with no constructor work.
- **Space** is O(n) for the set, or O(1) extra for the bit path, plus the O(h) stack during the constructor walk.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

public final class ContaminatedTreeFindBoundary {
    /** Binary tree node whose stored value is always -1. */
    static final class TreeNode {
        int val = -1;
        TreeNode left, right;
    }

    /** Rebuilds the original values from the tree shape. */
    static final class FindElements {
        private final TreeNode root;
        private final Set<Long> seen = new HashSet<>();

        /**
         * Recovers the value of every node with an explicit stack.
         * Time: O(n). Space: O(n) for the set plus O(h) for the stack.
         * Invariant: each stack entry carries the original value of its node.
         */
        FindElements(TreeNode root) {
            // The root is kept for the path method.
            this.root = root;
            ArrayDeque<TreeNode> nodes = new ArrayDeque<>();
            ArrayDeque<Long> values = new ArrayDeque<>();
            // The root had value 0 before the contamination.
            nodes.push(root);
            values.push(0L);
            while (!nodes.isEmpty()) {
                // Each node leaves the stack once, so the loop runs n times.
                TreeNode node = nodes.pop();
                long x = values.pop();
                // The recovered value is remembered for later queries.
                seen.add(x);
                // A left child had value 2x + 1, computed in long arithmetic.
                if (node.left != null) { nodes.push(node.left); values.push(2 * x + 1); }
                // A right child had value 2x + 2.
                if (node.right != null) { nodes.push(node.right); values.push(2 * x + 2); }
            }
        }

        /** Looks the target up in the recovered set. Time: O(1) expected. Space: O(1). */
        boolean find(long target) {
            // Membership in the set equals existence of a node with that original value.
            return seen.contains(target);
        }

        /**
         * Follows the bits of target + 1 from the root without any stored set.
         * Time: O(h). Space: O(1).
         * Invariant: after processing the high bits, the node holds the value for that bit prefix.
         */
        boolean findByPath(long target) {
            // Adding 1 turns the numbering into a binary heap numbering whose path is the bit string.
            long x = target + 1;
            // The position of the leading 1 tells how many turns the path has.
            int top = 63 - Long.numberOfLeadingZeros(x);
            TreeNode node = root;
            for (int bit = top - 1; bit >= 0; bit--) {
                // A 0 bit turns left and a 1 bit turns right.
                node = ((x >> bit) & 1L) == 0 ? node.left : node.right;
                // A missing child means no node has this value.
                if (node == null) return false;
            }
            // Every turn found a node, so the target exists.
            return true;
        }
    }

    /** Oracle: recursive recovery into a list, then a linear scan. */
    static void collect(TreeNode node, long x, List<Long> out) {
        if (node == null) return;
        out.add(x);
        collect(node.left, 2 * x + 1, out);
        collect(node.right, 2 * x + 2, out);
    }

    static TreeNode randomShape(Random rnd, int depth) {
        if (depth == 0 || rnd.nextInt(4) == 0) return null;
        TreeNode node = new TreeNode();
        node.left = randomShape(rnd, depth - 1);
        node.right = randomShape(rnd, depth - 1);
        return node;
    }

    static TreeNode fromLevels(Integer[] levels) {
        TreeNode[] nodes = new TreeNode[levels.length];
        for (int i = 0; i < levels.length; i++) if (levels[i] != null) nodes[i] = new TreeNode();
        int child = 1;
        for (int i = 0; i < levels.length && child < levels.length; i++) {
            if (nodes[i] == null) continue;
            nodes[i].left = nodes[child++];
            if (child < levels.length) nodes[i].right = nodes[child++];
        }
        return nodes[0];
    }

    public static void main(String[] args) {
        // Example 1: five nodes recovered as 0..4, so 5 is absent.
        FindElements a = new FindElements(fromLevels(new Integer[] {-1, -1, -1, -1, -1}));
        if (!a.find(1) || !a.find(3) || a.find(5)) throw new AssertionError("example 1");
        // Example 2: a right-going chain recovers 0, 2, 6.
        FindElements b = new FindElements(fromLevels(new Integer[] {-1, null, -1, null, -1}));
        if (!b.find(2) || b.find(1) || !b.find(6) || b.find(5)) throw new AssertionError("example 2");
        // Random shapes: the set, the bit path and the recursive oracle agree for every small target.
        Random rnd = new Random(3708L);
        for (int t = 0; t < 2000; t++) {
            TreeNode root = new TreeNode();
            root.left = randomShape(rnd, 5);
            root.right = randomShape(rnd, 5);
            List<Long> truth = new ArrayList<>();
            collect(root, 0L, truth);
            FindElements fe = new FindElements(root);
            for (long target = 0; target < 70; target++) {
                boolean expected = truth.contains(target);
                if (fe.find(target) != expected || fe.findByPath(target) != expected) throw new AssertionError("target " + target);
            }
        }
        // A right chain of depth 50 holds the value 2^51 - 2, which does not fit in int.
        TreeNode chain = new TreeNode();
        TreeNode tail = chain;
        for (int d = 0; d < 50; d++) { tail.right = new TreeNode(); tail = tail.right; }
        FindElements deep = new FindElements(chain);
        long big = (1L << 51) - 2;
        if ((int) big == big) throw new AssertionError("value should exceed int");
        if (!deep.find(big) || !deep.findByPath(big) || deep.find(big - 1) || deep.findByPath(big - 1)) throw new AssertionError("deep chain");
        // The upper limit of the target range does not overflow target + 1.
        if (deep.findByPath(1_000_000_000_000_000_000L)) throw new AssertionError("limit target");
    }
}
```

#### Solution: [Recognize] Operations On Tree (LeetCode 1993)
<!-- id: it37-operations-on-tree -->

**Approach.**
This transfer problem asks the same question as the lesson: which stored structures keep each method cheap, and when may a method mutate? Two structures serve the three calls. The `parent` array answers the ancestor test by climbing from the node to the root. A list of children per node answers the descendant search with an explicit stack. An array `owner` stores the user who holds each lock, with 0 meaning unlocked.

The calls `lock` and `unlock` read and write one entry of `owner`. The call `upgrade` runs its three tests in order of cost and collects the locked descendants into a list without changing anything. Only after the ancestor test passes and the list is non-empty does it clear those entries and lock the node. The invariant says that only a call returning `true` changes `owner`. A refusal therefore leaves the whole structure intact. Three review notes help in an interview. Descendants exclude the node itself. A locked descendant under a locked ancestor can exist, because `lock` tests only the node. The climb costs O(depth), while the search costs O(subtree size). The program compares the class with an oracle that precomputes every ancestor relation in a matrix and scans all nodes for each call.

**Complexity.**
- **Time** is O(1) for `lock` and `unlock`, and O(depth + size of the subtree) for `upgrade`, which is O(n) in the worst case.
- **Space** is O(n) for the parent array, the child lists and the owner array.

```java run
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public final class OperationsOnTreeRecognize {
    /** Tree with per-node locks. */
    static final class LockingTree {
        private final int[] parent;
        private final List<List<Integer>> children = new ArrayList<>();
        private final int[] owner;   // 0 means unlocked, otherwise the user id

        /**
         * Builds child lists from the parent array.
         * Time: O(n). Space: O(n).
         * Invariant: children.get(p) lists exactly the nodes whose parent is p.
         */
        LockingTree(int[] parent) {
            // The parent array is kept for the upward climb.
            this.parent = parent;
            this.owner = new int[parent.length];
            for (int i = 0; i < parent.length; i++) children.add(new ArrayList<>());
            // Each node registers once under its parent.
            for (int i = 0; i < parent.length; i++) if (parent[i] >= 0) children.get(parent[i]).add(i);
        }

        /** Locks an unlocked node. Time: O(1). Space: O(1). */
        boolean lock(int num, int user) {
            // A held lock refuses, and nothing changes.
            if (owner[num] != 0) return false;
            // The user takes the lock.
            owner[num] = user;
            return true;
        }

        /** Unlocks a node held by the same user. Time: O(1). Space: O(1). */
        boolean unlock(int num, int user) {
            // Users are at least 1, so an unlocked node (owner 0) never matches.
            if (owner[num] != user) return false;
            // The entry returns to the unlocked value.
            owner[num] = 0;
            return true;
        }

        /**
         * Locks a node and clears its locked descendants when the three conditions hold.
         * Time: O(depth + subtree). Space: O(subtree).
         * Invariant: no entry of owner changes until every test has passed.
         */
        boolean upgrade(int num, int user) {
            // Condition 1: the node itself is unlocked.
            if (owner[num] != 0) return false;
            // Condition 3: no ancestor is locked, found by climbing to the root.
            for (int a = parent[num]; a != -1; a = parent[a]) if (owner[a] != 0) return false;
            // Condition 2: collect locked descendants with an explicit stack and no mutation.
            List<Integer> locked = new ArrayList<>();
            ArrayDeque<Integer> stack = new ArrayDeque<>(children.get(num));
            while (!stack.isEmpty()) {
                // Each descendant leaves the stack once.
                int node = stack.pop();
                if (owner[node] != 0) locked.add(node);
                stack.addAll(children.get(node));
            }
            // With no locked descendant the call refuses.
            if (locked.isEmpty()) return false;
            // All tests passed, so the mutations begin now.
            for (int node : locked) owner[node] = 0;
            owner[num] = user;
            return true;
        }
    }

    /** Oracle: full ancestor matrix, then scans over all nodes for every call. */
    static final class Model {
        private final boolean[][] below;   // below[a][d] is true when d is a strict descendant of a
        private final int[] owner;
        Model(int[] parent) {
            int n = parent.length;
            below = new boolean[n][n];
            owner = new int[n];
            for (int d = 0; d < n; d++) for (int a = parent[d]; a != -1; a = parent[a]) below[a][d] = true;
        }
        boolean lock(int num, int user) { if (owner[num] != 0) return false; owner[num] = user; return true; }
        boolean unlock(int num, int user) { if (owner[num] != user) return false; owner[num] = 0; return true; }
        boolean upgrade(int num, int user) {
            if (owner[num] != 0) return false;
            boolean lockedAbove = false, lockedBelow = false;
            for (int x = 0; x < owner.length; x++) {
                if (below[x][num] && owner[x] != 0) lockedAbove = true;
                if (below[num][x] && owner[x] != 0) lockedBelow = true;
            }
            if (lockedAbove || !lockedBelow) return false;
            for (int x = 0; x < owner.length; x++) if (below[num][x]) owner[x] = 0;
            owner[num] = user;
            return true;
        }
    }

    public static void main(String[] args) {
        // Example 1: upgrading the root clears the locked nodes 1 and 5, and node 0 then refuses a second upgrade.
        LockingTree a = new LockingTree(new int[] {-1, 0, 0, 0, 1, 1, 3});
        boolean[] got1 = {a.lock(4, 7), a.upgrade(1, 2), a.lock(5, 3), a.upgrade(0, 4), a.unlock(1, 2), a.unlock(1, 4), a.lock(3, 3), a.upgrade(0, 5)};
        boolean[] want1 = {true, true, true, true, false, false, true, false};
        for (int i = 0; i < want1.length; i++) if (got1[i] != want1[i]) throw new AssertionError("example 1 call " + i);
        // Example 2: a locked ancestor blocks the upgrade, and later an empty subtree blocks it.
        LockingTree b = new LockingTree(new int[] {-1, 0, 1, 2});
        boolean[] got2 = {b.lock(2, 1), b.lock(0, 1), b.upgrade(1, 2), b.unlock(2, 1), b.upgrade(1, 2), b.unlock(1, 2)};
        boolean[] want2 = {true, true, false, true, false, false};
        for (int i = 0; i < want2.length; i++) if (got2[i] != want2[i]) throw new AssertionError("example 2 call " + i);
        // A refused upgrade leaves every lock in place.
        LockingTree c = new LockingTree(new int[] {-1, 0, 1});
        c.lock(0, 1);
        c.lock(2, 2);
        if (c.upgrade(1, 3) || c.unlock(2, 2) == false || c.unlock(0, 1) == false) throw new AssertionError("refused upgrade mutated");
        // Random trees and random call sequences agree with the matrix oracle.
        Random rnd = new Random(3709L);
        for (int t = 0; t < 3000; t++) {
            int n = 1 + rnd.nextInt(12);
            int[] parent = new int[n];
            parent[0] = -1;
            for (int i = 1; i < n; i++) parent[i] = rnd.nextInt(i);
            LockingTree real = new LockingTree(parent);
            Model model = new Model(parent);
            for (int step = 0; step < 60; step++) {
                int num = rnd.nextInt(n);
                int user = 1 + rnd.nextInt(3);
                int op = rnd.nextInt(3);
                boolean x, y;
                if (op == 0) { x = real.lock(num, user); y = model.lock(num, user); }
                else if (op == 1) { x = real.unlock(num, user); y = model.unlock(num, user); }
                else { x = real.upgrade(num, user); y = model.upgrade(num, user); }
                if (x != y) throw new AssertionError("op " + op + " node " + num);
            }
        }
    }
}
```
