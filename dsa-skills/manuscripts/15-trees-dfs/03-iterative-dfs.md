<!-- lesson-kind: standard -->
<!-- lesson-id: iterative-dfs -->
## Walk A Tree With Your Own Stack

<!-- stage: context -->
### A Formatter Crashes On A Long Sum

A code formatter parses a generated line of the form `1+1+1+ ... +1` with 100,000 terms. A parser that groups additions from the left builds a tree in which every node has its previous sum as the left child. The tree is one long chain. The formatter walks the tree with a recursive method, and the program stops with `StackOverflowError` before it prints anything.

The tree has only 100,000 nodes, and the walk does a constant amount of work per node. The failure comes from how the walk remembers where it is. This lesson shows how to keep that memory in a structure that the program controls.

<!-- stage: naive -->
### Writing The Walk As A Recursive Method

The recursive method keeps its position in the call stack. Each call to the method waits for its child calls to return.

```java
final class RecursiveText {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void write(Node node, StringBuilder text) {
        if (node == null) return;                 // nothing to write for a missing child
        text.append(node.val).append(' ');        // write this node before its children
        write(node.left, text);                   // the call waits here until the left side is done
        write(node.right, text);                  // then the call waits here for the right side
    }
}
```

For the tree with root 1, left child 2 and right child 3, the method writes `1 2 3 `. For a chain of three nodes it opens three calls at once, then closes them in reverse order. The result is correct for every tree that the call stack can hold.

<!-- stage: bottleneck -->
### Counting The Calls That Stay Open

```predict
In the chain of 100,000 nodes, how many calls of write are open at the same time at the deepest point, and does the number depend on n or on the height of the tree?

All 100,000 calls are open at once, because each node waits for its left call to return. The number of open calls equals the height h of the tree, and h equals n for a chain.
```

The time is O(n), which is fine. The memory is the problem. Each open call occupies one frame of the call stack, and the number of open calls equals the height h of the tree, so the space is O(h). A balanced tree of a million nodes has height about 20, and a chain of a million nodes has height one million.

The call stack has a fixed size that the thread receives when it starts. A program cannot grow it while running, and a chain can need more frames than it holds. Recursion therefore ties the largest tree that the walk can handle to the size of a memory area that the program does not control.

<!-- stage: insight -->
### Keeping Waiting Nodes In Your Own Stack

The recursive method already does one thing correctly. It remembers which nodes still wait for work, in the order they must resume. An **explicit stack** is a `Deque` of nodes that the program owns and manages with `push` and `pop`. It stores the same waiting nodes as the call stack does. It lives on the heap, so available memory limits its size and the thread stack does not.

<!-- names: explicit stack, left spine, last visited -->

#### Preorder Needs Only Pending Subtrees

In preorder the node is handled the moment it is reached, so nothing waits except the subtrees that have not started. The stack holds those subtrees. The loop pops one node, handles it, and pushes its two children. A stack is last in, first out, so the child pushed last is popped first. The loop pushes `right` and then `left`, so the left subtree is popped next. Pushing `left` first gives right-first order, which is the false friend of this lesson.

#### Inorder Walks The Left Spine

In inorder a node must wait until its whole left subtree is done. The **left spine** of a node is the chain that starts at the node and follows `left` references until `null`. The loop pushes every node of the left spine, then pops the top node, which is the deepest one and has no left side left to do. It handles that node and moves to its right child, then pushes the left spine of that child. Each node on the stack is waiting for its action.

#### Postorder Needs To Know What Was Done

In postorder a node waits for both sides. After its left side is finished, the loop meets the node on top of the stack a first time and must decide whether the right side is done. The variable **last visited** holds the node that was written most recently. If the right child of the top node exists and is not equal to `last visited`, the right side has not started, so the loop moves into it. Otherwise the loop writes the top node, pops it, and records it as `last visited`.

#### Why The Memory Limit Moves

Each node enters the stack once and leaves once, so the walk costs O(n) time. The stack holds at most one root-to-node path in the inorder and postorder loops, and it holds at most h + 1 nodes in the preorder loop. The memory is still O(h), but it now sits in an object on the heap, where a deep tree fits.

<!-- stage: variables -->
### The State Of Each Loop

- **stack** holds the nodes that still wait for work, and the top of the stack is the next node to resume.
- **cur** holds the node that the loop is about to enter, or `null` when the loop must pop.
- **last visited** holds the node written most recently, and it is `null` before the first write.
- **out** receives one value per node, in the order of the chosen walk.

The preorder loop needs only `stack` and `out`. The inorder loop adds `cur`. The postorder loop adds `last visited`.

<!-- stage: trace -->
### Following The Stack Step By Step

#### Preorder On A Five-Node Tree

The tree has root 7, left child 3 and right child 9, and node 3 has children 1 and 5. A step shows the node that the loop just popped and handled. The variable `stack` lists the waiting nodes from the top of the stack, and `out` lists the values written so far.

```trace
{"cells":["7","3","9","1","5"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"stack":"3 9","out":"7"},"note":"The loop pops the node 7 and writes it. Its children go in as 9 then 3, so the left child ends on top."},{"at":{"node":1},"vars":{"stack":"1 5 9","out":"7 3"},"note":"The loop pops the node 3 and writes it. Its children go in as 5 then 1, so the left child ends on top."},{"at":{"node":3},"vars":{"stack":"5 9","out":"7 3 1"},"note":"The loop pops the node 1 and writes it. It has no children, so nothing is pushed."},{"at":{"node":4},"vars":{"stack":"9","out":"7 3 1 5"},"note":"The loop pops the node 5 and writes it. It has no children, so nothing is pushed."},{"at":{"node":2},"vars":{"stack":"empty","out":"7 3 1 5 9"},"note":"The loop pops the node 9 and writes it. It has no children, so nothing is pushed."}]}
```

The root is popped first. Its right child 9 goes in before its left child 3, so the node 3 is on top and is popped next. The node 9 stays at the bottom until the whole subtree of 3 is done.

#### Postorder With A Missing Right Child

The second tree has root 4 and left child 2, and the node 2 has children 1 and 3. The root has no right child. A step shows the node that was pushed, or the node that was written and popped.

```trace
{"cells":["4","2","null","1","3"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"stack":"4","out":"empty"},"note":"The loop pushes the node 4 and moves to its left child."},{"at":{"node":1},"vars":{"stack":"2 4","out":"empty"},"note":"The loop pushes the node 2 and moves to its left child."},{"at":{"node":3},"vars":{"stack":"1 2 4","out":"empty"},"note":"The loop pushes the node 1 and moves to its left child."},{"at":{"node":3},"vars":{"stack":"2 4","out":"1"},"note":"The node 1 is on top and it has no right child, so the loop writes and pops it."},{"at":{"node":1},"vars":{"stack":"2 4","out":"1"},"note":"The node 2 is on top and its right child 3 is not the last node written, so the loop enters the right side."},{"at":{"node":4},"vars":{"stack":"3 2 4","out":"1"},"note":"The loop pushes the node 3 and moves to its left child."},{"at":{"node":4},"vars":{"stack":"2 4","out":"1 3"},"note":"The node 3 is on top and it has no right child, so the loop writes and pops it."},{"at":{"node":1},"vars":{"stack":"4","out":"1 3 2"},"note":"The node 2 is on top and its right child 3 was just written, so the loop writes and pops it."},{"at":{"node":0},"vars":{"stack":"empty","out":"1 3 2 4"},"note":"The node 4 is on top and it has no right child, so the loop writes and pops it."}]}
```

The node 2 is written only after the node 3, because the loop saw that its right child 3 was not yet `last visited`. The root has no right child, so it is written right after the node 2.

<!-- stage: code -->
### The Three Loops In Code

```java
import java.util.*;

final class StackWalks {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static List<Integer> preorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        if (root != null) stack.push(root);                      // an empty tree leaves the stack empty
        while (!stack.isEmpty()) {                               // one pop per node
            Node node = stack.pop();
            out.add(node.val);                                   // handle the node as soon as it is popped
            if (node.right != null) stack.push(node.right);      // right goes in first, so it comes out last
            if (node.left != null) stack.push(node.left);        // left goes in last, so it comes out next
        }
        return out;
    }

    static List<Integer> inorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root;
        while (cur != null || !stack.isEmpty()) {                // stop when nothing is left to enter or pop
            while (cur != null) { stack.push(cur); cur = cur.left; }   // push the whole left spine
            Node node = stack.pop();                             // the deepest waiting node has an empty left side
            out.add(node.val);                                   // its left subtree is done, so handle it
            cur = node.right;                                    // then enter the right subtree
        }
        return out;
    }

    static List<Integer> postorder(Node root) {
        List<Integer> out = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node cur = root, last = null;
        while (cur != null || !stack.isEmpty()) {
            while (cur != null) { stack.push(cur); cur = cur.left; }   // push the left spine
            Node top = stack.peek();                             // look at the node without removing it
            if (top.right != null && top.right != last) {
                cur = top.right;                                 // the right side has not started
            } else {
                out.add(top.val);                                // both sides are done
                last = stack.pop();                              // remember what was written
            }
        }
        return out;
    }
}
```

Each loop works unchanged on an empty tree and on a node with one child. The loop conditions test `cur` and the stack, and they never test the number of children.

- **Time** is O(n), because each node is pushed once and popped once.
- **Space** is O(h) for the stack, which lives on the heap, and the result list holds n values.

<!-- stage: applicability -->
### Choosing An Explicit Stack

#### Naming What The Stack Holds

The invariant of each loop is a sentence about the stack. In preorder the stack holds subtrees that have not started. In inorder it holds nodes whose left subtree is being walked. In postorder it holds the ancestors of the current position, each waiting for one more step. Write that sentence before the loop, and the push and pop statements follow from it.

#### Finding The False Friend

Pushing `left` before `right` looks natural, because the recursive method calls `left` first. Pushing in the same order gives the wrong result, because the stack reverses it. The tree with root 1, left child 2 and right child 3 then gives `1, 3, 2` and not `1, 2, 3`.

#### No-Go Conditions

If the tree is small and shallow, the recursive method is shorter and easier to check, so keep it. Suppose each node needs a value that its children computed, such as a height. The loop would then have to store partial results beside the nodes. Lessons 4 and 5 show that case with recursion first. The loop here does not make a tree safe to share. It reads the tree and never writes to it.

<!-- stage: exercises -->
### Exercises

#### [Build] Iterative Preorder (Author exercise)
<!-- id: it-preorder -->

**Prerequisites.** The preorder loop from this lesson.

**Problem.** Write a method that returns the values of a binary tree in preorder without recursion. Use one `Deque` of nodes. Handle a node when it is popped, and push its children so that the left subtree is processed before the right subtree.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers between -10^4 and 10^4.
- **Answer** is a list with one value per node, and an empty list for an empty tree.
- **Mutation** is not allowed.

**Example 1.** Input root 6 with left child 2 and right child 9, where node 2 has a right child 4, output `6, 2, 4, 9`.

**Example 2.** Input root 1 with right child 3 that has a right child 5, output `1, 3, 5`.

**Hint.** Which child do you push first so that it is popped last? What is on top of the stack right after the root is popped?

**Changed decision.** The call stack is replaced by a `Deque`, and the children enter the stack in reverse order.

#### [Vary] Iterative Inorder (Author exercise)
<!-- id: it-inorder -->

**Prerequisites.** The exercise above and the left spine from this lesson.

**Problem.** Write a method that returns the values of a binary tree in inorder without recursion. Push the left spine of the current node, pop one node, write it, and continue from its right child.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers between -10^4 and 10^4.
- **Answer** is a list with one value per node.
- **Mutation** is not allowed.

**Example 1.** Input root 6 with left child 2 and right child 9, where node 2 has a right child 4, output `2, 4, 6, 9`.

**Example 2.** Input root 8 with left child 5 that has a left child 3, output `3, 5, 8`.

**Hint.** What does the stack hold after the first inner loop ends? Which node is popped first?

**Changed decision.** A node is written when it is popped, not when it is pushed.

#### [Boundary] Deep Skewed Tree (Author exercise)
<!-- id: it-deep-sum -->

**Prerequisites.** The two exercises above.

**Problem.** Write a method that returns the sum of all node values of a binary tree as a `long`. The tree can be a chain of 200,000 nodes. The method must not recurse, because a recursive method overflows the call stack on that input. An empty tree has sum 0.

**Constraints.** The limits are:
- **Nodes** number between 0 and 2 * 10^5.
- **Values** are integers between -10^6 and 10^6.
- **Answer** fits in a `long`, and is 0 for an empty tree.
- **Mutation** is not allowed.

**Example 1.** Input `root = null`, output 0.

**Example 2.** Input a left-leaning chain of 200,000 nodes that each hold 1, output 200000.

**Hint.** Which order is easiest here, and why does the order not matter for a sum? How large does the stack grow on a chain?

**Changed decision.** The memory moves to the heap, and the order of the walk no longer matters.

#### [Recognize] Postorder Without Recursion (LeetCode 145)
<!-- id: it-postorder -->

**Prerequisites.** All three exercises above.

**Problem.** Write a method that returns the values of a binary tree in postorder without recursion. The walk must handle a chain of 100,000 nodes. A node is written after both of its subtrees. The earlier recursive version of this problem is not allowed here.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^5.
- **Values** are integers between -10^4 and 10^4.
- **Answer** is a list with one value per node.
- **Mutation** is not allowed.

**Example 1.** Input root 4 with left child 2, where node 2 has children 1 and 3, output `1, 3, 2, 4`.

**Example 2.** Input root 5 with right child 7 that has a left child 6, output `6, 7, 5`.

**Hint.** When a node is on top of the stack, how do you tell that its right subtree is already written? Which variable records that?

**Changed decision.** The loop needs visit state beside the stack, because a node is met twice before it is written.
