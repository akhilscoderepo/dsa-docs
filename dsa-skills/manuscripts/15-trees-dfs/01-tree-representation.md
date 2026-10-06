<!-- lesson-kind: standard -->
<!-- lesson-id: tree-representation -->
## Store A Tree In Node Objects

<!-- stage: context -->
### Counting The Elements Under A Parent

A page editor stores every element of a web page in one array. Each entry holds the element and the array index of its parent element. The user selects a `div` and the editor must report how many elements the `div` contains. The code has no list of the children of the `div`. It has to ask every element in the array whether the `div` is somewhere above it.

The answer is right, but the editor slows down on large pages, and every question about one part of the page rescans the whole page. Data with one top element and nested elements needs a layout where each element leads directly to its own children.

<!-- stage: naive -->
### Storing Only The Parent Of Each Element

The first layout keeps one array. Position `i` holds the position of the parent of element `i`, and the top element holds `-1`. To count the elements under element `x`, the method checks every element and walks upward from it until it reaches `x` or the top.

```java
final class ParentArrayCount {
    // parent[i] is the index of the parent of element i, or -1 for the top element.
    static int countUnder(int[] parent, int x) {
        int count = 1;                                       // the element x itself
        for (int i = 0; i < parent.length; i++) {            // check every element once
            if (i == x) continue;                            // x is already counted
            int up = parent[i];
            while (up != -1 && up != x) up = parent[up];     // walk upward until x or the top
            if (up == x) count++;                            // x was found above element i
        }
        return count;
    }
}
```

For `parent = {-1, 0, 0, 1}` and `x = 1`, the method returns 2, because element 3 sits under element 1. The method is correct on any layout where every walk ends at `-1`.

<!-- stage: bottleneck -->
### Walking Upward For Every Element

```predict
A page has n elements nested in one chain, so element i is the parent of element i + 1. How many parent steps does countUnder take when x is the top element, and what does the layout fail to show about the children of one element?

Element i needs i parent steps to reach the top, so the total is 0 + 1 + ... + (n - 1), which is O(n^2). The layout also fails to list the children of an element, so each question rescans every element.
```

The cost has two causes. The method repeats an upward walk for each element, and the walks overlap, because the elements below one parent share every step above it. The layout also stores the link in the wrong direction. A question about the part below `x` needs the children of `x`, and the array stores only the parent of each element.

If the layout stored the children of each element, a count could start at `x` and visit only the elements below `x`. The cost would then depend on the size of that part and not on the size of the page.

<!-- stage: insight -->
### Letting Each Element Point To Its Children

A tree stores a link from each element to its children. Each element becomes a **node object** that holds a value and references to its children. The top node is the **root**. A node without children is a **leaf**.

<!-- names: node object, subtree, empty subtree, child list -->

#### One Node Owns One Subtree

The **subtree** of a node is that node together with every node below it. A method that receives a node works on exactly the subtree of that node. The subtree of the root is the whole tree. The subtree of a leaf is the leaf alone. The subtree of a child is a smaller part of the subtree of its parent. A method can pass each child to a call of itself and combine the results. The count of a subtree is one for the node plus the counts of the child subtrees.

#### Two Shapes Of Child Storage

A binary tree node holds two fields, `left` and `right`. A reference that is `null` marks an **empty subtree**, which is a subtree with no nodes. A method treats `null` as a valid argument and returns the answer for no nodes, so a leaf needs no special case. An N-ary node holds a **child list** instead, which is a `List` of nodes with any length. A leaf holds an empty list, and a method loops over the list and does not assume a fixed number of positions.

#### What The Tree Contract Promises

A tree has exactly one root. Every other node has exactly one parent, and no node is its own ancestor. These rules guarantee that every node is reached by exactly one path from the root. A traversal therefore needs no record of visited nodes.

<!-- stage: variables -->
### The Fields And The Call

- **val** holds the value stored in one node.
- **left** and **right** hold the child nodes of a binary node, and each is `null` when that side is an empty subtree.
- **children** holds the child list of an N-ary node, and the list is empty for a leaf.
- **root** is the reference the caller keeps, and it is `null` for a tree with no nodes.
- **node** is the parameter of a recursive call, and the call owns the subtree of `node`.

The fields never change during a count. A count reads references and writes nothing.

<!-- stage: trace -->
### Counting The Nodes Of A Subtree

#### Counting A Full Three-Node Tree

The trace counts the nodes of the tree with root 2, left child 1 and right child 3. The cells list the nodes level by level, and a pointer that sits outside the cells means `null`. The variable `result` holds the value that the current call returns.

```trace
{"cells":["2","1","3"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"result":"?"},"note":"The call receives the node 2 and counts its left side first."},{"at":{"node":1},"vars":{"result":"?"},"note":"The call receives the node 1 and counts its left side first."},{"at":{"node":3},"vars":{"result":0},"note":"The call receives null, which is an empty subtree, and returns 0."},{"at":{"node":3},"vars":{"result":0},"note":"The call receives null, which is an empty subtree, and returns 0."},{"at":{"node":1},"vars":{"result":1},"note":"Both sides of the node 1 are counted as 0 and 0, so the call returns 1 + 0 + 0 = 1."},{"at":{"node":2},"vars":{"result":"?"},"note":"The call receives the node 3 and counts its left side first."},{"at":{"node":3},"vars":{"result":0},"note":"The call receives null, which is an empty subtree, and returns 0."},{"at":{"node":3},"vars":{"result":0},"note":"The call receives null, which is an empty subtree, and returns 0."},{"at":{"node":2},"vars":{"result":1},"note":"Both sides of the node 3 are counted as 0 and 0, so the call returns 1 + 0 + 0 = 1."},{"at":{"node":0},"vars":{"result":3},"note":"Both sides of the node 2 are counted as 1 and 1, so the call returns 1 + 1 + 1 = 3."}]}
```

The two leaves each make two calls on `null`, and each of those calls returns 0 at once. A leaf therefore returns 1, and the root returns 1 + 1 + 1.

#### Counting A Tree With A Missing Left Child

The second tree has root 7, no left child, and a chain of nodes to the right. The cells `null` mark missing left children, and a pointer on such a cell means the same as a pointer outside the cells.

```trace
{"cells":["7","null","8","null","9"],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"result":"?"},"note":"The call receives the node 7 and counts its left side first."},{"at":{"node":1},"vars":{"result":0},"note":"The call receives null, so it returns 0 without reading any field."},{"at":{"node":2},"vars":{"result":"?"},"note":"The call receives the node 8 and counts its left side first."},{"at":{"node":3},"vars":{"result":0},"note":"The call receives null, so it returns 0 without reading any field."},{"at":{"node":4},"vars":{"result":"?"},"note":"The call receives the node 9 and counts its left side first."},{"at":{"node":5},"vars":{"result":0},"note":"The call receives null, so it returns 0 without reading any field."},{"at":{"node":5},"vars":{"result":0},"note":"The call receives null, so it returns 0 without reading any field."},{"at":{"node":4},"vars":{"result":1},"note":"The sides of the node 9 return 0 and 0, so the call returns 1."},{"at":{"node":2},"vars":{"result":2},"note":"The sides of the node 8 return 0 and 1, so the call returns 2."},{"at":{"node":0},"vars":{"result":3},"note":"The sides of the node 7 return 0 and 2, so the call returns 3."}]}
```

The call on the missing left child returns 0, so the empty side adds nothing to the root. The same rule gives the right answer when the missing side is deeper in the tree.

<!-- stage: code -->
### The Node Classes And A Count

```java
import java.util.*;

final class TreeNodes {
    static final class Node {
        int val;
        Node left, right;                                   // null marks an empty subtree
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final class NNode {
        int val;
        List<NNode> children = new ArrayList<>();           // empty list for a leaf
        NNode(int val) { this.val = val; }
    }

    static int count(Node node) {
        if (node == null) return 0;                         // an empty subtree has no nodes
        return 1 + count(node.left) + count(node.right);    // this node plus both child subtrees
    }

    static int countN(NNode node) {
        int total = 1;                                      // this node
        for (NNode child : node.children) total += countN(child);   // one call per child, however many
        return total;
    }
}
```

The binary method has one base case, and it covers the empty tree, the leaf and a node with one child. The N-ary method has no base case, because the loop over an empty list ends the recursion at a leaf. The caller must not pass `null` to `countN`.

- **Time** is O(n) for n nodes, because each node is reached by one call and each `null` side by one call.
- **Space** is O(h) for the call stack, where h is the height of the tree, because one frame per level is open at the deepest point.

<!-- stage: applicability -->
### Checking What The Input Promises

#### Naming The Subtree Before Writing A Call

Every recursive method on a tree keeps one invariant: the call on `node` answers a question about the subtree of `node` and reads nothing outside it. Write that sentence for the method before writing the code. If the sentence needs a value from outside the subtree, such as the depth of the parent, the value must become a parameter.

#### Finding The False Friend

A graph with a cycle looks like a tree at first glance, because it has nodes and references. It is a false friend of the tree contract. If a node can be its own ancestor, the count above never reaches a base case and ends with `StackOverflowError`. If two parents share one child, the child is counted twice. A graph needs a record of visited nodes, which Chapter 21 teaches.

#### No-Go Conditions

Do not use the plain recursion above when the input is a graph or when the tree can be deeper than the call stack allows. A very deep tree needs the explicit stack from the lesson "Walk A Tree With Your Own Stack". The `NNode` method also fails on a `null` child inside the list, so check what the input promises before choosing the guard.

<!-- stage: exercises -->
### Exercises

#### [Build] Construct A Three-Node Tree (Author exercise)
<!-- id: tr-three-node -->

**Prerequisites.** The binary node class from this lesson.

**Problem.** Write a method `build(a, b, c)` that returns the root of a binary tree with exactly three nodes. The root holds `a`, its left child holds `b` and its right child holds `c`. Both children are leaves, so each of their `left` and `right` fields is `null`.

**Constraints.** The limits are:
- **Values** are integers in the range `-1000` to `1000`.
- **Answer** is a reference to the new root.
- **Shape** has one root, two leaves and four `null` fields in total.

**Example 1.** Input `a = 1, b = 2, c = 3`, output a root holding 1 with left child 2 and right child 3.

**Example 2.** Input `a = 5, b = 5, c = 5`, output three distinct nodes that each hold 5. The root is not the same object as either child.

**Hint.** How many `new Node` calls does the tree need, and which `null` fields do the two leaves keep?

**Changed decision.** The children are created first and passed to the constructor of the root.

#### [Vary] Count N-Ary Children (Author exercise)
<!-- id: tr-nary-children -->

**Prerequisites.** The `NNode` class and the exercise above.

**Problem.** Given the root of an N-ary tree, return the largest number of children held by any single node. A leaf has 0 children. Visit every node, and compare the length of each child list with the best length found so far.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4.
- **Children** per node number between 0 and 50.
- **Child list** is never `null` and never holds `null`.
- **Answer** is an integer between 0 and 50.

**Example 1.** Input root 1 with children 2, 3 and 4, where node 3 has one child 5, output 3.

**Example 2.** Input a chain of five nodes where each node has exactly one child, output 1.

**Hint.** Which node has the largest child list: the root, or a node deeper down? What does each recursive call return?

**Changed decision.** The loop over the child list replaces the fixed pair `left` and `right`.

#### [Boundary] Empty And Single-Node Trees (Author exercise)
<!-- id: tr-leaf-count -->

**Prerequisites.** The binary node class and the count method of this lesson.

**Problem.** Given the root of a binary tree, return the number of leaves. A leaf is a node whose `left` and `right` are both `null`. An empty tree has no leaves. A node with exactly one child is not a leaf.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and `root` is `null` for 0 nodes.
- **Values** are integers that the answer does not use.
- **Answer** is an integer between 0 and the number of nodes.

**Example 1.** Input `root = null`, output 0.

**Example 2.** Input root 1 with no left child and a right child 2, output 1, because only node 2 is a leaf.

**Hint.** What does the call return on `null`? What must hold for a node to count as 1 and not recurse further?

**Changed decision.** The base case at `null` returns 0, and a second base case at a leaf returns 1.

#### [Recognize] Maximum Depth Of N-ary Tree (LeetCode 559)
<!-- id: tr-nary-depth -->

**Prerequisites.** All exercises above.

**Problem.** Given the root of an N-ary tree, return its maximum depth. The depth is the number of nodes on the longest path from the root down to a leaf. An empty tree has depth 0.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Children** per node number between 0 and 50.
- **Root** is `null` for the empty tree.
- **Answer** is an integer between 0 and 10^4.

**Example 1.** Input root 1 with children 2, 3 and 4, where node 3 has child 5, output 3.

**Example 2.** Input a single node with no children, output 1.

**Hint.** The depth of a node is one more than the depth of its deepest child. What is the depth of a node with an empty child list?

**Changed decision.** A maximum over a child list replaces the maximum of two values.
