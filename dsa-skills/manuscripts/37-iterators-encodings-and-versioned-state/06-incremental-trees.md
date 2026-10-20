<!-- lesson-kind: standard -->
<!-- lesson-id: incremental-trees -->
## Incremental Trees

<!-- stage: context -->
### Adding Nodes To A Live Tree

A job scheduler stores its pending tasks in a complete binary tree of linked node objects. In a complete binary tree every level is full except possibly the last, and the last level fills from left to right. Each `add` call must place the new task in the first free slot of the bottom level. A service adds 100 000 tasks while it also reads the tree. Every `add` starts at the root and walks the levels until it meets a node that still lacks a child. The service slows down as the heap grows, and a profiler shows that most of the time goes into walking nodes that were already full.

The walk repeats work that the previous `add` call finished moments ago. That call already knew which node would receive the next child. The lesson asks two questions. What should a class remember about its tree between calls so that each call avoids the walk? And how does the class keep that memory correct after every change to the tree?

<!-- stage: naive -->
### Searching From The Root Each Time

The direct method treats every call as a fresh question. To insert a value, it walks the tree level by level with a queue. It stops at the first node that has an empty left or right child slot and attaches the new node there. The class stores only the root, so nothing can go stale.

```java
final class NaiveInserter {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private final TreeNode root;

    NaiveInserter(TreeNode root) { this.root = root; }

    int insert(int val) {
        java.util.ArrayDeque<TreeNode> queue = new java.util.ArrayDeque<>();
        queue.add(root);                      // level-order walk starts at the root
        while (true) {
            TreeNode node = queue.poll();     // next node in level order
            if (node.left == null) {          // first free slot is a left child
                node.left = new TreeNode(val);
                return node.val;
            }
            if (node.right == null) {         // first free slot is a right child
                node.right = new TreeNode(val);
                return node.val;
            }
            queue.add(node.left);             // both slots are taken, so visit the children later
            queue.add(node.right);
        }
    }
}
```

On a tree with 3 nodes the walk visits the root, finds it full, and then stops at the next node, which has no children. The result is correct on every call.

```predict
A complete tree has 10 nodes in level order, numbered 0 to 9. The naive insert runs once. How many nodes does the walk examine, and which node receives the new child?

The walk examines 5 nodes, the nodes numbered 0 to 4. Node 4 already has a left child, node 9, and lacks a right child, so the new node becomes its right child. In general the new node gets number n, and its parent has number (n - 1) / 2 rounded down, so the walk examines about n / 2 nodes.
```

<!-- stage: bottleneck -->
### Counting The Repeated Searches

The walk cannot skip the full nodes in front of the target, because the class keeps no record of them. When the tree holds `n` nodes, one insert examines about `n / 2` nodes. After `m` inserts starting from one node, the total is about `m^2 / 4` node visits. For `m = 100 000` that is about 2.5 billion visits, so the whole run costs O(m^2) time, although each insert changes only one node.

The waste has a precise source. All the nodes in front of the target are full, and they stay full forever, because inserts only fill slots and never empty them. The class discards that fact after each call and then rediscovers it at the cost of a linear walk. The cost problem therefore has a second half. A class that keeps the fact must update it on every change, or the stored fact points at the wrong node.

<!-- stage: insight -->
### Store The Search Result Between Calls

#### The Frontier Queue

The **frontier** is the queue of nodes that still have fewer than two children, listed in level order. In a complete tree these nodes form the tail of the level order, so the node at the head of the frontier is always the parent of the next insertion. An insert reads the head and attaches the new node to its left slot. When the left slot has a child already, the insert uses the right slot and removes the head, because the head now has two children. The new node has no children, so it joins the back of the frontier. The insert now costs O(1) time because it never walks the tree.

<!-- names: frontier -->

#### One Rule For Stored Facts

A stored structure describes a fact about the tree that a later call needs. The frontier is the example here. The invariant of this lesson says that after every public method returns, each stored structure agrees with the current tree. A method that changes the tree must change the stored structure in the same call. A method that only reads must leave both unchanged. The constructor has a separate duty. It builds the stored structure from the tree it receives. It may do that work once, because the cost then spreads across all later calls.

<!-- stage: variables -->
### Tree, Frontier And Return Value

The inserter keeps one tree and one queue. The trace below also records what each call returns.

- **root** is the top node of the linked tree. The trace variable `root` shows the level-order values of the tree below it.
- **frontier** is the queue of nodes with fewer than two children, written from head to back.
- **parent** is the node at the head of the frontier when the call starts. The trace pointer `parent` marks its position in level order.
- **fresh** is the node that the current call adds. The trace pointer `fresh` marks its position in level order.
- **result** is the value `parent.val` that the call returns to its caller.

The invariant is that the frontier lists exactly the nodes with fewer than two children, in level order, after the constructor and after every insert.

<!-- stage: trace -->
### Tracing Inserts On A Small Tree

#### A Correct Inserter

The first trace starts with the complete tree `1, 2, 3`, in which node 1 has two children and nodes 2 and 3 have none. The constructor therefore builds the frontier `2, 3`. The pointer `parent` marks the node that the call used, which is the node at the front of the frontier when the call starts. The pointer `fresh` marks the node that the call just added. The cells list the level order of the final tree, so a cell to the right of `fresh` does not exist yet.

The first insert places 4 as the left child of node 2 and leaves node 2 at the head, because node 2 still has an open right slot. The second insert places 5 as the right child of node 2. Node 2 is now full, so the insert removes it and the head moves to node 3. The next two inserts fill node 3 the same way, and the last insert starts node 4. Every insert adds the new node at the back of the frontier, so the order of the frontier always matches the level order of the tree. At each step the pointer `parent` therefore sits on the node whose value the call returns.

```trace
{"cells":["1","2","3","4","5","6","7","8"],"pointers":["parent","fresh"],"steps":[{"at":{"parent":1,"fresh":-1},"vars":{"frontier":"2,3","root":"1,2,3","result":"none"},"note":"The constructor reads the tree 1, 2, 3 once. Nodes 2 and 3 have no children, so the frontier is 2, 3 and parent will be node 2."},{"at":{"parent":1,"fresh":3},"vars":{"frontier":"2,3,4","root":"1,2,3,4","result":2},"note":"Insert 4: parent is node 2, the head of the frontier, and its left slot is open. The call attaches 4 as its left child, keeps node 2 in the frontier and appends node 4. The call returns 2."},{"at":{"parent":1,"fresh":4},"vars":{"frontier":"3,4,5","root":"1,2,3,4,5","result":2},"note":"Insert 5: parent is node 2, the head of the frontier, and its left slot is taken. The call attaches 5 as its right child, removes node 2 because it is full and appends node 5. The call returns 2."},{"at":{"parent":2,"fresh":5},"vars":{"frontier":"3,4,5,6","root":"1,2,3,4,5,6","result":3},"note":"Insert 6: parent is node 3, the head of the frontier, and its left slot is open. The call attaches 6 as its left child, keeps node 3 in the frontier and appends node 6. The call returns 3."},{"at":{"parent":2,"fresh":6},"vars":{"frontier":"4,5,6,7","root":"1,2,3,4,5,6,7","result":3},"note":"Insert 7: parent is node 3, the head of the frontier, and its left slot is taken. The call attaches 7 as its right child, removes node 3 because it is full and appends node 7. The call returns 3."},{"at":{"parent":3,"fresh":7},"vars":{"frontier":"4,5,6,7,8","root":"1,2,3,4,5,6,7,8","result":4},"note":"Insert 8: parent is node 4, the head of the frontier, and its left slot is open. The call attaches 8 as its left child, keeps node 4 in the frontier and appends node 8. The call returns 4."}]}
```

#### A Frontier That Is Not Updated

The second trace replays the same start on a class that forgets to remove a full node from the frontier. The first two inserts behave as before. After the second insert, node 2 has two children but remains at the head. The third insert reads the head, finds both slots of node 2 occupied, and writes to the right slot anyway. That write replaces node 5 with node 6. The class still reports success and its counter says 6 nodes exist, but only 5 nodes are reachable from the root. The stored frontier no longer agrees with the tree, and the error destroys data in a call that looks harmless.

```trace
{"cells":["1","2","3","4","5","6"],"pointers":["parent","fresh"],"steps":[{"at":{"parent":1,"fresh":-1},"vars":{"frontier":"2,3","root":"1,2,3","result":"none"},"note":"The constructor reads the tree 1, 2, 3 once. Nodes 2 and 3 have no children, so the frontier is 2, 3 and parent will be node 2."},{"at":{"parent":1,"fresh":3},"vars":{"frontier":"2,3,4","root":"1,2,3,4","result":2},"note":"Insert 4: parent is node 2, the head of the frontier, with an open left slot. The call attaches 4 and appends node 4. The class does not remove full nodes, so node 2 stays at the head."},{"at":{"parent":1,"fresh":4},"vars":{"frontier":"2,3,4,5","root":"1,2,3,4,5","result":2},"note":"Insert 5: parent is node 2, the head of the frontier, with an open right slot. The call attaches 5 and appends node 5. The class does not remove full nodes, so node 2 stays at the head."},{"at":{"parent":1,"fresh":5},"vars":{"frontier":"2,3,4,5,6","root":"1,2,3,4,6","result":2},"note":"Insert 6: parent is still node 2, the head of the frontier, which already has two children. The call overwrites its right child 5 with 6. The class returns 2 and counts 6 nodes, but only 5 nodes are reachable from the root."}]}
```

<!-- stage: code -->
### Writing The Inserter Class

#### The Class

The constructor reads the tree once with a level-order walk and keeps every node with fewer than two children in a queue. The method `insert` then reads the head, attaches the new node, removes a full head and appends the new node. The class keeps the root so that callers can read the whole tree.

```java
final class FrontierInserter {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    private final TreeNode root;
    private final java.util.ArrayDeque<TreeNode> frontier = new java.util.ArrayDeque<>();

    FrontierInserter(TreeNode root) {
        this.root = root;
        java.util.ArrayDeque<TreeNode> walk = new java.util.ArrayDeque<>();
        walk.add(root);                                   // level-order walk, done once
        while (!walk.isEmpty()) {
            TreeNode node = walk.poll();
            if (node.left != null) walk.add(node.left);
            if (node.right != null) walk.add(node.right);
            if (node.left == null || node.right == null) frontier.add(node);   // still has an open slot
        }
    }

    int insert(int val) {
        TreeNode parent = frontier.peek();                // head of the frontier receives the child
        TreeNode fresh = new TreeNode(val);
        if (parent.left == null) {
            parent.left = fresh;                          // left slot first, parent stays in the frontier
        } else {
            parent.right = fresh;                         // right slot fills the parent
            frontier.poll();                              // a full node leaves the frontier
        }
        frontier.add(fresh);                              // the new leaf has two open slots
        return parent.val;
    }

    TreeNode getRoot() { return root; }
}
```

#### Cost

- **Constructor** takes O(n) time and O(n) space for a tree of `n` nodes.
- **insert** costs O(1) time and adds one entry to the frontier.
- **getRoot** costs O(1) time and O(1) space.

<!-- stage: applicability -->
### When Stored Tree State Applies

#### Recognizing The Pattern

Look for a class whose public methods change a tree or move through it, while a later call depends on something an earlier call learned. List the questions that later calls ask. For each question, name the stored structure that answers it in constant or logarithmic time. Then write the rule that keeps the structure equal to what a full scan of the tree would produce. An insert into a complete tree asks for the first open slot, and the frontier answers it. A step backward asks for the previous value, and the list of values already returned answers it. The locking exercise below asks whether an ancestor is locked, and its `parent` array answers that question.

#### A False Friend

A class that returns correct answers on a freshly built tree is a false friend of a correct design. A stored structure that is right after the constructor can drift after the third mutation, and then it may silently drop a node, as the second trace shows. The check that matters is not whether the first call is right. The check is whether the invariant holds after the last call, whichever calls came before.

#### When The Method Does Not Apply

The frontier queue works only because a complete tree fills in level order. A tree that grows at arbitrary positions has no single next slot, so it needs a different structure. When a plain array can hold the tree, the array index replaces both the queue and the parent link. The parent of position `i` sits at position `(i - 1) / 2`. Calls from several threads need locking that this lesson does not describe, and every exercise assumes one caller at a time.

<!-- stage: exercises -->
### Exercises

#### [Build] Complete Binary Tree Inserter (LeetCode 919)
<!-- id: it37-complete-tree-inserter -->

**Prerequisites.** The frontier definition and the level-order walk from this lesson.

**Problem.** Design the class `CBTInserter`. The constructor receives the root of a complete binary tree of `TreeNode` objects. The call `insert(val)` adds a node with value `val` at the first free position in level order, so the tree stays complete. It returns the value of the new node's parent. The call `getRoot()` returns the root, so a caller can read the whole tree.

**Constraints.** The limits are:
- **Initial tree** has 1 to 1000 nodes.
- **Values** are `int` values, and duplicates occur.
- **Calls** number at most 10 000 per object.
- **Mutation** happens only inside `insert`, which edits the node objects in place.

**Example 1.** The initial tree is `[5,3,8,1]` in level order. Input calls `["insert","insert","getRoot"]` with arguments `[[9],[4],[]]`, output `[3,8,[5,3,8,1,9,4]]`, where the last entry lists the tree from `getRoot()` in level order.

**Example 2.** The initial tree is `[7]` in level order. Input calls `["insert","insert","insert","getRoot"]` with arguments `[[2],[6],[1],[]]`, output `[7,7,2,[7,2,6,1]]`, where the last entry lists the tree from `getRoot()` in level order.

**Hint.** Which nodes can still receive a child, and in which order must the class remember them so that the head is always the next parent?

**Changed decision.** Basic case: the class keeps a queue of nodes with open slots and updates it in the same call that changes the tree.

#### [Vary] Binary Search Tree Iterator II With A Window (LeetCode 1586)
<!-- id: it37-window-bst-iterator -->

**Prerequisites.** The stack-based inorder iterator for a binary search tree. A **visit history** is the sequence of values that the iterator already returned, kept so that `prev` can read them.

**Problem.** Design the class `WindowBstIterator` over a binary search tree with distinct values. The constructor receives the root and an integer `k`. The cursor starts before the smallest value. The call `next()` moves the cursor to the next larger value and returns it. The call `prev()` moves the cursor to the next smaller value and returns it. The call `hasNext()` reports whether a larger value exists, and `hasPrev()` reports whether a smaller value is still available. The iterator keeps only the `k` most recently produced values, so `prev()` never reaches a value older than that window.

**Constraints.** The limits are:
- **Tree** has 1 to 100 000 nodes with distinct `int` values, and its height is not bounded.
- **Window** satisfies `1 <= k <= 100 000`.
- **Calls** number at most 100 000, and the caller makes `next` only when `hasNext` is true and `prev` only when `hasPrev` is true.
- **Memory** for stored history is at most `k` values.

**Example 1.** Tree `[4,2,6,1,3,5,7]` in level order with `k = 3`. Input calls `["next","next","next","next","hasPrev","prev","prev","hasPrev","next","next","next","hasNext","next","hasNext"]` with empty arguments, output `[1,2,3,4,true,3,2,false,3,4,5,true,6,true]`.

**Example 2.** Tree `[5,2,9]` with `k = 1`. Input calls `["next","next","hasPrev","hasNext","next","hasNext","hasPrev"]` with empty arguments, output `[2,5,false,true,9,false,false]`.

**Hint.** A step backward cannot use the stack. Where do the already produced values live, and what happens to the oldest one when the window is full?

**Changed decision.** Changed from LeetCode 1586: the iterator keeps only the `k` latest values, so `prev` cannot go further back. The history is bounded by `k`, so the class stores produced values in a ring of size `k` and counts cursor positions from the first value.

#### [Boundary] Find Elements In A Contaminated Binary Tree (LeetCode 1261)
<!-- id: it37-contaminated-tree-find -->

**Prerequisites.** The Complete Binary Tree Inserter exercise above and the parent and child numbering of a tree stored in an array. It belongs here because the numbering comes from the tree shape alone, a fact that the constructor can compute once and keep.

**Problem.** A binary tree once had value 0 at the root. A node with value `x` had a left child with value `2x + 1` and a right child with value `2x + 2`. Every stored value has since been overwritten with -1, but the shape is intact. Design the class `FindElements`. The constructor receives the contaminated tree, given as a level-order list with `null` for absent children. The call `find(target)` returns `true` exactly when some node held the value `target` before the contamination.

**Constraints.** The limits are:
- **Tree** has 1 to 100 000 nodes, and its height is at most 58.
- **Stored values** are all -1.
- **Target** is a `long` with `0 <= target <= 10^18`.
- **Values** of recovered nodes can exceed `2^31 - 1`, so `int` arithmetic is wrong.

**Example 1.** Tree `[-1,-1,-1,-1,-1]`. Input calls `["find","find","find"]` with arguments `[[1],[3],[5]]`, output `[true,true,false]`.

**Example 2.** Tree `[-1,null,-1,null,-1]`. Input calls `["find","find","find","find"]` with arguments `[[2],[1],[6],[5]]`, output `[true,false,true,false]`.

**Hint.** The recovered value depends only on the path from the root. Which bits of `target + 1` describe the left and right turns?

**Changed decision.** The stored values are useless, so membership comes from the shape alone, and the recovered numbers need `long` arithmetic.

#### [Recognize] Operations On Tree (LeetCode 1993)
<!-- id: it37-operations-on-tree -->

**Prerequisites.** A **parent link** is a stored reference from a node to the node above it. Here the array `parent` holds one link for every node, so a climb to the root needs no search. This exercise is a transfer problem: treat it as an interview prompt.

**Problem.** A rooted tree has nodes numbered 0 to `n - 1`. The array `parent` gives the parent of each node, and `parent[0] = -1` marks the root. Design the class `LockingTree` with three calls. The call `lock(num, user)` locks the node for the user when the node is unlocked and returns `true`. Otherwise it returns `false`. The call `unlock(num, user)` unlocks the node and returns `true` when the same user locked it, and otherwise returns `false`. The call `upgrade(num, user)` needs three conditions: the node is unlocked, the node has at least one locked descendant, and no ancestor is locked. When all three hold, it unlocks every locked descendant, locks the node and returns `true`. Otherwise it returns `false` and changes nothing.

**Constraints.** The limits are:
- **Nodes** number 1 to 2000, and `parent` describes a valid tree rooted at 0.
- **Users** are integers with `1 <= user <= 10 000`.
- **Calls** number at most 2000 per object.
- **Descendant** means a node reached by following child links one or more times.

**Example 1.** Parent array `[-1,0,0,0,1,1,3]`. Input calls `["lock","upgrade","lock","upgrade","unlock","unlock","lock","upgrade"]` with arguments `[[4,7],[1,2],[5,3],[0,4],[1,2],[1,4],[3,3],[0,5]]`, output `[true,true,true,true,false,false,true,false]`.

**Example 2.** Parent array `[-1,0,1,2]`. Input calls `["lock","lock","upgrade","unlock","upgrade","unlock"]` with arguments `[[2,1],[0,1],[1,2],[2,1],[1,2],[1,2]]`, output `[true,true,false,true,false,false]`.

**Hint.** Which of the three conditions needs a parent link, which needs a list of children, and in which order must `upgrade` test them so that a refusal changes nothing?

**Changed decision.** Two stored structures now serve one method: the parent array answers the ancestor test, and the child lists answer the descendant search. The method mutates only after every test has passed.
