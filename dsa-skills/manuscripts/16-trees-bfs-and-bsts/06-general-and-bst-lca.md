<!-- lesson-kind: standard -->
<!-- lesson-id: general-and-bst-lca -->
## Find The Lowest Common Ancestor

<!-- stage: context -->
### Why Two Files Need A Shared Folder

A backup tool must copy two changed files together, and it wants the smallest folder that holds both of them, so the copy stays small. The first version lists every folder on the disk and asks of each one whether both files live inside it. The tool finds the right folder, but a large disk takes minutes, and the same disk answers a second pair of files just as slowly.

The **lowest common ancestor** of two nodes is the deepest node that has both of them in its subtree, and a node counts as being in its own subtree. This lesson asks how a program finds that node in one pass over a tree, and what extra help a search tree gives.

<!-- stage: naive -->
### Asking Every Node Whether It Holds Both

The direct plan tests candidates from the root downward. A node qualifies when its subtree holds both targets. The plan then tries to go lower, into the left child and into the right child, and keeps the deepest node that still qualifies.

```java
final class LcaByContains {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static boolean contains(TreeNode node, TreeNode target) {
        if (node == null) return false;
        return node == target || contains(node.left, target) || contains(node.right, target);   // compare references
    }

    static TreeNode lca(TreeNode node, TreeNode p, TreeNode q) {
        if (node == null || !contains(node, p) || !contains(node, q)) return null;   // this subtree lacks a target
        TreeNode inLeft = lca(node.left, p, q);                                      // try to go lower on the left
        if (inLeft != null) return inLeft;
        TreeNode inRight = lca(node.right, p, q);                                    // or lower on the right
        return inRight != null ? inRight : node;                                     // neither child holds both
    }
}
```

On the tree with the root 10, the children 4 and 15, and the children 2 and 7 under the node 4, with the children 6 and 9 under the node 7, the lowest common ancestor of the nodes 6 and 9 is the node 7. The method returns it.

<!-- stage: bottleneck -->
### Repeating The Subtree Scans

```predict
The tree is a chain of n nodes, and both targets are the deepest node. How many nodes do the contains calls visit in total, and what is the cost in big-O terms?

The call at depth d scans the remaining n - d nodes, twice, so the total is about n squared. The cost is O(n^2) on a chain, and O(n * h) in general.
```

The method scans the same nodes again at every level of the descent. Each `contains` call repeats work that the call one level above already did. The facts "this subtree holds p" and "this subtree holds q" are properties of a subtree, and a bottom-up walk can compute them once for each subtree.

A search tree gives a second kind of help. The keys of the targets, compared with the key of a node, can tell which side holds both of them without any scan.

<!-- stage: insight -->
### Report Upward Or Compare Keys

#### Letting Children Report The Targets

A **post-order** walk handles both children before it handles the node. Each call returns the target it found in its subtree, or `null` if it found none. A call that reaches `null` returns `null`. A call that meets a target returns that node at once, and it does not look below it. Otherwise the call collects the answers of its two children. When both answers are non-null, the two targets sit in different child subtrees, so the current node is the lowest common ancestor. When only one answer is non-null, the call passes it up unchanged. The root call returns the answer.

A node that is itself a target returns itself even when the other target lies below it. The other target is in that node's subtree, so the node is the answer, and the walk can ignore everything beneath it.

#### Finding The Split Point In A Search Tree

A search tree allows a shortcut with no recursion over both sides. Start at the root and compare the two target keys with the node key. If both keys are smaller, the whole answer lies in the left subtree, so the walk moves left. If both are larger, the walk moves right. Otherwise one key is smaller, one is larger, or one equals the node key. That node is the **split point**, the first node where the paths to the targets separate or end, and it is the lowest common ancestor.

The walk is a **descent** that follows one path and costs O(h). The shortcut relies on the key order. In a tree with no order, a comparison of keys says nothing about the side of a target.

<!-- names: post-order, split point, descent -->

<!-- stage: variables -->
### The State Of The Two Methods

- **node** is the node under test, starting at the root.
- **p** and **q** are the two targets, given as nodes.
- **left** and **right** hold what the two child calls returned, which is a target node or `null`.
- **answer** is `node` when both `left` and `right` are non-null, and otherwise the one non-null result.
- **lo** and **hi** are the smaller and larger target keys in the search tree method.

<!-- stage: trace -->
### Reports Rising And A Path Splitting

Each cell is one key of the tree, listed row by row from the root, and the pointer `node` marks the node being handled.

#### Collecting Reports Bottom-Up

The tree has the root 10, the children 4 and 15, the children 2 and 7 under the node 4, and the children 12 and 20 under the node 15. The nodes 6 and 9 are the children of the node 7. The targets are 6 and 9.

```trace
{"cells":[10,4,15,2,7,12,20,6,9],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"returns":"null"},"note":"No child reported a target, so the call returns null."},{"at":{"node":7},"vars":{"returns":6},"note":"6 is a target, so the call returns it at once."},{"at":{"node":8},"vars":{"returns":9},"note":"9 is a target, so the call returns it at once."},{"at":{"node":4},"vars":{"returns":7},"note":"Both children reported a target, so 7 is the lowest common ancestor and the call returns it."},{"at":{"node":1},"vars":{"returns":7},"note":"Only one child reported, so the call passes that report up."},{"at":{"node":5},"vars":{"returns":"null"},"note":"No child reported a target, so the call returns null."},{"at":{"node":6},"vars":{"returns":"null"},"note":"No child reported a target, so the call returns null."},{"at":{"node":2},"vars":{"returns":"null"},"note":"No child reported a target, so the call returns null."},{"at":{"node":0},"vars":{"returns":7},"note":"Only one child reported, so the call passes that report up."}]}
```

The node 7 is the first call to receive two non-null reports, so it is the answer. The node 4 and the root only pass that report up.

#### Walking Down To The Split Point

The same tree is a search tree. The method looks for the split point of the keys 6 and 9.

```trace
{"cells":[10,4,15,2,7,12,20,6,9],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"lo":6,"hi":9},"note":"Both keys are smaller than 10, so the walk goes left."},{"at":{"node":1},"vars":{"lo":6,"hi":9},"note":"Both keys are larger than 4, so the walk goes right."},{"at":{"node":4},"vars":{"lo":6,"hi":9},"note":"The keys 6 and 9 lie on different sides of 7, so 7 is the split point and the answer."}]}
```

The walk compares two keys per step and reaches the node 7 in three steps, without visiting any node of the right subtree of the root.

<!-- stage: code -->
### Both Methods In Code

```java
final class Ancestors {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode lcaGeneral(TreeNode node, TreeNode p, TreeNode q) {
        if (node == null || node == p || node == q) return node;     // stop at a target or at an empty slot
        TreeNode left = lcaGeneral(node.left, p, q);                 // children report before the node decides
        TreeNode right = lcaGeneral(node.right, p, q);
        if (left != null && right != null) return node;              // targets in different subtrees: this is the split
        return left != null ? left : right;                          // pass the single report up, or null
    }

    static TreeNode lcaSearchTree(TreeNode root, int a, int b) {
        int lo = Math.min(a, b), hi = Math.max(a, b);
        TreeNode node = root;
        while (node != null) {
            if (hi < node.val) node = node.left;                     // both keys are smaller
            else if (lo > node.val) node = node.right;               // both keys are larger
            else return node;                                        // the keys split here or one equals the node
        }
        return null;                                                 // only when the keys are not in the tree
    }
}
```

The general method compares node references with `==`, because two different nodes can hold the same value. The search tree method compares keys, because its keys are distinct.

- **Time** of `lcaGeneral` is O(n), because each node is visited once, and its space is O(h) for the recursion.
- **Time** of `lcaSearchTree` is O(h), and its space is O(1).

<!-- stage: applicability -->
### Choosing Between The Two Methods

#### Recognizing The Cue

The phrase "lowest common ancestor" or "smallest subtree containing both" asks for this lesson. Check the contract first. If the tree is a valid search tree, use the key descent. If keys may repeat or the order is unknown, use the post-order report.

#### Stating The Invariant

The invariant of the report method is that a call returns a target only if that target lies in its subtree, and it returns the lowest common ancestor when both targets lie there. The invariant of the key descent is that both targets always lie in the subtree of the current node. A split ends the descent because no child can hold both.

#### Avoiding The False Friend

The false friend is the key shortcut applied to a tree with no order. In a tree where the node 6 sits above the node 3, comparing keys sends the walk to the wrong side, and the result is wrong without any error. The shortcut is valid only for a search tree. A second trap is the target that is also the ancestor. The report method stops at the first target it meets, which is correct only when both targets are guaranteed to exist.

<!-- stage: exercises -->
### Exercises

#### [Build] General-Tree Ancestor Return (Author exercise)
<!-- id: tb-lca-combine -->

**Prerequisites.** The post-order report from this lesson.

**Problem.** Given the root of a binary tree with distinct values and the values of two different leaves `a` and `b`, return the value of their lowest common ancestor. Each call returns the leaf it found below it, or `null`. The call where both children return a leaf is the answer.

**Constraints.** The limits are:
- **Nodes** number between 3 and 10^4, and all values are distinct.
- **Targets** are values of two different leaves that exist in the tree.
- **Answer** is an `int` value of a node.
- **Mutation** does not occur.

**Example 1.** Input root 10 with children 4 and 15, where 4 has children 2 and 7, 7 has children 6 and 9, and 15 has children 12 and 20, with leaves 6 and 9, output 7.

**Example 2.** Input the same tree with leaves 2 and 12, output 10.

**Hint.** What does a call return when it reaches a leaf that is not a target? When do both children return non-null?

**Changed decision.** Only the rule that combines two child reports is new.

#### [Vary] Lowest Common Ancestor of a Binary Tree (LeetCode 236)
<!-- id: tb-lca-binary-tree -->

**Prerequisites.** The exercise above.

**Problem.** Given the root of a binary tree and two nodes `p` and `q` that exist in the tree, return their lowest common ancestor. The ancestor of a node may be the node itself. Values may repeat, so compare nodes by reference and not by value.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^5.
- **Values** satisfy `-10^9 <= val <= 10^9`, and values may repeat.
- **Targets** are different nodes that exist in the tree.
- **Mutation** does not occur.

**Example 1.** Input root 9 with children 4 and 11, where 4 has children 8 and 2, 2 has children 7 and 5, and 11 has children 0 and 6, with `p` the node 8 and `q` the node 11, output the node 9.

**Example 2.** Input the same tree with `p` the node 4 and `q` the node 5, output the node 4.

**Hint.** What should a call return when it meets `p` or `q`? What does a call return when only one child reports?

**Changed decision.** Targets are arbitrary nodes, and a target may sit above the other target.

#### [Boundary] One Target Is Ancestor (Author exercise)
<!-- id: tb-lca-ancestor-target -->

**Prerequisites.** The two exercises above.

**Problem.** Given the root of a binary tree with distinct values and the values of two nodes `a` and `b`, where one of the two nodes lies in the subtree of the other, return the value of the higher node. The method must return as soon as it meets the first target and must not visit any node below it.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^4, and all values are distinct.
- **Targets** exist, and one is an ancestor of the other.
- **Answer** is an `int` value of one of the two targets.
- **Mutation** does not occur.

**Example 1.** Input root 3 with children 5 and 1, where 5 has children 6 and 2 and 1 has children 0 and 8, with `a = 5` and `b = 2`, output 5.

**Example 2.** Input the same tree with `a = 3` and `b = 8`, where 8 is below 1, output 3.

**Hint.** What does the call at the higher target return, and does it need its children?

**Changed decision.** The first target found ends the walk below it.

#### [Recognize] Lowest Common Ancestor of a Binary Search Tree (LeetCode 235)
<!-- id: tb-lca-bst -->

**Prerequisites.** All three exercises above.

**Problem.** The input is a search tree and two nodes `p` and `q` that exist in it. Return their lowest common ancestor. Move left when both keys are smaller than the current key and right when both are larger. Stop at the first node where the keys split or one key equals the node key.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^5, and all keys are distinct.
- **Values** satisfy `-10^9 <= val <= 10^9`.
- **Targets** are different nodes that exist in the tree.
- **Mutation** does not occur.

**Example 1.** Input root 20 with children 8 and 30, where 8 has children 3 and 12 and 30 has children 25 and 40, with `p = 8` and `q = 30`, output the node 20.

**Example 2.** Input the same tree with `p = 8` and `q = 12`, output the node 8.

**Hint.** What do the two keys say about the side when both are smaller than the node? What ends the walk?

**Changed decision.** Key order replaces the report from both subtrees.
