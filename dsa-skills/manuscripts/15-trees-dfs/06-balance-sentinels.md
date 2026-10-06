<!-- lesson-kind: standard -->
<!-- lesson-id: balance-sentinels -->
## Check Balance In One Pass

<!-- stage: context -->
### Validating An Index That Must Stay Balanced

A database index is stored as a binary tree. The index stays fast only while the tree is balanced, which means that at every node the heights of the left and right subtrees differ by at most one. After a crash, a validator must confirm that the rule still holds at every node of a recovered index with 200,000 entries. The first validator measures heights again and again. It also keeps measuring after it has already found a node that breaks the rule.

The task has two parts that seem separate. The validator needs the height of each subtree, and it needs a yes or no answer for the whole tree. The question is how one pass can produce both, and how a failure deep in the tree can stop the work above it.

<!-- stage: naive -->
### Measuring Heights At Every Node

The first validator checks the rule at the current node with a separate height method. Then it asks the same question of the left subtree and of the right subtree.

```java
final class TopDownBalance {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static int height(Node node) {
        if (node == null) return 0;                              // an empty subtree has height 0
        return 1 + Math.max(height(node.left), height(node.right));
    }

    static boolean isBalanced(Node node) {
        if (node == null) return true;                           // an empty subtree satisfies the rule
        int diff = Math.abs(height(node.left) - height(node.right));   // measure both sides from scratch
        return diff <= 1 && isBalanced(node.left) && isBalanced(node.right);
    }
}
```

Take a root 5 with the leaf children 3 and 8. The method returns `true`. Take a root 1 whose left child 2 has a left child 3. The root has sides of height 2 and 0, so the method returns `false`.

<!-- stage: bottleneck -->
### Counting The Repeated Height Calls

```predict
The tree is a perfect binary tree of height k with n = 2^k - 1 nodes, and every node satisfies the rule. How many times does height visit a node on the bottom level, and what is the total number of visits for the whole tree?

A node on the bottom level has k - 1 ancestors above it, and every ancestor measures it once, so it is visited k - 1 times. The total is about n times k, which is O(n log n).
```

The method measures a subtree once for every ancestor of its nodes. For a balanced tree the depth is about log n, so the total cost is O(n log n) and not O(n). A second problem is that the method keeps no memory of the heights it already measured. Each call to `isBalanced` starts the measuring again.

The method also does not stop early in a useful way. The first violation is found only after the calls above it have finished their own measuring. A node that already knows that its left subtree fails does not need the height of its right subtree at all. The height of a subtree and the answer about its balance can come out of the same call.

<!-- stage: insight -->
### Returning A Height Or A Failure Marker

One call can report a height for a subtree that passes the rule and a marker for a subtree that fails. Heights are never negative, so a negative number is free to carry the failure.

<!-- names: sentinel, early exit, valid height -->

#### One Return Value Carries Two Meanings

A **sentinel** is a reserved return value that cannot be a real answer. In this method the sentinel is `-1`, because a real height is 0 or more. A call returns a **valid height** when its whole subtree satisfies the rule, which is a number from 0 upward. A call returns the sentinel when any node in its subtree breaks the rule. The caller learns both facts from one number.

#### The Order Of The Three Checks

A call on a node performs three checks in a fixed order. First it calls itself on the left child, and if the result is the sentinel, the call returns the sentinel at once. Then it does the same for the right child. Only when both results are valid heights does it compare them. If their difference is more than one, the call returns the sentinel. Otherwise it returns one plus the larger height.

#### Failure Skips The Remaining Work

The **early exit** is the immediate return of the sentinel. Once a child fails, the node above it fails too, because its subtree contains a node that breaks the rule. The call does not visit the right side and does not compare any heights. Each node is visited at most once, so the whole check costs O(n) time. The root's result answers the question: the tree is balanced exactly when the result is not the sentinel.

<!-- stage: variables -->
### The Values That A Call Handles

- **l** and **r** hold the results of the two child calls, and each is a valid height or the sentinel.
- **sentinel** is `-1`, which no valid height can equal.
- **diff** is the absolute difference of two valid heights, and it exists only after both checks pass.
- **result** is the sentinel or the height of the node, which is one plus the larger child height.

The comparison of `l` and `r` must never run on a sentinel. The value `-1` would act like a real height and could hide a failure.

<!-- stage: trace -->
### Following Heights And Failures Upward

#### A Tree That Passes

The tree has root 5. Its left child is 3, which has a left child 1. Its right child is 8, which has children 7 and 9. A step shows a call that finishes. The variable `result` is the value that the call returns.

```trace
{"cells":["5","3","8","1","null","7","9"],"pointers":["node"],"steps":[{"at":{"node":3},"vars":{"result":1},"note":"The node 1 has sides of height 0 and 0. The difference 0 is allowed, so the call returns 1."},{"at":{"node":1},"vars":{"result":2},"note":"The node 3 has sides of height 1 and 0. The difference 1 is allowed, so the call returns 2."},{"at":{"node":5},"vars":{"result":1},"note":"The node 7 has sides of height 0 and 0. The difference 0 is allowed, so the call returns 1."},{"at":{"node":6},"vars":{"result":1},"note":"The node 9 has sides of height 0 and 0. The difference 0 is allowed, so the call returns 1."},{"at":{"node":2},"vars":{"result":2},"note":"The node 8 has sides of height 1 and 1. The difference 0 is allowed, so the call returns 2."},{"at":{"node":0},"vars":{"result":3},"note":"The node 5 has sides of height 2 and 2. The difference 0 is allowed, so the call returns 3."}]}
```

Every call returns a valid height. The node 3 has sides of height 1 and 0, and the difference 1 is allowed. The root has two sides of height 2, so the result is 3.

#### A Failure That Stops The Walk

The second tree has root 6 with children 4 and 8. The node 4 has a left child 2, and the node 2 has a left child 1. The right subtree of the root is the single node 8.

```trace
{"cells":["6","4","8","2","null","null","null","1"],"pointers":["node"],"steps":[{"at":{"node":7},"vars":{"result":1},"note":"The node 1 has sides of height 0 and 0. The difference 0 is allowed, so the call returns 1."},{"at":{"node":3},"vars":{"result":2},"note":"The node 2 has sides of height 1 and 0. The difference 1 is allowed, so the call returns 2."},{"at":{"node":1},"vars":{"result":-1},"note":"The node 4 has sides of height 2 and 0. The difference 2 is more than 1, so the call returns -1."},{"at":{"node":0},"vars":{"result":-1},"note":"The left call of the node 6 returned -1, so the call returns -1 at once. The right side is not visited."}]}
```

The node 4 has a left side of height 2 and no right side, so the difference is 2 and the call returns the sentinel. The root receives the sentinel from its left call and returns it at once. The node 8 is never visited.

<!-- stage: code -->
### The One-Pass Check In Code

```java
final class OnePassBalance {
    static final class Node {
        int val;
        Node left, right;
        Node(int val, Node left, Node right) { this.val = val; this.left = left; this.right = right; }
    }

    static final int FAIL = -1;                                  // heights are never negative

    static int checkedHeight(Node node) {
        if (node == null) return 0;                              // an empty subtree is valid with height 0
        int l = checkedHeight(node.left);
        if (l == FAIL) return FAIL;                              // a failed left side ends this call
        int r = checkedHeight(node.right);
        if (r == FAIL) return FAIL;                              // a failed right side ends this call
        if (Math.abs(l - r) > 1) return FAIL;                    // both heights are valid, so compare them
        return 1 + Math.max(l, r);                               // the valid height of this subtree
    }

    static boolean isBalanced(Node root) {
        return checkedHeight(root) != FAIL;                      // any valid height means that every node passed
    }
}
```

The two checks against `FAIL` come before the comparison. Without them, a left result of `-1` and a right result of 0 would give a difference of 1 and the call would report a valid height.

- **Time** is O(n), because each node receives at most one call and does constant work.
- **Space** is O(h) in the stack of pending calls, because the early exit never opens more calls than the height.

<!-- stage: applicability -->
### Using A Reserved Return Value

#### Stating What The Return Value Promises

The invariant is that a call returns the exact height of its subtree when every node in it passes the rule, and the sentinel otherwise. Write down the sentinel and the range of real values before coding. The sentinel must lie outside that range.

#### Finding The False Friend

Calling `height` at every node looks harmless, because each call is correct, and it is the false friend of this lesson. The answer is right and the cost grows to O(n log n) or more, because each node is measured once per ancestor. A second false friend is a sentinel that overlaps a real value. If heights count edges, the empty tree has height -1, and `-1` can no longer serve as the failure marker.

#### No-Go Conditions

The sentinel idea works only when the failure of one subtree decides the answer of every ancestor. If the problem asks for the number of failing nodes, a failure cannot stop the walk, and each call must return a count and a height together. If every return value is a legal answer, such as a sum of signed numbers, no spare value exists, and the call needs a separate flag.

<!-- stage: exercises -->
### Exercises

#### [Build] Height Or Failure (Author exercise)
<!-- id: bs-height-or-fail -->

**Prerequisites.** The sentinel and the early exit from this lesson.

**Problem.** A tree is clean when no node holds a negative value. Write a method that returns the height of a clean tree, counted in nodes, and returns `-1` for a tree with a negative value anywhere. A call that receives `-1` from its left child must return `-1` without visiting the right child.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers between -100 and 100.
- **Answer** is the height of a clean tree, or `-1`.
- **Mutation** is not allowed.

**Example 1.** Input root 4 with left child 2 and right child 7, where node 7 has a right child 9, output 3.

**Example 2.** Input root 4 with left child -2 and right child 7, output -1.

**Hint.** What does the call return for an empty subtree? When does the call stop before it reads the right child?

**Changed decision.** The return value carries a height or a failure, and the failure ends the call.

#### [Vary] Detect Local Imbalance (Author exercise)
<!-- id: bs-first-bad -->

**Prerequisites.** The exercise above.

**Problem.** Given a binary tree, return the value of the first node whose left and right subtree heights differ by more than one. First means first in the order in which the calls finish. Return `-1` when no node breaks the rule. A node compares its two heights only after both child calls returned valid heights, and a failure above the first one must not hide it.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers between 0 and 1000.
- **Answer** is a node value, or `-1`.
- **Mutation** is not allowed.

**Example 1.** Input root 6 with left child 4 and right child 8, where node 4 has a left child 2 that has a left child 1, output 4.

**Example 2.** Input root 5 with left child 3 and right child 8, output -1.

**Hint.** Which node is the first to finish with a bad comparison? Where do you store its value so the callers above can return the sentinel?

**Changed decision.** The call compares heights only after both child results are valid, and the answer stores the first failing node.

#### [Boundary] Empty Tree Height (Author exercise)
<!-- id: bs-empty-height -->

**Prerequisites.** The two exercises above.

**Problem.** Write a balance check for a binary tree in which the height is counted in edges. The empty tree has height -1 and a single node has height 0. Choose a failure marker that no real height can equal. Return `true` when every node has sides whose heights differ by at most one.

**Constraints.** The limits are:
- **Nodes** number between 0 and 10^4.
- **Values** are integers that the answer does not use.
- **Heights** are integers from -1 upward.
- **Answer** is a `boolean`, and the empty tree gives `true`.

**Example 1.** Input `root = null`, output `true`.

**Example 2.** Input root 1 with left child 2 that has a left child 3, output `false`.

**Hint.** Which numbers can a real height take now? Which value is free for the failure marker?

**Changed decision.** The base height changes to -1, so the failure marker moves to a value below it.

#### [Recognize] Balanced Binary Tree (LeetCode 110)
<!-- id: bs-balanced -->

**Prerequisites.** All three exercises above.

**Problem.** A binary tree is height-balanced when at every node the heights of its two subtrees differ by at most one. Given a binary tree, return `true` if it is height-balanced. The method must make one pass and may not call a separate height method at each node.

**Constraints.** The limits are:
- **Nodes** number between 0 and 5000.
- **Values** are integers between -10^4 and 10^4.
- **Answer** is a `boolean`, and the empty tree gives `true`.
- **Mutation** is not allowed.

**Example 1.** Input root 5 with left child 3 that has a left child 1, and right child 8 that has children 7 and 9, output `true`.

**Example 2.** Input root 6 with children 4 and 8, where node 4 has a left child 2 with a left child 1, output `false`.

**Hint.** What single number can a call return to tell the parent both the height and the failure? When must the comparison be skipped?

**Changed decision.** One postorder pass merges the height and the verdict in one return value.
