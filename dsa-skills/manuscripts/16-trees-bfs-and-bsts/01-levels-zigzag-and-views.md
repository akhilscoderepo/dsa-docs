<!-- lesson-kind: standard -->
<!-- lesson-id: levels-zigzag-and-views -->
## Levels Zigzag And Views

<!-- stage: context -->
### The Lantern Ring Festival

At a lake festival one large lantern hangs from a pole in the middle. Strings run from it to up to two smaller lanterns, each of those has strings to up to two more, and the web spreads outward in rings. Volunteers light one ring at a time, so the organiser wants a printed card for every ring, listing its lanterns from left to right.

Some evenings the cards must alternate, the first ring read left to right, the next right to left, and so on, because the volunteers walk a snake-shaped path. The photographers ask for something else again: only the lantern farthest to the right in each ring, since that is the one that shows from the shore.

<!-- stage: naive -->
### Walk The Whole Web For Each Ring

The direct method fetches one ring per walk. A volunteer starts at the middle lantern with a step counter, follows the strings, and writes down every lantern that lies exactly d steps out. She makes one complete walk for d equal to 0, another for 1, and so on, and she stops when a walk finds nothing.

```java
static List<List<Integer>> byRepeatedWalks(Node middle) {
    List<List<Integer>> cards = new ArrayList<>();
    for (int d = 0; ; d++) {
        List<Integer> ring = new ArrayList<>();
        collect(middle, d, ring);
        if (ring.isEmpty()) return cards;
        cards.add(ring);
    }
}

static void collect(Node lantern, int stepsLeft, List<Integer> ring) {
    if (lantern == null) return;
    if (stepsLeft == 0) { ring.add(lantern.val); return; }
    collect(lantern.left, stepsLeft - 1, ring);
    collect(lantern.right, stepsLeft - 1, ring);
}
```

Every card is correct and the order inside a ring follows the left-before-right walk, so the method works on any web.

<!-- stage: bottleneck -->
### Inner Lanterns Are Walked Again And Again

A walk for ring d must pass through every lantern in rings 0 to d-1 on its way out, even though it writes down none of them. On a web that is one long string of n lanterns, walk d passes d lanterns, so the total is 1 + 2 + ... + n and the cost is O(n^2). For fifty thousand lanterns in a line that is over a billion steps, for a task that only needs each lantern written once.

The waste has a clear source. The method forgets what it learned. When the walk for ring 2 reaches a lantern, that lantern has just revealed its two neighbours for ring 3, but the information is thrown away and rediscovered by a longer walk next time. A better method would carry the discovered-but-unwritten lanterns forward from one ring to the next, and touch each lantern a constant number of times, for O(n) in total.

<!-- stage: insight -->
### A Queue Holds The Frontier

Keep a first-in, first-out queue of lanterns that have been reached but not yet processed. When the central lantern is the only one in the queue, that single lantern is the whole **frontier**: every lantern at distance 0. Process it, and append its children at the back. Those children are at distance 1, and because the queue is first-in, first-out they will be handled before any lantern farther out. The same holds for every later ring, so the queue always contains the lanterns of one ring followed by some lanterns of the next.

The only missing piece is where one ring ends and the next begins inside the queue. Before processing a ring, read the queue length once and keep it as a **size snapshot**. Exactly that many removals belong to the current ring, because everything added during those removals is a child and goes behind them. After the snapshot count is used up, the **level boundary** has been crossed and the queue holds precisely the next ring.

The invariant is that at the moment a ring starts, the queue holds exactly the lanterns of that ring in left-to-right order, and its length is the number of removals owed.

<!-- names: frontier, size snapshot, level boundary -->

Zigzag changes only where each value is written in its card, and the right view keeps only the last value written in each card; the queue order never changes.

<!-- stage: variables -->
### Queue, Snapshot And Ring Card

The variable `queue` is an `ArrayDeque<Node>` that holds the frontier, and it changes on every removal and every child append. The int `size` is taken from `queue.size()` once at the start of each ring and never reread inside the ring loop. The list `ring` collects the values of one ring and is added to the answer when the snapshot is used up. For zigzag, a boolean `leftToRight` flips after each ring and decides whether a value is appended or inserted at index 0. For the right view, the answer takes the value of the removal whose counter equals `size - 1`.

<!-- stage: trace -->
### Rings Of A Seven Lantern Web

The first trace runs the plain level method on the web 3, 9, 20, null, null, 15, 7 in level order. The pointer `node` marks the lantern just removed from the queue. The `queue` variable shows what waits behind it and `ring` shows the card being filled. Notice that after the lantern 3 is removed, the queue holds 9 and 20, and that the snapshot taken for the second ring is 2, so the lanterns 15 and 7 added meanwhile are not mixed into that card.

```trace
{"cells":["3","9","20","null","null","15","7"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"size":1,"ring":"3","queue":"9 20"},"note":"The lantern 3 is removed; the card for ring 0 now reads 3 and the queue behind it holds 9 20. The snapshot of 1 is used up, so the card is closed."},{"at":{"node":1},"vars":{"size":2,"ring":"9","queue":"20"},"note":"The lantern 9 is removed; the card for ring 1 now reads 9 and the queue behind it holds 20."},{"at":{"node":2},"vars":{"size":2,"ring":"9 20","queue":"15 7"},"note":"The lantern 20 is removed; the card for ring 1 now reads 9 20 and the queue behind it holds 15 7. The snapshot of 2 is used up, so the card is closed."},{"at":{"node":5},"vars":{"size":2,"ring":"15","queue":"7"},"note":"The lantern 15 is removed; the card for ring 2 now reads 15 and the queue behind it holds 7."},{"at":{"node":6},"vars":{"size":2,"ring":"15 7","queue":"empty"},"note":"The lantern 7 is removed; the card for ring 2 now reads 15 7 and the queue behind it holds empty. The snapshot of 2 is used up, so the card is closed."}]}
```

The second trace asks for the right view of the web 1, 2, 3, null, 5, null, 4. The pointer `node` again marks the removed lantern, and the variable `seen` counts removals inside the current ring while `size` holds the snapshot. A lantern is recorded only when `seen` reaches `size`, which is the last removal of its ring, so the left lantern 2 is skipped and the lantern 3 is kept for the second ring, while the third ring shows 4 because 5 is not last.

```trace
{"cells":["1","2","3","null","5","null","4"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"size":1,"seen":1,"queue":"2 3"},"note":"The lantern 1 is removal 1 of 1 in ring 0, the last of its ring, so it is recorded."},{"at":{"node":1},"vars":{"size":2,"seen":1,"queue":"3 5"},"note":"The lantern 2 is removal 1 of 2 in ring 1, not the last of its ring, so it is skipped."},{"at":{"node":2},"vars":{"size":2,"seen":2,"queue":"5 4"},"note":"The lantern 3 is removal 2 of 2 in ring 1, the last of its ring, so it is recorded."},{"at":{"node":4},"vars":{"size":2,"seen":1,"queue":"4"},"note":"The lantern 5 is removal 1 of 2 in ring 2, not the last of its ring, so it is skipped."},{"at":{"node":6},"vars":{"size":2,"seen":2,"queue":"empty"},"note":"The lantern 4 is removal 2 of 2 in ring 2, the last of its ring, so it is recorded."}]}
```

<!-- stage: code -->
### Level Walks With A Queue

```java
final class LevelWalks {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static List<List<Integer>> levels(Node root, boolean zigzag) {
        List<List<Integer>> cards = new ArrayList<>();
        if (root == null) return cards;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        boolean leftToRight = true;
        while (!queue.isEmpty()) {
            int size = queue.size();
            LinkedList<Integer> ring = new LinkedList<>();
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                if (zigzag && !leftToRight) ring.addFirst(node.val); else ring.addLast(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
            cards.add(ring);
            leftToRight = !leftToRight;
        }
        return cards;
    }

    static List<Integer> rightView(Node root) {
        List<Integer> view = new ArrayList<>();
        if (root == null) return view;
        ArrayDeque<Node> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();
            for (int k = 0; k < size; k++) {
                Node node = queue.poll();
                if (k == size - 1) view.add(node.val);
                if (node.left != null) queue.add(node.left);
                if (node.right != null) queue.add(node.right);
            }
        }
        return view;
    }
}
```

Each lantern enters and leaves the queue once, so the time is O(n). The queue holds at most one ring plus the start of the next, so the extra space is O(w) for the widest ring w, which can reach n/2.

<!-- stage: applicability -->
### When Distance From The Top Decides

Reach for the queue when the answer is grouped by depth or picks a position from each depth: floor-by-floor lists of an organisation chart, the nearest layer of a menu hierarchy that contains a target, or a width measurement of each level. The invariant is that the queue at the start of a ring holds exactly that ring, so its length is the number of removals the ring is owed.

The first false friend is reading `queue.size()` in the loop condition, as in `for (int k = 0; k < queue.size(); k++)`. The size grows as children arrive, so the loop never stops at the boundary and rings blend into one list. A second false friend is a depth-first walk with a depth argument that fills `cards.get(depth)`; it is correct for grouping, but it cannot stop early at the first ring that satisfies a test, and the queue can. A third is the right view taken as the right-child chain, which misses a left child that sits below a missing right branch.

In Java, `ArrayDeque` rejects `null`, so test the root for `null` before the first `add` and never enqueue absent children as markers. Use `poll()` for removal rather than `remove(0)` on an `ArrayList`, which shifts every element.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Tree Level Order Traversal (LeetCode 102)
<!-- id: tb-level-order -->

**Prerequisites.** The tree representation lesson and the queue from Chapter 11.

**Problem.** The lanterns arrive as a level-order array in which `null` marks an absent child and the children of an absent node are not listed. Return the values grouped by depth, topmost group first, and each group ordered from left to right.

**Constraints.** 0 <= values.length <= 2000 and every value is an integer between -1000 and 1000.

**Example 1.** Input `values = [3, 9, 20, null, null, 15, 7]`, output `[[3], [9, 20], [15, 7]]`.

**Example 2.** Input `values = [1, null, 2, null, 3]`, output `[[1], [2], [3]]`.

**Hint.** Where in the loop must the queue length be read so that children added during a ring do not count toward it?

**Changed decision.** The queue length is captured before each ring starts, and that count of removals forms one list.

#### [Vary] Binary Tree Zigzag Level Order Traversal (LeetCode 103)
<!-- id: tb-zigzag-order -->

**Prerequisites.** The Level Order rung and the size snapshot.

**Problem.** Using the same level-order input, return the depth groups again, but let the first group read left to right, the second right to left, the third left to right, and so on alternately. The order in which children are discovered must not change.

**Constraints.** 0 <= values.length <= 2000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [3, 9, 20, null, null, 15, 7]`, output `[[3], [20, 9], [15, 7]]`.

**Example 2.** Input `values = [1, 2, 3, 4, 5, 6, 7, 8, 9]`, output `[[1], [3, 2], [4, 5, 6, 7], [9, 8]]`.

**Hint.** Is it the order of enqueueing that must flip, or only the place where each value lands in its list?

**Changed decision.** Children are enqueued left then right as before, and only the insertion end of the group list alternates by depth.

#### [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tb-empty-and-chains -->

**Prerequisites.** The Zigzag rung and the `ArrayDeque` null rule.

**Problem.** Write the level grouping so that an empty input gives an empty outer list and a tree that is one long chain of single children, leaning in either direction, gives one group of one value per depth. The chain can be very long, so recursion must not be needed to walk it.

**Constraints.** 0 <= values.length <= 100000 where the chain form lists one `null` per level, and values are integers between -1000 and 1000.

**Example 1.** Input `values = []`, output `[]`.

**Example 2.** Input `values = [1, 2, null, 3, null, 4]`, output `[[1], [2], [3], [4]]`.

**Hint.** What does `ArrayDeque.add` do with `null`, and which line of the method would meet a null root first?

**Changed decision.** The root is checked for null before the first enqueue, since the queue cannot hold a null and a null root has no ring to report.

#### [Recognize] Binary Tree Right Side View (LeetCode 199)
<!-- id: tb-right-side-view -->

**Prerequisites.** The Empty And One-Sided Trees rung and the level grouping.

**Problem.** Standing to the right of a tree, you see one node per depth, namely the rightmost node at that depth, even when it is a left child hanging below a missing right branch. Given the level-order array, return the visible values from the top depth downward.

**Constraints.** 0 <= values.length <= 100 and values are integers between -100 and 100.

**Example 1.** Input `values = [1, 2, 3, null, 5, null, 4]`, output `[1, 3, 4]`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `[1, 2, 3]`.

**Hint.** Which removal in a captured ring is the last one, and what number identifies it?

**Changed decision.** No list is built per ring; the value is recorded only for the removal whose counter equals the snapshot minus one.
