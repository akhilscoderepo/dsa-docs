<!-- lesson-kind: standard -->
<!-- lesson-id: tree-representation -->
## Tree Representation

<!-- stage: context -->
### The Orchard Family Register

An orchard has been planted by grafting, so every tree in it grew from one older tree, and the orchard keeper writes the lineage in a register. One original tree sits at the top. Beneath it, one or two grafts were taken, and each of those had grafts of its own. The register lists, for every tree, who its parent is. The keeper's grandchildren will ask questions like how many trees are in the orchard, how many generations the oldest line has, and how many trees have no grafts at all, and she wants to answer them without walking the whole orchard on foot each time.

The register is only a list of parents, which is awkward for these questions. The keeper wonders whether it would be better to write each tree so that it knows its own grafts, and what such a record should say about a tree that has no graft on one side.

<!-- stage: naive -->
### Walk Up The Parent List

The register gives each tree's parent, with the original tree marked by minus one. To count generations, the direct method takes each tree in turn and follows parents upward until it reaches the original.

```java
static int generationsByParents(int[] parent) {
    int best = 0;
    for (int tree = 0; tree < parent.length; tree++) {
        int steps = 1, at = tree;
        while (parent[at] != -1) { at = parent[at]; steps++; }
        best = Math.max(best, steps);
    }
    return best;
}
```

It is correct, because the number of trees on the path from a tree up to the original is its generation count, and the largest such count over all trees is the depth of the orchard.

<!-- stage: bottleneck -->
### Every Tree Repeats The Same Climb

A line of n grafts where each tree is the parent of the next makes the climb from the last tree take n steps, the climb from the one before take n minus one, and so on, so the total is O(n^2) steps. The climbs overlap almost completely, since the tree at generation fifty and the tree at generation fifty-one share all but one step of their path, yet the loop walks the shared part again for each. A hundred thousand trees in one line need five billion parent lookups.

The parent list also points the wrong way for the questions asked. It says where to go up, while counting trees below a given tree needs to go down, and going down from a parent means searching the whole list for entries that name it. A record that stores each tree's grafts directly would let a question about a tree be answered from its grafts' answers, one level at a time, and each tree would be visited once, for O(n) work.

<!-- stage: insight -->
### Each Node Owns Its Whole Subtree

Store each tree as a node that holds its value and its grafts. In a binary tree a node has a left graft and a right graft, and either can be absent. In a tree with any number of grafts a node holds a **child collection**, such as a list, that may have zero, one or many entries. In both cases the node together with everything below it is the **owned subtree** of that node, and a question about the whole orchard becomes a question about the owned subtree of the original tree.

The rule that makes recursion safe is the **empty subtree** convention. A missing left graft is stored as `null`, and a recursive method treats `null` as a complete, valid input with a defined answer: zero trees, height zero, nothing to visit. With that base case written first, every other call can assume its node exists and ask its grafts for answers. A node's answer is built from the answers of the subtrees it owns, so the total count is one plus the counts of the left and right subtrees.

The invariant is that each recursive call owns exactly one node's subtree, no subtree is owned by two calls, and the calls on the subtrees of a node together cover everything below it. A tree has one root and no cycles and no node with two parents, so a traversal needs no visited marks. A general network can break all of that, which is why trees and graphs are treated differently later.

<!-- names: child collection, owned subtree, empty subtree -->

An absent graft is a missing branch and not a branch holding a placeholder value, so the code never stores a fake node to stand for nothing.

<!-- stage: variables -->
### Nodes, Null Links And Collections

A binary node has three fields: `val`, `left` and `right`, and the last two hold either another node or `null`. A node with no children has two null links, which is how a leaf is recognized. An N-ary node has `val` and a `List` of children, and a leaf has an empty list, never a null list, so that a loop over the children is always safe. The question functions return plain numbers built from the numbers of their children, and the recursion needs no global variables for these questions. A tree with `n` nodes always has `n + 1` null links in the binary form, which makes a handy check on a hand-built tree.

<!-- stage: trace -->
### Counting From The Bottom Up

The first trace counts the nodes of a binary tree given in level-order form as 4, 2, 7, 1, 3, where the cells hold that array. The pointer `node` marks the node whose count has just been finished. Leaves finish first: the node 1 has two empty subtrees, so its count is one plus zero plus zero. The node 2 then adds one to the two counts of its leaves.

```trace
{"cells":["4","2","7","1","3"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"count":1},"note":"The node 1 has an empty left subtree and an empty right subtree, so its count is 1 + 0 + 0 = 1."},{"at":{"node":4},"vars":{"count":1},"note":"The node 3 has an empty left subtree and an empty right subtree, so its count is 1 + 0 + 0 = 1."},{"at":{"node":1},"vars":{"count":3},"note":"The node 2 has the left subtree of size 1 and the right subtree of size 1, so its count is 1 + 1 + 1 = 3."},{"at":{"node":2},"vars":{"count":1},"note":"The node 7 has an empty left subtree and an empty right subtree, so its count is 1 + 0 + 0 = 1."},{"at":{"node":0},"vars":{"count":5},"note":"The node 4 has the left subtree of size 3 and the right subtree of size 1, so its count is 1 + 3 + 1 = 5."}]}
```

The second trace finds the depth of a tree where each node holds a list of children. The cells are the nodes numbered from zero, with node 0 as the root. A leaf has an empty list, so it has depth one. Look at node 3: its single child has depth one, so it returns two, and the root takes the largest child depth and adds one.

```trace
{"cells":["0","1","2","3","4","5"],"pointers":["node"],"steps":[{"at":{"node":4},"vars":{"depth":1},"note":"The node 4 is a leaf with an empty child list, so its depth is 1."},{"at":{"node":1},"vars":{"depth":2},"note":"The node 1 takes the largest child depth 1 and adds one, so its depth is 2."},{"at":{"node":2},"vars":{"depth":1},"note":"The node 2 is a leaf with an empty child list, so its depth is 1."},{"at":{"node":5},"vars":{"depth":1},"note":"The node 5 is a leaf with an empty child list, so its depth is 1."},{"at":{"node":3},"vars":{"depth":2},"note":"The node 3 takes the largest child depth 1 and adds one, so its depth is 2."},{"at":{"node":0},"vars":{"depth":3},"note":"The node 0 takes the largest child depth 2 and adds one, so its depth is 3."}]}
```

<!-- stage: code -->
### Binary And N-Ary Recursion

```java
static final class Node {
    int val;
    Node left, right;
    Node(int val) { this.val = val; }
}

static final class NNode {
    int val;
    List<NNode> children = new ArrayList<>();
    NNode(int val) { this.val = val; }
}

static int countNodes(Node root) {
    if (root == null) return 0;
    return 1 + countNodes(root.left) + countNodes(root.right);
}

static int nodeDepth(NNode root) {
    if (root == null) return 0;
    int deepest = 0;
    for (NNode child : root.children) deepest = Math.max(deepest, nodeDepth(child));
    return 1 + deepest;
}
```

Each node is visited once and does constant work besides its calls, so both methods run in O(n) time. The extra space is the call stack, which is as deep as the height of the tree, so it is O(h), and h can be as large as n for a chain.

<!-- stage: applicability -->
### When Data Nests Without Cycles

Reach for a node structure when data has one root and each part contains parts of its own, as in family lineages, file folders, organisation charts and parsed expressions. The invariant is that each recursive call owns one node's subtree, `null` is a valid empty subtree with a defined answer, and no node is reachable by two routes.

A false friend is the parent list, which is compact and answers upward questions but turns every downward question into a search. A second false friend is a general graph, where cycles or several parents mean that a traversal needs visited marks. A third is a placeholder node with a fake value to stand for a missing child, which pollutes every answer that sums or compares values.

In Java, test for `null` before touching a field, because `root.left` on a null root throws `NullPointerException`. Give an N-ary leaf an empty list so loops need no guard. Remember that the recursion depth equals the tree height, so a chain of a hundred thousand nodes can overflow the call stack, which the iterative lessons later deal with.

<!-- stage: exercises -->
### Exercises

#### [Build] Construct A Three-Node Tree (Author exercise)
<!-- id: tr-three-node-tree -->

**Prerequisites.** The earlier chapters on stacks.

**Problem.** Given a root value and optional left and right child values, build the binary tree with one node per given value and return the number of `null` links in it, counting both children of every node. Each missing child is one empty subtree, and a node with no children has two.

**Constraints.** The root value is an integer, each child value is an integer or `null`, and at most three nodes exist.

**Example 1.** Input `root = 1, left = 2, right = 3`, output `4`.

**Example 2.** Input `root = 1, left = 2, right = null`, output `3`.

**Hint.** How many child slots does each node have? How many of the slots are filled by nodes?

**Changed decision.** First rung: the tree is built by hand, and every empty child slot is a null link that counts as one empty subtree.

#### [Vary] Count N-Ary Children (Author exercise)
<!-- id: tr-count-nary-children -->

**Prerequisites.** The Construct A Three-Node Tree rung.

**Problem.** An N-ary tree is given by `children`, where `children[i]` lists the nodes that are the children of node `i`, and node 0 is the root. Return `[widest, leaves]`, the largest number of children any node has and the number of nodes with no children.

**Constraints.** 1 <= children.length <= 100000, every node other than 0 appears in exactly one list, and the lists describe a tree rooted at node 0.

**Example 1.** Input `children = [[1, 2, 3], [4], [], [], []]`, output `[3, 3]`.

**Example 2.** Input `children = [[]]`, output `[0, 1]`.

**Hint.** What is the length of a node's child list, and what does an empty list say about the node?

**Changed decision.** A node may have any number of children, so the code reads the length of the supplied collection and never assumes a left and a right.

#### [Boundary] Empty And Single-Node Trees (Author exercise)
<!-- id: tr-empty-single-trees -->

**Prerequisites.** The Count N-Ary Children rung.

**Problem.** A binary tree is given as a level-order array in which `null` marks a missing child, and the children of a missing node are not listed. Return `[size, height, leaves]`, where height counts nodes on the longest root-to-leaf path. For the empty tree, which is the empty array, all three values are zero.

**Constraints.** 0 <= values.length <= 100000 and the array follows the level-order format.

**Example 1.** Input `values = []`, output `[0, 0, 0]`.

**Example 2.** Input `values = [1, null, 2, null, 3]`, output `[3, 3, 1]`.

**Hint.** What should each of the three questions answer for a null node? How does that answer combine at a leaf?

**Changed decision.** The answers at `null` are fixed before any recursion is written, so the empty tree and the single node follow from the same rule.

#### [Recognize] Maximum Depth of N-ary Tree (LeetCode 559)
<!-- id: tr-max-depth-nary -->

**Prerequisites.** The Empty And Single-Node Trees rung.

**Problem.** An N-ary tree is given by `children` as before, with node 0 as the root. Return its maximum depth, the number of nodes on the longest path from the root down to a leaf.

**Constraints.** 1 <= children.length <= 10000 and the lists describe a tree rooted at node 0.

**Example 1.** Input `children = [[1, 2], [3], [], [4], []]`, output `4`.

**Example 2.** Input `children = [[]]`, output `1`.

**Hint.** What is the depth of a leaf? How does a node combine the depths of all of its children?

**Changed decision.** The depth recurrence of a binary tree is generalised from two children to a collection, and the answer is one plus the largest child depth.
