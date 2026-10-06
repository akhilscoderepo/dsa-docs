<!-- lesson-kind: standard -->
<!-- lesson-id: levels-zigzag-and-views -->
## Read A Tree Level By Level

<!-- stage: context -->
### Why The Chart Prints In Mixed Order

An org chart stores each manager with a list of direct reports. The printer must show the chief first, then everyone who reports to the chief, then everyone one step further down. A first version walks the tree with a recursive method and prints each person as it arrives. The output starts with the chief, jumps to the first report, and dives down that report's whole branch before it shows the second report. The reader sees people from three different layers mixed together.

The task asks for nodes grouped by depth, where depth counts the edges from the root. A walk that dives down one branch cannot group them, because it leaves a layer before it finishes the layer. This lesson asks which order of visits keeps every node of one depth together, and how a program knows exactly where one depth ends.

<!-- stage: naive -->
### Walking Once For Each Depth

The direct plan asks one question per depth: which nodes sit exactly `d` edges below the root? A recursive method answers it by going down `d` steps and collecting the nodes it reaches. The outer loop asks the question for `d = 0, 1, 2` until a depth comes back empty.

```java
final class LevelsByRepeatedWalks {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void collect(TreeNode node, int steps, List<Integer> out) {
        if (node == null) return;                        // a missing child holds no node
        if (steps == 0) { out.add(node.val); return; }   // this node lies exactly d edges down
        collect(node.left, steps - 1, out);              // one edge closer to the target depth
        collect(node.right, steps - 1, out);
    }

    static List<List<Integer>> levels(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        for (int d = 0; ; d++) {
            List<Integer> level = new ArrayList<>();
            collect(root, d, level);
            if (level.isEmpty()) return result;          // no node at depth d means no deeper node either
            result.add(level);
        }
    }
}
```

On the tree with root 3, children 9 and 20, and grandchildren 15 and 7 under 20, the result is `[[3], [9, 20], [15, 7]]`. The method is correct.

<!-- stage: bottleneck -->
### Counting The Repeated Visits

```predict
Take a tree that is a single chain of n nodes, where each node has only a right child. How many nodes does the repeated-walk method visit in total, and what is the cost in big-O terms?

The walk for depth d passes through d + 1 nodes before it stops, so the total is 1 + 2 + ... + n, which is about n squared over 2. The cost is O(n^2) on a chain, and in general O(n * h) for height h.
```

Every depth restarts the walk from the root and re-visits all the nodes above it. On a balanced tree the height is small, so the waste is small. On a chain of 100000 nodes the method makes about five billion visits, and the program stalls.

The information needed for the next depth already exists after the walk for the current depth, because the children of the nodes at depth `d` are exactly the nodes at depth `d + 1`. The method needs to keep those children and move on, so no node is reached more than once.

<!-- stage: insight -->
### Keep The Waiting Nodes In A Queue

A **queue** hands out items in the order they arrived, first in and first out. Put the root into a queue. Remove a node from the front, and add its non-null children to the back. The children of the shallow nodes always arrive before the children of the deep nodes. The queue therefore holds the nodes in the order of their depth, with all nodes of depth `d` ahead of all nodes of depth `d + 1`.

The queue still mixes depths at its boundary. After the program removes the last node of depth `d`, the first node of depth `d + 1` is already at the front, and the queue gives no sign of the change.

#### Capture The Level Size Before Removing

The **level size** is the number of nodes in the queue at the moment a level starts. At that moment the queue holds exactly the nodes of one depth, because the previous level's removals added all their children and nothing else. The program reads `queue.size()` once, stores it, and removes exactly that many nodes. Those removals form the **frontier** of this depth: the set of nodes the program is about to expand. Every child added during the removals lands behind the frontier and belongs to the next depth.

#### Why One Read Is Enough

The size must be read before the first removal. A removal shrinks the queue and an addition grows it, so a size read inside the loop condition changes while the loop runs. A stored value stays fixed, and it marks the **level boundary**: the position after which the nodes belong to the next depth. Each node enters the queue once and leaves it once, so the whole traversal costs O(n) time.

<!-- names: queue, level size, frontier, level boundary -->

<!-- stage: variables -->
### The State Of The Level Loop

- **queue** holds the discovered nodes that have not yet been expanded, in order of depth.
- **size** holds the number of nodes at the current depth, read once before the removals.
- **level** is the list of values collected from the current depth.
- **result** is the list of finished levels, one entry per depth.
- **node** is the node removed from the front of the queue.

<!-- stage: trace -->
### Two Levels Of A Small Tree

The cells show the nodes in the order the queue discovers them. The pointer `removed` marks the last node taken out of the queue, and the pointer `queued` marks the last node put into it. The nodes between the two pointers are the ones still waiting.

#### Reading The Tree With Five Nodes

The root is 3. Its children are 9 and 20, and the node 20 has the children 15 and 7. The cells hold `3, 9, 20, 15, 7`.

```trace
{"cells":[3,9,20,15,7],"pointers":["removed","queued"],"steps":[{"at":{"removed":-1,"queued":0},"vars":{"result":"[]"},"note":"Start: the queue holds only the root 3. Nothing has been removed."},{"at":{"removed":0,"queued":2},"vars":{"size":1,"result":"[[3]]"},"note":"Level 0 ends. The loop stored size 1, removed exactly 1 node(s) and collected [3]."},{"at":{"removed":2,"queued":4},"vars":{"size":2,"result":"[[3], [9, 20]]"},"note":"Level 1 ends. The loop stored size 2, removed exactly 2 node(s) and collected [9, 20]."},{"at":{"removed":4,"queued":4},"vars":{"size":2,"result":"[[3], [9, 20], [15, 7]]"},"note":"Level 2 ends. The loop stored size 2, removed exactly 2 node(s) and collected [15, 7]."}]}
```

Each step shows one finished level. The stored size is 1, then 2, then 2. Between two steps, `removed` moves forward by exactly the stored size, and `queued` moves forward by the number of children found. The result after the last step is `[[3], [9, 20], [15, 7]]`.

#### Reading The Size Inside The Loop

Take a tree with the root 1, the children 2 and 3, and one grandchild 4 under the node 2. A loop that tests `i < queue.size()` on every pass reads a size that keeps changing.

```trace
{"cells":[1,2,3,4],"pointers":["removed","queued"],"steps":[{"at":{"removed":-1,"queued":0},"vars":{"i":0,"queue size":1,"level":"[]"},"note":"Start: the queue holds the node 1, and the first test reads the queue size 1."},{"at":{"removed":0,"queued":2},"vars":{"i":1,"queue size":2,"level":"[1]"},"note":"The node 1 leaves and its children join, so the test now reads 2 and compares it with i = 1. The test passes, so the loop removes another node of depth 1 in this level."},{"at":{"removed":1,"queued":3},"vars":{"i":2,"queue size":2,"level":"[1, 2]"},"note":"The node 2 leaves and its children join, so the test now reads 2 and compares it with i = 2. The test fails and the loop stops."}]}
```

The first level should hold only the node 1. The queue shrinks by one removal and grows by two additions, so the test reads 2 on the second pass, and the loop removes the node 2 as well. The wrong reading puts a depth-1 node into the depth-0 list.

<!-- stage: code -->
### The Level Loop In Code

```java
final class LevelOrder {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;                  // ArrayDeque rejects null, so the empty tree returns early
        Deque<TreeNode> queue = new ArrayDeque<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            int size = queue.size();                      // read once; this is the level boundary
            List<Integer> level = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {              // exactly the nodes of one depth leave the queue
                TreeNode node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.add(node.left);     // children join the next depth
                if (node.right != null) queue.add(node.right);   // null children are skipped, never queued
            }
            result.add(level);
        }
        return result;
    }
}
```

The code never adds `null` to the queue, because `ArrayDeque.add(null)` throws a `NullPointerException`. The guard on each child and the early return for an empty root keep every queued value real.

- **Time** is O(n), because each node is added once and removed once.
- **Space** is O(w), where `w` is the widest level, because the queue never holds more than two adjacent levels and the result holds the n values the caller asked for.

<!-- stage: applicability -->
### Choosing The Level Loop

#### Recognizing The Cue

Use the level loop when the answer groups nodes by depth or picks a position from each depth. Words such as "each row", "layer by layer", "left to right on every level" and "the view from the right side" point to it. The output order follows the order of discovery, so a change in output order never changes the queue order.

#### Checking The Invariant

The invariant is that at the top of each outer pass the queue holds exactly the nodes of one depth. The stored size keeps it true, because the inner loop removes that many nodes and adds only their children. A size read inside the loop breaks the invariant on the first addition.

#### Avoiding The False Friend

The false friend is the recursive walk with a depth argument. Both give the same lists, but the recursive walk has a deep call stack on a chain, and the queue loop keeps its work in a heap-allocated structure. Another false friend is the order of keys. The level order of a search tree says nothing about sorted order, so a level list is not a sorted list.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Tree Level Order Traversal (LeetCode 102)
<!-- id: tb-level-order -->

**Prerequisites.** The queue and the stored level size from this lesson.

**Problem.** Given the root of a binary tree, return a list of lists. The list at position `d` holds the values of all nodes at depth `d`, ordered from left to right. The root has depth 0. Capture the number of queued nodes before removing any node of a level.

**Constraints.** The limits are:
- **Nodes** number between 0 and 2000.
- **Values** satisfy `-1000 <= val <= 1000`, and values may repeat.
- **Answer** is a list of lists, and an empty tree gives an empty outer list.
- **Mutation** does not occur; no field changes.

**Example 1.** Input root 3 with children 9 and 20, where 20 has children 15 and 7, output `[[3], [9, 20], [15, 7]]`.

**Example 2.** Input a root 1 with only a left child 2, and a child 3 below the node 2 on the right, output `[[1], [2], [3]]`.

**Hint.** What number tells the loop where a level ends? When does the program read it?

**Changed decision.** A stored size replaces a walk per depth.

#### [Vary] Binary Tree Zigzag Level Order Traversal (LeetCode 103)
<!-- id: tb-zigzag -->

**Prerequisites.** The exercise above.

**Problem.** For a binary tree, return the values by depth where depth 0 reads from left to right, depth 1 reads from right to left, depth 2 reads from left to right, and the directions keep alternating. The nodes enter the queue in the same order as in the plain level traversal.

**Constraints.** The limits are:
- **Nodes** number between 0 and 2000.
- **Values** satisfy `-100 <= val <= 100`.
- **Answer** is a list of lists, and an empty tree gives an empty outer list.
- **Mutation** does not occur.

**Example 1.** Input root 3 with children 9 and 20, where 20 has children 15 and 7, output `[[3], [20, 9], [15, 7]]`.

**Example 2.** Input a complete tree with values 1 to 7 in level order, output `[[1], [3, 2], [4, 5, 6, 7]]`.

**Hint.** Which part of the loop decides the output order of a level? Does the queue order need to change?

**Changed decision.** Only the place where each value lands in the level list changes.

#### [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: tb-level-edges -->

**Prerequisites.** The two exercises above.

**Problem.** A binary tree is supplied by its root. Return the number of nodes at each depth as a list of integers, so that the entry at position `d` is the width of depth `d`. A null root gives an empty list. A chain in which every node has one child gives a list of ones.

**Constraints.** The limits are:
- **Nodes** number between 0 and 3000.
- **Values** satisfy `-10^4 <= val <= 10^4`.
- **Answer** is a list of positive integers whose sum equals the node count.
- **Mutation** does not occur.

**Example 1.** Input a null root, output `[]`.

**Example 2.** Input a chain of four nodes where each node has only a left child, output `[1, 1, 1, 1]`.

**Hint.** What does the queue hold when the root is null? What size does each level have on a chain?

**Changed decision.** The method returns counts, and the null root must not enter the queue.

#### [Recognize] Binary Tree Right Side View (LeetCode 199)
<!-- id: tb-right-view -->

**Prerequisites.** All three exercises above.

**Problem.** Imagine standing on the right side of a binary tree. Return the values of the nodes visible from there, ordered from the top to the bottom. The visible node of a depth is the last node of that depth in left-to-right order, and a depth with one node shows that node.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** satisfy `-100 <= val <= 100`, and values may repeat.
- **Answer** has one value per depth.
- **Mutation** does not occur.

**Example 1.** Input root 1 with children 2 and 3, where 2 has a right child 5 and 3 has a right child 4, output `[1, 3, 4]`.

**Example 2.** Input root 1 with a left child 2, where 2 has a left child 4, output `[1, 2, 4]`, because the left branch is visible when nothing hides it.

**Hint.** Which node of a level is the last one the loop removes? Can the last node be a left child?

**Changed decision.** The method records one value per level, and it picks that value by its position in the level.
