<!-- lesson-kind: standard -->
<!-- lesson-id: iterative-dfs -->
## Iterative DFS

<!-- stage: context -->
### The Guide With A Desk Of Notes

A museum guide leads a visitor through rooms that branch into smaller rooms, and the visitor wants every room seen once, going as deep into one wing as possible before returning. Until now the guide has kept the route in her head, remembering each doorway she came through so she can step back to it. The new east wing is a single corridor of one hundred thousand rooms, each opening into only the next, and her memory of the way back fills up long before she reaches the end. She loses her place and has to stop.

The museum manager suggests that she stop remembering and write instead. At each room she can jot the rooms still to visit on a pile of notes on her desk, always taking the next job from the top. She wants to know which order to write the notes in so that the visit goes the way she wants.

<!-- stage: naive -->
### Let The Recursion Remember

The direct method is the recursive walk from the previous lesson. Each room is a call, the call on a room makes the calls on its two sub-rooms, and the program remembers the way back by leaving every unfinished call waiting.

```java
static void preorder(Node room, List<Integer> out) {
    if (room == null) return;
    out.add(room.val);
    preorder(room.left, out);
    preorder(room.right, out);
}
```

For ordinary trees it is short and correct, because the waiting calls hold exactly the doorways passed through so far.

<!-- stage: bottleneck -->
### The Waiting Calls Run Out Of Room

The number of waiting calls at the deepest point equals the height h of the tree, so the memory used is O(h) frames. The thread's call stack has a fixed size, which on a default Java setup holds some thousands of frames, and a tree that is a straight chain of a hundred thousand nodes has h = n. The walk then ends with a `StackOverflowError` even though the tree itself is small and the time is only O(n). The program cannot catch this and carry on in any useful way, because the call that overflowed was in the middle of the job.

The cost is not the number of steps. The cost is that the bookkeeping lives in a place of fixed size that the program does not control. If the same bookkeeping lived in a collection on the heap, the limit would be the available memory, and the program could decide in what order the notes are written and read.

<!-- stage: insight -->
### Write The Waiting Rooms Down

Replace the hidden waiting calls with an **explicit stack**, a `Deque` used at one end. The stack holds the **pending subtrees**, the rooms whose whole subtree is still to be visited. The walk takes the top entry, does the node action, and writes down the pending subtrees it leaves behind. Because the structure is last in, first out, the entry written last is the one processed next. Preorder wants the left subtree next, so the left child must be pushed after the right child. Pushing left first would send the visit down the right side first, which is a different walk.

For inorder the label of a node must wait until its left subtree is finished, so the stack holds the nodes whose left side is still open. Push the **left spine**, the node and its left child and that child's left child down to the end, then pop a node, visit it and move to its right child, where the same spine descent starts again. For postorder a node must wait for both sides, so each stack entry needs a visit state, or the walk must remember the last node completed.

The invariant is that the stack holds exactly the subtrees that are still waiting, the top is the one that must run next, and every node is pushed once and popped once, so the work is O(n) with the stack as large as the height.

<!-- names: explicit stack, pending subtrees, left spine -->

An empty child is never pushed, because a `Deque` rejects null.

<!-- stage: variables -->
### Pending Notes And The Current Room

Preorder needs one variable, the stack `pending`, which starts with the root unless the root is null. Inorder needs two, the stack and a cursor `cur` that follows the spine and then the right child. In both walks the output list receives a value at the moment the node action runs. Each push is guarded by a null test, because `ArrayDeque` throws `NullPointerException` on null, and the loop ends when the stack is empty and, for inorder, the cursor is also null.

<!-- stage: trace -->
### The Pile At Every Pop

The first trace runs the preorder walk on the shelf index 4, 2, 7, 1, 3 in level-order form. The pointer `node` marks the room just taken from the pile. The pile is shown with its top on the right. Each step takes the top room, writes its label, then pushes the right sub-room before the left one, so the left room sits on top and is taken next. Notice that the room 7 waits underneath while the whole left wing is handled, and is taken only when the pile has nothing above it.

```trace
{"cells":["4","2","7","1","3"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"pile":"7 2","sheet":"4"},"note":"The room 4 came off the top of the pile and is written down. It leaves right 7 then left 2 on the pile."},{"at":{"node":1},"vars":{"pile":"7 3 1","sheet":"4 2"},"note":"The room 2 came off the top of the pile and is written down. It leaves right 3 then left 1 on the pile."},{"at":{"node":3},"vars":{"pile":"7 3","sheet":"4 2 1"},"note":"The room 1 came off the top of the pile and is written down. It has no sub-rooms, so nothing is added to the pile."},{"at":{"node":4},"vars":{"pile":"7","sheet":"4 2 1 3"},"note":"The room 3 came off the top of the pile and is written down. It has no sub-rooms, so nothing is added to the pile."},{"at":{"node":2},"vars":{"pile":"empty","sheet":"4 2 1 3 7"},"note":"The room 7 came off the top of the pile and is written down. It has no sub-rooms, so nothing is added to the pile."}]}
```

The second trace runs the spine version on the index 6, 2, 9, 1, 4. The cursor first slides down the left side and every room it passes is put on the pile, then the top room is taken, written down, and the cursor moves to its right child. The sheet therefore grows in sorted order, and the pile never holds more rooms than the length of the left spine currently being followed.

```trace
{"cells":["6","2","9","1","4"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"pile":"6","sheet":""},"note":"The cursor reaches the room 6, which is put on the pile before the cursor goes to its left."},{"at":{"node":1},"vars":{"pile":"6 2","sheet":""},"note":"The cursor reaches the room 2, which is put on the pile before the cursor goes to its left."},{"at":{"node":3},"vars":{"pile":"6 2 1","sheet":""},"note":"The cursor reaches the room 1, which is put on the pile before the cursor goes to its left."},{"at":{"node":3},"vars":{"pile":"6 2","sheet":"1"},"note":"The left side is finished, so the room 1 is taken off the pile and written down, and the cursor moves to its right."},{"at":{"node":1},"vars":{"pile":"6","sheet":"1 2"},"note":"The left side is finished, so the room 2 is taken off the pile and written down, and the cursor moves to its right."},{"at":{"node":4},"vars":{"pile":"6 4","sheet":"1 2"},"note":"The cursor reaches the room 4, which is put on the pile before the cursor goes to its left."},{"at":{"node":4},"vars":{"pile":"6","sheet":"1 2 4"},"note":"The left side is finished, so the room 4 is taken off the pile and written down, and the cursor moves to its right."},{"at":{"node":0},"vars":{"pile":"empty","sheet":"1 2 4 6"},"note":"The left side is finished, so the room 6 is taken off the pile and written down, and the cursor moves to its right."},{"at":{"node":2},"vars":{"pile":"9","sheet":"1 2 4 6"},"note":"The cursor reaches the room 9, which is put on the pile before the cursor goes to its left."},{"at":{"node":2},"vars":{"pile":"empty","sheet":"1 2 4 6 9"},"note":"The left side is finished, so the room 9 is taken off the pile and written down, and the cursor moves to its right."}]}
```

<!-- stage: code -->
### Stack Based Preorder And Inorder

```java
final class IterativeWalks {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static List<Integer> preorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> pending = new ArrayDeque<>();
        if (root != null) pending.push(root);
        while (!pending.isEmpty()) {
            Node node = pending.pop();
            out.add(node.val);
            if (node.right != null) pending.push(node.right);
            if (node.left != null) pending.push(node.left);
        }
        return out;
    }

    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> pending = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !pending.isEmpty()) {
            while (cur != null) { pending.push(cur); cur = cur.left; }
            cur = pending.pop();
            out.add(cur.val);
            cur = cur.right;
        }
        return out;
    }
}
```

Each node is pushed once and popped once, so both walks take O(n) time, and the stack holds at most h entries for height h, which is O(n) on a chain but stored on the heap.

<!-- stage: applicability -->
### When The Call Stack Is Too Small

Switch to a stack you control when the tree can be very deep, when the walk must pause and resume, or when the language gives a limited call depth. Chains of inputs from users, sorted insertions into a plain binary tree, and parsed nesting all produce depth far above the usual. The invariant is that the stack lists the subtrees still waiting, with the next one on top, and that each subtree enters and leaves it exactly once.

A false friend is the push order. Pushing the left child first and the right child second makes a stack walk reach the right side first, so the output is a mirrored preorder that still looks plausible on symmetric trees. Another false friend is the idea that the iterative form is cheaper, when it uses the same O(h) space, only on the heap. A last one is that postorder follows the preorder recipe, when it needs a visit state.

In Java, prefer `ArrayDeque` to the old `Stack` class, test children for null before pushing, and use `pop` and `push` at the same end consistently.

<!-- stage: exercises -->
### Exercises

#### [Build] Iterative Preorder (Author exercise)
<!-- id: tr-iter-preorder -->

**Prerequisites.** The recursive preorder walk from the previous lesson.

**Problem.** Walk a level-order tree with a stack that starts holding the root, where each step pops the top node, records it, then pushes its right child and then its left child, skipping missing ones. Return an array whose first entry is the largest stack size ever reached, measured after each round of pushes, followed by the recorded values in order.

**Constraints.** 0 <= values.length <= 1000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [1, 2, 3, 4]`, output `[2, 1, 2, 4, 3]`.

**Example 2.** Input `values = []`, output `[0]`.

**Hint.** Which child must be pushed last so that it is on top? When is the size measured?

**Changed decision.** The right child is pushed before the left one, so the last-in, first-out stack hands back the left side first.

#### [Vary] Iterative Inorder (Author exercise)
<!-- id: tr-iter-inorder -->

**Prerequisites.** The Iterative Preorder rung and its stack discipline.

**Problem.** Return the inorder values of a level-order tree using a stack and a cursor, with no recursion. Push the whole left spine, pop and record a node, and continue from its right child.

**Constraints.** 0 <= values.length <= 1000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [4, 2, 7, 1, 3]`, output `[1, 2, 3, 4, 7]`.

**Example 2.** Input `values = [3, null, 5, 4]`, output `[3, 4, 5]`.

**Hint.** What must be on the stack when a node is popped, and where does the cursor go next?

**Changed decision.** A node is recorded when it is popped and not when it is pushed, since its left side must be finished first.

#### [Boundary] Deep Skewed Tree (Author exercise)
<!-- id: tr-deep-skewed -->

**Prerequisites.** Both iterative walks above and the null rule of the stack.

**Problem.** A chain has `n` nodes holding the values 1 to n from the top down, and a side flag says whether each node's only child is on the left or on the right. Return `[size, first, last]` for its inorder sequence, with `first` and `last` equal to -1 when the chain is empty. The code must not recurse and must not fail on a null root.

**Constraints.** 0 <= n <= 300000 and the side is either `left` or `right`.

**Example 1.** Input `n = 0, side = left`, output `[0, -1, -1]`.

**Example 2.** Input `n = 3, side = left`, output `[3, 3, 1]`.

**Hint.** What is the first node popped for a left chain, and how deep does the stack get?

**Changed decision.** The walk keeps its pending nodes on the heap, so the depth of the chain costs memory but cannot overflow the call stack.

#### [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: tr-iter-postorder-mirror -->

**Prerequisites.** The inorder rung and the push-order rule from the build rung.

**Problem.** Return the values of a level-order tree in mirrored postorder, which visits the right subtree first, then the left subtree, then the node. The walk must use an explicit stack and no recursion.

**Constraints.** 0 <= values.length <= 1000 and values are integers between -1000 and 1000.

**Example 1.** Input `values = [5, 3, 8, 1]`, output `[8, 1, 3, 5]`.

**Example 2.** Input `values = [2, null, 7, 6]`, output `[6, 7, 2]`.

**Hint.** What does the ordinary preorder look like when it is read backwards?

**Changed decision.** The node is delayed until both subtrees finish, here by recording in preorder and reversing, or by a visit state on the stack.
