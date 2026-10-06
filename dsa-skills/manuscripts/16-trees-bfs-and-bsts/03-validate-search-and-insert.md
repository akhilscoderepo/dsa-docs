<!-- lesson-kind: standard -->
<!-- lesson-id: validate-search-and-insert -->
## Search And Insert With One Path

<!-- stage: context -->
### Why The Dictionary Lookup Stalls

A dictionary app stores two million words in a binary search tree. The first version of the lookup visits every node until it finds the word, and a lookup of a word near the end freezes the screen for a visible moment. The tree was built so that one comparison at a node says which side holds the word, and the lookup ignores that fact. The same tree also needs a way to add a new word, and the insert must put the word where a later lookup will find it.

This lesson asks how many nodes a lookup must touch, and where a new key goes so that the tree stays a valid search tree.

<!-- stage: naive -->
### Visiting Every Node Until A Match

The direct plan treats the tree like an unordered collection. It visits the root, then the whole left subtree, then the whole right subtree, and it returns the node as soon as the key matches.

```java
final class SearchByScan {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode find(TreeNode node, int key) {
        if (node == null) return null;                   // this branch ends without a match
        if (node.val == key) return node;                // the key matches this node
        TreeNode inLeft = find(node.left, key);          // search the whole left side first
        return inLeft != null ? inLeft : find(node.right, key);   // then the whole right side
    }
}
```

On the tree with the root 4, the children 2 and 7, and the children 1 and 3 under the node 2, a search for 7 visits the nodes 4, 2, 1, 3 and 7 before it returns. The answer is correct.

<!-- stage: bottleneck -->
### Counting The Comparisons

```predict
A search tree holds one million keys and has the smallest possible height. About how many comparisons does a lookup need if it can discard one side at every node, and how many does the scan above need in the worst case?

A tree of height 20 holds more than a million nodes, so a lookup that discards one side per comparison needs about 20 comparisons. The scan above needs up to one million comparisons in the worst case.
```

The scan costs O(n), because a missing key sends it through every node. The ordering of the tree makes most of that work unnecessary. When the key is smaller than the node, every node on the right side is larger than the node, and so larger than the key. None of them can match. The scan visits them anyway.

The method needs a rule that takes one branch per node and ignores the other branch completely.

<!-- stage: insight -->
### Take One Branch At Every Node

Compare the key with the node key. An equal key ends the search. A smaller key sends the search to the left child, and a larger key sends it to the right child. The branch not taken is the **discarded subtree**, and it cannot hold the key, because the ordering puts every key of that subtree on the wrong side of the node. The nodes the search visits form the **search path**, a single line from the root downward. The method touches one node per level, so the cost is O(h) for height `h`.

The method can be a loop with no recursion. It keeps one reference, moves it down, and stops at a match or at `null`. A reference that reaches `null` means the key is absent.

#### Inserting At The End Of The Search Path

An insert starts with the same search for the new key. The search ends at a `null` child, and that empty slot is the **insertion point**. Every node on the path agreed that the key belongs below it on that side, so the slot is the only place that keeps the tree valid. The method creates a node and writes it into that slot. No existing node moves, and every key that was findable before stays findable.

#### Deleting A Node In Three Cases

A delete searches for the key and then repairs the slot of the removed node. A leaf leaves behind a `null`. A node with one child is replaced by that child, whose subtree already fits the slot. A node with two children cannot be replaced by either child alone. The method copies the smallest key of the right subtree into the node and then deletes that smallest node from the right subtree, which has at most one child. The copied key is larger than every left key and no larger than any other right key.

<!-- names: discarded subtree, search path, insertion point -->

<!-- stage: variables -->
### The State Of One Search

- **node** is the node under comparison, and it starts at the root.
- **key** is the value the method looks for or inserts.
- **parent** is the last node visited before `node`, and it is the owner of the empty slot when `node` becomes `null`.
- **side** records whether the last move went left or right, so the insert writes to the correct child field.

<!-- stage: trace -->
### One Branch Per Comparison

Each cell is a key listed from the top level down, and the pointer `node` marks the node under comparison.

#### Searching For A Key That Exists

The tree has the root 20, the children 10 and 30, and four more nodes below them. The search looks for the key 25.

```trace
{"cells":[20,10,30,5,15,25,35],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"key":25},"note":"The key 25 is larger than 20, so the search goes right and drops the other subtree."},{"at":{"node":2},"vars":{"key":25},"note":"The key 25 is smaller than 30, so the search goes left and drops the other subtree."},{"at":{"node":5},"vars":{"key":25},"note":"The key 25 equals the node key 25, so the search stops with a match."}]}
```

The search visits 3 nodes out of 7, and it never looks at the left subtree of the root.

#### Inserting At The Empty Slot

The same tree gets the new key 12. The last cell, 12, holds the new node and is not part of the tree until the final step.

```trace
{"cells":[20,10,30,5,15,25,35,12],"pointers":["node"],"steps":[{"at":{"node":0},"vars":{"key":12},"note":"The key 12 is smaller than 20, so the walk goes left."},{"at":{"node":1},"vars":{"key":12},"note":"The key 12 is larger than 10, so the walk goes right."},{"at":{"node":4},"vars":{"key":12},"note":"The key 12 is smaller than 15, and the left slot is empty, so this slot is the insertion point."},{"at":{"node":7},"vars":{"key":12},"note":"The method writes the new node 12 into the empty left slot of the node 15."}]}
```

The walk ends at an empty left slot of the node 15, because 12 is smaller than 15. The method writes the new node there, and the key 12 is reachable by the same three comparisons.

<!-- stage: code -->
### Search And Insert In Code

```java
final class OnePath {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode search(TreeNode root, int key) {
        TreeNode node = root;
        while (node != null && node.val != key) {         // stop at a match or at an empty slot
            node = key < node.val ? node.left : node.right;   // take one branch, drop the other
        }
        return node;                                      // the matching node, or null when absent
    }

    static TreeNode insert(TreeNode root, int key) {
        if (root == null) return new TreeNode(key);       // the empty tree gets its first node
        TreeNode node = root;
        while (true) {
            if (key < node.val) {
                if (node.left == null) { node.left = new TreeNode(key); break; }    // the empty left slot
                node = node.left;
            } else {
                if (node.right == null) { node.right = new TreeNode(key); break; }  // the empty right slot
                node = node.right;
            }
        }
        return root;                                      // the root never changes after the first insert
    }
}
```

The loops use no recursion, so a chain of 100000 nodes needs no deep call stack.

- **Time** is O(h) for both methods, because each step moves one level down.
- **Space** is O(1), because the methods keep one reference and no stack.

<!-- stage: applicability -->
### Using The One-Path Rule

#### Recognizing The Cue

Use one path when a question concerns a single key and the tree is a search tree. Words such as "find the node with this value", "add this value" and "remove this value" fit. The ordering must hold for the whole tree, so first confirm the contract says the input is a valid search tree.

#### Stating The Invariant

The invariant is that, if the key exists under the contract, it lies inside the subtree of the current node. A comparison moves to the child whose subtree can hold the key, so the invariant survives each step. A `null` reference means the subtree is empty, and the key is absent.

#### Avoiding The False Friend

The false friend is the validation task of the previous lesson. A search needs one path because the contract already guarantees the ordering. A validation must check the ordering of every node, so it needs the bounds of every node and visits the whole tree. Equal keys need a stated rule, because a search that moves right on equality never reaches a duplicate that was placed on the left.

<!-- stage: exercises -->
### Exercises

#### [Build] Search in a Binary Search Tree (LeetCode 700)
<!-- id: tb-bst-search -->

**Prerequisites.** The comparison rule from this lesson.

**Problem.** Given the root of a binary search tree and an integer `val`, return the node whose key equals `val`, or `null` if no such node exists. The returned node roots the subtree that contains it. Take exactly one branch at each node.

**Constraints.** The limits are:
- **Nodes** number between 1 and 5000.
- **Values** satisfy `1 <= val <= 10^7`, and all keys in the tree are distinct.
- **Answer** is a node reference or `null`.
- **Mutation** does not occur.

**Example 1.** Input root 4 with children 2 and 7, where 2 has children 1 and 3, and `val = 2`, output the node 2 with its subtree `2, 1, 3`.

**Example 2.** Input the same tree and `val = 5`, output `null`.

**Hint.** Which side of a node can hold a key smaller than the node key? What does the loop hold when the key is absent?

**Changed decision.** One comparison picks one child, and the other child is never visited.

#### [Vary] Insert into a Binary Search Tree (LeetCode 701)
<!-- id: tb-bst-insert -->

**Prerequisites.** The exercise above.

**Problem.** Given the root of a binary search tree and a value `val` that is not already in the tree, insert a node with the key `val` and return the root. Any result that is a valid search tree and contains all old keys plus `val` is accepted. The method must add a leaf and move no existing node.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `-10^8 <= val <= 10^8`, and the new value differs from every key in the tree.
- **Answer** is the root, which is the new node when the tree was empty.
- **Mutation** adds exactly one node.

**Example 1.** Input root 4 with children 2 and 7, where 2 has children 1 and 3, and `val = 5`, output a tree where 5 is the left child of 7.

**Example 2.** Input an empty tree and `val = 5`, output a single node 5.

**Hint.** Where does the walk stop? Which child field of the last node receives the new node?

**Changed decision.** The walk ends at an empty slot, and the method writes into it.

#### [Boundary] Duplicate-Key Policy (Author exercise)
<!-- id: tb-bst-duplicate-policy -->

**Prerequisites.** The two exercises above.

**Problem.** Each node holds a key and a count of how many times the key was inserted. Given the root of such a tree and a key, insert the key under the count policy: an existing key increases its node's count by 1, and a new key adds a node with count 1. Return the count of the key after the insert. The tree is built only by this operation.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys in the tree are distinct.
- **Counts** are positive and fit in an `int`.
- **Answer** is an `int` of at least 1.
- **Mutation** changes one count or adds one node, and the root changes only for an empty tree.

**Example 1.** Input a tree where the key 5 has count 2, and the key 5, output 3.

**Example 2.** Input an empty tree and the key 5, output 1, and the tree holds one node.

**Hint.** What does the loop do when the keys are equal? Where would a duplicate node have to go if the tree stored one node per insert?

**Changed decision.** An equal key ends the walk by updating a count and does not add a node.

#### [Recognize] Delete Node in a BST (LeetCode 450)
<!-- id: tb-bst-delete -->

**Prerequisites.** All three exercises above.

**Problem.** A binary search tree is stored by its root, and a key is supplied. Remove the node with that key if it exists, and return the root of the resulting tree. A leaf is removed, a node with one child is replaced by that child, and a node with two children takes the smallest key of its right subtree, after which that smallest node is removed from the right subtree.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** satisfy `-10^5 <= val <= 10^5`, and all keys are distinct.
- **Answer** is the new root, which may be `null`.
- **Mutation** rewires child references of the tree.

**Example 1.** Input root 5 with children 3 and 6, where 3 has children 2 and 4 and 6 has a right child 7, and key 3, output a tree with root 5, left child 4 holding the left child 2, and the unchanged right side.

**Example 2.** Input the same tree and key 0, output the unchanged tree.

**Hint.** Which node owns the slot of the removed node? How many children can the smallest node of the right subtree have?

**Changed decision.** A delete needs three cases for the removed node, and the two-child case moves one key.
