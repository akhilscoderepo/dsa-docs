<!-- lesson-kind: standard -->
<!-- lesson-id: recursive-traversal-orders -->
## Visit Nodes In Three Orders

<!-- stage: context -->
### Deleting A Folder Before Its Files

A cleanup tool removes a directory tree from disk. The first version deletes each directory and then deletes the entries inside it. The operating system refuses with "directory not empty", because a directory can only be removed after everything below it is gone. A copy tool needs the opposite order. It must create a directory before it creates the files inside.

Both tools walk the same tree and touch every node once. The only difference is the moment at which a node is handled, compared with the moment its children are handled. The question for this lesson is how one walk produces either order.

<!-- stage: naive -->
### Reusing One Walk And Reversing The Output

The first idea is to write one walk that records each node when the call begins, and then to reverse the list when the opposite order is needed.

```java
import java.util.*;

final class EntryOrder {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void collect(Node node, List<Integer> out) {
        if (node == null) return;                  // nothing to record for a missing child
        out.add(node.val);                         // record the node as soon as the call begins
        collect(node.left, out);                   // then the left side
        collect(node.right, out);                  // then the right side
    }

    static List<Integer> reversedEntryOrder(Node root) {
        List<Integer> out = new ArrayList<>();
        collect(root, out);
        Collections.reverse(out);                  // reverse the list so that children come before parents
        return out;
    }
}
```

For the tree with root 1, left child 2 and right child 3, `collect` records 1, 2, 3. The reversed list is 3, 2, 1. The method visits each node once, so it runs in linear time.

<!-- stage: bottleneck -->
### Checking Whether Reversing Is Enough

```predict
The deletion tool needs every node after both of its children, and the left child before the right child. For root 1 with left child 2 and right child 3, the correct sequence is 2, 3, 1. Does reversedEntryOrder return it, and could the same trick produce an order that places the root between its two children?

No. It returns 3, 2, 1, because reversing also swaps the left and right sides. No reversal of the list can place the root between its children, since the list only records the moment each call begins.
```

The reversed list has the right sizes and the wrong sequence. It reads the right child first. Swapping the two child calls before the reversal fixes one order. That trick does not extend to a node placed between its children. That order needs the action to sit between the two calls, and the walk above has no such place.

The cost of the method is O(n) time and O(n) extra memory for the list, so the cost is acceptable. The failure is in where the action sits. A walk that can place the action at three different positions handles all three tools without any trick.

<!-- stage: insight -->
### Moving The Action Between The Calls

Every walk below has the same skeleton. The method returns at `null`. Otherwise it calls itself on `left` and then on `right`. The **action** is the step that handles the node, such as appending its value to a list. The action has three possible positions in the skeleton, and each position gives a named order.

<!-- names: preorder, inorder, postorder -->

#### Three Positions For One Action

In **preorder** the action comes first, before both child calls. Every node is handled before any node of its subtree. In **inorder** the action sits between the two child calls. The whole left subtree is handled, then the node, then the whole right subtree. In **postorder** the action comes last, after both child calls. Every node is handled after all nodes below it.

#### What Each Order Guarantees

Preorder guarantees that a parent comes before each of its descendants, which the copy tool needs. Postorder guarantees that a node comes after all of its descendants, which the deletion tool needs. Inorder guarantees that everything in the left subtree comes before the node and everything in the right subtree comes after it. All three orders keep the left subtree ahead of the right subtree, so they differ only in where the node itself falls.

#### Why Each Node Appears Once

The skeleton makes one call per node and one call per `null` side. Each non-null call runs the action exactly once, in whichever position was chosen. The list of values therefore holds every node once, and the order depends on that position alone.

<!-- stage: variables -->
### The Pieces Of The Walk

- **node** is the parameter of the call, and the call owns the subtree of `node`.
- **out** is the list that receives one value per action, and the caller creates it fresh for each walk.
- **action position** is the place of the `out.add` statement, which is before, between or after the two child calls.
- **base case** is the `null` check at the top, and it returns without touching `out`.

The three methods differ in one line, so the order of the values in `out` follows only from the position of the `out.add` statement.

<!-- stage: trace -->
### Watching The Action Fire

#### Inorder On A Five-Node Tree

The tree has root 1, left child 2 and right child 3, and the node 2 has children 4 and 5. A pointer on a node means that a call is active there, and calls on `null` return at once and are not shown. The variable `out` lists the values handled so far.

```trace
{"cells":["1","2","3","4","5"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"out":"empty"},"note":"The call on the node 1 starts and calls its left child first."},{"at":{"node":1},"vars":{"out":"empty"},"note":"The call on the node 2 starts and calls its left child first."},{"at":{"node":3},"vars":{"out":"empty"},"note":"The call on the node 4 starts and calls its left child first."},{"at":{"node":3},"vars":{"out":"4"},"note":"The left subtree of the node 4 is done, so the call writes the value 4 and then calls the right child."},{"at":{"node":1},"vars":{"out":"4 2"},"note":"The left subtree of the node 2 is done, so the call writes the value 2 and then calls the right child."},{"at":{"node":4},"vars":{"out":"4 2"},"note":"The call on the node 5 starts and calls its left child first."},{"at":{"node":4},"vars":{"out":"4 2 5"},"note":"The left subtree of the node 5 is done, so the call writes the value 5 and then calls the right child."},{"at":{"node":0},"vars":{"out":"4 2 5 1"},"note":"The left subtree of the node 1 is done, so the call writes the value 1 and then calls the right child."},{"at":{"node":2},"vars":{"out":"4 2 5 1"},"note":"The call on the node 3 starts and calls its left child first."},{"at":{"node":2},"vars":{"out":"4 2 5 1 3"},"note":"The left subtree of the node 3 is done, so the call writes the value 3 and then calls the right child."}]}
```

The values 4, 2, 5, 1, 3 read the left subtree of the root, then the root, then the right subtree. The same pattern holds inside the subtree of node 2, which is handled as 4, then 2, then 5.

#### Preorder On A Tree With One Side

The second tree has root 3, no left child, and a right child 5 that has a left child 4. The cell `null` marks the missing left child of the root.

```trace
{"cells":["3","null","5","4"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"out":"3"},"note":"The call on the node 3 starts and writes the value at once, before it calls either child."},{"at":{"node":2},"vars":{"out":"3 5"},"note":"The call on the node 5 starts and writes the value at once, before it calls either child."},{"at":{"node":3},"vars":{"out":"3 5 4"},"note":"The call on the node 4 starts and writes the value at once, before it calls either child."}]}
```

Preorder handles each node on entry, so the root comes first and every node follows its parent. The same tree gives 3, 4, 5 in inorder and 4, 5, 3 in postorder, so the order differs while the set of values stays the same.

<!-- stage: code -->
### The Three Walks In Code

```java
import java.util.*;

final class ThreeOrders {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static void preorder(Node node, List<Integer> out) {
        if (node == null) return;                  // an empty subtree adds nothing
        out.add(node.val);                         // action before both child calls
        preorder(node.left, out);
        preorder(node.right, out);
    }

    static void inorder(Node node, List<Integer> out) {
        if (node == null) return;
        inorder(node.left, out);
        out.add(node.val);                         // action between the child calls
        inorder(node.right, out);
    }

    static void postorder(Node node, List<Integer> out) {
        if (node == null) return;
        postorder(node.left, out);
        postorder(node.right, out);
        out.add(node.val);                         // action after both child calls
    }
}
```

The caller creates a new list for each walk and passes it down. A list stored in a static field would keep the values of the previous walk and mix them with the next.

- **Time** is O(n), because each node receives one call and each `null` side receives one call.
- **Space** is O(h) on the chain of open calls, where h is the height of the tree, and the list `out` holds n values as the result.

<!-- stage: applicability -->
### Choosing The Position

#### Matching The Order To The Dependency

Ask which fact the action needs. If the action needs the parent to be handled first, such as creating a directory, place it before the calls. If it needs the results of both children, such as deleting or summing, place it after the calls. The invariant of every walk is that the call on `node` handles exactly the nodes of its own subtree, in the chosen order, and handles nothing else.

#### Finding The False Friend

The three orders look like three names for the same walk, and that is the false friend. Inorder of a general binary tree is not sorted, because the tree places values with no ordering rule. Inorder gives sorted values only when the tree follows a search rule, which Chapter 16 states. Reversing a preorder list does not give postorder either, as the opening method showed.

#### No-Go Conditions

These walks give depth-first orders only. If the answer needs the nodes grouped by distance from the root, a level-by-level queue is the right tool, and Chapter 16 teaches it. If the tree is deeper than the call stack allows, the explicit stack of the next lesson replaces the recursion.

<!-- stage: exercises -->
### Exercises

#### [Build] Binary Tree Preorder Traversal (LeetCode 144)
<!-- id: ro-preorder -->

**Prerequisites.** The skeleton and the action positions from this lesson.

**Problem.** Given the root of a binary tree, return the values of its nodes in preorder. Preorder handles a node, then every node of its left subtree, then every node of its right subtree. The tree may be empty.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** are integers between -100 and 100.
- **Answer** is a list with one value per node, and an empty list for an empty tree.
- **Mutation** is not allowed, and the tree stays unchanged.

**Example 1.** Input root 4 with left child 2 and right child 6, where node 2 has children 1 and 3, output `4, 2, 1, 3, 6`.

**Example 2.** Input root 8 with no left child and a right child 9 that has a left child 7, output `8, 9, 7`.

**Hint.** Where does the `add` statement sit relative to the two child calls? Does the left call come before the right call?

**Changed decision.** The action runs before both child calls.

#### [Vary] Binary Tree Inorder Traversal (LeetCode 94)
<!-- id: ro-inorder -->

**Prerequisites.** The exercise above.

**Problem.** Given the root of a binary tree, return the values of its nodes in inorder. Inorder handles every node of the left subtree, then the node, then every node of the right subtree.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** are integers between -100 and 100.
- **Answer** is a list with one value per node.
- **Mutation** is not allowed.

**Example 1.** Input root 5 with right child 7 and left child 3, where node 3 has a right child 4, output `3, 4, 5, 7`.

**Example 2.** Input root 2 with left child 1, where node 1 has left child 0, output `0, 1, 2`.

**Hint.** Which one line moves compared with the preorder method? What does the first value of the output tell you about the left spine?

**Changed decision.** The action moves between the two child calls.

#### [Boundary] Empty And One-Sided Trees (Author exercise)
<!-- id: ro-marked -->

**Prerequisites.** The two exercises above.

**Problem.** Given the root of a binary tree, return the inorder sequence of strings. Write each node as its value. Write each empty subtree that the walk reaches as `x` at its position.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** are integers between -100 and 100.
- **Answer** has `n + 1` entries for `n` nodes, and `x` alone for an empty tree.
- **Mutation** is not allowed.

**Example 1.** Input `root = null`, output `x`.

**Example 2.** Input root 1 with no left child and a right child 2, output `x, 1, x, 2, x`.

**Hint.** At which point of the call does the `x` get written? Which sides of a leaf produce it?

**Changed decision.** The base case at `null` now writes an entry, so a missing side keeps its place in the order.

#### [Recognize] Binary Tree Postorder Traversal (LeetCode 145)
<!-- id: ro-postorder -->

**Prerequisites.** All three exercises above.

**Problem.** Given the root of a binary tree, return the values of its nodes in postorder. Postorder handles every node of the left subtree, then every node of the right subtree, then the node. A node comes after all of its descendants.

**Constraints.** The limits are:
- **Nodes** number between 0 and 100.
- **Values** are integers between -100 and 100.
- **Answer** is a list with one value per node.
- **Mutation** is not allowed.

**Example 1.** Input root 5 with left child 3 and right child 8, output `1, 4, 3, 9, 8, 5`. Node 3 has children 1 and 4, and node 8 has a right child 9.

**Example 2.** Input a single node 7, output `7`.

**Hint.** Both child calls return before the node is written. Where does the root of the whole tree appear in the output?

**Changed decision.** The action moves after both child calls.
