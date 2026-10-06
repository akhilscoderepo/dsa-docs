<!-- lesson-kind: standard -->
<!-- lesson-id: diameter-and-subtree-returns -->
## Find The Longest Path In A Tree

<!-- stage: context -->
### The Longest Cable Run Between Two Devices

A network tool reads a tree-shaped cable layout. Each device connects to its parent and to up to two child devices. The tool must report the longest cable run between any two devices, because that run sets the worst-case signal delay. The developer measures how deep each side of every device goes and takes the best sum. On a test layout with 50,000 devices in one long line, the tool takes far longer than on a balanced layout of the same size.

The answer is right, but the tool repeats the measuring work for every device. The question is how one pass over the tree can measure the sides and find the best run together.

<!-- stage: naive -->
### Measuring Both Sides At Every Device

The first version treats every node as the top of a candidate run. It measures the height of the left side and the height of the right side with a separate recursive method, adds the two, and repeats the step for every node.

```java
final class MeasureEveryNode {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int height(Node node) {
        if (node == null) return 0;                              // an empty side has no nodes
        return 1 + Math.max(height(node.left), height(node.right));
    }

    static int longestRun(Node node) {
        if (node == null) return 0;
        int here = height(node.left) + height(node.right);       // edges of the run that has this node on top
        int below = Math.max(longestRun(node.left), longestRun(node.right));   // runs that lie fully inside one side
        return Math.max(here, below);
    }
}
```

Take a root 1 with a right leaf 3 and a left child 2 that has the leaves 4 and 5. The method `longestRun` returns 3. The run 4, 2, 1, 3 has three edges. The method is correct for every tree.

<!-- stage: bottleneck -->
### Measuring The Same Nodes Again

```predict
The tree is a chain of n nodes, where each node has only a left child. How many times does the method call height on the deepest node, and what is the total cost?

Every node above the deepest one measures its left side with a call that reaches the deepest node. The deepest node is visited about n times. The total cost is 1 + 2 + ... + n, which is O(n^2).
```

The method measures each subtree once for every ancestor above it. The call `height(node.left)` at the top node visits the whole left side. The call `longestRun(node.left)` then repeats that measuring for the next node down. On a balanced tree the repeated work is small, and on a chain it is O(n^2).

A node does not need to measure its sides again. Its children can report their heights when they finish, and the node can combine the two reports. The remaining difficulty is that the node needs two different things from the same recursion. The parent above needs one number, and the answer needs another.

<!-- stage: insight -->
### Returning One Number And Recording Another

Every path in a tree has one node closest to the root, which is the **top node** of the path. From the top node the path goes down into the left subtree, down into the right subtree, or both. The longest path overall is therefore the best result over all nodes of one formula about the top node.

<!-- names: single branch, complete path, summary -->

#### A Single Branch Can Be Extended

A **single branch** at a node is a path that starts at the node and goes downward through one child at each step. A branch never forks. The height of a subtree, counted in nodes, is the length of its longest single branch. A parent can attach to a single branch of a child and still form a path, because the result is one unbroken line.

#### A Complete Path Cannot Be Extended

A **complete path** at a node uses a branch down the left side and a branch down the right side, joined at the node. Its length in edges is the left height plus the right height. A parent cannot continue a complete path, because a path through the parent would then leave the node in three directions, which is a fork and not a path. A call therefore must not return the complete path to its parent.

#### One Call Gives Two Facts

Each call returns a **summary**, a small value with two numbers. The first is the height of the subtree, which the parent uses as a single branch and computes as one plus the larger child height. The second is the best complete path seen anywhere in the subtree. The call takes the largest of three numbers: the best of the left summary, the best of the right summary, and the complete path at this node. The root's summary holds the answer.

<!-- stage: variables -->
### The Numbers Behind Each Summary

- **height** counts the nodes of the longest single branch that starts at the node, and it is 0 for `null`.
- **best** is the largest number of edges on any path inside the subtree, and it is 0 for `null` and for a single node.
- **through** is the left height plus the right height, which is the number of edges of the complete path that has the node on top.

The call returns `height` and `best`. The value `through` is a local number that the call uses once and does not return.

<!-- stage: trace -->
### Reading The Summaries From The Leaves Up

#### A Path Through The Root

The tree has root 1 and right child 3. The root's left child is 2, which has children 4 and 5. A step shows the moment when a call finishes and returns its summary. The variable `through` is the left height plus the right height at that node.

```trace
{"cells":["1","2","3","4","5"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"height":1,"through":0,"best":0},"note":"The call on the node 4 finishes. The children report heights 0 and 0, so through is 0 and the height is 1. A leaf has no edges below it, so best stays 0."},{"at":{"node":4},"vars":{"height":1,"through":0,"best":0},"note":"The call on the node 5 finishes. The children report heights 0 and 0, so through is 0 and the height is 1. A leaf has no edges below it, so best stays 0."},{"at":{"node":1},"vars":{"height":2,"through":2,"best":2},"note":"The call on the node 2 finishes. The children report heights 1 and 1, so through is 2 and the height is 2. The complete path here is better than both sides, so best is 2."},{"at":{"node":2},"vars":{"height":1,"through":0,"best":0},"note":"The call on the node 3 finishes. The children report heights 0 and 0, so through is 0 and the height is 1. A leaf has no edges below it, so best stays 0."},{"at":{"node":0},"vars":{"height":3,"through":3,"best":3},"note":"The call on the node 1 finishes. The children report heights 2 and 1, so through is 3 and the height is 3. The complete path here is better than both sides, so best is 3."}]}
```

The best path has three edges and passes through the root. The summary of node 2 reports a height of 2, so the root can attach to it and form the path 4, 2, 1, 3.

#### A Path That Avoids The Root

The second tree has a root with only a left child 2. The node 2 has children 3 and 4. The node 3 has a left child 5, and the node 4 has a right child 6.

```trace
{"cells":["1","2","null","3","4","5","null","null","6"],"pointers":["node"],"steps":[{"at":{"node":5},"vars":{"height":1,"through":0,"best":0},"note":"The call on the node 5 finishes. The children report heights 0 and 0, so through is 0 and the height is 1. A leaf has no edges below it, so best stays 0."},{"at":{"node":3},"vars":{"height":2,"through":1,"best":1},"note":"The call on the node 3 finishes. The children report heights 1 and 0, so through is 1 and the height is 2. The complete path here is better than both sides, so best is 1."},{"at":{"node":8},"vars":{"height":1,"through":0,"best":0},"note":"The call on the node 6 finishes. The children report heights 0 and 0, so through is 0 and the height is 1. A leaf has no edges below it, so best stays 0."},{"at":{"node":4},"vars":{"height":2,"through":1,"best":1},"note":"The call on the node 4 finishes. The children report heights 0 and 1, so through is 1 and the height is 2. The complete path here is better than both sides, so best is 1."},{"at":{"node":1},"vars":{"height":3,"through":4,"best":4},"note":"The call on the node 2 finishes. The children report heights 2 and 2, so through is 4 and the height is 3. The complete path here is better than both sides, so best is 4."},{"at":{"node":0},"vars":{"height":4,"through":3,"best":4},"note":"The call on the node 1 finishes. The children report heights 3 and 0, so through is 3 and the height is 4. A path below is at least as long, so best stays 4."}]}
```

The best path 5, 3, 2, 4, 6 has four edges and lies fully inside the subtree of node 2. The root sees `best` equal to 4 in the left summary, although its own complete path has only three edges. The maximum of the three numbers keeps the better value.

<!-- stage: code -->
### The Summary Method In Code

```java
final class Diameter {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    record Summary(int height, int best) {}

    static Summary summarize(Node node) {
        if (node == null) return new Summary(0, 0);              // an empty subtree has no nodes and no edges
        Summary l = summarize(node.left);                        // the left subtree reports first
        Summary r = summarize(node.right);                       // then the right subtree reports
        int through = l.height() + r.height();                   // edges of the complete path with this node on top
        int best = Math.max(through, Math.max(l.best(), r.best()));   // the best path may lie anywhere below
        return new Summary(1 + Math.max(l.height(), r.height()), best);   // the parent may extend one branch only
    }

    static int diameter(Node root) {
        return summarize(root).best();                           // edges on the longest path in the tree
    }
}
```

The method keeps no shared variable, because both numbers travel in the return value. The empty tree returns a diameter of 0, and a single node also returns 0, because a path of one node has no edges.

- **Time** is O(n), because each node receives one call and does constant work after its children return.
- **Space** is O(h) for the recursion depth, and each call holds one `Summary` value.

<!-- stage: applicability -->
### Separating The Branch From The Path

#### Writing Down What Each Return Means

The invariant is that the return value describes a single branch that starts at the node, and a separate number describes the best complete path inside the subtree. Write both sentences before coding. If a return value mixes the two meanings, a parent will extend something that cannot be extended.

#### Finding The False Friend

Returning `through` to the parent looks like a shortcut, but it is the trap that this lesson warns about. Suppose node 2 on the first trace tree returned its complete path 4, 2, 5, which has 3 nodes. The root would see a left side of 3 nodes and report 3 + 1 = 4 edges. No such path exists, because the longest path in this tree has 3 edges.

#### No-Go Conditions

This pattern needs a tree, because one top node per path is what makes the formula work. In a graph with cycles a path has no single top node. The pattern also needs the question to ask for a path with no repeated node. A question about walks that may revisit nodes needs a different tool.

<!-- stage: exercises -->
### Exercises

#### [Build] Return Subtree Height (Author exercise)
<!-- id: dr-heights -->

**Prerequisites.** The height and the summary from this lesson.

**Problem.** Given a binary tree, return a list with one entry for every node. The entry is the height of the subtree of that node, counted in nodes. The entries follow the order in which the calls finish, so the left subtree comes first, then the right subtree, then the node. An empty tree gives an empty list.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Answer** is a list of `n` integers between 1 and the height of the tree.
- **Mutation** is not allowed.

**Example 1.** Input root 4 with left child 2 and right child 6, where node 6 has a left child 5, output `1, 1, 2, 3`.

**Example 2.** Input a single node, output `1`.

**Hint.** When does a call know the height of its node? Which two numbers must it have first?

**Changed decision.** The call computes both child heights before it forms its own result, and it records the result.

#### [Vary] Diameter Of Binary Tree (LeetCode 543)
<!-- id: dr-diameter -->

**Prerequisites.** The exercise above and the summary from this lesson.

**Problem.** Given a binary tree, return its diameter. The diameter is the number of edges on the longest path between any two nodes. The path may or may not pass through the root. A tree with one node or no node has diameter 0.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Answer** is an integer between 0 and `n - 1`.
- **Mutation** is not allowed.

**Example 1.** Input root 6 with right child 8 and left child 2, where node 2 has a left child 1 that has a left child 0, output 4.

**Example 2.** Input root 1 with only a left child 2, output 4. Node 2 has a left child 3 with a left child 5, and a right child 4 with a right child 6.

**Hint.** What does a call return to its parent, and what does it only compare against the best so far?

**Changed decision.** The complete path at a node is built from two heights and is compared and not returned.

#### [Boundary] Nodes Versus Edges (Author exercise)
<!-- id: dr-node-count -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary tree, return how many nodes lie on the longest path between any two nodes. A path of one node counts as 1. An empty tree has no path, so the answer is 0. State the unit of every number that the method returns.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Answer** is 0 for an empty tree and at least 1 otherwise.
- **Mutation** is not allowed.

**Example 1.** Input `root = null`, output 0.

**Example 2.** Input root 1 with only a left child 2, output 2.

**Hint.** How does a count in nodes differ from a count in edges on the same path? Which input must not add one?

**Changed decision.** The unit changes from edges to nodes, so the empty tree must stay at 0 and not become 1.

#### [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: dr-max-path -->

**Prerequisites.** All three exercises above.

**Problem.** Given a binary tree whose values may be negative, return the largest sum of values on any path. A path is a sequence of connected nodes with no repeats, has at least one node, and may start and end anywhere. The sum counts every node on the path once.

**Constraints.** The limits are:
- **Nodes** number between 1 and 3 * 10^4.
- **Values** are integers between -1000 and 1000.
- **Answer** is an integer, and it is negative when every value is negative.
- **Mutation** is not allowed.

**Example 1.** Input root 2 with left child -1 and right child 3, output 5.

**Example 2.** Input root -3 with left child -5 and right child -2, output -2.

**Hint.** What does a call return when the best branch below it has a negative sum? What does the complete path at a node add up?

**Changed decision.** A branch with a negative gain is dropped, and the complete path may use both sides.
