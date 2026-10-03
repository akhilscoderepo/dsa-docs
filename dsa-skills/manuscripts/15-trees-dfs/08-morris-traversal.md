<!-- lesson-kind: standard -->
<!-- lesson-id: morris-traversal -->
## Morris Traversal

<!-- stage: context -->
### The Keeper Who Carries Nothing

A lighthouse keeper walks the branching paths of a cliff garden to inspect each bench, meeting every bench on the left path before the bench at the fork and every bench on the right path after it. On earlier rounds he carried a long reel of notes and dropped a note at each fork, and he used the notes to find the way back. The reel grows with how deeply the paths branch, and on the steep south cliff, where the path is one narrow line of a hundred thousand benches, it is far heavier than he can carry.

The council has now banned carrying any reel at all, so he may keep only a few things in his pockets. He is allowed to tie a rope on the cliff itself as long as every rope is gone when the round ends. He wonders where a rope should be tied so that, at the end of a left path, it leads him back to the fork.

<!-- stage: naive -->
### Keep The Notes On A Reel

The direct method keeps the stack of notes from the previous lesson. He walks down the left side as far as it goes, dropping a note at each fork, and when the left side ends he takes the newest note, inspects that bench, and moves to its right path.

```java
static List<Integer> inspect(Node entrance) {
    List<Integer> sheet = new ArrayList<>();
    Deque<Node> notes = new ArrayDeque<>();
    Node at = entrance;
    while (at != null || !notes.isEmpty()) {
        if (at != null) { notes.push(at); at = at.left; }
        else { at = notes.pop(); sheet.add(at.val); at = at.right; }
    }
    return sheet;
}
```

The benches come out in the right order because the newest note always belongs to the nearest fork whose left side has just ended.

<!-- stage: bottleneck -->
### The Reel Grows With The Depth

At the deepest moment the reel holds one note for every fork on the way down, so it needs O(h) space for a garden of height h, and h is n for the south cliff of one hundred thousand benches. The time is fine at O(n). The cost is the extra memory, and the council's rule asks for O(1) beyond the garden itself.

The information on the reel is only where each fork is. Each fork that has a left path has, at the far end of that left path, a bench with no right path, since the far end is the last bench met on that side. That empty right path is a free place to tie a rope that points back to the fork, so the garden itself can hold the notes. The way back would then be stored inside the garden, using O(1) of the keeper's own memory, as long as every rope is removed afterwards.

<!-- stage: insight -->
### Borrow The Empty Right Link

Every node with a left subtree has an **inorder predecessor**, the node met just before it in inorder, which is the rightmost node of its left subtree. That node's right link is null, since nothing follows it inside the subtree. Morris traversal borrows that null link as a temporary **thread** that points back up to the current node, so the walk can return from the end of the left side without any stack.

At a node `cur` with a left child, find the predecessor by going left once and then right as far as possible, stopping at a null link or at a link that already points back to `cur`. If the right link is null, this is the first visit: set it to `cur` and go left. If it already points to `cur`, this is the **second arrival**: the whole left side is done, so cut the thread by setting the link to null, record the value of `cur`, and go right. A node with no left child is recorded at once, and moving right may follow a thread back to an ancestor, which is how the walk climbs without a stack.

The invariant is that every thread points from the last node of a finished or active left side to the node whose left side it closes, and a thread exists only while that left side is being walked. Each tree edge is followed at most about three times, so the walk takes O(n) time with O(1) extra space, and the tree is exactly as it was when the walk ends.

<!-- names: inorder predecessor, thread, second arrival -->

The cut of every thread on the second arrival is not optional, and it is what returns the garden to its first shape.

<!-- stage: variables -->
### Cursor, Predecessor And The Right Link

Only two references are needed. The cursor `cur` is the node being handled, and `pred` is used to find the predecessor of `cur`. The decision is the value of `pred.right` after the descent. A null value means no thread exists yet, and a value equal to `cur` means the thread was placed earlier. The output list is not extra working space, because it is the answer. The result depends on restoring `pred.right = null` before moving on from a second arrival.

<!-- stage: trace -->
### Ropes Tied And Untied On The Cliff

The first trace walks the garden 4, 2, 7, 1, 3 in level-order form, and the pointer `cur` marks the bench the keeper stands at. When he first stands at a fork with a left path, he ties a rope from the last bench of that path back to the fork and goes left. When he comes back along the rope he unties it, records the bench and moves right. The count of ropes tied at any moment is shown in the variable `ropes`.

```trace
{"cells":["4","2","7","1","3"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"sheet":"","ropes":1},"note":"The bench 4 has a left path whose last bench 3 has a free right link, so a rope is tied from 3 to 4 and the keeper goes left."},{"at":{"cur":1},"vars":{"sheet":"","ropes":2},"note":"The bench 2 has a left path whose last bench 1 has a free right link, so a rope is tied from 1 to 2 and the keeper goes left."},{"at":{"cur":3},"vars":{"sheet":"1","ropes":2},"note":"The bench 1 has no left path, so it is recorded at once and the keeper moves right."},{"at":{"cur":1},"vars":{"sheet":"1 2","ropes":1},"note":"The keeper returned to 2 along its rope from 1, so the rope is cut, the bench is recorded, and he moves right."},{"at":{"cur":4},"vars":{"sheet":"1 2 3","ropes":1},"note":"The bench 3 has no left path, so it is recorded at once and the keeper moves right."},{"at":{"cur":0},"vars":{"sheet":"1 2 3 4","ropes":0},"note":"The keeper returned to 4 along its rope from 3, so the rope is cut, the bench is recorded, and he moves right."},{"at":{"cur":2},"vars":{"sheet":"1 2 3 4 7","ropes":0},"note":"The bench 7 has no left path, so it is recorded at once and the keeper moves right."}]}
```

The second trace uses the narrow path 3, 2, null, 1, a chain that only goes left. The ropes pile up as he descends and come off in reverse order as he climbs, one at each second visit. Notice how the search for a predecessor at the bench 3 stops at a rope that is already tied, so it never walks beyond the current fork.

```trace
{"cells":["3","2","null","1"],"pointers":["cur"],"steps":[{"at":{"cur":0},"vars":{"sheet":"","ropes":1},"note":"The bench 3 has a left path whose last bench 2 has a free right link, so a rope is tied from 2 to 3 and the keeper goes left."},{"at":{"cur":1},"vars":{"sheet":"","ropes":2},"note":"The bench 2 has a left path whose last bench 1 has a free right link, so a rope is tied from 1 to 2 and the keeper goes left."},{"at":{"cur":3},"vars":{"sheet":"1","ropes":2},"note":"The bench 1 has no left path, so it is recorded at once and the keeper moves right."},{"at":{"cur":1},"vars":{"sheet":"1 2","ropes":1},"note":"The keeper returned to 2 along its rope from 1, so the rope is cut, the bench is recorded, and he moves right."},{"at":{"cur":0},"vars":{"sheet":"1 2 3","ropes":0},"note":"The keeper returned to 3 along its rope from 2, so the rope is cut, the bench is recorded, and he moves right."}]}
```

<!-- stage: code -->
### Morris Inorder With Threads

```java
final class MorrisWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        while (cur != null) {
            if (cur.left == null) {
                out.add(cur.val);
                cur = cur.right;
                continue;
            }
            Node pred = cur.left;
            while (pred.right != null && pred.right != cur) pred = pred.right;
            if (pred.right == null) {
                pred.right = cur;
                cur = cur.left;
            } else {
                pred.right = null;
                out.add(cur.val);
                cur = cur.right;
            }
        }
        return out;
    }
}
```

Finding a predecessor walks a right spine that is walked again on the second arrival, but each edge is used a bounded number of times, so the total time is O(n). The extra space is O(1) besides the output.

<!-- stage: applicability -->
### When Even The Stack Is Too Much

Use this walk when a traversal must take O(1) extra memory, for example on a structure so large that even a stack of its height is unwelcome, and when the program may change the tree temporarily and put it back. The invariant is that every temporary link points from the end of an active left side back to the node that owns it, and it is cut at the second arrival.

A false friend is the idea that this walk is read-only. For a moment the tree contains a cycle, so if the walk stops early, or another reader traverses the tree in the meantime, it sees a structure that is not a tree. Forgetting the cut leaves the right links changed for good, and any later recursive walk then loops through the same nodes without end. Another false friend is calling it faster, when it does the same O(n) work with a larger constant.

In Java, never share the tree with another thread during the walk, and finish the loop through every path, since an exception in the middle leaves ropes behind.

<!-- stage: exercises -->
### Exercises

#### [Build] Find Inorder Predecessor (Author exercise)
<!-- id: tr-find-predecessor -->

**Prerequisites.** The iterative traversals and the ordering of inorder.

**Problem.** A binary tree with distinct labels is given as a level-order array, together with the label `x` of one of its nodes. Return the label of the rightmost node in the left subtree of `x`, which is the node met just before `x` in inorder, or -1 when `x` has no left child.

**Constraints.** 1 <= values.length <= 2000, the labels are distinct integers between 0 and 100000, and `x` is one of them.

**Example 1.** Input `values = [4, 2, 7, 1, 3]`, `x = 4`, output `3`.

**Example 2.** Input `values = [4, 2, 7, 1, 3]`, `x = 1`, output `-1`.

**Hint.** Where does the search go first, and when does it stop?

**Changed decision.** The search steps left once and then right as long as a right child exists, so it ends on the node whose right link is null.

#### [Vary] Create And Remove One Thread (Author exercise)
<!-- id: tr-create-remove-thread -->

**Prerequisites.** The Find Inorder Predecessor rung and the idea of a temporary link.

**Problem.** Run the full Morris inorder walk on a level-order tree and return `[created, removed, mostAtOnce]`, the number of threads tied, the number cut, and the largest number of threads existing at the same moment. The empty tree gives `[0, 0, 0]`.

**Constraints.** 0 <= values.length <= 2000 and the labels are distinct integers.

**Example 1.** Input `values = [2, 1, 3]`, output `[1, 1, 1]`.

**Example 2.** Input `values = [1, 2, null, 3]`, output `[2, 2, 2]`.

**Hint.** What does the walk see the first time it reaches a node, and what the second time?

**Changed decision.** The same node is reached twice when it has a left child, and only the value of the predecessor's right link tells the two arrivals apart.

#### [Boundary] No Left Child And Existing Thread (Author exercise)
<!-- id: tr-direct-versus-restored -->

**Prerequisites.** The Create And Remove One Thread rung.

**Problem.** Run the Morris walk on a level-order tree and return `[direct, restored]`, where `direct` counts nodes that were recorded the moment they were reached because they have no left child, and `restored` counts nodes recorded on a second arrival after cutting a thread. The empty tree gives `[0, 0]`.

**Constraints.** 0 <= values.length <= 2000 and the labels are distinct integers.

**Example 1.** Input `values = [1, null, 2, null, 3]`, output `[3, 0]`.

**Example 2.** Input `values = [2, 1, 3]`, output `[2, 1]`.

**Hint.** Which nodes are ever reached a second time?

**Changed decision.** A node without a left child is recorded at once, and a node with one is recorded only after its thread is found and cut.

#### [Recognize] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: tr-morris-inorder -->

**Prerequisites.** The Direct Versus Restored rung and the cut of every thread.

**Problem.** Walk a level-order tree in inorder using Morris threading and no stack. Return an array whose first entry is the number of threads created, followed by the inorder values. The tree must be exactly as it was before the walk.

**Constraints.** 0 <= values.length <= 2000 and the labels are distinct integers between -100000 and 100000.

**Example 1.** Input `values = [2, 1, 3]`, output `[1, 1, 2, 3]`.

**Example 2.** Input `values = [1, null, 2, 3]`, output `[1, 1, 3, 2]`.

**Hint.** When is a thread cut, and what is the right link of the predecessor at that moment?

**Changed decision.** The walk may change the tree during the traversal, and it must restore every link before it returns.
