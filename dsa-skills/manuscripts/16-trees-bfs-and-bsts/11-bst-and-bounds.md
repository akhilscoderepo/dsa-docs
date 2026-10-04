<!-- lesson-kind: combination -->
<!-- lesson-id: bst-and-bounds -->
## BST And Bounds

<!-- stage: context -->
### The Archive Stacks Walker

An archive keeps its boxes in branching stacks, numbered so that every box on the left side below a stack has a smaller number and every box on the right side a larger one. A walker with a cart enters at the top stack, and each time he turns left or right he learns something about the boxes still ahead of him: they all lie between two numbers he has already passed. By the time he reaches the end of his path he has passed a handful of boxes, and he suspects those numbers say a lot more than he has been using them for.

The archivist asks four things of him, one after another. Find a box, and say what it was squeezed between. Check whether the stacks still obey the numbering and, if not, point to the first box that breaks it. Fetch the third box numbered between 40 and 70. And take one box out without leaving a gap in the numbering.

<!-- stage: contributions -->
### What Each Structure Brings

The ordered tree brings the promise. At every stack the left side holds smaller numbers and the right side holds larger ones, so one comparison with a stack's number settles which side to enter, and the numbers of the other side never need to be read. The promise can be used for as long as it is true, and nothing in the tree itself reports whether it still is.

The bounds bring the memory. A pair of numbers, a lower end and an upper end, travels with the walker, and every turn replaces exactly one of them with the number of the stack he has just left. The pair is a precise statement of which numbers are still possible ahead. What the pair lacks is a use: on its own it is two numbers and says nothing about boxes.

The recognition cue is a question about a sorted tree in which the interval of still possible keys, carried from the top, either decides where to walk, flags a violation, filters a band, or limits what can replace a removed key.

<!-- stage: naive -->
### Lay Everything Out In Sorted Order

The direct method takes the whole archive off the stacks and writes the numbers in a sorted list. The first question, finding a box and what it lay between, is answered by scanning that list for the number and reading its neighbours. The third box in a band is found by filtering the list. The list is also easy to test for the numbering, since the numbers must increase.

```java
static List<Integer> flatten(Node stack) {
    List<Integer> out = new ArrayList<>();
    spill(stack, out);
    return out;
}

static void spill(Node n, List<Integer> out) {
    if (n == null) return;
    spill(n.left, out);
    out.add(n.val);
    spill(n.right, out);
}

static Integer[] squeezedBetween(Node root, int key) {
    List<Integer> all = flatten(root);
    Integer lo = null, hi = null;
    boolean found = false;
    for (int x : all) {
        if (x < key) lo = x;
        else if (x == key) found = true;
        else { hi = x; break; }
    }
    return new Integer[] {found ? 1 : 0, lo, hi};
}
```

Because the flattened list holds every number in sorted order, the neighbours it reports are the true ones.

<!-- stage: bottleneck -->
### The Whole Archive For One Answer

Flattening costs O(n) time and O(n) space before a single question is answered, and the same cost is paid for every question. For a million boxes and a million questions the walker would handle a trillion numbers. A removal is worse, since after editing the list the stacks have to be built again from scratch.

Almost all of this work throws away what the stacks already know. A search needs the O(h) boxes along one path, a range question needs only the boxes inside the range plus two boundary paths, and a removal needs only the boxes near the removed one. The list method ignores the numbering promise, so it cannot skip anything. The target is O(h) per search, validation in one O(n) pass that stops at the first violation, a range question in O(h + k), and a removal in O(h).

<!-- stage: insight -->
### The Interval Is A Result As Well

Carry the lower and upper end down the walk, and treat the pair at the moment the walk stops as an answer in itself, the **stopping interval**. When a search ends at an empty place, no number can lie inside the interval, so its two ends are exactly the **neighbour keys** of the missing key, the next lower and the next higher in sorted order. When it ends at the key itself, the ends are the nearest ancestors on either side, and the other neighbours, if any, lie inside the branches of the found stack. The same pair gives every other operation its test.

Validation reads the pair as a demand: each stack must lie strictly inside the interval it arrives with, and the first stack that does not is the first violation in the order of the walk. A band query reads the pair as an overlap test. The **band overlap** rule says that a branch is only worth entering if its interval can meet the band, which is why a stack below the band lets the walk skip its whole left side and a stack above it skips its right side. The count of in-band boxes is done by the same sorted walk as before, with a countdown.

A removal reads the pair as a limit on replacements. A stack with two branches may be overwritten only by a key that keeps the numbering, and the two keys that can do so are its neighbours in sorted order, the largest on its left or the smallest on its right.

The invariant is that the interval carried into a stack describes exactly the numbers that may legally appear in its branch, and every operation either narrows it by one end or tests against it.

<!-- names: stopping interval, neighbour keys, band overlap -->

<!-- stage: variables -->
### Low End, High End And The Band

The ends `lo` and `hi` are `Integer` objects with `null` for an open end when they are returned as an answer, and `long` values when they are used for validation so that no `int` key can equal the sentinel. Each walk step replaces exactly one end by the number of the stack just left, and a call never changes its own copy. A band query adds `low` and `high` as fixed limits, a stack `stack` of nodes whose left sides are pending, and a countdown `k`. The first-violation search remembers each node's position in the input array, so the answer can be a position and not a value, with `-1` meaning that nothing violates.

<!-- stage: trace -->
### Interval Results In Three Walks

The first trace searches for 7 in the stacks 8, 3, 10, 1, 6, null, 14. The marker `node` is on the stack being compared and the variables `lo` and `hi` show the interval after the step. The walk goes left at 8, which sets the upper end to 8, and right at 3 and then at 6, which raise the lower end to 6. It stops below 6 with the interval 6 to 8, and these two ends are the neighbours of the missing 7.

```trace
{"cells":["8","3","10","1","6","null","14"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"lo":"-inf","hi":"8"},"note":"The key 7 is smaller than the stack 8, so the walk goes left and the upper end becomes 8."},{"at":{"node":1},"vars":{"lo":"3","hi":"8"},"note":"The key 7 is larger than the stack 3, so the walk goes right and the lower end becomes 3."},{"at":{"node":4},"vars":{"lo":"6","hi":"8"},"note":"The key 7 is larger than the stack 6, so the walk goes right and the lower end becomes 6."},{"at":{"node":-1},"vars":{"lo":"6","hi":"8"},"note":"The walk leaves the tree here, so nothing can lie between 6 and 8; these are the neighbours of the missing key 7."}]}
```

The second trace validates the stacks 5, 4, 6, null, null, 3, 7 and stops at the first violation. The stack 3 is on the left of 6, so it arrives with the interval from 5 to 6 and fits neither end. Its parent 6 was fine, which is why a local comparison would have missed it.

```trace
{"cells":["5","4","6","null","null","3","7"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"lo":"-inf","hi":"+inf"},"note":"The stack 5 arrives with the interval (-inf, +inf) and fits, so its left side gets (-inf, 5) and its right side gets (5, +inf)."},{"at":{"node":1},"vars":{"lo":"-inf","hi":"5"},"note":"The stack 4 arrives with the interval (-inf, 5) and fits, so its left side gets (-inf, 4) and its right side gets (4, 5)."},{"at":{"node":2},"vars":{"lo":"5","hi":"+inf"},"note":"The stack 6 arrives with the interval (5, +inf) and fits, so its left side gets (5, 6) and its right side gets (6, +inf)."},{"at":{"node":5},"vars":{"lo":"5","hi":"6"},"note":"The stack 3 arrives with the interval (5, 6) and does not fit, so the first violation is at position 5 and the walk stops."}]}
```

The third trace fetches the third key in the band from 5 to 12 on a complete archive of fifteen boxes. The marker `node` is on each box popped from the stack of pending left sides. Boxes below 5 never go on the stack, and the third pop in the band is 7.

```trace
{"cells":["8","4","12","2","6","10","14","1","3","5","7","9","11","13","15"],"pointers":["node"],"steps":[{"at":{"node":9},"vars":{"countdown":2,"stack":"6 8"},"note":"The box 5 is popped inside the band, so the countdown becomes 2."},{"at":{"node":4},"vars":{"countdown":1,"stack":"8"},"note":"The box 6 is popped inside the band, so the countdown becomes 1."},{"at":{"node":10},"vars":{"countdown":0,"stack":"8"},"note":"The box 7 is popped inside the band, so the countdown becomes 0. The countdown is zero, so 7 is the answer."}]}
```

<!-- stage: code -->
### Four Walks That Share One Interval

```java
final class BoundsToolkit {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static Integer[] stopInterval(Node root, int key) {
        Integer lo = null, hi = null;
        Node node = root;
        while (node != null && node.val != key) {
            if (key < node.val) { hi = node.val; node = node.left; }
            else { lo = node.val; node = node.right; }
        }
        return new Integer[] {node != null ? 1 : 0, lo, hi};
    }

    static boolean valid(Node node, long lo, long hi) {
        if (node == null) return true;
        if (node.val <= lo || node.val >= hi) return false;
        return valid(node.left, lo, node.val) && valid(node.right, node.val, hi);
    }

    static Integer kthInBand(Node root, int low, int high, int k) {
        ArrayDeque<Node> stack = new ArrayDeque<>();
        Node node = root;
        while (node != null || !stack.isEmpty()) {
            while (node != null) {
                if (node.val < low) node = node.right;
                else { stack.push(node); node = node.left; }
            }
            if (stack.isEmpty()) break;
            node = stack.pop();
            if (node.val > high) return null;
            if (--k == 0) return node.val;
            node = node.right;
        }
        return null;
    }

    static Node removeByPredecessor(Node node, int key) {
        if (node == null) return null;
        if (key < node.val) { node.left = removeByPredecessor(node.left, key); return node; }
        if (key > node.val) { node.right = removeByPredecessor(node.right, key); return node; }
        if (node.left == null) return node.right;
        if (node.right == null) return node.left;
        Node pred = node.left;
        while (pred.right != null) pred = pred.right;
        node.val = pred.val;
        node.left = removeByPredecessor(node.left, pred.val);
        return node;
    }
}
```

The search and the removal follow one path, so each is O(h). The validation visits every node once, O(n), and it can return as soon as one node fails. The band walk costs O(h + k) for a countdown of k, with O(h) stack space.

<!-- stage: applicability -->
### When The Numbers Carry A Promise

Use the carried interval when a tree promises order and the question is about positions in that order: finding the gap a new record would fill, auditing an index after a bulk load, reading the next few keys inside a date range, or deleting a record without rebuilding the index. The invariant is that the interval entering a node is exactly the set of keys allowed in that branch, so every comparison is against two numbers and never against a distant ancestor.

The first false friend is the local check of a parent and its children, which accepts the stacks 5, 4, 6, null, null, 3, 7 although 3 sits in the right side of 5. A second false friend is reading the ends of the stopping interval as neighbours when the search found its key, because then the neighbours may be deeper in the found node's own branches. A third is applying the interval to a tree that never promised order, where it has nothing to certify.

A no-go condition is an unstated duplicate policy: the strict comparisons used here assume distinct keys, and a policy that allows equal keys on one side has to change one end of the interval from exclusive to inclusive. In Java use `null` or `long` for open ends, never a magic `int` that real data can reach.

<!-- stage: exercises -->
### Exercises

#### [Build] Search With Its Stopping Interval (LeetCode 700)
<!-- id: tc-search-stopping-interval -->

**Prerequisites.** The search and bounds lessons.

**Problem.** The archive is a search tree of distinct keys stored by levels, with `null` marking each missing child. Search for `key` and report `[found, lo, hi]`, where `lo` and `hi` are the interval ends the walk carries when it stops, with `null` for an end that no stack passed. When the key is missing, the ends are its two neighbours in sorted order.

**Constraints.** 0 <= values.length <= 5000, keys are distinct integers between 0 and 100000, and the searched key is an integer in the same range.

**Example 1.** Input `values = [8, 3, 10, 1, 6, null, 14]`, `key = 7`, output `[false, 6, 8]`.

**Example 2.** Input `values = [8, 3, 10, 1, 6, null, 14]`, `key = 0`, output `[false, null, 1]`.

**Hint.** When the walk goes left at a stack, which end of the interval is replaced, and by what?

**Changed decision.** The walk returns the pair of ends it narrowed along the way instead of the subtree, so the same single path also yields the gap around a missing key.

#### [Vary] First Violation Of The Numbering (LeetCode 98)
<!-- id: tc-first-violation -->

**Prerequisites.** The Search With Its Stopping Interval rung and the strict test.

**Problem.** For a binary tree stored by levels, find the first node in preorder, meaning node, then left branch, then right branch, whose key is not strictly between the ends inherited from its ancestors. Return its position in the input array, or -1 if every node fits. Keys may be any 32-bit integers.

**Constraints.** 0 <= values.length <= 5000 and keys are integers between -2147483648 and 2147483647.

**Example 1.** Input `values = [5, 4, 6, null, null, 3, 7]`, output `5`.

**Example 2.** Input `values = [2, 1, 3]`, output `-1`.

**Hint.** At the node 3 in the first example, what interval does it inherit, and which of the earlier nodes set each end?

**Changed decision.** The walk reports where the numbering first breaks, which is the first failing test, rather than a bare yes or no for the whole tree.

#### [Boundary] Kth Smallest Inside A Band (LeetCode 230)
<!-- id: tc-kth-in-band -->

**Prerequisites.** The First Violation rung and the sorted visit of the previous lessons.

**Problem.** A search tree of distinct keys is stored by levels. Given a band `[low, high]` and a rank k, return the kth smallest key that lies inside the band, or `null` when fewer than k keys do. Branches that cannot overlap the band must not be entered.

**Constraints.** 0 <= values.length <= 10000, keys are distinct integers between 0 and 100000, 0 <= low <= high <= 100000, and 1 <= k <= 10000.

**Example 1.** Input `values = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]`, `low = 5`, `high = 12`, `k = 3`, output `7`.

**Example 2.** Input `values = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]`, `low = 5`, `high = 7`, `k = 4`, output `null`.

**Hint.** When a popped key is above the band, what is known about every key still waiting?

**Changed decision.** Keys below the band are skipped together with their left sides, and the walk ends with `null` at the first key above the band instead of counting past it.

#### [Recognize] Delete By Predecessor (LeetCode 450)
<!-- id: tc-delete-by-predecessor -->

**Prerequisites.** The Kth Smallest Inside A Band rung and the neighbour keys.

**Problem.** Remove `key` from a search tree of distinct keys stored by levels, if present. A stack with two branches takes the key of the largest node on its left side, which is then removed from there. Give back the resulting tree as a level-order array without its trailing `null` entries.

**Constraints.** 0 <= values.length <= 5000, keys are distinct integers between -100000 and 100000, and the key is an integer in the same range.

**Example 1.** Input `values = [5, 3, 6, 2, 4, null, 7]`, `key = 3`, output `[5, 2, 6, null, 4, null, 7]`.

**Example 2.** Input `values = [5, 3, 6, 2, 4, null, 7]`, `key = 5`, output `[4, 3, 6, 2, null, null, 7]`.

**Hint.** Which key on the left side of the removed one is the nearest in sorted order, and how many children can its old node have?

**Changed decision.** The replacement comes from the left neighbour rather than the right one, so the shapes produced differ from the successor version even though both preserve the numbering.
