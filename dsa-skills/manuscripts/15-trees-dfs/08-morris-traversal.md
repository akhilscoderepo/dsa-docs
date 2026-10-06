<!-- lesson-kind: standard -->
<!-- lesson-id: morris-traversal -->
## Walk A Tree Without A Stack

<!-- stage: context -->
### A Routine With No Spare Memory

A firmware routine must read every value of a binary tree that lives in a fixed memory region, in sorted position order from the left side to the right side. The routine runs inside an interrupt handler, where the program may not allocate and the call stack holds only a few hundred bytes. The tree can have 50,000 nodes in a long chain. A recursive walk overflows the call stack, and the explicit stack of the previous lesson needs one entry per pending node, which is also too much memory.

The walk must remember where to continue after it finishes the left side of a node. The routine has no place to store that information outside the tree. The question is whether the tree itself can hold it for a short time.

<!-- stage: naive -->
### Keeping Pending Nodes In A Deque

The method from the previous lesson stores every node that waits for its turn in a `Deque`. It pushes the left spine, pops a node, writes the value, and moves to the right child.

```java
import java.util.*;

final class StackedInorder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int peakWaiting(Node root) {
        Deque<Node> waiting = new ArrayDeque<>();
        Node cur = root;
        int peak = 0;
        while (cur != null || !waiting.isEmpty()) {              // stop when no node is left anywhere
            while (cur != null) { waiting.push(cur); cur = cur.left; }   // every node on the left spine waits
            peak = Math.max(peak, waiting.size());               // record the largest number of waiting nodes
            cur = waiting.pop().right;                           // write the node, then go right
        }
        return peak;
    }
}
```

Take the tree with root 4 and right child 6, where the left child 2 has children 1 and 3. The method reaches a peak of 3 waiting nodes, which are 4, 2 and 1. The walk visits the values in the right order.

<!-- stage: bottleneck -->
### Counting The Waiting Nodes

```predict
The tree is a chain of n nodes where each node has only a left child. What is the peak number of waiting nodes, and how much extra memory does the method need?

All n nodes wait at once, because the left spine is the whole tree. The extra memory is O(n), which is the same as the height h of the chain.
```

The time is O(n), and the extra memory is O(h). A recursive method has the same O(h) cost in its call stack. For a balanced tree the height is small, and for a chain it equals n. A routine with no allocation cannot pay O(h) in any form.

The waiting nodes carry one piece of information: after the left subtree of a node is finished, the walk must return to that node. The node that finishes the left subtree is its last node in inorder, and that node has no right child. Its empty `right` reference is unused space inside the tree, and it can store the way back.

<!-- stage: insight -->
### Borrowing An Empty Right Reference

The walk can leave itself a link that points back to the node it will need, and it can remove the link after use. The tree changes during the walk and is identical again at the end.

<!-- names: predecessor, thread, second arrival -->

#### The Last Node Of The Left Side

The **predecessor** of a node that has a left child is the last node of its left subtree in inorder. It is found by moving to the left child and then following `right` references until a `right` reference is `null`. The predecessor has no right child, because inorder visits the right subtree of a node after the node itself.

#### A Temporary Link Back

A **thread** is a temporary link that the walk stores in the `right` reference of the predecessor, so that it points to the node whose left side is being walked. When the walk arrives at a node with a left child, it finds the predecessor and looks at its `right` reference. If that reference is `null`, the walk stores the thread and moves to the left child. The walk will come back to the node by following the thread after the left side is done.

#### The Second Visit Removes The Link

The **second arrival** at a node happens when the walk reaches the node again through a thread. The search for the predecessor then ends on a `right` reference that already equals the node. The walk removes the thread by setting that reference back to `null`, writes the value of the node, and moves to the right child. A node with no left child needs no thread. The walk writes it at once and moves to its right child, which can be a real child or a thread to an ancestor.

#### Why The Cost Stays Linear

Each edge that goes to a right child lies on the predecessor search of exactly one node. The walk runs that search twice at most, once to create the thread and once to remove it. The total work is O(n), and the extra memory is O(1), because the method keeps only two references.

<!-- stage: variables -->
### The References And The Cases

- **cur** is the node where the walk stands, and the walk ends when it is `null`.
- **pred** is the predecessor of `cur`, found by following `right` from `cur.left` until a `null` or until a reference equal to `cur`.
- **thread** is the `right` reference of `pred` when it equals `cur`.
- **out** receives one value per node.

The walk has three cases at each node. No left child means write the node and move right. A `null` at the end of the search means create a thread and move left. A reference equal to `cur` at the end of the search means remove the thread, write the node, and move right.

<!-- stage: trace -->
### Threads Appearing And Disappearing

#### Walking A Five-Node Tree

The tree has root 4 and right child 6. The root's left child is 2, which has children 1 and 3. The pointer `cur` marks the node where the walk stands, and `pred` marks the predecessor when a search runs. The variable `threads` lists the links that exist now, written as the node that holds the link and its target.

```trace
{"cells":["4","2","6","1","3"],"pointers":["cur","pred"],"steps":[{"at":{"cur":0,"pred":4},"vars":{"out":"empty","threads":"3 to 4"},"note":"The predecessor of the node 4 is the node 3, and its right reference is empty. The walk stores a thread to 4 and moves to the left child."},{"at":{"cur":1,"pred":3},"vars":{"out":"empty","threads":"1 to 2, 3 to 4"},"note":"The predecessor of the node 2 is the node 1, and its right reference is empty. The walk stores a thread to 2 and moves to the left child."},{"at":{"cur":3,"pred":-1},"vars":{"out":"1","threads":"1 to 2, 3 to 4"},"note":"The node 1 has no left child, so the walk writes it and moves right, along a thread back to an ancestor."},{"at":{"cur":1,"pred":3},"vars":{"out":"1 2","threads":"3 to 4"},"note":"The predecessor 1 already links to the node 2, so this is the second arrival. The walk removes the thread, writes 2 and moves right."},{"at":{"cur":4,"pred":-1},"vars":{"out":"1 2 3","threads":"3 to 4"},"note":"The node 3 has no left child, so the walk writes it and moves right, along a thread back to an ancestor."},{"at":{"cur":0,"pred":4},"vars":{"out":"1 2 3 4","threads":"none"},"note":"The predecessor 3 already links to the node 4, so this is the second arrival. The walk removes the thread, writes 4 and moves right."},{"at":{"cur":2,"pred":-1},"vars":{"out":"1 2 3 4 6","threads":"none"},"note":"The node 6 has no left child and no right link, so the walk writes it and ends."}]}
```

The root receives its thread from node 3 and the node 2 receives its thread from node 1. The values appear as 1, 2, 3, 4, 6, and the last step leaves no thread in the tree.

#### A Predecessor Below The Left Child

The second tree has root 3 and a left child 1. The node 1 has a right child 2. The predecessor of the root is therefore not the left child but the node 2, which is one step further down.

```trace
{"cells":["3","1","null","null","2"],"pointers":["cur","pred"],"steps":[{"at":{"cur":0,"pred":4},"vars":{"out":"empty","threads":"2 to 3"},"note":"The predecessor of the node 3 is the node 2, and its right reference is empty. The walk stores a thread to 3 and moves to the left child."},{"at":{"cur":1,"pred":-1},"vars":{"out":"1","threads":"2 to 3"},"note":"The node 1 has no left child, so the walk writes it and moves right, along its right child."},{"at":{"cur":4,"pred":-1},"vars":{"out":"1 2","threads":"2 to 3"},"note":"The node 2 has no left child, so the walk writes it and moves right, along a thread back to an ancestor."},{"at":{"cur":0,"pred":4},"vars":{"out":"1 2 3","threads":"none"},"note":"The predecessor 2 already links to the node 3, so this is the second arrival. The walk removes the thread, writes 3 and moves right."}]}
```

The search for the predecessor of 3 follows the `right` reference of node 1 and ends at node 2. The walk reaches 3 a second time through the thread from node 2, removes it, and writes 3.

<!-- stage: code -->
### The Walk In Code

```java
import java.util.*;

final class ThreadedWalk {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Node cur = root;
        while (cur != null) {                                    // one round per move of the walk
            if (cur.left == null) {
                out.add(cur.val);                                // no left side, so write the node now
                cur = cur.right;                                 // a real child or a thread to an ancestor
            } else {
                Node pred = cur.left;                            // start the search in the left subtree
                while (pred.right != null && pred.right != cur) pred = pred.right;   // stop at null or at a thread
                if (pred.right == null) {
                    pred.right = cur;                            // first arrival: store the way back
                    cur = cur.left;
                } else {
                    pred.right = null;                           // second arrival: remove the thread
                    out.add(cur.val);                            // the left side is done, so write the node
                    cur = cur.right;
                }
            }
        }
        return out;
    }
}
```

The walk writes no field except `right` references, and every thread that it stores is removed on the second arrival. The method stores only the tree and the output list.

- **Time** is O(n), because every predecessor search is paid for by two uses of a tree edge.
- **Space** is O(1) beyond the output list, because the walk holds only `cur` and `pred`.

<!-- stage: applicability -->
### Deciding When To Change The Tree

#### Stating What The Walk Restores

The invariant is that every `right` reference that is not a real child is a thread that points to an ancestor whose left side is still being walked. A walk that reaches the end has removed every thread, so the tree equals the input. Check that sentence before using the method.

#### Finding The False Friend

A walk that stores threads and forgets to remove them looks fine on a single run, and it is the false friend of this lesson. The output is correct, but the tree now contains a cycle, and any later traversal never ends. The same damage happens if the walk stops early without finishing the removals.

#### No-Go Conditions

Do not use the method when another reader may look at the tree during the walk, because that reader sees threads. Do not use it on a tree that is read-only memory or shared between threads. If the caller can afford O(h) extra memory, the explicit stack is shorter and cannot corrupt the tree.

<!-- stage: exercises -->
### Exercises

#### [Build] Find Inorder Predecessor (Author exercise)
<!-- id: mo-predecessor -->

**Prerequisites.** The predecessor from this lesson.

**Problem.** A binary tree node `cur` has a left child. Return the value of the predecessor of `cur`, which is the last node of its left subtree in inorder. Follow `right` references from the left child until a `right` reference is `null`. The tree is not modified.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^4, and `cur.left` is not `null`.
- **Values** are integers between -10^4 and 10^4.
- **Answer** is the value of one node in the left subtree of `cur`.
- **Mutation** is not allowed, and every `right` reference is a real child.

**Example 1.** Input the node 4 in the tree with root 4, left child 2 with children 1 and 3, and right child 6, output 3.

**Example 2.** Input the node 3 whose left child 1 has a right child 2, output 2.

**Hint.** Where does the search start? When does it stop?

**Changed decision.** The search follows only `right` references, and it stops at `null`.

#### [Vary] Create And Remove One Thread (Author exercise)
<!-- id: mo-one-thread -->

**Prerequisites.** The exercise above.

**Problem.** Write a method `step(cur)` for a node `cur` that has a left child. It finds the predecessor `p` of `cur`, with the search stopping at `null` or at a reference equal to `cur`. If `p.right` is `null`, it sets `p.right = cur` and returns `cur.left`. Otherwise it sets `p.right = null` and returns `cur.right`.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^4, and `cur.left` is not `null`.
- **Values** are integers that the answer does not use.
- **Answer** is the node where the walk continues, or `null`.
- **Mutation** is allowed only for the single `right` reference of the predecessor.

**Example 1.** Input the root 4 of the tree with right child 6 and left child 2, which has children 1 and 3. On the first call the output is the node 2, and the node 3 now has `right` equal to the node 4.

**Example 2.** Input the same node 4 on a second call, output the node 6, and the node 3 has `right` equal to `null` again.

**Hint.** How does the search tell the first call from the second call? Which reference differs?

**Changed decision.** The same method handles two cases and tells them apart by what the predecessor's `right` holds.

#### [Boundary] No Left Child And Existing Thread (Author exercise)
<!-- id: mo-first-k -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary tree and an integer `k`, return the first `k` values of the inorder using the threaded walk with O(1) extra memory beyond the output. The tree must be identical to the input after the call. The value of `k` can be 0 or larger than the number of nodes.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers between -10^4 and 10^4.
- **k** is an integer between 0 and 2 * 10^4.
- **Answer** has `min(k, n)` values, and no thread may remain.

**Example 1.** Input root 9 with right child 12 and left child 5 that has children 2 and 7, and `k = 3`, output `2, 5, 7`. The tree is unchanged.

**Example 2.** Input the same tree and `k = 0`, output the empty list.

**Hint.** What is still in the tree at the moment the k-th value is written? What must happen to it?

**Changed decision.** The walk records only the first `k` values and still finishes every removal.

#### [Recognize] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: mo-inorder -->

**Prerequisites.** All three exercises above.

**Problem.** Given the root of a binary tree, return its inorder values using the threaded walk with O(1) extra memory beyond the output. After the call, every `left` and `right` reference in the tree must equal its value before the call.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** are integers between -100 and 100.
- **Answer** is a list with one value per node.
- **Mutation** is allowed during the walk, and none may remain afterward.

**Example 1.** Input root 7 with left child 3 that has a right child 5, and right child 9, output `3, 5, 7, 9`, and the tree is unchanged.

**Example 2.** Input `root = null`, output the empty list.

**Hint.** Which case has no thread at all? Which line removes a thread?

**Changed decision.** The walk may change the tree while it runs and must restore it before it returns.
