<!-- lesson-kind: combination -->
<!-- lesson-id: return-results-from-subtrees -->
## Return Results From Subtrees

<!-- stage: context -->
### One Report That Needs Three Walks

An organization chart is stored as a binary tree, where each manager has up to two direct reports. A reporting tool must print three facts about the whole chart. The first is the longest chain of managers. The second is the largest difference between the depths of the two sides of any manager. The third is the longest chain between any two people. The first version runs one walk per fact. Each walk asks for the height of both sides at every manager, so the heights are measured again and again.

On a chart of 100,000 people arranged as a long chain of managers, the report takes far longer than the size of the chart suggests. The facts overlap, because each one is built from the heights of the same subtrees. The question is how one walk can hand each manager the numbers that all three facts need.

<!-- stage: contributions -->
### What Each Earlier Lesson Adds

Four earlier lessons of this chapter supply the parts. The first lesson supplies the ownership rule. A call on a node owns exactly that node's subtree, and `null` stands for an empty subtree with a defined answer. The depth lesson supplies the split between facts that travel down as arguments and facts that travel up as return values. It shows that a height needs no search once both children have reported.

The diameter lesson supplies the rule that a parent can continue only one branch of a child. The best path through a node uses two branches, so a call compares it and does not pass it on. The balance lesson supplies the reserved failure value that lets one return value carry a height or a verdict. Together they give a single walk in which each call returns a small bundle of numbers, and each parent combines two bundles into its own.

<!-- stage: naive -->
### Measuring Both Heights At Every Manager

The first version visits every manager. At each one it measures the height of the left side and the right side with a helper that walks the whole side, and then it updates two running numbers.

```java
final class RepeatedHeights {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final class Report { int longestChain; int worstGap; }

    static int height(Node node) {
        if (node == null) return 0;                              // an empty side has no managers
        return 1 + Math.max(height(node.left), height(node.right));
    }

    static void visit(Node node, Report rep) {
        if (node == null) return;
        int lh = height(node.left);                              // measure the left side from scratch
        int rh = height(node.right);                             // measure the right side from scratch
        rep.longestChain = Math.max(rep.longestChain, lh + rh);  // the best chain with this manager on top
        rep.worstGap = Math.max(rep.worstGap, Math.abs(lh - rh)); // the largest lopsided pair so far
        visit(node.left, rep);
        visit(node.right, rep);
    }
}
```

Take the chart with root 6 and right child 8. The left child 4 has a left child 2, which has a left child 1. The method sets `longestChain` to 4 and `worstGap` to 2. The answers are correct for every chart.

<!-- stage: bottleneck -->
### Adding Up The Repeated Measuring

```predict
The chart is a chain of n managers where each manager has only a left report. How many manager visits do all the height calls make together, and what does that cost in time?

The manager at depth i measures a left side of n - 1 - i managers, so the calls visit (n - 1) + (n - 2) + ... + 0 managers. That total is n(n - 1) / 2, which is O(n^2).
```

The method repeats the work of the lessons before it. Every ancestor measures the same lower managers again, as the heights of a chain are remeasured at every level. The method also keeps its results in a `Report` object that the caller must create and that the recursion mutates. A call returns nothing, so no call can pass its subtree's numbers to its parent.

The heights are needed by three different facts. A call that finishes can report a height once, and the parent can reuse it. The remaining difficulty is that the parent needs one number to extend a chain, while the answer needs other numbers that do not extend. The bundle that each call returns must keep these apart.

<!-- stage: insight -->
### One Bundle Per Subtree

A call can return a small record of numbers for its finished subtree, and the parent combines the two records it receives. No second walk and no mutable report are needed.

<!-- names: returned fact, local answer, merge rule -->

#### What A Call Returns

A **returned fact** is a number in the record that a call hands to its parent, and it is chosen so that the parent needs nothing else from the subtree. Here the record has three numbers: the height of the subtree in nodes, the largest height gap of any node inside it, and the longest path inside it in edges. Each number summarizes a finished subtree, so the parent never looks inside it again.

#### What A Node Forms For Itself

A **local answer** is a number that exists only at one node, formed from the facts of its two children. The path with the node on top has `left height + right height` edges. The gap at the node is `|left height - right height|`. A local answer cannot be passed up as a branch, because a parent cannot extend a path that already uses both sides. The call folds each local answer into a returned fact by taking a maximum with the facts of the two children.

#### How Two Records Become One

The **merge rule** is the fixed formula that turns the left record, the right record and the node into the record of the node. The height is one more than the taller child. The gap is the largest of the local gap and the two child gaps. The path is the largest of the local path and the two child paths. An empty subtree returns the record of zeros, so a leaf needs no special case. The merge rule reads only the two records, and each node is merged once, so the whole walk costs O(n).

#### When A Failure May Stop The Walk

The balance lesson let one failing node stop all callers, because the answer was a yes or a no. This report needs a number from every node, so a worst gap cannot stop the walk at the first large gap. The bundle keeps going and records the maximum. The two designs differ in one question: does a failure decide the answer for every ancestor?

<!-- stage: variables -->
### The Three Numbers Of The Record

- **height** is the number of nodes on the longest downward chain of the subtree, and it is 0 for `null`.
- **gap** is the largest `|left height - right height|` at any node inside the subtree, and it is 0 for `null` and for a leaf.
- **path** is the largest number of edges on a path between two nodes inside the subtree, and it is 0 for `null` and for a leaf.

The local numbers `left height + right height` and `|left height - right height|` live inside one call and are not part of the record. Only `height` is a single branch that a parent can extend.

<!-- stage: trace -->
### Merging Records From The Leaves Up

#### A Chart With Uneven Sides

The chart has root 5. The root's left child is 3, which has children 1 and 4, and the node 1 has a left child 0. The root's right child is 8, which has a right child 9. A step shows a call that finishes. The variables show the record that it returns.

```trace
{"cells":["5","3","8","1","4","null","9","0"],"pointers":["node"],"steps":[{"at":{"node":7},"vars":{"height":1,"gap":0,"path":0},"note":"The call on the node 0 finishes. The children report heights 0 and 0, so the local gap is 0 and the local path is 0 edges. The record is height 1, gap 0, path 0."},{"at":{"node":3},"vars":{"height":2,"gap":1,"path":1},"note":"The call on the node 1 finishes. The children report heights 1 and 0, so the local gap is 1 and the local path is 1 edges. The record is height 2, gap 1, path 1."},{"at":{"node":4},"vars":{"height":1,"gap":0,"path":0},"note":"The call on the node 4 finishes. The children report heights 0 and 0, so the local gap is 0 and the local path is 0 edges. The record is height 1, gap 0, path 0."},{"at":{"node":1},"vars":{"height":3,"gap":1,"path":3},"note":"The call on the node 3 finishes. The children report heights 2 and 1, so the local gap is 1 and the local path is 3 edges. The record is height 3, gap 1, path 3."},{"at":{"node":6},"vars":{"height":1,"gap":0,"path":0},"note":"The call on the node 9 finishes. The children report heights 0 and 0, so the local gap is 0 and the local path is 0 edges. The record is height 1, gap 0, path 0."},{"at":{"node":2},"vars":{"height":2,"gap":1,"path":1},"note":"The call on the node 8 finishes. The children report heights 0 and 1, so the local gap is 1 and the local path is 1 edges. The record is height 2, gap 1, path 1."},{"at":{"node":0},"vars":{"height":4,"gap":1,"path":5},"note":"The call on the node 5 finishes. The children report heights 3 and 2, so the local gap is 1 and the local path is 5 edges. The record is height 4, gap 1, path 5."}]}
```

The root merges the records of 3 and 8. The left side has height 3 and the right side height 2, so the local gap is 1, and the local path is 5 edges. The record of the root reports the largest gap 1 and the longest path 5.

#### A Long Chain

The second chart is a chain: each manager has only a left report, and the chain has four managers.

```trace
{"cells":["1","2","null","3","null","4"],"pointers":["node"],"steps":[{"at":{"node":5},"vars":{"height":1,"gap":0,"path":0},"note":"The call on the node 4 finishes. The children report heights 0 and 0, so the local gap is 0 and the local path is 0 edges. The record is height 1, gap 0, path 0."},{"at":{"node":3},"vars":{"height":2,"gap":1,"path":1},"note":"The call on the node 3 finishes. The children report heights 1 and 0, so the local gap is 1 and the local path is 1 edges. The record is height 2, gap 1, path 1."},{"at":{"node":1},"vars":{"height":3,"gap":2,"path":2},"note":"The call on the node 2 finishes. The children report heights 2 and 0, so the local gap is 2 and the local path is 2 edges. The record is height 3, gap 2, path 2."},{"at":{"node":0},"vars":{"height":4,"gap":3,"path":3},"note":"The call on the node 1 finishes. The children report heights 3 and 0, so the local gap is 3 and the local path is 3 edges. The record is height 4, gap 3, path 3."}]}
```

Each call merges a record with an empty right record. The gap grows with the chain, and the path equals the height minus one at each step. The root reports a gap of 3 and a path of 3 edges after one visit per manager.

<!-- stage: code -->
### The Merge In Code

```java
final class OrgReport {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    record Facts(int height, int gap, int path) {}

    static Facts summarize(Node node) {
        if (node == null) return new Facts(0, 0, 0);             // an empty subtree is all zeros
        Facts l = summarize(node.left);                          // the left subtree reports first
        Facts r = summarize(node.right);                         // then the right subtree
        int localGap = Math.abs(l.height() - r.height());        // formed here, never returned alone
        int localPath = l.height() + r.height();                 // the path with this node on top
        return new Facts(
            1 + Math.max(l.height(), r.height()),                // a parent may extend one branch only
            Math.max(localGap, Math.max(l.gap(), r.gap())),      // fold the local gap into the maximum
            Math.max(localPath, Math.max(l.path(), r.path())));  // fold the local path into the maximum
    }
}
```

The method has no field and no parameter that the recursion changes. Every number travels in a return value, so the method is safe to call from two threads on the same tree.

- **Time** is O(n), as the walk makes one call per node and each merge reads two records.
- **Space** is O(h) for the open calls, and each call holds one small record.

<!-- stage: applicability -->
### Designing The Bundle

#### Writing The Merge Rule First

The invariant is that every field of the record describes exactly the finished subtree and needs no information from outside it. Write the merge rule for each field before coding, and check that it reads only the two child records and the node. A field that needs the parent's depth must become a parameter instead.

#### Finding The False Friend

Returning the local answer instead of the branch looks like it saves a field, and it is the false friend of this lesson. The parent would extend a path that already uses both sides. The reverse mistake is as common. A sentinel looks like the same tool, but it fits only a yes or no answer. A report of numbers needs the full record.

#### No-Go Conditions

The bundle works when each fact is a maximum, a sum or a count that merges from two children. If a fact needs the whole subtree again, such as the median of all values, the two records cannot give it. If the walk must stop at the first problem, return a sentinel and keep the record small.

<!-- stage: exercises -->
### Exercises

#### [Build] Maximum Depth With Deepest Leaf Count (LeetCode 104)
<!-- id: rr-depth-count -->

**Prerequisites.** The record and the merge rule from this lesson.

**Problem.** A binary tree has a root. The depth is the number of nodes on the longest path from the root to a leaf. Return an array of two integers: the depth and the number of leaves whose path from the root has exactly that many nodes. An empty tree gives `[0, 0]`.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Answer** is `[depth, count]` with `count >= 1` for a non-empty tree.
- **Mutation** is not allowed.

**Example 1.** Input root 9 with left child 4 and right child 7, output `[4, 1]`. Node 4 has a left child 2, and node 7 has a right child 8 with a right child 1.

**Example 2.** Input root 5 with the two leaf children 3 and 8, output `[2, 2]`.

**Hint.** What do two children with equal depths do to the count? What happens when one side is deeper?

**Changed decision.** The record holds a depth and a count, and the merge adds the counts only when the depths are equal.

#### [Vary] Diameter With Edge Costs (LeetCode 543)
<!-- id: rr-weighted-diameter -->

**Prerequisites.** The exercise above.

**Problem.** In a binary tree, the cost of the edge between a node and its parent equals the `val` of that node. The root's `val` is 0 and is never used. Return the largest total edge cost over all paths between two nodes. A tree with one node has answer 0.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4.
- **Values** are integers between 1 and 100, except the root, which holds 0.
- **Answer** is an integer between 0 and 2 * 10^6.
- **Mutation** is not allowed.

**Example 1.** Input root 0 with right child 5 and left child 4, where node 4 has children 2 and 3. Output 12, the path from the node 3 up to the root and down to the node 5.

**Example 2.** Input a single node 0, output 0.

**Hint.** What does a branch cost when it includes the edge to its parent? What does the path through a node add up to?

**Changed decision.** A branch carries a cost and not a length, and the path through a node adds two branch costs.

#### [Boundary] Balanced With Tolerance (LeetCode 110)
<!-- id: rr-tolerance -->

**Prerequisites.** The two exercises above.

**Problem.** Given a binary tree and an integer `k` with `k >= 0`, return `true` if at every node the heights of the two sides differ by at most `k`. Heights count nodes, and the empty tree has height 0. The value `k = 0` allows no difference at all. The method must make one pass.

**Constraints.** The limits are:
- **Nodes** number between 0 and 5000.
- **Values** are integers that the answer does not use.
- **Tolerance** `k` is an integer between 0 and 5000.
- **Answer** is a `boolean`, and the empty tree gives `true` for every `k`.

**Example 1.** Input root 6 with right child 8 and left child 4, where node 4 has a left child 2 with a left child 1. With `k = 1` the output is `false`.

**Example 2.** Input the same tree and `k = 2`, output `true`.

**Hint.** Which failure marker can no height equal? Where does `k` enter the comparison?

**Changed decision.** The allowed difference is a parameter, and `k = 0` accepts only perfectly even trees.

#### [Recognize] Binary Tree Maximum Path Sum (LeetCode 124)
<!-- id: rr-two-node-path -->

**Prerequisites.** All three exercises above.

**Problem.** A binary tree has at least two nodes, and its values may be negative. A path is a sequence of connected nodes with no repeats. It may start and end anywhere. Return the largest sum of values over all paths that contain at least two nodes.

**Constraints.** The limits are:
- **Nodes** number between 2 and 3 * 10^4.
- **Values** are integers between -1000 and 1000.
- **Answer** is an integer, and it is negative when every pair of connected nodes sums below zero.
- **Mutation** is not allowed.

**Example 1.** Input root -3 with the children -5 and -2, output -5, the path from the root to its right child.

**Example 2.** Input root 10 with a single left child -4, output 6, the only path of two nodes.

**Hint.** A branch may stop at its top node. A path at a node must use at least one child. What does a missing child contribute?

**Changed decision.** The path must contain at least two nodes, so a branch toward a child is forced even when its sum is negative.
