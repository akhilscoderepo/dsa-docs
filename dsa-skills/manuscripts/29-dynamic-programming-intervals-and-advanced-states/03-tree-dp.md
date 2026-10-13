<!-- lesson-kind: standard -->
<!-- lesson-id: tree-dp -->
## Tree DP

<!-- stage: context -->
### Choosing People In A Reporting Tree

A company wants to pick people for a review panel. Each person has a score, and nobody may sit on the panel together with their direct manager. The goal is the highest total score.

A manager scores 5 and has two reports who score 4 each. A quick rule picks the highest score first, so it picks the manager and blocks both reports. The total is 5. The better panel holds the two reports and totals 8. One early pick ruined the result.

Formally, the input is a **tree**: a set of nodes joined by edges with one **root** and no cycles. Every node except the root has one **parent**, and the nodes directly below a node are its **children**. A node with no children is a **leaf**. A **subtree** of a node is that node together with everything below it. Each node carries an integer weight. The task is to choose a set of nodes so that no chosen node has a chosen parent, and to return the largest total weight.

The code and traces in this lesson use binary trees, where each node has a `left` and a `right` child. The general form replaces the two children with a sum over all children of the node.

This lesson asks how a parent can decide well when the answer for each child depends on whether the parent is chosen.

<!-- stage: naive -->
### Trying Both Choices At Every Node

The direct method makes the decision at the root and recurses. If the root is chosen, its children are blocked, so the method adds the root weight to the best results of the grandchildren. If the root is not chosen, the method adds the best results of the two children. It returns the larger sum.

```java
static int best(Node node) {
    if (node == null) return 0;
    int withNode = node.val;
    if (node.left != null) withNode += best(node.left.left) + best(node.left.right);
    if (node.right != null) withNode += best(node.right.left) + best(node.right.right);
    int withoutNode = best(node.left) + best(node.right);
    return Math.max(withNode, withoutNode);
}
```

Here `Node` has an `int val` and two fields `left` and `right`, each a `Node` or `null`. The method is correct, because it tries both choices at every node. It also solves the same subtree again and again. The grandchild subtrees are visited once through `withNode` and once more through the children.

<!-- stage: bottleneck -->
### The Same Subtree Is Solved Twice

```predict
A chain has 30 nodes, and each node has exactly one child. Roughly how many calls does best make, counting calls on null?

It makes 7,049,153 calls. Each node spawns calls for its child and its grandchild, so the count follows the Fibonacci pattern and grows by a factor near 1.6 for every added node.
```

The call count `c(n)` for a chain of n nodes satisfies c(n) = 1 + c(n - 1) + c(n - 2) plus a few calls on null. That recurrence is exponential, so the method runs in O(1.6^n) time on a chain. In any tree, a grandchild subtree is solved once through `withNode` and once through its parent in `withoutNode`. The repeats compound with every added level of depth. The recursion also uses O(h) stack space for a tree of height h.

The repeated work has a clear cause. The method asks each subtree one question per call: what is your best total? Yet the parent needs two different answers from a child, one for a chosen parent and one for a free parent. Each call computes only one of them, so the other is recomputed later in a separate call. If each subtree answered both questions once and returned both answers, the parent could read everything from two numbers per child. Total work then falls to O(n), one visit per node. The next section defines these two numbers.

<!-- stage: insight -->
### Return Two Numbers From Each Subtree

A parent cares about only one fact of each child subtree: whether the child itself is chosen. So every subtree reports its best total for each of the two cases, and the parent combines those totals.

<!-- names: take value, skip value, neutral pair -->

#### Two Answers For Each Node

For a node `v`, the **take value** is the largest total weight in the subtree of `v` when `v` itself is chosen. The **skip value** is the largest total weight in the subtree of `v` when `v` is not chosen. Both values count only nodes inside that subtree. The best total for the whole subtree is the larger of the two.

#### How A Parent Combines Children

If `v` is chosen, both children must be left out. The take value is the weight of `v` plus the skip value of each child. If `v` is not chosen, each child is free to go either way. The skip value is the larger of take and skip for the left child plus the larger of take and skip for the right child. Each child contributes independently, because the only link between two sibling subtrees runs through their shared parent.

#### The Neutral Pair For A Missing Child

A missing child is an empty subtree with no nodes and no weight. Its **neutral pair** is take 0 and skip 0. Plugging the neutral pair into both formulas adds nothing, so a leaf gets take equal to its weight and skip equal to 0 with no special case. A node with one child uses the neutral pair for the other side in the same way.

#### Why Post-Order Works

The invariant is that the pair returned for a subtree is final and summarizes that subtree completely for both choices of its root. A parent reads two finished pairs and never needs to look inside them again. The method therefore visits the children first and the parent last. The answer for the whole tree is the larger value of the root pair.

<!-- stage: variables -->
### The Pair Each Call Returns

A call receives one node and returns two integers. The working values are these.

- **node** is the subtree root in the current call.
- **left** and **right** are the pairs returned for the two children, each holding a take value and a skip value.
- **take** is the weight of `node` plus the skip values of `left` and `right`.
- **skip** is the larger entry of `left` plus the larger entry of `right`.

The method returns the pair as an `int[2]`, with the take value at index 0 and the skip value at index 1. For a `null` node it returns `{0, 0}`, the neutral pair. A tree with n nodes produces n pairs, one per call, plus the neutral pairs for missing children.

<!-- stage: trace -->
### Two Runs Over Small Trees

#### A Tree With Two Levels Of Children

Trace cells need an array, so the tree is stored in heap layout. The root sits at cell 0, and the children of the node at cell `k` sit at cells `2k + 1` and `2k + 2`. The value -1 marks a missing node. The first tree is `[6, 2, 5, 4, 1, -1, 3]`. Node 6 has children 2 and 5. Node 2 has leaves 4 and 1, and node 5 has only a right child 3.

All weights in a tree are different, so the trace names each node by its weight. The pointer `node` marks the cell being finished, and the order is post-order, so children finish first. The variables `left` and `right` hold the pairs of the two children as (take, skip), and `take` and `skip` are the pair just computed. The leaves 4, 1 and 3 get a take value equal to their weight and a skip value of 0. Node 2 chooses itself for 2 or leaves itself out for 4 + 1 = 5, so its pair is (2, 5). Node 5 gets (5, 3). The root combines them: take is 6 + 5 + 3 = 14, and skip is 5 + 5 = 10. The answer is 14.

```trace
{"cells":[6,2,5,4,1,-1,3],"pointers":["node"],"steps":[{"at":{"node":-1},"vars":{},"note":"Start: no subtree is finished yet."},{"at":{"node":3},"vars":{"left":"(0, 0)","right":"(0, 0)","take":4,"skip":0},"note":"Node 4 finishes. Take is 4 + 0 + 0 = 4. Skip is 0 + 0 = 0."},{"at":{"node":4},"vars":{"left":"(0, 0)","right":"(0, 0)","take":1,"skip":0},"note":"Node 1 finishes. Take is 1 + 0 + 0 = 1. Skip is 0 + 0 = 0."},{"at":{"node":1},"vars":{"left":"(4, 0)","right":"(1, 0)","take":2,"skip":5},"note":"Node 2 finishes. Take is 2 + 0 + 0 = 2. Skip is 4 + 1 = 5."},{"at":{"node":6},"vars":{"left":"(0, 0)","right":"(0, 0)","take":3,"skip":0},"note":"Node 3 finishes. Take is 3 + 0 + 0 = 3. Skip is 0 + 0 = 0."},{"at":{"node":2},"vars":{"left":"(0, 0)","right":"(3, 0)","take":5,"skip":3},"note":"Node 5 finishes. Take is 5 + 0 + 0 = 5. Skip is 0 + 3 = 3."},{"at":{"node":0},"vars":{"left":"(2, 5)","right":"(5, 3)","take":14,"skip":10},"note":"Node 6 finishes. Take is 6 + 5 + 3 = 14. Skip is 5 + 5 = 10."},{"at":{"node":0},"vars":{"take":14,"skip":10,"answer":14},"note":"The answer is the larger of take 14 and skip 10, which is 14."}]}
```

#### A Skip Beats A Take

The second tree is `[2, 1, 3, -1, 4]`. Node 1 has only a right child, which is the leaf 4. Node 1 gets (1, 4), because choosing the leaf 4 beats choosing node 1. At the root, taking 2 gives 2 + 4 + 0 = 6, and skipping it gives the larger entry of node 1, which is 4, plus the larger entry of node 3, which is 3, so 7. The skip value wins and the answer is 7.

```trace
{"cells":[2,1,3,-1,4],"pointers":["node"],"steps":[{"at":{"node":-1},"vars":{},"note":"Start: no subtree is finished yet."},{"at":{"node":4},"vars":{"left":"(0, 0)","right":"(0, 0)","take":4,"skip":0},"note":"Node 4 finishes. Take is 4 + 0 + 0 = 4. Skip is 0 + 0 = 0."},{"at":{"node":1},"vars":{"left":"(0, 0)","right":"(4, 0)","take":1,"skip":4},"note":"Node 1 finishes. Take is 1 + 0 + 0 = 1. Skip is 0 + 4 = 4."},{"at":{"node":2},"vars":{"left":"(0, 0)","right":"(0, 0)","take":3,"skip":0},"note":"Node 3 finishes. Take is 3 + 0 + 0 = 3. Skip is 0 + 0 = 0."},{"at":{"node":0},"vars":{"left":"(1, 4)","right":"(3, 0)","take":6,"skip":7},"note":"Node 2 finishes. Take is 2 + 4 + 0 = 6. Skip is 4 + 3 = 7."},{"at":{"node":0},"vars":{"take":6,"skip":7,"answer":7},"note":"The answer is the larger of take 6 and skip 7, which is 7."}]}
```

<!-- stage: code -->
### Computing The Pair In One Pass

The method below returns the best total weight. A helper does the post-order recursion and returns the pair for each subtree.

```java
final class TreeDp {
    static final class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static int bestTotal(Node root) {
        int[] pair = pairOf(root);
        return Math.max(pair[0], pair[1]);
    }

    static int[] pairOf(Node node) {
        if (node == null) return new int[] {0, 0};
        int[] left = pairOf(node.left);
        int[] right = pairOf(node.right);
        int take = node.val + left[1] + right[1];
        int skip = Math.max(left[0], left[1]) + Math.max(right[0], right[1]);
        return new int[] {take, skip};
    }
}
```

Each node triggers one call, and each call does a constant amount of work, so time is O(n). The stack grows to the height of the tree, which is O(h) memory. A chain of a million nodes would overflow the default stack, and a parent array processed from the last index down avoids recursion entirely. An empty tree returns 0, because both entries of the neutral pair are 0.

<!-- stage: applicability -->
### Recognizing Subtree Summaries

#### Reading The Cue

Use this method when a decision at a node changes what its children may do, and the children's subtrees do not interact except through that node. Phrases such as "no two adjacent", "a parent and child may not both" and "answer for every node as the root" point here. The state is a node together with a small number of modes of that node, and each mode has its own best value.

#### Checking The Invariant

The invariant says that every returned pair describes its own subtree completely, for each mode the parent can ask about. Test a single node, which must return its weight when the weight is positive. Test a chain of three nodes with weights 4, 5, 4, where the middle node loses to the two ends. Test a node with only a left child and a node with only a right child. Compare the result with a subset check on trees of about a dozen nodes.

#### Avoiding The False Friend

The first false friend is the greedy pick of the heaviest node, which fails on the opening example. The second is the sum of every other level, which assumes the best panel uses whole levels. A tree where the top level is heavy but the next level has one very large node breaks it. The third is a single returned number, which cannot tell the parent whether the child is chosen. The method does not apply when nodes have several parents or when the graph has a cycle, because a subtree no longer isolates its own choices. It also does not apply when the rule links nodes farther apart than parent and child, unless the pair grows to hold the extra modes.

<!-- stage: exercises -->
### Exercises

#### [Build] Take Or Skip Node (Author exercise)
<!-- id: dp29-take-or-skip-node -->

**Prerequisites.** The pair of take and skip values from this lesson.

**Problem.** A rooted tree has nodes `0` to `n - 1`, with root `0`. An array `parent` gives the parent of each node, where `parent[0] = -1` and `parent[i] < i` for `i >= 1`. An array `w` gives the weight of each node. A set of nodes is valid if no chosen node has a chosen parent. Return an array of two integers. The first is the largest total weight of a valid set that contains node `0`. The second is the largest total weight of a valid set that does not contain node `0`.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 100000`.
- **Weights** satisfy `0 <= w[i] <= 1000`.
- **Result** is an `int[2]`, and the sums fit in `int`.
- **Mutation** is not allowed for the input arrays.

**Example 1.** Input `parent = [-1, 0, 0, 1, 1]`, `w = [2, 7, 4, 6, 1]`, output `[9, 11]`.

**Example 2.** Input `parent = [-1, 0, 1, 2]`, `w = [5, 1, 1, 5]`, output `[10, 6]`.

**Hint.** Every parent has a smaller index than its children. In which order can the loop visit the nodes so that each node is finished before its parent?

**Changed decision.** The method returns both values for the root in place of one maximum. The loop runs from the last node down to node 1 and pushes each finished pair into its parent.

#### [Vary] House Robber III (LeetCode 337)
<!-- id: dp29-house-robber-iii -->

**Prerequisites.** The exercise above.

**Problem.** A binary tree is given by its root. Each node holds a non-negative integer amount. Choose a set of nodes so that no chosen node is the parent of another chosen node. Return the largest total amount of a valid set.

**Constraints.** The limits are:
- **Size** satisfies `1 <= nodes <= 1000`, and the height is at most 1000.
- **Values** satisfy `0 <= val <= 10000`.
- **Result** is an `int`.
- **Mutation** is not allowed, so the tree stays unchanged.

**Example 1.** Input root `[5, 4, 3, 2, 1]` in level order, output `8`.

**Example 2.** Input root `[4, 1, null, 2, null, 3]` in level order, output `7`.

**Hint.** When a node is chosen, what must the skip value of each child supply, and what may the parent read when the node is left out?

**Changed decision.** The tree is binary with explicit child links in place of a parent array, so the method recurses over the links. Choosing a node forces both children into their skip states.

#### [Boundary] Null And Negative Values (Author exercise)
<!-- id: dp29-null-and-negative -->

**Prerequisites.** The two exercises above.

**Problem.** A binary tree is given by its root, which may be `null`. Each node holds an integer, possibly negative. Choose any set of nodes, possibly empty, so that no chosen node is the parent of another chosen node. Return the largest total of a valid set. The empty set has total 0.

**Constraints.** The limits are:
- **Size** satisfies `0 <= nodes <= 1000`, and the height is at most 1000.
- **Values** satisfy `-10000 <= val <= 10000`.
- **Result** is an `int`, and an empty tree returns 0.
- **Mutation** is not allowed, so the tree stays unchanged.

**Example 1.** Input root `[-3, -2, -4]` in level order, output `0`.

**Example 2.** Input root `[5, -10, 5, -1, 7]` in level order, output `12`.

**Hint.** What pair should a missing child return, and does the skip value of a subtree ever fall below 0 when the empty set is allowed?

**Changed decision.** Negative weights can push a take value below 0. The skip value of every subtree still allows the empty set, so the answer never falls below 0.

#### [Recognize] Rerooted Distance Sums (Author exercise)
<!-- id: dp29-rerooted-distance-sums -->

**Prerequisites.** All three exercises above.

**Problem.** An undirected tree has nodes `0` to `n - 1` and `n - 1` edges. The distance between two nodes is the number of edges on the path between them. For every node `v`, return the sum of the distances from `v` to all nodes of the tree. Return the sums as an array indexed by node.

**Constraints.** The limits are:
- **Size** satisfies `1 <= n <= 10000`.
- **Edges** are given as pairs `{a, b}` and form one connected tree.
- **Result** is an `int[n]`, and each sum fits in `int`.
- **Mutation** is not allowed for the edge list.

**Example 1.** Input `n = 4`, `edges = [[0, 1], [0, 2], [2, 3]]`, output `[4, 6, 4, 6]`.

**Example 2.** Input `n = 5`, `edges = [[0, 1], [1, 2], [2, 3], [3, 4]]`, output `[10, 7, 6, 7, 10]`.

**Hint.** One pass from the leaves up gives, for each node, its subtree size and the distance sum inside that subtree. How does the answer change when the root moves from a parent to one child?

**Changed decision.** Every node must be the root once, so a second pass from the root down hands each child a parent contribution. Each subtree returns a count and a distance sum, which is a pair in place of the take and skip values.
