<!-- lesson-kind: standard -->
<!-- lesson-id: successor-and-predecessor -->
## Find The Next And Previous Key

<!-- stage: context -->
### Why Next Ticket Takes Seconds

A help desk stores ticket numbers in a binary search tree. The screen has a "next ticket" button, and an agent clicks it dozens of times an hour. The first version of the button gathers every ticket number into a list, sorts out their order, and picks the number after the current one. With a million tickets, each click waits for a million numbers to be collected, even though the answer is usually a few steps away from the current ticket.

The **successor** of a key is the smallest key in the tree that is larger than it, and the **predecessor** is the largest key that is smaller. This lesson asks where the successor sits relative to the current node, and how a program finds it without looking at the rest of the tree.

<!-- stage: naive -->
### Collecting The Keys Into A List

The direct plan walks the whole tree in sorted order, stores the keys in a list, and scans the list for the first key that is larger than the target.

```java
final class SuccessorByList {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static void fill(TreeNode node, List<Integer> keys) {
        if (node == null) return;
        fill(node.left, keys);               // smaller keys first
        keys.add(node.val);                  // this key follows every key on its left
        fill(node.right, keys);              // larger keys last
    }

    static Integer successor(TreeNode root, int key) {
        List<Integer> keys = new ArrayList<>();
        fill(root, keys);
        for (int k : keys) if (k > key) return k;   // the first larger key in sorted order
        return null;                                // no key is larger than the target
    }
}
```

On the tree with the root 5, the children 3 and 8, and more nodes below them, the sorted list is `2, 3, 4, 5, 6, 7, 8, 9`, and the successor of 7 is 8. The result is correct.

<!-- stage: bottleneck -->
### Counting The Work Per Click

```predict
The tree is balanced and holds one million keys, and the current key is the root. What is the least number of nodes a method must look at to find the successor, and what does the list method look at?

The successor of the root lies at the bottom of the right side, so a method that follows the tree edges looks at about 20 nodes. The list method looks at all one million nodes and also stores them.
```

The list method costs O(n) time and O(n) space on every click. Most of that work is wasted, because the successor is close to the current key in the tree's own shape: it is somewhere on a single path from the root. The method needs a rule that follows that path and remembers the one node that can still become the answer.

<!-- stage: insight -->
### Remember The Last Larger Node

Start at the root and compare the key with each node. A node larger than the key is a **candidate** for the successor, because it is larger and it may be the smallest larger key. After recording it, the search must look for something smaller that is still larger than the key, so it goes left. A node that is not larger than the key cannot be the answer, and neither can anything in its left subtree, so the search goes right. Each later candidate is smaller than the one before, because the search only moves to nodes below a candidate on its left. The last recorded candidate is the answer.

#### Two Cases Hide In One Loop

When the key has a right subtree, the loop goes right from the key and then keeps going left, because each node below is larger. The answer is the leftmost node of that right subtree. When the key has no right subtree, the loop ends below the key and the answer is a candidate that was recorded earlier on the path. That candidate is the nearest ancestor from which the path took a **left turn**, which means it moved into the left child of that ancestor. A parent is the successor only when the key is its left child with no right subtree.

#### Reversing Every Comparison For The Predecessor

The predecessor follows the same rule in **mirror** form. A node smaller than the key becomes the candidate, and the search goes right. A node not smaller than the key sends the search left. The last candidate is the predecessor, and a missing candidate means no smaller key exists.

<!-- names: candidate, left turn, mirror -->

<!-- stage: variables -->
### The State Of The Descent

- **node** is the node under comparison, starting at the root.
- **key** is the value whose neighbor the method seeks.
- **best** is the smallest node larger than the key seen so far, and it is `null` until a larger node appears.
- **answer** is `best` when the loop ends, because the loop visits every node that could improve it.

<!-- stage: trace -->
### Candidates Along One Path

The cells list the keys row by row from the root. The pointers are `node` for the node under comparison and `best` for the recorded candidate, with -1 meaning none.

#### Finding The Next Key Of A Leaf

The tree has the root 5, the children 3 and 8, the children 2 and 4 under the node 3, and the children 6 and 9 under the node 8, with the node 7 below the node 6. The method looks for the successor of 7.

```trace
{"cells":[5,3,8,2,4,6,9,7],"pointers":["node","best"],"steps":[{"at":{"node":0,"best":-1},"vars":{"key":7},"note":"5 is not larger than 7, so it and its left side are skipped and the search goes right."},{"at":{"node":2,"best":2},"vars":{"key":7},"note":"8 is larger than 7, so it becomes the candidate and the search goes left."},{"at":{"node":5,"best":2},"vars":{"key":7},"note":"6 is not larger than 7, so it and its left side are skipped and the search goes right."},{"at":{"node":7,"best":2},"vars":{"key":7},"note":"7 is not larger than 7, so it and its left side are skipped and the search goes right."},{"at":{"node":-1,"best":2},"vars":{"key":7},"note":"The search reaches an empty slot, so the answer is the last candidate, 8."}]}
```

The last candidate is 8, which is the nearest ancestor of 7 where the path turned left.

#### Finding The Next Key With A Right Subtree

The same tree gives the successor of 5, and the node 5 has a right subtree.

```trace
{"cells":[5,3,8,2,4,6,9,7],"pointers":["node","best"],"steps":[{"at":{"node":0,"best":-1},"vars":{"key":5},"note":"5 is not larger than 5, so it and its left side are skipped and the search goes right."},{"at":{"node":2,"best":2},"vars":{"key":5},"note":"8 is larger than 5, so it becomes the candidate and the search goes left."},{"at":{"node":5,"best":5},"vars":{"key":5},"note":"6 is larger than 5, so it becomes the candidate and the search goes left."},{"at":{"node":-1,"best":5},"vars":{"key":5},"note":"The search reaches an empty slot, so the answer is the last candidate, 6."}]}
```

The loop turns right at the root and then walks left. The last candidate is 6, the leftmost node of the right subtree of 5.

<!-- stage: code -->
### Successor And Predecessor In Code

```java
final class Neighbors {
    static final class TreeNode {
        int val;
        TreeNode left, right;
        TreeNode(int val) { this.val = val; }
    }

    static TreeNode successor(TreeNode root, int key) {
        TreeNode best = null;
        TreeNode node = root;
        while (node != null) {
            if (node.val > key) { best = node; node = node.left; }   // a larger node is a candidate; look for a smaller one
            else node = node.right;                                    // this node and its left side are too small
        }
        return best;                                                   // null when no key is larger
    }

    static TreeNode predecessor(TreeNode root, int key) {
        TreeNode best = null;
        TreeNode node = root;
        while (node != null) {
            if (node.val < key) { best = node; node = node.right; }  // a smaller node is a candidate; look for a larger one
            else node = node.left;                                     // this node and its right side are too large
        }
        return best;                                                   // null when no key is smaller
    }
}
```

Both methods compare against the key, so they work for a key that is not in the tree. They store one reference and make no recursive calls.

- **Time** is O(h), because each step moves one level down.
- **Space** is O(1), because the loop keeps two references.

<!-- stage: applicability -->
### Using The Candidate Rule

#### Recognizing The Cue

Use the candidate rule when a question asks for the next or previous key in sorted order, for the smallest key above a threshold, or for the largest key below one. The tree must be a search tree, and no parent pointers are needed because the search starts at the root.

#### Stating The Invariant

The invariant is that the answer is either the current best candidate or a node in the subtree of the current node. A larger node moves the search left and becomes the new best candidate. A node that is too small discards itself and its left subtree. The loop ends at `null` with every possible improvement checked.

#### Avoiding The False Friend

The false friend is the parent. For the key 7 in the example tree, the parent is 6, which is smaller, and the successor is 8, two levels up. Another trap is a missing neighbor. The largest key has no successor, and the smallest key has no predecessor, and the method must return `null` for them and not a default number.

<!-- stage: exercises -->
### Exercises

#### [Build] Minimum Of Right Subtree (Author exercise)
<!-- id: tb-succ-right-min -->

**Prerequisites.** The leftmost walk from this lesson.

**Problem.** Given a node of a binary search tree that has a right child, return the node with the smallest key in its right subtree. Start at the right child and follow left links until a node has no left child.

**Constraints.** The limits are:
- **Nodes** number between 2 and 10^4, and all keys are distinct.
- **Input** is a node with a non-null right child.
- **Answer** is a node reference in the right subtree.
- **Mutation** does not occur.

**Example 1.** Input the node 5 in the tree with the root 5, the children 3 and 8, the children 2 and 4 under 3, and the children 6 and 9 under 8, with the node 7 as the right child of 6, output the node 6.

**Example 2.** Input the node 3 in the same tree, output the node 4.

**Hint.** Where does the walk start? What stops the walk?

**Changed decision.** The walk starts below the node and goes left only.

#### [Vary] Successor Without Parent Links (Author exercise)
<!-- id: tb-succ-no-parent -->

**Prerequisites.** The exercise above.

**Problem.** A binary search tree and an integer `key` are supplied. Return the smallest key in the tree that is strictly greater than `key`, or `null` if no key is greater. The key does not have to appear in the tree. Remember the last node larger than the key during the walk from the root.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^9 <= val <= 10^9`, and `key` has the same range.
- **Answer** is an `Integer` or `null`.
- **Mutation** does not occur.

**Example 1.** Input the tree above and `key = 7`, output 8.

**Example 2.** Input the same tree and `key = 1`, output 2.

**Hint.** Which direction does the search take after it records a larger node? Which node holds the answer when the loop ends?

**Changed decision.** The method uses recorded ancestors and not links to parents.

#### [Boundary] Maximum And Minimum Keys (Author exercise)
<!-- id: tb-succ-extremes -->

**Prerequisites.** The two exercises above.

**Problem.** For a binary search tree and an integer `key`, return a two-element array holding the predecessor and the successor of the key. The predecessor is the largest key strictly smaller than `key`, and the successor is the smallest key strictly larger. Use `null` for a neighbor that does not exist.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^9 <= val <= 10^9`.
- **Answer** is an `Integer[]` of length 2.
- **Mutation** does not occur.

**Example 1.** Input the tree above and the smallest key `2`, output `[null, 3]`.

**Example 2.** Input the same tree and the largest key `9`, output `[8, null]`.

**Hint.** What does each loop hold when no node passes its test? Which result means no neighbor?

**Changed decision.** Two mirrored loops run, and an unset candidate becomes `null`.

#### [Recognize] Inorder Successor in BST (LeetCode 285)
<!-- id: tb-succ-inorder -->

**Prerequisites.** All three exercises above.

**Problem.** The input is a search tree with distinct keys and a node `p` that belongs to the tree, return the node that follows `p` in sorted order, or `null` if `p` holds the largest key. The result may be the leftmost node of the right subtree of `p`, or the nearest ancestor from which the search path turned left.

**Constraints.** The limits are:
- **Nodes** number between 1 and 10^4, and all keys are distinct.
- **Values** satisfy `-10^5 <= val <= 10^5`.
- **Answer** is a node reference or `null`.
- **Mutation** does not occur.

**Example 1.** Input the tree above and `p` holding 4, output the node 5, because 4 has no right subtree.

**Example 2.** Input the same tree and `p` holding 9, output `null`.

**Hint.** Which case does a right subtree of `p` select? What does the plain descent by key do in both cases?

**Changed decision.** Both successor cases come from one descent by key.
